"use strict";

/* ============================== state ================================== */

let chapters = [];
let state = { chapter: 0, step: { kind: "lesson", idx: 0 } };
let progress = loadProgress();
let sidebarEntranceShown = false;

const $ = (id) => document.getElementById(id);
const STORE_KEY = "pytutor-progress-v1";
const NAME_KEY = "pytutor-name-v1";
const LANG_KEY = "pytutor-lang-v1";

/* ============================ language ================================= */

/* UI language — "en" or "fa".  The saved choice is restored in an inline
   <head> script (so direction is right before first paint); app.js reads
   the <html lang> attribute the same script set, so both stay in sync. */

function currentLang() {
  return document.documentElement.lang === "fa" ? "fa" : "en";
}
let lang = currentLang();

const STR = {
  en: {
    doc_title: "🐍 Python Tutor — Learn Python 3.14",
    brand_name: "Python Tutor",
    brand_sub: "from the official Python 3.14 docs",
    welcome_sub: "Learn Python 3.14 from the official tutorial — at your own " +
      "pace. Read the lessons, study the diagrams, then prove your " +
      "knowledge with real quiz questions.",
    name_label: "First, tell me your name:",
    name_placeholder: "e.g. Ada",
    start_btn: "Start learning",
    welcome_hint: "press Enter to continue",
    change_name: "✏️ Change name",
    progress_label: "Progress",
    progress_text: "{answered} of {total} questions · {done} of {chapters} chapters",
    greeting: "👋 Welcome, {name}!",
    greeting_anon: "👋 Welcome!",
    cat_tutorial: "Tutorial",
    cat_using: "Using Python",
    cat_library: "Library Reference",
    cat_howto: "HowTo",
    cat_reference: "Language Reference",
    cat_c_foundations: "Foundations",
    cat_c_memory: "Memory & Data",
    cat_c_programs: "Program Building",
    cat_c_deep: "Deep C",
    cat_c_system: "System & Modern",
    cat_c_modern: "Standards & Beyond",
    cat_h_basics: "HTML Basics",
    cat_h_structure: "Structure & Tables",
    cat_h_forms: "Forms & Attributes",
    cat_h_advanced: "Accessibility & Advanced",
    cat_s_fundamentals: "Fundamentals",
    cat_s_values: "Values & Boxes",
    cat_s_typography: "Typography",
    cat_s_layout: "Layout",
    cat_s_responsive: "Responsive",
    cat_s_modern: "Modern CSS",
    cat_s_effects: "Visual Effects",
    cat_s_advanced: "Advanced",
    cat_s_pro: "Professional",
    cat_j_fundamentals: "Fundamentals",
    cat_j_flow: "Control Flow",
    cat_j_functions: "Functions",
    cat_j_data: "Arrays & Objects",
    cat_j_advanced: "Advanced JS",
    cat_j_builtin: "Built-in Objects",
    cat_j_async: "Async JavaScript",
    cat_j_modules: "Modules",
    cat_j_browser: "Browser JS",
    cat_j_topics: "Advanced Topics",
    cat_p_basics: "C++ Basics",
    cat_p_scope: "Scope & Pointers",
    cat_p_oop: "OOP & Classes",
    cat_p_raii: "RAII & Memory",
    cat_p_stl: "STL",
    cat_p_modern: "Modern C++",
    cat_p_cpp23: "C++20/23 Features",
    cat_p_pro: "Professional C++",
    chapter_complete: "🎉 Chapter {num} complete, {name}!",
    finish_toast: "🏁 You finished the whole course, {name}! 🎉",
    welcome_back: "👋 Welcome back, {name}!",
    welcome_toast: "🎉 Welcome, {name}! Ready to learn Python?",
    breadcrumb: "Chapter {ch} · Lesson {lesson} of {of}",
    btn_prev: "← Previous",
    btn_next_lesson: "Next lesson →",
    btn_take_quiz: "Take the quiz →",
    btn_next_chapter: "Next chapter →",
    btn_finish: "Finish 🏁",
    btn_back_lessons: "← Back to lessons",
    copy_code: "Copy",
    copied_code: "Copied!",
    chips_label: "Programming language",
    read_time: "⏱ {min} min read",
    read_progress: "📖 {read} of {total} lessons read",
    search_ph: "Search lessons…",
    diff_beg: "Beginner",
    diff_int: "Intermediate",
    diff_adv: "Advanced",
    zen_title: "Focus mode (F)",
    zen_toast: "Focus mode — press F or ✕ to exit",
    bookmark_add: "Bookmark this lesson",
    bookmark_remove: "Remove bookmark",
    bookmarks: "Bookmarks",
    update_msg: "A new version is available!",
    update_btn: "Update",
    bn_menu: "Menu",
    bn_search: "Search",
    bn_saved: "Saved",
    bn_focus: "Focus",
    bn_lang: "Language",
    compare_title: "Compare across languages",
    pal_ph: "Search lessons or type a command…",
    pal_commands: "Commands",
    share_lesson: "Share this lesson",
    share_text: "Check out this lesson on PLT:",
    link_copied: "Lesson link copied ✓",
    tryit_label: "💻 Try it yourself — write Python and run it:",
    run: "▶ Run",
    running: "Running…",
    engine_loading: "⏳ Loading the in-browser Python engine (first run only — " +
      "about 10 MB, then cached)…",
    no_output: "(no output)",
    engine_fail: "Couldn't load the in-browser Python engine ({err}). Check " +
      "your internet connection and press Run again.",
    engine_timeout: "Timed out after {sec}s — the code may be stuck in an " +
      "infinite loop or waiting for input().",
    server_unreachable: "Could not reach the app server.",
    quiz_header: "Chapter Quiz",
    quiz_intro1: "{title} — answer every question to complete the chapter. " +
      "Questions come in four flavours: multiple choice, fill the blank, " +
      "order the lines, and write the code.",
    quiz_intro2: "Good luck, {name}! 🤞",
    quiz_done_banner: "✔ Chapter complete — great job, {name}!",
    q_label: "Q{n}.",
    check_btn: "Check",
    correct: "✅ Correct, {name}!",
    wrong: "❌ Not quite, {name}.",
    answer_label: "Answer:",
    show_answer: "Show answer",
    pick_option: "Pick an option first",
    pick_lines: "Pick all {n} lines first",
    blank_placeholder: "type your answer",
    hint_prefix: "hint: ",
    order_instruction: "Click the lines in the correct order.",
    status_all: "✅ All {n} questions answered — review your answers above, " +
      "then continue whenever you're ready.",
    status_partial: "{answered} of {total} questions answered so far.",
    load_error_title: "Could not load course content",
    load_error_body: "The course data file (<code>data.js</code>) was not " +
      "found next to <code>app.js</code>. Regenerate it with " +
      "<code>python build_static.py</code> and redeploy.",
    lang_aria: "Language",
    quiz_label: "Quiz",
    playground_btn: "🧪 Playground",
    playground_blocked: "Popup blocked — allow popups for this site to " +
      "open the playground window.",
    subject_title: "What do you want to learn?",
    subject_sub: "Pick a language — hover the circles to preview it in the " +
      "big one, click to choose.",
    subject_hint: "more tutors are on the way 🚧",
    start_with: "Start learning {name}",
    continue_with: "Continue with {name}",
    coming_soon_btn: "{name} — coming soon",
    coming_soon_tag: "under construction 🚧",
    ready_tag: "{chapters} chapters · {questions} questions · ready now",
    soon_toast: "{name} Tutor is on the way! Python is ready for now.",
    subject_started: "🐍 {subj} is ready — let's go, {name}!",
    soon_chip: "soon",
    home_btn: "🏠 Main menu",
  },

  fa: {
    doc_title: "🐍 Python Tutor — آموزش پایتون ۳٫۱۴",
    brand_name: "آموزش پایتون",
    brand_sub: "برگرفته از مستندات رسمی پایتون ۳٫۱۴",
    welcome_sub: "پایتون ۳٫۱۴ را قدم‌به‌قدم از روی مستندات رسمی بیاموز — " +
      "درس‌ها را بخوان، نمودارها را ببین و سپس با آزمون‌های واقعی " +
      "دانش‌ات را محک بزن.",
    name_label: "اول، نامت را به من بگو:",
    name_placeholder: "مثلاً آدا",
    start_btn: "شروع یادگیری",
    welcome_hint: "برای شروع، Enter را بزن",
    change_name: "✏️ تغییر نام",
    progress_label: "پیشرفت",
    progress_text: "{answered} از {total} سوال · {done} از {chapters} فصل",
    greeting: "👋 سلام، {name}!",
    greeting_anon: "👋 خوش آمدی!",
    cat_tutorial: "آموزش",
    cat_using: "استفاده از پایتون",
    cat_library: "مرجع کتابخانه",
    cat_howto: "راهنماها",
    cat_reference: "مرجع زبان",
    cat_c_foundations: "پایه‌ها",
    cat_c_memory: "حافظه و داده",
    cat_c_programs: "ساخت برنامه",
    cat_c_deep: "C عمیق",
    cat_c_system: "سیستم و مدرن",
    cat_c_modern: "استانداردها و فراتر",
    cat_h_basics: "مبانی HTML",
    cat_h_structure: "ساختار و جدول‌ها",
    cat_h_forms: "فرم‌ها و ویژگی‌ها",
    cat_h_advanced: "دسترس‌پذیری و پیشرفته",
    cat_s_fundamentals: "مبانی",
    cat_s_values: "مقادیر و جعبه‌ها",
    cat_s_typography: "تایپوگرافی",
    cat_s_layout: "چیدمان",
    cat_s_responsive: "واکنش‌گرا",
    cat_s_modern: "CSS مدرن",
    cat_s_effects: "جلوه‌های بصری",
    cat_s_advanced: "پیشرفته",
    cat_s_pro: "حرفه‌ای",
    cat_j_fundamentals: "مبانی",
    cat_j_flow: "کنترل جریان",
    cat_j_functions: "توابع",
    cat_j_data: "آرایه‌ها و شیءها",
    cat_j_advanced: "JS پیشرفته",
    cat_j_builtin: "شیءهای داخلی",
    cat_j_async: "JS ناهمگام",
    cat_j_modules: "ماژول‌ها",
    cat_j_browser: "JS مرورگر",
    cat_j_topics: "موضوعات پیشرفته",
    cat_p_basics: "مبانی ++C",
    cat_p_scope: "scope و اشاره‌گرها",
    cat_p_oop: "OOP و کلاس‌ها",
    cat_p_raii: "RAII و حافظه",
    cat_p_stl: "STL",
    cat_p_modern: "++C مدرن",
    cat_p_cpp23: "قابلیت‌های C++20/23",
    cat_p_pro: "‏++C حرفه‌ای",
    chapter_complete: "🎉 فصل {num} کامل شد، {name}!",
    finish_toast: "🏁 کل دوره را تمام کردی، {name}! 🎉",
    welcome_back: "👋 خوش برگشتی، {name}!",
    welcome_toast: "🎉 خوش آمدی، {name}! آماده‌ای پایتون یاد بگیری؟",
    breadcrumb: "فصل {ch} · درس {lesson} از {of}",
    btn_prev: "قبلی",
    btn_next_lesson: "درس بعدی",
    btn_take_quiz: "شروع آزمون",
    btn_next_chapter: "فصل بعدی",
    btn_finish: "پایان 🏁",
    btn_back_lessons: "بازگشت به درس‌ها",
    copy_code: "کپی",
    copied_code: "کپی شد!",
    chips_label: "زبان آموزش",
    read_time: "⏱ {min} دقیقه مطالعه",
    read_progress: "📖 {read} از {total} درس خوانده شد",
    search_ph: "جست‌وجوی درس‌ها…",
    diff_beg: "مبتدی",
    diff_int: "متوسط",
    diff_adv: "پیشرفته",
    zen_title: "حالت تمرکز (F)",
    zen_toast: "حالت تمرکز — برای خروج F یا ✕ را بزن",
    bookmark_add: "نشان‌گذاری این درس",
    bookmark_remove: "حذف نشان",
    bookmarks: "نشان‌شده‌ها",
    update_msg: "نسخهٔ جدیدی از آموزش‌ها آماده است!",
    update_btn: "به‌روزرسانی",
    bn_menu: "منو",
    bn_search: "جست‌وجو",
    bn_saved: "نشان‌شده",
    bn_focus: "تمرکز",
    bn_lang: "زبان",
    compare_title: "مقایسهٔ زبان‌ها",
    pal_ph: "جست‌وجوی درس‌ها یا دستورها…",
    pal_commands: "دستورها",
    share_lesson: "اشتراک‌گذاری این درس",
    share_text: "این درس را در PLT ببین:",
    link_copied: "لینک درس کپی شد ✓",
    tryit_label: "💻 خودت امتحان کن — کد پایتون بنویس و اجرا کن:",
    run: "▶ اجرا",
    running: "در حال اجرا…",
    engine_loading: "⏳ در حال بارگذاری موتور پایتون در مرورگر (فقط بار اول — " +
      "حدود ۱۰ مگابایت، سپس کش می‌شود)…",
    no_output: "(خروجی نیست)",
    engine_fail: "بارگذاری موتور پایتون ممکن نشد ({err}). اتصال اینترنت‌ات را " +
      "بررسی کن و دوباره «اجرا» را بزن.",
    engine_timeout: "پس از {sec} ثانیه متوقف شد — شاید کد در یک حلقهٔ بی‌نهایت " +
      "گیر کرده یا منتظر ورودی input() است.",
    server_unreachable: "برقراری ارتباط با سرور ممکن نشد.",
    quiz_header: "آزمون فصل",
    quiz_intro1: "{title} — برای کامل شدن فصل باید به همهٔ سوال‌ها پاسخ بدهی. " +
      "سوال‌ها چهار شکل دارند: چندگزینه‌ای، پر کردن جای خالی، " +
      "مرتب کردن خط‌ها و نوشتن کد.",
    quiz_intro2: "موفق باشی، {name}! 🤞",
    quiz_done_banner: "✔ فصل کامل شد — آفرین، {name}!",
    q_label: "سوال {n}.",
    check_btn: "بررسی",
    correct: "✅ درست است، {name}!",
    wrong: "❌ درست نیست، {name}.",
    answer_label: "پاسخ:",
    show_answer: "نمایش پاسخ",
    pick_option: "اول یک گزینه را انتخاب کن",
    pick_lines: "ابتدا هر {n} خط را انتخاب کن",
    blank_placeholder: "پاسخ را بنویس",
    hint_prefix: "راهنما: ",
    order_instruction: "روی خط‌ها به ترتیب درست کلیک کن.",
    status_all: "✅ به همهٔ {n} سوال پاسخ دادی — پاسخ‌ها را مرور کن و " +
      "هر وقت آماده بودی، ادامه بده.",
    status_partial: "{answered} از {total} سوال پاسخ داده شده.",
    load_error_title: "محتوای دوره بارگذاری نشد",
    load_error_body: "فایل دادهٔ دوره (<code>data.js</code>) کنار " +
      "<code>app.js</code> پیدا نشد. آن را با <code>python build_static.py</code> " +
      "بازتولید کن و دوباره منتشر کن.",
    lang_aria: "زبان",
    quiz_label: "آزمون",
    playground_btn: "🧪 محیط تمرین",
    playground_blocked: "باز کردن پنجره ممکن نشد — نمایش popup را برای " +
      "این سایت مجاز کن.",
    subject_title: "می‌خواهی چه چیزی یاد بگیری؟",
    subject_sub: "یک زبان را انتخاب کن — برای پیش‌نمایش، ماوس را روی " +
      "دایره‌ها ببر و برای انتخاب، کلیک کن.",
    subject_hint: "آموزش‌های بیشتری در راه‌اند 🚧",
    start_with: "شروع یادگیری {name}",
    continue_with: "ادامهٔ {name}",
    coming_soon_btn: "{name} — به‌زودی",
    coming_soon_tag: "در حال ساخت 🚧",
    ready_tag: "{chapters} فصل · {questions} سوال · آمادهٔ شروع",
    soon_toast: "آموزش {name} در راه است! فعلاً پایتون آماده است.",
    subject_started: "🐍 {subj} آماده است — بزن بریم، {name}!",
    soon_chip: "به‌زودی",
    home_btn: "🏠 منوی اصلی",
  },
};

