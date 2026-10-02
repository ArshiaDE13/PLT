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
<p>Every design system repeats the same colour in forty places — and
the old CSS way meant find-and-replace when the brand changed.
<b>Custom properties</b> — variables, in your stylesheet, native — fix
that: declare with <code>--</code>, read with <code>var()</code>:</p>

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

<p>Walk it: <code>:root</code> — the html element — holds the tokens,
so everything inherits them. The button reads three of them for its
background, spacing and corners; the link reads the brand colour.
Change <code>--brand</code> once and both repaint. Names are
case-sensitive, and the values can be anything — colours, lengths,
whole shadows, numbers you feed into calc(). Three capabilities make
them more powerful than any preprocessor variable:</p>

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

<p>The second block is the theme pattern in miniature: a class (or
<code>[data-theme="dark"]</code>) redefines the same token names
locally, and every descendant reading <code>var(--bg)</code> switches —
no component styles duplicated, only the values change. Design tokens
(named, reusable decisions — colours, spaces, radii) are built on
exactly this. Custom properties + color-mix() + calc() = a theme system
in twenty lines. Predict the Try-it: two identical cards, the second
redefining <code>--brand: rebeccapurple</code> locally — its border and
button repaint purple while the first stays blue. Gotcha: an invalid
value inside var() can't be rejected at parse time; at computed-value
time the property falls back to <i>inherit or initial</i>, which can
silently unset a colour — give important tokens sane var() fallbacks.</p>
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
<p>Preprocessors made nesting famous — one component, one block, its
states and children indented inside. CSS now has it <b>natively</b>, in
every modern browser: rules inside rules, with <code>&amp;</code>
referring to the parent:</p>

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

<p>Walk it: the outer rule styles the card itself (black text). Nested
inside, <code>&amp; .title</code> targets a child — the leading
<code>&amp;</code> is implied, so writing bare <code>.title</code> is
identical here. <code>&amp;:hover</code> is different: there
<code>&amp;</code> is <i>required</i>, gluing :hover onto the card
itself — omit it and you'd get <code>.card :hover</code>, which styles
whatever is hovered <i>inside</i> the card. The last rule nests two
levels: a button inside .actions inside .card. The rules of the
road:</p>

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
rule, readable and relocatable; delete the card block and every style
for it goes at once. Sass/LESS users feel at home; everyone else gets
cleaner stylesheets with zero build step. Predict the Try-it: hover the
card — its shadow lifts via the nested <code>&amp;:hover</code>; hover
the button — its own nested rule darkens it. Gotcha: nesting is not
scoping — nested selectors still match globally, so a component
rendered inside another one with the same class names will pick up the
outer rules; keep class names component-unique and nesting shallow
instead of trusting indentation to isolate anything.</p>
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
<p>Traditional box properties think in <b>physical</b> directions:
left, right, top, bottom — nailed to the screen. <b>Logical
properties</b> think in <b>flow</b> directions: inline (along the text)
and block (across it) — tied to how the content actually reads. One
mental flip, and bilingual pages get vastly simpler:</p>

<pre class="code">margin-inline: 1rem;      /* left AND right in LTR */
margin-block: 1rem;       /* top AND bottom */
padding-inline: 0.75rem;
border-inline-start: 3px solid #1572b6;   /* "the start side" */
inline-size: 300px;       /* logical width */
block-size: 80px;         /* logical height */</pre>

<p>Walk it: <code>margin-inline</code> is the two-sided shorthand —
both text-direction sides at once, <code>margin-left</code> +
<code>margin-right</code> without caring which is which.
<code>border-inline-start</code> is the accent-bar property: "the side
text starts on". <code>inline-size</code> is width in a horizontal
script, but the concept follows the flow, not the screen. Why they
matter — one word: <b>direction</b>. In an RTL (Arabic, Persian) page,
<code>margin-left</code> is still physically left — but
<code>margin-inline-start</code> flips to the <i>right</i>
automatically. A card styled with logical properties mirrors itself for
free; one styled with left/right needs a whole RTL override
sheet.</p>

<pre class="code">.callout {
  border-inline-start: 4px solid #1572b6;   /* left in LTR, right in RTL */
  padding-inline-start: 12px;
}
html[dir="rtl"] .callout { /* nothing needed! */ }</pre>

<p>The second block is the payoff: the callout gets its accent bar and
breathing room, and the RTL override rule is empty — there is nothing
to override. The <code>dir="rtl"</code> attribute does all the work;
the logical properties simply follow the text direction wherever it
points.</p>

