"""
translations.py
===============
Bilingual (English / العربية) interface layer.

- UI: every label, button, page title and message the app shows.
- Display-level translation for program metadata: section names, day names,
  day focuses, week themes and exercise names are translated at render time
  while the database keeps English keys — so logs and edits stay stable
  when the language changes.
- Arabic mode also flips the layout to RTL (handled in app.py CSS).

The detailed coaching text of each exercise (setup/execution/cues) is kept
in its original language for clinical precision; names, structure and every
interactive control are fully translated.
"""

LANGS = {"en": "English", "ar": "العربية"}

UI = {
    # ---------------- sidebar / navigation ----------------
    "app_title":        {"en": "⚽ Rehab & Performance", "ar": "⚽ التأهيل والأداء"},
    "app_tagline":      {"en": "ACL + shoulder rehab · strength · football performance",
                         "ar": "تأهيل الرباط الصليبي والكتف · قوة · أداء كرة القدم"},
    "nav_workout":      {"en": "🏋️ Today's Workout", "ar": "🏋️ تمرين اليوم"},
    "nav_program":      {"en": "📅 Monthly Program", "ar": "📅 البرنامج الشهري"},
    "nav_dashboard":    {"en": "📈 Progress Dashboard", "ar": "📈 لوحة التقدم"},
    "nav_recovery":     {"en": "😴 Recovery Tracker", "ar": "😴 متابعة الاستشفاء"},
    "nav_edit":         {"en": "✏️ Edit Mode", "ar": "✏️ وضع التعديل"},
    "nav_safety":       {"en": "🛟 Safety Guide", "ar": "🛟 دليل السلامة"},
    "nav_settings":     {"en": "⚙️ Settings", "ar": "⚙️ الإعدادات"},
    "streak":           {"en": "🔥 Streak", "ar": "🔥 أيام متتالية"},
    "days_unit":        {"en": "days", "ar": "يوم"},
    "workouts_completed": {"en": "Workouts completed", "ar": "التمارين المكتملة"},
    "today_is":         {"en": "Today", "ar": "اليوم"},
    "traffic_mini":     {"en": "🟢 0–2 continue · 🟡 3–4 modify · 🔴 5+ stop",
                         "ar": "🟢 ٠–٢ استمر · 🟡 ٣–٤ عدّل · 🔴 ٥+ توقف"},
    "language":         {"en": "Language / اللغة", "ar": "اللغة / Language"},

    # ---------------- workout page ----------------
    "workout_title":    {"en": "🏋️ Today's Workout", "ar": "🏋️ تمرين اليوم"},
    "date":             {"en": "Date", "ar": "التاريخ"},
    "program_week":     {"en": "Program week", "ar": "أسبوع البرنامج"},
    "day":              {"en": "Day", "ar": "اليوم"},
    "week_word":        {"en": "Week", "ar": "الأسبوع"},
    "pain_rules_title": {"en": "🛟 Pain rules — read me before every session",
                         "ar": "🛟 قواعد الألم — اقرأني قبل كل جلسة"},
    "progress_of":      {"en": "exercises", "ar": "تمارين"},
    "complete_word":    {"en": "complete", "ar": "مكتمل"},
    "match_day_info":   {"en": "⚽ **Match day.** Complete the pre-match activation before the "
                                "team warm-up, then the post-match reset within 30 minutes of "
                                "full-time. Log the match in the cardio log below and rate your "
                                "performance in the Recovery tab.",
                         "ar": "⚽ **يوم المباراة.** أكمل تمارين التنشيط قبل إحماء الفريق، ثم "
                                "تمارين الاستعادة خلال ٣٠ دقيقة من نهاية المباراة. سجّل المباراة "
                                "في سجل الكارديو أدناه وقيّم أداءك في تبويب الاستشفاء."},
    "no_program":       {"en": "No program found for this day.", "ar": "لا يوجد برنامج لهذا اليوم."},
    "session_done":     {"en": "🎉 Session complete — that's how champions are "
                                "built! See you at the next one.",
                         "ar": "🎉 اكتملت الجلسة — هكذا يُصنع الأبطال! نلقاك في "
                                "الجلسة القادمة."},
    "quote_prefix":     {"en": "💪 Today's fuel", "ar": "💪 وقود اليوم"},
    "last_time":        {"en": "Last time", "ar": "آخر مرة"},
    "view_label":       {"en": "View", "ar": "طريقة العرض"},
    "view_grid":        {"en": "🔲 Grid", "ar": "🔲 شبكة"},
    "view_list":        {"en": "📋 List", "ar": "📋 قائمة"},
    "open_ex":          {"en": "Open", "ar": "افتح"},
    "photo_start":      {"en": "Start position", "ar": "وضع البداية"},
    "photo_end":        {"en": "Finish position", "ar": "وضع النهاية"},
    "done_btn":         {"en": "✔ Done — back to workout", "ar": "✔ تم — عودة إلى التمرين"},
    "pain_short":       {"en": "pain", "ar": "ألم"},

    # tracker
    "tracker":          {"en": "📋 Tracker", "ar": "📋 المتابعة"},
    "completed":        {"en": "✅ Completed", "ar": "✅ تم الإنجاز"},
    "weight_used":      {"en": "Weight used (kg)", "ar": "الوزن المستخدم (كجم)"},
    "sets_done":        {"en": "Sets done", "ar": "الجولات المنجزة"},
    "pain_scale":       {"en": "Pain (0–10)", "ar": "الألم (٠–١٠)"},
    "difficulty_scale": {"en": "Difficulty (1–10)", "ar": "الصعوبة (١–١٠)"},
    "energy_scale":     {"en": "Energy (1–10)", "ar": "الطاقة (١–١٠)"},
    "reps_done":        {"en": "Reps done", "ar": "التكرارات المنجزة"},
    "notes":            {"en": "Notes", "ar": "ملاحظات"},
    "notes_ph":         {"en": "How did it feel? Test numbers, tweaks…",
                         "ar": "كيف كان الإحساس؟ أرقام الاختبار، التعديلات…"},
    "pain_stop":        {"en": "🔴 Pain ≥5/10 — STOP this exercise. Use the regression or "
                                "alternative, and if this repeats, book a reassessment.",
                         "ar": "🔴 ألم ≥٥/١٠ — أوقف هذا التمرين فورًا. استخدم النسخة الأسهل أو "
                                "البديل، وإذا تكرر ذلك احجز إعادة تقييم مع أخصائي العلاج الطبيعي."},
    "pain_modify":      {"en": "🟡 Pain 3–4/10 — reduce weight, speed or range of motion and "
                                "re-test before continuing.",
                         "ar": "🟡 ألم ٣–٤/١٠ — قلّل الوزن أو السرعة أو مدى الحركة وأعد "
                                "المحاولة قبل الاستمرار."},

    # exercise guide labels
    "why":              {"en": "Why this exercise", "ar": "لماذا هذا التمرين"},
    "start_pos":        {"en": "Starting position", "ar": "وضع البداية"},
    "how_to":           {"en": "How to perform it", "ar": "طريقة الأداء"},
    "key_cues":         {"en": "Key cues", "ar": "نقاط التركيز"},
    "tips_expander":    {"en": "Coaching tips, mistakes & safety",
                         "ar": "نصائح التدريب والأخطاء الشائعة والسلامة"},
    "avoid":            {"en": "Avoid", "ar": "تجنّب"},
    "safety_label":     {"en": "Safety", "ar": "السلامة"},
    "prog_expander":    {"en": "Progression · Regression · Alternative",
                         "ar": "التدرج · التسهيل · البديل"},
    "progression":      {"en": "Progression", "ar": "التدرج (أصعب)"},
    "regression":       {"en": "Regression", "ar": "التسهيل (أسهل)"},
    "alternative":      {"en": "Alternative", "ar": "البديل"},
    "watch_youtube":    {"en": "▶ Watch demonstration on YouTube",
                         "ar": "▶ شاهد الشرح على يوتيوب"},
    "guidance_pic":     {"en": "Guidance picture", "ar": "صورة توضيحية"},
    "demo_gif":         {"en": "Demonstration GIF", "ar": "صورة متحركة توضيحية"},
    "target":           {"en": "Target", "ar": "العضلة المستهدفة"},
    "equipment":        {"en": "Equipment", "ar": "الأدوات"},
    "sets":             {"en": "Sets", "ar": "الجولات"},
    "reps":             {"en": "Reps", "ar": "التكرارات"},
    "tempo":            {"en": "Tempo", "ar": "الإيقاع"},
    "rest":             {"en": "Rest", "ar": "الراحة"},
    "rpe":              {"en": "RPE", "ar": "شدة الجهد RPE"},

    # cardio + summary
    "cardio_log":       {"en": "🚴 Cardio log", "ar": "🚴 سجل الكارديو"},
    "activity":         {"en": "Activity", "ar": "النشاط"},
    "minutes":          {"en": "Minutes", "ar": "الدقائق"},
    "log_cardio":       {"en": "➕ Log cardio", "ar": "➕ سجّل الكارديو"},
    "logged":           {"en": "Logged", "ar": "تم تسجيل"},
    "session_completion": {"en": "Session completion", "ar": "نسبة إكمال الجلسة"},
    "est_burn":         {"en": "Est. workout burn", "ar": "السعرات المقدّرة للتمرين"},
    "cardio_burn":      {"en": "Cardio burn today", "ar": "سعرات الكارديو اليوم"},

    # ---------------- program page ----------------
    "program_title":    {"en": "📅 Monthly Program", "ar": "📅 البرنامج الشهري"},
    "rest_day_caption": {"en": "Rest / no structured session.", "ar": "راحة / لا توجد جلسة منظمة."},
    "col_section":      {"en": "Section", "ar": "القسم"},
    "col_exercise":     {"en": "Exercise", "ar": "التمرين"},

    # ---------------- dashboard ----------------
    "dash_title":       {"en": "📈 Progress Dashboard", "ar": "📈 لوحة التقدم"},
    "exercises_done":   {"en": "Exercises done", "ar": "تمارين منجزة"},
    "volume_lifted":    {"en": "Volume lifted", "ar": "الحجم التدريبي"},
    "avg_completion":   {"en": "Avg completion", "ar": "متوسط الإكمال"},
    "workouts":         {"en": "Workouts", "ar": "جلسات التدريب"},
    "body_weight":      {"en": "Body weight", "ar": "وزن الجسم"},
    "since_start":      {"en": "since start", "ar": "منذ البداية"},
    "fatloss_pace":     {"en": "Fat-loss pace", "ar": "معدل خسارة الدهون"},
    "fatloss_help":     {"en": "Sustainable target while keeping muscle: −0.25 to −0.5 kg/week",
                         "ar": "الهدف المستدام مع الحفاظ على العضلات: −٠٫٢٥ إلى −٠٫٥ كجم/أسبوع"},
    "ch_daily_completion": {"en": "Daily completion %", "ar": "نسبة الإكمال اليومية %"},
    "ch_weekly_completion": {"en": "Weekly completion %", "ar": "نسبة الإكمال الأسبوعية %"},
    "ch_pain":          {"en": "Pain trend (session average, 0-10)",
                         "ar": "اتجاه الألم (متوسط الجلسة، ٠-١٠)"},
    "ch_weight":        {"en": "Body weight (kg)", "ar": "وزن الجسم (كجم)"},
    "ch_calories":      {"en": "Estimated calories burned / day",
                         "ar": "السعرات المقدّرة المحروقة / يوم"},
    "ch_cardio_min":    {"en": "Cardio minutes / week", "ar": "دقائق الكارديو / أسبوع"},
    "ch_steps":         {"en": "Daily steps", "ar": "الخطوات اليومية"},
    "ch_recovery":      {"en": "Recovery score (1–10)", "ar": "درجة الاستشفاء (١–١٠)"},
    "ch_sleep":         {"en": "Sleep (hours)", "ar": "النوم (ساعات)"},
    "ch_soreness":      {"en": "Muscle soreness (1–10)", "ar": "ألم العضلات (١–١٠)"},
    "ch_energy":        {"en": "Energy (1–10)", "ar": "الطاقة (١–١٠)"},
    "ch_football":      {"en": "Football performance (1–10)", "ar": "الأداء في كرة القدم (١–١٠)"},

    # ---------------- recovery ----------------
    "recovery_title":   {"en": "😴 Recovery Tracker", "ar": "😴 متابعة الاستشفاء"},
    "sleep_h":          {"en": "Sleep (hours)", "ar": "النوم (ساعات)"},
    "water_l":          {"en": "Water (litres)", "ar": "الماء (لتر)"},
    "protein_g":        {"en": "Protein (g)", "ar": "البروتين (جم)"},
    "protein_help":     {"en": "Target ≈1.6–2.0 g/kg → 115–145 g at 72 kg",
                         "ar": "الهدف ≈١٫٦–٢ جم/كجم → ١١٥–١٤٥ جم عند وزن ٧٢ كجم"},
    "steps":            {"en": "Steps", "ar": "الخطوات"},
    "soreness_s":       {"en": "Muscle soreness (1–10)", "ar": "ألم العضلات (١–١٠)"},
    "energy_s":         {"en": "Energy level (1–10)", "ar": "مستوى الطاقة (١–١٠)"},
    "recscore_s":       {"en": "Recovery score (1–10)", "ar": "درجة الاستشفاء (١–١٠)"},
    "recscore_help":    {"en": "Gut feeling: how ready is your body today?",
                         "ar": "إحساسك العام: ما مدى جاهزية جسمك اليوم؟"},
    "football_s":       {"en": "Football performance (1–10)", "ar": "الأداء في كرة القدم (١–١٠)"},
    "football_help":    {"en": "Rate Saturday's match; leave untouched other days",
                         "ar": "قيّم مباراة السبت؛ اتركه دون تغيير بقية الأيام"},
    "rec_notes_ph":     {"en": "Knee felt stable, shoulder quiet, slept badly…",
                         "ar": "الركبة مستقرة، الكتف هادئ، النوم كان سيئًا…"},
    "bw_kg":            {"en": "Body weight (kg)", "ar": "وزن الجسم (كجم)"},
    "save_recovery":    {"en": "💾 Save today's recovery", "ar": "💾 احفظ استشفاء اليوم"},
    "recovery_saved":   {"en": "Recovery saved ✔", "ar": "تم حفظ الاستشفاء ✔"},
    "readiness_warn":   {"en": "⚠️ High soreness or short sleep — consider reducing today's "
                                "loads by ~20% or swapping to the recovery protocol. Never "
                                "chase numbers on a bad-sleep day.",
                         "ar": "⚠️ ألم عضلي مرتفع أو نوم قليل — فكّر في تقليل أحمال اليوم "
                                "بنحو ٢٠٪ أو التبديل إلى بروتوكول الاستشفاء. لا تطارد الأرقام "
                                "في يوم نوم سيئ."},
    "rec_empty":        {"en": "Save a few days of recovery data to unlock the trends below.",
                         "ar": "احفظ بيانات بضعة أيام لعرض الاتجاهات أدناه."},

    # ---------------- edit mode ----------------
    "edit_title":       {"en": "✏️ Edit Mode", "ar": "✏️ وضع التعديل"},
    "edit_caption":     {"en": "Customise the program: add, delete, replace and edit exercises; "
                                "attach your own pictures, GIFs, videos and YouTube links. "
                                "Changes save to the local database and persist between sessions.",
                         "ar": "خصّص البرنامج: أضف واحذف واستبدل وعدّل التمارين؛ أرفق صورك "
                                "وصورك المتحركة وفيديوهاتك وروابط يوتيوب. تُحفظ التغييرات في "
                                "قاعدة البيانات المحلية وتبقى بين الجلسات."},
    "save_changes":     {"en": "💾 Save changes", "ar": "💾 احفظ التغييرات"},
    "delete_ex":        {"en": "🗑 Delete exercise", "ar": "🗑 احذف التمرين"},
    "replace_with":     {"en": "Replace with…", "ar": "استبدل بـ…"},
    "confirm_replace":  {"en": "↔ Confirm replace", "ar": "↔ تأكيد الاستبدال"},
    "add_exercise":     {"en": "➕ Add exercise", "ar": "➕ أضف تمرينًا"},
    "into_section":     {"en": "Into section", "ar": "إلى القسم"},
    "from_library":     {"en": "From library", "ar": "من المكتبة"},
    "add_btn":          {"en": "Add ✔", "ar": "أضف ✔"},
    "exec_notes":       {"en": "Execution / notes", "ar": "طريقة الأداء / ملاحظات"},
    "reset_options":    {"en": "🧨 Reset options", "ar": "🧨 خيارات إعادة الضبط"},
    "reset_warning":    {"en": "Resetting restores the generated program and discards your "
                                "edits (logs and history are NOT touched).",
                         "ar": "إعادة الضبط تستعيد البرنامج المولّد وتتجاهل تعديلاتك "
                                "(السجلات والتاريخ لا تتأثر)."},
    "reset_confirm":    {"en": "I understand — reset discards program edits",
                         "ar": "أفهم — إعادة الضبط تحذف تعديلات البرنامج"},
    "reset_day":        {"en": "Reset THIS day", "ar": "أعد ضبط هذا اليوم"},
    "reset_all":        {"en": "Reset ENTIRE program", "ar": "أعد ضبط البرنامج كاملًا"},
    "saved":            {"en": "Saved.", "ar": "تم الحفظ."},
    "no_sections":      {"en": "This day has no sections yet.", "ar": "لا توجد أقسام لهذا اليوم بعد."},
    "f_name":           {"en": "Exercise name", "ar": "اسم التمرين"},
    "f_target":         {"en": "Target muscle", "ar": "العضلة المستهدفة"},
    "f_purpose":        {"en": "Purpose", "ar": "الهدف"},
    "f_safety":         {"en": "Safety notes", "ar": "ملاحظات السلامة"},
    "f_image":          {"en": "Picture URL", "ar": "رابط الصورة"},
    "f_gif":            {"en": "GIF URL", "ar": "رابط الصورة المتحركة"},
    "f_video":          {"en": "Video URL (embedded)", "ar": "رابط الفيديو (مضمّن)"},
    "f_youtube":        {"en": "YouTube link", "ar": "رابط يوتيوب"},

    # ---------------- safety page ----------------
    "safety_title":     {"en": "🛟 Safety Guide", "ar": "🛟 دليل السلامة"},
    "traffic_header":   {"en": "The pain traffic light — applies to every exercise",
                         "ar": "إشارة الألم الضوئية — تنطبق على كل تمرين"},
    "pain_green":       {"en": "🟢 <b>Pain 0–2 / 10</b> — Continue training. Mild awareness "
                                "during rehab work is normal.",
                         "ar": "🟢 <b>ألم ٠–٢ / ١٠</b> — استمر في التدريب. الإحساس الخفيف أثناء "
                                "تمارين التأهيل أمر طبيعي."},
    "pain_yellow":      {"en": "🟡 <b>Pain 3–4 / 10</b> — Reduce the weight, slow the speed, or "
                                "shrink the range of motion. Re-test — if it drops to ≤2, continue.",
                         "ar": "🟡 <b>ألم ٣–٤ / ١٠</b> — قلّل الوزن أو أبطئ السرعة أو صغّر مدى "
                                "الحركة. أعد المحاولة — إذا انخفض إلى ≤٢ فاستمر."},
    "pain_red":         {"en": "🔴 <b>Pain 5+ / 10</b> — <b>Stop the exercise.</b> Swap to a "
                                "pain-free alternative or end the block. If it repeats across "
                                "sessions, get reassessed by your physiotherapist.",
                         "ar": "🔴 <b>ألم ٥+ / ١٠</b> — <b>أوقف التمرين.</b> بدّل إلى بديل خالٍ من "
                                "الألم أو أنهِ هذا الجزء. إذا تكرر عبر الجلسات فاطلب إعادة تقييم "
                                "من أخصائي العلاج الطبيعي."},
    "traffic_caption":  {"en": "This rule applies to every exercise, every day. Sharp pain, joint "
                                "swelling, or the knee/shoulder feeling 'loose' override "
                                "everything — stop and reassess.",
                         "ar": "تنطبق هذه القاعدة على كل تمرين وكل يوم. الألم الحاد أو تورم "
                                "المفصل أو إحساس الركبة/الكتف بأنها «غير ثابتة» يتجاوز كل شيء — "
                                "توقف وأعد التقييم."},
    "knee_header":      {"en": "Knee (partial ACL) rules", "ar": "قواعد الركبة (قطع جزئي في الرباط الصليبي)"},
    "knee_md":          {"en": """
- **Green-light feelings:** muscle burn, fatigue, mild pressure that fades within minutes.
- **Stop signs:** sharp pain, the knee feeling *loose* or giving way, catching/locking, or **any swelling** the next morning — skip hops/deep loading and reassess.
- **Hops & landings (Weeks 3–4):** only pain-free, only fresh, and **never the day before football**.
- **Depth is a dial, not a badge** — squat/lunge to the depth you control with the knee tracking over the toes.
- Slow eccentrics (3–5 s lowering) are the safest, most productive stimulus for ligament and tendon remodelling.
""",
                         "ar": """
- **أحاسيس مسموح بها:** حرقان العضلات، التعب، ضغط خفيف يزول خلال دقائق.
- **علامات التوقف:** ألم حاد، إحساس الركبة بأنها *غير ثابتة* أو خيانتها لك، قفل/فرقعة، أو **أي تورم** في صباح اليوم التالي — أوقف القفزات والأحمال العميقة وأعد التقييم.
- **القفزات والهبوط (الأسبوعان ٣–٤):** فقط دون ألم، فقط وأنت نشيط، و**أبدًا في اليوم السابق لكرة القدم**.
- **العمق قابل للتعديل وليس وسام شرف** — انزل في السكوات/الاندفاع إلى العمق الذي تتحكم فيه مع بقاء الركبة فوق أصابع القدم.
- الإطالات البطيئة (نزول ٣–٥ ثوانٍ) هي المحفّز الأكثر أمانًا وفائدة لإعادة بناء الأربطة والأوتار.
"""},
    "shoulder_header":  {"en": "Shoulder (post-dislocation, suspected labral injury) rules",
                         "ar": "قواعد الكتف (بعد الخلع، اشتباه إصابة الشفا المفصلي)"},
    "shoulder_md":      {"en": """
- **The danger zone** is the cocked-back throwing position (arm out + rotated back). This month avoids loading it: floor presses cap the range, presses travel on a diagonal, the doorway stretch stays low and gentle.
- **Apprehension** (the *"it might pop"* feeling) is an immediate stop signal — it outranks pain.
- The **90/90 band work in Weeks 3–4 is gated**: only if Weeks 1–2 cuff work was 100% pain-free.
- Rowing, carries and cuff work are your shoulder's best friends — be as consistent with the small band exercises as with the big lifts.
- No barbell bench press, behind-the-neck anything, or max-effort throwing this month.
""",
                         "ar": """
- **منطقة الخطر** هي وضعية الرمي مع الذراع للخلف (الذراع مرفوعة + مدورة للخلف). هذا الشهر يتجنب تحميلها: الضغط الأرضي يحدّ المدى، والضغط يسير على خط مائل، وإطالة الصدر تبقى منخفضة ولطيفة.
- **إحساس الخوف من الخلع** (شعور *«قد تنخلع»*) إشارة توقف فورية — وهو أهم من الألم نفسه.
- تمارين **90/90 بالمطاط في الأسبوعين ٣–٤ مشروطة**: فقط إذا كانت تمارين الكفة المدورة في الأسبوعين ١–٢ خالية تمامًا من الألم.
- التجديف والحمل وتمارين الكفة المدورة أفضل أصدقاء كتفك — واظب على تمارين المطاط الصغيرة كمواظبتك على الرفعات الكبيرة.
- لا ضغط بار على البنش، ولا أي تمرين خلف الرقبة، ولا رمي بأقصى جهد هذا الشهر.
"""},
    "reassess_header":  {"en": "Get reassessed by a professional if",
                         "ar": "اطلب إعادة تقييم من مختص إذا"},
    "reassess_md":      {"en": """
- Pain ≥5/10 appears in the same exercise across **two or more sessions**
- The knee **swells** after sessions or **gives way** at any point
- The shoulder **subluxes** ("slips") even slightly, or night pain appears
- Numbness, tingling, or weakness radiates down the arm or leg
""",
                         "ar": """
- ظهر ألم ≥٥/١٠ في نفس التمرين عبر **جلستين أو أكثر**
- **تورمت** الركبة بعد الجلسات أو **خانتك** في أي لحظة
- **انزلق** الكتف ولو قليلًا، أو ظهر ألم ليلي
- امتد خدر أو تنميل أو ضعف إلى الذراع أو الساق
"""},
    "load_header":      {"en": "Weekly load rules", "ar": "قواعد الحمل الأسبوعي"},
    "load_md":          {"en": """
- Progress **one dial at a time**: load *or* range *or* speed — never all three in a week.
- After football: Sunday is mobility only. Heavy hamstring work (Nordics) never lands within 48 h of a match.
- Bad sleep (<6 h) or soreness ≥7/10 → cut today's loads ~20% or take the recovery protocol instead. The plan bends so you don't break.
""",
                         "ar": """
- تقدّم **بعامل واحد في كل مرة**: الحمل *أو* المدى *أو* السرعة — وليس الثلاثة معًا في أسبوع واحد.
- بعد كرة القدم: الأحد للمرونة فقط. تمارين أوتار الركبة الثقيلة (النورديك) لا تقع أبدًا خلال ٤٨ ساعة من المباراة.
- نوم سيئ (<٦ ساعات) أو ألم عضلي ≥٧/١٠ ← قلّل أحمال اليوم بنحو ٢٠٪ أو نفّذ بروتوكول الاستشفاء بدلًا منها. الخطة تنحني كي لا تنكسر أنت.
"""},

    # ---------------- settings ----------------
    "settings_title":   {"en": "⚙️ Settings", "ar": "⚙️ الإعدادات"},
    "program_calendar": {"en": "Program calendar", "ar": "تقويم البرنامج"},
    "start_date_label": {"en": "Program start date (Week 1 Monday)",
                         "ar": "تاريخ بداية البرنامج (اثنين الأسبوع الأول)"},
    "start_date_help":  {"en": "'Today's Workout' maps the calendar onto program weeks from "
                                "this date. It defaults to this week's Monday.",
                         "ar": "«تمرين اليوم» يربط التقويم بأسابيع البرنامج بدءًا من هذا "
                                "التاريخ. الافتراضي هو يوم الاثنين من هذا الأسبوع."},
    "start_date_set":   {"en": "Start date updated. Week/day now auto-select from it.",
                         "ar": "تم تحديث تاريخ البداية. سيُحدَّد الأسبوع واليوم تلقائيًا منه."},
    "profile":          {"en": "Profile", "ar": "الملف الشخصي"},
    "current_bw":       {"en": "Current body weight (kg)", "ar": "وزن الجسم الحالي (كجم)"},
    "save_weight":      {"en": "Save weight to profile & today's log",
                         "ar": "احفظ الوزن في الملف وسجل اليوم"},
    "profile_line":     {"en": "Profile: male · 34 y · 168 cm · football (weekend) · "
                                "intermediate · partial ACL tear + right shoulder "
                                "post-dislocation (conservative management, cleared to train).",
                         "ar": "الملف: ذكر · ٣٤ سنة · ١٦٨ سم · كرة قدم (نهاية الأسبوع) · مستوى "
                                "متوسط · قطع جزئي في الرباط الصليبي الأمامي + خلع سابق في الكتف "
                                "الأيمن (علاج تحفظي، مسموح بالتدريب)."},
    "appearance":       {"en": "Appearance", "ar": "المظهر"},
    "appearance_note":  {"en": "The app uses one fixed theme: the energetic, motivation-focused "
                                "gym look — bold orange on a warm light background, designed to "
                                "keep you fired up during training.",
                         "ar": "يستخدم التطبيق مظهرًا واحدًا ثابتًا: المظهر التحفيزي الرياضي — "
                                "برتقالي جريء على خلفية فاتحة دافئة، مصمم ليبقيك متحمسًا أثناء "
                                "التدريب."},
    # next training block
    "nb_header":        {"en": "🔄 Next Training Block", "ar": "🔄 البرنامج التدريبي التالي"},
    "nb_caption":       {"en": "When Week 4's tests are logged, generate the next 4-week "
                                "block automatically: same split, rep schemes shifted one gear "
                                "toward strength, and a personalised suggested start load "
                                "stamped on every exercise you logged a weight for.",
                         "ar": "بعد تسجيل اختبارات الأسبوع الرابع، وَلِّد البرنامج التالي "
                                "(٤ أسابيع) تلقائيًا: نفس التقسيم مع نقل التكرارات درجة نحو "
                                "القوة، ووزن بداية مقترح مخصص لكل تمرين سجلت له وزنًا."},
    "nb_current":       {"en": "Current block", "ar": "البرنامج الحالي"},
    "nb_tests_header":  {"en": "🏁 Your latest benchmark results", "ar": "🏁 أحدث نتائج اختباراتك"},
    "nb_no_tests":      {"en": "No benchmark tests logged yet — finish Week 4's assessment "
                                "days first (you can still generate, but the report will "
                                "have no test recap).",
                         "ar": "لا توجد اختبارات مسجلة بعد — أكمل أيام التقييم في الأسبوع "
                                "الرابع أولًا (يمكنك التوليد الآن لكن دون ملخص اختبارات)."},
    "nb_confirm":       {"en": "I understand — this replaces the current program (history "
                                "and logs are kept)",
                         "ar": "أفهم — سيستبدل هذا البرنامج الحالي (السجل والتاريخ محفوظان)"},
    "nb_generate":      {"en": "⚡ Generate next block", "ar": "⚡ ولِّد البرنامج التالي"},
    "nb_done":          {"en": "Block {block} generated! It starts Monday {start}.",
                         "ar": "تم توليد البرنامج رقم {block}! يبدأ يوم الاثنين {start}."},
    "nb_m_sugg":        {"en": "Load suggestions added", "ar": "اقتراحات أوزان أضيفت"},
    "nb_m_shift":       {"en": "Rep schemes shifted", "ar": "أنظمة تكرارات نُقلت"},
    "nb_m_pain":        {"en": "Avg pain (14 d)", "ar": "متوسط الألم (١٤ يومًا)"},
    "nb_conservative":  {"en": "⚠️ Recent pain averaged ≥3/10 — all load suggestions were "
                                "kept conservative (−10%). Re-test pain-free before pushing.",
                         "ar": "⚠️ متوسط الألم الأخير ≥٣/١٠ — أوزان البداية المقترحة "
                                "متحفظة (−١٠٪). عُد للاختبار بلا ألم قبل الزيادة."},
    "nb_next_steps":    {"en": "Open Today's Workout — each exercise now shows its suggested "
                                "start load in the 'Why this exercise' text.",
                         "ar": "افتح تمرين اليوم — كل تمرين يعرض الآن وزن البداية المقترح "
                                "ضمن نص «لماذا هذا التمرين»."},

    "export":           {"en": "Export data", "ar": "تصدير البيانات"},
    "export_note":      {"en": "Everything is stored locally in `gym_rehab.db` (SQLite) next to "
                                "the app — nothing leaves your machine.",
                         "ar": "كل شيء محفوظ محليًا في ملف `gym_rehab.db` (SQLite) بجوار "
                                "التطبيق — لا شيء يغادر جهازك."},
    "dl_workouts":      {"en": "Workout history", "ar": "سجل التمارين"},
    "dl_recovery":      {"en": "Recovery history", "ar": "سجل الاستشفاء"},
    "dl_weight":        {"en": "Body weight", "ar": "وزن الجسم"},
    "dl_cardio":        {"en": "Cardio log", "ar": "سجل الكارديو"},
}

