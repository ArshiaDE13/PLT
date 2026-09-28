"""CSS Tutor chapters 16-30 (Phases 6-9), grounded in MDN Web Docs."""

CHAPTERS_CSS_D = [
    # ------------------------------------------------------------------ cs16
    {
        "id": "cs16",
        "title": "CSS Custom Properties",
        "emoji": "🏷️",
        "lessons": [
            {
                "title": "Custom Properties & var()",
                "html": """
<p><b>Custom properties</b> — variables, in your stylesheet, native:
declare with <code>--</code>, read with <code>var()</code>:</p>

<pre class="code">:root {
  --brand: #1572b6;
  --space: 1rem;
  --radius: 10px;
}

.button {
  background: var(--brand);
  padding: 0.6em var(--space);
  border-radius: var(--radius);
}
.link { color: var(--brand); }</pre>

<p>What makes them powerful:</p>

<ul>
<li><b>They cascade and inherit</b> — <code>:root</code> defines global
tokens; any element can override locally (a card with
<code>--brand: rebeccapurple</code> re-themes everything inside
it)</li>
<li><b>They're live</b> — change at runtime from JavaScript
(<code>el.style.setProperty('--brand', 'hotpink')</code>) and the page
re-paints: the hook for themes and dark mode</li>
<li><b>Fallbacks</b> — <code>var(--accent, #33a9dc)</code> uses the
second value when the first isn't set</li>
</ul>

<pre class="code">.dark {
  --bg: #1c2a36;
  --text: #e8f1f8;
  background: var(--bg);
  color: var(--text);
}</pre>

<p>Design tokens (named, reusable decisions — colours, spaces, radii)
are built on exactly this. Custom properties + color-mix() + calc() =
a theme system in twenty lines.</p>
""",
                "tryit": """<!DOCTYPE html>
<html lang="en">
<head><title>Custom properties</title>
<style>
  :root {
    --brand: #1572b6;
    --radius: 10px;
    --space: 1rem;
  }
  body { font-family: sans-serif; }
  .card {
    border: 2px solid var(--brand);
    border-radius: var(--radius);
    padding: var(--space);
    margin: var(--space) auto;
    max-width: 300px;
  }
  .purple {
    --brand: rebeccapurple;   /* local override — cascades to children */
  }
  .button {
    background: var(--brand);
    color: white; border: none;
    padding: 8px 16px; border-radius: var(--radius);
  }
</style>
</head>
<body>
  <div class="card">
    <p>Global --brand token.</p>
    <button class="button">A button</button>
  </div>
  <div class="card purple">
    <p>Same card, local override: --brand: rebeccapurple.</p>
    <button class="button">A button</button>
  </div>
</body>
</html>
""",
            },
        ],
        "quiz": [
            {
                "type": "blank",
                "question": "Read a custom property with <code>____(--brand)</code>.",
                "answers": ["var"],
                "explain": "var(--brand) resolves the variable, with an optional fallback: var(--x, blue).",
            },
            {
                "type": "mc",
                "question": "A child sets --brand: red. What happens inside it?",
                "options": [
                    "Nothing — variables don't cascade",
                    "Every use of var(--brand) inside it resolves to red",
                    "Only backgrounds change",
                    "An error",
                ],
                "answer": 1,
                "explain": "Custom properties cascade and inherit — local overrides re-theme whole subtrees.",
            },
        ],
    },

    # ------------------------------------------------------------------ cs17
    {
        "id": "cs17",
        "title": "Modern CSS Nesting",
        "emoji": "🪆",
        "lessons": [
            {
                "title": "Native CSS Nesting",
                "html": """
<p>Preprocessors made nesting famous; CSS now has it <b>natively</b> —
rules inside rules, with <code>&amp;</code> referring to the parent:</p>

<pre class="code">.card {
  color: black;

  & .title {           /* or just .title — & is implicit */
    font-size: 2rem;
    color: var(--brand);
  }

  &amp;:hover {           /* the card itself, hovered */
    box-shadow: 0 4px 16px rgba(0,0,0,0.15);
  }

  &amp; .actions button {
    border: 1px solid #ccc;
  }
}</pre>

<p>The rules of the road:</p>

<ul>
<li><code>&amp;</code> is the parent selector — implicit at the start of a
nested selector, explicit elsewhere (<code>&amp;:hover</code>,
<code>&amp; + &amp;</code>)</li>
<li>It compiles to the same flat CSS the browser always ran — same
specificity, same cascade; nesting is <b>authoring sugar</b></li>
<li>Keep nesting shallow (2–3 levels): deeply nested selectors create
high specificity that's painful to override later</li>
</ul>

<p>The payoff is organisation — a component's styles live inside its
rule, readable and relocatable. Sass/LESS users feel at home;
everyone else gets cleaner stylesheets with zero build step.</p>
""",
                "tryit": """<!DOCTYPE html>
<html lang="en">
<head><title>Native nesting</title>
<style>
  body { font-family: sans-serif; }
  .card {
    border: 2px solid #1572b6;
    border-radius: 12px;
    padding: 14px;
    max-width: 320px;

    & h3 { color: #1572b6; margin-top: 0; }

    &:hover {
      box-shadow: 0 6px 18px rgba(21, 114, 182, 0.25);
    }

    & button {
      background: #1572b6; color: white; border: none;
      padding: 6px 14px; border-radius: 6px;
      &:hover { background: #0d4e82; }
    }
  }
</style>
</head>
<body>
  <div class="card">
    <h3>Nested rules</h3>
    <p>Hover styles, button styles — all inside .card.</p>
    <button>Hover me too</button>
  </div>
</body>
</html>
""",
            },
        ],
        "quiz": [
            {
                "type": "blank",
                "question": "Inside a nested rule, <code>____</code> refers to the parent selector.",
                "answers": ["&", "&amp;"],
                "explain": "& is the parent — required for :hover etc., implicit at the start.",
            },
            {
                "type": "mc",
                "question": "Native nesting compiles to:",
                "options": [
                    "A JavaScript bundle",
                    "The same flat CSS with the same cascade — it's authoring sugar",
                    "Shadow DOM",
                    "Media queries",
                ],
                "answer": 1,
                "explain": "Same specificity rules as flat CSS — organisation, not new semantics.",
            },
        ],
    },

    # ------------------------------------------------------------------ cs18
    {
        "id": "cs18",
        "title": "Logical Properties",
        "emoji": "↔️",
        "lessons": [
            {
                "title": "Logical Properties",
                "html": """
<p>Traditional box properties think in <b>physical</b> directions: left,
right, top, bottom. <b>Logical properties</b> think in <b>flow</b>
directions: inline (along the text) and block (across it):</p>

<pre class="code">margin-inline: 1rem;      /* left AND right in LTR */
margin-block: 1rem;       /* top AND bottom */
padding-inline: 0.75rem;
border-inline-start: 3px solid #1572b6;   /* "the start side" */
inline-size: 300px;       /* logical width */
block-size: 80px;         /* logical height */</pre>

<p>Why they matter — one word: <b>direction</b>. In an RTL (Arabic,
Persian) page, <code>margin-left</code> is still physically left — but
<code>margin-inline-start</code> flips to the <i>right</i>
automatically. A card styled with logical properties mirrors itself for
free; one styled with left/right needs a whole RTL override
sheet.</p>

<pre class="code">.callout {
  border-inline-start: 4px solid #1572b6;   /* left in LTR, right in RTL */
  padding-inline-start: 12px;
}
html[dir="rtl"] .callout { /* nothing needed! */ }</pre>

<p>Translation table: <code>width→inline-size</code>,
<code>height→block-size</code>,
<code>margin-left→margin-inline-start</code>,
<code>text-align: left→text-align: start</code>,
<code>top/bottom→inset-block-start/end</code>. This app is bilingual
(EN + Persian RTL) — and logical properties are exactly how such sites
stay sane.</p>
""",
                "tryit": """<!DOCTYPE html>
<html lang="en">
<head><title>Logical properties</title>
<style>
  body { font-family: sans-serif; }
  .callout {
    border-inline-start: 4px solid #1572b6;
    padding-inline-start: 12px;
    margin-block: 10px;
    background: #eaf4fd; padding-block: 8px;
  }
  .rtl { direction: rtl; }
</style>
</head>
<body>
  <div class="callout">LTR: the accent bar is on the inline-start
    (left) side.</div>
  <div class="callout rtl" lang="fa">RTL: همان کلاس — نوار به سمت راست
    رفت، بدون هیچ CSS اضافه‌ای!</div>
</body>
</html>
""",
            },
        ],
        "quiz": [
            {
                "type": "mc",
                "question": "In an RTL page, margin-inline-start resolves to the:",
                "options": ["Left side", "Right side", "Top", "Both sides"],
                "answer": 1,
                "explain": "inline-start follows text direction — right in RTL, left in LTR. Free mirroring.",
            },
            {
                "type": "blank",
                "question": "The logical replacement for width is <code>____-size</code>.",
                "answers": ["inline"],
                "explain": "inline-size follows the text flow direction; block-size is the other dimension.",
            },
        ],
    },

    # ------------------------------------------------------------------ cs19
    {
        "id": "cs19",
        "title": "CSS Functions",
        "emoji": "🧮",
        "lessons": [
            {
                "title": "The Functions Toolbox",
                "html": """
<p>You've met these throughout the course — this lesson lines them up as
one toolbox:</p>

<pre class="code">/* math */
width: calc(100% - 250px);        /* mix units */
font-size: clamp(1rem, 2vw, 1.5rem); /* min, preferred, max */
gap: min(4vw, 32px);              /* never larger */
padding: max(1rem, 3vh);          /* never smaller */

/* variables */
color: var(--brand, #1572b6);     /* with fallback */

/* colours */
background: color-mix(in srgb, var(--brand) 30%, white);
color: rgb(21 114 182 / 0.8);     /* space syntax + alpha */

/* attribute-driven */
content: attr(data-label);        /* pull an attribute's text into content */

/* counters (lists without &lt;ol&gt;) */
.counter { counter-increment: step; }
.counter::before { content: counter(step) ". "; }</pre>

<ul>
<li><b>calc()</b> — unit arithmetic; spaces around + and −</li>
<li><b>min()/max()/clamp()</b> — self-adapting values without media
queries</li>
<li><b>var()</b> — the token system's reader, with fallbacks</li>
<li><b>attr()</b> — surface HTML attributes in ::before/::after
content</li>
<li><b>counter()</b> — numbered anything</li>
</ul>

<p>They compose: <code>width: min(100%, calc(250px + 2rem))</code>,
<code>color: color-mix(in oklab, var(--a), var(--b))</code>. The
functions are the "programming language" layer of CSS — pure, stateless,
and recalculated live as inputs change.</p>
""",
                "tryit": """<!DOCTYPE html>
<html lang="en">
<head><title>Functions toolbox</title>
<style>
  body { font-family: sans-serif; }
  :root { --brand: #1572b6; }
  .step { counter-increment: step; list-style: none; padding: 0; }
  .step li { padding: 8px 0 8px 8px; }
  .step li::before {
    content: counter(step) ". ";
    color: var(--brand); font-weight: bold;
  }
  .tag::after { content: " [" attr(data-code) "]"; color: #888; }
  .fluid { width: min(100%, calc(300px + 2rem)); background: #eaf4fd;
           padding: 8px; border-radius: 8px; }
</style>
</head>
<body>
  <ol class="step">
    <li>counter() numbers me</li>
    <li>and me</li>
    <li>and me — no &lt;ol&gt; needed</li>
  </ol>
  <p class="tag" data-code="CS-19">attr() pulled this label's code</p>
  <div class="fluid">min(100%, calc(300px + 2rem))</div>
</body>
</html>
""",
            },
        ],
        "quiz": [
            {
                "type": "mc",
                "question": "attr(data-label) is used to:",
                "options": [
                    "Style the attribute",
                    "Read an attribute's value into generated content",
                    "Validate HTML",
                    "Replace variables",
                ],
                "answer": 1,
                "explain": "attr() surfaces attribute values in ::before/::after content.",
            },
            {
                "type": "mc",
                "question": "Which functions compose safely in one value?",
                "options": [
                    "None — use one per property",
                    "min(100%, calc(250px + 2rem))",
                    "Only in media queries",
                    "var() only",
                ],
                "answer": 1,
                "explain": "Functions nest and compose freely — that's the toolbox idea.",
            },
        ],
    },

    # ------------------------------------------------------------------ cs20
    {
        "id": "cs20",
        "title": "Transforms",
        "emoji": "🔄",
        "lessons": [
            {
                "title": "2D Transforms",
                "html": """
<p><code>transform</code> moves, scales, rotates and skews an element
<i>visually</i> — layout is untouched (neighbours never move; that's the
crucial difference from positioning):</p>

<pre class="code">.card:hover { transform: translateY(-6px); }      /* lift */
.zoom:hover { transform: scale(1.06); }           /* grow from center */
.spin    { transform: rotate(8deg); }
.skew    { transform: skewX(-6deg); }

/* compose left to right */
.stamp { transform: translate(20px, 8px) rotate(-4deg) scale(0.9); }</pre>

<ul>
<li><code>translate(x, y)</code> — slide; supports percentages of the
element's own size, and <code>translate(-50%, -50%)</code> is the
classic "center an absolute element" move</li>
<li><code>scale(x, y)</code> — enlarge/shrink; <code>scale(0.5)</code>
half size</li>
<li><code>rotate(angle)</code> — clockwise degrees</li>
<li><code>skewX/skewY</code> — slant</li>
</ul>

<p>Transforms don't trigger layout recalculation — the browser
composites them on the GPU, which is why hover lifts and load-in
animations are smooth. The transform <b>origin</b> defaults to center;
<code>transform-origin: top left</code> moves the hinge.</p>
""",
                "tryit": """<!DOCTYPE html>
<html lang="en">
<head><title>2D transforms</title>
<style>
  body { font-family: sans-serif; }
  .row { display: flex; gap: 14px; padding: 30px; }
  .box { width: 110px; height: 80px; border-radius: 10px;
         background: #1572b6; color: white;
         display: grid; place-items: center; font-weight: bold;
         transition: transform 0.3s; }
  .lift:hover  { transform: translateY(-10px); }
  .zoom:hover  { transform: scale(1.15); }
  .tilt:hover  { transform: rotate(8deg); }
  .combo:hover { transform: translate(6px, -6px) rotate(-4deg) scale(1.05);
                 background: #2e8b57; }
</style>
</head>
<body>
  <div class="row">
    <div class="box lift">lift</div>
    <div class="box zoom">zoom</div>
    <div class="box tilt">tilt</div>
    <div class="box combo">combo</div>
  </div>
  <p>Hover each — transforms don't disturb the layout.</p>
</body>
</html>
""",
            },
            {
                "title": "3D Transforms & Perspective",
                "html": """
<p>Add a <code>Z</code> axis and transforms go three-dimensional. The
key: 3D only reads as depth when an ancestor sets the
<b>perspective</b>:</p>

<pre class="code">.scene { perspective: 600px; }        /* the viewer's distance */

.flip {
  transform: rotateX(25deg);           /* tilt back */
}
.card3d { transform: rotateY(180deg); } /* turn around */</pre>

<ul>
<li><b>perspective</b> on the parent = the camera; smaller value =
stronger depth (like a wide-angle lens)</li>
<li><code>rotateX</code> (around the horizontal axis — think "tumble
back"), <code>rotateY</code> (around the vertical — "turn like a
door"), <code>rotateZ</code> = plain 2D rotate</li>
<li><code>translateZ</code> — pop toward the viewer</li>
<li><code>transform-style: preserve-3d</code> — keeps a child's 3D in
the parent's space instead of flattening it (the card-flip essential:
front and back faces plus rotateY(180deg))</li>
</ul>

<p>The famous 3D card flip is: a perspective scene, a preserve-3d
inner, two absolutely-stacked faces (one pre-rotated
<code>rotateY(180deg)</code> with <code>backface-visibility:
hidden</code>), and a hover that rotates the inner 180°. Every lesson
seed here renders in your browser — try building it in the
Playground.</p>
""",
                "tryit": """<!DOCTYPE html>
<html lang="en">
<head><title>3D transforms</title>
<style>
  body { font-family: sans-serif; }
  .scene { perspective: 600px; display: inline-block; margin: 20px; }
  .tilt {
    width: 160px; height: 110px; border-radius: 12px;
    background: linear-gradient(135deg, #1572b6, #33a9dc);
    color: white; display: grid; place-items: center; font-weight: bold;
    transform: rotateX(28deg) rotateZ(-6deg);
    transition: transform 0.4s;
  }
  .scene:hover .tilt { transform: rotateX(0deg) rotateZ(0deg) scale(1.05); }
</style>
</head>
<body>
  <div class="scene">
    <div class="tilt">rotateX(28deg) — hover to flatten</div>
  </div>
  <p>The parent's perspective turns rotation into depth.</p>
</body>
</html>
""",
            },
        ],
        "quiz": [
            {
                "type": "mc",
                "question": "transform: translateY(-6px) on hover moves the element. What happens to its neighbours?",
                "options": ["They shift up too", "Nothing — transforms don't affect layout", "They hide", "They scale"],
                "answer": 1,
                "explain": "Transforms are visual/composited — layout is untouched (unlike position changes).",
            },
            {
                "type": "blank",
                "question": "3D depth needs the parent to set <code>____</code>.",
                "answers": ["perspective"],
                "explain": "perspective is the camera distance — without it, rotateX/Y just squashes.",
            },
        ],
    },

    # ------------------------------------------------------------------ cs21
    {
        "id": "cs21",
        "title": "Transitions",
        "emoji": "🌉",
        "lessons": [
            {
                "title": "Transitions",
                "html": """
<p>A <b>transition</b> animates the change between two states — hover
lifts, menu slides, colour fades — automatically. Declare it on the
<i>resting</i> state so it plays both ways:</p>

<pre class="code">.button {
  background: #1572b6;
  transition: background 0.3s ease, transform 0.2s ease;
}
.button:hover {
  background: #0d4e82;
  transform: translateY(-2px);
}</pre>

<p>The four parts (shorthand order: property duration timing delay):</p>

<ul>
<li><b>transition-property</b> — which property to animate (or
<code>all</code> — convenient, slightly wasteful)</li>
<li><b>transition-duration</b> — seconds: 150–250ms for micro-feedback,
300–400ms for panels</li>
<li><b>transition-timing-function</b> — the pacing curve:
<code>ease</code> (default), <code>linear</code>, <code>ease-in</code>,
<code>ease-out</code>, <code>ease-in-out</code>, or custom
<code>cubic-bezier(...)</code></li>
<li><b>transition-delay</b> — wait before starting (negative values
start mid-flight!)</li>
</ul>

<p>What can transition: most numeric/colour properties — opacity,
transform, colours, shadows, sizes. What can't: <code>display</code>,
<code>height: auto</code> (use max-height or grid-template-rows tricks),
font-family. And performance wisdom: <b>transition only opacity and
transform</b> for anything that moves continuously — they're
GPU-accelerated; animating width/top forces layout on every
frame.</p>
""",
                "tryit": """<!DOCTYPE html>
<html lang="en">
<head><title>Transitions</title>
<style>
  body { font-family: sans-serif; padding: 20px; }
  .btn {
    padding: 10px 22px; border: none; border-radius: 8px;
    background: #1572b6; color: white; font-size: 1rem;
    cursor: pointer;
    transition: background 0.3s ease, transform 0.2s ease-out,
                box-shadow 0.3s ease;
  }
  .btn:hover {
    background: #0d4e82;
    transform: translateY(-3px);
    box-shadow: 0 8px 20px rgba(21, 114, 182, 0.4);
  }
  .panel {
    max-width: 260px; padding: 14px; border-radius: 8px;
    background: #eaf4fd;
    opacity: 0.4; filter: grayscale(1);
    transition: opacity 0.4s ease, filter 0.4s ease;
  }
  .panel:hover { opacity: 1; filter: none; }
</style>
</head>
<body>
  <button class="btn">Hover me — smooth lift</button>
  <p style="margin-top:18px">Hover the panel — opacity + colour
     transition together:</p>
  <div class="panel"><strong>Interactive panel</strong><br>
    transitions make interfaces feel alive.</div>
</body>
</html>
""",
            },
        ],
        "quiz": [
            {
                "type": "blank",
                "question": "The transition shorthand order is: property, duration, timing-function, ____.",
                "answers": ["delay"],
                "explain": "transition: property duration timing delay — the last two optional.",
            },
            {
                "type": "mc",
                "question": "For smooth animation at 60fps, prefer transitioning:",
                "options": ["width and top", "opacity and transform", "height: auto", "font-size"],
                "answer": 1,
                "explain": "Both are GPU-composited; width/top/height trigger layout per frame.",
            },
        ],
    },

    # ------------------------------------------------------------------ cs22
    {
        "id": "cs22",
        "title": "Animations",
        "emoji": "🎬",
        "lessons": [
            {
                "title": "@keyframes & Animation Properties",
                "html": """
<p>Transitions react to state changes; <b>animations</b> play on their
own. Define the movie with <code>@keyframes</code>, run it with
<code>animation</code>:</p>

<pre class="code">@keyframes slide-in {
  from { opacity: 0; transform: translateX(-24px); }
  to   { opacity: 1; transform: translateX(0); }
}

.toast {
  animation: slide-in 0.4s ease-out;
}

@keyframes pulse {
  0%   { transform: scale(1); }
  50%  { transform: scale(1.12); }
  100% { transform: scale(1); }
}
.badge { animation: pulse 1.6s ease-in-out infinite; }</pre>

<ul>
<li><code>from</code>/<code>to</code> are 0% / 100%; percentages stage
<i>multiple</i> steps (the pulse above)</li>
<li>the <code>animation</code> shorthand order: name duration timing
delay iteration-count direction fill-mode</li>
<li>only the properties <i>listed in the keyframes</i> animate —
everything else stays put</li>
</ul>

<p>A state change can also trigger a run: toggling a class whose
animation is defined plays it once — the pattern behind entrance
effects and shake-on-error. Combine with
<code>animation-delay</code> + a tiny per-item delay
(<code>style="animation-delay: 0.1s"</code>) for staggered entrances:
cards cascading in one after another.</p>
""",
                "tryit": """<!DOCTYPE html>
<html lang="en">
<head><title>@keyframes</title>
<style>
  body { font-family: sans-serif; padding: 16px; }
  @keyframes slide-in {
    from { opacity: 0; transform: translateX(-30px); }
    to   { opacity: 1; transform: translateX(0); }
  }
  @keyframes pulse {
    0%, 100% { transform: scale(1); }
    50%      { transform: scale(1.15); }
  }
  .toast {
    background: #1572b6; color: white; padding: 12px 18px;
    border-radius: 8px; margin: 8px 0;
    animation: slide-in 0.45s ease-out backwards;
  }
  .toast:nth-child(2) { animation-delay: 0.15s; }
  .toast:nth-child(3) { animation-delay: 0.3s; }
  .dot { display: inline-block; width: 14px; height: 14px;
         border-radius: 50%; background: #c0392b;
         animation: pulse 1.4s ease-in-out infinite; }
</style>
</head>
<body>
  <div class="toast">staggered entrance…</div>
  <div class="toast">…each with a delay…</div>
  <div class="toast">…pure CSS.</div>
  <p>Recording dot: <span class="dot"></span> (infinite pulse)</p>
</body>
</html>
""",
            },
            {
                "title": "Timing, Iteration, Direction & Fill Mode",
                "html": """
<p>The four fine-tuning knobs, and the one people always forget:</p>

<ul>
<li><b>timing-function</b> — pacing <i>within</i> each cycle:
<code>ease</code>, <code>linear</code>,
<code>ease-in-out</code>, or custom
<code>cubic-bezier(0.34, 1.56, 0.64, 1)</code> (overshoot — the bouncy
one; values above 1 overshoot the target)</li>
<li><b>iteration-count</b> — <code>3</code> or
<code>infinite</code></li>
<li><b>direction</b> — <code>normal</code>, <code>reverse</code>,
<code>alternate</code> (play forward then backward — the pendulum),
<code>alternate-reverse</code></li>
<li><b>fill-mode</b> — what the element looks like <b>before and
after</b>: <code>none</code> (snap back — default!),
<code>forwards</code> (hold the last keyframe),
<code>backwards</code> (apply the first keyframe during the delay),
<code>both</code></li>
</ul>

<p>fill-mode is the gotcha: an entrance animation with a delay and
<code>from { opacity: 0 }</code> shows the element <i>visible</i>
during the delay unless you set
<code>backwards</code> (or the shorthand
<code>animation-fill-mode: both</code>). That's why the earlier
staggered toasts said <code>backwards</code>.</p>

<pre class="code">.pendulum {
  transform-origin: top center;
  animation: swing 1.2s ease-in-out infinite alternate;
}
@keyframes swing {
  from { transform: rotate(-14deg); }
  to   { transform: rotate(14deg); }
}</pre>

<p>And always: respect <code>prefers-reduced-motion</code> (the
Accessibility chapter) — wrap decorative animation in a media query so
motion-sensitive users get a calm page.</p>
""",
                "tryit": """<!DOCTYPE html>
<html lang="en">
<head><title>Animation knobs</title>
<style>
  body { font-family: sans-serif; padding: 20px; }
  .bar { transform-origin: top center; width: 6px; height: 120px;
         background: #37475a; margin: 0 auto; border-radius: 3px;
         position: relative; }
  .bar::before {
    content: ""; position: absolute; bottom: -14px; left: 50%;
    transform: translateX(-50%);
    border: 10px solid transparent; border-top-color: #1572b6;
  }
  @keyframes swing {
    from { transform: rotate(-16deg); }
    to   { transform: rotate(16deg); }
  }
  .pendulum {
    position: absolute; top: 6px; left: 50%; margin-left: -30px;
    width: 60px; height: 60px; border-radius: 50%;
    background: #1572b6; color: white;
    display: grid; place-items: center;
    transform-origin: top center;
    animation: swing 1.1s ease-in-out infinite alternate;
  }
  .stage { height: 210px; position: relative; }
</style>
</head>
<body>
  <div class="stage">
    <div class="bar"></div>
    <div class="pendulum">alternate</div>
  </div>
  <p>ease-in-out + alternate = a believable pendulum. Try removing
     alternate!</p>
</body>
</html>
""",
            },
        ],
        "quiz": [
            {
                "type": "blank",
                "question": "The at-rule defining an animation's frames is <code>@____</code>.",
                "answers": ["keyframes", "@keyframes"],
                "explain": "@keyframes stages the property changes; animation runs them.",
            },
            {
                "type": "mc",
                "question": "animation-fill-mode: backwards is needed when:",
                "options": [
                    "The animation runs forever",
                    "There's a delay and the first keyframe differs from the resting state",
                    "You use percentages",
                    "Never",
                ],
                "answer": 1,
                "explain": "backwards applies the first keyframe during the delay — no flash of visible content.",
            },
            {
                "type": "mc",
                "question": "animation-direction: alternate does:",
                "options": [
                    "Reverses keyframe order permanently",
                    "Plays forward then backward, each cycle",
                    "Randomizes direction",
                    "Pauses between cycles",
                ],
                "answer": 1,
                "explain": "alternate is the pendulum/bounce setting.",
            },
        ],
    },

    # ------------------------------------------------------------------ cs23
    {
        "id": "cs23",
        "title": "Filters & Effects",
        "emoji": "🪄",
        "lessons": [
            {
                "title": "Filters, Opacity & Blend Modes",
                "html": """
<p><code>filter</code> applies image effects to any element — the same
sliders your photo editor has:</p>

<pre class="code">img.blurred  { filter: blur(4px); }
img.mood     { filter: grayscale(0.8) brightness(0.9) contrast(1.1); }
.glass:hover { filter: none; }        /* clear on hover */

.faded { opacity: 0.55; }

.drop { filter: drop-shadow(0 6px 8px rgba(0,0,0,0.35)); }</pre>

<ul>
<li><b>blur(px)</b>, <b>brightness()</b>, <b>contrast()</b>,
<b>saturate()</b>, <b>grayscale()</b>, <b>sepia()</b>,
<b>hue-rotate(deg)</b>, <b>invert()</b> — compose in one filter
declaration; they chain left to right</li>
<li><b>drop-shadow()</b> — like box-shadow but follows the element's
<i>actual alpha shape</i>: a transparent PNG's cloud gets a cloud-shaped
shadow, and it wraps SVG icons perfectly</li>
<li><b>opacity</b> — the whole element and its children fade together
(colour alpha fades one colour)</li>
</ul>

<p><b>Blend modes</b> mix layers like Photoshop:
<code>mix-blend-mode: multiply</code> on an element blends it with
what's behind it (multiply darkens, screen lightens, overlay boosts
contrast); <code>background-blend-mode</code> blends an element's own
background layers — the gradient-over-image looks from the Backgrounds
chapter get art-directed here.</p>
""",
                "tryit": """<!DOCTYPE html>
<html lang="en">
<head><title>Filters</title>
<style>
  body { font-family: sans-serif; }
  .row { display: flex; gap: 12px; flex-wrap: wrap; }
  figure { margin: 0; text-align: center; }
  img { width: 150px; border-radius: 10px;
        src: ""; }
  .blur  { filter: blur(2px); }
  .gray  { filter: grayscale(1); }
  .warm  { filter: sepia(0.6) saturate(1.4); }
  .shadow { filter: drop-shadow(0 8px 10px rgba(21,114,182,0.5)); }
</style>
</head>
<body>
  <div class="row">
    <figure>
      <img class="blur" src="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='150' height='100'%3E%3Crect width='150' height='100' fill='%231572b6'/%3E%3Ccircle cx='75' cy='50' r='30' fill='%23ffd43b'/%3E%3C/svg%3E" alt="blur demo">
      <figcaption>blur(2px)</figcaption>
    </figure>
    <figure>
      <img class="gray" src="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='150' height='100'%3E%3Crect width='150' height='100' fill='%231572b6'/%3E%3Ccircle cx='75' cy='50' r='30' fill='%23ffd43b'/%3E%3C/svg%3E" alt="grayscale demo">
      <figcaption>grayscale(1)</figcaption>
    </figure>
    <figure>
      <img class="warm" src="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='150' height='100'%3E%3Crect width='150' height='100' fill='%231572b6'/%3E%3Ccircle cx='75' cy='50' r='30' fill='%23ffd43b'/%3E%3C/svg%3E" alt="sepia demo">
      <figcaption>sepia+saturate</figcaption>
    </figure>
    <figure>
      <img class="shadow" src="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='150' height='100'%3E%3Crect width='150' height='100' fill='%231572b6'/%3E%3Ccircle cx='75' cy='50' r='30' fill='%23ffd43b'/%3E%3C/svg%3E" alt="drop-shadow demo">
      <figcaption>drop-shadow</figcaption>
    </figure>
  </div>
</body>
</html>
""",
            },
        ],
        "quiz": [
            {
                "type": "mc",
                "question": "drop-shadow() differs from box-shadow in that it:",
                "options": [
                    "Is faster",
                    "Follows the element's alpha shape (works on transparent PNGs/SVGs)",
                    "Only works on text",
                    "Requires borders",
                ],
                "answer": 1,
                "explain": "box-shadow outlines the box; drop-shadow traces the actual rendered shape.",
            },
            {
                "type": "mc",
                "question": "Multiple filters in one declaration:",
                "options": ["Overwrite each other", "Chain left to right", "Are invalid", "Need separate rules"],
                "answer": 1,
                "explain": "filter: grayscale(0.5) brightness(1.1) — applied in order.",
            },
        ],
    },

    # ------------------------------------------------------------------ cs24
    {
        "id": "cs24",
        "title": "Advanced Selectors",
        "emoji": "🔬",
        "lessons": [
            {
                "title": "Advanced Selectors in Practice",
                "html": """
<p>The Selectors chapter introduced :is/:where/:has/:not — this lesson
is the applied, pattern-building one. Patterns worth memorising:</p>

<pre class="code">/* 1. lighthouse list: everything except the done ones gets a marker */
li:not(.done)::before { content: "☐ "; }
li.done::before       { content: "☑ "; }

/* 2. gapless grids: spacing without outer edges */
.grid &gt; * + * { margin-top: 8px; }        /* sibling-chain spacing */

/* 3. forms: highlight the LABEL of an invalid field */
label:has(input:invalid) { color: #c0392b; }

/* 4. quantity queries — different layout at 3+ items */
ul:has(&gt; li:nth-child(3)) { columns: 2; }

/* 5. zero-specificity defaults, overridable anywhere */
:where(a) { text-decoration-color: #33a9dc; }

/* 6. compact grouping */
:is(h1, h2, h3):not(.logo) { line-height: 1.2; }</pre>

<p>Also from the toolbox: <code>:focus-visible</code> (focus rings only
for keyboard users — Accessibility chapter),
<code>:nth-child(An+B)</code> formulas (<code>3n+1</code> = 1st, 4th,
7th...), <code>:nth-last-child()</code> for "counting from the end"
quantity checks, <code>:empty</code>, <code>:default</code>,
<code>:indeterminate</code>.</p>

<p>The meta-skill: when you reach for a class to mark a state the DOM
already knows (:hover, :checked, :invalid, "contains an image"), stop —
a selector already expresses it. Fewer classes, markup that stays
clean, and CSS that documents itself.</p>
""",
                "tryit": """<!DOCTYPE html>
<html lang="en">
<head><title>Advanced selectors</title>
<style>
  body { font-family: sans-serif; }
  li::before { content: "☐ "; color: #999; }
  li.done::before { content: "☑ "; color: #2e8b57; }
  li.done { color: #999; text-decoration: line-through; }

  .grid &gt; * + * { margin-top: 8px; }
  .box { background: #eaf4fd; padding: 8px; border-radius: 6px; }

  ul:has(&gt; li:nth-child(4)) { outline: 2px solid #c73c1a;
    border-radius: 8px; padding: 8px; }
</style>
</head>
<body>
  <ul>
    <li>task one</li>
    <li class="done">task two (done)</li>
    <li>task three</li>
    <li>task four — this list has 4 items, so :has() outlined it!</li>
  </ul>

  <div class="grid">
    <div class="box">sibling-chain spacing…</div>
    <div class="box">…via .grid &gt; * + *…</div>
    <div class="box">…no margins on the first.</div>
  </div>
</body>
</html>
""",
            },
        ],
        "quiz": [
            {
                "type": "mc",
                "question": ".grid > * + * selects:",
                "options": [
                    "Only the first child",
                    "Every child that HAS a previous sibling (skips the first)",
                    "Grandchildren only",
                    "Nothing",
                ],
                "answer": 1,
                "explain": "The sibling combinator + : everything after the first — the gapless-spacing pattern.",
            },
            {
                "type": "mc",
                "question": "The meta-skill of advanced selectors:",
                "options": [
                    "Add classes for every state",
                    "Express DOM-known states with selectors instead of extra classes",
                    "Never use classes",
                    "Use only IDs",
                ],
                "answer": 1,
                "explain": ":checked/:invalid/:has() already know the state — fewer hooks, cleaner markup.",
            },
        ],
    },

    # ------------------------------------------------------------------ cs25
    {
        "id": "cs25",
        "title": "Cascade Layers",
        "emoji": "🥞",
        "lessons": [
            {
                "title": "@layer in Depth",
                "html": """
<p>From the Cascade chapter: <code>@layer</code> orders your stylesheet
into explicit tiers whose order beats specificity. Here's the
professional architecture in full:</p>

<pre class="code">@layer reset, base, layout, components, utilities, overrides;

@layer reset {
  *, *::before, *::after { box-sizing: border-box; }
  body { margin: 0; }
}
@layer base {
  body { font-family: sans-serif; color: #263238; }
  a { color: #1572b6; }
}
@layer components {
  .card { border-radius: 10px; padding: 14px; }
}
@layer utilities {
  .text-center { text-align: center; }
  .mt-2 { margin-top: 0.5rem; }
}</pre>

<p>The semantics:</p>

<ul>
<li>later layers <b>always beat</b> earlier layers — one class in
<code>utilities</code> overrides a three-ID selector in
<code>base</code>. Specificity still ranks <i>within</i> a layer</li>
<li><b>unlayered styles beat all layers</b> — one-off page fixes slot
in above the system</li>
<li>repeat layer names to append: <code>@layer base { ... }</code> adds
to base wherever it appears</li>
<li><code>@layer base, components;</code> up front fixes the order even
when the blocks appear in other files</li>
</ul>

<p>This is how design systems stop fighting themselves: resets can't
accidentally beat components, utilities always win, and third-party
styles get their own sealed layer
(<code>@layer vendor;</code> before importing). Compared to the
!important arms race, layers are peace treaties with an enforcement
mechanism.</p>
""",
                "tryit": """<!DOCTYPE html>
<html lang="en">
<head><title>@layer</title>
<style>
  @layer base, utilities;

  @layer base {
    .box { color: #1572b6 !important; /* even !important loses across layers */ }
  }
  @layer utilities {
    .red { color: #c0392b; }
  }
</style>
</head>
<body>
  <p class="box red">utilities beat base — and beat base's !important too
     (layer order outranks specificity).</p>
  <p class="box">Without .red: the base layer paints me blue.</p>
</body>
</html>
""",
            },
        ],
        "quiz": [
            {
                "type": "mc",
                "question": "Across cascade layers, the winner is decided by:",
                "options": ["Specificity only", "Layer order — regardless of specificity", "File size", "Source order of properties"],
                "answer": 1,
                "explain": "Layer order outranks specificity — even !important in an earlier layer loses to a later layer.",
            },
            {
                "type": "blank",
                "question": "Styles outside any layer beat styles ____ layers.",
                "answers": ["inside", "in", "within"],
                "explain": "Unlayered wins — a deliberate escape hatch for one-off fixes.",
            },
        ],
    },

    # ------------------------------------------------------------------ cs26
    {
        "id": "cs26",
        "title": "Advanced Layout",
        "emoji": "🚀",
        "lessons": [
            {
                "title": "Subgrid & Advanced Grid",
                "html": """
<p><b>Subgrid</b> fixes grid's last annoyance: a nested grid's rows
don't line up with its parent's. With
<code>grid-template-rows: subgrid</code>, the child inherits the
parent's tracks — every card in a row shares the same row heights:</p>

<pre class="code">.cards {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 14px;
}
.card {
  display: grid;
  grid-row: span 3;
  grid-template-rows: subgrid;   /* use the PARENT's rows */
}
/* all three cards' titles/prices/buttons align across cards */</pre>

<p>Before subgrid, card rows misaligned whenever one title wrapped to
two lines; now the parent's rows pace every card. It also works for
columns — form labels aligned across nested sections.</p>

<p>Other advanced grid moves from MDN's guides:</p>

<ul>
<li><b>named lines</b> — <code>grid-template-columns: [main-start] 1fr
[aside-start] 300px [main-end]</code> — placement by name, resilient to
track changes</li>
<li><b>grid-auto-flow: dense</b> — backfill holes left by spanning
items (masonry-ish)</li>
<li><b>item spanning + auto-placement</b> — mixed explicit/auto layouts:
one hero spanning 2×2 inside an auto-flowing grid</li>
</ul>
""",
                "tryit": """<!DOCTYPE html>
<html lang="en">
<head><title>Subgrid</title>
<style>
  body { font-family: sans-serif; }
  .cards { display: grid; grid-template-columns: repeat(3, 1fr);
           gap: 12px; }
  .card {
    display: grid;
    grid-row: span 3;
    grid-template-rows: subgrid;
    gap: 6px;
    border: 2px solid #33a9dc; border-radius: 10px; padding: 10px;
  }
  .card h4 { margin: 0; color: #1572b6; }
  .card p { margin: 0; }
  .card button { align-self: end; border: none; background: #1572b6;
                 color: white; padding: 6px; border-radius: 6px; }
</style>
</head>
<body>
  <div class="cards">
    <div class="card">
      <h4>Short title</h4>
      <p>Body.</p>
      <button>Buy</button>
    </div>
    <div class="card">
      <h4>A much longer title that wraps to two lines</h4>
      <p>Body — but note the buttons below still align!</p>
      <button>Buy</button>
    </div>
    <div class="card">
      <h4>Third</h4>
      <p>Subgrid paces all three cards from the parent's rows.</p>
      <button>Buy</button>
    </div>
  </div>
</body>
</html>
""",
            },
            {
                "title": "Anchor Positioning & Scroll-driven Animations",
                "html": """
<p>Two of the newest platform powers — both turn "impossible without
JavaScript" into a few lines.</p>

<p><b>Anchor positioning</b> — attach a floating element (tooltip,
popover, menu) to an anchor element, and the browser keeps it glued,
flipping to stay on-screen:</p>

<pre class="code">.info-btn { anchor-name: --info; }

.tooltip {
  position: absolute;
  position-anchor: --info;
  position-area: top;          /* above the anchor */
  position-try-fallbacks: flip-block;  /* flip if no room */
}</pre>

<p>For years every tooltip library was 300 lines of measuring code;
anchor positioning makes placement declarative. It pairs beautifully
with the native <code>&lt;dialog&gt;</code> and the Popover API
(HTML Advanced chapter).</p>

<p><b>Scroll-driven animations</b> — animations whose progress follows
the scroll, no scroll listeners:</p>

<pre class="code">.reading-bar {
  position: fixed; top: 0; left: 0; height: 4px;
  background: #1572b6;
  transform-origin: left;
  animation: grow linear;
  animation-timeline: scroll(root);   /* progress = page scroll */
}
@keyframes grow { from { transform: scaleX(0); } to { transform: scaleX(1); } }

.reveal {
  animation: fade-up linear both;
  animation-timeline: view();         /* progress = element in view */
}</pre>

<p><code>scroll()</code> ties to page scroll, <code>view()</code> to the
element's own journey through the viewport — reveal-on-scroll and
reading-progress bars become pure CSS. Both features are rolling out
across browsers; check <code>@supports</code> (Compatibility chapter)
and let the page simply work without them elsewhere.</p>
""",
                "tryit": """<!DOCTYPE html>
<html lang="en">
<head><title>Scroll-driven</title>
<style>
  body { font-family: sans-serif; margin: 0; }
  .bar {
    position: fixed; top: 0; left: 0; height: 5px; width: 100%;
    background: #1572b6; transform-origin: left;
    animation: grow linear both;
    animation-timeline: scroll(root);
  }
  @keyframes grow { from { transform: scaleX(0); } to { transform: scaleX(1); } }
  section { min-height: 60vh; padding: 20px; }
</style>
</head>
<body>
  <div class="bar"></div>
  <section><h2>Scroll down!</h2><p>The reading bar's width IS your
    scroll position — no JavaScript.</p></section>
  <section><p>Reveal-on-scroll, progress rings, parallax —
    all animation-timeline.</p></section>
  <section><p>More filler to scroll…</p></section>
  <section><p>Almost there…</p></section>
  <section><p>The end.</p></section>
</body>
</html>
""",
            },
        ],
        "quiz": [
            {
                "type": "mc",
                "question": "subgrid lets a nested grid:",
                "options": [
                    "Run faster",
                    "Use its parent's tracks so rows/columns align across siblings",
                    "Ignore gaps",
                    "Float",
                ],
                "answer": 1,
                "explain": "grid-template-rows: subgrid inherits the parent's pacing — aligned cards at last.",
            },
            {
                "type": "blank",
                "question": "Scroll-driven animations use <code>animation-____: scroll(root)</code>.",
                "answers": ["timeline"],
                "explain": "animation-timeline replaces time with scroll/view progress.",
            },
        ],
    },

    # ------------------------------------------------------------------ cs27
    {
        "id": "cs27",
        "title": "Accessibility",
        "emoji": "♿",
        "lessons": [
            {
                "title": "Focus, :focus-visible & Accessible States",
                "html": """
<p>CSS's accessibility duties start with the <b>focus ring</b>. Removing
<code>outline</code> without a replacement strands keyboard users —
they literally cannot see where they are. Modern CSS makes the ring
precise:</p>

<pre class="code">/* mouse clicks: no ring. Keyboard Tab: clear ring. */
:focus-visible {
  outline: 3px solid #ffd43b;
  outline-offset: 2px;
}
:focus:not(:focus-visible) { outline: none; }</pre>

<p><code>:focus-visible</code> fires only when the browser thinks the
user needs it (keyboard navigation) — the best of both worlds. Pair it
with <code>:focus-within</code> (highlight a whole form row when its
input is focused) and consider <code>scroll-margin-top</code> on
targets so keyboard jumps don't hide content under sticky
headers.</p>

<p>States to honour in CSS:</p>

<ul>
<li><code>:hover</code> — never hide information behind it alone (touch
has no hover)</li>
<li><code>:disabled</code> — dim but keep contrast readable; explain
<i>why</i> in text</li>
<li><code>:invalid</code> / <code>:user-invalid</code> — the latter only
after the user touched the field (kinder validation styling)</li>
<li>colour alone never carries meaning — pair red errors with icons or
text</li>
</ul>
""",
                "tryit": """<!DOCTYPE html>
<html lang="en">
<head><title>Focus states</title>
<style>
  body { font-family: sans-serif; padding: 16px; }
  button, input { font: inherit; padding: 8px 14px; }
  button:focus-visible, input:focus-visible {
    outline: 3px solid #ffd43b; outline-offset: 2px;
  }
  button:focus:not(:focus-visible) { outline: none; }
  .row:has(input:focus-visible) { background: #fff8e1; }
  .row { padding: 8px; border-radius: 8px; }
</style>
</head>
<body>
  <p>Click the button with the mouse (no ring), then Tab to it (ring
     appears) — :focus-visible in action.</p>
  <button>Tab target</button>
  <div class="row">
    <label>Highlight-the-row input: <input placeholder="Tab here"></label>
  </div>
</body>
</html>
""",
            },
            {
                "title": "Reduced Motion, Contrast & Forced Colors",
                "html": """
<p>CSS can sense and honour user needs through media queries:</p>

<pre class="code">/* vestibular disorders: no decorative motion */
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}

/* system-wide dark preference */
@media (prefers-color-scheme: dark) {
  :root { --bg: #1c2a36; --text: #e8f1f8; }
}

/* forced colours mode (high-contrast OS themes) */
@media (forced-colors: active) {
  .button { border: 1px solid ButtonText; }
}</pre>

<ul>
<li><b>prefers-reduced-motion</b> — the snippet above is the standard
mercy rule: parallax, auto-carousels and bounces become still; the
pattern this very app ships (check its stylesheet!)</li>
<li><b>contrast</b> — WCAG asks 4.5:1 for body text; test
<code>color-mix()</code>-generated tints before shipping them; never
convey state by colour alone</li>
<li><b>forced-colors</b> — high-contrast themes override your palette;
keep borders and outlines (they become the visible structure) and avoid
baking colours into essential meaning</li>
</ul>

<p>Accessibility in CSS is mostly restraint: the platform's defaults
are good — don't remove outlines, don't disable zoom, don't move things
without permission.</p>
""",
                "tryit": """<!DOCTYPE html>
<html lang="en">
<head><title>Reduced motion</title>
<style>
  body { font-family: sans-serif; padding: 20px; }
  @keyframes wiggle {
    from { transform: rotate(-4deg); } to { transform: rotate(4deg); }
  }
  .ad {
    display: inline-block; font-size: 1.4rem;
    animation: wiggle 0.3s ease-in-out infinite alternate;
  }
  @media (prefers-reduced-motion: reduce) {
    .ad { animation: none; }
  }
</style>
</head>
<body>
  <p>The badge wiggles — unless your OS asks for reduced motion
     (try toggling it in your system settings, then reload):</p>
  <p><span class="ad">🎉 wiggle wiggle</span></p>
  <p>This course's own stylesheet ships exactly this mercy rule —
     check the source!</p>
</body>
</html>
""",
            },
        ],
        "quiz": [
            {
                "type": "blank",
                "question": "Focus rings for KEYBOARD users only come from <code>:focus-____</code>.",
                "answers": ["visible"],
                "explain": ":focus-visible fires for keyboard navigation; mouse clicks stay clean.",
            },
            {
                "type": "mc",
                "question": "prefers-reduced-motion: reduce should make your page:",
                "options": [
                    "Unusable",
                    "Calm — decorative animation and transitions become still",
                    "Faster",
                    "Dark",
                ],
                "answer": 1,
                "explain": "Motion-sensitive users (vestibular disorders) need stillness; keep the content, drop the movement.",
            },
        ],
    },

    # ------------------------------------------------------------------ cs28
    {
        "id": "cs28",
        "title": "CSS Architecture",
        "emoji": "🏛️",
        "lessons": [
            {
                "title": "Naming Conventions & BEM",
                "html": """
<p>Stylesheets rot when names lie. Conventions exist to keep intent
readable. The most famous: <b>BEM</b> — Block, Element, Modifier:</p>

<pre class="code">.card { }                    Block: the component
.card__title { }             Element: a part of it (double underscore)
.card__button { }
.card--featured { }          Modifier: a variant (double dash)
.card--compact { }</pre>

<ul>
<li>Every selector is one flat class — <b>zero specificity wars</b>,
everything overridable by order</li>
<li>The name tells you the anatomy: <code>.card__title</code> obviously
belongs to the card, can never leak into <code>.modal__title</code>'s
business</li>
<li>Modifiers compose:
<code>class="card card--featured"</code></li>
</ul>

<p>Alternatives have different trade-offs: <b>SMACSS</b> categorises
rules (base/layout/module/state/theme), <b>ITCSS</b> orders layers by
specificity (the pre-@layer ancestor — cascade layers now do this
natively), and modern component frameworks sidestep naming entirely by
scoping styles to components. BEM remains the lingua franca — even if
you don't use it, you must be able to read it.</p>
""",
                "tryit": """<!DOCTYPE html>
<html lang="en">
<head><title>BEM</title>
<style>
  .card { border: 2px solid #1572b6; border-radius: 10px;
          padding: 14px; max-width: 300px; }
  .card__title { margin: 0 0 8px; color: #1572b6; }
  .card__body { color: #445; }
  .card__button { background: #1572b6; color: white;
                  border: none; padding: 6px 16px; border-radius: 6px; }
  .card--featured { border-width: 4px; background: #f2f8fe; }
</style>
</head>
<body>
  <div class="card">
    <h3 class="card__title">.card</h3>
    <p class="card__body">Flat class selectors — no nesting wars.</p>
    <button class="card__button">.card__button</button>
  </div>
  <div class="card card--featured">
    <h3 class="card__title">.card--featured</h3>
    <p class="card__body">The modifier adds the tint and thicker border.</p>
    <button class="card__button">.card__button</button>
  </div>
</body>
</html>
""",
            },
            {
                "title": "Utility CSS & Design Tokens",
                "html": """
<p>Two opposite philosophies, both mainstream:</p>

<p><b>Semantic/components-first</b> (BEM world): styles describe
meaning — <code>.card</code>, <code>.button--danger</code>. Change the
HTML rarely; change the CSS freely.</p>

<p><b>Utility-first</b> (the Tailwind model): tiny single-purpose
classes composed in markup:</p>

<pre class="code">&lt;div class="flex gap-3 rounded-lg p-4 bg-blue-50"&gt;...&lt;/div&gt;

/* the utilities behind it */
.flex { display: flex; }
.gap-3 { gap: 0.75rem; }
.rounded-lg { border-radius: 8px; }
.p-4 { padding: 1rem; }
.bg-blue-50 { background: #eff6ff; }</pre>

<ul>
<li>No naming bikeshed, no dead CSS, visually consistent by
construction — at the cost of classes in markup</li>
<li>Design <b>tokens</b> are the shared foundation either way: named
decisions (<code>--space-2: 0.5rem</code>,
<code>--color-brand</code>) that both approaches consume. Utilities
generated FROM tokens scale without drifting</li>
</ul>

<p>Most mature systems are hybrids: token-driven custom properties,
semantic component classes for the big pieces, a thin utility layer for
spacing/alignment one-offs — with cascade layers enforcing the
pecking order.</p>
""",
                "tryit": """<!DOCTYPE html>
<html lang="en">
<head><title>Tokens + utilities</title>
<style>
  :root {
    --space-2: 0.5rem; --space-4: 1rem;
    --color-brand: #1572b6;
    --radius-md: 10px;
  }
  /* utility layer */
  .flex { display: flex; gap: var(--space-2); }
  .p-4 { padding: var(--space-4); }
  .rounded { border-radius: var(--radius-md); }
  .bg-brand-10 { background: color-mix(in srgb, var(--color-brand) 10%, white); }
  .text-brand { color: var(--color-brand); }
</style>
</head>
<body>
  <div class="flex p-4 rounded bg-brand-10">
    <strong class="text-brand">Tokens +</strong>
    <span>utilities = a tiny design system in 12 lines.</span>
  </div>
  <p>Change --color-brand once — every utility follows.</p>
</body>
</html>
""",
            },
            {
                "title": "Organizing Stylesheets",
                "html": """
<p>A stylesheet is a codebase. The structural playbook:</p>

<ul>
<li><b>One purpose per file</b>: <code>reset.css</code>,
<code>tokens.css</code>, <code>base.css</code>,
<code>layout.css</code>, <code>components/*.css</code>,
<code>utilities.css</code> — imported in that order (or, better,
declared as cascade <b>layers</b> in that order)</li>
<li><b>Source order is design</b>: resets first, tokens early (they're
just definitions), base next, components, utilities last so they always
win</li>
<li><b>Component colocated styles</b> — keep a component's styles next
to its markup/component file; findability beats elegance</li>
<li><b>Comment the why</b>: "z-index: 40 — above sticky header (30)"
saves the next person an hour</li>
<li><b>Lint and prune</b>: dead selectors accumulate like dust; audits
are spring cleaning</li>
</ul>

<pre class="code">/* styles.css — the index */
@layer reset, tokens, base, layout, components, utilities;

@import "./reset.css" layer(reset);
@import "./tokens.css" layer(tokens);
@import "./base.css" layer(base);
@import "./components.css" layer(components);
@import "./utilities.css" layer(utilities);</pre>

<p>The cascade chapter's tools (layers, tokens, low-specificity
selectors) are exactly the mechanisms that make this structure
enforceable rather than aspirational. Architecture = deciding, up
front, where things go — so the answer never has to be
"anywhere".</p>
""",
            },
        ],
        "quiz": [
            {
                "type": "mc",
                "question": "In BEM, .card__title is:",
                "options": ["A modifier", "An element of the card block", "A utility", "An ID"],
                "answer": 1,
                "explain": "__ marks elements (parts of the block); -- marks modifiers.",
            },
            {
                "type": "mc",
                "question": "Design tokens are:",
                "options": [
                    "Fonts you bought",
                    "Named, reusable design decisions consumed via custom properties",
                    "HTML comments",
                    "Validators",
                ],
                "answer": 1,
                "explain": "--color-brand, --space-2... one source of truth for the whole system.",
            },
            {
                "type": "mc",
                "question": "In a layered architecture, utilities load LAST because:",
                "options": [
                    "They're small",
                    "Later layers win — utilities must always override components",
                    "Browsers require it",
                    "It loads faster",
                ],
                "answer": 1,
                "explain": "Layer order beats specificity: last layer = guaranteed winner.",
            },
        ],
    },

    # ------------------------------------------------------------------ cs29
    {
        "id": "cs29",
        "title": "Performance",
        "emoji": "⚡",
        "lessons": [
            {
                "title": "CSS Performance",
                "html": """
<p>CSS rarely tops a performance audit, but it has three costs worth
knowing: <b>download</b>, <b>parsing/matching</b>, and <b>rendering</b>.</p>

<p><b>Download:</b> stylesheets block first render — the browser waits
for CSS before painting (unstyled content is worse than late content).
So: ship it early (<code>&lt;link&gt;</code> in the head), keep it
compressed (gzip/brotli), split only when genuinely per-route, and
<code>font-display: swap</code> so web fonts don't hold text
hostage.</p>

<p><b>Matching:</b> the browser matches selectors right-to-left and does
it <i>fast</i> — modern engines make the old "avoid descendant
selectors!" advice mostly obsolete. The real costs today: enormous
stylesheets nobody prunes (every rule is matched against every DOM
change), and universal shenanigans. Write natural selectors; spend the
effort on deleting dead CSS.</p>

<p><b>Rendering</b> — the pipeline: style → layout → paint → composite.
Performance gold is animating only the last stage:</p>

<ul>
<li><b>opacity &amp; transform</b> — composite-only: the GPU moves the
already-painted pixels. 60fps for free</li>
<li><b>width/height/top/left/margin/font-size</b> — trigger
<b>layout</b> (reflow): the browser recalculates geometry for possibly
the whole page, then repaints. Animate these only on small, contained
areas</li>
<li>big filters/shadows on huge areas are paint-heavy — prefer
pre-baked images or contain the effect</li>
</ul>

<pre class="code">.reveal { will-change: transform; }  /* hint: promote to its own layer */
/* but add sparingly — every hint costs memory */</pre>

<p>The golden rule from MDN: measure first (devtools Performance panel),
then optimise what the numbers say — not what folklore says.</p>
""",
                "tryit": """<!DOCTYPE html>
<html lang="en">
<head><title>Layout vs composite</title>
<style>
  body { font-family: sans-serif; }
  .demo { padding: 16px; }
  .box { width: 90px; height: 90px; background: #1572b6; color: white;
         display: grid; place-items: center; border-radius: 10px;
         transition: all 2s linear; }
  .layout-anim:hover .box { width: 300px; }        /* layout every frame */
  .composite-anim:hover .box { transform: scaleX(3.3); } /* composite only */
</style>
</head>
<body>
  <div class="demo layout-anim">
    <div class="box">hover: width (layout)</div>
  </div>
  <div class="demo composite-anim">
    <div class="box">hover: scaleX (composite)</div>
  </div>
  <p>Both look the same — but the first re-flows the page every frame.
     On a busy page, you'd feel the difference.</p>
</body>
</html>
""",
            },
        ],
        "quiz": [
            {
                "type": "mc",
                "question": "The GPU-friendly properties to animate are:",
                "options": ["width & height", "opacity & transform", "margin & padding", "font-size"],
                "answer": 1,
                "explain": "They composite without layout/paint — the 60fps pair.",
            },
            {
                "type": "mc",
                "question": "Why does CSS block first render?",
                "options": [
                    "It's a bug",
                    "The browser avoids flashing unstyled content — CSS defines how anything looks",
                    "Fonts are heavy",
                    "JavaScript requires it",
                ],
                "answer": 1,
                "explain": "Painting before CSS means a jarring re-paint; hence render-blocking, hence ship CSS early.",
            },
        ],
    },

    # ------------------------------------------------------------------ cs30
    {
        "id": "cs30",
        "title": "Browser Compatibility",
        "emoji": "🌍",
        "lessons": [
            {
                "title": "Feature Detection & Progressive Enhancement",
                "html": """
<p>Browsers differ. The professional response is never "target one
browser" — it's <b>progressive enhancement</b>: build a solid baseline
every browser understands, then layer upgrades where supported.</p>

<p><b>@supports</b> — CSS's own feature detector:</p>

<pre class="code">.gallery { display: flex; gap: 8px; }        /* baseline: works everywhere */

@supports (display: grid) {
  .gallery { display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); }
}

@supports not (container-type: inline-size) {
  .card { /* a media-query fallback instead */ }
}</pre>

<p>The pattern: declare the fallback <i>first</i>, then the enhancement
inside @supports — browsers that don't understand the condition skip
the block entirely, and cascade order means the newer rule wins where
available. No JavaScript, no user-agent sniffing (that's the
anti-pattern).</p>

<p><b>Values with fallbacks</b> work at the declaration level — the
cascade's silent feature detector:</p>

<pre class="code">.card {
  background: #1572b6;                                /* fallback */
  background: color-mix(in srgb, #1572b6 80%, white); /* modern */
  width: max(300px, 50vw);                            /* unknown = ignored */
}</pre>

<p>An unsupported declaration is simply skipped; the previous one
survives. Write fallback-then-enhancement in that order and old
browsers get the old look, new browsers the new one — same
stylesheet.</p>
""",
                "tryit": """<!DOCTYPE html>
<html lang="en">
<head><title>@supports</title>
<style>
  body { font-family: sans-serif; }
  .card { padding: 12px; background: #eaf4fd; border-radius: 8px; }

  /* fallback first: a plain border */
  .badge { border: 3px solid #1572b6; }

  /* enhancement where supported */
  @supports (border: 1px solid color-mix(in srgb, red, blue)) {
    .badge { border-color: color-mix(in srgb, #1572b6, #ffd43b); }
  }
</style>
</head>
<body>
  <div class="card">
    <span class="badge">support-aware badge</span>
    <p>Modern browsers show a mixed-colour border; older ones the
       plain blue — same stylesheet, graceful both ways.</p>
  </div>
</body>
</html>
""",
            },
            {
                "title": "Browser Support & Baseline",
                "html": """
<p>How do you know what's safe to use? The ecosystem's answer is
<b>Baseline</b> — MDN/caniuse's shared label for web platform
features:</p>

<ul>
<li><b>Baseline: Newly available</b> — works across all the major
browsers' current versions; safe with a fallback mindset</li>
<li><b>Baseline: Widely available</b> — has worked across browsers for
30+ months; safe everywhere, old browsers included</li>
<li><b>Limited availability</b> — not yet in every engine; use with
@supports and a fallback</li>
</ul>

<p>Every MDN property page shows its Baseline status with browser
badges — it's the first thing to check before adopting a shiny feature
(look up <code>:has()</code> or container queries: both are Baseline
now; subgrid and anchor positioning are newer).</p>

<p>The working policy:</p>

<ul>
<li>know your <b>audience</b> (analytics), not a mythical "everyone uses
Chrome latest"</li>
<li><b>evergreen browsers</b> update themselves — the long tail is old
enterprise builds and old phones; feature-detect for them</li>
<li><b>testing</b>: the devtools of one browser can render/emulate
another's quirks, but at minimum test the newest Chrome, Firefox and
Safari before shipping a layout technique</li>
</ul>

<p>That's the whole journey, from "what is a rule" to cascade layers
and scroll-driven animation. CSS rewards exactly one habit: build the
baseline, layer the enhancements, and let every browser give its
best.</p>
""",
            },
        ],
        "quiz": [
            {
                "type": "mc",
                "question": "The @supports pattern for graceful enhancement:",
                "options": [
                    "Enhancement first, fallback after",
                    "Fallback first, then the enhancement inside @supports",
                    "Only use @supports",
                    "Detect browsers by user-agent",
                ],
                "answer": 1,
                "explain": "Cascade order: unsupported browsers keep the fallback; modern ones take the upgrade.",
            },
            {
                "type": "mc",
                "question": "Baseline 'Widely available' means:",
                "options": [
                    "Only Chrome supports it",
                    "It has worked across all major browsers for 30+ months",
                    "It is experimental",
                    "It needs JavaScript",
                ],
                "answer": 1,
                "explain": "Baseline labels tell you the safe-to-use status at a glance — right on each MDN page.",
            },
        ],
    },
]