<p>Translation table: <code>width→inline-size</code>,
<code>height→block-size</code>,
<code>margin-left→margin-inline-start</code>,
<code>text-align: left→text-align: start</code>,
<code>top/bottom→inset-block-start/end</code>. This app is bilingual
(EN + Persian RTL) — and logical properties are exactly how such sites
stay sane. Predict the Try-it: both callouts share one class; the
accent bar sits on the left in the English one and on the right in the
Persian one, same CSS. Gotcha: mixing physical and logical properties
on the same element invites order-dependent surprises — later
declarations win whichever vocabulary they use — so pick logical on
anything that might ever be mirrored, and stay consistent.</p>
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
<p>You've met these functions scattered across the course, each solving
one problem. This lesson lines them up as one toolbox — because their
shared superpower is the point: every function is recalculated live,
composes with the others, and turns CSS from static declarations into a
calculation language:</p>

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

<p>Walk it family by family. The math family mixes units and bounds
values: calc() for arithmetic (spaces around + and −!), clamp() for a
fluid value with hard floors and ceilings, min()/max() for one-sided
guards. The variables family reads design tokens, with an inline
fallback for safety. The colour family builds tints with color-mix()
and writes colours with alpha in the modern space-separated syntax.
Then two specials: attr() surfaces an HTML attribute's text inside
generated content — the tag above can print its own data-label without
JavaScript — and counter() numbers anything you increment, the engine
behind ordered lists you build yourself:</p>

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
<code>color: color-mix(in oklab, var(--a), var(--b))</code> — functions
nest freely, each returning a value the outer one consumes. The
functions are the "programming language" layer of CSS — pure,
stateless, and recalculated live as inputs change (a resize, a theme
flip, a changed custom property).</p>

<p>Predict the Try-it: a self-numbered list built from counter(), a tag
whose bracketed code comes from attr(), and a fluid box bounded by
min() and calc() together. Gotcha: attr() reads raw strings — the
extended form with types (attr(data-n number)) is still sparse in
browser support, and a missing attribute inside content: yields the
empty string, not an error, so typos fail silently.</p>
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
<p>Think of <code>transform</code> as sliding a photograph across a window pane: the view changes, but nothing behind the glass rearranges. It visually shifts, grows, rotates or slants an element <i>after</i> layout, so its neighbours never budge. That is the crucial difference from changing <code>margin</code> or <code>top</code>, which forces the browser to recompute the geometry of everything around the element. Because transforms skip that layout work and are composited on the GPU, hover lifts and entrance effects built on them stay smooth even on modest phones.</p>

<pre class="code">.card:hover { transform: translateY(-6px); }      /* lift */
.zoom:hover { transform: scale(1.06); }           /* grow from center */
.spin    { transform: rotate(8deg); }
.skew    { transform: skewX(-6deg); }

/* compose left to right */
.stamp { transform: translate(20px, 8px) rotate(-4deg) scale(0.9); }</pre>

<p>Walk the sample. <code>translateY(-6px)</code> slides the card 6 pixels up — negative Y is up on screen. <code>scale(1.06)</code> grows it 6% around its center; <code>scale(0.5)</code> would halve it. <code>rotate(8deg)</code> turns 8 degrees clockwise, and <code>skewX(-6deg)</code> leans it like italic type. Predict before you paste: the first two do nothing until you hover, the last two look permanently tilted.</p>

<p>The final rule composes three functions in one declaration, applied left to right: the stamp first moves 20px right and 8px down, then rotates -4 degrees, then shrinks to 0.9 — each step pivoting around the position the previous one produced. Reorder the functions and the rendered result genuinely changes. Also remember <code>translate</code> accepts percentages of the element's <i>own</i> size, which is exactly how the classic <code>translate(-50%, -50%)</code> centers an absolutely positioned element.</p>

<p>Two habits worth keeping. The pivot is <code>transform-origin</code> — the center by default; <code>top left</code> turns the element into a door swinging on its hinge. And any non-none transform creates a stacking context and becomes the containing block for <code>fixed</code> and <code>absolute</code> descendants, which is why a "position: fixed" badge sometimes stops pinning to the viewport. When animating, transition <code>transform</code> — never <code>top</code> or <code>left</code>.</p>
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
<p>2D transforms slide things around the page; add a <code>Z</code> axis and they can tilt toward or away from you — but only if somebody supplies a camera. That camera is <b>perspective</b>: the distance from the viewer to the Z=0 plane. Without it, <code>rotateX(60deg)</code> renders as a squashed rectangle; with it, you genuinely see the top face receding. Rule of thumb: <code>perspective</code> declared on the <i>parent</i> gives all its children one shared camera.</p>

<pre class="code">.scene { perspective: 600px; }        /* the viewer's distance */

.flip {
  transform: rotateX(25deg);           /* tilt back */
}
.card3d { transform: rotateY(180deg); } /* turn around */</pre>

