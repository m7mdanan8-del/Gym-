"""
garmin.py
=========
Garmin platform: sync, analysis, and recommendations.

Sync — two routes, so the app NEVER depends on a fragile dependency:

1. **File upload (always available, works on Streamlit Cloud).**
   Drop any of these from Garmin Connect and they are parsed and stored:
   - the *Activities* CSV export (connect.garmin.com → Activities → Export CSV)
   - individual activity files: .fit (needs `fitdecode`), .tcx, .gpx
   - the full account-data export ZIP (steps / sleep / resting HR / stress /
     body battery are extracted from the wellness JSON files inside)
2. **Live sync (optional).** If the community `garminconnect` library is
   installed locally (`pip install garminconnect`), the Settings-style
   connect + pull flow lights up. The import is lazy and guarded, so a
   missing or broken library can never take the app down — this is exactly
   what broke the previous integration on Streamlit Cloud.

Analysis — everything is computed from the two SQLite tables
(`garmin_activities`, `garmin_daily`):
   - daily training load (TRIMP-like: minutes × heart-rate-reserve fraction,
     with per-sport fallback intensities when no HR was recorded)
   - ACWR (acute 7-day : chronic 28-day workload ratio) — the standard
     load-spike metric used in ACL re-injury prevention
   - weekly volume, intensity distribution, sleep / steps / RHR trends

Recommendations — rule-based, bilingual, tuned to this user's context
(partial ACL tear + shoulder rehab, football on Saturdays).
"""

import io
import json
import math
import re
import zipfile
from datetime import date, datetime, timedelta

import pandas as pd

import database as db
from translations import tr

# ---------------------------------------------------------------------
# Profile-derived heart-rate model (age 34 → HRmax ≈ 186)
# ---------------------------------------------------------------------
AGE = 34
HR_MAX = 220 - AGE
HR_REST_DEFAULT = 60


def hr_rest() -> int:
    """Latest known resting HR (falls back to 60 bpm)."""
    ddf = db.garmin_daily_df()
    if not ddf.empty:
        s = ddf["resting_hr"].dropna()
        if not s.empty:
            return int(s.iloc[-1])
    return HR_REST_DEFAULT


def hr_zone(avg_hr: float) -> int:
    """Zone 1-5 from %HRmax (50-60-70-80-90 boundaries)."""
    pct = avg_hr / HR_MAX * 100
    for z, top in ((1, 60), (2, 70), (3, 80), (4, 90)):
        if pct < top:
            return z
    return 5


# ---------------------------------------------------------------------
# Activity-type normalisation (Garmin typeKeys / CSV labels → 10 groups)
# ---------------------------------------------------------------------
TYPE_GROUPS = ["Running", "Cycling", "Walking", "Hiking", "Swimming",
               "Football", "Strength", "Cardio", "Mobility", "Other"]

TYPE_AR = {
    "Running": "جري", "Cycling": "دراجة", "Walking": "مشي",
    "Hiking": "هايكنج", "Swimming": "سباحة", "Football": "كرة قدم",
    "Strength": "قوة", "Cardio": "كارديو", "Mobility": "مرونة",
    "Other": "أخرى",
}

# per-sport fallback intensity (fraction of heart-rate reserve) used for
# the load model when a session has no average HR
TYPE_INTENSITY = {
    "Running": 0.75, "Cycling": 0.65, "Walking": 0.35, "Hiking": 0.5,
    "Swimming": 0.65, "Football": 0.8, "Strength": 0.55, "Cardio": 0.7,
    "Mobility": 0.3, "Other": 0.5,
}

_TYPE_PATTERNS = [
    ("Football", r"soccer|football|futsal"),
    ("Running", r"run|jog|track|treadmill"),
    ("Cycling", r"cycl|bik|ride|spin|mtb"),
    ("Hiking", r"hik|trek|mountain"),
    ("Walking", r"walk"),
    ("Swimming", r"swim|pool"),
    ("Strength", r"strength|weight|gym|resistance|indoor.?train"),
    ("Mobility", r"yoga|pilates|stretch|mobilit|breath"),
    ("Cardio", r"cardio|hiit|elliptical|row|stair|aerobic"),
]


def norm_type(raw: str) -> str:
    s = str(raw or "").lower().replace("_", " ")
    for group, pat in _TYPE_PATTERNS:
        if re.search(pat, s):
            return group
    return "Other"


