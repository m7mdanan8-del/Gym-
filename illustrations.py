"""
illustrations.py
================
Self-contained SVG exercise illustrations (no internet required).

Each movement pattern gets a clean line-figure drawing. The figure is drawn
in a neutral ink that reads on both dark and light themes; the *target/working*
body segment or implement is highlighted in the accent blue so the user
instantly sees what the exercise is about.

Usage:
    from illustrations import get_svg
    st.markdown(get_svg("squat"), unsafe_allow_html=True)
"""

import re

# Neutral ink that passes on both light (#fcfcfb) and dark (#1a1a19) surfaces.
INK = "#898781"
ACCENT = "#3987e5"      # highlight: the working joint / muscle / implement
GROUND = "#55534e"


def _wrap(body: str, label: str = "") -> str:
    """Wrap SVG body in a responsive, theme-neutral frame.

    The output is collapsed to a single line: Markdown treats indented /
    multi-line HTML as a code block, so inline SVG must carry no newlines.
    """
    body = re.sub(r"<!--.*?-->", "", body)          # strip drawing comments
    html = f"""
<div style="max-width:340px;margin:0 auto;">
<svg viewBox="0 0 220 150" xmlns="http://www.w3.org/2000/svg" role="img"
     aria-label="{label}" style="width:100%;height:auto;">
  <g fill="none" stroke="{INK}" stroke-width="5" stroke-linecap="round"
     stroke-linejoin="round">
    {body}
  </g>
  <line x1="10" y1="140" x2="210" y2="140" stroke="{GROUND}" stroke-width="3"
        stroke-linecap="round" opacity="0.6"/>
</svg>
</div>
"""
    return re.sub(r"\s+", " ", html).strip()


