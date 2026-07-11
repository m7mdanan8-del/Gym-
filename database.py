"""
database.py
===========
SQLite persistence layer. Everything the app remembers lives here:

  program       – the (editable) training program, one JSON blob per week/day
  exercise_log  – per-exercise tracker entries (checkbox, weight, pain, ...)
  recovery      – daily recovery metrics (sleep, water, protein, steps, ...)
  body_weight   – body-weight history
  cardio        – logged cardio sessions (type, minutes, estimated kcal)
  settings      – key/value store (program start date, profile, prefs)

The DB file lives next to the code (gym_rehab.db) so the app remembers
everything between launches.
"""

import json
import sqlite3
from datetime import date, datetime, timedelta
from pathlib import Path

import pandas as pd

from program import default_program, DAYS

DB_PATH = Path(__file__).parent / "gym_rehab.db"


def _conn():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


# ---------------------------------------------------------------------
# Schema + seed
# ---------------------------------------------------------------------
def init_db():
    with _conn() as c:
        c.executescript("""
        CREATE TABLE IF NOT EXISTS program (
            week      INTEGER NOT NULL,
            day       TEXT    NOT NULL,
            data_json TEXT    NOT NULL,
            PRIMARY KEY (week, day)
        );
        CREATE TABLE IF NOT EXISTS exercise_log (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            log_date      TEXT NOT NULL,
            week          INTEGER,
            day           TEXT,
            section       TEXT,
            exercise_name TEXT NOT NULL,
            completed     INTEGER DEFAULT 0,
            weight        REAL,
            pain          INTEGER,
            difficulty    INTEGER,
            energy        INTEGER,
            sets_done     TEXT,
            reps_done     TEXT,
            notes         TEXT,
            updated_at    TEXT,
            UNIQUE (log_date, day, section, exercise_name)
        );
        CREATE TABLE IF NOT EXISTS recovery (
            log_date         TEXT PRIMARY KEY,
            sleep_hours      REAL,
            water_l          REAL,
            protein_g        REAL,
            steps            INTEGER,
            soreness         INTEGER,
            energy           INTEGER,
            recovery_score   INTEGER,
            football_rating  INTEGER,
            notes            TEXT
        );
        CREATE TABLE IF NOT EXISTS body_weight (
            log_date  TEXT PRIMARY KEY,
            weight_kg REAL NOT NULL
        );
        CREATE TABLE IF NOT EXISTS cardio (
            id       INTEGER PRIMARY KEY AUTOINCREMENT,
            log_date TEXT NOT NULL,
            activity TEXT,
            minutes  REAL,
            calories REAL
        );
        CREATE TABLE IF NOT EXISTS settings (
            key   TEXT PRIMARY KEY,
            value TEXT
        );
        CREATE TABLE IF NOT EXISTS garmin_activities (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            start_time    TEXT NOT NULL,
            log_date      TEXT NOT NULL,
            activity_type TEXT,
            title         TEXT,
            minutes       REAL,
            distance_km   REAL,
            calories      REAL,
            avg_hr        REAL,
            max_hr        REAL,
            ascent_m      REAL,
            training_effect REAL,
            source        TEXT,
            external_id   TEXT,
            UNIQUE (start_time, activity_type)
        );
        CREATE TABLE IF NOT EXISTS garmin_daily (
            log_date     TEXT PRIMARY KEY,
            steps        INTEGER,
            sleep_hours  REAL,
            resting_hr   INTEGER,
            stress       INTEGER,
            body_battery INTEGER,
            calories     REAL
        );
        """)
    seed_program_if_missing()


def seed_program_if_missing(force: bool = False):
    """Write the generated default program into the DB (first run only,
    unless force=True which resets all edits)."""
    with _conn() as c:
        if not force:
            n = c.execute("SELECT COUNT(*) FROM program").fetchone()[0]
            if n > 0:
                return
        prog = default_program()
        c.execute("DELETE FROM program")
        for week, days in prog.items():
            for day, data in days.items():
                c.execute(
                    "INSERT INTO program (week, day, data_json) VALUES (?,?,?)",
                    (week, day, json.dumps(data)))


