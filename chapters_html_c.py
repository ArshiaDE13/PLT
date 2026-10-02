"""HTML Tutor chapters 10-13, grounded in MDN Web Docs (developer.mozilla.org)."""

CHAPTERS_HTML_C = [
    # ------------------------------------------------------------------ h10
    {
        "id": "h10",
        "title": "Accessibility",
        "emoji": "♿",
        "lessons": [
            {
                "title": "Accessibility & Semantic HTML",
                "html": """
<p><b>Accessibility (a11y)</b> means the web works for everyone —
including the roughly 1 in 6 people worldwide with a disability: blind
and low-vision users, deaf users, motor-impaired users, and everyone
temporarily impaired (a broken arm, bright sunlight, a noisy train).</p>

<p>The quiet truth of a11y: <b>semantic HTML is most of it</b>. Native
elements come with decades of built-in accessibility — roles, keyboard
behaviour, announcements:</p>

<ul>
<li>a <code>&lt;button&gt;</code> is announced "button" and works with
Enter and Space</li>
<li>a <code>&lt;label&gt;</code> is read with its field</li>
<li>headings build a navigable outline; landmarks
(<code>main</code>/<code>nav</code>) offer jump points</li>
<li>an <code>&lt;img alt&gt;</code> speaks its content</li>
</ul>

<p>Almost every a11y bug on the web is a <b>div impersonating a native
element</b>: a clickable div (no focus, no announcement), a select
rebuilt from spans (unusable keyboard), a "link" with no href. The fix
is always the same and it's cheaper than the bug: use the real
element.</p>

<p>The golden tool to check yourself: unplug the mouse for five minutes.
Tab through your page. If you can't reach or operate something with the
keyboard, a large group of users can't either — and a screen-reader user
probably can't at all.</p>

<p>It helps to know who you are building for. Screen readers speak the
accessibility tree (built from your semantics); keyboard users need every
control reachable and operable with Tab, Enter and Space; users with low
vision need contrast and zoom that doesn't break; users with motor
impairments need generous click targets and no time-limited traps. One
page, four different ways of "reading" it — and semantic HTML serves all
four at once.</p>

<p>Gotcha: accessibility is not a final coat of paint. Bolted-on fixes
(an aria-label here, a tabindex there) cost more than writing semantic
markup from the start — which is why this is chapter 10, after you have
met all the real elements.</p>
""",
                "tryit": """<!DOCTYPE html>
<html lang="en">
<head><title>Keyboard test</title>
<style>
  body { font-family: sans-serif; }
  .fake, .real { display: block; margin: 10px 0; padding: 10px 16px;
                 background: #f16529; color: white; border: none;
                 border-radius: 8px; width: 200px; }
</style></head>
<body>
  <p>Press Tab repeatedly. Which control gets a focus ring
     (orange outline)?</p>

  <button class="fake" onclick="this.textContent='div clicked'
    ">I am a clickable DIV</button>

  <button class="real" onclick="this.textContent='button clicked'
    ">I am a real BUTTON</button>

  <p>The div can't take keyboard focus at all — keyboard users
     can never press it.</p>
</body>
</html>
""",
            },
            {
                "title": "Alt Text & Images",
                "html": """
<p><code>alt</code> is the blind visitor's version of your image. Write
it as if describing the image to someone on the phone — what
<i>information</i> it carries, not what it looks like:</p>

<ul>
<li><b>Informative image</b> — describe the content and its purpose:
<code>alt="Bar chart: sales doubled from 2024 to 2026"</code></li>
<li><b>Functional image</b> (a logo inside a link) — describe the
<b>destination/action</b>, not pixels:
<code>alt="MDN home"</code></li>
<li><b>Decorative image</b> — empty
<code>alt=""</code>: screen readers skip it entirely. A missing alt
makes them read the filename instead ("logo-slash-dot-png") — worse
than nothing</li>
<li><b>Complex images</b> (charts, diagrams) — short alt plus a longer
description nearby (caption, adjacent text, or
<code>figure</code>/<code>figcaption</code>)</li>
</ul>

<pre class="code">&lt;img src="chart.png"
     alt="Bar chart: sales doubled from 2024 to 2026"&gt;

&lt;a href="/"&gt;&lt;img src="logo.png" alt="MDN home"&gt;&lt;/a&gt;

&lt;img src="divider.png" alt=""&gt;    decorative — skip me</pre>

<p>Anti-patterns that help nobody: "image of...", "picture of..."
(the screen reader already says "image"), filenames, and keyword
stuffing (that's an SEO trick that hurts the very people alt text is
for).</p>

<p>Walk the demo's three images: the logo inside a link describes its
destination ("MDN home page") — click it and that is where you go, so
that is what matters. The chart's alt gives the takeaway, not the
pixels ("sales up 120 percent") — alt is a summary for ears, not a
caption for eyes. The decorative divider is silent on purpose.</p>

<p>Gotcha: alt length. Screen readers read the whole thing aloud, so one
clear sentence usually beats a paragraph; if an image genuinely needs
more, use figure/figcaption or a visible description nearby and keep
the alt short. And when you upgrade an image, upgrade its alt — stale
descriptions misinform more than missing ones.</p>
""",
                "tryit": """<!DOCTYPE html>
<html lang="en">
<head><title>Alt text clinic</title></head>
<body>
  <!-- Functional: describes the destination -->
  <a href="https://developer.mozilla.org">
    <img src="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='140' height='60'%3E%3Crect width='140' height='60' rx='8' fill='%2303599c'/%3E%3Ctext x='70' y='37' text-anchor='middle' fill='white' font-size='16' font-family='Arial'%3EMDN%3C/text%3E%3C/svg%3E"
         alt="MDN home page">
  </a>

  <!-- Informative -->
  <img src="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='140' height='60'%3E%3Crect width='140' height='60' fill='%232e8b57'/%3E%3Ctext x='70' y='37' text-anchor='middle' fill='white' font-size='14' font-family='Arial'%3E2026: +120%25%3C/text%3E%3C/svg%3E"
       alt="Chart showing 2026 sales up 120 percent" width="140">

  <!-- Decorative: intentionally skipped by screen readers -->
  <img src="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='140' height='12'%3E%3Crect width='140' height='12' fill='%23f16529'/%3E%3C/svg%3E"
       alt="" width="140">
</body>
</html>
""",
            },
            {
                "title": "Accessible Forms & Labels",
                "html": """
<p>Forms are where accessibility is won or lost — they are the checkout,
the login, the signup. The rules are small and absolute:</p>

<ul>
<li><b>Every field gets a <code>&lt;label&gt;</code></b>, connected with
<code>for</code>/<code>id</code> (or by wrapping). Placeholders are
hints, not labels — they vanish on typing and are usually too low-
contrast to read.</li>
<li><b>Group related controls</b> in
<code>&lt;fieldset&gt;&lt;legend&gt;</code> — radio groups especially:
the legend answers "what am I choosing?"</li>
<li><b>Announce errors in text.</b> Red borders alone help nobody who
can't see them; pair them with a message near the field
(<code>aria-describedby</code> links it formally)</li>
<li><b>Mark required fields</b> — the <code>required</code> attribute
plus visible text, not a lone asterisk</li>
<li><b>Keep the order logical</b> — Tab should visit fields in the order
a human would fill them (it does, if the DOM order matches the visual
order)</li>
</ul>

<pre class="code">&lt;label for="pw"&gt;Password (min 8 characters)&lt;/label&gt;
&lt;input id="pw" type="password" minlength="8" required
       aria-describedby="pw-hint"&gt;
&lt;span id="pw-hint"&gt;Use letters and numbers.&lt;/span&gt;</pre>

<p><code>aria-describedby</code> is the pattern to notice: the hint is
programmatically tied to the field, so screen readers read it right
after the label. The same connection trick works for error messages
(<code>aria-invalid="true"</code> flags the broken state).</p>

<p>Walk the snippet: the label says what the field is <i>and</i> its
constraint ("min 8 characters"), so the requirement is heard, not just
enforced. Tab into the field and a screen reader announces "Password,
required, edit text, use letters and numbers" — label, required state,
then the describedby hint. Three pieces of information, all wired by
attributes.</p>

<p>Gotcha: don't move focus with auto-advancing fields or hijack Enter —
let the browser's default behaviour work, since it is what users are
trained on. And test with the keyboard alone: if you can fill and
submit your form without touching the mouse, screen-reader users have
a fighting chance.</p>
""",
                "tryit": """<!DOCTYPE html>
<html lang="en">
<head><title>Accessible form</title>
<style>
  body { font-family: sans-serif; } fieldset { max-width: 320px; }
  label { display: block; margin: 8px 0 2px; }
  input { padding: 6px; width: 240px; }
  .hint { color: #666; font-size: 13px; }
</style></head>
<body>
  <form>
    <fieldset>
      <legend>Create account</legend>

      <label for="user">Username (required)</label>
      <input id="user" name="user" required
             aria-describedby="u-hint">
      <span class="hint" id="u-hint">Letters and numbers only.</span>

      <label for="pw">Password (required)</label>
      <input id="pw" name="pw" type="password" minlength="8" required
             aria-describedby="p-hint">
      <span class="hint" id="p-hint">At least 8 characters.</span>
    </fieldset>
    <button>Create</button>
  </form>
</body>
</html>
""",
            },
            {
                "title": "ARIA & Keyboard Accessibility",
                "html": """
<p>Sometimes no native element fits — a tab widget, a star rating, a
live notification. That's what <b>ARIA</b> (Accessible Rich Internet
Applications) is for: attributes that add semantics HTML lacks.</p>

<ul>
<li><b><code>role</code></b> — what this thing IS:
<code>role="tab"</code>, <code>role="navigation"</code>,
<code>role="alert"</code></li>
<li><b><code>aria-*</code> states &amp; properties</b> — what it's
doing: <code>aria-expanded="true"</code>,
<code>aria-checked</code>, <code>aria-label</code> (a label for
icon-only things), <code>aria-live</code> ("announce changes here")</li>
</ul>

<pre class="code">&lt;button aria-label="Close dialog"&gt;✕&lt;/button&gt;

&lt;button aria-expanded="false" aria-controls="menu"&gt;Menu ▾&lt;/button&gt;
&lt;ul id="menu" hidden&gt;...&lt;/ul&gt;

&lt;div role="alert"&gt;Your changes were saved.&lt;/div&gt;</pre>

<p>MDN's first rule of ARIA, worth tattooing: <b>don't use ARIA</b> —
if a native element exists, it already has the semantics, and ARIA on
top only adds work. ARIA is the repair kit for custom widgets, not a
decoration for native ones. And a <code>role</code> is a <b>promise</b>:
<code>role="button"</code> obliges you to also implement keyboard
activation — semantics without behaviour is a lie.</p>

<p><b>Keyboard accessibility</b> is non-negotiable and mostly free:</p>

<ul>
<li>every interactive element must be <b>reachable with Tab</b> and
<b>operable with keys</b> (buttons: Enter/Space; links: Enter)</li>
<li>a visible <b>focus indicator</b> — never
<code>outline: none</code> without a replacement</li>
<li>logical tab order: DOM order should match visual order
(<code>tabindex="1+"</code> breaks it — avoid)</li>
<li>"skip to content" link as the first tab stop for long pages</li>
</ul>

<p>Walk the demo: the close button shows only "✕" on screen, but
<code>aria-label</code> makes it "Close dialog, button" to screen
readers. The toggle button keeps <code>aria-expanded</code> in sync with
the box's hidden state, so assistive tech hears "expanded" the moment
it opens. The alert region announces "Details are now visible!"
without focus moving at all — that is <code>role="alert"</code>'s
live-region power.</p>

<p>Gotcha: ARIA on native elements is duplicate semantics —
<code>&lt;button role="button"&gt;</code> is noise. The decision ladder:
first ask "is there a native element?", then "can I fix the native
one?", and only then reach for ARIA. Semantics without matching
behaviour is still a lie, whichever way you write it.</p>
""",
                "tryit": """<!DOCTYPE html>
<html lang="en">
<head><title>ARIA & keyboard</title>
<style>
  body { font-family: sans-serif; }
  button:focus { outline: 3px solid #f16529; }
  [role="alert"] { background: #2e8b57; color: white; padding: 8px 12px;
                   border-radius: 6px; }
</style></head>
<body>
  <!-- Icon-only button rescued by aria-label -->
  <button aria-label="Close dialog"
    onclick="document.getElementById('box').hidden = true">✕</button>

  <button aria-expanded="false" aria-controls="box"
    onclick="const b=document.getElementById('box');
             b.hidden = !b.hidden;
             this.setAttribute('aria-expanded', String(!b.hidden));">
    Toggle details ▾
  </button>

  <div id="box" role="alert" hidden>Details are now visible!</div>

  <p>Tab through: the focus ring is clearly visible, and the ✕ is
     announced as "Close dialog".</p>
</body>
</html>
""",
            },
        ],
        "quiz": [
            {
                "type": "mc",
                "question": "MDN's first rule of ARIA is:",
                "options": [
                    "Add ARIA to every element",
                    "Don't use ARIA — prefer native elements with built-in semantics",
                    "role comes before id",
                    "ARIA replaces HTML",
                ],
                "answer": 1,
                "explain": "Native elements already have roles/keyboard behaviour; ARIA is the repair kit for custom widgets.",
            },
            {
                "type": "mc",
                "question": "A purely decorative image should carry:",
                "options": ["A detailed description", "alt=\"\"", "role=\"img\"", "aria-label"],
                "answer": 1,
                "explain": "Empty alt tells screen readers to skip it; missing alt means they read the filename.",
            },
            {
                "type": "blank",
                "question": "The attribute that ties a hint paragraph to a form field is <code>aria-____</code>.",
                "answers": ["describedby", "aria-describedby"],
                "explain": "aria-describedby links supporting text to the control so it's announced with it.",
            },
            {
                "type": "mc",
                "question": "The five-minute accessibility test is:",
                "options": [
                    "Run a spelling checker",
                    "Unplug the mouse and Tab through the page",
                    "Look at it on a big monitor",
                    "Ask a friend to read it",
                ],
                "answer": 1,
                "explain": "If Tab can't reach and operate it, keyboard and screen-reader users can't either.",
            },
        ],
    },

    # ------------------------------------------------------------------ h11
    {
        "id": "h11",
        "title": "Advanced HTML",
        "emoji": "🧰",
        "lessons": [
            {
                "title": "iframes & Embedding",
                "html": """
<p>Embedding one document inside another — the web inside the web — is
the <code>&lt;iframe&gt;</code> (inline frame):</p>

<pre class="code">&lt;iframe src="https://example.com"
        width="400" height="300"
        title="Embedded example"&gt;
&lt;/iframe&gt;</pre>

<p>Every video embed, map widget, comment box and ad you've seen is an
iframe. The embedded page lives in its own <b>browsing context</b>: its
own document, its own CSS, its own JS — separated from yours by the
browser. Parent and frame can't casually touch each other's internals
(the <b>same-origin policy</b> guards this), which is why widgets can be
embedded safely.</p>

<ul>
<li><code>width</code>/<code>height</code> — its box size</li>
<li><code>title</code> — what screen readers announce ("frame, Embedded
example") — required for accessibility</li>
<li><code>srcdoc</code> — inline HTML instead of a URL (how this
course's try-it previews work!)</li>
<li><code>sandbox</code> — restricts what the frame may do (scripts,
forms, popups...); enabling a subset is safer than nothing</li>
<li><code>loading="lazy"</code> — defer loading until near the
viewport</li>
</ul>

<p>Its siblings are mostly retired: <code>&lt;embed&gt;</code> and
<code>&lt;object&gt;</code> historically embedded plugins (Flash!) and
still can embed PDFs/media generically (<code>object</code> even has
fallback children — content shown if the embed fails). For modern work:
iframes for documents/apps, <code>&lt;video&gt;</code>/<code>&lt;audio&gt;</code>
for media, <code>&lt;img&gt;</code>/<code>&lt;picture&gt;</code> for
images, and native PDF viewing needs only a link.</p>

<p>Walk the demo: the frame's <code>srcdoc</code> holds a tiny HTML
document inline; the browser parses it as a separate page inside the
box. Notice the <code>title</code> attribute on the frame — that is how
screen readers announce what this foreign region is ("frame, A nested
page demo").</p>

<p>Gotcha: an iframe is not a borderless void — it is a full document
load, often the slowest thing on your page. Give it dimensions (or it
flickers while loading), load lazily when it sits below the fold, and
don't nest more than you need: every frame is another browsing context
the browser must spin up.</p>
""",
                "tryit": """<!DOCTYPE html>
<html lang="en">
<head><title>iframes</title></head>
<body>
  <h2>A nested document</h2>
  <iframe srcdoc="&lt;h1 style='font-family:sans-serif'&gt;Hi from inside the iframe!&lt;/h1&gt;
    &lt;p style='font-family:sans-serif'&gt;I have my own document.&lt;/p&gt;"
    width="320" height="120" title="A nested page demo"
    style="border: 2px solid #f16529; border-radius: 8px"></iframe>

  <p>The inner page can't touch this outer page — different browsing
     contexts.</p>
</body>
</html>
""",
            },
            {
                "title": "canvas",
                "html": """
<p><code>&lt;canvas&gt;</code> is a blank bitmap that JavaScript paints on —
the element itself does nothing until code draws into it:</p>

<pre class="code">&lt;canvas id="c" width="300" height="150"&gt;&lt;/canvas&gt;

&lt;script&gt;
  const ctx = document.getElementById("c").getContext("2d");
  ctx.fillStyle = "#f16529";
  ctx.fillRect(20, 20, 120, 80);        // an orange rectangle

  ctx.beginPath();
  ctx.arc(220, 60, 40, 0, Math.PI * 2); // an orange circle
  ctx.fillStyle = "#ffd43b";
  ctx.fill();
&lt;/script&gt;</pre>

<p>Walk the code: <code>getContext("2d")</code> hands you a paintbrush
object; <code>fillStyle</code> picks the colour; <code>fillRect</code>
stamps a rectangle; <code>arc</code> traces a circle's path and
<code>fill</code> inks it. Five lines of JavaScript, two shapes, no HTML
in between — the element is just a viewport onto a drawing
surface.</p>

<p>The mental model: <b>immediate mode</b>. You draw pixels now, and the
canvas remembers nothing — move something and you redraw everything
(each animation frame clears and repaints). That's why canvas powers
games, particle effects and chart renderers at 60fps.</p>

<ul>
<li><b>Always set <code>width</code>/<code>height</code> attributes</b> —
the defaults are 300×150, and CSS-stretching a canvas blurs it (CSS
scales the bitmap; it doesn't add pixels)</li>
<li>Its context has modes: <code>2d</code>, and <code>webgl</code>/
<code>webgpu</code> for 3D</li>
<li><b>Accessibility:</b> a canvas is an opaque bitmap — provide text
alternatives (offscreen content, aria labels, or a DOM fallback
inside the tags)</li>
<li>Everything inside is <b>not DOM</b> — you can't click "the orange
circle"; you get coordinates and do hit-testing yourself</li>
</ul>

<p>Gotcha: never size a canvas purely with CSS. The attributes define the
bitmap's real resolution; CSS merely stretches it — set both
consistently (or account for devicePixelRatio) or your crisp lines go
blurry. And remember the fallback content between the tags ("your
browser doesn't support canvas") shows only in ancient browsers — all
current ones support it.</p>
""",
                "tryit": """<!DOCTYPE html>
<html lang="en">
<head><title>canvas</title></head>
<body>
  <canvas id="c" width="300" height="150"
          style="border: 2px solid #263238; border-radius: 8px"></canvas>

  <script>
    const ctx = document.getElementById("c").getContext("2d");
    ctx.fillStyle = "#fff4ee";
    ctx.fillRect(0, 0, 300, 150);
    ctx.fillStyle = "#f16529";
    ctx.fillRect(20, 20, 120, 80);
    ctx.beginPath();
    ctx.arc(220, 75, 40, 0, Math.PI * 2);
    ctx.fillStyle = "#ffd43b";
    ctx.fill();
    ctx.fillStyle = "#263238";
    ctx.font = "14px sans-serif";
    ctx.fillText("painted by JS", 30, 135);
  </script>
</body>
</html>
""",
            },
            {
                "title": "svg",
                "html": """
<p><b>SVG (Scalable Vector Graphics)</b> is the opposite philosophy to
canvas: instead of pixels, you declare <b>shapes</b> — and the element
is real DOM:</p>

<pre class="code">&lt;svg width="200" height="120" viewBox="0 0 200 120"&gt;
  &lt;rect x="10" y="10" width="90" height="60" rx="8"
        fill="#f16529"&gt;&lt;/rect&gt;
  &lt;circle cx="150" cy="40" r="30" fill="#ffd43b"&gt;&lt;/circle&gt;
  &lt;text x="55" y="100" text-anchor="middle"
        font-family="sans-serif"&gt;shapes!&lt;/text&gt;
&lt;/svg&gt;</pre>

<p>Because shapes are elements, everything DOM applies: CSS styles them
(<code>circle { fill: red }</code>), JavaScript manipulates them
(<code>querySelector</code>!), and each shape can have its own click
handler. And being vector, SVG is crisp at any zoom or size — the
format of every icon system and logo on the modern web.</p>

<ul>
<li><code>viewBox="0 0 200 120"</code> — the internal coordinate system;
the element can be resized freely and the drawing scales with it</li>
<li>Basic shapes: <code>rect</code>, <code>circle</code>,
<code>ellipse</code>, <code>line</code>, <code>polyline</code>,
<code>polygon</code>, <code>path</code> (the all-powerful freeform
path)</li>
<li>Inline SVG (as above) is styleable; SVG files via
<code>&lt;img&gt;</code> render but can't be styled from the page</li>
<li>It's text! Gzip-compresses beautifully, version-controls cleanly,
and is accessible when labelled
(<code>role="img"</code> + <code>&lt;title&gt;</code>)</li>
</ul>

<p>canvas vs svg in one line: <b>canvas</b> for thousands of changing
pixels (games), <b>svg</b> for crisp resizable graphics you want to
style and interact with (icons, charts, diagrams).</p>

<p>Walk the demo: the <code>viewBox</code> sets an internal grid of
220×130 units; the rect and circle place themselves in those units, not
pixels — resize the element and they scale with it. The CSS rule
<code>svg circle:hover</code> restyles a shape like any element, and the
script gives the circle a click listener — try both in the preview.</p>

<p>Gotcha: SVG inside <code>&lt;img&gt;</code> is a dead end for styling
and scripts — it renders, but the page cannot reach inside. Inline it
when you need interaction. And always label meaningful SVGs with
<code>role="img"</code> plus a <code>&lt;title&gt;</code> or
<code>aria-label</code>, or screen readers hear an empty region.</p>
""",
                "tryit": """<!DOCTYPE html>
<html lang="en">
<head><title>svg</title>
<style> svg circle:hover { fill: #c0392b; cursor: pointer; } </style></head>
<body>
  <svg width="220" height="130" viewBox="0 0 220 130"
       role="img" aria-label="An orange rectangle and a yellow circle">
    <rect x="10" y="10" width="100" height="70" rx="10" fill="#f16529"></rect>
    <circle cx="170" cy="45" r="35" fill="#ffd43b"></circle>
    <text x="60" y="115" text-anchor="middle"
          font-family="sans-serif">hover the circle!</text>
  </svg>

  <script>
    document.querySelector("svg circle")
      .addEventListener("click", () => {
        document.querySelector("svg rect")
          .setAttribute("fill", "#2e8b57");
      });
  </script>
</body>
</html>
""",
            },
            {
                "title": "template",
                "html": """
<p><code>&lt;template&gt;</code> holds HTML that the browser
<b>parses but does not render</b> — inert markup waiting for JavaScript
to stamp out copies:</p>

<pre class="code">&lt;ul id="list"&gt;&lt;/ul&gt;

&lt;template id="item-template"&gt;
  &lt;li class="item"&gt;
    &lt;strong class="name"&gt;&lt;/strong&gt; — &lt;span class="price"&gt;&lt;/span&gt;
  &lt;/li&gt;
&lt;/template&gt;

&lt;script&gt;
  const items = [
    { name: "Espresso", price: "$2" },
    { name: "Latte",    price: "$3.5" },
  ];
  const tpl = document.getElementById("item-template");
  const list = document.getElementById("list");

  for (const it of items) {
    const node = tpl.content.cloneNode(true);   // a fresh copy
    node.querySelector(".name").textContent = it.name;
    node.querySelector(".price").textContent = it.price;
    list.appendChild(node);
  }
&lt;/script&gt;</pre>

<p>Why not just build the HTML with string concatenation? Because
template content is <b>real parsed DOM</b>: images don't load, scripts
don't run, and there's nothing to escape or inject — you fill in
textContent and everything stays safe. It's the standard-native way to
say "here's the shape of one row; make many."</p>

<ul>
<li>Content lives in <code>tpl.content</code> (a DocumentFragment)</li>
<li><code>cloneNode(true)</code> copies the whole subtree; you then
target classes inside and append</li>
<li>The template can sit anywhere in the document — head, body — it
never displays</li>
</ul>

<p>Walk the demo: three menu items render from one template. The loop
clones <code>tpl.content</code>, fills the <code>.name</code> and
<code>.price</code> slots with textContent, and appends each copy to the
list. Add a fourth item to the array and the markup needs no change at
all — data drives the DOM.</p>

<p>Templates + custom elements (HTML 12) are the two halves of native
web components.</p>

<p>Gotcha: fill cloned templates with <code>textContent</code>, not
<code>innerHTML</code>, when the data is user-supplied — that is the
whole safety story above. And don't forget the <code>true</code> in
<code>cloneNode(true)</code>: cloning without it copies the wrapper only
and your "rows" come out empty, a classic head-scratcher. Debug tip:
<code>console.log(tpl.content.children.length)</code> shows what the
fragment really holds.</p>
""",
                "tryit": """<!DOCTYPE html>
<html lang="en">
<head><title>template</title>
<style> body { font-family: sans-serif; } .item { padding: 6px 10px;
  border-left: 4px solid #f16529; margin: 6px 0; background: #fff4ee; }
</style></head>
<body>
  <h2>Menu</h2>
  <ul id="list" style="list-style:none; padding:0"></ul>

  <template id="item-template">
    <li class="item">
      <strong class="name"></strong> — <span class="price"></span>
    </li>
  </template>

  <script>
    const items = [
      { name: "Espresso", price: "$2.0" },
      { name: "Latte", price: "$3.5" },
      { name: "Mocha", price: "$4.0" },
    ];
    const tpl = document.getElementById("item-template");
    const list = document.getElementById("list");
    for (const it of items) {
      const node = tpl.content.cloneNode(true);
      node.querySelector(".name").textContent = it.name;
      node.querySelector(".price").textContent = it.price;
      list.appendChild(node);
    }
  </script>
</body>
</html>
""",
            },
            {
                "title": "dialog",
                "html": """
<p>Before HTML's <code>&lt;dialog&gt;</code> element, every modal popup
was a DIY pile of divs, z-index hacks and focus traps. Now it's an
element with built-in behaviour:</p>

<pre class="code">&lt;dialog id="confirm"&gt;
  &lt;h2&gt;Delete item?&lt;/h2&gt;
  &lt;p&gt;This cannot be undone.&lt;/p&gt;
  &lt;button id="yes"&gt;Delete&lt;/button&gt;
  &lt;button id="no"&gt;Cancel&lt;/button&gt;
&lt;/dialog&gt;

&lt;button id="open-btn"&gt;Delete item…&lt;/button&gt;

&lt;script&gt;
  const dlg = document.getElementById("confirm");
  document.getElementById("open-btn")
    .addEventListener("click", () => dlg.showModal());
  document.getElementById("no")
    .addEventListener("click", () => dlg.close());
  document.getElementById("yes")
    .addEventListener("click", () => { dlg.close("deleted"); });
&lt;/script&gt;</pre>

<p>What you get for free, which DIY modals famously get wrong:</p>

<ul>
<li><b><code>showModal()</code></b> opens it <i>modally</i>: page behind
is inert, focus moves into the dialog, Tab cycles <b>inside</b> it, and
the <code>Esc</code> key closes it — the whole focus-trap checklist,
built in</li>
<li>a ::backdrop pseudo-element styles the dimmed page behind it</li>
<li><b><code>show()</code></b> opens it non-modally (page stays live) if
you want a floating panel instead</li>
<li><code>dialog.close(returnValue)</code> closes it and records a
return value readable on <code>dlg.returnValue</code></li>
<li>it participates in forms via
<code>method="dialog"</code></li>
</ul>

<p>Walk the demo: open the dialog and the page behind dims
(::backdrop) and goes inert — Tab is trapped inside, Esc closes, and
focus returns where it came from. Cancel and Delete both call
<code>close(...)</code> with a return value; the <code>close</code>
event reads <code>dlg.returnValue</code> and prints which button won.
Modal semantics — historically the hairiest JavaScript on the web — in
about ten lines.</p>

<p>Gotcha: the element is invisible until opened; don't fight that with
CSS <code>display</code> overrides, because the attribute-driven states
<i>are</i> the API. And prefer <code>showModal()</code> over
<code>show()</code> for confirmations: the focus trap is an
accessibility feature, not a limitation. All current browsers support
<code>&lt;dialog&gt;</code>, so the old polyfills can retire.</p>
""",
                "tryit": """<!DOCTYPE html>
<html lang="en">
<head><title>dialog</title>
<style> body { font-family: sans-serif; }
  dialog { border: 2px solid #f16529; border-radius: 10px; }
  dialog::backdrop { background: rgba(38, 50, 56, 0.6); }
</style></head>
<body>
  <p>Press the button — then try Tab and Esc inside the dialog.</p>

  <button id="open">Open confirm dialog</button>
  <p id="result"></p>

  <dialog id="confirm">
    <h2>Delete item?</h2>
    <p>This cannot be undone.</p>
    <button id="yes">Delete</button>
    <button id="no">Cancel</button>
  </dialog>

  <script>
    const dlg = document.getElementById("confirm");
    document.getElementById("open")
      .addEventListener("click", () => dlg.showModal());
    document.getElementById("no")
      .addEventListener("click", () => dlg.close("cancelled"));
    document.getElementById("yes")
      .addEventListener("click", () => dlg.close("deleted"));
    dlg.addEventListener("close", () => {
      document.getElementById("result").textContent =
        "closed with: " + dlg.returnValue;
    });
  </script>
</body>
</html>
""",
            },
            {
                "title": "details, progress, meter & output",
                "html": """
<p>A quartet of small elements that replace common JavaScript widgets
with plain markup.</p>

<p><b><code>&lt;details&gt;</code> + <code>&lt;summary&gt;</code></b> — the
native accordion. Toggle logic, keyboard support and semantics included;
the <code>open</code> attribute shows it by default:</p>

<pre class="code">&lt;details&gt;
  &lt;summary&gt;What is HTML?&lt;/summary&gt;
  &lt;p&gt;The web's markup language...&lt;/p&gt;
&lt;/details&gt;</pre>

<p><b><code>&lt;progress&gt;</code></b> — a task in flight (upload,
installation). With <code>value</code> + <code>max</code> it shows the
partial bar; without them it's indeterminate (spinning):</p>

<pre class="code">&lt;progress value="70" max="100"&gt;70%&lt;/progress&gt;
&lt;progress&gt;working…&lt;/progress&gt;</pre>

<p><b><code>&lt;meter&gt;</code></b> — a <b>measurement within a known
range</b>, colour-coded by thresholds (disk usage, quiz score):</p>

<pre class="code">&lt;meter value="0.8" min="0" max="1" low="0.4" high="0.9"
       optimum="0"&gt;80%&lt;/meter&gt;</pre>

<p><b><code>&lt;output&gt;</code></b> — the element for displaying the
<i>result of a calculation</i>, semantically tied to its inputs via
<code>for</code>. Screen readers announce changes to it:</p>

<pre class="code">&lt;input type="range" id="qty" value="3"&gt;
&lt;output for="qty" id="total"&gt;$12&lt;/output&gt;

&lt;script&gt;
  const qty = document.getElementById("qty");
  qty.addEventListener("input", () =&gt; {
    document.getElementById("total").textContent =
      "$" + (qty.value * 4);
  });
&lt;/script&gt;</pre>

<p>The dividing line: <code>progress</code> = "how far through this
task", <code>meter</code> = "how does this value sit in its range". A
loading bar is progress; a fuel gauge is a meter.</p>

<p>Walk the demo: the accordion opens because of <code>open</code>, and
toggling needs no script at all — the browser wires the summary click.
The progress bar reads "70 of 100"; the meter reads "0.8 in a range
where 0.25 counts as low and 0.9 as high" — similar visuals, different
questions answered. Drag the quantity slider and the output element
updates through the one-line listener.</p>

<p>Gotchas: keep the fallback text inside <code>&lt;progress&gt;</code>
and <code>&lt;meter&gt;</code> (between the tags) — that is what screen
readers and very old browsers get. And use <code>&lt;output&gt;</code>
for <i>results</i>, not as a generic span; using it semantically earns
you the live-region announcements for free.</p>
""",
                "tryit": """<!DOCTYPE html>
<html lang="en">
<head><title>Small widgets</title>
<style> body { font-family: sans-serif; line-height: 2 } </style></head>
<body>
  <details open>
    <summary>What is HTML?</summary>
    <p>The web's markup language — no JavaScript needed to toggle me!</p>
  </details>

  <h3>progress vs meter</h3>
  <p>Uploading: <progress value="70" max="100">70%</progress></p>
  <p>Battery: <meter value="0.8" min="0" max="1" low="0.25"
     high="0.9" optimum="1">80%</meter></p>

  <h3>output</h3>
  <label>Quantity
    <input type="range" id="qty" min="1" max="10" value="3">
  </label>
  <output id="total" for="qty">$12</output>

  <script>
    const qty = document.getElementById("qty");
    qty.addEventListener("input", () => {
      document.getElementById("total").textContent =
        "$" + qty.value * 4;
    });
  </script>
</body>
</html>
""",
            },
        ],
        "quiz": [
            {
                "type": "mc",
                "question": "Which dialog method opens it modally with a focus trap and Esc-to-close?",
                "options": ["dlg.show()", "dlg.showModal()", "dlg.open()", "dlg.focus()"],
                "answer": 1,
                "explain": "showModal() = modal: inert page, Tab cycles inside, Esc closes — all built in.",
            },
            {
                "type": "mc",
                "question": "Thousands of moving pixels for a game — which element?",
                "options": ["svg", "canvas", "img", "template"],
                "answer": 1,
                "explain": "canvas is immediate-mode bitmap painting at 60fps; svg is DOM shapes best for interactive/resizable graphics.",
            },
            {
                "type": "blank",
                "question": "The element holding inert, unrendered HTML for JavaScript to clone is <code>&lt;____&gt;</code>.",
                "answers": ["template"],
                "explain": "template.content is parsed DOM that renders nothing until cloned.",
            },
            {
                "type": "mc",
                "question": "A fuel gauge showing a value within a known range is:",
                "options": ["&lt;progress&gt;", "&lt;meter&gt;", "&lt;output&gt;", "&lt;range&gt;"],
                "answer": 1,
                "explain": "progress = task completion; meter = a value measured against a range with thresholds.",
            },
        ],
    },

    # ------------------------------------------------------------------ h12
    {
        "id": "h12",
        "title": "HTML APIs & Browser Interaction",
        "emoji": "🔌",
        "lessons": [
            {
                "title": "The DOM",
                "html": """
<p>When the browser parses your HTML, it builds the <b>DOM</b> (Document
Object Model) — a live tree of JavaScript objects mirroring every
element. HTML is the source; the DOM is the running model your scripts
actually touch:</p>

<pre class="code">&lt;body&gt;
  &lt;h1 class="title"&gt;Hi&lt;/h1&gt;
  &lt;p&gt;Text&lt;/p&gt;
&lt;/body&gt;

         document
            └── body
              ├── h1 (class="title")
              └── p</pre>

<p>Read the tree: <code>document</code> is the root, <code>body</code> its
child, and each element becomes a node — the h1 and p are siblings, and
text inside them becomes text nodes. This tree is why "nesting right"
from chapter 1 pays off: the tree is what CSS selectors and JavaScript
walk.</p>

<p>Every node is an object with properties and methods. The everyday
toolkit:</p>

<pre class="code">// find
document.getElementById("x")            by id
document.querySelector("ul li a")       first CSS match
document.querySelectorAll(".item")      all matches

// read / write
el.textContent = "new text"             plain text
el.innerHTML = "&lt;b&gt;parsed&lt;/b&gt;"          markup (careful — XSS)
el.setAttribute("lang", "fa")
el.style.color = "crimson"
el.classList.add("active") / remove / toggle

// create / move
const p = document.createElement("p")
parent.appendChild(p) / parent.removeChild(el)</pre>

<p>Walk the toolkit: find elements by id or CSS selector, read or write
their text, attributes, inline styles and class lists, create new nodes
and attach them. Six verbs cover most of dynamic HTML. The demo below
uses four: it finds the list and input, creates an <code>&lt;li&gt;</code>,
sets its textContent, and appends it — a to-do list in a dozen
lines.</p>

<p>Two cautions from MDN's pages: <code>innerHTML</code> with
user-supplied strings is the classic <b>XSS</b> hole — prefer
<code>textContent</code> unless you truly mean to parse markup; and the
DOM is <i>live</i> — change it and the page updates instantly, no
refresh.</p>

<p>One more habit: query once, store the reference.
<code>const list = document.getElementById("list")</code> at the top of
your script beats calling it inside every handler — lookups cost, and a
stored node keeps working as the page changes around it.</p>
""",
                "tryit": """<!DOCTYPE html>
<html lang="en">
<head><title>The DOM</title>
<style> body { font-family: sans-serif; } li { padding: 4px 8px; }
  .done { text-decoration: line-through; color: #999; } </style></head>
<body>
  <h1>Groceries</h1>
  <ul id="list"></ul>
  <input id="new" placeholder="add item…">
  <button id="add">Add</button>

  <script>
    const list = document.getElementById("list");
    const input = document.getElementById("new");

    document.getElementById("add").addEventListener("click", () => {
      if (!input.value.trim()) return;
      const li = document.createElement("li");
      li.textContent = input.value;
      li.addEventListener("click", () => li.classList.toggle("done"));
      list.appendChild(li);
      input.value = "";
    });
  </script>
</body>
</html>
""",
            },
            {
                "title": "Events",
                "html": """
<p>Everything the user does — clicks, keys, scrolling, input — becomes an
<b>event</b>, and your code listens for them with
<code>addEventListener</code>:</p>

<pre class="code">element.addEventListener("click", (event) =&gt; {
  // runs every time the element is clicked
});

// the common families:
"click"            a press-and-release on an element
"input"            value changed, per keystroke (inputs)
"change"           value committed (blur, select, checkbox)
"submit"           a form is being sent
"keydown" / "keyup"  keys on the keyboard
"mouseover" / "mouseout" / "scroll" / "load" ...</pre>

<p>How it flows: something happens, the browser creates an event object
and calls every listener registered for that event type on that element
— in registration order. Nothing polls; your function sleeps until the
event arrives. This inversion of control is what makes pages feel alive
without loops.</p>

<p>The event object carries details
(<code>event.target</code> = what was hit, <code>event.key</code> = which
key) and can stop default behaviour:</p>

<pre class="code">form.addEventListener("submit", (e) =&gt; {
  e.preventDefault();          // no page reload — we handle it
  console.log(input.value);
});</pre>

<p>Two concepts make events scale. <b>Bubbling</b>: an event fires on the
deepest target, then bubbles up through its ancestors — so one listener
on the parent can handle clicks for all its children (event
delegation — how the sidebar in this app works). And
<code>event.stopPropagation()</code> stops that journey when needed.</p>

<pre class="code">// delegation: ONE listener for every list item, present or future
list.addEventListener("click", (e) =&gt; {
  if (e.target.matches("li")) e.target.classList.toggle("done");
});</pre>

<p>Walk the preventDefault example: without it, submitting reloads the
page with the data in the URL; with it, the default dies and your
handler takes over — the minimal skeleton behind every modern app
form.</p>

<p>Gotcha: don't sprinkle <code>onclick="..."</code> attributes in HTML —
one handler per attribute, and markup gets tangled with behaviour fast.
<code>addEventListener</code> keeps everything in the script and allows
many listeners per element. And remember events need elements that
exist: scripts can only query markup written above them — or wait for
the <code>DOMContentLoaded</code> event.</p>
""",
                "tryit": """<!DOCTYPE html>
<html lang="en">
<head><title>Events</title>
<style> body { font-family: sans-serif; } .box { width: 220px;
  padding: 14px; background: #fff4ee; border: 2px solid #f16529;
  border-radius: 8px; margin: 8px 0; } </style></head>
<body>
  <input id="live" placeholder="type here — event 'input'">
  <p>You typed: <output id="echo"></output></p>

  <div class="box">
    <button>One</button>
    <button>Two</button>
    <button>Three</button>
    — delegated: one listener on the box!
  </div>

  <script>
    document.getElementById("live").addEventListener("input", (e) => {
      document.getElementById("echo").textContent = e.target.value;
    });
    document.querySelector(".box").addEventListener("click", (e) => {
      if (e.target.matches("button"))
        e.target.style.background =
          e.target.style.background ? "" : "#ffd43b";
    });
  </script>
</body>
</html>
""",
            },
            {
                "title": "Web Storage",
                "html": """
<p>Cookies' modern replacement for keeping data in the browser:
<b>Web Storage</b> — two objects with the same tiny API:</p>

<ul>
<li><b><code>localStorage</code></b> — persists until deleted; survives
closing the browser. This app stores your name and progress here.</li>
<li><b><code>sessionStorage</code></b> — same API, but dies with the tab.
Perfect for half-finished forms.</li>
</ul>

<pre class="code">localStorage.setItem("name", "Ada");        // store (strings only!)
const name = localStorage.getItem("name");   // read → "Ada" or null
localStorage.removeItem("name");
localStorage.clear();                        // nuke everything

// objects go through JSON:
localStorage.setItem("prefs", JSON.stringify({ theme: "dark" }));
const prefs = JSON.parse(localStorage.getItem("prefs"));</pre>

<p>Walk the block: <code>setItem("name", "Ada")</code> writes;
<code>getItem</code> reads back — or <code>null</code> if absent, which
is why you check before using. Objects have no native storage form, so
<code>JSON.stringify</code> before writing and <code>JSON.parse</code>
after reading; forget the parse and you get the literal string
'{"theme": "dark"}' back instead of an object.</p>

<p>Know the limits:</p>

<ul>
<li><b>Strings only</b> — objects/numbers are serialised with
<code>JSON</code></li>
<li><b>~5 MB per origin</b> — it's a notebook, not a database (that's
IndexedDB's job)</li>
<li><b>Origin-scoped</b> — data belongs to
<code>scheme://host:port</code>; other sites can't see it</li>
<li><b>Synchronous</b> — fine for small values, blocking for
megabytes</li>
</ul>

<p>Fun fact: this course uses <code>localStorage</code> for your name,
language, progress and playground code — check your browser's devtools →
Application → Local Storage right now and you'll find the keys.</p>

<p>Gotcha: storage is per-origin and per-device — keep nothing secret in
it (any script on the page, and any user with devtools, reads it in
plaintext), and don't expect it to sync across a user's devices. Treat
it as a convenience cache, and guard your reads: one corrupted value
and an unguarded <code>JSON.parse</code> throws on every page
load.</p>
""",
                "tryit": """<!DOCTYPE html>
<html lang="en">
<head><title>Web Storage</title>
<style> body { font-family: sans-serif; } input, button { padding: 6px; }
</style></head>
<body>
  <p>Your name survives reloads — it lives in localStorage:</p>
  <input id="name" placeholder="type your name">
  <button id="save">Save</button>
  <button id="forget">Forget me</button>
  <p id="greeting"></p>

  <script>
    const input = document.getElementById("name");
    const greeting = document.getElementById("greeting");
    function refresh() {
      const n = localStorage.getItem("tutor-name");
      greeting.textContent = n ? "👋 Welcome back, " + n + "!" : "No name saved.";
      if (n) input.value = n;
    }
    document.getElementById("save").addEventListener("click", () => {
      localStorage.setItem("tutor-name", input.value.trim());
      refresh();
    });
    document.getElementById("forget").addEventListener("click", () => {
      localStorage.removeItem("tutor-name");
      refresh();
    });
    refresh();
  </script>
</body>
</html>
""",
            },
            {
                "title": "Drag & Drop",
                "html": """
<p>HTML has native drag &amp; drop. Mark a source
<code>draggable</code>, hand over data on <code>dragstart</code>, and let
targets accept it on <code>dragover</code> + <code>drop</code>:</p>

<pre class="code">&lt;img src="card.png" draggable="true" id="card"&gt;
&lt;div id="hand" style="min-height:100px"&gt;drop here&lt;/div&gt;

&lt;script&gt;
  card.addEventListener("dragstart", (e) =&gt; {
    e.dataTransfer.setData("text/plain", e.target.id);
  });

  hand.addEventListener("dragover", (e) =&gt; {
    e.preventDefault();          // REQUIRED — without it, no drop
  });

  hand.addEventListener("drop", (e) =&gt; {
    e.preventDefault();
    const id = e.dataTransfer.getData("text/plain");
    hand.appendChild(document.getElementById(id));
  });
&lt;/script&gt;</pre>

<p>Trace the flow: the user presses the card and <code>dragstart</code>
stashes its id in <code>dataTransfer</code>; as the drag crosses the
zone, <code>dragover</code> fires continuously and its
<code>preventDefault()</code> is what flips the target from "no drops
allowed" to accepting; release fires <code>drop</code>, which reads the
id back and moves the element. Three listeners, one contract.</p>

<p>The event family:</p>

<ul>
<li><code>dragstart</code> — on the source; stash data via
<code>dataTransfer.setData(type, string)</code></li>
<li><code>dragover</code> — on a potential target, firing continuously;
you <b>must</b> <code>preventDefault()</code> to signal "I accept
drops" (the #1 gotcha)</li>
<li><code>drop</code> — the release; read the data back with
<code>getData</code></li>
<li><code>dragend</code> — on the source, either way it ended</li>
</ul>

<p>Because <code>dataTransfer</code> only carries strings, objects travel
as JSON. Styling hooks: <code>:dragging</code>-like feedback comes from
<code>dragstart</code>/<code>dragend</code> classes, and
<code>dropEffect</code> (<code>copy</code>/<code>move</code>) shapes the
cursor. Native D&amp;D works on desktop; on touch screens it's spotty —
serious apps pair it with pointer-event fallbacks.</p>

<p>Gotchas: the missing <code>preventDefault()</code> on
<code>dragover</code> is the single most common "my drop zone doesn't
work" bug — the browser's default is to reject drops. And native drag
&amp; drop is keyboard- and touch-inaccessible: real products add
buttons ("move to zone") alongside, so the action is never
drag-only.</p>
""",
                "tryit": """<!DOCTYPE html>
<html lang="en">
<head><title>Drag & drop</title>
<style>
  body { font-family: sans-serif; }
  #hand { min-height: 110px; border: 2px dashed #f16529; border-radius: 8px;
          padding: 10px; }
  img { margin: 4px; }
  #hand.over { background: #fff4ee; }
</style></head>
<body>
  <p>Drag the card into the dashed zone:</p>
  <img id="card" draggable="true"
       src="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='90' height='120'%3E%3Crect width='90' height='120' rx='8' fill='%23f16529'/%3E%3Ctext x='45' y='66' text-anchor='middle' fill='white' font-size='15' font-family='Arial'%3Ecard%3C/text%3E%3C/svg%3E"
       alt="A draggable card" width="90" height="120">
  <div id="hand">drop zone</div>

  <script>
    const card = document.getElementById("card");
    const hand = document.getElementById("hand");
    card.addEventListener("dragstart", (e) =>
      e.dataTransfer.setData("text/plain", "card"));
    hand.addEventListener("dragover", (e) => {
      e.preventDefault();
      hand.classList.add("over");
    });
    hand.addEventListener("dragleave", () => hand.classList.remove("over"));
    hand.addEventListener("drop", (e) => {
      e.preventDefault();
      hand.classList.remove("over");
      hand.textContent = "got: " + e.dataTransfer.getData("text/plain");
    });
  </script>
</body>
</html>
""",
            },
            {
                "title": "Web Workers",
                "html": """
<p>JavaScript runs on one thread — one heavy loop and the page freezes.
<b>Web Workers</b> are real background threads: scripts that run in
parallel and talk to the page only through messages:</p>

<pre class="code">&lt;script&gt;
  const worker = new Worker("calc.js");
  worker.postMessage({ n: 40 });          // send a task
  worker.addEventListener("message", (e) =&gt; {
    console.log("result:", e.data);       // receive the answer
  });
&lt;/script&gt;

&lt;!-- calc.js — the worker's own file --&gt;
self.addEventListener("message", (e) =&gt; {
  const result = slowFibonacci(e.data.n);
  self.postMessage(result);               // answer back
});</pre>

<p>Walk both halves: the page creates a worker from a file, posts a
message object, and listens back. Inside <code>calc.js</code>, the
worker listens, computes — off the main thread, so the UI keeps
animating — and posts the result. The whole conversation is two
<code>addEventListener("message")</code> calls facing each other.</p>

<p>The rules, straight from MDN:</p>

<ul>
<li>Workers have <b>no DOM access</b> — no
<code>document</code>, no page elements. Pure computation.</li>
<li>Communication is <b>message-passing</b>: structured-cloned copies,
not shared objects (the reason a stuck worker can be killed without
corrupting the page — exactly how this app's Python engine works!)</li>
<li>Workers are same-origin only, and in dev they need a real file (or
a blob URL)</li>
<li><code>worker.terminate()</code> kills it instantly</li>
</ul>

<p>When to reach for one: anything over ~50ms that shouldn't jank the
UI — parsing big JSON, image processing, cryptography, search. The
browser has special-purpose workers too: <b>service workers</b> (the
proxy behind offline apps and installable PWAs) and shared workers.</p>

<p>This course is a live example: the C and Python playgrounds both run
engines inside workers so an infinite loop can be terminated without
freezing the page.</p>

<p>Gotcha: workers can't see the DOM, so the beginner plan "spawn a
worker to update the page" is impossible by design — workers compute
and hand back data; the main thread paints. And don't spawn one for a
5-millisecond task: message overhead exceeds the compute. Feel the
threshold: does the task jank a frame (~16ms) or stall a tap (~100ms)?
If yes, worker.</p>
""",
            },
            {
                "title": "Web Components & Custom Elements",
                "html": """
<p>HTML's own component system: define a new element in JavaScript once,
then use it like any tag — no framework required.</p>

<pre class="code">&lt;coffee-cup size="large"&gt;&lt;/coffee-cup&gt;

&lt;script&gt;
  class CoffeeCup extends HTMLElement {
    connectedCallback() {                 // inserted into the DOM
      const size = this.getAttribute("size") || "small";
      this.innerHTML =
        "&lt;span&gt;☕ ×" + (size === "large" ? 3 : 1) + "&lt;/span&gt;";
    }
  }
  customElements.define("coffee-cup", CoffeeCup);
&lt;/script&gt;</pre>

<p>Walk it: the page writes <code>&lt;coffee-cup size="large"&gt;</code>
like any tag; the script teaches the browser what that tag means. When
each element enters the DOM, <code>connectedCallback</code> fires, reads
the attribute, and stamps the inner HTML. Three cups in the markup, one
class in the script.</p>

<p>The rules: the tag name must contain a <b>dash</b>
(<code>coffee-cup</code>, never <code>coffee</code>) so custom elements
can never collide with future HTML; the class extends
<code>HTMLElement</code>; lifecycle callbacks fire at the right moments
(<code>connectedCallback</code>, <code>disconnectedCallback</code>,
<code>attributeChangedCallback</code>).</p>

<p>Two superpowers complete the picture:</p>

<ul>
<li><b>Shadow DOM</b> — <code>this.attachShadow({mode:"open"})</code>
gives the component a private DOM subtree whose styles don't leak in or
out: true encapsulation, the thing iframes did at document level, at
element level.</li>
<li><b><code>&lt;template&gt;</code>s + slots</b> — declarative skeletons
stamped per instance, with <code>&lt;slot&gt;</code> filling in
caller-provided content.</li>
</ul>

<p>Together these three — custom elements, shadow DOM, templates — are
<b>Web Components</b>: framework-free, standard, reusable widgets.
(MDN's full guide is the reference when you build your first
one.)</p>

<p>Gotcha: custom elements upgrade asynchronously — the element renders
empty until its defining script has run, which is why the definition
lives in a <code>&lt;script&gt;</code> on the page. And don't build
everything as a component: if a native element fits, use it. A custom
<code>&lt;my-button&gt;</code> re-implementing <code>&lt;button&gt;</code>
badly is the classic anti-pattern of the technique.</p>
""",
                "tryit": """<!DOCTYPE html>
<html lang="en">
<head><title>Web Components</title></head>
<body>
  <coffee-cup size="small"></coffee-cup>
  <coffee-cup size="large"></coffee-cup>
  <coffee-cup></coffee-cup>

  <script>
    class CoffeeCup extends HTMLElement {
      connectedCallback() {
        const size = this.getAttribute("size") || "small";
        const cups = size === "large" ? "☕☕☕" : "☕";
        this.style.fontSize = "26px";
        this.innerHTML = cups + " <small>(" + size + ")</small>";
      }
    }
    customElements.define("coffee-cup", CoffeeCup);
  </script>
</body>
</html>
""",
            },
        ],
        "quiz": [
            {
                "type": "blank",
                "question": "The live tree of objects the browser builds from your HTML is called the <code>____</code>.",
                "answers": ["dom", "DOM", "document object model"],
                "explain": "HTML is the source; the DOM is the running model JavaScript manipulates.",
            },
            {
                "type": "mc",
                "question": "One listener handling clicks for all current AND future list items is:",
                "options": ["A memory leak", "Event delegation via bubbling", "A worker", "Impossible"],
                "answer": 1,
                "explain": "Events bubble to ancestors; one parent listener + e.target covers future children.",
            },
            {
                "type": "mc",
                "question": "What can a Web Worker NOT access?",
                "options": ["fetch()", "setTimeout", "The DOM (document)", "console.log"],
                "answer": 2,
                "explain": "Workers are computation-only: no DOM. They talk to the page via messages.",
            },
            {
                "type": "mc",
                "question": "Why must custom element names contain a dash?",
                "options": [
                    "Style convention only",
                    "So they can never clash with present or future native tags",
                    "JavaScript requires dashes in class names",
                    "They don't — any name works",
                ],
                "answer": 1,
                "explain": "The dash guarantees namespacing: HTML will never ship a <coffee-cup>.",
            },
        ],
    },

    # ------------------------------------------------------------------ h13
    {
        "id": "h13",
        "title": "HTML Syntax & Standards",
        "emoji": "📜",
        "lessons": [
            {
                "title": "Parsing & the DOM Tree",
                "html": """
<p>What actually happens between your text file and the rendered page?
The browser's HTML <b>parser</b> reads the byte stream and builds the
<b>DOM tree</b> — and the algorithm is more forgiving than you'd
expect.</p>

<p>The pipeline: bytes → (encoding) → characters → <b>tokens</b> (tags,
text, comments) → <b>nodes</b> → the DOM tree → layout &amp; paint.
The parser works a chunk at a time, so pages start rendering before the
last byte arrives.</p>

<p>The surprising part: the parser has a <b>built-in error-recovery
recipe</b> for almost every mistake (the HTML5 spec literally spells out
the recovery steps — it's one of the most precisely specified parsers in
software). Unclosed <code>&lt;p&gt;</code>? Nested
<code>&lt;form&gt;</code>s? A stray tag in a table? The spec defines
exactly what the browser must do with it. That's why the web's billion
broken pages still render — and why two browsers agree on what a broken
page means.</p>

<p>But recovered markup produces a <b>different tree than you meant</b> —
usually silently. The professional stance: write correct markup, and
treat the parser's mercy as a safety net, not a style.</p>

<p>Fun proof this course uses everywhere: an iframe's
<code>srcdoc</code> is parsed through this same algorithm, so even a
fragment of HTML becomes a full document with implied
<code>html</code>/<code>head</code>/<code>body</code> nodes.</p>
""",
            },
            {
                "title": "Content Models",
                "html": """
<p>Not every element may live inside every other. The HTML spec groups
elements into <b>content models</b> — categories that define what each
element expects around and inside it:</p>

<ul>
<li><b>Metadata content</b> — sets up the page:
<code>title</code>, <code>meta</code>, <code>link</code>,
<code>style</code> (head territory)</li>
<li><b>Flow content</b> — nearly everything allowed in
<code>body</code></li>
<li><b>Sectioning content</b> — <code>article</code>,
<code>section</code>, <code>nav</code>, <code>aside</code>: defines the
outline</li>
<li><b>Heading content</b> — <code>h1</code>–<code>h6</code>,
<code>hgroup</code></li>
<li><b>Phrasing content</b> — the inline level: text, <code>a</code>,
<code>strong</code>, <code>img</code>, <code>code</code>,
<code>span</code>... (roughly "what can appear inside a paragraph")</li>
<li><b>Embedded content</b> — <code>img</code>, <code>iframe</code>,
<code>video</code>, <code>canvas</code>: imports another resource</li>
<li><b>Interactive content</b> — <code>a</code>,
<code>button</code>, <code>input</code>, <code>select</code>,
<code>details</code>: things the user operates</li>
</ul>

<p>Why care? Because <b>nesting rules come from these models</b>, and
breaking them produces real bugs. The classics:</p>

<ul>
<li>a <code>&lt;div&gt;</code> (flow) inside a
<code>&lt;p&gt;</code> (phrasing-only) — the parser <b>closes the
paragraph early</b>, splitting it in two. Number-one cause of mystery
gaps</li>
<li>an <code>&lt;a&gt;</code> inside another
<code>&lt;a&gt;</code> — forbidden; the parser untangles it into
siblings</li>
<li>interactive inside interactive (<code>button</code> in
<code>a</code>) — undefined focus/click behaviour</li>
</ul>

<p>The validator (next lesson) is the content-model checker.</p>
""",
            },
            {
                "title": "Void Elements & Optional Tags",
                "html": """
<p>Two places where HTML syntax quietly bends.</p>

<p><b>Void elements</b> can never have content, so they have no closing
tag: <code>area</code>, <code>base</code>, <code>br</code>,
<code>col</code>, <code>embed</code>, <code>hr</code>,
<code>img</code>, <code>input</code>, <code>link</code>,
<code>meta</code>, <code>source</code>, <code>track</code>,
<code>wbr</code>. Writing <code>&lt;br&gt;&lt;/br&gt;</code> is wrong;
<code>&lt;br/&gt;</code> (self-closing slash) is tolerated but means
nothing in HTML — it's an XHTML habit.</p>

<p><b>Optional tags</b>: famously, you may omit
<code>&lt;html&gt;</code>, <code>&lt;head&gt;</code>,
<code>&lt;body&gt;</code>, a table's <code>&lt;tbody&gt;</code>, a
paragraph's closing <code>&lt;/p&gt;</code> (before another
<code>&lt;p&gt;</code> or a block element), a list's final
<code>&lt;/li&gt;</code>... and the parser builds the full tree anyway:</p>

<pre class="code">&lt;!DOCTYPE html&gt;
&lt;title&gt;Minimal&lt;/title&gt;
&lt;p&gt;This parses into a complete
   html/head/body document!</pre>

<p>The parser never draws a wrong tree from this snippet: the title
lands in an implied head, the paragraph in an implied body, and html
wraps both. Every "missing" tag was implicit in context — the DOM comes
out complete.</p>

<p>Fun — and a trap. The omitted tags exist because their presence is
<i>implied by context</i>, and the parser applies exact rules (an
<code>&lt;/p&gt;</code> is implied before a following
<code>&lt;h1&gt;</code>). But implied structure is structure you can't
see, and one surprise (a div inside that paragraph!) changes where the
parser closes things. Professional markup writes the tags — the
optional ones are great for reading code, poor for writing it.</p>

<p>Gotcha: tooling disagrees with cleverness — XML pipelines and many
build tools require explicit closing, and diff-friendly code benefits
from visible structure. Write <code>&lt;/p&gt;</code>,
<code>&lt;/li&gt;</code>, <code>&lt;/html&gt;</code> even when you could
skip them: zero ambiguity for humans, parsers and validators alike. The
omission you'll meet anyway: browsers insert <code>&lt;tbody&gt;</code>
whether you wrote it or not — a selector bug waiting for anyone who
forgets.</p>
""",
            },
            {
                "title": "Character References",
                "html": """
<p>Some characters are <b>reserved</b> (they're markup syntax) and some
are just hard to type. <b>Character references</b> let you include
either, safely:</p>

<ul>
<li><b>Named</b>: <code>&amp;lt;</code> → &lt;, <code>&amp;gt;</code> →
&gt;, <code>&amp;amp;</code> → &amp;, <code>&amp;quot;</code> → ",
<code>&amp;nbsp;</code> → non-breaking space, <code>&amp;copy;</code> →
©</li>
<li><b>Decimal</b>: <code>&amp;#169;</code> → ©</li>
<li><b>Hexadecimal</b>: <code>&amp;#x1F40D;</code> → 🐍 (yes, emoji are
code points too)</li>
</ul>

<pre class="code">&lt;p&gt;5 &amp;lt; 10 &amp;amp; 10 &amp;gt; 5&lt;/p&gt;
&lt;p&gt;© 2026 — made with &amp;#x2665;&lt;/p&gt;</pre>

<p>Read the block: the first paragraph renders "5 &lt; 10 &amp;&amp; 10
&gt; 5" — the references told the parser these are text, not markup;
without them the <code>&lt;</code> would open a phantom tag and swallow
the rest of the line. The second renders © and the heart straight from
code points, no font trickery involved.</p>

<p>The reserved four matter most: a literal <code>&lt;</code> in text
starts a tag as far as the parser cares, so code samples, math
(<code>a &lt; b</code>) and any raw angle bracket must be escaped.
That is exactly why this course's code listings write
<code>&amp;lt;stdio.h&gt;</code> — the lesson source is HTML, and the
displayed angle brackets are references.</p>

<p><code>&amp;nbsp;</code> deserves a warning: it's for meaningful
non-breaking spaces ("10&nbsp;km"), not for making gaps — layout space
is CSS's job, and nbsp-chains are a screen-reader stumble.</p>

<p>And remember the deeper rule: the file itself is Unicode text — save
it as UTF-8 and declare <code>&lt;meta charset="utf-8"&gt;</code>, and
most accented letters need no references at all.</p>

<p>Gotcha: escape <b>late and locally</b>. Write plain UTF-8 text in your
source and reach for references only where meaning demands them
(<code>&amp;lt;</code>, <code>&amp;amp;</code>,
<code>&amp;nbsp;</code>). Pages stuffed with <code>&amp;copy;</code> and
numeric refs for every accented é are unreadable in the source and
error-prone to maintain; with the charset declared, you simply type the
letter.</p>
""",
                "tryit": """<!DOCTYPE html>
<html lang="en">
<head><title>Character references</title></head>
<body>
  <p>Escaping the reserved four: 5 &lt; 10 &amp;&amp; 10 &gt; 5</p>
  <p>To write the tag literally in text: &amp;lt;img&amp;gt;</p>
  <p>Symbols: &copy; 2026 &mdash; made with &#x2665; by &#x1F40D;</p>
  <p>Non-breaking space joins: 10&nbsp;km&nbsp;away</p>
</body>
</html>
""",
            },
            {
                "title": "MIME Types & HTML vs XML",
                "html": """
<p>Two ideas from the wider web ecosystem that every HTML author should
recognise.</p>

<p><b>MIME types</b> — when a server sends a file, it labels what the
bytes are: <code>text/html</code> for HTML documents,
<code>text/css</code>, <code>application/javascript</code>,
<code>image/png</code>, <code>application/json</code>. The browser
trusts this label over file extensions — that's why a badly configured
server serving HTML as <code>text/plain</code> shows source code, and
why the <code>&lt;script type=...&gt;</code> and
<code>&lt;source type=...&gt;</code> attributes you've met exist: they
let the browser skip formats it can't play <i>before</i> downloading.</p>

<p><b>HTML vs XML</b> — two syntax dialects of markup with opposite
personalities:</p>

<ul>
<li><b>HTML</b> — forgiving: optional tags, case-insensitive, unclosed
elements recovered, quotes optional. Built for humans.</li>
<li><b>XML (and XHTML)</b> — strict: every tag closed, everything
lowercase, all attributes quoted, one root element, case-sensitive.
A single error and an XML parser <b>refuses the whole document</b>.
Built for machines.</li>
</ul>

<p>Once upon a time the web tried to migrate to XHTML
(<code>&lt;!DOCTYPE html PUBLIC ...&gt;</code>, self-closing
<code>&lt;br /&gt;</code>) — and it failed for exactly that reason: one
stray <code>&amp;</code> and the page turned into a yellow error screen.
HTML5 absorbed the good parts (lowercase conventions, optional
self-closing style on void elements) without the fragility.</p>

<p>The strict-syntax habit is still worth keeping: it costs nothing,
reads cleanly, and makes your HTML trivially convertible when a machine
needs it (XML tooling, JSX-adjacent frameworks).</p>
""",
            },
            {
                "title": "Conformance, Validation & Obsolete Features",
                "html": """
<p>A document <b>conforms</b> when it follows the HTML standard: valid
nesting (content models), allowed attributes, required bits
(<code>DOCTYPE</code>, <code>title</code>, <code>lang</code> on
<code>html</code>). Browsers don't enforce this — they recover from
everything — which is why <b>validation</b> is a separate, voluntary
act.</p>

<p>The tool: the <b>W3C Markup Validator</b> (validator.w3.org). Paste a
URL or file and it lists real spec violations: unclosed elements,
invalid nesting, deprecated attributes, missing alt. Treat it like a
linter — run it when something renders strangely and before shipping;
it catches problems browsers forgive silently and designers never
see.</p>

<p><b>Obsolete &amp; deprecated features</b> — things old HTML had that
the standard has removed (browsers still render many, out of mercy for
the web's backlog):</p>

<ul>
<li>Presentational tags: <code>&lt;font&gt;</code>,
<code>&lt;center&gt;</code>, <code>&lt;big&gt;</code>,
<code>&lt;marquee&gt;</code> (RIP), <code>&lt;blink&gt;</code> (never
standard, mercifully)</li>
<li>Presentational attributes: <code>bgcolor</code>,
<code>align</code>, <code>border</code> on most elements — styling
moved to CSS</li>
<li><code>&lt;frame&gt;</code>/<code>&lt;frameset&gt;</code> — replaced by
iframes and layout</li>
<li><code>&lt;applet&gt;</code>, <code>&lt;acronym&gt;</code> (use
<code>&lt;abbr&gt;</code>)</li>
</ul>

<p>The pattern behind every removal: <b>structure stayed in HTML;
presentation moved to CSS; behaviour belongs to JavaScript.</b> When
you feel the urge to reach for a presentational attribute — that urge
is a CSS job.</p>

<p>This roadmap's end is really a beginning: HTML + the DOM + the APIs
you met are the platform everything else — CSS mastery, JavaScript
frameworks, PWAs — builds on. MDN will be there for the details;
you now speak the language.</p>
""",
                "tryit": """<!DOCTYPE html>
<html lang="en">
<head><title>Old vs modern HTML</title>
<style>
  body { font-family: sans-serif; }
  .old, .modern { padding: 10px; margin: 8px 0; }
  .old { background: #ffe8e0; border: 2px dashed #c0392b; }
  .modern { background: #eaf7f0; border: 2px solid #2e8b57; }
</style></head>
<body>
  <!-- Obsolete: presentational markup (still renders, but don't!) -->
  <div class="old">
    <font color="#c0392b" size="4"><b>1998 style:</b>
      &lt;font&gt; and &lt;b&gt; and bgcolor attributes…</font>
    <div align="center">centered with align="center"</div>
  </div>

  <!-- Modern: structure + CSS -->
  <div class="modern">
    <strong>2026 style:</strong> semantic elements,
    classes, and one style sheet doing the styling.
    <div style="text-align:center">centered with CSS</div>
  </div>
</body>
</html>
""",
            },
        ],
        "quiz": [
            {
                "type": "mc",
                "question": "Putting a <code>&lt;div&gt;</code> inside a <code>&lt;p&gt;</code> causes:",
                "options": [
                    "A validation warning only",
                    "The parser to close the paragraph early, splitting it",
                    "The div to become inline",
                    "Nothing — it's fine",
                ],
                "answer": 1,
                "explain": "p allows only phrasing content; a flow element closes it — the classic mystery-gap bug.",
            },
            {
                "type": "blank",
                "question": "The reference for a non-breaking space is <code>&amp;____;</code>.",
                "answers": ["nbsp"],
                "explain": "&nbsp; joins words without a break — for meaning, not for layout gaps.",
            },
            {
                "type": "mc",
                "question": "A server sends an HTML file with MIME type text/plain. The browser will:",
                "options": [
                    "Render the page normally",
                    "Show the source as plain text",
                    "Download the file",
                    "Guess and render anyway",
                ],
                "answer": 1,
                "explain": "The browser trusts the MIME label — text/plain means display as text.",
            },
            {
                "type": "mc",
                "question": "Which was REMOVED from the HTML standard?",
                "options": ["&lt;article&gt;", "&lt;font&gt;", "&lt;template&gt;", "&lt;dialog&gt;"],
                "answer": 1,
                "explain": "Presentational tags like <font> are obsolete — styling belongs to CSS.",
            },
        ],
    },
]