function t(key, vars) {
  /* subject-specific strings win: the C course overrides branding and
     engine wording without touching the shared table below */
  const sub = SUBJ_STR[activeSubject];
  let s = (sub && sub[lang] && sub[lang][key]) ||
    (STR[lang] && STR[lang][key]) || STR.en[key] || key;
  if (vars) {
    for (const k of Object.keys(vars)) {
      s = s.replace(new RegExp("\\{" + k + "\\}", "g"), String(vars[k]));
    }
  }
  return s;
}

/* Per-subject string overrides: the loaded course re-brands shared UI
   strings (title, subtitle, engine wording, toasts) without touching
   the shared STR table above. */
const SUBJ_STR = {
  c: {
    en: {
      doc_title: "🔷 C Tutor — Learn C Programming",
      brand_name: "C Tutor",
      brand_sub: "based on Beej's Guide to C Programming",
      welcome_sub: "Learn C from Beej's Guide to C Programming — at your " +
        "own pace. Read the lessons, run real C in your browser, then " +
        "prove your knowledge with quiz questions.",
      welcome_toast: "🎉 Welcome, {name}! Ready to learn C?",
      tryit_label: "💻 Try it yourself — write C and run it:",
      engine_loading: "⏳ Starting the in-browser C engine…",
      engine_fail: "Couldn't start the C engine ({err}). Press Run again.",
      engine_timeout: "Timed out after {sec}s — the code may be stuck in " +
        "an infinite loop or waiting for scanf().",
      subject_started: "🔷 C is ready — let's go, {name}!",
    },
    fa: {
      doc_title: "🔷 آموزش C — برنامه‌نویسی C را یاد بگیر",
      brand_name: "آموزش C",
      brand_sub: "برگرفته از کتاب راهنمای C اثر بیج",
      welcome_sub: "برنامه‌نویسی C را قدم‌به‌قدم از روی کتاب بیج بیاموز — " +
        "درس‌ها را بخوان، همین‌جا در مرورگر کد C واقعی اجرا کن و بعد با " +
        "سؤال‌های آزمون دانش‌ات را محک بزن.",
      welcome_toast: "🎉 خوش آمدی، {name}! آماده‌ای C یاد بگیری؟",
      tryit_label: "💻 خودت امتحان کن — کد C بنویس و اجرا کن:",
      engine_loading: "⏳ در حال آماده‌سازی موتور C در مرورگر…",
      engine_fail: "راه‌اندازی موتور C ممکن نشد ({err}). دوباره «اجرا» را بزن.",
      engine_timeout: "پس از {sec} ثانیه متوقف شد — شاید کد در حلقهٔ بی‌نهایت " +
        "گیر کرده یا منتظر scanf() است.",
      subject_started: "🔷 C آماده است — بزن بریم، {name}!",
    },
  },
  html: {
    en: {
      doc_title: "🛡️ HTML Tutor — Learn HTML",
      brand_name: "HTML Tutor",
      brand_sub: "based on MDN Web Docs",
      welcome_sub: "Learn HTML — the structure of the web — at your own " +
        "pace. Read the lessons, see your markup render live in the " +
        "browser, then prove your knowledge with quiz questions.",
      welcome_toast: "🎉 Welcome, {name}! Ready to learn HTML?",
      tryit_label: "💻 Try it yourself — write HTML and see it render:",
      subject_started: "🛡️ HTML is ready — let's go, {name}!",
    },
    fa: {
      doc_title: "🛡️ آموزش HTML — اچ‌تی‌ام‌ال را یاد بگیر",
      brand_name: "آموزش HTML",
      brand_sub: "برگرفته از اسناد وب MDN",
      welcome_sub: "HTML — ساختار وب — را قدم‌به‌قدم بیاموز. درس‌ها را بخوان، " +
        "نشانه‌گذاری‌ات را زنده در مرورگر ببین و بعد با سؤال‌های آزمون " +
        "دانش‌ات را محک بزن.",
      welcome_toast: "🎉 خوش آمدی، {name}! آماده‌ای HTML یاد بگیری؟",
      tryit_label: "💻 خودت امتحان کن — HTML بنویس و زنده ببینش:",
      subject_started: "🛡️ HTML آماده است — بزن بریم، {name}!",
    },
  },
  css: {
    en: {
      doc_title: "🎯 CSS Tutor — Learn CSS",
      brand_name: "CSS Tutor",
      brand_sub: "based on MDN Web Docs",
      welcome_sub: "Learn CSS — the presentation of the web — across 30 " +
        "chapters: from selectors and the cascade to Flexbox, Grid and " +
        "modern CSS. Style real pages and see them render live.",
      welcome_toast: "🎉 Welcome, {name}! Ready to learn CSS?",
      tryit_label: "💻 Try it yourself — edit the CSS and see it live:",
      subject_started: "🎯 CSS is ready — let's go, {name}!",
    },
    fa: {
      doc_title: "🎯 آموزش CSS — سی‌اس‌اس را یاد بگیر",
      brand_name: "آموزش CSS",
      brand_sub: "برگرفته از اسناد وب MDN",
      welcome_sub: "CSS — نمایشِ وب — را در ۳۰ فصل بیاموز: از سلکتورها و " +
        "آبشار تا Flexbox، Grid و CSS مدرن. صفحه‌های واقعی را استایل بده " +
        "و زنده ببینشان.",
      welcome_toast: "🎉 خوش آمدی، {name}! آماده‌ای CSS یاد بگیری؟",
      tryit_label: "💻 خودت امتحان کن — CSS را ویرایش کن و زنده ببینش:",
      subject_started: "🎯 CSS آماده است — بزن بریم، {name}!",
    },
  },
  js: {
    en: {
      doc_title: "🟨 JavaScript Tutor — Learn JS",
      brand_name: "JavaScript Tutor",
      brand_sub: "based on MDN Web Docs",
      welcome_sub: "Learn JavaScript — the language of the web — across " +
        "10 phases: from variables and control flow to closures, async, " +
        "DOM and beyond. Write real JS and see the console output live.",
      welcome_toast: "🎉 Welcome, {name}! Ready to learn JavaScript?",
      tryit_label: "💻 Try it yourself — write JS and check the console:",
      subject_started: "🟨 JavaScript is ready — let's go, {name}!",
    },
    fa: {
      doc_title: "🟨 آموزش جاوااسکریپت — JS را یاد بگیر",
      brand_name: "آموزش جاوااسکریپت",
      brand_sub: "برگرفته از اسناد وب MDN",
      welcome_sub: "جاوااسکریپت — زبانِ وب — را در ۱۰ مرحله بیاموز: از " +
        "متغیرها و کنترل جریان تا closureها، async و DOM. کد JS واقعی " +
        "بنویس و خروجی console را زنده ببین.",
      welcome_toast: "🎉 خوش آمدی، {name}! آماده‌ای جاوااسکریپت یاد بگیری؟",
      tryit_label: "💻 خودت امتحان کن — JS بنویس و خروجی console را ببین:",
      subject_started: "🟨 جاوااسکریپت آماده است — بزن بریم، {name}!",
    },
  },
  cpp: {
    en: {
      doc_title: "🔷 C++ Tutor — Learn C++23",
      brand_name: "C++ Tutor",
      brand_sub: "based on learncpp.com and MDN",
      welcome_sub: "Learn C++23 — from fundamentals through templates, " +
        "STL, smart pointers, ranges and beyond. 44 chapters covering " +
        "the complete modern C++ journey.",
      welcome_toast: "🎉 Welcome, {name}! Ready to learn C++?",
      tryit_label: "💻 Try it yourself — write C++ and see the output:",
      subject_started: "🔷 C++ is ready — let's go, {name}!",
    },
    fa: {
      doc_title: "🔷 آموزش ++C — بیاموز C++23",
      brand_name: "آموزش ++C",
      brand_sub: "برگرفته از learncpp.com و MDN",
      welcome_sub: "‏C++23 را بیاموز — از مبانی تا قالب‌ها، STL، اشاره‌گرهای " +
        "هوشمند، رنج‌ها و فراتر. ۴۴ فصل پوشش‌دهندهٔ سفرِ کاملِ ++C مدرن.",
      welcome_toast: "🎉 خوش آمدی، {name}! آماده‌ای ++C یاد بگیری؟",
      tryit_label: "💻 خودت امتحان کن — کد بنویس و خروجی را ببین:",
      subject_started: "🔷 ++C آماده است — بزن بریم، {name}!",
    },
  },
};

const FA_DIGITS = ["۰", "۱", "۲", "۳", "۴", "۵", "۶", "۷", "۸", "۹"];
function fmtNum(n) {
  const s = String(n);
  return lang === "fa" ? s.replace(/[0-9]/g, (d) => FA_DIGITS[+d]) : s;
}

/* static elements in index.html carry data-i18n (text) / data-i18n-ph (placeholder) */
function applyStaticText() {
  document.title = t("doc_title");
  document.querySelectorAll("[data-i18n]").forEach((el) => {
    el.textContent = t(el.getAttribute("data-i18n"));
  });
  document.querySelectorAll("[data-i18n-ph]").forEach((el) => {
    el.setAttribute("placeholder", t(el.getAttribute("data-i18n-ph")));
  });
  document.querySelectorAll(".lang-switch").forEach((el) => {
    el.setAttribute("aria-label", t("lang_aria"));
  });
  renderSubjectChips(); // chip labels follow the UI language
}

function ensureLangPills() {
  document.querySelectorAll(".lang-switch").forEach((box) => {
    if (box.dataset.built) return;
    box.dataset.built = "1";
    [["en", "English"], ["fa", "فارسی"]].forEach(([code, label]) => {
      const b = document.createElement("button");
      b.type = "button";
      b.dataset.lang = code;
      b.textContent = label;
      b.setAttribute("role", "radio");
      b.addEventListener("click", () => setLang(code));
      box.appendChild(b);
    });
  });
  updateLangPills();
}

function updateLangPills() {
  document.querySelectorAll(".lang-switch button").forEach((b) => {
    const active = b.dataset.lang === lang;
    b.classList.toggle("active", active);
    b.setAttribute("aria-checked", String(active));
  });
}

/* The language switch: everything fades + soft-blurs out, the strings and
   text direction are swapped behind the veil, then it fades back in. */
let langBusy = false;
function sleep(ms) {
  return new Promise((r) => setTimeout(r, ms));
}
async function setLang(next) {
  if (langBusy || next === lang) return;
  langBusy = true;
  document.body.classList.add("switching");
  await sleep(220);
  applyLang(next);
  document.body.classList.remove("switching");
  langBusy = false;
}

function applyLang(next) {
  lang = next;
  try { localStorage.setItem(LANG_KEY, next); } catch (e) { /* non-fatal */ }
  const root = document.documentElement;
  root.lang = next;
  if (next === "fa") root.setAttribute("dir", "rtl");
  else root.removeAttribute("dir");
  applyStaticText();
  updateSubjectBrand();
  updateLangPills();
  if ($("subject").classList.contains("show")) {
    renderChooser();
    setPreview(previewSubject, false);
    updateStartButton();
  } else if (courseActive) {
    renderSidebar();
    renderView(true);
  }
}

/* ======================= Persian course content ======================== */
/* The course data carries optional Persian variants: chapters have
   title_fa, lessons have title_fa/html_fa (code blocks and [[diag:...]]
   diagrams identical to the English version), and quiz questions carry a
   fa override for question/options/explain. English stays the canonical
   source; these helpers pick the variant at render time. */

function faChapterTitle(ch) {
  return (lang === "fa" && ch.title_fa) ? ch.title_fa : ch.title;
}
function faLesson(lesson) {
  if (lang === "fa" && lesson && lesson.html_fa) {
    // the try-it seed code is shared: the sandbox runs the same C either way
    return { __fa: true, title: lesson.title_fa || lesson.title,
             html: lesson.html_fa, tryit: lesson.tryit };
  }
  return lesson;
}
function faQuestion(q) {
  if (lang !== "fa" || !q || !q.fa) return q;
  return Object.assign({}, q, q.fa, { __fa: true });
}
/* direction + alignment for a block whose text may be Persian (RTL) or
   English (LTR). Inline style beats every CSS rule, so this is reliable
   no matter what the surrounding page direction is. */
function applyDir(el, isFa) {
  el.style.direction = isFa ? "rtl" : "ltr";
  el.style.textAlign = isFa ? "right" : "left";
}

function getUserName() {
  try { return localStorage.getItem(NAME_KEY) || ""; } catch (e) { return ""; }
}
function saveUserName(n) {
  try { localStorage.setItem(NAME_KEY, n); } catch (e) { /* non-fatal */ }
}
function displayName() {
  const n = getUserName().trim();
  if (n) return n;
  return lang === "fa" ? "دوست" : "friend";
}

function loadProgress() {
  try {
    return JSON.parse(localStorage.getItem(STORE_KEY)) || {};
  } catch (e) {
    return {};
  }
}
function saveProgress() {
  try {
    localStorage.setItem(STORE_KEY, JSON.stringify(progress));
  } catch (e) { /* storage full or disabled — non-fatal */ }
}

function chapterState(ch) {
  const s = progress[ch.id] || { q: ch.quiz.map(() => "none") };
  return s;
}
function chapterDone(ch) {
  const s = chapterState(ch);
  return s.q.length > 0 && s.q.every((st) => st === "ok");
}
function quizAnsweredCount(ch) {
  return chapterState(ch).q.filter((st) => st !== "none").length;
}
function setQuestionStatus(ch, i, status) {
  const s = chapterState(ch);
  s.q[i] = status === "ok" ? "ok" : (s.q[i] === "ok" ? "ok" : "missed");
  progress[ch.id] = s;
  saveProgress();
  renderSidebar();
  updateQuizStatus();
  if (status === "ok" && chapterDone(ch)) {
    toast(t("chapter_complete", {
      num: fmtNum(chapters.indexOf(ch) + 1),
      name: displayName(),
    }));
  }
}