# --------------------------------------------------------------------------
# Movement-pattern drawings.
# Every figure: circle head + connected trunk/limb strokes.
# Accent strokes mark the prime mover / key joint of the pattern.
# --------------------------------------------------------------------------
_PATTERNS = {
    # -------------------------- lower body ------------------------------
    "squat": _wrap("""
      <circle cx="118" cy="42" r="11"/>
      <path d="M114 53 L102 88"/>                                  <!-- trunk -->
      <path d="M102 88 L120 112 L118 138" stroke="{A}"/>           <!-- thigh+shin -->
      <path d="M118 138 L132 138" stroke="{A}"/>                   <!-- foot -->
      <path d="M112 62 L138 74 L156 70"/>                          <!-- arms fwd -->
      <circle cx="160" cy="69" r="7" stroke="{A}"/>                <!-- goblet -->
    """.replace("{A}", ACCENT), "Squat"),

    "split_squat": _wrap("""
      <circle cx="110" cy="34" r="11"/>
      <path d="M110 45 L108 84"/>
      <path d="M108 84 L134 100 L134 138" stroke="{A}"/>           <!-- front leg -->
      <path d="M134 138 L148 138" stroke="{A}"/>
      <path d="M108 84 L84 108 L64 122"/>                          <!-- rear leg -->
      <path d="M64 122 L58 132"/>
      <path d="M108 56 L96 76"/><path d="M110 56 L122 76"/>        <!-- arms -->
    """.replace("{A}", ACCENT), "Split squat / lunge"),

    "step_up": _wrap("""
      <rect x="128" y="104" width="62" height="36" rx="3"/>
      <circle cx="112" cy="26" r="11"/>
      <path d="M112 37 L114 74"/>
      <path d="M114 74 L138 86 L140 104" stroke="{A}"/>            <!-- lead leg on box -->
      <path d="M140 104 L154 104" stroke="{A}"/>
      <path d="M114 74 L98 106 L96 138"/>
      <path d="M112 46 L96 64"/><path d="M114 46 L130 60"/>
    """.replace("{A}", ACCENT), "Step-up"),

    "hinge": _wrap("""
      <circle cx="152" cy="58" r="11"/>
      <path d="M144 66 L100 82" stroke="{A}"/>                     <!-- flat back -->
      <path d="M100 82 L104 112 L102 138"/>
      <path d="M102 138 L116 138"/>
      <path d="M136 72 L134 100"/>                                 <!-- arms hang -->
      <path d="M124 104 L146 104" stroke="{A}"/>                   <!-- bar/DBs -->
    """.replace("{A}", ACCENT), "Hip hinge / RDL"),

    "single_leg_hinge": _wrap("""
      <circle cx="150" cy="52" r="11"/>
      <path d="M142 60 L98 74" stroke="{A}"/>                      <!-- torso tips -->
      <path d="M98 74 L60 62"/>                                    <!-- rear leg lifts -->
      <path d="M98 74 L104 108 L102 138" stroke="{A}"/>            <!-- stance leg -->
      <path d="M102 138 L116 138"/>
      <path d="M134 66 L132 96"/>
      <circle cx="132" cy="102" r="6" stroke="{A}"/>
    """.replace("{A}", ACCENT), "Single-leg Romanian deadlift"),

    "bridge": _wrap("""
      <circle cx="42" cy="112" r="11"/>
      <path d="M52 108 L108 88" stroke="{A}"/>                     <!-- trunk raised -->
      <path d="M108 88 L128 108 L130 138" stroke="{A}"/>           <!-- thigh+shin -->
      <path d="M130 138 L142 138"/>
      <path d="M62 112 L78 128"/>                                  <!-- arm down -->
    """.replace("{A}", ACCENT), "Glute bridge / hip thrust"),

    "hip_thrust": _wrap("""
      <rect x="18" y="92" width="34" height="48" rx="3"/>
      <circle cx="46" cy="70" r="11"/>
      <path d="M54 78 L106 84" stroke="{A}"/>                      <!-- torso on bench -->
      <path d="M106 84 L124 110 L126 138" stroke="{A}"/>
      <path d="M126 138 L138 138"/>
      <circle cx="102" cy="72" r="9" stroke="{A}"/>                <!-- load on hips -->
    """.replace("{A}", ACCENT), "Hip thrust"),

    "hamstring_curl": _wrap("""
      <circle cx="36" cy="122" r="11"/>
      <path d="M48 120 L108 112"/>                                  <!-- body lying -->
      <path d="M108 112 L146 116" stroke="{A}"/>                    <!-- thigh -->
      <path d="M146 116 L138 84" stroke="{A}"/>                     <!-- heel curls in -->
      <circle cx="136" cy="78" r="6"/>
      <path d="M64 122 L84 130"/>
    """.replace("{A}", ACCENT), "Lying / slider hamstring curl"),

    "nordic": _wrap("""
      <circle cx="86" cy="34" r="11"/>
      <path d="M90 45 L112 92" stroke="{A}"/>                       <!-- long body falling fwd -->
      <path d="M112 92 L112 122" stroke="{A}"/>                     <!-- shin anchored -->
      <path d="M112 122 L98 132"/>
      <rect x="118" y="118" width="30" height="14" rx="3"/>         <!-- anchor pad -->
      <path d="M92 56 L78 78"/><path d="M94 58 L84 82"/>            <!-- arms ready -->
    """.replace("{A}", ACCENT), "Nordic hamstring curl"),

    "calf_raise": _wrap("""
      <circle cx="118" cy="26" r="11"/>
      <path d="M118 37 L118 86"/>
      <path d="M118 86 L120 114" />
      <path d="M120 114 L122 128" stroke="{A}"/>                    <!-- ankle -->
      <path d="M122 128 L134 122" stroke="{A}"/>                    <!-- heel raised -->
      <rect x="128" y="128" width="34" height="12" rx="2"/>         <!-- step edge -->
      <path d="M118 48 L102 60"/><path d="M118 48 L134 60"/>
    """.replace("{A}", ACCENT), "Calf raise"),

    "wall_sit": _wrap("""
      <path d="M60 20 L60 140"/>                                    <!-- wall -->
      <circle cx="78" cy="46" r="11"/>
      <path d="M74 57 L68 92"/>                                     <!-- back on wall -->
      <path d="M68 92 L106 96 L108 138" stroke="{A}"/>              <!-- 90/90 legs -->
      <path d="M108 138 L122 138"/>
      <path d="M72 66 L88 84"/>
    """.replace("{A}", ACCENT), "Wall sit"),

    "tke": _wrap("""
      <path d="M28 30 L28 96"/>
      <path d="M28 62 L92 78" stroke="{A}" stroke-dasharray="4 6"/> <!-- band -->
      <circle cx="112" cy="30" r="11"/>
      <path d="M112 41 L108 82"/>
      <path d="M108 82 L96 108 L98 138" stroke="{A}"/>              <!-- knee straightens -->
      <path d="M98 138 L112 138"/>
      <path d="M108 82 L128 112 L128 138"/>
      <path d="M110 52 L94 68"/>
    """.replace("{A}", ACCENT), "Terminal knee extension with band"),

    "clamshell": _wrap("""
      <circle cx="34" cy="106" r="11"/>
      <path d="M46 108 L102 104"/>                                  <!-- side-lying trunk -->
      <path d="M102 104 L138 118"/>                                 <!-- bottom thigh -->
      <path d="M138 118 L126 136"/>
      <path d="M102 104 L136 92" stroke="{A}"/>                     <!-- top knee opens -->
      <path d="M136 92 L128 112" stroke="{A}"/>
      <path d="M60 112 L76 122"/>
    """.replace("{A}", ACCENT), "Clamshell"),

    "side_leg_raise": _wrap("""
      <circle cx="34" cy="112" r="11"/>
      <path d="M46 112 L106 108"/>
      <path d="M106 108 L152 116"/>                                 <!-- bottom leg -->
      <path d="M152 116 L166 116"/>
      <path d="M106 108 L156 82" stroke="{A}"/>                     <!-- top leg lifts -->
      <path d="M156 82 L168 78" stroke="{A}"/>
      <path d="M60 116 L78 126"/>
    """.replace("{A}", ACCENT), "Side-lying leg raise"),

    "band_walk": _wrap("""
      <circle cx="108" cy="34" r="11"/>
      <path d="M108 45 L106 82"/>
      <path d="M106 82 L84 108 L80 138"/>
      <path d="M106 82 L130 108 L136 138"/>
      <path d="M84 116 L132 116" stroke="{A}" stroke-dasharray="4 5"/> <!-- band -->
      <path d="M104 54 L90 70"/><path d="M108 54 L124 70"/>
      <path d="M150 96 L166 96" stroke="{A}"/><path d="M160 88 L170 96 L160 104" stroke="{A}"/>
    """.replace("{A}", ACCENT), "Lateral band walk"),

    "balance": _wrap("""
      <circle cx="110" cy="28" r="11"/>
      <path d="M110 39 L110 84"/>
      <path d="M110 84 L112 112 L110 138" stroke="{A}"/>            <!-- stance leg -->
      <path d="M110 138 L124 138" stroke="{A}"/>
      <path d="M110 84 L88 100 L92 118"/>                           <!-- free leg bent -->
      <path d="M110 50 L86 56"/><path d="M110 50 L134 56"/>         <!-- arms out -->
    """.replace("{A}", ACCENT), "Single-leg balance"),

    "hop": _wrap("""
      <circle cx="106" cy="22" r="11"/>
      <path d="M106 33 L104 68"/>
      <path d="M104 68 L120 92 L116 116" stroke="{A}"/>             <!-- landing leg -->
      <path d="M116 116 L130 118" stroke="{A}"/>
      <path d="M104 68 L86 88 L92 106"/>
      <path d="M104 42 L84 34"/><path d="M106 42 L126 34"/>         <!-- arms up -->
      <path d="M62 128 L84 128" opacity="0.5"/><path d="M56 134 L92 134" opacity="0.35"/>
    """.replace("{A}", ACCENT), "Hop and stick landing"),

    "leg_press": _wrap("""
      <path d="M30 128 L74 128 L74 96 L46 78"/>                     <!-- seat -->
      <circle cx="58" cy="62" r="11"/>
      <path d="M62 72 L74 100"/>                                    <!-- torso on seat -->
      <path d="M74 100 L110 84 L142 96" stroke="{A}"/>              <!-- legs pressing -->
      <path d="M148 60 L148 130" stroke="{A}"/>                     <!-- sled plate -->
      <path d="M148 70 L176 70"/><path d="M148 120 L176 120"/>      <!-- rails -->
      <path d="M70 84 L92 92"/>
    """.replace("{A}", ACCENT), "Leg press machine"),

    "pulldown": _wrap("""
      <path d="M60 16 L164 16"/>                                    <!-- crossbar -->
      <path d="M112 16 L112 34" stroke-dasharray="4 5"/>            <!-- cable -->
      <path d="M84 36 L140 36" stroke="{A}"/>                       <!-- bar -->
      <circle cx="112" cy="62" r="11"/>
      <path d="M112 73 L112 106"/>
      <path d="M112 106 L94 120 L96 140"/><path d="M112 106 L130 120 L132 140"/>
      <path d="M108 78 L88 56 L86 38" stroke="{A}"/>                <!-- pulling arms -->
      <path d="M116 78 L136 56 L138 38" stroke="{A}"/>
    """.replace("{A}", ACCENT), "Lat pulldown"),

    "jog": _wrap("""
      <circle cx="112" cy="30" r="11"/>
      <path d="M112 41 L106 78"/>
      <path d="M106 78 L128 100 L124 130" stroke="{A}"/>
      <path d="M106 78 L86 96 L94 116"/>
      <path d="M110 50 L130 62"/><path d="M110 50 L90 64"/>
      <path d="M52 60 L70 60" opacity="0.5"/><path d="M44 76 L66 76" opacity="0.35"/>
    """.replace("{A}", ACCENT), "Light jog / march"),

    "bike": _wrap("""
      <circle cx="66" cy="112" r="22"/>
      <circle cx="158" cy="112" r="22"/>
      <path d="M66 112 L104 112 L124 84 L152 84"/>
      <path d="M104 112 L96 78 L120 70"/>
      <circle cx="128" cy="34" r="10"/>
      <path d="M126 44 L112 66" />
      <path d="M114 66 L104 96 L108 112" stroke="{A}"/>             <!-- pedalling leg -->
      <path d="M120 52 L146 66"/>
    """.replace("{A}", ACCENT), "Stationary bike"),

    # -------------------------- upper body ------------------------------
    "band_er": _wrap("""
      <circle cx="96" cy="30" r="11"/>
      <path d="M96 41 L96 88"/>
      <path d="M96 88 L86 112 L88 138"/><path d="M96 88 L110 112 L110 138"/>
      <path d="M96 52 L114 66" stroke="{A}"/>                       <!-- upper arm pinned -->
      <path d="M114 66 L148 56" stroke="{A}"/>                      <!-- forearm rotates out -->
      <path d="M148 56 L196 62" stroke-dasharray="4 5"/>            <!-- band -->
      <path d="M162 40 L174 34" opacity="0.6"/>
    """.replace("{A}", ACCENT), "Banded shoulder external rotation"),

    "band_er_90": _wrap("""
      <circle cx="92" cy="34" r="11"/>
      <path d="M92 45 L92 92"/>
      <path d="M92 92 L82 116 L84 138"/><path d="M92 92 L106 116 L106 138"/>
      <path d="M92 54 L126 54" stroke="{A}"/>                       <!-- arm abducted 90 -->
      <path d="M126 54 L128 24" stroke="{A}"/>                      <!-- forearm vertical -->
      <path d="M128 24 L182 30" stroke-dasharray="4 5"/>
    """.replace("{A}", ACCENT), "90/90 banded external rotation"),

    "row": _wrap("""
      <circle cx="126" cy="44" r="11"/>
      <path d="M120 52 L94 76"/>                                    <!-- hinged trunk -->
      <path d="M94 76 L100 108 L98 138"/>
      <path d="M98 138 L112 138"/>
      <path d="M112 62 L124 88" stroke="{A}"/>                      <!-- pulling arm -->
      <path d="M124 88 L120 104"/>
      <circle cx="120" cy="110" r="6" stroke="{A}"/>
    """.replace("{A}", ACCENT), "Row"),

    "face_pull": _wrap("""
      <path d="M196 26 L196 60"/>
      <path d="M150 46 L192 42" stroke-dasharray="4 5"/>            <!-- band high anchor -->
      <circle cx="96" cy="42" r="11"/>
      <path d="M96 53 L96 96"/>
      <path d="M96 96 L86 118 L88 138"/><path d="M96 96 L108 118 L108 138"/>
      <path d="M96 60 L126 50 L148 44" stroke="{A}"/>               <!-- pull to face -->
      <path d="M96 60 L120 66 L146 50" stroke="{A}" opacity="0.65"/>
    """.replace("{A}", ACCENT), "Band face pull"),

    "scaption": _wrap("""
      <circle cx="108" cy="34" r="11"/>
      <path d="M108 45 L108 92"/>
      <path d="M108 92 L96 116 L98 138"/><path d="M108 92 L120 116 L120 138"/>
      <path d="M108 54 L74 34" stroke="{A}"/>                       <!-- arms raise on Y -->
      <path d="M108 54 L142 34" stroke="{A}"/>
      <circle cx="70" cy="31" r="5" stroke="{A}"/><circle cx="146" cy="31" r="5" stroke="{A}"/>
    """.replace("{A}", ACCENT), "Scaption / Y-raise"),

    "wall_slide": _wrap("""
      <path d="M156 16 L156 140"/>                                  <!-- wall -->
      <circle cx="128" cy="46" r="11"/>
      <path d="M130 57 L134 96"/>
      <path d="M134 96 L124 118 L126 138"/><path d="M134 96 L146 118 L146 138"/>
      <path d="M132 60 L152 44" stroke="{A}"/>                      <!-- forearm slides up -->
      <path d="M152 44 L152 20" stroke="{A}"/>
    """.replace("{A}", ACCENT), "Wall slide"),

    "press": _wrap("""
      <circle cx="110" cy="44" r="11"/>
      <path d="M110 55 L110 96"/>
      <path d="M110 96 L98 118 L100 138"/><path d="M110 96 L124 118 L124 138"/>
      <path d="M110 60 L134 46" stroke="{A}"/>                      <!-- pressing arm -->
      <path d="M134 46 L150 24" stroke="{A}"/>
      <circle cx="153" cy="19" r="7" stroke="{A}"/>
      <path d="M110 60 L92 74"/>
    """.replace("{A}", ACCENT), "Landmine / dumbbell press"),

    "pushup": _wrap("""
      <circle cx="46" cy="74" r="11"/>
      <path d="M56 80 L128 96 L172 106"/>                           <!-- straight body -->
      <path d="M172 106 L184 134"/>
      <path d="M62 86 L58 112 L62 136" stroke="{A}"/>               <!-- bent arm -->
      <path d="M108 92 L104 116 L108 138" stroke="{A}"/>
    """.replace("{A}", ACCENT), "Push-up"),

    "carry": _wrap("""
      <circle cx="110" cy="28" r="11"/>
      <path d="M110 39 L110 86"/>
      <path d="M110 86 L94 112 L92 138"/><path d="M110 86 L128 110 L134 138"/>
      <path d="M110 50 L146 58" stroke="{A}"/>                      <!-- loaded arm -->
      <path d="M146 58 L146 84"/>
      <rect x="136" y="86" width="20" height="16" rx="3" stroke="{A}"/>
      <path d="M110 50 L82 64"/>
    """.replace("{A}", ACCENT), "Loaded carry"),

    # ------------------------------ core --------------------------------
    "plank": _wrap("""
      <circle cx="42" cy="86" r="11"/>
      <path d="M54 92 L128 104 L170 112" stroke="{A}"/>             <!-- rigid line -->
      <path d="M170 112 L186 136"/>
      <path d="M58 96 L54 138"/><path d="M54 138 L70 138"/>         <!-- forearm -->
    """.replace("{A}", ACCENT), "Front plank"),

    "side_plank": _wrap("""
      <circle cx="44" cy="72" r="11"/>
      <path d="M54 80 L128 102 L176 116" stroke="{A}"/>
      <path d="M176 116 L192 138"/>
      <path d="M62 86 L58 138"/><path d="M50 138 L74 138"/>
      <path d="M56 74 L52 40"/>                                     <!-- top arm up -->
    """.replace("{A}", ACCENT), "Side plank"),

    "deadbug": _wrap("""
      <circle cx="52" cy="118" r="11"/>
      <path d="M64 118 L124 116"/>                                  <!-- back on floor -->
      <path d="M124 116 L142 88" stroke="{A}"/>                     <!-- one leg extends -->
      <path d="M142 88 L166 96" stroke="{A}"/>
      <path d="M124 116 L134 92 L122 76"/>                          <!-- other leg 90/90 -->
      <path d="M76 114 L72 78" stroke="{A}"/>                       <!-- opposite arm up -->
      <path d="M92 114 L108 88"/>
    """.replace("{A}", ACCENT), "Dead bug"),

    "bird_dog": _wrap("""
      <circle cx="58" cy="70" r="11"/>
      <path d="M68 76 L138 84"/>                                    <!-- flat back -->
      <path d="M74 80 L74 122"/><path d="M74 122 L86 122"/>         <!-- support arm -->
      <path d="M138 84 L146 120"/><path d="M146 120 L158 120"/>     <!-- support knee -->
      <path d="M64 74 L26 62" stroke="{A}"/>                        <!-- arm reaches -->
      <path d="M138 84 L184 68" stroke="{A}"/>                      <!-- leg reaches -->
    """.replace("{A}", ACCENT), "Bird dog"),

    "pallof": _wrap("""
      <path d="M24 24 L24 96"/>
      <path d="M24 52 L88 66" stroke-dasharray="4 5"/>              <!-- band from side -->
      <circle cx="112" cy="34" r="11"/>
      <path d="M112 45 L112 90"/>
      <path d="M112 90 L96 114 L96 138"/><path d="M112 90 L128 114 L130 138"/>
      <path d="M112 58 L88 66"/>
      <path d="M88 66 L146 66" stroke="{A}"/>                       <!-- press out, resist twist -->
      <circle cx="150" cy="66" r="5" stroke="{A}"/>
    """.replace("{A}", ACCENT), "Pallof press"),

    "copenhagen": _wrap("""
      <rect x="140" y="96" width="52" height="44" rx="3"/>
      <circle cx="34" cy="82" r="11"/>
      <path d="M44 88 L112 96 L152 100" stroke="{A}"/>              <!-- body bridged -->
      <path d="M152 100 L172 100" stroke="{A}"/>                    <!-- top leg on bench -->
      <path d="M50 94 L46 138"/><path d="M42 138 L62 138"/>
      <path d="M100 98 L108 124" opacity="0.6"/>                    <!-- bottom leg free -->
    """.replace("{A}", ACCENT), "Copenhagen adductor plank"),

    # --------------------------- mobility -------------------------------
    "stretch_hamstring": _wrap("""
      <circle cx="70" cy="46" r="11"/>
      <path d="M76 56 L104 80"/>                                    <!-- lean forward -->
      <path d="M104 80 L110 110 L108 138"/>
      <path d="M104 80 L142 96" stroke="{A}"/>                      <!-- straight front leg -->
      <path d="M142 96 L172 102" stroke="{A}"/>
      <path d="M172 102 L176 92"/>
      <path d="M84 64 L120 88"/>
    """.replace("{A}", ACCENT), "Hamstring stretch"),

    "stretch_hip_flexor": _wrap("""
      <circle cx="102" cy="32" r="11"/>
      <path d="M102 43 L104 84"/>
      <path d="M104 84 L134 96 L134 132"/>                          <!-- front leg lunge -->
      <path d="M134 132 L148 132"/>
      <path d="M104 84 L72 108" stroke="{A}"/>                      <!-- rear hip opens -->
      <path d="M72 108 L46 120" stroke="{A}"/>
      <path d="M100 52 L84 40"/><path d="M104 52 L120 42"/>
    """.replace("{A}", ACCENT), "Half-kneeling hip flexor stretch"),

    "stretch_quad": _wrap("""
      <circle cx="104" cy="30" r="11"/>
      <path d="M104 41 L104 86"/>
      <path d="M104 86 L106 112 L104 138"/>
      <path d="M104 138 L118 138"/>
      <path d="M104 86 L128 104" stroke="{A}"/>                     <!-- thigh back -->
      <path d="M128 104 L124 74" stroke="{A}"/>                     <!-- heel to glute -->
      <path d="M106 52 L126 68"/>
      <path d="M102 52 L82 60"/>
    """.replace("{A}", ACCENT), "Standing quad stretch"),

    "stretch_chest": _wrap("""
      <path d="M160 16 L160 140"/>                                  <!-- doorway -->
      <circle cx="112" cy="38" r="11"/>
      <path d="M112 49 L112 94"/>
      <path d="M112 94 L100 118 L102 138"/><path d="M112 94 L126 118 L126 138"/>
      <path d="M112 56 L142 48" stroke="{A}"/>                      <!-- arm on frame -->
      <path d="M142 48 L158 30" stroke="{A}"/>
    """.replace("{A}", ACCENT), "Doorway pec stretch"),

    "stretch_calf": _wrap("""
      <path d="M172 16 L172 140"/>
      <circle cx="92" cy="38" r="11"/>
      <path d="M94 49 L104 88"/>
      <path d="M104 88 L128 110 L130 138"/>                         <!-- front leg -->
      <path d="M104 88 L84 116 L78 138" stroke="{A}"/>              <!-- rear leg straight -->
      <path d="M78 138 L92 138" stroke="{A}"/>
      <path d="M96 56 L140 52"/><path d="M140 52 L168 44"/>
    """.replace("{A}", ACCENT), "Wall calf stretch"),

    "stretch_glute": _wrap("""
      <circle cx="52" cy="98" r="11"/>
      <path d="M62 102 L108 110"/>
      <path d="M108 110 L142 96" stroke="{A}"/>                     <!-- figure-4 leg -->
      <path d="M142 96 L128 118" stroke="{A}"/>
      <path d="M108 110 L134 124 L120 138"/>
      <path d="M78 106 L98 92"/>
    """.replace("{A}", ACCENT), "Figure-4 glute stretch"),

    "foam_roll": _wrap("""
      <circle cx="40" cy="92" r="11"/>
      <path d="M52 98 L118 110"/>
      <circle cx="132" cy="122" r="12" stroke="{A}"/>               <!-- roller -->
      <path d="M118 110 L156 106"/>
      <path d="M156 106 L178 122"/>
      <path d="M58 102 L52 134"/><path d="M46 134 L66 134"/>
    """.replace("{A}", ACCENT), "Foam rolling"),

    "cat_cow": _wrap("""
      <circle cx="56" cy="64" r="11"/>
      <path d="M66 70 Q106 46 142 78" stroke="{A}"/>                <!-- arched spine -->
      <path d="M72 74 L72 120"/><path d="M72 120 L84 120"/>
      <path d="M142 78 L150 118"/><path d="M150 118 L162 118"/>
    """.replace("{A}", ACCENT), "Cat-cow"),

    "worlds_greatest": _wrap("""
      <circle cx="96" cy="36" r="11"/>
      <path d="M98 47 L112 78"/>
      <path d="M112 78 L146 92 L146 128"/>
      <path d="M146 128 L160 128"/>
      <path d="M112 78 L76 104 L48 122"/>
      <path d="M102 56 L106 108"/>                                  <!-- hand inside foot -->
      <path d="M98 56 L86 22" stroke="{A}"/>                        <!-- rotating arm up -->
    """.replace("{A}", ACCENT), "World's greatest stretch"),

    "leg_swing": _wrap("""
      <path d="M40 20 L40 110"/>
      <circle cx="86" cy="32" r="11"/>
      <path d="M86 43 L88 86"/>
      <path d="M88 86 L92 112 L90 138"/>
      <path d="M88 86 L134 72" stroke="{A}"/>                       <!-- swinging leg -->
      <path d="M134 72 L162 62" stroke="{A}"/>
      <path d="M86 52 L44 48"/>                                     <!-- hand on support -->
      <path d="M150 96 Q166 82 158 66" stroke-dasharray="3 6" opacity="0.6"/>
    """.replace("{A}", ACCENT), "Leg swing"),

    "ankle_mob": _wrap("""
      <path d="M176 20 L176 140"/>
      <circle cx="84" cy="42" r="11"/>
      <path d="M86 53 L96 90"/>
      <path d="M96 90 L134 102 L138 138" stroke="{A}"/>             <!-- knee drives to wall -->
      <path d="M138 138 L156 138" stroke="{A}"/>
      <path d="M96 90 L74 116 L70 138"/>
      <path d="M90 60 L130 62"/><path d="M130 62 L170 58"/>
    """.replace("{A}", ACCENT), "Knee-to-wall ankle mobilisation"),

    "breathing": _wrap("""
      <circle cx="60" cy="110" r="11"/>
      <path d="M72 112 L128 108"/>
      <path d="M128 108 L146 90 L142 118"/>                         <!-- knees bent -->
      <path d="M142 118 L152 132"/>
      <ellipse cx="104" cy="98" rx="16" ry="9" stroke="{A}"/>       <!-- belly rise -->
      <path d="M104 82 L104 72" stroke="{A}"/><path d="M99 76 L104 70 L109 76" stroke="{A}"/>
    """.replace("{A}", ACCENT), "Diaphragmatic breathing"),
}


def get_svg(pattern: str) -> str:
    """Return the inline SVG for a movement pattern (fallback: balance figure)."""
    return _PATTERNS.get(pattern, _PATTERNS["balance"])


def available_patterns():
    return sorted(_PATTERNS.keys())
