"""
program.py
==========
STRENGTH / BALANCE ALTERNATING BLOCK — the specialist's rhythm the user
trained with before: one day strength, the next day balance & stability,
focused on the three priority areas (shoulders, legs, knees).
Dumbbells & machines only.

  Mon  LEG & KNEE STRENGTH   (heavy legs + knee armour + jumps)
  Tue  BALANCE & STABILITY   (knee proprioception + shoulder stability)
  Wed  SHOULDER STRENGTH     (presses, raises, rows, cuff — the rows and
                              face pulls ARE shoulder protection)
  Thu  BALANCE & CONTROL     (landing mechanics, reactive balance,
                              closed-chain shoulder work, footwork)
  Fri  Recovery
  Sat  Football (pre-match activation + post-match reset)
  Sun  Recovery + Mobility

Leg strength sits on Monday: five full days before Saturday's match, so
heavy legs and Nordics never steal match sharpness. Thursday's balance
work is deliberately low-load — it sharpens the knee without costing
anything two days out.

Four-week wave:
  Week 1 – Load      (strength grooved at RPE 7; balance on stable ground)
  Week 2 – Progress  (heavier strength; balance with eyes closed / head turns)
  Week 3 – Advanced  (top loads; perturbation balance + bigger landings)
  Week 4 – Peak + Retest (benchmarks on both sides: strength tests Monday,
           balance battery Thursday)

Standing guardrails (independent of training age):
- dumbbells and machines only — no barbell work in this block
- no behind-the-neck pressing/pulling, no dips, pressing depth capped
- jumps/bounds/landings only fresh and pain-free; box jumps stepped down
- Nordics never within 48 h of a match (Monday placement guarantees it)

The materialised program (library data + weekly prescription overrides)
is what gets seeded into SQLite; Edit Mode then owns it.
"""

import copy

from exercise_library import EXERCISES

DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday",
        "Saturday", "Sunday"]

TRAINING_DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday"]

WEEK_THEMES = {
    1: ("Load",
        "The specialist rhythm returns: strength one day, balance the "
        "next. Strength days open at RPE 7 while you set your working "
        "weights; balance days start on stable ground, eyes open — "
        "quality of control is the score."),
    2: ("Progress",
        "Strength days get heavier (RPE 7-8). Balance days progress the "
        "challenge instead of the load: eyes-closed holds, head turns "
        "and longer single-leg reaches."),
    3: ("Advanced",
        "Top strength week (RPE 8) — and the balance days turn reactive: "
        "ball tosses, cushion stands, bigger hop-and-stick landings. "
        "Control decides every progression."),
    4: ("Peak + Retest",
        "Volume drops and both sides get measured: wall-sit and calf "
        "tests on strength Monday; Y-balance, single-leg hop and plank "
        "on balance Thursday. Beat last block's numbers."),
}

# Friendly names for the day focus
DAY_FOCUS = {
    "Monday":    "Leg & Knee Strength — Heavy Day",
    "Tuesday":   "Balance & Stability — Knee + Shoulder",
    "Wednesday": "Shoulder Strength — Heavy Day",
    "Thursday":  "Balance & Control — Landings + Reactive",
    "Friday":    "Recovery Day",
    "Saturday":  "Football Match Day",
    "Sunday":    "Recovery + Mobility",
}


def _mat(ex_id, section, **ov):
    """Materialise one exercise: library data + weekly overrides."""
    ex = copy.deepcopy(EXERCISES[ex_id])
    ex["id"] = ex_id
    ex["section"] = section
    for k, v in ov.items():
        ex[k] = v
    return ex


def _day(title, sections):
    """sections: list of (section_name, [item, ...]) where item is
    ex_id or (ex_id, override_dict)."""
    out = {"focus": title, "sections": []}
    for sec_name, items in sections:
        mat_items = []
        for it in items:
            if isinstance(it, tuple):
                mat_items.append(_mat(it[0], sec_name, **it[1]))
            else:
                mat_items.append(_mat(it, sec_name))
        out["sections"].append({"name": sec_name, "exercises": mat_items})
    return out