/* ============================== checking =============================== */
/* Quiz scoring now runs entirely in the browser (ported 1:1 from the
   Python checker.py), so the deployed site needs no backend at all. */

function normalizeAnswer(text) {
  return String(text == null ? "" : text).toLowerCase()
    .replace(/\s+/g, " ").trim();
}

function matchAny(answers, given) {
  const g = normalizeAnswer(given);
  return (answers || []).some((a) => normalizeAnswer(a) === g);
}

function checkQuestion(q, answer) {
  if (q.type === "mc") {
    return { correct: answer === q.answer, explain: q.explain || "" };
  }
  if (q.type === "blank") {
    return { correct: matchAny(q.answers, answer), explain: q.explain || "" };
  }
  if (q.type === "order") {
    const correct = Array.isArray(answer) &&
      answer.length === (q.lines || []).length &&
      answer.every((v, i) => v === i);
    return { correct: !!correct, explain: q.explain || "" };
  }
  if (q.type === "codefill") {
    const blanks = (q.code || []).filter((item) => typeof item === "object");
    const correct = Array.isArray(answer) &&
      answer.length === blanks.length &&
      blanks.every((b, i) => matchAny(b.answers, answer[i]));
    return { correct: !!correct, explain: q.explain || "" };
  }
  return { correct: false, explain: "Unknown question type: " + q.type };
}

/* ========================== in-browser engines ========================= */
/* The "Try it yourself" playground runs REAL code in the browser: Pyodide
   for Python (pyrunner.js) and the CEngine interpreter for C (cengine.js,
   wrapped in a worker by crunner.js). Both share the same interface. */

function engineFor(subject) {
  return (subject === "c" || subject === "cpp")
    ? window.CRunner : window.PyRunner;
}

/* Engine wording for status lines: HTML has no engine (the browser
   renders), so those strings never surface there. */

async function apiRun(code) {
  const runner = engineFor(activeSubject);
  const res = await runner.run(code);
  if (!res.err) return { ok: res.ok, output: res.output };
  if (res.err === "load") {
    return {
      ok: false,
      output: t("engine_fail", {
        err: res.error || "network error",
      }),
    };
  }
  return {
    ok: false,
    output: t("engine_timeout", { sec: runner.RUN_TIMEOUT_MS / 1000 }),
  };
}

/* ============================== sidebar ================================ */

/* One header per course section, in course order — per subject. */
const CATEGORIES = {
  python: [
    { key: "cat_tutorial",   emoji: "\u{1F4D6}", start: 1,  end: 16 },
    { key: "cat_using",      emoji: "\u2699\uFE0F", start: 17, end: 19 },
    { key: "cat_library",    emoji: "\u{1F4DA}", start: 20, end: 23 },
    { key: "cat_howto",      emoji: "\u{1F9ED}", start: 24, end: 27 },
    { key: "cat_reference",  emoji: "\u{1F4DC}", start: 28, end: 31 },
  ],
  c: [
    { key: "cat_c_foundations", emoji: "\u{1F9F1}", start: 1,  end: 2  },
    { key: "cat_c_memory",      emoji: "\u{1F9E0}", start: 3,  end: 5  },
    { key: "cat_c_programs",    emoji: "\u{1F6E0}\uFE0F", start: 6,  end: 8  },
    { key: "cat_c_deep",        emoji: "\u{1F52C}", start: 9,  end: 10 },
    { key: "cat_c_system",      emoji: "\u{1F5A5}\uFE0F", start: 11, end: 13 },
    { key: "cat_c_modern",      emoji: "\u{1F4DC}", start: 14, end: 15 },
  ],
  html: [
    { key: "cat_h_basics",      emoji: "\u{1F680}", start: 1,  end: 5  },
    { key: "cat_h_structure",   emoji: "\u{1F3D7}\uFE0F", start: 6,  end: 7  },
    { key: "cat_h_forms",       emoji: "\u{1F4DD}", start: 8,  end: 9  },
    { key: "cat_h_advanced",    emoji: "\u{1F9F0}", start: 10, end: 13 },
  ],
  css: [
    { key: "cat_s_fundamentals", emoji: "\u{1F331}", start: 1,  end: 3  },
    { key: "cat_s_values",       emoji: "\u{1F7E1}", start: 4,  end: 7  },
    { key: "cat_s_typography",   emoji: "\u270D\uFE0F", start: 8,  end: 8  },
    { key: "cat_s_layout",       emoji: "\u{1F7E3}", start: 9,  end: 13 },
    { key: "cat_s_responsive",   emoji: "\u{1F4F1}", start: 14, end: 15 },
    { key: "cat_s_modern",       emoji: "\u{1F534}", start: 16, end: 19 },
    { key: "cat_s_effects",      emoji: "\u{1FA84}", start: 20, end: 23 },
    { key: "cat_s_advanced",     emoji: "\u26AB", start: 24, end: 27 },
    { key: "cat_s_pro",          emoji: "\u{1F3DB}\uFE0F", start: 28, end: 30 },
  ],
  js: [
    { key: "cat_j_fundamentals", emoji: "\u{1F7E1}", start: 1,  end: 1  },
    { key: "cat_j_flow",         emoji: "\u{1F500}", start: 2,  end: 2  },
    { key: "cat_j_functions",    emoji: "\u{1F9E9}", start: 3,  end: 3  },
    { key: "cat_j_data",         emoji: "\u{1F4E6}", start: 4,  end: 4  },
    { key: "cat_j_advanced",     emoji: "\u{1F393}", start: 5,  end: 5  },
    { key: "cat_j_builtin",      emoji: "\u{1F9F0}", start: 6,  end: 6  },
    { key: "cat_j_async",        emoji: "\u23F3", start: 7,  end: 7  },
    { key: "cat_j_modules",      emoji: "\u{1F4C4}", start: 8,  end: 8  },
    { key: "cat_j_browser",      emoji: "\u{1F310}", start: 9,  end: 9  },
    { key: "cat_j_topics",       emoji: "\u{1F9E0}", start: 10, end: 10 },
  ],
  cpp: [
    { key: "cat_p_basics",       emoji: "\u{1F537}", start: 1,  end: 5  },
    { key: "cat_p_scope",        emoji: "\u{1F5C2}\uFE0F", start: 6,  end: 10 },
    { key: "cat_p_oop",          emoji: "\u{1F3DB}\uFE0F", start: 11, end: 16 },
    { key: "cat_p_raii",         emoji: "\u{1F511}", start: 17, end: 20 },
    { key: "cat_p_stl",          emoji: "\u{1F4DA}", start: 21, end: 24 },
    { key: "cat_p_modern",       emoji: "\u26A1", start: 25, end: 32 },
    { key: "cat_p_cpp23",        emoji: "\u{1F195}", start: 33, end: 40 },
    { key: "cat_p_pro",          emoji: "\u{1F3C6}", start: 41, end: 44 },
  ],
};

function sidebarCategories() {
  return CATEGORIES[activeSubject] || CATEGORIES.python;
}

/* Chevron shown at the end of every chapter row; points at the inline
   start edge when closed and rotates down when the group is open. */
const CHEV_SVG = '<svg width="10" height="10" viewBox="0 0 10 10">' +
  '<path d="M2.5 1.5 L7.5 5 L2.5 8.5" fill="none" stroke="currentColor" ' +
  'stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>';

function faLessonTitle(lesson) {
  return (lang === "fa" && lesson && lesson.title_fa)
    ? lesson.title_fa
    : lesson.title;
}

function renderSidebar() {
  const list = $("chapter-list");
  list.innerHTML = "";
  const firstBuild = !sidebarEntranceShown;
  for (const cat of sidebarCategories()) {
    const head = document.createElement("div");
    head.className = "category-head";
    head.innerHTML = '<span class="cat-emoji">' + cat.emoji +
      "</span><span>" + esc(t(cat.key)) + "</span>";
    if (firstBuild) head.style.animationDelay = (0.05 + (cat.start - 1) * 0.02) + "s";
    list.appendChild(head);
    for (let i = cat.start - 1; i < cat.end; i++) {
      const ch = chapters[i];
      if (!ch) continue;
      list.append(...renderChapterGroup(ch, i, firstBuild));
    }
  }
  if (firstBuild) {
    sidebarEntranceShown = true;
    list.classList.add("entrance");
    setTimeout(() => list.classList.remove("entrance"), 1500);
  }

  const name = getUserName().trim();
  $("user-greeting").textContent = name
    ? t("greeting", { name })
    : t("greeting_anon");

  const doneCount = chapters.filter(chapterDone).length;
  const mastered = chapters.reduce((n, ch) =>
    n + chapterState(ch).q.filter((st) => st === "ok").length, 0);
  const totalQ = chapters.reduce((n, ch) => n + ch.quiz.length, 0);
  $("overall-text").textContent = t("progress_text", {
    answered: fmtNum(mastered),
    total: fmtNum(totalQ),
    done: fmtNum(doneCount),
    chapters: fmtNum(chapters.length),
  });
  $("overall-bar").style.width = (100 * mastered / totalQ) + "%";
  updateReadProgressLine();
}

/* A chapter header row plus its collapsible sub-list: one item per lesson
   and a Quiz item at the end (w3schools-style section navigation). */
function renderChapterGroup(ch, i, firstBuild) {
  const done = chapterDone(ch);
  const finished = quizAnsweredCount(ch) >= ch.quiz.length;
  const open = sidebarOpenChapter === i;
  const activeLessonIdx = i === state.chapter && state.step.kind === "lesson"
    ? state.step.idx : -1;
  const quizActive = i === state.chapter && state.step.kind === "quiz";

  const btn = document.createElement("button");
  btn.className = "chapter-item" +
    (i === state.chapter ? " active" : "") +
    (finished ? " finished" : "") +
    (open ? " open" : "");
  btn.dataset.ch = i;
  btn.setAttribute("aria-expanded", open ? "true" : "false");
  if (firstBuild) btn.style.animationDelay = (0.05 + i * 0.02) + "s";
  btn.innerHTML =
    '<span class="num">' + fmtNum(i + 1) + "</span>" +
    '<span class="ch-title">' + esc(faChapterTitle(ch)) + "</span>" +
    '<span class="dot">' + (done ? "\u2714" : "") + "</span>" +
    '<span class="chev" aria-hidden="true">' + CHEV_SVG + "</span>";
  btn.addEventListener("click", () => chapterHeaderClick(i));

  const inner = document.createElement("div");
  inner.className = "sublist-inner";
  const readSet = readStore()[activeSubject] || {};
  ch.lessons.forEach((lesson, j) => {
    const s = document.createElement("button");
    s.className = "sub-item" + (j === activeLessonIdx ? " active" : "") +
      (readSet[ch.id + "/" + j] ? " read" : "");
    s.dataset.ch = i;
    s.dataset.idx = j;
    s.innerHTML = '<span class="sub-title">' + esc(faLessonTitle(lesson)) +
      '</span><span class="read-tick" aria-hidden="true">✔</span>';
    s.addEventListener("click", () => goToStep(i, "lesson", j));
    inner.appendChild(s);
  });

  const answered = quizAnsweredCount(ch);
  const badge = done
    ? "\u2714"
    : (answered ? fmtNum(answered) + "/" + fmtNum(ch.quiz.length) : "");
  const qz = document.createElement("button");
  qz.className = "sub-item quiz" + (quizActive ? " active" : "");
  qz.innerHTML = '<span class="quiz-ico">\u{1F4DD}</span>' +
    "<span>" + esc(t("quiz_label")) + "</span>" +
    '<span class="quiz-badge">' + badge + "</span>";
  qz.addEventListener("click", () => goToStep(i, "quiz", 0));
  inner.appendChild(qz);

  const sub = document.createElement("div");
  sub.className = "sublist" + (open ? " open" : "");
  sub.appendChild(inner);
  return [btn, sub];
}

/* Keep the open/closed state of every group in the existing DOM in sync
   with sidebarOpenChapter (without a rebuild, so CSS transitions play). */
function syncSublists() {
  document.querySelectorAll("#chapter-list .chapter-item").forEach((btn) => {
    const i = +btn.dataset.ch;
    const open = sidebarOpenChapter === i;
    btn.classList.toggle("open", open);
    btn.setAttribute("aria-expanded", open ? "true" : "false");
    const sub = btn.nextElementSibling;
    if (sub && sub.classList.contains("sublist")) {
      sub.classList.toggle("open", open);
    }
  });
}

function esc(s) {
  const d = document.createElement("div");
  d.textContent = s;
  return d.innerHTML;
}

/* ============================== navigation ============================= */

/* w3schools-style accordion: exactly one chapter group is expanded at a
   time; it always follows the chapter being read. */
let sidebarOpenChapter = 0;

function goToStep(chIdx, kind, stepIdx) {
  state.chapter = chIdx;
  state.step = { kind, idx: stepIdx };
  sidebarOpenChapter = chIdx;
  renderSidebar();
  renderView();
  $("main").scrollTop = 0;
}

function openChapter(i) {
  goToStep(i, "lesson", 0);
}

/* Clicking a chapter header: navigate to the chapter (and open its
   sub-list); clicking the header of the chapter you are already reading
   just collapses the sub-list. */
function chapterHeaderClick(i) {
  if (state.chapter === i && sidebarOpenChapter === i) {
    sidebarOpenChapter = null;
    syncSublists();
  } else {
    openChapter(i);
  }
}

function openStep(kind, idx) {
  state.step = { kind, idx };
  sidebarOpenChapter = state.chapter;
  renderSidebar();
  renderView();
  $("main").scrollTop = 0;
}

function currentChapter() {
  return chapters[state.chapter];
}

function nextStep() {
  const ch = currentChapter();
  if (state.step.kind === "lesson") {
    if (state.step.idx + 1 < ch.lessons.length) {
      openStep("lesson", state.step.idx + 1);
    } else {
      openStep("quiz", 0);
    }
  } else {
    if (state.chapter + 1 < chapters.length) {
      openChapter(state.chapter + 1);
    } else {
      toast(t("finish_toast", { name: displayName() }));
    }
  }
}

function prevStep() {
  const ch = currentChapter();
  if (state.step.kind === "lesson") {
    if (state.step.idx > 0) openStep("lesson", state.step.idx - 1);
  } else {
    openStep("lesson", ch.lessons.length - 1);
  }
}

/* ============================== main view ============================== */

/* skipAnim is used by the language switch: the whole app is mid-crossfade,
   so the per-view entrance would double-dim it. */
function renderView(skipAnim) {
  const view = $("view");
  view.classList.remove("anim-in");
  // skeleton first (one short beat) — content renders right after, so a
  // lesson switch never shows a blank/jumping page
  if (skipAnim) { renderViewInto(view); return; }
  view.innerHTML =
    '<div class="skel">' +
    '<div class="skel-row w35"></div>' +
    '<div class="skel-line w90"></div>' +
    '<div class="skel-line w75"></div>' +
    '<div class="skel-line w82"></div>' +
    '<div class="skel-code"></div>' +
    '<div class="skel-line w88"></div>' +
    '<div class="skel-line w64"></div>' +
    "</div>";
  setTimeout(() => {
    if (view.firstElementChild && view.firstElementChild.classList.contains("skel")) {
      renderViewInto(view);
    }
  }, 130);
}

