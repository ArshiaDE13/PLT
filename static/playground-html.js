"use strict";

/* HTML Playground — a live-preview IDE page.
   The browser IS the engine: your markup renders in a sandboxed iframe
   below the editor (auto-refresh while "Live" is checked, or on
   ▶ Run / Ctrl+Enter). Includes HTML syntax highlighting, ready-made
   examples, autosave and the same English/Persian switch as the app. */

(function () {
  const $ = (id) => document.getElementById(id);
  const CODE_KEY = "pytutor-playground-code-html-v1";
  const LANG_KEY = "pytutor-lang-v1";

  /* ------------------------------ i18n -------------------------------- */

  let lang = document.documentElement.lang === "fa" ? "fa" : "en";

  const STR = {
    en: {
      doc_title: "🛡️ HTML Playground",
      pg_title: "HTML Playground",
      pg_sub: "write HTML — see it render live, right in your browser",
      pg_run: "▶  Run",
      pg_running: "Rendering…",
      pg_examples_title: "Load an example",
      pg_examples_ph: "Examples…",
      pg_reset: "Reset",
      pg_clear: "Clear preview",
      pg_close: "✕ Close",
      pg_output: "PREVIEW",
      pg_live: "Live",
      pg_shortcut: "Ctrl+Enter = render · Tab = indent",
      pg_engine_idle: "the browser renders your markup — nothing to install",
      pg_engine_ready: "● live preview ready",
      pg_saved: "saved ✓",
      pg_hint: "Your markup renders here — live.",
      lang_aria: "Language",
    },
    fa: {
      doc_title: "🛡️ محیط تمرین HTML",
      pg_title: "محیط تمرین HTML",
      pg_sub: "HTML بنویس — همین‌جا زنده در مرورگر ببینش",
      pg_run: "▶  اجرا",
      pg_running: "در حال رندر…",
      pg_examples_title: "بارگذاری نمونه",
      pg_examples_ph: "نمونه‌ها…",
      pg_reset: "بازنشانی",
      pg_clear: "خالی کردن پیش‌نمایش",
      pg_close: "✕ بستن",
      pg_output: "پیش‌نمایش",
      pg_live: "زنده",
      pg_shortcut: "Ctrl+Enter = رندر · Tab = تورفتگی",
      pg_engine_idle: "مرورگر خودش نشانه‌گذاری‌ات را رندر می‌کند — چیزی برای نصب نیست",
      pg_engine_ready: "● پیش‌نمایش زنده آماده است",
      pg_saved: "ذخیره شد ✓",
      pg_hint: "نشانه‌گذاری‌ات همین‌جا زنده رندر می‌شود.",
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
    buildLangPills();
    buildExamples();
    runBtn.textContent = t("pg_run");
    $("pg-engine").textContent = t("pg_engine_ready");
    $("pg-engine").className = "pg-engine ready";
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

  const VOID_TAGS = new Set(("area base br col embed hr img input link meta " +
    "param source track wbr").split(" "));

  /* comments | doctype | tags (open/close + name) */
  const TOKEN_RE = /(<!--[\s\S]*?-->)|(<!DOCTYPE[^>]*>)|(<\/?[a-zA-Z][^>]*>?)/g;

  const TAG_ATTR_RE = /^(<\/?)([a-zA-Z][\w-]*)([\s\S]*?)(\/?>?)$/;

  function esc(s) {
    return String(s).replace(/&/g, "&amp;")
      .replace(/</g, "&lt;").replace(/>/g, "&gt;");
  }

  function highlightTag(tag) {
    const m = tag.match(TAG_ATTR_RE);
    if (!m) return esc(tag);
    let attrs = m[3].replace(
      /([a-zA-Z-]+)(=)("(?:[^"]*)"|'(?:[^']*)')?/g,
      (all, name, eq, val) => '<span class="tk-b">' + esc(name) + "</span>" +
        esc(eq) + (val ? '<span class="tk-s">' + esc(val) + "</span>" : ""));
    const cls = VOID_TAGS.has(m[2].toLowerCase()) ? "tk-n" : "tk-k";
    return '<span class="tk-d">' + esc(m[1]) + "</span>" +
      '<span class="' + cls + '">' + esc(m[2]) + "</span>" +
      attrs + '<span class="tk-d">' + esc(m[4]) + "</span>";
  }

  function highlightHtml(src) {
    let out = "", last = 0, m;
    TOKEN_RE.lastIndex = 0;
    while ((m = TOKEN_RE.exec(src))) {
      out += esc(src.slice(last, m.index));
      if (m[1]) out += '<span class="tk-c">' + esc(m[1]) + "</span>";
      else if (m[2]) out += '<span class="tk-d">' + esc(m[2]) + "</span>";
      else out += highlightTag(m[3]);
      last = m.index + m[0].length;
    }
    return out + esc(src.slice(last));
  }

  /* ------------------------------ editor ------------------------------ */

  const ta = $("pg-code");
  const hlCode = $("pg-hl").querySelector("code");
  const gutter = $("pg-gutter");
  const preview = $("pg-preview");
  const liveBox = $("pg-live");

  function refreshHighlight() {
    hlCode.innerHTML = highlightHtml(ta.value) + "\n";
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
    if (/>\s*$/.test(line) && !/\/>\s*$/.test(line)) extra = "  ";
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
      renderNow();
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
    "<!-- Welcome to the HTML Playground! 🛡️ -->",
    "<!-- Your markup renders live on the right. -->",
    "<!DOCTYPE html>",
    '<html lang="en">',
    "<head>",
    "  <title>My page</title>",
    "  <style>",
    "    body { font-family: sans-serif; text-align: center;",
    "           padding-top: 30px; }",
    "    h1 { color: #e44d26; }",
    "  </style>",
    "</head>",
    "<body>",
    "  <h1>Hello, HTML! 🛡️</h1>",
    "  <p>Edit me and watch the preview update.</p>",
    "  <button onclick=\"this.textContent = 'Clicked! 🎉'\">",
    "    Try clicking me",
    "  </button>",
    "</body>",
    "</html>",
  ].join("\n");

  const EXAMPLES = [
    {
      en: "Semantic page", fa: "صفحهٔ معنایی",
      code: [
        "<!DOCTYPE html>",
        '<html lang="en">',
        "<head><title>Semantic layout</title>",
        "<style>",
        "  body { font-family: sans-serif; margin: 0; }",
        "  header, footer { background: #e44d26; color: white; padding: 14px; }",
        "  nav { background: #f16529; padding: 8px 14px; }",
        "  main { display: flex; gap: 14px; padding: 14px; }",
        "  article { flex: 2; } aside { flex: 1; background: #fff4ee; padding: 12px; }",
        "</style></head>",
        "<body>",
        "  <header><strong>📰 The Daily Markup</strong></header>",
        "  <nav>Home · Tech · About</nav>",
        "  <main>",
        "    <article><h1>Top story</h1>",
        "      <p>Semantic HTML makes everyone happier.</p></article>",
        "    <aside><h3>Related</h3><p>Div soup: a cautionary tale</p></aside>",
        "  </main>",
        "  <footer><small>© 2026 The Daily Markup</small></footer>",
        "</body>",
        "</html>",
      ].join("\n"),
    },
    {
      en: "Lists & links", fa: "فهرست‌ها و پیوندها",
      code: [
        "<!DOCTYPE html>",
        '<html lang="en">',
        "<head><title>Lists & links</title></head>",
        "<body>",
        "  <h1>Web basics</h1>",
        "  <ul>",
        "    <li>HTML — structure",
        "      <ol>",
        "        <li>Elements</li>",
        "        <li>Attributes</li>",
        "      </ol>",
        "    </li>",
        "    <li>CSS — presentation</li>",
        "  </ul>",
        '  <p>Read the docs at <a href="https://developer.mozilla.org"',
        '     target="_blank" rel="noopener">MDN</a>.</p>',
        '  <p><a href="mailto:hi@example.com">Email us</a> or',
        '     <a href="tel:+15551234567">call us</a>.</p>',
        "</body>",
        "</html>",
      ].join("\n"),
    },
    {
      en: "Table", fa: "جدول",
      code: [
        "<!DOCTYPE html>",
        '<html lang="en">',
        "<head><title>Table</title>",
        "<style>",
        "  table { border-collapse: collapse; font-family: sans-serif; }",
        "  th, td { border: 1px solid #ddd; padding: 6px 16px; }",
        "  thead th { background: #e44d26; color: white; }",
        "  tfoot td { font-weight: bold; background: #fff4ee; }",
        "</style></head>",
        "<body>",
        "  <table>",
        '    <caption>Café order</caption>',
        "    <thead><tr><th>Item</th><th>Qty</th><th>Price</th></tr></thead>",
        "    <tbody>",
        "      <tr><td>Coffee</td><td>2</td><td>$6</td></tr>",
        "      <tr><td>Tea</td><td>1</td><td>$3</td></tr>",
        "    </tbody>",
        '    <tfoot><tr><td colspan="2">Total</td><td>$9</td></tr></tfoot>',
        "  </table>",
        "</body>",
        "</html>",
      ].join("\n"),
    },
    {
      en: "Form with validation", fa: "فرم با اعتبارسنجی",
      code: [
        "<!DOCTYPE html>",
        '<html lang="en">',
        "<head><title>Form</title>",
        "<style>",
        "  body { font-family: sans-serif; }",
        "  input { display: block; margin: 4px 0 12px; padding: 6px; }",
        "  input:invalid { border-color: #c0392b; }",
        "  input:valid { border-color: #2e8b57; }",
        "</style></head>",
        "<body>",
        "  <form>",
        '    <label for="user">Username (3 letters + 4 digits)</label>',
        '    <input id="user" required pattern="[A-Za-z]{3}[0-9]{4}"',
        '           title="e.g. ABC1234">',
        '    <label for="age">Age (1–120)</label>',
        '    <input id="age" type="number" min="1" max="120">',
        "    <button>Sign up</button>",
        "  </form>",
        "</body>",
        "</html>",
      ].join("\n"),
    },
    {
      en: "Canvas & SVG", fa: "canvas و SVG",
      code: [
        "<!DOCTYPE html>",
        '<html lang="en">',
        "<head><title>Graphics</title></head>",
        "<body>",
        "  <h2>SVG (DOM shapes)</h2>",
        '  <svg width="220" height="90">',
        '    <rect x="10" y="10" width="80" height="60" rx="10" fill="#f16529"></rect>',
        '    <circle cx="170" cy="40" r="30" fill="#ffd43b"></circle>',
        "  </svg>",
        "  <h2>Canvas (painted by JS)</h2>",
        '  <canvas id="c" width="220" height="90"',
        '          style="border:1px solid #ccc"></canvas>',
        "  <script>",
        '    const ctx = document.getElementById("c").getContext("2d");',
        '    ctx.fillStyle = "#2e8b57";',
        "    ctx.fillRect(30, 20, 100, 50);",
        "    ctx.beginPath();",
        "    ctx.arc(170, 45, 28, 0, Math.PI * 2);",
        '    ctx.fillStyle = "#03599c";',
        "    ctx.fill();",
        "  </script>",
        "</body>",
        "</html>",
      ].join("\n"),
    },
    {
      en: "dialog & details", fa: "dialog و details",
      code: [
        "<!DOCTYPE html>",
        '<html lang="en">',
        "<head><title>Widgets</title>",
        "<style>",
        "  body { font-family: sans-serif; }",
        "  dialog { border: 2px solid #f16529; border-radius: 10px; }",
        "  dialog::backdrop { background: rgba(0,0,0,.5); }",
        "</style></head>",
        "<body>",
        "  <details open>",
        "    <summary>What is HTML?</summary>",
        "    <p>The web's markup language.</p>",
        "  </details>",
        "  <p>",
        '    <button id="open">Open dialog</button>',
        "  </p>",
        '  <dialog id="dlg">',
        "    <p>A native modal — try Esc or Tab!</p>",
        '    <button onclick="dlg.close()">Close</button>',
        "  </dialog>",
        "  <script>",
        '    const dlg = document.getElementById("dlg");',
        '    document.getElementById("open")',
        '      .addEventListener("click", () => dlg.showModal());',
        "  </script>",
        "</body>",
        "</html>",
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
      renderNow();
      ta.focus();
    }
    e.target.value = "";
  });

  /* ------------------------------ render ------------------------------ */

  function renderNow() {
    preview.srcdoc = ta.value;
  }

  let liveTimer = null;
  function onEdit() {
    refreshHighlight();
    rebuildGutter();
    updatePos();
    scheduleSave();
    if (liveBox.checked) {
      clearTimeout(liveTimer);
      liveTimer = setTimeout(renderNow, 500);
    }
  }

  liveBox.addEventListener("change", () => {
    if (liveBox.checked) renderNow();
  });

  /* --------------------------- other buttons -------------------------- */

  const runBtn = $("pg-run");
  runBtn.addEventListener("click", renderNow);

  document.addEventListener("keydown", (e) => {
    if ((e.ctrlKey || e.metaKey) && e.key === "Enter") {
      e.preventDefault();
      renderNow();
    }
  });

  $("pg-clear").addEventListener("click", () => {
    preview.srcdoc = "";
  });

  $("pg-reset").addEventListener("click", () => {
    ta.value = DEFAULT_CODE;
    onEdit();
    renderNow();
    ta.focus();
  });

  $("pg-close").addEventListener("click", () => {
    saveNow();
    window.close();
  });

  /* ------------------------------- boot ------------------------------- */

  ta.addEventListener("input", onEdit);

  let saved = null;
  try { saved = localStorage.getItem(CODE_KEY); } catch (e) { /* blocked */ }
  ta.value = saved && saved.trim() ? saved : DEFAULT_CODE;

  buildLangPills();
  applyLang(lang);
  onEdit();
  renderNow();
  ta.focus();
})();