# ---------------------------------------------------------------------
# Settings
# ---------------------------------------------------------------------
def get_setting(key, default=None):
    with _conn() as c:
        row = c.execute("SELECT value FROM settings WHERE key=?", (key,)).fetchone()
    return row[0] if row else default


def set_setting(key, value):
    with _conn() as c:
        c.execute("INSERT INTO settings (key, value) VALUES (?,?) "
                  "ON CONFLICT(key) DO UPDATE SET value=excluded.value",
                  (key, str(value)))


def get_start_date() -> date:
    """Program start date (defaults to the Monday of the current week)."""
    raw = get_setting("start_date")
    if raw:
        return date.fromisoformat(raw)
    today = date.today()
    monday = today - timedelta(days=today.weekday())
    set_setting("start_date", monday.isoformat())
    return monday


def current_week_and_day(on: date | None = None):
    """Map a calendar date onto (program week 1-4, weekday name)."""
    on = on or date.today()
    start = get_start_date()
    delta_days = (on - start).days
    week = (delta_days // 7) % 4 + 1 if delta_days >= 0 else 1
    return week, DAYS[on.weekday()]


# ---------------------------------------------------------------------
# Program (editable)
# ---------------------------------------------------------------------
def get_day_program(week: int, day: str) -> dict:
    with _conn() as c:
        row = c.execute("SELECT data_json FROM program WHERE week=? AND day=?",
                        (week, day)).fetchone()
    return json.loads(row[0]) if row else {"focus": "", "sections": []}


def save_day_program(week: int, day: str, data: dict):
    with _conn() as c:
        c.execute("INSERT INTO program (week, day, data_json) VALUES (?,?,?) "
                  "ON CONFLICT(week, day) DO UPDATE SET data_json=excluded.data_json",
                  (week, day, json.dumps(data)))


def count_day_exercises(week: int, day: str) -> int:
    data = get_day_program(week, day)
    return sum(len(s["exercises"]) for s in data.get("sections", []))


# ---------------------------------------------------------------------
# Exercise log (the workout tracker)
# ---------------------------------------------------------------------
def upsert_exercise_log(log_date: str, week: int, day: str, section: str,
                        exercise_name: str, completed: bool,
                        weight, pain, difficulty, energy,
                        sets_done, reps_done, notes):
    with _conn() as c:
        c.execute("""
        INSERT INTO exercise_log
            (log_date, week, day, section, exercise_name, completed, weight,
             pain, difficulty, energy, sets_done, reps_done, notes, updated_at)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        ON CONFLICT (log_date, day, section, exercise_name) DO UPDATE SET
            completed=excluded.completed, weight=excluded.weight,
            pain=excluded.pain, difficulty=excluded.difficulty,
            energy=excluded.energy, sets_done=excluded.sets_done,
            reps_done=excluded.reps_done, notes=excluded.notes,
            week=excluded.week, updated_at=excluded.updated_at
        """, (log_date, week, day, section, exercise_name, int(completed),
              weight, pain, difficulty, energy, sets_done, reps_done, notes,
              datetime.now().isoformat(timespec="seconds")))


def get_day_logs(log_date: str) -> dict:
    """{(section, exercise_name): row-dict} for one calendar day."""
    with _conn() as c:
        c.row_factory = sqlite3.Row
        rows = c.execute("SELECT * FROM exercise_log WHERE log_date=?",
                         (log_date,)).fetchall()
    return {(r["section"], r["exercise_name"]): dict(r) for r in rows}


def logs_df() -> pd.DataFrame:
    with _conn() as c:
        df = pd.read_sql_query("SELECT * FROM exercise_log", c)
    if not df.empty:
        df["log_date"] = pd.to_datetime(df["log_date"])
    return df


def last_exercise_entry(exercise_name: str, before_date: str) -> dict | None:
    """Most recent completed log of this exercise before the given date —
    powers the 'Last time: X kg' hint in the workout tracker."""
    with _conn() as c:
        c.row_factory = sqlite3.Row
        row = c.execute(
            "SELECT log_date, weight, pain, sets_done, reps_done "
            "FROM exercise_log WHERE exercise_name=? AND log_date<? "
            "AND completed=1 ORDER BY log_date DESC LIMIT 1",
            (exercise_name, before_date)).fetchone()
    return dict(row) if row else None


# ---------------------------------------------------------------------
# Recovery / weight / cardio
# ---------------------------------------------------------------------
def upsert_recovery(log_date: str, **kw):
    cols = ["sleep_hours", "water_l", "protein_g", "steps", "soreness",
            "energy", "recovery_score", "football_rating", "notes"]
    vals = [kw.get(c) for c in cols]
    with _conn() as c:
        c.execute(f"""
        INSERT INTO recovery (log_date, {','.join(cols)})
        VALUES (?,?,?,?,?,?,?,?,?,?)
        ON CONFLICT (log_date) DO UPDATE SET
        {','.join(f'{c}=excluded.{c}' for c in cols)}
        """, [log_date] + vals)


def get_recovery(log_date: str) -> dict | None:
    with _conn() as c:
        c.row_factory = sqlite3.Row
        row = c.execute("SELECT * FROM recovery WHERE log_date=?",
                        (log_date,)).fetchone()
    return dict(row) if row else None


def recovery_df() -> pd.DataFrame:
    with _conn() as c:
        df = pd.read_sql_query("SELECT * FROM recovery ORDER BY log_date", c)
    if not df.empty:
        df["log_date"] = pd.to_datetime(df["log_date"])
    return df


def upsert_weight(log_date: str, weight_kg: float):
    with _conn() as c:
        c.execute("INSERT INTO body_weight (log_date, weight_kg) VALUES (?,?) "
                  "ON CONFLICT (log_date) DO UPDATE SET weight_kg=excluded.weight_kg",
                  (log_date, weight_kg))


def weight_df() -> pd.DataFrame:
    with _conn() as c:
        df = pd.read_sql_query(
            "SELECT * FROM body_weight ORDER BY log_date", c)
    if not df.empty:
        df["log_date"] = pd.to_datetime(df["log_date"])
    return df


def add_cardio(log_date: str, activity: str, minutes: float, calories: float):
    with _conn() as c:
        c.execute("INSERT INTO cardio (log_date, activity, minutes, calories) "
                  "VALUES (?,?,?,?)", (log_date, activity, minutes, calories))


def cardio_df() -> pd.DataFrame:
    with _conn() as c:
        df = pd.read_sql_query("SELECT * FROM cardio ORDER BY log_date", c)
    if not df.empty:
        df["log_date"] = pd.to_datetime(df["log_date"])
    return df


def delete_cardio(row_id: int):
    with _conn() as c:
        c.execute("DELETE FROM cardio WHERE id=?", (row_id,))


# ---------------------------------------------------------------------
# Garmin data (synced from watch exports / Garmin Connect)
# ---------------------------------------------------------------------
def upsert_garmin_activity(a: dict) -> bool:
    """Insert an activity; the (start_time, activity_type) unique key makes
    repeated imports of the same file harmless. Returns True if new."""
    cols = ["start_time", "log_date", "activity_type", "title", "minutes",
            "distance_km", "calories", "avg_hr", "max_hr", "ascent_m",
            "training_effect", "source", "external_id"]
    with _conn() as c:
        exists = c.execute(
            "SELECT 1 FROM garmin_activities WHERE start_time=? AND activity_type=?",
            (a.get("start_time"), a.get("activity_type"))).fetchone()
        c.execute(f"""
        INSERT INTO garmin_activities ({','.join(cols)})
        VALUES ({','.join('?' * len(cols))})
        ON CONFLICT (start_time, activity_type) DO UPDATE SET
            title=excluded.title, minutes=excluded.minutes,
            distance_km=excluded.distance_km, calories=excluded.calories,
            avg_hr=excluded.avg_hr, max_hr=excluded.max_hr,
            ascent_m=excluded.ascent_m,
            training_effect=excluded.training_effect
        """, [a.get(col) for col in cols])
    return not exists


def garmin_activities_df() -> pd.DataFrame:
    with _conn() as c:
        df = pd.read_sql_query(
            "SELECT * FROM garmin_activities ORDER BY start_time", c)
    if not df.empty:
        df["log_date"] = pd.to_datetime(df["log_date"])
    return df


def delete_garmin_activity(row_id: int):
    with _conn() as c:
        c.execute("DELETE FROM garmin_activities WHERE id=?", (row_id,))


def upsert_garmin_daily(log_date: str, **kw):
    """Merge daily wellness values — only overwrite with non-null data."""
    cols = ["steps", "sleep_hours", "resting_hr", "stress",
            "body_battery", "calories"]
    vals = [kw.get(c) for c in cols]
    with _conn() as c:
        c.execute(f"""
        INSERT INTO garmin_daily (log_date, {','.join(cols)})
        VALUES (?,?,?,?,?,?,?)
        ON CONFLICT (log_date) DO UPDATE SET
        {','.join(f'{c}=COALESCE(excluded.{c}, {c})' for c in cols)}
        """, [log_date] + vals)


def garmin_daily_df() -> pd.DataFrame:
    with _conn() as c:
        df = pd.read_sql_query(
            "SELECT * FROM garmin_daily ORDER BY log_date", c)
    if not df.empty:
        df["log_date"] = pd.to_datetime(df["log_date"])
    return df


def clear_garmin_data():
    with _conn() as c:
        c.execute("DELETE FROM garmin_activities")
        c.execute("DELETE FROM garmin_daily")


# ---------------------------------------------------------------------
# Derived stats for the dashboard
# ---------------------------------------------------------------------
def completion_by_date() -> pd.DataFrame:
    """Per calendar date: exercises completed / planned (planned = number of
    exercises in that day's program) -> completion %."""
    df = logs_df()
    if df.empty:
        return pd.DataFrame(columns=["log_date", "completed", "planned", "pct"])
    grp = (df.groupby(["log_date", "week", "day"])
             .agg(completed=("completed", "sum"))
             .reset_index())
    grp["planned"] = grp.apply(
        lambda r: max(count_day_exercises(int(r["week"]), r["day"]), 1), axis=1)
    grp["pct"] = (grp["completed"] / grp["planned"] * 100).clip(0, 100)
    return grp.sort_values("log_date")


def workout_streak() -> int:
    """Consecutive days (ending today or yesterday) with ≥1 completed
    exercise. Recovery-day logging counts — showing up is showing up."""
    df = logs_df()
    if df.empty:
        return 0
    days_done = set(df.loc[df["completed"] == 1, "log_date"].dt.date)
    if not days_done:
        return 0
    streak, cur = 0, date.today()
    if cur not in days_done:      # allow "yesterday" anchoring
        cur = cur - timedelta(days=1)
    while cur in days_done:
        streak += 1
        cur -= timedelta(days=1)
    return streak


def totals() -> dict:
    df = logs_df()
    if df.empty:
        return {"workouts": 0, "exercises": 0, "volume_kg": 0.0}
    done = df[df["completed"] == 1].copy()
    workouts = done.groupby(done["log_date"].dt.date).ngroups
    exercises = len(done)

    def _vol(row):
        try:
            w = float(row["weight"] or 0)
            s = float(str(row["sets_done"] or "0").split("/")[0] or 0)
            reps_raw = str(row["reps_done"] or "0")
            digits = "".join(ch for ch in reps_raw.split("-")[0].split("/")[0]
                             if ch.isdigit())
            r = float(digits or 0)
            return w * s * r
        except (TypeError, ValueError):
            return 0.0

    vol = done.apply(_vol, axis=1).sum() if not done.empty else 0.0
    return {"workouts": workouts, "exercises": exercises,
            "volume_kg": round(vol, 1)}


def pain_trend_df() -> pd.DataFrame:
    df = logs_df()
    if df.empty:
        return pd.DataFrame(columns=["log_date", "avg_pain", "max_pain"])
    df = df[df["pain"].notna()]
    if df.empty:
        return pd.DataFrame(columns=["log_date", "avg_pain", "max_pain"])
    out = (df.groupby(df["log_date"].dt.date)
             .agg(avg_pain=("pain", "mean"), max_pain=("pain", "max"))
             .reset_index().rename(columns={"log_date": "log_date"}))
    out["log_date"] = pd.to_datetime(out["log_date"])
    return out
