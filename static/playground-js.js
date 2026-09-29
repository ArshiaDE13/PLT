"use strict";

/* JavaScript Playground — a console-style IDE.
   The browser IS the JS engine: your code runs with new Function() and
   console output appears in the dark console pane. Includes JS syntax
   highlighting, ready-made examples, autosave and the same English/
   Persian switch as the app. */

(function () {
  const $ = (id) => document.getElementById(id);
  const CODE_KEY = "pytutor-playground-code-js-v1";
  const LANG_KEY = "pytutor-lang-v1";

  let lang = document.documentElement.lang === "fa" ? "fa" : "en";

  const STR = {
    en: {
      doc_title: "🟨 JavaScript Playground",
      pg_title: "JavaScript Playground",
      pg_sub: "write JS — see the console output live, right in your browser",
      pg_run: "▶  Run",
      pg_running: "Running…",
      pg_examples_title: "Load an example",
      pg_examples_ph: "Examples…",
      pg_reset: "Reset",
      pg_clear: "Clear console",
      pg_close: "✕ Close",
      pg_output: "CONSOLE",
      pg_shortcut: "Ctrl+Enter = run · Tab = indent",
      pg_no_output: "(no output)",
      pg_ok: "✓ finished · {sec}s",
      pg_err: "✗ error (see output above)",
      pg_engine_idle: "the browser IS the JS engine — nothing to install",
      pg_engine_ready: "● JS engine ready",
      pg_saved: "saved ✓",
      pg_hint: "Press ▶ Run (or Ctrl+Enter) — console output appears here.",
      lang_aria: "Language",
    },
    fa: {
      doc_title: "🟨 محیط تمرین جاوااسکریپت",
      pg_title: "محیط تمرین جاوااسکریپت",
      pg_sub: "جاوااسکریپت بنویس — خروجی console را زنده ببین",
      pg_run: "▶  اجرا",
      pg_running: "در حال اجرا…",
      pg_examples_title: "بارگذاری نمونه",
      pg_examples_ph: "نمونه‌ها…",
      pg_reset: "بازنشانی",
      pg_clear: "پاک کردن console",
      pg_close: "✕ بستن",
      pg_output: "CONSOLE",
      pg_shortcut: "Ctrl+Enter = اجرا · Tab = تورفتگی",
      pg_no_output: "(خروجی نیست)",
      pg_ok: "✓ تمام شد · {sec} ثانیه",
      pg_err: "✗ خطا (خروجی را بالا ببین)",
      pg_engine_idle: "مرورگر خودش موتور JS است — چیزی برای نصب نیست",
      pg_engine_ready: "● موتور JS آماده است",
      pg_saved: "ذخیره شد ✓",
      pg_hint: "دکمهٔ اجرا (یا Ctrl+Enter) را بزن — خروجی console همین‌جا ظاهر می‌شود.",
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

  function buildLangPills() {
    const box = $("lang-pg");
    box.innerHTML = "";
    [["en", "English"], ["fa", "فارسی"]].forEach(([code, label]) => {
      const b = document.createElement("button");
      b.type = "button";
      b.dataset.lang = code;
      b.textContent = label;
      b.setAttribute("role", "radio");
      b.setAttribute("aria-checked", String(code === lang));
      b.classList.toggle("active", code === lang);
      b.addEventListener("click", () => setLang(code));
      box.appendChild(b);
    });
    box.setAttribute("aria-label", t("lang_aria"));
  }

  function applyLang(next) {
    lang = next;
    try { localStorage.setItem(LANG_KEY, next); } catch (e) {}
    const root = document.documentElement;
    root.lang = next;
    if (next === "fa") root.setAttribute("dir", "rtl");
    else root.removeAttribute("dir");
    document.title = t("doc_title");
    document.querySelectorAll("[data-i18n]").forEach((el) => {
      el.textContent = t(el.getAttribute("data-i18n"));
    });
    buildLangPills();
    buildExamples();
    runBtn.textContent = t("pg_run");
    $("pg-engine").textContent = t("pg_engine_ready");
    $("pg-engine").className = "pg-engine ready";
  }

  function setLang(next) {
    if (next === lang) return;
    document.body.classList.add("switching");
    setTimeout(() => { applyLang(next); document.body.classList.remove("switching"); }, 200);
  }

  /* ------------------------ syntax highlighting ------------------------ */

  const KEYWORDS = new Set(("break case catch class const continue debugger " +
    "default delete do else export extends finally for function if import in " +
    "instanceof let new return super switch this throw try typeof var void " +
    "while with yield async await static get set of null undefined true false " +
    "NaN Infinity").split(" "));

  const BUILTINS = new Set(("console Math JSON Object Array String Number " +
    "Boolean Date Map Set WeakMap WeakSet Symbol BigInt Promise RegExp Error " +
    "TypeError RangeError ReferenceError parseInt parseFloat isNaN isFinite " +
    "encodeURIComponent decodeURIComponent setTimeout setInterval clearTimeout " +
    "clearInterval requestAnimationFrame fetch alert prompt confirm structuredClone " +
    "proxy Reflect Intl globalThis document window localStorage sessionStorage").split(" "));

  const TOKEN_RE = new RegExp(
    "(//[^\\n]*|/\\*[\\s\\S]*?\\*/)" +
    "|(`(?:\\\\.|[^`\\\\])*`|\"(?:\\\\.|[^\"\\\\\\n])*\"|'(?:\\\\.|[^'\\\\\\n])*')" +
    "|(\\b\\d[\\d.]*(?:[eE][+-]?\\d+)?\\b|\\b0[xX][0-9a-fA-F]+\\b)" +
    "|([A-Za-z_$]\\w*)",
    "g");

  function esc(s) {
    return String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  }

  function highlightJs(src) {
    let out = "", last = 0, m;
    TOKEN_RE.lastIndex = 0;
    while ((m = TOKEN_RE.exec(src))) {
      out += esc(src.slice(last, m.index));
      const cls = m[1] ? "tk-c"
        : m[2] ? "tk-s"
        : m[3] ? "tk-n"
        : KEYWORDS.has(m[4]) ? "tk-k"
        : BUILTINS.has(m[4]) ? "tk-b"
        : "";
      out += cls ? '<span class="' + cls + '">' + esc(m[0]) + "</span>" : esc(m[0]);
      last = m.index + m[0].length;
    }
    return out + esc(src.slice(last));
  }

  /* ------------------------------ editor ------------------------------ */

  const ta = $("pg-code");
  const hlCode = $("pg-hl").querySelector("code");
  const gutter = $("pg-gutter");

  function refreshHighlight() { hlCode.innerHTML = highlightJs(ta.value) + "\n"; }

  function rebuildGutter() {
    const n = ta.value.split("\n").length;
    if (+gutter.dataset.lines !== n) {
      let html = "";
      for (let i = 1; i <= n; i++) html += "<div>" + i + "</div>";
      gutter.innerHTML = html;
      gutter.dataset.lines = n;
    }
  }

  function updatePos() {
    const pos = ta.selectionStart;
    const before = ta.value.slice(0, pos);
    const line = (before.match(/\n/g) || []).length + 1;
    const col = pos - before.lastIndexOf("\n");
    $("pg-pos").textContent = "Ln " + line + ", Col " + col;
  }

  function currentLineIndent(beforeCursor) {
    const line = beforeCursor.slice(beforeCursor.lastIndexOf("\n") + 1);
    return (line.match(/^[ \t]*/) || [""])[0];
  }

  function handleTab(e) {
    e.preventDefault();
    if (e.shiftKey) {
      const pos = ta.selectionStart;
      const before = ta.value.slice(0, pos);
      const lineStart = before.lastIndexOf("\n") + 1;
      const ws = currentLineIndent(before);
      if (ws) ta.setRangeText("", lineStart, lineStart + Math.min(4, ws.length), "end");
    } else {
      ta.setRangeText("  ", ta.selectionStart, ta.selectionEnd, "end");
    }
    onEdit();
  }

  function handleEnter(e) {
    e.preventDefault();
    const pos = ta.selectionStart;
    const before = ta.value.slice(0, pos);
    const indent = currentLineIndent(before);
    const line = before.slice(before.lastIndexOf("\n") + 1);
    let extra = "";
    if (/\{\s*$/.test(line)) extra = "  ";
    ta.setRangeText("\n" + indent + extra, pos, ta.selectionEnd, "end");
    onEdit();
  }

  ta.addEventListener("keydown", (e) => {
    if (e.key === "Tab") handleTab(e);
    else if (e.key === "Enter" && !e.ctrlKey && !e.metaKey && !e.shiftKey &&
             ta.selectionStart === ta.selectionEnd) handleEnter(e);
    else if (e.key === "Enter" && (e.ctrlKey || e.metaKey)) { e.preventDefault(); runCode(); }
  });

  ["keyup", "click", "select"].forEach((ev) => ta.addEventListener(ev, updatePos));

  ta.addEventListener("scroll", () => {
    const hl = $("pg-hl");
    hl.scrollTop = ta.scrollTop;
    hl.scrollLeft = ta.scrollLeft;
    gutter.scrollTop = ta.scrollTop;
  });

  /* ----------------------------- autosave ----------------------------- */

  let saveTimer = null;
  function scheduleSave() {
    clearTimeout(saveTimer);
    saveTimer = setTimeout(() => {
      try { localStorage.setItem(CODE_KEY, ta.value); } catch (e) {}
      const s = $("pg-save");
      s.textContent = t("pg_saved");
      s.classList.add("show");
      setTimeout(() => s.classList.remove("show"), 1400);
    }, 400);
  }

  function saveNow() { try { localStorage.setItem(CODE_KEY, ta.value); } catch (e) {} }
  window.addEventListener("pagehide", saveNow);

  /* ----------------------------- examples ----------------------------- */

  const DEFAULT_CODE = [
    "// Welcome to the JavaScript Playground! 🟨",
    "// Write any JS and press Run (Ctrl+Enter) —",
    "// console output appears on the right.",
    "",
    'console.log("Hello, JavaScript! 🟡");',
    "",
    "const langs = ['HTML', 'CSS', 'JS'];",
    'console.log("I\'m learning:", langs.join(", "));',
    "",
    "const squares = [1, 2, 3, 4, 5].map(n => n ** 2);",
    'console.log("Squares:", squares);',
    "",
    "const user = { name: 'Ada', role: 'admin' };",
    "console.table ? console.table(user) : console.log(user);",
  ].join("\n");

  const EXAMPLES = [
    {
      en: "Variables & types", fa: "متغیرها و انواع",
      code: [
        "const name = 'Ada';",
        "let score = 95;",
        "const isActive = true;",
        "const tags = ['dev', 'admin'];",
        "const profile = { name, score, isActive };",
        "",
        "console.log('name:', name, typeof name);",
        "console.log('score:', score, typeof score);",
        "console.log('isActive:', isActive, typeof isActive);",
        "console.log('tags:', tags, typeof tags);",
        "console.log('profile:', profile);",
        "",
        "// null vs undefined",
        "let notAssigned;",
        "let intentionallyNull = null;",
        "console.log('notAssigned:', notAssigned, typeof notAssigned);",
        "console.log('null:', intentionallyNull, typeof intentionallyNull);",
      ].join("\n"),
    },
    {
      en: "Control flow", fa: "کنترل جریان",
      code: [
        "const scores = [95, 87, 72, 60, 45, 100];",
        "",
        "for (const score of scores) {",
        "  if (score >= 90)      console.log(score, '→ A 🏆');",
        "  else if (score >= 80) console.log(score, '→ B');",
        "  else if (score >= 70) console.log(score, '→ C');",
        "  else                  console.log(score, '→ F 😅');",
        "}",
        "",
        "// switch",
        "const grade = 'B';",
        "switch (grade) {",
        "  case 'A': console.log('Excellent!'); break;",
        "  case 'B': console.log('Good job!'); break;",
        "  default:  console.log('Keep trying!');",
        "}",
        "",
        "// while + break + continue",
        "let n = 0;",
        "while (true) {",
        "  n++;",
        "  if (n % 2 !== 0) continue;  // skip odds",
        "  if (n > 10) break;          // stop",
        "  console.log('even:', n);",
        "}",
      ].join("\n"),
    },
    {
      en: "Functions & closures", fa: "توابع و closureها",
      code: [
        "// Arrow functions",
        "const add = (a, b) => a + b;",
        "const greet = name => `Hello, ${name}!`;",
        "console.log(greet('Ada'));",
        "",
        "// Default + rest parameters",
        "function power(base, exp = 2) { return base ** exp; }",
        "console.log('power(3):', power(3));",
        "console.log('power(2,10):', power(2, 10));",
        "",
        "function sum(...nums) {",
        "  return nums.reduce((a, b) => a + b, 0);",
        "}",
        "console.log('sum:', sum(1, 2, 3, 4, 5));",
        "",
        "// Closure: a private counter",
        "function makeCounter() {",
        "  let count = 0;  // private!",
        "  return {",
        "    increment: () => ++count,",
        "    get: () => count,",
        "  };",
        "}",
        "const c1 = makeCounter();",
        "const c2 = makeCounter();",
        "c1.increment(); c1.increment(); c1.increment();",
        "console.log('c1:', c1.get());  // 3",
        "console.log('c2:', c2.get());  // 1 (independent!)",
      ].join("\n"),
    },
    {
      en: "Arrays & objects", fa: "آرایه‌ها و شیءها",
      code: [
        "const users = [",
        "  { name: 'Ada', age: 36, role: 'admin' },",
        "  { name: 'Grace', age: 45, role: 'user' },",
        "  { name: 'Linus', age: 28, role: 'user' },",
        "];",
        "",
        "// map: extract + transform",
        "const names = users.map(u => u.name.toUpperCase());",
        "console.log('names:', names);",
        "",
        "// filter: keep matching",
        "const admins = users.filter(u => u.role === 'admin');",
        "console.log('admins:', admins.map(u => u.name));",
        "",
        "// reduce: aggregate",
        "const totalAge = users.reduce((sum, u) => sum + u.age, 0);",
        "console.log('total age:', totalAge);",
        "",
        "// destructuring",
        "const { name, age } = users[0];",
        "console.log(`${name} is ${age}`);",
        "",
        "// spread + rest",
        "const [first, ...rest] = users.map(u => u.name);",
        "console.log('first:', first, '| rest:', rest);",
        "",
        "// optional chaining + nullish",
        "console.log(users[0]?.profile?.bio ?? 'no bio');",
      ].join("\n"),
    },
    {
      en: "Classes", fa: "کلاس‌ها",
      code: [
        "class Animal {",
        "  #secret = 'hidden';",
        "  static count = 0;",
        "",
        "  constructor(name) {",
        "    this.name = name;",
        "    Animal.count++;",
        "  }",
        "",
        "  speak() { return `${this.name} makes a sound`; }",
        "",
        "  get info() { return `${this.name} (${this.constructor.name})`; }",
        "",
        "  static getTotal() { return Animal.count; }",
        "}",
        "",
        "class Dog extends Animal {",
        "  constructor(name, breed) {",
        "    super(name);",
        "    this.breed = breed;",
        "  }",
        "  speak() { return `${this.name} says woof!`; }",
        "}",
        "",
        "const cat = new Animal('Whiskers');",
        "const dog = new Dog('Rex', 'Golden');",
        "console.log(cat.speak());",
        "console.log(dog.speak());",
        "console.log(dog.info);",
        "console.log('Total animals:', Animal.getTotal());",
      ].join("\n"),
    },
    {
      en: "Promises & async/await", fa: "Promiseها و async/await",
      code: [
        "// async/await makes promises read like sync code",
        "function wait(ms) {",
        "  return new Promise(resolve => setTimeout(resolve, ms));",
        "}",
        "",
        "async function main() {",
        "  console.log('starting...');",
        "  await wait(100);",
        "  console.log('100ms later');",
        "",
        "  // parallel with Promise.all",
        "  const [a, b] = await Promise.all([",
        "    wait(100).then(() => 'result A'),",
        "    wait(150).then(() => 'result B'),",
        "  ]);",
        "  console.log(a, '|', b);",
        "",
        "  // error handling",
        "  try {",
        "    await Promise.reject(new Error('something broke'));",
        "  } catch (e) {",
        "    console.log('caught:', e.message);",
        "  } finally {",
        "    console.log('done!');",
        "  }",
        "}",
        "",
        "main();",
      ].join("\n"),
    },
  ];

  function buildExamples() {
    const sel = $("pg-examples");
    sel.innerHTML = "";
    const ph = document.createElement("option");
    ph.value = "";
    ph.textContent = t("pg_examples_ph");
    sel.appendChild(ph);
    EXAMPLES.forEach((ex, i) => {
      const o = document.createElement("option");
      o.value = String(i);
      o.textContent = (lang === "fa" && ex.fa) ? ex.fa : ex.en;
      sel.appendChild(o);
    });
    sel.value = "";
    sel.setAttribute("title", t("pg_examples_title"));
  }

  $("pg-examples").addEventListener("change", (e) => {
    const i = +e.target.value;
    if (EXAMPLES[i]) { ta.value = EXAMPLES[i].code; onEdit(); runCode(); ta.focus(); }
    e.target.value = "";
  });

  /* ------------------------------ console ----------------------------- */

  const consoleBody = $("pg-console");

  function addRunBlock() {
    const hint = consoleBody.querySelector(".pg-hint");
    if (hint) hint.remove();
    const block = document.createElement("div");
    block.className = "pg-run-block";
    const time = new Date().toLocaleTimeString(lang === "fa" ? "fa-IR" : "en-GB");
    block.innerHTML =
      '<div class="pg-run-head">▶ script.js · ' + esc(time) + "</div>" +
      '<pre class="pg-run-out loading">' + esc(t("pg_running")) + "</pre>";
    consoleBody.appendChild(block);
    consoleBody.scrollTop = consoleBody.scrollHeight;
    return block;
  }

  function fillRunBlock(block, logs, sec, hasError) {
    const out = block.querySelector(".pg-run-out");
    const status = document.createElement("div");
    status.className = "pg-run-status";
    block.appendChild(status);
    out.classList.remove("loading");
    out.textContent = logs.join("\n") || t("pg_no_output");
    if (hasError) {
      block.classList.add("err");
      status.classList.add("err");
      status.textContent = t("pg_err");
    } else {
      status.classList.add("ok");
      status.textContent = t("pg_ok", { sec });
    }
    consoleBody.scrollTop = consoleBody.scrollHeight;
  }

  /* ------------------------------- run -------------------------------- */

  const runBtn = $("pg-run");
  let running = false;

  function formatVal(v) {
    if (typeof v === "string") return v;
    if (typeof v === "object" && v !== null) {
      try { return JSON.stringify(v, null, 2); } catch (e) { return String(v); }
    }
    return String(v);
  }

  async function runCode() {
    if (running) return;
    if (!ta.value.trim()) return;
    running = true;
    runBtn.disabled = true;
    runBtn.textContent = t("pg_running");
    const block = addRunBlock();
    const t0 = performance.now();
    const logs = [];
    let hasError = false;

    const origLog = console.log;
    const origWarn = console.warn;
    const origError = console.error;
    console.log = (...args) => logs.push(args.map(formatVal).join(" "));
    console.warn = (...args) => logs.push("⚠ " + args.map(formatVal).join(" "));
    console.error = (...args) => { logs.push("✗ " + args.map(formatVal).join(" ")); hasError = true; };

    try {
      const fn = new Function(ta.value);
      fn();
    } catch (e) {
      logs.push("✗ " + e.name + ": " + e.message);
      hasError = true;
    } finally {
      console.log = origLog;
      console.warn = origWarn;
      console.error = origError;
    }

    const sec = ((performance.now() - t0) / 1000).toFixed(2);
    fillRunBlock(block, logs, sec, hasError);
    running = false;
    runBtn.disabled = false;
    runBtn.textContent = t("pg_run");
  }

  runBtn.addEventListener("click", runCode);

  document.addEventListener("keydown", (e) => {
    if ((e.ctrlKey || e.metaKey) && e.key === "Enter") { e.preventDefault(); runCode(); }
  });

  /* --------------------------- other buttons -------------------------- */

  $("pg-clear").addEventListener("click", () => {
    consoleBody.innerHTML = '<div class="pg-hint">' + esc(t("pg_hint")) + "</div>";
  });

  $("pg-reset").addEventListener("click", () => {
    ta.value = DEFAULT_CODE;
    onEdit();
    ta.focus();
  });

  $("pg-close").addEventListener("click", () => { saveNow(); window.close(); });

  /* ------------------------------- boot ------------------------------- */

  function onEdit() {
    refreshHighlight();
    rebuildGutter();
    updatePos();
    scheduleSave();
  }

  ta.addEventListener("input", onEdit);

  let saved = null;
  try { saved = localStorage.getItem(CODE_KEY); } catch (e) {}
  ta.value = saved && saved.trim() ? saved : DEFAULT_CODE;

  buildLangPills();
  applyLang(lang);
  onEdit();
  consoleBody.innerHTML = '<div class="pg-hint">' + esc(t("pg_hint")) + "</div>";
  ta.focus();
})();
