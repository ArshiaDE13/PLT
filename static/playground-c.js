"use strict";

/* C Playground — a small self-contained IDE page for the C course.
   It shares the CEngine interpreter (wrapped in a worker by crunner.js)
   with the course, adds a syntax-highlighted editor, an optional stdin
   box for scanf(), a run console, ready-made examples, autosave and the
   same English/Persian language switch as the main app. */

(function () {
  const $ = (id) => document.getElementById(id);
  const CODE_KEY = "pytutor-playground-code-c-v1";
  const LANG_KEY = "pytutor-lang-v1";

  /* ------------------------------ i18n -------------------------------- */

  let lang = document.documentElement.lang === "fa" ? "fa" : "en";

  const STR = {
    en: {
      doc_title: "🔷 C Playground",
      pg_title: "C Playground",
      pg_sub: "write and run real C — right in your browser",
      pg_run: "▶  Run",
      pg_running: "Running…",
      pg_examples_title: "Load an example",
      pg_examples_ph: "Examples…",
      pg_reset: "Reset",
      pg_clear: "Clear console",
      pg_close: "✕ Close",
      pg_output: "OUTPUT",
      pg_stdin: "stdin (for scanf)",
      pg_shortcut: "Ctrl+Enter = run · Tab = indent",
      pg_no_output: "(no output)",
      pg_ok: "✓ finished · {sec}s · exit {code}",
      pg_err: "✗ error (see output above)",
      pg_engine_idle: "C engine ships with the site — instant start",
      pg_engine_loading: "⏳ starting the C engine…",
      pg_engine_ready: "● C engine ready",
      pg_engine_fail: "Couldn't start the C engine ({err}). Press Run again.",
      pg_engine_timeout: "Timed out after {sec}s — the code may be stuck in " +
        "an infinite loop or waiting for scanf().",
      pg_saved: "saved ✓",
      pg_hint: "Press ▶ Run (or Ctrl+Enter) — your output appears here.",
      lang_aria: "Language",
    },
    fa: {
      doc_title: "🔷 محیط تمرین C",
      pg_title: "محیط تمرین C",
      pg_sub: "کد C واقعی بنویس و همین‌جا در مرورگر اجرا کن",
      pg_run: "▶  اجرا",
      pg_running: "در حال اجرا…",
      pg_examples_title: "بارگذاری نمونه",
      pg_examples_ph: "نمونه‌ها…",
      pg_reset: "بازنشانی",
      pg_clear: "پاک کردن خروجی",
      pg_close: "✕ بستن",
      pg_output: "خروجی",
      pg_stdin: "ورودی stdin (برای scanf)",
      pg_shortcut: "Ctrl+Enter = اجرا · Tab = تورفتگی",
      pg_no_output: "(خروجی نیست)",
      pg_ok: "✓ تمام شد · {sec} ثانیه · کد خروج {code}",
      pg_err: "✗ خطا (خروجی را بالا ببین)",
      pg_engine_idle: "موتور C همراه خود سایت است — شروع فوری",
      pg_engine_loading: "⏳ در حال آماده‌سازی موتور C…",
      pg_engine_ready: "● موتور C آماده است",
      pg_engine_fail: "راه‌اندازی موتور C ممکن نشد ({err}). دوباره «اجرا» را بزن.",
      pg_engine_timeout: "پس از {sec} ثانیه متوقف شد — احتمالاً کد در " +
        "حلقهٔ بی‌نهایت گیر کرده یا منتظر scanf() است.",
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
    $("pg-stdin").placeholder = lang === "fa"
      ? "مثلاً 42 و بعد Enter" : "e.g. 42 then Enter";
    buildLangPills();
    buildExamples();
    runBtn.textContent = running ? t("pg_running") : t("pg_run");
    setEngineStatus(CRunner.status);
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
    "auto break case char const continue default do double else enum extern " +
    "float for goto if inline int long register restrict return short signed " +
    "sizeof static struct switch typedef union unsigned void volatile while " +
    "_Bool _Complex _Generic _Alignof _Alignas _Noreturn _Thread_local"
  ).split(" "));

  const LIBFUNCS = new Set((
    "printf fprintf sprintf snprintf puts putchar getchar getc fgetc putc " +
    "fputc fputs fgets gets scanf fscanf sscanf perror malloc calloc realloc " +
    "free exit _Exit _exit quick_exit abort atexit abs labs llabs atoi atol " +
    "atof strtol strtod strtoul rand srand qsort bsearch getenv system " +
    "memcpy memmove memset memcmp strlen strcpy strncpy strcat strncat strcmp " +
    "strncmp strchr strrchr strstr strtok strdup strspn strcspn strpbrk " +
    "fopen freopen fclose fread fwrite fseek ftell rewind feof ferror remove " +
    "rename fflush time clock difftime mktime localtime gmtime strftime " +
    "timespec_get setjmp longjmp signal raise isalpha isdigit isalnum " +
    "isspace isupper islower ispunct isprint iscntrl isxdigit tolower toupper " +
    "sin cos tan asin acos atan atan2 sinh cosh tanh exp log log10 log2 sqrt " +
    "pow floor ceil fabs fmod round trunc cbrt fmin fmax hypot creal cimag " +
    "cabs conj carg cexp clog csqrt csin ccos cpow"
  ).split(" "));

  /* comments | preprocessor | strings/chars | numbers | words */
  const TOKEN_RE = new RegExp(
    "(//[^\\n]*|/\\*[\\s\\S]*?\\*/)" +
    "|(^[ \\t]*#[ \\t]*[A-Za-z]\\w*)" +
    "|(\"(?:\\\\.|[^\"\\\\\\n])*\"|'(?:\\\\.|[^'\\\\\\n])*')" +
    "|(\\b0[xX][0-9a-fA-F]+[uUlL]*\\b|\\b\\d[\\d.]*(?:[eE][+-]?\\d+)?[uUlLfF]*\\b)" +
    "|([A-Za-z_]\\w*)",
    "gm");

  function esc(s) {
    return String(s).replace(/&/g, "&amp;")
      .replace(/</g, "&lt;").replace(/>/g, "&gt;");
  }

  function highlightC(src) {
    let out = "", last = 0, m;
    TOKEN_RE.lastIndex = 0;
    while ((m = TOKEN_RE.exec(src))) {
      out += esc(src.slice(last, m.index));
      const cls = m[1] ? "tk-c"
        : m[2] ? "tk-d"
        : m[3] ? "tk-s"
        : m[4] ? "tk-n"
        : KEYWORDS.has(m[5]) ? "tk-k"
        : LIBFUNCS.has(m[5]) ? "tk-b"
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
    hlCode.innerHTML = highlightC(ta.value) + "\n";
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
    // after { indent one level; after } keep the same level
    let extra = "";
    if (/\{\s*$/.test(line)) extra = "    ";
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
    "// Welcome to the C Playground! 🔷",
    "// Write ISO C here, then press Run (Ctrl+Enter).",
    "// Everything runs in your browser — nothing to install.",
    "",
    "#include <stdio.h>",
    "",
    "int main(void) {",
    '    printf("Hello, C!\\n");',
    "",
    "    for (int i = 1; i <= 5; i++) {",
    '        printf("%d squared is %d\\n", i, i * i);',
    "    }",
    "",
    "    return 0;",
    "}",
  ].join("\n");

  const EXAMPLES = [
    {
      en: "Hello & printf formats", fa: "سلام و قالب‌های printf",
      code: [
        "#include <stdio.h>",
        "",
        "int main(void) {",
        '    printf("[%5d] [%-5d] [%05d]\\n", 42, 42, 42);',
        '    printf("[%10.3f] [%g]\\n", 3.14159, 1.0 / 3.0);',
        '    printf("%s has %zu letters\\n", "Beej", strlen("Beej"));',
        "    return 0;",
        "}",
      ].join("\n"),
    },
    {
      en: "FizzBuzz", fa: "فیزباز",
      code: [
        "#include <stdio.h>",
        "",
        "int main(void) {",
        "    for (int n = 1; n <= 20; n++) {",
        "        if (n % 15 == 0)      printf(\"FizzBuzz\\n\");",
        "        else if (n % 3 == 0)  printf(\"Fizz\\n\");",
        "        else if (n % 5 == 0)  printf(\"Buzz\\n\");",
        "        else                  printf(\"%d\\n\", n);",
        "    }",
        "    return 0;",
        "}",
      ].join("\n"),
    },
    {
      en: "Pointers & swap", fa: "اشاره‌گرها و جابه‌جایی",
      code: [
        "#include <stdio.h>",
        "",
        "void swap(int *a, int *b) {",
        "    int t = *a; *a = *b; *b = t;",
        "}",
        "",
        "int main(void) {",
        "    int x = 1, y = 2;",
        "    int *p = &x;",
        '    printf("x = %d, *p = %d\\n", x, *p);',
        "    *p = 99;",
        '    printf("after *p = 99, x = %d\\n", x);',
        "    swap(&x, &y);",
        '    printf("after swap: %d %d\\n", x, y);',
        "    return 0;",
        "}",
      ].join("\n"),
    },
    {
      en: "Malloc & linked list", fa: "malloc و لیست پیوندی",
      code: [
        "#include <stdio.h>",
        "#include <stdlib.h>",
        "",
        "struct node { int v; struct node *next; };",
        "",
        "int main(void) {",
        "    struct node *head = NULL, *tail = NULL;",
        "    for (int i = 1; i <= 5; i++) {",
        "        struct node *n = malloc(sizeof(struct node));",
        "        n->v = i * i;",
        "        n->next = NULL;",
        "        if (tail) tail->next = n; else head = n;",
        "        tail = n;",
        "    }",
        "    for (struct node *n = head; n; n = n->next)",
        '        printf("%d ", n->v);',
        '    printf("\\n");',
        "    while (head) { struct node *n = head; head = head->next; free(n); }",
        "    return 0;",
        "}",
      ].join("\n"),
    },
    {
      en: "Structs & qsort", fa: "struct و qsort",
      code: [
        "#include <stdio.h>",
        "#include <stdlib.h>",
        "#include <string.h>",
        "",
        "typedef struct {",
        "    const char *name;",
        "    int score;",
        "} player;",
        "",
        "int by_score(const void *a, const void *b) {",
        "    return ((const player *)b)->score - ((const player *)a)->score;",
        "}",
        "",
        "int main(void) {",
        "    player team[] = {",
        '        {"Ada", 91}, {"Grace", 97}, {"Linus", 84},',
        "    };",
        "    qsort(team, 3, sizeof(player), by_score);",
        '    printf("leaderboard:\\n");',
        "    for (int i = 0; i < 3; i++)",
        '        printf("  %s — %d\\n", team[i].name, team[i].score);',
        "    (void)strcmp;",
        "    return 0;",
        "}",
      ].join("\n"),
    },
    {
      en: "scanf with stdin", fa: "scanf با ورودی stdin",
      code: [
        "// Type numbers in the stdin box above, e.g.:",
        "// 7",
        "// then press Run.",
        "#include <stdio.h>",
        "",
        "int main(void) {",
        "    int n;",
        '    printf("enter a number: ");',
        '    if (scanf("%d", &n) == 1) {',
        '        printf("%d * 2 = %d\\n", n, n * 2);',
        "    } else {",
        '        printf("no number seen (EOF)\\n");',
        "    }",
        "    return 0;",
        "}",
      ].join("\n"),
    },
    {
      en: "Files", fa: "فایل‌ها",
      code: [
        "#include <stdio.h>",
        "",
        "int main(void) {",
        '    FILE *f = fopen("names.txt", "r");',
        "    char line[64];",
        "    while (fgets(line, sizeof line, f)) {",
        '        printf("hi %s", line);',
        "    }",
        "    fclose(f);",
        "",
        '    FILE *out = fopen("story2.txt", "w");',
        '    fprintf(out, "written in the sandbox\\n");',
        "    fclose(out);",
        "    return 0;",
        "}",
      ].join("\n"),
    },
    {
      en: "Bit games", fa: "بازی با بیت‌ها",
      code: [
        "#include <stdio.h>",
        "",
        "int main(void) {",
        "    unsigned flags = 0;",
        "    flags |= 0x04;  flags |= 0x01;      /* set bits 2 and 0 */",
        '    printf("flags = 0x%x\\n", flags);',
        '    printf("bit 2? %d\\n", (flags & 0x04) != 0);',
        "    flags &= ~0x01;                     /* clear bit 0 */",
        '    printf("bit 0? %d\\n", (flags & 0x01) != 0);',
        "",
        "    int x = 1;",
        "    while (x < 100) {",
        '        printf("%d ", x);',
        "        x <<= 1;                        /* double it */",
        "    }",
        '    printf("\\n");',
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
    if (EXAMPLES[i]) {
      ta.value = EXAMPLES[i].code;
      onEdit();
      ta.focus();
    }
    e.target.value = "";
  });

  /* ------------------------------ console ----------------------------- */

  const consoleBody = $("pg-console");
  const stdinBox = $("pg-stdin");

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
      '<div class="pg-run-head">▶ main.c · ' + esc(time) + "</div>" +
      '<pre class="pg-run-out loading">' +
      esc(t("pg_running")) + "</pre>";
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
        sec: CRunner.RUN_TIMEOUT_MS / 1000,
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
        status.textContent = t("pg_ok", { sec: sec, code: res.exit !== undefined ? res.exit : 0 });
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
      const res = await CRunner.run(ta.value, stdinBox.value);
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
  CRunner.addListener(setEngineStatus);

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
