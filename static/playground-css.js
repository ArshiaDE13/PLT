"use strict";

/* CSS Playground — a dual-pane live-preview IDE, specially for CSS.
   Two panes share one editor via tabs (🎨 CSS / 📄 HTML): style your own
   markup and watch it render in the sandboxed preview. Live mode
   re-renders 500ms after every keystroke; ▶ Run / Ctrl+Enter always
   does. Includes CSS+HTML syntax highlighting, ready-made examples,
   autosave and the same English/Persian switch as the app. */

(function () {
  const $ = (id) => document.getElementById(id);
  const CODE_KEY = "pytutor-playground-code-css-v1";
  const LANG_KEY = "pytutor-lang-v1";

  /* ------------------------------ i18n -------------------------------- */

  let lang = document.documentElement.lang === "fa" ? "fa" : "en";

  const STR = {
    en: {
      doc_title: "🎯 CSS Playground",
      pg_title: "CSS Playground",
      pg_sub: "style your own markup — CSS in one tab, HTML in the other",
      pg_run: "▶  Run",
      pg_examples_title: "Load an example",
      pg_examples_ph: "Examples…",
      pg_reset: "Reset",
      pg_clear: "Clear preview",
      pg_close: "✕ Close",
      pg_output: "PREVIEW",
      pg_live: "Live",
      pg_shortcut: "Ctrl+Enter = render · Tab = indent",
      pg_engine_idle: "the browser renders your styles — nothing to install",
      pg_engine_ready: "● live preview ready",
      pg_saved: "saved ✓",
      lang_aria: "Language",
    },
    fa: {
      doc_title: "🎯 محیط تمرین CSS",
      pg_title: "محیط تمرین CSS",
      pg_sub: "markup خودت را استایل بده — CSS در یک تب، HTML در تب دیگر",
      pg_run: "▶  اجرا",
      pg_examples_title: "بارگذاری نمونه",
      pg_examples_ph: "نمونه‌ها…",
      pg_reset: "بازنشانی",
      pg_clear: "خالی کردن پیش‌نمایش",
      pg_close: "✕ بستن",
      pg_output: "پیش‌نمایش",
      pg_live: "زنده",
      pg_shortcut: "Ctrl+Enter = رندر · Tab = تورفتگی",
      pg_engine_idle: "مرورگر خودش استایل‌هایت را رندر می‌کند — چیزی برای نصب نیست",
      pg_engine_ready: "● پیش‌نمایش زنده آماده است",
      pg_saved: "ذخیره شد ✓",
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

  /* ------------------- dual-pane state (CSS / HTML) ------------------- */

  let activePane = "css";
  const panes = {
    css: { value: "" },
    html: { value: "" },
  };

  function paneLabel(pane) {
    return pane === "css" ? (lang === "fa" ? "استایل" : "styles.css")
      : (lang === "fa" ? "نشانه‌گذاری" : "index.html");
  }

  function switchPane(next) {
    if (next === activePane) return;
    panes[activePane].value = ta.value;   // stash the outgoing pane
    activePane = next;
    ta.value = panes[next].value;
    document.getElementById("tab-css").classList.toggle("active", next === "css");
    document.getElementById("tab-html").classList.toggle("active", next === "html");
    onEdit();
    ta.focus();
  }

  /* ------------------------ syntax highlighting ------------------------ */

  const CSS_PROPS = new Set(("color background background-color " +
    "background-image background-size background-position background-repeat " +
    "border border-radius border-color border-width border-style " +
    "border-left border-right border-top border-bottom box-shadow " +
    "margin margin-top margin-right margin-bottom margin-left " +
    "margin-inline margin-block margin-inline-start margin-inline-end " +
    "padding padding-top padding-right padding-bottom padding-left " +
    "padding-inline padding-block width height min-width max-width " +
    "min-height max-height inline-size block-size aspect-ratio " +
    "display position top right bottom left z-index float clear " +
    "flex flex-direction flex-wrap flex-grow flex-shrink flex-basis " +
    "justify-content align-items align-content align-self align " +
    "grid grid-template-columns grid-template-rows grid-template-areas " +
    "grid-area grid-column grid-row grid-auto-flow gap row-gap column-gap " +
    "font-family font-size font-weight font-style line-height " +
    "letter-spacing word-spacing text-align text-decoration text-transform " +
    "text-shadow text-overflow white-space vertical-align " +
    "transition transition-property transition-duration " +
    "transition-timing-function transition-delay animation " +
    "animation-name animation-duration animation-timing-function " +
    "animation-delay animation-iteration-count animation-direction " +
    "animation-fill-mode transform transform-origin perspective " +
    "overflow overflow-x overflow-y opacity filter backdrop-filter " +
    "list-style list-style-type object-fit outline outline-offset " +
    "cursor pointer-events user-select content quotes counter-increment " +
    "columns column-count column-gap column-rule box-sizing " +
    "visibility direction writing-mode text-wrap resize inset"));

  const AT_RULES = new Set(("media supports keyframes font-face import " +
    "layer container page charset namespace property").split(" "));

  /* comments | at-rules | selectors-ish { | props | values */
  function highlightCss(src) {
    let out = "";
    let i = 0;
    const n = src.length;
    while (i < n) {
      const rest = src.slice(i);
      if (rest.startsWith("/*")) {                       // comment
        const end = rest.indexOf("*/");
        const stop = end === -1 ? n : i + end + 2;
        out += '<span class="tk-c">' + esc(src.slice(i, stop)) + "</span>";
        i = stop;
      } else if (rest[0] === "@") {                      // at-rule
        const m = rest.match(/^@[a-zA-Z-]+/);
        out += '<span class="tk-d">' + esc(m[0]) + "</span>";
        i += m[0].length;
      } else if (rest[0] === "{") {
        out += '<span class="tk-d">{</span>'; i++;
      } else if (rest[0] === "}") {
        out += '<span class="tk-d">}</span>'; i++;
      } else {
        // scan to the next structural character
        let j = i;
        while (j < n && !"{}@;/*".includes(src[j])) j++;
        const chunk = src.slice(i, j);
        // within the chunk, split "prop: value;" lines
        const lineRe = /([a-zA-Z-]+)(\s*:\s*)([^;{}]*)(;?)/g;
        let last = 0, m;
        while ((m = lineRe.exec(chunk))) {
          if (CSS_PROPS.has(m[1].toLowerCase())) {
            out += esc(chunk.slice(last, m.index));
            out += '<span class="tk-b">' + esc(m[1]) + "</span>" + esc(m[2]) +
              '<span class="tk-s">' + esc(m[3]) + "</span>" + esc(m[4]);
            last = m.index + m[0].length;
          }
        }
        out += esc(chunk.slice(last));
        // advance past any structural char not handled above (e.g. a lone /)
        i = Math.max(j, i + 1);
      }
    }
    return out;
  }

  function highlightHtml(src) {
    return esc(src)
      .replace(/(&lt;\/?)([a-zA-Z][\w-]*)/g,
        '$1<span class="tk-k">$2</span>')
      .replace(/([a-zA-Z-]+)=(&quot;.*?&quot;)/g,
        '<span class="tk-b">$1</span>=<span class="tk-s">$2</span>');
  }

  function esc(s) {
    return String(s).replace(/&/g, "&amp;")
      .replace(/</g, "&lt;").replace(/>/g, "&gt;");
  }

  function highlight(src) {
    return activePane === "css" ? highlightCss(src) : highlightHtml(src);
  }

  /* ------------------------------ editor ------------------------------ */

  const ta = $("pg-code");
  const hlCode = $("pg-hl").querySelector("code");
  const gutter = $("pg-gutter");
  const preview = $("pg-preview");
  const liveBox = $("pg-live");

  function refreshHighlight() {
    hlCode.innerHTML = highlight(ta.value) + "\n";
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
    if (/\{\s*$/.test(line) && activePane === "css") extra = "  ";
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
      saveNow();
      const s = $("pg-save");
      s.textContent = t("pg_saved");
      s.classList.add("show");
      setTimeout(() => s.classList.remove("show"), 1400);
    }, 400);
  }

  function saveNow() {
    try { localStorage.setItem(CODE_KEY, JSON.stringify(panes)); } catch (e) {}
  }
  window.addEventListener("pagehide", saveNow);

  /* ----------------------------- examples ----------------------------- */

  const DEFAULT = {
    css: [
      "/* Style the markup on the HTML tab! 🎯 */",
      "body {",
      "  font-family: sans-serif;",
      "  background: #f2f8fe;",
      "  display: grid;",
      "  place-items: center;",
      "  min-height: 100vh;",
      "  margin: 0;",
      "}",
      "",
      ".card {",
      "  background: white;",
      "  padding: 28px 36px;",
      "  border-radius: 14px;",
      "  box-shadow: 0 10px 30px rgba(21, 114, 182, 0.25);",
      "  text-align: center;",
      "  transition: transform 0.3s ease;",
      "}",
      "",
      ".card:hover {",
      "  transform: translateY(-6px) scale(1.03);",
      "}",
      "",
      "h1 {",
      "  color: #1572b6;",
      "  margin: 0 0 6px;",
      "}",
      "",
      "p {",
      "  color: #5b6b7a;",
      "}",
    ].join("\n"),
    html: [
      '<div class="card">',
      "  <h1>Hello, CSS! 🎯</h1>",
      "  <p>Edit the CSS tab — I update live.</p>",
      "  <p>Switch tabs above: 🎨 CSS / 📄 HTML</p>",
      "</div>",
    ].join("\n"),
  };

  const EXAMPLES = [
    {
      en: "Flexbox navbar", fa: "نوار ناوبری Flexbox",
      css: [
        "body { margin: 0; font-family: sans-serif; }",
        ".navbar {",
        "  display: flex;",
        "  align-items: center;",
        "  gap: 16px;",
        "  background: #1572b6;",
        "  color: white;",
        "  padding: 12px 20px;",
        "}",
        ".navbar .logo { font-weight: bold; font-size: 1.2rem; }",
        ".navbar nav { display: flex; gap: 14px; margin-inline-start: auto; }",
        ".navbar a { color: #c9e6f9; text-decoration: none; }",
        ".navbar a:hover { color: white; text-decoration: underline; }",
      ].join("\n"),
      html: [
        '<div class="navbar">',
        '  <span class="logo">🎯 CSS Cafe</span>',
        "  <nav>",
        '    <a href="#">Home</a>',
        '    <a href="#">Menu</a>',
        '    <a href="#">About</a>',
        "  </nav>",
        "</div>",
        '<p style="padding: 16px">A flexbox navbar: logo left, links pushed',
        "  right with margin-inline-start: auto.</p>",
      ].join("\n"),
    },
    {
      en: "Card grid (auto-fit)", fa: "شبکهٔ کارت (auto-fit)",
      css: [
        "body { margin: 0; font-family: sans-serif; background: #f2f8fe; }",
        ".cards {",
        "  display: grid;",
        "  grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));",
        "  gap: 14px;",
        "  padding: 16px;",
        "}",
        ".card {",
        "  background: white;",
        "  border-radius: 12px;",
        "  padding: 18px;",
        "  box-shadow: 0 4px 14px rgba(21, 114, 182, 0.15);",
        "  transition: transform 0.25s ease;",
        "}",
        ".card:hover { transform: translateY(-4px); }",
        ".card h3 { color: #1572b6; margin: 0 0 6px; }",
      ].join("\n"),
      html: [
        '<div class="cards">',
        '  <div class="card"><h3>One</h3>Resize the preview —',
        "    columns come and go.</div>",
        '  <div class="card"><h3>Two</h3>No media queries.</div>',
        '  <div class="card"><h3>Three</h3>auto-fit + minmax.</div>',
        '  <div class="card"><h3>Four</h3>fr units share space.</div>',
        '  <div class="card"><h3>Five</h3>gap for spacing.</div>',
        "</div>",
      ].join("\n"),
    },
    {
      en: "Transitions & transforms", fa: "transition و transform",
      css: [
        "body { margin: 0; font-family: sans-serif; background: #0a3c63;",
        "  min-height: 100vh; display: grid; place-items: center; }",
        ".stage { display: flex; gap: 18px; }",
        ".tile {",
        "  width: 90px; height: 90px; border-radius: 14px;",
        "  background: #33a9dc; color: white;",
        "  display: grid; place-items: center; font-weight: bold;",
        "  cursor: pointer;",
        "  transition: transform 0.3s ease, background 0.3s ease;",
        "}",
        ".tile:hover {",
        "  transform: translateY(-12px) rotate(6deg) scale(1.1);",
        "  background: #ffd43b; color: #0a3c63;",
        "}",
      ].join("\n"),
      html: [
        '<div class="stage">',
        '  <div class="tile">lift</div>',
        '  <div class="tile">tilt</div>',
        '  <div class="tile">zoom</div>',
        "</div>",
      ].join("\n"),
    },
    {
      en: "Custom properties (theming)", fa: "متغیرهای سفارشی (تم)",
      css: [
        ":root {",
        "  --bg: #f2f8fe; --card: white; --text: #263238;",
        "  --brand: #1572b6;",
        "}",
        ".dark {",
        "  --bg: #1c2a36; --card: #22333f; --text: #e8f1f8;",
        "  --brand: #7fd0ff;",
        "}",
        "body { margin: 0; font-family: sans-serif; background: var(--bg);",
        "  color: var(--text); min-height: 100vh;",
        "  display: grid; place-items: center; }",
        ".theme-card {",
        "  background: var(--card); padding: 24px 30px;",
        "  border-radius: 14px; text-align: center;",
        "  border: 2px solid var(--brand);",
        "}",
        "button { background: var(--brand); color: var(--bg);",
        "  border: none; padding: 8px 18px; border-radius: 8px;",
        "  cursor: pointer; font-weight: bold; }",
      ].join("\n"),
      html: [
        '<div class="theme-card">',
        "  <h2>One token set, two themes</h2>",
        "  <p>Click the button to toggle .dark on the body.</p>",
        '  <button onclick="document.body.classList.toggle(\'dark\')">',
        "    Toggle theme",
        "  </button>",
        "</div>",
      ].join("\n"),
    },
    {
      en: "Grid template areas", fa: "grid-template-areas",
      css: [
        "body { margin: 0; font-family: sans-serif; min-height: 100vh;",
        "  display: grid; place-items: center; background: #f2f8fe; }",
        ".page {",
        "  display: grid;",
        "  grid-template-areas:",
        '    "header header"',
        '    "nav    main"',
        '    "footer footer";',
        "  grid-template-columns: 150px 1fr;",
        "  grid-template-rows: auto 1fr auto;",
        "  gap: 8px;",
        "  width: min(90%, 460px);",
        "  min-height: 300px;",
        "}",
        ".page > * { border-radius: 8px; padding: 12px; color: white; }",
        ".page header { grid-area: header; background: #1572b6; }",
        ".page nav { grid-area: nav; background: #2e8b57; }",
        ".page main { grid-area: main; background: #eaf4fd; color: #1572b6; }",
        ".page footer { grid-area: footer; background: #37475a; }",
      ].join("\n"),
      html: [
        '<div class="page">',
        "  <header>header</header>",
        "  <nav>nav</nav>",
        "  <main>main — the ASCII-art layout</main>",
        "  <footer>footer</footer>",
        "</div>",
      ].join("\n"),
    },
    {
      en: "Animation playground", fa: "زمین بازی انیمیشن",
      css: [
        "body { margin: 0; font-family: sans-serif; background: #0a3c63;",
        "  min-height: 100vh; display: grid; place-items: center;",
        "  overflow: hidden; }",
        ".orbit { position: relative; width: 200px; height: 200px; }",
        ".planet {",
        "  position: absolute; inset: 0;",
        "  animation: spin 6s linear infinite;",
        "}",
        ".planet::before {",
        '  content: "🛡️";',
        "  position: absolute; top: -14px; left: 50%;",
        "  font-size: 26px;",
        "}",
        ".core {",
        "  position: absolute; inset: 70px;",
        "  border-radius: 50%;",
        "  background: radial-gradient(circle at 35% 30%, #7fd0ff, #1572b6);",
        "  display: grid; place-items: center;",
        "  color: white; font-weight: bold;",
        "}",
        "@keyframes spin {",
        "  from { transform: rotate(0deg); }",
        "  to   { transform: rotate(360deg); }",
        "}",
      ].join("\n"),
      html: [
        '<div class="orbit">',
        '  <div class="planet"></div>',
        '  <div class="core">CSS</div>',
        "</div>",
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
      panes.css.value = EXAMPLES[i].css;
      panes.html.value = EXAMPLES[i].html;
      activePane = "css";
      ta.value = panes.css.value;
      document.getElementById("tab-css").classList.add("active");
      document.getElementById("tab-html").classList.remove("active");
      onEdit();
      renderNow();
      ta.focus();
    }
    e.target.value = "";
  });

  /* ------------------------------ render ------------------------------ */

  /* Compose the preview document: if the HTML pane is a full document,
     inject the CSS before </head>; otherwise wrap the fragment. */
  function composeDoc() {
    const css = panes.css.value;
    const styleTag = "<style>\n" + css + "\n</style>";
    let html = panes.html.value.trim();
    if (/<\/head>/i.test(html)) {
      html = html.replace(/<\/head>/i, styleTag + "\n</head>");
    } else if (/<html[^>]*>/i.test(html)) {
      html = html.replace(/(<html[^>]*>)/i, "$1\n" + styleTag);
    } else {
      html = "<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n" +
        '<meta charset="utf-8">\n' + styleTag + "\n</head>\n<body>\n" +
        html + "\n</body>\n</html>";
    }
    return html;
  }

  function renderNow() {
    preview.srcdoc = composeDoc();
  }

  let liveTimer = null;
  function onEdit() {
    panes[activePane].value = ta.value;
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

  /* ------------------------------- tabs ------------------------------- */

  document.getElementById("tab-css").addEventListener("click",
    () => switchPane("css"));
  document.getElementById("tab-html").addEventListener("click",
    () => switchPane("html"));

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
    panes.css.value = DEFAULT.css;
    panes.html.value = DEFAULT.html;
    activePane = "css";
    ta.value = panes.css.value;
    document.getElementById("tab-css").classList.add("active");
    document.getElementById("tab-html").classList.remove("active");
    onEdit();
    renderNow();
    ta.focus();
  });

  $("pg-close").addEventListener("click", () => {
    saveNow();
    window.close();
  });

  /* ------------------------------- boot ------------------------------- */

  let saved = null;
  try { saved = JSON.parse(localStorage.getItem(CODE_KEY)); } catch (e) {}
  if (saved && typeof saved === "object") {
    // only strings are valid pane content — a corrupted (object) save
    // self-heals back to the defaults instead of showing [object Object]
    panes.css.value = typeof saved.css === "string" ? saved.css : DEFAULT.css;
    panes.html.value = typeof saved.html === "string" ? saved.html : DEFAULT.html;
  } else {
    panes.css.value = DEFAULT.css;
    panes.html.value = DEFAULT.html;
  }
  ta.value = panes.css.value;

  buildLangPills();
  applyLang(lang);
  onEdit();
  renderNow();
  ta.focus();
})();