# ---------------------------------------------------------------------
# Shared day templates (recovery / football)
# ---------------------------------------------------------------------
def _friday(week):
    extra = [("incline_walk", {"reps": "20 min easy", "rpe": "4",
                               "purpose": "Optional gentle flush walk — skip "
                               "if legs feel heavy before tomorrow's match."})]
    return _day(DAY_FOCUS["Friday"], [
        ("Soft Tissue & Mobility", [
            "foam_roll_quads", "cat_cow", "open_book", "worlds_greatest"]),
        ("Keep-The-Knee-Awake (pain-free, light)", [
            ("quad_set_ssq", {"sets": 1, "rpe": "3"}),
            ("sl_balance", {"sets": 2, "reps": "30 s/side", "rpe": "3"})]),
        ("Optional Easy Movement", extra),
        ("Downshift", ["breathing_reset"]),
    ])


def _saturday(week):
    return _day(DAY_FOCUS["Saturday"], [
        ("Pre-Match Activation (15 min before kickoff warm-up)", [
            ("leg_swings", {"sets": 1}),
            ("lateral_leg_swings", {"sets": 1}),
            ("glute_bridge", {"sets": 1, "reps": "10", "rpe": "4"}),
            ("band_walk", {"sets": 1, "reps": "8 steps/direction", "rpe": "5",
                           "safety": "If you have no band at the pitch, do 10 "
                           "lateral lunges per side instead."}),
            ("shadow_footwork", {"reps": "3-4 min build-up", "rpe": "5-6"}),
        ]),
        ("Post-Match Reset (within 30 min of full-time)", [
            ("stretch_quad", {}),
            ("stretch_hamstring", {}),
            ("stretch_hip_flexor", {}),
            ("breathing_reset", {}),
        ]),
    ])


def _sunday(week):
    return _day(DAY_FOCUS["Sunday"], [
        ("Gentle Cardio Flush", [
            ("incline_walk", {"reps": "20-30 min easy pace", "rpe": "3-4"})]),
        ("Full-Body Mobility Flow", [
            "cat_cow", "worlds_greatest", "open_book", "ankle_rocks"]),
        ("Long Stretch Series", [
            "stretch_quad", "stretch_hamstring", "stretch_hip_flexor",
            "stretch_glute", "stretch_calf", "stretch_chest",
            "cross_body_stretch"]),
        ("Soft Tissue + Downshift", [
            "foam_roll_quads", "breathing_reset"]),
    ])