function renderViewInto(view) {
  view.classList.remove("anim-in");
  view.innerHTML = "";
  const ch = currentChapter();
  if (state.step.kind === "lesson") {
    view.appendChild(renderLesson(ch));
  } else {
    view.appendChild(renderQuiz(ch));
  }
  view.classList.add("anim-in");
  // a freshly opened lesson/quiz always starts at its own top — on phones
  // the sidebar sits ABOVE the content, so without this the lesson opens
  // half-hidden below it
  $("main").scrollTop = 0;
  const active = document.querySelector(".sub-item.active, .chapter-item.active");
  if (active) active.scrollIntoView({ block: "nearest" });
  // phones: picking a title closes the drawer so the page shows fully
  setDrawer(false);
  savePosition();
  markOnLessonEnd();
  updateHash();
}
/* a lesson counts as "read" when its end becomes visible (or when it is
   too short to scroll at all) */
let lessonEndHandler = null;
function markOnLessonEnd() {
  const main = $("main");
  if (lessonEndHandler) main.removeEventListener("scroll", lessonEndHandler);
  updateScrollProgress();
  const ch = chapters[state.chapter];
  const mark = () => {
    if (state.step.kind !== "lesson") return;
    if (main.scrollTop + main.clientHeight >= main.scrollHeight - 60) {
      markLessonRead(ch.id, state.step.idx);
      main.removeEventListener("scroll", lessonEndHandler);
      lessonEndHandler = null;
    }
  };
  lessonEndHandler = mark;
  main.addEventListener("scroll", mark, { passive: true });
  mark(); // short lessons: already at the end
}

function lessonBreadcrumb(ch, idx) {
  return t("breadcrumb", {
    ch: fmtNum(chapters.indexOf(ch) + 1),
    lesson: fmtNum(idx + 1),
    of: fmtNum(ch.lessons.length),
  });
}

function renderLesson(ch) {
  const idx = state.step.idx;
  const chapterFa = !!(lang === "fa" && ch.title_fa);
  const lesson = faLesson(ch.lessons[idx]);
  const card = document.createElement("div");
  card.className = "card";

  const head = document.createElement("div");
  head.className = "chapter-head";
  head.innerHTML = '<span class="emoji">' + ch.emoji + "</span>" +
    "<h2>" + esc(faChapterTitle(ch)) + "</h2>";
  applyDir(head.querySelector("h2"), chapterFa);
  card.appendChild(head);

  const bc = document.createElement("div");
  bc.className = "breadcrumb";
  bc.textContent = lessonBreadcrumb(ch, idx);
  card.appendChild(bc);

  const meta = document.createElement("div");
  meta.className = "lesson-meta";
  const d = difficultyOf(state.chapter);
  const badge = document.createElement("span");
  badge.className = "diff-badge " + d.cls;
  badge.textContent = d.dot + " " + t(d.key);
  meta.appendChild(badge);
  const words = (lesson.html || "").replace(/<[^>]+>/g, " ").split(/\s+/)
    .filter(Boolean).length;
  const rt = document.createElement("span");
  rt.className = "read-time";
  rt.textContent = t("read_time", { min: Math.max(1, Math.round(words / 180)) });
  meta.appendChild(rt);
  card.appendChild(meta);

  const h = document.createElement("h3");
  h.className = "lesson-title";
  h.textContent = lesson.title;
  applyDir(h, !!lesson.__fa);
  const star = document.createElement("button");
  star.type = "button";
  star.className = "star-btn" +
    (isBookmarked(activeSubject, ch.id, idx) ? " on" : "");
  star.title = isBookmarked(activeSubject, ch.id, idx)
    ? t("bookmark_remove") : t("bookmark_add");
  star.textContent = isBookmarked(activeSubject, ch.id, idx) ? "★" : "☆";
  star.addEventListener("click", () => {
    triggerHaptic();
    const on = toggleBookmark(ch.id, idx);
    star.classList.toggle("on", on);
    star.textContent = on ? "★" : "☆";
    star.title = on ? t("bookmark_remove") : t("bookmark_add");
  });
  const share = document.createElement("button");
  share.type = "button";
  share.className = "share-btn";
  share.title = t("share_lesson");
  share.textContent = "🔗";
  share.addEventListener("click", async () => {
    const url = location.href;
    if (navigator.share) {
      try { await navigator.share({ title: document.title,
        text: t("share_text"), url }); } catch (e) { /* user cancelled */ }
    } else if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(url).then(
        () => toast(t("link_copied")), () => {});
    }
  });
  card.appendChild(h);
  card.appendChild(star);
  card.appendChild(share);



  const body = document.createElement("div");
  body.className = "lesson-body";
  body.innerHTML = lesson.html;
  applyDir(body, !!lesson.__fa);
  // each code block gets a meta-bar: language on the left, Copy on the
  // right — touch users should never have to select code by hand
  body.querySelectorAll("pre.code").forEach((pre) => {
    const bar = document.createElement("div");
    bar.className = "code-head";
    const langName = document.createElement("span");
    langName.className = "code-lang";
    langName.textContent = subjName(subjectById(activeSubject));
    const copy = document.createElement("button");
    copy.type = "button";
    copy.className = "code-copy";
    copy.textContent = "📋 " + t("copy_code");
    copy.addEventListener("click", () => {
      const done = () => {
        copy.textContent = "✓ " + t("copied_code");
        copy.classList.add("ok");
        setTimeout(() => {
          copy.textContent = "📋 " + t("copy_code");
          copy.classList.remove("ok");
        }, 2000);
      };
      triggerHaptic();
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(pre.textContent).then(done, done);
      } else {
        const range = document.createRange();
        range.selectNodeContents(pre);
        const sel = window.getSelection();
        sel.removeAllRanges();
        sel.addRange(range);
        try { document.execCommand("copy"); } catch (e) { /* best effort */ }
        sel.removeAllRanges();
        done();
      }
    });
    const compare = document.createElement("button");
    compare.type = "button";
    compare.className = "code-expand";
    compare.textContent = "⇄";
    compare.title = t("compare_title");
    compare.addEventListener("click", openCompare);
    const group = document.createElement("span");
    group.className = "bar-group";
    const expand = document.createElement("button");
    expand.type = "button";
    expand.className = "code-expand";
    expand.textContent = "⛶";
    expand.title = t("zen_title").indexOf("(") > -1 ? "Full screen" : "Full screen";
    expand.addEventListener("click", () => openCodeModal(pre, langName.textContent));
    group.appendChild(copy);
    group.appendChild(expand);
    group.appendChild(compare);
    bar.appendChild(langName);
    bar.appendChild(group);
    pre.parentNode.insertBefore(bar, pre);
  });
  // callout cards: gotcha/tip lists become tinted boxes so key points
  // stand out (conservative keyword matching, EN + FA)
  const GOTCHA_RE = /(common mistake|gotcha|beginner mistake|surprises?|watch out|caveat|trap\b|rule of thumb|undefined behaviou?r)/i;
  const TIP_RE = /(pro tip|tip:|handy|clean way|convention)/i;
  const FA_WARN_RE = /(اشتباه رایج|تله|هشدار|مراقب|غافلگیر|اشتباه beginners)/;
  const FA_TIP_RE = /(قاعده|ترفند|نکته)/;
  const kids = [...body.children];
  kids.forEach((el, i) => {
    if (el.tagName !== "P" || el.classList.contains("callout")) return;
    const txt = el.textContent;
    const next = kids[i + 1];
    if (!next || next.tagName !== "UL") return;
    const fa = !!lesson.__fa;
    let kind = null;
    if (GOTCHA_RE.test(txt) || (fa && FA_WARN_RE.test(txt))) kind = "warning";
    else if (TIP_RE.test(txt) || (fa && FA_TIP_RE.test(txt))) kind = "tip";
    if (kind) {
      el.classList.add("callout", "callout-" + kind);
      next.classList.add("callout", "callout-" + kind);
    }
  });
  card.appendChild(body);

  // try-it playground — HTML/CSS render live; JS runs with console output,
  // except browser-lesson seeds that are full HTML documents (they render
  // live like the HTML ones); C/C++ ship seed code for the engine; Python
  // keeps its always-present box
  if (activeSubject === "html" || activeSubject === "css") {
    card.appendChild(renderTryItHtml(lesson.tryit));
  } else if (activeSubject === "js") {
    card.appendChild(/^\s*<(!DOCTYPE|html)/i.test(lesson.tryit || "")
      ? renderTryItHtml(lesson.tryit) : renderTryItJs(lesson.tryit));
  } else if (activeSubject === "python" || lesson.tryit) {
    card.appendChild(renderTryIt(lesson.tryit));
  }

  const nav = document.createElement("div");
  nav.className = "nav-row";
  const prev = document.createElement("button");
  prev.className = "btn secondary";
  prev.textContent = t("btn_prev");
  prev.disabled = state.step.idx === 0 && state.chapter === 0;
  prev.addEventListener("click", prevStep);
  const next = document.createElement("button");
  next.className = "btn";
  const isLastLesson = idx === ch.lessons.length - 1;
  next.textContent = isLastLesson ? t("btn_take_quiz") : t("btn_next_lesson");
  next.addEventListener("click", nextStep);
  nav.appendChild(prev);
  nav.appendChild(document.createElement("span")).className = "spacer";
  nav.appendChild(next);
  card.appendChild(nav);
  return card;
}

/* The HTML try-it is a live renderer: the browser IS the engine, so the
   code goes into a sandboxed iframe instead of a text console. */
function renderTryItHtml(seedCode) {
  const box = document.createElement("div");
  box.className = "tryit";
  const label = document.createElement("div");
  label.className = "tryit-label";
  label.textContent = t("tryit_label");
  const ta = document.createElement("textarea");
  ta.className = "codebox";
  ta.value = seedCode || "";
  ta.placeholder = "<!DOCTYPE html>\n<html lang=\"en\">\n<head><title>Demo</title></head>\n<body>\n  <h1>Hello!</h1>\n</body>\n</html>";
  ta.style.minHeight = "170px";
  const row = document.createElement("div");
  row.className = "answer-actions";
  const runBtn = document.createElement("button");
  runBtn.className = "btn secondary";
  runBtn.textContent = t("run");
  const frame = document.createElement("iframe");
  frame.className = "html-preview";
  frame.setAttribute("sandbox", "allow-scripts allow-same-origin");
  frame.setAttribute("title", "HTML preview");
  const out = document.createElement("div");
  out.className = "run-output show html-preview-note";
  function render() {
    out.style.display = "none";
    frame.srcdoc = ta.value;
  }
  runBtn.addEventListener("click", render);
  // render the seed right away — the preview is cheap and this way the
  // box works even before any scrolling
  render();
  row.appendChild(runBtn);
  box.appendChild(label);
  box.appendChild(ta);
  box.appendChild(row);
  box.appendChild(frame);
  box.appendChild(out);
  return box;
}

/* The JS try-it runs code with the browser's own engine and shows
   console output — the browser IS the JS engine. */
function renderTryItJs(seedCode) {
  const box = document.createElement("div");
  box.className = "tryit";
  const label = document.createElement("div");
  label.className = "tryit-label";
  label.textContent = t("tryit_label");
  const ta = document.createElement("textarea");
  ta.className = "codebox";
  ta.value = seedCode || "";
  ta.placeholder = 'console.log("Hello, JS!");';
  ta.style.minHeight = "140px";
  const row = document.createElement("div");
  row.className = "answer-actions";
  const runBtn = document.createElement("button");
  runBtn.className = "btn secondary";
  runBtn.textContent = t("run");
  const out = document.createElement("div");
  out.className = "run-output show";
  async function run() {
    const logs = [];
    const origLog = console.log;
    const origWarn = console.warn;
    const origError = console.error;
    console.log = (...args) => logs.push(args.map(a =>
      typeof a === "object" ? JSON.stringify(a, null, 2) : String(a)).join(" "));
    console.warn = (...args) => logs.push("⚠ " + args.join(" "));
    console.error = (...args) => logs.push("✗ " + args.join(" "));
    try {
      const fn = new Function(ta.value);
      fn();
    } catch (e) {
      logs.push("✗ " + e.message);
    } finally {
      // async lessons log from microtasks and timers — keep the hooks
      // installed briefly so their output lands in the box too
      await new Promise((r) => setTimeout(r, 300));
      console.log = origLog;
      console.warn = origWarn;
      console.error = origError;
    }
    out.textContent = logs.join("\n") || "(no output)";
    out.classList.toggle("err", logs.some(l => l.startsWith("✗")));
  }
  runBtn.addEventListener("click", run);
  // lazy render on scroll into view
  const io = new IntersectionObserver((entries) => {
    if (entries.some((e) => e.isIntersecting)) { run(); io.disconnect(); }
  });
  io.observe(out);
  row.appendChild(runBtn);
  box.appendChild(label);
  box.appendChild(ta);
  box.appendChild(row);
  box.appendChild(out);
  return box;
}

function renderTryIt(seedCode) {
  const box = document.createElement("div");
  box.className = "tryit";
  const label = document.createElement("div");
  label.className = "tryit-label";
  label.textContent = t("tryit_label");
  const ta = document.createElement("textarea");
  ta.className = "codebox";
  ta.value = seedCode || "";
  ta.placeholder = activeSubject === "c"
    ? "#include <stdio.h>\nint main(void) {\n    printf(\"hello\\n\");\n    return 0;\n}"
    : activeSubject === "cpp"
    ? "#include <iostream>\n\nint main() {\n    std::cout << \"Hello, C++23!\\n\";\n    return 0;\n}"
    : "print('hello')\nfor i in range(3):\n    print(i)";
  const row = document.createElement("div");
  row.className = "answer-actions";
  const runBtn = document.createElement("button");
  runBtn.className = "btn secondary";
  runBtn.textContent = t("run");
  const out = document.createElement("div");
  out.className = "run-output";
  const runner = engineFor(activeSubject);
  runBtn.addEventListener("click", async () => {
    out.className = "run-output show";
    out.textContent = runner.status === "ready"
      ? t("running")
      : t("engine_loading");
    runBtn.disabled = true;
    try {
      const res = await apiRun(ta.value);
      out.textContent = res.output || t("no_output");
      out.classList.toggle("err", !res.ok);
    } catch (e) {
      out.textContent = t("server_unreachable");
    } finally {
      runBtn.disabled = false;
    }
  });
  row.appendChild(runBtn);
  box.appendChild(label);
  box.appendChild(ta);
  box.appendChild(row);
  box.appendChild(out);
  return box;
}

/* ============================== quiz =================================== */

