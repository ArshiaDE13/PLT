"use strict";

/* Python Playground — a small self-contained IDE page.
   It shares the Pyodide Web-Worker engine (pyrunner.js) with the course,
   adds a syntax-highlighted editor (transparent <textarea> layered over a
   highlighted <pre>), a run console, ready-made examples, autosave and the
   same English/Persian language switch as the main app. */

(function () {
  const $ = (id) => document.getElementById(id);
  const CODE_KEY = "pytutor-playground-code-v1";
  const LANG_KEY = "pytutor-lang-v1";

  /* ------------------------------ i18n -------------------------------- */

  let lang = document.documentElement.lang === "fa" ? "fa" : "en";

  const STR = {
    en: {
      doc_title: "🐍 Python Playground",
      pg_title: "Python Playground",
      pg_sub: "write and run real Python 3.14 — right in your browser",
      pg_run: "▶  Run",
      pg_running: "Running…",
      pg_examples_title: "Load an example",
      pg_examples_ph: "Examples…",
      pg_reset: "Reset",
      pg_clear: "Clear console",
      pg_close: "✕ Close",
      pg_output: "OUTPUT",
      pg_shortcut: "Ctrl+Enter = run · Tab = indent",
      pg_no_output: "(no output)",
      pg_ok: "✓ finished · {sec}s",
      pg_err: "✗ error (see output above)",
      pg_engine_idle: "engine loads on first Run (~10 MB, then cached)",
      pg_engine_loading: "⏳ loading the Python engine…",
      pg_engine_ready: "● Python 3.14 ready",
      pg_engine_fail: "Couldn't load the Python engine ({err}). Check your " +
        "internet connection and press Run again.",
      pg_engine_timeout: "Timed out after {sec}s — the code may be stuck in " +
        "an infinite loop or waiting for input().",
      pg_saved: "saved ✓",
      pg_hint: "Press ▶ Run (or Ctrl+Enter) — your output appears here.",
      lang_aria: "Language",
    },
    fa: {
      doc_title: "🐍 محیط تمرین پایتون",
      pg_title: "محیط تمرین پایتون",
      pg_sub: "کد پایتون ۳٫۱۴ واقعی بنویس و همین‌جا در مرورگر اجرا کن",
      pg_run: "▶  اجرا",
      pg_running: "در حال اجرا…",
      pg_examples_title: "بارگذاری نمونه",
      pg_examples_ph: "نمونه‌ها…",
      pg_reset: "بازنشانی",
      pg_clear: "پاک کردن خروجی",
      pg_close: "✕ بستن",
      pg_output: "خروجی",
      pg_shortcut: "Ctrl+Enter = اجرا · Tab = تورفتگی",
      pg_no_output: "(خروجی نیست)",
      pg_ok: "✓ تمام شد · {sec} ثانیه",
      pg_err: "✗ خطا (خروجی را بالا ببین)",
      pg_engine_idle: "موتور با اولین اجرا بارگذاری می‌شود (حدود ۱۰ مگابایت)",
      pg_engine_loading: "⏳ در حال بارگذاری موتور پایتون…",
      pg_engine_ready: "● پایتون ۳٫۱۴ آماده است",
      pg_engine_fail: "بارگذاری موتور پایتون ممکن نشد ({err}). اتصال " +
        "اینترنت را بررسی کن و دوباره «اجرا» را بزن.",
      pg_engine_timeout: "پس از {sec} ثانیه متوقف شد — احتمالاً کد در " +
        "حلقهٔ بی‌نهایت گیر کرده یا منتظر input() است.",
      pg_saved: "ذخیره شد ✓",
      pg_hint: "دکمهٔ اجرا (یا Ctrl+Enter) را بزن — خروجی همین‌جا نمایش داده می‌شود.",
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

  /* ------------------------- language switch -------------------------- */

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
    try { localStorage.setItem(LANG_KEY, next); } catch (e) { /* non-fatal */ }
    const root = document.documentElement;
    root.lang = next;
    if (next === "fa") root.setAttribute("dir", "rtl");
    else root.removeAttribute("dir");
    document.title = t("doc_title");
    document.querySelectorAll("[data-i18n]").forEach((el) => {
      el.textContent = t(el.getAttribute("data-i18n"));
    });
    document.querySelectorAll("[data-i18n-title]").forEach((el) => {
      el.setAttribute("title", t(el.getAttribute("data-i18n-title")));
    });
    buildLangPills();
    buildExamples();
    runBtn.textContent = running ? t("pg_running") : t("pg_run");
    setEngineStatus(PyRunner.status);
  }

  function setLang(next) {
    if (next === lang) return;
    document.body.classList.add("switching");
    setTimeout(() => {
      applyLang(next);
      document.body.classList.remove("switching");
    }, 200);
  }

  /* ------------------------ syntax highlighting ------------------------ */

  const KEYWORDS = new Set((
    "False None True and as assert async await break class continue def del " +
    "elif else except finally for from global if import in is lambda " +
    "nonlocal not or pass raise return try while with yield match case"
  ).split(" "));

  const BUILTINS = new Set((
    "abs aiter all any anext bin bool bytearray bytes callable chr " +
    "classmethod compile complex delattr dict dir divmod enumerate eval " +
    "exec filter float format frozenset getattr globals hasattr hash hex " +
    "id input int isinstance issubclass iter len list locals map max " +
    "memoryview min next object oct open ord pow print property range repr " +
    "reversed round set setattr slice sorted staticmethod str sum super " +
    "tuple type vars zip self cls __name__ __main__"
  ).split(" "));

  /* comments | triple strings | single-line strings | numbers | decorators | words */
  const TOKEN_RE = new RegExp(
    "(#[^\\n]*)" +
    "|([A-Za-z_]{0,2}\"\"\"[\\s\\S]*?\"\"\"|[A-Za-z_]{0,2}'''[\\s\\S]*?''')" +
    "|([A-Za-z_]{0,2}(?:\"(?:\\\\.|[^\"\\\\\\n])*\"|'(?:\\\\.|[^'\\\\\\n])*'))" +
    "|(\\.\\d[\\d_]*(?:[eE][+-]?\\d+)?[jJ]?\\b" +
    "|\\b\\d[\\d_]*(?:\\.\\d[\\d_]*)?(?:[eE][+-]?\\d+)?[jJ]?\\b" +
    "|\\b0[xXbBoO][0-9a-fA-F_]+\\b)" +
    "|(@[A-Za-z_]\\w*)" +
    "|([A-Za-z_]\\w*)",
    "g");

  function esc(s) {
    return String(s).replace(/&/g, "&amp;")
      .replace(/</g, "&lt;").replace(/>/g, "&gt;");
  }

  function highlightPython(src) {
    let out = "", last = 0, m;
    TOKEN_RE.lastIndex = 0;
    while ((m = TOKEN_RE.exec(src))) {
      out += esc(src.slice(last, m.index));
      const cls = m[1] ? "tk-c"
        : (m[2] || m[3]) ? "tk-s"
        : m[4] ? "tk-n"
        : m[5] ? "tk-d"
        : KEYWORDS.has(m[6]) ? "tk-k"
        : BUILTINS.has(m[6]) ? "tk-b"
        : "";
      out += cls ? '<span class="' + cls + '">' + esc(m[0]) + "</span>"
                 : esc(m[0]);
      last = m.index + m[0].length;
    }
    return out + esc(src.slice(last));
  }

  /* ------------------------------ editor ------------------------------ */

  const ta = $("pg-code");
  const hlCode = $("pg-hl").querySelector("code");
  const gutter = $("pg-gutter");

  function refreshHighlight() {
    // trailing newline keeps the last line visible when scrolled to the end
    hlCode.innerHTML = highlightPython(ta.value) + "\n";
  }

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
      if (ws) {
        ta.setRangeText("", lineStart, lineStart + Math.min(4, ws.length), "end");
      }
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
    const extra = /:\s*$/.test(line) ? "    " : "";
    ta.setRangeText("\n" + indent + extra, pos, ta.selectionEnd, "end");
    onEdit();
  }

  ta.addEventListener("keydown", (e) => {
    if (e.key === "Tab") handleTab(e);
    else if (e.key === "Enter" && !e.ctrlKey && !e.metaKey && !e.shiftKey &&
             ta.selectionStart === ta.selectionEnd) {
      handleEnter(e);
    } else if (e.key === "Enter" && (e.ctrlKey || e.metaKey)) {
      e.preventDefault();
      runCode();
    }
  });

  ["keyup", "click", "select"].forEach((ev) =>
    ta.addEventListener(ev, updatePos));

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
      try { localStorage.setItem(CODE_KEY, ta.value); } catch (e) { /* full */ }
      const s = $("pg-save");
      s.textContent = t("pg_saved");
      s.classList.add("show");
      setTimeout(() => s.classList.remove("show"), 1400);
    }, 400);
  }

  function saveNow() {
    try { localStorage.setItem(CODE_KEY, ta.value); } catch (e) { /* full */ }
  }
  window.addEventListener("pagehide", saveNow);

  /* ----------------------------- examples ----------------------------- */

  const DEFAULT_CODE = [
    "# Welcome to the Python Playground! 🐍",
    "# Write any Python 3.14 code here, then press Run (Ctrl+Enter).",
    "",
    "import sys",
    "",
    "print(f\"Hello, Python {sys.version_info.major}.{sys.version_info.minor}!\")",
    "",
    "for i in range(1, 6):",
    "    print(\" \" * (5 - i) + \"*\" * (2 * i - 1))",
    "",
    "print()",
    "print(\"Now try the Examples menu, or make this code yours ✏️\")",
  ].join("\n");

  const EXAMPLES = [
    {
      en: "Hello & f-strings", fa: "سلام و f-رشته‌ها",
      code: [
        "name = \"Ada\"",
        "age = 36",
        "",
        "print(f\"Hello, {name}!\")",
        "print(f\"Next year you'll be {age + 1}.\")",
        "",
        "price = 49.5",
        "print(f\"Total: {price:>10.2f}\")",
        "print(f\"{1234567:,}\")   # thousand separators",
      ].join("\n"),
    },
    {
      en: "FizzBuzz", fa: "فیز‌باز",
      code: [
        "for n in range(1, 21):",
        "    if n % 15 == 0:",
        "        print(\"FizzBuzz\")",
        "    elif n % 3 == 0:",
        "        print(\"Fizz\")",
        "    elif n % 5 == 0:",
        "        print(\"Buzz\")",
        "    else:",
        "        print(n)",
      ].join("\n"),
    },
    {
      en: "Fibonacci function", fa: "تابع فیبوناچی",
      code: [
        "def fib(n):",
        "    \"\"\"Return the first n Fibonacci numbers.\"\"\"",
        "    seq, a, b = [], 0, 1",
        "    for _ in range(n):",
        "        seq.append(a)",
        "        a, b = b, a + b",
        "    return seq",
        "",
        "print(fib(12))",
        "print(\"ratio:\", round(89 / 55, 6))",
      ].join("\n"),
    },
    {
      en: "Comprehensions & sorting", fa: "لیست‌سازی و مرتب‌سازی",
      code: [
        "words = \"the quick brown fox jumps over the lazy dog\".split()",
        "",
        "lengths = {w: len(w) for w in words}",
        "print(lengths)",
        "",
        "longest = sorted(words, key=len, reverse=True)[:3]",
        "print(\"longest:\", longest)",
        "",
        "squares = [n * n for n in range(10) if n % 2 == 0]",
        "print(squares)",
      ].join("\n"),
    },
    {
      en: "A tiny class", fa: "یک کلاس کوچک",
      code: [
        "class Stack:",
        "    def __init__(self):",
        "        self._items = []",
        "",
        "    def push(self, item):",
        "        self._items.append(item)",
        "",
        "    def pop(self):",
        "        return self._items.pop()",
        "",
        "    def __len__(self):",
        "        return len(self._items)",
        "",
        "s = Stack()",
        "for x in \"python\":",
        "    s.push(x)",
        "while len(s):",
        "    print(s.pop(), end=\" \")",
        "print()",
      ].join("\n"),
    },
    {
      en: "JSON round-trip", fa: "رفت‌وبرگشت JSON",
      code: [
        "import json",
        "",
        "person = {\"name\": \"Ada\", \"skills\": [\"math\", \"code\"], \"age\": 36}",
        "text = json.dumps(person, indent=2)",
        "print(text)",
        "",
        "back = json.loads(text)",
        "print(back[\"skills\"][1], \"== code?\")",
      ].join("\n"),
    },
    {
      en: "An honest traceback", fa: "یک خطای واقعی",
      code: [
        "# Errors show up here in red — read the LAST line first:",
        "# that's what went wrong, and the lines above show where.",
        "",
        "def average(numbers):",
        "    return sum(numbers) / len(numbers)",
        "",
        "print(average([2, 4, 6]))",
        "print(average([]))   # ZeroDivisionError!",
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
    if (EXAMPLES[i]) {
      ta.value = EXAMPLES[i].code;
      onEdit();
      ta.focus();
    }
    e.target.value = "";
  });

  /* ------------------------------ console ----------------------------- */

  const consoleBody = $("pg-console");

  function ensureConsoleEmptyHint() {
    if (!consoleBody.querySelector(".pg-hint") &&
        !consoleBody.querySelector(".pg-run-block")) {
      consoleBody.innerHTML = '<div class="pg-hint">' + esc(t("pg_hint")) +
        "</div>";
    }
  }

  function addRunBlock() {
    const hint = consoleBody.querySelector(".pg-hint");
    if (hint) hint.remove();
    const block = document.createElement("div");
    block.className = "pg-run-block";
    const time = new Date().toLocaleTimeString(lang === "fa" ? "fa-IR" : "en-GB");
    block.innerHTML =
      '<div class="pg-run-head">▶ main.py · ' + esc(time) + "</div>" +
      '<pre class="pg-run-out loading">' +
      (PyRunner.status === "ready"
        ? esc(t("pg_running"))
        : esc(t("pg_engine_loading"))) + "</pre>";
    consoleBody.appendChild(block);
    consoleBody.scrollTop = consoleBody.scrollHeight;
    return block;
  }

  function fillRunBlock(block, res, sec) {
    const out = block.querySelector(".pg-run-out");
    const status = document.createElement("div");
    status.className = "pg-run-status";
    block.appendChild(status);
    if (res.err === "load") {
      out.classList.remove("loading");
      out.textContent = t("pg_engine_fail", { err: res.error || "network error" });
      block.classList.add("err");
      status.classList.add("err");
      status.textContent = t("pg_err");
    } else if (res.err === "timeout") {
      out.classList.remove("loading");
      out.textContent = t("pg_engine_timeout", {
        sec: PyRunner.RUN_TIMEOUT_MS / 1000,
      });
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
        status.textContent = t("pg_ok", { sec: sec });
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
      const res = await PyRunner.run(ta.value);
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
    if ((e.ctrlKey || e.metaKey) && e.key === "Enter") {
      e.preventDefault();
      runCode();
    }
  });

  function setEngineStatus(s) {
    const el = $("pg-engine");
    el.className = "pg-engine " + s;
    el.textContent = s === "ready" ? t("pg_engine_ready")
      : s === "loading" ? t("pg_engine_loading")
      : t("pg_engine_idle");
  }
  PyRunner.addListener(setEngineStatus);

  /* --------------------------- other buttons -------------------------- */

  $("pg-clear").addEventListener("click", () => {
    consoleBody.innerHTML = '<div class="pg-hint">' + esc(t("pg_hint")) +
      "</div>";
  });

  $("pg-reset").addEventListener("click", () => {
    ta.value = DEFAULT_CODE;
    onEdit();
    ta.focus();
  });

  $("pg-close").addEventListener("click", () => {
    saveNow();
    window.close();
    // If the browser refused (page not opened by script), stay open.
  });

  /* ------------------------------- boot ------------------------------- */

  function onEdit() {
    refreshHighlight();
    rebuildGutter();
    updatePos();
    scheduleSave();
  }

  ta.addEventListener("input", onEdit);

  let saved = null;
  try { saved = localStorage.getItem(CODE_KEY); } catch (e) { /* blocked */ }
  ta.value = saved && saved.trim() ? saved : DEFAULT_CODE;

  buildLangPills();
  applyLang(lang);
  onEdit();
  ensureConsoleEmptyHint();
  ta.focus();
})();
