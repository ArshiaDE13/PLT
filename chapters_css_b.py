"""CSS Tutor chapters 4-8 (Phase 2 continued + Phase 3), grounded in MDN."""

CHAPTERS_CSS_B = [
    # ------------------------------------------------------------------ cs04
    {
        "id": "cs04",
        "title": "CSS Values & Units",
        "emoji": "📏",
        "lessons": [
            {
                "title": "Absolute & Relative Lengths",
                "html": """
<p>Every size you write in CSS — font, padding, width, shadow — carries
a unit, and the unit decides whether that size is frozen or adaptive.
Two families exist, and choosing between them is a design decision, not
a syntax detail.</p>

<p><b>Absolute</b> — fixed, predictable:</p>

<ul>
<li><code>px</code> — the CSS pixel (not a hardware pixel); the everyday
unit for borders, shadows, small details</li>
<li><code>pt</code>, <code>cm</code>, <code>in</code> — print-world
units, rarely used on screens</li>
</ul>

<p><b>Relative</b> — scale with context; the backbone of flexible
design:</p>

<ul>
<li><code>em</code> — relative to the <b>element's own font-size</b>.
Careful: it compounds — nested ems multiply</li>
<li><code>rem</code> — relative to the <b>root</b> element's font-size
(default 16px). No compounding — the recommended default for font sizes,
paddings, margins</li>
<li><code>%</code> — relative to the parent (widths) or font (some
properties)</li>
<li><code>ch</code> — the width of the "0" digit; lovely for limiting
text measure: <code>max-width: 60ch</code></li>
</ul>

<p>The compounding gotcha deserves a number. A <code>1.2em</code> list
inside another <code>1.2em</code> list inside a third computes
1.2 × 1.2 × 1.2 ≈ 1.73× the base size — each nesting level multiplies
the last. <code>rem</code> has no ladder: it always reads the root, so
<code>2rem</code> is 32px no matter how deep it sits:</p>

<pre class="code">html { font-size: 100%; }        /* 16px */
h1   { font-size: 2rem; }        /* 32px, scales if user zooms text */
p    { max-width: 65ch; }        /* readable line length */
.note{ font-size: 0.8em; }       /* 80% of this element's font */</pre>

<p>Walk the block: the root stays at its 16px default; the heading is
32px in rem; the paragraph caps its measure at 65 digit-widths — the
classic readable line; the note is 80% of <i>its own</i> font — em,
deliberately, because it's a one-level tweak. Predict the Try-it: the
nested <code>1.2em</code> boxes render progressively larger text, while
the rem box ignores nesting entirely.</p>

<p>Why <code>rem</code> wins for typography: users who need bigger text
change their browser's default font size, and every rem-based value
respects that. px ignores them — an accessibility loss you can avoid
for free.</p>
""",
                "tryit": """<!DOCTYPE html>
<html lang="en">
<head><title>Lengths</title>
<style>
  body { font-family: sans-serif; }
  .box { padding: 0.5rem 1rem; margin: 8px 0; border-radius: 6px; }
  .px-rem { background: #1572b6; color: white; width: 20rem; }
  .em-compound { font-size: 1.2em; background: #33a9dc33; }
    .em-compound .em-compound { font-size: 1.2em; } /* compounds! */
  .measure { max-width: 30ch; background: #f2f8fe; padding: 8px; }
</style>
</head>
<body>
  <div class="box px-rem">width: 20rem — scales with root font size</div>
  <div class="em-compound">1.2em
    <div class="em-compound">nested 1.2em compounds (1.44×)</div>
  </div>
  <p class="measure">max-width: 30ch keeps this paragraph readable —
     lines never grow past about 30 "0" characters.</p>
</body>
</html>
""",
            },
            {
                "title": "Viewport Units & fr",
                "html": """
<p>Sometimes the reference you want isn't the parent element — it's the
<b>browser window itself</b>. Viewport units measure against it:</p>

<ul>
<li><code>1vw</code> — 1% of the viewport <b>width</b></li>
<li><code>1vh</code> — 1% of the viewport <b>height</b></li>
<li><code>vmin</code> / <code>vmax</code> — 1% of the smaller/larger
dimension (adapts to rotation!)</li>
</ul>

<p>Turn a phone sideways and <code>vmin</code> follows the new short
edge — that's the rotation superpower. Three idioms you'll meet
constantly:</p>

<pre class="code">.hero  { height: 60vh; }        /* 60% of the screen height */
.modal { width: min(90vw, 600px); }  /* never wider than the screen */
h1     { font-size: clamp(2rem, 5vw, 4rem); }  /* fluid type */</pre>

<p>Walk them: the hero fills 60% of whatever height exists; the modal
grows with the screen but stops at 600px (min() is next lesson); the
heading scales between 2rem and 4rem as the viewport widens. Each line
replaces what used to be a media query.</p>

<p>The <code>fr</code> unit is special: it exists only inside grids (and
flex sizing) and means "one fraction of the <i>leftover
space</i>":</p>

<pre class="code">grid-template-columns: 1fr 2fr;   /* second column is twice the first */
grid-template-columns: 1fr 1fr;   /* equal halves of what remains */</pre>

<p>Unlike <code>%</code>, <code>fr</code> divides only the space left
after fixed-size tracks take theirs — <code>200px 1fr</code> gives the
fixed column exactly 200px and <code>1fr</code> everything else.
Predict the Try-it: the <code>1fr</code> box is visibly half the width
of the <code>2fr</code> box, and the hero's height tracks the preview
window when you resize it.</p>

<p>Gotcha: <code>100vh</code> on mobile browsers can overshoot the
visible area because the address bar collapses while scrolling — the
modern fix is <code>100dvh</code> (dynamic viewport height). Viewport
units + fr are the vocabulary of modern layout; Grid (Layout chapter)
makes them sing.</p>
""",
                "tryit": """<!DOCTYPE html>
<html lang="en">
<head><title>Viewport & fr</title>
<style>
  body { font-family: sans-serif; margin: 0; }
  .hero { height: 40vh; background: #1572b6; color: white;
          display: grid; place-items: center;
          font-size: clamp(1.4rem, 4vw, 3rem); }
  .cols { display: grid; grid-template-columns: 1fr 2fr; gap: 8px;
          padding: 10px; }
  .cols div { background: #eaf4fd; padding: 8px; border-radius: 6px; }
</style>
</head>
<body>
  <div class="hero">height: 40vh — resize the preview!</div>
  <div class="cols">
    <div>1fr</div>
    <div>2fr — twice as wide</div>
  </div>
  <p>The heading above scales with viewport width via clamp().</p>
</body>
</html>
""",
            },
            {
                "title": "Math Functions: calc(), min(), max(), clamp()",
                "html": """
<p>CSS can do arithmetic — right inside any value, mixing units that
JavaScript would refuse to add. Four functions cover nearly every
need.</p>

<p><b><code>calc()</code></b> mixes units freely:</p>

<pre class="code">.sidebar-page { width: calc(100% - 250px); }
.hero { height: calc(100vh - 64px); }   /* full height minus a header */
.gap-fix { margin-left: calc(50% + 8px); }</pre>

<p>Percentages meet pixels: "everything except the 250px sidebar",
"full height minus the 64px header". One famous syntax trap: spaces
around <code>+ -</code> are <b>required</b> —
<code>calc(100%-8px)</code> is invalid, because the parser reads
"100%-8" as one malformed identifier and silently drops the whole
declaration. <code>* /</code> work without spaces, and one side must be
a plain number.</p>

<p><b><code>min()</code> / <code>max()</code></b> pick the smallest or
largest of their arguments — self-adapting values without media
queries:</p>

<pre class="code">.panel { width: min(90%, 600px); }   /* big: 600px, phone: 90% */
.text  { font-size: max(1rem, 14px); } /* never below 14px */</pre>

<p>On a desktop the panel caps at 600px; on a phone, 90% of a narrow
screen is smaller, so that wins. Note the mental flip: <code>min()</code>
gives you a <i>maximum</i> — it returns whichever argument is smaller.</p>

<p><b><code>clamp(min, preferred, max)</code></b> — min and max with a
fluid middle in one function. The fluid-typography idiom:</p>

<pre class="code">h1 { font-size: clamp(2rem, 5vw, 4rem); }
/* small screens: 2rem, scales with viewport, never above 4rem */</pre>

<p>One line replaces a whole media-query ladder: below the range the
value pins to 2rem, above it pins to 4rem, and between them 5vw glides.
Predict the Try-it: the heading resizes as you drag, the panel stops
growing past 420px, and nothing jumps. Gotcha: keep the arguments in
order — clamp guards the middle value, so a swapped min/max silently
inverts your intent; when in doubt, nest clamp inside calc() freely,
since all these functions compose.</p>
""",
                "tryit": """<!DOCTYPE html>
<html lang="en">
<head><title>CSS math</title>
<style>
  body { font-family: sans-serif; margin: 0; }
  h1 { font-size: clamp(1.6rem, 6vw, 3.4rem); color: #1572b6; }
  .panel {
    width: min(90%, 420px);
    margin: 12px auto;
    padding: 12px;
    background: #eaf4fd;
    border-radius: 10px;
  }
  .page { width: calc(100% - 40px); background: #f2f8fe;
          margin: 0 auto; padding: 8px; }
</style>
</head>
<body>
  <h1>Fluid heading</h1>
  <div class="panel">width: min(90%, 420px) — resize and watch it stop.</div>
  <div class="page">width: calc(100% - 40px)</div>
</body>
</html>
""",
            },
        ],
        "quiz": [
            {
                "type": "mc",
                "question": "Which unit is relative to the ROOT font-size and avoids compounding?",
                "options": ["em", "rem", "%", "vh"],
                "answer": 1,
                "explain": "rem = root em; em compounds through nesting, rem always anchors to the root.",
            },
            {
                "type": "blank",
                "question": "max-width: <code>____</code>ch is the classic readable-line-length trick.",
                "answers": ["60", "65", "60-75", "70"],
                "explain": "ch measures the digit width — 60-75ch keeps text comfortably readable.",
            },
            {
                "type": "mc",
                "question": "What does <code>clamp(2rem, 5vw, 4rem)</code> do?",
                "options": [
                    "Always 2rem",
                    "Scales with viewport but never below 2rem or above 4rem",
                    "Adds the three values",
                    "Picks 5vw always",
                ],
                "answer": 1,
                "explain": "clamp = min and max guards around a fluid preferred value — one-line responsive type.",
            },
            {
                "type": "mc",
                "question": "Which calc() is VALID?",
                "options": ["calc(100%-8px)", "calc(100% - 8px)", "calc(100 % - 8 px)", "calc(100%- 8px)"],
                "answer": 1,
                "explain": "The + and - operators need spaces on both sides, or the parser reads them as signs.",
            },
        ],
    },

    # ------------------------------------------------------------------ cs05
    {
        "id": "cs05",
        "title": "Colors",
        "emoji": "🎨",
        "lessons": [
            {
                "title": "Color Values",
                "html": """
<p>CSS speaks several colour languages — all spelling the same painted
pixels. Knowing which to reach for speeds up every design decision:</p>

<ul>
<li><b>Named</b>: <code>tomato</code>, <code>royalblue</code>,
<code>rebeccapurple</code> — 148 predefined names</li>
<li><b>HEX</b>: <code>#1572b6</code>, shorthand
<code>#0af</code>, and with alpha <code>#1572b680</code></li>
<li><b>RGB</b>: <code>rgb(21, 114, 182)</code> — red/green/blue 0–255;
modern syntax allows spaces and optional slash-alpha:
<code>rgb(21 114 182 / 50%)</code></li>
<li><b>HSL</b>: <code>hsl(205deg 79% 40%)</code> — <b>hue</b> (the colour
wheel position, 0–360), <b>saturation</b> (grey→vivid), <b>lightness</b>
(black→white). The human-readable one</li>
<li><b>HWB</b>: <code>hwb(205 10% 20%)</code> — hue + white + black;
intuitive for tinting</li>
</ul>

<p>All five describe colours the browser converts to one internal model
before painting — what differs is how <i>you</i> think. HEX is the
interchange format of design tools; RGB is what screens physically mix.
HSL is the designer's choice because its parts are meaningful: want a
darker shade of your brand blue? Keep the hue, lower the lightness.
Want the accent? Raise the saturation. Picking colours by wheel
position beats guessing hex codes.</p>

<p><b>Alpha</b> (opacity) rides along in every syntax:
<code>rgb(21 114 182 / 0.5)</code>, <code>#1572b680</code>,
<code>hsl(205 79% 40% / .5)</code>. Now the classic exam question —
alpha in the colour versus the separate <code>opacity</code> property.
Alpha fades <i>only that colour</i>; <code>opacity</code> fades the
<i>whole element</i> including its text. A banner with an alpha
background keeps its text crisp; the same banner with
<code>opacity: 0.5</code> goes ghostly — text included.</p>

<p>Gotcha: hex is case-insensitive (<code>#1572b6</code> equals
<code>#1572B6</code>), but named colours are keywords — a typo like
<code>bleu</code> fails silently and the declaration is dropped.
Predict the Try-it: the last swatch is the brand hue at 35% alpha, so
the text inside stays fully solid while the panel goes translucent.</p>
""",
                "tryit": """<!DOCTYPE html>
<html lang="en">
<head><title>Colour values</title>
<style>
  body { font-family: sans-serif; }
  .swatch { display: inline-block; width: 130px; padding: 10px;
            border-radius: 8px; color: white; margin: 4px; }
  .named { background: steelblue; }
  .hex   { background: #1572b6; }
  .rgb   { background: rgb(46, 139, 87); }
  .hsl   { background: hsl(25 84% 53%); }
  .alpha { background: hsl(205 79% 40% / 0.35); color: #1572b6; }
</style>
</head>
<body>
  <span class="swatch named">named: steelblue</span>
  <span class="swatch hex">hex: #1572b6</span>
  <span class="swatch rgb">rgb()</span>
  <span class="swatch hsl">hsl()</span>
  <span class="swatch alpha">alpha 0.35</span>
</body>
</html>
""",
            },
            {
                "title": "Gradients",
                "html": """
<p>A gradient is a <b>generated image</b> — CSS paints it on the fly, no
file to download. Formally a value of the <code>&lt;image&gt;</code>
type, it goes anywhere an image is valid: backgrounds, borders, even
text via background-clip. Three flavours:</p>

<pre class="code">/* linear: colour flow along an angle */
background: linear-gradient(to right, #1572b6, #33a9dc);
background: linear-gradient(135deg, #1572b6 0%, #33a9dc 60%, #7fd0ff 100%);

/* radial: radiating from a point */
background: radial-gradient(circle at center, #ffd43b, #f5a623);

/* conic: sweeping around a point — pie charts for free */
background: conic-gradient(#1572b6 0 60%, #33a9dc 60% 85%, #eee 85%);</pre>

<p>Walk it: the first linear flows left-to-right, brand blue fading to
lighter blue; the second adds a position to each stop, so the final
colour only occupies the last 40% of the diagonal. Radial bursts
outward from a centre point; conic sweeps like a clock hand, and
because stops can carry position ranges (<code>#1572b6 0 60%</code>),
three ranges give you a pie chart with hard edges — two stops sharing a
position (<code>blue 50%, red 50%</code>) is the hard-boundary trick.</p>

<ul>
<li>Colour stops can carry positions (<code>#1572b6 60%</code>) — hard
edges come from two stops sharing a position
(<code>blue 50%, red 50%</code>)</li>
<li>Gradients are paint, not layout — they scale with their box, so
they're resolution-independent by nature</li>
<li>Because they're images, they can be <b>multiple</b> and layered with
transparency (next lesson)</li>
</ul>

<p>Predict the Try-it before running: three rounded bars — a soft
diagonal wash, a yellow-to-orange glow brightest at its centre, and a
segmented conic divided 60 / 25 / 15. The classic tricks to steal:
soft page backgrounds (<code>linear-gradient(#fff, #f2f8fe)</code>),
progress-like conic rings, and image overlays — a gradient from
transparent to black over a photo so text stays readable (next lesson
does exactly that).</p>

<p>Gotcha: a gradient lives in <code>background-image</code>, never in
<code>background-color</code> — if yours "doesn't show", that mix-up is
the first thing to check.</p>
""",
                "tryit": """<!DOCTYPE html>
<html lang="en">
<head><title>Gradients</title>
<style>
  body { font-family: sans-serif; }
  .demo { height: 70px; border-radius: 10px; margin: 10px 0;
          color: white; display: grid; place-items: center;
          font-weight: bold; }
  .linear { background: linear-gradient(135deg, #1572b6, #33a9dc); }
  .radial { background: radial-gradient(circle, #ffd43b, #f5a623); }
  .conic  { background: conic-gradient(#1572b6 0 60%, #33a9dc 60% 85%, #ddd 85%); }
</style>
</head>
<body>
  <div class="demo linear">linear-gradient</div>
  <div class="demo radial">radial-gradient</div>
  <div class="demo conic">conic-gradient (60% / 25% / 15%)</div>
</body>
</html>
""",
            },
            {
                "title": "color-mix() & Modern Color",
                "html": """
<p>Design systems need ten shades of the brand colour: pale tints for
backgrounds, deeper shades for hover, faded ones for borders. The old
way: a designer generates and hand-codes all ten. The new way: CSS
computes them. <b><code>color-mix()</code></b> mixes two colours in any
colour space, with optional percentages:</p>

<pre class="code">:root { --brand: #1572b6; }

.card        { background: color-mix(in srgb, var(--brand) 15%, white); }
.card:hover  { background: color-mix(in srgb, var(--brand) 85%, white); }
.border      { border-color: color-mix(in srgb, var(--brand) 40%, transparent); }</pre>

<p>Read the first line as "15% brand blue + 85% white" — a pale tint.
The hover ramps to 85% brand: same family, nearly full strength. The
border mixes with <code>transparent</code>, the clean way to build an
alpha ramp. One custom property feeds the entire tint/shade ladder —
hover states, borders, backgrounds — and a rebrand is a one-line
change. Percentages default to 50/50 when omitted.</p>

<p>Beyond mixing, modern CSS adds <b>wider-gamut spaces</b>:
<code>oklch()</code> and <code>lab()</code> describe colour the way
humans perceive it — uniform lightness means
<code>oklch(70% 0.1 250)</code> and <code>oklch(70% 0.1 30)</code> look
<b>equally bright</b> despite being different hues, which the old HSL
never guaranteed (its 50% yellow is far brighter than its 50% blue).
And <b>relative colour syntax</b> derives from an existing colour:</p>

<pre class="code">.darker {
  background: oklch(from var(--brand) calc(l - 0.15) c h);
}</pre>

<p>Take the brand colour, keep its chromaticity and hue, subtract 0.15
of lightness — a shade computed from the source, not sampled by eye.
Predict the Try-it: four rows stepping from a 12% tint through the pure
brand to an 80%-with-black shade, all from one <code>--brand</code>.</p>

<p>Start with color-mix() — it's supported everywhere modern and solves
the everyday need; reach for oklch when you need perceptually-even
palettes at scale. Gotcha: mixing happens in the space you name —
<code>in srgb</code> and <code>in oklab</code> give visibly different
midpoints for the same two inputs.</p>
""",
                "tryit": """<!DOCTYPE html>
<html lang="en">
<head><title>color-mix()</title>
<style>
  body { font-family: sans-serif; }
  :root { --brand: #1572b6; }
  .card {
    border: 2px solid var(--brand);
    border-radius: 10px;
    padding: 12px;
    max-width: 320px;
  }
  .row { padding: 10px; border-radius: 6px; margin: 4px 0; }
  .tint  { background: color-mix(in srgb, var(--brand) 12%, white); }
  .mid   { background: color-mix(in srgb, var(--brand) 50%, white); color: white; }
  .full  { background: var(--brand); color: white; }
  .shade { background: color-mix(in srgb, var(--brand) 80%, black); color: white; }
</style>
</head>
<body>
  <div class="card">
    <div class="row tint">brand 12% + white</div>
    <div class="row mid">50/50 mix</div>
    <div class="row full">brand</div>
    <div class="row shade">brand 80% + black</div>
    <p>Four shades, one source of truth. Change --brand above!</p>
  </div>
</body>
</html>
""",
            },
        ],
        "quiz": [
            {
                "type": "mc",
                "question": "HSL's three components are:",
                "options": ["Red, Green, Blue", "Hue, Saturation, Lightness", "Height, Size, Length", "Hex, Weight, Blend"],
                "answer": 1,
                "explain": "HSL = hue (wheel position), saturation (vividness), lightness — meaningful parts to tweak.",
            },
            {
                "type": "blank",
                "question": "The function generating a colour flow between stops is <code>____-gradient</code>.",
                "answers": ["linear", "radial", "conic"],
                "explain": "linear/radial/conic-gradient are all generated images usable anywhere an image is.",
            },
            {
                "type": "mc",
                "question": "opacity: 0.5 on an element vs an alpha colour — the difference:",
                "options": [
                    "No difference",
                    "opacity fades the WHOLE element including text; alpha fades only that colour",
                    "alpha is faster",
                    "opacity only works on images",
                ],
                "answer": 1,
                "explain": "Whole-element fade vs per-colour fade — the reason text stays readable with alpha backgrounds.",
            },
            {
                "type": "mc",
                "question": "color-mix(in srgb, var(--brand) 15%, white) gives you:",
                "options": [
                    "A 15% white tint of the brand colour",
                    "The brand colour at 15% opacity",
                    "A brand colour 15% darker",
                    "An error",
                ],
                "answer": 0,
                "explain": "15% brand + 85% white — a generated tint that updates when --brand changes.",
            },
        ],
    },

    # ------------------------------------------------------------------ cs06
    {
        "id": "cs06",
        "title": "Box Model",
        "emoji": "📦",
        "lessons": [
            {
                "title": "The Box Model",
                "html": """
<p>Every element on the page — text, image, button — renders as a
<b>box</b>, and CSS layout is the art of stacking and nesting boxes.
Every box has the same four layers, from inside out. Memorise the
diagram once and devtools will never confuse you again:</p>

<pre class="code">┌─────────────── margin ────────────────┐
│  ┌──────────── border ─────────────┐  │
│  │  ┌───────── padding ─────────┐  │  │
│  │  │  ┌────── content ──────┐  │  │  │
│  │  │  │  width × height     │  │  │  │
│  │  │  └─────────────────────┘  │  │  │
│  │  └───────────────────────────┘  │  │
│  └─────────────────────────────────┘  │
└───────────────────────────────────────┘</pre>

<ul>
<li><b>Content</b> — the stuff itself (text, image), sized by
<code>width</code>/<code>height</code></li>
<li><b>Padding</b> — breathing room <b>inside</b>, between content and
border. Shows the element's background</li>
<li><b>Border</b> — the frame: <code>border: 2px solid #1572b6</code>
(width, style, colour — style is required)</li>
<li><b>Margin</b> — space <b>outside</b>, pushing neighbours away.
Always transparent</li>
</ul>

<p>The key paint rule: background colour fills the content <i>and</i>
the padding, but never the margin — that's why padding "looks part of"
a button while margin looks like nothing at all. Open devtools, hover
any element, and the browser literally draws these four layers in
different colours. Now see them in code:</p>

<pre class="code">.card {
  padding: 16px;
  border: 2px solid #1572b6;
  border-radius: 10px;      /* rounds the border+padding box */
  margin: 12px 0;           /* top/bottom 12, left/right 0 */
}</pre>

<p>Predict the render: a 16px cushion painted with the background,
inside a 2px rounded frame, with 12px of clear air above and below the
neighbouring cards. Padding and margin each accept 1–4 values (top
right bottom left, or pairs — <code>12px 0</code> means "12 top/bottom,
0 sides"), and per-side properties
(<code>padding-top</code>, <code>margin-left</code>...) exist for
asymmetric cases.</p>

<p>One famous quirk to meet early: <b>vertical margins collapse</b> —
adjacent siblings' top/bottom margins merge into the larger of the
two, rather than adding. A 20px bottom margin over a 30px top margin
yields a 30px gap, not 50. Horizontal margins never collapse.</p>
""",
                "tryit": """<!DOCTYPE html>
<html lang="en">
<head><title>The box model</title>
<style>
  body { font-family: sans-serif; }
  .box {
    width: 220px;
    padding: 16px;
    border: 4px solid #1572b6;
    margin: 20px;
    background: #eaf4fd;
  }
  .sides { margin: 8px 40px; border-color: #c73c1a; }
</style>
</head>
<body>
  <div class="box">padding 16, border 4, margin 20 — the browser
    devtools draws exactly these four layers for me.</div>
  <div class="box sides">Asymmetric: margin 8px 40px (top/bottom vs
    left/right).</div>
</body>
</html>
""",
            },
            {
                "title": "box-sizing",
                "html": """
<p>Here's the trap that bites every beginner in week one. You set
<code>width: 200px</code> — and the element renders 250px wide. By
default (<code>box-sizing: content-box</code>), <code>width</code> sizes
the <b>content only</b> — padding and border are <b>added on top</b>:</p>

<pre class="code">.box { width: 200px; padding: 20px; border: 5px solid; }
/* content-box: the real box is 200 + 40 + 10 = 250px wide! */</pre>

<p>Do the arithmetic the way the browser does: 200px content + 20px
padding on each of 2 sides + 5px border on each of 2 sides = 250px.
Now place two <code>width: 50%</code> boxes with padding side by side —
each overflows its container and your "50/50 layout" breaks. The cure
is the first line of virtually every stylesheet ever written:</p>

<pre class="code">*, *::before, *::after {
  box-sizing: border-box;
}</pre>

<p>The universal selector hits every element and pseudo-element, and
<code>border-box</code> changes what <code>width</code> <i>means</i>:
the whole box — padding and border squeezed <i>inside</i> it.
<code>width: 200px</code> is truly 200px wide, whatever you put inside.
Arithmetic stops being a puzzle:</p>

<pre class="code">.half { width: 50%; padding: 16px; }   /* actually half! */</pre>

<p>Predict the Try-it: inside the dashed container, the content-box div
pokes outside the border while the border-box div fits exactly — then
change both to border-box in the CSS and watch the overflow
disappear. That demonstration is why practically every modern codebase
ships the universal rule; MDN's guidance agrees border-box is the sane
mental model.</p>

<p>Gotcha: it becomes even more relevant with layout systems — grid
columns and flex items carrying padding just fit, no surprises, because
<code>width: 100%</code> plus padding finally adds up to 100%.</p>
""",
                "tryit": """<!DOCTYPE html>
<html lang="en">
<head><title>box-sizing</title>
<style>
  body { font-family: sans-serif; }
  .container { max-width: 340px; border: 2px dashed #999; padding: 4px; }
  .content-box { box-sizing: content-box; }
  .border-box  { box-sizing: border-box; }
  .half { width: 50%; padding: 16px; border: 4px solid #1572b6;
          background: #eaf4fd; display: inline-block; }
</style>
</head>
<body>
  <div class="container">
    <div class="half content-box">content-box: 50% + padding + border
      = OVERFLOW</div>
    <div class="half border-box">border-box: truly 50%</div>
  </div>
  <p>Change both to border-box in the CSS and watch the overflow
     disappear — that's why the universal rule exists.</p>
</body>
</html>
""",
            },
            {
                "title": "Width & Height Constraints",
                "html": """
<p>Naked <code>width</code>/<code>height</code> are rigid numbers — real
layouts need boundaries that adapt. The constraint quartet gives you a
range instead of a point:</p>

<ul>
<li><code>min-width</code> / <code>min-height</code> — the smallest a box
may shrink</li>
<li><code>max-width</code> / <code>max-height</code> — the largest it may
grow</li>
</ul>

<pre class="code">.page   { max-width: 960px; margin: 0 auto; }   /* centred column */
img     { max-width: 100%; height: auto; }      /* never overflow! */
.dialog { width: 90vw; max-height: 80vh; overflow: auto; }</pre>

<p>Walk each line. The page column grows with the screen until 960px,
then stops — and <code>margin: 0 auto</code> centres it by splitting
the leftover space equally left and right. The image rule is the most
famous in responsive CSS: the image may never exceed its container,
shrinking instead, and <code>height: auto</code> keeps the aspect ratio
while it does. The dialog takes 90% of the viewport width but never
grows past 80% of its height — the rest scrolls inside.</p>

<p>When constraints collide there is a fixed priority:
<code>min-width</code> beats <code>max-width</code> beats
<code>width</code> — a box with <code>width: 100px; max-width: 50px;</code>
renders 50px; the max clamps the declared width. Also meet
<code>aspect-ratio</code>: <code>aspect-ratio: 16 / 9</code> keeps boxes
proportional as they resize — video frames, cards, placeholders.</p>

<p>The centring idiom above — <code>max-width</code> plus
<code>margin: 0 auto</code> — is how every readable content column on
the web is built: grow with the screen, stop at the limit, sit in the
middle. Predict the Try-it: resize the preview and the column stops
growing while the image scales down with it. Gotcha: drop the
<code>height: auto</code> and the image squashes instead of scaling —
the two properties work as a pair.</p>
""",
                "tryit": """<!DOCTYPE html>
<html lang="en">
<head><title>Constraints</title>
<style>
  body { font-family: sans-serif; margin: 0; }
  .page { max-width: 480px; margin: 0 auto; padding: 12px;
          background: #f2f8fe; min-height: 100vh; }
  img { max-width: 100%; height: auto; display: block;
        border-radius: 8px; }
  .card { aspect-ratio: 16 / 9; background: #1572b6; color: white;
          display: grid; place-items: center; margin-top: 10px; }
</style>
</head>
<body>
  <div class="page">
    <p>A centred column: max-width + margin auto. Resize the
       preview — the column stops growing, and the image never
       overflows.</p>
    <img src="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='600' height='200'%3E%3Crect width='600' height='200' fill='%2333a9dc'/%3E%3C/svg%3E"
         alt="wide placeholder">
    <div class="card">aspect-ratio: 16/9</div>
  </div>
</body>
</html>
""",
            },
        ],
        "quiz": [
            {
                "type": "mc",
                "question": "Which layer shows the element's background colour?",
                "options": ["margin", "padding", "margin and padding", "only content"],
                "answer": 1,
                "explain": "Padding sits inside the border and is painted; margin is always transparent.",
            },
            {
                "type": "mc",
                "question": "With box-sizing: content-box, an element with width:200px, padding:20px, border:5px is:",
                "options": ["200px wide", "245px wide", "225px wide", "250px wide"],
                "answer": 3,
                "explain": "content-box adds padding and border on top: 200 + 40 + 10 = 250.",
            },
            {
                "type": "blank",
                "question": "The universal rule every stylesheet ships: * { box-sizing: ____; }",
                "answers": ["border-box"],
                "explain": "border-box makes width include padding+border — sane arithmetic.",
            },
            {
                "type": "mc",
                "question": "width: 100px with max-width: 50px renders:",
                "options": ["100px", "50px — min beats max beats width", "an error", "50%"],
                "answer": 1,
                "explain": "Priority: min-width > max-width > width.",
            },
        ],
    },

    # ------------------------------------------------------------------ cs07
    {
        "id": "cs07",
        "title": "Backgrounds & Borders",
        "emoji": "🖼️",
        "lessons": [
            {
                "title": "Backgrounds",
                "html": """
<p>The <code>background</code> family paints the stage <i>behind</i> the
content — colour, image, size, position, repeat, each controllable
separately. Start from the longhand set and every shorthand becomes
predictable:</p>

<pre class="code">.card {
  background-color: #eaf4fd;
  background-image: url("texture.png");
  background-size: cover;         /* cover | contain | sizes */
  background-position: center;    /* or coords: 20px 30px, 50% 0% */
  background-repeat: no-repeat;   /* repeat | repeat-x | ... */
}</pre>

<p>Read it as a photo-framing problem: place the image at
<code>center</code>, size it to <code>cover</code> the box, and forbid
tiling. The size keywords are the ones to internalise:</p>

<ul>
<li><code>background-size: cover</code> — fill the box, cropping the
overflow (hero images); <code>contain</code> — fit entirely inside
(letterboxing)</li>
<li><code>background-position</code> — which part of the image to show
when it's cropped</li>
<li><code>background-attachment: fixed</code> — the image stays put
while the page scrolls (parallax-lite)</li>
</ul>

<p>And boxes can wear <b>multiple backgrounds</b> — comma-separated,
first on top:</p>

<pre class="code">.hero {
  background-image:
    linear-gradient(rgba(0, 0, 0, 0.55), rgba(0, 0, 0, 0.55)),
    url("city.jpg");
  background-size: cover;
  background-position: center;
}</pre>

<p>Layer order matters: the dark, half-transparent gradient sits
<i>above</i> the photo, dimming it evenly. That's the standard
text-readability overlay — white text on any image, always legible, no
photo editing. Predict the Try-it: a dimmed hero with crisp white
text, and below it a dot pattern — one small radial-gradient tile
repeated every 18px by <code>background-size</code>. Tiling a tiny
generated image like that is how patterns get made without any image
file at all.</p>

<p>Gotcha: the <code>background:</code> shorthand packs everything but
<b>resets unspecified parts</b> to defaults — writing
<code>background: url(x.png)</code> after a <code>background-color</code>
wipes the colour out. When composing layers, prefer the longhands —
each longhand sets only the one property you name, so your other
layers survive.</p>
""",
                "tryit": """<!DOCTYPE html>
<html lang="en">
<head><title>Backgrounds</title>
<style>
  body { font-family: sans-serif; margin: 0; }
  .hero {
    height: 180px;
    display: grid;
    place-items: center;
    color: white;
    font-size: 1.4rem;
    text-align: center;
    background-image:
      linear-gradient(rgba(21, 62, 100, 0.7), rgba(21, 62, 100, 0.7)),
      url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='300' height='180'%3E%3Crect width='300' height='180' fill='%23f5a623'/%3E%3Ccircle cx='70' cy='60' r='30' fill='%23ffd43b'/%3E%3Crect x='150' y='70' width='110' height='70' fill='%23c73c1a'/%3E%3C/svg%3E");
    background-size: cover;
    background-position: center;
  }
  .dots {
    height: 80px;
    background-image: radial-gradient(#33a9dc 20%, transparent 25%);
    background-size: 18px 18px;
  }
</style>
</head>
<body>
  <div class="hero">Readable text on any image — gradient overlay</div>
  <div class="dots"></div>
</body>
</html>
""",
            },
            {
                "title": "Borders, Radius & Shadows",
                "html": """
<p>Three properties turn flat boxes into UI: <b>borders</b> give
structure, <b>radius</b> gives friendliness, <b>shadows</b> give depth.
Borders are one line of CSS with three parts — width, style, colour
(style is mandatory; <code>solid</code>, <code>dashed</code>,
<code>dotted</code>, <code>double</code>...):</p>

<pre class="code">.box {
  border: 2px solid #1572b6;          /* all sides */
  border-left: 6px solid #c73c1a;     /* one side — accent bars! */
}</pre>

<p>Omit the style and nothing renders — <code>border: 2px blue</code> is
invalid without a style keyword. The per-side form is the callout
pattern: a thick <code>border-left</code> instantly reads as
"note / warning / quote". <b>Border radius</b> rounds corners — from
subtle (<code>4px</code>) to pill (<code>999px</code>) to circle
(<code>50%</code> on a square). Per-corner control exists
(<code>border-top-left-radius</code>), and larger values create organic
blob shapes.</p>

<p><b>Shadows</b> — two kinds, each taking a comma list:</p>

<pre class="code">.card {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  /* x-offset, y-offset, blur, spread, colour */
}
.text-shadow { text-shadow: 1px 1px 2px rgba(0,0,0,0.4); }</pre>

<p>Read the box-shadow numbers: no horizontal shift, 4px downward, 12px
of blur, low alpha. Positive y-offset + blur + low alpha = believable
elevation — soft, offset, quiet. Predict the render: the card looks
slightly lifted off the page; the pill reads as a button.</p>

<p>Layered shadows look even more <i>real</i> — that's the
material-design recipe:</p>

<pre class="code">box-shadow:
  0 1px 2px rgba(0, 0, 0, 0.08),
  0 8px 24px rgba(0, 0, 0, 0.12);</pre>

<p>A tight dark shadow hugs the edges; a wide soft one suggests ambient
light — your eye reads the pair as genuine depth. Together the trio
defines modern UI: radius says friendly, borders say structure,
shadows say depth — and all three are painted by the box model you
already know. Gotcha: shadows don't affect layout — a big shadow
overlaps neighbours freely, so give elements carrying them margin to
breathe.</p>
""",
                "tryit": """<!DOCTYPE html>
<html lang="en">
<head><title>Borders & shadows</title>
<style>
  body { font-family: sans-serif; background: #f6f9fc; padding: 16px; }
  .card {
    max-width: 300px; padding: 14px; border-radius: 12px;
    background: white;
    border: 1px solid #e3ecf4;
    box-shadow: 0 1px 2px rgba(0,0,0,0.08), 0 8px 24px rgba(0,0,0,0.12);
  }
  .accent { border-left: 6px solid #1572b6; margin-top: 12px; }
  .pill { display: inline-block; padding: 4px 14px; border-radius: 999px;
          background: #1572b6; color: white; font-size: 13px; }
</style>
</head>
<body>
  <span class="pill">border-radius: 999px</span>
  <div class="card">
    <strong>Layered shadow card</strong>
    <p>Tight dark shadow + wide soft shadow = believable depth.</p>
  </div>
  <div class="card accent">An accent border-left — the callout pattern.</div>
</body>
</html>
""",
            },
        ],
        "quiz": [
            {
                "type": "mc",
                "question": "background-size: cover does what?",
                "options": [
                    "Fits the whole image inside the box",
                    "Fills the box, cropping the overflow",
                    "Tiles the image",
                    "Stretches it flat",
                ],
                "answer": 1,
                "explain": "cover fills and crops; contain fits whole with possible empty space.",
            },
            {
                "type": "blank",
                "question": "Rounded corners come from the <code>border-____</code> property.",
                "answers": ["radius"],
                "explain": "border-radius rounds corners — 999px makes pills, 50% makes circles.",
            },
            {
                "type": "mc",
                "question": "The standard readable-text-over-photo technique is:",
                "options": [
                    "A dark transparent gradient layered over the image background",
                    "text-shadow only",
                    "A solid black background",
                    "opacity: 0.5 on the text",
                ],
                "answer": 0,
                "explain": "Multiple backgrounds: gradient first (on top), image below.",
            },
            {
                "type": "mc",
                "question": "A believable card elevation usually uses:",
                "options": [
                    "One huge dark shadow",
                    "A small offset with low alpha, often layered",
                    "border: 10px solid black",
                    "No shadow",
                ],
                "answer": 1,
                "explain": "Subtle layered shadows read as real depth; heavy single shadows look pasted.",
            },
        ],
    },

    # ------------------------------------------------------------------ cs08
    {
        "id": "cs08",
        "title": "Text & Fonts",
        "emoji": "✒️",
        "lessons": [
            {
                "title": "Font Properties",
                "html": """
<p>Typography is 80% of visual design — get these five properties right
and most of the battle is won. The canonical body-text block:</p>

<pre class="code">.page {
  font-family: "Segoe UI", Roboto, Arial, sans-serif;
  font-size: 1rem;          /* 16px baseline */
  font-weight: 400;         /* 100–900, or normal/bold */
  font-style: normal;       /* or italic */
  line-height: 1.6;         /* unitless = multiplier — the good way */
}</pre>

<p>Walk it line by line:</p>

<ul>
<li><b>font-family</b> — a fallback <b>list</b>: the browser walks it and
uses the first installed font, ending in a generic family
(<code>sans-serif</code>, <code>serif</code>,
<code>monospace</code>) as the safety net. Always end with one.</li>
<li><b>font-size</b> — in <code>rem</code> so user preferences work</li>
<li><b>font-weight</b> — 400 is normal, 700 is bold; variable fonts
expose everything between</li>
<li><b>line-height</b> — unitless is the convention: <code>1.6</code>
means 1.6× the font-size, and children compute correctly (a fixed
<code>24px</code> would not adapt)</li>
</ul>

<p>That last bullet hides the classic gotcha, so make it concrete. Set
<code>line-height: 24px</code> on the body, and a child with
<code>font-size: 32px</code> still gets 24px lines — its text
overlaps. Set <code>1.6</code> and the child inherits the
<i>ratio</i>, computing about 51px for its own bigger font.
Multipliers travel down the tree; pixel heights don't.</p>

<p>Web conventions worth borrowing: body text 16–18px with
line-height 1.5–1.7; headings distinct by <b>size and weight</b>, not
colour alone; measure (line length) capped around 60–75ch for
readability. The shorthand <code>font:</code> exists but is finicky —
it also resets several properties — longhands are clearer. Predict the
Try-it: a serif page with comfortable 1.7 rhythm, and a UI card inside
it running a sans stack at weight 300 — two typographic voices, one
page.</p>
""",
                "tryit": """<!DOCTYPE html>
<html lang="en">
<head><title>Font properties</title>
<style>
  body { font-family: Georgia, 'Times New Roman', serif; }
  .ui {
    font-family: "Segoe UI", system-ui, sans-serif;
    background: #f2f8fe; padding: 12px; border-radius: 8px;
  }
  h1 { font-weight: 800; font-size: 1.8rem; color: #1572b6; }
  p  { line-height: 1.7; max-width: 60ch; }
  .light { font-weight: 300; }
</style>
</head>
<body>
  <h1>Serif headline</h1>
  <p>This page's body uses Georgia with line-height 1.7 — comfortable
     reading measure and rhythm.</p>
  <div class="ui">
    <p class="light">And this card uses a sans-serif UI stack
       (weight 300).</p>
    <p><strong>Bold is just weight 700.</strong></p>
  </div>
</body>
</html>
""",
            },
            {
                "title": "Spacing, Alignment & Decoration",
                "html": """
<p>Where font properties choose the typeface, these properties shape,
place, and dress the words themselves:</p>

<pre class="code">h1 {
  text-align: center;          /* left | right | justify */
  letter-spacing: 0.5px;       /* tracking — headers love a touch */
  word-spacing: 2px;
  text-transform: uppercase;   /* capitalize | lowercase | none */
  text-decoration: none;       /* underline | line-through | overline */
  text-shadow: 0 1px 2px rgba(0,0,0,0.3);
}</pre>

<p>Six declarations, six jobs: centre the heading, add air between the
letters, loosen the words, force uppercase display, strip decoration,
cast a faint shadow. The ones with real depth:</p>

<ul>
<li><b>letter-spacing</b> — all-caps headings breathe with
<code>+0.5px</code> to <code>+2px</code>; body text usually shouldn't be
touched</li>
<li><b>text-transform</b> — change the LOOK without changing the text:
markup stays "Sign up", the button reads "SIGN UP" (screen readers
still say "sign up")</li>
<li><b>text-decoration</b> — the default link underline lives here;
<code>none</code> removes it (keep underlines for text-in-paragraph
links — a11y)</li>
<li><b>text-shadow</b> — subtle depth for headings over images</li>
</ul>

<p>The text-transform bullet is worth dwelling on, because it's a
separation-of-concerns lesson: the <i>content</i> keeps its natural
casing in the HTML, so copy-paste, search engines and screen readers
all keep it — only the paint changes. Decoration can be styled further:
<code>text-decoration: underline dotted #33a9dc</code> picks both line
style and colour (see the Try-it's dotted link).</p>

<p>One modern star for alignment: <code>text-wrap: balance</code>
(balances multi-line headings so no lonely word rides the last line) —
and for long-form readability, remember the measure trick from Values:
<code>max-width: 65ch</code>. Gotcha: uppercase text is wider — a
button that fits in sentence case can overflow in uppercase; test
both.</p>
""",
                "tryit": """<!DOCTYPE html>
<html lang="en">
<head><title>Text shaping</title>
<style>
  body { font-family: sans-serif; padding: 12px; }
  h1 {
    text-transform: uppercase;
    letter-spacing: 2px;
    text-align: center;
    color: #1572b6;
  }
  .strike { text-decoration: line-through; color: #999; }
  a { text-decoration: underline dotted #33a9dc; }
  .shadow { font-size: 1.6rem; font-weight: bold;
            text-shadow: 2px 2px 3px rgba(0,0,0,0.25); }
</style>
</head>
<body>
  <h1>shaped by css</h1>
  <p class="strike">This was struck through, not deleted.</p>
  <p>Links can wear dotted underlines: <a href="#">a dotted link</a>.</p>
  <p class="shadow">Text shadow without mercy.</p>
</body>
</html>
""",
            },
            {
                "title": "Web Fonts & @font-face",
                "html": """
<p>System fonts are safe but samey — every site wears Arial. <b>Web
fonts</b> ship the actual font file with your page, and CSS loads it
with one at-rule:</p>

<pre class="code">@font-face {
  font-family: "MyFont";
  src: url("myfont.woff2") format("woff2");
  font-weight: 400;
  font-style: normal;
  font-display: swap;
}

body { font-family: "MyFont", sans-serif; }</pre>

<p>Read it as: "when text asks for the family MyFont at weight 400,
serve this file". The name inside @font-face is a <i>label you
invent</i>; the rule below is what uses it. Three details matter:</p>

<ul>
<li><b>woff2</b> is the modern format — small and supported
everywhere</li>
<li><b>font-weight/font-style in the face</b> — you declare one
<i>file per variant</i>; four weights means four @font-face blocks
sharing the same family name</li>
<li><b><code>font-display: swap</code></b> — show the fallback font
immediately, swap in the web font when loaded (no invisible-text
waiting)</li>
</ul>

<p>The practical route is Google Fonts (or any host): pick a family,
copy the provided <code>&lt;link&gt;</code> tags into the head — the
@font-face plumbing is generated for you:</p>

<pre class="code">&lt;link rel="preconnect" href="https://fonts.googleapis.com"&gt;
&lt;link rel="preconnect" href="https://fonts.gstatic.com" crossorigin&gt;
&lt;link href="https://fonts.googleapis.com/css2?family=Vazirmatn:wght@400;700&amp;display=swap"
      rel="stylesheet"&gt;</pre>

<p>The two <code>preconnect</code> links warm up the connection so the
font starts downloading sooner; the third fetches a stylesheet that
declares the @font-face rules for Vazirmatn's weights 400 and 700.
(That's exactly how this app loads Vazirmatn for the Persian
interface.) Two disciplines: load only the weights you use (each is a
download users pay for), and keep a solid fallback list — the site must
remain usable while fonts travel.</p>

<p>Gotcha: asking for <code>font-weight: 700</code> with only a 400 file
loaded triggers <i>faux bold</i> — the browser smears the glyphs
itself. Declare the real 700 face instead.</p>
""",
                "tryit": """<!DOCTYPE html>
<html lang="en">
<head><title>Web fonts</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Josefin+Sans:wght@400;700&display=swap" rel="stylesheet">
<style>
  body { font-family: sans-serif; }
  .webfont { font-family: "Josefin Sans", sans-serif;
             font-size: 1.4rem; color: #1572b6; }
</style>
</head>
<body>
  <p class="webfont">If the network is available, this heading wears
     Josefin Sans — loaded from Google Fonts.</p>
  <p>Offline or blocked? The fallback sans-serif takes over gracefully —
     that's the font stack working as designed.</p>
</body>
</html>
""",
            },
        ],
        "quiz": [
            {
                "type": "mc",
                "question": "Why end font-family lists with a generic (sans-serif)?",
                "options": [
                    "Required by validation",
                    "It's the fallback if no listed font is installed",
                    "It makes text load faster",
                    "It sets the font size",
                ],
                "answer": 1,
                "explain": "The browser walks the list; the generic guarantees something reasonable renders.",
            },
            {
                "type": "blank",
                "question": "Unitless line-height (e.g. 1.6) is preferred because children inherit the ____ not the computed size.",
                "answers": ["multiplier", "ratio", "factor"],
                "explain": "Fixed px line-height breaks when child elements have different font sizes.",
            },
            {
                "type": "mc",
                "question": "text-transform: uppercase changes:",
                "options": [
                    "The actual text in the markup",
                    "Only how it renders — the markup text is unchanged",
                    "The font file",
                    "Nothing on screen readers",
                ],
                "answer": 1,
                "explain": "Presentation-only: screen readers still read the original casing/words.",
            },
            {
                "type": "mc",
                "question": "font-display: swap means:",
                "options": [
                    "Show the fallback immediately, swap when the web font loads",
                    "Swap fonts on hover",
                    "Never load web fonts",
                    "Load fonts last",
                ],
                "answer": 0,
                "explain": "Avoids invisible text while the font downloads.",
            },
        ],
    },
]
