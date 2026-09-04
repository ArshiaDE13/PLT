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
  },

  fa: {
    doc_title: "🐍 Python Tutor — آموزش پایتون ۳٫۱۴",
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
  },
};

function t(key, vars) {
  let s = (STR[lang] && STR[lang][key]) || STR.en[key] || key;
  if (vars) {
    for (const k of Object.keys(vars)) {
      s = s.replace(new RegExp("\\{" + k + "\\}", "g"), String(vars[k]));
    }
  }
  return s;
}

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
  updateLangPills();
  renderSidebar();
  renderView(true);
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
    return { __fa: true, title: lesson.title_fa || lesson.title, html: lesson.html_fa };
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

/* ========================== in-browser Python ========================== */
/* The "Try it yourself" playground runs REAL Python 3.14 in the browser:
   Pyodide (CPython compiled to WebAssembly) executes the code inside a
   Web Worker, so a stuck program (infinite loop, input()) is killed after
   RUN_TIMEOUT_MS instead of freezing the page. The engine (~10 MB) is
   fetched from a CDN on the first Run click, then cached by the browser. */

const PYODIDE_VERSION = "v314.0.6";
const PYODIDE_CDN = "https://cdn.jsdelivr.net/pyodide/" + PYODIDE_VERSION +
  "/full/";
const RUN_TIMEOUT_MS = 10000;
const LOAD_TIMEOUT_MS = 60000;

let pyWorker = null;
let pyLoadPromise = null;
let pyEngineReady = false;

function pyWorkerSource() {
  return [
    'import { loadPyodide } from "' + PYODIDE_CDN + 'pyodide.mjs";',
    "let pyodide = null;",
    "self.onmessage = async (e) => {",
    "  try {",
    "    if (e.data.msg === 'load') {",
    "      pyodide = await loadPyodide({ indexURL: '" + PYODIDE_CDN + "' });",
    "      self.postMessage({ msg: 'loaded' });",
    "    } else if (e.data.msg === 'run') {",
    "      let out = '';",
    "      pyodide.setStdout({ batched: (s) => { out += s + '\\n'; } });",
    "      try {",
    "        await pyodide.runPythonAsync(e.data.code);",
    "        self.postMessage({ msg: 'done', ok: true, output: out.replace(/\\n+$/, '') });",
    "      } catch (err) {",
    "        self.postMessage({ msg: 'done', ok: false, output: String((err && err.message) || err) });",
    "      }",
    "    }",
    "  } catch (err) {",
    "    self.postMessage({ msg: 'loadError', error: String((err && err.message) || err) });",
    "  }",
    "};",
  ].join("\n");
}

function makePyWorker() {
  // Pyodide 314.x only runs inside a MODULE worker (ESM); the blob itself
  // must still be a plain JS MIME type.
  const url = URL.createObjectURL(
    new Blob([pyWorkerSource()], { type: "text/javascript" }));
  return new Worker(url, { type: "module" });
}

function askWorker(worker, msg, timeoutMs) {
  return new Promise((resolve, reject) => {
    const timer = setTimeout(() => {
      cleanup();
      reject(new Error("timeout"));
    }, timeoutMs);
    function onMsg(e) { cleanup(); resolve(e.data); }
    function onErr(err) { cleanup(); reject(err); }
    function cleanup() {
      clearTimeout(timer);
      worker.removeEventListener("message", onMsg);
      worker.removeEventListener("error", onErr);
    }
    worker.addEventListener("message", onMsg);
    worker.addEventListener("error", onErr);
    worker.postMessage(msg);
  });
}

async function getPyWorker() {
  if (pyLoadPromise) return pyLoadPromise;
  pyLoadPromise = (async () => {
    const w = makePyWorker();
    pyWorker = w;
    const res = await askWorker(w, { msg: "load" }, LOAD_TIMEOUT_MS);
    if (res.msg !== "loaded") {
      w.terminate();
      pyWorker = null;
      pyLoadPromise = null;
      throw new Error(res.error || "the Python engine failed to start");
    }
    pyEngineReady = true;
    return w;
  })();
  return pyLoadPromise;
}

function resetPyEngine() {
  if (pyWorker) {
    try { pyWorker.terminate(); } catch (e) { /* non-fatal */ }
    pyWorker = null;
  }
  pyLoadPromise = null;
  pyEngineReady = false;
}