<p>Read it as a two-actor scene. <code>.scene</code> plants the camera 600px from the page — small enough that depth reads strongly, like a wide-angle lens; 2000px would look nearly flat. Inside, predict what <code>rotateX(25deg)</code> does to <code>.flip</code>: it tips the top edge away from the viewer, so you see a trapezoid whose far edge is slightly narrower. <code>.card3d</code> rotates a full 180° around the vertical axis — you are looking at its back face, mirrored, like reading through thin paper.</p>

<p>The axes, memorised once: <code>rotateX</code> tumbles around the horizontal axis (a coin flipping away), <code>rotateY</code> swings around the vertical one (a door on its hinge), <code>rotateZ</code> is ordinary 2D rotation, and <code>translateZ</code> pops the element toward the camera — under strong perspective a few pixels of Z visibly enlarge it.</p>

<p>The gotchas that bite everyone building the classic 3D card flip: children of a 3D-transformed element are flattened back into its plane unless you set <code>transform-style: preserve-3d</code> on the flipping inner. Then stack the two faces absolutely, pre-rotate one <code>rotateY(180deg)</code>, and give both <code>backface-visibility: hidden</code>, so hover can rotate the inner a full turn. And don't confuse the property with the function: <code>perspective: 600px</code> on the parent is a shared camera, while <code>transform: perspective(600px)</code> gives this one element a private camera that its children won't share.</p>
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
<p>Nothing makes an interface feel cheaper than a state change that snaps. A <b>transition</b> tells the browser: when this property changes between two states, don't jump — interpolate. You declare it once on the <i>resting</i> state, and every change that follows — hover, focus, a toggled class — animates itself, in both directions, for free.</p>

<pre class="code">.button {
  background: #1572b6;
  transition: background 0.3s ease, transform 0.2s ease;
}
.button:hover {
  background: #0d4e82;
  transform: translateY(-2px);
}</pre>

<p>Walk it. The resting rule carries two comma-separated transitions; the hover rule only lists destination values. Predict the motion: the background blends to <code>#0d4e82</code> over 300ms while the 2px lift finishes in 200ms — the mismatch is deliberate, quick physical feedback first, colour settling underneath. Each transition has four parts in a fixed order: property, duration, timing-function, delay — the last two optional.</p>

<p>The timing function is the pacing: <code>ease</code> (the default), <code>linear</code>, <code>ease-in</code>, <code>ease-out</code>, <code>ease-in-out</code>, or a custom <code>cubic-bezier(...)</code> when stock curves won't do. Durations: 150–250ms feels right for micro-feedback, 300–400ms for panels. A <code>transition-delay</code> stalls the start — and negative delays start mid-flight.</p>

<p>Gotchas. Only interpolable properties transition: opacity, transform, colours, shadows and most numbers work; <code>display</code> snaps, and <code>height: auto</code> can't animate — use the <code>grid-template-rows: 0fr → 1fr</code> or max-height trick instead. Avoid <code>transition: all</code> — it animates whatever happens to change, often expensively. And the performance rule doubles here: anything moving continuously should transition <b>only opacity and transform</b>, because animating <code>width</code> or <code>top</code> forces a layout pass on every single frame.</p>
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
<p>Transitions need a state change to react to. <b>Animations</b> run on their own schedule from the moment they apply — which is what you want for entrances, attention loops and multi-step sequences that no hover could express. Define the movie once with <code>@keyframes</code>, then screen it with an <code>animation</code> property.</p>

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

<p>Walk both examples. <code>slide-in</code> has exactly two frames: the toast starts invisible and 24px to the left, then animates to visible at its resting spot over 0.4s with an <code>ease-out</code> deceleration — predict it sliding in while fading up. <code>pulse</code> stages three frames with percentages (<code>from</code>/<code>to</code> are just 0%/100%): scale 1, then 1.12 at the halfway point, back to 1 — and <code>infinite</code> repeats it every 1.6s, a patient heartbeat.</p>

<p>The <code>animation</code> shorthand reads: name, duration, timing-function, delay, iteration-count, direction, fill-mode. Mind the order trap: the first time value is always the duration, the second the delay — <code>animation: pulse 1.6s 0.2s</code> waits 0.2s before starting. Only the properties <i>listed in the keyframes</i> animate; everything else stays put.</p>

<p>Two patterns to steal. Toggling a class that carries an animation plays it once — the whole secret behind shake-on-error and re-triggerable entrances (remove and re-add the class to replay). And staggered entrances are just per-item delays: give the third card <code>animation-delay: 0.2s</code> and the list cascades in one after another. Wrap decorative loops in a <code>prefers-reduced-motion</code> query — the Accessibility chapter shows the standard mercy rule.</p>
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
<p>Once an animation runs, four knobs shape its character: how each cycle is paced, how many times it repeats, which way it travels, and what the element looks like before the first frame and after the last. Master these and the same keyframes read as a pendulum, a heartbeat or a bouncy badge.</p>

