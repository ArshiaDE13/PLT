"""CSS Tutor chapters 9-30 (Phases 4-9), grounded in MDN Web Docs."""

CHAPTERS_CSS_C = [
    # ------------------------------------------------------------------ cs09
    {
        "id": "cs09",
        "title": "Display & Normal Flow",
        "emoji": "🧱",
        "lessons": [
            {
                "title": "display & Normal Flow",
                "html": """
<p>Without any CSS at all, a page already lays itself out — headings on
their own lines, paragraphs stacked below, links flowing inside
sentences. That default arrangement is <b>normal flow</b>, and
<code>display</code> is the property that changes what kind of box each
element generates. It is the first property to reach for whenever a
layout question appears.</p>

<p>The two ancestors of everything:</p>

<ul>
<li><code>display: block</code> — a box that takes the <b>full width
available</b> and stacks vertically: headings, paragraphs, divs</li>
<li><code>display: inline</code> — a box that flows <b>inside text</b>,
like a word in a sentence: spans, links, strong. Width/height don't
apply; margins only work horizontally</li>
</ul>

<p>Why care? Because most "why is this element behaving strangely"
questions in week one are really "what kind of box is this?" A link
refuses a width — it's inline. A div won't sit beside another div —
both are block. Name the box type and the behaviour stops being
mysterious. Everything else is a variation on the theme:
<code>flex</code> and <code>grid</code> are whole layout systems (later
chapters), <code>none</code> removes the box entirely — no space is
kept, screen readers skip it too — and further values like
<code>list-item</code> and <code>table</code> serve special cases. The
flow underneath never leaves: block-in-flow, inline-in-text, on every
page ever made.</p>

<p>Compare the sibling property: <code>visibility: hidden</code> hides
the element but <i>keeps its space</i> in the layout, while
<code>display: none</code> erases it completely. Choose by whether the
gap should remain.</p>

<p>Gotcha: <code>display</code> overrides the browser's built-in choice
for a tag — set an <code>li</code> to inline and it loses its bullet;
set a <code>div</code> to inline and it behaves like a span. The markup
suggests a default; display has the final word. Predict the Try-it: the
two blue blocks stack, the yellow inline boxes share one line (their
padding paints without pushing neighbours), and the "hidden" paragraph
is gone without leaving a hole.</p>
""",
                "tryit": """<!DOCTYPE html>
<html lang="en">
<head><title>display</title>
<style>
  body { font-family: sans-serif; }
  .block-demo { display: block; background: #eaf4fd;
                padding: 6px; margin: 6px 0; }
  .inline-demo { display: inline; background: #ffd43b; padding: 2px; }
  .hidden { display: none; }
</style>
</head>
<body>
  <div class="block-demo">block: full width, stacks</div>
  <div class="block-demo">block: next one below</div>

  <p>Text with <span class="inline-demo">an inline box</span> flowing
     inside the line, and
     <span class="inline-demo">another one</span> next to it.</p>

  <p class="hidden">display: none — I'm not here at all (no space kept).</p>
  <p>Everything above this line is normal flow + display.</p>
</body>
</html>
""",
            },
            {
                "title": "Block, Inline & Inline-block",
                "html": """
<p>The three everyday box behaviours, compared precisely — internalise
this trio and a decade of beginner confusion evaporates:</p>

<ul>
<li><b>block</b> — full width by default, stacks, respects all
box-model properties (width, height, all margins)</li>
<li><b>inline</b> — sits in the text line, sizes to content,
<strong>ignores width/height</strong>, vertical margins and vertical
padding behave oddly (they paint over the neighbouring lines rather
than pushing them apart)</li>
<li><b>inline-block</b> — the hybrid: flows in the text line like
inline, but accepts width/height and the full box model like block</li>
</ul>

<p>See the hybrid at work. The chip declares <code>inline-block</code>:
it continues the line after the previous word like inline, yet its
padding is real space that moves surrounding content — and it would
honour an explicit width just the same. That combination is exactly
what a tag, badge, or button-in-a-row needs:</p>

<pre class="code">.chip {
  display: inline-block;    /* sits inline BUT can be sized */
  padding: 4px 12px;
  width: auto;              /* or a fixed width — your choice */
}</pre>

<p>inline-block is the classic answer for "sized things that sit next
to each other": chips, badges, buttons-in-a-row. The modern toolkit
often replaces it with flexbox (a row of flex items is easier to
align), but inline-block remains everywhere in the wild — and it's the
honest way to understand what display really does: it's not about
looks, it's about <i>which box rules apply</i>. Predict the Try-it: the
first two blue boxes stack (block, width honoured); the yellow inline
span's <code>width: 200px</code> is ignored — it hugs its text; the two
green inline-blocks are 160px wide <i>and</i> share a line.</p>

<p>Gotcha: the line breaks or spaces between inline-block elements in
the HTML render as a visible gap — about one space wide — between the
boxes, and it has defeated many pixel-perfect layouts. Remove the
whitespace in the markup (or comment it out), or hand the row to
flexbox and <code>gap</code>.</p>
""",
                "tryit": """<!DOCTYPE html>
<html lang="en">
<head><title>Three box types</title>
<style>
  body { font-family: sans-serif; line-height: 2.2; }
  .blk  { display: block; width: 200px; background: #1572b6;
          color: white; padding: 6px; margin: 4px 0; text-align: center; }
  .inl  { display: inline; width: 200px; background: #ffd43b;
          padding: 6px; }  /* width ignored! */
  .inlb { display: inline-block; width: 160px; background: #2e8b57;
          color: white; padding: 6px; text-align: center; }
</style>
</head>
<body>
  <span class="blk">block (width works)</span>
  <span class="blk">block stacks below</span>

  <p>inline: <span class="inl">width:200px IGNORED</span> flows with text.</p>

  <p>inline-block: <span class="inlb">160px, still inline</span>
     <span class="inlb">next to it</span></p>
</body>
</html>
""",
            },
            {
                "title": "Overflow",
                "html": """
<p>Content doesn't always fit its box: a fixed-height panel, a long
URL, a code line too wide for its column. Left alone, overflowing
content simply spills out and paints over whatever sits below — the
default value is literally <code>visible</code>. <code>overflow</code>
decides what happens instead, for the whole box or per axis:</p>

<pre class="code">.panel {
  height: 120px;
  overflow: auto;    /* visible | hidden | scroll | auto | clip */
}</pre>

<p>Walk it: the panel is 120px tall no matter how much text sits
inside, and <code>auto</code> means the browser adds a scrollbar only
when the content actually exceeds that height. The five values in
full:</p>

<ul>
<li><b>visible</b> (default) — spills out, drawn over whatever's there</li>
<li><b>hidden</b> — clipped at the edge, unreachable</li>
<li><b>scroll</b> — scrollbars always present, even when content fits</li>
<li><b>auto</b> — scrollbars only when needed (the everyday choice)</li>
<li><b>clip</b> — like hidden but unscrollable even programmatically;
harder edge, better for pure clipping</li>
</ul>

<p>Per-axis controls: <code>overflow-x</code> /
<code>overflow-y</code>. The most useful everyday pattern is
<code>overflow-x: auto</code> on code blocks and wide tables: long
lines scroll sideways while the page's vertical rhythm stays intact.
(Technical footnote: mixing <code>visible</code> with a scrolling axis
isn't allowed — the visible axis computes to auto.)</p>

<p>Two consequences worth knowing: any overflow value other than
visible makes the element a <b>containing block</b> for
absolutely-positioned children and a scroll container — which is why
adding overflow sometimes "fixes" or "breaks" a layout mysteriously
(that dropdown clipped, that sticky header unstuck). And sticky
headers need an ancestor WITHOUT overflow to stick against the page
(Positioning chapter). Predict the Try-it: the first panel scrolls
vertically, the second simply amputates its excess text, and the long
code line scrolls sideways instead of breaking the page.</p>
""",
                "tryit": """<!DOCTYPE html>
<html lang="en">
<head><title>overflow</title>
<style>
  body { font-family: sans-serif; }
  .panel {
    height: 100px; width: 260px; padding: 8px;
    border: 2px solid #1572b6; border-radius: 8px;
    margin-bottom: 10px;
  }
  .auto   { overflow: auto; }
  .hidden { overflow: hidden; }
  .code { overflow-x: auto; white-space: nowrap; background: #f2f8fe; }
</style>
</head>
<body>
  <div class="panel auto">overflow: auto — scroll me! I contain far more
    text than fits in 100px of height, so the scrollbar appears and my
    content remains reachable.</div>
  <div class="panel hidden">overflow: hidden — the rest of me is simply
    clipped away, unreachable.</div>
  <div class="panel code">.code-sample { overflow-x: auto; } — long code lines
    scroll sideways instead of breaking the page.</div>
</body>
</html>
""",
            },
        ],
        "quiz": [
            {
                "type": "mc",
                "question": "Which display value respects width AND sits in the text line?",
                "options": ["inline", "block", "inline-block", "none"],
                "answer": 2,
                "explain": "inline-block = inline flow + full box model (width/height apply).",
            },
            {
                "type": "mc",
                "question": "The everyday overflow choice — scrollbars only when needed:",
                "options": ["scroll", "hidden", "auto", "clip"],
                "answer": 2,
                "explain": "auto adds scrollbars only when content actually overflows.",
            },
            {
                "type": "blank",
                "question": "display: ____ removes an element entirely, leaving no space.",
                "answers": ["none"],
                "explain": "display:none unrenders it; visibility:hidden keeps the space.",
            },
        ],
    },

    # ------------------------------------------------------------------ cs10
    {
        "id": "cs10",
        "title": "Positioning",
        "emoji": "📌",
        "lessons": [
            {
                "title": "Positioning Schemes",
                "html": """
<p>Normal flow is a great default, but some elements need to escape it:
a badge hanging off a card's corner, a cookie banner pinned to the
viewport, a table header that stays visible while you scroll.
<code>position</code> takes an element out of the flow's rules — fully
or partly — and hands you coordinates. Five schemes:</p>

<ul>
<li><b>static</b> — default; flow as usual, offsets ignored</li>
<li><b>relative</b> — flow unchanged (neighbours never move), but
offsets (<code>top/right/bottom/left</code>) <b>nudge it from where it
would have been</b>; also becomes the reference for absolute
children</li>
<li><b>absolute</b> — removed from flow entirely, positioned against
its nearest <b>positioned ancestor</b> (or the page)</li>
<li><b>fixed</b> — removed from flow, pinned to the <b>viewport</b>;
stays put while scrolling (banners, floating buttons)</li>
<li><b>sticky</b> — flows normally until a scroll threshold, then
sticks (table headers, section labels)</li>
</ul>

<pre class="code">.badge {
  position: absolute;
  top: -8px; right: -8px;      /* against the nearest positioned ancestor */
}
.parent { position: relative; } /* THAT's why parents get relative */

.toast {
  position: fixed;
  bottom: 16px; right: 16px;
}
thead th { position: sticky; top: 0; }</pre>

<p>Walk the block: the badge is pulled 8px beyond the parent's top-right
corner — negative offsets are legal and love the corner-hanging look.
The parent declares relative <i>solely</i> so the badge measures from
it. The toast sits 16px from the viewport's bottom-right and stays
there through any amount of scrolling. The table header sticks to the
top edge only once its row reaches it. The absolute pattern to
memorise once: <b>parent relative, child absolute</b> — the child's
offsets then measure from the parent's box. Absolute without a
positioned ancestor flies to the page corner and confuses everyone;
the parent-relative move is always the fix.</p>

<p>Predict the Try-it: scroll the preview — the sticky bar rides the
top, the fixed button hugs the corner, and the red badge hangs off the
card because the card itself is relative. Gotcha: a relative element
<i>keeps its original space</i> in the flow — the nudge leaves a hole
where the element would have been; if you want it truly gone, that's
absolute's job.</p>
""",
                "tryit": """<!DOCTYPE html>
<html lang="en">
<head><title>Positioning</title>
<style>
  body { font-family: sans-serif; margin: 0; height: 160vh; }
  .card { position: relative; border: 2px solid #1572b6; border-radius: 8px;
          padding: 14px; max-width: 320px; margin: 40px auto; }
  .badge { position: absolute; top: -12px; right: -12px;
           background: #c0392b; color: white; padding: 4px 10px;
           border-radius: 999px; font-size: 12px; }
  .nudged { position: relative; top: 4px; left: 12px;
            background: #ffd43b; display: inline-block; }
  .sticky { position: sticky; top: 0; background: #1572b6; color: white;
            padding: 8px; text-align: center; }
</style>
</head>
<body>
  <div class="sticky">position: sticky — scroll down, I stick to the top!</div>
  <p>Scroll down to see sticky and fixed in action.</p>
  <div class="card">
    <span class="badge">absolute</span>
    <p>parent relative + child absolute — the badge hangs off the card.</p>
    <p>A <span class="nudged">relatively nudged</span> span.</p>
  </div>
  <button style="position: fixed; bottom: 12px; right: 12px;
                 padding: 8px 14px; border-radius: 999px; border: none;
                 background: #1572b6; color: white">fixed ↑</button>
</body>
</html>
""",
            },
            {
                "title": "z-index & Stacking Contexts",
                "html": """
<p>When positioned elements overlap, <code>z-index</code> decides who's
on top — higher wins, negative goes below. But its power comes wrapped
in the web's most-misunderstood rule: z-index only competes <b>within
the same stacking context</b>. Learn this once and the dreaded "why is
my modal underneath?" bug dies forever.</p>

<pre class="code">.modal { z-index: 100; }
.toast { z-index: 50; }      /* fine — siblings in the same context */</pre>

<p>These two are siblings, so their numbers compare directly: 100
paints over 50. The values don't have to be huge — 1, 2, 3 is enough —
but teams often leave headroom (10, 20, 30...) so a new layer can slot
in between existing ones later.</p>

<p>A <b>stacking context</b> is created by (among others): the root
element, positioned elements with z-index ≠ auto, elements with
opacity &lt; 1, transforms, filters... Once an element creates a
context, its descendants' z-index values are <b>trapped inside it</b> —
z-index: 9999 on a child of a z-index: 1 parent can never rise above a
sibling of that parent with z-index: 2. The whole subtree is flattened
into one layer at the parent's level before any outside comparison
happens.</p>

<p>The classic bug: "my z-index: 9999 dropdown is UNDER the card!" —
because the card has <code>opacity: 0.99</code> or a transform, making
its whole subtree one sealed context. The fix is never a bigger number —
it's finding which ancestor seals the stack and adjusting there.</p>

<p>Debugging recipe: in devtools, walk up from the element looking for
the context creators (opacity, transform, filter, position+z-index),
then set the z-index at that level. MDN's "stacking context" guide has
the complete creator list. Predict the Try-it: the three boxes
overlap in order 1 &lt; 2 &lt; 3, and the faded paragraph — opacity
below 1 — is its own sealed context: a child with z-index: 9999 inside
it could never climb above the green box. Gotcha: adding
<code>position: relative; z-index: 1</code> to a "harmless" wrapper as
a quick fix silently creates one of these prisons — check the wrappers
first.</p>
""",
                "tryit": """<!DOCTYPE html>
<html lang="en">
<head><title>z-index</title>
<style>
  body { font-family: sans-serif; }
  .wrap { position: relative; }
  .box { position: absolute; width: 120px; height: 90px;
         display: grid; place-items: center; color: white;
         font-weight: bold; border-radius: 8px; }
  .a { top: 10px;  left: 10px;  background: #1572b6; z-index: 1; }
  .b { top: 50px;  left: 70px;  background: #c73c1a; z-index: 2; }
  .c { top: 90px;  left: 130px; background: #2e8b57; z-index: 3; }
  .faded { position: relative; opacity: 0.85; }
</style>
</head>
<body>
  <div class="wrap">
    <div class="box a">z:1</div>
    <div class="box b">z:2</div>
    <div class="box c">z:3</div>
  </div>
  <p>Higher z-index paints on top — but only within the same stacking
     context (the .wrap above).</p>
  <p class="faded">This paragraph has opacity &lt; 1: it creates its OWN
     stacking context. A child with z-index: 9999 could never climb
     above the green box.</p>
</body>
</html>
""",
            },
        ],
        "quiz": [
            {
                "type": "mc",
                "question": "position: fixed positions an element against:",
                "options": ["Its parent", "The viewport", "The nearest heading", "The document only"],
                "answer": 1,
                "explain": "fixed pins to the viewport — it stays put while scrolling.",
            },
            {
                "type": "blank",
                "question": "For absolute children to measure from their parent, the parent needs <code>position: ____</code>.",
                "answers": ["relative"],
                "explain": "parent relative + child absolute — the foundational pattern.",
            },
            {
                "type": "mc",
                "question": "A child with z-index: 9999 is under a sibling of its parent. The likely cause:",
                "options": [
                    "z-index is broken",
                    "An ancestor (with opacity/transform) creates a stacking context that seals it",
                    "The number must be even",
                    "It needs !important",
                ],
                "answer": 1,
                "explain": "z-index only competes within its stacking context — find the sealing ancestor.",
            },
        ],
    },

    # ------------------------------------------------------------------ cs11
    {
        "id": "cs11",
        "title": "Flexbox ⭐",
        "emoji": "🤸",
        "lessons": [
            {
                "title": "Flex Container & the Two Axes",
                "html": """
<p>Flexbox is one-dimensional layout: arrange a row or column of items,
distribute the space between them, align them — the daily driver of
modern UI. It solves the problems the float hacks never could:
equal-height cards in a row, a toolbar whose buttons space themselves,
a footer that stays at the bottom. Flip it on — on the <b>parent</b>,
not the children:</p>

<pre class="code">.toolbar {
  display: flex;      /* children become flex items in a row */
}</pre>

<p>One declaration, and the div's buttons stop stacking as blocks:
they line up on a single row, each sized to its content. From that
moment two invisible <b>axes</b> define everything: the <b>main
axis</b> (the direction items flow) and the <b>cross axis</b>
(perpendicular to it). A horizontal row → the main axis is horizontal;
a column → the main axis is vertical. Every alignment property is
phrased against these axes, so naming them first is half of
understanding flexbox.</p>

<p>The division of labour is clean: the <i>container</i> gets the
layout properties (direction, wrap, gap, justify-content,
align-items); the <i>items</i> get the sizing ones (flex-grow,
flex-shrink, flex-basis, align-self). That's the whole subject — five
container properties, four item properties, one gap — and the next
lessons walk each in turn.</p>

<p>Predict the Try-it: the middle button carries <code>flex: 1</code>,
so it stretches to swallow the leftover width while the arrow buttons
hug their content. Gotcha: <code>display: flex</code> on the parent is
the only setup step — applying flex properties to children while the
parent is still a plain block does nothing, a classic misread of
copied snippets.</p>
""",
                "tryit": """<!DOCTYPE html>
<html lang="en">
<head><title>Flex container</title>
<style>
  body { font-family: sans-serif; }
  .toolbar {
    display: flex;
    gap: 8px;
    background: #eaf4fd;
    padding: 10px;
    border-radius: 8px;
  }
  .toolbar button { padding: 8px 16px; border: 1px solid #33a9dc;
    background: white; border-radius: 6px; }
</style>
</head>
<body>
  <div class="toolbar">
    <button>◀</button>
    <button style="flex:1">I stretch (flex: 1)</button>
    <button>▶</button>
  </div>
  <p>display: flex turned the div into a flex container and its three
     buttons into items on one row.</p>
</body>
</html>
""",
            },
            {
                "title": "flex-direction, wrap & gap",
                "html": """
<p>Three container properties set the geometry: direction points the
flow, wrap decides whether lines may multiply, gap spaces the items.
<b><code>flex-direction</code></b> points the main axis:</p>

<ul>
<li><code>row</code> (default) — items left→right</li>
<li><code>column</code> — items top→bottom</li>
<li><code>row-reverse</code> / <code>column-reverse</code> — flow
backwards (handy for RTL layouts and chat bubbles)</li>
</ul>

<p><b><code>flex-wrap</code></b> — by default items shrink to squeeze
onto one line, compressing below their comfortable width; <code>wrap</code>
lets them flow onto the next line instead (the responsive default for
chip rows and card strips):</p>

<pre class="code">.chips {
  display: flex;
  flex-wrap: wrap;      /* items flow to a second line */
  gap: 8px;
}</pre>

<p>Walk it: the container takes any number of pill chips; when the row
runs out of width, the next chip starts a second line instead of
crushing its siblings, and <code>gap</code> spaces both the columns
and the rows at once.</p>

<p><b><code>gap</code></b> — the space BETWEEN items, replacing the old
margin-hacks where every child needed margin-right except the last.
One value for both axes, or <code>gap: 8px 16px</code> (row-gap
column-gap). It applies to flex, grid, and multi-column alike — and
unlike margins it never adds space after the last item or before the
first, so container padding stays honest.</p>

<p>Note what direction does to alignment vocabulary: in a row,
justify-content works horizontally; in a column, vertically. The axes
rotate — the property names don't. Predict the Try-it: the chips wrap
onto as many lines as needed with even spacing, and below them the
column example stacks three boxes top-to-bottom with gap still
working. Gotcha: without <code>wrap</code>, flex items refuse to break
lines — they instead shrink below their content size (text overlapping,
buttons crushed), because flex-shrink is on by default. If your row
"won't wrap", it's because you never asked it to.</p>
""",
                "tryit": """<!DOCTYPE html>
<html lang="en">
<head><title>direction & wrap</title>
<style>
  body { font-family: sans-serif; }
  .chips { display: flex; flex-wrap: wrap; gap: 8px; margin: 10px 0; }
  .chips span { background: #1572b6; color: white; padding: 6px 14px;
                border-radius: 999px; }
  .column { display: flex; flex-direction: column; gap: 4px;
            max-width: 220px; }
  .column div { background: #eaf4fd; padding: 6px 10px; border-radius: 6px; }
</style>
</head>
<body>
  <div class="chips">
    <span>#css</span><span>#flexbox</span><span>#gap</span>
    <span>#wrap</span><span>#chips</span><span>#flow</span>
  </div>

  <div class="column">
    <div>flex-direction: column</div>
    <div>items stack top→bottom</div>
    <div>gap still spaces them</div>
  </div>
</body>
</html>
""",
            },
            {
                "title": "justify-content & align-items",
                "html": """
<p>The two great alignment properties — one per axis, and between them
they answer most of layout's daily questions: where does the extra
space go, and how do items sit within their line?</p>

<ul>
<li><b><code>justify-content</code></b> — distribute items along the
<b>main axis</b>: <code>flex-start</code> (default), <code>center</code>,
<code>flex-end</code>, <code>space-between</code> (first/last at the
edges, even gaps), <code>space-around</code>,
<code>space-evenly</code></li>
<li><b><code>align-items</code></b> — align items along the
<b>cross axis</b>: <code>stretch</code> (default — items fill the cross
size!), <code>flex-start</code>, <code>center</code>,
<code>flex-end</code>, <code>baseline</code></li>
</ul>

<p>The three <code>space-*</code> values differ subtly:
<code>space-between</code> puts no space at the edges,
<code>space-around</code> gives each item half-width space at the edges
(so edge gaps are half the inner gaps), <code>space-evenly</code> makes
every gap identical. Toolbar with logo left and actions right?
space-between. Evenly spread icon row? space-evenly. The stretch
default on align-items explains why flex children in a row grow to
equal height for free — they're stretching along the cross
axis:</p>

<pre class="code">.center-anything {
  display: flex;
  justify-content: center;   /* main axis */
  align-items: center;       /* cross axis */
  height: 200px;
}</pre>

<p>That three-property snippet is the most famous CSS idiom ever —
perfect centering, both directions, no hacks (the container needs a
size to centre within — that's the height's job). The modern one-liner
is <code>place-items: center</code> on a grid. When a single item needs
a different cross-alignment than its siblings, <code>align-self</code>
overrides per item; and <code>align-content</code> positions the
wrapped <i>lines</i> when the container has multiple rows (only
visible with flex-wrap). Predict the Try-it: the stage spreads its
three dots with space-between and centres them vertically; the blue
box centres its text on both axes at once. Gotcha:
<code>justify-content: center</code> with items wider than the
container clips <i>both</i> ends — and the clipped start becomes
unreachable when you scroll; use margin: auto centering or smaller
items.</p>
""",
                "tryit": """<!DOCTYPE html>
<html lang="en">
<head><title>Alignment</title>
<style>
  body { font-family: sans-serif; }
  .stage { display: flex; justify-content: space-between;
           align-items: center; height: 90px;
           background: #eaf4fd; border-radius: 8px; padding: 0 12px; }
  .dot { width: 44px; height: 44px; border-radius: 50%;
         display: grid; place-items: center;
         color: white; font-weight: bold; }
  .perfect { display: flex; justify-content: center; align-items: center;
             height: 110px; background: #1572b6; color: white;
             border-radius: 8px; margin-top: 10px; }
</style>
</head>
<body>
  <div class="stage">
    <div class="dot" style="background:#1572b6">1</div>
    <div class="dot" style="background:#2e8b57">2</div>
    <div class="dot" style="background:#c73c1a">3</div>
  </div>

  <div class="perfect">perfectly centered — both axes</div>
</body>
</html>
""",
            },
            {
                "title": "Flex Items: grow, shrink & basis",
                "html": """
<p>The container decides the axes; the <code>flex</code> shorthand on
each item decides how the space is shared: <code>flex: grow shrink
basis</code>. Three numbers, three questions:</p>

<ul>
<li><b>flex-grow</b> — when there's <i>extra</i> space, who gets it?
Proportionally to their number: <code>flex: 1</code> on all items =
equal shares; 2 on one, 1 on another = double share</li>
<li><b>flex-shrink</b> — when space is <i>missing</i>, who gives it up?
(default 1; 0 = never shrink)</li>
<li><b>flex-basis</b> — the starting size before growing/shrinking
(<code>auto</code> = the content's natural size)</li>
</ul>

<pre class="code">.side  { flex: 0 0 200px; }     /* fixed 200px, never grows/shrinks */
.main  { flex: 1; }             /* takes ALL remaining space */
.equal { flex: 1; }             /* three of these = thirds */
.grow2 { flex: 2; }             /* twice the share of flex:1 items */</pre>

<p>Walk it: the sidebar declares grow 0, shrink 0, basis 200px — a rail
of exactly 200px that neither yields nor swells; the main content takes
every remaining pixel. Read <code>flex: 2</code> versus
<code>flex: 1</code> as "double the share of the leftover", not "double
the final width" — with a fixed 200px rail subtracted first, the 2:1
ratio applies only to what remains. <code>flex: 1</code> itself is
shorthand for <code>1 1 0%</code> — grow freely, shrink freely, start
from zero so shares are purely proportional; that's why equal flex:1
items come out equal regardless of their content lengths, a subtle
difference from basis: auto that you can exploit (or be bitten by).</p>

<p>The sidebar layout above is the classic two-line flexbox app: fixed
rail + fluid main. Add <code>min-width: 0</code> to items containing
long text — flex items refuse to shrink below their content's minimum
size by default (imagine a long unbreakable word blowing out the row),
and min-width: 0 unlocks shrinking.</p>

<p>Predict the Try-it: the fixed rail stays 110px while the flex: 1 and
flex: 2 boxes share the rest at 1:2; resize the preview and only the
shares change. Gotcha: the unitless <code>flex: 1</code> resets basis
to 0% — an item that looked content-sized can suddenly collapse toward
nothing once its siblings also have flex; check the basis whenever an
item "disappears".</p>
""",
                "tryit": """<!DOCTYPE html>
<html lang="en">
<head><title>flex grow</title>
<style>
  body { font-family: sans-serif; }
  .app { display: flex; gap: 8px; height: 140px; }
  .app > div { border-radius: 8px; padding: 10px; color: white;
               display: grid; place-items: center; font-weight: bold; }
  .side  { flex: 0 0 110px; background: #1572b6; }
  .main  { flex: 1; background: #2e8b57; }
  .grow2 { flex: 2; background: #c73c1a; }
</style>
</head>
<body>
  <div class="app">
    <div class="side">fixed 110px</div>
    <div class="main">flex: 1</div>
    <div class="grow2">flex: 2 — double share</div>
  </div>
  <p>Resize the preview: the fixed rail stays, the others share the
     leftover 2:1.</p>
</body>
</html>
""",
            },
        ],
        "quiz": [
            {
                "type": "mc",
                "question": "In flex-direction: column, justify-content works along the:",
                "options": ["Horizontal axis", "Vertical (main) axis", "Diagonal", "z-axis"],
                "answer": 1,
                "explain": "justify-content always follows the MAIN axis; column makes the main axis vertical.",
            },
            {
                "type": "blank",
                "question": "The property that spaces flex items WITHOUT margins is <code>____</code>.",
                "answers": ["gap", "gap property"],
                "explain": "gap works in flex, grid and multi-column — never adds space after the last item.",
            },
            {
                "type": "mc",
                "question": "Three items with flex: 1 each share leftover space:",
                "options": ["Unequally", "Equally — thirds", "The first takes all", "By content size"],
                "answer": 1,
                "explain": "Equal grow factors = equal shares of free space (flex:1 = 1 1 0%).",
            },
            {
                "type": "mc",
                "question": "The perfect-centering flexbox idiom is:",
                "options": [
                    "text-align: center only",
                    "justify-content: center + align-items: center",
                    "position: absolute everywhere",
                    "margin: auto on children only",
                ],
                "answer": 1,
                "explain": "One center per axis — the most famous three lines of CSS.",
            },
        ],
    },

    # ------------------------------------------------------------------ cs12
    {
        "id": "cs12",
        "title": "CSS Grid ⭐",
        "emoji": "🔲",
        "lessons": [
            {
                "title": "Grid Tracks & the fr Unit",
                "html": """
<p>Flexbox is one-dimensional; <b>Grid</b> is two: rows AND columns at
once, with items placed into the cells they belong to. For whole-page
skeletons and card walls it beats flex. Flip it on and declare the
tracks:</p>

<pre class="code">.board {
  display: grid;
  grid-template-columns: 120px 1fr 2fr;
  grid-template-rows: auto 1fr auto;
  gap: 12px;
}</pre>

<p>Read the declaration: three columns — one fixed at 120px, then two
fractional ones splitting the rest 1:2; two rows — first and last
sized to their content (<code>auto</code>), the middle taking the
leftover; a 12px gutter between every cell. Tracks can be fixed
(<code>120px</code>), content-sized (<code>auto</code>), or fractional
— <code>1fr</code> means "one share of the leftover space", and like
flex's fr it divides only what remains after fixed tracks take
theirs:</p>

<pre class="code">grid-template-columns: repeat(3, 1fr);   /* three equal columns */
grid-template-columns: 2fr 1fr;          /* two-thirds / one-third */</pre>

<p><code>repeat()</code> is the shorthand for patterned tracks —
<code>repeat(3, 1fr)</code> is literally "three tracks of one share
each", sparing you <code>1fr 1fr 1fr</code>. Children flow into the
cells automatically in source order, wrapping row by row: twelve
children in a repeat(3, 1fr) grid = a 4×3 card wall with zero
per-item code. Combined with <code>gap</code> (which works in both
directions at once), a responsive card grid is three lines of
CSS.</p>

<p>Predict the Try-it: six numbered cells pour into a 3-column grid,
two rows, equal widths, even gaps — no width set on any cell.
Gotcha: <code>1fr</code> is not "1 fraction of the container" — it's a
share of the space <i>left after</i> fixed tracks and gaps; a 1000px
container with <code>200px 1fr 2fr</code> splits what remains (after
the 200px and the two gutters) in a 1:2 ratio. And rows created
implicitly by extra children get <code>auto</code> height — set
<code>grid-auto-rows</code> when card rows come out uneven.</p>
""",
                "tryit": """<!DOCTYPE html>
<html lang="en">
<head><title>Grid tracks</title>
<style>
  body { font-family: sans-serif; }
  .board {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 10px;
  }
  .cell { background: #eaf4fd; border: 2px solid #33a9dc;
          border-radius: 8px; padding: 12px; text-align: center;
          font-weight: bold; color: #1572b6; }
</style>
</head>
<body>
  <div class="board">
    <div class="cell">1</div><div class="cell">2</div>
    <div class="cell">3</div><div class="cell">4</div>
    <div class="cell">5</div><div class="cell">6</div>
  </div>
  <p>repeat(3, 1fr) + gap — a 2×3 wall, six items placed automatically.</p>
</body>
</html>
""",
            },
            {
                "title": "grid-template-areas",
                "html": """
<p>Grid's most readable feature: name your regions in ASCII art, and
the layout documents itself. Where column line numbers ("what was line
3 again?") get opaque fast, areas read like the finished page:</p>

<pre class="code">.page {
  display: grid;
  grid-template-areas:
    "header header header"
    "nav    main   side"
    "footer footer footer";
  grid-template-columns: 180px 1fr 220px;
  grid-template-rows: auto 1fr auto;
  min-height: 100vh;
  gap: 10px;
}
.page > header { grid-area: header; }
.page > nav    { grid-area: nav; }
.page > main   { grid-area: main; }
.page > aside  { grid-area: side; }
.page > footer { grid-area: footer; }</pre>

<p>Every quote-delimited word is a cell; repeated words span. Walk it:
the top row is three cells all named "header" — so the header element
spans all three columns; the middle row gives nav, main and side one
cell each, paced 180px / fluid / 220px by the column template; the
bottom row is the footer across everything. Each child claims its
region with <code>grid-area: name</code> — one line per element, no
line numbers anywhere. The grid above is a full app shell — header,
sidebar, content, aside, footer — and rearranging the layout is
<b>editing the ASCII art</b>: swap "side" and "main" and you're done,
no child rule changes at all. Responsive variants become trivial:
redefine the areas inside a media query (a single stacked column, say)
and every grid-area assignment follows automatically.</p>

<p>Predict the Try-it: header and footer stretch across both columns,
the green "side" column takes its 140px, main absorbs the rest — the
art in the CSS is literally the page you see. Gotcha: the art must
form a proper rectangle — every row the same number of words — or the
whole declaration is invalid and dropped silently. A name must also
occupy one connected block: two separate "main" islands are illegal,
so truly L-shaped regions need line-number placement instead.</p>
""",
                "tryit": """<!DOCTYPE html>
<html lang="en">
<head><title>Grid areas</title>
<style>
  body { font-family: sans-serif; margin: 0; }
  .page {
    display: grid;
    grid-template-areas:
      "header header"
      "side   main"
      "footer footer";
    grid-template-columns: 140px 1fr;
    grid-template-rows: auto 1fr auto;
    gap: 8px;
    min-height: 230px;
  }
  .page > * { border-radius: 8px; padding: 10px; color: white; }
  header { grid-area: header; background: #1572b6; }
  nav    { grid-area: side;   background: #2e8b57; }
  main   { grid-area: main;   background: #eaf4fd; color: #1572b6; }
  footer { grid-area: footer; background: #37475a; }
</style>
</head>
<body>
  <div class="page">
    <header>header — spans 2 columns</header>
    <nav>side</nav>
    <main>main — 1fr</main>
    <footer>footer</footer>
  </div>
  <p>The layout is literally written as ASCII art in the CSS.</p>
</body>
</html>
""",
            },
            {
                "title": "Placement & the Grid Gap",
                "html": """
<p>Auto-flow handles the common case, but real layouts need authority:
this item spans two columns, that one takes the full row. Grid lets
you place items by <b>line numbers</b> — note that grid counts lines,
not cells (a 3-column grid has 4 column lines):</p>

<pre class="code">.featured {
  grid-column: 1 / 3;      /* from line 1 to line 3 = spans 2 columns */
  grid-row: 1;
}
.wide  { grid-column: span 2; }         /* shorthand: span 2 tracks */
.tall  { grid-row: span 2; }
.full  { grid-column: 1 / -1; }         /* -1 = the last line: full width */</pre>

<p>Walk it: <code>1 / 3</code> means "start at line 1, end at line 3" —
two tracks wide, since the item crosses two of them. The negative
index counts from the end, so <code>1 / -1</code> is "first line to
last line" — the full row, whatever the column count happens to be;
that's the hero-banner move. <code>span n</code> is the human way to
say "take n tracks" without knowing absolute line numbers — the
friendliest form, and the one that survives track changes. Named lines
and named areas also participate. Items placed explicitly reserve
their cells first; the auto-flowing ones pour around them — magazine
layouts come from sprinkling span-2 items into an auto-flowing
grid.</p>

<p><b>gap</b> in grid is the same property as flexbox's:
<code>gap: 12px</code> both directions, <code>row-gap</code>/
<code>column-gap</code> separately. And alignment has grid-native
extras: <code>justify-items</code>/<code>align-items</code> align items
<i>within their cells</i>, <code>justify-content</code>/
<code>align-content</code> distribute the tracks themselves when the
grid is smaller than the container.</p>

<p>Predict the Try-it: the featured tile is twice as wide as its
neighbours, the green bar crosses the entire row, and the plain cells
auto-flow around both. Gotcha: a <code>span</code> larger than the
remaining room doesn't overflow — the grid quietly adds an implicit
extra row (or column) to honour it; if items "fall off the bottom",
check spans against the track count.</p>
""",
                "tryit": """<!DOCTYPE html>
<html lang="en">
<head><title>Placement</title>
<style>
  body { font-family: sans-serif; }
  .mag { display: grid; grid-template-columns: repeat(3, 1fr);
         gap: 8px; }
  .mag div { background: #eaf4fd; border: 2px solid #33a9dc;
             border-radius: 8px; padding: 10px; text-align: center; }
  .featured { grid-column: span 2; background: #1572b6; color: white;
              font-weight: bold; display: grid; place-items: center; }
  .full { grid-column: 1 / -1; background: #2e8b57; color: white; }
</style>
</head>
<body>
  <div class="mag">
    <div class="featured">featured — spans 2 columns</div>
    <div>2</div>
    <div>3</div>
    <div>4</div>
    <div>5</div>
    <div class="full">1 / -1 — the full row</div>
  </div>
</body>
</html>
""",
            },
            {
                "title": "auto-fit, auto-fill & minmax()",
                "html": """
<p>The pattern behind every responsive card grid with <b>zero media
queries</b> — arguably the single most useful line of modern CSS:</p>

<pre class="code">.cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 12px;
}</pre>

<p>Read it inside-out:</p>

<ul>
<li><code>minmax(220px, 1fr)</code> — a track at least 220px, at most an
equal share of the free space</li>
<li><code>auto-fill</code> — cram in as many 220px+ tracks as fit,
leaving empty ones if items run out</li>
<li><code>auto-fit</code> — same, but collapse empty tracks so items
<b>stretch to fill</b> the row</li>
</ul>

<p>The browser redoes the arithmetic on every resize: a wide screen
fits four 220px-plus columns — four it is; narrow — three, then two,
then one. Every card is never squeezed below its 220px floor, no
breakpoint is written, and adding a fifth card means touching
nothing. The difference between fill and fit appears with few items:
fill keeps the ghost columns (useful when rows must align with each
other), fit stretches the items to span the full width — usually what
you want for a card list.</p>

<p>Variations worth knowing: <code>minmax(220px, auto)</code> sizes
tracks to content; combine with <code>grid-auto-flow: dense</code> to
backfill holes left by spanning items; and <code>auto-fill</code> plus
<code>justify-content: center</code> keeps a small set of cards
centred instead of stretched edge to edge.</p>

<p>Predict the Try-it: drag the preview narrow and watch four columns
become three, two, one — every card intact, never below its floor.
Gotcha: with only one or two cards, auto-fit stretches them absurdly
wide because the empty tracks collapse; that's the moment to pick
auto-fill instead, whose ghost tracks hold each card near its
220px width.</p>
""",
                "tryit": """<!DOCTYPE html>
<html lang="en">
<head><title>auto-fit</title>
<style>
  body { font-family: sans-serif; }
  .cards {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
    gap: 10px;
  }
  .card { background: #eaf4fd; border: 2px solid #1572b6;
          border-radius: 10px; padding: 12px; }
  .card strong { color: #1572b6; }
</style>
</head>
<body>
  <h3>Resize the preview — columns come and go, no media queries:</h3>
  <div class="cards">
    <div class="card"><strong>Card 1</strong><p>minmax(180px, 1fr)</p></div>
    <div class="card"><strong>Card 2</strong><p>auto-fit</p></div>
    <div class="card"><strong>Card 3</strong><p>responsive</p></div>
    <div class="card"><strong>Card 4</strong><p>zero breakpoints</p></div>
  </div>
</body>
</html>
""",
            },
        ],
        "quiz": [
            {
                "type": "mc",
                "question": "grid-template-columns: repeat(3, 1fr) creates:",
                "options": ["One 3fr column", "Three equal columns", "Three rows", "A 3px gap"],
                "answer": 1,
                "explain": "repeat(3, 1fr) = three tracks, each one equal share.",
            },
            {
                "type": "blank",
                "question": "grid-column: 1 / ____ makes an item span the full row width.",
                "answers": ["-1"],
                "explain": "-1 refers to the last column line — 1 to -1 is the whole row.",
            },
            {
                "type": "mc",
                "question": "The zero-media-query responsive card grid line is:",
                "options": [
                    "display: flex; flex-wrap: wrap;",
                    "grid-template-columns: repeat(auto-fit, minmax(220px, 1fr))",
                    "float: left; width: 33%",
                    "grid-auto-flow: column",
                ],
                "answer": 1,
                "explain": "auto-fit + minmax reflows columns with the viewport — no breakpoints.",
            },
            {
                "type": "mc",
                "question": "grid-template-areas gives you:",
                "options": [
                    "Faster rendering",
                    "A visual ASCII-art layout that rearranges responsively",
                    "Free shadows",
                    "Automatic animations",
                ],
                "answer": 1,
                "explain": "Named regions written as art; redefining the art reflows every grid-area item.",
            },
        ],
    },

    # ------------------------------------------------------------------ cs13
    {
        "id": "cs13",
        "title": "Multi-column Layout",
        "emoji": "📰",
        "lessons": [
            {
                "title": "Multi-column Layout",
                "html": """
<p>Newspapers flow text down one column and continue at the top of the
next — CSS multi-column does exactly that to any block of content. It
is the one layout module that <i>balances and fills columns of
text</i> for you:</p>

<pre class="code">.article {
  columns: 3;                /* ideally 3 columns */
  column-gap: 2rem;
  column-rule: 1px solid #ddd;   /* the line between them */
}
h2 { column-span: all; }     /* a heading across all columns */</pre>

<p>Walk it: the browser splits the article's content into three
balanced columns with 2rem between them and a hairline rule drawn in
the gap — the rule paints in the gutter, never touching the text. The
<code>h2</code> escapes the column flow entirely and stretches across
all of them, the masthead move:</p>

<ul>
<li><code>columns: 3</code> — a wish: the browser fits 3 columns of at
least its implied width; <code>columns: 200px</code> instead means
"columns of ~200px, as many as fit" (the responsive way)</li>
<li>Content <b>fills column 1 to the bottom, then column 2</b> — true
text flow, not slicing: a paragraph reads continuously down one column
and resumes at the top of the next</li>
<li><code>break-inside: avoid</code> keeps a card/figure from being
split across columns</li>
</ul>

<p>Multi-column is the right tool for <i>long text</i>: articles,
changelogs, glossaries, legal copy. For boxed content (cards,
products), grid's auto-fit is usually better — m-col optimises reading
flow, grid optimises placement. A fun modern use: a masonry-ish look
with <code>columns</code> + <code>break-inside: avoid</code> on cards
— items keep their height and stack within their columns.</p>

<p>Predict the Try-it: the octopus facts flow into two columns split
by a dashed rule, the heading riding across both, each boxed fact kept
whole. Gotcha: a column container is a <i>fragmented</i> flow — a
child's background stops at each column break and re-paints in the
next fragment, which looks broken on boxes you expected to be solid;
that's exactly what break-inside: avoid is for. And on narrow screens
prefer <code>columns: 200px</code> over a fixed count, or your three
columns shrink to unreadable slivers.</p>
""",
                "tryit": """<!DOCTYPE html>
<html lang="en">
<head><title>Multi-column</title>
<style>
  body { font-family: sans-serif; }
  .paper {
    columns: 2;
    column-gap: 2rem;
    column-rule: 1px dashed #33a9dc;
    max-width: 560px;
  }
  .paper h2 { column-span: all; color: #1572b6; }
  .fact { break-inside: avoid; background: #f2f8fe;
          padding: 8px; border-radius: 6px; margin: 8px 0; }
</style>
</head>
<body>
  <div class="paper">
    <h2>Facts about octopuses</h2>
    <div class="fact">Three hearts. Two pump blood to the gills, one to
      the body — and the body one stops when they swim.</div>
    <div class="fact">Blue blood, based on copper rather than iron.</div>
    <div class="fact">Each of the eight arms can act semi-independently,
      with two-thirds of the neurons located in the arms themselves.</div>
    <div class="fact">Masters of disguise: colour, texture, and even
      texture-matching within a second.</div>
    <div class="fact">They squeeze through gaps as small as their
      beak — the only hard part of their body.</div>
  </div>
</body>
</html>
""",
            },
        ],
        "quiz": [
            {
                "type": "mc",
                "question": "columns: 200px (instead of a count) means:",
                "options": [
                    "Exactly one 200px column",
                    "As many ~200px columns as fit — the responsive form",
                    "A 200px gap",
                    "Invalid",
                ],
                "answer": 1,
                "explain": "A width wish lets the browser choose the column count per available space.",
            },
            {
                "type": "blank",
                "question": "To keep a card from splitting across columns: break-inside: ____.",
                "answers": ["avoid"],
                "explain": "break-inside: avoid keeps boxes whole as they flow between columns.",
            },
        ],
    },

    # ------------------------------------------------------------------ cs14
    {
        "id": "cs14",
        "title": "Responsive Design",
        "emoji": "📱",
        "lessons": [
            {
                "title": "Media Queries & Breakpoints",
                "html": """
<p>One page, every screen — from a 320px phone to a 4K monitor.
<b>Media queries</b> apply CSS conditionally: the stylesheet asks about
the viewport (and more), and rules apply only when the answer matches.
The mobile-first idiom:</p>

<pre class="code">/* mobile-first: base styles = phones */
.cards { grid-template-columns: 1fr; }

@media (min-width: 600px) {     /* tablets and up */
  .cards { grid-template-columns: repeat(2, 1fr); }
}
@media (min-width: 960px) {     /* desktops and up */
  .cards { grid-template-columns: repeat(3, 1fr); }
}</pre>

<p>Walk it: the base rule — no query at all — is what every device
gets: one column. Then two <code>@media</code> blocks each say "from
this width upward, override". A small phone matches only the base; a
700px tablet matches base + 600px (two columns); a desktop matches all
three (three columns). Because min-width queries only ever <i>add</i>,
each block stays short and nothing ever needs undoing:</p>

<ul>
<li><b>min-width queries</b> — the mobile-first pattern: base styles for
small screens, <i>add</i> complexity as space grows</li>
<li><b>conditions combine</b>:
<code>@media (min-width: 600px) and (max-width: 959px)</code>;
<code>, </code> = or; <code>not</code> negates</li>
<li><b>the meta tag is mandatory</b>:
<code>&lt;meta name="viewport" content="width=device-width,
initial-scale=1"&gt;</code> — without it phones fake a 980px desktop and
your breakpoints never fire</li>
</ul>

<p>Beyond width, media queries test <code>prefers-reduced-motion</code>,
<code>prefers-color-scheme: dark</code>, <code>hover: none</code>
(touch devices), <code>orientation</code>... — the tool for adapting to
the <i>device</i>, while container queries (next chapter) adapt to the
<i>container</i>. On <b>breakpoints</b>: don't chase device models; add
one when the <i>design</i> breaks. With fluid units (rem, %, clamp) and
modern layout (auto-fit!), most designs need far fewer breakpoints than
you'd think. Predict the Try-it: drag the preview's width and the panel
recolours as it crosses 480px and 760px. Gotcha: the base styles must
live OUTSIDE any query — burying them inside the first @media means
devices that match no query (or one deleted query) get nothing at
all.</p>
""",
                "tryit": """<!DOCTYPE html>
<html lang="en">
<head><title>Media queries</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
  body { font-family: sans-serif; }
  .panel { background: #1572b6; color: white; padding: 14px;
           border-radius: 8px; }
  .panel::after { content: " base styles — narrow screen"; }

  @media (min-width: 480px) {
    .panel { background: #2e8b57; }
    .panel::after { content: " ≥ 480px"; }
  }
  @media (min-width: 760px) {
    .panel { background: #c73c1a; }
    .panel::after { content: " ≥ 760px"; }
  }
</style>
</head>
<body>
  <div class="panel">Resize the preview and watch my colour change.</div>
  <p>Also note this page HAS the viewport meta tag — required for
     media queries to behave on phones.</p>
</body>
</html>
""",
            },
            {
                "title": "Fluid Layouts & Typography",
                "html": """
<p>Media queries step; fluid design glides. Between the breakpoints
lies a continuum of screen widths, and fluid techniques make the page
adapt <i>continuously</i> — nothing jumps at a magic width. The
techniques from earlier chapters stack into one system:</p>

<ul>
<li><b>Fluid type</b> — clamp with viewport units:
<code>font-size: clamp(1.8rem, 1.2rem + 3vw, 3.2rem)</code></li>
<li><b>Fluid space</b> — section padding that grows with the screen:
<code>padding: clamp(1rem, 4vw, 3rem)</code></li>
<li><b>Fluid tracks</b> — auto-fit + minmax grids; fr units</li>
<li><b>Fluid measure</b> — <code>max-width: 65ch</code> on prose</li>
</ul>

<pre class="code">:root {
  /* a space scale that scales itself */
  --space: clamp(1rem, 0.5rem + 2vw, 2.5rem);
}
section { padding-block: var(--space); gap: var(--space); }</pre>

<p>Walk it: the custom property holds one fluid value — a floor of
1rem, a ceiling of 2.5rem, and a formula that grows with the viewport
between them. Every section's vertical padding and every gap reads the
same token, so spacing stays in rhythm everywhere while scaling from
phone to desktop. The preferred value's <code>0.5rem + 2vw</code> form
is deliberate: a constant plus a viewport term keeps the value growing
from the very first pixel instead of sitting clamped at small
widths.</p>

<p>The modern mindset: base everything on the root font size (rem), let
clamp handle the in-between zones, and reserve media queries for genuine
<i>structural</i> changes — a sidebar becoming a row, a grid changing
its areas. Fewer breakpoints, smoother screens, and every screen between
the breakpoints looks intentional rather than stretched.</p>

<p>Predict the Try-it: drag the width slowly — padding, gaps, the
heading, the card columns all move proportionally and never snap.
Gotcha: viewport units ignore the scrollbar and text-zoom settings;
tie minimums and maximums to rem (as above) so users with larger text
preferences keep a usable floor — and never set body text purely in
vw, which becomes unreadably tiny on phones.</p>
""",
                "tryit": """<!DOCTYPE html>
<html lang="en">
<head><title>Fluid design</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
  body { font-family: sans-serif; margin: 0; }
  :root { --space: clamp(0.75rem, 0.4rem + 2vw, 2.5rem); }
  .hero {
    padding: var(--space);
    background: #1572b6; color: white;
  }
  h1 { font-size: clamp(1.5rem, 1rem + 3.5vw, 3.2rem); margin: 0; }
  .cards { display: grid; gap: var(--space); padding: var(--space);
           grid-template-columns: repeat(auto-fit, minmax(170px, 1fr)); }
  .card { background: #eaf4fd; border-radius: 8px; padding: var(--space); }
</style>
</head>
<body>
  <div class="hero"><h1>Everything here is fluid</h1></div>
  <div class="cards">
    <div class="card">Fluid padding</div>
    <div class="card">Fluid gaps</div>
    <div class="card">Fluid columns</div>
  </div>
  <p>Drag the preview's width slowly — nothing jumps; everything glides.</p>
</body>
</html>
""",
            },
        ],
        "quiz": [
            {
                "type": "mc",
                "question": "Mobile-first media queries use:",
                "options": ["max-width", "min-width", "equal-width", "no queries"],
                "answer": 1,
                "explain": "Base styles for small screens; @media (min-width) adds complexity upward.",
            },
            {
                "type": "blank",
                "question": "Without the <code>&lt;meta name=\"____\"&gt;</code> tag, phones fake a 980px desktop viewport.",
                "answers": ["viewport"],
                "explain": "width=device-width, initial-scale=1 makes media queries work as intended.",
            },
            {
                "type": "mc",
                "question": "The modern guidance on breakpoints:",
                "options": [
                    "One per device model",
                    "Add them when the design breaks — fluid techniques reduce the need",
                    "Exactly five",
                    "Never use any",
                ],
                "answer": 1,
                "explain": "clamp/auto-fit/fr handle the between-zones; queries handle structural change.",
            },
        ],
    },

    # ------------------------------------------------------------------ cs15
    {
        "id": "cs15",
        "title": "Container Queries",
        "emoji": "🪟",
        "lessons": [
            {
                "title": "Container Queries",
                "html": """
<p>Media queries ask "how wide is the <i>screen</i>?" — but components
live in sidebars, cards, and grid cells where the screen is a lie. The
same card that works full-width turns cramped inside a 220px sidebar,
and no media query can even see the difference. <b>Container
queries</b> ask the right question: "how wide is <i>my box</i>?"</p>

<pre class="code">.card-wrap { container-type: inline-size; }   /* declare a container */

@container (min-width: 400px) {
  .card {                 /* this card KNOWS it's in a wide spot */
    display: flex;        /* go horizontal */
    gap: 14px;
  }
  .card img { width: 120px; }
}</pre>

<p>Two parts, always both. First, mark an ancestor with
<code>container-type: inline-size</code> — its inline size becomes
queryable. Second, write <code>@container</code> rules that apply based
on the <b>nearest container's size</b>: here, when the wrapper is at
least 400px wide, the card inside switches from stacked to horizontal
with a fixed image column; below that width those rules simply don't
match. The same card component now adapts to wherever it lands —
full-width column, sidebar, grid cell — with zero knowledge of the
page. Move the component and its responsiveness moves with it; that is
exactly what media queries, triggered only by page dimensions, could
never do.</p>

<p>Container query units complete the picture: <code>cqw</code>/
<code>cqh</code> are percentages of the <i>container's</i> size —
<code>font-size: 4cqw</code> scales a card's title with its box, not
the screen. This is <b>component-based responsive design</b>: design
systems where every component carries its own responsive rules. MDN
calls it one of the biggest architectural shifts in recent CSS.</p>

<p>Predict the Try-it: identical card markup, two wrappers — the wide
one lays the card out horizontally with the image aside, the narrow
220px one keeps it stacked. Gotcha: <code>container-type:
inline-size</code> applies size containment — the element's width no
longer depends on its contents (that's what prevents circularity), so
a container never shrink-wraps to the card inside. And @container
rules can only style <i>descendants</i> of the container, never the
container itself — which is why the pattern is always wrap-then-style.</p>
""",
                "tryit": """<!DOCTYPE html>
<html lang="en">
<head><title>Container queries</title>
<style>
  body { font-family: sans-serif; }
  .wide-wrap, .narrow-wrap { container-type: inline-size;
    margin: 10px 0; padding: 8px; border: 2px dashed #33a9dc;
    border-radius: 8px; }
  .narrow-wrap { max-width: 220px; }

  .card { background: #eaf4fd; border-radius: 8px; padding: 10px; }
  .card img { width: 100%; border-radius: 6px; }

  @container (min-width: 380px) {
    .card { display: flex; gap: 12px; align-items: center; }
    .card img { width: 110px; }
  }
</style>
</head>
<body>
  <p>Same component, two containers:</p>
  <div class="wide-wrap">
    <div class="card">
      <img src="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='220' height='80'%3E%3Crect width='220' height='80' fill='%231572b6'/%3E%3C/svg%3E" alt="placeholder">
      <p>Wide container → horizontal layout.</p>
    </div>
  </div>
  <div class="narrow-wrap">
    <div class="card">
      <img src="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='220' height='80'%3E%3Crect width='220' height='80' fill='%232e8b57'/%3E%3C/svg%3E" alt="placeholder">
      <p>Narrow container → stacked.</p>
    </div>
  </div>
</body>
</html>
""",
            },
        ],
        "quiz": [
            {
                "type": "mc",
                "question": "Container queries respond to:",
                "options": [
                    "The viewport width",
                    "The size of the element's nearest container",
                    "The user's font size",
                    "The device type",
                ],
                "answer": 1,
                "explain": "@container measures the nearest ancestor with container-type — component-level responsiveness.",
            },
            {
                "type": "blank",
                "question": "An ancestor gets <code>container-type: ____</code> to become queryable.",
                "answers": ["inline-size"],
                "explain": "container-type: inline-size exposes the element's width to @container rules.",
            },
        ],
    },
]