# -------------------------------------------------------------------------
# Display translations for program metadata (DB keeps English keys)
# -------------------------------------------------------------------------
DAY_AR = {
    "Monday": "الاثنين", "Tuesday": "الثلاثاء", "Wednesday": "الأربعاء",
    "Thursday": "الخميس", "Friday": "الجمعة", "Saturday": "السبت",
    "Sunday": "الأحد",
}

DAY_FOCUS_AR = {
    "Monday":    "يوم الصدر — ضغط وتفتيح وترايسبس",
    "Tuesday":   "يوم الأرجل — رباعية وأوتار ومقعدة وسمانة",
    "Wednesday": "يوم الظهر — عقلة وسحب وتجديف وبايسبس",
    "Thursday":  "يوم الأكتاف — دالية وترابيس وكفة مدورة",
    "Friday":    "يوم استشفاء",
    "Saturday":  "يوم مباراة كرة القدم",
    "Sunday":    "استشفاء + مرونة",
}

WEEK_THEMES_AR = {
    1: ("التحميل",
        "يبدأ تقسيم عضلة لكل يوم: صدر، أرجل، ظهر، أكتاف — دمبل وأجهزة "
        "فقط. الأوزان أخف بدرجة (RPE 7) بينما تحدد وزن عملك على كل "
        "جهاز — سجّلها كلها في المتابعة."),
    2: ("زيادة الحمل",
        "نفس التقسيم بأوزان أثقل (RPE 7-8). يدخل دفع الأرجل برجل واحدة "
        "والرفعة الرومانية الثقيلة بالدمبل في يوم الأرجل. أضف وزنًا حيث "
        "كانت الجولة الأخيرة سلسة."),
    3: ("الشدة",
        "أسبوع الذروة (RPE 8): أثقل أوزان البرنامج، أعلى صناديق القفز "
        "ووثبات المتزلج في يوم الأرجل. الجودة تحكم كل شيء — تمارين "
        "القوة تتوقف لحظة تباطؤ التكرارات."),
    4: ("الذروة + إعادة الاختبار",
        "الحجم ينخفض وتُجرى الاختبارات موزعة على التقسيم: أقصى ضغط "
        "(يوم الصدر)، ثبات الحائط والسمانة واتزان Y والقفز برجل واحدة "
        "(يوم الأرجل)، أقصى عقلات متقنة (يوم الظهر)، وأقصى بلانك (يوم "
        "الأكتاف). تفوّق على أرقامك السابقة."),
}