def type_label(group: str, lang: str) -> str:
    return TYPE_AR.get(group, group) if lang == "ar" else group


# ---------------------------------------------------------------------
# Small parsing helpers
# ---------------------------------------------------------------------
def _num(val) -> float | None:
    """Robust number parse: '1,234', '4,5', '--', '' → float | None."""
    if val is None:
        return None
    s = str(val).strip().replace('"', "")
    if not s or s in ("--", "-", "nan", "None"):
        return None
    if re.fullmatch(r"\d+,\d+", s):          # decimal comma
        s = s.replace(",", ".")
    else:                                     # thousands separators
        s = s.replace(",", "")
    try:
        return float(s)
    except ValueError:
        return None


def _dur_minutes(val) -> float | None:
    """'1:02:33', '41:26.0', '00:41:26', plain seconds → minutes."""
    if val is None:
        return None
    s = str(val).strip()
    if not s or s in ("--", "-"):
        return None
    parts = s.split(":")
    try:
        if len(parts) == 3:
            h, m, sec = float(parts[0]), float(parts[1]), float(parts[2])
            return round(h * 60 + m + sec / 60, 1)
        if len(parts) == 2:
            m, sec = float(parts[0]), float(parts[1])
            return round(m + sec / 60, 1)
        return round(float(s) / 60, 1)        # bare seconds
    except ValueError:
        return None


def _parse_dt(val) -> datetime | None:
    s = str(val or "").strip()
    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d %H:%M",
                "%d/%m/%Y %H:%M", "%m/%d/%Y %H:%M", "%Y-%m-%d"):
        try:
            return datetime.strptime(s[:len(datetime.now().strftime(fmt))], fmt)
        except ValueError:
            continue
    try:
        return pd.to_datetime(s).to_pydatetime()
    except Exception:                                     # noqa: BLE001
        return None


def _store_activity(start: datetime, a_type: str, title: str,
                    minutes, distance_km, calories, avg_hr, max_hr,
                    ascent_m, te, source: str, ext_id: str = "") -> bool:
    if start is None or not minutes or minutes < 1:
        return False
    return db.upsert_garmin_activity({
        "start_time": start.isoformat(timespec="seconds"),
        "log_date": start.date().isoformat(),
        "activity_type": norm_type(a_type),
        "title": (title or a_type or "Activity").strip()[:120],
        "minutes": round(float(minutes), 1),
        "distance_km": round(distance_km, 2) if distance_km else None,
        "calories": round(calories) if calories else None,
        "avg_hr": round(avg_hr) if avg_hr else None,
        "max_hr": round(max_hr) if max_hr else None,
        "ascent_m": round(ascent_m) if ascent_m else None,
        "training_effect": round(te, 1) if te else None,
        "source": source,
        "external_id": str(ext_id or ""),
    })


# ---------------------------------------------------------------------
# Parser 1 — Garmin Connect "Activities" CSV export
# ---------------------------------------------------------------------
_CSV_COLS = {
    "type": ("activity type",),
    "date": ("date",),
    "title": ("title", "activity name", "name"),
    "distance": ("distance",),
    "calories": ("calories",),
    "time": ("time", "duration", "elapsed time", "moving time"),
    "avg_hr": ("avg hr", "average hr", "average heart rate", "avg heart rate"),
    "max_hr": ("max hr", "max heart rate", "maximum heart rate"),
    "te": ("aerobic te", "training effect", "aerobic training effect"),
    "ascent": ("total ascent", "elev gain", "elevation gain", "ascent"),
}


def parse_activities_csv(data: bytes) -> dict:
    """Parse the Activities CSV export. Returns {new, seen, errors}."""
    rep = {"new": 0, "seen": 0, "errors": 0}
    try:
        df = pd.read_csv(io.BytesIO(data), dtype=str,
                         encoding="utf-8-sig", on_bad_lines="skip")
    except Exception:                                     # noqa: BLE001
        rep["errors"] += 1
        return rep

    low = {str(c).strip().lower(): c for c in df.columns}

    def col(field):
        for cand in _CSV_COLS[field]:
            if cand in low:
                return low[cand]
        return None

    c_date = col("date")
    if c_date is None:                     # not an activities export
        rep["errors"] += 1
        return rep
    for _, row in df.iterrows():
        start = _parse_dt(row.get(c_date))
        if start is None:
            rep["errors"] += 1
            continue

        def v(field):
            c = col(field)
            return row.get(c) if c else None

        ok = _store_activity(
            start, str(v("type") or "Other"), str(v("title") or ""),
            _dur_minutes(v("time")), _num(v("distance")), _num(v("calories")),
            _num(v("avg_hr")), _num(v("max_hr")), _num(v("ascent")),
            _num(v("te")), source="csv")
        rep["new" if ok else "seen"] += 1
    return rep