async function apiRun(code) {
  if (!code || !code.trim()) return { ok: true, output: "" };
  let worker;
  try {
    worker = await getPyWorker();
  } catch (e) {
    resetPyEngine();
    return {
      ok: false,
      output: t("engine_fail", {
        err: (e && e.message) ? e.message : "network error",
      }),
    };
  }
  try {
    const res = await askWorker(worker, { msg: "run", code }, RUN_TIMEOUT_MS);
    return { ok: !!res.ok, output: res.output || "" };
  } catch (e) {
    resetPyEngine(); // the worker may have been killed by the timeout
    return {
      ok: false,
      output: t("engine_timeout", { sec: RUN_TIMEOUT_MS / 1000 }),
    };
  }
}

/* ============================== sidebar ================================ */

/* One header per official documentation section, in course order. */
const CATEGORIES = [
  { key: "cat_tutorial",   emoji: "\u{1F4D6}", start: 1,  end: 16 },
  { key: "cat_using",      emoji: "\u2699\uFE0F", start: 17, end: 19 },
  { key: "cat_library",    emoji: "\u{1F4DA}", start: 20, end: 23 },
  { key: "cat_howto",      emoji: "\u{1F9ED}", start: 24, end: 27 },
  { key: "cat_reference",  emoji: "\u{1F4DC}", start: 28, end: 31 },
];

function renderSidebar() {
  const list = $("chapter-list");
  list.innerHTML = "";
  const firstBuild = !sidebarEntranceShown;
  for (const cat of CATEGORIES) {
    const head = document.createElement("div");
    head.className = "category-head";
    head.innerHTML = '<span class="cat-emoji">' + cat.emoji +
      "</span><span>" + esc(t(cat.key)) + "</span>";
    if (firstBuild) head.style.animationDelay = (0.05 + (cat.start - 1) * 0.02) + "s";
    list.appendChild(head);
    for (let i = cat.start - 1; i < cat.end; i++) {
      const ch = chapters[i];
      if (!ch) continue;
      const done = chapterDone(ch);
      const finished = quizAnsweredCount(ch) >= ch.quiz.length;
      const btn = document.createElement("button");
      btn.className = "chapter-item" +
        (i === state.chapter ? " active" : "") +
        (finished ? " finished" : "");
      if (firstBuild) btn.style.animationDelay = (0.05 + i * 0.02) + "s";
      btn.innerHTML =
        '<span class="num">' + fmtNum(i + 1) + "</span>" +
        "<span>" + esc(faChapterTitle(ch)) + "</span>" +
        '<span class="dot">' + (done ? "\u2714" : "") + "</span>";
      btn.addEventListener("click", () => openChapter(i));
      list.appendChild(btn);
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

function esc(s) {
  const d = document.createElement("div");
  d.textContent = s;
  return d.innerHTML;
}

/* ============================== navigation ============================= */

function openChapter(i) {
  state.chapter = i;
  state.step = { kind: "lesson", idx: 0 };
  renderSidebar();
  renderView();
  $("main").scrollTop = 0;
}

function openStep(kind, idx) {
  state.step = { kind, idx };
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

  // try-it playground
  card.appendChild(renderTryIt());

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

function renderTryIt() {
  const box = document.createElement("div");
  box.className = "tryit";
  const label = document.createElement("div");
  label.className = "tryit-label";
  label.textContent = t("tryit_label");
  const ta = document.createElement("textarea");
  ta.className = "codebox";
  ta.placeholder = "print('hello')\nfor i in range(3):\n    print(i)";
  const row = document.createElement("div");
  row.className = "answer-actions";
  const runBtn = document.createElement("button");
  runBtn.className = "btn secondary";
  runBtn.textContent = t("run");
  const out = document.createElement("div");
  out.className = "run-output";
  runBtn.addEventListener("click", async () => {
    out.className = "run-output show";
    out.textContent = pyEngineReady
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
    renderSidebar();
    renderView();
    toast(t("welcome_toast", { name: n }));
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
}

/* ============================== boot =================================== */

function boot() {
  setupNameUi();
  ensureLangPills();
  applyStaticText();
  if (window.COURSE_DATA && Array.isArray(window.COURSE_DATA.chapters) &&
      window.COURSE_DATA.chapters.length) {
    chapters = window.COURSE_DATA.chapters;
  } else {
    $("view").innerHTML = "<div class='card'><h2>" +
      esc(t("load_error_title")) + "</h2><p>" +
      t("load_error_body") + "</p></div>";
    return;
  }
  if (!getUserName().trim()) {
    showWelcome();
  } else {
    renderSidebar();
    renderView();
    toast(t("welcome_back", { name: displayName() }));
  }
}

boot();
