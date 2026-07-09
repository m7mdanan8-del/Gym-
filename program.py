"""
program.py
==========
Generates the default one-month program:

  Week 1 – Foundation            (RPE 5-6, groove patterns, isometrics)
  Week 2 – Progression           (RPE 6-7, add load & new exercises)
  Week 3 – Advanced Progression  (RPE 7-8, unilateral bias, eccentrics, hops)
  Week 4 – Variation + Assessment (moderate load + benchmark tests)

Weekly schedule:
  Mon  Lower Body – Quad / ACL focus
  Tue  Upper Body – Shoulder rehab focus
  Wed  Posterior Chain – Hamstrings / Glutes / Balance
  Thu  Full-Body Functional – Core / Football prep
  Fri  Recovery
  Sat  Football (pre-match activation + post-match reset)
  Sun  Recovery + Mobility

Exercise variations change each week ON PURPOSE (progressive overload and
skill layering) — the rehabilitation objective of every slot stays constant.

The materialised program (library data + weekly prescription overrides)
is what gets seeded into SQLite; Edit Mode then owns it.
"""

import copy

from exercise_library import EXERCISES

DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday",
        "Saturday", "Sunday"]

TRAINING_DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday"]

WEEK_THEMES = {
    1: ("Foundation",
        "Groove every movement pattern at comfortable intensity (RPE 5-6). "
        "Isometrics and controlled tempo re-awaken the quad and rotator "
        "cuff. Nothing should feel hard yet — that is by design."),
    2: ("Progression",
        "Same objectives, more load (RPE 6-7). Nordic lowering, hip "
        "thrusts and floor pressing enter. Add small weight jumps only "
        "where last week's final set felt controlled."),
    3: ("Advanced Progression",
        "Single-leg bias, slow eccentrics and the first hop-and-stick "
        "landings (RPE 7-8). The 90/90 shoulder position appears — only "
        "proceed if Weeks 1-2 cuff work was pain-free."),
    4: ("Variation + Assessment",
        "Fresh variations at moderate load plus benchmark tests: wall-sit "
        "hold, calf-raise reps, plank hold, Y-balance and (if pain-free) "
        "the single-leg hop test. The numbers you record steer next "
        "month."),
}

