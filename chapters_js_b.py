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
<p>Copy-pasting the same five lines three times is how programs rot:
you fix a bug in one copy and forget the other two. <b>Functions</b>
solve this — they package behavior behind a name so you write it once
and call it anywhere. They are also <b>first-class citizens</b> in JS,
meaning a function is a value like a number or a string: you can
store it in a variable, pass it to another function, and return it
from one. That single idea powers callbacks, array methods, and the
entire async chapter later on.</p>

<p>Walk the block. The declaration <code>function greet(name)</code>
defines a function with one <b>parameter</b>, <code>name</code> — a
placeholder. Calling <code>greet("Ada")</code> passes the
<b>argument</b> "Ada": the placeholder becomes the real value, the
body runs, and <code>return</code> hands "Hello, Ada!" back to the
caller, where <code>console.log</code> prints it.
<code>add(2, 3)</code> shows two parameters working the same way —
predict the printed result before reading the comment.</p>

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

<p>Keep the parameter/argument vocabulary straight: parameters are the
named slots in the definition; arguments are the actual values in
the call. And JS is loose about counts — missing arguments arrive as
<code>undefined</code>, extra arguments are ignored (but still
reachable via rest parameters, later in this chapter). That
looseness is convenient, but it pushes validation onto you.</p>

<p><b>Gotcha:</b> defining a function does nothing visible — there is
no output until you call it. Beginners write a perfect function, run
the file, see nothing, and panic. A function is a recipe; you still
have to cook. If your code "does nothing", first check whether you
actually called it.</p>
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
<p>Printing is not the same as computing. A function that only
<code>console.log</code>s hands its result to the console and to
nobody else — you cannot add it, store it, or test it.
<code>return</code> is what makes a function reusable: it sends a
value back to wherever the function was called, and it exits the
function immediately.</p>

<p>Read the first block. In <code>add</code>, <code>return a +
b;</code> computes 3 and sends it back, so
<code>console.log(add(1, 2))</code> prints 3. The line below it —
<code>console.log("never runs")</code> — is dead code: <code>return</code>
already left the function. That "return exits immediately" fact is a
feature: the early-return pattern checks bad input first and bails
out before doing any real work. The try-it's <code>classify</code>
does exactly this, three times in a row.</p>

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

<p>What about a function with no return at all, like <code>log</code>
in the block? It still returns something: <code>undefined</code>.
Predict the output of <code>console.log(log("hi"))</code> before
running — you will see "hi" first (the function logs while it
runs), then undefined (its return value).</p>

<pre class="code">function getStats(numbers) {
  return { min: Math.min(...numbers), max: Math.max(...numbers) };
}
const { min, max } = getStats([3, 1, 4, 1, 5]);
console.log(min, max);   // 1 5</pre>

<p>One return value per function feels limiting until you remember
objects: the second block returns <code>{ min, max }</code> in a
single object, and the caller destructures both into variables on
one line. Returning an object or array is the standard way to hand
back multiple results.</p>

<p><b>Gotcha:</b> JS inserts a semicolon after a <code>return</code>
that ends its line — writing <code>return</code> on one line and the
value on the next makes the function silently return
<code>undefined</code>. Always keep <code>return value;</code> on a
single line.</p>
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
<p>So far every function had a name in its declaration. But functions
are values, so they can also appear inside expressions — assigned to
variables, passed around. That opens the door to <b>arrow
functions</b>, the compact modern syntax you will see in virtually
every contemporary codebase.</p>

<p>Read the block as an evolution. The function expression
<code>const double = function(n) {...}</code> proves a function can
be a value. The arrow version <code>(n) =&gt; n * 2</code> says the
same thing with less ceremony. Then the shortcuts kick in: one
parameter lets you drop the parentheses (<code>n =&gt; n * 3</code>);
a body that is a single expression lets you drop both the braces and
the word <code>return</code> — the expression's value is returned
implicitly. Multiple parameters require parens; no parameters use
empty ones <code>()</code>.</p>

<p>Predict what <code>double2(5)</code> and <code>hello()</code> each
give before moving on — 10 and "hello!".</p>

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