function renderQuiz(ch) {
  const card = document.createElement("div");
  card.className = "card";
  const head = document.createElement("div");
  head.className = "chapter-head";
  head.innerHTML = '<span class="emoji">' + ch.emoji + "</span>" +
    "<h2>" + esc(t("quiz_header")) + "</h2>";
  card.appendChild(head);

  const intro = document.createElement("div");
  intro.className = "quiz-intro";
  intro.innerHTML = "<p>" + esc(t("quiz_intro1", { title: faChapterTitle(ch) })) + "</p>" +
    "<p>" + esc(t("quiz_intro2", { name: displayName() })) + "</p>";
  card.appendChild(intro);

  if (chapterDone(ch)) {
    const banner = document.createElement("div");
    banner.className = "done-banner";
    banner.textContent = t("quiz_done_banner", { name: displayName() });
    card.appendChild(banner);
  }

  ch.quiz.forEach((q, i) => {
    const qbox = renderQuestion(ch, faQuestion(q), i);
    qbox.style.animationDelay = (i * 0.08) + "s";
    card.appendChild(qbox);
  });

  const statusEl = document.createElement("div");
  statusEl.className = "quiz-status";
  statusEl.id = "quiz-status";
  card.appendChild(statusEl);
  updateQuizStatus();

  const nav = document.createElement("div");
  nav.className = "nav-row";
  const prev = document.createElement("button");
  prev.className = "btn secondary";
  prev.textContent = t("btn_back_lessons");
  prev.addEventListener("click", () => openStep("lesson", ch.lessons.length - 1));
  const next = document.createElement("button");
  next.className = "btn";
  next.textContent = state.chapter + 1 < chapters.length
    ? t("btn_next_chapter") : t("btn_finish");
  next.addEventListener("click", nextStep);
  nav.appendChild(prev);
  nav.appendChild(document.createElement("span")).className = "spacer";
  nav.appendChild(next);
  card.appendChild(nav);
  return card;
}

function feedbackBox(q) {
  const box = document.createElement("div");
  box.className = "feedback";
  const title = document.createElement("div");
  const explain = document.createElement("div");
  explain.className = "explain";
  box.appendChild(title);
  box.appendChild(explain);
  box.show = function (ok, text) {
    box.className = "feedback show " + (ok ? "ok" : "no");
    title.textContent = ok
      ? t("correct", { name: displayName() })
      : t("wrong", { name: displayName() });
    explain.textContent = text || "";
    applyDir(explain, !!(this.q && this.q.__fa));
  };
  box.q = q;
  return box;
}

function showAnswer(q, fb) {
  let text = "";
  if (q.type === "mc") text = q.options[q.answer];
  else if (q.type === "blank") text = q.answers[0];
  else if (q.type === "order") text = "1. " + q.lines.join("\n   ");
  else if (q.type === "codefill") {
    text = q.code.map((item) =>
      typeof item === "string" ? item : item.answers[0]).join("");
  }
  const div = document.createElement("div");
  div.className = "feedback show no";
  div.innerHTML = "<div><b>" + esc(t("answer_label")) + "</b></div>" +
    "<pre style='margin:6px 0 0;white-space:pre-wrap;direction:ltr;text-align:left;font-family:Consolas,Menlo,monospace;font-size:13px'>"
    + esc(text) + "</pre>";
  fb.replaceWith ? fb.parentNode.replaceChild(div, fb) : null;
}

/* --- multiple choice --- */
function renderQuestionMC(ch, q, i) {
  const box = document.createElement("div");
  box.className = "question";
  box.innerHTML = '<div class="q-text">' + esc(t("q_label", { n: fmtNum(i + 1) })) +
    " " + q.question + "</div>";
  applyDir(box.querySelector(".q-text"), !!q.__fa);

  let selected = null;
  const opts = q.options.map((opt, oi) => {
    const b = document.createElement("button");
    b.className = "option";
    b.textContent = opt;
    applyDir(b, !!q.__fa);
    b.addEventListener("click", () => {
      triggerHaptic();
      opts.forEach((x) => x.classList.remove("selected"));
      b.classList.add("selected");
      selected = oi;
    });
    box.appendChild(b);
    return b;
  });

  const fb = feedbackBox(q);
  const actions = document.createElement("div");
  actions.className = "answer-actions";
  const check = document.createElement("button");
  check.className = "btn";
  check.textContent = t("check_btn");
  check.addEventListener("click", () => {
    if (selected === null) { toast(t("pick_option")); return; }
    const res = checkQuestion(q, selected);
    fb.show(res.correct, res.explain);
    if (res.correct) opts[q.answer].classList.add("correct");
    else opts[selected].classList.add("wrong");
    setQuestionStatus(ch, i, res.correct ? "ok" : "missed");
    check.disabled = true;
    addShowAnswer(q, fb, actions);
  });
  actions.appendChild(check);
  box.appendChild(actions);
  box.appendChild(fb);
  return box;
}

/* --- fill the blank --- */
function renderQuestionBlank(ch, q, i) {
  const box = document.createElement("div");
  box.className = "question";
  box.innerHTML = '<div class="q-text">' + esc(t("q_label", { n: fmtNum(i + 1) })) +
    " " + q.question + "</div>";
  applyDir(box.querySelector(".q-text"), !!q.__fa);
  const input = document.createElement("input");
  input.className = "blank";
  input.placeholder = t("blank_placeholder");
  box.appendChild(input);

  const fb = feedbackBox(q);
  const actions = document.createElement("div");
  actions.className = "answer-actions";
  const check = document.createElement("button");
  check.className = "btn";
  check.textContent = t("check_btn");
  const doCheck = () => {
    const res = checkQuestion(q, input.value);
    fb.show(res.correct, res.explain);
    input.classList.add(res.correct ? "correct" : "wrong");
    setQuestionStatus(ch, i, res.correct ? "ok" : "missed");
    check.disabled = true;
    addShowAnswer(q, fb, actions);
  };
  check.addEventListener("click", doCheck);
  input.addEventListener("keydown", (e) => {
    if (e.key === "Enter" && !check.disabled) doCheck();
  });
  actions.appendChild(check);
  box.appendChild(actions);
  box.appendChild(fb);
  return box;
}

/* --- write the code (fill the blanks in code) --- */
function renderQuestionCodefill(ch, q, i) {
  const box = document.createElement("div");
  box.className = "question";
  box.innerHTML = '<div class="q-text">' + esc(t("q_label", { n: fmtNum(i + 1) })) +
    " " + q.question + "</div>";
  applyDir(box.querySelector(".q-text"), !!q.__fa);

  const pre = document.createElement("div");
  pre.className = "codefill";
  const inputs = [];
  q.code.forEach((item) => {
    if (typeof item === "string") {
      pre.appendChild(document.createTextNode(item));
    } else {
      const inp = document.createElement("input");
      inp.className = "blank";
      inp.placeholder = item.blank;
      inp.title = t("hint_prefix") + (item.hint || item.blank);
      inputs.push(inp);
      pre.appendChild(inp);
    }
    pre.appendChild(document.createTextNode("\n"));
  });
  box.appendChild(pre);

  const fb = feedbackBox(q);
  const actions = document.createElement("div");
  actions.className = "answer-actions";
  const check = document.createElement("button");
  check.className = "btn";
  check.textContent = t("check_btn");
  const doCheck = () => {
    const res = checkQuestion(q, inputs.map((x) => x.value));
    fb.show(res.correct, res.explain);
    inputs.forEach((x) =>
      x.classList.add(x.value.trim() ? (res.correct ? "correct" : "wrong") : "wrong"));
    setQuestionStatus(ch, i, res.correct ? "ok" : "missed");
    check.disabled = true;
    addShowAnswer(q, fb, actions);
  };
  check.addEventListener("click", doCheck);
  actions.appendChild(check);
  box.appendChild(actions);
  box.appendChild(fb);
  return box;
}

/* --- order the lines --- */
function renderQuestionOrder(ch, q, i) {
  const box = document.createElement("div");
  box.className = "question";
  box.innerHTML = '<div class="q-text">' + esc(t("q_label", { n: fmtNum(i + 1) })) +
    " " + q.question + "</div>" +
    '<div class="tryit-label">' + esc(t("order_instruction")) + "</div>";
  applyDir(box.querySelector(".q-text"), !!q.__fa);

  const idxs = q.lines.map((_, x) => x).sort(() => Math.random() - 0.5);
  const picked = [];
  const chipByOrig = {};
  const chips = idxs.map((orig) => {
    const chip = document.createElement("span");
    chip.className = "order-chip";
    chip.textContent = q.lines[orig];
    applyDir(chip, !!q.__fa);
    chipByOrig[orig] = chip;
    chip.addEventListener("click", () => {
      const pos = picked.indexOf(orig);
      if (pos === -1) {
        picked.push(orig);
        chip.classList.add("picked");
        chip.classList.add("used");
        chip.dataset.pos = picked.length;
      } else {
        picked.splice(pos, 1);
        chip.classList.remove("picked");
        chip.classList.remove("used");
        picked.forEach((o, k) => { chipByOrig[o].dataset.pos = k + 1; });
      }
    });
    box.appendChild(chip);
    return chip;
  });

  const fb = feedbackBox(q);
  const actions = document.createElement("div");
  actions.className = "answer-actions";
  const check = document.createElement("button");
  check.className = "btn";
  check.textContent = t("check_btn");
  check.addEventListener("click", () => {
    if (picked.length !== q.lines.length) {
      toast(t("pick_lines", { n: fmtNum(q.lines.length) }));
      return;
    }
    const res = checkQuestion(q, picked);
    fb.show(res.correct, res.explain);
    setQuestionStatus(ch, i, res.correct ? "ok" : "missed");
    check.disabled = true;
    picked.forEach((orig, pos) => {
      const c = chipByOrig[orig];
      c.classList.remove("picked", "used");
      c.classList.add(orig === pos ? "correct" : "wrong");
    });
    addShowAnswer(q, fb, actions);
  });
  actions.appendChild(check);
  box.appendChild(actions);
  box.appendChild(fb);
  return box;
}

function addShowAnswer(q, fb, actions) {
  if (actions.querySelector(".show-answer")) return;
  const btn = document.createElement("button");
  btn.className = "btn secondary show-answer";
  btn.textContent = t("show_answer");
  btn.addEventListener("click", () => showAnswer(q, fb));
  actions.appendChild(btn);
}

function renderQuestion(ch, q, i) {
  if (q.type === "mc") return renderQuestionMC(ch, q, i);
  if (q.type === "blank") return renderQuestionBlank(ch, q, i);
  if (q.type === "codefill") return renderQuestionCodefill(ch, q, i);
  if (q.type === "order") return renderQuestionOrder(ch, q, i);
  const box = document.createElement("div");
  box.className = "question";
  box.textContent = "Unknown question type: " + q.type;
  return box;
}

/* ============================== playground ============================= */

/* The Playground opens in THIS tab (never a popup): the playground's
   "Back to lessons" button — or the browser back button — returns to the
   exact place you left, because the position is saved on every render. */
function openPlayground() {
  const page = activeSubject === "c" ? "playground-c.html"
    : activeSubject === "html" ? "playground-html.html"
    : activeSubject === "css" ? "playground-css.html"
    : activeSubject === "js" ? "playground-js.html"
    : activeSubject === "cpp" ? "playground-cpp.html"
    : "playground.html";
  window.location.href = page;
}

/* remember where the reader is, so the playground round-trip (and any
   reload) lands back on the same lesson */
const POSITION_KEY = "pytutor-position-v1";
function savePosition() {
  try {
    localStorage.setItem(POSITION_KEY, JSON.stringify({
      subject: activeSubject,
      chapter: state.chapter,
      step: state.step,
    }));
  } catch (e) { /* storage blocked — worst case: course reopens at ch.1 */ }
}

function restorePosition() {
  try {
    const pos = JSON.parse(localStorage.getItem(POSITION_KEY) || "null");
    if (!pos || pos.subject !== activeSubject) return;
    const ch = Number(pos.chapter);
    if (!Number.isInteger(ch) || ch < 0 || ch >= chapters.length) return;
    const st = pos.step || {};
    const len = chapters[ch].lessons.length;
    state.chapter = ch;
    state.step = st.kind === "quiz"
      ? { kind: "quiz", idx: len }
      : { kind: "lesson", idx: Math.min(Math.max(0, Math.trunc(st.idx) || 0), len - 1) };
    sidebarOpenChapter = ch;
  } catch (e) { /* corrupt position — start at chapter 1 */ }
}

/* ============================== toast ================================== */

let toastTimer = null;
function toast(msg) {
  const tEl = $("toast");
  tEl.textContent = msg;
  tEl.classList.add("show");
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => tEl.classList.remove("show"), 2600);
}

function updateQuizStatus() {
  const el = $("quiz-status");
  if (!el) return;
  const ch = currentChapter();
  const answered = quizAnsweredCount(ch);
  const total = ch.quiz.length;
  if (answered >= total) {
    el.textContent = t("status_all", { n: fmtNum(total) });
    el.classList.add("all");
  } else {
    el.textContent = t("status_partial", {
      answered: fmtNum(answered),
      total: fmtNum(total),
    });
    el.classList.remove("all");
  }
}

/* ============================== subjects =============================== */
/* The main menu lets the learner pick WHICH language to learn. Six tutors
   have room here; Python and C ship full content — the others preview in
   the orbital menu and answer with a friendly "coming soon". */

const SUBJECT_KEY = "pytutor-subject-v1";
let courseActive = false;        // the course view is on screen
let activeSubject = "python";    // subject of the loaded course
let chooserChosen = "python";    // selection inside the chooser overlay
let previewSubject = "python";   // what the big circle is morphing/showing

function courseDataFor(id) {
  if (id === "python") {
    return (window.COURSE_DATA &&
            Array.isArray(window.COURSE_DATA.chapters) &&
            window.COURSE_DATA.chapters.length) ? window.COURSE_DATA : null;
  }
  if (id === "c") {
    return (window.COURSE_DATA_C &&
            Array.isArray(window.COURSE_DATA_C.chapters) &&
            window.COURSE_DATA_C.chapters.length) ? window.COURSE_DATA_C : null;
  }
  if (id === "html") {
    return (window.COURSE_DATA_HTML &&
            Array.isArray(window.COURSE_DATA_HTML.chapters) &&
            window.COURSE_DATA_HTML.chapters.length) ? window.COURSE_DATA_HTML : null;
  }
  if (id === "css") {
    return (window.COURSE_DATA_CSS &&
            Array.isArray(window.COURSE_DATA_CSS.chapters) &&
            window.COURSE_DATA_CSS.chapters.length) ? window.COURSE_DATA_CSS : null;
  }
  if (id === "js") {
    return (window.COURSE_DATA_JS &&
            Array.isArray(window.COURSE_DATA_JS.chapters) &&
            window.COURSE_DATA_JS.chapters.length) ? window.COURSE_DATA_JS : null;
  }
  if (id === "cpp") {
    return (window.COURSE_DATA_CPP &&
            Array.isArray(window.COURSE_DATA_CPP.chapters) &&
            window.COURSE_DATA_CPP.chapters.length) ? window.COURSE_DATA_CPP : null;
  }
  return null;
}

/* Load a subject's course: swap the chapter data, reset navigation state
   and re-theme the page (data-subject drives the CSS variables). */
