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
| 1 | Load | Strength days at RPE 7 while working weights are set; balance days on stable ground |
| 2 | Progress | Heavier strength days; balance progresses to eyes-closed holds and head turns |
| 3 | Advanced | Top loads (RPE 8); reactive balance — ball tosses, cushion stands, bigger landings |
| 4 | Peak + Retest | Strength tests Monday (wall-sit, calf); balance battery Thursday (Y-balance, hop, plank) |

**Strength / balance alternating rhythm (current)** — the physiotherapy
pattern of one strength day followed by one balance day, focused on the
three priority areas (shoulders, legs, knees), dumbbells & machines only:
Mon **Leg & Knee Strength** (leg press, hack squat, Bulgarians, leg
extension/curl, calves + Nordics, Copenhagens, box jumps) · Tue
**Balance & Stability** (single-leg balance progressions, Y-reaches,
single-leg RDLs, TKE + wall slides, cuff work, YTW) · Wed **Shoulder
Strength** (DB press, lateral raises, rows, rear-delt fly, face pulls,
shrugs + cuff block) · Thu **Balance & Control** (hop-and-stick landings,
reactive balance, closed-chain shoulder work, footwork) · Fri recovery ·
Sat football · Sun recovery + mobility. Leg strength sits five days
before the match; Thursday's balance work is deliberately low-load.
Standing guardrails: no behind-the-neck work, no dips, no barbell bench,
pressing depth capped, step-down box jumps, Nordics never within 48 h of
a match.

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
- **📸 Real exercise photos** — 90 of the 125 exercises show real
  start/finish demonstration photos (public-domain, from the
  [free-exercise-db](https://github.com/yuhonas/free-exercise-db)
  project) in both the grid cards and the exercise guide; rehab-specific
  drills keep the built-in illustrations.
- **🔄 Next-block generator** — in Settings, once Week 4's benchmarks are
  logged, one tap generates the next 4-week block: same split with rep
  schemes shifted a gear toward strength, a personalised suggested start
  load stamped on every exercise you logged a weight for (with a pain
  guard that keeps suggestions conservative when recent pain averaged
  ≥3/10), and a recap of your latest test results.
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