# ---------------------------------------------------------------------
# MONDAY — LEG & KNEE STRENGTH (heavy)
# ---------------------------------------------------------------------
def _leg_strength_day(week):
    w = week
    sections = [
        ("Warm-Up", ["cardio_warmup_20"]),
        ("Mobility", ["ankle_rocks", "worlds_greatest"]),
        ("Activation", [
            ("glute_bridge", {"sets": 2, "reps": "10"}),
            ("band_walk", {"sets": 2})]),
    ]
    if w == 4:
        sections.append(("Assessment", [
            ("assess_wall_sit", {}),
            ("assess_sl_calf", {})]))
    else:
        sections.append(("Power & Plyometrics (fresh)", [
            ("box_jump", {"sets": 2 + w, "reps": "3",
                          "rpe": "7" if w == 1 else "7-8" if w == 2 else "8",
                          "purpose": {1: "Knee-height box, quiet landings, "
                                         "always step down.",
                                      2: "One height up if every Week-1 "
                                         "landing was quiet.",
                                      3: "Peak jump week — highest box you "
                                         "land QUIETLY on."}[w]})]))
    strength = {
        1: [("leg_press", {"sets": 4, "reps": "10", "rpe": "7"}),
            ("hack_squat", {"sets": 3, "reps": "10", "rpe": "7"}),
            ("rfe_split_squat", {"sets": 3, "reps": "8/side", "rpe": "7",
                                 "equipment": "Bench + dumbbells"}),
            ("leg_curl_machine", {"sets": 3, "reps": "10", "rpe": "7-8"}),
            ("smith_calf", {"sets": 4, "reps": "10", "rpe": "7"})],
        2: [("leg_press", {"sets": 4, "reps": "8", "rpe": "7-8"}),
            ("single_leg_press", {"sets": 3, "reps": "8/side", "rpe": "7-8",
                                  "purpose": "Close the left-right gap — "
                                  "weak side first."}),
            ("romanian_deadlift", {"sets": 3, "reps": "8", "rpe": "7-8",
                                   "equipment": "Heavy dumbbells"}),
            ("leg_curl_machine", {"sets": 3, "reps": "10", "rpe": "8"}),
            ("seated_calf_machine", {"sets": 3, "reps": "12-15", "rpe": "7-8"})],
        3: [("hack_squat", {"sets": 4, "reps": "8", "rpe": "8",
                            "purpose": "Top leg week — heaviest guided "
                            "squatting of the block."}),
            ("leg_press", {"sets": 3, "reps": "8", "rpe": "8"}),
            ("walking_lunge", {"sets": 3, "reps": "10 steps/side", "rpe": "8",
                               "equipment": "Heavier dumbbells"}),
            ("romanian_deadlift", {"sets": 3, "reps": "8", "rpe": "8",
                                   "equipment": "Heavy dumbbells"}),
            ("smith_calf", {"sets": 4, "reps": "8-10", "rpe": "8"})],
        4: [("leg_press", {"sets": 3, "reps": "10", "rpe": "7",
                           "purpose": "Moderate plates on test day — "
                           "smooth reps only."}),
            ("leg_curl_machine", {"sets": 2, "reps": "10-12", "rpe": "7"}),
            ("smith_calf", {"sets": 3, "reps": "10", "rpe": "7"})],
    }[w]
    rehab = {
        1: [("leg_extension", {"sets": 3, "reps": "12", "rpe": "7"}),
            ("nordic_curl", {"sets": 3, "reps": "5", "rpe": "8"}),
            ("copenhagen", {"sets": 2, "reps": "20 s/side", "rpe": "7"})],
        2: [("leg_extension", {"sets": 3, "reps": "12", "rpe": "7-8"}),
            ("nordic_curl", {"sets": 3, "reps": "6", "rpe": "8"}),
            ("copenhagen", {"sets": 2, "reps": "15-20 s/side", "rpe": "8",
                            "setup": "Progress to the LONG lever: the top "
                            "FOOT (not the knee) rests on the bench."})],
        3: [("leg_extension", {"sets": 3, "reps": "10-12", "rpe": "8"}),
            ("nordic_curl", {"sets": 3, "reps": "6-8", "rpe": "8"}),
            ("copenhagen", {"sets": 2, "reps": "20-25 s/side", "rpe": "8",
                            "setup": "Long lever (foot on the bench)."})],
        4: [("nordic_curl", {"sets": 2, "reps": "5-6", "rpe": "8",
                             "safety": "Reduced volume on test week; never "
                             "the day before football."}),
            ("copenhagen", {"sets": 2, "reps": "20 s/side", "rpe": "7",
                            "setup": "Long lever (foot on the bench)."})],
    }[w]
    sections += [
        ("Strength", strength),
        ("Rehabilitation", rehab),
        ("Cool-Down & Stretch", [
            "stretch_quad", "stretch_hamstring", "stretch_calf",
            "breathing_reset"]),
    ]
    return _day(DAY_FOCUS["Monday"], sections)


