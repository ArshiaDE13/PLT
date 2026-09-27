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
    brand_name: "🐍 Python Tutor",
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
    brand_name: "🐍 آموزش پایتون",
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
      brand_name: "🔷 C Tutor",
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
      brand_name: "🔷 آموزش C",
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
  return subject === "c" ? window.CRunner : window.PyRunner;
}

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
  ch.lessons.forEach((lesson, j) => {
    const s = document.createElement("button");
    s.className = "sub-item" + (j === activeLessonIdx ? " active" : "");
    s.textContent = faLessonTitle(lesson);
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
  void view.offsetWidth;
  view.innerHTML = "";
  const ch = currentChapter();
  if (state.step.kind === "lesson") {
    view.appendChild(renderLesson(ch));
  } else {
    view.appendChild(renderQuiz(ch));
  }
  if (!skipAnim) view.classList.add("anim-in");
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

  const h = document.createElement("h3");
  h.className = "lesson-title";
  h.textContent = lesson.title;
  applyDir(h, !!lesson.__fa);
  card.appendChild(h);

  const body = document.createElement("div");
  body.className = "lesson-body";
  body.innerHTML = lesson.html;
  applyDir(body, !!lesson.__fa);
  card.appendChild(body);

  // try-it playground — C lessons ship their own seed code; the Python
  // course keeps its always-present box, C shows one only where runnable
  if (activeSubject === "python" || lesson.tryit) {
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

/* The Playground is a separate page opened in its own browser window, so
   the course stays where it is while you experiment with real code. */
function openPlayground() {
  const page = activeSubject === "c" ? "playground-c.html" : "playground.html";
  const w = window.open(page, "pytutor-playground-" + activeSubject,
    "popup=yes,width=1180,height=780");
  if (!w) toast(t("playground_blocked"));
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

/* Branding that follows the subject: titles, logo emoji and favicon. */
function updateSubjectBrand() {
  const s = subjectById(activeSubject);
  document.querySelectorAll("[data-subject-brand]").forEach((el) => {
    el.textContent = t("brand_name");
  });
  document.querySelectorAll("[data-subject-logo]").forEach((el) => {
    el.textContent = s.emoji || "📘";
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
    inner: pyInner, soon: false },
  { id: "c", en: "C", fa: "C", emoji: "🔷",
    c1: "#03599c", c2: "#4f8cc9",
    blob: { r: [136, 120, 136, 120, 136, 120, 136, 120], rot: Math.PI / 8 },
    inner: (u) => hexInner("C", "#03599c", "#4f8cc9", u, 40), soon: false },
  { id: "cpp", en: "C++", fa: "C++", emoji: "🔷",
    c1: "#004482", c2: "#5f94d2",
    blob: { r: [140, 116, 138, 118, 140, 116, 138, 118], rot: Math.PI / 8 },
    inner: (u) => hexInner("C++", "#004482", "#5f94d2", u, 28), soon: true },
  { id: "html", en: "HTML", fa: "HTML", emoji: "🛡️",
    c1: "#e44d26", c2: "#f16529",
    blob: { r: [120, 126, 130, 136, 144, 130, 120, 116], rot: -Math.PI / 2 },
    inner: (u) => shieldInner("5", "#e44d26", "#f16529", u), soon: true },
  { id: "css", en: "CSS", fa: "CSS", emoji: "🛡️",
    c1: "#1572b6", c2: "#33a9dc",
    blob: { r: [122, 126, 130, 132, 140, 130, 126, 122], rot: -Math.PI / 2 },
    inner: (u) => shieldInner("3", "#1572b6", "#33a9dc", u), soon: true },
  { id: "js", en: "JavaScript", fa: "جاوااسکریپت", emoji: "🟨",
    c1: "#e9d823", c2: "#f7df1e",
    blob: { r: [138, 120, 138, 120, 138, 120, 138, 120], rot: Math.PI / 4 },
    inner: jsInner, soon: true },
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
  const nodeR = Math.max(46, Math.round(W * 0.13));
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
  $("welcome").classList.remove("show", "entering");
  closeChooser();
  renderSidebar();
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

function boot() {
  setupNameUi();
  ensureLangPills();
  applyStaticText();
  $("open-playground").addEventListener("click", openPlayground);
  if (!courseDataFor("python") && !courseDataFor("c")) {
    $("view").innerHTML = "<div class='card'><h2>" +
      esc(t("load_error_title")) + "</h2><p>" +
      t("load_error_body") + "</p></div>";
    return;
  }
  // default the course data to Python so the chooser's ready-tag works
  activateSubject("python");
  if (!getUserName().trim()) {
    showWelcome();
  } else {
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