function activateSubject(id) {
  const data = courseDataFor(id);
  if (!data) return false;
  if (activeSubject !== id || chapters.length !== data.chapters.length) {
    chapters = data.chapters;
    state = { chapter: 0, step: { kind: "lesson", idx: 0 } };
    sidebarOpenChapter = 0;
    sidebarEntranceShown = false; // replay the sidebar entrance
  }
  activeSubject = id;
  document.documentElement.dataset.subject = id;
  updateSubjectBrand();
  applyStaticText();
  return true;
}

/* Branding that follows the subject: titles, logo and favicon. The logo
   spans get the subject's REAL vector icon (the same art as the menu),
   not an emoji. */
function updateSubjectBrand() {
  const s = subjectById(activeSubject);
  document.querySelectorAll("[data-subject-brand]").forEach((el) => {
    el.textContent = t("brand_name");
  });
  document.querySelectorAll("[data-subject-logo]").forEach((el) => {
    const size = el.classList.contains("welcome-emoji") ? 56 : 34;
    el.innerHTML = '<svg viewBox="0 0 100 100" style="width:' + size +
      'px;height:' + size + 'px;display:block;direction:ltr" aria-hidden="true">' +
      s.inner("lg-" + activeSubject) + "</svg>";
  });
  const favicon = document.querySelector("link[rel='icon']");
  if (favicon) {
    favicon.href = "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'%3E%3Ctext y='.9em' font-size='90'%3E" +
      encodeURIComponent(s.emoji || "📘") + "%3C/text%3E%3C/svg%3E";
  }
}

/* --- vector icons (hand-drawn, 100×100 viewBox, no image files) -------- */

const PY_ICON_PATH = "M54.9 4.5c-4.2-.02-8 .37-11.4 1.1-9.3 2-11 6.2-11 13.9v9h22v3h-22-8.3c-6.4 0-12 3.9-13.8 11.3-2 8.4-2.1 13.7 0 22.5 1.6 6.6 5.3 11.3 11.7 11.3h7.6v-10.8c0-7.4 6.4-13.9 13.8-13.9h22c6.1 0 11-5 11-11.2v-21c0-6-5-10.5-11-11.5-4.5-.75-9.2-1.1-13.4-1.1zM42 11.6c2.6 0 4.7 2.1 4.7 4.7 0 2.6-2.1 4.7-4.7 4.7-2.6 0-4.7-2.1-4.7-4.7 0-2.6 2.1-4.7 4.7-4.7z";

function svgIcon(inner) {
  return '<svg viewBox="0 0 100 100" aria-hidden="true" style="direction:ltr">' +
    inner + "</svg>";
}

function pyInner() {
  return '<path d="' + PY_ICON_PATH + '" fill="#3776ab"/>' +
    '<path d="' + PY_ICON_PATH + '" fill="#ffd43b" transform="rotate(180 50 50)"/>' +
    '<circle cx="42" cy="16.3" r="4.7" fill="#fff"/>' +
    '<circle cx="58" cy="83.7" r="4.7" fill="#fff"/>';
}

function gradDefs(uid, c1, c2) {
  return '<defs><linearGradient id="sg-' + uid + '" x1="0" y1="0" x2="0" y2="1">' +
    '<stop offset="0" stop-color="' + c1 + '"/>' +
    '<stop offset="1" stop-color="' + c2 + '"/></linearGradient></defs>';
}

function hexInner(text, c1, c2, uid, fontSize) {
  return gradDefs(uid, c1, c2) +
    '<path d="M32 5h36l27 45-27 45H32L5 50z" fill="url(#sg-' + uid + ')"/>' +
    '<text x="50" y="56" text-anchor="middle" dominant-baseline="middle" ' +
    'font-family="Segoe UI, Arial, sans-serif" font-weight="800" ' +
    'font-size="' + fontSize + '" fill="#fff">' + text + "</text>";
}

function shieldInner(text, c1, c2, uid) {
  // spans nearly the full viewBox and sits optically centred, so the
  // shield reads as large as the hexagon/square icons
  return gradDefs(uid, c1, c2) +
    '<path d="M12 4h76l-7 66L50 92l-31-22z" fill="url(#sg-' + uid + ')"/>' +
    '<text x="50" y="37" text-anchor="middle" dominant-baseline="middle" ' +
    'font-family="Segoe UI, Arial, sans-serif" font-weight="800" ' +
    'font-size="40" fill="#fff">' + text + "</text>";
}

function jsInner() {
  return '<rect x="14" y="14" width="72" height="72" rx="12" fill="#f7df1e"/>' +
    '<text x="52" y="55" text-anchor="middle" dominant-baseline="middle" ' +
    'font-family="Segoe UI, Arial, sans-serif" font-weight="800" ' +
    'font-size="30" fill="#263238">JS</text>';
}

const SUBJECTS = [
  { id: "python", en: "Python", fa: "پایتون", emoji: "🐍",
    c1: "#3776ab", c2: "#ffd43b",
    blob: { r: [130, 124, 128, 132, 124, 128, 130, 124], rot: 0.12 },
    grad: ["#0e1f2c", "#16364d", "#1d4d6b", "#2a5a82"], inner: pyInner, soon: false },
  { id: "c", en: "C", fa: "C", emoji: "🔷",
    c1: "#283593", c2: "#7986cb",
    blob: { r: [136, 120, 136, 120, 136, 120, 136, 120], rot: Math.PI / 8 },
    grad: ["#12154d", "#283593", "#1a237e", "#1e2670"], inner: (u) => hexInner("C", "#283593", "#7986cb", u, 40), soon: false },
  { id: "cpp", en: "C++", fa: "C++", emoji: "🔷",
    c1: "#00599c", c2: "#004482",
    blob: { r: [140, 116, 138, 118, 140, 116, 138, 118], rot: Math.PI / 8 },
    grad: ["#00305a", "#00599c", "#0077cc", "#004482"], inner: (u) => hexInner("C++", "#00599c", "#004482", u, 28), soon: false },
  { id: "html", en: "HTML", fa: "HTML", emoji: "🛡️",
    c1: "#e44d26", c2: "#f16529",
    blob: { r: [120, 126, 130, 136, 144, 130, 120, 116], rot: -Math.PI / 2 },
    grad: ["#8f2f12", "#e44d26", "#f16529", "#c73c1a"], inner: (u) => shieldInner("5", "#e44d26", "#f16529", u), soon: false },
  { id: "css", en: "CSS", fa: "CSS", emoji: "🛡️",
    c1: "#1572b6", c2: "#33a9dc",
    blob: { r: [122, 126, 130, 132, 140, 130, 126, 122], rot: -Math.PI / 2 },
    grad: ["#0a3c63", "#1572b6", "#33a9dc", "#0d5590"], inner: (u) => shieldInner("3", "#1572b6", "#33a9dc", u), soon: false },
  { id: "js", en: "JavaScript", fa: "جاوااسکریپت", emoji: "🟨",
    c1: "#f7df1e", c2: "#323330",
    blob: { r: [138, 120, 138, 120, 138, 120, 138, 120], rot: Math.PI / 4 },
    grad: ["#1a1a12", "#323330", "#f7df1e", "#2b2b20"], inner: jsInner, soon: false },
];

function subjectById(id) {
  return SUBJECTS.find((s) => s.id === id) || SUBJECTS[0];
}
function subjName(s) {
  return (lang === "fa" && s.fa) ? s.fa : s.en;
}
function getSavedSubject() {
  try { return localStorage.getItem(SUBJECT_KEY) || ""; } catch (e) { return ""; }
}
function saveSubject(id) {
  try { localStorage.setItem(SUBJECT_KEY, id); } catch (e) { /* non-fatal */ }
}

/* --- the big circle: a living blob whose SHAPE morphs per language ----- */
/* The blob is a closed 8-point Catmull-Rom path; every language owns its
   own radius signature (round like Python, hexed like C, shielded like
   HTML…). Each frame the current radii/rotation/colors ease toward the
   previewed language, so switching icons genuinely morphs the shape. */

function hexToRgb(h) {
  const n = parseInt(h.slice(1), 16);
  return [(n >> 16) & 255, (n >> 8) & 255, n & 255];
}
function lerp(a, b, k) { return a + (b - a) * k; }
function rgbCss(c) { return "rgb(" + c.map((v) => Math.round(v)).join(",") + ")"; }

const blobState = {
  cur: SUBJECTS[0].blob.r.slice(),
  tgt: SUBJECTS[0].blob.r.slice(),
  rot: SUBJECTS[0].blob.rot,
  tgtRot: SUBJECTS[0].blob.rot,
  c1: hexToRgb(SUBJECTS[0].c1), c2: hexToRgb(SUBJECTS[0].c2),
  t1: hexToRgb(SUBJECTS[0].c1), t2: hexToRgb(SUBJECTS[0].c2),
  raf: 0,
};

function blobPoints(radii, rot, t) {
  const cx = 180, cy = 180, pts = [];
  for (let i = 0; i < 8; i++) {
    const a = rot + i * (Math.PI / 4);
    const r = radii[i] + Math.sin(t / 900 + i * 1.7) * 2.6;
    pts.push([cx + r * Math.cos(a), cy + r * Math.sin(a)]);
  }
  let d = "M" + pts[0][0].toFixed(1) + " " + pts[0][1].toFixed(1);
  for (let i = 0; i < 8; i++) {
    const p0 = pts[(i + 7) % 8], p1 = pts[i], p2 = pts[(i + 1) % 8], p3 = pts[(i + 2) % 8];
    const c1 = [p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6];
    const c2 = [p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6];
    d += "C" + c1[0].toFixed(1) + " " + c1[1].toFixed(1) + " " +
         c2[0].toFixed(1) + " " + c2[1].toFixed(1) + " " +
         p2[0].toFixed(1) + " " + p2[1].toFixed(1);
  }
  return d + "Z";
}

function blobTick(t) {
  const b = blobState, k = 0.06; // slow enough to read as a real morph
  for (let i = 0; i < 8; i++) b.cur[i] = lerp(b.cur[i], b.tgt[i], k);
  b.rot = lerp(b.rot, b.tgtRot, k);
  for (let i = 0; i < 3; i++) {
    b.c1[i] = lerp(b.c1[i], b.t1[i], k);
    b.c2[i] = lerp(b.c2[i], b.t2[i], k);
  }
  const path = $("blob-path");
  if (!path) { blobState.raf = 0; return; }
  path.setAttribute("d", blobPoints(b.cur, b.rot, t));
  $("blob-stop1").setAttribute("stop-color", rgbCss(b.c1));
  $("blob-stop2").setAttribute("stop-color", rgbCss(b.c2));
  blobState.raf = requestAnimationFrame(blobTick);
}

function totalQuestions() {
  return chapters.reduce((n, ch) => n + ch.quiz.length, 0);
}

function subjectChapterCount(id) {
  const data = courseDataFor(id);
  return data ? data.chapters.length : 0;
}

function subjectQuestionCount(id) {
  const data = courseDataFor(id);
  return data
    ? data.chapters.reduce((n, ch) => n + ch.quiz.length, 0) : 0;
}

function blobTag(s) {
  if (!s.soon) {
    return t("ready_tag", {
      chapters: fmtNum(subjectChapterCount(s.id)),
      questions: fmtNum(subjectQuestionCount(s.id)),
    });
  }
  return t("coming_soon_tag");
}

function blobIconSvg(s, uid) {
  // nested <svg> places the 100×100 icon inside the 360×360 blob viewBox,
  // centred slightly above the blob's middle (name/tag sit below it);
  // sized so even the wide-topped shields stay inside the blob edge
  return '<svg viewBox="0 0 100 100" x="114" y="75" width="132" height="132" ' +
    'style="direction:ltr" aria-hidden="true">' + s.inner(uid) + "</svg>";
}

function blobMeta(s) {
  return '<h3 class="blob-name">' + esc(subjName(s)) + "</h3>" +
    '<p class="blob-tag">' + esc(blobTag(s)) + "</p>";
}

/* shape-shift: through a gooey SVG filter the old icon MELTS into the
   centre while the new one GROWS out of it — both stay fully opaque, so
   it reads as one liquid shape transforming, never a crossfade */
let morphTimer = null;
function setBlobContent(prev, s, animate) {
  const stage = $("icon-stage");
  const meta = $("blob-content");
  if (!stage || !meta) return;
  if (!animate) {
    stage.innerHTML = "<g>" + blobIconSvg(s, "bc") + "</g>";
    meta.innerHTML = blobMeta(s);
    return;
  }
  stage.innerHTML =
    '<g class="icon-melt" filter="url(#goo-fx)">' + blobIconSvg(prev, "bco") + "</g>" +
    '<g class="icon-grow" filter="url(#goo-fx)">' + blobIconSvg(s, "bci") + "</g>";
  meta.innerHTML = blobMeta(s);
  meta.classList.remove("meta-swap");
  void meta.offsetWidth;
  meta.classList.add("meta-swap");
  clearTimeout(morphTimer);
  morphTimer = setTimeout(() => {
    if (previewSubject === s.id) {
      stage.innerHTML = "<g>" + blobIconSvg(s, "bc") + "</g>";
    }
  }, 1000);
}

function setPreview(id, animate) {
  const prev = subjectById(previewSubject);
  const s = subjectById(id);
  previewSubject = id;
  blobState.tgt = s.blob.r.slice();
  blobState.tgtRot = s.blob.rot;
  blobState.t1 = hexToRgb(s.c1);
  blobState.t2 = hexToRgb(s.c2);
  setBlobContent(prev, s, animate);
}

function updateNodeActive() {
  document.querySelectorAll("#orbit .lang-node").forEach((n) => {
    n.classList.toggle("active", n.dataset.id === chooserChosen);
  });
}

function updateStartButton() {
  const btn = $("subject-start");
  const s = subjectById(chooserChosen);
  if (!s.soon) {
    btn.disabled = false;
    btn.textContent = (courseActive && activeSubject === s.id)
      ? t("continue_with", { name: subjName(s) })
      : t("start_with", { name: subjName(s) });
    btn.style.setProperty("--sc1", s.c1);
    btn.style.setProperty("--sc2", s.c2);
  } else {
    btn.disabled = true;
    btn.textContent = t("coming_soon_btn", { name: subjName(s) });
    btn.style.setProperty("--sc1", "#46586a");
    btn.style.setProperty("--sc2", "#37475a");
  }
}