SECTION_AR = {
    "Warm-Up": "الإحماء",
    "Mobility": "المرونة",
    "Activation": "التنشيط",
    "Strength": "القوة",
    "Strength (moderate — testing week)": "القوة (متوسطة — أسبوع الاختبارات)",
    "Strength (variation)": "القوة (تنويع)",
    "Rehabilitation": "التأهيل",
    "Shoulder Rehabilitation": "تأهيل الكتف",
    "Core": "الجذع",
    "Balance": "التوازن",
    "Conditioning": "اللياقة",
    "Conditioning (Football Prep)": "اللياقة (تحضير كرة القدم)",
    "Cool-Down & Stretch": "التهدئة والإطالة",
    "Functional Finisher": "الختام الوظيفي",
    "Landing Mechanics (fresh — before strength)": "ميكانيكا الهبوط (وأنت نشيط — قبل القوة)",
    "Landing Mechanics (fresh)": "ميكانيكا الهبوط (وأنت نشيط)",
    "Assessment": "التقييم",
    "Power & Plyometrics (fresh)": "القوة الانفجارية والبلايومتركس (وأنت نشيط)",
    "Speed (fresh)": "السرعة (وأنت نشيط)",
    "Assessment Battery (fresh + fully warm)": "مجموعة الاختبارات (نشيط + إحماء كامل)",
    "Light Functional Work (after tests)": "عمل وظيفي خفيف (بعد الاختبارات)",
    "Soft Tissue & Mobility": "الأنسجة الرخوة والمرونة",
    "Keep-The-Knee-Awake (pain-free, light)": "إبقاء الركبة نشطة (خفيف، بلا ألم)",
    "Optional Easy Movement": "حركة خفيفة اختيارية",
    "Downshift": "التهدئة العصبية",
    "Pre-Match Activation (15 min before kickoff warm-up)": "تنشيط ما قبل المباراة (قبل الإحماء بـ١٥ دقيقة)",
    "Post-Match Reset (within 30 min of full-time)": "استعادة ما بعد المباراة (خلال ٣٠ دقيقة من النهاية)",
    "Gentle Cardio Flush": "كارديو خفيف منشّط للدورة الدموية",
    "Full-Body Mobility Flow": "تدفق مرونة لكامل الجسم",
    "Long Stretch Series": "سلسلة الإطالات الطويلة",
    "Soft Tissue + Downshift": "الأنسجة الرخوة + التهدئة",
}

