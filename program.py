"""
program.py
==========
ADVANCED BLOCK — for the trained athlete (4+ months of consistent gym
work, pain-free knee and shoulder through the earlier progressions):

  Week 1 – Advanced Load  (new heavy patterns grooved at RPE 7)
  Week 2 – Overload       (heavier bars, RPE 7-8)
  Week 3 – Power          (top loading + jumps, bounds, sprints, RPE 8)
  Week 4 – Peak + Retest  (reduced volume + benchmark battery)

Weekly schedule:
  Mon  Lower Body Strength & Power (front squat, leg press, jumps)
  Tue  Upper Body & Shoulder Building (presses, pull-ups, rows, raises)
  Wed  Posterior Chain (trap-bar, hip thrust, Nordics, Copenhagens)
  Thu  Speed, Power & Football Prep (sprints, bounds, lateral strength)
  Fri  Recovery
  Sat  Football (pre-match activation + post-match reset)
  Sun  Recovery + Mobility

Standing guardrails (non-negotiable regardless of training age):
- no behind-the-neck pressing or pulling, no dips, no barbell bench
- front squat replaces back squat (back-rack position stresses a
  post-dislocation shoulder)
- pressing depth capped at arms-parallel; pull-up bottoms stay ACTIVE
- jumps/bounds/sprints only fresh, pain-free, never within 48 h of
  a match; box jumps are always stepped down from

The materialised program (library data + weekly prescription overrides)
is what gets seeded into SQLite; Edit Mode then owns it.
"""

import copy

from exercise_library import EXERCISES

DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday",
        "Saturday", "Sunday"]

TRAINING_DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday"]

WEEK_THEMES = {
    1: ("Advanced Load",
        "New heavy patterns enter: front squat, seated DB shoulder press, "
        "pull-ups, box jumps and sprint strides. Loads stay one gear down "
        "(RPE 7) while the new movements are grooved — add weight only "
        "where technique is already crisp."),
    2: ("Overload",
        "Same structure, heavier bars (RPE 7-8). Walking lunges, barbell "
        "rows, single-leg press and low-incline pressing join. Add weight "
        "anywhere last week's final set was smooth."),
    3: ("Power",
        "Top loading week (RPE 8): heavier front squats and trap-bar "
        "pulls, higher box jumps, skater bounds and strides at 85%. "
        "Quality gates everything — power work ends the moment reps slow "
        "down."),
    4: ("Peak + Retest",
        "Volume drops, intensity stays honest, and the benchmark battery "
        "runs: wall-sit, single-leg calf raises, plank, Y-balance, "
        "single-leg hop — plus max strict pull-ups. Beat last block's "
        "numbers and write them all down."),
}

