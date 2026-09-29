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
mirroring your HTML. JavaScript reads and manipulates it to make pages
interactive:</p>

<pre class="code">// select ONE element
const el = document.querySelector(".card");       // first match
const byId = document.getElementById("header");   // by id

// select ALL matching elements (returns NodeList)
const items = document.querySelectorAll(".item");
items.forEach(item =&gt; console.log(item.textContent));</pre>

<ul>
<li><code>querySelector</code> — uses CSS selectors, returns the first
match (or null)</li>
<li><code>querySelectorAll</code> — returns a static NodeList (use
<code>forEach</code> or spread to an array)</li>
<li><code>getElementById</code> — fastest, but only for IDs</li>
</ul>
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
<p>JavaScript can create, modify, and remove DOM elements dynamically:</p>

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

<p>Always prefer <code>textContent</code> over <code>innerHTML</code>
for user-supplied data — innerHTML parses HTML and is the #1 XSS
vulnerability.</p>
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
<p><b>Events</b> are the user's actions: clicks, keypresses, scrolls.
<code>addEventListener</code> is how you respond:</p>

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

<p>The event object has <code>event.target</code> (what was clicked),
<code>event.key</code> (which key), and <code>event.preventDefault()</code>
to stop default behaviour (form submission, link navigation).</p>
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
<p>When you click a nested element, the event <b>bubbles up</b> from
the target through its ancestors. This enables <b>event delegation</b>
— one listener on a parent handles events for all its children (present
and future):</p>

<pre class="code">// instead of adding a listener to EVERY item:
list.addEventListener("click", (e) =&gt; {
  if (e.target.matches(".delete-btn")) {
    e.target.closest(".item").remove();   // delegate!
  }
});</pre>

<p>Delegation is how dynamic lists work — items added later are
automatically handled. <code>event.stopPropagation()</code> stops
bubbling when needed.</p>
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
<p><code>fetch()</code> makes HTTP requests — the modern replacement
for XMLHttpRequest:</p>

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

<p>fetch returns a Promise that resolves to a Response object. You must
check <code>response.ok</code> — fetch only rejects on network errors,
not HTTP errors (404, 500 still resolve!). Methods: <code>.json()</code>,
<code>.text()</code>, <code>.blob()</code>.</p>
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
<p><b>Web Storage</b> (localStorage + sessionStorage) stores key-value
pairs in the browser — simpler than cookies:</p>

<pre class="code">localStorage.setItem("name", "Ada");
localStorage.getItem("name")          // "Ada"
localStorage.removeItem("name");
localStorage.clear();

// objects: serialize with JSON
localStorage.setItem("user", JSON.stringify({ name: "Ada" }));
const user = JSON.parse(localStorage.getItem("user"));</pre>

<ul>
<li><b>localStorage</b> — persists until deleted</li>
<li><b>sessionStorage</b> — dies with the tab</li>
<li><b>Cookies</b> — sent to the server on every request (4KB limit,
dated mechanism; use for auth tokens, not data)</li>
</ul>

<p>This app uses localStorage for your name, progress, language, and
playground code — check devtools → Application → Local Storage!</p>
""",
            },
            {
                "title": "Browser APIs",
                "html": """
<p>The browser provides many APIs beyond the DOM. The ones you'll
encounter most:</p>

<ul>
<li><b>setTimeout / setInterval / requestAnimationFrame</b> — timing
and animation</li>
<li><b>Geolocation</b> — user's location (with permission)</li>
<li><b>Clipboard</b> — copy/paste</li>
<li><b>Intersection Observer</b> — detect when elements enter the
viewport (lazy loading, animations)</li>
<li><b>Notifications</b> — system notifications</li>
<li><b>Web Workers</b> — background threads (covered in HTML course)</li>
<li><b>History</b> — pushState/back (SPA routing)</li>
<li><b>Console</b> — log, warn, error, table, time...</li>
</ul>

<p>These are documented under <b>Web APIs</b> on MDN — separate from
the JavaScript language itself. Each has its own MDN page with
browser support info.</p>
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
<p>JS has automatic memory management — the <b>garbage collector (GC)</b>
finds objects that are no longer reachable and frees their memory. You
don't call <code>free()</code> like in C, but you can still leak
memory:</p>

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

<p>The GC uses the <b>mark-and-sweep</b> algorithm: starting from
roots (global object, current function's locals), it marks all
reachable objects, then sweeps unreachable ones. If an object is
reachable from a root, it can't be collected — even if nothing
"uses" it.</p>
""",
            },
            {
                "title": "Proxy, Reflect & Meta Programming",
                "html": """
<p><b>Proxy</b> wraps an object and intercepts operations on it —
property access, assignment, function calls. <b>Reflect</b> provides
the default behaviour for these operations:</p>

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

<p>Proxy use cases: validation, logging, access control, reactive
systems (Vue.js uses it!). <code>Reflect</code> provides the default
implementations so you can call them inside your interceptors.</p>
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
<p>Every object property has a <b>descriptor</b> with attributes:
<code>value</code>, <code>writable</code>, <code>enumerable</code>,
<code>configurable</code>. You can inspect and change them:</p>

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

<p><b>Enumerability</b> determines if a property shows up in
<code>for...in</code>, <code>Object.keys()</code>, and JSON. Built-in
methods (like <code>toString</code>) are non-enumerable — that's why
they don't clutter your loops.</p>
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
<p><b>Internationalization (i18n)</b> — the <code>Intl</code> object
formats dates, numbers, and strings for different locales:</p>

<pre class="code">new Intl.NumberFormat("en", { style: "currency", currency: "USD" })
  .format(1234.56);   // "$1,234.56"
new Intl.NumberFormat("de-DE").format(1234.56);  // "1.234,56"

new Intl.DateTimeFormat("fa", { dateStyle: "full" }).format(new Date());
// Persian date format!

new Intl.Collator("fa").compare("ا", "ب");   // locale-aware sorting</pre>

<p><b>Typed Arrays</b> — binary data with fixed-size numeric types for
performance-critical code (canvas, WebGL, file handling):</p>

<pre class="code">const buffer = new ArrayBuffer(16);     // 16 bytes
const view = new Int32Array(buffer);     // 4 x 32-bit integers
view[0] = 42;
const f64 = new Float64Array(buffer);    // same bytes, different lens</pre>

<p>These topics round out your JS education. MDN's guides cover them in
depth — you now have the foundation to understand them all.</p>
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