# ---------------------------------------------------------------------
# Parser 2 — FIT activity files (via optional pure-python fitdecode)
# ---------------------------------------------------------------------
def parse_fit(data: bytes) -> dict:
    rep = {"new": 0, "seen": 0, "errors": 0}
    try:
        import fitdecode
    except Exception:                                     # noqa: BLE001
        rep["errors"] += 1
        return rep
    try:
        with fitdecode.FitReader(io.BytesIO(data)) as reader:
            for frame in reader:
                if (isinstance(frame, fitdecode.FitDataMessage)
                        and frame.name == "session"):
                    g = (lambda f: frame.get_value(f, fallback=None))
                    start = g("start_time")
                    if hasattr(start, "tzinfo") and start is not None:
                        start = start.replace(tzinfo=None)
                    secs = g("total_timer_time") or g("total_elapsed_time")
                    dist = g("total_distance")
                    ok = _store_activity(
                        start, str(g("sport") or "Other"),
                        str(g("sport") or "Activity"),
                        (secs or 0) / 60,
                        (dist or 0) / 1000 if dist else None,
                        g("total_calories"), g("avg_heart_rate"),
                        g("max_heart_rate"), g("total_ascent"),
                        g("total_training_effect"), source="fit")
                    rep["new" if ok else "seen"] += 1
    except Exception:                                     # noqa: BLE001
        rep["errors"] += 1
    return rep


# ---------------------------------------------------------------------
# Parser 3 — TCX activity files (stdlib XML)
# ---------------------------------------------------------------------
def parse_tcx(data: bytes) -> dict:
    import xml.etree.ElementTree as ET
    rep = {"new": 0, "seen": 0, "errors": 0}
    try:
        root = ET.fromstring(data)
    except ET.ParseError:
        rep["errors"] += 1
        return rep
    ns = {"t": "http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2"}
    for act in root.findall(".//t:Activity", ns):
        sport = act.get("Sport", "Other")
        start = _parse_dt((act.findtext("t:Id", "", ns) or "")
                          .replace("Z", "").split(".")[0])
        secs = dist = kcal = 0.0
        hr_sum = hr_time = 0.0
        max_hr = None
        for lap in act.findall("t:Lap", ns):
            lap_s = _num(lap.findtext("t:TotalTimeSeconds", "", ns)) or 0
            secs += lap_s
            dist += _num(lap.findtext("t:DistanceMeters", "", ns)) or 0
            kcal += _num(lap.findtext("t:Calories", "", ns)) or 0
            ahr = _num(lap.findtext("t:AverageHeartRateBpm/t:Value", "", ns))
            if ahr and lap_s:
                hr_sum += ahr * lap_s
                hr_time += lap_s
            mhr = _num(lap.findtext("t:MaximumHeartRateBpm/t:Value", "", ns))
            if mhr:
                max_hr = max(max_hr or 0, mhr)
        ok = _store_activity(
            start, sport, sport, secs / 60,
            dist / 1000 if dist else None, kcal or None,
            hr_sum / hr_time if hr_time else None, max_hr,
            None, None, source="tcx")
        rep["new" if ok else "seen"] += 1
    return rep


# ---------------------------------------------------------------------
# Parser 4 — GPX tracks (stdlib XML + haversine)
# ---------------------------------------------------------------------
def _haversine_km(lat1, lon1, lat2, lon2) -> float:
    r = 6371.0
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp, dl = p2 - p1, math.radians(lon2 - lon1)
    a = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * r * math.asin(math.sqrt(a))


