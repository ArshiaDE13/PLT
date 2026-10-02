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
<p>Every web page you have ever used is built from three layers.
<b>HTML</b> is the skeleton: headings, paragraphs, buttons. <b>CSS</b>
is the skin: colors, fonts, layout. <b>JavaScript</b> is the muscles:
when you click "Add to cart" and the total updates without a page
reload, that is JS running. Without it, a web page is a poster you can
only look at. This chapter's job is to make you fluent in the language
itself before later chapters use it to build real things.</p>

<p>So what <i>is</i> JavaScript? A full programming language that runs
<i>inside your browser</i>. MDN describes it as dynamically typed,
prototype-based, and garbage-collected, with first-class functions —
you will meet every one of those ideas in the coming chapters. Despite
the name, it has nothing to do with Java; the similar name was 1995
marketing, and the two languages share about as much as "car" and
"carpet".</p>

<p>How does it actually run? The browser ships an engine (V8 in
Chrome, SpiderMonkey in Firefox) that reads your code and executes it
statement by statement, top to bottom. The same language also runs
outside browsers — Node.js uses it for servers and tools — but in this
course you write code, press Run, and the page's own engine executes
it, printing every <code>console.log()</code> to the console
below.</p>

<p><b>Gotcha:</b> JavaScript is standardized as <b>ECMAScript</b>
(ECMA-262) and gains new features every year, but browsers adopt them
at different speeds. If something that "should work" throws an error,
check MDN's browser-support tables before assuming your code is
wrong.</p>
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
<p>Before you can say anything interesting, you need the punctuation
rules of JS: how statements end, how code is grouped, and how to leave
notes the engine ignores. That last one matters more than beginners
expect — professional code is read far more often than it is written,
and comments are how you explain the <i>why</i> to the next reader,
who is usually future you.</p>

<p>JS executes statements one at a time, top to bottom. Each statement
usually ends with a semicolon — technically optional, because the
engine can often infer it, but recommended, because the inference
rules have edge cases. Curly braces <code>{ }</code> group statements
into blocks, which you will use for functions, conditions and loops.
Whitespace and indentation mean nothing to the engine — but they mean
everything to humans, so indent consistently.</p>

<p>The block below shows both comment styles. Before you read any
explanation, predict: what will the console show when this runs? The
answer is <i>nothing</i>. Both lines are comments, so the engine skips
them entirely — they exist only for human eyes.</p>

<pre class="code">// single-line comment

/* multi-line
   comment */</pre>

<p>The first style, <code>//</code>, comments out the rest of its
line; use it for short notes or for switching off a single line while
debugging. The second, <code>/* ... */</code>, stretches across
lines; use it for longer explanations or for temporarily disabling a
whole chunk of code.</p>

<p><b>Gotchas:</b> JS is <b>case-sensitive</b> — <code>myVar</code>
and <code>myvar</code> are two different variables, and a
capitalization typo produces "is not defined" errors that look
baffling. Also, block comments do not nest: the first
<code>*/</code> ends the comment, and everything after it is code
again — usually a syntax error. (Modern modules and classes run in
strict mode automatically, which catches silent mistakes like
assigning to undeclared variables — you rarely type
<code>"use strict"</code> yourself anymore.)</p>
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
<p>A program needs to remember things — a score, a user's name, a
counter. <b>Variables</b> are named boxes for values, and JS gives you
three keywords to create them. Picking the wrong one leads to bugs
that are painful to trace, so learn the decision now: default to
<code>const</code>, switch to <code>let</code> only when the value
must change, and never write <code>var</code> in new code.</p>

<p>Walk the first block. <code>const PI = 3.14159</code> creates a
binding that can never be reassigned — try <code>PI = 3</code> later
and the engine throws a TypeError. <code>let count = 0</code> is a
normal, changeable variable: reassign it freely. <code>var old =
"legacy"</code> is the 1995 keyword — it ignores block boundaries
(function-scoped) and is hoisted, meaning usable before its line.
Both behaviors cause subtle bugs, which is why modern code avoids
it.</p>

<pre class="code">const PI = 3.14159;    // cannot be reassigned
let count = 0;          // can be reassigned, block-scoped
var old = "legacy";     // function-scoped, hoisted — avoid in new code</pre>

