# 🐍 Python Tutor

An interactive, **pure-browser** course that teaches Python from scratch,
built from the official **Python 3.14 documentation** in its recommended
order: the 16-chapter Tutorial, then **"Python Setup and Usage"
(using)**, a practice-oriented **Library Reference** section, the
**HowTo** guides, and a tour of the **Language Reference**. Read the
lesson, look at the diagrams, then prove your knowledge with four kinds
of quiz questions — and write and run real Python 3.14 code right in
your browser.

No Python, no server, no installation — the whole course ships as static
files, so anyone can open it from a live link and start learning.

![stack](https://img.shields.io/badge/static_web_app-✔-green)

## What's inside

- **31 chapters** in official doc order — the 16-chapter tutorial, the
  *Using Python* section (running the interpreter, Windows, other
  platforms & editors), the *Library Reference* distilled the project
  way (files & paths with `pathlib`, supercharged containers, data &
  the web, real programs with `argparse`/`subprocess`/`sqlite3`/
  `logging`/`unittest`), the *HowTo* guides (sorting, regex, deeper
  argparse/logging/enum, Unicode + async), and finally a *Language
  Reference* tour: the data model (identity vs value, dunders), scopes
  & execution (`global`/`nonlocal`, frames, tracebacks), expressions
  & operator precedence, and the import system (`sys.modules`,
  packages, `__main__`).
- **w3schools-style sidebar navigation** — every chapter expands into
  its own sub-list: one entry per lesson plus a **Quiz** entry at the
  end (with an answered-count badge). Exactly one chapter is expanded
  at a time and the open group follows whatever you are reading;
  clicking the header of the chapter you're on collapses the list.
- **🧪 Playground** — a dedicated IDE-style window (button in the
  sidebar, next to the progress box) with a syntax-highlighted
  `main.py` editor (line numbers, auto-indent, Tab/Shift+Tab), a run
  console with per-run output blocks and timing, 7 ready-made examples
  (f-strings, FizzBuzz, Fibonacci, comprehensions, a class, JSON, an
  honest traceback), autosave to the browser, and the same
  English/فارسی switch as the course. Code is written once, saved
  between sessions, and runs on the same in-browser Python engine.
- **Visual diagrams** — every major topic has a drawn-to-order SVG image
  (string indexing, control flow, exception hierarchy, scopes, float
  representation, venv isolation, and more). No image files needed.
- **4 quiz formats**, checked instantly in your browser:
  - *Multiple choice* — pick the right answer.
  - *Fill the blank* — type the missing word.
  - *Order the lines* — click the code lines in the correct order.
  - *Write the code* — complete real code snippets by filling the blanks.
- **"Try it yourself" playground** on every lesson — write Python, hit
  *Run*, and see real output. Execution happens in your browser: Pyodide
  (CPython 3.14 compiled to WebAssembly) runs the code in a sandboxed
  Web Worker with a 10-second kill switch for infinite loops.
- **Bilingual: English + فارسی** — a 🌐 *English | فارسی* toggle (on the
  welcome card and in the sidebar) switches the whole interface, text
  direction (RTL), fonts (Vazirmatn) and Persian digits with a smooth
  crossfade animation. The choice is remembered; browsers set to Persian
  start in Persian automatically. The whole course is fully translated —
  every chapter, lesson, quiz question and explanation across all five
  sections (Tutorial, Using Python, Library, HowTo, Language Reference) —
  while code listings and diagrams stay English on purpose (so real code
  is always copy-pasteable).
- **Personalized** — on first launch the app asks for your name, then
  greets you, wishes you luck on quizzes, and celebrates with you when you
  finish a chapter or the whole course. Change it anytime with the
  "✏️ Change name" button.
- **Progress tracking** — the overall progress bar fills question by
  question as you get answers right, each chapter's number ball turns
  green once you've answered all its questions, and everything is saved
  in the browser between sessions.
- **Polished motion** — the name page has an animated gradient, drifting
  glow orbs and floating emojis with a staggered card entrance; the rest
  of the site has card transitions, hover lifts, a shimmering progress
  bar and pop-in feedback (all disabled for users who prefer reduced
  motion). Quiz feedback stays on screen for every question — nothing
  advances until you click the button.
- **Deployable anywhere** — one static folder (`static/`), no build step
  needed at host time: works on GitHub Pages, Netlify, Cloudflare Pages,
  Vercel, or any static file server. (Legacy desktop builds still exist —
  see below.)

## Deploy it online — live link, zero installation

The site lives in the `static/` folder: `index.html` + `style.css` +
`app.js` + `data.js` (the whole course, pre-rendered with its diagrams).
Everything runs in the visitor's browser — quiz scoring, progress, even
the Python engine (loaded lazily from a CDN on the first *Run* click,
then cached by the browser).

### Option A — GitHub Pages (recommended, uses Actions)

1. Push this folder to a GitHub repo.
2. In the repo: **Settings → Pages → Source → "GitHub Actions"**.
3. Push to `main` (or click **Run workflow** in the Actions tab).

`.github/workflows/pages.yml` regenerates `data.js`, runs the self-test
as a gate, and publishes the site — your live link is
`https://<user>.github.io/<repo>/`.

### Option B — Netlify (drag & drop, 30 seconds)

1. Go to [app.netlify.com/drop](https://app.netlify.com/drop).
2. Drag the `static/` folder onto the page.

Done — you get a live `https://<name>.netlify.app` link. For Git deploys,
`netlify.toml` is already configured (it runs `python build_static.py`
and publishes `static/`).

### Option C — anything else

`static/` is a plain static site: point Cloudflare Pages or Vercel at it
(publish dir `static`), or copy it onto any web server or object storage.
There is no mandatory build step — `data.js` is committed, so the folder
works as-is.

> **Note:** the "Try it" playground downloads the Pyodide engine
> (~10 MB, cached after the first run) from jsDelivr the first time a
> visitor presses **Run**. If the visitor is offline, the button shows a
> clear message; everything else on the site works without internet.

## Run it locally (dev mode, needs Python 3.8+)

```text
python app.py
```

or double-click `run.bat`. Your browser opens
[http://127.0.0.1:8765/](http://127.0.0.1:8765/). Close the console window
to stop the app.

Options:

```text
python app.py --port 9000     # different port
python app.py --no-browser    # don't auto-open the browser
python app.py --selftest      # headless self-test of content + quizzes
```

## Legacy (optional): standalone desktop builds

> The web app above is the product — a desktop executable is no longer
> needed, but these build scripts are kept for offline/air-gapped use.
> PyInstaller **cannot cross-compile**, so build the Windows version on
> Windows and the Linux version on Linux.

### 🪟 Windows

1. On any Windows machine that has Python: double-click `build_exe.bat`
   (or run it from a command prompt).
2. Take `dist\PythonTutor.exe` — that's your whole program.
3. Copy it to any Windows PC (Python not needed) and double-click.
   The windowed app starts its local server and opens your browser; if
   something goes wrong, an error box explains it.

### 🐧 Linux

1. On any Linux machine that has Python 3.8+:
   `bash build_linux.sh` (it creates its own project-local venv for the
   build tool, so nothing is installed system-wide).
2. Take `dist/PythonTutor` — that's your whole program.
3. Copy it to any Linux machine (Python not needed), make it executable
   if needed (`chmod +x PythonTutor`), and run `./PythonTutor`. It starts
   its local server and opens your browser; Ctrl+C stops it.

The app uses only the Python **standard library**, so the built file is
self contained — no internet, no installers, no runtime.

### 🤖 Build BOTH versions automatically (GitHub Actions)

No Linux machine? No problem. The two versions are built **separately
on their own operating systems, in the cloud** — `PythonTutor.exe` on
Windows and `PythonTutor` on Linux — by `.github/workflows/build.yml`:

1. Put this folder in a GitHub repository (create one on github.com,
   then `git push` this project to it).
2. The workflow runs on **every push** and produces two separate
   downloadable artifacts:
   - `PythonTutor-Windows` → `PythonTutor.exe`
   - `PythonTutor-Linux` → `PythonTutor`
3. To get a ready-to-share **Release page** with both files attached,
   push a tag: `git tag v1.0 && git push origin v1.0` — the workflow
   zips the Windows exe, tars the Linux binary, and attaches both to
   the Release.
4. No push needed? You can also click **Run workflow** in the Actions
   tab to trigger a build manually.

Each build also runs `python app.py --selftest` first, so a broken
build never ships. Download the file for your OS — Windows users get
`PythonTutor.exe`, Linux users get `PythonTutor` — and run it with no
Python installed.

## Project layout

```text
python-tutor/
├── build_static.py   build-time helper: renders the whole course into static/data.js
├── app.py            dev server entry point (--selftest, --port, --no-browser)
├── server.py         tiny dev HTTP server (source mode only)
├── content.py        combines chapters, validates, injects diagrams
├── chapters_a.py     chapters 1–8  (lessons + quizzes)
├── chapters_b.py     chapters 9–16 (lessons + quizzes)
├── chapters_c.py     chapters 17–19 (the "using" section)
├── chapters_d.py     chapters 20–23 (the "library" section)
├── chapters_e.py     chapters 24–27 (the "howto" section)
├── chapters_f.py     chapters 28–31 (the "reference" tour)
├── fa_tutorial_a/b.py Persian lessons + quizzes for chapters 1–8 / 9–16
├── fa_using.py       Persian lessons + quizzes for chapters 17–19
├── fa_library.py     Persian lessons + quizzes for chapters 20–23
├── fa_howto.py       Persian lessons + quizzes for chapters 24–27
├── fa_reference.py   Persian lessons + quizzes for chapters 28–31
├── fa_tutorial.py    merges the Tutorial Persian maps into FA_CONTENT
├── checker.py        quiz answer checking + sandboxed code runner (dev)
├── diagrams.py       SVG diagram generators (the "images")
├── static/           ⬅ THE WEB APP: index.html, style.css, app.js,
│                       pyrunner.js (shared Python engine), data.js,
│                       playground.html/css/js (the 🧪 Playground window)
├── .github/          workflows: pages.yml (web deploy) + build.yml (legacy exe)
├── netlify.toml      Netlify config for Git deploys
├── build_exe.bat     legacy Windows build script → dist\PythonTutor.exe
├── build_linux.sh    legacy Linux build script  → dist/PythonTutor
├── python_tutor.spec legacy PyInstaller config
└── run.bat           dev launcher
```

## Adding your own content

Lessons and quizzes are plain Python data in `chapters_a.py` …
`chapters_f.py` (one file per documentation section). A lesson is HTML with optional `[[diag:name]]`
placeholders (see `diagrams.py` for the available names). Quiz questions
use these shapes:

```python
{"type": "mc",       "question": "...", "options": [...], "answer": 0, "explain": "..."}
{"type": "blank",    "question": "...", "answers": ["...", "..."],      "explain": "..."}
{"type": "order",    "question": "...", "lines": ["...", "..."],        "explain": "..."}
{"type": "codefill", "question": "...", "code": ["line", {"blank": "...", "answers": [...]}, ...], "explain": "..."}
```

Run `python app.py --selftest` after editing to check your content, then
`python build_static.py` to regenerate `static/data.js` for the web app.

## Notes

- In the deployed web app, the "Try it" runner executes your code with
  Pyodide (Python 3.14 → WebAssembly) inside a Web Worker with a
  10-second kill switch; the engine is fetched from jsDelivr on first
  use and cached by the browser. In dev mode (`python app.py`), it
  instead runs a sandboxed subprocess with a 5-second timeout.
- Content is distilled from the official Python 3.14 documentation,
  following the recommended order: **Tutorial → Practice → Project →
  Library → HowTo → Reference**. The tutorial chapters include
  3.14-specific details (new interactive shell, exception groups,
  `add_note()`, f-string `=`, PEP 765 `SyntaxWarning`s in `finally`);
  the "using" chapters cover the `python` command line, environment
  variables, the Windows install manager & `py` launcher, venvs on
  Windows, macOS/Unix installs, shebangs and editors.
- The library chapters are deliberately practice-oriented (per the
  docs' own advice to browse rather than read it like a novel): each
  chapter pairs two lessons with a mini-project flavoured quiz,
  spotlighting 3.14 additions like `pathlib.Path.copy()/copy_into()`,
  `Path.walk()`, and `itertools.batched()`.
- The howto chapters follow the guides' own practical tone: sorting
  with `key=`/`operator`, a gentle regex tutorial (`\d`, classes,
  quantifiers, groups), argparse `choices`/`type`, logging levels &
  file output,  `enum`, UTF-8 encode/decode, and a conceptual
  asyncio intro (`async def`, `await`, `asyncio.run`).
- The reference chapters are a tour, not a translation of the whole
  manual (which is a lookup document by design): the data model's
  identity/value/mutability rules and dunder methods, naming/binding
  and the `global`/`nonlocal`/`UnboundLocalError` rules, the operator
  precedence ladder and chained comparisons, and how `import` finds
  and caches modules — plus 3.14 details like `NotImplemented` in
  boolean contexts now raising `TypeError`.
