"""JS Tutor chapters 1-2 (Phases 1-2), grounded in MDN Web Docs.

All 120 roadmap topics are covered — closely related items (e.g. break +
continue) are grouped into focused lessons.
"""

CHAPTERS_JS_A = [
    # ------------------------------------------------------------------ js01
    {
        "id": "js01",
        "title": "Fundamentals",
        "emoji": "🟡",
        "lessons": [
            {
                "title": "What is JavaScript?",
                "html": """
<p><b>JavaScript</b> is a lightweight, interpreted (or JIT-compiled)
programming language with <b>first-class functions</b>. MDN describes it
as prototype-based, garbage-collected, and dynamically typed — supporting
imperative, functional and object-oriented paradigms. Despite the name,
it has nothing to do with Java.</p>

<p>The three core web technologies, per MDN:</p>

<ul>
<li><b>HTML</b> — structure and meaning</li>
<li><b>CSS</b> — presentation and layout</li>
<li><b>JavaScript</b> — <i>interactivity and dynamic behaviour</i></li>
</ul>

<p>JS runs in browsers (making pages interactive) and outside them too
(Node.js for servers, tools, and more). It's standardized as
<b>ECMAScript</b> (ECMA-262), with new features added every year.</p>

<p>This course runs your code in the browser's own engine — the same
V8/SpiderMonkey that powers real websites. Press Run and see the
console output.</p>
""",
                "tryit": """// Welcome to the JS Tutor! 🟡
// Everything after // is a comment — the browser ignores it.

console.log("Hello, JavaScript!");

// Variables hold values
const name = "Ada";
let year = 2026;

// Template literals embed values with ${}
console.log(`Hello, ${name}! Welcome to ${year}.`);

// Math works as expected
console.log("2 + 3 =", 2 + 3);
""",
            },
            {
                "title": "Syntax & Comments",
                "html": """
<p>JS statements end with a semicolon (optional but recommended),
blocks wrap in curly braces, and comments come in two flavours:</p>

<pre class="code">// single-line comment

/* multi-line
   comment */</pre>

<p>JavaScript is <b>case-sensitive</b>: <code>myVar</code> and
<code>myvar</code> are different variables. Statements execute top to
bottom unless control flow redirects them. Whitespace is mostly
insignificant — but consistent indentation makes code readable.</p>

<p>MDN's strict mode (<code>"use strict"</code>) opts into stricter
parsing: it catches silent errors like assigning to undeclared
variables. Modern modules and classes are always in strict mode — you
rarely need to type it manually anymore.</p>
""",
                "tryit": """// Case-sensitive!
let greeting = "hello";
let Greeting = "HELLO";
console.log(greeting, Greeting);   // different variables!

// Semicolons separate statements
let a = 1; let b = 2;
console.log(a + b);

/* Multi-line comment:
   this whole block is ignored */
console.log("done");
""",
            },
            {
                "title": "Variables: let, const, var",
                "html": """
<p>Three keywords declare variables — and the differences matter:</p>

<pre class="code">const PI = 3.14159;    // cannot be reassigned
let count = 0;          // can be reassigned, block-scoped
var old = "legacy";     // function-scoped, hoisted — avoid in new code</pre>

<ul>
<li><b><code>const</code></b> — the default choice. The binding can't be
reassigned (though objects/arrays assigned to const can still be
<i>mutated</i>)</li>
<li><b><code>let</code></b> — when you know the value will change
(counters, accumulators)</li>
<li><b><code>var</code></b> — the legacy keyword; function-scoped and
hoisted (accessible before its line!), which causes subtle bugs. Modern
code uses let/const exclusively</li>
</ul>

<pre class="code">const user = { name: "Ada" };
user.name = "Grace";     // ✓ mutation is fine — same object
// user = {};            // ✗ TypeError: assignment to constant</pre>

<p>Block scoping: <code>let</code>/<code>const</code> only exist inside
their <code>{ }</code> block; <code>var</code> leaks to the function
level. This is why <code>var</code> in loops caused bugs for
years.</p>
""",
                "tryit": """const name = "Ada";
let score = 0;

score = score + 10;    // let CAN be reassigned
console.log(`${name}: ${score}`);

// const objects can be mutated (not reassigned)
const prefs = { theme: "light" };
prefs.theme = "dark";    // ✓ fine
console.log("theme:", prefs.theme);

// block scoping with let
if (true) {
  let inner = "only visible inside this block";
  console.log(inner);
}
// console.log(inner);  // ← would throw ReferenceError!
""",
            },
            {
                "title": "Data Types",
                "html": """
<p>JavaScript has <b>8 data types</b> — 7 primitives and 1 object
type:</p>

<ul>
<li><b>Number</b> — integers and floats: <code>42</code>,
<code>3.14</code>, <code>NaN</code>, <code>Infinity</code></li>
<li><b>String</b> — text: <code>"hello"</code>,
<code>'world'</code>, <code>`template`</code></li>
<li><b>Boolean</b> — <code>true</code> / <code>false</code></li>
<li><b>undefined</b> — a variable declared but not yet assigned</li>
<li><b>null</b> — intentional absence of value</li>
<li><b>BigInt</b> — arbitrary precision integers:
<code>123n</code></li>
<li><b>Symbol</b> — unique identifiers: <code>Symbol("id")</code></li>
<li><b>Object</b> — everything else: arrays, functions, dates... (the
only non-primitive type)</li>
</ul>

<p>The <code>typeof</code> operator reveals a value's type at runtime —
with one famous quirk: <code>typeof null</code> returns
<code>"object"</code> (a bug from 1995 that can't be fixed without
breaking the web).</p>

<p>JS is <b>dynamically typed</b>: variables have no fixed type — the
<i>value</i> has the type. A variable can hold a number, then a string,
then an object. Flexibility with responsibility.</p>
""",
                "tryit": """// typeof reveals the type of a VALUE
console.log(typeof 42);           // "number"
console.log(typeof "hello");      // "string"
console.log(typeof true);         // "boolean"
console.log(typeof undefined);    // "undefined"
console.log(typeof null);         // "object" (the famous bug!)
console.log(typeof Symbol());    // "symbol"
console.log(typeof 123n);         // "bigint"
console.log(typeof {});           // "object"
console.log(typeof []);           // "object" (arrays are objects!)
console.log(typeof function(){}); // "function"

// Dynamic typing: same variable, different types
let x = 42;
console.log(typeof x);    // "number"
x = "now a string";
console.log(typeof x);    // "string"
""",
            },
            {
                "title": "Numbers & Strings",
                "html": """
<p><b>Numbers</b> are 64-bit floating point (there's no separate int
type). Special values: <code>NaN</code> ("Not a Number" — the result of
invalid math), <code>Infinity</code>, <code>-Infinity</code>:</p>

<pre class="code">42 + 1        // 43
3.14 * 2      // 6.28
10 / 3        // 3.3333...
10 / 0        // Infinity
0 / 0         // NaN
parseInt("42")  // 42
parseFloat("3.14")  // 3.14
(42.5678).toFixed(2)  // "42.57"</pre>

<p><b>Strings</b> are sequences of characters, immutable (methods
return new strings). Key methods:</p>

<pre class="code">"hello".length          // 5
"hello".toUpperCase()   // "HELLO"
"hello".slice(1, 3)     // "el"
"a,b,c".split(",")      // ["a", "b", "c"]
"  hi  ".trim()         // "hi"
"abc".includes("b")     // true
"abc".replace("a", "X") // "Xbc"</pre>

<p>Numbers and strings convert: <code>String(42) → "42"</code>,
<code>Number("42") → 42</code>, <code>+"42" → 42</code>. But
<code>Number("abc") → NaN</code> — always check!</p>
""",
                "tryit": """// Numbers
console.log(10 / 3);            // division
console.log(10 % 3);            // remainder
console.log(2 ** 10);           // exponent: 1024
console.log(0.1 + 0.2);         // 0.30000000000000004 (floating point!)
console.log((0.1 + 0.2).toFixed(2)); // "0.30"
console.log(parseInt("42abc")); // 42 (parses the leading number)
console.log(NaN === NaN);       // false — NaN is never equal to itself!

// Strings
const s = "JavaScript";
console.log(s.length);          // 10
console.log(s.toUpperCase());   // "JAVASCRIPT"
console.log(s.slice(0, 4));     // "Java"
console.log(s.includes("Script")); // true
console.log(s.replace("Java", "Type")); // "TypeScript"
console.log("a,b,c".split(","));  // ["a", "b", "c"]
""",
            },
            {
                "title": "Booleans, null & undefined",
                "html": """
<p><b>Booleans</b> are <code>true</code> and <code>false</code> — but
JS also has <b>truthy</b> and <b>falsy</b> values that coerce to
booleans in conditions:</p>

<ul>
<li><b>Falsy (6 total):</b> <code>false</code>, <code>0</code>,
<code>""</code>, <code>null</code>, <code>undefined</code>,
<code>NaN</code></li>
<li><b>Truthy:</b> everything else — including <code>"0"</code>,
<code>[]</code>, <code>{}</code>, <code>" "</code> (space!)</li>
</ul>

<p><b>null vs undefined</b> — the two "absence" values:</p>

<ul>
<li><code>undefined</code> — a variable declared but not assigned; a
function that doesn't return; an object property that doesn't exist.
JS's way of saying "not set yet"</li>
<li><code>null</code> — <i>you</i> set it, intentionally, to mean "no
value". It's a deliberate assignment</li>
</ul>

<pre class="code">let a;           // undefined
let b = null;    // null (intentional)

console.log(a == b);    // true (loose: both "empty")
console.log(a === b);   // false (strict: different types!)</pre>

<p>The <code>!!</code> double-negation converts any value to its boolean
equivalent — a common idiom: <code>!!"hello" → true</code>,
<code>!!0 → false</code>.</p>
""",
                "tryit": """// Falsy values (all 6)
console.log(!!false);     // false
console.log(!!0);         // false
console.log(!!"");        // false
console.log(!!null);      // false
console.log(!!undefined); // false
console.log(!!NaN);       // false

// Truthy surprises
console.log(!!"0");       // true (non-empty string!)
console.log(!![]);        // true (empty array is truthy!)
console.log(!!{});        // true (empty object is truthy!)

// null vs undefined
let a;
let b = null;
console.log(a, b);        // undefined null
console.log(typeof a);   // "undefined"
console.log(typeof b);   // "object" (the bug)
console.log(a == b);     // true (loose)
console.log(a === b);    // false (strict)
""",
            },
            {
                "title": "Type Conversion",
                "html": """
<p>JS converts types <i>all the time</i> — sometimes when you don't
expect it. <b>Explicit</b> conversion is when you call the conversion
yourself; <b>implicit</b> (coercion) is when JS does it behind your
back:</p>

<pre class="code">// explicit
Number("42")       // 42
String(42)         // "42"
Boolean(1)         // true
(42).toString()    // "42"
parseInt("3.14")   // 3 (integer part)

// implicit coercion — the tricky ones!
"5" + 3      // "53"   (number → string, concatenation)
"5" - 3      // 2      (string → number, subtraction)
"5" * "2"    // 10     (both → numbers)
1 + true     // 2      (true → 1)
[] + []      // ""     (both → "", concatenated)
[] + {}      // "[object Object]"</pre>

<p>The <code>+</code> operator is unique: it prefers string
concatenation if either operand is a string. Every other math operator
coerces to number. This asymmetry causes real bugs:</p>

<pre class="code">// form inputs are always strings!
const val = "10";
val + 5     // "105" — concatenation, not addition!
Number(val) + 5  // 15 — convert first!</pre>

<p>Modern operators avoid coercion: <code>===</code> (strict equality),
<code>??</code> (nullish coalescing), and
<code>Object.is()</code> never surprise you.</p>
""",
                "tryit": """// Explicit conversion
console.log(Number("42"));      // 42
console.log(String(42));        // "42"
console.log(Boolean(0));        // false
console.log(parseInt("3.14")); // 3
console.log(parseFloat("3.14")); // 3.14

// Implicit coercion — the weird ones
console.log("5" + 3);     // "53" (string concat)
console.log("5" - 3);     // 2 (number subtract)
console.log("5" * "2");   // 10
console.log(1 + true);   // 2
console.log([] + []);    // "" (empty string!)

// The form-input gotcha
const input = "10";  // like reading from an <input>
console.log(input + 5);        // "105" — NOT 15!
console.log(Number(input) + 5); // 15 — convert first!
""",
            },
            {
                "title": "Operators & Comparisons",
                "html": """
<p>JS operators, grouped by purpose:</p>

<ul>
<li><b>Arithmetic:</b> <code>+ - * / % **</code></li>
<li><b>Assignment:</b> <code>= += -= *= /= %= **= &amp;&amp;= ||= ??=</code></li>
<li><b>Comparison:</b> <code>&gt; &lt; &gt;= &lt;=</code></li>
<li><b>Equality:</b> <code>==</code> (loose), <code>===</code>
(strict), <code>!=</code>, <code>!==</code></li>
<li><b>Logical:</b> <code>&amp;&amp;</code> (AND), <code>||</code>
(OR), <code>!</code> (NOT), <code>??</code> (nullish)</li>
<li><b>Ternary:</b> <code>condition ? a : b</code></li>
<li><b>Optional chaining:</b> <code>obj?.prop</code></li>
<li><b>Increment/Decrement:</b> <code>++i</code>, <code>i--</code></li>
</ul>

<p>The logical operators are <i>short-circuiting</i>: they return the
value that decides the result, not just true/false. This enables
powerful patterns:</p>

<pre class="code">name = name || "Anonymous";   // default value (old style)
name = name ?? "Anonymous";   // default (only for null/undefined, not 0 or "")

isReady && start();            // only call if isReady is truthy
value = mayBeNull?.property;   // no crash if mayBeNull is null</pre>

<p><code>==</code> vs <code>===</code> deserves its own lesson (next!),
but the rule is simple: <b>always use ===</b>. The loose ==
performs type coercion that produces surprising results.</p>
""",
                "tryit": """// Short-circuit evaluation
const name = "" || "Anonymous";     // "" is falsy → "Anonymous"
console.log(name);

const count = 0 ?? 99;              // 0 is NOT null/undefined → stays 0
console.log(count);

const user = { profile: { email: "ada@x.io" } };
console.log(user?.profile?.email);  // "ada@x.io"
console.log(user?.missing?.deep);   // undefined (no crash!)

// Ternary
const age = 20;
const status = age >= 18 ? "adult" : "minor";
console.log(status);

// Chained assignment operators
let n = 10;
n += 5;   // 15
n *= 2;   // 30
n -= 5;   // 25
console.log(n);
""",
            },
            {
                "title": "Equality: == vs ===",
                "html": """
<p>The single most important distinction for JS beginners:</p>

<ul>
<li><code>==</code> (loose equality) — converts both sides to the same
type, <i>then</i> compares. Convenient but full of traps</li>
<li><code>===</code> (strict equality) — compares value AND type. No
conversion. Always predictable</li>
</ul>

<pre class="code">1 == "1"      // true  (string → number)
1 === "1"     // false (different types!)

null == undefined   // true
null === undefined  // false

NaN == NaN     // false (NaN never equals itself!)
NaN === NaN    // false

0 == false     // true
0 === false    // false</pre>

<p>The rules for <code>==</code> are so complex that MDN recommends
<b>never using it</b>. The only valid use case:
<code>x == null</code> checks for both null AND undefined at
once.</p>

<p><code>Object.is()</code> is a third comparison that's like
<code>===</code> but treats <code>NaN === NaN</code> as true and
<code>+0 !== -0</code>. It's what <code>Object.is()</code> is
for.</p>
""",
                "tryit": """// The traps of ==
console.log(1 == "1");          // true (coerced!)
console.log(0 == "");           // true ("" → 0)
console.log(null == undefined); // true
console.log([] == false);       // true ([] → "" → 0!)

// === is always predictable
console.log(1 === "1");         // false
console.log(0 === "");          // false
console.log(null === undefined);// false

// Object.is — edge cases
console.log(Object.is(NaN, NaN));     // true (!)
console.log(NaN === NaN);             // false
console.log(Object.is(0, -0));       // false
console.log(0 === -0);               // true

// The ONE valid use of ==
const x = null;
console.log(x == null);     // true — checks null OR undefined
console.log(x === null);    // true — but only null
console.log(x === undefined); // false
""",
            },
            {
                "title": "Template Literals",
                "html": """
<p>Template literals use <b>backticks</b> (<code>`</code>) instead of
quotes and unlock three superpowers that regular strings don't
have:</p>

<ul>
<li><b>Interpolation:</b> embed any expression with
<code>${expression}</code></li>
<li><b>Multi-line</b>: line breaks are preserved, no <code>\\n</code>
needed</li>
<li><b>Tagged templates</b>: functions can process the template (how
styled-components works)</li>
</ul>

<pre class="code">const name = "Ada";
const score = 95;

// interpolation — no more string concatenation!
console.log(`${name} scored ${score}%`);
console.log(`Next year: ${score + 5}%`);

// multi-line — natural formatting
const html = `
  &lt;div class="card"&gt;
    &lt;h2&gt;${name}&lt;/h2&gt;
    &lt;p&gt;Score: ${score}&lt;/p&gt;
  &lt;/div&gt;
`;

// expressions inside ${}
console.log(`Double: ${score * 2}`);
console.log(`Upper: ${name.toUpperCase()}`);
console.log(`Conditional: ${score >= 90 ? "pass" : "fail"}`);</pre>

<p>Any expression works inside <code>${}</code> — function calls,
ternaries, even nested template literals. This is the modern way to
build strings; string concatenation with <code>+</code> is
legacy.</p>
""",
                "tryit": """const name = "Ada";
const items = ["sword", "shield", "potion"];
const gold = 150;

// Interpolation
console.log(`${name} has ${gold} gold and ${items.length} items.`);

// Multi-line HTML
const html = `
  <div class="inventory">
    <h3>${name}'s Bag</h3>
    <ul>
      ${items.map(i => `<li>${i}</li>`).join("\\n")}
    </ul>
    <p>Gold: ${gold >= 100 ? "rich 💰" : "broke 😅"}</p>
  </div>
`;
console.log(html);

// Expressions inside ${}
console.log(`${items[0].toUpperCase()} costs ${Math.round(gold / 3)}g`);
""",
            },
        ],
        "quiz": [
            {
                "type": "mc",
                "question": "Which keyword declares a variable that CANNOT be reassigned?",
                "options": ["let", "var", "const", "static"],
                "answer": 2,
                "explain": "const = constant binding. Objects assigned to const can still be mutated.",
            },
            {
                "type": "mc",
                "question": "What does <code>typeof null</code> return?",
                "options": ["\"null\"", "\"undefined\"", "\"object\"", "\"boolean\""],
                "answer": 2,
                "explain": "typeof null returns \"object\" — a famous bug from 1995 that can't be fixed.",
            },
            {
                "type": "blank",
                "question": "The template literal syntax for embedding an expression is <code>____</code>.",
                "answers": ["${}", "${ }", "${expression}"],
                "explain": "${} embeds any expression inside backtick strings.",
            },
            {
                "type": "mc",
                "question": "How many falsy values does JavaScript have?",
                "options": ["2", "4", "6", "8"],
                "answer": 2,
                "explain": "false, 0, \"\", null, undefined, NaN — exactly 6.",
            },
            {
                "type": "mc",
                "question": "What does <code>\"5\" + 3</code> evaluate to?",
                "options": ["8", "\"53\"", "NaN", "Error"],
                "answer": 1,
                "explain": "+ prefers string concatenation when either operand is a string.",
            },
            {
                "type": "mc",
                "question": "The ONLY recommended use of == is:",
                "options": ["Comparing numbers", "x == null (checks both null and undefined)", "Comparing strings", "Never — always use ==="],
                "answer": 1,
                "explain": "x == null checks for both null and undefined in one expression.",
            },
        ],
    },

    # ------------------------------------------------------------------ js02
    {
        "id": "js02",
        "title": "Control Flow",
        "emoji": "🔀",
        "lessons": [
            {
                "title": "if / else",
                "html": """
<p>The fundamental branching statement — run code only when a condition
is truthy:</p>

<pre class="code">if (temperature &gt; 30) {
  console.log("hot");
} else if (temperature &gt; 20) {
  console.log("nice");
} else {
  console.log("cold");
}</pre>

<p>Conditions coerce to boolean — falsy values (0, "", null,
undefined, NaN) are treated as <code>false</code>. Curly braces are
technically optional for single statements, but always use them —
omitting them causes real bugs. For simple conditionals, the ternary
operator <code>condition ? a : b</code> is often cleaner.</p>

<p>MDN also documents <code>if...else if...else</code> chains (which are
really nested ifs) — keep them shallow; deeply nested conditionals are
a code smell that early returns or lookup tables can fix.</p>
""",
                "tryit": """const hour = 14;

if (hour < 12) {
  console.log("Good morning");
} else if (hour < 18) {
  console.log("Good afternoon");
} else {
  console.log("Good evening");
}

// Falsy values in conditions
const name = "";   // empty string = falsy
if (name) {
  console.log("Hello,", name);
} else {
  console.log("No name given");
}

// Ternary for simple cases
const label = hour < 12 ? "AM" : "PM";
console.log(label);
""",
            },
            {
                "title": "switch",
                "html": """
<p><code>switch</code> compares a value against multiple cases —
cleaner than long if-else chains:</p>

<pre class="code">switch (fruit) {
  case "apple":
    console.log("red or green");
    break;                    // REQUIRED — prevents fall-through!
  case "banana":
  case "plantain":            // multiple cases, same body
    console.log("yellow");
    break;
  default:
    console.log("unknown fruit");
}</pre>

<p>The <b>break</b> keyword exits the switch. Without it, execution
<b>falls through</b> to the next case — sometimes useful
(intentional fall-through for grouping), often a bug. The
<b>default</b> case handles unmatched values.</p>

<p>Important: switch uses <b>strict comparison</b> (===) —
<code>switch("1")</code> will NOT match <code>case 1:</code>. This
catches people off guard when working with form inputs.</p>
""",
                "tryit": """const day = "sat";

switch (day.toLowerCase()) {
  case "sat":
  case "sun":
    console.log("Weekend! 🎉");
    break;
  case "mon":
  case "tue":
  case "wed":
  case "thu":
    console.log("Weekday");
    break;
  case "fri":
    console.log("Almost weekend!");
    break;
  default:
    console.log("Not a day:", day);
}

// switch uses === (strict)
const num = "1";
switch (num) {
  case 1:
    console.log("number 1");     // NOT reached — num is a string!
    break;
  case "1":
    console.log("string \\"1\\"");  // THIS matches
    break;
}
""",
            },
            {
                "title": "while & do...while",
                "html": """
<p>Two loops that repeat while a condition is true:</p>

<pre class="code">// while: check condition FIRST (may run 0 times)
let count = 0;
while (count &lt; 5) {
  console.log(count);
  count++;         // don't forget! Otherwise: infinite loop
}

// do...while: run body FIRST, then check (always runs ≥ 1 time)
let input;
do {
  input = getNextGuess();
} while (input !== "correct");</pre>

<p>The critical difference: <code>while</code> checks before the first
iteration; <code>do...while</code> checks after — so do...while always
executes at least once. Use <code>while</code> for "repeat as long as"
and <code>do...while</code> for "do at least once, then repeat
if".</p>

<p>Infinite loops are the classic mistake — always ensure something in
the body moves toward the exit condition. The playground has a step
limit to protect you.</p>
""",
                "tryit": """let countdown = 5;
while (countdown > 0) {
  console.log("T-minus", countdown);
  countdown--;
}
console.log("Liftoff! 🚀");

// do...while runs at least once, even if condition is false
let n = 100;
do {
  console.log("runs once even though 100 > 10 is true");
  n++;
} while (n < 10);  // false after first iteration

// while with arrays
const stack = ["a", "b", "c"];
while (stack.length > 0) {
  console.log("popped:", stack.pop());
}
""",
            },
            {
                "title": "for & for...of",
                "html": """
<p>The classic <code>for</code> loop and the modern
<code>for...of</code>:</p>

<pre class="code">// classic for: full control over the counter
for (let i = 0; i &lt; 5; i++) {
  console.log(i);           // 0 1 2 3 4
}

// for...of: iterate VALUES of any iterable (arrays, strings, Maps...)
const fruits = ["apple", "banana", "cherry"];
for (const fruit of fruits) {
  console.log(fruit);
}

// for...of with strings (iterates characters)
for (const ch of "JS") {
  console.log(ch);          // "J" "S"
}

// for...of with entries() to get index + value
for (const [index, fruit] of fruits.entries()) {
  console.log(index, fruit);
}</pre>

<p><b>for...of is the modern way</b> to iterate arrays — no counter to
manage, no off-by-one errors. Use the classic <code>for</code> when you
need the index or need to skip/modify the counter. Use
<code>for...of</code> when you just need each value.</p>
""",
                "tryit": """// Classic for: full control
for (let i = 0; i <= 4; i++) {
  console.log("i =", i);
}

// Nested for: multiplication table
for (let row = 1; row <= 3; row++) {
  let line = "";
  for (let col = 1; col <= 3; col++) {
    line += (row * col).toString().padStart(3) + " ";
  }
  console.log(line);
}

// for...of: the modern way
const langs = ["JS", "Python", "C"];
for (const lang of langs) {
  console.log(`I'm learning ${lang}`);
}

// for...of with entries for index+value
for (const [i, lang] of langs.entries()) {
  console.log(`${i + 1}. ${lang}`);
}
""",
            },
            {
                "title": "for...in",
                "html": """
<p><code>for...in</code> iterates over the <b>keys</b> (property names)
of an object:</p>

<pre class="code">const user = { name: "Ada", age: 36, role: "admin" };

for (const key in user) {
  console.log(key, user[key]);    // "name" "Ada", "age" 36, ...
}

// with Object.keys() — often preferred
for (const key of Object.keys(user)) {
  console.log(key);
}

// Object.entries() for key+value pairs
for (const [key, value] of Object.entries(user)) {
  console.log(`${key}: ${value}`);
}</pre>

<p>Important: <b>don't use for...in on arrays</b> — it iterates string
indices ("0", "1"...) and may include inherited properties. Use
<code>for...of</code> or array methods (<code>forEach</code>,
<code>map</code>) instead. for...in is for <b>objects</b>.</p>

<p>The modern preference is <code>Object.keys()</code>,
<code>Object.values()</code>, or <code>Object.entries()</code> — they
return real arrays you can use with map/filter/reduce.</p>
""",
                "tryit": """const scores = { math: 95, science: 88, art: 92 };

// for...in iterates keys
for (const subject in scores) {
  console.log(`${subject}: ${scores[subject]}`);
}

// Object.entries() — the modern way
for (const [subject, score] of Object.entries(scores)) {
  console.log(`${subject}: ${score >= 90 ? "✓" : "✗"} ${score}`);
}

// Object.keys() and Object.values()
console.log("subjects:", Object.keys(scores));
console.log("scores:", Object.values(scores));

// find the best subject
let best = "";
for (const [subject, score] of Object.entries(scores)) {
  if (score > (scores[best] || 0)) best = subject;
}
console.log("best subject:", best);
""",
            },
            {
                "title": "break & continue",
                "html": """
<p>Two loop-control keywords that change the flow:</p>

<ul>
<li><b>break</b> — exit the loop entirely</li>
<li><b>continue</b> — skip to the next iteration</li>
</ul>

<pre class="code">// break: stop when found
const nums = [3, 7, 12, 8, 15];
for (const n of nums) {
  if (n &gt; 10) {
    console.log("found:", n);
    break;               // stop here
  }
}

// continue: skip odds
for (let i = 0; i &lt; 10; i++) {
  if (i % 2 !== 0) continue;   // skip odd numbers
  console.log(i);               // 0 2 4 6 8
}</pre>

<p>In nested loops, <code>break</code>/<code>continue</code> affect only
the <b>innermost</b> loop. To exit an outer loop, use labeled
statements:</p>

<pre class="code">outer: for (let i = 0; i &lt; 3; i++) {
  for (let j = 0; j &lt; 3; j++) {
    if (i * j === 2) break outer;   // exits BOTH loops
    console.log(i, j);
  }
}</pre>
""",
                "tryit": """// break: early exit
const passwords = ["1234", "letmein", "correct-horse", "hack"];
for (const pw of passwords) {
  if (pw === "correct-horse") {
    console.log("Found it:", pw);
    break;
  }
  console.log("tried:", pw);
}

// continue: skip and keep going
for (let i = 1; i <= 10; i++) {
  if (i % 3 === 0) continue;   // skip multiples of 3
  console.log(i);              // 1 2 4 5 7 8 10
}

// labeled break for nested loops
outer:
for (let row = 0; row < 5; row++) {
  for (let col = 0; col < 5; col++) {
    if (row * col > 6) {
      console.log(`found at (${row}, ${col})`);
      break outer;
    }
  }
}
console.log("done searching");
""",
            },
            {
                "title": "Error Handling: try / catch / finally & throw",
                "html": """
<p>Errors happen — invalid input, network failures, missing data. JS
handles them with <code>try / catch / finally</code> and creates them
with <code>throw</code>:</p>

<pre class="code">try {
  // code that might fail
  const data = JSON.parse(invalidJson);
} catch (error) {
  // runs ONLY if an error occurred
  console.error("Caught:", error.message);
} finally {
  // ALWAYS runs (cleanup)
  console.log("done trying");
}

// creating your own errors
function divide(a, b) {
  if (b === 0) {
    throw new Error("Cannot divide by zero!");
  }
  return a / b;
}

try {
  divide(10, 0);
} catch (e) {
  console.log(e.message);   // "Cannot divide by zero!"
}</pre>

<ul>
<li><b>throw</b> — signal an error; you can throw anything, but always
throw <code>Error</code> instances</li>
<li><b>catch(error)</b> — receives the thrown error object
(<code>error.message</code>, <code>error.stack</code>)</li>
<li><b>finally</b> — cleanup code that runs regardless of success or
failure</li>
<li><b>Error types:</b> <code>TypeError</code>,
<code>ReferenceError</code>, <code>SyntaxError</code>,
<code>RangeError</code> — or make your own with
<code>class MyError extends Error</code></li>
</ul>

<p>Don't catch-and-ignore: an empty <code>catch {}</code> hides bugs.
Log the error or re-throw it.</p>
""",
                "tryit": """// Basic try/catch
try {
  const data = JSON.parse("not valid json");
  console.log("never reaches here");
} catch (error) {
  console.log("caught:", error.message);
} finally {
  console.log("finally always runs");
}

// throwing custom errors
function validateAge(age) {
  if (typeof age !== "number") {
    throw new TypeError("Age must be a number");
  }
  if (age < 0 || age > 150) {
    throw new RangeError("Age must be 0-150");
  }
  return `${age} is valid`;
}

try {
  console.log(validateAge(25));
  console.log(validateAge(-5));
} catch (e) {
  console.log(`${e.constructor.name}: ${e.message}`);
}

// catch with different error types
try {
  null.property;   // TypeError
} catch (e) {
  if (e instanceof TypeError) console.log("It's a TypeError!");
}
""",
            },
        ],
        "quiz": [
            {
                "type": "mc",
                "question": "What happens if you omit 'break' in a switch case?",
                "options": ["A syntax error", "Execution falls through to the next case", "The switch is skipped", "It returns undefined"],
                "answer": 1,
                "explain": "Without break, execution continues into the next case — sometimes useful, often a bug.",
            },
            {
                "type": "blank",
                "question": "The loop that always runs at least once is <code>____...while</code>.",
                "answers": ["do", "do..."],
                "explain": "do...while checks the condition after the first iteration.",
            },
            {
                "type": "mc",
                "question": "for...in iterates over:",
                "options": ["Values of an array", "Keys of an object", "Characters of a string", "Elements of a Set"],
                "answer": 1,
                "explain": "for...in yields property names (keys). Use for...of for values.",
            },
            {
                "type": "mc",
                "question": "Which runs regardless of whether an error occurred?",
                "options": ["try", "catch", "finally", "throw"],
                "answer": 2,
                "explain": "finally always runs — it's for cleanup code.",
            },
            {
                "type": "mc",
                "question": "In nested loops, 'break' exits:",
                "options": ["All loops", "The innermost loop only", "The outermost loop", "The function"],
                "answer": 1,
                "explain": "break affects the innermost loop; labeled break (break outer:) exits the labeled one.",
            },
        ],
    },
]