<p>Now the classic surprise. <code>const</code> freezes the
<i>binding</i>, not the value. Predict what the second block does:
replacing <code>user</code> entirely throws, but editing the object's
<i>contents</i> is fine — so <code>user.name = "Grace"</code>
succeeds. Run the try-it to confirm both sides.</p>

<pre class="code">const user = { name: "Ada" };
user.name = "Grace";     // ✓ mutation is fine — same object
// user = {};            // ✗ TypeError: assignment to constant</pre>

<p>Both <code>let</code> and <code>const</code> are block-scoped: they
exist only inside the <code>{ }</code> they were declared in.
<code>var</code> leaks to the whole function — which is exactly why
<code>var</code> inside loops caused bugs for years.</p>

<p><b>Gotcha:</b> "const means the value never changes" is the wrong
mental model — it means the <i>name</i> never points somewhere else.
Objects and arrays behind a <code>const</code> stay fully
mutable.</p>
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
<p>Every value in JS has a type, and the type decides what you can do
with it: multiplying numbers makes sense, multiplying two strings does
not. JS has <b>8 types</b> — 7 small, immutable <b>primitives</b> and
one big <b>object</b> type. The primitives:</p>

<ul>
<li><b>Number</b> — integers and floats: <code>42</code>,
<code>3.14</code>, plus the special values <code>NaN</code> and
<code>Infinity</code></li>
<li><b>String</b> — text: <code>"hello"</code>,
<code>'world'</code>, <code>`template`</code></li>
<li><b>Boolean</b> — <code>true</code> / <code>false</code></li>
<li><b>undefined</b> — declared, but not yet assigned a value</li>
<li><b>null</b> — deliberately empty, set by you</li>
<li><b>BigInt</b> — huge integers: <code>123n</code></li>
<li><b>Symbol</b> — unique identifiers: <code>Symbol("id")</code></li>
<li><b>Object</b> — everything else: arrays, functions, dates, plain
<code>{ }</code>... the only non-primitive type</li>
</ul>

<p>How do you find out what you are holding? The <code>typeof</code>
operator answers at runtime: <code>typeof 42</code> gives
<code>"number"</code>, <code>typeof "hello"</code> gives
<code>"string"</code>. The try-it below asks typeof about ten values —
predict every answer before you press Run, especially
<code>typeof []</code> and <code>typeof null</code>.</p>

<p>That last one is the famous quiz question: <code>typeof null</code>
returns <code>"object"</code>. It is a bug from the very first version
of JS in 1995 — the value is obviously not an object — but it can
never be fixed, because changing it would break every website that
relies on today's behavior.</p>

<p>JS is <b>dynamically typed</b>: the variable has no fixed type, the
<i>value</i> does. One variable can hold a number, then a string, then
an object — the last lines of the try-it demonstrate exactly that
sequence. Flexibility, with responsibility.</p>

<p><b>Gotcha:</b> <code>typeof []</code> is <code>"object"</code>, not
"array" — arrays are objects with numbered keys. When you specifically
need to know "is this an array?", use
<code>Array.isArray(x)</code>.</p>
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
<p>Real programs juggle two kinds of data constantly: quantities and
text. JS models them with <b>Number</b> and <b>String</b> — and both
hide surprises. There is no separate integer type: every number is a
64-bit floating-point value, so <code>1</code> and <code>1.0</code>
are the same number. That is mostly harmless; the surprises live at
the edges.</p>

<p>Read the first block top to bottom and predict each result before
reading the comments. The arithmetic you expect works: <code>42 +
1</code> is 43. Division produces decimals: <code>10 / 3</code> is
3.3333... Dividing by zero does not error — it gives
<code>Infinity</code> — and the truly broken case, <code>0 / 0</code>,
gives <code>NaN</code> ("Not a Number"), the result of invalid math.
The last lines convert text to numbers: <code>parseInt("42")</code>
is 42, <code>parseFloat("3.14")</code> keeps the decimals, and
<code>(42.5678).toFixed(2)</code> rounds for display, giving
"42.57".</p>

<pre class="code">42 + 1        // 43
3.14 * 2      // 6.28
10 / 3        // 3.3333...
10 / 0        // Infinity
0 / 0         // NaN
parseInt("42")  // 42
parseFloat("3.14")  // 3.14
(42.5678).toFixed(2)  // "42.57"</pre>