EXERCISE_NAME_AR = {
    "bike_warmup": "دراجة ثابتة — دوران خفيف",
    "cardio_warmup_20": "إحماء كارديو — ٢٠ دقيقة دراجة أو جري خفيف",
    "brisk_march": "مشية ديناميكية + هرولة خفيفة في المكان",
    "leg_swings": "أرجحة الرجل للأمام والخلف",
    "lateral_leg_swings": "أرجحة الرجل الجانبية",
    "worlds_greatest": "أعظم إطالة في العالم",
    "cat_cow": "القطة والجمل",
    "open_book": "الكتاب المفتوح لدوران الصدر",
    "ankle_rocks": "تحريك الكاحل — الركبة إلى الحائط",
    "glute_bridge": "جسر المقعدة",
    "single_leg_bridge": "جسر المقعدة برجل واحدة",
    "clamshell": "الصدفة بالمطاط",
    "side_leg_raise": "رفع الرجل جانبيًا (استلقاء جانبي)",
    "band_walk": "المشي الجانبي بالمطاط",
    "monster_walk": "مشية الوحش (مشي قطري بالمطاط)",
    "quad_set_ssq": "شد الرباعية الثابت",
    "deadbug": "الحشرة الميتة",
    "bird_dog": "الطائر والكلب",
    "scap_pushup": "ضغط لوح الكتف",
    "band_pull_apart": "شد المطاط للخلف",
    "wall_slide": "انزلاق الساعدين على الحائط",
    "box_squat": "سكوات إلى الصندوق",
    "goblet_squat": "سكوات الكأس",
    "tempo_goblet_squat": "سكوات الكأس البطيء (نزول ٥ ثوانٍ)",
    "spanish_squat": "السكوات الإسباني (مطاط خلف الركبتين)",
    "wall_sit": "الجلسة على الحائط",
    "split_squat": "سكوات الانفراج",
    "rfe_split_squat": "سكوات بلغاري (القدم الخلفية مرفوعة)",
    "reverse_lunge": "الاندفاع للخلف",
    "lateral_lunge": "الاندفاع الجانبي",
    "step_up": "الصعود على الصندوق بالدمبل",
    "lateral_step_up": "الصعود الجانبي على الصندوق",
    "tke": "مد الركبة النهائي بالمطاط",
    "romanian_deadlift": "الرفعة الرومانية بالدمبل",
    "single_leg_rdl": "الرفعة الرومانية برجل واحدة",
    "slider_curl": "ثني أوتار الركبة بالمنزلقات",
    "nordic_curl": "النزول النوردي لأوتار الركبة",
    "hip_thrust": "دفع الورك بالدمبل",
    "single_leg_hip_thrust": "دفع الورك برجل واحدة",
    "bridge_march": "مشية الجسر",
    "calf_raise_double": "رفع السمانة واقفًا (حافة درجة)",
    "calf_raise_single": "رفع السمانة برجل واحدة",
    "soleus_raise": "رفع السمانة بركبة مثنية (النعلية)",
    "eccentric_calf": "إنزال الكعب البطيء",
    "iso_er_wall": "دوران خارجي ثابت ضد الحائط",
    "band_er": "دوران خارجي بالمطاط (المرفق ملاصق)",
    "band_ir": "دوران داخلي بالمطاط",
    "band_er_90": "دوران خارجي بالمطاط وضعية 90/90",
    "face_pull": "السحب للوجه بالمطاط",
    "scaption_raise": "رفع الذراعين بمستوى لوح الكتف (الإبهام لأعلى)",
    "prone_ytw": "حروف Y-T-W منبطحًا",
    "db_row": "تجديف الدمبل بذراع واحدة",
    "band_row": "التجديف جالسًا بالمطاط",
    "floor_press": "الضغط الأرضي بالدمبل",
    "incline_pushup": "الضغط المائل",
    "pushup": "الضغط الكامل",
    "landmine_press": "الضغط المائل نصف راكع",
    "banded_pulldown": "السحب لأسفل بالمطاط راكعًا",
    "farmer_carry": "حمل المزارع",
    "suitcase_carry": "حمل الحقيبة (ذراع واحدة)",
    "plank": "البلانك الأمامي",
    "plank_tap": "لمس الكتف من البلانك",
    "side_plank": "البلانك الجانبي",
    "side_plank_leglift": "البلانك الجانبي مع رفع الرجل",
    "pallof_press": "ضغط بالوف",
    "copenhagen": "بلانك كوبنهاجن للضامة (ذراع قصيرة)",
    "sl_balance": "التوازن على رجل واحدة",
    "sl_balance_perturb": "توازن رجل واحدة + رمي كرة / التفات الرأس",
    "sl_reach": "مد النجمة على رجل واحدة (اتزان Y)",
    "hop_stick": "القفز والتثبيت (للأمام)",
    "lateral_hop_stick": "القفز الجانبي والتثبيت",
    "bike_intervals": "فترات الدراجة 30/30",
    "bike_tempo": "دراجة بإيقاع ثابت",
    "incline_walk": "مشي سريع على منحدر",
    "shadow_footwork": "حركة قدمين كروية منخفضة الصدمة",
    "stretch_quad": "إطالة الرباعية واقفًا",
    "stretch_hamstring": "إطالة أوتار الركبة واقفًا",
    "stretch_hip_flexor": "إطالة عاطفات الورك نصف راكع",
    "stretch_glute": "إطالة المقعدة (شكل ٤)",
    "stretch_calf": "إطالة السمانة على الحائط",
    "stretch_chest": "إطالة الصدر على إطار الباب",
    "cross_body_stretch": "إطالة خلفية الكتف عبر الجسم",
    "foam_roll_quads": "الأسطوانة الإسفنجية — رباعية / سمانة / مقعدة",
    "breathing_reset": "إعادة ضبط التنفس الحجابي",
    "assess_wall_sit": "اختبار — أقصى ثبات على الحائط",
    "assess_sl_calf": "اختبار — أقصى تكرارات سمانة برجل واحدة",
    "assess_sl_hop": "اختبار — القفز لمسافة برجل واحدة",
    "assess_y_balance": "اختبار — أفضل مدى في اتزان Y",
    "assess_plank": "اختبار — أقصى ثبات بلانك",
    # ------- gym (weighted) exercises -------
    "leg_press": "دفع الأرجل (جهاز)",
    "leg_extension": "مد الرجلين (جهاز، مدى متحكم به)",
    "leg_curl_machine": "ثني الرجلين جالسًا (جهاز)",
    "barbell_rdl": "الرفعة الرومانية بالبار",
    "trap_bar_deadlift": "الرفعة الميتة بالبار السداسي",
    "barbell_hip_thrust": "دفع الورك بالبار",
    "back_extension_45": "مد الظهر ٤٥° (تركيز المقعدة)",
    "smith_calf": "رفع السمانة واقفًا (سميث / جهاز)",
    "seated_calf_machine": "رفع السمانة جالسًا (جهاز)",
    "adductor_machine": "جهاز تقريب الفخذين (الضامة)",
    "abductor_machine": "جهاز تبعيد الفخذين",
    "lat_pulldown_machine": "السحب العلوي بالكابل (قبضة متعادلة)",
    "seated_cable_row": "التجديف جالسًا بالكابل",
    "db_bench": "ضغط الدمبل على البنش (قبضة متعادلة، عمق محدود)",
    "chest_press_machine": "جهاز ضغط الصدر",
    "cable_face_pull": "السحب للوجه بالكابل (حبل)",
    "cable_er": "دوران خارجي بالكابل (المرفق ملاصق)",
    "rear_delt_fly": "الرفرفة الخلفية (جهاز بيك-دك عكسي)",
    "cable_pallof": "ضغط بالوف بالكابل",
    # ------- advanced block -------
    "front_squat": "السكوات الأمامي (قبضة متقاطعة أو أحزمة)",
    "hack_squat": "هاك سكوات (جهاز)",
    "single_leg_press": "دفع الأرجل برجل واحدة",
    "walking_lunge": "الاندفاع مشيًا بالدمبل",
    "db_shoulder_press": "ضغط الكتف بالدمبل جالسًا (قبضة متعادلة)",
    "lateral_raise": "الرفرفة الجانبية بالدمبل",
    "incline_db_press": "ضغط الدمبل المائل المنخفض (١٥-٣٠°)",
    "pullup": "العقلة / عقلة بمساعدة (قبضة متعادلة)",
    "barbell_row": "التجديف بالبار منحنيًا",
    "box_jump": "القفز على الصندوق (النزول مشيًا)",
    "skater_bound": "وثبة المتزلج الجانبية مع التثبيت",
    "sprint_strides": "انطلاقات العدو التدريجية (~٨٥٪)",
    # ------- split-routine additions -------
    "pec_deck": "تفتيح الصدر (جهاز بيك-دك)",
    "chest_supported_row": "تجديف الدمبل بدعم الصدر",
    "db_curl": "ثني العضلة ذات الرأسين بالدمبل (بالتناوب)",
    "triceps_pushdown": "دفع الترايسبس بالكابل (حبل)",
    "db_shrug": "هز الكتفين بالدمبل",
}