<p>The <b>timing-function</b> paces <i>within</i> each cycle: <code>ease</code>, <code>linear</code>, <code>ease-in-out</code>, or a custom curve like <code>cubic-bezier(0.34, 1.56, 0.64, 1)</code> — Y values above 1 overshoot the target, which is where bounce comes from. The <b>iteration-count</b> is a number or <code>infinite</code>. The <b>direction</b> can be <code>normal</code>, <code>reverse</code>, or <code>alternate</code> — forward, then backward, each cycle, like a pendulum. The <b>fill-mode</b> decides what the element looks like outside the run: <code>none</code> (the default — snap back!), <code>forwards</code> (hold the last keyframe), <code>backwards</code> (apply the first keyframe during any delay), <code>both</code>.</p>

<pre class="code">.pendulum {
  transform-origin: top center;
  animation: swing 1.2s ease-in-out infinite alternate;
}
@keyframes swing {
  from { transform: rotate(-14deg); }
  to   { transform: rotate(14deg); }
}</pre>

<p>Predict the pendulum before reading on: <code>ease-in-out</code> slows it at both ends of the arc the way gravity does, and <code>alternate</code> makes the return swing a reversed playback instead of a jarring jump back to -14deg. Mentally delete <code>alternate</code> and picture the snap — that is how much one keyword buys. Also note <code>transform-origin: top center</code> moving the pivot, so the swing hangs from the top like a real pendulum.</p>

<p>fill-mode is the classic beginner trap. An entrance with a delay and <code>from { opacity: 0 }</code> shows the element <i>fully visible</i> during the delay, because fill-mode <code>none</code> keeps the resting style until the first frame lands. Set <code>backwards</code> — or <code>both</code> in the shorthand — to apply the first keyframe during the wait. And as always: wrap decorative motion in <code>prefers-reduced-motion: reduce</code> so motion-sensitive users get a calm page (the Accessibility chapter has the standard snippet).</p>
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
<p><code>filter</code> hands any element the same sliders your photo editor has: blur, brightness, contrast, saturate, grayscale, sepia, hue-rotate, invert. Reach for it when an image needs a mood — dimmed, colourless, softly out of focus behind a modal — or when a hover should sharpen attention. The effect is paint-only, so it never disturbs the layout.</p>

<pre class="code">img.blurred  { filter: blur(4px); }
img.mood     { filter: grayscale(0.8) brightness(0.9) contrast(1.1); }
.glass:hover { filter: none; }        /* clear on hover */

.faded { opacity: 0.55; }

.drop { filter: drop-shadow(0 6px 8px rgba(0,0,0,0.35)); }</pre>

<p>Walk the samples. <code>blur(4px)</code> spreads each pixel over a 4px radius — soft, decorative. The <code>mood</code> rule chains three functions in one declaration, applied left to right: 80% grayscale, then slightly darker, then slightly more contrast — predict a flat, film-like image. <code>.glass:hover</code> clears the filter on hover, the standard "unfocused until needed" pattern. <code>opacity: 0.55</code> is not a filter but sits in the same family: it fades the whole element <i>including its children</i>, while an alpha on a colour would fade only that one colour.</p>

<p><code>drop-shadow(0 6px 8px ...)</code> looks like <code>box-shadow</code> but traces the element's <i>actual alpha shape</i>: a transparent PNG cloud gets a cloud-shaped shadow, and it hugs SVG icons perfectly — box-shadow would only outline their rectangular box.</p>

<p>Blend modes mix layers like Photoshop. <code>mix-blend-mode: multiply</code> blends an element with whatever sits behind it (multiply darkens, screen lightens, overlay boosts contrast); <code>background-blend-mode</code> instead blends an element's <i>own</i> background layers — gradient over photo, art-directed. Two gotchas: any non-none filter creates a stacking context, so z-index neighbours can reshuffle; and large blurs over big areas are paint-expensive — prefer fading opacity or pre-baked images where speed matters.</p>
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
<p>The Selectors chapter introduced <code>:is</code>, <code>:where</code>, <code>:has</code> and <code>:not</code>; this lesson builds working patterns with them. The idea behind all six: the DOM already knows its own state, so CSS can ask questions instead of waiting for JavaScript to add classes.</p>

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

