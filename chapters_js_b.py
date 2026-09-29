"""JS Tutor chapters 3-5 (Phases 3-5), grounded in MDN Web Docs."""

CHAPTERS_JS_B = [
    # ------------------------------------------------------------------ js03
    {
        "id": "js03",
        "title": "Functions",
        "emoji": "🧩",
        "lessons": [
            {
                "title": "Functions & Parameters",
                "html": """
<p>Functions package behaviour behind a name. JS functions are
<b>first-class citizens</b> — they can be stored in variables, passed as
arguments, and returned from other functions:</p>

<pre class="code">// declaration
function greet(name) {
  return `Hello, ${name}!`;
}

// call it
console.log(greet("Ada"));     // "Hello, Ada!"

// multiple parameters
function add(a, b) {
  return a + b;
}
console.log(add(2, 3));        // 5</pre>

<p>Parameters are the named placeholders in the definition
(<code>a, b</code>); arguments are the actual values passed in
(<code>2, 3</code>). JS doesn't enforce parameter counts — missing
arguments become <code>undefined</code>, extras are ignored (but
accessible via <code>arguments</code> or rest params).</p>
""",
                "tryit": """function greet(name, greeting = "Hello") {
  return `${greeting}, ${name}!`;
}

console.log(greet("Ada"));
console.log(greet("Grace", "Hi"));

// functions as values
const sayHi = greet;
console.log(sayHi("Beej"));

// passing functions to functions
function callTwice(fn, arg) {
  console.log(fn(arg));
  console.log(fn(arg));
}
callTwice(greet, "MDN");
""",
            },
            {
                "title": "Return Values",
                "html": """
<p><code>return</code> sends a value back to the caller and exits the
function immediately:</p>

<pre class="code">function add(a, b) {
  return a + b;      // exits here
  console.log("never runs");
}

console.log(add(1, 2));   // 3

// functions without return → undefined
function log(msg) {
  console.log(msg);
  // no return → returns undefined
}
console.log(log("hi"));  // undefined</pre>

<p>Functions can return any type — including other functions, objects,
arrays. Multiple values come back as an object or array:</p>

<pre class="code">function getStats(numbers) {
  return { min: Math.min(...numbers), max: Math.max(...numbers) };
}
const { min, max } = getStats([3, 1, 4, 1, 5]);
console.log(min, max);   // 1 5</pre>
""",
                "tryit": """function calculateCircle(r) {
  const area = Math.PI * r ** 2;
  const circumference = 2 * Math.PI * r;
  return { area: area.toFixed(2), circumference: circumference.toFixed(2) };
}

const { area, circumference } = calculateCircle(5);
console.log("area:", area);
console.log("circumference:", circumference);

// early return pattern
function classify(n) {
  if (n < 0) return "negative";
  if (n === 0) return "zero";
  return "positive";
}
console.log(classify(-5), classify(0), classify(7));
""",
            },
            {
                "title": "Function Expressions & Arrow Functions",
                "html": """
<p>Functions can be <b>expressions</b> (assigned to variables) rather
than declarations. The modern arrow syntax is shorter and has a
different <code>this</code> binding:</p>

<pre class="code">// function expression
const double = function(n) { return n * 2; };

// arrow function (same result, shorter)
const double2 = (n) => n * 2;

// single parameter → parens optional
const triple = n => n * 3;

// multiple parameters → parens required
const add = (a, b) => a + b;

// no parameters → empty parens
const hello = () => "hello!";

// multi-line body → braces + return
const process = (x) => {
  const result = x * 2;
  return result + 1;
};

// returning an object literal → wrap in parens
const makePair = (a, b) => ({ first: a, second: b });</pre>

<p>Key difference: arrow functions don't have their own
<code>this</code> — they inherit it from the surrounding scope. This
makes them perfect for callbacks where you want the outer
<code>this</code>.</p>
""",
                "tryit": """const nums = [1, 2, 3, 4, 5];

// arrow functions shine as callbacks
const doubled = nums.map(n => n * 2);
console.log("doubled:", doubled);

const evens = nums.filter(n => n % 2 === 0);
console.log("evens:", evens);

const sum = nums.reduce((acc, n) => acc + n, 0);
console.log("sum:", sum);

// implicit return — no braces needed
const squares = nums.map(n => n ** 2);
console.log("squares:", squares);

// multi-line with explicit return
const labeled = nums.map(n => {
  const label = n % 2 === 0 ? "even" : "odd";
  return `${n} is ${label}`;
});
console.log(labeled);
""",
            },
            {
                "title": "Default & Rest Parameters",
                "html": """
<p><b>Default parameters</b> provide fallback values when an argument
is <code>undefined</code>:</p>

<pre class="code">function greet(name = "guest", greeting = "Hello") {
  return `${greeting}, ${name}!`;
}
console.log(greet());           // "Hello, guest!"
console.log(greet("Ada"));     // "Hello, Ada!"
console.log(greet("Ada", "Hi")); // "Hi, Ada!"</pre>

<p><b>Rest parameters</b> (<code>...name</code>) collect remaining
arguments into a real array:</p>

<pre class="code">function sum(...numbers) {
  return numbers.reduce((acc, n) => acc + n, 0);
}
console.log(sum(1, 2));           // 3
console.log(sum(1, 2, 3, 4, 5)); // 15

// mixed: named params first, rest last
function introduce(greeting, ...names) {
  return `${greeting}, ${names.join(" and ")}!`;
}
console.log(introduce("Hi", "Ada", "Grace"));</pre>

<p>Rest parameters must be the <b>last</b> parameter. They replace the
legacy <code>arguments</code> object with a real array that has
<code>map</code>, <code>filter</code>, etc.</p>
""",
                "tryit": """// Default parameters
function power(base, exponent = 2) {
  return base ** exponent;
}
console.log(power(3));     // 9 (default exponent = 2)
console.log(power(3, 3));  // 27

// Rest parameters
function average(...scores) {
  if (scores.length === 0) return 0;
  return scores.reduce((a, b) => a + b, 0) / scores.length;
}
console.log(average(90, 85, 92));  // average of 3 scores
console.log(average());            // 0 (empty)

// combining defaults + rest
function createPost(title, tags = ["general"], ...meta) {
  console.log("title:", title);
  console.log("tags:", tags);
  console.log("meta:", meta);
}
createPost("Hello World", "js", "tutorial", "2026");
""",
            },
            {
                "title": "Spread Syntax",
                "html": """
<p>Spread (<code>...</code>) "unpacks" an iterable into individual
elements — the mirror of rest parameters. It expands arrays, strings,
and objects in places where multiple elements are expected:</p>

<pre class="code">// spread in function calls
const nums = [3, 1, 4];
console.log(Math.max(...nums));    // 4 (not [3,1,4])

// copy an array (shallow)
const copy = [...nums];

// merge arrays
const a = [1, 2], b = [3, 4];
const merged = [...a, ...b];       // [1, 2, 3, 4]

// spread in object literals
const defaults = { theme: "light", lang: "en" };
const user = { ...defaults, theme: "dark" };  // override theme
// { theme: "dark", lang: "en" }</pre>

<p>Spread creates <b>shallow</b> copies — nested objects are still
shared references. For deep copies, use
<code>structuredClone()</code>.</p>
""",
                "tryit": """const arr1 = [1, 2, 3];
const arr2 = [4, 5, 6];

// spread in function calls
console.log(Math.max(...arr1, ...arr2));  // 6

// array copy + merge
const combined = [...arr1, 0, ...arr2];
console.log(combined);   // [1, 2, 3, 0, 4, 5, 6]

// string spread (iterates characters)
console.log([..."abc"]);  // ["a", "b", "c"]

// object spread: merge + override
const base = { a: 1, b: 2 };
const extended = { ...base, b: 99, c: 3 };
console.log(extended);   // { a: 1, b: 99, c: 3 }

// shallow copy caveat
const nested = { inner: { val: 1 } };
const copy = { ...nested };
copy.inner.val = 99;
console.log(nested.inner.val);  // 99 — still shared!
""",
            },
            {
                "title": "Scope & Closures",
                "html": """
<p><b>Scope</b> determines where variables are visible. JS has:
<b>global</b> scope, <b>function</b> scope, and <b>block</b> scope
(let/const):</p>

<pre class="code">const global = "everywhere";

function outer() {
  const outerVar = "visible in outer";
  function inner() {
    console.log(global);    // ✓ can see global
    console.log(outerVar);  // ✓ can see outer's variable
  }
  inner();
}</pre>

<p>A <b>closure</b> is a function that remembers the variables from
where it was created, even after that scope has exited. It's one of
JS's most powerful features:</p>

<pre class="code">function makeCounter() {
  let count = 0;              // private variable!
  return function() {
    count++;                  // closure captures count
    return count;
  };
}

const counter = makeCounter();
console.log(counter());   // 1
console.log(counter());   // 2
console.log(counter());   // 3 — count persists!

const counter2 = makeCounter();
console.log(counter2());  // 1 — independent counter!</pre>

<p>Closures enable <b>data privacy</b> (count is invisible from
outside), <b>factories</b> (makeCounter creates independent
instances), and <b>partial application</b>. Every callback that
references outer variables is using a closure.</p>
""",
                "tryit": """// Closure: a private counter
function makeWallet(startingBalance) {
  let balance = startingBalance;   // private!

  return {
    deposit(amount) { balance += amount; return balance; },
    withdraw(amount) {
      if (amount > balance) return "insufficient funds";
      balance -= amount;
      return balance;
    },
    getBalance() { return balance; },
  };
}

const wallet = makeWallet(100);
console.log(wallet.deposit(50));   // 150
console.log(wallet.withdraw(30));  // 120
console.log(wallet.getBalance()); // 120
// wallet.balance = 999999;       // doesn't work — it's private!

// closure in a loop (the classic interview question)
const functions = [];
for (let i = 0; i < 3; i++) {
  functions.push(() => i);   // let creates a new i per iteration
}
console.log(functions.map(f => f()));  // [0, 1, 2] — not [3, 3, 3]!
""",
            },
            {
                "title": "Callbacks",
                "html": """
<p>A <b>callback</b> is a function passed as an argument to another
function, to be called later. Callbacks are the foundation of
event handling, array methods, and async code:</p>

<pre class="code">// callback in array methods
const nums = [1, 2, 3];
const doubled = nums.map(n =&gt; n * 2);      // [2, 4, 6]
const evens = nums.filter(n =&gt; n % 2 === 0); // [2]

// callback in setTimeout (async)
setTimeout(() =&gt; {
  console.log("1 second later");
}, 1000);

// custom function that accepts a callback
function process(data, onSuccess, onError) {
  if (data) onSuccess(data);
  else onError("no data");
}

process({ msg: "hello" },
  (d) =&gt; console.log("got:", d.msg),
  (err) =&gt; console.log("error:", err)
);</pre>

<p>Callbacks can be <b>synchronous</b> (called immediately, like in
map) or <b>asynchronous</b> (called later, like setTimeout). Nested
callbacks for sequential async operations lead to
<b>callback hell</b> — the problem Promises solve (Async chapter).</p>
""",
                "tryit": """// callbacks with array methods
const words = ["hello", "world", "js"];

const upper = words.map(w => w.toUpperCase());
console.log(upper);

const long = words.filter(w => w.length > 4);
console.log("long words:", long);

// custom higher-order function
function repeat(times, fn) {
  for (let i = 0; i < times; i++) fn(i);
}
repeat(3, (i) => console.log(`iteration ${i + 1}`));

// callback with error pattern
function divide(a, b, callback) {
  if (b === 0) {
    callback(new Error("division by zero"), null);
    return;
  }
  callback(null, a / b);
}
divide(10, 2, (err, result) => {
  if (err) console.log("error:", err.message);
  else console.log("result:", result);
});
""",
            },
        ],
        "quiz": [
            {
                "type": "mc",
                "question": "What does an arrow function NOT have its own of?",
                "options": ["Parameters", "Return value", "this", "Name"],
                "answer": 2,
                "explain": "Arrow functions inherit this from the surrounding scope — that's their key feature.",
            },
            {
                "type": "blank",
                "question": "Rest parameters collect remaining arguments into a ____.",
                "answers": ["array", "real array"],
                "explain": "function sum(...nums) — nums is a real array with map/filter/etc.",
            },
            {
                "type": "mc",
                "question": "What is a closure?",
                "options": [
                    "A closed curly brace",
                    "A function that remembers variables from where it was created",
                    "A way to end a program",
                    "A type of loop",
                ],
                "answer": 1,
                "explain": "Closures capture outer variables, enabling data privacy and factories.",
            },
            {
                "type": "mc",
                "question": "The spread syntax ... does what to an array in a function call?",
                "options": [
                    "Collects arguments",
                    "Unpacks elements as individual arguments",
                    "Copies the reference",
                    "Sorts it",
                ],
                "answer": 1,
                "explain": "Math.max(...[3,1,4]) becomes Math.max(3,1,4).",
            },
        ],
    },

    # ------------------------------------------------------------------ js04
    {
        "id": "js04",
        "title": "Arrays & Objects",
        "emoji": "📦",
        "lessons": [
            {
                "title": "Arrays",
                "html": """
<p>Arrays are ordered, zero-indexed collections. They can hold any mix
of types and grow dynamically:</p>

<pre class="code">const fruits = ["apple", "banana", "cherry"];

fruits.length           // 3
fruits[0]               // "apple" (first)
fruits[fruits.length - 1]  // "cherry" (last)

fruits.push("date");    // add to end → 4
fruits.pop();           // remove from end → "date"
fruits.unshift("avocado"); // add to start
fruits.shift();          // remove from start

fruits.indexOf("banana") // 1
fruits.includes("apple") // true

// slicing (doesn't modify original)
fruits.slice(1, 3)       // ["banana", "cherry"]

// joining
fruits.join(", ")        // "apple, banana, cherry"</pre>

<p>Arrays are actually objects with numeric keys —
<code>typeof fruits</code> returns <code>"object"</code>. Use
<code>Array.isArray()</code> to check.</p>
""",
                "tryit": """const todo = ["learn JS", "build projects", "get a job"];

console.log("length:", todo.length);
console.log("first:", todo[0]);
console.log("last:", todo[todo.length - 1]);

// mutate
todo.push("teach others");
console.log("after push:", todo);
todo.shift();
console.log("after shift:", todo);

// search
console.log("has 'learn JS':", todo.includes("learn JS"));
console.log("index of 'build':", todo.indexOf("build projects"));

// slice (non-destructive)
const firstTwo = todo.slice(0, 2);
console.log("sliced:", firstTwo);
console.log("original:", todo);
""",
            },
            {
                "title": "Array Methods",
                "html": """
<p>The three essential array methods — <code>map</code>,
<code>filter</code>, <code>reduce</code> — transform data without
mutating the original:</p>

<pre class="code">const nums = [1, 2, 3, 4, 5];

// map: transform each element → new array
const doubled = nums.map(n =&gt; n * 2);       // [2, 4, 6, 8, 10]

// filter: keep elements that pass the test → new array
const evens = nums.filter(n =&gt; n % 2 === 0); // [2, 4]

// reduce: boil down to a single value
const sum = nums.reduce((acc, n) =&gt; acc + n, 0); // 15

// find: first matching element
const first = nums.find(n =&gt; n &gt; 3);        // 4

// some/every: boolean checks
nums.some(n =&gt; n &gt; 4);       // true (at least one)
nums.every(n =&gt; n &gt; 0);      // true (all of them)

// sort: MUTATES the original! Use [...arr].sort() to avoid
const sorted = [...nums].sort((a, b) =&gt; b - a);  // descending</pre>

<p><code>map</code>, <code>filter</code>, and <code>reduce</code> are
the functional programming trio — they chain beautifully:
<code>nums.filter(n =&gt; n &gt; 2).map(n =&gt; n * 10).reduce((a, b) =&gt; a + b)</code></p>
""",
                "tryit": """const products = [
  { name: "Laptop", price: 999, inStock: true },
  { name: "Mouse", price: 25, inStock: true },
  { name: "Keyboard", price: 75, inStock: false },
  { name: "Monitor", price: 300, inStock: true },
];

// map: extract names
const names = products.map(p => p.name);
console.log("names:", names);

// filter: in-stock items
const available = products.filter(p => p.inStock);
console.log("in stock:", available.map(p => p.name));

// reduce: total value of in-stock items
const total = products
  .filter(p => p.inStock)
  .reduce((sum, p) => sum + p.price, 0);
console.log("total value:", total);

// find: first expensive item
const expensive = products.find(p => p.price > 200);
console.log("first expensive:", expensive?.name);

// chaining
const result = products
  .filter(p => p.inStock)
  .map(p => `${p.name} ($${p.price})`)
  .join(", ");
console.log("shopping list:", result);
""",
            },
            {
                "title": "Destructuring",
                "html": """
<p><b>Destructuring</b> unpacks values from arrays and objects into
distinct variables — cleaner than manual assignment:</p>

<pre class="code">// array destructuring
const [first, second] = [1, 2, 3];
console.log(first, second);      // 1 2

// skip elements
const [, third] = [1, 2, 3];    // 3

// default values
const [a = 10, b = 20] = [1];   // a=1, b=20 (default)

// swap variables
let x = 1, y = 2;
[x, y] = [y, x];                 // x=2, y=1

// object destructuring
const user = { name: "Ada", age: 36 };
const { name, age } = user;      // name="Ada", age=36

// rename
const { name: fullName } = user; // fullName="Ada"

// nested destructuring
const config = { db: { host: "localhost", port: 5432 } };
const { db: { host, port } } = config;</pre>

<p>Destructuring also works in function parameters — the pattern for
options objects:</p>

<pre class="code">function connect({ host = "localhost", port = 3000 }) {
  console.log(`${host}:${port}`);
}
connect({ port: 8080 });   // "localhost:8080"</pre>
""",
                "tryit": """// Array destructuring
const rgb = [255, 128, 0];
const [red, green, blue] = rgb;
console.log(`R:${red} G:${green} B:${blue}`);

// Skip + default
const [first, , third = "default"] = ["a", "b"];
console.log(first, third);

// Swap without a temp variable
let x = 1, y = 2;
[x, y] = [y, x];
console.log("x:", x, "y:", y);

// Object destructuring in function params
function printUser({ name, role = "user", email }) {
  console.log(`${name} (${role}) — ${email}`);
}
printUser({ name: "Ada", email: "ada@x.io" });
printUser({ name: "Admin", role: "admin", email: "admin@x.io" });
""",
            },
            {
                "title": "Objects, Properties & Methods",
                "html": """
<p>Objects are key-value collections — the fundamental data structure
of JS. Almost everything is an object:</p>

<pre class="code">const user = {
  name: "Ada",              // property
  age: 36,
  "has-pets": true,         // keys with dashes need quotes
  greet() {                 // method (shorthand)
    return `Hi, I'm ${this.name}`;
  },
};

// access: dot or bracket
user.name                  // "Ada"
user["age"]                // 36
user["has-pets"]           // true (bracket needed for dashes)

// add / modify / delete
user.email = "ada@x.io";   // add
user.age = 37;             // modify
delete user.email;         // remove

// check if property exists
"name" in user             // true
user.hasOwnProperty("age") // true
user.email?.length         // undefined (already deleted)</pre>

<p><code>this</code> inside a method refers to the object the method is
called on — that's how <code>this.name</code> works above. The value of
<code>this</code> depends on HOW the function is called, not where it's
defined (the Advanced chapter covers this deeply).</p>
""",
                "tryit": """const book = {
  title: "Eloquent JavaScript",
  author: "Marijn Haverbeke",
  pages: 472,
  read: false,

  // method
  summary() {
    return `${this.title} by ${this.author} (${this.pages}p)`;
  },

  markRead() {
    this.read = true;
    return `${this.title} — marked as read!`;
  },
};

console.log(book.summary());
console.log(book.markRead());
console.log("read:", book.read);

// dynamic keys
const key = "publisher";
book[key] = "No Starch Press";
console.log(book.publisher);

// Object.keys/values/entries
console.log("keys:", Object.keys(book));
console.log("values:", Object.values(book));
""",
            },
            {
                "title": "Optional Chaining & Nullish Coalescing",
                "html": """
<p>Two modern operators that make null-safety elegant instead of
messy.</p>

<p><b><code>?.</code> (optional chaining)</b> — safely access nested
properties without checking each level:</p>

<pre class="code">// before: the pyramid of doom
if (user &amp;&amp; user.profile &amp;&amp; user.profile.email) {
  console.log(user.profile.email);
}

// after: one line
console.log(user?.profile?.email);   // undefined, no crash!

// also works with methods and array access
const result = data?.find?.(x =&gt; x.id === 1);
const first = list?.[0];</pre>

<p><b><code>??</code> (nullish coalescing)</b> — default value for
null/undefined only (not 0 or ""):</p>

<pre class="code">const volume = 0;
volume || 50    // 50 (0 is falsy — WRONG!)
volume ?? 50    // 0  (0 is not nullish — correct!)

const name = null;
name ?? "Anonymous"   // "Anonymous"</pre>

<p>They chain: <code>user?.settings?.volume ?? 50</code> — safe access
with a sensible default. These two operators eliminate most null-check
boilerplate.</p>
""",
                "tryit": """const users = [
  { name: "Ada", profile: { bio: "Programmer", social: { twitter: "@ada" } } },
  { name: "Grace", profile: {} },
  { name: "Anonymous" },
];

// optional chaining: safe deep access
console.log(users[0]?.profile?.social?.twitter);  // "@ada"
console.log(users[1]?.profile?.social?.twitter);  // undefined
console.log(users[2]?.profile?.social?.twitter);  // undefined (no crash!)

// nullish coalescing: defaults for null/undefined
for (const u of users) {
  const bio = u.profile?.bio ?? "No bio";
  const twitter = u.profile?.social?.twitter ?? "no twitter";
  console.log(`${u.name}: ${bio} | ${twitter}`);
}

// ?? vs || — the critical difference
const volume = 0;
console.log(volume || 50);   // 50 (0 is falsy — wrong!)
console.log(volume ?? 50);   // 0 (0 is not nullish — right!)
""",
            },
        ],
        "quiz": [
            {
                "type": "mc",
                "question": "What does map() return?",
                "options": ["The original array", "A new transformed array", "undefined", "A single value"],
                "answer": 1,
                "explain": "map creates a new array by transforming each element.",
            },
            {
                "type": "blank",
                "question": "To safely access nested properties without checking each level, use <code>____</code> chaining.",
                "answers": ["optional", "?.", "optional chaining"],
                "explain": "user?.profile?.email — returns undefined instead of crashing.",
            },
            {
                "type": "mc",
                "question": "What's the difference between ?? and ||?",
                "options": [
                    "No difference",
                    "?? only defaults for null/undefined; || defaults for all falsy values",
                    "|| is newer",
                    "?? works only with numbers",
                ],
                "answer": 1,
                "explain": "0 ?? 50 gives 0 (0 isn't nullish); 0 || 50 gives 50 (0 is falsy).",
            },
            {
                "type": "mc",
                "question": "In object destructuring, { name: fullName } means:",
                "options": [
                    "Access property 'fullName'",
                    "Extract 'name' and rename it to 'fullName'",
                    "Create a new property",
                    "It's invalid syntax",
                ],
                "answer": 1,
                "explain": "The pattern is { property: newName } — extract and rename in one step.",
            },
        ],
    },

    # ------------------------------------------------------------------ js05
    {
        "id": "js05",
        "title": "Advanced JavaScript",
        "emoji": "🎓",
        "lessons": [
            {
                "title": "this",
                "html": """
<p><code>this</code> is one of JS's most confusing features. Its value
depends on <b>how</b> a function is called, not where it's
defined:</p>

<pre class="code">const user = {
  name: "Ada",
  greet() { console.log(`Hi, ${this.name}`); },
};
user.greet();        // "Hi, Ada" — this = user

// the same function, different context!
const greeting = user.greet;
greeting();          // "Hi, undefined" — this = global/undefined</pre>

<ul>
<li><b>Method call</b> (<code>obj.fn()</code>) — <code>this</code> = the
object before the dot</li>
<li><b>Standalone call</b> (<code>fn()</code>) — <code>this</code> =
undefined (strict) or global</li>
<li><b>Arrow function</b> — <code>this</code> = inherited from the
enclosing scope (no own <code>this</code>)</li>
<li><b>new</b> — <code>this</code> = the newly created object</li>
<li><b>call/apply/bind</b> — explicitly set <code>this</code></li>
</ul>

<pre class="code">// arrow functions inherit this — perfect for callbacks
const timer = {
  seconds: 0,
  start() {
    setInterval(() =&gt; {
      this.seconds++;    // this = timer (arrow inherits from start)
      console.log(this.seconds);
    }, 1000);
  },
};</pre>
""",
                "tryit": """const team = {
  name: "Web Dev",
  members: ["Ada", "Grace"],
  // regular method: this = team
  printMembers() {
    // arrow function inherits this from printMembers
    this.members.forEach(member => {
      console.log(`${member} is part of ${this.name}`);
    });
  },
  // the classic bug: using a regular function inside
  printMembersBroken() {
    this.members.forEach(function(member) {
      // 'this' is undefined here — NOT team!
      console.log(`${member} is part of ${this?.name ?? "?"}`);
    });
  },
};

team.printMembers();
console.log("---");
team.printMembersBroken();

// call() and bind() — explicit this control
function introduce(city) {
  return `I'm ${this.name} from ${city}`;
}
const person = { name: "Ada" };
console.log(introduce.call(person, "London"));
console.log(introduce.bind(person)("Paris"));
""",
            },
            {
                "title": "Prototypes & Prototype Chain",
                "html": """
<p>JavaScript uses <b>prototypes</b> for inheritance — every object has
a hidden link to a prototype object. When you access a property that
doesn't exist on the object, JS looks up the <b>prototype chain</b>:</p>

<pre class="code">const animal = {
  eat() { return "eating..."; },
};

const dog = Object.create(animal);  // dog's prototype = animal
dog.bark = () =&gt; "woof!";

dog.bark();   // "woof!" — own property
dog.eat();    // "eating..." — found on prototype!

// the chain: dog → animal → Object.prototype → null</pre>

<p>When you call <code>dog.eat()</code>:</p>
<ol>
<li>Is <code>eat</code> on <code>dog</code> itself? No</li>
<li>Is it on <code>dog</code>'s prototype (<code>animal</code>)? Yes! Call it</li>
</ol>

<p>Built-in methods like <code>array.map()</code> work this way — they
live on <code>Array.prototype</code>, and every array inherits from
it. That's why you can call <code>map</code> on any array without
defining it.</p>
""",
                "tryit": """const vehicle = {
  start() { return "starting engine..."; },
  wheels: 4,
};

const car = Object.create(vehicle);
car.brand = "Tesla";
car.drive = function() {
  return `${this.brand} — ${this.start()}`;
};

console.log(car.drive());    // "Tesla — starting engine..."
console.log(car.wheels);     // 4 (inherited from vehicle)
console.log(Object.getPrototypeOf(car) === vehicle);  // true

// the prototype chain
console.log(Object.getPrototypeOf(Object.getPrototypeOf(
  Object.getPrototypeOf(car))) === null);  // true — chain ends at null

// method lookup: own first, then prototype
vehicle.start = function() { return "vroom!"; };
console.log(car.start());   // "vroom!" — prototype was modified!
""",
            },
            {
                "title": "Constructor Functions",
                "html": """
<p>Before classes existed, <b>constructor functions</b> were how you
created multiple objects with shared behaviour. They're still used in
older code and explain what classes do under the hood:</p>

<pre class="code">function Person(name, age) {
  // 'new' creates {} and sets 'this' to it
  this.name = name;
  this.age = age;
}

// methods go on the prototype (shared across all instances!)
Person.prototype.greet = function() {
  return `Hi, I'm ${this.name}`;
};

const ada = new Person("Ada", 36);
const grace = new Person("Grace", 45);

console.log(ada.greet());   // "Hi, I'm Ada"
console.log(ada instanceof Person);  // true

// shared method — both instances use the SAME function
console.log(ada.greet === grace.greet);  // true (on prototype!)</pre>

<p>The <code>new</code> keyword does 4 things:</p>
<ol>
<li>Creates an empty object <code>{}</code></li>
<li>Sets its prototype to <code>Person.prototype</code></li>
<li>Calls the function with <code>this</code> = the new object</li>
<li>Returns the object (unless the function returns its own object)</li>
</ol>
""",
                "tryit": """function Animal(name, sound) {
  this.name = name;
  this.sound = sound;
}

Animal.prototype.speak = function() {
  return `${this.name} says ${this.sound}`;
};

Animal.prototype.info = function() {
  return `${this.name} (${this.constructor.name})`;
};

const cat = new Animal("Whiskers", "meow");
const dog = new Animal("Rex", "woof");

console.log(cat.speak());  // "Whiskers says meow"
console.log(dog.speak());  // "Rex says woof"
console.log(dog.info());   // "Rex (Animal)"

// both share the same speak function (on prototype)
console.log(cat.speak === dog.speak);  // true

// adding to prototype later affects ALL instances
Animal.prototype.describe = function() {
  return `${this.name} is an animal that says ${this.sound}`;
};
console.log(cat.describe());
""",
            },
            {
                "title": "Classes",
                "html": """
<p><b>Classes</b> (ES6/ES2015) are syntactic sugar over constructor
functions + prototypes — but cleaner and less error-prone:</p>

<pre class="code">class Animal {
  constructor(name, sound) {
    this.name = name;
    this.sound = sound;
  }

  speak() {
    return `${this.name} says ${this.sound}`;
  }

  static compare(a, b) {       // static: called on the CLASS
    return a.name.localeCompare(b.name);
  }
}

const cat = new Animal("Whiskers", "meow");
console.log(cat.speak());
console.log(Animal.compare(cat, new Animal("Rex", "woof")));</pre>

<p>Everything a constructor function does, a class does — but with
enforced <code>new</code> (calling without <code>new</code> throws),
cleaner method syntax, and support for <code>extends</code>,
<code>super</code>, <code>static</code>, and private fields.</p>

<p>Under the hood, it's still prototypes. <code>class</code> is
syntactic sugar — but it's very good sugar.</p>
""",
                "tryit": """class BankAccount {
  #balance = 0;         // private field (next lesson covers this deeply)

  constructor(owner, initial = 0) {
    this.owner = owner;
    this.#balance = initial;
  }

  deposit(amount) {
    this.#balance += amount;
    return this;        // return this for chaining!
  }

  withdraw(amount) {
    if (amount > this.#balance) throw new Error("Insufficient funds");
    this.#balance -= amount;
    return this;
  }

  get balance() {       // getter
    return this.#balance;
  }

  static printAll(...accounts) {
    accounts.forEach(a => console.log(`${a.owner}: ${a.balance}`));
  }
}

const acct1 = new BankAccount("Ada", 100);
const acct2 = new BankAccount("Grace", 250);

acct1.deposit(50).withdraw(30);   // method chaining!
console.log(acct1.balance);        // 120

BankAccount.printAll(acct1, acct2);
""",
            },
            {
                "title": "Inheritance",
                "html": """
<p><b>Inheritance</b> lets a class build on another class using
<code>extends</code> and <code>super</code>:</p>

<pre class="code">class Animal {
  constructor(name) {
    this.name = name;
  }
  eat() {
    return `${this.name} is eating`;
  }
  describe() {
    return `${this.name} is an animal`;
  }
}

class Dog extends Animal {
  constructor(name, breed) {
    super(name);            // call parent's constructor (REQUIRED)
    this.breed = breed;
  }
  speak() {
    return `${this.name} says woof!`;
  }
  // override parent method
  describe() {
    return `${super.describe()} — specifically a ${this.breed}`;
  }
}

const dog = new Dog("Rex", "Golden Retriever");
dog.eat();        // inherited from Animal
dog.speak();      // own method
dog.describe();   // overridden — uses super.describe()</pre>

<p><code>super()</code> must be called before using <code>this</code>
in the constructor. <code>super.method()</code> calls the parent's
version. The <b>prototype chain</b> is set up automatically:
<code>dog</code> → <code>Dog.prototype</code> →
<code>Animal.prototype</code> → <code>Object.prototype</code>.</p>
""",
                "tryit": """class Shape {
  constructor(color = "black") {
    this.color = color;
  }
  area() {
    return 0;
  }
  describe() {
    return `A ${this.color} shape with area ${this.area().toFixed(2)}`;
  }
}

class Circle extends Shape {
  constructor(radius, color) {
    super(color);
    this.radius = radius;
  }
  area() { return Math.PI * this.radius ** 2; }
}

class Rectangle extends Shape {
  constructor(width, height, color) {
    super(color);
    this.width = width;
    this.height = height;
  }
  area() { return this.width * this.height; }
}

const shapes = [
  new Circle(5, "blue"),
  new Rectangle(4, 6, "red"),
  new Circle(2, "green"),
];

shapes.forEach(s => console.log(s.describe()));
""",
            },
            {
                "title": "Getters, Setters & Private Fields",
                "html": """
<p><b>Getters</b> and <b>setters</b> look like properties but run code.
<b>Private fields</b> (prefixed with <code>#</code>) are truly
invisible from outside the class:</p>

<pre class="code">class Temperature {
  #celsius = 0;              // private — invisible outside!

  get celsius() {
    return this.#celsius;
  }

  set celsius(value) {
    if (value &lt; -273.15) {
      throw new Error("Below absolute zero!");
    }
    this.#celsius = value;
  }

  get fahrenheit() {         // computed getter
    return this.#celsius * 9 / 5 + 32;
  }

  set fahrenheit(value) {
    this.#celsius = (value - 32) * 5 / 9;
  }
}

const temp = new Temperature();
temp.celsius = 25;           // calls the setter
console.log(temp.fahrenheit); // 77 — computed getter
// temp.#celsius              // SyntaxError — truly private!</pre>

<p>Private fields with <code>#</code> are enforced by the language —
unlike the old underscore convention (<code>_private</code>) which was
just a naming hint. They can't be accessed, enumerated, or seen in
JSON.</p>
""",
                "tryit": """class SecureStore {
  #data = new Map();
  #accessLog = [];

  set(key, value) {
    this.#data.set(key, value);
    this.#accessLog.push(`SET ${key}`);
    return this;
  }

  get(key) {
    this.#accessLog.push(`GET ${key}`);
    return this.#data.get(key);
  }

  // read-only access to the log
  get log() {
    return [...this.#accessLog];  // return a copy!
  }

  // computed property
  get size() {
    return this.#data.size;
  }
}

const store = new SecureStore();
store.set("name", "Ada").set("role", "admin");
console.log(store.get("name"));  // "Ada"
console.log(store.size);         // 2
console.log(store.log);          // ["SET name", "SET role", "GET name"]
// store.#data                   // SyntaxError!
""",
            },
            {
                "title": "Static Members & Symbols",
                "html": """
<p><b>Static members</b> belong to the class itself, not to instances
— they're utility methods and properties:</p>

<pre class="code">class MathHelper {
  static PI = 3.14159;         // static property

  static circleArea(r) {       // static method
    return this.PI * r ** 2;   // 'this' = the class itself
  }

  static clamp(value, min, max) {
    return Math.min(Math.max(value, min), max);
  }
}

// called on the CLASS, not instances
console.log(MathHelper.PI);             // 3.14159
console.log(MathHelper.circleArea(2));  // 12.57
console.log(MathHelper.clamp(15, 0, 10)); // 10

// const m = new MathHelper();  // not useful — no constructor</pre>

<p><b>Symbols</b> create unique identifiers that never collide — even
two symbols with the same description are different:</p>

<pre class="code">const id1 = Symbol("id");
const id2 = Symbol("id");
console.log(id1 === id2);    // false — always unique!

// use as object keys (hidden from for...in and JSON)
const user = {
  name: "Ada",
  [id1]: 12345,             // symbol key
};
console.log(user[id1]);      // 12345
console.log(Object.keys(user)); // ["name"] — symbol is invisible!
console.log(JSON.stringify(user)); // {"name":"Ada"}</pre>

<p>Symbols are used for metaprogramming
(<code>Symbol.iterator</code>, <code>Symbol.toStringTag</code>) and
adding "hidden" properties to objects that won't interfere with other
code.</p>
""",
                "tryit": """class Vector {
  static ZERO = new Vector(0, 0);
  static #instanceCount = 0;

  constructor(x, y) {
    this.x = x;
    this.y = y;
    Vector.#instanceCount++;
  }

  static get instanceCount() {
    return Vector.#instanceCount;
  }

  static add(a, b) {
    return new Vector(a.x + b.x, a.y + b.y);
  }

  toString() {
    return `Vector(${this.x}, ${this.y})`;
  }
}

const v1 = new Vector(1, 2);
const v2 = new Vector(3, 4);
const v3 = Vector.add(v1, v2);
console.log(v3.toString());        // "Vector(4, 6)"
console.log(Vector.instanceCount); // 3
console.log(Vector.ZERO.toString()); // "Vector(0, 0)"

// Symbols: unique keys
const SECRET = Symbol("secret");
const obj = { name: "app", [SECRET]: "hidden value" };
console.log(obj[SECRET]);         // "hidden value"
console.log(Object.keys(obj));   // ["name"] — symbol invisible!
""",
            },
            {
                "title": "Iterators & Generators",
                "html": """
<p><b>Iterators</b> are objects with a <code>next()</code> method that
returns <code>{ value, done }</code>. <b>Generators</b>
(<code>function*</code>) create iterators with the <code>yield</code>
keyword — they can pause and resume:</p>

<pre class="code">// generator: lazy, pausable sequence
function* countdown(from) {
  while (from &gt; 0) {
    yield from;     // pause here, return 'from'
    from--;
  }
}

const counter = countdown(3);
console.log(counter.next());  // { value: 3, done: false }
console.log(counter.next());  // { value: 2, done: false }
console.log(counter.next());  // { value: 1, done: false }
console.log(counter.next());  // { value: undefined, done: true }

// for...of consumes generators
for (const n of countdown(3)) {
  console.log(n);     // 3 2 1
}

// infinite generator (lazy — only computes when asked)
function* fibonacci() {
  let [a, b] = [0, 1];
  while (true) {
    yield a;
    [a, b] = [b, a + b];
  }
}

const fib = fibonacci();
console.log(fib.next().value);  // 0
console.log(fib.next().value);  // 1
console.log(fib.next().value);  // 1
console.log(fib.next().value);  // 2</pre>

<p>Generators are memory-efficient (lazy evaluation), can represent
infinite sequences, and enable custom iteration protocols. Any object
with a <code>[Symbol.iterator]</code> method is iterable and works with
<code>for...of</code>, spread, and destructuring.</p>
""",
                "tryit": """// generator for paginated data
function* pageGenerator(items, pageSize) {
  for (let i = 0; i < items.length; i += pageSize) {
    yield items.slice(i, i + pageSize);
  }
}

const data = ["a", "b", "c", "d", "e", "f", "g"];
const pages = pageGenerator(data, 3);

console.log(pages.next().value);  // ["a", "b", "c"]
console.log(pages.next().value);  // ["d", "e", "f"]
console.log(pages.next().value);  // ["g"]
console.log(pages.next().done);   // true

// generator with delegation (yield*)
function* innerGen() {
  yield 2;
  yield 3;
}

function* outerGen() {
  yield 1;
  yield* innerGen();  // delegate to another generator
  yield 4;
}

console.log([...outerGen()]);  // [1, 2, 3, 4]

// custom iterable object
const range = {
  from: 1, to: 5,
  *[Symbol.iterator]() {
    for (let i = this.from; i <= this.to; i++) yield i;
  },
};
console.log([...range]);  // [1, 2, 3, 4, 5]
""",
            },
        ],
        "quiz": [
            {
                "type": "mc",
                "question": "In an arrow function inside a method, 'this' refers to:",
                "options": ["The arrow function itself", "The global object", "The enclosing scope's this", "undefined"],
                "answer": 2,
                "explain": "Arrow functions inherit this from their enclosing lexical scope.",
            },
            {
                "type": "blank",
                "question": "Private class fields are prefixed with ____.",
                "answers": ["#", "hash"],
                "explain": "#balance is truly private — inaccessible from outside the class.",
            },
            {
                "type": "mc",
                "question": "A generator function is declared with:",
                "options": ["function gen()", "function* gen()", "async function gen()", "gen = () => yield"],
                "answer": 1,
                "explain": "function* marks a generator; yield pauses and resumes execution.",
            },
            {
                "type": "mc",
                "question": "Static members belong to:",
                "options": ["Each instance", "The class itself", "The prototype", "The module"],
                "answer": 1,
                "explain": "Static members are called on the class: MathHelper.clamp(...)",
            },
        ],
    },
]