function renderChooser() {
  const orbit = $("orbit");
  orbit.querySelectorAll(".lang-node").forEach((n) => n.remove());
  const wrap = orbit.closest(".orbit-wrap");
  const W = (wrap && wrap.clientWidth) || 560;
  const R = W / 2 - 28; // keep a clear gap between ring and blob edge
  const nodeR = W < 620
    ? Math.max(38, Math.round(W * 0.115))   // phones: smaller bubbles...
    : Math.max(46, Math.round(W * 0.13));   // desktop: unchanged sizing
  SUBJECTS.forEach((s, i) => {
    const ang = -Math.PI / 2 + i * (2 * Math.PI / SUBJECTS.length);
    const x = W / 2 + R * Math.cos(ang);
    const y = W / 2 + R * Math.sin(ang);
    const node = document.createElement("button");
    node.type = "button";
    node.className = "lang-node" + (s.soon ? " soon" : "");
    node.dataset.id = s.id;
    node.style.left = (100 * x / W) + "%";
    node.style.top = (100 * y / W) + "%";
    node.style.setProperty("--c", s.c1);
    node.innerHTML =
      '<span class="node-circle" style="width:' + nodeR + 'px;height:' + nodeR + 'px">' +
      svgIcon(s.inner("n" + i)) +
      (s.soon ? '<span class="soon-chip">' + esc(t("soon_chip")) + "</span>" : "") +
      "</span>" +
      '<span class="node-label">' + esc(subjName(s)) + "</span>";
    node.addEventListener("click", () => chooseSubject(s.id));
    orbit.appendChild(node);
  });
  updateNodeActive();
}

function chooseSubject(id) {
  const s = subjectById(id);
  chooserChosen = id;
  // the menu itself adopts the chosen language's colors — before entering
  const menu = $("subject");
  menu.style.background =
    "linear-gradient(-45deg, " + s.grad.join(", ") + ")";
  menu.style.backgroundSize = "400% 400%";
  updateNodeActive();
  updateStartButton();
  setPreview(id, true);
  if (s.soon) toast(t("soon_toast", { name: subjName(s) }));
}

function openChooser() {
  chooserChosen = courseActive ? activeSubject : "python";
  renderChooser();
  setPreview(chooserChosen, false);
  updateStartButton();
  openWelcomeOverlay($("subject"));
  if (!blobState.raf) blobState.raf = requestAnimationFrame(blobTick);
}

function closeChooser() {
  $("subject").classList.remove("show", "entering");
  if (blobState.raf) {
    cancelAnimationFrame(blobState.raf);
    blobState.raf = 0;
  }
}

function subjectStart() {
  const s = subjectById(chooserChosen);
  if (s.soon) {
    toast(t("soon_toast", { name: subjName(s) }));
    return;
  }
  if (!activateSubject(s.id)) {
    toast(t("soon_toast", { name: subjName(s) }));
    return;
  }
  saveSubject(s.id);
  const firstTime = !courseActive;
  closeChooser();
  enterCourse(firstTime);
}

function enterCourse(greet) {
  courseActive = true;
  document.body.classList.add("course-active");
  $("welcome").classList.remove("show", "entering");
  closeChooser();
  renderSidebar();
  restorePosition(); // return to the lesson you were reading (playground round-trip)
  const deep = pendingDeepLink;
  pendingDeepLink = null;
  if (deep && deep.subject === activeSubject) {
    const ci = Math.min(deep.chapter, chapters.length - 1);
    state.chapter = ci;
    state.step = deep.quiz
      ? { kind: "quiz", idx: chapters[ci].lessons.length }
      : { kind: "lesson", idx: Math.min(deep.idx, chapters[ci].lessons.length - 1) };
    sidebarOpenChapter = ci;
  }
  renderView();
  if (greet) {
    toast(t("subject_started", {
      subj: subjName(subjectById(activeSubject)),
      name: displayName(),
    }));
  }
}

/* ============================== welcome ================================ */

function openWelcomeOverlay(overlay) {
  overlay.classList.remove("entering");
  void overlay.offsetWidth;
  overlay.classList.add("entering");
  overlay.classList.add("show");
}

function showWelcome() {
  const overlay = $("welcome");
  openWelcomeOverlay(overlay);
  const input = $("name-input");
  const start = $("name-start");
  const doStart = () => {
    const n = input.value.trim();
    if (!n) {
      input.classList.add("shake");
      setTimeout(() => input.classList.remove("shake"), 450);
      input.focus();
      return;
    }
    saveUserName(n);
    overlay.classList.remove("show");
    overlay.classList.remove("entering");
    input.value = "";
    const saved = getSavedSubject();
    if (courseDataFor(saved)) {
      activateSubject(saved);
      enterCourse(false);
      toast(t("welcome_toast", { name: n }));
    } else {
      openChooser();
    }
  };
  start.addEventListener("click", doStart);
  input.addEventListener("keydown", (e) => {
    if (e.key === "Enter") doStart();
  });
  setTimeout(() => input.focus(), 120);
}

function setupNameUi() {
  $("change-name").addEventListener("click", () => {
    const input = $("name-input");
    input.value = getUserName();
    openWelcomeOverlay($("welcome"));
    setTimeout(() => { input.focus(); input.select(); }, 300);
  });
  $("home-btn").addEventListener("click", openChooser);
  $("subject-start").addEventListener("click", subjectStart);
}

/* ============================== boot =================================== */

/* mobile drawer: on phones the chapter sidebar slides in over the page
   instead of sitting above it — the floating button and backdrop toggle it,
   and picking any title closes it (see renderView). */
function setDrawer(open) {
  const btn = document.getElementById("drawer-btn");
  if (!btn) return;
  document.body.classList.toggle("drawer-open", open);
  btn.setAttribute("aria-expanded", String(open));
  const ic = btn.querySelector(".drawer-ic");
  if (ic) ic.textContent = open ? "✕" : "☰";
}

/* the programming-language chips at the top of the sidebar: switch subject
   without leaving the course. The UI language (FA/EN) lives at the sidebar
   footer, deliberately kept separate from the educational language. */
function renderSubjectChips() {
  const bar = document.getElementById("subject-chips");
  if (!bar) return;
  bar.innerHTML = "";
  SUBJECTS.forEach((s) => {
    const chip = document.createElement("button");
    chip.type = "button";
    chip.className = "subject-chip" + (s.id === activeSubject ? " active" : "");
    chip.dataset.subject = s.id;
    chip.style.setProperty("--c", s.c1);
    chip.title = subjName(s);
    chip.innerHTML =
      '<span class="chip-ic">' + svgIcon(s.inner("chip-" + s.id)) + "</span>" +
      '<span class="chip-name">' + esc(subjName(s)) + "</span>";
    chip.addEventListener("click", () => { triggerHaptic(); switchSubject(s.id); });
    bar.appendChild(chip);
  });
}

function switchSubject(id) {
  if (!courseActive) { chooseSubject(id); return; }
  if (id === activeSubject) return;
  if (!activateSubject(id)) return;
  saveSubject(id);
  renderSidebar();
  restorePosition();
  renderView();
  renderSubjectChips();
}

let pendingDeepLink = null;

/* -------- haptic feedback (native-feeling taps on mobile) -------- */
function triggerHaptic(ms) {
  if (navigator.vibrate) {
    try { navigator.vibrate(ms || 10); } catch (e) { /* unsupported */ }
  }
}

/* -------- lesson difficulty: early chapters are the basics -------- */
function difficultyOf(chapterIdx) {
  const total = chapters.length;
  const r = total <= 1 ? 0 : chapterIdx / (total - 1);
  if (r <= 0.34) return { key: "diff_beg", cls: "beg", dot: "🟢" };
  if (r <= 0.67) return { key: "diff_int", cls: "int", dot: "🟡" };
  return { key: "diff_adv", cls: "adv", dot: "🔴" };
}

/* -------- per-lesson "read" tracking (study checklist) -------- */
const READ_KEY = "pytutor-read-v1";
function readStore() {
  try { return JSON.parse(localStorage.getItem(READ_KEY) || "{}") || {}; }
  catch (e) { return {}; }
}
function markLessonRead(chId, idx) {
  const store = readStore();
  const set = store[activeSubject] || (store[activeSubject] = {});
  const key = chId + "/" + idx;
  if (set[key]) return;
  set[key] = 1;
  try { localStorage.setItem(READ_KEY, JSON.stringify(store)); } catch (e) {}
  const tick = document.querySelector(
    '.sub-item[data-ch="' + chapters.findIndex((c) => c.id === chId) +
    '"][data-idx="' + idx + '"] .read-tick');
  if (tick) tick.textContent = "✔";
  updateReadProgressLine();
}
function countReadLessons() {
  const set = readStore()[activeSubject] || {};
  let n = 0;
  chapters.forEach((ch) => ch.lessons.forEach((_, j) => {
    if (set[ch.id + "/" + j]) n++;
  }));
  return n;
}
function updateReadProgressLine() {
  const el = $("read-progress");
  if (!el) return;
  const total = chapters.reduce((n, ch) => n + ch.lessons.length, 0);
  el.textContent = t("read_progress",
    { read: fmtNum(countReadLessons()), total: fmtNum(total) });
}

/* ---- scroll reading-progress bar (the lessons pane is the scroller) ---- */
function updateScrollProgress() {
  const bar = document.getElementById("scroll-progress");
  if (!bar) return;
  const main = $("main");
  const max = main.scrollHeight - main.clientHeight;
  bar.style.width = (max > 0 ? Math.min(100, 100 * main.scrollTop / max) : 100) + "%";
}

/* ---- fullscreen code modal (opened from the code meta-bar) ---- */
let codeModalSource = null;
function openCodeModal(pre, langName) {
  const modal = document.getElementById("code-modal");
  codeModalSource = pre;
  $("cm-pre").textContent = pre.textContent;
  $("cm-lang").textContent = langName;
  modal.hidden = false;
}
function closeCodeModal() {
  const modal = document.getElementById("code-modal");
  if (modal) modal.hidden = true;
  codeModalSource = null;
}

