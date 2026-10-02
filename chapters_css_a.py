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
<p>Open any web page with its CSS stripped away and you get plain black
text on a white background, blue underlined links, default fonts
everywhere. <b>CSS (Cascading Style Sheets)</b> is the language that
turns that skeleton into a designed page — it describes the
<b>presentation</b> of an HTML (or XML, SVG...) document: colours,
spacing, fonts, layout. MDN puts the division of labour plainly: HTML
defines the structure and meaning; CSS describes how elements should be
rendered <i>on screen, on paper, in speech, or on other media</i>.</p>

<p>Why does the separation matter to you? Because <b>one style sheet can
dress thousands of pages</b>. Your site has one <code>h1</code> rule;
change its colour in one place and every heading on every page updates.
Bake that styling into the HTML instead and a rebrand means editing
every file you own. Structure in HTML, presentation in CSS — that split
is what makes the web maintainable.</p>

<p>A vocabulary note that surprises everyone: there will never be a
"CSS3" or "CSS4". CSS grows as <b>independently-versioned modules</b> —
CSS Color Module Level 5, CSS Grid Layout Level 2 — and browsers
implement features one module at a time. It's all just "CSS".</p>

<p>How does the browser actually use your rules? It parses each rule,
matches the <b>selector</b> against the elements in the page, and paints
the winning declarations — when two rules disagree, the cascade decides
(chapter 3). Try it now: every lesson in this course ships a working
Try-it box. Predict the result first, press Run second — that habit will
teach you faster than any reading.</p>
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
<p>Every stylesheet you will ever write is built from one shape: the
<b>ruleset</b>. Learn this one shape and you can read any CSS file on
earth. A rule has two halves — a <b>selector</b> saying <i>what</i> to
style, and a <b>declaration block</b> saying <i>how</i>. Watch it being
assembled:</p>

<pre class="code">h1                          ← selector
{                           ← open the declaration block
  color: #1572b6;           ← declaration: property: value;
  font-size: 2rem;
}                           ← close</pre>

<p>Read it top to bottom: <code>h1</code> tells the browser which
elements to find; inside the braces, each line is one <b>declaration</b>
— a <code>property: value;</code> pair. This rule says "every
<code>&lt;h1&gt;</code> gets brand-blue text at twice the base size."
The vocabulary, per MDN: the <b>selector</b> targets elements; the
<b>property</b> names an aspect you can style (<code>color</code>,
<code>font-size</code>, <code>padding</code> — hundreds exist); the
<b>value</b> is what to set it to. Semicolons separate declarations; the
final one is optional, but keep it — a missing one is the top beginner
bug.</p>

<p>Stylesheets also need notes for humans. CSS has exactly one comment
syntax, <code>/* ... */</code>, and it spans lines:</p>

<pre class="code">/* Brand colours — do not edit without design */
.card {
  color: #333;          /* text */
  /* padding: 1rem;     ← disabled for now */
}</pre>

<p>The first comment documents intent for teammates. The last line shows
the second use: <b>commenting out</b> a declaration you're not ready to
delete — a debugging habit you'll use daily. The browser skips the
commented padding and applies only the colour.</p>

<p>Gotcha: CSS fails <b>silently</b>. Misspell <code>colour</code> or
drop a semicolon and there is no error message — the browser skips that
one declaration and carries on. When a style mysteriously "doesn't
apply", check spelling and semicolons before anything else.</p>
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
<p>Your CSS can reach a page through three doors, and picking the right
door for the situation is a professional skill.</p>

<p><b>1. External stylesheet</b> — a separate <code>.css</code> file
linked from the head. <i>The</i> professional choice: the browser
downloads it once and caches it for every page of your site:</p>

<pre class="code">&lt;head&gt;
  &lt;link rel="stylesheet" href="styles.css"&gt;
&lt;/head&gt;</pre>

<p>One <code>&lt;link&gt;</code> tag, one file, a thousand pages sharing
it. Change <code>styles.css</code> and the whole site updates — the
"one sheet dresses thousands of pages" power from lesson 1, in its
purest form.</p>

<p><b>2. Internal stylesheet</b> — a <code>&lt;style&gt;</code> block in
the head. All the styling lives in the document itself; good for
single-page demos — and every Try-it in this course uses exactly
this:</p>

