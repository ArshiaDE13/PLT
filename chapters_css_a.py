"""CSS Tutor chapters 1-7 (Phases 1-2), grounded in MDN Web Docs."""

CHAPTERS_CSS_A = [
    # ------------------------------------------------------------------ cs01
    {
        "id": "cs01",
        "title": "Introduction to CSS",
        "emoji": "🌱",
        "lessons": [
            {
                "title": "What is CSS?",
                "html": """
<p><b>CSS (Cascading Style Sheets)</b> is a stylesheet language that
describes the <b>presentation</b> of a document written in HTML (or XML,
SVG...). MDN puts it plainly: HTML defines the structure and meaning;
CSS describes how elements should be rendered <i>on screen, on paper, in
speech, or on other media</i>.</p>

<p>One vocabulary note that surprises everyone: there will never be a
"CSS3" or "CSS4". CSS is one language, developed as
<b>independently-versioned modules</b> — CSS Color Module Level 5, CSS
Grid Layout Level 2 — so browsers implement features one module at a
time. It's just "CSS".</p>

<p>The superpower CSS gives you: <b>one style sheet can dress thousands
of pages</b>. Change a value in one place, and every heading, every
button, every card across the whole site updates. That separation —
structure in HTML, presentation in CSS — is what makes the web
maintainable.</p>

<p>In this course you style real pages in the live preview — every
lesson's Try-it box is a working document waiting for your CSS.</p>
""",
                "tryit": """<!DOCTYPE html>
<html lang="en">
<head><title>Your first CSS</title>
<style>
  body {
    font-family: sans-serif;
    background: #eef6ff;
  }
  h1 {
    color: #1572b6;
    border-bottom: 3px solid #33a9dc;
  }
  p {
    color: #445;
  }
</style>
</head>
<body>
  <h1>Styled by CSS</h1>
  <p>This page has <em>zero</em> inline styling — everything you see
     comes from the &lt;style&gt; block in the head.</p>
  <p>Change <code>#1572b6</code> to another colour and press Run!</p>
</body>
</html>
""",
            },
            {
                "title": "Syntax, Rules & Comments",
                "html": """
<p>CSS is made of <b>rulesets</b>. Each rule has two parts — a
<b>selector</b> that says <i>what</i> to style, and a <b>declaration
block</b> that says <i>how</i>:</p>

<pre class="code">h1                          ← selector
{                           ← open the declaration block
  color: #1572b6;           ← declaration: property: value;
  font-size: 2rem;
}                           ← close</pre>

<p>The anatomy, per MDN:</p>

<ul>
<li><b>Selector</b> — targets the element(s) to style (next chapter is
all about them)</li>
<li><b>Property</b> — the aspect being styled: <code>color</code>,
<code>font-size</code>, <code>padding</code>... (hundreds exist)</li>
<li><b>Value</b> — what to set it to: a colour, a length, a keyword,
a function</li>
<li><b>Declaration</b> — a <code>property: value;</code> pair, separated
by semicolons</li>
</ul>

<p>Comments wrap in <code>/* ... */</code> — the only comment syntax CSS
has, and it can span lines:</p>

<pre class="code">/* Brand colours — do not edit without design */
.card {
  color: #333;          /* text */
  /* padding: 1rem;     ← disabled for now */
}</pre>

<p>Mistakes are forgiving but silent: a missing semicolon or a misspelled
property doesn't error — the browser just skips that one declaration and
carries on. When a style mysteriously "doesn't apply", check the
spelling and the semicolons first.</p>
""",
                "tryit": """<!DOCTYPE html>
<html lang="en">
<head><title>Anatomy of a rule</title>
<style>
  /* One rule per element, many declarations per rule */
  body { font-family: sans-serif; }
  h1 {
    color: white;
    background: #1572b6;
    padding: 12px 18px;
    border-radius: 8px;
  }
  .muted {
    /* this class styles two elements below */
    color: #778;
    font-style: italic;
  }
</style>
</head>
<body>
  <h1>Anatomy of a rule</h1>
  <p class="muted">Selector → declarations → result.</p>
  <p class="muted">Try adding <code>letter-spacing: 2px;</code> to the h1 rule.</p>
</body>
</html>
""",
            },
            {
                "title": "Three Ways to Add CSS",
                "html": """
<p>CSS reaches a page through three doors:</p>

<p><b>1. External stylesheet</b> — a separate <code>.css</code> file
linked from the head. <i>The</i> professional choice: cached across
pages, shared by the whole site:</p>

<pre class="code">&lt;head&gt;
  &lt;link rel="stylesheet" href="styles.css"&gt;
&lt;/head&gt;</pre>

<p><b>2. Internal stylesheet</b> — a <code>&lt;style&gt;</code> block in
the head. All the styling lives in the document itself; good for
single-page demos (and every Try-it in this course!):</p>

<pre class="code">&lt;head&gt;
  &lt;style&gt;
    p { color: #1572b6; }
  &lt;/style&gt;
&lt;/head&gt;</pre>

<p><b>3. Inline styles</b> — a <code>style</code> attribute on one
element. The most specific and the least maintainable; reserve it for
one-off exceptions (or JavaScript-generated values):</p>

<pre class="code">&lt;p style="color: crimson"&gt;Just this one&lt;/p&gt;</pre>

<p>When all three target the same element, the <b>cascade</b> decides
(its own chapter — short version: inline beats internal beats...
well, it's more interesting than that, and specificity sits in the
middle).</p>
""",
                "tryit": """<!DOCTYPE html>
<html lang="en">
<head><title>Three doors</title>
<style>
  /* INTERNAL stylesheet: styles every p on the page */
  p { color: #1572b6; }
</style>
</head>
<body>
  <h1>Three doors to CSS</h1>
  <p>This paragraph is styled by the internal &lt;style&gt; block.</p>

  <!-- INLINE style: wins over the internal sheet for this element only -->
  <p style="color: #c73c1a">This paragraph has an inline style.</p>

  <p>In a real site you would use an external .css file with
     &lt;link rel="stylesheet"&gt;.</p>
</body>
</html>
""",
            },
        ],
        "quiz": [
            {
                "type": "mc",
                "question": "In the rule <code>p { color: navy; }</code>, what is <code>color</code>?",
                "options": ["A selector", "A property", "A value", "A comment"],
                "answer": 1,
                "explain": "p is the selector; color is the property; navy is its value — together a declaration.",
            },
            {
                "type": "blank",
                "question": "CSS comments are written between <code>/*</code> and <code>____</code>.",
                "answers": ["*/"],
                "explain": "/* ... */ is the only comment syntax CSS has.",
            },
            {
                "type": "mc",
                "question": "Which way of adding CSS is recommended for a whole site?",
                "options": [
                    "Inline style attributes",
                    "An external .css file via &lt;link&gt;",
                    "A &lt;style&gt; block per page",
                    "Copying styles into each element",
                ],
                "answer": 1,
                "explain": "External sheets are cached, shared across pages, and keep presentation out of markup.",
            },
            {
                "type": "mc",
                "question": "A declaration is missing its semicolon. What happens?",
                "options": [
                    "The page fails to load",
                    "The browser shows an error",
                    "That declaration (and possibly the next) is silently ignored",
                    "The whole stylesheet is rejected",
                ],
                "answer": 2,
                "explain": "CSS fails silently per-declaration — the top cause of 'my style won't apply'.",
            },
        ],
    },

    # ------------------------------------------------------------------ cs02
    {
        "id": "cs02",
        "title": "Selectors",
        "emoji": "🎯",
        "lessons": [
            {
                "title": "Basic Selectors",
                "html": """
<p>Selectors answer the only question that matters: <i>which elements get
this style?</i> The four foundational types:</p>

<pre class="code">p              type selector — every &lt;p&gt;
.card          class selector — every element with class="card"
#header        ID selector — the one element with id="header"
*              universal selector — everything</pre>

<ul>
<li><b>Type</b> — broad strokes: base typography, reset styles</li>
<li><b>Class</b> — the workhorse of real projects: reusable categories,
combinable (<code>class="card featured"</code>), many elements per
class</li>
<li><b>ID</b> — one exact element per page; powerful but brittle for
styling (its high specificity bites later — see the Cascade
chapter)</li>
<li><b>Universal</b> — everything; mostly seen in resets like
<code>* { box-sizing: border-box }</code></li>
</ul>

<p>You can also chain and group. Chaining tightens (no space!):
<code>p.featured</code> = a <code>p</code> that <i>also</i> has class
<code>featured</code>. Grouping shares one rule across selectors with
commas:</p>

<pre class="code">h1, h2, h3 {
  font-family: Georgia, serif;
  color: #1572b6;
}</pre>
""",
                "tryit": """<!DOCTYPE html>
<html lang="en">
<head><title>Basic selectors</title>
<style>
  body { font-family: sans-serif; }
  p        { color: #445; }
  .card    { background: #eaf4fd; border: 2px solid #33a9dc;
             border-radius: 8px; padding: 10px 14px; margin: 8px 0; }
  #special { color: white; background: #1572b6; }
  p.featured { font-weight: bold; }
  h1, h2   { color: #1572b6; }
</style>
</head>
<body>
  <h1>Selector zoo</h1>
  <p>A plain paragraph (type selector).</p>
  <div class="card">A .card (class selector).</div>
  <p class="card featured">A p AND .card AND .featured — all three apply!</p>
  <div class="card" id="special">The one #special element.</div>
</body>
</html>
""",
            },
            {
                "title": "Attribute Selectors",
                "html": """
<p>Elements can be selected by their <b>attributes</b> — any attribute —
with and without value matching. The operators:</p>

<pre class="code">[disabled]                 has the attribute at all
[type="checkbox"]          exact value
[href^="https"]            value STARTS with "https"
[href$=".pdf"]             value ENDS with ".pdf"
[title*="CSS"]             value CONTAINS "CSS"
[lang|="fa"]               value is "fa" or starts with "fa-"</pre>

<p>The prefix/suffix/contains operators are why attribute selectors are
the link-styler's best friend — file-type icons without a single class:</p>

<pre class="code">a[href^="http"]::after { content: " ↗"; }      external links
a[href$=".pdf"]::after  { content: " 📄"; }    PDF links</pre>

<p>They also accept a third argument for case-insensitivity:
<code>[title*="css" i]</code> matches "CSS", "css", "Css"... Useful for
data attributes: <code>[data-state="open"]</code> is a common pattern in
component styling.</p>
""",
                "tryit": """<!DOCTYPE html>
<html lang="en">
<head><title>Attribute selectors</title>
<style>
  body { font-family: sans-serif; line-height: 2; }
  a[href^="http"]::after  { content: " ↗"; }
  a[href$=".pdf"]::after  { content: " 📄"; }
  a[href*="github"]        { color: #c73c1a; font-weight: bold; }
  [data-state="open"]      { background: #eaf4fd; }
  [type="checkbox"]        { accent-color: #1572b6; }
</style>
</head>
<body>
  <p><a href="https://developer.mozilla.org">MDN (external)</a></p>
  <p><a href="/files/report.pdf">Report (PDF)</a></p>
  <p><a href="https://github.com/mdn">MDN on GitHub (contains github)</a></p>
  <p data-state="open">This paragraph has data-state="open".</p>
  <p><label><input type="checkbox" checked> checkboxes get blue accents</label></p>
</body>
</html>
""",
            },
            {
                "title": "Combinators",
                "html": """
<p>Combinators express <b>relationships</b> between elements. Four of
them, from loosest to tightest:</p>

<pre class="code">A B      descendant  — B anywhere inside A
A &gt; B    child       — B is a DIRECT child of A
A + B    next sibling — B immediately follows A
A ~ B    siblings    — every B that follows A (same parent)</pre>

<pre class="code">.card p        { color: #445; }   any p inside .card, any depth
.card &gt; p      { color: #1572b6; } only direct p children
h2 + p         { font-style: italic; }  the paragraph right after an h2
h2 ~ p         { border-top: 1px solid #ccc; }  later p siblings</pre>

<p>The difference between descendant and child matters in nested
structures: descendant reaches through any depth (grandchildren
included); child stops at one level. The sibling selectors power
"state affects neighbour" patterns — like styling a paragraph that
follows a heading, without classes.</p>

<p>And they chain: <code>ul.nav &gt; li &gt; a</code> = links that are
direct children of list items that are direct children of the nav
list.</p>
""",
                "tryit": """<!DOCTYPE html>
<html lang="en">
<head><title>Combinators</title>
<style>
  body { font-family: sans-serif; }
  .menu li        { list-style: none; }
  .menu > li      { font-weight: bold; }
  .menu > li > ul > li { font-weight: normal; color: #556; }
  h2 + p          { font-style: italic; color: #1572b6; }
  h2 ~ p          { border-top: 1px dashed #33a9dc; padding-top: 4px; }
</style>
</head>
<body>
  <ul class="menu">
    <li>Direct child (bold)
      <ul><li>Grandchild — NOT a direct child</li></ul>
    </li>
    <li>Another direct child</li>
  </ul>

  <h2>Heading</h2>
  <p>h2 + p: I immediately follow the heading.</p>
  <p>h2 ~ p: I'm a later sibling too.</p>
</body>
</html>
""",
            },
            {
                "title": "Pseudo-classes",
                "html": """
<p>A <b>pseudo-class</b> styles an element based on its <b>state or
position</b> — things markup can't express. One colon:</p>

<pre class="code">a:hover            mouse is over it
a:visited          already visited link
button:focus       has keyboard/click focus
input:disabled     is disabled
input:checked      is checked
li:first-child     first among its siblings
li:last-child      last among its siblings
li:nth-child(2n)   every 2nd child (even)
li:nth-child(3n+1) children 1, 4, 7, ...
p:not(.skip)       every p WITHOUT class skip</pre>

<p><code>nth-child()</code> is the star — zebra-striped tables and lists
in one line:</p>

<pre class="code">tbody tr:nth-child(odd) { background: #f2f8fe; }</pre>

<p>The functional pseudo-classes deserve special mention (their own
lesson below), but the everyday state set —
<code>:hover</code>, <code>:focus</code>, <code>:active</code>,
<code>:disabled</code>, <code>:checked</code> — is what makes interfaces
feel alive without a line of JavaScript.</p>
""",
                "tryit": """<!DOCTYPE html>
<html lang="en">
<head><title>Pseudo-classes</title>
<style>
  body { font-family: sans-serif; }
  button {
    padding: 8px 18px; border: 2px solid #1572b6; border-radius: 8px;
    background: white; color: #1572b6; cursor: pointer;
  }
  button:hover   { background: #eaf4fd; }
  button:active  { background: #1572b6; color: white; }
  button:focus   { outline: 3px solid #ffd43b; }

  li:nth-child(odd)  { background: #f2f8fe; }
  li:first-child     { font-weight: bold; }
  li:last-child      { color: #c73c1a; }
</style>
</head>
<body>
  <button>Hover, click & Tab me</button>
  <ul>
    <li>first-child (bold)</li>
    <li>nth-child(odd) — striped</li>
    <li>nth-child(odd) — striped</li>
    <li>last-child (red)</li>
  </ul>
</body>
</html>
""",
            },
            {
                "title": "Pseudo-elements",
                "html": """
<p>A <b>pseudo-element</b> styles a <b>part</b> of an element — or an
element that doesn't exist in markup at all. Two colons:</p>

<pre class="code">p::first-line    the first rendered line
p::first-letter  the first letter (drop caps!)
::selection      the highlight when text is selected
::placeholder    an input's placeholder text
::marker         a list item's bullet/number</pre>

<p>And the two most powerful — <b>::before and ::after</b> — which
<i>insert</i> a virtual child as the first/last content of the element,
via the <code>content</code> property:</p>

<pre class="code">.tag::before {
  content: "★ ";
  color: #f5a623;
}
a[href^="http"]::after {
  content: " ↗";
}
.quote::before { content: open-quote; }
.quote::after  { content: close-quote; }</pre>

<p>Rules of the road: <code>content</code> is <b>required</b> (use
<code>content: ""</code> for purely decorative boxes), the inserted
content is <b>not in the DOM</b> (screen readers may not read it — never
put essential text there), and everything else about them is normal CSS
— box model, positioning, backgrounds all work.</p>

<p>Decorative arrows, badges, overlays, custom checkboxes — half of
"advanced CSS" on the web is really ::before and ::after.</p>
""",
                "tryit": """<!DOCTYPE html>
<html lang="en">
<head><title>Pseudo-elements</title>
<style>
  body { font-family: sans-serif; }
  .tag { background: #eaf4fd; padding: 6px 12px; border-radius: 6px; }
  .tag::before { content: "★ "; color: #f5a623; }
  .quote::before { content: open-quote; color: #33a9dc; }
  .quote::after  { content: close-quote; color: #33a9dc; }
  p::first-letter { font-size: 1.6em; color: #1572b6; font-weight: bold; }
  ::selection { background: #ffd43b; }
</style>
</head>
<body>
  <p class="tag">This badge gets a star ::before.</p>
  <p class="quote">The browser adds my quotation marks.</p>
  <p>Every paragraph's first letter here is styled by ::first-letter.</p>
  <p>Select any text on this page — ::selection is gold.</p>
</body>
</html>
""",
            },
            {
                "title": ":is(), :where(), :has() & :not()",
                "html": """
<p>The modern <b>logical pseudo-classes</b> take a selector list as an
argument and compose — they turn long selector chains into readable
ones.</p>

<p><b><code>:not()</code></b> — everything except:</p>

<pre class="code">li:not(.done) { color: #333; }</pre>

<p><b><code>:is()</code></b> — matches any of the listed selectors; great
for deduplicating:</p>

<pre class="code">/* instead of: header a, main a, footer a { ... } */
:is(header, main, footer) a { color: #1572b6; }</pre>

<p><b><code>:where()</code></b> — identical to <code>:is()</code> with one
crucial difference: it contributes <b>zero specificity</b> (Cascade
chapter). Perfect for defaults that any real style should override.</p>

<p><b><code>:has()</code></b> — the long-awaited <b>parent selector</b>:
"an element that contains..." — styling based on what's <i>inside</i>:</p>

<pre class="code">/* a card that contains an image gets special padding */
.card:has(img) { padding: 0; }

/* a heading followed by a warning box */
h2:has(+ .warning) { color: #c0392b; }

/* form:highlight invalid state from the field INSIDE */
form:has(input:invalid) { border: 2px solid #c0392b; }</pre>

<p><code>:has()</code> unlocked decades of requested patterns — parent
styling, sibling lookahead — without JavaScript. MDN calls it one of the
most significant recent additions to CSS.</p>
""",
                "tryit": """<!DOCTYPE html>
<html lang="en">
<head><title>Logical selectors</title>
<style>
  body { font-family: sans-serif; }
  :is(h1, h2) { color: #1572b6; }

  .card { border: 2px solid #ccc; border-radius: 8px;
          padding: 12px; margin: 8px 0; }
  .card:has(img) { border-color: #1572b6; background: #f2f8fe; }

  li:not(.done) { font-weight: bold; }
  li.done { text-decoration: line-through; color: #999; }

  form:has(input:invalid) { border: 2px solid #c0392b; border-radius: 8px;
                            padding: 8px; }
</style>
</head>
<body>
  <h1>:is() styled this heading</h1>

  <div class="card">A card without an image.</div>
  <div class="card">
    <img src="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='80' height='50'%3E%3Crect width='80' height='50' fill='%2333a9dc'/%3E%3C/svg%3E"
         alt="placeholder" width="80">
    A card :has(img) — blue border!
  </div>

  <ul>
    <li>not .done → bold</li>
    <li class="done">done → struck through</li>
  </ul>

  <form>
    <label>Type 3+ chars: <input required minlength="3"></label>
  </form>
  <p>The form gets a red border while its input is :invalid — via :has().</p>
</body>
</html>
""",
            },
        ],
        "quiz": [
            {
                "type": "mc",
                "question": "Which selector targets the element with id=\"hero\"?",
                "options": [".hero", "#hero", "*hero", "hero"],
                "answer": 1,
                "explain": "# targets IDs; . targets classes; a bare word targets the element type.",
            },
            {
                "type": "mc",
                "question": "<code>.card &gt; p</code> selects:",
                "options": [
                    "Any p anywhere inside .card",
                    "Only p elements that are direct children of .card",
                    "The p right after .card",
                    "Every .card and every p",
                ],
                "answer": 1,
                "explain": "> = child combinator: one level deep only. A space (descendant) reaches any depth.",
            },
            {
                "type": "blank",
                "question": "The pseudo-class matching the mouse-over state is <code>:____</code>.",
                "answers": ["hover"],
                "explain": ":hover applies while the pointer is over the element.",
            },
            {
                "type": "mc",
                "question": "What makes :has() historic?",
                "options": [
                    "It is faster than other selectors",
                    "It styles a PARENT based on what's inside it",
                    "It works only in tables",
                    "It replaces classes",
                ],
                "answer": 1,
                "explain": ":has() is the parent selector — style the card because it contains an image, the form because a field is invalid.",
            },
            {
                "type": "mc",
                "question": ":where() differs from :is() in that it:",
                "options": [
                    "Matches more elements",
                    "Contributes zero specificity",
                    "Works only in media queries",
                    "Is not supported",
                ],
                "answer": 1,
                "explain": "Same matching, zero specificity — ideal for overridable defaults.",
            },
        ],
    },

    # ------------------------------------------------------------------ cs03
    {
        "id": "cs03",
        "title": "Cascade & Specificity",
        "emoji": "🌊",
        "lessons": [
            {
                "title": "The Cascade & Specificity",
                "html": """
<p>The C in CSS: when <b>multiple rules target the same element</b> with
conflicting values, something must decide. That something is the
<b>cascade</b> — and its main tie-breaker is <b>specificity</b>.</p>

<p>Specificity is a three-number score, counted per selector:</p>

<ul>
<li><b>IDs</b> — 1 point each: <code>#header</code></li>
<li><b>Classes / pseudo-classes / attributes</b> — 1 point each:
<code>.card</code>, <code>:hover</code>, <code>[type="text"]</code></li>
<li><b>Elements / pseudo-elements</b> — 1 point each: <code>p</code>,
<code>::before</code></li>
</ul>

<p>Written as (IDs, classes, elements):</p>

<pre class="code">p                    → (0, 0, 1)
.card                → (0, 1, 0)
p.card               → (0, 1, 1)
#nav .card &gt; a:hover → (1, 2, 1)   ← wins over everything above</pre>

<p>Compare left to right: more IDs beats any number of classes; more
classes beats any number of elements. <b>Inline
<code>style="..."</code></b> sits above all of them (a virtual fourth
column), and <code>!important</code> above that (its own lesson).</p>

<p>When scores are <b>equal</b>, the cascade falls back to source order:
<b>the later rule wins</b>. This is why reset sheets come first and
theme sheets come last — order is design.</p>
""",
                "tryit": """<!DOCTYPE html>
<html lang="en">
<head><title>Specificity showdown</title>
<style>
  p              { color: gray;  }   /* (0,0,1) */
  .message       { color: #1572b6; } /* (0,1,0) — beats the element */
  p.message      { color: #2e8b57; } /* (0,1,1) — beats .message */
  #banner        { color: #c0392b; } /* (1,0,0) — beats everything here */
</style>
</head>
<body>
  <p class="message">Which colour? (0,1,1) — p.message wins.</p>
  <p class="message" id="banner">This one has an ID: (1,0,0) wins!</p>
</body>
</html>
""",
            },
            {
                "title": "Inheritance & Computed Values",
                "html": """
<p>Some properties flow down the tree automatically — that's
<b>inheritance</b>. Set <code>color</code> on <code>body</code> and every
descendant inherits it; set <code>border</code> and nothing inherits it
(imagine every child of a bordered box growing its own border!).</p>

<ul>
<li><b>Inherited by default:</b> text-related properties —
<code>color</code>, <code>font-*</code>, <code>line-height</code>,
<code>letter-spacing</code>, <code>text-align</code>,
<code>visibility</code>, <code>list-style</code>...</li>
<li><b>Not inherited:</b> the box and layout properties —
<code>border</code>, <code>margin</code>, <code>padding</code>,
<code>background</code>, <code>width</code>, <code>display</code>...
(which would be chaos)</li>
</ul>

<p>Every property can be controlled explicitly with universal keywords:</p>

<pre class="code">.deep-child {
  color: inherit;    /* take the parent's value (the default for color) */
  border: inherit;   /* FORCE inheritance of a non-inherited property */
  color: initial;    /* back to the spec's default */
  color: unset;      /* inherit if naturally inherited, else initial */
}</pre>

<p>And the value an element finally renders with is its
<b>computed value</b>: the cascade picks the winner, relative units are
resolved, keywords become concrete numbers — <code>font-size:
2em</code> on a 16px parent computes to 32px. The devtools "Computed"
tab shows exactly this final state per element.</p>
""",
                "tryit": """<!DOCTYPE html>
<html lang="en">
<head><title>Inheritance</title>
<style>
  body { font-family: sans-serif; color: #1572b6;
         border: 2px solid #33a9dc; padding: 10px; }
  .boxed { border: 2px dashed #c73c1a; padding: 8px; }
  .inherit-border { border: inherit; padding: 8px; }
</style>
</head>
<body>
  <p>color inherits from body → blue. border does NOT → only the body
     has one.</p>
  <div class="boxed">
    This div sets its own border (red).
    <span class="inherit-border">This span uses border: inherit —
      it borrowed the red from its parent!</span>
  </div>
</body>
</html>
""",
            },
            {
                "title": "!important & Cascade Layers",
                "html": """
<p><b><code>!important</code></b> elevates a declaration above the normal
specificity game — above inline styles, above everything except another
!important:</p>

<pre class="code">.hidden-banner { display: none !important; }</pre>

<p>It exists for one legitimate purpose: <b>overriding styles you cannot
control</b> — user-agent defaults, third-party widget CSS, accessibility
user stylesheets. As a daily tool it's a trap: each !important forces
the next override to also be !important, and specificity wars escalate
until nobody can change anything. Exhaust every alternative — better
specificity, source order, layers — before reaching for it.</p>

<p>The modern alternative for structuring big stylesheets is
<b>cascade layers</b> (<code>@layer</code>) — an explicit ordering
system:</p>

<pre class="code">@layer reset, base, components, utilities;

@layer reset {
  * { margin: 0; }
}
@layer base {
  p { color: #333; }
}
@layer utilities {
  .text-blue { color: #1572b6 !important-ish; }  /* utilities beat base */
}</pre>

<p>Layer order is declared up front: later layers beat earlier ones
<b>regardless of specificity</b> — a one-class rule in
<code>utilities</code> beats a triple-ID rule in <code>base</code>.
Un-layered styles beat all layers, which keeps overrides simple.
MDN positions layers as the sane answer to the "which of my 4000 rules
wins" problem; they get their own Advanced chapter later.</p>
""",
            },
        ],
        "quiz": [
            {
                "type": "mc",
                "question": "Rank: which selector wins?",
                "options": ["p", ".card", "#nav .card", "p.card"],
                "answer": 2,
                "explain": "#nav .card = (1,1,0) — one ID beats any number of classes/elements.",
            },
            {
                "type": "mc",
                "question": "Two rules with EQUAL specificity — which wins?",
                "options": ["The first in the stylesheet", "The last in the stylesheet", "A random one", "Both apply partially"],
                "answer": 1,
                "explain": "Source order is the tie-breaker: later rule wins.",
            },
            {
                "type": "blank",
                "question": "The property-category that flows from parent to child (like color and font) is said to be ____.",
                "answers": ["inherited", "inheritable", "inherited by default"],
                "explain": "Text properties inherit; box/layout properties don't.",
            },
            {
                "type": "mc",
                "question": "When is !important appropriate?",
                "options": [
                    "For every rule, to be safe",
                    "Overriding styles you can't control (third-party CSS, UA defaults)",
                    "Only in inline styles",
                    "Never",
                ],
                "answer": 1,
                "explain": "It's an escape hatch for foreign CSS — daily use starts specificity wars.",
            },
            {
                "type": "mc",
                "question": "With cascade layers, a rule in a LATER layer beats an earlier layer's rule:",
                "options": [
                    "only if it has higher specificity",
                    "regardless of specificity",
                    "only with !important",
                    "never",
                ],
                "answer": 1,
                "explain": "Layer order outranks specificity — that's the whole point of @layer.",
            },
        ],
    },
]