/* ---------------- deep links: #/subject/chapter/lesson ---------------- */
function updateHash() {
  if (!courseActive) return;
  const h = "#/" + activeSubject + "/" + state.chapter + "/" +
    (state.step.kind === "quiz" ? "q" : state.step.idx);
  if (location.hash !== h) history.replaceState(null, "", h);
}
function parseHash() {
  const m = location.hash.match(/^#\/([a-z]+)\/(\d+)\/(q|\d+)$/i);
  if (!m) return null;
  return { subject: m[1].toLowerCase(), chapter: +m[2],
           quiz: m[3] === "q", idx: +m[3] || 0 };
}

/* ---------------- bookmarks (localStorage, no account) ---------------- */
const BOOKMARK_KEY = "pytutor-bookmarks-v1";
function bookmarkStore() {
  try { return JSON.parse(localStorage.getItem(BOOKMARK_KEY) || "{}") || {}; }
  catch (e) { return {}; }
}
function isBookmarked(subj, chId, idx) {
  const list = bookmarkStore()[subj] || [];
  return list.some((b) => b.c === chId && b.i === idx);
}
function toggleBookmark(chId, idx) {
  const store = bookmarkStore();
  const list = store[activeSubject] || (store[activeSubject] = []);
  const at = list.findIndex((b) => b.c === chId && b.i === idx);
  const added = at === -1;
  if (added) list.push({ c: chId, i: idx }); else list.splice(at, 1);
  try { localStorage.setItem(BOOKMARK_KEY, JSON.stringify(store)); } catch (e) {}
  renderBookmarks();
  return added;
}
function renderBookmarks() {
  const box = document.getElementById("bookmarks-box");
  const listEl = document.getElementById("bookmarks-list");
  if (!box || !listEl) return;
  const store = bookmarkStore();
  listEl.innerHTML = "";
  let any = false;
  Object.keys(store).forEach((subj) => {
    (store[subj] || []).forEach((b) => {
      const data = courseDataFor(subj);
      const ch = data ? data.chapters.find((c) => c.id === b.c) : null;
      if (!ch || !ch.lessons[b.i]) return;
      any = true;
      const sub = subjectById(subj);
      const item = document.createElement("button");
      item.type = "button";
      item.className = "bm-item" + (subj === activeSubject ? " current" : "");
      item.innerHTML =
        '<span class="bm-subj" style="--c:' + sub.c1 + '">' + esc(subjName(sub)) +
        '</span><span class="bm-title">' + esc(ch.lessons[b.i].title) + "</span>";
      item.addEventListener("click", () => {
        if (subj !== activeSubject) switchSubject(subj);
        goToStep(data.chapters.findIndex((c) => c.id === b.c), "lesson", b.i);
        if (window.matchMedia("(max-width: 760px)").matches) setDrawer(true);
      });
      listEl.appendChild(item);
    });
  });
  box.hidden = !any;
}

/* ---------------- command palette (Ctrl+K, /) ---------------- */
let palItems = [], palSel = 0;

function palOpen() {
  const p = $("palette");
  if (!p) return;
  p.hidden = false;
  const input = $("pal-input");
  input.value = "";
  buildPalResults("");
  input.focus();
}
function palClose() {
  const p = $("palette");
  if (p) p.hidden = true;
}
function palRun(item) {
  palClose();
  if (item) item.run();
}
function buildPalResults(q, keepSel) {
  const prev = palItems[palSel] ? palItems[palSel].label : null;
  q = (q || "").trim().toLowerCase();
  const res = $("pal-results");
  res.innerHTML = "";
  palItems = [];
  palSel = 0;

  const cmds = [];
  cmds.push({ tag: "⌘", c: "#6b7f95",
    label: lang === "fa"
      ? "تغییر زبان رابط به " + (lang === "fa" ? "English" : "فارسی")
      : "Switch UI language to فارسی",
    run: () => toggleLang() });
  cmds.push({ tag: "⌘", c: "#6b7f95",
    label: lang === "fa" ? "حالت تمرکز" : "Focus mode",
    run: () => toggleZen() });
  cmds.push({ tag: "⌘", c: "#6b7f95",
    label: lang === "fa" ? "باز کردن Playground" : "Open Playground",
    run: () => openPlayground() });
  cmds.push({ tag: "⌘", c: "#6b7f95",
    label: lang === "fa" ? "منوی اصلی" : "Main menu",
    run: () => { const b = $("home-btn"); if (b) b.click(); } });

  const cmdHits = cmds.filter((c) => c.label.toLowerCase().includes(q));
  if (cmdHits.length) {
    const h = document.createElement("div");
    h.className = "pal-group";
    h.textContent = t("pal_commands");
    res.appendChild(h);
    cmdHits.forEach((c) => { c.kind = "cmd"; palItems.push(c); });
  }

  SUBJECTS.forEach((s) => {
    const data = courseDataFor(s.id);
    if (!data) return;
    const name = subjName(s);
    data.chapters.forEach((ch, ci) => {
      ch.lessons.forEach((lesson, li) => {
        const title = (lang === "fa" && lesson.title_fa) ? lesson.title_fa : lesson.title;
        const label = name + " — " + title;
        if (q && !label.toLowerCase().includes(q) &&
            !(ch.title || "").toLowerCase().includes(q)) return;
        palItems.push({ kind: "lesson", tag: name, c: s.c1, label,
          run: () => {
            if (s.id !== activeSubject) switchSubject(s.id);
            goToStep(ci, "lesson", li);
          } });
      });
    });
  });

  const shown = palItems.slice(0, 80);
  palItems = shown;
  if (keepSel && prev !== null) {
    const at = shown.findIndex((it) => it.label === prev);
    if (at !== -1) palSel = at; else palSel = 0;
  } else palSel = 0;
  shown.forEach((item, i) => {
    const el = document.createElement("button");
    el.type = "button";
    el.className = "pal-item" + (i === palSel ? " sel" : "");
    el.innerHTML = '<span class="pal-tag" style="--c:' + item.c + '">' +
      esc(item.tag) + "</span><span>" + esc(item.label) + "</span>";
    el.addEventListener("click", () => palRun(item));
    el.addEventListener("mousemove", () => {
      [...res.children].forEach((c) => c.classList.remove("sel"));
      el.classList.add("sel");
      palSel = i;
    });
    res.appendChild(el);
  });
  if (!palItems.length) {
    res.innerHTML = '<div class="pal-item">—</div>';
  }
}

function toggleLang() {
  applyLang(lang === "fa" ? "en" : "fa");
}

/* ---------------- syntax comparison modal ---------------- */
let cmpTopicId = null, cmpA = null, cmpB = null;
const CMP_LANGS = ["python", "c", "cpp", "js"];

function openCompare() {
  const modal = $("compare-modal");
  if (!modal) return;
  const topics = window.COMPARISON_TOPICS || [];
  if (!topics.some((t) => t.id === cmpTopicId)) cmpTopicId = topics[0] ? topics[0].id : null;
  if (cmpA === null) {
    cmpA = CMP_LANGS.indexOf(activeSubject) !== -1 ? activeSubject : "python";
    cmpB = cmpA === "python" ? "cpp" : "python";
  }
  renderCompare();
  modal.hidden = false;
}
function renderCompare() {
  const topics = window.COMPARISON_TOPICS || [];
  const topic = topics.find((t) => t.id === cmpTopicId) || topics[0];
  if (!topic) return;
  const top = $("cmp-topics");
  top.innerHTML = "";
  topics.forEach((t) => {
    const b = document.createElement("button");
    b.type = "button";
    b.className = "cmp-topic" + (t.id === cmpTopicId ? " sel" : "");
    b.textContent = (lang === "fa" && t.fa) ? t.fa : t.en;
    b.addEventListener("click", () => { cmpTopicId = t.id; renderCompare(); });
    top.appendChild(b);
  });
  $("cmp-topic-label").textContent =
    (lang === "fa" && topic.fa) ? topic.fa : topic.en;

  const renderPane = (paneId, sel) => {
    const pane = $(paneId);
    pane.innerHTML = "";
    const pills = document.createElement("div");
    pills.className = "cmp-pills";
    CMP_LANGS.forEach((lid) => {
      const sub = subjectById(lid);
      const p = document.createElement("button");
      p.type = "button";
      p.className = "cmp-pill" + (lid === sel ? " sel" : "");
      p.style.setProperty("--c", sub.c1);
      p.textContent = subjName(sub);
      p.addEventListener("click", () => {
        if (paneId === "cmp-pane-a") cmpA = lid; else cmpB = lid;
        renderCompare();
      });
      pills.appendChild(p);
    });
    pane.appendChild(pills);
    const pre = document.createElement("pre");
    pre.textContent = topic.code[sel] || "(not available)";
    pane.appendChild(pre);
  };
  renderPane("cmp-pane-a", cmpA);
  renderPane("cmp-pane-b", cmpB);
}

/* -------- swipe navigation + edge-swipe drawer (touch devices) -------- */
function initSwipeGestures() {
  let sx = 0, sy = 0, tracking = false, fromEdge = false;
  document.addEventListener("touchstart", (e) => {
    if (e.touches.length !== 1) { tracking = false; return; }
    const t = e.touches[0];
    sx = t.clientX; sy = t.clientY;
    const w = document.documentElement.clientWidth;
    fromEdge = sx <= 30 || sx >= w - 30;
    const bad = e.target.closest("pre, textarea, select, input, .code-copy, .code-expand, .html-preview");
    tracking = !bad;
  }, { passive: true });
  document.addEventListener("touchend", (e) => {
    if (!tracking) return;
    tracking = false;
    const t = e.changedTouches[0];
    const dx = t.clientX - sx, dy = t.clientY - sy;
    const drawerOpen = document.body.classList.contains("drawer-open");
    // edge-swipe opens the drawer; any inward swipe closes it
    if (drawerOpen) {
      if (Math.abs(dx) > 70 && Math.abs(dx) > Math.abs(dy) * 1.4) setDrawer(false);
      return;
    }
    if (fromEdge && Math.abs(dx) > 60 && Math.abs(dx) > Math.abs(dy) * 1.4) {
      setDrawer(true);
      return;
    }
    // horizontal swipe across the lesson navigates next / previous
    if (!courseActive || Math.abs(dx) < 90 || Math.abs(dy) > 60) return;
    if (e.target.closest(".tryit, .code-head")) return;
    const rtl = document.documentElement.getAttribute("dir") === "rtl";
    if ((dx < 0) !== rtl) nextStep(); else prevStep();
  }, { passive: true });
}

/* live filter: hide chapters/lessons that do not match the query */
function applyChapterFilter(q) {
  q = q.trim().toLowerCase();
  const heads = [...document.querySelectorAll("#chapter-list .category-head")];
  document.querySelectorAll("#chapter-list .chapter-item").forEach((btn) => {
    const i = +btn.dataset.ch;
    const ch = chapters[i];
    const sublist = btn.nextElementSibling;
    if (!sublist) return;
    const items = [...sublist.querySelectorAll(".sub-item")];
    if (!q) {
      btn.classList.remove("search-hide");
      sublist.classList.remove("search-hide");
      items.forEach((it) => it.classList.remove("search-hide"));
      heads.forEach((h) => h.classList.remove("search-hide"));
      syncSublists();
      return;
    }
    const chMatch = faChapterTitle(ch).toLowerCase().includes(q);
    let any = chMatch;
    items.forEach((it, j) => {
      const hit = chMatch ||
        it.textContent.toLowerCase().includes(q) ||
        (ch.lessons[j] && (ch.lessons[j].title || "").toLowerCase().includes(q));
      it.classList.toggle("search-hide", !hit);
      any = any || hit;
    });
    btn.classList.toggle("search-hide", !any && !chMatch);
    sublist.classList.toggle("search-hide", !any);
    if (any) { // searching shows every group's matches expanded
      btn.classList.add("open");
      btn.setAttribute("aria-expanded", "true");
      sublist.classList.add("open");
    }
  });
  heads.forEach((h) => {
    const cat = h.textContent.trim();
    const idx = sidebarCategories().findIndex((c) => t(c.key) === cat);
    if (idx === -1) return;
    const cat_ = sidebarCategories()[idx];
    let visible = false;
    for (let i = cat_.start - 1; i < cat_.end; i++) {
      const b = document.querySelector('#chapter-list .chapter-item[data-ch="' + i + '"]');
      if (b && !b.classList.contains("search-hide")) { visible = true; break; }
    }
    h.classList.toggle("search-hide", !visible);
  });
}

/* focus mode: only the lesson — sidebar, buttons and hints disappear */
function toggleZen(force) {
  const on = force === undefined ? !document.body.classList.contains("zen") : force;
  document.body.classList.toggle("zen", on);
  const fab = document.getElementById("zen-fab");
  const exit = document.getElementById("zen-exit");
  if (fab) fab.textContent = "📖";
  if (exit) exit.hidden = !on;
  if (on) {
    $("main").scrollTop = 0;
    toast(t("zen_toast"));
  }
}

function boot() {
  setupNameUi();
  ensureLangPills();
  applyStaticText();
  $("open-playground").addEventListener("click", openPlayground);
  const drawerBtn = document.getElementById("drawer-btn");
  const drawerBackdrop = document.getElementById("drawer-backdrop");
  if (drawerBtn && drawerBackdrop) {
    drawerBtn.addEventListener("click", () =>
      setDrawer(!document.body.classList.contains("drawer-open")));
    drawerBackdrop.addEventListener("click", () => setDrawer(false));
    document.addEventListener("keydown", (e) => {
      if (e.key === "Escape") {
        setDrawer(false);
        closeCodeModal();
        if (document.body.classList.contains("zen")) toggleZen(false);
      }
    });
  }

  // live search over chapters + lessons
  const search = document.getElementById("chapter-search");
  if (search) search.addEventListener("input", () => applyChapterFilter(search.value));

  // bottom navigation bar (mobile thumb bar)
  const bn = document.getElementById("bottom-nav");
  if (bn) bn.addEventListener("click", (e) => {
    const b = e.target.closest("button");
    if (!b) return;
    triggerHaptic();
    if (b.dataset.nav === "menu") setDrawer(true);
    if (b.dataset.nav === "search") palOpen();
    if (b.dataset.nav === "saved") {
      setDrawer(true);
      setTimeout(() => {
        const bb = document.getElementById("bookmarks-box");
        if (bb) {
          bb.scrollIntoView({ block: "center" });
          bb.style.outline = "2px solid rgba(255, 212, 59, .8)";
          setTimeout(() => { bb.style.outline = ""; }, 1500);
        }
      }, 380);
    }
    if (b.dataset.nav === "focus") toggleZen();
    if (b.dataset.nav === "lang") toggleLang();
  });

  // command palette input keys
  const palInput = $("pal-input");
  if (palInput) {
    palInput.addEventListener("input", () => buildPalResults(palInput.value));
    palInput.addEventListener("focus", () => buildPalResults(palInput.value));
  }
  if (palInput) palInput.addEventListener("keydown", (e) => {
    if (e.key === "ArrowDown") {
      e.preventDefault();
      palSel = Math.min(palSel + 1, palItems.length - 1);
      buildPalResults(palInput.value, true);
    } else if (e.key === "ArrowUp") {
      e.preventDefault();
      palSel = Math.max(palSel - 1, 0);
      buildPalResults(palInput.value, true);
    } else if (e.key === "Enter") {
      e.preventDefault();
      palRun(palItems[palSel]);
    }
  });

  // zen (focus) mode: button + F key
  const zen = document.getElementById("zen-fab");
  if (zen) {
    zen.title = t("zen_title");
    zen.addEventListener("click", () => toggleZen());
  }
  const zenExit = document.getElementById("zen-exit");
  if (zenExit) zenExit.addEventListener("click", () => toggleZen(false));
  document.addEventListener("keydown", (e) => {
    const typing = /^(INPUT|TEXTAREA|SELECT)$/.test(e.target.tagName);
    if (e.code === "KeyF" && !typing && courseActive && !e.ctrlKey && !e.metaKey) {
      toggleZen();
      return;
    }
    if (typing) {
      const search = document.getElementById("chapter-search");
      if (e.key === "Escape" && search && search.value) {
        search.value = "";
        applyChapterFilter("");
      }
      return;
    }
    if (e.key === "k" && !e.ctrlKey) { /* plain k handled below with courseActive */ }
    if (e.key === "Escape") { palClose(); }
    if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === "k") {
      e.preventDefault();
      palOpen();
      return;
    }
    if (e.key === "/" && courseActive) {
      e.preventDefault();
      palOpen();
      return;
    }
    if (!courseActive || e.ctrlKey || e.metaKey || e.altKey) return;
    if (!$("palette").hidden) return;
    if (e.key === "ArrowRight" || e.key === "j" || e.key === "J") {
      e.preventDefault();
      nextStep();
    } else if (e.key === "ArrowLeft" || e.key === "k" || e.key === "K") {
      e.preventDefault();
      prevStep();
    }
    // Escape already closes the drawer / modal / zen via the handler above
  });

  // reading-progress line follows the lessons pane scroll
  $("main").addEventListener("scroll", updateScrollProgress, { passive: true });
  window.addEventListener("resize", updateScrollProgress);

  // compare modal
  $("cmp-close").addEventListener("click", () => {
    $("compare-modal").hidden = true;
  });
  $("cmp-share").addEventListener("click", async () => {
    const pane = $("cmp-pane-a");
    const code = pane ? pane.querySelector("pre").textContent : "";
    const topic = $("cmp-topic-label").textContent;
    if (navigator.share) {
      try { await navigator.share({ title: "PLT — " + topic, text: code }); }
      catch (e) { /* cancelled */ }
    } else if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(code).then(
        () => toast(t("link_copied")), () => {});
    }
  });

  // fullscreen code modal
  $("cm-close").addEventListener("click", closeCodeModal);
  $("code-modal").addEventListener("click", (e) => {
    if (e.target.id === "code-modal") closeCodeModal();
  });
  $("cm-copy").addEventListener("click", () => {
    if (!codeModalSource) return;
    const btn = $("cm-copy");
    const done = () => { btn.textContent = "✓"; setTimeout(() => { btn.textContent = "📋"; }, 2000); };
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(codeModalSource.textContent).then(done, done);
    } else done();
  });

  initSwipeGestures();

  // PWA update prompt: when a new service worker installs while an old one
  // still controls the page, offer the refresh instead of stale content
  if ("serviceWorker" in navigator) {
    navigator.serviceWorker.addEventListener("controllerchange", () => {
      if (window.__pltReloadPending) window.location.reload();
    });
    navigator.serviceWorker.register("sw.js").then((reg) => {
      const showUpdateToast = () => {
        // an old worker controls the page + a new one is ready: offer refresh
        if (!navigator.serviceWorker.controller) return;
        const t = document.getElementById("update-toast");
        if (t) t.hidden = false;
      };
      const watch = (sw) => {
        if (!sw) return;
        sw.addEventListener("statechange", () => {
          if (sw.state === "installed") showUpdateToast();
        });
      };
      watch(reg.installing);
      watch(reg.waiting);
      if (reg.waiting) showUpdateToast();          // already waiting at load
      if (reg.active && !reg.waiting) {
        // force the browser's update check now (navigations do this too,
        // but this catches SPA-long sessions)
        reg.update().then(() => {
          watch(reg.installing);
          if (reg.waiting) showUpdateToast();
        }).catch(() => {});
      }
      reg.addEventListener("updatefound", () => watch(reg.installing));
    }).catch(() => {});
    const ub = $("update-btn");
    if (ub) ub.addEventListener("click", async () => {
      const reg = await navigator.serviceWorker.getRegistration();
      if (reg && reg.waiting) reg.waiting.postMessage({ action: "skipWaiting" });
      window.__pltReloadPending = true;
    });
  }
  if (!courseDataFor("python") && !courseDataFor("c") &&
      !courseDataFor("html") && !courseDataFor("css") &&
      !courseDataFor("js") && !courseDataFor("cpp")) {
    $("view").innerHTML = "<div class='card'><h2>" +
      esc(t("load_error_title")) + "</h2><p>" +
      t("load_error_body") + "</p></div>";
    return;
  }
  // default the course data to Python so the chooser's ready-tag works
  activateSubject("python");
  const deep = parseHash();
  if (!getUserName().trim()) {
    pendingDeepLink = deep;
    showWelcome();
  } else {
    if (deep && courseDataFor(deep.subject)) {
      activateSubject(deep.subject);
      pendingDeepLink = deep;
      enterCourse(false); // consumes pendingDeepLink
      return;
    }
    const saved = getSavedSubject();
    if (courseDataFor(saved) && activateSubject(saved)) {
      enterCourse(false);
      toast(t("welcome_back", { name: displayName() }));
    } else {
      openChooser();
    }
  }
}

boot();
