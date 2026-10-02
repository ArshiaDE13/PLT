"""JS Tutor chapters 9-10 (Phases 9-10), grounded in MDN Web Docs."""

CHAPTERS_JS_D = [
    # ------------------------------------------------------------------ js09
    {
        "id": "js09",
        "title": "Browser JavaScript",
        "emoji": "🌐",
        "lessons": [
            {
                "title": "DOM & Selecting Elements",
                "html": """
<p>The <b>DOM (Document Object Model)</b> is a live tree of objects
the browser builds from your HTML — every tag becomes a node with
properties and methods. "Live" is the key word: change the tree and
the page repaints instantly. Before you can change anything, you
must select it — and <code>document.querySelector</code> is the
modern one-liner for that.</p>

<pre class="code">// select ONE element
const el = document.querySelector(".card");       // first match
const byId = document.getElementById("header");   // by id

// select ALL matching elements (returns NodeList)
const items = document.querySelectorAll(".item");
items.forEach(item =&gt; console.log(item.textContent));</pre>

<p>Predict the block: <code>querySelector(".card")</code> takes ANY
CSS selector and returns the FIRST matching element, or
<code>null</code> if nothing matches. <code>getElementById("header")</code>
is the older, fastest specialist — id lookups only. And
<code>querySelectorAll(".item")</code> returns every match wrapped in
a <code>NodeList</code>, which supports <code>forEach</code>
directly; if you need array methods like <code>map</code>, spread it
first: <code>[...items]</code>.</p>

<ul>
<li><code>querySelector</code> — uses CSS selectors, returns the first
match (or null)</li>
<li><code>querySelectorAll</code> — returns a static NodeList (use
<code>forEach</code> or spread to an array)</li>
<li><code>getElementById</code> — fastest, but only for IDs</li>
</ul>

<p>Rules of thumb that cover most real choices: querySelector for
flexibility (classes, nesting, attributes), getElementById when an id
exists, querySelectorAll for groups. Anything you can select in a
stylesheet, you can grab in JS — that is the whole mental model.</p>

<p>Gotcha: <code>querySelector</code> returning <code>null</code> is
the source of endless "Cannot read properties of null" errors. It
usually means your script ran before the HTML existed — put scripts
at the end of <code>&lt;body&gt;</code> or use <code>defer</code> —
or that your selector has a typo.</p>
""",
                "tryit": """<!DOCTYPE html>
<html>
<head><style>
  .highlight { background: #ffd43b; }
  .box { padding: 8px; margin: 4px; border: 2px solid #1572b6;
         border-radius: 6px; }
</style></head>
<body>
  <div id="app">
    <div class="box" data-id="1">Item 1</div>
    <div class="box" data-id="2">Item 2</div>
    <div class="box" data-id="3">Item 3</div>
  </div>
  <script>
    // select and modify
    const first = document.querySelector(".box");
    first.textContent = "← selected by querySelector";

    // select all and highlight
    document.querySelectorAll(".box").forEach(box => {
      box.classList.add("highlight");
    });

    // by data attribute
    const item2 = document.querySelector('[data-id="2"]');
    console.log("item 2:", item2?.textContent);
  </script>
</body>
</html>
""",
            },
            {
                "title": "Creating & Modifying Elements",
                "html": """
<p>Pages like todo lists, chats and feeds never ship every item in
the HTML — JavaScript builds them at runtime. The workflow is always
the same four beats: <b>create</b> an element with
<code>createElement</code>, <b>fill</b> it with text, classes and
attributes, <b>insert</b> it into the tree, and later <b>remove</b>
it. Modifying existing elements reuses the same fill and remove
tools.</p>

<pre class="code">// create
const div = document.createElement("div");
div.textContent = "Hello!";
div.className = "card";
div.innerHTML = "&lt;strong&gt;Bold&lt;/strong&gt; text";

// modify existing
el.textContent = "new text";        // safe (no HTML parsing)
el.innerHTML = "&lt;b&gt;parsed&lt;/b&gt;";   // parses HTML (XSS risk with user data!)
el.setAttribute("data-id", "42");
el.classList.add("active");
el.classList.remove("hidden");
el.classList.toggle("dark");
el.style.color = "#1572b6";

// insert into the DOM
parent.appendChild(el);              // add as last child
parent.prepend(el);                  // add as first child
el.before(newEl);                    // insert before
el.after(newEl);                     // insert after
el.remove();                         // delete</pre>

<p>Walk it top to bottom. <code>createElement("div")</code> makes a
detached <code>&lt;div&gt;</code> — it exists in memory but is not on
the page yet. Setting <code>textContent</code>, <code>className</code>
and <code>innerHTML</code> fills it; note that
<code>innerHTML</code> <i>parses</i> its string as HTML, so the
<code>&lt;strong&gt;</code> becomes a real element while
<code>textContent</code> would have shown the tags as plain text. On
an existing element, <code>setAttribute("data-id", "42")</code>
writes an attribute, <code>classList.add/remove/toggle</code>
manipulate classes one at a time, and <code>style.color</code> sets
an inline style. The insertion lines each pick a position:
<code>appendChild</code> last child, <code>prepend</code> first
child, <code>before</code>/<code>after</code> as siblings, and
<code>remove()</code> deletes the element itself.</p>

<p>Security rule you should never bend: for anything a user typed,
use <code>textContent</code>. <code>innerHTML</code> executes markup
inside the string, which is the number-one <b>XSS</b> hole — a
user's <code>&lt;img onerror=...&gt;</code> becomes code running on
your page.</p>

<p>Gotcha: appending nodes one at a time inside a big loop forces a
layout pass each iteration. For hundreds of nodes, build them into a
<code>DocumentFragment</code> and append once.</p>
""",
                "tryit": """<!DOCTYPE html>
<html>
<head><style>
  .todo-item { padding: 6px 12px; margin: 4px 0; background: #f2f8fe;
    border-radius: 6px; display: flex; justify-content: space-between; }
  .done { text-decoration: line-through; color: #999; }
</style></head>
<body>
  <h3>Dynamic Todo List</h3>
  <div id="list"></div>
  <script>
    const list = document.getElementById("list");
    const items = ["Learn DOM", "Build projects", "Master JS"];

    items.forEach((text, i) => {
      const div = document.createElement("div");
      div.className = "todo-item";
      div.innerHTML = `<span>${text}</span><span>item ${i + 1}</span>`;
      div.addEventListener("click", () => div.classList.toggle("done"));
      list.appendChild(div);
    });
    console.log("Created", items.length, "items");
  </script>
</body>
</html>
""",
            },
            {
                "title": "Events & Event Listeners",
                "html": """
<p>Interactivity is a conversation: the user does something — clicks,
types, scrolls — and the browser fires an <b>event</b> announcing it.
<code>addEventListener(eventType, handler)</code> is how you join the
conversation: "when a <code>click</code> happens on this element,
call this function". The handler receives an <b>event object</b>
describing what happened, and you can register many handlers on one
element without overwriting each other — the big advantage over the
old <code>onclick</code> attribute.</p>

<pre class="code">button.addEventListener("click", (event) =&gt; {
  console.log("clicked!", event.target);
});

// common events
"click"          mouse/touch press
"input"          value changed per keystroke
"change"         value committed
"submit"         form submitted
"keydown" / "keyup"  keyboard
"mouseover" / "mouseout"
"scroll" / "load" / "resize"</pre>

<p>The first lines wire a click: every time the button is pressed,
the arrow runs and logs the clicked element via
<code>event.target</code>. The rest of the block is a vocabulary
list worth memorizing. <code>click</code> covers presses;
<code>input</code> fires on EVERY keystroke in a field while
<code>change</code> waits until the value is committed (blur or
Enter); <code>submit</code> belongs to forms;
<code>keydown</code>/<code>keyup</code> watch the keyboard;
<code>mouseover</code>/<code>mouseout</code> track hover; and
<code>scroll</code>, <code>load</code>, <code>resize</code> report
window and page life.</p>

<p>The event object is your information packet:
<code>event.target</code> is the element that fired,
<code>event.key</code> names the pressed key
(<code>"Enter"</code>, <code>"ArrowUp"</code>), and
<code>event.preventDefault()</code> cancels the browser's default
reaction — without it, submitting a form reloads the page and
clicking a link navigates away.</p>

<p>Gotchas: do not pick <code>change</code> when you want live search
feedback — that is <code>input</code>. And listeners keep elements
alive; remove them with <code>removeEventListener</code> (it needs
the same function reference) when the element should be
forgotten.</p>
""",
                "tryit": """<!DOCTYPE html>
<html>
<head><style>
  .counter { font-size: 2rem; font-weight: bold; margin: 10px; }
  button { padding: 8px 16px; margin: 4px; cursor: pointer; }
</style></head>
<body>
  <div class="counter" id="display">0</div>
  <button id="inc">+1</button>
  <button id="dec">-1</button>
  <button id="reset">Reset</button>

  <script>
    let count = 0;
    const display = document.getElementById("display");

    document.getElementById("inc").addEventListener("click", () => {
      count++;
      display.textContent = count;
    });
    document.getElementById("dec").addEventListener("click", () => {
      count--;
      display.textContent = count;
    });
    document.getElementById("reset").addEventListener("click", () => {
      count = 0;
      display.textContent = count;
    });

    // keyboard events
    document.addEventListener("keydown", (e) => {
      if (e.key === "ArrowUp") { count++; display.textContent = count; }
      if (e.key === "ArrowDown") { count--; display.textContent = count; }
    });
  </script>
</body>
</html>
""",
            },
            {
                "title": "Event Bubbling & Delegation",
                "html": """
<p>Click a button inside a card inside a list: who hears about it?
By default, everyone. The event fires at the exact target and then
<b>bubbles up</b> through every ancestor — button, card, list, body —
giving each a chance to react. Instead of fighting this, good
JavaScript exploits it: <b>event delegation</b> puts ONE listener on
a parent and inspects <code>e.target</code> to see which child was
actually hit.</p>

<pre class="code">// instead of adding a listener to EVERY item:
list.addEventListener("click", (e) =&gt; {
  if (e.target.matches(".delete-btn")) {
    e.target.closest(".item").remove();   // delegate!
  }
});</pre>

<p>Read the handler as three steps. The click lands on a delete
button and bubbles up to <code>list</code>. Step one:
<code>e.target.matches(".delete-btn")</code> filters — react only if
the original target was a delete button, so a plain click on the item
text does nothing. Step two:
<code>e.target.closest(".item")</code> climbs from the button to the
surrounding item row — you need the row, not the button. Step three:
<code>.remove()</code> deletes it. One listener now handles ten items
or ten thousand.</p>

<p>The payoff is future-proofing: items added next week — via fetch,
or a "+" button — are handled automatically, because the listener
lives on the parent that outlives them. This is exactly how dynamic
lists work.</p>

<p>Two controls complete the picture:
<code>event.stopPropagation()</code> halts bubbling when an inner
handler must not trigger outer ones, and
<code>event.preventDefault()</code> — a different job entirely —
cancels default browser behaviour.</p>

<p>Gotcha: <code>e.target</code> is the DEEPEST node clicked, even a
<code>&lt;span&gt;</code> inside your button. Always filter with
<code>matches()</code> or climb with <code>closest()</code> — never
assume the target is the element the listener is attached to (that
one is <code>e.currentTarget</code>).</p>
""",
                "tryit": """<!DOCTYPE html>
<html>
<head><style>
  .tag { display: inline-block; padding: 6px 14px; margin: 4px;
         background: #eaf4fd; border: 2px solid #33a9dc;
         border-radius: 999px; cursor: pointer; }
  .tag.selected { background: #1572b6; color: white; }
</style></head>
<body>
  <h3>Click tags — one delegated listener handles all!</h3>
  <div id="container">
    <span class="tag">js</span>
    <span class="tag">css</span>
    <span class="tag">html</span>
  </div>
  <button id="add">Add new tag</button>

  <script>
    // ONE listener for all current AND future tags
    document.getElementById("container").addEventListener("click", (e) => {
      if (e.target.classList.contains("tag")) {
        e.target.classList.toggle("selected");
      }
    });

    // add new tags — they work automatically!
    let counter = 0;
    document.getElementById("add").addEventListener("click", () => {
      const tag = document.createElement("span");
      tag.className = "tag";
      tag.textContent = `new-${++counter}`;
      document.getElementById("container").appendChild(tag);
    });
  </script>
</body>
</html>
""",
            },
            {
                "title": "Fetch API & HTTP Requests",
                "html": """
<p>Sooner or later your page needs data that lives on a server.
<code>fetch()</code> is the modern browser tool for HTTP: give it a
URL, get a <b>Promise</b> resolving to a <b>Response</b> object,
then extract the body as JSON, text or a blob. It replaced
XMLHttpRequest with something readable — and combined with
<code>async/await</code> it reads like plain function calls.</p>

<pre class="code">// GET request
const response = await fetch("https://api.example.com/users");
if (!response.ok) throw new Error(`HTTP ${response.status}`);
const data = await response.json();

// POST request with body
const res = await fetch("/api/users", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ name: "Ada", email: "ada@x.io" }),
});
const created = await res.json();</pre>

<p>Walk the GET: <code>await fetch(url)</code> resolves as soon as
the <b>headers</b> arrive — not the body. That is why the next line
checks <code>response.ok</code> (true for status 200-299) and throws
with the status code otherwise. Only then does
<code>await response.json()</code> download and parse the body —
and note it is asynchronous too, so it needs its own
<code>await</code>. The POST version adds an options object: a
<code>method</code>, a <code>Content-Type</code> header announcing
that the body is JSON, and the body itself serialized with
<code>JSON.stringify</code>.</p>

<p>Here is the trap that bites everyone once: fetch does not reject
on HTTP errors. A 404 or 500 still resolves normally — only a
network failure (offline, DNS) rejects. Skipping the
<code>ok</code> check means your app "succeeds" while holding an
error page.</p>

<p>Body-reading methods: <code>.json()</code> for JSON,
<code>.text()</code> for anything textual, <code>.blob()</code> for
files and images. A body can be read only once — calling
<code>.json()</code> twice throws; clone the response first if you
need two looks.</p>
""",
                "tryit": """<!DOCTYPE html>
<html>
<head><style>
  .result { padding: 10px; background: #f2f8fe; border-radius: 8px;
            margin: 8px 0; font-family: monospace; white-space: pre-wrap; }
  button { padding: 8px 16px; cursor: pointer; margin: 4px; }
</style></head>
<body>
  <h3>Fetch API demo (public API)</h3>
  <button onclick="loadData()">Fetch a random user</button>
  <div class="result" id="output">Click the button!</div>

  <script>
    async function loadData() {
      const output = document.getElementById("output");
      output.textContent = "Loading...";
      try {
        const res = await fetch("https://randomuser.me/api/");
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const data = await res.json();
        const user = data.results[0];
        output.textContent = JSON.stringify({
          name: `${user.name.first} ${user.name.last}`,
          email: user.email,
          country: user.location.country,
        }, null, 2);
      } catch (e) {
        output.textContent = `Error: ${e.message}`;
      }
    }
  </script>
</body>
</html>
""",
            },
            {
                "title": "Web Storage & Cookies",
                "html": """
<p>Browsers remember things between visits — that is how "dark mode"
survives a refresh. <b>Web Storage</b> gives every origin two
key-value stores with a tiny string-only API:
<code>setItem(key, value)</code>, <code>getItem(key)</code>,
<code>removeItem(key)</code>, <code>clear()</code>. Values must be
strings, so objects travel as JSON. It is simpler, roomier (about
5MB) and lighter on the network than cookies, which ride along with
every request.</p>

<pre class="code">localStorage.setItem("name", "Ada");
localStorage.getItem("name")          // "Ada"
localStorage.removeItem("name");
localStorage.clear();

// objects: serialize with JSON
localStorage.setItem("user", JSON.stringify({ name: "Ada" }));
const user = JSON.parse(localStorage.getItem("user"));</pre>

<p>The first four lines are the entire primitive API — set, get,
remove, wipe. Note that <code>getItem</code> returns
<code>null</code> for a missing key (not an error), which is how you
detect first visits. The last two lines show the standard object
pattern: stringify on the way in, parse on the way out. Skip the
<code>JSON.parse</code> and you get the string
<code>'{"name":"Ada"}'</code> instead of an object — a classic
head-scratcher.</p>

<ul>
<li><b>localStorage</b> — persists until deleted</li>
<li><b>sessionStorage</b> — dies with the tab</li>
<li><b>Cookies</b> — sent to the server on every request (4KB limit,
dated mechanism; use for auth tokens, not data)</li>
</ul>

<p>Choose the store by lifetime: localStorage for preferences and
saved progress, sessionStorage for one-session state like form
drafts, cookies only when the server must receive the value on every
request (auth tokens). Seeing is believing: this app keeps your
name, progress, language and playground code in localStorage — open
devtools → Application → Local Storage and find yourself.</p>

<p>Gotchas: storage is per-origin and synchronous — any script on
the page can read it, so never store passwords there. And do not
stuff in megabytes of data: <code>setItem</code> starts throwing
QuotaExceededError around the 5MB limit.</p>
""",
            },
            {
                "title": "Browser APIs",
                "html": """
<p>JavaScript the language knows nothing about timers, cameras or
notifications — those come from <b>Web APIs</b> that the browser adds
on top. The split matters: MDN documents them separately, and they
are the reason two browsers can run the same JS yet offer different
features. These are the ones you will actually use in your first
year of building things:</p>

<ul>
<li><b>setTimeout / setInterval / requestAnimationFrame</b> — run
code later, repeatedly, or once per animation frame (the right pick
for animation)</li>
<li><b>Geolocation</b> — the user's location, always behind a
permission prompt</li>
<li><b>Clipboard</b> — programmatic copy/paste</li>
<li><b>Intersection Observer</b> — efficient "is this element visible
in the viewport?" checks; lazy-loaded images and scroll animations
run on it</li>
<li><b>Notifications</b> — system-level popups, also
permission-gated</li>
<li><b>Web Workers</b> — background threads for heavy computation,
keeping the UI responsive</li>
<li><b>History</b> — <code>pushState</code> and back/forward control,
the backbone of single-page-app routing</li>
<li><b>Console</b> — far beyond <code>log</code>: try
<code>table</code>, <code>time</code>, <code>group</code></li>
</ul>

<p>A pattern to notice: anything touching the user's device or
privacy — location, clipboard, notifications, camera — asks
permission first, and a denied permission means your code must
degrade gracefully rather than crash. Each API has its own MDN page
with browser support tables; when a feature fails in one browser,
that page is your first stop.</p>
""",
            },
        ],
        "quiz": [
            {
                "type": "mc",
                "question": "What does querySelector return?",
                "options": ["All matching elements", "The first matching element", "An array", "A string"],
                "answer": 1,
                "explain": "querySelector returns the first match; querySelectorAll returns all.",
            },
            {
                "type": "blank",
                "question": "The safe way to set text content (no HTML parsing) is <code>____</code>.",
                "answers": ["textContent"],
                "explain": "textContent is safe; innerHTML parses HTML and risks XSS.",
            },
            {
                "type": "mc",
                "question": "Event delegation means:",
                "options": [
                    "Sending events to a server",
                    "One listener on a parent handles events for all children",
                    "Removing all listeners",
                    "Using event.target only",
                ],
                "answer": 1,
                "explain": "Events bubble to ancestors — a parent listener covers future children too.",
            },
            {
                "type": "blank",
                "question": "fetch() only rejects on ____ errors, not HTTP 404/500.",
                "answers": ["network"],
                "explain": "Always check response.ok — fetch resolves even for 404/500.",
            },
        ],
    },

    # ------------------------------------------------------------------ js10
    {
        "id": "js10",
        "title": "Advanced Topics",
        "emoji": "🧠",
        "lessons": [
            {
                "title": "Memory Management & Garbage Collection",
                "html": """
<p>In C you allocate and free memory by hand. JavaScript does it for
you: create objects freely, and the <b>garbage collector (GC)</b>
finds the ones nothing can reach anymore and reclaims them.
"Automatic" is not "carefree", though — the GC can only free what is
<b>unreachable</b>. If any live variable, closure or timer still
points at an object, it survives forever. That is what a memory leak
means in JS.</p>

<pre class="code">// memory leak: forgotten timer keeps a reference alive
const leak = setInterval(() =&gt; { ... }, 1000);
// if you never call clearInterval(leak), the closure lives forever!

// memory leak: detached DOM nodes
const el = document.getElementById("old");
document.body.removeChild(el);
// if 'el' is still referenced in JS, the DOM node can't be GC'd

// memory leak: unbounded arrays/caches
const cache = [];
function addToCache(item) {
  cache.push(item);    // grows forever — no eviction!
}</pre>

<p>Study the three classic leaks. First, the forgotten timer:
<code>setInterval</code> returns an id, and the callback closure
references everything it captured — never calling
<code>clearInterval(leak)</code> keeps that whole closure, and
everything it touches, alive for the page's lifetime. Second, the
detached DOM node: removing an element from the document does not
free it while a JS variable still references it — the node is
invisible but uncollectable. Third, the unbounded cache:
<code>cache.push(item)</code> grows without limit; nothing in it ever
becomes unreachable, so the GC is powerless by design.</p>

<p>The algorithm behind it is <b>mark-and-sweep</b>: starting from
roots (the global object, the currently running function's locals),
mark every object reachable through references; then sweep — free —
everything unmarked. Reachability, not usage, is the rule: an object
referenced from a root survives even if no code ever reads it
again.</p>

<p>Gotchas: clean up what you start — clear timers, remove listeners
with <code>removeEventListener</code>, null out references to large
data you are done with. And weak references
(<code>WeakMap</code>, <code>WeakSet</code>) exist precisely so that
caches and metadata do not pin objects alive.</p>
""",
            },
            {
                "title": "Proxy, Reflect & Meta Programming",
                "html": """
<p>Sometimes you want to watch or veto what happens to an object: log
every write, validate before every assignment, react when a value
changes. <b>Proxy</b> wraps a target object and lets you intercept
its operations — <code>get</code>, <code>set</code>, function calls,
even <code>delete</code> — through handler functions called
<b>traps</b>. <b>Reflect</b> is its companion: a namespace holding
the default implementations of those same operations, so a trap can
say "and then do the normal thing".</p>

<pre class="code">const handler = {
  get(target, prop) {
    console.log(`getting ${prop}`);
    return Reflect.get(target, prop);    // default behaviour
  },
  set(target, prop, value) {
    console.log(`setting ${prop} to ${value}`);
    return Reflect.set(target, prop, value);
  },
};

const obj = new Proxy({ name: "Ada" }, handler);
obj.name;     // logs "getting name"
obj.age = 36; // logs "setting age to 36"</pre>

<p>The handler defines two traps. The <code>get</code> trap runs on
EVERY property read: it logs <code>"getting name"</code> first, then
<code>Reflect.get(target, prop)</code> performs the ordinary read and
returns the value. The <code>set</code> trap runs on every
assignment, logging <code>"setting age to 36"</code> before
<code>Reflect.set</code> does the real write. From the outside,
<code>obj</code> behaves exactly like a normal object — the
interception is invisible to its users.</p>

<p>This is not a party trick. Validation (reject bad assignments),
logging and access control all fall out of these two traps, and
<b>reactive systems</b> are built on the <code>set</code> trap:
Vue.js detects state changes exactly this way — the same idea as the
mini-reactive object in this lesson's playground.</p>

<p>Gotchas: proxies are slower than plain objects, so do not wrap
hot-path data. A trap that forgets to return — especially
<code>set</code>, which must return <code>true</code> on success —
throws a TypeError in strict mode. When in doubt, delegate to
Reflect.</p>
""",
                "tryit": """// Proxy: a reactive object (mini-Vue!)
function reactive(obj) {
  return new Proxy(obj, {
    set(target, prop, value) {
      const old = target[prop];
      target[prop] = value;
      if (old !== value) {
        console.log(`⚡ ${prop} changed: ${old} → ${value}`);
      }
      return true;
    },
  });
}

const state = reactive({ count: 0, message: "hello" });
state.count = 5;       // ⚡ count changed: 0 → 5
state.count = 5;       // no log (same value)
state.message = "world"; // ⚡ message changed

// Reflect: default behaviour with clean API
const obj = { a: 1 };
Reflect.set(obj, "b", 2);
console.log(Reflect.get(obj, "b"));       // 2
console.log(Reflect.has(obj, "a"));       // true
console.log(Reflect.ownKeys(obj));        // ["a", "b"]
""",
            },
            {
                "title": "Property Descriptors & Immutability",
                "html": """
<p>A property is more than a value. Each one carries a hidden
<b>descriptor</b> with four flags: <code>value</code> (the data),
<code>writable</code> (can it be reassigned?),
<code>enumerable</code> (does it show up in loops and
<code>Object.keys</code>?), and <code>configurable</code> (can its
flags be changed, or the property deleted?). You rarely look at
these flags — until you need a read-only constant or want to hide a
helper from <code>for...in</code>.</p>

<pre class="code">const obj = { x: 1 };
const desc = Object.getOwnPropertyDescriptor(obj, "x");
// { value: 1, writable: true, enumerable: true, configurable: true }

// make a property read-only
Object.defineProperty(obj, "x", { writable: false });
obj.x = 99;              // silently fails (strict mode: throws)
console.log(obj.x);      // still 1

// immutability levels
const frozen = Object.freeze({ a: 1 });   // can't add, modify, or delete
const sealed = Object.seal({ a: 1 });     // can modify, can't add/delete
const extensible = Object.preventExtensions({ a: 1 }); // can't add</pre>

<p>The first lines read the descriptor of <code>x</code> — a plain
object literal produces all four flags <code>true</code> with value
1. Then <code>defineProperty</code> flips <code>writable</code> to
false: the assignment <code>obj.x = 99</code> now <b>silently
fails</b> in sloppy mode (or throws in strict mode), and
<code>obj.x</code> still prints 1. The last three lines are the
immutability levels, strictest first: <code>freeze</code> forbids
adding, changing AND deleting; <code>seal</code> forbids add and
delete but allows changing existing values;
<code>preventExtensions</code> only forbids adding. Predict which
one locks the most before re-reading — freeze, always.</p>

<p><b>Enumerability</b> explains a mystery you may have noticed:
built-ins like <code>toString</code> exist on every object yet never
appear in <code>Object.keys()</code>, <code>for...in</code> or JSON —
they are non-enumerable by design, so your loops stay clean.</p>

<p>Gotchas: <code>Object.freeze</code> is <b>shallow</b> — nested
objects stay mutable unless you freeze them too (a
<code>deepFreeze</code> helper recurses; the playground has one).
And <code>defineProperty</code> on a non-configurable property is
one-way: you cannot undo it.</p>
""",
                "tryit": """// property descriptors
const obj = { visible: true, hidden: false };
Object.defineProperty(obj, "secret", {
  value: "classified",
  enumerable: false,      // invisible in loops!
  writable: false,
});
console.log(obj.secret);             // "classified"
console.log(Object.keys(obj));       // ["visible", "hidden"] — no secret!
console.log("secret" in obj);        // true — still exists

// freeze vs seal
const frozen = Object.freeze({ a: 1 });
const sealed = Object.seal({ b: 2 });

try { frozen.a = 99; } catch(e) { /* strict mode throws */ }
console.log(frozen.a);  // 1 (unchanged)

sealed.b = 99;           // ✓ can modify
// sealed.c = 3;        // ✗ can't add
console.log(sealed.b);  // 99

// deep freeze (freeze nested objects too)
function deepFreeze(obj) {
  Object.getOwnPropertyNames(obj).forEach(prop => {
    const val = obj[prop];
    if (val && typeof val === "object") deepFreeze(val);
  });
  return Object.freeze(obj);
}
""",
            },
            {
                "title": "Internationalization, Typed Arrays & More",
                "html": """
<p>Two topics round out the language. <b>Internationalization
(i18n)</b>: users everywhere expect dates, numbers and sorted lists
in THEIR format — the <code>Intl</code> object delivers that without
any library. <b>Typed Arrays</b>: when you touch binary data —
canvas pixels, WebGL, files, audio — ordinary arrays are too slow
and too loose; typed arrays give you fixed-size, raw-number views
over memory.</p>

<pre class="code">new Intl.NumberFormat("en", { style: "currency", currency: "USD" })
  .format(1234.56);   // "$1,234.56"
new Intl.NumberFormat("de-DE").format(1234.56);  // "1.234,56"

new Intl.DateTimeFormat("fa", { dateStyle: "full" }).format(new Date());
// Persian date format!

new Intl.Collator("fa").compare("ا", "ب");   // locale-aware sorting</pre>

<p>Predict the first block before reading: the same number
<code>1234.56</code> formats as <code>"$1,234.56"</code> for US
English but <code>"1.234,56"</code> in German — comma and dot swap
roles. The Persian line asks <code>Intl.DateTimeFormat</code> for a
full date in the <code>"fa"</code> locale, producing a Persian
calendar date in Persian digits. The last line uses
<code>Intl.Collator</code>, whose <code>compare</code> sorts strings
by locale rules — pass it wherever a comparator function goes, and
alphabetical sorting works for non-English alphabets too.</p>

<pre class="code">const buffer = new ArrayBuffer(16);     // 16 bytes
const view = new Int32Array(buffer);     // 4 x 32-bit integers
view[0] = 42;
const f64 = new Float64Array(buffer);    // same bytes, different lens</pre>

<p>Typed arrays think in buffers and views. The second block
allocates 16 raw bytes with <code>ArrayBuffer</code>, then lays an
<code>Int32Array</code> over them: 4 slots of 32-bit integers
(4 slots x 4 bytes = 16). Writing <code>view[0] = 42</code> stores
42 in the first four bytes. Then <code>Float64Array</code>
reinterprets the SAME 16 bytes as two 64-bit floats — what you read
back is garbage, because the bytes now mean something different.
That reinterpretation is the point: one buffer, many lenses.</p>

<p>Gotchas: typed arrays have a fixed length — no
<code>push</code>, and out-of-range writes are silently ignored.
Also, Float32 loses precision fast: <code>3.14159</code> stored in a
<code>Float32Array</code> reads back as
<code>3.141590118408203</code>; use Float64 when precision
matters.</p>
""",
                "tryit": """// Internationalization
console.log(new Intl.NumberFormat("en", { style: "currency", currency: "USD" }).format(1234.56));
console.log(new Intl.NumberFormat("de-DE").format(1234.56));
console.log(new Intl.NumberFormat("fa").format(1234.56));

// date formatting in different locales
const date = new Date();
console.log(date.toLocaleDateString("en", { dateStyle: "full" }));
console.log(date.toLocaleDateString("fa", { dateStyle: "full" }));

// Typed arrays: binary precision
const f32 = new Float32Array(4);
f32[0] = 3.14159;
console.log(f32[0]);  // 3.141590118408203 (32-bit precision)
const f64 = new Float64Array(4);
f64[0] = 3.14159;
console.log(f64[0]);  // 3.14159 (64-bit — full precision)
""",
            },
        ],
        "quiz": [
            {
                "type": "mc",
                "question": "The JS garbage collector uses which algorithm?",
                "options": ["Reference counting only", "Mark-and-sweep", "Manual free()", "Copy collection"],
                "answer": 1,
                "explain": "Mark reachable objects from roots, sweep unreachable ones.",
            },
            {
                "type": "mc",
                "question": "Proxy can intercept:",
                "options": [
                    "Only property reads",
                    "Property reads, writes, function calls, and more",
                    "Only network requests",
                    "Only DOM events",
                ],
                "answer": 1,
                "explain": "Proxy handlers can intercept get, set, apply, has, delete, and more.",
            },
            {
                "type": "blank",
                "question": "Object.____ makes an object completely immutable (no add, modify, or delete).",
                "answers": ["freeze"],
                "explain": "Object.freeze is the strictest; Object.seal allows modification but not add/delete.",
            },
        ],
    },
]