<p>Walk them one at a time. Pattern 1 puts a checkbox glyph before every list item <i>except</i> the done ones — <code>:not()</code> inverts, <code>::before</code> paints the glyph. Pattern 2 is the gapless-spacing trick: <code>* + *</code> matches every child that has a previous sibling, so the first box gets no margin and outer edges stay flush. Pattern 3 is <code>:has()</code> doing what needed JavaScript for twenty years — the label of any row containing an invalid input turns red, live, as the user types. Pattern 4 is a quantity query: the moment a list holds a third item, it becomes two columns. Pattern 5 styles every link at <b>zero specificity</b>, so any later rule wins without a fight. Pattern 6 groups three headings with <code>:is()</code> — predict the score: <code>:is()</code> takes the specificity of its <i>most</i> specific argument, so the selector counts as <code>h1</code> plus <code>:not(.logo)</code>.</p>

<p>Keep the wider toolbox handy: <code>:nth-child(An+B)</code> formulas (<code>3n+1</code> hits items 1, 4, 7...), <code>:nth-last-child()</code> for counting from the end, <code>:empty</code>, <code>:default</code>, <code>:indeterminate</code>.</p>

<p>The meta-skill: before reaching for a class to mark a state — hover, checked, invalid, "contains an image" — ask whether a selector already expresses it. Fewer hooks, cleaner markup, CSS that documents itself.</p>
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
<p>The Cascade chapter promised that <code>@layer</code> lets you draw the winner bracket yourself: sort declarations into named tiers, and tier order outranks specificity. Here is the professional architecture in full — six named tiers, declared in one breath before any block fills them.</p>

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

<p>Each block fills one tier, and each tier has one job. reset holds only mechanical normalisation — border-box, zeroed margins — that nobody should ever need to out-rank. base sets element-level defaults: fonts, text colour, link colour. components holds the classes your markup actually uses, and utilities are single-purpose override classes like <code>.mt-2</code>. Notice what is absent: no IDs, no <code>!important</code>, no specificity games — the tiers do the sorting.</p>

<p>Predict the fights before reading the verdicts. The single class <code>.text-center</code> in <code>utilities</code> beats a three-ID selector in <code>base</code>, because layers are compared <i>before</i> specificity — yet inside one layer, specificity still ranks normally, so <code>base</code>'s own rules resolve the old way. Unlayered styles outrank every layer, the escape hatch for one-off page fixes. Repeating a name appends to it, and the up-front <code>@layer a, b;</code> line locks the order even when the blocks live in different files.</p>

<p>The design-system payoff: resets can never accidentally beat components, utilities always win arguments, and third-party CSS gets a sealed <code>@layer vendor;</code> declared before you import it. One genuinely surprising gotcha — <code>!important</code> <i>reverses</i> layer order: among important declarations the <i>earliest</i> layer wins, and any important declaration beats a normal one outright. Use important inside layered systems only when you truly mean it.</p>
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
<p>Every card-grid has the same old bug: one card's title wraps to two lines and the Buy buttons in the other cards no longer line up. A nested grid couldn't fix it, because a child grid sizes its own rows independently. <b>Subgrid</b> hands the child the parent's tracks instead — <code>grid-template-rows: subgrid</code> means "pace me with the same rows my siblings use".</p>

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

<p>Read it as a contract. The parent lays out three 1fr columns; each card is itself a grid that spans three rows of the parent and, with subgrid, renders its title, body and button into those <i>shared</i> rows. Predict what happens when the middle card's title wraps: the parent's first row grows for everyone, and every button still sits on the same baseline. Without subgrid, only the middle card would stretch and the buttons would scatter.</p>

<p>It works on columns too — nested form sections whose labels align across containers. Support is Baseline across all major browsers since 2023, so use it freely; just remember a subgridded axis inherits the parent's <code>gap</code>, and a different gap on the child is ignored along it.</p>

<p>Three more advanced moves from MDN's guides. <b>Named lines</b> — <code>grid-template-columns: [main-start] 1fr [aside-start] 300px [main-end]</code> — let you place items by name, so renumbering tracks doesn't break placement. <code>grid-auto-flow: dense</code> backfills the holes spanning items leave behind, masonry-style packing for mixed image sizes. And mixing item spanning with auto-placement gives you one 2×2 hero inside a grid that otherwise flows on its own.</p>
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
<p>Two of the newest platform powers — both turn "impossible without JavaScript" into a few lines of CSS.</p>

<p><b>Anchor positioning</b> attaches a floating element — tooltip, popover, menu — to an anchor element and lets the browser keep it glued there, flipping it to stay on-screen. For years that meant hundreds of lines of measuring JavaScript in every tooltip library; now it is declarative.</p>

<pre class="code">.info-btn { anchor-name: --info; }

.tooltip {
  position: absolute;
  position-anchor: --info;
  position-area: top;          /* above the anchor */
  position-try-fallbacks: flip-block;  /* flip if no room */
}</pre>

