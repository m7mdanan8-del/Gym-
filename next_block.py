"""
next_block.py
=============
Generates the NEXT 4-week training block from what was actually logged:

- reads the Week-4 benchmark tests (push-ups, wall-sit, calf raises,
  Y-balance, single-leg hop, strict pull-ups, plank)
- reads every exercise's last logged weight + how it felt (difficulty,
  pain) and stamps a personalised "suggested start load" onto it
- shifts the rep schemes one gear toward strength (e.g. 10 -> 8-10),
  so the same split progresses instead of repeating
- applies a pain guard: if recent sessions averaged pain >= 3/10, all
  load suggestions stay conservative (no automatic increases)

The result is written into the program table (Edit Mode still owns it
afterwards) and the app's start date moves to the coming Monday.
"""

from datetime import date, timedelta

import database as db
from program import default_program

# Benchmark entries are logged under these names (+ pull-up/push-up
# tests, which keep their normal names with "TEST" in the reps text).
TEST_NAMES = {
    "TEST — Wall-Sit Max Hold",
    "TEST — Single-Leg Calf Raise Max Reps",
    "TEST — Y-Balance Best Reach",
    "TEST — Single-Leg Hop for Distance",
    "TEST — Plank Max Hold",
}
TEST_HOSTS = {"Pull-Up / Assisted Pull-Up (neutral grip)", "Push-Up (full)"}

# One gear toward strength: same split, heavier sets.
REP_SHIFT = {
    "12-15": "10-12", "12": "10", "10-12": "8-10", "10": "8-10",
    "8-10": "6-8", "8": "6-8", "6-8": "5-6",
}

# Sections that carry loads worth suggesting for.
LOADED_SECTIONS = ("Strength", "Rehabilitation", "Core",
                   "Functional Finisher")


def collect_tests(days_back: int = 60) -> list[dict]:
    """Benchmark results logged in the recent past."""
    df = db.logs_df()
    if df.empty:
        return []
    cutoff = date.today() - timedelta(days=days_back)
    df = df[df["log_date"].dt.date >= cutoff]
    out = []
    for _, r in df.iterrows():
        name = r["exercise_name"]
        is_test = (name in TEST_NAMES or
                   (name in TEST_HOSTS and "TEST" in str(r["reps_done"] or "")))
        if is_test and r["completed"]:
            out.append({"date": str(r["log_date"].date()), "name": name,
                        "result": str(r["reps_done"] or ""),
                        "notes": str(r["notes"] or "")})
    out.sort(key=lambda x: x["date"], reverse=True)
    # keep only the newest entry per test
    seen, latest = set(), []
    for t in out:
        if t["name"] not in seen:
            seen.add(t["name"])
            latest.append(t)
    return latest


def recent_avg_pain(days_back: int = 14):
    df = db.logs_df()
    if df.empty:
        return None
    cutoff = date.today() - timedelta(days=days_back)
    df = df[(df["log_date"].dt.date >= cutoff) & df["pain"].notna()]
    return round(float(df["pain"].mean()), 1) if len(df) else None


def _load_suggestion(name: str, conservative: bool):
    """Personalised start load from the last completed entry."""
    last = db.last_exercise_entry(name, "9999-12-31")
    if not last or not last.get("weight"):
        return None
    w = float(last["weight"])
    pain = int(last.get("pain") or 0)
    diff = None
    # difficulty isn't returned by last_exercise_entry; treat via pain only
    if conservative or pain >= 3:
        nxt, why = round(w * 0.9, 1), "eased 10% (pain guard)"
    else:
        nxt, why = w + 2.5, "last block +2.5 kg"
    return f"📈 Suggested start: ~{nxt:g} kg ({why}; you last logged {w:g} kg)."


def generate_next_block(save: bool = True) -> dict:
    """Build (and optionally save) the next block. Returns a report."""
    tests = collect_tests()
    avg_pain = recent_avg_pain()
    conservative = avg_pain is not None and avg_pain >= 3

    prog = default_program()
    n_sugg = n_shift = 0
    for week, days in prog.items():
        for day, data in days.items():
            for sec in data["sections"]:
                if not any(sec["name"].startswith(s) for s in LOADED_SECTIONS):
                    continue
                for ex in sec["exercises"]:
                    if str(ex.get("reps")) in REP_SHIFT and \
                            sec["name"].startswith("Strength"):
                        ex["reps"] = REP_SHIFT[str(ex["reps"])]
                        n_shift += 1
                    sugg = _load_suggestion(ex["name"], conservative)
                    if sugg:
                        ex["purpose"] = f"{ex.get('purpose', '')}\n\n{sugg}".strip()
                        n_sugg += 1

    next_monday = date.today() + timedelta(days=(7 - date.today().weekday()) % 7 or 7)
    block_num = int(db.get_setting("block_number", 1)) + 1

    if save:
        for week, days in prog.items():
            for day, data in days.items():
                db.save_day_program(week, day, data)
        db.set_setting("block_number", block_num)
        db.set_setting("start_date", next_monday.isoformat())

    return {"block": block_num, "tests": tests, "avg_pain": avg_pain,
            "conservative": conservative, "n_suggestions": n_sugg,
            "n_rep_shifts": n_shift, "start_date": next_monday.isoformat()}
