"""
garmin_sync.py
==============
Garmin watch integration (via the community `garminconnect` library —
the same unofficial-but-battle-tested route most hobby dashboards use).

What syncs, per day:
- daily steps            -> Recovery Tracker (steps)
- sleep hours            -> Recovery Tracker (sleep), when the watch has it
- recorded activities    -> Cardio log, with the watch's REAL duration and
                            calories (runs, rides, football, …)

Privacy model: the password is used once to log in and is NOT stored.
Only the resulting Garmin session tokens (valid ~1 year) are kept in the
app's local database, plus the e-mail for display. "Disconnect" wipes both.

MFA (two-factor) accounts: the first connect attempt reports that a code
is needed; the user enters the code Garmin sent and connects again.
"""

import json
from datetime import date, timedelta

import database as db

try:
    from garminconnect import (
        Garmin,
        GarminConnectAuthenticationError,
        GarminConnectConnectionError,
        GarminConnectTooManyRequestsError,
    )
    GARMIN_AVAILABLE = True
except Exception:                                    # library missing
    GARMIN_AVAILABLE = False


# ---------------------------------------------------------------------
# Connection state
# ---------------------------------------------------------------------
def is_connected() -> bool:
    return bool(db.get_setting("garmin_tokens"))


def connected_email() -> str:
    return db.get_setting("garmin_email", "")


def disconnect():
    db.set_setting("garmin_tokens", "")
    db.set_setting("garmin_email", "")
    db.set_setting("garmin_seen_ids", "[]")


def connect(email: str, password: str, mfa_code: str = "") -> dict:
    """Log in to Garmin Connect. Returns {ok, needs_mfa, error, name}."""
    if not GARMIN_AVAILABLE:
        return {"ok": False, "error": "library-missing"}
    try:
        if mfa_code.strip():
            garmin = Garmin(email=email, password=password,
                            prompt_mfa=lambda: mfa_code.strip())
            garmin.login()
        else:
            garmin = Garmin(email=email, password=password,
                            return_on_mfa=True)
            status, _state = garmin.login()
            if status == "needs_mfa":
                return {"ok": False, "needs_mfa": True}
        tokens = garmin.client.dumps()
        db.set_setting("garmin_tokens", tokens)
        db.set_setting("garmin_email", email)
        name = getattr(garmin, "full_name", None) or email
        return {"ok": True, "name": name}
    except GarminConnectAuthenticationError:
        return {"ok": False, "error": "auth"}
    except GarminConnectTooManyRequestsError:
        return {"ok": False, "error": "rate"}
    except GarminConnectConnectionError:
        return {"ok": False, "error": "network"}
    except Exception as e:                            # noqa: BLE001
        msg = str(e)
        if "password" in msg.lower() or "credentials" in msg.lower():
            return {"ok": False, "error": "auth"}
        if "proxy" in msg.lower() or "connect" in msg.lower():
            return {"ok": False, "error": "network"}
        return {"ok": False, "error": msg[:200]}


def _client():
    """Session from stored tokens (None if missing/expired)."""
    tokens = db.get_setting("garmin_tokens")
    if not tokens or not GARMIN_AVAILABLE:
        return None
    try:
        garmin = Garmin()
        garmin.login(tokens)
        return garmin
    except Exception:                                 # noqa: BLE001
        return None


# ---------------------------------------------------------------------
# Sync
# ---------------------------------------------------------------------
def _merge_recovery(day_iso: str, steps=None, sleep_h=None):
    """Update only the synced fields; keep everything the user typed."""
    prev = db.get_recovery(day_iso) or {}
    db.upsert_recovery(
        day_iso,
        sleep_hours=sleep_h if sleep_h else prev.get("sleep_hours"),
        water_l=prev.get("water_l"),
        protein_g=prev.get("protein_g"),
        steps=steps if steps else prev.get("steps"),
        soreness=prev.get("soreness"),
        energy=prev.get("energy"),
        recovery_score=prev.get("recovery_score"),
        football_rating=prev.get("football_rating"),
        notes=prev.get("notes"),
    )


def sync(days_back: int = 7) -> dict:
    """Pull recent Garmin data. Returns a report dict."""
    garmin = _client()
    if garmin is None:
        return {"ok": False, "error": "not-connected"}

    report = {"ok": True, "days_steps": 0, "days_sleep": 0,
              "activities": 0, "errors": 0}
    today = date.today()

    # ---- daily steps + sleep ----
    for i in range(days_back):
        d = today - timedelta(days=i)
        d_iso = d.isoformat()
        steps = sleep_h = None
        try:
            stats = garmin.get_stats(d_iso) or {}
            steps = stats.get("totalSteps")
        except Exception:                             # noqa: BLE001
            report["errors"] += 1
        try:
            sleep = garmin.get_sleep_data(d_iso) or {}
            secs = (sleep.get("dailySleepDTO") or {}).get("sleepTimeSeconds")
            if secs:
                sleep_h = round(secs / 3600, 1)
        except Exception:                             # noqa: BLE001
            pass
        if steps or sleep_h:
            _merge_recovery(d_iso, steps=steps, sleep_h=sleep_h)
            report["days_steps"] += 1 if steps else 0
            report["days_sleep"] += 1 if sleep_h else 0

    # ---- activities -> cardio log (deduped by Garmin activityId) ----
    try:
        seen = set(json.loads(db.get_setting("garmin_seen_ids", "[]")))
    except Exception:                                 # noqa: BLE001
        seen = set()
    try:
        start = (today - timedelta(days=days_back)).isoformat()
        acts = garmin.get_activities_by_date(start, today.isoformat()) or []
        for a in acts:
            aid = str(a.get("activityId"))
            if aid in seen:
                continue
            mins = round((a.get("duration") or 0) / 60)
            if mins < 3:
                continue
            name = (a.get("activityName")
                    or (a.get("activityType") or {}).get("typeKey", "Activity"))
            kcal = round(a.get("calories") or 0)
            day_iso = str(a.get("startTimeLocal", today.isoformat()))[:10]
            db.add_cardio(day_iso, f"⌚ {name}", mins, kcal)
            seen.add(aid)
            report["activities"] += 1
        db.set_setting("garmin_seen_ids",
                       json.dumps(sorted(seen)[-500:]))
    except Exception:                                 # noqa: BLE001
        report["errors"] += 1

    return report