# Friendly names for the day focus
DAY_FOCUS = {
    "Monday":    "Lower Body Strength & Power — Quad Focus",
    "Tuesday":   "Upper Body & Shoulder Building",
    "Wednesday": "Posterior Chain — Hamstrings & Glutes",
    "Thursday":  "Speed, Power & Football Prep",
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
# WEEK 1 — ADVANCED LOAD
# ---------------------------------------------------------------------
def _week1():
    return {
        "Monday": _day(DAY_FOCUS["Monday"], [
            ("Warm-Up", ["cardio_warmup_20"]),
            ("Mobility", ["ankle_rocks", "worlds_greatest"]),
            ("Activation", [
                ("glute_bridge", {"sets": 2, "reps": "10"}),
                ("band_walk", {"sets": 2})]),
            ("Power & Plyometrics (fresh)", [
                ("box_jump", {"sets": 3, "reps": "3", "rpe": "7",
                              "purpose": "First week: knee-height box, "
                              "perfect quiet landings, always step down."})]),
            ("Strength", [
                ("front_squat", {"sets": 4, "reps": "6", "rpe": "7",
                                 "purpose": "New this block: groove the rack "
                                 "position and depth with modest plates — "
                                 "the bar gets heavy from Week 2."}),
                ("leg_press", {"sets": 3, "reps": "8", "rpe": "7-8"}),
                ("rfe_split_squat", {"sets": 3, "reps": "8/side", "rpe": "7",
                                     "equipment": "Bench + dumbbells"}),
                ("smith_calf", {"sets": 4, "reps": "10", "rpe": "7"})]),
            ("Rehabilitation", [
                ("leg_extension", {"sets": 3, "reps": "12", "rpe": "7"}),
                ("spanish_squat", {"sets": 2, "reps": "40 s iso hold",
                                   "rpe": "7"})]),
            ("Core", [
                ("cable_pallof", {"sets": 3})]),
            ("Conditioning", [
                ("bike_intervals", {"reps": "8 rounds (8 min)", "rpe": "8 work",
                                    "purpose": "Optional finisher — the 20-min "
                                    "warm-up already banked aerobic work; skip "
                                    "if the legs are done."})]),
            ("Cool-Down & Stretch", [
                "stretch_quad", "stretch_calf", "breathing_reset"]),
        ]),
        "Tuesday": _day(DAY_FOCUS["Tuesday"], [
            ("Warm-Up", ["cardio_warmup_20"]),
            ("Mobility", ["cat_cow", "open_book"]),
            ("Activation", [
                ("scap_pushup", {"sets": 2, "reps": "12"}),
                ("band_pull_apart", {"sets": 2})]),
            ("Shoulder Rehabilitation", [
                ("band_er_90", {"sets": 2, "reps": "12", "rpe": "6-7"}),
                ("cable_er", {"sets": 2, "rpe": "7"})]),
            ("Strength", [
                ("db_shoulder_press", {"sets": 4, "reps": "8", "rpe": "7",
                                       "purpose": "New: direct overhead "
                                       "building — neutral grip, elbows "
                                       "forward, moderate first week."}),
                ("pullup", {"sets": 4, "reps": "5-8", "rpe": "7-8",
                            "purpose": "New: set the assist for 5-8 strict "
                            "reps; the assist shrinks every week."}),
                ("incline_db_press", {"sets": 3, "reps": "8", "rpe": "7"}),
                ("seated_cable_row", {"sets": 3, "reps": "10", "rpe": "7-8"}),
                ("lateral_raise", {"sets": 3, "reps": "12-15", "rpe": "7"})]),
            ("Core", [
                ("plank_tap", {"sets": 2, "reps": "10 taps/side", "rpe": "7"})]),
            ("Functional Finisher", [
                ("farmer_carry", {"sets": 3, "reps": "40 m", "rpe": "8"})]),
            ("Cool-Down & Stretch", [
                "stretch_chest", "cross_body_stretch", "breathing_reset"]),
        ]),
        "Wednesday": _day(DAY_FOCUS["Wednesday"], [
            ("Warm-Up", ["cardio_warmup_20"]),
            ("Mobility", ["lateral_leg_swings", "worlds_greatest"]),
            ("Activation", [
                ("bridge_march", {"sets": 2}),
                ("monster_walk", {"sets": 2})]),
            ("Strength", [
                ("trap_bar_deadlift", {"sets": 4, "reps": "6", "rpe": "7"}),
                ("barbell_hip_thrust", {"sets": 4, "reps": "8", "rpe": "7-8"}),
                ("leg_curl_machine", {"sets": 3, "reps": "10", "rpe": "7-8"}),
                ("seated_calf_machine", {"sets": 3, "reps": "12", "rpe": "7"})]),
            ("Rehabilitation", [
                ("nordic_curl", {"sets": 3, "reps": "5", "rpe": "8"}),
                ("copenhagen", {"sets": 2, "reps": "20 s/side", "rpe": "7"})]),
            ("Core", [
                ("side_plank_leglift", {"sets": 2, "reps": "8 lifts/side",
                                        "rpe": "7"})]),
            ("Balance", [("sl_reach", {"sets": 2,
                          "equipment": "Dumbbell at chest"})]),
            ("Conditioning", [
                ("bike_intervals", {"reps": "10 rounds (10 min)",
                                    "rpe": "8 work"})]),
            ("Cool-Down & Stretch", [
                "stretch_hamstring", "stretch_glute", "breathing_reset"]),
        ]),
        "Thursday": _day(DAY_FOCUS["Thursday"], [
            ("Warm-Up", ["cardio_warmup_20"]),
            ("Mobility", ["leg_swings", "ankle_rocks"]),
            ("Activation", [
                ("band_walk", {"sets": 2}),
                ("deadbug", {"sets": 2})]),
            ("Speed (fresh)", [
                ("sprint_strides", {"reps": "5 × 60 m (build to ~80%)",
                                    "rpe": "7-8",
                                    "purpose": "First week: five smooth "
                                    "build-ups to 80% — grooving mechanics, "
                                    "not racing."})]),
            ("Power & Plyometrics (fresh)", [
                ("skater_bound", {"sets": 3, "reps": "3/side", "rpe": "7",
                                  "purpose": "First week: short bounds, "
                                  "frozen 2-s landings, film the knee."})]),
            ("Strength", [
                ("lateral_step_up", {"sets": 3, "reps": "8/side", "rpe": "7-8",
                                     "equipment": "Box + dumbbells"}),
                ("back_extension_45", {"sets": 3, "reps": "12", "rpe": "7"})]),
            ("Core", [
                ("suitcase_carry", {"sets": 3, "reps": "30 m/side", "rpe": "8"})]),
            ("Conditioning (Football Prep)", [
                ("shadow_footwork", {"reps": "8 min, crisp", "rpe": "7"})]),
            ("Cool-Down & Stretch", [
                "stretch_hip_flexor", "stretch_calf", "breathing_reset"]),
        ]),
        "Friday": _friday(1),
        "Saturday": _saturday(1),
        "Sunday": _sunday(1),
    }


# ---------------------------------------------------------------------
# WEEK 2 — OVERLOAD
# ---------------------------------------------------------------------
def _week2():
    return {
        "Monday": _day(DAY_FOCUS["Monday"], [
            ("Warm-Up", ["cardio_warmup_20"]),
            ("Mobility", ["ankle_rocks", "worlds_greatest"]),
            ("Activation", [
                ("glute_bridge", {"sets": 2, "reps": "10"}),
                ("band_walk", {"sets": 2})]),
            ("Power & Plyometrics (fresh)", [
                ("box_jump", {"sets": 4, "reps": "3", "rpe": "7-8",
                              "purpose": "One box height up if every Week-1 "
                              "landing was quiet."})]),
            ("Strength", [
                ("front_squat", {"sets": 4, "reps": "5", "rpe": "7-8",
                                 "purpose": "Add 2.5-5 kg per side on last "
                                 "week — the pattern is grooved, now load "
                                 "it."}),
                ("hack_squat", {"sets": 3, "reps": "8-10", "rpe": "7-8",
                                "purpose": "New: guided heavy quad overload "
                                "behind the front squat."}),
                ("walking_lunge", {"sets": 2, "reps": "10 steps/side",
                                   "rpe": "7-8",
                                   "purpose": "New: continuous single-leg "
                                   "loading — the most football-specific "
                                   "strength there is."}),
                ("smith_calf", {"sets": 4, "reps": "10", "rpe": "7-8"})]),
            ("Rehabilitation", [
                ("leg_extension", {"sets": 3, "reps": "12", "rpe": "7-8"})]),
            ("Core", [
                ("cable_pallof", {"sets": 3, "reps": "10/side (half-kneeling)"})]),
            ("Conditioning", [
                ("bike_intervals", {"reps": "10 rounds (10 min)",
                                    "rpe": "8 work",
                                    "purpose": "Optional — skip if the "
                                    "lunges emptied the tank."})]),
            ("Cool-Down & Stretch", [
                "stretch_quad", "stretch_calf", "breathing_reset"]),
        ]),
        "Tuesday": _day(DAY_FOCUS["Tuesday"], [
            ("Warm-Up", ["cardio_warmup_20"]),
            ("Mobility", ["cat_cow", "open_book"]),
            ("Activation", [
                ("scap_pushup", {"sets": 2, "reps": "12"}),
                ("wall_slide", {"sets": 2})]),
            ("Shoulder Rehabilitation", [
                ("band_er_90", {"sets": 2, "reps": "12", "rpe": "7"}),
                ("cable_er", {"sets": 2, "rpe": "7",
                              "equipment": "One plate heavier"})]),
            ("Strength", [
                ("db_shoulder_press", {"sets": 4, "reps": "8", "rpe": "7-8",
                                       "equipment": "Heavier DBs than Week 1"}),
                ("pullup", {"sets": 4, "reps": "5-8", "rpe": "8",
                            "purpose": "Reduce the assist one notch; keep "
                            "the 3-s negatives."}),
                ("barbell_row", {"sets": 4, "reps": "6-8", "rpe": "7-8",
                                 "purpose": "New: the heaviest horizontal "
                                 "pull — strict torso, bar to the ribs."}),
                ("db_bench", {"sets": 3, "reps": "8", "rpe": "7-8"}),
                ("lateral_raise", {"sets": 3, "reps": "12-15", "rpe": "7"}),
                ("rear_delt_fly", {"sets": 2, "reps": "15", "rpe": "7"})]),
            ("Core", [
                ("plank_tap", {"sets": 2, "reps": "10 taps/side", "rpe": "7"})]),
            ("Cool-Down & Stretch", [
                "stretch_chest", "cross_body_stretch", "breathing_reset"]),
        ]),
        "Wednesday": _day(DAY_FOCUS["Wednesday"], [
            ("Warm-Up", ["cardio_warmup_20"]),
            ("Mobility", ["lateral_leg_swings", "worlds_greatest"]),
            ("Activation", [
                ("bridge_march", {"sets": 2}),
                ("monster_walk", {"sets": 2})]),
            ("Strength", [
                ("trap_bar_deadlift", {"sets": 4, "reps": "5", "rpe": "7-8",
                                       "purpose": "Add 5 kg on Week 1 if "
                                       "every rep was crisp."}),
                ("barbell_rdl", {"sets": 3, "reps": "8", "rpe": "7-8"}),
                ("single_leg_hip_thrust", {"sets": 3, "reps": "8/side",
                                           "rpe": "7-8",
                                           "equipment": "Dumbbell on the "
                                           "working hip"}),
                ("leg_curl_machine", {"sets": 3, "reps": "10", "rpe": "8"})]),
            ("Rehabilitation", [
                ("nordic_curl", {"sets": 3, "reps": "6", "rpe": "8"}),
                ("copenhagen", {"sets": 2, "reps": "15-20 s/side", "rpe": "8",
                                "setup": "Progress to the LONG lever this "
                                "week: the top FOOT (not the knee) rests on "
                                "the bench.",
                                "purpose": "Long-lever progression — the "
                                "full-strength version of football's best "
                                "groin protector."})]),
            ("Core", [
                ("side_plank_leglift", {"sets": 2, "reps": "8 lifts/side",
                                        "rpe": "7-8"})]),
            ("Conditioning", [
                ("bike_intervals", {"reps": "12 rounds (12 min)",
                                    "rpe": "8 work"})]),
            ("Cool-Down & Stretch", [
                "stretch_hamstring", "stretch_glute", "breathing_reset"]),
        ]),
        "Thursday": _day(DAY_FOCUS["Thursday"], [
            ("Warm-Up", ["cardio_warmup_20"]),
            ("Mobility", ["leg_swings", "ankle_rocks"]),
            ("Activation", [
                ("band_walk", {"sets": 2}),
                ("deadbug", {"sets": 2})]),
            ("Speed (fresh)", [
                ("sprint_strides", {"reps": "6 × 70 m (build to ~80-85%)",
                                    "rpe": "8"})]),
            ("Power & Plyometrics (fresh)", [
                ("skater_bound", {"sets": 3, "reps": "4/side", "rpe": "7-8",
                                  "purpose": "Slightly longer bounds — "
                                  "landings still frozen for 2 s."})]),
            ("Strength", [
                ("lateral_step_up", {"sets": 3, "reps": "8/side", "rpe": "8",
                                     "equipment": "Higher box + dumbbells"}),
                ("lateral_lunge", {"sets": 3, "reps": "8/side", "rpe": "7-8",
                                   "equipment": "Heavier dumbbell at chest"}),
                ("back_extension_45", {"sets": 3, "reps": "12", "rpe": "7-8",
                                       "equipment": "Plate hugged to chest"})]),
            ("Core", [
                ("suitcase_carry", {"sets": 3, "reps": "30 m/side", "rpe": "8"})]),
            ("Conditioning (Football Prep)", [
                ("shadow_footwork", {"reps": "8 min, quick feet", "rpe": "7"})]),
            ("Cool-Down & Stretch", [
                "stretch_hip_flexor", "stretch_calf", "breathing_reset"]),
        ]),
        "Friday": _friday(2),
        "Saturday": _saturday(2),
        "Sunday": _sunday(2),
    }


# ---------------------------------------------------------------------
# WEEK 3 — POWER
# ---------------------------------------------------------------------
def _week3():
    return {
        "Monday": _day(DAY_FOCUS["Monday"], [
            ("Warm-Up", ["cardio_warmup_20"]),
            ("Mobility", ["ankle_rocks", "worlds_greatest"]),
            ("Activation", [
                ("glute_bridge", {"sets": 2, "reps": "10"}),
                ("band_walk", {"sets": 2})]),
            ("Power & Plyometrics (fresh)", [
                ("box_jump", {"sets": 5, "reps": "3", "rpe": "8",
                              "purpose": "Peak jump week — highest box you "
                              "land QUIETLY on. Step down, full rest."})]),
            ("Strength", [
                ("front_squat", {"sets": 5, "reps": "5", "rpe": "8",
                                 "purpose": "Top squat week — heaviest "
                                 "clean fives of the block."}),
                ("single_leg_press", {"sets": 3, "reps": "8/side", "rpe": "8",
                                      "purpose": "New: expose and close the "
                                      "left-right gap — weak side first."}),
                ("walking_lunge", {"sets": 3, "reps": "10 steps/side",
                                   "rpe": "8",
                                   "equipment": "Heavier dumbbells"}),
                ("smith_calf", {"sets": 4, "reps": "8-10", "rpe": "8"})]),
            ("Rehabilitation", [
                ("leg_extension", {"sets": 3, "reps": "10-12", "rpe": "8"})]),
            ("Core", [
                ("cable_pallof", {"sets": 3, "reps": "10/side (split stance)"})]),
            ("Cool-Down & Stretch", [
                "stretch_quad", "stretch_calf", "breathing_reset"]),
        ]),
        "Tuesday": _day(DAY_FOCUS["Tuesday"], [
            ("Warm-Up", ["cardio_warmup_20"]),
            ("Mobility", ["cat_cow", "open_book"]),
            ("Activation", [
                ("scap_pushup", {"sets": 2, "reps": "12"}),
                ("band_pull_apart", {"sets": 2})]),
            ("Shoulder Rehabilitation", [
                ("band_er_90", {"sets": 2, "reps": "12", "rpe": "7"}),
                ("cable_er", {"sets": 2, "rpe": "7-8"})]),
            ("Strength", [
                ("db_shoulder_press", {"sets": 5, "reps": "6", "rpe": "8",
                                       "purpose": "Top pressing week — "
                                       "heaviest clean sixes, elbows "
                                       "forward, zero grinding."}),
                ("pullup", {"sets": 4, "reps": "max strict (leave 1 in "
                            "the tank)", "rpe": "8",
                            "purpose": "Minimal assist — or bodyweight with "
                            "slow negatives on the last set."}),
                ("barbell_row", {"sets": 4, "reps": "6", "rpe": "8"}),
                ("incline_db_press", {"sets": 3, "reps": "8", "rpe": "8"}),
                ("lateral_raise", {"sets": 4, "reps": "12", "rpe": "7-8"})]),
            ("Core", [
                ("plank_tap", {"sets": 3, "reps": "10 taps/side", "rpe": "7-8"})]),
            ("Functional Finisher", [
                ("suitcase_carry", {"sets": 3, "reps": "30 m/side", "rpe": "8"})]),
            ("Cool-Down & Stretch", [
                "stretch_chest", "cross_body_stretch", "breathing_reset"]),
        ]),
        "Wednesday": _day(DAY_FOCUS["Wednesday"], [
            ("Warm-Up", ["cardio_warmup_20"]),
            ("Mobility", ["lateral_leg_swings", "worlds_greatest"]),
            ("Activation", [
                ("bridge_march", {"sets": 2}),
                ("monster_walk", {"sets": 2})]),
            ("Strength", [
                ("trap_bar_deadlift", {"sets": 5, "reps": "3", "rpe": "8",
                                       "purpose": "Peak pull — heavy, crisp "
                                       "triples with full resets. Two reps "
                                       "always left in the tank."}),
                ("barbell_hip_thrust", {"sets": 4, "reps": "6-8", "rpe": "8"}),
                ("leg_curl_machine", {"sets": 3, "reps": "8-10", "rpe": "8"}),
                ("eccentric_calf", {"sets": 3, "reps": "10/side", "rpe": "7"})]),
            ("Rehabilitation", [
                ("nordic_curl", {"sets": 3, "reps": "6-8", "rpe": "8"}),
                ("copenhagen", {"sets": 2, "reps": "20-25 s/side", "rpe": "8",
                                "setup": "Long lever (foot on the bench)."})]),
            ("Core", [
                ("side_plank_leglift", {"sets": 3, "reps": "8 lifts/side",
                                        "rpe": "8"})]),
            ("Conditioning", [
                ("bike_intervals", {"reps": "12 rounds, harder gear",
                                    "rpe": "8-9 work"})]),
            ("Cool-Down & Stretch", [
                "stretch_hamstring", "stretch_glute", "breathing_reset"]),
        ]),
        "Thursday": _day(DAY_FOCUS["Thursday"], [
            ("Warm-Up", ["cardio_warmup_20"]),
            ("Mobility", ["leg_swings", "ankle_rocks"]),
            ("Activation", [
                ("band_walk", {"sets": 2}),
                ("deadbug", {"sets": 2})]),
            ("Speed (fresh)", [
                ("sprint_strides", {"reps": "6 × 80 m (float at 85%)",
                                    "rpe": "8",
                                    "purpose": "Peak speed week — tall hips, "
                                    "relaxed face, long gradual "
                                    "decelerations."})]),
            ("Power & Plyometrics (fresh)", [
                ("skater_bound", {"sets": 4, "reps": "4/side", "rpe": "8",
                                  "purpose": "Longest bounds of the block — "
                                  "every landing still frozen and silent."})]),
            ("Strength", [
                ("lateral_step_up", {"sets": 3, "reps": "6/side", "rpe": "8",
                                     "equipment": "Heavier dumbbells"}),
                ("back_extension_45", {"sets": 3, "reps": "10-12", "rpe": "8",
                                       "equipment": "Heavier plate"})]),
            ("Core", [
                ("cable_pallof", {"sets": 3, "reps": "10/side"})]),
            ("Conditioning (Football Prep)", [
                ("shadow_footwork", {"reps": "8 min at match tempo", "rpe": "7-8"})]),
            ("Cool-Down & Stretch", [
                "stretch_hip_flexor", "stretch_calf", "breathing_reset"]),
        ]),
        "Friday": _friday(3),
        "Saturday": _saturday(3),
        "Sunday": _sunday(3),
    }


# ---------------------------------------------------------------------
# WEEK 4 — PEAK + RETEST
# ---------------------------------------------------------------------
def _week4():
    return {
        "Monday": _day(DAY_FOCUS["Monday"], [
            ("Warm-Up", ["cardio_warmup_20"]),
            ("Mobility", ["ankle_rocks", "worlds_greatest"]),
            ("Activation", [
                ("glute_bridge", {"sets": 2, "reps": "10"}),
                ("band_walk", {"sets": 2})]),
            ("Assessment", [
                ("assess_wall_sit", {}),
                ("assess_sl_calf", {})]),
            ("Strength (moderate — testing week)", [
                ("front_squat", {"sets": 3, "reps": "5", "rpe": "7",
                                 "purpose": "Week-2 weights, perfect bar "
                                 "speed — stay sharp for the tests."}),
                ("leg_press", {"sets": 2, "reps": "10", "rpe": "7"}),
                ("smith_calf", {"sets": 3, "reps": "10", "rpe": "7"})]),
            ("Core", [
                ("cable_pallof", {"sets": 2})]),
            ("Conditioning", [
                ("bike_tempo", {"reps": "15 min", "rpe": "6"})]),
            ("Cool-Down & Stretch", [
                "stretch_quad", "stretch_calf", "breathing_reset"]),
        ]),
        "Tuesday": _day(DAY_FOCUS["Tuesday"], [
            ("Warm-Up", ["cardio_warmup_20"]),
            ("Mobility", ["cat_cow", "open_book"]),
            ("Activation", [
                ("scap_pushup", {"sets": 2}),
                ("band_pull_apart", {"sets": 2})]),
            ("Assessment", [
                ("pullup", {"sets": 1, "reps": "TEST — max strict reps "
                            "(record the number + assist used)", "rpe": "9",
                            "purpose": "Block benchmark: strict neutral-grip "
                            "reps to one shy of failure. Beat it next "
                            "block."})]),
            ("Strength (variation)", [
                ("db_shoulder_press", {"sets": 3, "reps": "8", "rpe": "7",
                                       "purpose": "Week-2 weights at "
                                       "perfect speed."}),
                ("seated_cable_row", {"sets": 3, "reps": "10", "rpe": "7",
                                      "tempo": "2-2-2-1",
                                      "purpose": "Variation: 2-s pause on "
                                      "the ribs every rep."}),
                ("lateral_raise", {"sets": 3, "reps": "12-15", "rpe": "7"}),
                ("prone_ytw", {"sets": 2,
                               "purpose": "Cuff deload week — quality "
                               "letters, gravity only."})]),
            ("Functional Finisher", [
                ("farmer_carry", {"sets": 3, "reps": "40 m", "rpe": "7-8"})]),
            ("Cool-Down & Stretch", [
                "stretch_chest", "cross_body_stretch", "breathing_reset"]),
        ]),
        "Wednesday": _day(DAY_FOCUS["Wednesday"], [
            ("Warm-Up", ["cardio_warmup_20"]),
            ("Mobility", ["lateral_leg_swings", "worlds_greatest"]),
            ("Activation", [
                ("bridge_march", {"sets": 2}),
                ("band_walk", {"sets": 2})]),
            ("Strength (variation)", [
                ("barbell_rdl", {"sets": 3, "reps": "8", "rpe": "7",
                                 "tempo": "4-1-1-0",
                                 "purpose": "Variation: 4-s eccentric at "
                                 "Week-2 load."}),
                ("barbell_hip_thrust", {"sets": 3, "reps": "8", "rpe": "7",
                                        "tempo": "2-3-1-1",
                                        "purpose": "Variation: 3-s top "
                                        "squeeze."}),
                ("leg_curl_machine", {"sets": 2, "reps": "10-12", "rpe": "7"})]),
            ("Rehabilitation", [
                ("nordic_curl", {"sets": 2, "reps": "5-6", "rpe": "8",
                                 "safety": "Reduced volume on test week; "
                                 "never the day before football."}),
                ("copenhagen", {"sets": 2, "reps": "20 s/side", "rpe": "7",
                                "setup": "Long lever (foot on the bench)."})]),
            ("Conditioning", [
                ("bike_intervals", {"reps": "10 rounds (10 min)",
                                    "rpe": "8 work"})]),
            ("Cool-Down & Stretch", [
                "stretch_hamstring", "stretch_glute", "breathing_reset"]),
        ]),
        "Thursday": _day(DAY_FOCUS["Thursday"], [
            ("Warm-Up", ["cardio_warmup_20"]),
            ("Mobility", ["leg_swings", "ankle_rocks", "worlds_greatest"]),
            ("Activation", [
                ("band_walk", {"sets": 2}),
                ("glute_bridge", {"sets": 2})]),
            ("Assessment Battery (fresh + fully warm)", [
                ("assess_y_balance", {}),
                ("assess_sl_hop", {}),
                ("assess_plank", {})]),
            ("Speed (fresh)", [
                ("sprint_strides", {"reps": "4 × 60 m (smooth, ~80%)",
                                    "rpe": "7",
                                    "purpose": "Light speed maintenance "
                                    "after the tests."})]),
            ("Light Functional Work (after tests)", [
                ("suitcase_carry", {"sets": 2, "reps": "30 m/side", "rpe": "7"}),
                ("lat_pulldown_machine", {"sets": 2, "reps": "12", "rpe": "6-7"})]),
            ("Conditioning (Football Prep)", [
                ("shadow_footwork", {"reps": "6 min crisp", "rpe": "6-7"})]),
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