def parse_gpx(data: bytes) -> dict:
    import xml.etree.ElementTree as ET
    rep = {"new": 0, "seen": 0, "errors": 0}
    try:
        root = ET.fromstring(data)
    except ET.ParseError:
        rep["errors"] += 1
        return rep
    ns = {"g": "http://www.topografix.com/GPX/1/1"}
    if root.tag.startswith("{http://www.topografix.com/GPX/1/0"):
        ns = {"g": "http://www.topografix.com/GPX/1/0"}
    for trk in root.findall("g:trk", ns):
        name = trk.findtext("g:name", "", ns) or "GPX track"
        a_type = trk.findtext("g:type", "", ns) or name
        pts, dist = [], 0.0
        prev = None
        for pt in trk.findall(".//g:trkpt", ns):
            t = pt.findtext("g:time", "", ns)
            when = _parse_dt(t.replace("Z", "").split(".")[0]) if t else None
            if when:
                pts.append(when)
            try:
                lat, lon = float(pt.get("lat")), float(pt.get("lon"))
                if prev:
                    dist += _haversine_km(prev[0], prev[1], lat, lon)
                prev = (lat, lon)
            except (TypeError, ValueError):
                pass
        if len(pts) < 2:
            rep["errors"] += 1
            continue
        minutes = (max(pts) - min(pts)).total_seconds() / 60
        ok = _store_activity(min(pts), a_type, name, minutes,
                             dist or None, None, None, None, None, None,
                             source="gpx")
        rep["new" if ok else "seen"] += 1
    return rep


# ---------------------------------------------------------------------
# Parser 5 — wellness JSON from the full Garmin account-data export
# (steps, sleep, resting HR, stress, body battery — best-effort walk)
# ---------------------------------------------------------------------
def _wellness_record(rec: dict) -> bool:
    """Extract known daily-wellness keys from one JSON dict."""
    cal_date = rec.get("calendarDate")
    if isinstance(cal_date, dict):                 # {"date": "..."}
        cal_date = cal_date.get("date")
    if not cal_date or not re.match(r"\d{4}-\d{2}-\d{2}", str(cal_date)):
        return False
    d = str(cal_date)[:10]
    out = {}
    steps = rec.get("totalSteps") or rec.get("steps")
    if isinstance(steps, (int, float)) and steps > 0:
        out["steps"] = int(steps)
    rhr = rec.get("restingHeartRate") or rec.get("restingHeartRateInBeatsPerMinute")
    if isinstance(rhr, (int, float)) and 25 < rhr < 120:
        out["resting_hr"] = int(rhr)
    stress = rec.get("averageStressLevel") or rec.get("avgStressLevel")
    if isinstance(stress, (int, float)) and stress >= 0:
        out["stress"] = int(stress)
    bb = rec.get("bodyBatteryHighestValue") or rec.get("maxBodyBattery")
    if isinstance(bb, (int, float)) and bb > 0:
        out["body_battery"] = int(bb)
    kcal = rec.get("totalKilocalories")
    if isinstance(kcal, (int, float)) and kcal > 0:
        out["calories"] = float(kcal)
    sleep_secs = rec.get("sleepTimeSeconds")
    if not isinstance(sleep_secs, (int, float)):
        parts = [rec.get(k) for k in ("deepSleepSeconds", "lightSleepSeconds",
                                      "remSleepSeconds")]
        nums = [p for p in parts if isinstance(p, (int, float))]
        sleep_secs = sum(nums) if nums else None
    if isinstance(sleep_secs, (int, float)) and sleep_secs > 0:
        out["sleep_hours"] = round(sleep_secs / 3600, 1)
    if not out:
        return False
    db.upsert_garmin_daily(d, **out)
    return True


def parse_wellness_json(data: bytes) -> dict:
    rep = {"days": 0, "errors": 0}
    try:
        obj = json.loads(data.decode("utf-8", errors="replace"))
    except Exception:                                     # noqa: BLE001
        rep["errors"] += 1
        return rep

    def walk(node):
        if isinstance(node, dict):
            if _wellness_record(node):
                rep["days"] += 1
            for v in node.values():
                walk(v)
        elif isinstance(node, list):
            for v in node:
                walk(v)

    walk(obj)
    return rep


