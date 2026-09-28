"""HTML Tutor chapters 1-5, grounded in MDN Web Docs (developer.mozilla.org)."""

CHAPTERS_HTML_A = [
    # ------------------------------------------------------------------ h01
    {
        "id": "h01",
        "title": "Introduction & Fundamentals",
        "emoji": "🚀",
        "lessons": [
            {
                "title": "What is HTML?",
                "html": """
<p><b>HTML (HyperText Markup Language)</b> is the most basic building block
of the Web. It defines the <b>meaning and structure</b> of web content —
MDN calls it exactly that. "Hypertext" refers to text with links that
connect pages; publish pages and link them together, and you become an
active participant in the World Wide Web.</p>

<p>HTML works as a team with two other technologies, and knowing the
division of labour is half of understanding the web:</p>

<ul>
<li><b>HTML</b> — <i>structure &amp; meaning</i>: this is a heading, this is
a paragraph, this is a link</li>
<li><b>CSS</b> — <i>presentation</i>: colours, fonts, layout, animation</li>
<li><b>JavaScript</b> — <i>behaviour</i>: what happens when you click,
type, scroll</li>
</ul>

<p>A house metaphor works well: HTML is the frame and walls, CSS is the
paint and decoration, JavaScript is the electricity and plumbing. Removing
any one changes the result — but HTML comes first, because without
structure there is nothing to present or make interactive.</p>

<p>"Markup" means you annotate ordinary content with special markers
(<b>elements</b>) that tell the browser what each piece <i>is</i>. The
browser reads your markup and builds the page you see.</p>
""",
                "tryit": """<!DOCTYPE html>
<html lang="en">
<head>
  <title>My first page</title>
  <style>
    body { font-family: sans-serif; }
    h1 { color: #e44d26; }
  </style>
</head>
<body>
  <h1>Hello, web!</h1>
  <p>This is <strong>HTML</strong> — the structure.</p>
  <p style="color: teal">This line wears inline <strong>CSS</strong> — the presentation.</p>
  <button onclick="this.textContent = 'Clicked! 🎉'">
    And this is JavaScript — the behaviour.
  </button>
</body>
</html>
""",
            },
            {
                "title": "Elements, Tags & Attributes",
                "html": """
<p>An <b>element</b> is a part of the page; a <b>tag</b> is the marker that
writes it. Most elements have an opening tag, some content, and a closing
tag with a slash:</p>

<pre class="code">&lt;p&gt;Hello world&lt;/p&gt;
└ opening   content   closing ┘</pre>

<p>Tag names are case-insensitive — <code>&lt;P&gt;</code> works the same as
<code>&lt;p&gt;</code> — but the universal convention is <b>lowercase</b>.</p>

<p><b>Attributes</b> give an element extra information. They live in the
opening tag as <code>name="value"</code> pairs:</p>

<pre class="code">&lt;a href="https://developer.mozilla.org"&gt;MDN&lt;/a&gt;
└   └ element    └ href attribute ┘         ┘

&lt;img src="cat.jpg" alt="A cat sleeping"&gt;</pre>

<p>Some elements have <b>no content</b> and therefore no closing tag — the
<b>void elements</b>: <code>&lt;img&gt;</code>, <code>&lt;br&gt;</code>,
<code>&lt;hr&gt;</code>, <code>&lt;input&gt;</code>, <code>&lt;meta&gt;</code>,
<code>&lt;link&gt;</code> and a few more. They are complete in one tag.</p>

<p>The most important attribute of all is <code>id</code> (unique name for
one element) and its sibling <code>class</code> (group membership) — you
will meet them everywhere, especially once CSS and JavaScript join the
party.</p>
""",
                "tryit": """<!DOCTYPE html>
<html lang="en">
<head><title>Elements & attributes</title></head>
<body>
  <h1 style="color:#e44d26">Elements at work</h1>

  <p>A paragraph element with a <strong>strong</strong> child.</p>

  <a href="https://developer.mozilla.org" title="MDN Web Docs">
    A link with attributes
  </a>

  <img src="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='120' height='80'%3E%3Crect width='120' height='80' rx='8' fill='%23f16529'/%3E%3Ctext x='60' y='46' text-anchor='middle' fill='white' font-size='14' font-family='Arial'%3Eimg%3C/text%3E%3C/svg%3E"
       alt="an orange placeholder box" width="120">

  <br>A void element: <input placeholder="type here">
</body>
</html>
""",
            },
            {
                "title": "Nesting & Comments",
                "html": """
<p>Elements live <b>inside</b> other elements — that is nesting, and it is
how every page is built. The one iron rule: tags must close in the
<b>reverse order</b> they opened:</p>

<pre class="code">&lt;p&gt;This is &lt;strong&gt;important&lt;/strong&gt; text&lt;/p&gt;   ✓ correct

&lt;p&gt;This is &lt;strong&gt;important&lt;/p&gt;&lt;/strong&gt;        ✗ overlapping</pre>

<p>Browsers recover from mistakes (usually), but overlapping tags produce
surprising structures — always close what you opened, in order.
Indentation is not required by HTML (unlike Python!) but it makes nesting
visible:</p>

<pre class="code">&lt;ul&gt;
  &lt;li&gt;Outer item
    &lt;ol&gt;
      &lt;li&gt;Nested item&lt;/li&gt;
    &lt;/ol&gt;
  &lt;/li&gt;
&lt;/ul&gt;</pre>

<p><b>Comments</b> are notes for humans that the browser ignores
completely. They start with <code>&lt;!--</code> and end with
<code>--&gt;</code>:</p>

<pre class="code">&lt;!-- Navigation section — do not remove --&gt;
&lt;nav&gt;...&lt;/nav&gt;

&lt;p&gt;Visible text&lt;/p&gt;
&lt;!-- &lt;p&gt;Temporarily disabled&lt;/p&gt; --&gt;</pre>

<p>Comments are also the standard way to "switch off" a line of markup
while testing — wrap it, refresh, unwrap it.</p>
""",
                "tryit": """<!DOCTYPE html>
<html lang="en">
<head><title>Nesting & comments</title></head>
<body>
  <!-- This comment is invisible in the page,
       but you can read it in the source! -->
  <ul>
    <li>Fruits
      <ol>
        <li>Apple</li>
        <li>Orange</li>
      </ol>
    </li>
    <li>Vegetables</li>
  </ul>

  <!-- <p>This paragraph is commented out.</p> -->
  <p>View this page's source to see the comments.</p>
</body>
</html>
""",
            },
            {
                "title": "Document Structure",
                "html": """
<p>Every proper HTML page wears the same skeleton. Learn it once, use it
forever:</p>

<pre class="code">&lt;!DOCTYPE html&gt;          ← "this is modern HTML" (always first)
&lt;html lang="en"&gt;          ← the whole document; its language
  &lt;head&gt;                  ← information ABOUT the page
    &lt;title&gt;Page title&lt;/title&gt;
  &lt;/head&gt;
  &lt;body&gt;                  ← the visible CONTENT of the page
    &lt;h1&gt;Hello&lt;/h1&gt;
  &lt;/body&gt;
&lt;/html&gt;</pre>

<ul>
<li><b><code>&lt;!DOCTYPE html&gt;</code></b> — not an element; a declaration.
It puts the browser into standards mode so it follows the modern rules.
Every document needs it, always first.</li>
<li><b><code>&lt;html&gt;</code></b> — the root element that wraps everything.
Its <code>lang</code> attribute declares the page's language
(<code>en</code>, <code>fa</code>, <code>de</code>...) — screen readers and
search engines rely on it.</li>
<li><b><code>&lt;head&gt;</code></b> — metadata: the <code>&lt;title&gt;</code>
(shown on the browser tab, not the page), character set
(<code>&lt;meta charset="utf-8"&gt;</code>), viewport settings, linked CSS,
and more. Nothing here renders in the page body.</li>
<li><b><code>&lt;body&gt;</code></b> — everything the visitor actually
sees.</li>
</ul>

<p>The <code>&lt;title&gt;</code> is required and is what appears in the tab,
bookmarks and search results. A page without a title is incomplete.</p>
""",
                "tryit": """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>This title lives on the browser tab — not the page!</title>
</head>
<body>
  <h1>The body is what you see</h1>
  <p>But the head holds the title, charset, and other metadata.</p>
  <p>Look at the preview's tab/title area above the page.</p>
</body>
</html>
""",
            },
        ],
        "quiz": [
            {
                "type": "mc",
                "question": "Which technology is responsible for the <b>presentation</b> of a web page?",
                "options": ["HTML", "CSS", "JavaScript", "HTTP"],
                "answer": 1,
                "explain": "Per MDN's division: HTML is structure/meaning, CSS is appearance, JavaScript is behaviour.",
            },
            {
                "type": "mc",
                "question": "In <code>&lt;a href=\"https://mdn.dev\"&gt;MDN&lt;/a&gt;</code>, what is <code>href</code>?",
                "options": ["An element", "A tag", "An attribute", "A comment"],
                "answer": 2,
                "explain": "href is an attribute — a name=\"value\" pair in the opening tag that gives the element extra information.",
            },
            {
                "type": "blank",
                "question": "Comments in HTML start with <code>&lt;!--</code> and end with <code>____</code>.",
                "answers": ["-->", "--&gt;", "-- >"],
                "explain": "<!-- note --> — everything between is ignored by the browser.",
            },
            {
                "type": "order",
                "question": "Order the pieces of a minimal HTML document from top to bottom:",
                "lines": [
                    "<!DOCTYPE html>",
                    "<html lang=\"en\">",
                    "<head><title>Hi</title></head>",
                    "<body><h1>Hello</h1></body>",
                    "</html>",
                ],
                "explain": "DOCTYPE first, then <html>, head, body — closed by </html>.",
            },
        ],
    },

    # ------------------------------------------------------------------ h02
    {
        "id": "h02",
        "title": "Text & Content",
        "emoji": "✍️",
        "lessons": [
            {
                "title": "Headings",
                "html": """
<p>Headings give a page its outline. HTML has six levels,
<code>&lt;h1&gt;</code> (most important) through
<code>&lt;h6&gt;</code> (least):</p>

<pre class="code">&lt;h1&gt;The Solar System&lt;/h1&gt;
  &lt;h2&gt;Inner planets&lt;/h2&gt;
    &lt;h3&gt;Mercury&lt;/h3&gt;
    &lt;h3&gt;Venus&lt;/h3&gt;
  &lt;h2&gt;Outer planets&lt;/h2&gt;
    &lt;h3&gt;Jupiter&lt;/h3&gt;</pre>

<p>Think of them as a <b>table of contents</b>, not as font sizes — you can
make any heading any size with CSS, so choose the level by
<i>structure</i>, not by how big it looks.</p>

<p>Two rules that keep pages accessible:</p>

<ul>
<li>Use <b>one <code>&lt;h1&gt;</code></b> per page — the topic of the whole
document.</li>
<li><b>Don't skip levels</b>: go <code>h1 → h2 → h3</code>, not
<code>h1 → h4</code>. Screen-reader users navigate by jumping between
headings, and skipped levels make the outline lie.</li>
</ul>
""",
                "tryit": """<!DOCTYPE html>
<html lang="en">
<head><title>Headings</title></head>
<body>
  <h1>The Solar System</h1>
  <h2>Inner planets</h2>
  <h3>Mercury</h3>
  <h3>Venus</h3>
  <h2>Outer planets</h2>
  <h3>Jupiter</h3>
  <h4>Great Red Spot</h4>
</body>
</html>
""",
            },
            {
                "title": "Paragraphs",
                "html": """
<p>The <code>&lt;p&gt;</code> element is a paragraph — the workhorse of
text on the web:</p>

<pre class="code">&lt;p&gt;HTML defines the structure of web content.&lt;/p&gt;
&lt;p&gt;This is a second, separate paragraph.&lt;/p&gt;</pre>

<p>A crucial detail: HTML <b>collapses whitespace</b>. Any run of spaces,
tabs and newlines in your source becomes a single space in the rendered
page. Pressing Enter twice inside a paragraph does <b>not</b> create a
new paragraph — only a new <code>&lt;p&gt;</code> does:</p>

<pre class="code">&lt;p&gt;Line one
     still    line one&lt;/p&gt;
&lt;p&gt;Line two&lt;/p&gt;</pre>

<p>Both lines of the first paragraph render as one continuous sentence
with single spaces. This surprises every beginner once — now you know
it is by design: <i>meaning</i> lives in elements, not in whitespace.</p>

<p>Browsers also render paragraphs with spacing between them
automatically — that gap is CSS's default margin, not an empty
paragraph. Never press Enter twice to "add space"; that is styling, and
styling belongs to CSS.</p>
""",
                "tryit": """<!DOCTYPE html>
<html lang="en">
<head><title>Paragraphs</title></head>
<body>
  <p>Line one
       with    lots    of spaces
     and newlines — all collapsed!</p>
  <p>This is a real second paragraph.</p>
</body>
</html>
""",
            },
            {
                "title": "Inline Text Semantics",
                "html": """
<p>Inside a paragraph, inline elements mark up what pieces of text
<i>are</i>. The two you will use constantly:</p>

<ul>
<li><code>&lt;strong&gt;</code> — <b>strong importance</b> (renders bold)</li>
<li><code>&lt;em&gt;</code> — <b>emphasis</b> with stress (renders italic)</li>
</ul>

<p>Then the specialist set:</p>

<pre class="code">&lt;b&gt;bold&lt;/b&gt;              just visual bold, no extra meaning
&lt;i&gt;italic&lt;/i&gt;            a different voice: terms, thoughts, ship names
&lt;mark&gt;highlighted&lt;/mark&gt; relevant in another context
&lt;small&gt;fine print&lt;/small&gt; side comments, copyright
&lt;del&gt;deleted&lt;/del&gt;       removed text
&lt;ins&gt;inserted&lt;/ins&gt;      added text
H&lt;sub&gt;2&lt;/sub&gt;O            subscript
x&lt;sup&gt;2&lt;/sup&gt;             superscript</pre>

<p>The difference between <code>&lt;strong&gt;</code> and
<code>&lt;b&gt;</code> is <b>meaning</b>, not looks: strong tells screen
readers and search engines "this matters"; <code>&lt;b&gt;</code> only says
"draw it bold". Same for <code>&lt;em&gt;</code> vs <code>&lt;i&gt;</code>.
Prefer the meaningful one when in doubt — the visual default can always
be restyled with CSS.</p>
""",
                "tryit": """<!DOCTYPE html>
<html lang="en">
<head><title>Inline semantics</title></head>
<body>
  <p><strong>Warning:</strong> this is <em>really</em> important.</p>
  <p>The term <i>HyperText</i> was coined in the 1960s.</p>
  <p>Answer: <mark>42</mark> <small>(per Douglas Adams)</small></p>
  <p><del>Old price: $99</del> <ins>New price: $49</ins></p>
  <p>Water is H<sub>2</sub>O; area = πr<sup>2</sup></p>
</body>
</html>
""",
            },
            {
                "title": "Line Breaks & Horizontal Rules",
                "html": """
<p>Two void elements handle visual separation inside flowing text.</p>

<p><code>&lt;br&gt;</code> forces a <b>line break</b> — the text continues on
the next line <i>within the same paragraph</i>. Its legitimate home is
content where the line break is part of the meaning:</p>

<pre class="code">&lt;p&gt;Roses are red,&lt;br&gt;
violets are blue.&lt;/p&gt;

&lt;p&gt;123 Main Street&lt;br&gt;
Springfield&lt;/p&gt;</pre>

<p>For everything else — separating <i>topics</i>, <i>paragraphs</i>,
<i>sections</i> — <code>&lt;br&gt;</code> is the wrong tool. Two addresses
in a poem: perfect. Gaps between paragraphs: use new paragraphs and CSS
margins.</p>

<p><code>&lt;hr&gt;</code> is a <b>thematic break</b> — "the story changes
here". It renders as a horizontal line, but the meaning is the break
between topics, not the line:</p>

<pre class="code">&lt;h2&gt;Chapter 1&lt;/h2&gt;
&lt;p&gt;It was a dark and stormy night...&lt;/p&gt;

&lt;hr&gt;

&lt;h2&gt;Chapter 2&lt;/h2&gt;
&lt;p&gt;The morning brought news.&lt;/p&gt;</pre>

<p>Both are void elements: no closing tag, no content, nothing inside.</p>
""",
                "tryit": """<!DOCTYPE html>
<html lang="en">
<head><title>br and hr</title></head>
<body>
  <p>Knock, knock.<br>Who's there?<br>HTML.<br>HTML who?</p>

  <h2>Part one</h2>
  <p>A paragraph of story.</p>
  <hr>
  <h2>Part two</h2>
  <p>A new thematic section begins.</p>
</body>
</html>
""",
            },
            {
                "title": "Quotes",
                "html": """
<p>HTML has dedicated elements for quoting, each with different
behaviour:</p>

<ul>
<li><code>&lt;blockquote&gt;</code> — a <b>block-level</b> quote: its own
chunk of content, usually a long quotation from another source. Browsers
indent it.</li>
<li><code>&lt;q&gt;</code> — an <b>inline</b> quote: a short quotation inside
a paragraph. Browsers add the quotation marks themselves — do not type
your own!</li>
<li><code>&lt;cite&gt;</code> — the <b>title of a work</b> (a book, a film,
an article), not the author's name.</li>
</ul>

<pre class="code">&lt;p&gt;In &lt;cite&gt;The Design of Everyday Things&lt;/cite&gt; we read:&lt;/p&gt;

&lt;blockquote&gt;
  &lt;p&gt;When people make errors, the cause is often bad design.&lt;/p&gt;
&lt;/blockquote&gt;

&lt;p&gt;As the guide says, &lt;q&gt;HTML defines meaning and structure&lt;/q&gt;
for the web.&lt;/p&gt;</pre>

<p>Both <code>&lt;blockquote&gt;</code> and <code>&lt;q&gt;</code> accept a
<code>cite="URL"</code> <i>attribute</i> pointing at the source — machine-
readable provenance that doesn't render visually. The
<code>&lt;cite&gt;</code> <i>element</i>, meanwhile, marks up the work's
title in text. Attribute and element, same name, different jobs.</p>
""",
                "tryit": """<!DOCTYPE html>
<html lang="en">
<head><title>Quotes</title></head>
<body>
  <p>MDN says HTML is
     <q cite="https://developer.mozilla.org/en-US/docs/Web/HTML">
       the most basic building block of the Web</q>.</p>

  <blockquote cite="https://developer.mozilla.org">
    <p>Hypertext refers to links that connect web pages to one
       another.</p>
  </blockquote>

  <p>From the book <cite>Learning Web Design</cite>.</p>
</body>
</html>
""",
            },
            {
                "title": "Code-Related Elements",
                "html": """
<p>Writing <i>about</i> code has its own inline elements, each with a
meaning:</p>

<ul>
<li><code>&lt;code&gt;</code> — a fragment of code, inline</li>
<li><code>&lt;pre&gt;</code> — <b>preformatted</b> text: whitespace and
line breaks are preserved exactly (unlike everywhere else!)</li>
<li><code>&lt;kbd&gt;</code> — keyboard input the user should press</li>
<li><code>&lt;samp&gt;</code> — sample <b>output</b> from a program</li>
<li><code>&lt;var&gt;</code> — a variable name</li>
</ul>

<p><code>&lt;pre&gt;</code> is the exception to whitespace collapsing — and
the reason code examples on the web keep their shape. The classic
combination is <code>&lt;pre&gt;</code> wrapping
<code>&lt;code&gt;</code>: pre handles the layout, code declares the
meaning:</p>

<pre class="code">&lt;pre&gt;&lt;code&gt;function greet(name) {
  return "Hello, " + name;
}&lt;/code&gt;&lt;/pre&gt;

&lt;p&gt;Press &lt;kbd&gt;Ctrl&lt;/kbd&gt; + &lt;kbd&gt;S&lt;/kbd&gt; to save.&lt;/p&gt;

&lt;p&gt;The program prints &lt;samp&gt;Hello, Ada&lt;/samp&gt; when
&lt;var&gt;name&lt;/var&gt; is Ada.&lt;/p&gt;</pre>

<p>Careful: because <code>&lt;pre&gt;</code> preserves everything, the
source must start the code on the line right after the opening tag —
otherwise your indentation becomes part of the output.</p>
""",
                "tryit": """<!DOCTYPE html>
<html lang="en">
<head><title>Code elements</title>
<style>
  pre, code, kbd, samp { background: #f6f1ec; padding: 1px 4px;
                         border-radius: 4px; }
  pre { padding: 10px; }
</style></head>
<body>
  <p>The function <code>greet()</code> below takes a <var>name</var>:</p>

  <pre><code>function greet(name) {
  return "Hello, " + name;
}</code></pre>

  <p>Press <kbd>Ctrl</kbd> + <kbd>Enter</kbd> to run it.
     It prints <samp>Hello, Ada</samp>.</p>
</body>
</html>
""",
            },
        ],
        "quiz": [
            {
                "type": "mc",
                "question": "How many &lt;h1&gt; elements should a typical page have?",
                "options": ["As many as needed", "One", "Six", "None — h1 is deprecated"],
                "answer": 1,
                "explain": "h1 is the topic of the whole page — one per page, then descend h2, h3... without skipping.",
            },
            {
                "type": "mc",
                "question": "Inside a paragraph, pressing Enter twice creates:",
                "options": [
                    "A new paragraph",
                    "A line break",
                    "Nothing special — HTML collapses it to a single space",
                    "An error",
                ],
                "answer": 2,
                "explain": "Whitespace collapses; only elements (<p>, <br>) create structure.",
            },
            {
                "type": "mc",
                "question": "Which pair marks up removed and added text?",
                "options": ["&lt;remove&gt; / &lt;add&gt;", "&lt;del&gt; / &lt;ins&gt;", "&lt;strike&gt; / &lt;new&gt;", "&lt;old&gt; / &lt;update&gt;"],
                "answer": 1,
                "explain": "<del> marks deletion, <ins> insertion — perfect for diffs and price changes.",
            },
            {
                "type": "blank",
                "question": "A short inline quotation uses <code>&lt;q&gt;</code>, and the browser adds the ____ ____ itself.",
                "answers": ["quotation marks", "quote marks", "quotes"],
                "explain": "<q> renders its own quotation marks — never type your own inside it.",
            },
            {
                "type": "mc",
                "question": "Which element preserves whitespace and line breaks exactly?",
                "options": ["&lt;code&gt;", "&lt;pre&gt;", "&lt;samp&gt;", "&lt;var&gt;"],
                "answer": 1,
                "explain": "<pre> is preformatted text — the standard wrapper for code listings (usually around <code>).",
            },
        ],
    },

    # ------------------------------------------------------------------ h03
    {
        "id": "h03",
        "title": "Links",
        "emoji": "🔗",
        "lessons": [
            {
                "title": "The Anchor & href",
                "html": """
<p>Links are the "hyper" in HyperText — the element is
<code>&lt;a&gt;</code> (anchor), and the <b>destination</b> lives in its
<code>href</code> attribute. The content between the tags is what the
visitor clicks:</p>

<pre class="code">&lt;a href="https://developer.mozilla.org"&gt;Visit MDN&lt;/a&gt;</pre>

<p>The value of <code>href</code> is a URL, and URLs come in three
flavours:</p>

<ul>
<li><b>Absolute</b> — the full address, protocol included:
<code>https://developer.mozilla.org/en-US/docs/Web/HTML</code>. Works
from anywhere on Earth.</li>
<li><b>Relative</b> — a path from the current page:
<code>about.html</code>, <code>docs/css/intro.html</code>,
<code>../index.html</code>. Moves with your site; use these for your own
pages.</li>
<li><b>Fragment</b> — a jump to a spot on the page:
<code>#chapter2</code> — where some element has
<code>id="chapter2"</code>. Combine with relative paths:
<code>guide.html#intro</code>.</li>
</ul>

<pre class="code">&lt;a href="chapter2.html"&gt;Next chapter&lt;/a&gt;   relative
&lt;a href="#top"&gt;Back to top&lt;/a&gt;             fragment
&lt;h2 id="top"&gt;The Guide&lt;/h2&gt;                 the target</pre>
""",
                "tryit": """<!DOCTYPE html>
<html lang="en">
<head><title>Links</title></head>
<body>
  <h1>Link zoo</h1>

  <p>Absolute: <a href="https://developer.mozilla.org">MDN Web Docs</a></p>

  <p>Fragment: <a href="#footnote">jump to the footnote ↓</a></p>

  <p style="margin-top: 300px" id="footnote">
    <strong>Footnote:</strong> hypertext = text with links.
    <a href="#">Back to top ↑</a>
  </p>
</body>
</html>
""",
            },
            {
                "title": "target & rel",
                "html": """
<p>By default a link opens <b>in the same tab</b>. The
<code>target</code> attribute changes that:</p>

<pre class="code">&lt;a href="https://mdn.dev" target="_blank"&gt;opens in a NEW tab&lt;/a&gt;

&lt;a href="https://mdn.dev" target="_self"&gt;same tab (default)&lt;/a&gt;</pre>

<p><code>_blank</code> means "a new browsing context" — usually a new tab.
There are more values (<code>_parent</code>, <code>_top</code>) that
matter inside frames.</p>

<p>Opening a new tab has a security twist: the new page can, via
<code>window.opener</code>, reach back and manipulate the page that
linked to it (called <b>tabnabbing</b>). The cure is the
<code>rel</code> attribute — a space-separated list of the
<i>relationship</i> between the pages:</p>

<pre class="code">&lt;a href="https://mdn.dev" target="_blank"
   rel="noopener"&gt;safe new tab&lt;/a&gt;</pre>

<p><code>rel="noopener"</code> severs that back-channel; modern browsers
imply it for <code>target="_blank"</code>, but writing it explicitly is
the good habit. Other <code>rel</code> values describe relationships:
<code>nofollow</code> ("don't count this link for ranking"),
<code>preload</code>, <code>license</code>, <code>author</code>...</p>

<p>Style note: use <code>target="_blank"</code> sparingly — visitors
decide with Ctrl+Click or right-click whether they want a new tab.
Reserve it for keeping the visitor's place (docs, references).</p>
""",
                "tryit": """<!DOCTYPE html>
<html lang="en">
<head><title>target & rel</title></head>
<body>
  <h1>Same tab vs new tab</h1>

  <p><a href="https://developer.mozilla.org">MDN — same tab</a>
     (use Back to return)</p>

  <p><a href="https://developer.mozilla.org" target="_blank"
        rel="noopener">MDN — new tab, rel="noopener"</a></p>
</body>
</html>
""",
            },
            {
                "title": "Download, Email & Telephone",
                "html": """
<p>Three special-purpose link patterns round out the family.</p>

<p><b>Download links</b>: the <code>download</code> attribute asks the
browser to save the target to disk instead of navigating to it. Its value
becomes the suggested filename:</p>

<pre class="code">&lt;a href="files/report.pdf" download&gt;Download the report&lt;/a&gt;

&lt;a href="files/data.csv" download="sales-2026.csv"&gt;
  Export data
&lt;/a&gt;</pre>

<p><b>Email links</b>: the URL scheme is
<code>mailto:</code>, and it opens the visitor's mail client with the
fields pre-filled. Parameters join with <code>?</code> and
<code>&amp;</code>:</p>

<pre class="code">&lt;a href="mailto:hi@example.com"&gt;Email us&lt;/a&gt;

&lt;a href="mailto:hi@example.com?subject=Hello&amp;body=Just saying hi"&gt;
  Email with subject and body
&lt;/a&gt;</pre>

<p><b>Telephone links</b>: the <code>tel:</code> scheme dials a number on
phones and does nothing useful on desktops — perfect for contact
pages:</p>

<pre class="code">&lt;a href="tel:+15551234567"&gt;Call +1 555 123 4567&lt;/a&gt;</pre>

<p>Note the pattern: <code>href</code> accepts any URL <i>scheme</i> —
<code>https:</code>, <code>mailto:</code>, <code>tel:</code> — the
element itself never changes.</p>
""",
                "tryit": """<!DOCTYPE html>
<html lang="en">
<head><title>Special links</title></head>
<body>
  <ul>
    <li><a href="mailto:hi@example.com?subject=Hi%20from%20the%20tutorial">
          Send an email</a></li>
    <li><a href="tel:+15551234567">Call +1 555 123 4567</a></li>
  </ul>
  <p>On a phone, tel: opens the dialer. mailto: opens a mail app.</p>
</body>
</html>
""",
            },
        ],
        "quiz": [
            {
                "type": "blank",
                "question": "The destination of a link lives in the <code>____</code> attribute.",
                "answers": ["href", "href attribute"],
                "explain": "href holds the URL: absolute, relative, or a #fragment.",
            },
            {
                "type": "mc",
                "question": "<code>href=\"docs/css/intro.html\"</code> is:",
                "options": ["An absolute URL", "A relative URL", "A fragment", "A mailto link"],
                "answer": 1,
                "explain": "No scheme and no leading slash — the path is resolved from the current page's location.",
            },
            {
                "type": "mc",
                "question": "Why write rel=\"noopener\" together with target=\"_blank\"?",
                "options": [
                    "It makes the link load faster",
                    "It stops the new page from accessing window.opener (tabnabbing)",
                    "It is required for the link to work",
                    "It hides the URL",
                ],
                "answer": 1,
                "explain": "noopener cuts the new page's back-reference to your page — the tabnabbing defence.",
            },
            {
                "type": "mc",
                "question": "Which href opens the visitor's mail client?",
                "options": ["href=\"email:hi@x.com\"", "href=\"mailto:hi@x.com\"", "href=\"mail:hi@x.com\"", "href=\"@hi@x.com\""],
                "answer": 1,
                "explain": "mailto: is the URL scheme for email; tel: is its sibling for phone numbers.",
            },
        ],
    },

    # ------------------------------------------------------------------ h04
    {
        "id": "h04",
        "title": "Lists",
        "emoji": "📋",
        "lessons": [
            {
                "title": "Unordered & Ordered Lists",
                "html": """
<p>Lists are everywhere on the web — navigation, features, steps, tags.
HTML has two workhorse list elements:</p>

<ul>
<li><code>&lt;ul&gt;</code> — <b>unordered list</b>: the order of items does
not matter (bullet points). Shopping lists, feature lists, menus.</li>
<li><code>&lt;ol&gt;</code> — <b>ordered list</b>: the order IS the meaning
(numbered). Recipes, rankings, instructions.</li>
</ul>

<p>Each item is an <code>&lt;li&gt;</code> (list item) — and every
<code>&lt;li&gt;</code> must live directly inside its
<code>&lt;ul&gt;</code>/<code>&lt;ol&gt;</code> parent:</p>

<pre class="code">&lt;ul&gt;
  &lt;li&gt;Flour&lt;/li&gt;
  &lt;li&gt;Eggs&lt;/li&gt;
  &lt;li&gt;Milk&lt;/li&gt;
&lt;/ul&gt;

&lt;ol&gt;
  &lt;li&gt;Preheat the oven to 180°&lt;/li&gt;
  &lt;li&gt;Mix the ingredients&lt;/li&gt;
  &lt;li&gt;Bake for 30 minutes&lt;/li&gt;
&lt;/ol&gt;</pre>

<p><code>&lt;ol&gt;</code> understands two handy attributes:
<code>start="5"</code> begins counting at 5, and
<code>reversed</code> counts down. Choose <code>ul</code> vs
<code>ol</code> by <i>meaning</i>: would reordering the items change
anything? If yes, it's an <code>ol</code>.</p>
""",
                "tryit": """<!DOCTYPE html>
<html lang="en">
<head><title>Lists</title></head>
<body>
  <h2>Shopping (order doesn't matter)</h2>
  <ul>
    <li>Flour</li>
    <li>Eggs</li>
    <li>Milk</li>
  </ul>

  <h2>Recipe (order matters)</h2>
  <ol start="3">
    <li>Preheat the oven</li>
    <li>Mix everything</li>
    <li>Bake 30 minutes</li>
  </ol>
  <p>The ol above starts at 3 thanks to start="3".</p>
</body>
</html>
""",
            },
            {
                "title": "Description Lists",
                "html": """
<p>The third list element is the one everyone forgets:
<code>&lt;dl&gt;</code>, the <b>description list</b> — for pairs of terms
and their descriptions. A glossary, metadata, FAQs, product
specifications:</p>

<pre class="code">&lt;dl&gt;
  &lt;dt&gt;HTML&lt;/dt&gt;
  &lt;dd&gt;HyperText Markup Language — the web's structure.&lt;/dd&gt;

  &lt;dt&gt;CSS&lt;/dt&gt;
  &lt;dd&gt;Cascading Style Sheets — the web's presentation.&lt;/dd&gt;

  &lt;dt&gt;URL&lt;/dt&gt;
  &lt;dd&gt;Uniform Resource Locator.&lt;/dd&gt;
  &lt;dd&gt;Also informally called a web address.&lt;/dd&gt;
&lt;/dl&gt;</pre>

<p>The structure:</p>

<ul>
<li><code>&lt;dt&gt;</code> — description <b>term</b> (the thing being
defined)</li>
<li><code>&lt;dd&gt;</code> — <b>description</b> (indented under the term)</li>
</ul>

<p>Two legal flexibilities make it fit real data: one term can have
<b>multiple descriptions</b> (two <code>&lt;dd&gt;</code>s after one
<code>&lt;dt&gt;</code>, as above), and one description can serve
<b>multiple terms</b> (several <code>&lt;dt&gt;</code>s in a row —
"TLA" and "Three-Letter Acronym" sharing one definition).</p>
""",
                "tryit": """<!DOCTYPE html>
<html lang="en">
<head><title>Description list</title>
<style> dt { font-weight: bold; color: #e44d26; } </style>
</head>
<body>
  <h2>Glossary</h2>
  <dl>
    <dt>Element</dt>
    <dd>A part of the page, written with tags.</dd>

    <dt>Attribute</dt>
    <dd>Extra information in an element's opening tag.</dd>

    <dt>Void element</dt>
    <dd>An element with no content and no closing tag.</dd>
  </dl>
</body>
</html>
""",
            },
            {
                "title": "Nested Lists",
                "html": """
<p>Real content nests: a chapter has sections, a menu has submenus. A
list goes inside another list by placing it <b>inside an
<code>&lt;li&gt;</code></b> of the outer list — never directly inside the
<code>&lt;ul&gt;</code> or <code>&lt;ol&gt;</code>:</p>

<pre class="code">&lt;ul&gt;
  &lt;li&gt;Fruits
    &lt;ul&gt;
      &lt;li&gt;Apples&lt;/li&gt;
      &lt;li&gt;Oranges&lt;/li&gt;
    &lt;/ul&gt;
  &lt;/li&gt;
  &lt;li&gt;Vegetables&lt;/li&gt;
&lt;/ul&gt;</pre>

<p>Read the structure: the inner <code>&lt;ul&gt;</code> is part of the
"Fruiits" item's content, so it belongs inside that
<code>&lt;li&gt;</code>, before its closing tag. Mix levels freely — an
<code>&lt;ol&gt;</code> inside a <code>&lt;ul&gt;</code> inside an
<code>&lt;ol&gt;</code> is perfectly legal, and browsers style each level
differently for you.</p>

<p>The same pattern builds every site navigation you have ever used — a
<code>&lt;nav&gt;</code> wrapping a list of links:</p>

<pre class="code">&lt;nav&gt;
  &lt;ul&gt;
    &lt;li&gt;&lt;a href="/"&gt;Home&lt;/a&gt;&lt;/li&gt;
    &lt;li&gt;&lt;a href="/docs"&gt;Docs&lt;/a&gt;&lt;/li&gt;
  &lt;/ul&gt;
&lt;/nav&gt;</pre>

<p>Navigation menus are lists of links <i>semantically</i> — screen
readers announce "list, 2 items", which tells the visitor what to
expect before they hear the links.</p>
""",
                "tryit": """<!DOCTYPE html>
<html lang="en">
<head><title>Nested lists</title></head>
<body>
  <h2>Course outline</h2>
  <ol>
    <li>Fundamentals
      <ul>
        <li>Elements & tags</li>
        <li>Attributes</li>
      </ul>
    </li>
    <li>Text & content
      <ul>
        <li>Headings</li>
        <li>Links</li>
      </ul>
    </li>
    <li>Tables</li>
  </ol>
</body>
</html>
""",
            },
        ],
        "quiz": [
            {
                "type": "mc",
                "question": "Which list type for a recipe's steps, where order matters?",
                "options": ["&lt;ul&gt;", "&lt;ol&gt;", "&lt;dl&gt;", "&lt;li&gt; alone"],
                "answer": 1,
                "explain": "Ordered list <ol> — the numbering IS the meaning.",
            },
            {
                "type": "mc",
                "question": "In a description list, what does <code>&lt;dd&gt;</code> hold?",
                "options": ["The term", "The description", "A nested list", "A link"],
                "answer": 1,
                "explain": "<dt> = the term, <dd> = its description.",
            },
            {
                "type": "mc",
                "question": "Where does a nested list belong?",
                "options": [
                    "Directly inside <ul>, next to the <li>s",
                    "Inside the parent <li>, before its closing tag",
                    "Inside another <li>'s text, no wrapper",
                    "Anywhere — HTML doesn't care",
                ],
                "answer": 1,
                "explain": "A sub-list is part of an item's content, so it lives inside that <li>.",
            },
            {
                "type": "codefill",
                "question": "Build the skeleton of a two-item ordered list:",
                "code": [
                    "<", { "blank": "ol", "answers": ["ol"] }, ">",
                    "  <", { "blank": "li", "answers": ["li"] }, ">First</li>",
                    "  <li>Second</li>",
                    "</", { "blank": "ol", "answers": ["ol"] }, ">",
                ],
                "explain": "<ol> wraps <li> items — every item is an <li>.",
            },
        ],
    },

    # ------------------------------------------------------------------ h05
    {
        "id": "h05",
        "title": "Images & Media",
        "emoji": "🖼️",
        "lessons": [
            {
                "title": "Images",
                "html": """
<p>The <code>&lt;img&gt;</code> element embeds an image. It is a void
element, and it lives on two required attributes:</p>

<pre class="code">&lt;img src="grapefruit.jpg" alt="A sliced grapefruit on a blue table"&gt;</pre>

<ul>
<li><code>src</code> — the <b>source</b>: a URL, absolute or relative,
exactly like a link's <code>href</code></li>
<li><code>alt</code> — <b>alternative text</b>: what the image communicates,
for visitors who cannot see it (screen readers), when it fails to load,
and for search engines. Every meaningful image deserves honest alt text;
purely decorative images take an <b>empty</b> <code>alt=""</code> so
screen readers skip them.</li>
</ul>

<p><code>width</code> and <code>height</code> reserve the image's space
before it loads, so the page doesn't jump around:</p>

<pre class="code">&lt;img src="grapefruit.jpg" alt="A sliced grapefruit"
     width="640" height="427"&gt;</pre>

<p>For images with <i>captions</i>, the semantic wrapper is
<code>&lt;figure&gt;</code> with <code>&lt;figcaption&gt;</code>:</p>

<pre class="code">&lt;figure&gt;
  &lt;img src="grapefruit.jpg" alt="A sliced grapefruit"&gt;
  &lt;figcaption&gt;Fig 1. Citrus paradise.&lt;/figcaption&gt;
&lt;/figure&gt;</pre>

<p>And a common gotcha: an image that fails to load shows the alt text in
its place — which is exactly why alt text should describe the
<i>information</i> ("A sliced grapefruit"), not the file
("grapefruit.jpg").</p>
""",
                "tryit": """<!DOCTYPE html>
<html lang="en">
<head><title>Images</title></head>
<body>
  <figure>
    <img
      src="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='200' height='150'%3E%3Crect width='200' height='150' fill='%23f16529'/%3E%3Ccircle cx='100' cy='75' r='45' fill='%23ffd43b'/%3E%3C/svg%3E"
      alt="An abstract orange-and-yellow graphic"
      width="200" height="150">
    <figcaption>Fig 1. A placeholder rendered from a data: URL.</figcaption>
  </figure>

  <img src="definitely-missing.jpg" alt="This alt text shows when the image fails to load"
       width="200">
</body>
</html>
""",
            },
            {
                "title": "Responsive Images",
                "html": """
<p>One image file does not fit every screen: a phone on mobile data and a
4K desktop want different things. HTML solves this with two tools.</p>

<p><b><code>srcset</code></b> offers the browser several resolutions of the
same image; it picks based on the screen:</p>

<pre class="code">&lt;img src="photo-small.jpg"
     srcset="photo-small.jpg 400w,
             photo-medium.jpg 800w,
             photo-large.jpg 1600w"
     sizes="(max-width: 600px) 400px, 800px"
     alt="A mountain lake"&gt;</pre>

<ul>
<li><code>srcset</code> lists candidate files with their widths
(<code>400w</code> = 400 pixels wide)</li>
<li><code>sizes</code> tells the browser how wide the image will
<i>render</i> under each condition — here: 400px on narrow screens,
otherwise 800px</li>
</ul>

<p><b><code>&lt;picture&gt;</code></b> goes further: it lets you swap the
<i>artwork</i> itself — different crops, or a modern format with a
fallback:</p>

<pre class="code">&lt;picture&gt;
  &lt;source srcset="photo.avif" type="image/avif"&gt;
  &lt;source srcset="photo.webp" type="image/webp"&gt;
  &lt;img src="photo.jpg" alt="A mountain lake"&gt;
&lt;/picture&gt;</pre>

<p>The browser walks the <code>&lt;source&gt;</code>s top-down and uses the
first it understands; the plain <code>&lt;img&gt;</code> at the bottom is
the mandatory fallback — and it's the element that carries
<code>alt</code>. Rules of thumb: same image, different sizes →
<code>srcset</code> alone; genuinely different files →
<code>&lt;picture&gt;</code>.</p>
""",
                "tryit": """<!DOCTYPE html>
<html lang="en">
<head><title>Responsive images</title></head>
<body>
  <p>Try resizing the preview — the browser swaps sources
     when you also change the window size.</p>

  <picture>
    <source
      srcset="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='400' height='120'%3E%3Crect width='400' height='120' fill='%232e8b57'/%3E%3Ctext x='200' y='66' text-anchor='middle' fill='white' font-size='18' font-family='Arial'%3Esource: the AVIF version%3C/text%3E%3C/svg%3E"
      type="image/svg+xml">
    <img
      src="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='400' height='120'%3E%3Crect width='400' height='120' fill='%23c0392b'/%3E%3Ctext x='200' y='66' text-anchor='middle' fill='white' font-size='18' font-family='Arial'%3Eimg: the fallback%3C/text%3E%3C/svg%3E"
      alt="A labelled rectangle" width="400" height="120">
  </picture>

  <p>This browser understood the first source, so it used it.</p>
</body>
</html>
""",
            },
            {
                "title": "Audio & Video",
                "html": """
<p>Sound and moving pictures are first-class citizens:
<code>&lt;audio&gt;</code> and <code>&lt;video&gt;</code> play media files
natively — no plugin, no Flash (RIP):</p>

<pre class="code">&lt;video src="cat.mp4" controls width="400"&gt;&lt;/video&gt;

&lt;audio src="birdsong.mp3" controls&gt;&lt;/audio&gt;</pre>

<p>The <b><code>controls</code></b> attribute shows the browser's play/
pause/volume UI — without it, media has no interface at all. Common
attributes for <code>&lt;video&gt;</code>:</p>

<ul>
<li><code>width</code> / <code>height</code> — display size</li>
<li><code>poster="frame.jpg"</code> — the image shown before play</li>
<li><code>autoplay muted playsinline</code> — browsers only allow
auto-playing <b>silent</b> video (try uninvited noise at 2 a.m. once and
you'll understand)</li>
<li><code>loop</code> — start again when it ends</li>
</ul>

<p>Like <code>&lt;picture&gt;</code>, both elements support multiple
sources for format compatibility, plus fallback content:</p>

<pre class="code">&lt;video controls width="400"&gt;
  &lt;source src="cat.webm" type="video/webm"&gt;
  &lt;source src="cat.mp4" type="video/mp4"&gt;
  Sorry, your browser can't play this video.
&lt;/video&gt;</pre>

<p>The last child that isn't a <code>&lt;source&gt;</code> renders only if
no source could play. And <code>&lt;track&gt;</code> adds
<b>subtitles/captions</b> — an accessibility essential:</p>

<pre class="code">&lt;video src="lecture.mp4" controls&gt;
  &lt;track src="en.vtt" kind="subtitles" label="English" srclang="en"&gt;
&lt;/video&gt;</pre>
""",
                "tryit": """<!DOCTYPE html>
<html lang="en">
<head><title>Media</title></head>
<body>
  <h2>Video (no source — watch the fallback!)</h2>
  <video controls width="320" poster="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='320' height='180'%3E%3Crect width='320' height='180' fill='%23263' /%3E%3Ctext x='160' y='95' text-anchor='middle' fill='white' font-size='16' font-family='Arial'%3Eposter frame%3C/text%3E%3C/svg%3E">
    <source src="missing.webm" type="video/webm">
    Sorry — no playable source here (this is the fallback text).
  </video>

  <h2>Audio element</h2>
  <audio controls></audio>
  <p>With controls, each media element shows its own player UI.</p>
</body>
</html>
""",
            },
        ],
        "quiz": [
            {
                "type": "blank",
                "question": "The two required attributes of <code>&lt;img&gt;</code> are <code>src</code> and <code>____</code>.",
                "answers": ["alt", "alt attribute"],
                "explain": "src points at the file; alt describes it for those who can't see it.",
            },
            {
                "type": "mc",
                "question": "A purely decorative image should have:",
                "options": [
                    "A long description",
                    "alt=\"\" (empty) so screen readers skip it",
                    "No alt attribute at all",
                    "alt=\"decoration\"",
                ],
                "answer": 1,
                "explain": "Empty alt says \"ignore me\" — missing alt makes screen readers read the filename instead.",
            },
            {
                "type": "mc",
                "question": "Same image in several resolutions for different screens — you reach for:",
                "options": ["&lt;picture&gt;", "srcset on &lt;img&gt;", "&lt;source&gt; alone", "multiple &lt;img&gt;s"],
                "answer": 1,
                "explain": "srcset (with sizes) offers resolution candidates; <picture> is for genuinely different files.",
            },
            {
                "type": "mc",
                "question": "Why do browsers refuse to autoplay video with sound?",
                "options": [
                    "A technical limitation",
                    "Uninvited audio is hostile — autoplay is only allowed when muted",
                    "It saves bandwidth",
                    "HTML forbids it",
                ],
                "answer": 1,
                "explain": "autoplay muted playsinline is the pattern browsers permit; sound requires a user gesture.",
            },
        ],
    },
]