<p>Strings are sequences of characters and are <b>immutable</b>: no
method ever edits a string in place — each one returns a new string.
In the second block, <code>"hello".length</code> is 5. Notice
<code>slice(1, 3)</code> takes characters from index 1 up to — but
not including — index 3, giving "el". <code>split(",")</code> chops
the text into an array at each comma, <code>trim()</code> strips
whitespace from both ends, and <code>replace()</code> swaps its first
match, building the new string.</p>

<pre class="code">"hello".length          // 5
"hello".toUpperCase()   // "HELLO"
"hello".slice(1, 3)     // "el"
"a,b,c".split(",")      // ["a", "b", "c"]
"  hi  ".trim()         // "hi"
"abc".includes("b")     // true
"abc".replace("a", "X") // "Xbc"</pre>

<p>Converting between the two types is routine: <code>String(42)</code>
gives "42", <code>Number("42")</code> gives 42, and the shortcut
<code>+"42"</code> also gives 42. But <code>Number("abc")</code> gives
<code>NaN</code> — so always check conversions from text.</p>

<p><b>Gotcha:</b> <code>0.1 + 0.2</code> is
<code>0.30000000000000004</code>, not 0.3 — floating-point rounding,
the classic beginner shock (the try-it shows it). Format with
<code>toFixed()</code> for display, and never test floats for exact
equality.</p>
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
<p>Conditions need to answer yes/no questions, so JS has
<code>true</code> and <code>false</code>. But here is what trips up
beginners: JS does not require a real boolean in an <code>if</code>.
It converts <i>any</i> value to true or false on the spot. Exactly
<b>6 values</b> convert to false — the "falsy" list: <code>false</code>,
<code>0</code>, <code>""</code> (empty string), <code>null</code>,
<code>undefined</code>, <code>NaN</code>. Everything else — including
<code>"0"</code>, <code>" "</code> (a space!), and even empty arrays
and objects — is truthy.</p>

<p>Why does this matter? Because <code>if (count)</code> silently
treats 0 as "no", and <code>if (name)</code> treats an empty string as
"no". Sometimes that is exactly what you want; sometimes it is a bug.
Memorize the 6-item list and you can predict any condition.</p>

<p>Next, the two "absence" values. They look interchangeable but mean
different things. <code>undefined</code> is JS's way of saying "not
set yet": a declared-but-unassigned variable, a function that finishes
without <code>return</code>, a missing object property.
<code>null</code> is <i>you</i> deliberately writing "no value here"
in your code.</p>

<p>Now walk the code block. Predict both comparisons before reading
the comments. <code>a</code> is undefined and <code>b</code> is null.
The loose comparison <code>==</code> says they are equal — both count
as "empty" — while the strict <code>===</code> says false, because the
types differ.</p>

<pre class="code">let a;           // undefined
let b = null;    // null (intentional)

console.log(a == b);    // true (loose: both "empty")
console.log(a === b);   // false (strict: different types!)</pre>

<p>A handy idiom: the double negation <code>!!value</code> converts
anything to its real boolean — <code>!!"hello"</code> is
<code>true</code>, <code>!!0</code> is <code>false</code>. The try-it
uses it to test the entire falsy list.</p>

<p><b>Gotcha:</b> <code>typeof b</code> for a null value returns
<code>"object"</code> — the same 1995 bug again. Test for null with
<code>b === null</code>, never with typeof.</p>
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
<p>JS constantly converts between types — sometimes because you asked
(explicit), sometimes behind your back (implicit coercion). You need
both in your mental model, because the implicit ones are where real
bugs live. The one rule that explains half the weirdness: the
<code>+</code> operator prefers strings; every other math operator
prefers numbers.</p>

<p>Start with explicit conversion, where you call the conversion
yourself — the safe, readable style. <code>Number("42")</code> turns
text into a number, <code>String(42)</code> does the reverse,
<code>Boolean(1)</code> gives <code>true</code>,
<code>(42).toString()</code> is another route to "42", and
<code>parseInt("3.14")</code> chops off the decimals and gives 3.
Predict each line, then check the comments.</p>

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

