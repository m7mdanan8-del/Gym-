"""
app.py
======
Rehab & Performance — a professional bilingual (English / العربية)
rehabilitation and performance training platform for a footballer with a
partial ACL tear and a previously dislocated right shoulder.

Run with:  streamlit run app.py
"""

from datetime import date

import pandas as pd
import streamlit as st

import charts
import database as db
from exercise_library import EXERCISES
from illustrations import get_svg
from program import DAYS, DAY_FOCUS, WEEK_THEMES
from translations import (LANGS, tr, day_label, section_label, focus_label,
                          week_theme, exercise_label)

# ----------------------------------------------------------------------
# App setup
# ----------------------------------------------------------------------
st.set_page_config(
    page_title="Rehab & Performance",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded",
)

db.init_db()

PROFILE = {"age": 34, "height_cm": 168, "sex": "male"}

CARDIO_MET = {
    "Stationary bike — easy/tempo": 5.5,
    "Stationary bike — intervals": 8.5,
    "Incline walk": 6.0,
    "Walk": 3.5,
    "Jog": 7.0,
    "Swimming": 6.0,
    "Rowing": 7.0,
    "Football match": 8.5,
    "Football training": 7.0,
}
CARDIO_AR = {
    "Stationary bike — easy/tempo": "دراجة ثابتة — خفيف/إيقاع",
    "Stationary bike — intervals": "دراجة ثابتة — فترات",
    "Incline walk": "مشي على منحدر",
    "Walk": "مشي",
    "Jog": "هرولة",
    "Swimming": "سباحة",
    "Rowing": "تجديف",
    "Football match": "مباراة كرة قدم",
    "Football training": "تدريب كرة قدم",
}
STRENGTH_MET = 5.0          # moderate resistance training
MIN_PER_EXERCISE = 4.0      # avg minutes per completed exercise incl. rest

# ----------------------------------------------------------------------
# Language (persisted)
# ----------------------------------------------------------------------
if "lang" not in st.session_state:
    st.session_state.lang = db.get_setting("lang", "en")
LANG = st.session_state.lang


def L(key: str) -> str:
    return tr(key, LANG)


def is_dark() -> bool:
    """Follow the Streamlit theme the user selected (menu -> Settings).
    The app ships with a light default; charts match whichever is active."""
    try:
        return getattr(st.context.theme, "type", "light") == "dark"
    except Exception:
        return False


def bodyweight_kg() -> float:
    df = db.weight_df()
    if not df.empty:
        return float(df.iloc[-1]["weight_kg"])
    return float(db.get_setting("profile_weight", 72.0))


def est_strength_kcal(n_completed: int, kg: float) -> float:
    """MET-based estimate: kcal = MET * 3.5 * kg / 200 * minutes."""
    minutes = n_completed * MIN_PER_EXERCISE
    return STRENGTH_MET * 3.5 * kg / 200.0 * minutes


def cardio_kcal(met: float, minutes: float, kg: float) -> float:
    return met * 3.5 * kg / 200.0 * minutes


# ----------------------------------------------------------------------
# Global CSS — large touch targets, workout-friendly, both themes, RTL
# ----------------------------------------------------------------------
_RTL_CSS = """
/* Right-to-left layout for Arabic */
section.main .block-container, [data-testid="stSidebar"] .block-container {
    direction: rtl; text-align: right;
}
.stMarkdown, .stCaption, [data-testid="stMetric"], .rp-safety, .rp-rx,
[data-testid="stWidgetLabel"] { direction: rtl; text-align: right; }
.rp-rx td:first-child { padding: 3px 0 3px 10px; }
.rp-safety { border-left: none !important; border-right: 5px solid #3987e5; }
""" if LANG == "ar" else ""