# ---------------------------------------------------------------------
# TUESDAY — BALANCE & STABILITY (knee proprioception + shoulder stability)
# ---------------------------------------------------------------------
def _balance_stability_day(week):
    w = week
    knee_balance = {
        1: [("sl_balance", {"sets": 3, "reps": "30 s/side", "rpe": "5",
                            "purpose": "Week 1: stable ground, eyes open — "
                            "own the quiet stand first."}),
            ("sl_reach", {"sets": 2}),
            ("single_leg_rdl", {"sets": 2, "reps": "6/side", "rpe": "6",
                                "equipment": "Light dumbbell",
                                "purpose": "Balance-focused here: slow, "
                                "perfect, light."}),
            ("tke", {"sets": 2}),
            ("wall_sit", {"sets": 2, "reps": "40 s", "rpe": "6"})],
        2: [("sl_balance", {"sets": 3, "reps": "30 s/side, eyes CLOSED",
                            "rpe": "6",
                            "purpose": "Progression: eyes closed — the "
                            "knee's sensors must do all the work."}),
            ("sl_reach", {"sets": 2, "reps": "5 reaches × 3 directions/side, "
                          "longer reaches"}),
            ("single_leg_rdl", {"sets": 3, "reps": "6/side", "rpe": "6-7",
                                "equipment": "Light dumbbell"}),
            ("tke", {"sets": 2}),
            ("wall_sit", {"sets": 3, "reps": "45 s", "rpe": "6-7"})],
        3: [("sl_balance_perturb", {"sets": 3, "reps": "30 s/side",
                                    "purpose": "Reactive week: ball tosses "
                                    "and head turns; add a folded towel "
                                    "underfoot on the last set."}),
            ("sl_reach", {"sets": 2, "equipment": "Dumbbell at chest"}),
            ("single_leg_rdl", {"sets": 3, "reps": "6-8/side", "rpe": "7",
                                "equipment": "Moderate dumbbell"}),
            ("lateral_step_up", {"sets": 2, "reps": "8/side", "rpe": "6-7",
                                 "purpose": "Control focus: slow lowering, "
                                 "frozen pelvis — this is a balance "
                                 "exercise wearing a strength costume."}),
            ("spanish_squat", {"sets": 2, "reps": "40 s iso hold", "rpe": "7"})],
        4: [("sl_balance_perturb", {"sets": 2, "reps": "30 s/side",
                                    "rpe": "6"}),
            ("sl_reach", {"sets": 2}),
            ("single_leg_rdl", {"sets": 2, "reps": "6/side", "rpe": "6",
                                "equipment": "Light dumbbell"}),
            ("wall_sit", {"sets": 2, "reps": "40 s", "rpe": "6"})],
    }[w]
    shoulder_stab = {
        1: [("wall_slide", {"sets": 2}),
            ("scap_pushup", {"sets": 2, "reps": "12"}),
            ("band_er", {"sets": 3, "rpe": "6"}),
            ("band_ir", {"sets": 3, "rpe": "6"}),
            ("bird_dog", {"sets": 2})],
        2: [("wall_slide", {"sets": 2, "equipment": "Mini-band around wrists"}),
            ("scap_pushup", {"sets": 2, "reps": "12"}),
            ("band_er_90", {"sets": 2, "reps": "12", "rpe": "6-7"}),
            ("band_ir", {"sets": 3, "rpe": "6-7"}),
            ("prone_ytw", {"sets": 2})],
        3: [("wall_slide", {"sets": 2, "equipment": "Mini-band around wrists"}),
            ("band_er_90", {"sets": 3, "reps": "12", "rpe": "7"}),
            ("cable_er", {"sets": 2, "rpe": "7"}),
            ("prone_ytw", {"sets": 2}),
            ("bird_dog", {"sets": 2, "reps": "10/side"})],
        4: [("wall_slide", {"sets": 2}),
            ("band_er", {"sets": 2, "rpe": "6"}),
            ("band_ir", {"sets": 2, "rpe": "6"}),
            ("prone_ytw", {"sets": 2,
                           "purpose": "Deload week — quality letters, "
                           "gravity only."})],
    }[w]
    return _day(DAY_FOCUS["Tuesday"], [
        ("Warm-Up", ["cardio_warmup_20"]),
        ("Mobility", ["cat_cow", "open_book"]),
        ("Balance", knee_balance),
        ("Shoulder Rehabilitation", shoulder_stab),
        ("Core", [
            ("pallof_press", {"sets": 3}),
            ("side_plank", {"sets": 2, "reps": "30-40 s/side", "rpe": "6-7"})]),
        ("Cool-Down & Stretch", [
            "stretch_glute", "stretch_chest", "breathing_reset"]),
    ])