# Friendly names for the day focus
DAY_FOCUS = {
    "Monday":    "Lower Body Strength — Quad & ACL Focus",
    "Tuesday":   "Upper Body Strength — Shoulder Rehab Focus",
    "Wednesday": "Posterior Chain — Hamstrings, Glutes & Balance",
    "Thursday":  "Full-Body Functional — Core & Football Prep",
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
# Shared day templates (recovery / football) — vary slightly by week
# ---------------------------------------------------------------------
def _friday(week):
    extra = []
    if week >= 2:
        extra = [("incline_walk", {"reps": "20 min easy", "rpe": "4",
                                   "purpose": "Optional gentle flush walk — skip "
                                   "if legs feel heavy before tomorrow's match."})]
    return _day(DAY_FOCUS["Friday"], [
        ("Soft Tissue & Mobility", [
            "foam_roll_quads", "cat_cow", "open_book", "worlds_greatest"]),
        ("Keep-The-Knee-Awake (pain-free, light)", [
            ("quad_set_ssq", {"sets": 1, "rpe": "3"}),
            ("sl_balance", {"sets": 2, "reps": "30 s/side", "rpe": "3"})]),
        ("Optional Easy Movement", extra or [
            ("brisk_march", {"reps": "10 min easy walk", "rpe": "3"})]),
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
# WEEK 1 — FOUNDATION
# ---------------------------------------------------------------------
def _week1():
    e = {"rpe": "5-6"}
    return {
        "Monday": _day(DAY_FOCUS["Monday"], [
            ("Warm-Up", ["bike_warmup"]),
            ("Mobility", ["ankle_rocks", "leg_swings"]),
            ("Activation", [
                ("quad_set_ssq", {}),
                ("glute_bridge", {"sets": 2}),
                ("clamshell", {"sets": 2})]),
            ("Strength", [
                ("box_squat", {"sets": 3, "reps": "10", "rpe": "5-6",
                               "equipment": "Bench + light dumbbells at the sides"}),
                ("leg_press", {"sets": 2, "reps": "12", "rpe": "5-6",
                               "purpose": "Light first exposure — dial in your "
                               "seat, foot position and safe depth this week; "
                               "the load comes later."}),
                ("split_squat", {"sets": 2, "reps": "8/side", "rpe": "5-6",
                                 "equipment": "Bodyweight (hold support if needed)"}),
                ("smith_calf", {"sets": 3, "reps": "12", **e})]),
            ("Rehabilitation", [
                ("tke", {"sets": 2}),
                ("wall_sit", {"sets": 2, "reps": "30 s", "rpe": "5-6"})]),
            ("Core", [
                ("deadbug", {"sets": 2}),
                ("plank", {"sets": 2, "reps": "30 s", **e})]),
            ("Balance", [("sl_balance", {"sets": 3})]),
            ("Conditioning", [
                ("bike_tempo", {"reps": "12 min", "rpe": "5-6"})]),
            ("Cool-Down & Stretch", [
                "stretch_quad", "stretch_calf", "breathing_reset"]),
        ]),
        "Tuesday": _day(DAY_FOCUS["Tuesday"], [
            ("Warm-Up", ["brisk_march"]),
            ("Mobility", ["cat_cow", "open_book"]),
            ("Activation", [
                ("scap_pushup", {"sets": 2}),
                ("band_pull_apart", {"sets": 2}),
                ("wall_slide", {"sets": 2})]),
            ("Shoulder Rehabilitation", [
                ("iso_er_wall", {}),
                ("band_er", {"sets": 2, "reps": "12", **e}),
                ("band_ir", {"sets": 2, "reps": "12", **e})]),
            ("Strength", [
                ("chest_press_machine", {"sets": 3, "reps": "12", **e,
                                         "purpose": "Guided pressing with the "
                                         "start depth set shallow — a safe "
                                         "week to learn the machine setup."}),
                ("seated_cable_row", {"sets": 3, "reps": "12", **e}),
                ("scaption_raise", {"sets": 2, "reps": "10", **e})]),
            ("Core", [
                ("bird_dog", {"sets": 2}),
                ("side_plank", {"sets": 2, "reps": "20 s/side", **e})]),
            ("Functional Finisher", [
                ("farmer_carry", {"sets": 2, "reps": "30 m", "rpe": "6"})]),
            ("Cool-Down & Stretch", [
                "stretch_chest", "cross_body_stretch", "breathing_reset"]),
        ]),
        "Wednesday": _day(DAY_FOCUS["Wednesday"], [
            ("Warm-Up", ["bike_warmup"]),
            ("Mobility", ["lateral_leg_swings", "worlds_greatest"]),
            ("Activation", [
                ("bridge_march", {"sets": 2}),
                ("band_walk", {"sets": 2})]),
            ("Strength", [
                ("romanian_deadlift", {"sets": 3, "reps": "10", "rpe": "6",
                                       "purpose": "Groove the hinge with "
                                       "dumbbells this week — the barbell "
                                       "takes over from Week 2."}),
                ("leg_curl_machine", {"sets": 2, "reps": "12", "rpe": "6"}),
                ("seated_calf_machine", {"sets": 2, **e})]),
            ("Rehabilitation", [
                ("side_leg_raise", {"sets": 2}),
                ("single_leg_bridge", {"sets": 2, "reps": "6/side", **e})]),
            ("Core", [
                ("pallof_press", {"sets": 2}),
                ("side_plank", {"sets": 2, "reps": "20 s/side", **e})]),
            ("Balance", [("sl_balance", {"sets": 3})]),
            ("Conditioning", [
                ("bike_intervals", {"reps": "8 rounds (8 min)", "rpe": "7 work"})]),
            ("Cool-Down & Stretch", [
                "stretch_hamstring", "stretch_glute", "breathing_reset"]),
        ]),
        "Thursday": _day(DAY_FOCUS["Thursday"], [
            ("Warm-Up", ["brisk_march"]),
            ("Mobility", ["leg_swings", "ankle_rocks"]),
            ("Activation", [
                ("monster_walk", {"sets": 2}),
                ("deadbug", {"sets": 2})]),
            ("Strength", [
                ("step_up", {"sets": 3, "reps": "8/side", "rpe": "6",
                             "equipment": "Low box + light dumbbells"}),
                ("hip_thrust", {"sets": 3, "reps": "10", "rpe": "6"}),
                ("lat_pulldown_machine", {"sets": 2, "reps": "12", **e})]),
            ("Core", [
                ("pallof_press", {"sets": 2}),
                ("suitcase_carry", {"sets": 2, "reps": "20 m/side", "rpe": "6"})]),
            ("Balance", [("sl_reach", {"sets": 2})]),
            ("Conditioning (Football Prep)", [
                ("shadow_footwork", {"reps": "6 min", "rpe": "5-6"})]),
            ("Cool-Down & Stretch", [
                "stretch_hip_flexor", "stretch_calf", "breathing_reset"]),
        ]),
        "Friday": _friday(1),
        "Saturday": _saturday(1),
        "Sunday": _sunday(1),
    }


# ---------------------------------------------------------------------
# WEEK 2 — PROGRESSION
# ---------------------------------------------------------------------
def _week2():
    return {
        "Monday": _day(DAY_FOCUS["Monday"], [
            ("Warm-Up", ["bike_warmup"]),
            ("Mobility", ["ankle_rocks", "leg_swings"]),
            ("Activation", [
                ("glute_bridge", {"sets": 2}),
                ("clamshell", {"sets": 2}),
                ("tke", {"sets": 2, "purpose": "Moved into activation this "
                         "week: prime the VMO before squatting."})]),
            ("Strength", [
                ("goblet_squat", {"sets": 3, "reps": "10", "rpe": "6-7",
                                  "equipment": "Heavier dumbbell than Week 1"}),
                ("leg_press", {"sets": 3, "reps": "10", "rpe": "6-7",
                               "purpose": "Settings found last week — now "
                               "start adding plates while the 3-s lowering "
                               "stays smooth."}),
                ("reverse_lunge", {"sets": 3, "reps": "8/side", "rpe": "6-7",
                                   "equipment": "Dumbbells at the sides"}),
                ("smith_calf", {"sets": 3, "reps": "10-12", "rpe": "6-7"})]),
            ("Rehabilitation", [
                ("spanish_squat", {"sets": 2, "reps": "10", "rpe": "6-7"}),
                ("leg_extension", {"sets": 2, "reps": "15", "rpe": "6",
                                   "purpose": "New: machine quad isolation — "
                                   "STRICTLY in the protected 90°→45° arc, "
                                   "light weight, slow lowering."})]),
            ("Core", [
                ("deadbug", {"sets": 3, "equipment": "Optional light plate"}),
                ("plank", {"sets": 3, "reps": "35-40 s", "rpe": "6-7"})]),
            ("Balance", [("sl_balance_perturb", {"sets": 2})]),
            ("Conditioning", [
                ("bike_tempo", {"reps": "15 min", "rpe": "6"})]),
            ("Cool-Down & Stretch", [
                "stretch_quad", "stretch_calf", "breathing_reset"]),
        ]),
        "Tuesday": _day(DAY_FOCUS["Tuesday"], [
            ("Warm-Up", ["brisk_march"]),
            ("Mobility", ["cat_cow", "open_book"]),
            ("Activation", [
                ("scap_pushup", {"sets": 2}),
                ("wall_slide", {"sets": 2})]),
            ("Shoulder Rehabilitation", [
                ("cable_er", {"sets": 3, "rpe": "6",
                              "purpose": "Band ER graduates to the cable "
                              "stack — same movement, measurable weight."}),
                ("band_ir", {"sets": 3, "rpe": "6"}),
                ("cable_face_pull", {"sets": 2, "rpe": "6"})]),
            ("Strength", [
                ("floor_press", {"sets": 3, "reps": "10", "rpe": "6-7"}),
                ("seated_cable_row", {"sets": 3, "reps": "10-12", "rpe": "6-7",
                                      "equipment": "Heavier than Week 1"}),
                ("prone_ytw", {"sets": 2})]),
            ("Core", [
                ("bird_dog", {"sets": 2, "reps": "10/side"}),
                ("plank_tap", {"sets": 2, "reps": "6 taps/side", "rpe": "6",
                               "regression": "Hands on a bench if the "
                               "shoulder isn't ready for floor-level taps."})]),
            ("Functional Finisher", [
                ("farmer_carry", {"sets": 3, "reps": "35 m", "rpe": "7"})]),
            ("Cool-Down & Stretch", [
                "stretch_chest", "cross_body_stretch", "breathing_reset"]),
        ]),
        "Wednesday": _day(DAY_FOCUS["Wednesday"], [
            ("Warm-Up", ["bike_warmup"]),
            ("Mobility", ["lateral_leg_swings", "worlds_greatest"]),
            ("Activation", [
                ("bridge_march", {"sets": 2}),
                ("band_walk", {"sets": 2, "reps": "12 steps/direction"})]),
            ("Strength", [
                ("barbell_rdl", {"sets": 3, "reps": "8-10", "rpe": "7",
                                 "purpose": "The hinge you grooved with "
                                 "dumbbells, now on the bar — start with "
                                 "just the bar and add small plates."}),
                ("barbell_hip_thrust", {"sets": 3, "reps": "10-12", "rpe": "7"}),
                ("leg_curl_machine", {"sets": 3, "reps": "10", "rpe": "7"})]),
            ("Rehabilitation", [
                ("nordic_curl", {"sets": 2, "reps": "3-4", "rpe": "7",
                                 "safety": "First Nordic week: 2×3 only. "
                                 "Expect hamstring DOMS — that's normal. "
                                 "Never the day before football."}),
                ("adductor_machine", {"sets": 2, "reps": "12-15", "rpe": "6",
                                      "purpose": "New: machine groin "
                                      "strength — conservative range this "
                                      "first week."})]),
            ("Core", [
                ("pallof_press", {"sets": 3}),
                ("side_plank", {"sets": 3, "reps": "25-30 s/side", "rpe": "6-7"})]),
            ("Balance", [("sl_balance_perturb", {"sets": 3})]),
            ("Conditioning", [
                ("bike_intervals", {"reps": "10 rounds (10 min)", "rpe": "8 work"})]),
            ("Cool-Down & Stretch", [
                "stretch_hamstring", "stretch_glute", "breathing_reset"]),
        ]),
        "Thursday": _day(DAY_FOCUS["Thursday"], [
            ("Warm-Up", ["brisk_march"]),
            ("Mobility", ["leg_swings", "ankle_rocks"]),
            ("Activation", [
                ("monster_walk", {"sets": 2, "reps": "12 steps each way"}),
                ("deadbug", {"sets": 2})]),
            ("Strength", [
                ("step_up", {"sets": 3, "reps": "8/side", "rpe": "7",
                             "equipment": "Box + light dumbbells"}),
                ("lateral_lunge", {"sets": 2, "reps": "6/side", "rpe": "6",
                                   "purpose": "New this week: first "
                                   "frontal-plane strength exposure."}),
                ("lat_pulldown_machine", {"sets": 3, "reps": "10-12",
                                          "rpe": "6-7"})]),
            ("Core", [
                ("plank_tap", {"sets": 2, "reps": "8 taps/side", "rpe": "6-7"}),
                ("suitcase_carry", {"sets": 3, "reps": "25 m/side", "rpe": "7"})]),
            ("Balance", [("sl_reach", {"sets": 2})]),
            ("Conditioning (Football Prep)", [
                ("shadow_footwork", {"reps": "7 min", "rpe": "6"})]),
            ("Cool-Down & Stretch", [
                "stretch_hip_flexor", "stretch_calf", "breathing_reset"]),
        ]),
        "Friday": _friday(2),
        "Saturday": _saturday(2),
        "Sunday": _sunday(2),
    }


# ---------------------------------------------------------------------
# WEEK 3 — ADVANCED PROGRESSION
# ---------------------------------------------------------------------
def _week3():
    return {
        "Monday": _day(DAY_FOCUS["Monday"], [
            ("Warm-Up", ["bike_warmup"]),
            ("Mobility", ["ankle_rocks", "worlds_greatest"]),
            ("Activation", [
                ("glute_bridge", {"sets": 2}),
                ("band_walk", {"sets": 2}),
                ("tke", {"sets": 2})]),
            ("Landing Mechanics (fresh — before strength)", [
                ("hop_stick", {"sets": 3, "reps": "4/side", "rpe": "7",
                               "purpose": "First hop exposure — tiny "
                               "distances, perfect frozen landings."})]),
            ("Strength", [
                ("leg_press", {"sets": 3, "reps": "8", "rpe": "7-8",
                               "purpose": "Now the heavy quad builder — add "
                               "plates while the 3-s lowering and depth stay "
                               "identical to Week 2."}),
                ("rfe_split_squat", {"sets": 3, "reps": "8/side", "rpe": "7",
                                     "equipment": "Bench + dumbbells"}),
                ("calf_raise_single", {"sets": 3, "reps": "12/side", "rpe": "7-8",
                                       "equipment": "Step + dumbbell in "
                                       "same-side hand"})]),
            ("Rehabilitation", [
                ("spanish_squat", {"sets": 3, "reps": "30-40 s iso hold",
                                   "rpe": "7-8"}),
                ("leg_extension", {"sets": 3, "reps": "12-15", "rpe": "7",
                                   "purpose": "Progress the weight — the "
                                   "90°→45° protected arc stays exactly the "
                                   "same."})]),
            ("Core", [
                ("deadbug", {"sets": 3, "equipment": "Mini-band around feet"}),
                ("plank", {"sets": 3, "reps": "45 s", "rpe": "7"})]),
            ("Balance", [("sl_balance_perturb", {"sets": 3,
                          "reps": "30 s/side (add head turns)"})]),
            ("Conditioning", [
                ("bike_tempo", {"reps": "18 min", "rpe": "6"})]),
            ("Cool-Down & Stretch", [
                "stretch_quad", "stretch_calf", "breathing_reset"]),
        ]),
        "Tuesday": _day(DAY_FOCUS["Tuesday"], [
            ("Warm-Up", ["brisk_march"]),
            ("Mobility", ["cat_cow", "open_book"]),
            ("Activation", [
                ("scap_pushup", {"sets": 2, "reps": "12"}),
                ("wall_slide", {"sets": 2, "equipment": "Mini-band around wrists"})]),
            ("Shoulder Rehabilitation", [
                ("band_er_90", {"sets": 2, "reps": "10", "rpe": "6",
                                "safety": "GATE: only if Weeks 1-2 cuff work "
                                "was 100% pain-free. Any apprehension = drop "
                                "back to elbow-at-side ER today."}),
                ("cable_er", {"sets": 2, "rpe": "7",
                              "equipment": "One plate heavier than Week 2"}),
                ("cable_face_pull", {"sets": 3, "rpe": "7"})]),
            ("Strength", [
                ("db_bench", {"sets": 3, "reps": "8", "rpe": "7",
                              "purpose": "Graduated from the floor press — "
                              "neutral grip, depth capped at arms-parallel. "
                              "Only if Weeks 1-2 pressing was silent."}),
                ("db_row", {"sets": 3, "reps": "8/side", "rpe": "7-8"}),
                ("landmine_press", {"sets": 3, "reps": "8/side", "rpe": "7",
                                    "purpose": "New: the first controlled "
                                    "path back toward overhead strength."}),
                ("rear_delt_fly", {"sets": 2, "reps": "12-15", "rpe": "6-7"})]),
            ("Core", [
                ("plank_tap", {"sets": 3, "reps": "8 taps/side", "rpe": "7"}),
                ("side_plank", {"sets": 2, "reps": "35 s/side", "rpe": "7"})]),
            ("Functional Finisher", [
                ("suitcase_carry", {"sets": 3, "reps": "30 m/side", "rpe": "7-8"})]),
            ("Cool-Down & Stretch", [
                "stretch_chest", "cross_body_stretch", "breathing_reset"]),
        ]),
        "Wednesday": _day(DAY_FOCUS["Wednesday"], [
            ("Warm-Up", ["bike_warmup"]),
            ("Mobility", ["lateral_leg_swings", "worlds_greatest"]),
            ("Activation", [
                ("bridge_march", {"sets": 2}),
                ("monster_walk", {"sets": 2})]),
            ("Strength", [
                ("trap_bar_deadlift", {"sets": 3, "reps": "6-8", "rpe": "7-8",
                                       "purpose": "New: the month's heaviest "
                                       "pull. The neutral handles keep the "
                                       "right shoulder safe while the whole "
                                       "posterior chain works."}),
                ("single_leg_rdl", {"sets": 2, "reps": "6/side", "rpe": "7",
                                    "equipment": "One dumbbell",
                                    "purpose": "Kept light after the trap-bar "
                                    "work: hamstring strength + "
                                    "proprioception in one lift."}),
                ("single_leg_hip_thrust", {"sets": 3, "reps": "8/side", "rpe": "7-8"}),
                ("eccentric_calf", {"sets": 3, "reps": "10/side", "rpe": "6-7"})]),
            ("Rehabilitation", [
                ("nordic_curl", {"sets": 3, "reps": "4-5", "rpe": "8"}),
                ("copenhagen", {"sets": 2, "reps": "15 s/side", "rpe": "7",
                                "purpose": "New: adductor armour — proven "
                                "~40% groin-injury reduction in footballers."})]),
            ("Core", [
                ("pallof_press", {"sets": 3, "reps": "10/side (half-kneeling)",
                                  "rpe": "7"})]),
            ("Balance", [("sl_reach", {"sets": 2,
                          "equipment": "Light dumbbell at chest"})]),
            ("Conditioning", [
                ("bike_intervals", {"reps": "12 rounds (12 min)", "rpe": "8 work"})]),
            ("Cool-Down & Stretch", [
                "stretch_hamstring", "stretch_glute", "breathing_reset"]),
        ]),
        "Thursday": _day(DAY_FOCUS["Thursday"], [
            ("Warm-Up", ["brisk_march"]),
            ("Mobility", ["leg_swings", "ankle_rocks"]),
            ("Activation", [
                ("band_walk", {"sets": 2}),
                ("deadbug", {"sets": 2})]),
            ("Landing Mechanics (fresh)", [
                ("lateral_hop_stick", {"sets": 2, "reps": "4/direction/side",
                                       "rpe": "7",
                                       "purpose": "First lateral hop "
                                       "exposure — small and perfect."})]),
            ("Strength", [
                ("lateral_step_up", {"sets": 3, "reps": "8/side", "rpe": "7"}),
                ("lateral_lunge", {"sets": 3, "reps": "8/side", "rpe": "7",
                                   "equipment": "Dumbbell at chest"}),
                ("lat_pulldown_machine", {"sets": 3, "reps": "8-10", "rpe": "7",
                                          "equipment": "Heavier than Week 2"})]),
            ("Core", [
                ("side_plank_leglift", {"sets": 2, "reps": "6 lifts/side",
                                        "rpe": "7"}),
                ("farmer_carry", {"sets": 3, "reps": "40 m", "rpe": "7-8"})]),
            ("Balance", [("sl_balance_perturb", {"sets": 2,
                          "reps": "30 s/side, eyes-closed finish"})]),
            ("Conditioning (Football Prep)", [
                ("shadow_footwork", {"reps": "8 min", "rpe": "6-7"})]),
            ("Cool-Down & Stretch", [
                "stretch_hip_flexor", "stretch_calf", "breathing_reset"]),
        ]),
        "Friday": _friday(3),
        "Saturday": _saturday(3),
        "Sunday": _sunday(3),
    }


# ---------------------------------------------------------------------
# WEEK 4 — VARIATION + ASSESSMENT
# ---------------------------------------------------------------------
def _week4():
    return {
        "Monday": _day(DAY_FOCUS["Monday"], [
            ("Warm-Up", ["bike_warmup"]),
            ("Mobility", ["ankle_rocks", "leg_swings"]),
            ("Activation", [
                ("glute_bridge", {"sets": 2}),
                ("clamshell", {"sets": 2}),
                ("tke", {"sets": 2})]),
            ("Assessment", [
                ("assess_wall_sit", {}),
                ("assess_sl_calf", {})]),
            ("Strength (moderate — testing week)", [
                ("goblet_squat", {"sets": 3, "reps": "8", "rpe": "6-7",
                                  "purpose": "Familiar pattern, moderate "
                                  "load — keep quality high on test week."}),
                ("leg_press", {"sets": 2, "reps": "10", "rpe": "6-7",
                               "purpose": "Moderate plates on test week — "
                               "smooth reps, nothing grinding."})]),
            ("Core", [
                ("deadbug", {"sets": 2}),
                ("side_plank", {"sets": 2, "reps": "30 s/side", "rpe": "6-7"})]),
            ("Balance", [("sl_balance_perturb", {"sets": 2})]),
            ("Conditioning", [
                ("bike_tempo", {"reps": "15 min", "rpe": "6"})]),
            ("Cool-Down & Stretch", [
                "stretch_quad", "stretch_calf", "breathing_reset"]),
        ]),
        "Tuesday": _day(DAY_FOCUS["Tuesday"], [
            ("Warm-Up", ["brisk_march"]),
            ("Mobility", ["cat_cow", "open_book"]),
            ("Activation", [
                ("scap_pushup", {"sets": 2}),
                ("band_pull_apart", {"sets": 2})]),
            ("Shoulder Rehabilitation", [
                ("band_er_90", {"sets": 3, "reps": "10-12", "rpe": "7",
                                "safety": "Same gate as Week 3: apprehension "
                                "= drop to elbow-at-side ER."}),
                ("band_ir", {"sets": 3, "rpe": "7",
                             "equipment": "Heavier band"}),
                ("prone_ytw", {"sets": 2})]),
            ("Strength (variation)", [
                ("pushup", {"sets": 3, "reps": "as able, stop 2 reps shy of "
                            "failure", "rpe": "7",
                            "purpose": "Graduation test of the pressing "
                            "ladder: floor push-ups — only if incline "
                            "push-ups were crisp and painless.",
                            "regression": "Stay on the incline — that is "
                            "still a pass."}),
                ("seated_cable_row", {"sets": 3, "reps": "10", "rpe": "7",
                                      "tempo": "2-2-2-1",
                                      "purpose": "Variation: 2-s pause with "
                                      "the handle on the ribs every rep."}),
                ("scaption_raise", {"sets": 3, "rpe": "7",
                                    "equipment": "Slightly heavier DBs than "
                                    "Week 1"}),
                ("rear_delt_fly", {"sets": 2, "reps": "12-15", "rpe": "6-7"})]),
            ("Core", [
                ("plank_tap", {"sets": 2, "reps": "10 taps/side", "rpe": "7"})]),
            ("Functional Finisher", [
                ("farmer_carry", {"sets": 3, "reps": "40 m", "rpe": "7-8"})]),
            ("Cool-Down & Stretch", [
                "stretch_chest", "cross_body_stretch", "breathing_reset"]),
        ]),
        "Wednesday": _day(DAY_FOCUS["Wednesday"], [
            ("Warm-Up", ["bike_warmup"]),
            ("Mobility", ["lateral_leg_swings", "worlds_greatest"]),
            ("Activation", [
                ("bridge_march", {"sets": 2}),
                ("band_walk", {"sets": 2})]),
            ("Strength (variation)", [
                ("barbell_rdl", {"sets": 3, "reps": "8", "rpe": "7",
                                 "tempo": "4-1-1-0",
                                 "purpose": "Variation: slower 4-s eccentric "
                                 "at Week-2 load."}),
                ("barbell_hip_thrust", {"sets": 3, "reps": "10", "rpe": "7",
                                        "tempo": "2-3-1-1",
                                        "purpose": "Variation: 3-s squeeze "
                                        "at the top of every rep."}),
                ("leg_curl_machine", {"sets": 2, "reps": "10-12", "rpe": "7"})]),
            ("Rehabilitation", [
                ("nordic_curl", {"sets": 2, "reps": "5", "rpe": "8",
                                 "safety": "Reduced volume on test week; "
                                 "never the day before football."}),
                ("copenhagen", {"sets": 2, "reps": "20 s/side", "rpe": "7"})]),
            ("Core", [
                ("pallof_press", {"sets": 3, "reps": "10/side (split stance)"})]),
            ("Conditioning", [
                ("bike_intervals", {"reps": "10 rounds, harder gear",
                                    "rpe": "8 work"})]),
            ("Cool-Down & Stretch", [
                "stretch_hamstring", "stretch_glute", "breathing_reset"]),
        ]),
        "Thursday": _day(DAY_FOCUS["Thursday"], [
            ("Warm-Up", ["brisk_march"]),
            ("Mobility", ["leg_swings", "ankle_rocks", "worlds_greatest"]),
            ("Activation", [
                ("band_walk", {"sets": 2}),
                ("glute_bridge", {"sets": 2})]),
            ("Assessment Battery (fresh + fully warm)", [
                ("assess_y_balance", {}),
                ("assess_sl_hop", {}),
                ("assess_plank", {})]),
            ("Light Functional Work (after tests)", [
                ("suitcase_carry", {"sets": 2, "reps": "30 m/side", "rpe": "6-7"}),
                ("lat_pulldown_machine", {"sets": 2, "reps": "12", "rpe": "6"})]),
            ("Conditioning (Football Prep)", [
                ("shadow_footwork", {"reps": "6 min crisp", "rpe": "6"})]),
            ("Cool-Down & Stretch", [
                "stretch_hip_flexor", "stretch_quad", "stretch_calf",
                "breathing_reset"]),
        ]),
        "Friday": _friday(4),
        "Saturday": _saturday(4),
        "Sunday": _sunday(4),
    }


def default_program() -> dict:
    """Full materialised month: {week:int -> {day:str -> day_dict}}."""
    return {1: _week1(), 2: _week2(), 3: _week3(), 4: _week4()}