# ---------------------------------------------------------------------
# File router (single files + account-export ZIPs, one nesting level)
# ---------------------------------------------------------------------
def import_file(name: str, data: bytes, _depth: int = 0) -> dict:
    """Route one uploaded file to the right parser. Returns a merged
    report {new, seen, days, errors}."""
    rep = {"new": 0, "seen": 0, "days": 0, "errors": 0}

    def merge(r):
        for k in rep:
            rep[k] += r.get(k, 0)

    low = name.lower()
    if low.endswith(".zip") and _depth < 2:
        try:
            with zipfile.ZipFile(io.BytesIO(data)) as z:
                for info in z.infolist():
                    if info.is_dir() or info.file_size > 80_000_000:
                        continue
                    inner = info.filename.lower()
                    if inner.endswith((".csv", ".fit", ".tcx", ".gpx",
                                       ".json", ".zip")):
                        merge(import_file(info.filename, z.read(info),
                                          _depth + 1))
        except zipfile.BadZipFile:
            rep["errors"] += 1
    elif low.endswith(".csv"):
        merge(parse_activities_csv(data))
    elif low.endswith(".fit"):
        merge(parse_fit(data))
    elif low.endswith(".tcx"):
        merge(parse_tcx(data))
    elif low.endswith(".gpx"):
        merge(parse_gpx(data))
    elif low.endswith(".json"):
        merge(parse_wellness_json(data))
    else:
        rep["errors"] += 1
    return rep