st.markdown(f"""
<style>
/* Large, thumb-friendly buttons */
.stButton > button, .stLinkButton > a, .stDownloadButton > button {{
    min-height: 48px; font-size: 1.02rem; font-weight: 600;
    border-radius: 12px;
}}
/* Big checkboxes for mid-workout use */
.stCheckbox [data-testid="stWidgetLabel"] p {{ font-size: 1.05rem; font-weight: 700; }}
.stCheckbox input[type="checkbox"] {{ transform: scale(1.5); }}
.stCheckbox label span:first-child {{ transform: scale(1.35); margin-right: 6px; }}
.rp-pill {{
    display:inline-block; padding: 2px 12px; border-radius: 999px;
    font-size: 0.8rem; font-weight: 700; letter-spacing: .02em;
    border: 1px solid rgba(128,128,128,0.35); margin-right: 6px;
}}
.rp-safety {{
    border-left: 5px solid #3987e5; border-radius: 8px;
    padding: .55rem .9rem; margin: .3rem 0; font-size: .95rem;
    background: rgba(128,128,128,0.08);
}}
/* Prescription table */
.rp-rx {{ width:100%; border-collapse: collapse; font-size: .92rem; }}
.rp-rx td {{ padding: 3px 10px 3px 0; vertical-align: top; }}
.rp-rx td:first-child {{ font-weight: 700; opacity: .75; white-space: nowrap; }}
/* Tighter mobile padding */
@media (max-width: 640px) {{
    .block-container {{ padding: 1rem 0.7rem; }}
}}
h1, h2, h3 {{ letter-spacing: -0.01em; }}
{_RTL_CSS}
</style>
""", unsafe_allow_html=True)


# ----------------------------------------------------------------------
# Safety traffic light (workout page + safety page)
# ----------------------------------------------------------------------
def pain_traffic_light(compact: bool = False):
    st.markdown(f"""
<div class="rp-safety" style="border-color:#0ca30c;">{L('pain_green')}</div>
<div class="rp-safety" style="border-color:#fab219;">{L('pain_yellow')}</div>
<div class="rp-safety" style="border-color:#d03b3b;">{L('pain_red')}</div>
""", unsafe_allow_html=True)
    if not compact:
        st.caption(L("traffic_caption"))


