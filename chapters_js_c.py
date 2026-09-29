"""JS Tutor chapters 6-8 (Phases 6-8), grounded in MDN Web Docs."""

CHAPTERS_JS_C = [
    # ------------------------------------------------------------------ js06
    {
        "id": "js06",
        "title": "Built-in Objects",
        "emoji": "🧰",
        "lessons": [
            {
                "title": "Object & Array Globals",
                "html": """
<p>The <code>Object</code> and <code>Array</code> global objects provide
static utility methods:</p>

<pre class="code">// Object static methods
Object.keys({a: 1, b: 2})          // ["a", "b"]
Object.values({a: 1, b: 2})        // [1, 2]
Object.entries({a: 1, b: 2})       // [["a",1],["b",2]]
Object.assign({}, {a: 1}, {b: 2}) // merge
Object.freeze({a: 1})              // make immutable

// Array static methods
Array.isArray([])                   // true
Array.from("abc")                   // ["a", "b", "c"]
Array.from({length: 3}, (_, i) =&gt; i * 10)  // [0, 10, 20]
Array.of(1, 2, 3)                   // [1, 2, 3]</pre>

<p>Array instance methods you should know:
<code>at(-1)</code> (last element), <code>flat()</code>,
<code>flatMap()</code>, <code>includes()</code>,
<code>indexOf()</code>, <code>fill()</code>, <code>reverse()</code>,
<code>splice()</code> (mutates!).</p>
""",
                "tryit": """// Object utilities
const user = { name: "Ada", age: 36, role: "admin" };
console.log(Object.keys(user));
console.log(Object.entries(user).map(([k, v]) => `${k}=${v}`));

// frozen object — mutations are silently ignored
const frozen = Object.freeze({ x: 1 });
frozen.x = 99;
console.log(frozen.x);  // still 1

// Array.from with a mapping function
const grid = Array.from({ length: 3 }, (_, i) => `row-${i + 1}`);
console.log(grid);

// at() — negative indexing
const arr = [10, 20, 30, 40];
console.log(arr.at(-1));  // 40
console.log(arr.at(-2));  // 30
""",
            },
            {
                "title": "String & Number Globals",
                "html": """
<p><code>String</code> and <code>Number</code> global objects provide
conversion and utility methods:</p>

<pre class="code">// String static
String(42)              // "42"
String.fromCharCode(72, 105)  // "Hi"

// String instance
"  hello  ".trimStart()  // "hello  "
"hello".padStart(8, "*") // "***hello"
"hello".repeat(3)         // "hellohellohello"
"hello".replaceAll("l", "L") // "heLLo"
"hello".at(-1)           // "o"

// Number static
Number.isInteger(42)     // true
Number.isNaN(NaN)        // true (safer than global isNaN)
Number.MAX_SAFE_INTEGER  // 9007199254740991
Number.EPSILON           // 2.220446049250313e-16
(42).toString(2)         // "101010" (binary)
(255).toString(16)       // "ff" (hexadecimal)</pre>
""",
                "tryit": """// String tricks
console.log("5".padStart(3, "0"));     // "005"
console.log("Hello".repeat(3));        // "HelloHelloHello"
console.log("a-b-c".replaceAll("-", "_"));
console.log([..."hello"].reverse().join("")); // "olleh"

// Number formatting
const price = 1234.567;
console.log(price.toFixed(2));          // "1234.57"
console.log(price.toLocaleString("en", { style: "currency", currency: "USD" }));
console.log((255).toString(16));        // "ff"
console.log(Number.parseInt("0x1A", 16)); // 26

// Number.isNaN vs global isNaN
console.log(Number.isNaN(NaN));        // true (reliable)
console.log(Number.isNaN("abc"));      // false (not a NaN number)
""",
            },
            {
                "title": "Math",
                "html": """
<p>The <code>Math</code> object provides mathematical constants and
functions — always available, never instantiated:</p>

<pre class="code">Math.PI                 // 3.14159...
Math.E                  // 2.718...
Math.abs(-5)            // 5
Math.round(4.7)         // 5 (nearest)
Math.floor(4.7)         // 4 (down)
Math.ceil(4.2)          // 5 (up)
Math.trunc(4.7)         // 4 (truncate decimal)
Math.max(1, 5, 3)       // 5
Math.min(1, 5, 3)       // 1
Math.pow(2, 10)         // 1024
Math.sqrt(16)           // 4
Math.random()           // [0, 1)
Math.sign(-3)           // -1</pre>

<p>Common patterns:</p>

<pre class="code">// random integer between min and max (inclusive)
const random = (min, max) =&gt; Math.floor(Math.random() * (max - min + 1)) + min;

// random element from array
const pick = arr =&gt; arr[Math.floor(Math.random() * arr.length)];</pre>
""",
                "tryit": """const random = (min, max) => Math.floor(Math.random() * (max - min + 1)) + min;

// dice roll
const die = random(1, 6);
console.log("🎲 You rolled:", die);

// random element
const fruits = ["apple", "banana", "cherry", "date"];
console.log("random fruit:", fruits[Math.floor(Math.random() * fruits.length)]);

// rounding comparison
const n = 4.7;
console.log("round:", Math.round(n), "floor:", Math.floor(n), "ceil:", Math.ceil(n));

// clamp with Math
const clamp = (val, min, max) => Math.min(Math.max(val, min), max);
console.log("clamped:", clamp(15, 0, 10));  // 10

// Math.hypot — hypotenuse
console.log("hypotenuse:", Math.hypot(3, 4)); // 5
""",
            },
            {
                "title": "Date",
                "html": """
<p>The <code>Date</code> object handles dates and times. Months are
0-indexed (0 = January) — a classic trap!</p>

<pre class="code">const now = new Date();
const specific = new Date(2026, 8, 27);     // Sep 27 2026 (month=8!)
const parsed = new Date("2026-09-27T14:30:00");

now.getFullYear()     // 2026
now.getMonth()        // 0-11 (add 1!)
now.getDate()         // day of month
now.getDay()          // day of week (0 = Sunday)
now.getHours()
now.getTime()         // milliseconds since epoch
Date.now()            // shortcut for timestamp</pre>

<p>Formatting with <code>toLocaleString</code> and
<code>Intl.DateTimeFormat</code>:</p>

<pre class="code">now.toLocaleDateString("en", { weekday: "long", year: "numeric",
  month: "long", day: "numeric" });
// "Saturday, September 27, 2026"</pre>
""",
                "tryit": """const now = new Date();

// Date components
console.log("Year:", now.getFullYear());
console.log("Month:", now.getMonth() + 1); // add 1!
console.log("Day:", now.getDate());
console.log("Day of week:", now.getDay()); // 0=Sunday

// formatting
console.log(now.toLocaleDateString("en", {
  weekday: "long", month: "long", day: "numeric", year: "numeric"
}));

// date arithmetic
const tomorrow = new Date(now);
tomorrow.setDate(now.getDate() + 1);
console.log("Tomorrow:", tomorrow.toLocaleDateString());

// timestamp (ms since epoch)
console.log("Timestamp:", Date.now());
""",
            },
            {
                "title": "RegExp",
                "html": """
<p>Regular expressions match patterns in strings — created with a
literal <code>/pattern/flags</code> or <code>new RegExp("pattern")</code>:</p>

<pre class="code">// test: does the string match?
/\\d+/.test("abc123")        // true (has digits)

// match: extract matches
"hello 42 world 99".match(/\\d+/g)  // ["42", "99"]

// replace
"hello world".replace(/o/g, "0")   // "hell0 w0rld"

// common patterns
/^\\S+@\\S+\\.\\S+$/       // email (simplified)
/^\\d{3}-\\d{4}$/           // phone: 555-1234
/^[A-Za-z0-9]+$/           // alphanumeric only

// flags: g=global, i=case-insensitive, m=multiline
/HELLO/i.test("hello")     // true</pre>
""",
                "tryit": """// basic matching
const text = "Contact: ada@example.com or grace@mdn.org";
const emails = text.match(/\\S+@\\S+\\.\\S+/g);
console.log("emails found:", emails);

// named capture groups
const dateStr = "2026-09-27";
const { year, month, day } = dateStr.match(
  /(?<year>\\d{4})-(?<month>\\d{2})-(?<day>\\d{2})/
).groups;
console.log(`Day: ${day}, Month: ${month}, Year: ${year}`);

// validation patterns
const patterns = {
  email: /^\\S+@\\S+\\.\\S+$/,
  phone: /^\\d{3}-\\d{4}$/,
  hex: /^#[0-9a-fA-F]{6}$/,
};
console.log("is email:", patterns.email.test("ada@x.io"));
console.log("is phone:", patterns.phone.test("555-1234"));
console.log("is hex:", patterns.hex.test("#1572b6"));

// replace with capture groups
const name = "Ada Lovelace";
const reversed = name.replace(/(\\w+) (\\w+)/, "$2, $1");
console.log(reversed);  // "Lovelace, Ada"
""",
            },
            {
                "title": "Map, Set, WeakMap & WeakSet",
                "html": """
<p><b>Map</b> is a key-value store where keys can be ANY type (not just
strings like in objects):</p>

<pre class="code">const map = new Map();
map.set("name", "Ada");
map.set(42, "number key");
map.set(true, "boolean key");
map.get("name")       // "Ada"
map.has(42)           // true
map.size              // 3
map.delete("name")
map.clear()</pre>

<p><b>Set</b> is a collection of unique values:</p>

<pre class="code">const set = new Set([1, 2, 3, 3, 2, 1]);
set.size              // 3 (duplicates removed!)
set.add(4);
set.has(2)            // true

// remove duplicates from array
const unique = [...new Set([1, 2, 2, 3, 3, 3])];  // [1, 2, 3]</pre>

<p><b>WeakMap/WeakSet</b> — keys must be objects and are held
<i>weakly</i>: if the key object is garbage-collected, the entry
disappears automatically. Used for caching and metadata without memory
leaks.</p>
""",
                "tryit": """// Map: any type of key
const userRoles = new Map();
userRoles.set("ada", "admin");
userRoles.set(42, "bot");
userRoles.set(true, "system");
console.log(userRoles.get("ada"));   // "admin"
console.log(userRoles.get(42));      // "bot"

// iterate a Map
for (const [key, role] of userRoles) {
  console.log(`${key} → ${role}`);
}

// Set: deduplicate
const tags = ["js", "css", "html", "js", "css"];
const unique = new Set(tags);
console.log("unique tags:", [...unique]);

// Set operations
const setA = new Set([1, 2, 3]);
const setB = new Set([2, 3, 4]);
const intersection = [...setA].filter(x => setB.has(x));
console.log("intersection:", intersection);

// WeakMap for private data
const privateData = new WeakMap();
class User {
  constructor(name) { privateData.set(this, { name }); }
  getName() { return privateData.get(this).name; }
}
""",
            },
            {
                "title": "JSON",
                "html": """
<p><b>JSON (JavaScript Object Notation)</b> is the universal data
format for APIs. Two methods do everything:</p>

<pre class="code">// serialize: object → string
const user = { name: "Ada", tags: ["admin", "dev"], active: true };
const json = JSON.stringify(user);
// '{"name":"Ada","tags":["admin","dev"],"active":true}'

// deserialize: string → object
const parsed = JSON.parse(json);
console.log(parsed.name);     // "Ada"

// pretty-print with indentation
console.log(JSON.stringify(user, null, 2));

// filter keys during serialization
JSON.stringify(user, ["name", "active"]);
// '{"name":"Ada","active":true}'</pre>

<p>JSON limitations: no functions, no undefined, no comments, no
circular references (throws). Dates become strings.</p>
""",
                "tryit": """const app = {
  name: "MyApp",
  version: "1.0",
  config: { theme: "dark", lang: "en" },
  tags: ["web", "dev"],
  sayHi: () => "hi",      // functions are DROPPED
};

// serialize
const json = JSON.stringify(app, null, 2);
console.log(json);
// note: sayHi is gone!

// deserialize
const copy = JSON.parse(json);
console.log(copy.config.theme);

// deep clone using JSON (simple but limited)
const original = { a: 1, nested: { b: 2 } };
const clone = JSON.parse(JSON.stringify(original));
clone.nested.b = 99;
console.log(original.nested.b);  // 2 — truly separate!

// modern deep clone
const deepCopy = structuredClone(original);
deepCopy.nested.b = 777;
console.log(original.nested.b);  // 2 — still separate!
""",
            },
            {
                "title": "Error & Promise (preview)",
                "html": """
<p><b>Error</b> objects carry error information. The built-in types:
<code>Error</code>, <code>TypeError</code>,
<code>ReferenceError</code>, <code>RangeError</code>,
<code>SyntaxError</code>. Create custom errors by extending:</p>

<pre class="code">class ValidationError extends Error {
  constructor(field, message) {
    super(message);
    this.name = "ValidationError";
    this.field = field;
  }
}

try {
  throw new ValidationError("email", "Invalid email format");
} catch (e) {
  if (e instanceof ValidationError) {
    console.log(`Field "${e.field}": ${e.message}`);
  }
}</pre>

<p><b>Promise</b> represents a value that will be available later —
the foundation of async JavaScript (Phase 7 covers it deeply). You'll
see promises returned from <code>fetch()</code>,
<code>setTimeout()</code> wrappers, and every modern async
API.</p>
""",
                "tryit": """// custom error classes
class NetworkError extends Error {
  constructor(status, message) {
    super(message);
    this.name = "NetworkError";
    this.status = status;
  }
}

class NotFoundError extends NetworkError {
  constructor(resource) {
    super(404, `${resource} not found`);
  }
}

// error hierarchy in action
function fetchUser(id) {
  if (id <= 0) throw new ValidationError("id", "ID must be positive");
  if (id > 100) throw new NotFoundError(`User ${id}`);
  return { id, name: `User${id}` };
}

for (const id of [5, -1, 200]) {
  try {
    console.log(fetchUser(id));
  } catch (e) {
    console.log(`${e.name}: ${e.message}`);
  }
}

// Promise preview — full coverage in Phase 7!
const promise = new Promise((resolve) => {
  setTimeout(() => resolve("done!"), 100);
});
promise.then(result => console.log("Promise resolved:", result));
""",
            },
        ],
        "quiz": [
            {
                "type": "mc",
                "question": "Which method removes duplicates from an array?",
                "options": ["arr.unique()", "[...new Set(arr)]", "arr.distinct()", "arr.filter()"],
                "answer": 1,
                "explain": "Set only stores unique values; spreading back gives a deduplicated array.",
            },
            {
                "type": "blank",
                "question": "The method to convert an object to a JSON string is <code>JSON.____</code>.",
                "answers": ["stringify"],
                "explain": "JSON.stringify serializes; JSON.parse deserializes.",
            },
            {
                "type": "mc",
                "question": "What is the main advantage of WeakMap over Map?",
                "options": [
                    "It's faster",
                    "Keys can be any type",
                    "Entries are garbage-collected when the key object is destroyed",
                    "It has more methods",
                ],
                "answer": 2,
                "explain": "Weak references prevent memory leaks when key objects are no longer needed.",
            },
        ],
    },

    # ------------------------------------------------------------------ js07
    {
        "id": "js07",
        "title": "Asynchronous JavaScript",
        "emoji": "⏳",
        "lessons": [
            {
                "title": "Synchronous vs Asynchronous",
                "html": """
<p>JS is <b>single-threaded</b> — it can only do one thing at a time.
<b>Synchronous</b> code blocks: each line waits for the previous.
<b>Asynchronous</b> code schedules work for later without
blocking:</p>

<pre class="code">// synchronous: each line blocks
console.log("1");
console.log("2");    // waits for "1" to finish
console.log("3");    // waits for "2"

// asynchronous: doesn't block
console.log("start");
setTimeout(() =&gt; console.log("later"), 0);
console.log("end");
// output: "start" → "end" → "later"
// even with delay=0, the callback runs AFTER all sync code!</pre>

<p>The event loop: JS runs sync code first, then processes the
<b>callback queue</b> (timers, events) and the <b>microtask queue</b>
(promises). Microtasks always run before the next timer. This is why
promise callbacks execute before setTimeout callbacks.</p>
""",
                "tryit": """console.log("1: sync start");

setTimeout(() => console.log("4: setTimeout (macrotask)"), 0);

Promise.resolve().then(() => console.log("3: promise (microtask)"));

console.log("2: sync end");

// Output order: 1 → 2 → 3 → 4
// Microtasks (promises) always run before macrotasks (timers)!
""",
            },
            {
                "title": "Callbacks & Promises",
                "html": """
<p><b>Callbacks</b> were the original async pattern — pass a function
to be called when the operation completes. Nested callbacks for
sequential operations create <b>callback hell</b>:</p>

<pre class="code">// callback hell (the problem)
getUser(id, (user) =&gt; {
  getPosts(user.id, (posts) =&gt; {
    getComments(posts[0].id, (comments) =&gt; {
      console.log(comments);   // deeply nested!
    });
  });
});</pre>

<p>A <b>Promise</b> represents a value that will be available later. It
has three states: <b>pending</b> → <b>fulfilled</b> (with a value) or
<b>rejected</b> (with an error). Once settled, a promise's state never
changes:</p>

<pre class="code">const promise = new Promise((resolve, reject) =&gt; {
  // async work here
  setTimeout(() =&gt; {
    const success = true;
    if (success) resolve("data!");
    else reject(new Error("failed"));
  }, 1000);
});

promise
  .then(value =&gt; console.log("got:", value))
  .catch(error =&gt; console.log("error:", error.message));</pre>

<p>Promises chain — each <code>.then()</code> receives the previous
one's return value, flattening callback hell into a readable
chain.</p>
""",
                "tryit": """// creating a promise
function wait(ms) {
  return new Promise((resolve) => {
    setTimeout(() => resolve(`waited ${ms}ms`), ms);
  });
}

// promise chaining
wait(100)
  .then(msg => {
    console.log(msg);
    return wait(100);       // return another promise
  })
  .then(msg => {
    console.log(msg);
    return "all done";
  })
  .then(final => console.log(final));

// promise states
const p = new Promise((resolve) => resolve(42));
console.log(p instanceof Promise);  // true

// settled promises
Promise.resolve("instant").then(v => console.log(v));
Promise.reject(new Error("instant fail")).catch(e => console.log(e.message));
""",
            },
            {
                "title": "then(), catch() & finally()",
                "html": """
<p>The three instance methods every promise has:</p>

<pre class="code">fetchData()
  .then(data =&gt; {          // runs on success
    console.log(data);
    return data.id;         // return value passes to next .then()
  })
  .then(id =&gt; {
    console.log("id:", id);
  })
  .catch(error =&gt; {         // catches ANY error above
    console.error("failed:", error.message);
  })
  .finally(() =&gt; {          // always runs (cleanup)
    console.log("done");
  });</pre>

<p><code>.catch()</code> catches errors from ANY previous
<code>.then()</code> — it's like a try/catch for the whole chain.
<code>.finally()</code> doesn't receive the result; it's for cleanup
(hide a loading spinner, close a connection).</p>
""",
                "tryit": """function fetchUser(id) {
  return new Promise((resolve, reject) => {
    setTimeout(() => {
      if (id <= 0) reject(new Error("Invalid ID"));
      else resolve({ id, name: `User${id}` });
    }, 100);
  });
}

fetchUser(1)
  .then(user => {
    console.log("got user:", user.name);
    return fetchUser(user.id + 1);   // chain to another promise
  })
  .then(user => console.log("and also:", user.name))
  .catch(err => console.log("error:", err.message))
  .finally(() => console.log("cleanup done"));

// error in the chain
fetchUser(-5)
  .then(user => console.log(user))
  .catch(err => console.log("caught:", err.message))
  .finally(() => console.log("always"));
""",
            },
            {
                "title": "Promise.all(), allSettled(), race() & any()",
                "html": """
<p>Four static methods for handling <b>multiple promises</b>:</p>

<pre class="code">// all: wait for ALL to succeed (fails if ANY fails)
const [users, posts, comments] = await Promise.all([
  fetchUsers(), fetchPosts(), fetchComments()
]);

// allSettled: wait for ALL to settle (success or fail)
const results = await Promise.allSettled([
  fetchA(), fetchB(), fetchC()
]);
// results: [{status: "fulfilled", value: ...}, {status: "rejected", reason: ...}]

// race: first to settle wins (success OR failure)
const fastest = await Promise.race([serverA(), serverB()]);

// any: first to SUCCEED wins (ignores rejections)
const first = await Promise.any([mirror1(), mirror2(), mirror3()]);</pre>

<ul>
<li><b>all</b> — fail-fast: one rejection rejects the whole thing</li>
<li><b>allSettled</b> — never rejects; gives status for each</li>
<li><b>race</b> — first settled (even if rejected) wins</li>
<li><b>any</b> — first fulfilled wins; rejects only if ALL reject</li>
</ul>
""",
                "tryit": """// create test promises
const makePromise = (name, ms, shouldFail = false) =>
  new Promise((resolve, reject) => {
    setTimeout(() => {
      shouldFail ? reject(new Error(`${name} failed`)) : resolve(`${name} done`);
    }, ms);
  });

// Promise.all — all must succeed
Promise.all([
  makePromise("A", 100),
  makePromise("B", 200),
])
  .then(results => console.log("all:", results))
  .catch(e => console.log("all failed:", e.message));

// Promise.allSettled — get every result
Promise.allSettled([
  makePromise("X", 100),
  makePromise("Y", 100, true),   // this one fails
])
  .then(results => {
    results.forEach(r => {
      console.log(r.status, r.value || r.reason?.message);
    });
  });

// Promise.race — first wins
Promise.race([
  makePromise("fast", 50),
  makePromise("slow", 300),
])
  .then(winner => console.log("race winner:", winner));
""",
            },
            {
                "title": "async & await",
                "html": """
<p><code>async/await</code> is syntactic sugar over promises that makes
async code <b>look and read like synchronous code</b>:</p>

<pre class="code">// async function always returns a Promise
async function getData() {
  return 42;    // becomes Promise.resolve(42)
}

// await pauses INSIDE the async function until the promise settles
async function main() {
  const user = await fetchUser(1);      // waits for the promise
  const posts = await fetchPosts(user.id);
  const comments = await fetchComments(posts[0].id);
  console.log(comments);                 // reads like sync code!
}

// error handling with try/catch (the natural way)
async function safeMain() {
  try {
    const data = await riskyOperation();
    console.log(data);
  } catch (error) {
    console.error("failed:", error.message);
  } finally {
    console.log("done");
  }
}

// run independent promises in PARALLEL with Promise.all
async function efficient() {
  const [users, posts] = await Promise.all([
    fetchUsers(),      // start both
    fetchPosts(),      // at the same time
  ]);                    // wait for both
}</pre>

<p><code>await</code> can only be used inside <code>async</code>
functions (or top-level in modules). It pauses the async function, NOT
the whole thread — other code continues running.</p>
""",
                "tryit": """function wait(ms) {
  return new Promise(resolve => setTimeout(() => resolve(ms), ms));
}

// async/await: sequential (easy to read)
async function sequential() {
  console.log("starting...");
  const a = await wait(200);
  console.log("step 1 done:", a);
  const b = await wait(200);
  console.log("step 2 done:", b);
  return a + b;
}

// async/await: parallel (faster for independent tasks)
async function parallel() {
  const start = Date.now();
  const [a, b] = await Promise.all([wait(200), wait(200)]);
  console.log(`both done in ${Date.now() - start}ms (not 400ms!)`);
}

// error handling with try/catch
async function safeOperation() {
  try {
    await wait(100);
    throw new Error("something went wrong");
  } catch (e) {
    console.log("caught:", e.message);
  } finally {
    console.log("cleanup");
  }
}

// run them
(async () => {
  await sequential();
  await parallel();
  await safeOperation();
})();
""",
            },
            {
                "title": "Error Handling in Async Code",
                "html": """
<p>Async errors don't get caught by regular try/catch — they need
special handling depending on the pattern:</p>

<pre class="code">// with promises: .catch()
riskyOperation().catch(err =&gt; console.log(err));

// with async/await: try/catch works naturally
async function main() {
  try {
    await riskyOperation();
  } catch (err) {
    console.log(err.message);
  }
}

// ⚠️ common mistake: forgetting await
async function buggy() {
  try {
    riskyOperation();      // ← missing await! Error is UNHANDLED
  } catch (e) { /* never reached */ }
}

// Promise.all fails fast — use allSettled for independent ops
async function fetchAll() {
  const results = await Promise.allSettled([
    fetchA(), fetchB(), fetchC()
  ]);
  const errors = results.filter(r =&gt; r.status === "rejected");
  const values = results.filter(r =&gt; r.status === "fulfilled")
                         .map(r =&gt; r.value);
  return { values, errors };
}</pre>

<p>Always handle async errors: an unhandled promise rejection crashes
modern Node.js and shows ugly console errors in browsers. Add a global
handler as a safety net:
<code>window.addEventListener("unhandledrejection", e =&gt; ...)</code></p>
""",
                "tryit": """// the #1 mistake: forgetting await
async function buggy() {
  try {
    Promise.reject(new Error("unhandled!"));  // no await!
  } catch (e) {
    console.log("never reached!");  // catch can't see it
  }
}

// the fix: await the promise
async function correct() {
  try {
    await Promise.reject(new Error("caught!"));
  } catch (e) {
    console.log("now caught:", e.message);
  }
}

(async () => {
  await buggy();
  await correct();

  // allSettled for independent operations
  const results = await Promise.allSettled([
    Promise.resolve("success 1"),
    Promise.reject(new Error("fail")),
    Promise.resolve("success 2"),
  ]);
  results.forEach(r => {
    console.log(r.status, r.value ?? r.reason?.message);
  });
})();
""",
            },
        ],
        "quiz": [
            {
                "type": "mc",
                "question": "What does an async function always return?",
                "options": ["undefined", "A Promise", "The resolved value", "An iterator"],
                "answer": 1,
                "explain": "async functions wrap their return value in Promise.resolve().",
            },
            {
                "type": "blank",
                "question": "The operator that pauses inside an async function is <code>____</code>.",
                "answers": ["await", "await operator"],
                "explain": "await pauses the async function until the promise settles.",
            },
            {
                "type": "mc",
                "question": "Promise.all() rejects when:",
                "options": ["All promises reject", "ANY promise rejects", "The first promise settles", "Never"],
                "answer": 1,
                "explain": "Promise.all is fail-fast: one rejection rejects the whole batch.",
            },
            {
                "type": "mc",
                "question": "The #1 mistake with async/await error handling:",
                "options": [
                    "Using try/catch",
                    "Forgetting 'await' before the promise call",
                    "Using .catch()",
                    "Throwing too many errors",
                ],
                "answer": 1,
                "explain": "Without await, the try/catch can't catch the async error — it's unhandled.",
            },
            {
                "type": "mc",
                "question": "Which Promise method never rejects?",
                "options": ["Promise.all()", "Promise.race()", "Promise.allSettled()", "Promise.any()"],
                "answer": 2,
                "explain": "allSettled always resolves with {status, value/reason} for each promise.",
            },
        ],
    },

    # ------------------------------------------------------------------ js08
    {
        "id": "js08",
        "title": "Modules",
        "emoji": "📄",
        "lessons": [
            {
                "title": "Modules: export & import",
                "html": """
<p><b>Modules</b> are self-contained files that export values for other
files to import. Modern JS uses ES modules natively:</p>

<pre class="code">// math.js — export values
export const PI = 3.14159;
export function circleArea(r) { return PI * r ** 2; }

// default export (one per module)
export default class Calculator { ... }

// app.js — import them
import Calculator from './math.js';          // default import (no braces)
import { PI, circleArea } from './math.js';  // named imports (braces)
import * as math from './math.js';           // namespace import

console.log(PI);                  // 3.14159
console.log(circleArea(2));      // 12.57
console.log(math.PI);            // 3.14159 (via namespace)</pre>

<p>Modules are <b>strict mode</b> by default, <b>deferred</b> (load
after HTML parsing), and <b>cached</b> (imported once, shared by all
importers). They enable code organization, dependency management, and
tree-shaking (removing unused code at build time).</p>

<p>In the browser: <code>&lt;script type="module" src="app.js"&gt;</code>.
In Node.js: <code>.mjs</code> extension or <code>"type":
"module"</code> in package.json.</p>
""",
            },
            {
                "title": "Dynamic import() & Module Resolution",
                "html": """
<p><b>Dynamic import</b> loads a module on demand — returning a
Promise. This enables code splitting and lazy loading:</p>

<pre class="code">// static import: loaded immediately
import { heavy } from './heavy.js';

// dynamic import: loaded when needed
button.addEventListener('click', async () =&gt; {
  const { chart } = await import('./chart.js');
  chart.render();     // chart.js only loaded now!
});</pre>

<p>Module resolution: the browser resolves relative paths
(<code>./utils.js</code>), bare paths need import maps, and the file
extension is required in browsers (unlike some bundlers). MDN's guide
covers the details.</p>
""",
            },
        ],
        "quiz": [
            {
                "type": "mc",
                "question": "How many default exports can a module have?",
                "options": ["Zero", "One", "Unlimited", "One per type"],
                "answer": 1,
                "explain": "Each module can have exactly one default export (plus any number of named exports).",
            },
            {
                "type": "blank",
                "question": "Dynamic import returns a ____.",
                "answers": ["promise", "Promise"],
                "explain": "import() returns a Promise that resolves to the module namespace.",
            },
        ],
    },
]