# ---------------------------------------------------------------------
# Push synced data into the app's own trackers
# (recovery: steps + sleep · cardio log: activities) — idempotent
# ---------------------------------------------------------------------
def apply_to_trackers() -> dict:
    rep = {"recovery_days": 0, "cardio": 0}

    ddf = db.garmin_daily_df()
    for _, r in ddf.iterrows():
        steps = int(r["steps"]) if pd.notna(r["steps"]) else None
        sleep_h = float(r["sleep_hours"]) if pd.notna(r["sleep_hours"]) else None
        if steps is None and sleep_h is None:
            continue
        d_iso = r["log_date"].date().isoformat()
        prev = db.get_recovery(d_iso) or {}
        db.upsert_recovery(
            d_iso,
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
        rep["recovery_days"] += 1

    adf = db.garmin_activities_df()
    try:
        seen = set(json.loads(db.get_setting("garmin_cardio_seen", "[]")))
    except Exception:                                     # noqa: BLE001
        seen = set()
    for _, a in adf.iterrows():
        sig = f"{a['start_time']}|{a['activity_type']}"
        if sig in seen or not a["minutes"] or a["minutes"] < 3:
            continue
        db.add_cardio(a["log_date"].date().isoformat(),
                      f"⌚ {a['title']}", float(a["minutes"]),
                      float(a["calories"]) if pd.notna(a["calories"]) else 0)
        seen.add(sig)
        rep["cardio"] += 1
    db.set_setting("garmin_cardio_seen", json.dumps(sorted(seen)[-1000:]))
    return rep


# ---------------------------------------------------------------------
# Optional live sync via the community garminconnect library.
# Lazy + guarded: a missing/broken library only disables THIS section.
# ---------------------------------------------------------------------
try:
    from garminconnect import Garmin                      # noqa: F401
    GARMIN_API_AVAILABLE = True
except Exception:                                         # noqa: BLE001
    GARMIN_API_AVAILABLE = False


def api_is_connected() -> bool:
    return bool(db.get_setting("garmin_tokens"))


def api_connected_email() -> str:
    return db.get_setting("garmin_email", "")


def api_disconnect():
    db.set_setting("garmin_tokens", "")
    db.set_setting("garmin_email", "")


def api_connect(email: str, password: str, mfa_code: str = "") -> dict:
    """Log in. The password is used once and never stored — only the
    session tokens. Returns {ok, needs_mfa, error}."""
    if not GARMIN_API_AVAILABLE:
        return {"ok": False, "error": "library-missing"}
    from garminconnect import Garmin
    try:
        if mfa_code.strip():
            g = Garmin(email=email, password=password,
                       prompt_mfa=lambda: mfa_code.strip())
            g.login()
        else:
            g = Garmin(email=email, password=password, return_on_mfa=True)
            status, _ = g.login()
            if status == "needs_mfa":
                return {"ok": False, "needs_mfa": True}
        db.set_setting("garmin_tokens", g.garth.dumps()
                       if hasattr(g, "garth") else g.client.dumps())
        db.set_setting("garmin_email", email)
        return {"ok": True}
    except Exception as e:                                # noqa: BLE001
        msg = str(e).lower()
        if "password" in msg or "credential" in msg or "unauthorized" in msg:
            return {"ok": False, "error": "auth"}
        return {"ok": False, "error": str(e)[:200]}


def _api_client():
    if not api_is_connected() or not GARMIN_API_AVAILABLE:
        return None
    from garminconnect import Garmin
    try:
        g = Garmin()
        g.login(db.get_setting("garmin_tokens"))
        return g
    except Exception:                                     # noqa: BLE001
        return None


def api_sync(days_back: int = 14) -> dict:
    """Pull daily wellness + activities straight from Garmin Connect."""
    g = _api_client()
    if g is None:
        return {"ok": False, "error": "not-connected"}
    rep = {"ok": True, "days": 0, "new": 0, "seen": 0, "errors": 0}
    today = date.today()

    for i in range(days_back):
        d = (today - timedelta(days=i)).isoformat()
        vals = {}
        try:
            stats = g.get_stats(d) or {}
            vals = {
                "steps": stats.get("totalSteps"),
                "resting_hr": stats.get("restingHeartRate"),
                "stress": stats.get("averageStressLevel"),
                "body_battery": stats.get("bodyBatteryHighestValue"),
                "calories": stats.get("totalKilocalories"),
            }
        except Exception:                                 # noqa: BLE001
            rep["errors"] += 1
        try:
            sleep = g.get_sleep_data(d) or {}
            secs = (sleep.get("dailySleepDTO") or {}).get("sleepTimeSeconds")
            if secs:
                vals["sleep_hours"] = round(secs / 3600, 1)
        except Exception:                                 # noqa: BLE001
            pass
        vals = {k: v for k, v in vals.items() if v}
        if vals:
            db.upsert_garmin_daily(d, **vals)
            rep["days"] += 1

    try:
        start = (today - timedelta(days=days_back)).isoformat()
        for a in g.get_activities_by_date(start, today.isoformat()) or []:
            begin = _parse_dt(a.get("startTimeLocal"))
            ok = _store_activity(
                begin,
                (a.get("activityType") or {}).get("typeKey", "Other"),
                a.get("activityName") or "",
                (a.get("duration") or 0) / 60,
                (a.get("distance") or 0) / 1000 or None,
                a.get("calories"), a.get("averageHR"), a.get("maxHR"),
                a.get("elevationGain"), a.get("aerobicTrainingEffect"),
                source="api", ext_id=a.get("activityId"))
            rep["new" if ok else "seen"] += 1
    except Exception:                                     # noqa: BLE001
        rep["errors"] += 1
    return rep


# ---------------------------------------------------------------------
# Analysis — training load, ACWR, weekly volume, intensity mix
# ---------------------------------------------------------------------
def session_load(minutes: float, avg_hr: float | None, a_type: str) -> float:
    """TRIMP-like load units: minutes × heart-rate-reserve fraction × 10.
    Falls back to a per-sport intensity when no HR was recorded."""
    if not minutes:
        return 0.0
    rest = hr_rest()
    if avg_hr and avg_hr > rest:
        frac = min(max((avg_hr - rest) / max(HR_MAX - rest, 1), 0.2), 1.0)
    else:
        frac = TYPE_INTENSITY.get(a_type, 0.5)
    return round(minutes * frac * 10, 1)


def activities_with_load() -> pd.DataFrame:
    df = db.garmin_activities_df()
    if df.empty:
        return df
    df = df.copy()
    df["load"] = df.apply(
        lambda r: session_load(r["minutes"] or 0,
                               r["avg_hr"] if pd.notna(r["avg_hr"]) else None,
                               r["activity_type"]), axis=1)
    df["zone"] = df["avg_hr"].apply(
        lambda h: hr_zone(h) if pd.notna(h) else None)
    df["hard"] = df["avg_hr"].apply(
        lambda h: pd.notna(h) and h >= 0.85 * HR_MAX)
    return df


def daily_load_df() -> pd.DataFrame:
    """One row per calendar day from first activity to today, load-summed
    (0 on rest days) — the base series for the ACWR maths."""
    df = activities_with_load()
    if df.empty:
        return pd.DataFrame(columns=["log_date", "load", "minutes"])
    per_day = (df.groupby(df["log_date"].dt.date)
                 .agg(load=("load", "sum"), minutes=("minutes", "sum"))
                 .reset_index().rename(columns={"log_date": "d"}))
    idx = pd.date_range(per_day["d"].min(), date.today(), freq="D")
    out = (per_day.set_index(pd.to_datetime(per_day["d"]))
           .reindex(idx, fill_value=0.0)
           .drop(columns=["d"]).rename_axis("log_date").reset_index())
    return out


def acwr_df() -> pd.DataFrame:
    """Acute (7-day) vs chronic (28-day) workload ratio per day."""
    daily = daily_load_df()
    if len(daily) < 10:
        return pd.DataFrame(columns=["log_date", "acute", "chronic", "acwr"])
    s = daily.set_index("log_date")["load"]
    acute = s.rolling(7, min_periods=4).sum()
    chronic = s.rolling(28, min_periods=14).sum() / 4
    out = pd.DataFrame({"acute": acute, "chronic": chronic})
    out["acwr"] = (out["acute"] / out["chronic"]).where(out["chronic"] > 50)
    return out.reset_index().dropna(subset=["acute"])


def weekly_df() -> pd.DataFrame:
    df = activities_with_load()
    if df.empty:
        return pd.DataFrame(columns=["week_start", "sessions", "minutes",
                                     "km", "kcal", "load"])
    df["week_start"] = df["log_date"].dt.to_period("W").dt.start_time
    return (df.groupby("week_start")
              .agg(sessions=("id", "count"), minutes=("minutes", "sum"),
                   km=("distance_km", "sum"), kcal=("calories", "sum"),
                   load=("load", "sum"))
              .reset_index())


def type_mix_df(days: int = 28) -> pd.DataFrame:
    df = activities_with_load()
    if df.empty:
        return pd.DataFrame(columns=["activity_type", "minutes"])
    cutoff = pd.Timestamp(date.today() - timedelta(days=days))
    df = df[df["log_date"] >= cutoff]
    return (df.groupby("activity_type")["minutes"].sum()
              .sort_values(ascending=False).reset_index())


def stats_summary() -> dict:
    """Headline numbers for the metric tiles."""
    df = activities_with_load()
    ddf = db.garmin_daily_df()
    out = {"activities": 0, "minutes_7d": 0, "km_7d": 0.0, "load_7d": 0,
           "acwr": None, "sleep_7d": None, "steps_7d": None, "rhr_7d": None,
           "last_sync": None}
    if not df.empty:
        cutoff = pd.Timestamp(date.today() - timedelta(days=7))
        recent = df[df["log_date"] >= cutoff]
        out["activities"] = len(df)
        out["minutes_7d"] = float(recent["minutes"].sum())
        out["km_7d"] = float(recent["distance_km"].fillna(0).sum())
        out["load_7d"] = float(recent["load"].sum())
        out["last_sync"] = df["log_date"].max().date()
    a = acwr_df()
    if not a.empty and pd.notna(a.iloc[-1]["acwr"]):
        out["acwr"] = float(a.iloc[-1]["acwr"])
    if not ddf.empty:
        cutoff = pd.Timestamp(date.today() - timedelta(days=7))
        recent = ddf[ddf["log_date"] >= cutoff]
        for field, key in (("sleep_hours", "sleep_7d"), ("steps", "steps_7d"),
                           ("resting_hr", "rhr_7d")):
            s = recent[field].dropna()
            if not s.empty:
                out[key] = float(s.mean())
        last_daily = ddf["log_date"].max().date()
        out["last_sync"] = max(filter(None, [out["last_sync"], last_daily]))
    return out


# ---------------------------------------------------------------------
# Recommendations — rule-based, bilingual, rehab-aware
# ---------------------------------------------------------------------
def insights(lang: str) -> list[tuple[str, str]]:
    """[(level, text)] — level in success/info/warning/error, ordered
    most-important first."""
    out: list[tuple[str, str]] = []
    T = lambda k, **kw: tr(k, lang).format(**kw)

    adf = activities_with_load()
    ddf = db.garmin_daily_df()
    if adf.empty and ddf.empty:
        return [("info", T("gm_i_nodata"))]

    today = pd.Timestamp(date.today())

    # ---- 1. load spike / sweet spot (ACWR — key ACL re-injury metric) ----
    a = acwr_df()
    ratio = float(a.iloc[-1]["acwr"]) if (not a.empty and
                                          pd.notna(a.iloc[-1]["acwr"])) else None
    if ratio is not None:
        if ratio > 1.5:
            out.append(("error", T("gm_i_spike_high", r=f"{ratio:.2f}")))
        elif ratio > 1.3:
            out.append(("warning", T("gm_i_spike_mild", r=f"{ratio:.2f}")))
        elif ratio < 0.8:
            out.append(("info", T("gm_i_undertrain", r=f"{ratio:.2f}")))
        else:
            out.append(("success", T("gm_i_sweet", r=f"{ratio:.2f}")))

    if not adf.empty:
        # ---- 2. week-over-week volume ramp ----
        wk = weekly_df()
        if len(wk) >= 2:
            this_w, prev_w = wk.iloc[-1], wk.iloc[-2]
            if (prev_w["minutes"] >= 60
                    and this_w["minutes"] > prev_w["minutes"] * 1.35):
                pct = (this_w["minutes"] / prev_w["minutes"] - 1) * 100
                out.append(("warning", T("gm_i_ramp", pct=f"{pct:.0f}")))

        # ---- 3. no rest day in the last 7 ----
        daily = daily_load_df().tail(7)
        if len(daily) == 7 and (daily["load"] > 0).all():
            out.append(("warning", T("gm_i_norest")))

        # ---- 4. back-to-back hard days ----
        hard_days = sorted(set(
            adf.loc[adf["hard"], "log_date"].dt.date))
        b2b = any((b - a_).days == 1
                  for a_, b in zip(hard_days, hard_days[1:]))
        if b2b:
            out.append(("warning", T("gm_i_hard_b2b")))

        # ---- 5. intensity distribution (80/20) ----
        cutoff = today - pd.Timedelta(days=28)
        recent = adf[(adf["log_date"] >= cutoff) & adf["zone"].notna()]
        if len(recent) >= 6:
            hard_share = (recent["zone"] >= 4).mean()
            if hard_share > 0.4:
                out.append(("info", T("gm_i_polarize",
                                      pct=f"{hard_share * 100:.0f}")))

        # ---- 6. stale data ----
        last = adf["log_date"].max()
        if not ddf.empty:
            last = max(last, ddf["log_date"].max())
        gap = (today - last).days
        if gap > 7:
            out.append(("info", T("gm_i_stale", days=gap)))

        # ---- 7. consistency praise ----
        if len(wk) >= 4 and (wk.tail(4)["sessions"] >= 3).all():
            out.append(("success", T("gm_i_consistent")))

    if not ddf.empty:
        recent7 = ddf[ddf["log_date"] >= today - pd.Timedelta(days=7)]

        # ---- 8. sleep ----
        sleep = recent7["sleep_hours"].dropna()
        if len(sleep) >= 3:
            avg = sleep.mean()
            if avg < 7:
                out.append(("warning", T("gm_i_sleep_low", h=f"{avg:.1f}")))
            elif avg >= 7.5:
                out.append(("success", T("gm_i_sleep_good", h=f"{avg:.1f}")))

        # ---- 9. resting-HR drift (fatigue / illness early-warning) ----
        rhr = ddf[["log_date", "resting_hr"]].dropna()
        if len(rhr) >= 14:
            base = rhr[rhr["log_date"] < today - pd.Timedelta(days=7)]
            week = rhr[rhr["log_date"] >= today - pd.Timedelta(days=7)]
            if len(base) >= 7 and len(week) >= 3:
                drift = week["resting_hr"].mean() - base["resting_hr"].mean()
                if drift >= 5:
                    out.append(("warning", T("gm_i_rhr_up",
                                             bpm=f"{drift:.0f}")))

        # ---- 10. steps ----
        steps = recent7["steps"].dropna()
        if len(steps) >= 3 and steps.mean() < 6000:
            out.append(("info", T("gm_i_steps_low",
                                  n=f"{steps.mean():,.0f}")))

        # ---- 11. stress / body battery ----
        stress = recent7["stress"].dropna()
        if len(stress) >= 3 and stress.mean() >= 50:
            out.append(("info", T("gm_i_stress", s=f"{stress.mean():.0f}")))
        bb = recent7["body_battery"].dropna()
        if len(bb) >= 3 and bb.mean() < 50:
            out.append(("info", T("gm_i_battery", b=f"{bb.mean():.0f}")))

    if not out:
        out.append(("info", T("gm_i_allquiet")))
    order = {"error": 0, "warning": 1, "info": 2, "success": 3}
    out.sort(key=lambda x: order[x[0]])
    return out