<p>Now the implicit ones — read them slowly, they are interview
favorites. <code>"5" + 3</code> gives <code>"53"</code>: + sees a
string and switches to concatenation. <code>"5" - 3</code> gives 2:
minus only does math, so the string converts to a number.
<code>1 + true</code> gives 2 because true becomes 1. And
<code>[] + []</code> gives <code>""</code> — both arrays become empty
strings first. Nobody writes these on purpose; you need them to
diagnose accidents.</p>

<p>The second block is the bug that bites every beginner once: form
inputs always deliver strings. <code>"10" + 5</code> is
<code>"105"</code>, not 15. Convert first with <code>Number(val)</code>,
then do the math.</p>

<pre class="code">// form inputs are always strings!
const val = "10";
val + 5     // "105" — concatenation, not addition!
Number(val) + 5  // 15 — convert first!</pre>

<p><b>Rule of thumb:</b> modern operators avoid coercion — prefer
<code>===</code> over <code>==</code>, <code>??</code> over
<code>||</code> for defaults, and convert incoming text to numbers
explicitly at the boundary where data enters your program.</p>
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
<p>Operators are the verbs of JS: arithmetic (<code>+ - * / %
**</code>), assignment shortcuts (<code>+=</code>, <code>*=</code>...),
comparisons (<code>&gt;</code>, <code>&lt;=</code>), logical
(<code>&amp;&amp;</code>, <code>||</code>, <code>!</code>), plus the
ternary and optional chaining. You have already used most of them in
try-it boxes; here we focus on the family that behaves in a
non-obvious way: the logical operators.</p>

<p><code>&amp;&amp;</code> and <code>||</code> are
<b>short-circuiting</b>: they stop evaluating as soon as the answer is
decided — and, crucially, they return the <i>value that decided the
result</i>, not just true/false. That sounds odd until you see the
pattern it enables: <code>name || "Anonymous"</code> evaluates to
<code>name</code> when name is truthy, otherwise to the fallback
string. One line gives you "use this, or a default".</p>

<p>But the old <code>||</code> default has a trap: it falls back on
<i>every</i> falsy value, including 0 and "". That is why
<code>??</code> exists — it falls back only on null/undefined. Walk
the code block and predict each result: which default wins for the
empty name, what happens to the count of 0, when does
<code>isReady &amp;&amp; start()</code> actually call, and what does
optional chaining return for a missing property.</p>

<pre class="code">name = name || "Anonymous";   // default value (old style)
name = name ?? "Anonymous";   // default (only for null/undefined, not 0 or "")

isReady && start();            // only call if isReady is truthy
value = mayBeNull?.property;   // no crash if mayBeNull is null</pre>

<p>The ternary <code>condition ? a : b</code> is a whole if/else
compressed into one expression — great for picking between two
values, too clever for anything longer. Optional chaining
<code>obj?.prop</code> reads a property safely: if <code>obj</code>
is null or undefined you get <code>undefined</code> back instead of a
TypeError crash.</p>

<p><b>Gotcha:</b> do not write <code>count = count || 10</code> for a
counter — a perfectly legitimate 0 would be replaced by 10. That is
precisely what <code>??</code> is for. And the loose
<code>==</code> versus strict <code>===</code> question gets its own
next lesson; for now the rule is simply: always <code>===</code>.</p>
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
<p>Comparing values sounds trivial — until JS converts one side just
to surprise you. The two equality operators differ in exactly one
thing: <code>==</code> (loose) converts both sides to the same type
<i>first</i>, then compares; <code>===</code> (strict) compares value
<i>and</i> type, converting nothing. Strict equality is always
predictable, which is why the community rule is blunt: use
<code>===</code> everywhere.</p>

<p>Walk the block line by line and predict before reading the
comments. <code>1 == "1"</code> is true because the string "1" is
converted to the number 1. <code>1 === "1"</code> is false — a number
is not a string, done. <code>null == undefined</code> is a special
pair that loose equality treats as matching; strict says false.
<code>NaN === NaN</code> is false — NaN is defined as unequal to
everything, including itself. And <code>0 == false</code> is true
because false converts to 0; strict says false.</p>

<pre class="code">1 == "1"      // true  (string → number)
1 === "1"     // false (different types!)

null == undefined   // true
null === undefined  // false

NaN == NaN     // false (NaN never equals itself!)
NaN === NaN    // false