# ----------------------------------------------------------------------
# Exercise guidance renderer
# ----------------------------------------------------------------------
def render_exercise_guide(ex: dict):
    c1, c2 = st.columns([2, 3], gap="medium")
    with c1:
        st.markdown(get_svg(ex.get("pattern", "balance")),
                    unsafe_allow_html=True)
        if ex.get("image_url"):
            st.image(ex["image_url"], caption=L("guidance_pic"))
        if ex.get("gif_url"):
            st.image(ex["gif_url"], caption=L("demo_gif"))
        st.markdown(
            f"""<table class="rp-rx">
            <tr><td>{L('target')}</td><td>{ex['target']}</td></tr>
            <tr><td>{L('equipment')}</td><td>{ex.get('equipment','Bodyweight')}</td></tr>
            <tr><td>{L('sets')}</td><td>{ex['sets']}</td></tr>
            <tr><td>{L('reps')}</td><td>{ex['reps']}</td></tr>
            <tr><td>{L('tempo')}</td><td>{ex['tempo']}</td></tr>
            <tr><td>{L('rest')}</td><td>{ex['rest']}</td></tr>
            <tr><td>{L('rpe')}</td><td>{ex['rpe']} / 10</td></tr>
            </table>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"**{L('why')}:** {ex['purpose']}")
        st.markdown(f"**{L('start_pos')}:** {ex['setup']}")
        st.markdown(f"**{L('how_to')}:** {ex['execution']}")
        st.markdown(f"**{L('key_cues')}:** " +
                    " · ".join(f"*{c}*" for c in ex["cues"]))
        with st.expander(L("tips_expander")):
            for tip in ex.get("tips", []):
                st.markdown(f"💡 {tip}")
            for m in ex.get("mistakes", []):
                st.markdown(f"⚠️ {L('avoid')}: {m}")
            st.markdown(f"🛟 **{L('safety_label')}:** {ex['safety']}")
        with st.expander(L("prog_expander")):
            st.markdown(f"**{L('progression')}:** {ex['progression']}")
            st.markdown(f"**{L('regression')}:** {ex['regression']}")
            st.markdown(f"**{L('alternative')}:** {ex['alternative']}")
        if ex.get("video_url"):
            st.video(ex["video_url"])
        st.link_button(L("watch_youtube"), ex["youtube"],
                       use_container_width=True)


# ----------------------------------------------------------------------
# Workout tracker (auto-saving widgets)
# ----------------------------------------------------------------------
def _tracker_save(kbase, log_date, week, day, section, name):
    ss = st.session_state
    db.upsert_exercise_log(
        log_date, week, day, section, name,
        completed=ss.get(kbase + "done", False),
        weight=ss.get(kbase + "wt"),
        pain=ss.get(kbase + "pain", 0),
        difficulty=ss.get(kbase + "diff", 5),
        energy=ss.get(kbase + "energy", 5),
        sets_done=str(ss.get(kbase + "sets", "")),
        reps_done=str(ss.get(kbase + "reps", "")),
        notes=ss.get(kbase + "notes", ""),
    )


def render_tracker(ex, log_date, week, day, section, existing):
    name = ex["name"]                      # English key — stable across languages
    kbase = f"trk|{log_date}|{day}|{section}|{name}|"
    prev = existing.get((section, name), {})
    cb = dict(on_change=_tracker_save,
              args=(kbase, log_date, week, day, section, name))

    st.markdown(f"##### {L('tracker')}")
    c0, c1, c2 = st.columns([1.3, 1, 1])
    with c0:
        st.checkbox(L("completed"), key=kbase + "done",
                    value=bool(prev.get("completed", 0)), **cb)
    with c1:
        st.number_input(L("weight_used"), 0.0, 300.0,
                        float(prev.get("weight") or 0.0), 0.5,
                        key=kbase + "wt", **cb)
    with c2:
        st.text_input(L("sets_done"), value=prev.get("sets_done") or str(ex["sets"]),
                      key=kbase + "sets", **cb)
    c3, c4, c5 = st.columns(3)
    with c3:
        st.slider(L("pain_scale"), 0, 10, int(prev.get("pain") or 0),
                  key=kbase + "pain", **cb)
    with c4:
        st.slider(L("difficulty_scale"), 1, 10, int(prev.get("difficulty") or 5),
                  key=kbase + "diff", **cb)
    with c5:
        st.slider(L("energy_scale"), 1, 10, int(prev.get("energy") or 5),
                  key=kbase + "energy", **cb)
    c6, c7 = st.columns([1, 2])
    with c6:
        st.text_input(L("reps_done"), value=prev.get("reps_done") or str(ex["reps"]),
                      key=kbase + "reps", **cb)
    with c7:
        st.text_input(L("notes"), value=prev.get("notes") or "",
                      placeholder=L("notes_ph"),
                      key=kbase + "notes", **cb)

    pain_now = st.session_state.get(kbase + "pain", int(prev.get("pain") or 0))
    if pain_now >= 5:
        st.error(L("pain_stop"))
    elif pain_now >= 3:
        st.warning(L("pain_modify"))


# ----------------------------------------------------------------------
# PAGE: Today's Workout
# ----------------------------------------------------------------------
def page_workout():
    st.title(L("workout_title"))

    c1, c2, c3 = st.columns([1.2, 1, 1])
    with c1:
        sel_date = st.date_input(L("date"), value=date.today())
    d_week, d_day = db.current_week_and_day(sel_date)
    with c2:
        week = st.selectbox(L("program_week"), [1, 2, 3, 4], index=d_week - 1)
    with c3:
        day = st.selectbox(L("day"), DAYS, index=DAYS.index(d_day),
                           format_func=lambda d: day_label(d, LANG))

    theme_name, theme_desc = week_theme(week, LANG, WEEK_THEMES)
    st.markdown(
        f'<span class="rp-pill">{L("week_word")} {week} — {theme_name}</span>'
        f'<span class="rp-pill">{focus_label(day, DAY_FOCUS[day], LANG)}</span>',
        unsafe_allow_html=True)
    st.caption(theme_desc)

    with st.expander(L("pain_rules_title"), expanded=False):
        pain_traffic_light(compact=True)

    data = db.get_day_program(week, day)
    log_date = sel_date.isoformat()
    existing = db.get_day_logs(log_date)

    # Day progress
    planned = sum(len(s["exercises"]) for s in data["sections"])
    done = sum(1 for v in existing.values()
               if v.get("completed") and v.get("day") == day)
    pct = int(done / planned * 100) if planned else 0
    st.progress(pct / 100,
                text=f"**{done} / {planned} {L('progress_of')} — {pct}% {L('complete_word')}**")

    if day == "Saturday":
        st.info(L("match_day_info"))
    if not data["sections"]:
        st.warning(L("no_program"))
        return

    for section in data["sections"]:
        st.subheader(section_label(section["name"], LANG))
        for ex in section["exercises"]:
            key = (section["name"], ex["name"])
            done_mark = "✅ " if existing.get(key, {}).get("completed") else ""
            label = (f"{done_mark}**{exercise_label(ex, LANG)}**  —  "
                     f"{ex['sets']} × {ex['reps']}  ·  RPE {ex['rpe']}")
            with st.expander(label):
                render_exercise_guide(ex)
                st.divider()
                render_tracker(ex, log_date, week, day, section["name"],
                               existing)

    # ---------------- cardio quick log ----------------
    st.subheader(L("cardio_log"))
    kg = bodyweight_kg()
    with st.form("cardio_form", clear_on_submit=True):
        cc1, cc2, cc3 = st.columns([2, 1, 1])
        act = cc1.selectbox(
            L("activity"), list(CARDIO_MET.keys()),
            format_func=lambda a: CARDIO_AR.get(a, a) if LANG == "ar" else a)
        mins = cc2.number_input(L("minutes"), 1.0, 240.0, 20.0, 1.0)
        sub = cc3.form_submit_button(L("log_cardio"), use_container_width=True)
        if sub:
            kcal = cardio_kcal(CARDIO_MET[act], mins, kg)
            db.add_cardio(log_date, act, mins, round(kcal, 0))
            st.success(f"{L('logged')}: {act} — {mins:.0f} min ≈ {kcal:.0f} kcal")
    cdf = db.cardio_df()
    todays = cdf[cdf["log_date"].dt.date == sel_date] if not cdf.empty else pd.DataFrame()
    if not todays.empty:
        for _, r in todays.iterrows():
            act_disp = CARDIO_AR.get(r["activity"], r["activity"]) \
                if LANG == "ar" else r["activity"]
            cA, cB = st.columns([5, 1])
            cA.markdown(f"• {act_disp} — {r['minutes']:.0f} min ≈ "
                        f"{r['calories']:.0f} kcal")
            if cB.button("🗑", key=f"delc{r['id']}"):
                db.delete_cardio(int(r["id"]))
                st.rerun()

    # ---------------- session summary ----------------
    est = est_strength_kcal(done, kg)
    card_kcal = todays["calories"].sum() if not todays.empty else 0
    m1, m2, m3 = st.columns(3)
    m1.metric(L("session_completion"), f"{pct}%")
    m2.metric(L("est_burn"), f"{est:.0f} kcal")
    m3.metric(L("cardio_burn"), f"{card_kcal:.0f} kcal")


# ----------------------------------------------------------------------
# PAGE: Program overview
# ----------------------------------------------------------------------
def page_program():
    st.title(L("program_title"))
    week = st.radio(
        L("week_word"), [1, 2, 3, 4], horizontal=True,
        format_func=lambda w: f"{L('week_word')} {w} — {week_theme(w, LANG, WEEK_THEMES)[0]}")
    st.info(week_theme(week, LANG, WEEK_THEMES)[1])

    tabs = st.tabs([day_label(d, LANG) for d in DAYS])
    for tab, day in zip(tabs, DAYS):
        with tab:
            data = db.get_day_program(week, day)
            st.markdown(f"**{focus_label(day, data.get('focus', DAY_FOCUS[day]), LANG)}**")
            rows = []
            for s in data.get("sections", []):
                for ex in s["exercises"]:
                    rows.append({
                        L("col_section"): section_label(s["name"], LANG),
                        L("col_exercise"): exercise_label(ex, LANG),
                        L("target"): ex["target"],
                        L("sets"): ex["sets"],
                        L("reps"): ex["reps"],
                        L("tempo"): ex["tempo"],
                        L("rest"): ex["rest"],
                        L("rpe"): ex["rpe"],
                    })
            if rows:
                st.dataframe(pd.DataFrame(rows), use_container_width=True,
                             hide_index=True)
            else:
                st.caption(L("rest_day_caption"))


# ----------------------------------------------------------------------
# PAGE: Progress dashboard
# ----------------------------------------------------------------------
def page_dashboard():
    st.title(L("dash_title"))
    dark = is_dark()
    kg = bodyweight_kg()

    comp = db.completion_by_date()
    tots = db.totals()
    streak = db.workout_streak()

    # ---- stat tiles ----
    monthly_pct = comp["pct"].mean() if not comp.empty else 0
    m = st.columns(5)
    m[0].metric(L("streak"), f"{streak} {L('days_unit')}")
    m[1].metric(L("workouts"), tots["workouts"])
    m[2].metric(L("exercises_done"), tots["exercises"])
    m[3].metric(L("volume_lifted"), f"{tots['volume_kg']:.0f} kg")
    m[4].metric(L("avg_completion"), f"{monthly_pct:.0f}%")

    wdf = db.weight_df()
    if len(wdf) >= 2:
        delta = wdf.iloc[-1]["weight_kg"] - wdf.iloc[0]["weight_kg"]
        weeks = max((wdf.iloc[-1]["log_date"] - wdf.iloc[0]["log_date"]).days / 7, 1)
        f1, f2 = st.columns(2)
        f1.metric(L("body_weight"), f"{wdf.iloc[-1]['weight_kg']:.1f} kg",
                  f"{delta:+.1f} kg {L('since_start')}", delta_color="inverse")
        f2.metric(L("fatloss_pace"), f"{delta / weeks:+.2f} kg/{L('week_word')}",
                  help=L("fatloss_help"))

    st.divider()

    # ---- completion charts ----
    c1, c2 = st.columns(2)
    with c1:
        recent = comp.tail(30) if not comp.empty else comp
        st.plotly_chart(charts.bar(
            recent, "log_date", "pct", L("ch_daily_completion"), "blue",
            "%", dark, pct=True, hover_fmt="%{y:.0f}%"),
            use_container_width=True)
    with c2:
        if not comp.empty:
            wk = comp.copy()
            wk["week_start"] = wk["log_date"].dt.to_period("W").dt.start_time
            wkg = wk.groupby("week_start", as_index=False)["pct"].mean()
        else:
            wkg = comp
        st.plotly_chart(charts.bar(
            wkg, "week_start", "pct", L("ch_weekly_completion"), "blue",
            "%", dark, pct=True, hover_fmt="%{y:.0f}%"),
            use_container_width=True)

    # ---- pain + body weight ----
    c3, c4 = st.columns(2)
    with c3:
        st.plotly_chart(charts.pain_chart(db.pain_trend_df(), dark,
                                          title=L("ch_pain")),
                        use_container_width=True)
    with c4:
        st.plotly_chart(charts.weight_chart(wdf, dark, title=L("ch_weight")),
                        use_container_width=True)

    # ---- calories + cardio ----
    cdf = db.cardio_df()
    ldf = db.logs_df()
    cal_rows = {}
    if not ldf.empty:
        done = ldf[ldf["completed"] == 1]
        for d, n in done.groupby(done["log_date"].dt.date).size().items():
            cal_rows[d] = cal_rows.get(d, 0) + est_strength_kcal(n, kg)
    if not cdf.empty:
        for d, s in cdf.groupby(cdf["log_date"].dt.date)["calories"].sum().items():
            cal_rows[d] = cal_rows.get(d, 0) + s
    cal_df = (pd.DataFrame({"log_date": pd.to_datetime(list(cal_rows)),
                            "kcal": list(cal_rows.values())})
              .sort_values("log_date") if cal_rows else pd.DataFrame())

    c5, c6 = st.columns(2)
    with c5:
        st.plotly_chart(charts.bar(
            cal_df, "log_date", "kcal", L("ch_calories"), "orange", "kcal",
            dark, hover_fmt="%{y:.0f} kcal"), use_container_width=True)
    with c6:
        if not cdf.empty:
            mins = (cdf.groupby(cdf["log_date"].dt.to_period("W").dt.start_time)
                    ["minutes"].sum().reset_index())
            mins.columns = ["week_start", "minutes"]
        else:
            mins = pd.DataFrame()
        st.plotly_chart(charts.bar(
            mins, "week_start", "minutes", L("ch_cardio_min"), "aqua",
            "min", dark, hover_fmt="%{y:.0f} min"), use_container_width=True)

    # ---- recovery-linked charts ----
    rdf = db.recovery_df()
    c7, c8 = st.columns(2)
    with c7:
        steps = rdf[rdf["steps"].notna()] if not rdf.empty else pd.DataFrame()
        st.plotly_chart(charts.bar(
            steps, "log_date", "steps", L("ch_steps"), "aqua", "",
            dark, hover_fmt="%{y:,.0f}"), use_container_width=True)
    with c8:
        rec = rdf[rdf["recovery_score"].notna()] if not rdf.empty else pd.DataFrame()
        st.plotly_chart(charts.line(
            rec, "log_date", "recovery_score", L("ch_recovery"),
            "violet", "/10", dark, y_range=[0, 10.5],
            hover_fmt="%{y:.0f}/10"), use_container_width=True)


# ----------------------------------------------------------------------
# PAGE: Recovery tracker
# ----------------------------------------------------------------------
def page_recovery():
    st.title(L("recovery_title"))
    dark = is_dark()
    sel_date = st.date_input(L("date"), value=date.today(), key="rec_date")
    log_date = sel_date.isoformat()
    prev = db.get_recovery(log_date) or {}

    with st.form("recovery_form"):
        c1, c2, c3, c4 = st.columns(4)
        sleep = c1.number_input(L("sleep_h"), 0.0, 14.0,
                                float(prev.get("sleep_hours") or 7.0), 0.5)
        water = c2.number_input(L("water_l"), 0.0, 10.0,
                                float(prev.get("water_l") or 2.0), 0.25)
        protein = c3.number_input(L("protein_g"), 0.0, 400.0,
                                  float(prev.get("protein_g") or 120.0), 5.0,
                                  help=L("protein_help"))
        steps = c4.number_input(L("steps"), 0, 60000,
                                int(prev.get("steps") or 8000), 500)
        c5, c6, c7, c8 = st.columns(4)
        soreness = c5.slider(L("soreness_s"), 1, 10,
                             int(prev.get("soreness") or 3))
        energy = c6.slider(L("energy_s"), 1, 10,
                           int(prev.get("energy") or 7))
        rec_score = c7.slider(L("recscore_s"), 1, 10,
                              int(prev.get("recovery_score") or 7),
                              help=L("recscore_help"))
        football = c8.slider(L("football_s"), 1, 10,
                             int(prev.get("football_rating") or 5),
                             help=L("football_help"))
        c9, c10 = st.columns([2, 1])
        notes = c9.text_input(L("notes"), value=prev.get("notes") or "",
                              placeholder=L("rec_notes_ph"))
        bw = c10.number_input(L("bw_kg"), 40.0, 150.0, bodyweight_kg(), 0.1)
        if st.form_submit_button(L("save_recovery"), use_container_width=True):
            db.upsert_recovery(log_date, sleep_hours=sleep, water_l=water,
                               protein_g=protein, steps=steps,
                               soreness=soreness, energy=energy,
                               recovery_score=rec_score,
                               football_rating=football, notes=notes)
            db.upsert_weight(log_date, bw)
            st.success(L("recovery_saved"))

    # readiness hint
    if soreness >= 7 or sleep < 6:
        st.warning(L("readiness_warn"))

    st.divider()
    rdf = db.recovery_df()
    if rdf.empty:
        st.caption(L("rec_empty"))
        return
    c1, c2 = st.columns(2)
    with c1:
        st.plotly_chart(charts.line(rdf, "log_date", "sleep_hours",
                                    L("ch_sleep"), "violet", "h", dark,
                                    hover_fmt="%{y:.1f} h"),
                        use_container_width=True)
        st.plotly_chart(charts.line(rdf, "log_date", "soreness",
                                    L("ch_soreness"), "red", "/10",
                                    dark, y_range=[0, 10.5],
                                    hover_fmt="%{y:.0f}/10"),
                        use_container_width=True)
    with c2:
        st.plotly_chart(charts.line(rdf, "log_date", "energy",
                                    L("ch_energy"), "yellow", "/10", dark,
                                    y_range=[0, 10.5],
                                    hover_fmt="%{y:.0f}/10"),
                        use_container_width=True)
        fb = rdf[rdf["football_rating"].notna()]
        st.plotly_chart(charts.line(fb, "log_date", "football_rating",
                                    L("ch_football"), "aqua",
                                    "/10", dark, y_range=[0, 10.5],
                                    hover_fmt="%{y:.0f}/10"),
                        use_container_width=True)


# ----------------------------------------------------------------------
# PAGE: Edit mode
# ----------------------------------------------------------------------
def _editable_fields():
    return [
        ("name", L("f_name")), ("target", L("f_target")),
        ("purpose", L("f_purpose")), ("sets", L("sets")),
        ("reps", L("reps")), ("tempo", L("tempo")), ("rest", L("rest")),
        ("rpe", L("rpe")), ("equipment", L("equipment")),
        ("safety", L("f_safety")), ("image_url", L("f_image")),
        ("gif_url", L("f_gif")), ("video_url", L("f_video")),
        ("youtube", L("f_youtube")),
    ]


def page_edit():
    st.title(L("edit_title"))
    st.caption(L("edit_caption"))

    c1, c2 = st.columns(2)
    week = c1.selectbox(
        L("week_word"), [1, 2, 3, 4],
        format_func=lambda w: f"{L('week_word')} {w} — {week_theme(w, LANG, WEEK_THEMES)[0]}")
    day = c2.selectbox(L("day"), DAYS,
                       format_func=lambda d: day_label(d, LANG))
    data = db.get_day_program(week, day)

    if not data["sections"]:
        st.warning(L("no_sections"))
    section_names = [s["name"] for s in data["sections"]]

    # ---------------- edit / delete / replace ----------------
    for si, section in enumerate(data["sections"]):
        st.subheader(section_label(section["name"], LANG))
        for ei, ex in enumerate(section["exercises"]):
            with st.expander(f"{exercise_label(ex, LANG)}  ·  "
                             f"{ex['sets']} × {ex['reps']}"):
                cols = st.columns(2)
                edited = {}
                for fi, (field, label) in enumerate(_editable_fields()):
                    with cols[fi % 2]:
                        val = ex.get(field, "")
                        if field == "sets":
                            edited[field] = st.number_input(
                                label, 1, 10, int(val or 1),
                                key=f"e{week}{day}{si}{ei}{field}")
                        else:
                            edited[field] = st.text_input(
                                label, str(val),
                                key=f"e{week}{day}{si}{ei}{field}")
                notes_field = st.text_area(
                    L("exec_notes"), ex.get("execution", ""),
                    key=f"e{week}{day}{si}{ei}exec")

                b1, b2, b3 = st.columns(3)
                if b1.button(L("save_changes"), key=f"sv{week}{day}{si}{ei}",
                             use_container_width=True):
                    ex.update(edited)
                    ex["execution"] = notes_field
                    db.save_day_program(week, day, data)
                    st.success(L("saved"))
                    st.rerun()
                if b2.button(L("delete_ex"), key=f"dl{week}{day}{si}{ei}",
                             use_container_width=True):
                    section["exercises"].pop(ei)
                    db.save_day_program(week, day, data)
                    st.rerun()
                repl = b3.selectbox(
                    L("replace_with"), ["—"] + sorted(
                        EXERCISES, key=lambda k: EXERCISES[k]["name"]),
                    format_func=lambda k: (
                        exercise_label({"id": k, "name": EXERCISES[k]["name"]}, LANG)
                        if k in EXERCISES else k),
                    key=f"rp{week}{day}{si}{ei}")
                if repl != "—":
                    if st.button(L("confirm_replace"),
                                 key=f"rpb{week}{day}{si}{ei}",
                                 use_container_width=True):
                        import copy as _copy
                        new_ex = _copy.deepcopy(EXERCISES[repl])
                        new_ex["id"] = repl
                        new_ex["section"] = section["name"]
                        section["exercises"][ei] = new_ex
                        db.save_day_program(week, day, data)
                        st.rerun()

    # ---------------- add exercise ----------------
    st.divider()
    st.subheader(L("add_exercise"))
    a1, a2, a3 = st.columns([1.5, 1.5, 1])
    with a1:
        target_sec = st.selectbox(
            L("into_section"), section_names or ["Strength"],
            format_func=lambda s: section_label(s, LANG))
    with a2:
        new_id = st.selectbox(
            L("from_library"),
            sorted(EXERCISES, key=lambda k: EXERCISES[k]["name"]),
            format_func=lambda k: exercise_label(
                {"id": k, "name": EXERCISES[k]["name"]}, LANG))
    with a3:
        st.write("")
        st.write("")
        if st.button(L("add_btn"), use_container_width=True):
            import copy as _copy
            new_ex = _copy.deepcopy(EXERCISES[new_id])
            new_ex["id"] = new_id
            new_ex["section"] = target_sec
            for s in data["sections"]:
                if s["name"] == target_sec:
                    s["exercises"].append(new_ex)
            db.save_day_program(week, day, data)
            st.rerun()

    # ---------------- reset ----------------
    st.divider()
    with st.expander(L("reset_options")):
        st.warning(L("reset_warning"))
        r1, r2 = st.columns(2)
        confirm = st.checkbox(L("reset_confirm"))
        if r1.button(L("reset_day"), disabled=not confirm,
                     use_container_width=True):
            from program import default_program
            db.save_day_program(week, day, default_program()[week][day])
            st.rerun()
        if r2.button(L("reset_all"), disabled=not confirm,
                     use_container_width=True):
            db.seed_program_if_missing(force=True)
            st.rerun()


# ----------------------------------------------------------------------
# PAGE: Safety guide
# ----------------------------------------------------------------------
def page_safety():
    st.title(L("safety_title"))
    st.subheader(L("traffic_header"))
    pain_traffic_light()
    st.subheader(L("knee_header"))
    st.markdown(L("knee_md"))
    st.subheader(L("shoulder_header"))
    st.markdown(L("shoulder_md"))
    st.subheader(L("reassess_header"))
    st.markdown(L("reassess_md"))
    st.subheader(L("load_header"))
    st.markdown(L("load_md"))


# ----------------------------------------------------------------------
# PAGE: Settings
# ----------------------------------------------------------------------
def page_settings():
    st.title(L("settings_title"))
    st.subheader(L("program_calendar"))
    start = db.get_start_date()
    new_start = st.date_input(L("start_date_label"), value=start,
                              help=L("start_date_help"))
    if new_start != start:
        db.set_setting("start_date", new_start.isoformat())
        st.success(L("start_date_set"))

    st.subheader(L("profile"))
    w = st.number_input(L("current_bw"), 40.0, 150.0, bodyweight_kg(), 0.1)
    if st.button(L("save_weight")):
        db.set_setting("profile_weight", w)
        db.upsert_weight(date.today().isoformat(), w)
        st.success(L("saved"))
    st.caption(L("profile_line"))

    st.subheader(L("appearance"))
    st.markdown(L("appearance_note"))

    st.subheader(L("export"))
    for label, df in [(L("dl_workouts"), db.logs_df()),
                      (L("dl_recovery"), db.recovery_df()),
                      (L("dl_weight"), db.weight_df()),
                      (L("dl_cardio"), db.cardio_df())]:
        if not df.empty:
            st.download_button(f"⬇ {label} (CSV)",
                               df.to_csv(index=False).encode("utf-8-sig"),
                               file_name=f"{label.replace(' ', '_')}.csv",
                               mime="text/csv")
    st.caption(L("export_note"))


# ----------------------------------------------------------------------
# Navigation
# ----------------------------------------------------------------------
def _set_lang():
    st.session_state.lang = st.session_state["_lang_widget"]
    db.set_setting("lang", st.session_state.lang)


with st.sidebar:
    st.markdown(f"## {L('app_title')}")
    st.caption(L("app_tagline"))
    st.selectbox(L("language"), list(LANGS.keys()),
                 index=list(LANGS.keys()).index(LANG),
                 format_func=lambda k: LANGS[k],
                 key="_lang_widget", on_change=_set_lang)
    nav_items = ["nav_workout", "nav_program", "nav_dashboard",
                 "nav_recovery", "nav_edit", "nav_safety", "nav_settings"]
    page = st.radio("Navigate", nav_items, format_func=L,
                    label_visibility="collapsed")
    st.divider()
    _streak = db.workout_streak()
    _tots = db.totals()
    st.metric(L("streak"), f"{_streak} {L('days_unit')}")
    st.metric(L("workouts_completed"), _tots["workouts"])
    wk, dy = db.current_week_and_day()
    st.caption(f"{L('today_is')}: **{L('week_word')} {wk} — "
               f"{week_theme(wk, LANG, WEEK_THEMES)[0]}**, {day_label(dy, LANG)}\n\n"
               f"{focus_label(dy, DAY_FOCUS[dy], LANG)}")
    st.divider()
    st.caption(L("traffic_mini"))

PAGES = {
    "nav_workout": page_workout,
    "nav_program": page_program,
    "nav_dashboard": page_dashboard,
    "nav_recovery": page_recovery,
    "nav_edit": page_edit,
    "nav_safety": page_safety,
    "nav_settings": page_settings,
}
PAGES[page]()
