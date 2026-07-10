# ⚽ Rehab & Performance · التأهيل والأداء

A professional **bilingual (English / العربية)** rehabilitation and
performance training platform built with
**Python + Streamlit + SQLite + Plotly**, tailored for a 34-year-old
weekend footballer managing:

- a **partial ACL tear** (conservative management, cleared to train), and
- a **previously dislocated right shoulder** with suspected labral injury.

It automatically generates a safe, progressive, evidence-based **one-month
program**, lets you follow it day by day with full visual guidance, and
tracks everything — completion, pain, weight, recovery, calories — in a
local SQLite database that remembers everything between sessions.

## Quick start

```bash
pip install -r requirements.txt
streamlit run app.py
```

Open the URL Streamlit prints (works great on iPhone via your computer's
local network address). The app uses **one fixed theme**: an energetic,
motivation-focused light look — bold orange accents, a daily motivational
quote banner, and a fiery progress bar — designed to keep you fired up
during training.

**Session flow:** every training day starts with a **20-minute cardio
warm-up (bike or easy run — your choice)**, then mobility, activation,
the weighted work, core/balance, and stretching. The tracker also shows a
**"Last time"** hint per exercise (previous weight, sets × reps, pain) so
you always know what to load next.

## The program

| Week | Theme | Emphasis |
|------|-------|----------|
| 1 | Advanced Load | Front squat, seated DB shoulder press, pull-ups, box jumps and sprint strides enter at RPE 7 |
| 2 | Overload | Heavier bars (RPE 7–8); walking lunges, barbell rows, single-leg press, long-lever Copenhagens join |
| 3 | Power | Peak loading: front squat 5×5, trap-bar triples, highest box jumps, skater bounds, strides at 85% |
| 4 | Peak + Retest | Reduced volume + benchmark battery: wall-sit, calf raises, plank, Y-balance, single-leg hop, max strict pull-ups |

**Built for the gym:** the program is loaded with real weights — leg press,
leg extension (limited arc), seated leg curl, barbell RDL, trap-bar
deadlift, barbell hip thrust, Smith/seated calf machines, hip
adduction/abduction machines, lat pulldown, seated cable row, dumbbell
bench (neutral grip, capped depth), chest press machine, cable face pulls,
cable external rotations, reverse pec-deck and cable Pallof presses —
every one selected and range-restricted to stay safe for a partial-ACL
knee and a post-dislocation shoulder.

**Advanced block (current):** built for a trained athlete (4+ months in
the gym) — front squats, seated DB shoulder presses, pull-ups, barbell
rows, lateral raises, walking lunges, hack squats, single-leg press, box
jumps, skater bounds and sprint strides, with strict quality gates on all
power work. Standing guardrails: no behind-the-neck work, no dips, no
barbell bench, pressing depth capped, pull-up bottoms stay active.

**Weekly schedule:** Mon lower-body strength & power · Tue upper body &
shoulder building · Wed posterior chain (hamstrings/glutes) · Thu speed,
power & football prep · Fri recovery · Sat football (pre-match activation
+ post-match reset) · Sun recovery + mobility.

Every exercise includes: target muscle, purpose, sets/reps/tempo/rest/RPE,
starting position, execution, coaching cues, tips, common mistakes,
injury-specific safety notes, progression/regression/alternative, a
built-in movement illustration, and a YouTube demonstration link (Edit Mode
lets you pin a specific video, GIF or picture, which the app embeds).

## Features

- **🏋️ Today's Workout** — auto-selects the right week/day from your start
  date; **grid view** (default) shows every exercise of the day as a card
  with its illustration and prescription — tap Open for the full guide +
  tracker in a popup — or switch to the classic list view; per-exercise
  tracker (completion checkbox, weight, pain 0–10, difficulty, energy,
  sets/reps done, notes) that **auto-saves on change**; live pain-rule
  warnings; cardio log with MET-based calorie estimates.
- **📅 Monthly Program** — full month overview, per week and day.
- **📈 Progress Dashboard** — streak, totals, training volume, daily/weekly
  completion, pain trend with modify/stop guide-lines, body-weight and
  fat-loss pace, calories burned, cardio minutes, steps, recovery score.
- **😴 Recovery Tracker** — sleep, water, protein, steps, soreness, energy,
  recovery score, football performance rating, with trend charts and
  readiness warnings.
- **✏️ Edit Mode** — add / delete / replace exercises, edit sets, reps and
  notes, attach your own pictures / GIFs / videos / YouTube links; reset
  to the generated program at any time (history is never touched).
- **🛟 Safety Guide** — the pain traffic light (0–2 continue · 3–4 modify ·
  5+ stop), knee and shoulder-specific rules, and reassessment red flags.
- **⚙️ Settings** — program start date, profile weight, CSV export.
- **🌐 Arabic language option** — a sidebar switcher (English / العربية)
  translates the entire interface, exercise names, section names, week
  themes, day focuses and the full safety guide, and flips the layout to
  right-to-left. The choice persists between sessions. Logs stay keyed on
  stable English identifiers, so your history is safe when switching.

## Storage

Everything lives in `gym_rehab.db` (SQLite) next to the app: program
edits, workout history, pain scores, body weight, recovery data, cardio
log. Delete the file to start completely fresh.

## Disclaimer

This program follows evidence-based conservative-rehab principles but is
not a substitute for in-person medical care. The built-in safety rules are
strict on purpose — respect the traffic light, and reassess with your
physiotherapist if red flags appear.
