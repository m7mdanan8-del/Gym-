"""
exercise_library.py
===================
Evidence-based exercise library for a footballer (34 y/o, 168 cm, 72 kg)
rehabilitating a partial ACL tear (no surgery, cleared for conservative
training) and a previously dislocated right shoulder with suspected labral
injury.

Every exercise carries the full professional prescription:
name, target muscles, purpose, sets/reps/tempo/rest/RPE, start position,
execution, coaching cues, coaching tips, common mistakes, safety notes,
progression, regression, alternative — plus a movement-pattern illustration
key (see illustrations.py) and a reliable YouTube demonstration link.

YouTube links are curated *search deep-links* ("exercise name + proper form")
so they never go stale; Edit Mode lets the user pin a specific video URL,
which the app then embeds directly.
"""

from urllib.parse import quote_plus


def _yt(query: str) -> str:
    """Reliable, never-stale YouTube demonstration link."""
    return "https://www.youtube.com/results?search_query=" + quote_plus(query)


def _ex(name, pattern, target, purpose, sets, reps, tempo, rest, rpe,
        setup, execution, cues, tips, mistakes, safety,
        progression, regression, alternative,
        equipment="Bodyweight", yt_query=None, image_url="", gif_url="",
        video_url=""):
    return {
        "name": name,
        "pattern": pattern,          # key into illustrations.py
        "target": target,
        "purpose": purpose,
        "equipment": equipment,
        "sets": sets,
        "reps": reps,                # string: "10-12", "30-45 s", "8/side"
        "tempo": tempo,              # ecc-pause-con-pause, e.g. "3-1-1-0"
        "rest": rest,                # e.g. "60 s"
        "rpe": rpe,                  # e.g. "6-7"
        "setup": setup,              # correct starting position
        "execution": execution,      # how to perform the movement
        "cues": cues,                # list[str] – key coaching cues
        "tips": tips,                # list[str] – coaching tips
        "mistakes": mistakes,        # list[str] – common mistakes
        "safety": safety,            # injury-specific safety note
        "progression": progression,
        "regression": regression,
        "alternative": alternative,
        "youtube": _yt(yt_query or f"{name} exercise proper form"),
        "image_url": image_url,      # optional user-supplied picture
        "gif_url": gif_url,          # optional user-supplied GIF
        "video_url": video_url,      # optional pinned video (embedded)
    }