<p>Walk it. The button declares itself as <code>--info</code>; the tooltip's <code>position-anchor</code> adopts that name, so its <code>absolute</code> positioning now resolves against the <i>button</i> instead of the nearest positioned ancestor. <code>position-area: top</code> seats it above the anchor — predict the edge case the last line covers: bring the button near the top of the viewport and there is no room above, so <code>flip-block</code> re-seats the tooltip below. It pairs naturally with the native <code>&lt;dialog&gt;</code> element and the Popover API.</p>

<p><b>Scroll-driven animations</b> swap an animation's clock: progress follows scrolling instead of seconds — no scroll listeners, no jank from main-thread handlers.</p>

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

<p>The reading bar starts at <code>scaleX(0)</code>, grows from its left edge, and its <code>scroll(root)</code> timeline maps page progress onto the animation — 40% down the page, bar 40% wide. <code>view()</code> instead tracks the element's own journey through the viewport, which is reveal-on-scroll in two lines. Support is still uneven across engines: wrap both in <code>@supports</code> (Compatibility chapter) so other browsers keep a static fallback — and give users with reduced-motion preferences a still page.</p>
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
<p>CSS's first accessibility duty is the <b>focus ring</b>. Keyboard users navigate with Tab, and the ring is their cursor — delete <code>outline</code> with no replacement and they are literally lost on your page. The old dilemma was aesthetic: rings also appeared for mouse clicks, where designers hated them. <code>:focus-visible</code> ends the argument by letting the browser decide who needs the ring.</p>

<pre class="code">/* mouse clicks: no ring. Keyboard Tab: clear ring. */
:focus-visible {
  outline: 3px solid #ffd43b;
  outline-offset: 2px;
}
:focus:not(:focus-visible) { outline: none; }</pre>

