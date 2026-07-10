"""
program.py
==========
MUSCLE-SPLIT BLOCK — dumbbells & machines only, one muscle group per
training day (user preference), for a trained athlete (4+ months of
consistent gym work, pain-free knee and shoulder):

  Mon  CHEST day    (presses, flys, triceps)
  Tue  LEG day      (quads, hamstrings, glutes, calves + knee armour)
  Wed  BACK day     (pull-ups, pulldowns, rows, biceps)
  Thu  SHOULDER day (delts, traps, rotator cuff)
  Fri  Recovery
  Sat  Football (pre-match activation + post-match reset)
  Sun  Recovery + Mobility

Leg day sits on Tuesday deliberately: four full days before Saturday's
match, so heavy legs (and Nordics) never steal match sharpness.

Four-week wave:
  Week 1 – Load       (groove the split at RPE 7)
  Week 2 – Overload   (heavier dumbbells/stacks, RPE 7-8)
  Week 3 – Intensity  (top week, RPE 8; jumps & bounds peak on leg day)
  Week 4 – Peak + Retest (reduced volume + benchmark tests spread
           across the split: push-ups, leg battery, pull-ups, plank)

Standing guardrails (independent of training age):
- dumbbells and machines only — no barbell work in this block
- no behind-the-neck pressing/pulling, no dips
- pressing depth capped at arms-parallel; pec-deck range stop shallow
- pull-up bottoms stay ACTIVE (no dead hang on the capsule)
- jumps/bounds only fresh and pain-free; box jumps always stepped down

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
        "The muscle-per-day split begins: chest, legs, back, shoulders — "
        "dumbbells and machines only. Weights stay one gear down (RPE 7) "
        "while you find your working loads on every machine; write them "
        "all in the tracker."),
    2: ("Overload",
        "Same split, heavier dumbbells and stacks (RPE 7-8). Single-leg "
        "press and heavy dumbbell RDLs join leg day. Add weight anywhere "
        "last week's final set was smooth."),
    3: ("Intensity",
        "Top week (RPE 8): heaviest loads of the block, box jumps at "
        "their highest and skater bounds on leg day. Quality gates "
        "everything — power work ends the moment reps slow down."),
    4: ("Peak + Retest",
        "Volume drops and the benchmarks run, spread across the split: "
        "max push-ups (chest day), wall-sit / calf / Y-balance / "
        "single-leg hop (leg day), max strict pull-ups (back day) and "
        "max plank (shoulder day). Beat last block's numbers."),
}

# Friendly names for the day focus
DAY_FOCUS = {
    "Monday":    "Chest Day — Presses, Flys & Triceps",
    "Tuesday":   "Leg Day — Quads, Hamstrings, Glutes & Calves",
    "Wednesday": "Back Day — Pull-Ups, Rows & Biceps",
    "Thursday":  "Shoulder Day — Delts, Traps & Rotator Cuff",
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
# Day builders — one per muscle group, parameterised by week
# ---------------------------------------------------------------------
def _chest_day(week):
    """Monday — CHEST. Progression: load W1→W3, W4 moderate + push-up test."""
    w = week
    sections = [
        ("Warm-Up", ["cardio_warmup_20"]),
        ("Mobility", ["cat_cow", "open_book"]),
        ("Activation", [
            ("scap_pushup", {"sets": 2, "reps": "12"}),
            ("band_pull_apart", {"sets": 2})]),
    ]
    if w == 4:
        sections.append(("Assessment", [
            ("pushup", {"sets": 1, "reps": "TEST — max strict push-ups "
                        "(record the number)", "rpe": "9",
                        "purpose": "Chest-day benchmark: strict full-range "
                        "push-ups to one shy of failure. Beat it next "
                        "block."})]))
    strength = {
        1: [("chest_press_machine", {"sets": 4, "reps": "10", "rpe": "7",
                                     "purpose": "Open the block finding your "
                                     "working stack — log it."}),
            ("db_bench", {"sets": 4, "reps": "8", "rpe": "7"}),
            ("incline_db_press", {"sets": 3, "reps": "10", "rpe": "7"}),
            ("pec_deck", {"sets": 3, "reps": "12-15", "rpe": "7",
                          "purpose": "New: chest isolation finisher — set "
                          "the range stop shallow before rep one."}),
            ("triceps_pushdown", {"sets": 3, "reps": "12", "rpe": "7"})],
        2: [("db_bench", {"sets": 4, "reps": "8", "rpe": "7-8",
                          "equipment": "Heavier DBs than Week 1"}),
            ("incline_db_press", {"sets": 4, "reps": "8-10", "rpe": "7-8"}),
            ("chest_press_machine", {"sets": 3, "reps": "10", "rpe": "7-8"}),
            ("pec_deck", {"sets": 3, "reps": "12", "rpe": "7-8"}),
            ("triceps_pushdown", {"sets": 3, "reps": "12", "rpe": "7-8"})],
        3: [("db_bench", {"sets": 5, "reps": "6-8", "rpe": "8",
                          "purpose": "Top pressing week — heaviest clean "
                          "sets of the block, depth cap unchanged."}),
            ("incline_db_press", {"sets": 4, "reps": "8", "rpe": "8"}),
            ("chest_press_machine", {"sets": 3, "reps": "8-10", "rpe": "8"}),
            ("pec_deck", {"sets": 3, "reps": "12", "rpe": "8"}),
            ("triceps_pushdown", {"sets": 4, "reps": "10-12", "rpe": "8"})],
        4: [("db_bench", {"sets": 3, "reps": "8", "rpe": "7",
                          "purpose": "Week-2 weights at perfect speed — "
                          "stay crisp on test week."}),
            ("incline_db_press", {"sets": 3, "reps": "10", "rpe": "7"}),
            ("pec_deck", {"sets": 2, "reps": "12-15", "rpe": "7"}),
            ("triceps_pushdown", {"sets": 3, "reps": "12", "rpe": "7"})],
    }[w]
    sections += [
        ("Strength", strength),
        ("Core", [("plank_tap", {"sets": 2, "reps": "10 taps/side",
                                 "rpe": "7"})]),
        ("Conditioning", [
            ("bike_intervals", {"reps": f"{8 + (w in (2, 3)) * 2} rounds",
                                "rpe": "8 work",
                                "purpose": "Optional finisher — the 20-min "
                                "warm-up already banked aerobic work."})]),
        ("Cool-Down & Stretch", [
            "stretch_chest", "cross_body_stretch", "breathing_reset"]),
    ]
    return _day(DAY_FOCUS["Monday"], sections)


def _leg_day(week):
    """Tuesday — LEGS. Quads + hamstrings + glutes + calves + knee armour.
    Four days before the match, so heavy legs and Nordics recover fully."""
    w = week
    sections = [
        ("Warm-Up", ["cardio_warmup_20"]),
        ("Mobility", ["ankle_rocks", "worlds_greatest"]),
        ("Activation", [
            ("glute_bridge", {"sets": 2, "reps": "10"}),
            ("band_walk", {"sets": 2})]),
    ]
    if w == 4:
        sections.append(("Assessment Battery (fresh + fully warm)", [
            ("assess_wall_sit", {}),
            ("assess_sl_calf", {}),
            ("assess_y_balance", {}),
            ("assess_sl_hop", {})]))
    else:
        power = {
            1: ("box_jump", {"sets": 3, "reps": "3", "rpe": "7",
                             "purpose": "Knee-height box, quiet landings, "
                             "always step down."}),
            2: ("box_jump", {"sets": 4, "reps": "3", "rpe": "7-8",
                             "purpose": "One box height up if every Week-1 "
                             "landing was quiet."}),
            3: ("skater_bound", {"sets": 4, "reps": "4/side", "rpe": "8",
                                 "purpose": "Peak power week: lateral bounds "
                                 "with frozen 2-s landings — film the "
                                 "knee."}),
        }[w]
        sections.append(("Power & Plyometrics (fresh)", [power]))
    strength = {
        1: [("leg_press", {"sets": 4, "reps": "10", "rpe": "7"}),
            ("hack_squat", {"sets": 3, "reps": "10", "rpe": "7"}),
            ("rfe_split_squat", {"sets": 3, "reps": "8/side", "rpe": "7",
                                 "equipment": "Bench + dumbbells"}),
            ("leg_extension", {"sets": 3, "reps": "12", "rpe": "7"}),
            ("leg_curl_machine", {"sets": 3, "reps": "10", "rpe": "7-8"}),
            ("smith_calf", {"sets": 4, "reps": "10", "rpe": "7"})],
        2: [("leg_press", {"sets": 4, "reps": "8", "rpe": "7-8"}),
            ("single_leg_press", {"sets": 3, "reps": "8/side", "rpe": "7-8",
                                  "purpose": "New: close the left-right gap "
                                  "— weak side first."}),
            ("romanian_deadlift", {"sets": 3, "reps": "8", "rpe": "7-8",
                                   "equipment": "Heavy dumbbells",
                                   "purpose": "Heavy DB hinge for the "
                                   "hamstrings at length."}),
            ("leg_extension", {"sets": 3, "reps": "12", "rpe": "7-8"}),
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
            ("leg_curl_machine", {"sets": 3, "reps": "8-10", "rpe": "8"}),
            ("smith_calf", {"sets": 4, "reps": "8-10", "rpe": "8"})],
        4: [("leg_press", {"sets": 3, "reps": "10", "rpe": "7",
                           "purpose": "Moderate plates on test day — "
                           "smooth reps only."}),
            ("leg_curl_machine", {"sets": 2, "reps": "10-12", "rpe": "7"}),
            ("smith_calf", {"sets": 3, "reps": "10", "rpe": "7"})],
    }[w]
    rehab = {
        1: [("nordic_curl", {"sets": 3, "reps": "5", "rpe": "8"}),
            ("copenhagen", {"sets": 2, "reps": "20 s/side", "rpe": "7"})],
        2: [("nordic_curl", {"sets": 3, "reps": "6", "rpe": "8"}),
            ("copenhagen", {"sets": 2, "reps": "15-20 s/side", "rpe": "8",
                            "setup": "Progress to the LONG lever: the top "
                            "FOOT (not the knee) rests on the bench."})],
        3: [("nordic_curl", {"sets": 3, "reps": "6-8", "rpe": "8"}),
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
    return _day(DAY_FOCUS["Tuesday"], sections)


def _back_day(week):
    """Wednesday — BACK. Vertical pull + horizontal rows + biceps."""
    w = week
    sections = [
        ("Warm-Up", ["cardio_warmup_20"]),
        ("Mobility", ["cat_cow", "open_book"]),
        ("Activation", [
            ("scap_pushup", {"sets": 2}),
            ("band_pull_apart", {"sets": 2})]),
    ]
    if w == 4:
        sections.append(("Assessment", [
            ("pullup", {"sets": 1, "reps": "TEST — max strict reps (record "
                        "the number + assist used)", "rpe": "9",
                        "purpose": "Back-day benchmark: strict neutral-grip "
                        "reps to one shy of failure."})]))
    strength = {
        1: [("pullup", {"sets": 4, "reps": "5-8", "rpe": "7-8",
                        "purpose": "Set the assist for 5-8 strict reps; it "
                        "shrinks every week."}),
            ("lat_pulldown_machine", {"sets": 3, "reps": "10", "rpe": "7"}),
            ("seated_cable_row", {"sets": 3, "reps": "10", "rpe": "7"}),
            ("chest_supported_row", {"sets": 3, "reps": "10", "rpe": "7",
                                     "purpose": "New: heavy strict rowing "
                                     "with zero low-back cost."}),
            ("back_extension_45", {"sets": 3, "reps": "12", "rpe": "7"}),
            ("db_curl", {"sets": 3, "reps": "10/side", "rpe": "7"})],
        2: [("pullup", {"sets": 4, "reps": "5-8", "rpe": "8",
                        "purpose": "One notch less assist; keep the 3-s "
                        "negatives."}),
            ("chest_supported_row", {"sets": 4, "reps": "8-10", "rpe": "7-8"}),
            ("lat_pulldown_machine", {"sets": 3, "reps": "10", "rpe": "7-8"}),
            ("seated_cable_row", {"sets": 3, "reps": "10", "rpe": "7-8"}),
            ("back_extension_45", {"sets": 3, "reps": "12", "rpe": "7-8",
                                   "equipment": "Plate hugged to chest"}),
            ("db_curl", {"sets": 3, "reps": "10/side", "rpe": "7-8"})],
        3: [("pullup", {"sets": 4, "reps": "max strict (leave 1 in the "
                        "tank)", "rpe": "8",
                        "purpose": "Minimal assist — or bodyweight with "
                        "slow negatives on the last set."}),
            ("chest_supported_row", {"sets": 4, "reps": "8", "rpe": "8"}),
            ("lat_pulldown_machine", {"sets": 3, "reps": "8-10", "rpe": "8"}),
            ("seated_cable_row", {"sets": 3, "reps": "8-10", "rpe": "8"}),
            ("back_extension_45", {"sets": 3, "reps": "10-12", "rpe": "8",
                                   "equipment": "Heavier plate"}),
            ("db_curl", {"sets": 4, "reps": "10/side", "rpe": "8"})],
        4: [("chest_supported_row", {"sets": 3, "reps": "10", "rpe": "7"}),
            ("seated_cable_row", {"sets": 3, "reps": "10", "rpe": "7",
                                  "tempo": "2-2-2-1",
                                  "purpose": "Variation: 2-s pause on the "
                                  "ribs every rep."}),
            ("lat_pulldown_machine", {"sets": 2, "reps": "12", "rpe": "6-7"}),
            ("db_curl", {"sets": 3, "reps": "10/side", "rpe": "7"})],
    }[w]
    sections += [
        ("Strength", strength),
        ("Core", [("cable_pallof", {"sets": 3,
                                    "reps": "10/side" if w < 3
                                    else "10/side (split stance)"})]),
        ("Conditioning", [
            ("bike_intervals", {"reps": f"{8 + (w in (2, 3)) * 2} rounds",
                                "rpe": "8 work",
                                "purpose": "Optional finisher."})]),
        ("Cool-Down & Stretch", [
            "stretch_hamstring", "stretch_glute", "breathing_reset"]),
    ]
    return _day(DAY_FOCUS["Wednesday"], sections)


def _shoulder_day(week):
    """Thursday — SHOULDERS. Delts + traps + the rotator-cuff insurance
    block. Two days before the match: moderate legs-free work only."""
    w = week
    sections = [
        ("Warm-Up", ["cardio_warmup_20"]),
        ("Mobility", ["cat_cow", "open_book"]),
        ("Activation", [
            ("wall_slide", {"sets": 2}),
            ("band_pull_apart", {"sets": 2})]),
        ("Shoulder Rehabilitation", [
            ("band_er_90", {"sets": 2, "reps": "12", "rpe": "6-7"}),
            ("cable_er", {"sets": 2, "rpe": "7"})]),
    ]
    if w == 4:
        sections.append(("Assessment", [
            ("assess_plank", {})]))
    strength = {
        1: [("db_shoulder_press", {"sets": 4, "reps": "8", "rpe": "7",
                                   "purpose": "The day's anchor lift — "
                                   "neutral grip, elbows forward."}),
            ("lateral_raise", {"sets": 4, "reps": "12-15", "rpe": "7"}),
            ("rear_delt_fly", {"sets": 3, "reps": "15", "rpe": "7"}),
            ("cable_face_pull", {"sets": 3, "reps": "12", "rpe": "7"}),
            ("db_shrug", {"sets": 3, "reps": "12-15", "rpe": "7",
                          "purpose": "New: vertical-only trap work to "
                          "finish the day."})],
        2: [("db_shoulder_press", {"sets": 4, "reps": "8", "rpe": "7-8",
                                   "equipment": "Heavier DBs than Week 1"}),
            ("lateral_raise", {"sets": 4, "reps": "12", "rpe": "7-8"}),
            ("scaption_raise", {"sets": 3, "reps": "10-12", "rpe": "7"}),
            ("rear_delt_fly", {"sets": 3, "reps": "12-15", "rpe": "7-8"}),
            ("cable_face_pull", {"sets": 3, "reps": "12", "rpe": "7-8"}),
            ("db_shrug", {"sets": 3, "reps": "12", "rpe": "7-8"})],
        3: [("db_shoulder_press", {"sets": 5, "reps": "6", "rpe": "8",
                                   "purpose": "Top pressing week — "
                                   "heaviest clean sixes, zero grinding."}),
            ("lateral_raise", {"sets": 4, "reps": "10-12", "rpe": "8"}),
            ("rear_delt_fly", {"sets": 4, "reps": "12", "rpe": "8"}),
            ("cable_face_pull", {"sets": 3, "reps": "12", "rpe": "8"}),
            ("db_shrug", {"sets": 4, "reps": "10-12", "rpe": "8"})],
        4: [("db_shoulder_press", {"sets": 3, "reps": "8", "rpe": "7",
                                   "purpose": "Week-2 weights at perfect "
                                   "speed."}),
            ("lateral_raise", {"sets": 3, "reps": "12-15", "rpe": "7"}),
            ("cable_face_pull", {"sets": 3, "reps": "12", "rpe": "7"}),
            ("prone_ytw", {"sets": 2,
                           "purpose": "Cuff deload — quality letters, "
                           "gravity only."})],
    }[w]
    sections += [
        ("Strength", strength),
        ("Core", [("side_plank", {"sets": 2, "reps": "35-40 s/side",
                                  "rpe": "7"})]),
        ("Functional Finisher", [
            ("farmer_carry", {"sets": 3, "reps": "40 m",
                              "rpe": "7-8" if w != 3 else "8"})]),
        ("Cool-Down & Stretch", [
            "stretch_chest", "cross_body_stretch", "breathing_reset"]),
    ]
    return _day(DAY_FOCUS["Thursday"], sections)


def _week(n):
    return {
        "Monday": _chest_day(n),
        "Tuesday": _leg_day(n),
        "Wednesday": _back_day(n),
        "Thursday": _shoulder_day(n),
        "Friday": _friday(n),
        "Saturday": _saturday(n),
        "Sunday": _sunday(n),
    }


def default_program() -> dict:
    """Full materialised month: {week:int -> {day:str -> day_dict}}."""
    return {1: _week(1), 2: _week(2), 3: _week(3), 4: _week(4)}