<p>Two rules close the gallery. A multi-line body needs braces — and
braces bring back the explicit <code>return</code>; forgetting it
makes the function return <code>undefined</code>, a classic bug. And
returning an object literal directly requires parentheses around it:
<code>() =&gt; ({ first: a })</code> — a bare <code>{</code> would be
read as the start of a function body.</p>

<p>The deeper difference is <code>this</code>: arrow functions have no
<code>this</code> of their own — they inherit it from the surrounding
scope, which makes them ideal inside methods and callbacks. The
"this" lesson in the Advanced chapter demonstrates it fully.</p>

<p><b>Gotcha:</b> arrows are for expressions and callbacks, not for
every function you write: <code>function greet() {}</code> is hoisted
and callable before its line, while a <code>const</code> arrow is
not — order of execution matters with arrows.</p>
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
<p>Two small features remove enormous amounts of boilerplate:
defaults handle "the caller did not provide this", and rest handles
"the caller provided an unknown amount". Both make functions
flexible without <code>if</code>-checks cluttering the top of the
body.</p>

<p>A default parameter names a fallback used only when the argument is
<code>undefined</code>. In the first block, <code>greet()</code> with
no arguments uses both defaults and prints "Hello, guest!";
<code>greet("Ada")</code> fills the first slot and keeps the second
default; <code>greet("Ada", "Hi")</code> overrides both. Note the
trigger is specifically <code>undefined</code> — passing
<code>null</code> or <code>""</code> counts as a real value and
skips the default.</p>

<pre class="code">function greet(name = "guest", greeting = "Hello") {
  return `${greeting}, ${name}!`;
}
console.log(greet());           // "Hello, guest!"
console.log(greet("Ada"));     // "Hello, Ada!"
console.log(greet("Ada", "Hi")); // "Hi, Ada!"</pre>

<p>Rest parameters (<code>...name</code>) collect all remaining
arguments into a genuine array. <code>sum(...numbers)</code> accepts
2, 5 or a hundred arguments; inside the function,
<code>numbers</code> is a real array, so <code>reduce</code> works
on it directly — the second block sums 1+2 to 3, then 1 through 5 to
15. The mixed form shows the ordering rule: named parameters first,
rest last, so <code>introduce("Hi", "Ada", "Grace")</code> peels
"Hi" off as the greeting and gathers the rest into
<code>names</code>.</p>

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

<p><b>Gotchas:</b> rest must be the last parameter —
<code>function f(...nums, last)</code> is a syntax error. And prefer
rest over the legacy <code>arguments</code> object:
<code>arguments</code> is array-<i>like</i> but has no
<code>map</code>, <code>filter</code> or friends — a difference that
bites the first time you call a method on it. One more habit:
calling <code>sum()</code> with no arguments gives an empty array —
check for it, as the try-it's <code>average</code> does, or
<code>reduce</code> will throw on an empty list without an initial
value.</p>
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
<p>Spread (<code>...</code>) is the mirror image of rest: where rest
<i>collects</i> many values into an array, spread <i>unpacks</i> an
array into many individual values. Same three dots, opposite
directions — the context decides which one you are writing.</p>

<p>The killer use case is in the first lines: <code>Math.max</code>
accepts numbers, not arrays, so <code>Math.max([3, 1, 4])</code> is
useless, but <code>Math.max(...nums)</code> becomes
<code>Math.max(3, 1, 4)</code> and returns 4. Predict that before
reading the comment — this one-liner is the most common spread
pattern you will meet.</p>

<p>The other three patterns appear everywhere in modern code.
<code>[...nums]</code> copies an array — a new array you can sort or
reverse without touching the original. <code>[...a, ...b]</code>
merges arrays, and you can slip new elements in between.
Spreading an object (<code>{ ...defaults, theme: "dark" }</code>)
builds a new object from an old one with selected overrides — the
standard pattern for "start from defaults, apply user settings".
Watch the order: later properties win, so <code>theme</code> ends up
"dark" while <code>lang</code> survives from the defaults.</p>

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

<p>Spread also works on strings: <code>[..."abc"]</code> gives
<code>["a", "b", "c"]</code>, because strings are iterable — the
try-it demonstrates.</p>

<p><b>Gotcha — the big one:</b> spread makes a <b>shallow</b> copy.
The top level is new, but nested objects are still <i>shared
references</i>. In the try-it, copying <code>nested</code> and
editing <code>copy.inner.val</code> changes the original too —
predict that, then run it and watch. When you need a fully
independent copy, use <code>structuredClone()</code>.</p>
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
<p>Where can a variable be seen from? That question is <b>scope</b>.
JS has global scope (everywhere), function scope (inside a
function), and block scope — the <code>{ }</code> territory that
<code>let</code>/<code>const</code> respect. The lookup rule: when
code reads a name, JS checks the innermost scope first, then walks
outward. That is why <code>inner</code> in the first block can read
<code>outerVar</code> and <code>global</code> — the search goes
inside-out, never the other way. Code outside cannot see in.</p>

<pre class="code">const global = "everywhere";

function outer() {
  const outerVar = "visible in outer";
  function inner() {
    console.log(global);    // ✓ can see global
    console.log(outerVar);  // ✓ can see outer's variable
  }
  inner();
}</pre>

<p>Now the payoff of that machinery: a <b>closure</b>. When a function
is created, it keeps a live link to the variables of the scope it
was born in — even after that scope has finished running. The second
block builds one: <code>makeCounter</code> declares
<code>count</code>, then returns a small function that increments
it. After <code>makeCounter()</code> finishes, <code>count</code>
should be gone... but it is not. The returned function holds the
link, so <code>counter()</code> prints 1, 2, 3 across separate
calls. Calling <code>makeCounter()</code> again builds a
<i>fresh</i> count, so <code>counter2()</code> starts at 1.</p>

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

<p>Read those consequences carefully: <code>count</code> is
effectively <b>private</b> — nothing outside can touch it except
through the returned function. This is how JS does data privacy and
factory functions, and it is why every callback that mentions an
outer variable works at all. The try-it builds a wallet whose
<code>balance</code> cannot be reached except through deposit and
withdraw.</p>

<p><b>Gotcha:</b> a closure captures the <i>variable</i>, not a
snapshot of its value — if the variable changes later, the closure
sees the new value. The <code>let</code>-in-a-loop example at the
bottom of the try-it shows the one case where each iteration gets a
fresh variable instead of a shared one.</p>
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
<p>How does code react to things it cannot predict — a click, a
timer, data arriving from a server? It hands over a <b>callback</b>:
a function passed as an argument to another function, to be called
when the moment comes. This is the single most important pattern in
browser JS — event handling, array methods and all async code are
built on it.</p>

<p>The block shows three flavors. Array methods call their callback
once per element, synchronously: <code>nums.map(n =&gt; n * 2)</code>
runs the arrow on each item and collects the results into
<code>[2, 4, 6]</code>. <code>setTimeout</code> schedules its
callback for about 1000 ms later and moves on immediately, which
makes it asynchronous — the surrounding code does not wait. The
third example is the pattern in its purest form: <code>process</code>
accepts two callbacks and calls exactly one, depending on the data —
the success path or the error path.</p>

<p>Because functions are values (previous lesson), passing them costs
nothing special — you are literally handing an object to another
function. When the callee decides <i>when</i> and <i>how many
times</i> to call back, you get flexible, decoupled code:
<code>process</code> knows nothing about logging or retrying; its
callers decide.</p>

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

<p><b>Gotchas:</b> nesting callbacks for sequential async steps
("get data, then use it to get more data...") piles indentation
into what veterans call <b>callback hell</b> — hard to read and
harder to error-handle; Promises and async/await are the cure,
covered in the async chapter. And remember: an error thrown inside a
timer's callback cannot be caught by a try/catch sitting outside the
call — the error must be handled inside the callback itself.</p>
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
<p>A shopping list, a set of open tabs, a player's inventory —
programs are full of collections. The <b>array</b> is JS's core one:
an ordered, zero-indexed list that can grow and shrink at runtime and
hold any mix of types. If you learn one data structure well, make it
this one.</p>

<p>Indexing starts at 0, so in the block <code>fruits[0]</code> is
"apple", and the <i>last</i> item sits at <code>length - 1</code> —
an idiom worth memorizing. Predict each line's result as you read:
length is 3, first is "apple", last is "cherry".</p>

<p>The four workhorse methods add and remove at the ends:
<code>push</code> appends to the end and returns the new length,
<code>pop</code> removes from the end and returns the removed item,
and <code>unshift</code>/<code>shift</code> do the same pair at the
front. Then come the searchers: <code>indexOf</code> gives the
position (or -1 if missing), <code>includes</code> gives a clean
true/false. Note the last two lines: <code>slice(1, 3)</code> copies
a section <i>without</i> touching the original, while
<code>join(", ")</code> glues the array into a single string.</p>

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

<p><b>Gotchas:</b> <code>fruits[10]</code> on a 3-item array is not
an error — it is politely <code>undefined</code>, which then poisons
whatever math you do next. And keep straight which methods mutate:
<code>push</code>, <code>pop</code>, <code>shift</code>,
<code>unshift</code> change the array; <code>slice</code>,
<code>indexOf</code>, <code>includes</code>, <code>join</code> do
not. When a method surprises you by changing your data, check this
list first. (Also: <code>typeof []</code> says "object" — test for
arrays with <code>Array.isArray()</code>.)</p>
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
<p>Loop-plus-push is the beginner's reflex for transforming a list —
it works, but it buries the intent under bookkeeping. The functional
trio <code>map</code>, <code>filter</code>, <code>reduce</code>
states the <i>intent</i> directly and never mutates the original.
They are the most-used methods in modern JS, so this lesson is worth
extra practice time.</p>

<p>Read the block as three questions. <code>map</code> asks "what
should each element become?" — it calls your arrow once per element
and collects the returns into a <i>new</i> array:
<code>[1,2,3,4,5]</code> becomes <code>[2,4,6,8,10]</code>.
<code>filter</code> asks "which elements survive?" — it keeps those
where the arrow returns true: the evens <code>[2, 4]</code>.
<code>reduce</code> asks "what single value does the whole array boil
down to?" — it carries an accumulator from element to element; here
the accumulator starts at 0 and eats each number, ending at 15.</p>

<p>The helpers cover the smaller questions: <code>find</code> returns
the first matching element (4) or undefined; <code>some</code> is
true if at least one element passes; <code>every</code> demands all
of them. Then the trap: <code>sort()</code> <b>mutates</b> the
original array — the spread copy <code>[...nums].sort(...)</code> in
the block is the defensive idiom that avoids it.</p>

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

<p>The superpower is chaining, because each method returns an array:
<code>nums.filter(...).map(...).reduce(...)</code> reads like a
pipeline of transformations. The try-it runs a realistic chain over
product objects — filter to in-stock items, map to names, join into
a printable string.</p>

<p><b>Gotcha:</b> always pass the initial value to
<code>reduce</code> — on an empty array, <code>reduce</code> without
one throws. And a multi-line arrow body (with braces) needs an
explicit <code>return</code>; forgetting it makes <code>map</code>
silently produce an array of <code>undefined</code>s.</p>
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
<p>Objects and arrays bundle values together — but half your code
exists to un-bundle them into single variables. <b>Destructuring</b>
is the syntax for that: it pulls values out of arrays and objects
straight into variables in one line, replacing three or four lines
of <code>const x = obj.x</code> bookkeeping.</p>

<p>Array destructuring matches by position: <code>const [first,
second] = [1, 2, 3]</code> gives first=1 and second=2, ignoring the
rest. The extras are what make it shine: an empty slot skips a
position, <code>= default</code> covers missing values, and the swap
trick <code>[x, y] = [y, x]</code> exchanges two variables with no
temporary. Object destructuring matches by <i>name</i>:
<code>const { name, age } = user</code> grabs the properties with
those exact keys. Renaming is <code>{ name: fullName }</code> — read
it as "extract name, call it fullName". Nesting works to any depth:
the last line of the block pulls <code>host</code> and
<code>port</code> out of the inner <code>db</code> object.</p>

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

<p>The second block shows the pattern you will meet in every modern
library: destructuring in the parameter list. <code>connect({
port: 8080 })</code> — the signature documents exactly which options
the function wants, and each can carry its own default. Callers
pass a plain options object; predict the printed result
("localhost:8080") before running.</p>

<pre class="code">function connect({ host = "localhost", port = 3000 }) {
  console.log(`${host}:${port}`);
}
connect({ port: 8080 });   // "localhost:8080"</pre>

<p><b>Gotchas:</b> destructuring <code>null</code> or
<code>undefined</code> throws — guard a possibly-missing object with
<code>const { name } = maybeUser || {}</code>. And read the array
syntax carefully: in <code>const [, third]</code> the bare comma is
the skipped slot — it looks strange until you parse it as "skip one,
take the next".</p>
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
<p>Arrays are for ordered lists; <b>objects</b> are for things with
named attributes: a user with a name and age, a book with a title
and author. An object is a set of key–value pairs — the fundamental
structure of JS, and the shape of almost every piece of data the web
sends you.</p>

<p>Walk the block. Properties are written <code>key: value</code>
inside <code>{ }</code>; a function stored as a property is a
<b>method</b>, and the shorthand <code>greet() { ... }</code> is how
you will usually write them. Notice <code>"has-pets": true</code> —
keys that are not valid identifiers need quotes, and reading them
needs brackets. That is the general access rule: dot for normal keys
(<code>user.name</code>), brackets when the key sits in a variable
or contains odd characters (<code>user[key]</code>,
<code>user["has-pets"]</code>).</p>

<p>Objects stay open for business after creation: the block adds
<code>email</code> with plain assignment, updates <code>age</code>,
and deletes <code>email</code> with <code>delete</code>. Existence
checks come in two flavors — <code>"name" in user</code> tests any
key, and <code>user.email?.length</code> reads a property that might
be gone without crashing.</p>

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

<p>Then <code>this</code>: inside a method, it refers to the object
the method was called on — <code>this.name</code> in
<code>greet</code> is whatever object stood before the dot. That
single rule makes one method definition work for many objects, and
it is the foundation constructor functions and classes build on
later.</p>

<p><b>Gotcha:</b> reading a missing property is harmless —
<code>user.email</code> is just <code>undefined</code> — but chaining
off it crashes: <code>user.email.length</code> throws a TypeError.
This is exactly the problem optional chaining (next lesson)
fixes.</p>
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
<p>Real-world data is full of holes: a user has no profile, a profile
has no social links. Two modern operators — both from 2020 — turn
the resulting pyramid of null-checks into one clean line, and you
should reach for them daily.</p>

<p>Optional chaining <code>?.</code> short-circuits a property chain
the moment something is null/undefined, yielding
<code>undefined</code> instead of throwing. The old way checks every
level by hand (<code>user &amp;&amp; user.profile &amp;&amp;
user.profile.email</code>); the new way is
<code>user?.profile?.email</code>. It also works for methods
(<code>data?.find?.(...)</code>) and indexes (<code>list?.[0]</code>)
— see the end of the block. Predict what the "after" line prints
when <code>user</code> is null: undefined, no crash.</p>

<pre class="code">// before: the pyramid of doom
if (user &amp;&amp; user.profile &amp;&amp; user.profile.email) {
  console.log(user.profile.email);
}

// after: one line
console.log(user?.profile?.email);   // undefined, no crash!

// also works with methods and array access
const result = data?.find?.(x =&gt; x.id === 1);
const first = list?.[0];</pre>

<p>Nullish coalescing <code>??</code> supplies a default <i>only</i>
for null/undefined. That precision is the whole point: in the second
block, <code>volume</code> is 0 — a real, meaningful value.
<code>volume || 50</code> wrongly replaces it with 50 because 0 is
falsy; <code>volume ?? 50</code> correctly keeps 0. When a
legitimate value can be 0, <code>""</code> or <code>false</code>,
choosing <code>??</code> is not a style preference — it is the
difference between right and wrong.</p>

<pre class="code">const volume = 0;
volume || 50    // 50 (0 is falsy — WRONG!)
volume ?? 50    // 0  (0 is not nullish — correct!)

const name = null;
name ?? "Anonymous"   // "Anonymous"</pre>

<p>They compose: <code>user?.settings?.volume ?? 50</code> reads as
"get the volume if the whole path exists, otherwise 50". The try-it
loops over users with differently-shaped profiles — watch each line
degrade gracefully from a real value down to the default.</p>

<p><b>Gotcha:</b> <code>?.</code> does not guard the <i>final</i>
property — in <code>user.profile?.email</code>, a null
<code>user</code> still throws; every link in the chain needs its own
<code>?.</code>. And do not blanket-replace every <code>||</code>
with <code>??</code> mechanically — sometimes "treat 0 as missing"
really is what you want. Choose per case, and know why.</p>
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
<p><code>this</code> is the JS concept that generates the most
confusion — and the confusion evaporates once you learn the one
rule: <b>this is decided by how a function is called, not where it
is written</b>. It is a runtime question ("who invoked me?"), not a
property of the code's location.</p>

<p>Walk the first block. <code>user.greet()</code> calls the function
<i>as a method</i>, with <code>user</code> before the dot, so
<code>this</code> is <code>user</code> and the log prints "Hi, Ada".
The next two lines copy that same function into a variable and call
it bare. Now nothing stands before the dot, so <code>this</code> is
undefined in strict mode — "Hi, undefined". Same function, different
call, different this. Predict both outputs before reading the
comments.</p>

<pre class="code">const user = {
  name: "Ada",
  greet() { console.log(`Hi, ${this.name}`); },
};
user.greet();        // "Hi, Ada" — this = user

// the same function, different context!
const greeting = user.greet;
greeting();          // "Hi, undefined" — this = global/undefined</pre>

<p>The full call-site checklist: method call <code>obj.fn()</code> →
this is obj. Standalone <code>fn()</code> → undefined (strict) or
the global object. <code>new</code> → the freshly created object.
<code>call/apply/bind</code> → whatever you pass explicitly. And
arrow functions: no own <code>this</code> at all — they inherit the
enclosing one, which is often exactly what you want.</p>

<p>The second block fixes the classic bug: a regular function used as
a callback gets its own useless <code>this</code>; an arrow inherits
the method's. In the timer, <code>setInterval(() =&gt; {...})</code>
— the arrow means <code>this.seconds</code> still points at
<code>timer</code>. Swap the arrow for <code>function() {...}</code>
and the code breaks.</p>

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

<p><b>Gotcha:</b> extracting a method into a variable
(<code>const g = user.greet; g();</code>) silently disconnects it
from its object — this sits behind most "works alone, fails in a
callback" stories. Use an arrow, or reattach the object with
<code>bind</code>.</p>
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
<p>Where do methods really live? When you call <code>array.map()</code>,
your array has no <code>map</code> inside it — so how does it work?
The answer is <b>prototypes</b>, JS's inheritance mechanism: every
object has a hidden link to a prototype object, and property lookups
climb that link whenever the property is not found directly.</p>

<p>The block builds a chain by hand. <code>Object.create(animal)</code>
makes a new object whose prototype is <code>animal</code>, then
<code>dog.bark</code> is added as an <i>own</i> property. Now walk
the lookup for <code>dog.eat()</code>: check <code>dog</code> itself
— no <code>eat</code>; follow the hidden link to <code>animal</code>
— found, call it. For <code>dog.bark()</code> the very first check
succeeds. That is the entire mechanism: own first, then prototype,
then the prototype's prototype, until <code>null</code> ends the
chain: <code>dog → animal → Object.prototype → null</code>.</p>

<p>Predict before reading the comments: both calls succeed — "woof!"
from the object itself, "eating..." inherited from the
prototype.</p>

<pre class="code">const animal = {
  eat() { return "eating..."; },
};

const dog = Object.create(animal);  // dog's prototype = animal
dog.bark = () =&gt; "woof!";

dog.bark();   // "woof!" — own property
dog.eat();    // "eating..." — found on prototype!

// the chain: dog → animal → Object.prototype → null</pre>

<p>This explains the standard library too: <code>map</code>,
<code>filter</code> and <code>push</code> live on
<code>Array.prototype</code>, and every array links to it — one copy
of each method shared by millions of arrays, not millions of
copies. Strings, numbers and plain objects work the same way, which
is why <code>"abc".toUpperCase()</code> needs no import and no
setup.</p>

<p><b>Gotcha:</b> mutating built-in prototypes
(<code>Array.prototype.foo = ...</code>) technically works and is
widely considered harmful — your "feature" silently leaks into every
script on the page. Read the chain with
<code>Object.getPrototypeOf()</code>, do not rewrite it; for shared
behavior, classes (two lessons ahead) are the supported tool.</p>
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
<p>Before ES6 classes existed, the way to stamp out many objects with
shared behavior was the <b>constructor function</b> — a normal
function called with <code>new</code>. You will still meet them in
older codebases and tutorials, and they show exactly what classes do
under the hood, which is why this lesson exists.</p>

<p>Read the block with the <code>new</code> mechanics in mind — it
performs four steps: create an empty object, link its prototype to
<code>Person.prototype</code>, call the function with
<code>this</code> set to that object, and return it. So
<code>this.name = name</code> inside the function writes onto the
fresh object, and <code>new Person("Ada", 36)</code> hands it back.
Both <code>ada</code> and <code>grace</code> get their own
name/age copies.</p>

<p>Now the crucial design detail: methods go on
<code>Person.prototype</code>, not inside the function. Why? Predict
what <code>ada.greet === grace.greet</code> prints — it is
<code>true</code>. Both instances share the <i>one</i> function via
the prototype chain from the previous lesson. If instead you wrote
<code>this.greet = function() {...}</code> inside the constructor,
every person would carry a separate copy — slower and
memory-hungrier for no benefit.</p>

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

<p><code>instanceof</code> answers "was this object built by
Person?" — true for <code>ada</code>. And the naming convention —
constructor functions start with a capital letter — exists purely to
remind you to call them with <code>new</code>.</p>

<p><b>Gotcha:</b> calling a constructor <i>without</i>
<code>new</code> does not fail loudly: <code>this</code> becomes the
global object and the properties leak onto it — a nasty legacy bug.
Modern classes (next lesson) throw in that situation, which is one
more reason to prefer them.</p>
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
<p>The constructor-plus-prototype dance works, but it scatters one
object's definition across several places and lets you forget
<code>new</code>. <b>Classes</b> (ES6, 2015) gather everything into
one clean block — they are syntactic sugar over the same prototypes,
but the sugar prevents real bugs.</p>

<p>Walk the block. <code>constructor(name, sound)</code> runs
automatically on <code>new</code> — it is the same "set up this"
step as before, now labeled. Methods like <code>speak()</code> are
written directly in the class body; behind the scenes they still
land on <code>Animal.prototype</code>, shared by all instances. The
<code>static</code> keyword is new: <code>compare</code> belongs to
the class itself, called as <code>Animal.compare(a, b)</code>, not
on instances — useful for utilities that need no specific
object.</p>

<p>Predict the two console lines before running: "Whiskers says
meow", then the result of comparing two names with
localeCompare.</p>

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

<p>What the syntax buys you: calling a class without
<code>new</code> is now a hard error (old constructors silently
corrupted global state); the method syntax is terser; and the door
opens to <code>extends</code>, <code>super</code>, static members
and <code>#private</code> fields — the next lessons. The try-it
builds a bank account with a private <code>#balance</code> and
shows <code>return this</code> enabling chaining:
<code>acct1.deposit(50).withdraw(30)</code>.</p>

<p><b>Gotcha:</b> class declarations are <i>not</i> hoisted the way
function declarations are — using a class before its definition line
throws a ReferenceError. Also, everything inside a class body is
automatically strict mode, which can surface errors that sloppy-mode
code never showed.</p>
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
<p>Copy-pasting methods across similar classes — Dog and Cat both
needing <code>eat()</code>, Circle and Rectangle both needing
<code>describe()</code> — is where <b>inheritance</b> comes in. A
child class <code>extends</code> a parent: it inherits all methods
for free, then adds or overrides only what makes it different. That
is how class hierarchies stay small and readable.</p>

<p>Walk the block. <code>class Dog extends Animal</code> means every
Dog instance can call <code>eat()</code> and <code>describe()</code>
with zero re-declaration. Inside Dog's constructor,
<code>super(name)</code> calls the parent's constructor to set up
<code>this.name</code> — and it is <b>required</b>: in a subclass
constructor you must call <code>super()</code> before touching
<code>this</code>, or JS throws a ReferenceError. The logic is
fair: the parent initializes the shared part before the child adds
its own (<code>breed</code>).</p>

<p>Overriding is the second half of the story: Dog defines its own
<code>describe()</code>, replacing Animal's version. But look inside
— <code>super.describe()</code> calls the <i>parent's</i> version
and extends its result. That "extend, don't duplicate" pattern is
the idiomatic override. Predict the output of
<code>dog.describe()</code>: "Rex is an animal — specifically a
Golden Retriever".</p>

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

<p>Under the hood this is the prototype chain again, now built for
you: <code>dog → Dog.prototype → Animal.prototype →
Object.prototype</code>. Method lookup walks it exactly as the
earlier prototype lesson described.</p>

<p><b>Gotchas:</b> forgetting <code>super()</code> in a child
constructor is the number-one inheritance error — the error message
mentions "super" explicitly, so read it. And keep hierarchies
shallow: three levels are usually fine, five usually means the
design wants composition instead of inheritance.</p>
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
<p>Two upgrades make classes feel like well-designed data types
instead of bags of fields. <b>Getters and setters</b> let a property
run code on access — so <code>temp.fahrenheit</code> can be computed
on the fly, and every assignment can be validated. <b>Private
fields</b> (the <code>#</code> prefix) make internal state genuinely
invisible, so nobody can bypass your validation.</p>

<p>Walk the block. <code>#celsius</code> is the real storage — note
that the <code>#</code> appears everywhere the field is used; it is
part of the name, not decoration. The getter <code>get
celsius()</code> runs whenever you read <code>temp.celsius</code>;
the setter <code>set celsius(value)</code> runs whenever you
<i>assign</i> to it — and it validates, throwing below absolute
zero. Assignment syntax triggering validation is the whole point:
callers write plain property code while the object stays in charge.
<code>fahrenheit</code> is a <i>computed</i> pair: reading it
converts, writing it converts back — no storage needed.</p>

<p>Predict the output of <code>temp.celsius = 25;
console.log(temp.fahrenheit)</code>: the setter stores 25, the
getter computes 25 × 9 / 5 + 32 = 77.</p>

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

<p>The <code>#</code> fields are enforced by the language itself:
<code>temp.#celsius</code> from outside is a SyntaxError — not a
convention like the old underscore <code>_private</code>, which any
code could ignore. Private fields also vanish from
<code>JSON.stringify</code> and <code>for...in</code>, keeping
internals out of serialized data. The try-it's store exposes its
access log through a getter that returns a <i>copy</i> — read-only
by design.</p>

<p><b>Gotcha:</b> a setter that throws turns <code>obj.x = bad</code>
from "silently accepted" into "crash at the assignment line" — that
is the feature, but it means every call site can now throw. Validate
deliberately, and document what the property accepts.</p>
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
<p>Not everything belongs to an instance. Conversion helpers, shared
constants, counters — these belong to the <b>class itself</b>.
<code>static</code> members are accessed on the class
(<code>MathHelper.clamp(...)</code>), never through instances, and
inside a static method <code>this</code> is the class, not an
object. You have already used statics on the built-ins:
<code>Array.from()</code>, <code>Object.keys()</code> and
<code>Number.isInteger()</code> all work this way.</p>

<p>Walk the first block: a static constant <code>PI</code>, a static
method that reads it via <code>this.PI</code>, and a pure utility
<code>clamp</code>. Predict the three outputs before reading the
comments: 3.14159, then 12.57 (the area of a circle with radius 2),
then 10 (15 clamped to the maximum).</p>

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

<p><b>Symbols</b> solve a different problem: unique keys. Every
<code>Symbol("id")</code> call creates a brand-new value — two
symbols with identical descriptions are still different (the block
proves it: <code>id1 === id2</code> is false). Used as object keys,
symbol properties are <i>hidden</i> from <code>for...in</code>,
<code>Object.keys()</code> and <code>JSON.stringify</code> — see the
second block, where <code>user</code> prints only "name" while
<code>user[id1]</code> still works. That makes symbols the tool for
attaching metadata that must not collide with, or leak into, normal
data.</p>

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

<p>You have already met the metaprogramming side: well-known symbols
like <code>Symbol.iterator</code> tell the language how your objects
behave — the generators lesson closes that loop with a custom
iterable in its try-it.</p>

<p><b>Gotcha:</b> symbols are <i>not</i> private fields — anyone
holding the symbol can read the property. When you need true
encapsulation, use <code>#fields</code>; reach for symbols when the
goal is uniqueness and non-collision.</p>
""",
                "tryit": """class Vector {
  static #instanceCount = 0;      // must be declared BEFORE ZERO below —
                                  // static fields initialize in text order
  static ZERO = new Vector(0, 0);

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
<p>Why does <code>for...of</code> work on arrays and strings? Because
they implement a protocol: the object exposes a method (keyed by
<code>Symbol.iterator</code>) that returns an <b>iterator</b> — an
object whose <code>next()</code> hands back <code>{ value, done
}</code>, one step at a time. Writing that by hand is tedious, so JS
added <b>generators</b>: functions declared with
<code>function*</code> that build iterators using <code>yield</code>
to pause and resume.</p>

<p>Walk the block. Calling <code>countdown(3)</code> does not run the
body — it returns a paused iterator. Each <code>.next()</code> runs
the body until the next <code>yield</code>, returns that value with
<code>done: false</code>, and freezes everything until the next
call. Predict the four outputs before reading the comments: 3, 2,
1, then <code>{ value: undefined, done: true }</code> when the body
finishes. The <code>for...of</code> lines show that the loop is just
<code>next()</code> behind the scenes — it stops at
<code>done: true</code>.</p>

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

<p>The second generator, <code>fibonacci()</code>, shows why this
matters: it is an <i>infinite</i> sequence, and that is fine —
generators are lazy, computing one value only when asked. No array
of a million numbers is ever built. Pull a few <code>next()</code>s
and you get 0, 1, 1, 2.</p>

<p>Where you will actually use this: paginating a long list without
slicing it all at once (the try-it's <code>pageGenerator</code>),
custom iterables via <code>*[Symbol.iterator]()</code>, and — in the
async chapter — async generators for streams of data.</p>

<p><b>Gotcha:</b> generators are one-shot — a finished iterator
cannot be restarted; call the generator function again for a fresh
run. And <code>yield</code> is illegal in regular functions and in
arrow functions: the star and the pause are a package deal.</p>
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