# ---------------------------------------------------------------------
# WEDNESDAY — SHOULDER STRENGTH (heavy)
# ---------------------------------------------------------------------
def _shoulder_strength_day(week):
    w = week
    strength = {
        1: [("db_shoulder_press", {"sets": 4, "reps": "8", "rpe": "7",
                                   "purpose": "The day's anchor lift — "
                                   "neutral grip, elbows forward."}),
            ("lateral_raise", {"sets": 4, "reps": "12-15", "rpe": "7"}),
            ("seated_cable_row", {"sets": 3, "reps": "10", "rpe": "7",
                                  "purpose": "Rows ARE shoulder training: "
                                  "they build the wall behind the joint."}),
            ("rear_delt_fly", {"sets": 3, "reps": "15", "rpe": "7"}),
            ("cable_face_pull", {"sets": 3, "reps": "12", "rpe": "7"})],
        2: [("db_shoulder_press", {"sets": 4, "reps": "8", "rpe": "7-8",
                                   "equipment": "Heavier DBs than Week 1"}),
            ("lateral_raise", {"sets": 4, "reps": "12", "rpe": "7-8"}),
            ("chest_supported_row", {"sets": 4, "reps": "8-10", "rpe": "7-8"}),
            ("scaption_raise", {"sets": 3, "reps": "10-12", "rpe": "7"}),
            ("cable_face_pull", {"sets": 3, "reps": "12", "rpe": "7-8"}),
            ("db_shrug", {"sets": 3, "reps": "12", "rpe": "7-8"})],
        3: [("db_shoulder_press", {"sets": 5, "reps": "6", "rpe": "8",
                                   "purpose": "Top pressing week — "
                                   "heaviest clean sixes, zero grinding."}),
            ("lateral_raise", {"sets": 4, "reps": "10-12", "rpe": "8"}),
            ("chest_supported_row", {"sets": 4, "reps": "8", "rpe": "8"}),
            ("rear_delt_fly", {"sets": 4, "reps": "12", "rpe": "8"}),
            ("cable_face_pull", {"sets": 3, "reps": "12", "rpe": "8"}),
            ("db_shrug", {"sets": 4, "reps": "10-12", "rpe": "8"})],
        4: [("db_shoulder_press", {"sets": 3, "reps": "8", "rpe": "7",
                                   "purpose": "Week-2 weights at perfect "
                                   "speed — stay crisp on test week."}),
            ("lateral_raise", {"sets": 3, "reps": "12-15", "rpe": "7"}),
            ("seated_cable_row", {"sets": 3, "reps": "10", "rpe": "7",
                                  "tempo": "2-2-2-1",
                                  "purpose": "Variation: 2-s pause on the "
                                  "ribs every rep."}),
            ("cable_face_pull", {"sets": 3, "reps": "12", "rpe": "7"})],
    }[w]
    return _day(DAY_FOCUS["Wednesday"], [
        ("Warm-Up", ["cardio_warmup_20"]),
        ("Mobility", ["cat_cow", "open_book"]),
        ("Activation", [
            ("band_pull_apart", {"sets": 2}),
            ("wall_slide", {"sets": 2})]),
        ("Shoulder Rehabilitation", [
            ("band_er_90", {"sets": 2, "reps": "12", "rpe": "6-7"}),
            ("cable_er", {"sets": 2, "rpe": "7"})]),
        ("Strength", strength),
        ("Core", [
            ("plank_tap", {"sets": 2, "reps": "10 taps/side", "rpe": "7"})]),
        ("Functional Finisher", [
            ("farmer_carry", {"sets": 3, "reps": "40 m",
                              "rpe": "8" if w == 3 else "7-8"})]),
        ("Cool-Down & Stretch", [
            "stretch_chest", "cross_body_stretch", "breathing_reset"]),
    ])