EXERCISES = {

    # ================================================================
    # WARM-UP
    # ================================================================
    "bike_warmup": _ex(
        "Stationary Bike – Easy Spin", "bike",
        "Whole body / knee synovial fluid",
        "Raises tissue temperature and lubricates the knee joint with zero "
        "impact — the safest way to prepare a partial-ACL knee for loading.",
        1, "5-8 min", "steady", "—", "3-4",
        "Saddle height so the knee keeps a slight bend (~25-30°) at the "
        "bottom of the pedal stroke. Light resistance.",
        "Pedal smoothly at 80-90 rpm. Breathe through the nose; you should "
        "be able to hold a conversation throughout.",
        ["Smooth circles, not stomping", "Relaxed shoulders", "Nasal breathing"],
        ["If the knee feels stiff, spend the first 2 minutes at almost zero "
         "resistance before adding any.",
         "Use this time to mentally rehearse the session."],
        ["Saddle too low (increases patellofemoral compression)",
         "Sprinting cold"],
        "Pain-free cardio choice for ACL rehab. Keep it easy — this is a "
        "warm-up, not conditioning.",
        "Add 30 s of moderate resistance in the final minute.",
        "March in place or brisk 5-minute walk.",
        "Brisk incline walk or elliptical.",
        equipment="Stationary bike",
        yt_query="stationary bike warm up proper setup saddle height"),

    "brisk_march": _ex(
        "Dynamic March + Light Jog in Place", "jog",
        "Whole body",
        "General warm-up when no bike is available; raises heart rate and "
        "core temperature with controlled, low-amplitude impact.",
        1, "3-4 min", "rhythmic", "—", "3-4",
        "Stand tall, arms relaxed at your sides.",
        "March with high knees for 30 s, then transition to a very light "
        "jog in place for 30 s. Alternate for 3-4 minutes.",
        ["Land softly through the mid-foot", "Tall posture", "Swing the arms"],
        ["Progress amplitude gradually — start small, finish bouncy."],
        ["Slamming the heels down", "Holding the breath"],
        "Keep impact minimal for the first minute while the knee warms up.",
        "Add lateral shuffles and backwards jogging.",
        "Marching only, no jogging.",
        "Stationary bike easy spin.",
        yt_query="dynamic warm up march high knees light jog"),

    # ================================================================
    # MOBILITY
    # ================================================================
    "leg_swings": _ex(
        "Front-to-Back Leg Swings", "leg_swing",
        "Hip flexors, hamstrings, hip capsule",
        "Dynamic hip mobility that prepares the swing mechanics used in "
        "kicking and sprinting.",
        1, "12/side", "dynamic controlled", "—", "3",
        "Stand side-on to a wall, hand on it for support, weight on the leg "
        "closest to the wall.",
        "Swing the outside leg forward and back like a pendulum, letting the "
        "range grow gradually with each swing. Keep the trunk tall and still.",
        ["Move from the hip, not the low back", "Tall chest",
         "Range grows swing by swing"],
        ["The stance-leg glute should stay switched on — that is free "
         "single-leg stability work for the knee."],
        ["Arching the low back to fake range", "Ballistic max-range swings "
         "from the first rep"],
        "Controlled swings only — no forceful end-range kicking on a cold "
        "hamstring.",
        "Increase amplitude; add a toe-touch reach at the top.",
        "Smaller range, slower tempo.",
        "Standing knee-to-chest + heel-to-glute walk.",
        yt_query="front to back leg swings dynamic warm up"),

    "lateral_leg_swings": _ex(
        "Side-to-Side Leg Swings", "leg_swing",
        "Adductors, abductors, hip capsule",
        "Opens the hips in the frontal plane — the plane where footballers "
        "get injured. Prepares adductors for cutting and passing.",
        1, "12/side", "dynamic controlled", "—", "3",
        "Face a wall with both hands on it, standing on one leg.",
        "Swing the free leg across the body and out to the side, keeping "
        "the pelvis level and the trunk quiet.",
        ["Pelvis stays level", "Foot relaxed", "Build range gradually"],
        ["Feel a gentle stretch in the groin at the top of each swing — "
         "never a pull."],
        ["Twisting the trunk to create fake range", "Rushing"],
        "Groin strains happen to cold adductors — always precede sprint or "
        "cutting work with these.",
        "Increase amplitude and speed slightly.",
        "Standing hip abduction without swing.",
        "Cossack squat rock (bodyweight).",
        yt_query="lateral side to side leg swings warm up"),

    "worlds_greatest": _ex(
        "World's Greatest Stretch", "worlds_greatest",
        "Hip flexors, hamstrings, thoracic spine, adductors",
        "One movement that opens every area a footballer needs: hips, "
        "hamstrings and upper back rotation.",
        1, "5/side", "slow flow", "—", "4",
        "From a push-up position, step the right foot outside the right hand "
        "into a long lunge.",
        "Drop the right elbow toward the instep, then rotate the right arm "
        "up to the ceiling following it with your eyes. Return the hand, "
        "rock back to straighten the front knee (hamstring bias), then flow "
        "back to the lunge. Switch sides after all reps.",
        ["Long spine", "Rotate from the mid-back", "Exhale into each position"],
        ["Move slowly — this is mobility, not cardio.",
         "Follow the rotating hand with your eyes to drive thoracic rotation."],
        ["Collapsing the back hip", "Rotating from the low back instead of "
         "the mid-back"],
        "Keep the front knee tracking over the mid-foot; if the shoulder "
        "feels unstable overhead, reduce the rotation range.",
        "Add a hip-flexor pulse at the bottom of the lunge.",
        "Perform with the back knee resting on the floor.",
        "Half-kneeling hip flexor stretch + open book, done separately.",
        yt_query="world's greatest stretch tutorial"),

    "cat_cow": _ex(
        "Cat-Cow", "cat_cow",
        "Thoracic and lumbar spine, deep core",
        "Segmental spine mobility and a gentle nervous-system 'switch on' "
        "before loading.",
        1, "8-10 cycles", "slow with breath", "—", "2",
        "Quadruped: hands under shoulders, knees under hips, spine neutral.",
        "Inhale — drop the belly, lift the chest and tailbone (cow). "
        "Exhale — press the floor away, round the whole spine and tuck the "
        "chin (cat). Move one vertebra at a time.",
        ["Match movement to breath", "Push the floor away in cat",
         "Move the whole spine, not just the neck"],
        ["Great daily habit on recovery days too."],
        ["Only moving the neck and low back", "Rushing the cycles"],
        "Pain-free range only. Keeps the spine happy under farm carries and "
        "squats later in the session.",
        "Add thread-the-needle rotation between cycles.",
        "Seated version on a chair.",
        "Open book T-spine rotation.",
        yt_query="cat cow stretch proper form"),

    "open_book": _ex(
        "Open Book Thoracic Rotation", "cat_cow",
        "Thoracic spine, pec minor, posterior shoulder",
        "Restores mid-back rotation so the shoulder doesn't have to steal "
        "range — protective for a post-dislocation shoulder.",
        1, "8/side", "3 s hold at end range", "—", "3",
        "Lie on your left side, hips and knees bent to 90°, both arms "
        "extended together in front of the chest, palms touching.",
        "Keeping the knees glued down, lift the top (right) arm and open it "
        "across the body toward the floor behind you, following the hand "
        "with your eyes. Pause, breathe out, return.",
        ["Knees stay stacked and down", "Follow the hand with the eyes",
         "Exhale at end range"],
        ["Put a foam roller or cushion under the top knee if the low back "
         "twists."],
        ["Letting the knees separate (turns it into lumbar rotation)",
         "Forcing the arm to the floor"],
        "Move within comfortable shoulder range — the goal is mid-back "
        "rotation, not shoulder stretch. Stop short of any apprehension.",
        "Add a 5 s exhale hold at end range.",
        "Reduce the arc; keep the moving hand on the ribcage.",
        "Quadruped thread-the-needle.",
        yt_query="open book thoracic rotation exercise"),

    "ankle_rocks": _ex(
        "Knee-to-Wall Ankle Mobilisation", "ankle_mob",
        "Ankle dorsiflexion (soleus, joint capsule)",
        "Stiff ankles overload the ACL during squatting and landing — "
        "restoring dorsiflexion directly protects the knee.",
        2, "10/side", "2 s end-range hold", "20 s", "3",
        "Face a wall, one foot about a hand-length away from it, heel down.",
        "Drive the knee straight forward over the middle toes to touch the "
        "wall while the heel stays glued down. Pause, return. Move the foot "
        "back a centimetre when it gets easy.",
        ["Heel welded to the floor", "Knee tracks over 2nd-3rd toe",
         "Pain-free stretch, not pinch"],
        ["Measure your distance from the wall each week — it is a built-in "
         "progress test (aim ≥10 cm)."],
        ["Letting the heel lift", "Knee collapsing inward"],
        "A pinch at the front of the ankle means back off a little and work "
        "within the pain-free arc.",
        "Add a light dumbbell on the knee.",
        "Shorter distance from the wall.",
        "Half-kneeling ankle rock with hands on knee.",
        yt_query="knee to wall ankle dorsiflexion mobilization"),

    # ================================================================
    # ACTIVATION
    # ================================================================
    "glute_bridge": _ex(
        "Glute Bridge", "bridge",
        "Gluteus maximus, hamstrings",
        "Wakes up the glutes before loading. Strong glutes reduce dynamic "
        "knee valgus — the single biggest mechanical threat to an ACL.",
        2, "12-15", "2-1-2-1", "45 s", "5-6",
        "Lie on your back, knees bent, feet hip-width and close enough that "
        "your fingertips can graze your heels. Arms by your sides.",
        "Exhale, squeeze the glutes and lift the hips until knees-hips-"
        "shoulders form a straight line. Hold 1 s at the top, lower with "
        "control.",
        ["Squeeze glutes before you lift", "Ribs down, no back arch",
         "Push through the whole foot"],
        ["If you feel it in the hamstrings more than the glutes, bring the "
         "heels closer to your hips."],
        ["Arching the low back to fake height", "Pushing through the toes"],
        "Zero knee stress — this is a green-light exercise even on higher "
        "pain days.",
        "Single-leg glute bridge or add a dumbbell on the hips.",
        "Smaller range of motion; both arms pressing into the floor.",
        "Hip thrust with shoulders on a bench.",
        yt_query="glute bridge proper form physical therapy"),

    "single_leg_bridge": _ex(
        "Single-Leg Glute Bridge", "bridge",
        "Gluteus maximus, hamstrings, pelvic control",
        "Unilateral glute strength and pelvic stability — directly transfers "
        "to single-leg landing control that protects the ACL.",
        3, "8-10/side", "2-1-2-1", "45 s", "6-7",
        "Glute bridge position; extend one leg so the thighs stay parallel.",
        "Drive through the grounded heel and lift the hips without letting "
        "the pelvis tip toward the free-leg side. Pause, lower slowly.",
        ["Pelvis stays level like a table", "Drive the heel down",
         "Free leg thigh matches the working thigh"],
        ["Place your hands on the hip bones to feel any tilt."],
        ["Pelvis dropping on the free side", "Hyperextending the low back"],
        "If the hamstring cramps, shorten the range and build gradually.",
        "Add a slow 3 s lowering or a weight on the hips.",
        "Two-leg bridge with a 1-leg lower (up on 2, down on 1).",
        "B-stance hip thrust.",
        yt_query="single leg glute bridge form"),

    "clamshell": _ex(
        "Banded Clamshell", "clamshell",
        "Gluteus medius, deep hip rotators",
        "Glute medius controls the knee's position over the foot. Weakness "
        "here is directly linked to ACL injury risk in footballers.",
        2, "15/side", "2-1-2-0", "30 s", "6",
        "Lie on your side, hips bent ~45°, knees bent 90°, heels in line "
        "with your spine, mini-band just above the knees.",
        "Keeping the feet together and the pelvis stacked, lift the top "
        "knee against the band as high as possible without rolling back. "
        "Lower with control.",
        ["Pelvis stacked — don't roll backward", "Lead with the knee, not "
         "the foot", "Feel it in the side of the hip"],
        ["Put your top hand on your hip bone; if it rolls, the range is too "
         "big."],
        ["Rolling the pelvis backward to fake range",
         "Moving fast and using momentum"],
        "Burning in the side of the glute is the goal; front-of-hip pinch "
        "means reset your pelvis position.",
        "Stronger band, or add a 2 s hold at the top.",
        "No band.",
        "Side-lying hip abduction.",
        equipment="Mini-band",
        yt_query="banded clamshell exercise glute medius"),

    "side_leg_raise": _ex(
        "Side-Lying Hip Abduction", "side_leg_raise",
        "Gluteus medius",
        "Isolates the hip's frontal-plane stabiliser through a longer lever "
        "than the clamshell — the next step in glute medius strength.",
        2, "12/side", "2-1-2-1", "30 s", "6",
        "Lie on your side in a straight line, bottom leg slightly bent for "
        "balance, top leg straight with the toes pointing slightly down.",
        "Lift the top leg to ~30-40° leading with the heel, pause 1 s, "
        "lower slowly. The leg should travel slightly behind the body line.",
        ["Toes down, heel up", "Leg slightly behind the torso",
         "Slow lowering"],
        ["If you feel it on the front/side of the thigh (TFL), you've "
         "drifted the leg forward — re-align."],
        ["Hiking the hip toward the ribs", "Swinging the leg"],
        "Height is not the goal — glute medius burn is. 30-40° is plenty.",
        "Add an ankle weight or mini-band at the ankles.",
        "Bend the top knee slightly (shorter lever).",
        "Standing banded hip abduction.",
        yt_query="side lying hip abduction gluteus medius proper form"),

    "band_walk": _ex(
        "Lateral Band Walk", "band_walk",
        "Gluteus medius, glute max, hip stabilisers",
        "Standing, football-specific glute activation — trains the hips to "
        "control the knees during defensive shuffles and cutting.",
        2, "10 steps/direction", "controlled", "30 s", "6",
        "Mini-band just above the knees (or at the ankles for more "
        "challenge). Quarter-squat athletic stance, feet hip-width, chest up.",
        "Step sideways leading with the heel, keeping constant tension on "
        "the band. Trail leg follows without dragging. Stay level — no "
        "bobbing up and down.",
        ["Stay low the whole set", "Knees pushed out against the band",
         "Lead with the heel"],
        ["Imagine a ceiling just above your head — glide, don't bounce."],
        ["Knees caving inward", "Standing up between steps",
         "Dragging the trail foot"],
        "Knees must track over the toes at all times — the band tries to "
        "pull them in; your job is to resist. That resistance IS the "
        "exercise.",
        "Band at the ankles, or add a diagonal (monster) walk.",
        "Band above the knees, higher stance.",
        "Monster walk or standing banded hip abduction.",
        equipment="Mini-band",
        yt_query="lateral band walk glute activation proper form"),

    "monster_walk": _ex(
        "Monster Walk (Diagonal Band Walk)", "band_walk",
        "Glute max + medius together",
        "Diagonal stepping pattern loads the glutes in the exact hip angles "
        "used when decelerating and changing direction on the pitch.",
        2, "10 steps forward + 10 back", "controlled", "30 s", "6",
        "Mini-band above the knees, athletic quarter-squat, feet hip-width.",
        "Walk forward taking wide diagonal steps (out and forward), keeping "
        "band tension constant. Then reverse, stepping back and out.",
        ["Wide steps — keep the band taut", "Hips low and level",
         "Toes pointing forward"],
        ["Backwards steps are where most people lose tension — stay wide."],
        ["Feet drifting narrow", "Torso rocking side to side"],
        "Same rule as all band work: knees never collapse inside the feet.",
        "Band at ankles; slower steps with a 1 s pause.",
        "Band above knees, smaller steps.",
        "Lateral band walk.",
        equipment="Mini-band",
        yt_query="monster walk resistance band exercise"),

    "quad_set_ssq": _ex(
        "Quad Set (Isometric Quad Activation)", "tke",
        "Quadriceps (especially VMO)",
        "Re-establishes the brain-to-quad connection that is inhibited "
        "after ACL injury. The foundation every knee session builds on.",
        2, "10 × 5 s holds", "5 s max squeeze", "20 s", "5",
        "Sit with the leg straight, a small rolled towel under the knee.",
        "Push the back of the knee down into the towel by squeezing the "
        "thigh as hard as comfortable, pulling the kneecap up toward the "
        "hip. Hold 5 s, fully relax between reps.",
        ["Pull the kneecap toward you", "Push the knee into the towel",
         "Full relax between holds"],
        ["Place a hand on the inner thigh just above the knee to feel the "
         "VMO fire."],
        ["Holding the breath", "Lifting the heel instead of pressing the "
         "knee down"],
        "Completely joint-safe. Do these daily — even on recovery days.",
        "Straight-leg raise with the quad locked.",
        "Shorter holds (3 s).",
        "Terminal knee extension with band.",
        yt_query="quad sets exercise ACL rehab"),

    "deadbug": _ex(
        "Dead Bug", "deadbug",
        "Deep core (transverse abdominis), anterior core",
        "Teaches the core to stay braced while the limbs move — exactly "
        "what happens when you strike a ball or reach for a tackle.",
        2, "8/side", "slow 3 s per rep", "45 s", "6",
        "Lie on your back, arms straight up over the chest, hips and knees "
        "at 90/90. Flatten the low back gently into the floor.",
        "Exhale and slowly lower the right arm overhead and the left leg "
        "toward the floor at the same time, stopping before the low back "
        "arches. Return and switch.",
        ["Low back stays glued to the floor", "Exhale as the limbs lower",
         "Slow is strong"],
        ["Press the non-moving foot's knee gently into your hand for extra "
         "core tension if needed."],
        ["Low back arching off the floor", "Holding the breath",
         "Racing through reps"],
        "If the back arches, shorten the leg lever (keep the knee more bent).",
        "Add a mini-band around the feet or hold a light plate over the chest.",
        "Move only the legs (heel taps), arms stay up.",
        "Bird dog.",
        yt_query="dead bug exercise proper form core"),

    "bird_dog": _ex(
        "Bird Dog", "bird_dog",
        "Multifidus, glutes, deep core, shoulder stabilisers",
        "Anti-rotation core control plus gentle, closed-chain shoulder "
        "loading — safe early work for the right shoulder.",
        2, "8/side", "2 s hold at top", "45 s", "5-6",
        "Quadruped, hands under shoulders, knees under hips, spine neutral. "
        "Imagine a glass of water resting on your low back.",
        "Reach the right arm forward and the left leg back until both are "
        "parallel to the floor. Hold 2 s without the hips tipping, return "
        "quietly, switch sides.",
        ["Don't spill the glass of water", "Reach long, don't lift high",
         "Toes and fingers pull in opposite directions"],
        ["Move slower than feels natural — wobble means it's working."],
        ["Hips rotating open", "Arching the neck to look up",
         "Leg swinging above hip height"],
        "The supporting arm gently loads the right shoulder in its safest "
        "position — push the floor away with it the whole time.",
        "Elbow-to-knee touch under the body between reps.",
        "Lift only the leg, or only the arm.",
        "Dead bug.",
        yt_query="bird dog exercise proper form"),

    "scap_pushup": _ex(
        "Scapular Push-Up", "pushup",
        "Serratus anterior",
        "The serratus anchors the shoulder blade to the ribcage — the "
        "foundation of a stable socket for a post-dislocation shoulder.",
        2, "10-12", "2-1-2-1", "45 s", "5-6",
        "High plank (or hands-elevated on a bench), arms straight, hands "
        "under shoulders.",
        "Without bending the elbows, let the chest sink as the shoulder "
        "blades pinch together, then push the floor away hard until the "
        "upper back rounds slightly and the blades wrap around the ribs.",
        ["Elbows locked the whole time", "Push the floor away at the top",
         "Small movement, big control"],
        ["Think of the shoulder blades sliding around the ribcage like "
         "hands around a barrel."],
        ["Bending the elbows (turns it into a push-up)",
         "Sagging hips"],
        "Stay in a comfortable range — no pinching in the front of the "
        "shoulder. Elevate the hands to reduce load if needed.",
        "Feet elevated, or slow 3 s phases.",
        "Hands on a wall (wall scap slide-push).",
        "Serratus wall slide.",
        yt_query="scapular push up serratus anterior exercise"),

    "band_pull_apart": _ex(
        "Band Pull-Apart", "face_pull",
        "Rear deltoids, rhomboids, mid-traps",
        "Balances all the pushing in daily life and strengthens the muscles "
        "that hold the shoulder blame back and down — key posture support "
        "for an unstable shoulder.",
        2, "15", "2-1-2-1", "30 s", "6",
        "Stand tall holding a light band at shoulder height, hands "
        "shoulder-width, palms down, arms straight.",
        "Pull the band apart until it touches the chest, squeezing the "
        "shoulder blades together and down. Return with control — the "
        "return is half the exercise.",
        ["Squeeze the blades together and down", "Ribs stay down",
         "Control the band back in"],
        ["Vary grip width week to week to hit fibres differently."],
        ["Shrugging the shoulders up", "Arching the low back",
         "Letting the band snap back"],
        "Stay in the pain-free arc. If the right shoulder front pinches, "
        "lower the hands to chest height.",
        "Heavier band or add a 2 s hold on the chest.",
        "Lighter band, smaller range.",
        "Prone T raise.",
        equipment="Resistance band",
        yt_query="band pull apart proper form rear delt"),

    "wall_slide": _ex(
        "Serratus Wall Slide", "wall_slide",
        "Serratus anterior, lower traps",
        "Teaches the shoulder blade to rotate upward correctly as the arm "
        "raises — the mechanism that keeps the humeral head centred in the "
        "socket overhead.",
        2, "10", "3 s up, 3 s down", "30 s", "5",
        "Stand facing a wall, forearms on it at shoulder height, elbows "
        "shoulder-width, a light band looped around the wrists (optional).",
        "Pressing the forearms firmly into the wall, slide them up the wall "
        "as high as comfortable while the shoulder blades rotate up and "
        "around. Slide back down with the same pressure.",
        ["Press into the wall the whole time", "Reach tall at the top",
         "Shoulders away from the ears"],
        ["At the top, take a small step toward the wall and reach an extra "
         "centimetre — that extra reach is the serratus."],
        ["Shrugging into the ears", "Losing wall pressure on the way down",
         "Arching the low back"],
        "Stop at the height where the shoulder stays comfortable — range "
        "will grow weekly. No apprehension positions.",
        "Add a mini-band around the wrists; slide on a foam roller.",
        "Smaller range of motion.",
        "Quadruped serratus reach (child's pose reach-through).",
        yt_query="serratus wall slide exercise shoulder"),

    # ================================================================
    # KNEE / ACL STRENGTH
    # ================================================================
    "box_squat": _ex(
        "Box Squat (to bench)", "squat",
        "Quadriceps, glutes",
        "The safest way to rebuild squat strength on a partial-ACL knee: "
        "the box controls depth, guarantees consistent form and removes "
        "the fear of the bottom position.",
        3, "10-12", "3-1-1-0", "75 s", "6",
        "Stand in front of a knee-height bench/box, feet shoulder-width, "
        "toes slightly out, arms reaching forward as a counterbalance.",
        "Push the hips back and bend the knees to sit back onto the box "
        "over 3 seconds. Touch it lightly (do not plop), keep tension, "
        "then drive up through the whole foot.",
        ["Sit back, not just down", "Knees track over the toes",
         "Touch the box like it's hot"],
        ["Film yourself from the front once a week — the knees should "
         "never dip inward, especially on the way up."],
        ["Collapsing onto the box", "Knees caving in on the drive up",
         "Heels lifting"],
        "Depth is limited by comfort, not ego. Pain 0-2/10 continue; 3-4 "
        "reduce depth; 5+ stop.",
        "Goblet box squat (hold a dumbbell at the chest).",
        "Higher box; hold a support.",
        "Wall sit or leg press (light).",
        equipment="Bench or box",
        yt_query="box squat to bench proper form"),

    "goblet_squat": _ex(
        "Goblet Squat", "squat",
        "Quadriceps, glutes, core",
        "Front-loaded squat that keeps the torso upright, spreads load "
        "evenly through the knee and builds the leg strength floor "
        "everything else stands on.",
        3, "8-10", "3-0-1-0", "90 s", "7",
        "Hold a dumbbell vertically against the chest, elbows tucked, feet "
        "shoulder-width, toes slightly out.",
        "Descend over 3 s, elbows tracking inside the knees, to the depth "
        "you control cleanly (thighs near parallel). Drive up through the "
        "whole foot, knees tracking over the toes.",
        ["Chest proud, elbows down", "Spread the floor with the feet",
         "Own the way down"],
        ["The 3-second lowering is deliberate — slow eccentrics build "
         "tendon and ligament resilience."],
        ["Knees caving inward", "Heels lifting", "Dive-bombing the descent"],
        "Progress depth before load, and load before speed. Any sharp or "
        "deep knee pain (>4/10) — stop and reassess.",
        "Heavier dumbbell; then tempo goblet squat (5 s down).",
        "Box squat or bodyweight squat to a target.",
        "Double-dumbbell front squat.",
        equipment="Dumbbell",
        yt_query="goblet squat proper form"),

    "tempo_goblet_squat": _ex(
        "Tempo Goblet Squat (5-s eccentric)", "squat",
        "Quadriceps, glutes, patellar & quad tendon",
        "Long eccentrics are the gold standard for tendon and ligament "
        "remodelling — maximum stimulus for the healing knee at moderate "
        "loads.",
        3, "6-8", "5-1-1-0", "90 s", "7-8",
        "Same as the goblet squat: dumbbell at the chest, feet "
        "shoulder-width.",
        "Take a full 5 seconds to lower — count out loud. Pause 1 s at "
        "your controlled depth, then stand up strong. Every centimetre of "
        "the descent is under your command.",
        ["Count 5 slow seconds down", "No free-fall centimetres",
         "Strong, fast stand-up"],
        ["Use ~70-80 % of your normal goblet squat weight — the tempo does "
         "the work."],
        ["Speeding up the last third of the descent",
         "Cutting depth as fatigue builds"],
        "Fatigue arrives fast with tempo work — end the set when the tempo "
        "breaks, not when the muscles fail.",
        "Add load, or 7-s eccentric.",
        "Standard-tempo goblet squat.",
        "Tempo box squat.",
        equipment="Dumbbell",
        yt_query="tempo squat slow eccentric form"),

    "spanish_squat": _ex(
        "Spanish Squat (band behind knees)", "squat",
        "Quadriceps (knee-dominant, low shear)",
        "The band pulls the shins back, letting you load the quads deeply "
        "with an upright torso and minimal strain on the ACL — a rehab "
        "classic for exactly your knee.",
        3, "10-12 (or 30-45 s iso hold)", "3-2-2-0", "75 s", "7",
        "Loop a heavy band around a rack/post and step both legs inside so "
        "it sits behind the knees. Walk back until taut, feet under hips.",
        "Squat down keeping the shins vertical and torso upright — lean "
        "back into the band. Pause 2 s at the bottom, drive up.",
        ["Lean back into the band", "Shins stay vertical",
         "Torso tall like sitting into a chair"],
        ["The isometric version (hold at 60-90° for 30-45 s) is superb on "
         "days the knee is grumpy — isometrics reduce tendon pain."],
        ["Letting the knees drift forward (slack band)",
         "Bending forward at the hips"],
        "Should feel like a deep quad burn with a comfortable knee joint. "
        "If the joint itself hurts, raise the depth.",
        "Add a goblet dumbbell, or slow to a 5 s descent.",
        "Wall sit.",
        "Wall sit or leg extension isometric.",
        equipment="Heavy loop band + anchor",
        yt_query="spanish squat band knee rehab"),

    "wall_sit": _ex(
        "Wall Sit", "wall_sit",
        "Quadriceps (isometric)",
        "Isometric quad loading at a fixed, safe knee angle. Isometrics "
        "build strength with minimal joint irritation and can reduce "
        "knee-tendon pain acutely.",
        3, "30-45 s", "isometric", "60 s", "6-7",
        "Back flat on a wall, feet out so the knees sit at ~90° (or "
        "shallower if 90° is uncomfortable), knees over ankles.",
        "Slide down until the thighs approach parallel and hold. Breathe "
        "steadily. Press the low back gently into the wall.",
        ["Whole back against the wall", "Weight through the heels",
         "Breathe — don't brace and hold"],
        ["Add 5 s per session — small wins compound."],
        ["Knees drifting past the toes", "Hands resting on the thighs",
         "Holding the breath"],
        "Choose the deepest angle that is pain ≤2/10. Depth is a dial — "
        "use it.",
        "Hold a dumbbell on the thighs, or single-leg wall sit (advanced).",
        "Higher (shallower) angle, shorter holds.",
        "Spanish squat isometric.",
        yt_query="wall sit proper form quad isometric"),

    "split_squat": _ex(
        "Split Squat", "split_squat",
        "Quads, glutes, single-leg control",
        "First step of the single-leg ladder. Football is played one leg "
        "at a time — so is ACL protection.",
        3, "8-10/side", "3-0-1-0", "60 s/side", "6-7",
        "Take a long stride stance; back heel up, front foot flat, hips "
        "square. Hold support if needed.",
        "Lower straight down (not forward) until the back knee hovers just "
        "above the floor, front shin near vertical. Drive up through the "
        "front foot's whole surface.",
        ["Elevator down, not escalator forward", "Front knee over mid-foot",
         "Hips stay square to the front"],
        ["80 % of your weight belongs on the front leg — the back leg is a "
         "kickstand."],
        ["Front knee diving inward", "Bouncing off the back knee",
         "Leaning the torso forward"],
        "The front knee must track over the 2nd-3rd toe. If it wobbles "
        "inward, regress to a shorter range and fix it there.",
        "Hold dumbbells; then rear-foot-elevated split squat.",
        "Hold a support (pole/doorframe); reduce depth.",
        "Static lunge with hand support.",
        yt_query="split squat proper form knees"),

    "rfe_split_squat": _ex(
        "Rear-Foot-Elevated Split Squat (Bulgarian)", "split_squat",
        "Quads, glutes",
        "The most bang-for-buck single-leg strength lift in sport — big "
        "quad and glute stimulus with lighter absolute loads, kind to the "
        "spine and progressive for the knee.",
        3, "8/side", "3-0-1-0", "75 s/side", "7-8",
        "Rear foot laces-down on a knee-height bench behind you; front "
        "foot far enough forward that the shin stays near vertical at the "
        "bottom. Dumbbells at the sides (or bodyweight first).",
        "Lower under control until the rear knee approaches the floor, "
        "torso upright with a slight forward lean. Drive up through the "
        "front foot.",
        ["Front foot far enough forward", "Down on a rail — no wobble",
         "Push the floor away"],
        ["Find your foot position with bodyweight before adding dumbbells; "
         "mark it."],
        ["Front stance too short (knee shoots forward)",
         "Hips rotating open", "Using the back leg to push"],
        "This is a Week-3+ exercise: earn it by owning the split squat "
        "first. Any knee pain >3/10 — return to split squats.",
        "Add dumbbell load weekly (2.5-5 %).",
        "Split squat.",
        "Reverse lunge with dumbbells.",
        equipment="Bench + dumbbells",
        yt_query="bulgarian split squat proper form"),

    "reverse_lunge": _ex(
        "Reverse Lunge", "split_squat",
        "Quads, glutes, balance",
        "Stepping backward keeps the front shin vertical and the knee "
        "happy while adding the balance demand of a moving base — a "
        "perfect bridge from split squats to the pitch.",
        3, "8/side", "2-0-1-0", "60 s/side", "6-7",
        "Stand tall, feet hip-width, hands on hips or holding dumbbells.",
        "Step back into a long lunge, lowering the back knee toward the "
        "floor while the front shin stays vertical. Push through the front "
        "foot to return to standing.",
        ["Step back long", "Front shin vertical",
         "Push the floor away to stand"],
        ["Tap the back foot down lightly — the front leg does the work."],
        ["Stepping back too short", "Front knee collapsing in",
         "Pushing off the back foot to stand"],
        "More knee-friendly than forward lunges (less shear on the front "
        "knee). Keep it that way by keeping the step long.",
        "Hold dumbbells; step from a low step (deficit).",
        "Split squat (no stepping).",
        "Split squat.",
        yt_query="reverse lunge proper form"),

    "lateral_lunge": _ex(
        "Lateral Lunge", "split_squat",
        "Glutes, quads, adductors",
        "Frontal-plane strength for defending, cutting and reaching "
        "tackles. Trains the adductors eccentrically — the muscle group "
        "footballers strain most.",
        3, "6-8/side", "2-0-1-0", "60 s/side", "6-7",
        "Stand tall, feet together, hands clasped at the chest.",
        "Step wide to the right, sitting the hips back over the right heel "
        "while the left leg stays straight. Chest up, right knee tracking "
        "over the toes. Push back to the start.",
        ["Sit back over the heel", "Trail leg straight — feel the groin "
         "stretch", "Chest stays proud"],
        ["Width beats depth: a wider step with less bend is more valuable "
         "than a deep narrow one."],
        ["Knee rolling inward over the bent leg", "Rounding the back",
         "Step too narrow"],
        "Load the range you control. The inner-thigh stretch on the "
        "straight leg should be gentle, never sharp.",
        "Hold a dumbbell at the chest (goblet lateral lunge).",
        "Cossack rock holding support, partial range.",
        "Cossack squat (assisted).",
        yt_query="lateral lunge proper form"),

    "step_up": _ex(
        "Dumbbell Step-Up", "step_up",
        "Quads, glutes",
        "Concentric-biased single-leg strength that mirrors climbing, "
        "accelerating and jumping — with the working knee always in your "
        "control.",
        3, "8/side", "2-1-1-0", "60 s/side", "6-7",
        "Stand facing a knee-height (or lower) box, whole foot of the "
        "working leg on it. Dumbbells at the sides (optional to start).",
        "Drive through the top foot to lift the body up — do NOT spring "
        "off the bottom foot. Touch the box lightly with the trailing "
        "foot, then lower down slowly on the working leg.",
        ["The top leg does 100 % of the work", "Slow lowering — 2 seconds",
         "Knee tracks over the toes"],
        ["Test: pause with the bottom foot hovering before each rep — no "
         "bounce possible."],
        ["Pushing off the floor leg", "Knee caving on the drive",
         "Dropping down instead of lowering"],
        "Box height is the dial: start below knee height and raise it only "
        "when reps are crisp and painless.",
        "Higher box or heavier dumbbells; lateral step-up.",
        "Lower box, no weight.",
        "Low lateral step-up.",
        equipment="Box/bench + dumbbells",
        yt_query="dumbbell step up proper form glute"),

    "lateral_step_up": _ex(
        "Lateral Step-Up", "step_up",
        "Quads, glute medius",
        "Sideways stepping loads the knee stabilisers in the frontal plane "
        "— closer to real cutting mechanics than any forward exercise.",
        3, "8/side", "2-1-1-0", "60 s/side", "7",
        "Stand side-on to a low box, near foot fully on it.",
        "Drive through the box-side leg to stand tall on the box, trail "
        "leg lifting to a knee-drive finish. Lower down slowly, hip "
        "controlling the descent.",
        ["Push straight down through the box foot", "Pelvis stays level",
         "Descent is the exercise"],
        ["Watch the pelvis: if it drops on the free-leg side, lower the "
         "box."],
        ["Pelvis dropping", "Bouncing off the floor leg",
         "Knee caving toward the box edge"],
        "Start with a low box (15-20 cm). This one exposes weaknesses — "
        "that's why it's here.",
        "Higher box, add dumbbell.",
        "Forward step-up or lower box.",
        "Step-up (forward).",
        equipment="Low box",
        yt_query="lateral step up knee exercise"),

    "tke": _ex(
        "Terminal Knee Extension (Band TKE)", "tke",
        "Quadriceps — VMO emphasis",
        "Strengthens the final degrees of knee extension where the quad "
        "protects the ACL. A cornerstone of conservative ACL rehab.",
        2, "15/side", "2-2-2-0", "45 s", "6",
        "Loop a band around a post and place it behind one knee; step back "
        "until taut. The banded knee starts slightly bent, heel down.",
        "Squeeze the quad to straighten the knee fully against the band, "
        "pulling the kneecap up. Hold 2 s at full extension, bend slowly "
        "back to the start.",
        ["Squeeze to a fully straight knee", "2-second lock-out hold",
         "Heel stays down"],
        ["Watch the kneecap glide upward on each squeeze — that's the VMO "
         "doing its job."],
        ["Hyperextending/snapping the knee back", "Rushing the reps",
         "Letting the band pull the knee forward passively"],
        "Straighten firmly but never *snap* into hyperextension.",
        "Heavier band; single-leg quarter squat against band.",
        "Quad sets (seated).",
        "Quad set with straight-leg raise.",
        equipment="Loop band + anchor",
        yt_query="terminal knee extension band TKE exercise"),

    # ================================================================
    # HAMSTRINGS / POSTERIOR CHAIN
    # ================================================================
    "romanian_deadlift": _ex(
        "Dumbbell Romanian Deadlift", "hinge",
        "Hamstrings, glutes, spinal erectors",
        "The hamstrings are the ACL's best friend — they pull the shin "
        "backward, directly opposing the strain the ACL resists. The RDL "
        "loads them long and heavy.",
        3, "8-10", "3-1-1-0", "90 s", "7",
        "Stand tall with dumbbells resting on the front of the thighs, "
        "feet hip-width, soft knees.",
        "Push the hips straight back, sliding the dumbbells down the legs "
        "with a flat back until you feel a strong hamstring stretch "
        "(usually just below the knees). Drive the hips forward to stand.",
        ["Hips back, not down", "Dumbbells shave the legs",
         "Flat back — proud chest"],
        ["Your knees should barely change angle — if they bend more as you "
         "descend, you're squatting it."],
        ["Rounding the low back", "Bending the knees to reach lower",
         "Bar drifting away from the legs"],
        "Range is set by hamstring flexibility with a flat back — never by "
        "the floor.",
        "Heavier dumbbells; then single-leg RDL.",
        "Hip hinge to a wall (bodyweight patterning).",
        "45° back extension or good morning (light).",
        equipment="Dumbbells",
        yt_query="dumbbell romanian deadlift proper form"),

    "single_leg_rdl": _ex(
        "Single-Leg Romanian Deadlift", "single_leg_hinge",
        "Hamstrings, glutes, ankle/hip proprioception",
        "Combines hamstring strength with the single-leg balance challenge "
        "— simultaneously the best ACL protector and the best "
        "proprioception drill in this program.",
        3, "6-8/side", "3-1-1-0", "60 s/side", "7",
        "Stand on one leg holding a dumbbell in the opposite hand, soft "
        "stance knee.",
        "Hinge at the hip, extending the free leg straight behind as the "
        "chest lowers — body moves as one plank from head to heel. Lower "
        "until the hamstring says stop, then drive the hips through to "
        "stand.",
        ["Hips square to the floor", "Free leg and torso move as one plank",
         "Push the floor away to stand"],
        ["Do it barefoot when possible — the foot is part of the exercise.",
         "Fix your eyes on a spot 2 m ahead on the floor."],
        ["Hips opening to the sky", "Rounding the back",
         "Stance knee locking straight"],
        "Wobble is welcome (it's the training stimulus); losing balance "
        "completely is not — keep a fingertip on support until crisp.",
        "Heavier dumbbell; eyes-closed final rep.",
        "Kickstand RDL (rear toes lightly down).",
        "Kickstand RDL.",
        equipment="Dumbbell",
        yt_query="single leg romanian deadlift proper form"),

    "slider_curl": _ex(
        "Slider Hamstring Curl", "hamstring_curl",
        "Hamstrings (knee-flexor function), glutes",
        "Trains the hamstrings in their knee-bending role — the exact "
        "function that dynamically shields the ACL during deceleration.",
        3, "8-10", "3-1-2-0", "75 s", "7",
        "Lie on your back on a smooth floor, heels on sliders (or a towel/"
        "socks), knees bent, hips lifted into a bridge.",
        "Keeping the hips high, slowly slide the heels away until the legs "
        "are nearly straight, then drag them back in with the hamstrings. "
        "Hips never touch down mid-set.",
        ["Hips stay bridged throughout", "Slide out slow — 3 seconds",
         "Drag the heels home"],
        ["No sliders? Socks on a wooden floor, or a towel on tiles, work "
         "perfectly."],
        ["Hips dropping as the legs extend", "Going further than you can "
         "pull back from", "Arching the low back"],
        "Hamstring cramp = too much range too soon. Shorten the slide and "
        "build out over weeks.",
        "Eccentric-only from further out; then single-leg sliders.",
        "Eccentric-only (slide out slow, drop hips, reset).",
        "Stability-ball leg curl or Nordic lowering.",
        equipment="Sliders / towel",
        yt_query="slider hamstring curl exercise"),

    "nordic_curl": _ex(
        "Nordic Hamstring Lowering", "nordic",
        "Hamstrings (eccentric)",
        "The single most-proven hamstring-injury-prevention exercise in "
        "football (≈50 % strain-risk reduction in studies). Eccentric "
        "strength here also supports the ACL.",
        3, "4-6", "as slow as possible down", "90 s", "8",
        "Kneel on a pad with the ankles anchored (partner, heavy sofa, or "
        "loaded bar). Body upright, hips extended, hands ready at the chest.",
        "Keeping a straight line from knees to head, lower the body toward "
        "the floor as slowly as the hamstrings allow. Catch yourself with "
        "the hands, use a small push-up to return, repeat.",
        ["Hips stay extended — no bending forward", "Fight every degree",
         "Catch softly with the hands"],
        ["Everyone loses the fight eventually — the fighting IS the "
         "exercise. Even 20-30° of control is productive at first."],
        ["Breaking at the hips (bum sticking back)",
         "Free-falling the last half", "Doing too many too soon"],
        "Expect real soreness the first two weeks — start with 2 sets of "
        "3. Never do these the day before football.",
        "Slower descents, deeper control point, band-assisted full reps.",
        "Band-assisted Nordic or slider curls.",
        "Slider hamstring curl.",
        equipment="Ankle anchor + pad",
        yt_query="nordic hamstring curl proper form"),

    "hip_thrust": _ex(
        "Dumbbell Hip Thrust", "hip_thrust",
        "Gluteus maximus",
        "The most direct heavy glute exercise there is. Strong glutes "
        "power sprinting and shield both the knee and the hamstrings.",
        3, "10-12", "2-1-1-1", "90 s", "7",
        "Upper back on a bench edge, feet flat and hip-width, dumbbell "
        "resting across the hip crease (pad it), chin tucked.",
        "Drive through the heels to lift the hips until the body is a "
        "flat table — knees at 90°, shins vertical. Squeeze the glutes "
        "hard 1 s at the top, lower with control.",
        ["Chin tucked, ribs down", "Full squeeze at the top",
         "Shins vertical at lockout"],
        ["Push the knees out slightly against an imaginary band at the top "
         "for extra glute medius."],
        ["Hyperextending the low back at the top",
         "Feet too far forward (hamstring takeover)",
         "Cutting the top squeeze"],
        "Zero knee shear — a great strength builder even on cautious days.",
        "Heavier dumbbell; single-leg hip thrust.",
        "Glute bridge from the floor.",
        "Glute bridge (weighted).",
        equipment="Bench + dumbbell",
        yt_query="dumbbell hip thrust proper form"),

    "single_leg_hip_thrust": _ex(
        "Single-Leg Hip Thrust", "hip_thrust",
        "Gluteus maximus, pelvic stability",
        "Unilateral glute power with a big anti-rotation core demand — "
        "builds the hip drive of your stronger sprint stride.",
        3, "8/side", "2-1-1-1", "60 s/side", "7-8",
        "Hip-thrust setup on a bench; lift one foot, knee held at 90°.",
        "Drive through the grounded heel to full hip extension, keeping "
        "the pelvis dead level. Squeeze, lower with control.",
        ["Pelvis level — no tipping", "Heel drives the floor away",
         "Top position identical to the two-leg version"],
        ["Hold the free knee with one hand at first to groove the level "
         "pelvis."],
        ["Pelvis rotating toward the free leg", "Short, bouncy reps"],
        "Earn this after 3 clean weeks of two-leg thrusts or bridges.",
        "Add a dumbbell on the working hip.",
        "B-stance (free foot heel lightly down).",
        "B-stance hip thrust.",
        equipment="Bench",
        yt_query="single leg hip thrust form"),

    "bridge_march": _ex(
        "Glute Bridge March", "bridge",
        "Glutes, hamstrings, anti-rotation core",
        "Adds an alternating-leg demand to the bridge — the pelvis must "
        "stay level as the legs trade places, just like running.",
        2, "10 steps/side", "slow 2 s per lift", "45 s", "6",
        "Hold a strong two-leg glute bridge, arms by the sides.",
        "Keeping the hips high and level, lift one knee toward the chest, "
        "place it back, then the other. The hips must not rock or drop.",
        ["Hips high and frozen", "Slow, quiet steps",
         "Ribs stay down"],
        ["Imagine balancing a cup of coffee on each hip bone."],
        ["Hips see-sawing", "Range shrinking as you fatigue"],
        "If the hamstrings cramp, walk the feet slightly further from the "
        "hips.",
        "Straighten the moving leg instead of just lifting the knee.",
        "Reduce hold height; fewer steps.",
        "Single-leg glute bridge.",
        yt_query="glute bridge march exercise"),

    # ================================================================
    # CALVES
    # ================================================================
    "calf_raise_double": _ex(
        "Standing Calf Raise (edge of step)", "calf_raise",
        "Gastrocnemius, soleus",
        "Calves absorb the first impact of every stride and jump landing. "
        "Full-range strength here protects the Achilles, ankle and knee "
        "up the chain.",
        3, "12-15", "2-1-2-1", "60 s", "6-7",
        "Balls of the feet on a step edge, heels hanging, fingertips on a "
        "wall for balance.",
        "Lower the heels below the step until a full calf stretch, pause "
        "1 s, then rise as high as possible onto the big toes. Pause 1 s "
        "at the top.",
        ["Full stretch at the bottom", "Rise over the big toe",
         "Pause at both ends"],
        ["The pause at the top removes the bounce — the bounce is why most "
         "people's calf raises don't work."],
        ["Bouncing", "Partial range", "Rolling to the outside of the foot"],
        "Slight Achilles stretch at the bottom is good; sharp pain is not.",
        "Add dumbbells; then single-leg calf raises.",
        "From the floor (no deficit).",
        "Seated calf raise.",
        equipment="Step",
        yt_query="standing calf raise full range proper form"),

    "calf_raise_single": _ex(
        "Single-Leg Calf Raise", "calf_raise",
        "Gastrocnemius, soleus, ankle stability",
        "The benchmark of calf strength: footballers should own 20+ crisp "
        "single-leg reps per side. Also a potent ankle-proprioception "
        "drill.",
        3, "10-12/side", "2-1-2-1", "45 s/side", "7",
        "One foot's ball on a step edge, other foot hooked behind the "
        "ankle, fingertips on the wall.",
        "Full stretch at the bottom, powerful rise to the very top over "
        "the big toe, 1 s squeeze, slow lowering.",
        ["Straight up-down — no leaning", "Over the big toe",
         "Every rep full range"],
        ["Track your max-rep number in Week 4's assessment — it's one of "
         "your progress KPIs."],
        ["Knee bending to cheat", "Ankle rolling outward", "Half reps"],
        "Compare sides. A >10 % rep difference between legs is a gap worth "
        "closing before adding jump work.",
        "Hold a dumbbell in the same-side hand.",
        "Two-up, one-down (rise on both, lower on one).",
        "Two-up-one-down calf raise.",
        equipment="Step",
        yt_query="single leg calf raise proper form"),

    "soleus_raise": _ex(
        "Bent-Knee (Soleus) Calf Raise", "calf_raise",
        "Soleus",
        "The soleus takes up to 8× bodyweight when running — it is the "
        "engine of repeated sprints. Bending the knee shifts the work to "
        "it specifically.",
        3, "15/side or 15 both", "2-1-2-1", "45 s", "6-7",
        "Same step setup, but hips and knees bent ~30-45° and held there "
        "(like a shallow ski squat).",
        "Keeping the knee bend constant, lower the heels to a full "
        "stretch, then rise to the top. The knee angle never changes.",
        ["Freeze the knee bend", "Full range at the ankle",
         "Slow and burning is right"],
        ["This burns differently — deeper in the calf. That's the soleus."],
        ["Straightening the knees on the way up", "Bouncing"],
        "Fatigues fast — quality over rep count.",
        "Single-leg bent-knee raises; add load.",
        "Both legs, floor level.",
        "Seated calf raise with weight on knees.",
        equipment="Step",
        yt_query="bent knee soleus calf raise"),

    "eccentric_calf": _ex(
        "Eccentric Heel Drop", "calf_raise",
        "Achilles tendon, calf complex",
        "Slow single-leg lowering is the proven protocol for Achilles "
        "tendon resilience — insurance for a sprinting footballer.",
        3, "10/side", "5 s lowering", "45 s", "6",
        "Ball of one foot on a step edge; rise up using BOTH legs.",
        "Shift all weight to one leg and lower that heel below the step "
        "over a full 5 seconds. Use both legs to rise again. All the work "
        "is in the lowering.",
        ["Up on two, down on one", "5 whole seconds down",
         "Full depth at the bottom"],
        ["Do these on football-free days; mild next-day calf stiffness is "
         "normal early on."],
        ["Lowering too fast", "Skipping the bottom range"],
        "Mild tendon awareness (≤3/10) during eccentrics is acceptable and "
        "normal; sharp pain is not.",
        "Add a dumbbell; slow to 7 s.",
        "Two-leg slow lowering.",
        "Standing calf raise with 3 s lowering.",
        equipment="Step",
        yt_query="eccentric heel drop achilles exercise"),

    # ================================================================
    # SHOULDER REHAB — ROTATOR CUFF & SCAPULA
    # ================================================================
    "iso_er_wall": _ex(
        "Isometric External Rotation vs Wall", "band_er",
        "Rotator cuff (infraspinatus, teres minor)",
        "Pain-free cuff activation with zero movement — the safest entry "
        "point for a post-dislocation shoulder and a great pre-load before "
        "band work.",
        2, "5 × 10 s/side", "10 s holds", "20 s", "5",
        "Stand side-on to a wall, right elbow bent 90° and pinned to the "
        "ribs, back of the wrist against the wall.",
        "Press the back of the wrist outward into the wall at ~50-70 % "
        "effort for 10 s. Nothing moves — the wall wins. Breathe.",
        ["Elbow glued to the ribs", "50-70 % effort — not maximal",
         "Shoulder blade set back and down"],
        ["Also do the inward version (palm side against the wall) for the "
         "subscapularis — the key stabiliser after anterior dislocation."],
        ["Shrugging while pressing", "Elbow drifting off the ribs",
         "Holding the breath"],
        "Must be 0-2/10 pain. Isometrics are your barometer: if these "
        "hurt, the shoulder needs an easier day.",
        "Increase effort toward 80 %; progress to band ER.",
        "Reduce push effort to 30-40 %.",
        "Band external rotation (very light band).",
        yt_query="isometric shoulder external rotation wall rehab"),

    "band_er": _ex(
        "Band External Rotation (elbow at side)", "band_er",
        "Infraspinatus, teres minor",
        "The bread-and-butter cuff strengthener. The external rotators "
        "hold the ball of the shoulder centred in its socket — exactly "
        "what a post-dislocation shoulder lacks.",
        3, "12-15", "2-1-3-0", "45 s", "6",
        "Band anchored at elbow height to your left; stand right-side "
        "away, right elbow bent 90° and pinned to the ribs (towel under "
        "the elbow), hand across the belly holding the band.",
        "Rotate the forearm outward like a gate opening, elbow staying "
        "welded to the ribs, to a comfortable range (~30-45°). Return "
        "over a slow 3 seconds.",
        ["Towel stays trapped under the elbow", "Gate swings open, hinge "
         "still", "Slow 3-count back in"],
        ["The 3-second return is the money — cuff tissue responds best to "
         "slow eccentrics."],
        ["Elbow drifting away from the body", "Wrist bending",
         "Using the trunk to swing"],
        "Work only in the pain-free arc; range grows over weeks. Never "
        "push into the position of apprehension.",
        "Heavier band; then 90/90 position ER.",
        "Lighter band or isometric holds.",
        "Side-lying dumbbell external rotation.",
        equipment="Resistance band",
        yt_query="band external rotation shoulder rotator cuff form"),

    "band_ir": _ex(
        "Band Internal Rotation", "band_er",
        "Subscapularis",
        "The subscapularis is the front wall of the shoulder — the single "
        "most important muscle for preventing another anterior "
        "dislocation.",
        3, "12-15", "2-1-3-0", "45 s", "6",
        "Band anchored at elbow height to your right; stand right-side "
        "toward it, right elbow bent 90° at the ribs, hand starting out "
        "wide holding the band.",
        "Rotate the forearm inward across the belly against the band, "
        "elbow pinned. Slow 3-second return.",
        ["Elbow pinned to the ribs", "Pull across the belly",
         "Resist the band on the way back"],
        ["This one guards the exact direction your shoulder dislocated — "
         "treat it with the same respect as the big lifts."],
        ["Leaning the trunk", "Shrugging", "Fast, snappy reps"],
        "Should feel like deep, front-of-shoulder work with zero joint "
        "pain.",
        "Heavier band.",
        "Isometric IR press against the wall.",
        "Side-lying dumbbell internal rotation.",
        equipment="Resistance band",
        yt_query="band internal rotation shoulder subscapularis"),

    "band_er_90": _ex(
        "90/90 Band External Rotation", "band_er_90",
        "Rotator cuff in the overhead/throwing position",
        "Trains cuff control in the abducted position where shoulders "
        "actually dislocate — the graduation exercise of cuff rehab. "
        "Introduce only once elbow-at-side ER is strong and painless.",
        3, "10-12", "2-1-3-0", "60 s", "6-7",
        "Face the band anchor (set high). Right upper arm lifted to "
        "shoulder height out to the side, elbow bent 90°, forearm parallel "
        "to the floor holding the band.",
        "Rotate the forearm up and back until vertical (like signalling a "
        "free kick), upper arm staying level. Lower over 3 s.",
        ["Upper arm stays parallel to the floor", "Rotate around a fixed "
         "elbow", "Stop short of any apprehension"],
        ["If this position feels 'loose' or nervy, you are not ready — "
         "bank two more weeks of elbow-at-side work first."],
        ["Arching the back", "Elbow dropping",
         "Pushing into end-range discomfort"],
        "THE red-flag exercise: any apprehension (the 'it might pop' "
        "feeling) = stop immediately and stay with lower positions.",
        "Heavier band; slower eccentrics.",
        "Return to elbow-at-side band ER.",
        "Prone 90/90 external rotation (chest on bench).",
        equipment="Resistance band",
        yt_query="90 90 external rotation band shoulder"),

    "face_pull": _ex(
        "Band Face Pull", "face_pull",
        "Rear delts, lower traps, external rotators",
        "One movement that trains scapular retraction AND external "
        "rotation together — the exact combination that keeps a shoulder "
        "seated during pressing and reaching.",
        3, "12-15", "2-1-2-0", "45 s", "6-7",
        "Band anchored just above head height. Grip with both hands, "
        "thumbs pointing back toward you, arms long, staggered stance.",
        "Pull the band toward the bridge of the nose, elbows high and "
        "wide, finishing with knuckles beside the ears in a double-"
        "biceps-like position. Control the return.",
        ["Pull to the nose, not the chest", "Thumbs finish by the ears",
         "Blades squeeze down and together"],
        ["End each rep with a tiny extra outward rotation — that final "
         "wrist-up wins the set."],
        ["Turning it into a row (elbows low)", "Shrugging",
         "Leaning back to fake strength"],
        "Golden exercise for your shoulder — hard to do wrong if the "
        "elbows stay high. Keep loads moderate and crisp.",
        "Heavier band; half-kneeling to remove momentum.",
        "Lighter band; seated.",
        "Band pull-apart + band ER combo.",
        equipment="Band + high anchor",
        yt_query="band face pull proper form"),

    "scaption_raise": _ex(
        "Scaption Raise (thumbs up)", "scaption",
        "Supraspinatus, deltoid, upper traps",
        "Raising in the scapular plane (~30° forward of sideways) with "
        "thumbs up gives the cuff maximum mechanical advantage and keeps "
        "the tendon un-pinched — the safest way to rebuild overhead "
        "strength.",
        3, "10-12", "2-1-3-0", "60 s", "6-7",
        "Stand tall, light dumbbells at the sides, palms rotated so thumbs "
        "point up. Feet hip-width, ribs down.",
        "Raise both arms up and slightly forward (a 'Y', ~30° in front of "
        "the body line) to shoulder height — or as high as comfortable. "
        "3-second lowering.",
        ["Thumbs lead the way up", "Y shape, not a T",
         "Shoulder blades rotate, don't shrug"],
        ["Start with 1-3 kg. This is a precision tool, not an ego lift."],
        ["Going too heavy", "Swinging", "Shrugging into the neck"],
        "Stop the raise at the height where the shoulder stays quiet — "
        "shoulder height is plenty; overhead comes later, if ever needed.",
        "Slightly heavier DBs; pause 2 s at the top.",
        "Empty hands; smaller arc.",
        "Prone Y raise on a bench.",
        equipment="Light dumbbells",
        yt_query="scaption raise thumbs up rotator cuff"),

    "prone_ytw": _ex(
        "Prone Y-T-W", "scaption",
        "Lower traps (Y), mid traps/rhomboids (T), external rotators (W)",
        "Hits every scapular stabiliser in one circuit, using gravity as "
        "the perfect gentle resistance. Elite shoulder housekeeping.",
        2, "8 of each letter", "2 s hold each rep", "60 s", "6",
        "Lie face down on a bench (or floor), forehead supported, arms "
        "hanging.",
        "Y: raise the arms overhead-and-out, thumbs up; hold 2 s. "
        "T: raise them straight out sideways, thumbs up; hold. "
        "W: elbows bent, squeeze the blades and rotate the hands up; hold. "
        "8 reps of each letter = 1 set.",
        ["Thumbs up on every letter", "Lift from the shoulder blades",
         "Neck long and relaxed"],
        ["No weight needed for weeks — gravity and 2-s holds are plenty."],
        ["Lifting the chest off the bench", "Rushing between letters",
         "Cranking the neck up"],
        "All letters stay below pain threshold; shrink the Y arc if the "
        "overhead angle nags.",
        "Add 0.5-1 kg plates; 3 s holds.",
        "Do only T and W; add Y later.",
        "Wall angels (standing).",
        equipment="Bench (optional)",
        yt_query="prone Y T W exercise shoulder blade"),

    # ================================================================
    # UPPER-BODY STRENGTH (shoulder-safe)
    # ================================================================
    "db_row": _ex(
        "Single-Arm Dumbbell Row", "row",
        "Lats, rhomboids, biceps, core",
        "Big, safe pulling strength. Rowing strengthens everything that "
        "stabilises the shoulder from behind, in a position where a "
        "post-dislocation joint is fully secure.",
        3, "10/side", "2-1-2-1", "60 s/side", "7",
        "Left hand and left knee on a bench, back flat like a table, "
        "dumbbell hanging from the right hand, shoulder blade reaching "
        "long.",
        "Start the pull by drawing the shoulder blade back, then pull the "
        "dumbbell to the hip crease (not the armpit). Squeeze 1 s, lower "
        "long and slow.",
        ["Blade first, then arm", "Pull to the hip pocket",
         "Long stretch at the bottom"],
        ["Pulling to the hip keeps the elbow path shoulder-friendly; "
         "pulling to the armpit flares it into the vulnerable zone."],
        ["Rotating the torso to heave", "Shrugging the weight up",
         "Cutting the bottom stretch"],
        "Rows are your shoulder's best friend — but keep the elbow path "
        "close to the body and stop shy of end-range extension behind "
        "the back.",
        "Heavier dumbbell; pause rows.",
        "Chest-supported band row (seated).",
        "Seated band row.",
        equipment="Dumbbell + bench",
        yt_query="single arm dumbbell row proper form"),

    "band_row": _ex(
        "Seated Band Row", "row",
        "Mid-back, lats, rear delts",
        "Constant band tension with zero lower-back load — perfect "
        "higher-rep pulling volume that feeds the scapular stabilisers.",
        3, "12-15", "2-1-2-1", "45 s", "6-7",
        "Sit tall on the floor, legs long with soft knees, band looped "
        "around the mid-feet, handles/ends in both hands, arms long.",
        "Row the hands to the lower ribs, elbows brushing the sides, "
        "chest proud. Squeeze the blades 1 s, return slowly until the "
        "arms are long and the blades reach forward.",
        ["Elbows shave the ribs", "Proud chest all set",
         "Let the blades reach at the front"],
        ["Exhale on the pull to keep the ribcage stacked."],
        ["Leaning back to cheat tension", "Shrugging",
         "Half-range short pulls"],
        "Fully shoulder-safe pulling — great volume filler on upper days.",
        "Double the band or shorten it; add a pause.",
        "Lighter band.",
        "Single-arm dumbbell row.",
        equipment="Resistance band",
        yt_query="seated resistance band row form"),

    "floor_press": _ex(
        "Dumbbell Floor Press", "press",
        "Chest, triceps, anterior shoulder (protected range)",
        "Pressing with the elbows stopped by the floor caps the range "
        "exactly where a labral-injury shoulder is vulnerable — press "
        "strength with a built-in safety net.",
        3, "8-10", "2-1-1-0", "90 s", "7",
        "Lie on the floor, knees bent, dumbbells pressed over the chest, "
        "palms facing slightly inward (neutral-ish), shoulder blades "
        "tucked back and down.",
        "Lower the dumbbells until the upper arms rest gently on the "
        "floor — elbows at ~45° from the ribs, never flared to 90°. Press "
        "back up to lockout.",
        ["Elbows 45° from the body", "Blades pinned back and down",
         "Touch the floor softly, no bounce"],
        ["The neutral (palms-in) grip is measurably kinder to an anterior-"
         "unstable shoulder — use it for at least the first month."],
        ["Flaring elbows to 90°", "Bouncing off the floor",
         "Losing the blade set at lockout"],
        "The floor prevents the deep, cocked-back position where your "
        "labrum is at risk. Do NOT swap this for a full bench press this "
        "month.",
        "Heavier DBs; slow 3 s lowering.",
        "Single-DB press or incline push-up.",
        "Incline push-up.",
        equipment="Dumbbells",
        yt_query="dumbbell floor press proper form"),

    "incline_pushup": _ex(
        "Incline Push-Up", "pushup",
        "Chest, triceps, serratus, core",
        "Closed-chain pressing lets the shoulder blade move freely — the "
        "friendliest pressing pattern for a healing shoulder, plus free "
        "core work.",
        3, "10-12", "2-1-1-0", "60 s", "6-7",
        "Hands on a bench/box/wall-bar at hip-to-chest height, "
        "shoulder-width. Body one straight line, glutes and core braced.",
        "Lower the chest to the edge with the elbows at ~45°, then push "
        "the surface away hard — an extra push at the top rounds the "
        "upper back slightly (serratus bonus).",
        ["Body is a plank", "Elbows 45°, not chicken wings",
         "Push the surface away plus one more inch"],
        ["Lower the incline over the weeks — each step down is a measurable "
         "progression."],
        ["Hips sagging", "Head pecking forward", "Flared elbows"],
        "Choose the incline height where all reps are crisp and pain-free; "
        "the ground version can wait until the shoulder earns it.",
        "Lower surface → floor push-up → feet-elevated.",
        "Higher surface (wall push-up).",
        "Dumbbell floor press.",
        equipment="Bench/box",
        yt_query="incline push up proper form"),

    "pushup": _ex(
        "Push-Up (full)", "pushup",
        "Chest, triceps, serratus, core",
        "The graduation press: full bodyweight, full scapular freedom. "
        "Only appears once incline push-ups are strong and silent.",
        3, "8-12", "2-1-1-0", "75 s", "7",
        "High plank, hands slightly wider than shoulders, fingers spread, "
        "body rigid from ears to heels.",
        "Lower as one unit until the chest is a fist-height off the "
        "floor, elbows ~45°. Press the floor away to a tall top position "
        "with the blades wrapped forward.",
        ["One rigid line", "Chest leads, hips follow",
         "Full push at the top"],
        ["Squeeze the glutes before the first rep and keep them on."],
        ["Hips sagging or piking", "Half reps", "Elbows flaring"],
        "If the right shoulder pinches at the bottom, stop 5-10 cm higher "
        "or return to the incline for another week.",
        "Feet elevated, or add a slow 3 s descent.",
        "Incline push-up.",
        "DB floor press.",
        yt_query="push up perfect form"),

    "landmine_press": _ex(
        "Half-Kneeling Angled Press (landmine-style)", "press",
        "Shoulders, upper chest, serratus, core",
        "Pressing on a ~45° diagonal is the shoulder-safest path to "
        "overhead strength — the angle keeps the humeral head centred "
        "while the half-kneeling base trains the hips and core.",
        3, "8/side", "2-1-1-0", "60 s/side", "7",
        "Half-kneeling (right knee down when pressing right). Hold one "
        "dumbbell at the right shoulder, ribs stacked over hips. (With a "
        "barbell in a corner this is the classic landmine press.)",
        "Press the dumbbell up-and-forward at ~45° until the elbow is "
        "long, letting the shoulder blade glide naturally around the "
        "ribs. Lower to the shoulder with control.",
        ["Press on the diagonal, not straight up", "Ribs down, glute of "
         "the down-knee squeezed", "Blade glides — don't pin it"],
        ["This replaces strict overhead pressing this month — same "
         "strength, fraction of the joint risk."],
        ["Arching the low back", "Pressing straight vertical",
         "Leaning away from the weight"],
        "The moment the press path drifts vertical, the labrum works "
        "harder — keep the diagonal honest.",
        "Heavier DB; standing version.",
        "Both hands on one dumbbell, taller angle.",
        "Incline push-up (steep).",
        equipment="Dumbbell (or barbell landmine)",
        yt_query="half kneeling landmine press form"),

    "banded_pulldown": _ex(
        "Tall-Kneeling Band Pulldown", "row",
        "Lats, lower traps",
        "Vertical pulling volume without hanging load on the shoulder "
        "capsule — builds the lats that decelerate the arm in throws and "
        "falls.",
        3, "12/side or both", "2-1-3-0", "45 s", "6-7",
        "Anchor a band high (door or pull-up bar). Tall-kneeling below "
        "it, arms long overhead-forward holding the band, ribs down.",
        "Pull the elbows down and slightly back until the hands reach "
        "shoulder height, feeling the armpit muscles work. 3-second "
        "return, letting the blades rise naturally.",
        ["Elbows drive to the back pockets", "Ribs stay down",
         "Slow ride back up"],
        ["Single-arm version doubles as anti-rotation core work."],
        ["Leaning back into a row", "Shrugging at the top",
         "Snapping the return"],
        "Keep the start position short of full overhead stretch if the "
        "shoulder front nags — range grows weekly.",
        "Heavier band; add pauses.",
        "Half-range pulls from eye height.",
        "Single-arm DB row.",
        equipment="Band + high anchor",
        yt_query="tall kneeling band lat pulldown"),

    "farmer_carry": _ex(
        "Farmer Carry", "carry",
        "Grip, traps, core, hips",
        "Loaded walking teaches the shoulder to sit packed under load and "
        "the core to resist collapse each stride — whole-body strength "
        "with almost zero technique risk.",
        3, "30-40 m (or 30-40 s)", "steady walk", "60 s", "7",
        "Dumbbell in each hand, stand tall — ears over shoulders over "
        "hips, blades set gently back and down.",
        "Walk with controlled, quiet steps, dumbbells still (no swinging), "
        "breathing steadily. Turn slowly at the ends.",
        ["Walk tall — someone's watching", "Knuckles quiet, no swing",
         "Breathe every few steps"],
        ["Grip is the timer: end the set while posture is still perfect."],
        ["Leaning to one side", "Rushing with short choppy steps",
         "Shrugging the load"],
        "Packed-shoulder carrying is actually therapeutic for your "
        "shoulder — heavy is fine as long as posture is perfect.",
        "Heavier DBs; then suitcase (one-sided) carry.",
        "Lighter DBs, shorter distance.",
        "Suitcase carry (single side).",
        equipment="Dumbbells",
        yt_query="farmer carry proper form"),

    "suitcase_carry": _ex(
        "Suitcase Carry (single-arm)", "carry",
        "Obliques, QL, grip, lateral hip",
        "One-sided load makes the opposite core wall and the stance hip "
        "fight every step — walking anti-lean training that transfers "
        "straight to shielding the ball.",
        3, "30 m/side", "steady walk", "45 s/side", "7",
        "One dumbbell in the right hand, stand perfectly level — a "
        "broomstick across the shoulders would sit horizontal.",
        "Walk tall and level. The free hand stays relaxed. Swap sides "
        "each length.",
        ["Shoulders level — fight the tilt", "Slow, quiet feet",
         "Ribs stacked over the pelvis"],
        ["Film from behind once — visible lean means drop 20 % of the "
         "load."],
        ["Leaning away from (or into) the weight", "Hip swaying out",
         "Holding the breath"],
        "Level shoulders are non-negotiable; the lean is the mistake the "
        "exercise exists to fix.",
        "Heavier DB; add a slow march (knee lift) every 5 steps.",
        "Lighter DB.",
        "Farmer carry.",
        equipment="Dumbbell",
        yt_query="suitcase carry core exercise form"),

    # ================================================================
    # CORE
    # ================================================================
    "plank": _ex(
        "Front Plank", "plank",
        "Anterior core, glutes, shoulders",
        "The baseline of trunk stiffness — the rigid link that transfers "
        "leg power into sprinting and shooting without leaking energy.",
        3, "30-45 s", "isometric", "45 s", "6-7",
        "Forearms down, elbows under shoulders, feet together or "
        "hip-width. One straight line ear-shoulder-hip-ankle.",
        "Squeeze the glutes, tuck the pelvis slightly, push the floor away "
        "through the forearms and breathe in a steady rhythm. Stop when "
        "the line breaks, not the clock.",
        ["Glutes on, pelvis tucked", "Push the floor away",
         "Breathe — never hold"],
        ["A hard 30 s beats a saggy 90 s. When 45 s is easy, make it "
         "harder (see progression), don't make it longer."],
        ["Hips sagging", "Bum in the air", "Breath-holding"],
        "Supporting on the forearms is comfortable for the right shoulder; "
        "keep pushing the floor away to keep the blade active.",
        "Weight-shift taps, or feet on a bench.",
        "Knees down; or incline plank on a bench.",
        "Dead bug (moving alternative).",
        yt_query="plank proper form"),

    "plank_tap": _ex(
        "Plank Shoulder Tap", "plank",
        "Anti-rotation core, shoulder stability",
        "Removing one hand forces the trunk to refuse rotation — and "
        "gives the right shoulder graded single-arm weight-bearing, a key "
        "rehab milestone.",
        3, "8 taps/side", "1 s per tap, controlled", "45 s", "7",
        "High plank, feet wider than usual (stability base), hands under "
        "shoulders.",
        "Shift weight subtly and lift one hand to tap the opposite "
        "shoulder. Hips stay dead level — imagine a full glass on the low "
        "back. Alternate.",
        ["Hips frozen — no see-saw", "Feet wide, squeeze the floor",
         "Slow taps beat fast taps"],
        ["Narrow the feet over the weeks to progress difficulty without "
         "adding reps."],
        ["Hips rocking side to side", "Rushing", "Sagging between taps"],
        "The single-arm support moment loads the right shoulder — if it "
        "aches, drop to an incline (hands on bench) version first.",
        "Feet narrower; slow 2 s taps.",
        "Incline shoulder taps (hands on bench).",
        "Bird dog.",
        yt_query="plank shoulder taps proper form"),

    "side_plank": _ex(
        "Side Plank", "side_plank",
        "Obliques, QL, glute medius",
        "Lateral trunk strength correlates with fewer knee AND groin "
        "injuries in footballers. The side wall of your core is built "
        "here.",
        3, "20-40 s/side", "isometric", "30 s/side", "6-7",
        "Lie on one side, elbow under the shoulder, forearm across, feet "
        "stacked (or staggered), body straight.",
        "Lift the hips until the body is one rigid line. Top hand on the "
        "hip or reaching to the ceiling. Push the floor away with the "
        "forearm; breathe.",
        ["Hips high — no banana", "Push the floor away",
         "Neck long, gaze forward"],
        ["On the right-elbow side this doubles as shoulder-stability work "
         "— push through the forearm actively."],
        ["Hips sagging toward the floor", "Rolling the chest forward",
         "Neck cranked upward"],
        "Right-side support loads the healing shoulder in a safe, closed "
        "chain. If it aches, do the knees-bent version on that side.",
        "Top-leg lift, or feet on a bench.",
        "Knees-bent side plank.",
        "Suitcase carry.",
        yt_query="side plank proper form"),

    "side_plank_leglift": _ex(
        "Side Plank + Top-Leg Lift", "side_plank",
        "Obliques + gluteus medius together",
        "Marries the side plank with hip abduction — the ultimate 2-for-1 "
        "for lateral chain and knee-guard strength.",
        3, "8 lifts/side", "2 s per lift", "45 s/side", "7-8",
        "Strong side plank position, feet staggered or stacked.",
        "Holding the plank rock-solid, lift the top leg to ~30-40°, pause "
        "1 s, lower. The body stays one plane — no rolling.",
        ["Plank first, lift second", "Leg slightly behind the body line",
         "Pause at the top"],
        ["If the plank shakes apart, do fewer lifts — plank quality rules."],
        ["Rolling backward as the leg lifts", "Hips dropping",
         "Swinging the leg"],
        "Advanced — earn it with 40 s clean side planks first.",
        "Add an ankle weight or band.",
        "Side plank only; or clamshell + side plank separately.",
        "Copenhagen plank (short lever).",
        yt_query="side plank leg raise exercise"),

    "pallof_press": _ex(
        "Pallof Press", "pallof",
        "Deep core (anti-rotation), obliques",
        "The band tries to twist you; you refuse. Anti-rotation is the "
        "core skill of kicking, tackling and shielding — trained here "
        "with zero spinal loading.",
        3, "10/side", "2 s hold pressed out", "45 s", "6-7",
        "Band anchored at chest height to your side. Stand side-on in an "
        "athletic stance, band held with both hands at the sternum, "
        "enough distance for firm tension.",
        "Press the hands straight out from the chest and hold 2 s while "
        "the band tries to rotate you toward the anchor. Refuse. Return "
        "to the chest. All reps one side, then face the other way.",
        ["Press out slow, hold, resist", "Hips and shoulders square "
         "forward", "Breathe out as you press"],
        ["Step further from the anchor to progress — distance is the "
         "dial."],
        ["Rotating toward the anchor", "Leaning away", "Bending the arms "
         "back early"],
        "Completely spine- and knee-safe. A staple you can keep for life.",
        "Half-kneeling or split-stance version; further from anchor.",
        "Closer to the anchor; lighter band.",
        "Suitcase carry.",
        equipment="Band + anchor",
        yt_query="pallof press proper form"),

    "copenhagen": _ex(
        "Copenhagen Adductor Plank (short lever)", "copenhagen",
        "Adductors, obliques",
        "Proven to cut groin-injury risk in footballers by ~40 %. The "
        "adductors also steer the knee — this is quiet ACL insurance too.",
        2, "15-25 s/side", "isometric", "45 s/side", "7",
        "Side-plank position with the top KNEE (short lever — not the "
        "foot) resting on a bench, bottom leg bent behind, elbow under "
        "shoulder.",
        "Lift the hips by squeezing the top inner thigh down into the "
        "bench until the body is one line from knee to shoulder. Hold. "
        "Breathe.",
        ["Squeeze the bench with the inner thigh", "Hips in line",
         "Short holds, perfect quality"],
        ["Groin DOMS after the first exposures is famous — start with one "
         "10-15 s hold per side and let it grow."],
        ["Starting with the long-lever (foot on bench) version",
         "Hips sagging", "Holding the breath"],
        "Never do these the day before football in the first two weeks — "
        "adductor DOMS ruins passing.",
        "Longer holds → long-lever (foot on bench) → lifts.",
        "Standing ball/pillow squeeze between the knees.",
        "Ball squeeze isometric (lying).",
        equipment="Bench",
        yt_query="copenhagen plank short lever adductor"),

    # ================================================================
    # BALANCE & PROPRIOCEPTION
    # ================================================================
    "sl_balance": _ex(
        "Single-Leg Balance", "balance",
        "Ankle-knee-hip proprioceptors, foot intrinsics",
        "An ACL injury damages the knee's position sensors, not just the "
        "ligament. Balance training literally re-installs them — it is as "
        "important as any lift in this plan.",
        3, "30 s/side", "isometric", "20 s", "5",
        "Barefoot if possible. Stand on one leg, soft knee, other foot "
        "hovering by the ankle, arms relaxed.",
        "Hold. Grip the floor with the toes, keep the pelvis level and "
        "the knee tracking over the mid-foot. When 30 s is calm, close "
        "your eyes.",
        ["Grip the floor with the toes", "Soft knee, never locked",
         "Quiet hips"],
        ["Do these while brushing your teeth on recovery days — frequency "
         "beats duration for proprioception."],
        ["Locking the knee straight", "Hip jutting sideways",
         "Staring at the feet"],
        "Wobbling is the training. Stand near a wall so a real loss of "
        "balance costs nothing.",
        "Eyes closed → head turns → unstable surface (folded towel).",
        "Fingertip on the wall.",
        "Tandem (heel-to-toe) stance holds.",
        yt_query="single leg balance training proprioception"),

    "sl_balance_perturb": _ex(
        "Single-Leg Balance + Ball Toss / Head Turn", "balance",
        "Reactive knee stabilisers",
        "Adds chaos to balance — catching, turning, reacting — so the "
        "knee learns to stabilise while the brain is busy, exactly like "
        "on the pitch.",
        3, "30 s/side", "reactive", "20 s", "6",
        "Single-leg stance, soft knee, ball in hands (or none for head "
        "turns).",
        "Toss a ball off a wall and catch it, or pass hand-to-hand in "
        "arcs, or turn the head side-to-side / up-down — all while the "
        "stance leg stays quiet and the knee tracks straight.",
        ["Knee stays over the mid-foot no matter what", "Soft landings of "
         "attention — eyes can leave the floor", "Breathe"],
        ["A tennis or juggling ball is perfect; a football works too."],
        ["Knee wobbling inward during catches", "Rigid, locked knee",
         "Toe-gripping panic"],
        "Progression of plain balance — earn 30 s eyes-open calm first.",
        "Eyes-closed holds between catches; stand on a cushion.",
        "Plain single-leg balance.",
        "Single-leg balance, eyes closed.",
        equipment="Any ball",
        yt_query="single leg balance ball toss knee rehab"),

    "sl_reach": _ex(
        "Single-Leg Star Reach (Y-Balance)", "balance",
        "Hip-knee-ankle control through range",
        "Reaching the free leg in three directions forces the stance knee "
        "to stabilise through bend and lean — the standard test AND "
        "trainer of dynamic knee control.",
        2, "5 reaches × 3 directions/side", "slow", "30 s/side", "6-7",
        "Stand on one leg in the centre of an imaginary Y (one line "
        "forward, two lines back-diagonal).",
        "Bend the stance knee and reach the free foot as far as control "
        "allows along one line — tap the floor featherlight, return to "
        "tall standing. Rotate through the three directions.",
        ["Featherlight taps — no weight on the reaching foot",
         "Stance knee over the mid-foot", "Return to tall between reaches"],
        ["Measure your best forward reach in Week 4 (cm) — a "
         "side-to-side difference >4 cm is your homework."],
        ["Dumping weight onto the reaching foot", "Stance knee caving",
         "Rushed, bouncy reaches"],
        "Reach distance is earned, not forced — control decides range.",
        "Hold a light dumbbell at the chest; longer reaches.",
        "Shorter reaches; fingertip support.",
        "Single-leg RDL reach.",
        yt_query="Y balance test single leg reach exercise"),

    "hop_stick": _ex(
        "Hop & Stick (forward)", "hop",
        "Landing mechanics — quads, glutes, calves",
        "Teaches the knee to absorb landings with perfect alignment — the "
        "skill that decides whether a bad landing becomes a full ACL "
        "tear. Introduced only in Week 3, small and controlled.",
        3, "5/side", "stick 2 s per landing", "60 s", "7",
        "Stand on one leg, athletic quarter-squat.",
        "Hop forward a modest distance (start ~30-50 cm) and land on the "
        "SAME leg, freezing the landing for a full 2 s: knee bent and "
        "tracking over the toes, chest up, silent foot. Reset, repeat.",
        ["Land like a ninja — silent", "Freeze 2 full seconds",
         "Knee over the toes, every single landing"],
        ["Video the landings from the front weekly — the knee must never "
         "dive inward. Distance grows ONLY when landings are perfect."],
        ["Chasing distance over quality", "Loud, stiff landings",
         "Knee valgus on landing"],
        "STRICT rules: pain must be 0-2/10, and this never runs the day "
        "before football. Any knee pain or swelling after — remove hops "
        "for a week and tell your physio.",
        "Slightly further; then lateral hop & stick.",
        "Two-leg hop to single-leg landing; or just landing drops.",
        "Drop-and-stick from a 15 cm step.",
        yt_query="single leg hop and stick landing mechanics"),

    "lateral_hop_stick": _ex(
        "Lateral Hop & Stick", "hop",
        "Frontal-plane landing control",
        "Sideways hops mirror cutting — the No. 1 ACL mechanism in "
        "football. Mastering small lateral landings is direct game "
        "insurance.",
        3, "4/direction/side", "stick 2 s", "60 s", "7-8",
        "Single-leg athletic stance beside an imaginary line.",
        "Hop sideways over the line (small — 20-30 cm to start) and stick "
        "the landing on the same leg for 2 s, knee tracking, hips level. "
        "Hop back. Quality only.",
        ["Small hops, perfect freezes", "Hips stay level",
         "Knee refuses to cave"],
        ["This is the most 'football' exercise in the plan — treat every "
         "landing like a match action."],
        ["Too big too soon", "Landing with a straight knee",
         "Upper body flailing"],
        "Same strict rules as forward hops: pain ≤2/10, never before "
        "match day, quality gates every progression.",
        "Slightly wider; add a 90° hop-turn later (Month 2).",
        "Forward hop & stick, or side step-and-hold.",
        "Skater step-and-stick (no flight phase).",
        yt_query="lateral hop and hold single leg stability"),

    # ================================================================
    # CONDITIONING (knee-friendly)
    # ================================================================
    "bike_intervals": _ex(
        "Bike Intervals 30/30", "bike",
        "Cardiovascular system, legs",
        "High-calorie, zero-impact conditioning. 30 s hard / 30 s easy "
        "mimics football's stop-start rhythm and drives the afterburn "
        "(EPOC) that keeps burning calories post-session.",
        1, "8-12 rounds (8-12 min)", "30 s hard / 30 s easy", "—", "8 work / 3 recovery",
        "Bike set up as in the warm-up. 2 min easy spin first.",
        "30 s strong effort (RPE 8 — breathing hard, legs burning) then "
        "30 s easy spin. Repeat. Finish with 2 min easy.",
        ["Hard means hard — honest 8/10", "Easy means easy — actually "
         "recover", "Cadence high, resistance moderate"],
        ["Add one round per week: 8 → 10 → 12."],
        ["Medium-effort everything (grey zone)", "Grinding huge gears "
         "with a sore knee"],
        "Spinning fast beats grinding heavy — high resistance at low rpm "
        "loads the patellofemoral joint.",
        "More rounds, or 40/20 timing.",
        "Fewer rounds; 20/40 timing.",
        "Rower intervals, incline-walk intervals, or swimming.",
        equipment="Stationary bike",
        yt_query="bike interval training 30 30 workout"),

    "bike_tempo": _ex(
        "Bike Tempo Ride", "bike",
        "Aerobic base, fat oxidation",
        "Continuous 'comfortably hard' riding builds the aerobic engine "
        "that lets you repeat sprints in the 90th minute — and it is a "
        "direct fat-burning session.",
        1, "15-20 min", "steady RPE 6", "—", "6",
        "Bike, saddle set correctly, easy 2-min spin to start.",
        "Settle into a pace you could hold while speaking in short "
        "sentences (not full conversation, not gasping). Hold it. Easy "
        "2 min to finish.",
        ["Short-sentences pace", "Smooth circles", "Consistent — no surges"],
        ["Heart-rate guide if you track it: roughly 130-150 bpm at your "
         "age."],
        ["Starting too fast and fading", "Turning it into intervals"],
        "Fully knee-safe steady work — the volume dial for fat loss.",
        "Add 5 min, or small resistance bumps each 5 min.",
        "Shorten to 10-12 min.",
        "Brisk incline walk 20-25 min, or swim.",
        equipment="Stationary bike",
        yt_query="tempo ride stationary bike zone 2 3"),

    "incline_walk": _ex(
        "Brisk Incline Walk", "jog",
        "Aerobic system, glutes, calves",
        "Walking uphill burns serious calories with a fraction of "
        "running's impact — ideal extra conditioning that never steals "
        "recovery from the knee.",
        1, "20-30 min", "brisk steady", "—", "5-6",
        "Treadmill at 6-10 % incline (or a real hill), comfortable shoes.",
        "Walk briskly without holding the rails, arms swinging naturally, "
        "tall posture. You should feel warm and lightly out of breath.",
        ["Don't hold the rails", "Tall chest, eyes ahead",
         "Push through the whole foot"],
        ["A loaded backpack (5-8 kg) turns this into 'rucking' — a big "
         "calorie upgrade with the same joint cost."],
        ["Hanging on the rails (deletes half the work)",
         "Overstriding downhill afterwards"],
        "Zero-risk conditioning — use freely on recovery days too (lighter "
        "pace).",
        "More incline, light backpack, or +10 min.",
        "Flat brisk walk.",
        "Bike tempo ride.",
        equipment="Treadmill or hill",
        yt_query="incline treadmill walking workout benefits"),

    "shadow_footwork": _ex(
        "Low-Impact Football Footwork", "jog",
        "Agility patterns, calves, coordination",
        "Rehearses match footwork — side shuffles, backpedal, carioca — "
        "at sub-maximal intensity, re-patterning football movement in a "
        "controlled dose.",
        1, "6-8 min", "quality over speed", "as needed", "6",
        "A 5-10 m corridor of clear floor. Light shoes.",
        "Cycle 30-40 s each: side shuffles (stay low, no crossing feet), "
        "backpedal, carioca (cross-step), diagonal forward zig-zag. Walk "
        "back easy between drills. 2 rounds.",
        ["Stay in the athletic half-squat", "Quiet, quick feet",
         "Knees track over toes on every cut"],
        ["This is movement rehearsal, not conditioning — crisp and fresh "
         "beats fast and sloppy."],
        ["Standing tall (defeats the drill)", "Full-speed cuts before the "
         "knee is ready", "Sloppy crossover steps"],
        "Sub-maximal by design this month: 70 % speed maximum. Sharp "
        "cutting stays on the pitch warm-up, not here.",
        "Add a ball; slightly quicker tempo in Week 4.",
        "Walk-through patterns.",
        "Ladder drills at half speed.",
        yt_query="football agility footwork drills low intensity"),

    # ================================================================
    # COOL-DOWN & STRETCHING
    # ================================================================
    "stretch_quad": _ex(
        "Standing Quad Stretch", "stretch_quad",
        "Quadriceps, hip flexors",
        "Restores quad length after knee-dominant work; tight quads "
        "increase patellofemoral pressure.",
        1, "30-45 s/side", "static", "—", "2",
        "Stand tall by a wall, fingertips on it for balance.",
        "Bend one knee and hold the ankle behind you, knees together, "
        "pelvis tucked slightly. Gentle pull until a comfortable front-"
        "thigh stretch. Breathe slowly.",
        ["Knees together", "Tuck the tailbone slightly",
         "Comfortable stretch — never pain"],
        ["Squeeze the glute of the stretched leg to deepen it safely."],
        ["Arching the low back", "Knee flaring sideways", "Yanking"],
        "If holding the ankle bothers the knee, rest the foot on a low "
        "chair behind you instead.",
        "Add a gentle forward hip shift.",
        "Foot on a chair version.",
        "Side-lying quad stretch.",
        yt_query="standing quadriceps stretch proper form"),

    "stretch_hamstring": _ex(
        "Standing Hamstring Stretch (hip-hinge)", "stretch_hamstring",
        "Hamstrings",
        "Restores hamstring length with a flat back after posterior-chain "
        "work — keeps sprint mechanics free.",
        1, "30-45 s/side", "static", "—", "2",
        "Place one heel on a low step/curb, leg straight, standing leg "
        "soft.",
        "With a flat back, hinge at the hips toward the raised leg until "
        "a clear (not sharp) stretch behind the thigh. Hands on the "
        "standing thigh. Breathe.",
        ["Hinge, don't round", "Chest toward the foot, not head toward "
         "knee", "Relax into the exhale"],
        ["Point the raised foot's toes to the ceiling, then gently flex "
         "the ankle for a calf bonus."],
        ["Rounding the spine to touch toes", "Bouncing",
         "Locking the standing knee"],
        "Never stretch a hamstring to pain — especially within 48 h of "
        "sprint work.",
        "Slightly higher step over the weeks.",
        "Lying strap/towel hamstring stretch.",
        "Lying hamstring stretch with towel.",
        yt_query="standing hamstring stretch flat back"),

    "stretch_hip_flexor": _ex(
        "Half-Kneeling Hip Flexor Stretch", "stretch_hip_flexor",
        "Hip flexors, rectus femoris",
        "Footballers live in hip flexion (sprinting, sitting, kicking). "
        "Opening the hip front lets the glutes fully extend the hip — "
        "more sprint power, less back strain.",
        1, "30-45 s/side", "static + breath", "—", "2",
        "Half-kneeling (pad the down knee), both knees ~90°, torso tall.",
        "Tuck the tailbone, squeeze the down-leg glute and shift the "
        "hips slightly forward until the front of that hip stretches. "
        "Raise the same-side arm overhead and side-bend a touch away for "
        "extra.",
        ["Tuck the tail first, then shift", "Squeeze the back-leg glute",
         "Grow tall — don't just lean"],
        ["The tuck-and-squeeze does more than the forward lunge does — "
         "small movement, big stretch."],
        ["Arching the low back and calling it a stretch",
         "Front knee drifting past the toes"],
        "Comfortable pressure on the kneecap only — always pad the down "
        "knee.",
        "Reach overhead + slight side bend + back-foot elevated (couch "
        "stretch).",
        "Standing hip-flexor lean.",
        "Couch stretch (rear foot elevated).",
        yt_query="half kneeling hip flexor stretch proper form"),

    "stretch_glute": _ex(
        "Figure-4 Glute Stretch", "stretch_glute",
        "Glutes, piriformis",
        "Releases the deep hip rotators after all the glute work — happy "
        "hips take pressure off both the knee and the low back.",
        1, "30-45 s/side", "static", "—", "2",
        "Lie on your back, knees bent. Cross the right ankle over the "
        "left knee, flexing the right foot.",
        "Reach through and hug the left thigh toward the chest until the "
        "right glute stretches. Keep the head and shoulders relaxed on "
        "the floor. Swap.",
        ["Flex the crossed foot (protects the knee)",
         "Pull the thigh, not the shin", "Shoulders stay down"],
        ["Gently press the crossed knee away with the elbow for a deeper "
         "line."],
        ["Pulling on the shin of the crossed leg", "Neck craning up"],
        "Pull on the back of the thigh, never on the crossed shin — that "
        "torques the healing knee.",
        "Seated or standing figure-4 (deeper).",
        "Feet-on-wall figure-4 (lighter).",
        "Pigeon stretch (careful, advanced).",
        yt_query="figure 4 stretch glute piriformis lying"),

    "stretch_calf": _ex(
        "Wall Calf Stretch (straight + bent knee)", "stretch_calf",
        "Gastrocnemius (straight), soleus (bent)",
        "Two-part calf stretch restoring the ankle range that keeps "
        "squats deep and landings soft.",
        1, "30 s each variation/side", "static", "—", "2",
        "Hands on a wall, one leg back with the heel down, toes pointing "
        "dead straight forward.",
        "Straight-knee: lean in until the upper calf stretches — 30 s. "
        "Then bend the back knee slightly, keeping the heel down, to move "
        "the stretch to the lower calf/Achilles — 30 s. Swap legs.",
        ["Heel glued down", "Toes point at the wall",
         "Both versions, every time"],
        ["The bent-knee half is the one people skip — it's also the one "
         "your ankle mobility needs most."],
        ["Back toes turned out", "Heel floating", "Bouncing"],
        "Gentle Achilles pull is the goal; sharp heel pain is a stop sign.",
        "Drop the heel off a step edge instead.",
        "Reduce the lean.",
        "Downward-dog pedals.",
        yt_query="calf stretch wall gastrocnemius soleus"),

    "stretch_chest": _ex(
        "Doorway Pec Stretch", "stretch_chest",
        "Pectorals, anterior shoulder",
        "Opens the chest so the shoulder blades can sit back where they "
        "belong — undoing desk posture that crowds the healing shoulder.",
        1, "30 s/side", "static, gentle", "—", "2",
        "Forearm on a doorframe, elbow slightly BELOW shoulder height "
        "(safer for your shoulder), staggered stance.",
        "Turn the body gently away from the arm until a soft stretch "
        "crosses the chest. Breathe. Do NOT push into any front-of-"
        "shoulder pinch or nervy feeling.",
        ["Elbow below shoulder height", "Soft stretch, long breaths",
         "Turn the body — don't crank the arm"],
        ["For a labral-injury shoulder, low-and-gentle beats deep — this "
         "stretch should whisper."],
        ["Elbow set high (impinges the joint)", "Aggressive leaning",
         "Any 'opening up' apprehension feeling"],
        "The stretch position resembles the dislocation position — that "
        "is why the elbow stays LOW and the intensity stays gentle. Any "
        "apprehension = skip it entirely; the open book covers the need.",
        "Very gradually raise the elbow toward shoulder height over "
        "months.",
        "Open book stretch (side-lying).",
        "Open book thoracic rotation.",
        yt_query="doorway pec stretch safe shoulder"),

    "cross_body_stretch": _ex(
        "Cross-Body Posterior Shoulder Stretch", "band_er",
        "Posterior deltoid, posterior capsule",
        "A tight back capsule pushes the ball of the shoulder forward — "
        "the direction yours dislocated. Stretching the back of the "
        "shoulder actually improves front-side stability.",
        1, "30 s/side", "static", "—", "2",
        "Stand or sit tall. Bring the right arm across the chest at "
        "shoulder height.",
        "With the left hand above the right elbow, gently pull the arm "
        "across until the BACK of the right shoulder stretches. Keep the "
        "right shoulder blade from rolling forward — pin it back.",
        ["Pull at the elbow, not the wrist", "Blade pinned back",
         "Feel it behind the shoulder, never in front"],
        ["If you feel it in the FRONT of the shoulder, the blade has "
         "rolled forward — reset and pull less."],
        ["Shrugging the shoulder up", "Front-of-shoulder stretching "
         "(wrong target)"],
        "Back-of-shoulder stretch only. Front pain or apprehension = "
        "release immediately.",
        "Side-lying sleeper stretch (advanced, gentle).",
        "Reduce the pull.",
        "Sleeper stretch (only if fully comfortable).",
        yt_query="cross body shoulder stretch posterior capsule"),

    "foam_roll_quads": _ex(
        "Foam Rolling — Quads / Calves / Glutes", "foam_roll",
        "Quadriceps, calves, glutes (fascia)",
        "Down-regulates tone after training and gives a gentle flush to "
        "worked tissue — a recovery accelerant that costs 5 minutes.",
        1, "60-90 s per area", "slow rolls", "—", "3",
        "Foam roller on the floor; forearms supporting the trunk.",
        "Roll each thigh slowly hip-to-knee (never over the kneecap), "
        "pausing 10-15 s on tender spots and breathing into them. Then "
        "calves, then glutes (sit on the roller, figure-4 the leg).",
        ["Slow — 2-3 cm per second", "Breathe into tender spots",
         "Never roll the joint itself"],
        ["Tender is productive; wincing is too much — take weight off "
         "through the arms."],
        ["Racing back and forth", "Rolling directly over the knee",
         "White-knuckle pain tolerance"],
        "Skip any area with acute sharp pain or swelling.",
        "Single-leg (stack one leg over the other).",
        "Use a massage ball standing against a wall.",
        "Massage gun (light) or hands-on self-massage.",
        equipment="Foam roller",
        yt_query="foam rolling legs quads calves technique"),

    "breathing_reset": _ex(
        "Diaphragmatic Breathing Reset", "breathing",
        "Diaphragm, parasympathetic nervous system",
        "Ninety seconds of slow belly breathing flips the body from "
        "fight-mode to recovery-mode — measurably better HRV and a calm "
        "end to every session.",
        1, "8-10 breaths (~2 min)", "4 s in / 6-8 s out", "—", "1",
        "Lie on your back, knees bent, one hand on the chest, one on the "
        "belly.",
        "Inhale through the nose 4 s — the belly hand rises, the chest "
        "hand barely moves. Exhale through pursed lips 6-8 s, letting the "
        "ribs melt down. Repeat.",
        ["Belly hand moves, chest hand doesn't", "Exhale longer than the "
         "inhale", "Jaw and shoulders loose"],
        ["Also brilliant before sleep on the night before match day."],
        ["Chest-dominant gulping", "Forcing the breath"],
        "None — universally safe. The most underrated recovery tool in "
        "sport.",
        "Extend the exhale to 10 s; add a 2-s hold after the inhale.",
        "Any comfortable slow breathing.",
        "Box breathing (4-4-4-4).",
        yt_query="diaphragmatic breathing exercise recovery"),

    # ================================================================
    # WEEK-4 ASSESSMENTS
    # ================================================================
    "assess_wall_sit": _ex(
        "TEST — Wall-Sit Max Hold", "wall_sit",
        "Quadriceps endurance",
        "Month-end benchmark of isometric quad capacity. Target: 60 s+ "
        "pain-free at 90°. Record the time in the notes.",
        1, "1 max hold", "isometric to form-failure", "full recovery", "9",
        "Standard wall sit at your best pain-free depth (note the depth).",
        "Hold as long as form allows. Stop at pain >2/10 or when the "
        "thighs start rising. Record seconds + depth + pain score.",
        ["Same depth as training", "Stop on form-failure, not collapse",
         "Write down the number"],
        ["Compare with Week 1's training holds — expect +30-60 %."],
        ["Changing depth mid-hold", "Hands on thighs"],
        "One attempt only, fully warmed up.",
        "Next month: 90° standard depth for all tests.",
        "Submaximal 45 s hold if the knee is grumpy today.",
        "—",
        yt_query="wall sit test quad endurance"),

    "assess_sl_calf": _ex(
        "TEST — Single-Leg Calf Raise Max Reps", "calf_raise",
        "Calf strength-endurance + left/right symmetry",
        "Benchmark: 20-25 clean full-range reps per side, with <10 % "
        "side-to-side difference. Record both numbers.",
        1, "max reps each side", "2-0-2-0 strict", "2 min between sides", "9",
        "Single-leg calf raise setup on a step, fingertips on the wall.",
        "Full-range reps at a strict tempo until the range visibly "
        "shrinks — that rep doesn't count. Record reps per side.",
        ["Every rep full height and full depth", "Strict tempo — no "
         "bouncing", "Both sides, rested"],
        ["Do the weaker/injured side first, fresh."],
        ["Counting shrinking half-reps", "Leaning into the wall"],
        "Stop at calf cramp or Achilles pain.",
        "Add the loaded version next month.",
        "Two-leg max reps.",
        "—",
        yt_query="single leg calf raise test"),

    "assess_sl_hop": _ex(
        "TEST — Single-Leg Hop for Distance", "hop",
        "Explosive strength + landing confidence, L/R symmetry",
        "The classic ACL return-to-sport metric. Target symmetry: hop "
        "distance on the injured leg ≥90 % of the healthy leg. ONLY "
        "attempt if Weeks 3-4 hop training was pain-free.",
        1, "3 hops/side (best counts)", "max effort, stuck landing", "1 min between hops", "9",
        "Toe on a start line, single-leg athletic stance. Measuring tape "
        "along the floor.",
        "Hop forward maximally and STICK the landing on the same leg for "
        "2 s — a hop only counts if the landing is stuck and clean. "
        "Measure toe-to-heel. Best of three per side.",
        ["No stick, no score", "Knee tracks on takeoff AND landing",
         "Healthy leg first"],
        ["Injured ÷ healthy × 100 = your symmetry %. Write it down — it "
         "steers next month."],
        ["Counting unstuck landings", "Testing with any knee swelling",
         "Competing with yourself past pain"],
        "GATE: skip entirely if hops caused any pain this month, or any "
        "swelling exists today. This is a test, not a challenge.",
        "Triple hop and crossover hop tests next block.",
        "Skip — repeat the Y-balance test instead.",
        "Y-balance reach test.",
        yt_query="single leg hop test ACL distance"),

    "assess_y_balance": _ex(
        "TEST — Y-Balance Best Reach", "balance",
        "Dynamic knee control, L/R symmetry",
        "Measures single-leg control through range. A forward-reach "
        "difference >4 cm between legs predicts elevated injury risk — "
        "it becomes next month's priority if found.",
        1, "3 reaches × 3 directions/side", "slow, controlled", "30 s", "7",
        "Y-balance setup; a tape measure along each reach line.",
        "Best controlled featherlight reach in each direction, each leg. "
        "Record the best forward reach per side in the notes.",
        ["Featherlight taps only", "Hands free (no support) for the test",
         "Record every direction"],
        ["Normalise if curious: reach ÷ leg length × 100."],
        ["Weighting the reach foot", "Stance heel lifting"],
        "Controlled test — safe whenever balance training was pain-free.",
        "Add the composite score next month.",
        "Supported (fingertip) version.",
        "—",
        yt_query="y balance test how to perform"),

    "assess_plank": _ex(
        "TEST — Plank Max Hold", "plank",
        "Core endurance",
        "Benchmark trunk endurance. Target: 90 s+ with perfect line. "
        "Record the time.",
        1, "1 max hold", "isometric to form-failure", "—", "9",
        "Perfect front plank position.",
        "Hold until the hips sag or rise despite one self-correction cue. "
        "The clock stops at the SECOND form break, not at collapse.",
        ["Form decides the end, not agony", "Breathe throughout",
         "One warning, then done"],
        ["Have your phone film side-on — honest judging."],
        ["Grinding out a sagging plank (trains back pain, not core)"],
        "Stop for any low-back discomfort.",
        "Weighted or feet-elevated test next month.",
        "Knee plank max hold.",
        "—",
        yt_query="plank test core endurance"),
}


def get_exercise(ex_id: str) -> dict:
    """Fetch a library exercise by id (raises KeyError if unknown)."""
    return EXERCISES[ex_id]


def all_exercise_ids():
    return list(EXERCISES.keys())
