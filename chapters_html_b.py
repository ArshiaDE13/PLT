"""HTML Tutor chapters 6-9, grounded in MDN Web Docs (developer.mozilla.org)."""

CHAPTERS_HTML_B = [
    # ------------------------------------------------------------------ h06
    {
        "id": "h06",
        "title": "Document Structure & Semantic HTML",
        "emoji": "🏗️",
        "lessons": [
            {
                "title": "Sectioning Elements",
                "html": """
<p>A page is more than a pile of paragraphs — it has a header, a menu,
main content, sidebars, a footer. HTML reserves elements for exactly
these regions, and using them turns layout into meaning:</p>

<pre class="code">&lt;body&gt;
  &lt;header&gt;       site title, logo, tagline
    &lt;nav&gt;        the major navigation (a list of links!)
  &lt;/header&gt;

  &lt;main&gt;         THE content — one per page
    &lt;section&gt;    a thematic group (usually with a heading)
    &lt;article&gt;    self-contained: a post, a card, a comment
    &lt;aside&gt;      tangential: sidebar, related links, ads
  &lt;/main&gt;

  &lt;footer&gt;       copyright, contact, small links
  &lt;address&gt;      contact details for the page's author
&lt;/body&gt;</pre>

<p>The semantics, per MDN's guidance:</p>

<ul>
<li><b><code>&lt;header&gt;</code></b> — introductory content for its
nearest section or the page. Can appear several times (every
<code>&lt;article&gt;</code> can have one).</li>
<li><b><code>&lt;nav&gt;</code></b> — navigation blocks. Not every group of
links — the <i>major</i> ones.</li>
<li><b><code>&lt;main&gt;</code></b> — the unique content of this page;
exactly one per document, and everything that's "what this page is
about" lives inside it.</li>
<li><b><code>&lt;section&gt;</code></b> — a thematic grouping, almost always
with a heading. If you're adding it just for styling, that's a
<code>&lt;div&gt;</code>'s job.</li>
<li><b><code>&lt;article&gt;</code></b> — would this make sense on its own,
in a feed or printed alone? Then it's an article.</li>
<li><b><code>&lt;aside&gt;</code></b> — tangentially related content; remove
it and the main content still makes sense.</li>
<li><b><code>&lt;footer&gt;</code></b> — closing matter: author, copyright,
related links.</li>
</ul>
""",
                "tryit": """<!DOCTYPE html>
<html lang="en">
<head><title>Page anatomy</title>
<style>
  body { font-family: sans-serif; margin: 0; }
  header, nav, footer { background: #e44d26; color: #fff; padding: 10px 16px; }
  nav { background: #f16529; }
  main { padding: 16px; display: flex; gap: 16px; }
  section { flex: 2; } aside { flex: 1; background: #fff4ee; padding: 12px; }
  footer { background: #263238; }
</style></head>
<body>
  <header><strong>📰 The Daily Markup</strong></header>
  <nav>Home · Tech · About</nav>
  <main>
    <section>
      <h1>Top story</h1>
      <article><h2>Semantic HTML wins hearts</h2>
        <p>Developers report calmer dreams after switching to
           &lt;main&gt; and &lt;article&gt;.</p></article>
    </section>
    <aside><h3>Related</h3><p>Divs: a cautionary tale</p></aside>
  </main>
  <footer><address>Newsroom: 1 Web Way</address></footer>
</body>
</html>
""",
            },
            {
                "title": "div & span",
                "html": """
<p>After all that meaning, meet the two elements with <b>none</b>:
<code>&lt;div&gt;</code> (block-level) and
<code>&lt;span&gt;</code> (inline). They group things purely as
containers — hooks for CSS and JavaScript:</p>

<pre class="code">&lt;div class="card"&gt;          a block container: layout, boxes
  &lt;h3&gt;Card title&lt;/h3&gt;
  &lt;p&gt;Text with a &lt;span class="price"&gt;$4&lt;/span&gt; inline span.&lt;/p&gt;
&lt;/div&gt;</pre>

<ul>
<li><b><code>&lt;div&gt;</code></b> — a block-level box. Use it when no
semantic element fits: layout wrappers, grid items, card containers,
styling groups.</li>
<li><b><code>&lt;span&gt;</code></b> — an inline wrapper for text — marking
part of a sentence for styling or scripting without changing the
flow.</li>
</ul>

<p>The skill is knowing when <b>not</b> to use them. MDN's rule of thumb:
prefer a semantic element whenever one exists, and reach for div/span
only for pure grouping. Two smells of "div soup":</p>

<ul>
<li><code>&lt;div class="nav"&gt;</code> when
<code>&lt;nav&gt;</code> exists</li>
<li>a <code>&lt;div&gt;</code> wrapping a single styled word where a
<code>&lt;span&gt;</code> (or a real inline element) belongs</li>
</ul>

<p>A modern layout usually looks like: semantic skeleton (header/main/
article/footer) with a few divs inside for the grid — meaning on the
outside, containers on the inside.</p>
""",
                "tryit": """<!DOCTYPE html>
<html lang="en">
<head><title>div & span</title>
<style>
  .card { border: 2px solid #f16529; border-radius: 10px;
          padding: 12px; max-width: 320px; }
  .price { color: #2e8b57; font-weight: bold; }
  .badge { background: #e44d26; color: white; padding: 2px 8px;
           border-radius: 999px; font-size: 12px; }
</style></head>
<body>
  <div class="card">
    <h3>Fresh oranges <span class="badge">NEW</span></h3>
    <p>Juicy and sweet — <span class="price">$4.50/kg</span>
       while stocks last.</p>
  </div>
</body>
</html>
""",
            },
            {
                "title": "Semantic HTML & the Outline",
                "html": """
<p>"Semantic HTML" means choosing elements for what content <i>is</i>,
not how it should look. Why it's the web's most valuable habit:</p>

<ul>
<li><b>Accessibility:</b> screen readers navigate by landmarks and
headings. A real <code>&lt;button&gt;</code> is announced as "button" and
is keyboard-activatable; a clickable <code>&lt;div&gt;</code> is
announced as... nothing, and traps keyboard users.</li>
<li><b>SEO:</b> search engines lean on headings, landmarks and structure
to understand and rank a page.</li>
<li><b>Free behaviour:</b> native elements bring built-in keyboard
handling, focus, and form semantics you would have to rebuild by
hand.</li>
<li><b>Maintainability:</b> <code>&lt;nav&gt;</code> reads as intent — six
months later, so does the code.</li>
</ul>

<p>Together, headings and landmarks build the page's <b>outline</b> —
the machine-readable table of contents. Screen-reader users literally
browse this outline (press a key, hear "main, heading level 1,
Top story"), the way you scan a book's TOC. A div-based page has no
outline: to them it's an undifferentiated wall of text.</p>

<p>The practical checklist:</p>

<ul>
<li>One <code>&lt;h1&gt;</code>, heading levels without gaps</li>
<li>Landmarks: <code>header</code>/<code>nav</code>/<code>main</code>/
<code>footer</code> instead of styled divs</li>
<li>Real <code>&lt;button&gt;</code> for actions,
<code>&lt;a&gt;</code> for navigation — never a clickable div</li>
<li>Lists for lists, tables for data, <code>&lt;label&gt;</code> for
every form field</li>
</ul>
""",
                "tryit": """<!DOCTYPE html>
<html lang="en">
<head><title>Semantic outline</title>
<style> body { font-family: sans-serif; } </style></head>
<body>
  <header><h1>Coffee Guide</h1></header>
  <main>
    <section>
      <h2>Espresso</h2>
      <p>Small, strong, no apologies.</p>
    </section>
    <section>
      <h2>Latte</h2>
      <p>Milk-forward and friendly.</p>
    </section>
  </main>
  <footer><p>☕ Brewed with semantic HTML</p></footer>
</body>
</html>
""",
            },
        ],
        "quiz": [
            {
                "type": "mc",
                "question": "How many <code>&lt;main&gt;</code> elements per page?",
                "options": ["One", "One per section", "Unlimited", "Zero — it's deprecated"],
                "answer": 0,
                "explain": "main is the unique content region of the page — exactly one.",
            },
            {
                "type": "mc",
                "question": "A blog post that would make sense on its own in a feed is:",
                "options": ["&lt;section&gt;", "&lt;div&gt;", "&lt;article&gt;", "&lt;aside&gt;"],
                "answer": 2,
                "explain": "article = self-contained content: posts, cards, comments.",
            },
            {
                "type": "blank",
                "question": "The inline, non-semantic container element is <code>&lt;____&gt;</code>.",
                "answers": ["span", "span element"],
                "explain": "span = inline container, div = block container — both purely for grouping.",
            },
            {
                "type": "mc",
                "question": "Which is the best replacement for a clickable <code>&lt;div&gt;</code> that navigates?",
                "options": ["&lt;div onclick&gt; with a span inside", "&lt;a href&gt;", "&lt;span&gt;", "&lt;section&gt;"],
                "answer": 1,
                "explain": "Navigation is a link: <a href> gets focus, keyboard activation and screen-reader semantics for free.",
            },
        ],
    },

    # ------------------------------------------------------------------ h07
    {
        "id": "h07",
        "title": "Tables",
        "emoji": "📊",
        "lessons": [
            {
                "title": "Table Basics",
                "html": """
<p>Tables present <b>data with relationships</b> — rows and columns that
belong together: schedules, prices, comparisons. The trio:</p>

<pre class="code">&lt;table&gt;
  &lt;tr&gt;                       table row
    &lt;th&gt;Planet&lt;/th&gt;          table header cell
    &lt;th&gt;Moons&lt;/th&gt;
  &lt;/tr&gt;
  &lt;tr&gt;
    &lt;td&gt;Earth&lt;/td&gt;           table data cell
    &lt;td&gt;1&lt;/td&gt;
  &lt;/tr&gt;
  &lt;tr&gt;
    &lt;td&gt;Mars&lt;/td&gt;
    &lt;td&gt;2&lt;/td&gt;
  &lt;/tr&gt;
&lt;/table&gt;</pre>

<p>Anatomy, per MDN:</p>

<ul>
<li><code>&lt;table&gt;</code> — the whole thing</li>
<li><code>&lt;tr&gt;</code> — <b>table row</b>, wraps one row's cells</li>
<li><code>&lt;th&gt;</code> — a <b>header</b> cell: bold and centred by
default, and semantically "this labels the row/column"</li>
<li><code>&lt;td&gt;</code> — a <b>data</b> cell</li>
</ul>

<p>Give the table a name with <code>&lt;caption&gt;</code> — the first
child of <code>&lt;table&gt;</code>:</p>

<pre class="code">&lt;table&gt;
  &lt;caption&gt;Planets and their moon counts&lt;/caption&gt;
  ...
&lt;/table&gt;</pre>

<p>Two warnings from experience: tables are for <b>data</b>, never for
page layout (a 2003 habit that makes pages inaccessible); and raw tables
come unstyled — borders and spacing are CSS's job.</p>
""",
                "tryit": """<!DOCTYPE html>
<html lang="en">
<head><title>Tables</title>
<style>
  table { border-collapse: collapse; }
  th, td { border: 1px solid #ccc; padding: 6px 14px; text-align: left; }
  th { background: #fff1ea; }
  caption { caption-side: top; font-weight: bold; padding: 6px; }
</style></head>
<body>
  <table>
    <caption>Planets and their moon counts</caption>
    <tr><th>Planet</th><th>Moons</th><th>Ringed?</th></tr>
    <tr><td>Earth</td><td>1</td><td>no</td></tr>
    <tr><td>Mars</td><td>2</td><td>no</td></tr>
    <tr><td>Jupiter</td><td>95</td><td>yes</td></tr>
  </table>
</body>
</html>
""",
            },
            {
                "title": "Head, Body, Foot & Spanning",
                "html": """
<p>Long tables get a skeleton in three parts — and cells can stretch
across several rows or columns.</p>

<p>The three sections:</p>

<pre class="code">&lt;table&gt;
  &lt;thead&gt;    column headers
    &lt;tr&gt;&lt;th&gt;Item&lt;/th&gt;&lt;th&gt;Qty&lt;/th&gt;&lt;th&gt;Price&lt;/th&gt;&lt;/tr&gt;
  &lt;/thead&gt;
  &lt;tbody&gt;    the data (browsers add one even if you don't)
    &lt;tr&gt;&lt;td&gt;Coffee&lt;/td&gt;&lt;td&gt;2&lt;/td&gt;&lt;td&gt;$6&lt;/td&gt;&lt;/tr&gt;
    &lt;tr&gt;&lt;td&gt;Tea&lt;/td&gt;&lt;td&gt;1&lt;/td&gt;&lt;td&gt;$3&lt;/td&gt;&lt;/tr&gt;
  &lt;/tbody&gt;
  &lt;tfoot&gt;    summary rows
    &lt;tr&gt;&lt;td colspan="2"&gt;Total&lt;/td&gt;&lt;td&gt;$9&lt;/td&gt;&lt;/tr&gt;
  &lt;/tfoot&gt;
&lt;/table&gt;</pre>

<p>Beyond structure, the sections enable repeated headers when printing,
sticky headers when scrolling, and clearer targeting for styling.</p>

<p><b>Spanning</b> merges cells:</p>

<ul>
<li><code>colspan="2"</code> — this cell occupies <b>2 columns</b></li>
<li><code>rowspan="3"</code> — this cell occupies <b>3 rows</b></li>
</ul>

<p>The rule that keeps tables honest: whatever you span, the other rows
must not also contain those cells — a merged cell is <i>shared</i>, not
duplicated. Span carefully: deeply merged tables are unreadable both to
screen readers and to the human three weeks later who has to fix
them.</p>
""",
                "tryit": """<!DOCTYPE html>
<html lang="en">
<head><title>Table sections</title>
<style>
  table { border-collapse: collapse; font-family: sans-serif; }
  th, td { border: 1px solid #ddd; padding: 6px 16px; }
  thead th { background: #e44d26; color: white; }
  tfoot td { font-weight: bold; background: #fff1ea; }
</style></head>
<body>
  <table>
    <caption>Café order</caption>
    <thead>
      <tr><th>Item</th><th>Qty</th><th>Price</th></tr>
    </thead>
    <tbody>
      <tr><td>Coffee</td><td>2</td><td>$6</td></tr>
      <tr><td>Tea</td><td>1</td><td>$3</td></tr>
    </tbody>
    <tfoot>
      <tr><td colspan="2">Total</td><td>$9</td></tr>
    </tfoot>
  </table>
</body>
</html>
""",
            },
            {
                "title": "Table Accessibility",
                "html": """
<p>Tables are the classic accessibility trap: sighted users see the grid,
screen-reader users hear cells one by one — and only proper markup tells
them <i>which headers</i> each cell belongs to.</p>

<p><b>Level 1 — use <code>&lt;th&gt;</code></b>. Header cells are announced
as headers, and for simple tables (headers only in the top row and/or
first column) that alone is enough.</p>

<p><b>Level 2 — <code>scope</code></b>. Say explicitly what a header
labels:</p>

<pre class="code">&lt;tr&gt;
  &lt;th scope="col"&gt;Month&lt;/th&gt;
  &lt;th scope="col"&gt;Sales&lt;/th&gt;
&lt;/tr&gt;
&lt;tr&gt;
  &lt;th scope="row"&gt;January&lt;/th&gt;
  &lt;td&gt;$1,200&lt;/td&gt;
&lt;/tr&gt;</pre>

<p>Now "January, Sales, $1,200" is spoken as a coherent fact instead of
three loose words.</p>

<p><b>Level 3 — <code>headers</code>/<code>id</code></b>, only for complex
tables with multi-level headers: give each <code>&lt;th&gt;</code> an id
and list those ids in each data cell's <code>headers</code> attribute.
Powerful, verbose, rare — reach for it when scope isn't enough.</p>

<p>And the checklist that prevents most suffering:</p>

<ul>
<li><code>&lt;caption&gt;</code> names the table (screen readers announce it
on entry)</li>
<li>Real <code>&lt;th&gt;</code>s, with <code>scope</code></li>
<li>Never tables for layout — use CSS grid/flexbox; layout tables
confuse screen readers into reading spreadsheets that aren't
there</li>
<li>Keep it simple: if you need cells nested inside cells, the data
wants to be several small tables (or a list)</li>
</ul>
""",
                "tryit": """<!DOCTYPE html>
<html lang="en">
<head><title>Accessible tables</title>
<style>
  table { border-collapse: collapse; font-family: sans-serif; }
  th, td { border: 1px solid #ddd; padding: 6px 14px; text-align: left; }
  thead th { background: #f16529; color: white; }
  tbody th { background: #fff1ea; }
</style></head>
<body>
  <table>
    <caption>Monthly sales — note the scope attributes in the source</caption>
    <thead>
      <tr><th scope="col">Month</th><th scope="col">Sales</th></tr>
    </thead>
    <tbody>
      <tr><th scope="row">January</th><td>$1,200</td></tr>
      <tr><th scope="row">February</th><td>$1,850</td></tr>
    </tbody>
  </table>
</body>
</html>
""",
            },
        ],
        "quiz": [
            {
                "type": "mc",
                "question": "Which element wraps the cells of a single row?",
                "options": ["&lt;tr&gt;", "&lt;td&gt;", "&lt;table&gt;", "&lt;row&gt;"],
                "answer": 0,
                "explain": "table row <tr> holds <th>/<td> cells.",
            },
            {
                "type": "mc",
                "question": "A total row at the bottom of a long table belongs in:",
                "options": ["&lt;thead&gt;", "&lt;tbody&gt;", "&lt;tfoot&gt;", "&lt;caption&gt;"],
                "answer": 2,
                "explain": "tfoot = table footer: summary rows like totals.",
            },
            {
                "type": "blank",
                "question": "To make a cell span two columns, set <code>____=\"2\"</code>.",
                "answers": ["colspan"],
                "explain": "colspan merges columns; rowspan merges rows.",
            },
            {
                "type": "mc",
                "question": "Why does &lt;th scope=\"col\"&gt; matter for accessibility?",
                "options": [
                    "It makes the header bold",
                    "It tells screen readers which cells this header labels",
                    "It is required for validation",
                    "It improves SEO only",
                ],
                "answer": 1,
                "explain": "scope connects headers to data cells so a cell is heard as 'January, Sales, $1,200'.",
            },
        ],
    },

    # ------------------------------------------------------------------ h08
    {
        "id": "h08",
        "title": "Forms",
        "emoji": "📝",
        "lessons": [
            {
                "title": "Form Basics",
                "html": """
<p>Forms are how the web listens: search boxes, logins, checkouts, every
comment field. The container is <code>&lt;form&gt;</code>, the workhorse
is <code>&lt;input&gt;</code>, and the visitor's friend is
<code>&lt;label&gt;</code>:</p>

<pre class="code">&lt;form action="/signup" method="post"&gt;
  &lt;label for="email"&gt;Email&lt;/label&gt;
  &lt;input id="email" name="email" type="email"&gt;

  &lt;button type="submit"&gt;Sign up&lt;/button&gt;
&lt;/form&gt;</pre>

<p>Three load-bearing ideas:</p>

<ul>
<li><code>action</code> — the URL that receives the data;
<code>method</code> — how it travels (<code>get</code> puts data in the
URL, <code>post</code> in the request body)</li>
<li><code>name</code> on each input — the key the data travels under. An
input without <code>name</code> is <b>not submitted at all</b> — the
classic lost-data bug</li>
<li><code>&lt;label for="id"&gt;</code> — connects text to its field. Click
the label, the field focuses; screen readers announce the label when the
field is entered. Every input gets a label — no exceptions</li>
</ul>

<p><code>&lt;button&gt;</code> submits the form by default
(<code>type="submit"</code>); give it
<code>type="button"</code> when it should do something else.</p>
""",
                "tryit": """<!DOCTYPE html>
<html lang="en">
<head><title>Form basics</title>
<style> body { font-family: sans-serif; } form { max-width: 280px; }
  input, button { padding: 6px; margin: 4px 0; } </style></head>
<body>
  <form>
    <label for="email">Email</label><br>
    <input id="email" name="email" type="email"
           placeholder="you@example.com"><br>
    <button type="submit">Sign up</button>
  </form>
  <p>Submitting navigates — the action URL is empty here, so the
     page reloads with ?email=... in the address bar.</p>
</body>
</html>
""",
            },
            {
                "title": "Input Types",
                "html": """
<p>The <code>type</code> attribute turns one element —
<code>&lt;input&gt;</code> — into around twenty different controls, each
with the right keyboard, validation and mobile UI:</p>

<pre class="code">&lt;input type="text"&gt;      plain text
&lt;input type="email"&gt;     @-validated, email keyboard on phones
&lt;input type="password"&gt;  dots instead of letters
&lt;input type="number"&gt;    numeric keyboard, steppers
&lt;input type="tel"&gt;       phone number
&lt;input type="date"&gt;      a date picker
&lt;input type="color"&gt;     a colour swatch picker
&lt;input type="range"&gt;     a slider
&lt;input type="checkbox"&gt;  yes/no, multiple choices
&lt;input type="radio"&gt;     pick exactly one of a group
&lt;input type="file"&gt;      upload picker
&lt;input type="hidden"&gt;    invisible — machine data only</pre>

<p>Radio buttons group by sharing the same <code>name</code>; each also
needs a <code>value</code> (that's what gets submitted) and its own
label:</p>

<pre class="code">&lt;fieldset&gt;
  &lt;legend&gt;Size&lt;/legend&gt;
  &lt;input type="radio" id="s" name="size" value="s"&gt;
  &lt;label for="s"&gt;Small&lt;/label&gt;
  &lt;input type="radio" id="m" name="size" value="m"&gt;
  &lt;label for="m"&gt;Medium&lt;/label&gt;
&lt;/fieldset&gt;</pre>

<p>Checkboxes, by contrast, are independent — same name is fine, and
each carries its own on/off state.</p>
""",
                "tryit": """<!DOCTYPE html>
<html lang="en">
<head><title>Input types</title>
<style> body { font-family: sans-serif; line-height: 2.2 } </style></head>
<body>
  <input type="text" placeholder="text">
  <input type="email" placeholder="email">
  <input type="password" placeholder="password"><br>
  <input type="number" value="42">
  <input type="date">
  <input type="color" value="#e44d26"><br>
  <input type="range" min="0" max="100" value="30">

  <p>Radio group (pick one):</p>
  <input type="radio" id="cat" name="pet" value="cat" checked>
  <label for="cat">Cat</label>
  <input type="radio" id="dog" name="pet" value="dog">
  <label for="dog">Dog</label>

  <p>Checkboxes (pick any):</p>
  <input type="checkbox" id="milk" name="extra" value="milk" checked>
  <label for="milk">Milk</label>
  <input type="checkbox" id="sugar" name="extra" value="sugar">
  <label for="sugar">Sugar</label>
</body>
</html>
""",
            },
            {
                "title": "textarea, select & option",
                "html": """
<p>Not every answer fits in one line. Three more controls cover the
rest:</p>

<p><b><code>&lt;textarea&gt;</code></b> — multi-line text (comments,
messages). Unlike <code>&lt;input&gt;</code>, it is NOT a void element:
its default content goes between the tags, and rows/cols suggest the
size:</p>

<pre class="code">&lt;textarea name="message" rows="4" cols="40"&gt;
Prefilled text here
&lt;/textarea&gt;</pre>

<p><b><code>&lt;select&gt;</code></b> — a dropdown of
<code>&lt;option&gt;</code>s. The submitted value is each option's
<code>value</code>; the visible text is its content:</p>

<pre class="code">&lt;label for="planet"&gt;Favourite planet&lt;/label&gt;
&lt;select id="planet" name="planet"&gt;
  &lt;option value=""&gt;— choose —&lt;/option&gt;
  &lt;option value="mars"&gt;Mars&lt;/option&gt;
  &lt;option value="titan" selected&gt;Titan&lt;/option&gt;
&lt;/select&gt;</pre>

<ul>
<li><code>selected</code> pre-chooses an option (the default is the
first one)</li>
<li>add the <code>multiple</code> attribute for a multi-select list</li>
<li><code>&lt;optgroup label="Inner planets"&gt;</code> groups options</li>
</ul>

<p><b><code>&lt;datalist&gt;</code></b> is the hybrid: suggestions for a
text input, still free-typed — an "autocomplete" with no JavaScript:</p>

<pre class="code">&lt;input list="planets" name="planet"&gt;
&lt;datalist id="planets"&gt;
  &lt;option value="Mars"&gt;
  &lt;option value="Venus"&gt;
&lt;/datalist&gt;</pre>
""",
                "tryit": """<!DOCTYPE html>
<html lang="en">
<head><title>textarea, select, datalist</title>
<style> body { font-family: sans-serif; line-height: 2.4 } </style></head>
<body>
  <label for="msg">Message</label><br>
  <textarea id="msg" name="message" rows="3" cols="34">You can edit me…</textarea><br>

  <label for="planet">Planet</label>
  <select id="planet" name="planet">
    <option value="">— choose —</option>
    <option value="mars">Mars</option>
    <option value="titan" selected>Titan</option>
  </select><br>

  <label for="p2">Or type one</label>
  <input id="p2" name="p2" list="planets" placeholder="type 'M'…">
  <datalist id="planets">
    <option value="Mercury">
    <option value="Venus">
    <option value="Mars">
  </datalist>
</body>
</html>
""",
            },
            {
                "title": "fieldset & legend",
                "html": """
<p>Groups of related fields deserve a visible frame and a group label —
that is <code>&lt;fieldset&gt;</code> and
<code>&lt;legend&gt;</code>:</p>

<pre class="code">&lt;fieldset&gt;
  &lt;legend&gt;Shipping address&lt;/legend&gt;

  &lt;label for="street"&gt;Street&lt;/label&gt;
  &lt;input id="street" name="street"&gt;

  &lt;label for="city"&gt;City&lt;/label&gt;
  &lt;input id="city" name="city"&gt;
&lt;/fieldset&gt;</pre>

<p><code>&lt;legend&gt;</code> must be the <b>first child</b> of the
fieldset — it becomes the group's caption (rendered on the frame's
border by default, restyled by CSS).</p>

<p>Beyond looks, fieldsets carry meaning. Two places they shine:</p>

<ul>
<li><b>Radio groups:</b> a legend tells screen-reader users what the
radio buttons are collectively choosing ("Payment method: Credit card
/ PayPal / ..."). Without it, clicking into the third radio button is a
guessing game.</li>
<li><b>Form sections:</b> shipping vs billing, personal vs account —
long forms become scannable chapters.</li>
</ul>

<p>Fieldsets can also take <code>disabled</code> — disabling every
control inside at once, the standard trick for freezing a whole section
while, say, "use billing address" is checked.</p>
""",
                "tryit": """<!DOCTYPE html>
<html lang="en">
<head><title>fieldset & legend</title>
<style> body { font-family: sans-serif; } fieldset { max-width: 300px; }
  legend { font-weight: bold; color: #e44d26; padding: 0 6px; } </style>
</head>
<body>
  <form>
    <fieldset>
      <legend>Payment method</legend>
      <input type="radio" id="card" name="pay" value="card" checked>
      <label for="card">Credit card</label><br>
      <input type="radio" id="paypal" name="pay" value="paypal">
      <label for="paypal">PayPal</label><br>
      <input type="radio" id="cod" name="pay" value="cod">
      <label for="cod">Cash on delivery</label>
    </fieldset>
  </form>
</body>
</html>
""",
            },
            {
                "title": "Common Attributes",
                "html": """
<p>A handful of attributes cover most of form behaviour. The data
plumbing:</p>

<ul>
<li><code>name</code> — the key in the submitted data (mandatory for
submission)</li>
<li><code>value</code> — the current/submitted value; also the choice a
radio or checkbox represents</li>
</ul>

<p>The user-experience set:</p>

<ul>
<li><code>placeholder</code> — hint text inside an empty field. A hint,
<b>never</b> a label replacement: it vanishes on typing and is easy to
confuse with a filled-in value</li>
<li><code>required</code> — the form cannot submit while this is empty;
the browser blocks it and explains</li>
<li><code>disabled</code> — un-usable and un-clickable, <b>excluded from
submission</b>, and not focusable</li>
<li><code>readonly</code> — visible and submitted, but not editable
(useful for computed values)</li>
<li><code>checked</code> — pre-selects a checkbox/radio</li>
<li><code>min</code>/<code>max</code>/<code>step</code>/<code>maxlength</code>/
<code>pattern</code> — constraint details (next lesson uses them)</li>
</ul>

<pre class="code">&lt;input name="code" value="HT-2026" readonly&gt;
&lt;input name="coupon" placeholder="SUMMER10" required&gt;
&lt;button disabled&gt;Unavailable&lt;/button&gt;</pre>

<p>disabled vs readonly is a favourite interview question and a real UX
decision: disabled means "this doesn't apply to you right now";
readonly means "look but don't touch — it still counts".</p>
""",
                "tryit": """<!DOCTYPE html>
<html lang="en">
<head><title>Attributes</title>
<style> body { font-family: sans-serif; line-height: 2.4 } </style></head>
<body>
  <form>
    <label>readonly: <input value="HT-2026" readonly></label><br>
    <label>required: <input required placeholder="can't submit empty"></label><br>
    <label>disabled: <input value="locked" disabled></label><br>
    <label>maxlength=5: <input maxlength="5" placeholder="12345"></label><br>
    <button>Submit (try it!)</button>
  </form>
</body>
</html>
""",
            },
            {
                "title": "Validation & Submission",
                "html": """
<p>The browser validates forms <b>before</b> anything is sent — free,
instant, on every device. Constraints come from attributes; CSS can even
style the outcome via <code>:valid</code>, <code>:invalid</code>,
<code>:required</code>:</p>

<pre class="code">&lt;input type="email" required&gt;             must be a non-empty email
&lt;input type="number" min="1" max="10"&gt;    range
&lt;input minlength="8" maxlength="20"&gt;      length
&lt;input pattern="[A-Za-z]{3}[0-9]{4}"&gt;     regex: ABC1234
&lt;input title="3 letters + 4 digits" pattern="..."&gt;</pre>

<p>When a constraint fails, submission is blocked and the browser shows a
<bubble</b> — styled with the <code>::invalid</code> state and explained
by the <code>title</code> attribute or built-in messages. MDN calls this
whole system the <b>constraint validation API</b>.</p>

<p><b>Submission</b>: pressing the submit button (or Enter in a text
field) sends the data to <code>action</code> via <code>method</code>:</p>

<ul>
<li><code>method="get"</code> — data in the URL
(<code>?email=a@b.c</code>): bookmarkable, visible — right for searches
and filters</li>
<li><code>method="post"</code> — data in the request body: right for
anything that changes something (signups, orders)</li>
</ul>

<p>Then take over with JavaScript when needed:
<code>form.noValidate = true</code> (or the
<code>novalidate</code> attribute) switches off the built-in bubbles so
you can show your own; <code>form.addEventListener("submit", ...)</code>
with <code>event.preventDefault()</code> handles the data yourself —
the standard pattern behind AJAX-style forms.</p>
""",
                "tryit": """<!DOCTYPE html>
<html lang="en">
<head><title>Validation</title>
<style> body { font-family: sans-serif; } input { display: block; margin: 4px 0; }
  input:invalid { border-color: #c0392b; } input:valid { border-color: #2e8b57; }
  input, button { padding: 6px; } </style></head>
<body>
  <form>
    <label>Username (3 letters + 4 digits)
      <input name="user" required pattern="[A-Za-z]{3}[0-9]{4}"
             title="3 letters followed by 4 digits, e.g. ABC1234">
    </label>
    <label>Age (1–120)
      <input type="number" min="1" max="120" name="age">
    </label>
    <button>Submit</button>
  </form>
  <p>Green border = valid. Try submitting empty or wrong — the browser
     blocks it and explains.</p>
</body>
</html>
""",
            },
        ],
        "quiz": [
            {
                "type": "mc",
                "question": "An input without a name attribute is:",
                "options": [
                    "Submitted with an empty key",
                    "Not submitted at all",
                    "Rejected by the browser",
                    "Required to have one",
                ],
                "answer": 1,
                "explain": "name is the key the data travels under — no name, no submission.",
            },
            {
                "type": "mc",
                "question": "Which attribute connects a label to its field?",
                "options": [
                    "label links to input via for=\"id\" matching the input's id",
                    "name",
                    "wrap — labels must wrap inputs only",
                    "ref",
                ],
                "answer": 0,
                "explain": "<label for=\"email\"> + <input id=\"email\"> — click the label, focus the field; screen readers announce it.",
            },
            {
                "type": "mc",
                "question": "disabled vs readonly — which is still submitted?",
                "options": ["disabled", "readonly", "both", "neither"],
                "answer": 1,
                "explain": "readonly is read-only but part of the data; disabled is excluded from submission entirely.",
            },
            {
                "type": "blank",
                "question": "The attribute that blocks submission while a field is empty is <code>____</code>.",
                "answers": ["required"],
                "explain": "required engages the browser's constraint validation for empty fields.",
            },
            {
                "type": "mc",
                "question": "method=\"get\" is the right choice when the form:",
                "options": [
                    "Creates an account",
                    "Places an order",
                    "Is a search box — data in the URL is shareable",
                    "Uploads a file",
                ],
                "answer": 2,
                "explain": "get puts data in the URL (bookmarkable searches); post is for state-changing operations.",
            },
        ],
    },

    # ------------------------------------------------------------------ h09
    {
        "id": "h09",
        "title": "Global Attributes",
        "emoji": "🏷️",
        "lessons": [
            {
                "title": "id & class",
                "html": """
<p>Two attributes exist to name elements, and CSS and JavaScript live
off them.</p>

<p><b><code>id</code></b> — a <b>unique</b> identifier for exactly one
element on the page:</p>

<pre class="code">&lt;h1 id="page-title"&gt;Welcome&lt;/h1&gt;

&lt;a href="#page-title"&gt;jump to it&lt;/a&gt;        fragment navigation
&lt;label for="email"&gt;                          pairs with inputs
#page-title { color: red }                   CSS selector (one!)
document.getElementById("page-title")        JS lookup</pre>

<p>Rules: unique in the document, at least one character, no spaces.
Duplicates don't crash anything — but <code>getElementById</code> and
fragment links behave unpredictably, so don't.</p>

<p><b><code>class</code></b> — a membership tag; elements can share
classes, and one element can carry several (space-separated):</p>

<pre class="code">&lt;p class="note"&gt;A note&lt;/p&gt;
&lt;p class="note urgent"&gt;An urgent note&lt;/p&gt;

.note   { font-style: italic; }      all notes
.urgent { color: crimson; }          the urgent ones</pre>

<p>The design rule of thumb: <code>id</code> for "this exact thing"
(targets, labels, JS handles); <code>class</code> for "things like
this" (styling categories). When a page needs a CSS hook, most teams
reach for classes first — they compose.</p>
""",
                "tryit": """<!DOCTYPE html>
<html lang="en">
<head><title>id & class</title>
<style>
  .note { border-left: 4px solid #f16529; padding: 8px 12px;
          background: #fff4ee; }
  .urgent { border-left-color: #c0392b; color: #c0392b; }
  #mission { color: #2e8b57; font-weight: bold; }
</style></head>
<body>
  <h1 id="mission">Our mission</h1>

  <p class="note">A regular note.</p>
  <p class="note urgent">An urgent note — two classes!</p>

  <a href="#mission">Jump back to the mission (via its id)</a>
</body>
</html>
""",
            },
            {
                "title": "title, style, lang & dir",
                "html": """
<p>Four more global attributes — available on every element, per MDN's
global attributes list.</p>

<p><b><code>title</code></b> — a tooltip: hover the element and the
browser shows it after a moment. Also read aloud by screen readers as
supplementary info. Fine for hints, poor for essential text (invisible
on touch screens):</p>

<pre class="code">&lt;abbr title="HyperText Markup Language"&gt;HTML&lt;/abbr&gt;</pre>

<p><b><code>style</code></b> — inline CSS, right on the element:</p>

<pre class="code">&lt;p style="color: #e44d26; font-weight: bold"&gt;Orange and bold&lt;/p&gt;</pre>

<p>Convenient for one-offs (and for this course's little demos!), but
the worst place for real styling: it can't be reused, can't use
<code>:hover</code>, and fights the cascade. Style sheets win; inline
style is for exceptions.</p>

<p><b><code>lang</code></b> — declares the language of that element's
content, overriding the page default. Vital for screen readers (a
Persian paragraph inside an English page needs
<code>lang="fa"</code> to be read with the right voice) and for
hyphenation, spellcheck and font selection:</p>

<pre class="code">&lt;p&gt;The Persian word for web is
   &lt;span lang="fa" dir="rtl"&gt;وب&lt;/span&gt;.&lt;/p&gt;</pre>

<p><b><code>dir</code></b> — text direction: <code>ltr</code> (default),
<code>rtl</code> for right-to-left scripts like Persian and Arabic, or
<code>auto</code> (guess from the first strong character). Essential for
bilingual pages — this very site uses both.</p>
""",
                "tryit": """<!DOCTYPE html>
<html lang="en">
<head><title>title, style, lang, dir</title></head>
<body>
  <p>Hover this: <abbr title="HyperText Markup Language">HTML</abbr></p>

  <p style="color:#e44d26; font-weight:bold">Inline style in action</p>

  <p>The Persian word for web is
     <span lang="fa" dir="rtl" style="font-size: 20px">وب</span>
     — written right-to-left.</p>

  <p dir="rtl" lang="fa">این جمله راست‌به‌چپ است.</p>
</body>
</html>
""",
            },
            {
                "title": "hidden, data-* & Interaction Attributes",
                "html": """
<p>The rest of the everyday global set.</p>

<p><b><code>hidden</code></b> — a boolean attribute that removes the
element from display (like <code>display: none</code>). Semantic
"this is currently not relevant" — state, not styling:</p>

<pre class="code">&lt;p hidden&gt;Only shown by JavaScript when needed&lt;/p&gt;</pre>

<p><b><code>data-*</code></b> — invent your own attributes, as long as
they start with <code>data-</code>: a private channel between HTML and
JavaScript. HTML never interprets them; scripts read them with
<code>dataset</code>:</p>

<pre class="code">&lt;button data-product-id="42" data-stock="3"&gt;Add to cart&lt;/button&gt;

&lt;script&gt;
  const btn = document.querySelector("button");
  console.log(btn.dataset.productId);   // "42"
  console.log(btn.dataset.stock);       // "3"
&lt;/script&gt;</pre>

<p><b>The interaction attributes:</b></p>

<ul>
<li><code>contenteditable</code> — makes the element's content editable
in the browser (the root of every rich-text editor)</li>
<li><code>spellcheck</code> — enable/disable the spellchecker</li>
<li><code>draggable</code> — the element participates in drag &amp; drop
(HTML 12 puts it to work)</li>
<li><code>tabindex</code> — controls keyboard focus order:
<code>0</code> joins the natural tab order (for custom widgets),
<code>-1</code> allows programmatic focus only, positive numbers
manually order — an anti-pattern that breaks the expected flow; avoid
them</li>
</ul>

<pre class="code">&lt;p contenteditable="true" spellcheck="false"&gt;Edit me!&lt;/p&gt;</pre>
""",
                "tryit": """<!DOCTYPE html>
<html lang="en">
<head><title>hidden, data-*, contenteditable</title>
<style> body { font-family: sans-serif; } [hidden] { } </style></head>
<body>
  <p contenteditable="true" style="border:1px dashed #f16529; padding:8px">
    This paragraph is contenteditable — click and type!
  </p>

  <button data-product-id="42" data-stock="3" onclick="
    this.nextElementSibling.hidden = false;
    this.nextElementSibling.textContent =
      'product ' + this.dataset.productId +
      ' has stock ' + this.dataset.stock;
  ">Read my data-*</button>
  <p hidden></p>
</body>
</html>
""",
            },
        ],
        "quiz": [
            {
                "type": "mc",
                "question": "Which attribute names ONE specific element, uniquely?",
                "options": ["class", "id", "name", "data-id"],
                "answer": 1,
                "explain": "id must be unique in the document; class marks group membership.",
            },
            {
                "type": "mc",
                "question": "How many classes can one element carry?",
                "options": ["One", "Two", "As many as needed, space-separated", "Classes are CSS-only"],
                "answer": 2,
                "explain": "class=\"note urgent\" — space-separated list.",
            },
            {
                "type": "blank",
                "question": "Custom attributes for JavaScript must start with <code>____</code>.",
                "answers": ["data-", "data"],
                "explain": "data-* attributes are the sanctioned private channel (read via element.dataset).",
            },
            {
                "type": "mc",
                "question": "Which pair makes a Persian paragraph inside an English page read correctly?",
                "options": ["lang=\"fa\" dir=\"rtl\"", "rtl=\"true\"", "lang=\"arabic\"", "dir is CSS-only"],
                "answer": 0,
                "explain": "lang sets the language (screen-reader voice, fonts); dir sets the text direction.",
            },
        ],
    },
]