# ---------------------------------------------------------------------
# THURSDAY — BALANCE & CONTROL (landings, reactive, closed-chain shoulder)
# ---------------------------------------------------------------------
def _balance_control_day(week):
    w = week
    sections = [
        ("Warm-Up", ["cardio_warmup_20"]),
        ("Mobility", ["leg_swings", "ankle_rocks"]),
        ("Activation", [
            ("band_walk", {"sets": 2}),
            ("deadbug", {"sets": 2})]),
    ]
    if w == 4:
        sections.append(("Assessment Battery (fresh + fully warm)", [
            ("assess_y_balance", {}),
            ("assess_sl_hop", {}),
            ("assess_plank", {})]))
    else:
        landing = {
            1: [("hop_stick", {"sets": 3, "reps": "4/side", "rpe": "7",
                               "purpose": "Small forward hops, frozen 2-s "
                               "landings — quality is the only score."})],
            2: [("hop_stick", {"sets": 3, "reps": "5/side", "rpe": "7",
                               "purpose": "Slightly further — landings "
                               "still silent and frozen."}),
                ("lateral_hop_stick", {"sets": 2, "reps": "4/direction/side",
                                       "rpe": "7"})],
            3: [("lateral_hop_stick", {"sets": 3, "reps": "4/direction/side",
                                       "rpe": "7-8"}),
                ("skater_bound", {"sets": 3, "reps": "3/side", "rpe": "7-8",
                                  "purpose": "Reactive week: short bounds, "
                                  "frozen landings, film the knee. Kept "
                                  "sub-maximal two days before the "
                                  "match."})],
        }[w]
        sections.append(("Landing Mechanics (fresh)", landing))
        balance = {
            1: [("sl_balance", {"sets": 2, "reps": "30 s/side", "rpe": "5"}),
                ("sl_reach", {"sets": 2})],
            2: [("sl_balance_perturb", {"sets": 2, "reps": "30 s/side, "
                                        "head turns"}),
                ("sl_reach", {"sets": 2})],
            3: [("sl_balance_perturb", {"sets": 3, "reps": "30 s/side, "
                                        "ball toss + eyes-closed finish"}),
                ("sl_reach", {"sets": 2, "equipment": "Dumbbell at chest"})],
        }[w]
        sections.append(("Balance", balance))
    shoulder_cc = {
        1: [("plank_tap", {"sets": 2, "reps": "8 taps/side", "rpe": "6-7"}),
            ("incline_pushup", {"sets": 3, "reps": "10-12", "rpe": "6-7",
                                "purpose": "Closed-chain shoulder stability "
                                "— the blade moves freely under load."}),
            ("bird_dog", {"sets": 2})],
        2: [("plank_tap", {"sets": 3, "reps": "8 taps/side", "rpe": "7"}),
            ("incline_pushup", {"sets": 3, "reps": "12", "rpe": "7"}),
            ("side_plank_leglift", {"sets": 2, "reps": "6 lifts/side",
                                    "rpe": "7"})],
        3: [("plank_tap", {"sets": 3, "reps": "10 taps/side", "rpe": "7",
                           "purpose": "Feet narrower this week — more "
                           "anti-rotation demand."}),
            ("pushup", {"sets": 3, "reps": "8-12", "rpe": "7",
                        "purpose": "Graduated from the incline — full "
                        "push-ups if the shoulder stays silent."}),
            ("side_plank_leglift", {"sets": 2, "reps": "8 lifts/side",
                                    "rpe": "7-8"})],
        4: [("plank_tap", {"sets": 2, "reps": "8 taps/side", "rpe": "6-7"}),
            ("suitcase_carry", {"sets": 2, "reps": "30 m/side", "rpe": "7"})],
    }[w]
    sections += [
        ("Shoulder Rehabilitation", shoulder_cc),
        ("Conditioning (Football Prep)", [
            ("shadow_footwork", {"reps": "6-8 min, crisp",
                                 "rpe": "6-7"})]),
        ("Cool-Down & Stretch", [
            "stretch_hip_flexor", "stretch_calf", "breathing_reset"]),
    ]
    return _day(DAY_FOCUS["Thursday"], sections)


def _week(n):
    return {
        "Monday": _leg_strength_day(n),
        "Tuesday": _balance_stability_day(n),
        "Wednesday": _shoulder_strength_day(n),
        "Thursday": _balance_control_day(n),
        "Friday": _friday(n),
        "Saturday": _saturday(n),
        "Sunday": _sunday(n),
    }


def default_program() -> dict:
    """Full materialised month: {week:int -> {day:str -> day_dict}}."""
    return {1: _week(1), 2: _week(2), 3: _week(3), 4: _week(4)}