<pre class="code">&lt;head&gt;
  &lt;style&gt;
    p { color: #1572b6; }
  &lt;/style&gt;
&lt;/head&gt;</pre>

<p>Read the block as: "these rules apply to this document only". Copy
the page elsewhere and the styling travels with it — which is exactly
why it's wrong for a multi-page site: fifty pages would carry fifty
copies.</p>

<p><b>3. Inline styles</b> — a <code>style</code> attribute on one
element. The most specific and the least maintainable:</p>

<pre class="code">&lt;p style="color: crimson"&gt;Just this one&lt;/p&gt;</pre>

<p>The style is welded to a single tag: reusable nowhere, invisible to
cached sheets, painful to override. Reserve it for one-off exceptions
(or JavaScript-generated values).</p>

<p>Rule of thumb: external by default, internal for quick demos, inline
almost never. When several doors target the same element, the
<b>cascade</b> decides who wins — short version: inline beats internal,
and the full story (specificity!) gets its own chapter 3.</p>
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
<p>Selectors answer the only question that matters in CSS: <i>which
elements get this style?</i> You write a rule; the selector is the
address label the browser uses to find its targets. Four foundational
types cover most of your daily work:</p>

<pre class="code">p              type selector — every &lt;p&gt;
.card          class selector — every element with class="card"
#header        ID selector — the one element with id="header"
*              universal selector — everything</pre>

<p>Walk through them. The <b>type</b> selector matches by tag name —
write <code>p</code> and every paragraph changes: broad strokes like
base typography and resets. The <b>class</b> selector matches every
element carrying <code>class="card"</code> — the workhorse of real
projects because it's reusable (fifty elements can share it) and
combinable (<code>class="card featured"</code>). The <b>ID</b> selector
targets the single element with that id — powerful but brittle for
styling, because its high specificity bites later (chapter 3). The
<b>universal</b> selector <code>*</code> matches everything; you'll
mostly meet it in resets like <code>* { box-sizing: border-box }</code>.</p>

<p>Selectors also compose. <b>Chaining</b> (no space!) narrows:
<code>p.featured</code> matches only a <code>p</code> that <i>also</i>
has class <code>featured</code>. <b>Grouping</b> shares one rule across
different selectors with commas — same declarations, several
targets:</p>

<pre class="code">h1, h2, h3 {
  font-family: Georgia, serif;
  color: #1572b6;
}</pre>

<p>Read the grouped rule as "headings 1 through 3 all get Georgia and
the brand blue" — one edit now maintains all three. Predict the Try-it
before you run it: which elements turn blue, and which plain paragraph
stays default?</p>

<p>Gotcha: class and id values are case-sensitive, and a chained
selector with an accidental space becomes a different selector
entirely (a descendant — next lesson). When a class rule "doesn't
work", first check the spelling matches the HTML exactly.</p>
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
<p>Classes aren't the only handle on an element. <b>Attribute
selectors</b> match elements by <i>any</i> attribute they carry —
<code>href</code>, <code>type</code>, <code>disabled</code>, your own
<code>data-*</code> attributes — with or without checking the value.
The problem they solve: styling based on information the markup already
has, no extra classes required.</p>

<pre class="code">[disabled]                 has the attribute at all
[type="checkbox"]          exact value
[href^="https"]            value STARTS with "https"
[href$=".pdf"]             value ENDS with ".pdf"
[title*="CSS"]             value CONTAINS "CSS"
[lang|="fa"]               value is "fa" or starts with "fa-"</pre>

<p>Six operators, six questions. The first only asks "does the attribute
exist?" — <code>[disabled]</code> hits anything you can't interact
with. The second checks exact equality. Then the substring operators:
<code>^=</code> (starts with), <code>$=</code> (ends with), <code>*=</code>
(contains). Those three are why attribute selectors are the
link-styler's best friend — file-type icons without a single class:</p>

<pre class="code">a[href^="http"]::after { content: " ↗"; }      external links
a[href$=".pdf"]::after  { content: " 📄"; }    PDF links</pre>

<p>Predict the render before you run the Try-it: every link whose
<code>href</code> begins with <code>http</code> grows an arrow after
its text; every link ending in <code>.pdf</code> grows a page icon.
The browser inspects attribute values at render time — zero markup
changes, and a newly added PDF link gets its icon automatically.</p>

<p>Two refinements. Append <code>i</code> for case-insensitive
matching: <code>[title*="css" i]</code> matches "CSS", "css",
"Css"... And a modern idiom is selecting by state data:
<code>[data-state="open"]</code> is the common component-styling
pattern. Gotcha: attribute selectors carry class-level specificity
(0,1,0) — as easy to collide as classes, so keep the matched values
as exact as the markup allows.</p>
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
<p>Real pages are trees: elements inside elements inside elements.
<b>Combinators</b> let a selector describe those <b>relationships</b> —
"style this, but only when it sits inside / next to that". Four of
them, from loosest to tightest:</p>

<pre class="code">A B      descendant  — B anywhere inside A
A &gt; B    child       — B is a DIRECT child of A
A + B    next sibling — B immediately follows A
A ~ B    siblings    — every B that follows A (same parent)</pre>

<p>Note that the space in <code>A B</code> is itself a combinator. Now
watch the differences in code — these four rules all touch paragraphs,
but they disagree about <i>which</i> paragraphs:</p>

<pre class="code">.card p        { color: #445; }   any p inside .card, any depth
.card &gt; p      { color: #1572b6; } only direct p children
h2 + p         { font-style: italic; }  the paragraph right after an h2
h2 ~ p         { border-top: 1px solid #ccc; }  later p siblings</pre>

<p>Descendant reaches through <i>any</i> depth — grandchildren
included; child stops at one level. So if a card's paragraph is wrapped
in an inner <code>div</code>, <code>.card p</code> still finds it but
<code>.card &gt; p</code> does not. That one-glyph difference
(<code> </code> vs <code>&gt;</code>) is a classic "why did my style
stop working?" — someone added a wrapper div and the child selector
lost its target.</p>

<p>The sibling selectors power "state affects neighbour" patterns —
styling a paragraph that follows a heading, without classes:
<code>h2 + p</code> hits only the paragraph <i>immediately</i> after
the heading; <code>h2 ~ p</code> hits every later paragraph sibling.
And combinators chain: <code>ul.nav &gt; li &gt; a</code> = links that
are direct children of list items that are direct children of the nav
list.</p>

<p>Gotcha: every relationship you add raises specificity and fragility.
When the nesting is an accident of markup rather than a meaning, prefer
a plain class.</p>
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
<p>Markup says what an element <i>is</i>; it cannot say what is
<i>happening</i> to it. A <b>pseudo-class</b> styles an element based on
its <b>state or position</b> — hovered, focused, first in its list.
Syntactically it's a colon attached to a selector:</p>

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

<p>Two families live in that list. The <b>state</b> family
(<code>:hover</code>, <code>:focus</code>, <code>:active</code>,
<code>:disabled</code>, <code>:checked</code>) switches on and off as
the user interacts — it's what makes interfaces feel alive without a
line of JavaScript. The <b>position</b> family
(<code>:first-child</code>, <code>:nth-child()</code>...) depends on
where the element sits among its siblings. <code>nth-child()</code> is
the star: it takes an "an+b" pattern — <code>2n</code> picks children
2, 4, 6..., and the keyword <code>odd</code> does the same. Zebra-striping
a table in one line:</p>

<pre class="code">tbody tr:nth-child(odd) { background: #f2f8fe; }</pre>

<p>Every odd row paints pale blue; even rows keep the default. Delete a
row and the striping re-computes — the browser tracks positions, not
your markup, so the CSS never needs updating.</p>

<p>Gotchas: <code>:hover</code> doesn't exist on touch screens — never
hide essential information behind hover only. And link states have
equal specificity, so source order decides: write them in the LVHA
order <code>:link</code>, <code>:visited</code>, <code>:hover</code>,
<code>:active</code>, or a later rule will shadow your hover style
(chapter 3 explains why).</p>
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
<p>A <b>pseudo-element</b> styles a <b>part</b> of an element — its
first line, first letter, selected text — or conjures an element that
doesn't exist in markup at all. Two colons distinguish them from
pseudo-classes:</p>

<pre class="code">p::first-line    the first rendered line
p::first-letter  the first letter (drop caps!)
::selection      the highlight when text is selected
::placeholder    an input's placeholder text
::marker         a list item's bullet/number</pre>

<p>Each targets a sub-part the DOM doesn't contain —
<code>p::first-letter</code> follows the text, so if the paragraph's
first word changes, the styled letter changes with it. The two most
powerful pseudo-elements, though, don't style existing parts: they
<i>insert</i> a virtual child as the first or last content of the
element, via the <code>content</code> property:</p>

<pre class="code">.tag::before {
  content: "★ ";
  color: #f5a623;
}
a[href^="http"]::after {
  content: " ↗";
}
.quote::before { content: open-quote; }
.quote::after  { content: close-quote; }</pre>

<p>Read the first rule as: "inside every <code>.tag</code>, before its
text, paint a gold star and a space". The second decorates every
external link with an arrow — attribute selectors from two lessons ago
plus today's insertion. Predict the Try-it: the badge paragraph gains a
star it never had in the HTML, and the quote paragraph grows quotation
marks from <code>open-quote</code>/<code>close-quote</code>.</p>

<p>Rules of the road: <code>content</code> is <b>required</b> (use
<code>content: ""</code> for purely decorative boxes), and the inserted
content is <b>not in the DOM</b> — screen readers may not read it, so
never put essential text there. Everything else is normal CSS: box
model, positioning, backgrounds all work.</p>

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
<p>Long selector lists get ugly fast: <code>header a, main a, footer
a</code>. The modern <b>logical pseudo-classes</b> take a selector list
as an argument and compose — they turn those chains into readable ones,
and one of them finally lets a parent react to its children.</p>

<p><b><code>:not()</code></b> — everything except:</p>

<pre class="code">li:not(.done) { color: #333; }</pre>

<p>Every list item that does <i>not</i> carry class <code>done</code>
goes dark — the completed ones are left for another rule to style.</p>

<p><b><code>:is()</code></b> — matches any of the listed selectors; great
for deduplicating:</p>

<pre class="code">/* instead of: header a, main a, footer a { ... } */
:is(header, main, footer) a { color: #1572b6; }</pre>

<p>The comment tells the story: the argument expands to "a link inside
a header OR main OR footer". Add an <code>&lt;aside&gt;</code> later and
you edit one place, not four selectors.</p>

<p><b><code>:where()</code></b> — identical to <code>:is()</code> with one
crucial difference: it contributes <b>zero specificity</b> (chapter 3).
Perfect for defaults that any real style should override.</p>

<p><b><code>:has()</code></b> — the long-awaited <b>parent selector</b>:
"an element that contains..." — styling based on what's <i>inside</i>:</p>

<pre class="code">/* a card that contains an image gets special padding */
.card:has(img) { padding: 0; }

/* a heading followed by a warning box */
h2:has(+ .warning) { color: #c0392b; }

/* form:highlight invalid state from the field INSIDE */
form:has(input:invalid) { border: 2px solid #c0392b; }</pre>

<p>The first rule styles the card <i>because of</i> what it contains;
the second looks ahead to a sibling; the third outlines a form while a
field inside is invalid — three patterns that needed JavaScript for
decades. MDN calls :has() one of the most significant recent additions
to CSS. Predict the Try-it: only the card holding an image turns
blue-framed, and the form stays red-bordered until its input passes
<code>minlength</code>.</p>

<p>Gotcha: <code>:is()</code> takes the specificity of its <i>most
specific</i> argument, so <code>:is(#special, p)</code> acts like an ID
selector — prefer <code>:where()</code> for low-impact defaults.</p>
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
<p>Two rules tell the same paragraph to be red and blue. Which wins?
Browsers can't ask you every time, so CSS ships a tie-breaking machine:
the <b>cascade</b>. Its main lever is <b>specificity</b> — a score every
selector earns, counted in three columns:</p>

<ul>
<li><b>IDs</b> — 1 point each: <code>#header</code></li>
<li><b>Classes / pseudo-classes / attributes</b> — 1 point each:
<code>.card</code>, <code>:hover</code>, <code>[type="text"]</code></li>
<li><b>Elements / pseudo-elements</b> — 1 point each: <code>p</code>,
<code>::before</code></li>
</ul>

<p>Written as (IDs, classes, elements), score these:</p>

<pre class="code">p                    → (0, 0, 1)
.card                → (0, 1, 0)
p.card               → (0, 1, 1)
#nav .card &gt; a:hover → (1, 2, 1)   ← wins over everything above</pre>

<p>Compare left to right: the last selector wins because its first
column holds a 1 — <b>one ID beats any number of classes</b>, and one
class beats any number of elements. <code>p.card</code> beats
<code>.card</code> only because its third column is higher. Two habits
follow: keep specificity low on purpose (classes over element soup), so
overrides stay cheap. And know what outranks the columns — <b>inline
<code>style="..."</code></b> sits above all three (a virtual fourth
column), and <code>!important</code> above that (next lesson).</p>

<p>When scores are <b>equal</b>, the cascade falls back to source order:
<b>the later rule wins</b>. This is why reset sheets come first and
theme sheets come last — order is design.</p>

<p>Predict the Try-it: the first paragraph takes <code>p.message</code>'s
green (0,1,1) over gray and blue; the second also has
<code>id="banner"</code>, so red (1,0,0) wins — the ID column trumps
everything. Gotcha: when a rule "refuses" to apply, compute its
specificity against the winner's before you touch any values.</p>
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
<p>Why do you set <code>font-family</code> once on <code>body</code> and
the whole page follows — yet borders never spread anywhere you didn't
explicitly draw them? The answer is <b>inheritance</b>: some properties
flow down the tree automatically, others don't. Set <code>color</code>
on <code>body</code> and every descendant inherits it; set
<code>border</code> and nothing inherits it (imagine every child of a
bordered box growing its own border!).</p>

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

<p>The split is sensible: text inherits because a paragraph nested deep
inside your styled section should read the same; boxes don't because a
child is not its parent's frame. CSS still lets you override the
default per property, with four universal keywords:</p>

<pre class="code">.deep-child {
  color: inherit;    /* take the parent's value (the default for color) */
  border: inherit;   /* FORCE inheritance of a non-inherited property */
  color: initial;    /* back to the spec's default */
  color: unset;      /* inherit if naturally inherited, else initial */
}</pre>

<p>One rule, four attitudes: <code>inherit</code> grabs the parent's
value even for box properties (the Try-it makes a span borrow its
parent's red border); <code>initial</code> resets to the spec's
default; <code>unset</code> means "act natural". Since later
declarations win, this rule ends up applying <code>color: unset</code>
and <code>border: inherit</code> — a little cascade puzzle to trace on
paper before you run it.</p>

<p>And whatever wins the cascade becomes the <b>computed value</b>: the
browser resolves relative units and keywords into concrete numbers —
<code>font-size: 2em</code> on a 16px parent computes to 32px. The
devtools "Computed" tab shows exactly this final state per element;
when behaviour confuses you, read the computed values, not your
source.</p>
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
<p>Sometimes you genuinely cannot touch the rule that's beating you: a
third-party widget, a browser default, a plugin's sheet.
<b><code>!important</code></b> exists for exactly that — it lifts one
declaration above the normal specificity game, above inline styles,
above everything except another !important:</p>

<pre class="code">.hidden-banner { display: none !important; }</pre>

<p>Read it as an asterisk on the rule: "this one wins the cascade
regardless of score". As a daily tool it's a trap: each !important
forces the next override to also be !important, and the stylesheet
escalates until nobody can change anything. Exhaust every alternative —
better specificity, source order, layers — before reaching for it, and
when you do, leave a comment saying why.</p>

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

<p>The first line declares the layer order up front — that ordering is
the whole mechanism. Later layers beat earlier ones <b>regardless of
specificity</b>: a one-class rule in <code>utilities</code> beats a
triple-ID rule in <code>base</code>, by design. Un-layered styles beat
all layers, which keeps quick overrides simple. (The
<code>!important-ish</code> in the example is a wink, not syntax — the
layer alone does the work.) MDN positions layers as the sane answer to
the "which of my 4000 rules wins" problem; they get their own Advanced
chapter later.</p>

<p>Gotcha: !important doesn't beat !important-plus-higher-specificity
by accident — among !important declarations the normal specificity
rules apply again, so the arms race resumes one level up.</p>
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