# -------------------------------------------------------------------------
# Helpers
# -------------------------------------------------------------------------
# -------------------------------------------------------------------------
# Daily motivation — one quote per day, rotating (both languages)
# -------------------------------------------------------------------------
QUOTES = {
    "en": [
        "The comeback is always stronger than the setback.",
        "You don't have to be extreme — just consistent.",
        "Strong knees, strong shoulders, strong season.",
        "Every rep today is a tackle you win on Saturday.",
        "Discipline beats motivation — today you have both.",
        "Rehab IS training. Train it like a final.",
        "Small weights now, big future later.",
        "Champions are built on the days nobody is watching.",
        "Slow is smooth, and smooth is strong.",
        "One quality rep beats ten sloppy ones.",
        "Protect the knee. Power the game.",
        "Show up. The streak takes care of the rest.",
    ],
    "ar": [
        "العودة دائمًا أقوى من الكبوة.",
        "لست بحاجة لأن تكون متطرفًا — فقط كن مستمرًا.",
        "ركبة قوية، كتف قوي، موسم قوي.",
        "كل تكرار اليوم هو التحام تكسبه يوم السبت.",
        "الانضباط يتفوق على الحماس — واليوم لديك الاثنان.",
        "التأهيل تدريبٌ حقيقي. تدرّب كأنه نهائي.",
        "أوزان صغيرة الآن، مستقبل كبير لاحقًا.",
        "الأبطال يُصنعون في الأيام التي لا يراقبك فيها أحد.",
        "البطء إتقان، والإتقان قوة.",
        "تكرار واحد متقن خيرٌ من عشرة مهملة.",
        "احمِ الركبة، واصنع اللعب.",
        "احضر فقط — والاستمرارية تتكفل بالباقي.",
    ],
}


def daily_quote(lang: str, day_index: int) -> str:
    """Rotating motivational quote — same quote all day, new one tomorrow."""
    qs = QUOTES.get(lang, QUOTES["en"])
    return qs[day_index % len(qs)]


def tr(key: str, lang: str) -> str:
    """UI string in the active language (falls back to English)."""
    entry = UI.get(key)
    if not entry:
        return key
    return entry.get(lang, entry["en"])


def day_label(day: str, lang: str) -> str:
    return DAY_AR.get(day, day) if lang == "ar" else day


def section_label(name: str, lang: str) -> str:
    return SECTION_AR.get(name, name) if lang == "ar" else name


def focus_label(day: str, default: str, lang: str) -> str:
    return DAY_FOCUS_AR.get(day, default) if lang == "ar" else default


def week_theme(week: int, lang: str, en_themes: dict):
    return WEEK_THEMES_AR[week] if lang == "ar" else en_themes[week]


def exercise_label(ex: dict, lang: str) -> str:
    """Translated display name; DB keys stay English."""
    if lang == "ar":
        ar = EXERCISE_NAME_AR.get(ex.get("id", ""))
        if ar:
            return ar
    return ex["name"]