<p>Walk the pair of rules, then run the two tests in your head. Click the button with a mouse: the browser judged this a pointer user, so <code>:focus-visible</code> does not match and the second rule strips the outline — clean. Now press Tab instead: the browser has watched the interaction method, matches <code>:focus-visible</code>, and paints a 3px yellow ring with a 2px gap (<code>outline-offset</code> keeps it clear of the button's edge). Every modern engine agrees on the essentials, so this snippet is safe to paste into every project.</p>

<p>Related tools: <code>:focus-within</code> styles a whole form row while its input holds focus, and <code>scroll-margin-top</code> on link targets keeps keyboard jumps from hiding content under sticky headers.</p>

<p>States to honour honestly. Never put information behind <code>:hover</code> alone — touch screens have no hover. Keep <code>:disabled</code> readable and explain <i>why</i> in text next to the control. Prefer <code>:user-invalid</code> over <code>:invalid</code> so error styling waits until the user has actually touched the field — shouting red on page load is worse than silence. And colour never carries meaning alone: pair a red error with an icon or words.</p>
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
<p>CSS can sense user needs and honour them through media queries — no JavaScript, no settings page of your own. The three that matter most: reduced motion, dark preference, and forced colours.</p>

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

<p>Walk the first block — it is the standard mercy rule, and this app ships it too. Users with vestibular disorders get motion sickness from parallax, auto-carousels and bouncing badges; forcing every duration to 0.01ms with one iteration ends the movement while keeping the end states, and <code>scroll-behavior: auto</code> stops smooth-scroll jumps. Predict the result: the page looks identical, just still. The second block flips the OS preference into tokens: when the system is dark, the <code>:root</code> variables change — and because every rule reads <code>var(--bg)</code>, the whole page follows. Tokens from the Architecture chapter, doing real work. The third block answers Windows High Contrast themes, which override your palette: <code>ButtonText</code> is a system keyword that resolves to the user's theme colour, and borders and outlines become the visible structure of your UI.</p>

<p>Gotchas: WCAG asks 4.5:1 contrast for body text (3:1 for large text), so test any <code>color-mix()</code>-generated tint before shipping it; never let colour alone carry meaning. In forced-colours mode, don't bake essential information into your chosen colours — the user's theme owns them now. Mostly this is a chapter about restraint: don't remove outlines, don't disable zoom, don't move things without permission.</p>
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
<p>Stylesheets rot when names lie: is <code>.title</code> safe to change, or does a modal three screens away depend on it? Conventions keep intent readable, and the most famous is <b>BEM</b> — Block, Element, Modifier. A block is a standalone component, an element is a part of one, a modifier is a variant.</p>

<pre class="code">.card { }                    Block: the component
.card__title { }             Element: a part of it (double underscore)
.card__button { }
.card--featured { }          Modifier: a variant (double dash)
.card--compact { }</pre>

<p>Read the anatomy straight from the names: the double underscore says <code>.card__title</code> belongs to the card and can never interfere with <code>.modal__title</code>'s business; the double dash says <code>.card--featured</code> is the same card in different clothes. In markup a variant composes beside its base — <code>class="card card--featured"</code> — so the card styles apply and the modifier only adds on top. Predict the specificity table: every selector is one flat class, worth 0-1-0, so nothing out-ranks anything and later rules or layers decide. That flatness is the entire point — no descendant selectors means no accidental leaks in either direction. BEM's names run long, but that length is the price of styles that cannot leak.</p>

<p>Alternatives, briefly: <b>SMACSS</b> categorises rules (base, layout, module, state, theme); <b>ITCSS</b> orders layers by specificity — the pre-<code>@layer</code> ancestor, whose job cascade layers now do natively; modern component frameworks scope styles per component and sidestep naming altogether. BEM stays the lingua franca. Even if your next project never uses it, you must be able to read it — and the flat-class discipline it teaches transfers everywhere.</p>
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
<p>Two opposite philosophies, both mainstream. <b>Semantic-first</b> (the BEM world) names styles after meaning — <code>.card</code>, <code>.button--danger</code> — so HTML rarely changes and CSS changes freely. <b>Utility-first</b> (the Tailwind model) composes tiny single-purpose classes directly in the markup:</p>

<pre class="code">&lt;div class="flex gap-3 rounded-lg p-4 bg-blue-50"&gt;...&lt;/div&gt;

/* the utilities behind it */
.flex { display: flex; }
.gap-3 { gap: 0.75rem; }
.rounded-lg { border-radius: 8px; }
.p-4 { padding: 1rem; }
.bg-blue-50 { background: #eff6ff; }</pre>

<p>Read the markup as a sentence: flexbox layout, 0.75rem gap, 8px radius, 1rem padding, pale blue background. Each utility does exactly one thing, so <code>.p-4</code> can never surprise you; predict the payoff — delete the element and its styles leave with it, so there is no dead CSS and no naming debate. Compare the semantic world, where deleting a component means hunting its CSS across files. The cost of utilities sits in the markup: spacing decisions live in templates, so a redesign touches many files instead of one.</p>

<p>Design <b>tokens</b> are the shared foundation either approach consumes: named decisions like <code>--space-2: 0.5rem</code> and <code>--color-brand</code> defined once as custom properties — one source of truth for the whole system. Generate utilities <i>from</i> tokens and the system scales without drifting — change <code>--color-brand</code> once and every tint, button and badge follows. Tokens also document the scale itself: when a new spacing step is needed, designers see the existing list before inventing a fourth value. That is the trick the tryit below performs: twelve lines that already behave like a tiny design system.</p>

<p>Most mature codebases end up hybrid: token-driven custom properties, semantic component classes for the big pieces, a thin utility layer for spacing and alignment one-offs — with cascade layers enforcing the pecking order (utilities last, so they always win).</p>
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
<p>Past a few hundred rules, a stylesheet is a codebase and needs a structure: one purpose per file, an agreed order, and an obvious place for every new rule. The classic breakdown is <code>reset.css</code>, <code>tokens.css</code>, <code>base.css</code>, <code>layout.css</code>, <code>components/*.css</code>, <code>utilities.css</code> — and the order is not taste, it is the cascade doing your architecture for you.</p>

<pre class="code">/* styles.css — the index */
@layer reset, tokens, base, layout, components, utilities;

@import "./reset.css" layer(reset);
@import "./tokens.css" layer(tokens);
@import "./base.css" layer(base);
@import "./components.css" layer(components);
@import "./utilities.css" layer(utilities);</pre>

<p>Walk the index file. The first line declares all six layers up front, locking their order; each import then lands in its named layer. Predict the consequences: a one-class utility in <code>utilities.css</code> beats any selector in <code>components.css</code> regardless of specificity, tokens are merely definitions so their position matters little, and nobody fixes a component by sneaking in a heavier selector — the layer decides, not cleverness.</p>

<p>The habits that keep it alive: keep a component's styles next to its markup or component file, because findability beats elegance; comment the <i>why</i> — "z-index: 40, above the sticky header (30)" saves the next person an hour; and prune dead selectors regularly, since they accumulate like dust and every rule costs matching work on DOM changes. One caveat: chained <code>@import</code>s fetch files one after another at runtime, so let a bundler inline the final stylesheet — the layer statements survive bundling and keep enforcing the order.</p>

<p>Architecture is deciding up front where things go, so the answer never has to be "anywhere".</p>
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
<p>CSS rarely tops a performance audit, but it has three costs worth knowing: <b>download</b>, <b>matching</b> and <b>rendering</b>.</p>

<p><b>Download:</b> stylesheets block first render — the browser refuses to paint before CSS arrives, because unstyled content flashing and re-painting looks broken. So ship CSS early (<code>&lt;link&gt;</code> in the head), compressed with gzip or brotli; split into per-route files only when routes truly differ; and set <code>font-display: swap</code> so a slow web font shows fallback text instead of holding your copy hostage.</p>

<p><b>Matching:</b> engines match selectors right-to-left and do it <i>fast</i> — the folklore "avoid descendant selectors" is mostly obsolete. The real cost today is an enormous stylesheet nobody prunes: every rule can be re-matched after every DOM change. Write natural selectors; spend the saved effort deleting dead CSS.</p>

<p><b>Rendering</b> is a pipeline: style → layout → paint → composite. The gold is animating only the last stage. <code>opacity</code> and <code>transform</code> are composite-only — the GPU moves pixels that are already painted, so 60fps is nearly free. Geometry properties — <code>width</code>, <code>height</code>, <code>top</code>, <code>margin</code>, <code>font-size</code> — trigger <b>layout</b>: the browser recomputes geometry, possibly for the whole page, then repaints. The tryit below shows both side by side; hover each box and feel which one stays smooth on a busy page.</p>

<pre class="code">.reveal { will-change: transform; }  /* hint: promote to its own layer */
/* but add sparingly — every hint costs memory */</pre>

<p><code>will-change</code> is a hint, not a switch: it promotes the element to its own compositor layer so the GPU can animate it cheaply. Add it just before an animation runs and remove it afterwards — one per animated element, because every layer costs memory. Big filters and shadows over large areas are paint-heavy for the same reason; contain the effect or pre-bake the image. Then the golden rule: open the devtools Performance panel, <i>measure</i>, and optimise what the numbers say — not what folklore says.</p>
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
<p>Browsers differ — that is permanent. The professional response is never "target one browser": it is <b>progressive enhancement</b>. Build a solid baseline every engine understands, then layer upgrades where support exists. CSS ships its own feature detector: <code>@supports</code>.</p>

<pre class="code">.gallery { display: flex; gap: 8px; }        /* baseline: works everywhere */

@supports (display: grid) {
  .gallery { display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); }
}

@supports not (container-type: inline-size) {
  .card { /* a media-query fallback instead */ }
}</pre>

<p>Walk the pattern. Every browser applies the flex baseline. A browser that understands grid answers the condition and applies the block too — and because it comes <i>later</i> in the cascade, the upgrade wins. A browser that has never seen <code>(display: grid)</code> skips the whole block as if it did not exist. The <code>@supports not (...)</code> form is the mirror image: patch only the engines lacking a feature. The order is load-bearing — fallback first, enhancement after — and no JavaScript or user-agent sniffing is involved (sniffing is the anti-pattern: it lies the moment a new engine ships).</p>

<p>The quieter detector lives at the declaration level. CSS's error recovery drops any declaration it cannot parse — one declaration at a time, never the whole rule:</p>

<pre class="code">.card {
  background: #1572b6;                                /* fallback */
  background: color-mix(in srgb, #1572b6 80%, white); /* modern */
  width: max(300px, 50vw);                            /* unknown = ignored */
}</pre>

<p>An old browser reads the first <code>background</code>, fails on <code>color-mix()</code>, discards only that line and keeps plain blue; a modern browser parses both and the later one wins. Same stylesheet, two looks, zero detection code — one extra line, no runtime work. Write fallback-then-enhancement as a reflex, and compatibility stops being a chore.</p>
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
<p>How do you know what is safe to use today? The ecosystem's shared answer is <b>Baseline</b> — a label that MDN and caniuse put on every web platform feature. Read it as a traffic light with three states. <b>Newly available</b>: the feature works in the current version of every major browser, so use it behind an <code>@supports</code> check with a fallback in mind. <b>Widely available</b>: it has worked across browsers for 30+ months, so even users who never update are covered — use it without ceremony. <b>Limited availability</b>: not yet in every engine; experiment, but keep the fallback first in the cascade.</p>

<p>Make checking it a reflex: every MDN property page opens with its Baseline status and browser badges. Predict the answers for features from this course — <code>:has()</code> and container queries are Baseline now; subgrid reached Baseline more recently; anchor positioning is still limited. That one glance replaces memorising release tables for four engines.</p>

<p>The working policy beyond the label. Know your <b>audience</b> from analytics — "everyone uses the latest Chrome" is a myth, and the real long tail is old enterprise builds and phones. <b>Evergreen browsers</b> update themselves, so your problem users are the ones who can't update. And <b>test</b>: before shipping any new layout technique, at minimum open it in current Chrome, Firefox and Safari — one browser's devtools can emulate some differences, but rendering engines still disagree in the corners.</p>

<p>That closes the journey, from "what is a rule" to cascade layers and scroll-driven animation. CSS rewards one habit above all: build the baseline, layer the enhancements, and let every browser give its best.</p>
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
