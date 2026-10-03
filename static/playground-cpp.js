"use strict";

/* C++ Playground — reuses the C engine (cengine.js) which handles
   basic C++ syntax: classes, structs, functions, control flow, etc.
   Advanced C++ features (templates, STL containers, smart pointers)
   are not supported by the sandbox engine. */

(function () {
  const $ = (id) => document.getElementById(id);
  const CODE_KEY = "pytutor-playground-code-cpp-v1";
  const LANG_KEY = "pytutor-lang-v1";

  let lang = document.documentElement.lang === "fa" ? "fa" : "en";

  const STR = {
    en: {
      doc_title: "🔷 C++ Playground",
      pg_title: "C++ Playground",
      pg_sub: "write and run basic C++ — right in your browser",
      pg_run: "▶  Run",
      pg_examples_title: "Load an example",
      pg_examples_ph: "Examples…",
      pg_reset: "Reset",
      pg_clear: "Clear console",
      pg_close: "✕ Back to lessons",
      pg_output: "OUTPUT",
      pg_shortcut: "Ctrl+Enter = run · Tab = indent",
      pg_no_output: "(no output)",
      pg_ok: "✓ finished · {sec}s",
      pg_err: "✗ error (see output above)",
      pg_engine_idle: "C++ engine ready (cout, strings, references, structs)",
      pg_engine_ready: "● C++ engine ready (basic mode)",
      pg_engine_fail: "Couldn't start the engine ({err}). Press Run again.",
      pg_engine_timeout: "Timed out after {sec}s.",
      pg_saved: "saved ✓",
      pg_hint: "Press ▶ Run (or Ctrl+Enter) — output appears here.",
      lang_aria: "Language",
    },
    fa: {
      doc_title: "🔷 محیط تمرین ++C",
      pg_title: "محیط تمرین ++C",
      pg_sub: "کد ++C بنویس و همین‌جا اجرا کن",
      pg_run: "▶  اجرا",
      pg_examples_title: "بارگذاری نمونه",
      pg_examples_ph: "نمونه‌ها…",
      pg_reset: "بازنشانی",
      pg_clear: "پاک کردن console",
      pg_close: "✕ بازگشت به درس‌ها",
      pg_output: "خروجی",
      pg_shortcut: "Ctrl+Enter = اجرا · Tab = تورفتگی",
      pg_no_output: "(خروجی نیست)",
      pg_ok: "✓ تمام شد · {sec} ثانیه",
      pg_err: "✗ خطا (خروجی را بالا ببین)",
      pg_engine_idle: "موتور آماده است (cout، رشته‌ها، مرجع‌ها، structها)",
      pg_engine_ready: "● موتور ++C آماده است (حالت پایه)",
      pg_engine_fail: "راه‌اندازی موتور ممکن نشد ({err}). دوباره «اجرا» را بزن.",
      pg_engine_timeout: "پس از {sec} ثانیه متوقف شد.",
      pg_saved: "ذخیره شد ✓",
      pg_hint: "دکمهٔ اجرا (یا Ctrl+Enter) را بزن — خروجی همین‌جا ظاهر می‌شود.",
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

  const KEYWORDS = new Set(("alignas alignof and and_eq asm auto bitand bitor " +
    "break case catch class co_await co_return co_yield compl concept const " +
    "consteval constexpr constinit const_cast continue co_await decltype " +
    "default delete do dynamic_cast else enum explicit export extern for friend " +
    "goto if inline mutable namespace new noexcept not not_eq nullptr operator " +
    "or or_eq private protected public register reinterpret_cast requires " +
    "return sizeof static static_assert static_cast struct switch template this " +
    "thread_local throw true false try typedef typeid typename union using " +
    "virtual volatile while xor xor_eq int char float double long short signed " +
    "unsigned bool void wchar_t").split(" "));

  const BUILTINS = new Set(("std cout cin endl endl string vector map set " +
    "unordered_map unordered_set optional variant any expected span pair tuple " +
    "make_unique make_shared unique_ptr shared_ptr weak_ptr allocator printf " +
    "scanf malloc free memcpy memset strlen strcpy strcmp sort find transform " +
    "accumulate max_element min_element count_if begin end push_back pop_back " +
    "size empty clear resize reserve").split(" "));

  const TOKEN_RE = new RegExp(
    "(//[^\\n]*|/\\*[\\s\\S]*?\\*/)" +
    "|(\"(?:\\\\.|[^\"\\\\\\n])*\"|'(?:\\\\.|[^'\\\\\\n])*')" +
    "|(\\b\\d[\\d.]*(?:[eE][+-]?\\d+)?\\b|\\b0[xX][0-9a-fA-F]+\\b)" +
    "|([A-Za-z_]\\w*)",
    "g");

  function esc(s) {
    return String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  }

  function highlightCpp(src) {
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

  function refreshHighlight() { hlCode.innerHTML = highlightCpp(ta.value) + "\n"; }

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
      ta.setRangeText("    ", ta.selectionStart, ta.selectionEnd, "end");
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
    if (/\{\s*$/.test(line)) extra = "    ";
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
    "// Welcome to the C++ Playground! 🔷",
    "// Write basic C++ and press Run (Ctrl+Enter).",
    "// The sandbox supports C++ basics: std::cout, std::string,",
    "// references, structs and functions.",
    "",
    "#include <iostream>",
    "#include <string>",
    "",
    "int main() {",
    '    std::string name = "C++23";',
    '    std::cout << "Hello, " << name << "! 🔷" << std::endl;',
    "",
    "    for (int i = 1; i <= 5; i++) {",
    '        std::cout << i << " squared = " << i * i << "\\n";',
    "    }",
    "",
    "    return 0;",
    "}",
  ].join("\n");

  const EXAMPLES = [
    {
      en: "strings & structs", fa: "رشته‌ها و structها",
      code: [
        "#include <iostream>",
        "#include <string>",
        "",
        "struct Player {",
        "    std::string name;",
        "    int health;",
        "};",
        "",
        "void print(const Player& p) {",
        '    std::cout << p.name << ": " << p.health << " HP\\n";',
        "}",
        "",
        "int main() {",
        '    Player hero = {"Hero", 100};',
        "    hero.health -= 30;",
        "    print(hero);",
        "",
        '    std::string full = hero.name + " the Brave";',
        '    std::cout << full << " (" << full.length() << " chars)\\n";',
        "    return 0;",
        "}",
      ].join("\n"),
    },
    {
      en: "References & pointers", fa: "مرجع‌ها و اشاره‌گرها",
      code: [
        "#include <iostream>",
        "",
        "void swap(int* a, int* b) {",
        "    int t = *a; *a = *b; *b = t;",
        "}",
        "",
        "void modify(int& ref) { ref *= 2; }",
        "",
        "int main() {",
        "    int x = 1, y = 2;",
        "    swap(&x, &y);",
        '    std::cout << "after swap: " << x << " " << y << "\\n";',
        "",
        "    modify(x);",
        '    std::cout << "after modify: " << x << "\\n";',
        "",
        "    int* ptr = &x;",
        '    std::cout << "via pointer: " << *ptr << "\\n";',
        "    return 0;",
        "}",
      ].join("\n"),
    },
    {
      en: "Control flow & logic", fa: "جریان کنترل و منطق",
      code: [
        "#include <iostream>",
        "",
        "int main() {",
        "    int scores[] = {72, 95, 88, 61, 100};",
        "    int best = 0;",
        "",
        "    for (int i = 0; i < 5; i++) {",
        "        if (scores[i] > best) best = scores[i];",
        "    }",
        "",
        '    std::cout << "best score: " << best << "\\n";',
        "",
        "    for (int s : scores) {",
        '        if (s >= 90) std::cout << s << " is excellent\\n";',
        "        else std::cout << s << \" needs work\\n\";",
        "    }",
        "    return 0;",
        "}",
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
    if (EXAMPLES[i]) { ta.value = EXAMPLES[i].code; onEdit(); ta.focus(); }
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
      '<div class="pg-run-head">▶ main.cpp · ' + esc(time) + "</div>" +
      '<pre class="pg-run-out loading">' + esc(t("pg_running")) + "</pre>";
    consoleBody.appendChild(block);
    consoleBody.scrollTop = consoleBody.scrollHeight;
    return block;
  }

  function fillRunBlock(block, res, sec) {
    const out = block.querySelector(".pg-run-out");
    const status = document.createElement("div");
    status.className = "pg-run-status";
    block.appendChild(status);
    if (res.err === "timeout") {
      out.classList.remove("loading");
      out.textContent = t("pg_engine_timeout", { sec: CRunner.RUN_TIMEOUT_MS / 1000 });
      block.classList.add("err");
      status.classList.add("err");
      status.textContent = t("pg_err");
    } else {
      out.classList.remove("loading");
      out.textContent = res.output || t("pg_no_output");
      if (!res.ok) {
        block.classList.add("err");
        status.classList.add("err");
        status.textContent = t("pg_err");
      } else {
        status.classList.add("ok");
        status.textContent = t("pg_ok", { sec });
      }
    }
    consoleBody.scrollTop = consoleBody.scrollHeight;
  }

  /* ------------------------------- run -------------------------------- */

  const runBtn = $("pg-run");
  let running = false;

  async function runCode() {
    if (running) return;
    if (!ta.value.trim()) return;
    running = true;
    runBtn.disabled = true;
    runBtn.textContent = t("pg_running");
    const block = addRunBlock();
    const t0 = performance.now();
    try {
      const res = await CRunner.run(ta.value);
      const sec = ((performance.now() - t0) / 1000).toFixed(2);
      fillRunBlock(block, res, sec);
    } finally {
      running = false;
      runBtn.disabled = false;
      runBtn.textContent = t("pg_run");
    }
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

  $("pg-close").addEventListener("click", () => { saveNow(); window.location.href = "index.html"; });

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