0 == false     // true
0 === false    // false</pre>

<p>Why not just learn the conversion rules of <code>==</code>?
Because they form a maze of special cases nobody remembers fully —
MDN recommends never using it. There is exactly one accepted use:
<code>x == null</code> is true when x is null <i>or</i> undefined, a
compact "has no value" check.</p>

<p>For completeness, <code>Object.is()</code> is a third comparison:
like <code>===</code> except it treats NaN as equal to itself and
distinguishes <code>+0</code> from <code>-0</code>. The try-it
demonstrates both edge cases, plus the one valid
<code>==</code>.</p>

<p><b>Gotcha:</b> if a condition like <code>if (input == 0)</code>
behaves strangely, suspect loose-equality coercion — an empty string
also equals 0 loosely. Switch to <code>===</code> and the mystery
usually disappears immediately.</p>
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
<p>You constantly need strings that mix fixed text with live values:
"Ada scored 95%". The old way was concatenation with <code>+</code> —
opening quotes, plus signs, closing quotes, and a mess once the
sentence grows. Template literals, written with backticks
(<code>`</code>), solve this: you write the sentence naturally and
embed values with <code>${expression}</code>.</p>

<p>Three powers come with backticks. First, <b>interpolation</b>:
anything legal in JS goes inside <code>${}</code> — a variable, a
sum, a function call, even a ternary. Second, <b>multi-line</b>:
press Enter and the line break becomes part of the string, no
<code>\\n</code> needed — that is how the HTML card in the code block
keeps its neat indentation. Third, <b>tagged templates</b>: a
function can process the template; you will rarely write one, but
libraries like styled-components are built on them.</p>

<p>Walk the block. <code>`${name} scored ${score}%`</code> substitutes
the variables' values — predict the exact output, punctuation
included. <code>`Next year: ${score + 5}%`</code> proves that
expressions are evaluated: 95 becomes 100. The multi-line HTML string
shows why backticks won: quotes inside the string, no escaping, real
line breaks. The last three lines compute, call a method, and branch
— all inside <code>${}</code>.</p>

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

<p><b>Gotcha:</b> backticks only — a normal quote mark does not
interpolate, so <code>"${name}"</code> prints a literal dollar-brace
instead of the value. Also remember that a multi-line template really
contains line breaks and the indentation spaces you typed — perfect
for readable HTML, wrong when you need a tight single-line
value.</p>
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
<p>Programs need to make decisions: show a "hot" icon above 30
degrees, a different message otherwise. <code>if / else</code> is the
fundamental branching tool — it runs a block only when its condition
is truthy, and optionally an alternative block otherwise. You will
use it in nearly every function you ever write.</p>

<p>The mechanics: JS evaluates the condition inside the parentheses,
converts it to true or false (remember the 6 falsy values), and runs
the matching block. The chain in the code block is checked top to
bottom — first match wins, everything after it is skipped. Order
matters: if you tested <code>&gt; 20</code> first, a temperature of
35 would print "nice" and never reach "hot".</p>

<p>Predict the output for <code>temperature = 25</code> before reading
on: the first test fails (25 is not greater than 30), the second
succeeds, so "nice" prints and the final <code>else</code> is
skipped.</p>

<pre class="code">if (temperature &gt; 30) {
  console.log("hot");
} else if (temperature &gt; 20) {
  console.log("nice");
} else {
  console.log("cold");
}</pre>

<p>Three habits worth building now. First, always use curly braces,
even for a single statement — omitting them causes real, documented
bugs when someone later adds a second line at the wrong indentation.
Second, keep chains shallow; deeply nested if/else is a code smell
that early <code>return</code>s or a lookup table usually fix
better. Third, for choosing between exactly two values, the ternary
<code>condition ? a : b</code> is cleaner than a four-line
if/else.</p>

<p><b>Gotcha:</b> <code>if (name)</code> with an empty string skips
the block, because <code>""</code> is falsy — is that what you meant?
For presence checks, prefer explicit tests like
<code>if (name !== "")</code> so your intent is visible to every
reader, including you in six months.</p>
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
<p>When one value must be compared against many fixed options — a
menu choice, a status code, a day of the week — a long if/else chain
works but gets noisy. <code>switch</code> states the value once and
lists the matching cases under it, which reads better and is harder
to get wrong.</p>

<p>Execution jumps to the matching <code>case</code> and runs from
there — and here is the famous mechanic: it keeps running into the
next case until it hits <code>break</code>. That is <b>fall-through</b>.
Sometimes you want it on purpose: notice how "banana" and "plantain"
share one body by stacking their cases. Most of the time it is an
accident, so end every case with <code>break</code>. The
<code>default</code> case catches everything that no case
matched.</p>

<p>Predict: what happens with <code>fruit = "cherry"</code>? No case
matches, so execution lands in <code>default</code> and prints
"unknown fruit".</p>

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

<p>One more mechanic that surprises people: switch compares with
<b>strict ===</b>, not loose ==. The string <code>"1"</code> will not
match <code>case 1:</code>. This bites hardest with form inputs,
which always arrive as strings — convert with
<code>Number(...)</code> before switching on numbers.</p>

<p><b>Gotcha:</b> forgetting a single <code>break</code> produces no
error — the code simply runs the next case's body too, which can
look like a logic bug from far away. If a switch prints two lines
when you expected one, look for a missing break first.</p>
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
<p>Loops answer "how do I repeat this without copy-pasting it?"
<code>while</code> is the most basic form: as long as the condition
is true, run the body again. Reach for it when you do not know in
advance how many repetitions you need — draining a queue, waiting
for a value, counting down.</p>

<p>Walk the first half of the block. <code>count</code> starts at 0;
the condition <code>count &lt; 5</code> is checked <i>before</i> each
pass; the body prints and then increments. So the loop prints 0
through 4 — five numbers — and then the condition fails and execution
continues below. Because the check comes first, a <code>while</code>
loop can legitimately run zero times: start <code>count</code> at 10
and nothing prints at all.</p>

<p><code>do...while</code> flips the order: the body runs
<i>first</i>, and the condition is checked after. That guarantees at
least one execution — useful for "ask the user, then ask again if the
answer was wrong" style logic, sketched in the second half of the
block.</p>

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

<p><b>Gotchas:</b> the classic beginner disaster is the infinite
loop — if nothing in the body moves the condition toward false
(forgetting <code>count++</code>), the loop never ends and the tab
freezes. Before running any while loop, point at the exact line that
makes progress. And never put a semicolon directly after
<code>while (...)</code> — it creates an empty loop body, and your
"real" block below runs once, unguarded by the condition.</p>
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
<p>When you know — or can compute — how many times to repeat, the
classic <code>for</code> loop packs the whole setup into one header:
start, condition, step. When you just want each element of an array
or string, the modern <code>for...of</code> is simpler and safer.
Knowing when each one fits is the actual skill here.</p>

<p>The header has three parts separated by semicolons:
<code>let i = 0</code> runs once before anything;
<code>i &lt; 5</code> is checked before every pass; <code>i++</code>
runs after every pass. So the loop prints 0, 1, 2, 3, 4 — notice it
stops <i>before</i> 5. Off-by-one errors live exactly here: writing
<code>&lt;=</code> would print six numbers instead.</p>

<p><code>for...of</code> removes the counter entirely: for each
element of an iterable — array, string, Map — it hands you the value
itself. Predict the fruit loop's output: "apple", "banana",
"cherry", one per line. Strings are iterable too, so
<code>for (const ch of "JS")</code> gives "J" then "S". When you need
the index <i>and</i> the value together, <code>fruits.entries()</code>
yields <code>[index, value]</code> pairs that the loop header can
destructure on the spot.</p>

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

<p><b>Rules of thumb:</b> default to <code>for...of</code> for "do
something with each item"; reach for classic <code>for</code> when
you need to skip elements, walk backwards, or bend the counter. And
never use <code>for...in</code> on arrays — the next lesson explains
exactly why.</p>
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
<p>Arrays answer "give me each value", but objects raise a different
question: "what keys do I even have?" <code>for...in</code> is the
loop built for that — it walks the property <i>names</i> of an
object, and you fetch each value with bracket access,
<code>user[key]</code>.</p>

<p>In the block's first loop, the keys "name", "age" and "role" come
out one at a time as strings, and <code>user[key]</code> reads the
matching value. The second and third loops show the modern
alternatives: <code>Object.keys(user)</code> returns the keys as a
real array, and <code>Object.entries(user)</code> returns
<code>[key, value]</code> pairs — which the loop header can
destructure directly, as the third loop does.</p>

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

<p>Why prefer the <code>Object.*</code> versions? Two reasons. They
give real arrays, which you can also feed to
<code>map</code>/<code>filter</code>/<code>reduce</code>. And
<code>for...in</code> has a quirk: it walks <i>inherited</i>
properties too, so keys you never wrote can appear. With plain
object literals this is rare, but the habit of using
<code>Object.entries()</code> sidesteps the issue entirely.</p>

<p><b>Gotcha — the big one:</b> never use <code>for...in</code> on
arrays. It yields indexes as <i>strings</i> ("0", "1", ...) and can
include inherited members; <code>for...of</code> or array methods are
what you want there. Split the rule in your head: <code>for...of</code>
for arrays and strings, <code>for...in</code> — or better,
<code>Object.entries()</code> — for objects.</p>
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
<p>Normal loops run to completion, but search problems rarely need to:
once you have found the answer, more iterations are wasted work.
<b>break</b> exits the loop immediately; <b>continue</b> abandons just
the current pass and jumps to the next one. Together they turn blunt
loops into efficient ones.</p>

<p>In the first block, the loop scans <code>nums</code> until it finds
a value above 10, prints it, and <code>break</code> stops everything
— the remaining numbers are never checked. In the second block,
<code>continue</code> filters: odd numbers fail the test, jump
straight to <code>i++</code>, and never reach the print, so only 0,
2, 4, 6 and 8 appear.</p>

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

<p>Nested loops need one more tool: a plain <code>break</code> only
leaves the <i>innermost</i> loop — the outer one keeps going, which
is usually not what "stop searching entirely" means. A <b>label</b>
names the outer loop (<code>outer:</code>) and <code>break
outer;</code> exits <i>both</i>. The second block demonstrates: the
moment <code>i * j === 2</code>, the whole search ends.</p>

<pre class="code">outer: for (let i = 0; i &lt; 3; i++) {
  for (let j = 0; j &lt; 3; j++) {
    if (i * j === 2) break outer;   // exits BOTH loops
    console.log(i, j);
  }
}</pre>

<p><b>Gotcha:</b> <code>continue</code> inside a classic
<code>for</code> loop still runs the update expression
(<code>i++</code>), but inside a <code>while</code> loop it jumps
straight back to the condition check — if your <code>count++</code>
sits below the <code>continue</code>, you have just built an infinite
loop. Also remember that <code>find()</code> and <code>some()</code>
often replace an entire search loop more cleanly.</p>
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
<p>Code fails in the real world: JSON from a server is malformed, a
value that should be a number arrives as a string. Without a plan,
the failure crashes your program halfway through. JS's plan is
<code>try / catch / finally</code> for handling failures and
<code>throw</code> for signaling them.</p>

<p>The flow: risky code goes inside <code>try</code>. If anything
throws there, execution jumps instantly to <code>catch</code>, which
receives an Error object — <code>error.message</code> holds the
human-readable description, <code>error.stack</code> the trail.
<code>finally</code> runs afterward no matter what happened: success,
failure, even a <code>return</code> — its job is cleanup like closing
a connection. In the block, <code>JSON.parse</code> throws on invalid
text, so "never reaches here" really never runs; "Caught:" prints,
then "done trying" from finally.</p>

<p>The second half shows the other direction — your own code can
<code>throw</code>. The <code>divide</code> function checks its input
and throws an <code>Error</code> with a clear message rather than
letting nonsense flow onward. Always throw <code>Error</code>
instances — throwing bare strings or numbers loses the stack trace.
Know the built-in types too: <code>TypeError</code>,
<code>ReferenceError</code>, <code>SyntaxError</code>,
<code>RangeError</code> each signal a different kind of mistake, and
<code>instanceof</code> tells you which one you caught (the try-it
demonstrates).</p>

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

<p><b>Gotcha:</b> never write an empty <code>catch {}</code> — it
swallows the error and hides the bug from yourself; you will end up
debugging ghosts. Log it or re-throw it. And note that try/catch has
limits: it cannot catch syntax errors, and an error thrown later
inside an async callback escapes it entirely.</p>
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
