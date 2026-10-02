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
<p>Almost everything in JavaScript is an object, and the language keeps
two toolboxes within reach at all times: the <code>Object</code> and
<code>Array</code> globals. You reach for them when plain syntax is not
enough — listing an object's keys, turning a string into a real array,
or answering "is this actually an array?". These are <b>static</b>
methods, so you call them on <code>Object</code> or <code>Array</code>
themselves, never on an instance: <code>Object.keys(user)</code> works,
<code>user.keys()</code> does not. The instance-side helpers worth
knowing are <code>at(-1)</code> (last element), <code>flat()</code>,
<code>flatMap()</code>, <code>includes()</code>,
<code>indexOf()</code>, <code>fill()</code>, <code>reverse()</code> and
<code>splice()</code>.</p>

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

<p>Walk the block top to bottom. <code>Object.keys</code>,
<code>Object.values</code> and <code>Object.entries</code> each take
one object and give back arrays — <code>["a", "b"]</code>,
<code>[1, 2]</code>, and pairs as nested arrays. Keep
<code>entries()</code> in mind: it is the bridge that lets
<code>map</code> and <code>forEach</code> see both halves of every
property. <code>Object.assign({}, {a: 1}, {b: 2})</code> merges the
later objects into the first, producing <code>{a: 1, b: 2}</code>
without touching the sources. <code>Object.freeze</code> locks an
object down: later assignments are silently ignored, so
<code>frozen.x</code> stays 1 no matter what you write to it.</p>

<p>Now the array side — predict each line's result before reading on.
<code>Array.isArray([])</code> is <code>true</code>: the reliable way
to detect arrays. <code>Array.from("abc")</code> spreads the string
into <code>["a", "b", "c"]</code>. The two-argument form builds
<code>[0, 10, 20]</code> — <code>{length: 3}</code> says "make 3
slots" and the function fills slot <code>i</code> with
<code>i * 10</code>. <code>Array.of(1, 2, 3)</code> simply makes an
array from its arguments.</p>

<p>Gotchas: <code>typeof []</code> is <code>"object"</code>, so never
detect arrays with <code>typeof</code> — use
<code>Array.isArray</code>. And do not confuse <code>splice()</code>
with <code>slice()</code>: splice <i>mutates</i> the array it is
called on and returns the removed items; slice returns a harmless
copy.</p>
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
<p><code>String</code> and <code>Number</code> are the two converters
you will use every day. Called as plain functions —
<code>String(42)</code>, <code>Number("17")</code> — they convert
values safely and predictably. Beyond conversion, each carries useful
static helpers and constants: number checks like
<code>Number.isInteger</code>, the safe-integer limit, and string
building blocks like <code>padStart</code> and <code>repeat</code>
that format text for display.</p>

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

<p>Read the block in three groups. First, conversion:
<code>String(42)</code> returns <code>"42"</code>, and
<code>String.fromCharCode(72, 105)</code> builds <code>"Hi"</code>
from two character codes (72 is H, 105 is i). Second, the instance
methods: <code>trimStart()</code> strips the left-side spaces,
<code>padStart(8, "*")</code> grows the string to 8 characters by
padding with stars on the left, <code>repeat(3)</code> copies the
string three times, <code>replaceAll</code> swaps every
<code>"l"</code> for <code>"L"</code>, and <code>at(-1)</code> counts
from the end to give <code>"o"</code>. Third, the numbers:
<code>Number.isInteger(42)</code> is <code>true</code>,
<code>Number.isNaN(NaN)</code> is the reliable NaN test,
<code>MAX_SAFE_INTEGER</code> is 9007199254740991, and
<code>EPSILON</code> is the tiny gap between neighbouring floats. The
last two lines show <code>toString(radix)</code>: 42 in binary is
<code>"101010"</code>, 255 in hex is <code>"ff"</code>.</p>

<p>Gotcha: <code>toString()</code> on a bare number literal fails —
<code>42.toString()</code> is a syntax error because that dot looks
like a decimal point. Parenthesize first: <code>(42).toString(2)</code>.
Also prefer <code>Number.isNaN(x)</code> over the old global
<code>isNaN(x)</code>, which coerces its argument and calls
<code>"abc"</code> a NaN.</p>
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
<p>When you need a square root, a rounded value or a random number,
you never create a Math object — <code>Math</code> is a static
namespace that is simply there, holding constants like
<code>Math.PI</code> and pure functions that take numbers in and
return numbers out. Every dice roll, score clamp and pixel
calculation you write will run through it.</p>

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

<p>Test yourself on that block before reading the answers. What is
<code>Math.floor(4.7)</code>? If you said 4, correct — floor always
rounds DOWN, however big the decimal. <code>Math.ceil</code> always
rounds UP (so 4.2 becomes 5), <code>Math.round</code> goes to the
nearest integer, and <code>Math.trunc</code> just cuts the decimal
part off. Keep the four apart: they differ only on negatives and .5
cases, which is exactly where bugs hide. Around them,
<code>Math.abs(-5)</code> strips the sign,
<code>Math.max</code>/<code>Math.min</code> compare any number of
arguments, <code>Math.pow(2, 10)</code> is 1024,
<code>Math.sqrt(16)</code> is 4, and <code>Math.sign(-3)</code> is
-1. Note that <code>Math.random()</code> returns a decimal from 0
inclusive up to 1 exclusive — it can give 0, never 1.</p>

<p>Because <code>Math.random()</code> hands you decimals, real code
wraps it in helpers. Predict what the next block produces:</p>

<pre class="code">// random integer between min and max (inclusive)
const random = (min, max) =&gt; Math.floor(Math.random() * (max - min + 1)) + min;

// random element from array
const pick = arr =&gt; arr[Math.floor(Math.random() * arr.length)];</pre>

<p>The <code>random(min, max)</code> helper works in three moves:
multiply by <code>(max - min + 1)</code> to stretch the range,
<code>Math.floor</code> snaps it to an integer, and <code>+ min</code>
shifts it up — so <code>random(1, 6)</code> can return 1 through 6
inclusive, a fair die. The <code>pick</code> helper multiplies by the
array length and floors, producing an index from 0 to
<code>arr.length - 1</code>, which is always safe to subscript
with.</p>

<p>Gotcha: <code>Math.random() * 10</code> can return 0 but never 10 —
forgetting the <code>+ 1</code>, or flooring too late, is the classic
off-by-one in random ranges.</p>
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
<p>Computers count time in milliseconds since one fixed instant — the
Unix epoch, midnight January 1 1970 UTC. A <code>Date</code> object is
a wrapper around such a number, plus methods to read and format it.
Create one with <code>new Date()</code> for "right now", a constructor
for a specific moment, or a string to parse. When you only need the
raw timestamp, skip the object and call <code>Date.now()</code>.</p>

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

<p>Look closely at the second line: <code>new Date(2026, 8, 27)</code>
creates September 27, 2026 — even though 8 is not September. Months
are 0-indexed (0 = January, so 8 = September) while days are
1-indexed. This asymmetry is the most famous trap in the whole date
API. The getters each extract one component: <code>getFullYear()</code>
gives 2026, <code>getMonth()</code> gives 8 (add 1 for humans),
<code>getDate()</code> is the day of the month, <code>getDay()</code>
is the day of the week (0 = Sunday), <code>getHours()</code> the hour,
and <code>getTime()</code> returns the whole moment as milliseconds
since the epoch — exactly what <code>Date.now()</code> gives without
building an object.</p>

<p>Reading components is fine for logic, but users need formatted
text. Predict what the next block prints:</p>

<pre class="code">now.toLocaleDateString("en", { weekday: "long", year: "numeric",
  month: "long", day: "numeric" });
// "Saturday, September 27, 2026"</pre>

<p><code>toLocaleDateString</code> takes a locale code and an options
object; here it asks for the long weekday, month name and 4-digit
year, producing something like "Saturday, September 27, 2026". Swap
the locale string and the same call renders the date in another
language and calendar convention — no libraries needed.</p>

<p>Gotchas: parsing strings with
<code>new Date("2026-09-27T14:30:00")</code> works, but avoid
ambiguous formats like <code>new Date("09/27/2026")</code> — string
parsing is only standardized for ISO. For date math, mutate a copy
with <code>setDate(now.getDate() + 1)</code>: it correctly rolls over
month ends and year ends for you, which manual arithmetic does
not.</p>
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
<p>A regular expression (regex) is a tiny pattern language for
searching inside strings: "one or more digits in a row", "starts with
a word, ends with .com", and so on. You write one as a literal
<code>/pattern/flags</code> or build it at runtime with
<code>new RegExp("pattern")</code>. Reach for regex when plain string
methods cannot express the match — validation, extraction, or bulk
replacement.</p>

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

<p>Walk the block. <code>/\\d+/</code> means "one or more digits in a
row" — <code>\\d</code> is a digit, <code>+</code> means one or more —
so <code>.test("abc123")</code> returns <code>true</code>: the string
contains digits somewhere. With the <code>g</code> (global) flag,
<code>"hello 42 world 99".match(/\\d+/g)</code> collects every match
into <code>["42", "99"]</code>. <code>replace</code> with
<code>/o/g</code> swaps every "o"; without <code>g</code> it would
only touch the first. The "common patterns" section reads left to
right: <code>^</code> anchors the start, <code>\\S+</code> means one or
more non-space characters, <code>@</code> is literal, and
<code>$</code> anchors the end — together a simplified email shape.
Finally, flags modify the search: <code>i</code> ignores case, so
<code>/HELLO/i.test("hello")</code> is <code>true</code>;
<code>m</code> makes <code>^</code> and <code>$</code> match line
starts and ends too.</p>

<p>Gotchas: without <code>g</code>, <code>match()</code> returns only
the first match plus extra detail — not an array of all matches.
Regexes are objects, so two identical-looking literals are never
<code>===</code>. And regexes become unreadable fast: build them in a
tester first, and keep each one short enough to explain.</p>
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
<p>Plain objects work as key-value stores, but their keys are always
strings (or symbols), they carry prototype baggage, and they have no
<code>size</code>. <b>Map</b> is the purpose-built dictionary: keys
can be numbers, booleans, objects — anything. <b>Set</b> is its
one-value cousin: a collection where every value appears at most once.
Reach for Map when keys are not strings, and for Set whenever you
need a "have I seen this before?" check.</p>

<pre class="code">const map = new Map();
map.set("name", "Ada");
map.set(42, "number key");
map.set(true, "boolean key");
map.get("name")       // "Ada"
map.has(42)           // true
map.size              // 3
map.delete("name")
map.clear()</pre>

<p>Read the Map block as a lifecycle: <code>set</code> adds or updates
an entry, <code>get</code> reads by key, <code>has</code> asks "does
this key exist?", <code>size</code> counts entries,
<code>delete</code> removes one, and <code>clear()</code> empties
everything. Notice the keys in the example — <code>"name"</code>, the
number <code>42</code>, the boolean <code>true</code> — three
different types, all legal, and <code>map.size</code> is 3 after the
first three <code>set</code> calls.</p>

<p>Now predict the Set block's output before reading on.</p>

<pre class="code">const set = new Set([1, 2, 3, 3, 2, 1]);
set.size              // 3 (duplicates removed!)
set.add(4);
set.has(2)            // true

// remove duplicates from array
const unique = [...new Set([1, 2, 2, 3, 3, 3])];  // [1, 2, 3]</pre>

<p>The constructor receives six values but keeps only unique ones, so
<code>set.size</code> is 3 — duplicates vanish silently.
<code>add</code> and <code>has</code> mirror Map's
<code>set</code> and <code>get</code>. The last line is the idiomatic
dedupe you will use constantly: spread the Set back into an array and
<code>[...new Set([1, 2, 2, 3, 3, 3])]</code> comes out as
<code>[1, 2, 3]</code>.</p>

<p><b>WeakMap/WeakSet</b> are the memory-safe variants: keys must be
objects and are held <i>weakly</i>, so when nothing else references a
key object, garbage collection removes its entry automatically. Use
them for caches and private metadata that should not outlive their
owners.</p>

<p>Gotcha: <code>object[key]</code> coerces keys to strings — using an
object as a key becomes the literal <code>"[object Object]"</code>.
If you catch yourself serializing keys to strings to fake a Map,
stop and use a real Map.</p>
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
<p>Every API you will ever call speaks JSON: a text format that looks
like a JavaScript object but is only a string. Networks carry strings,
not objects, so your app converts constantly in both directions —
<b>serializing</b> an object into a string with
<code>JSON.stringify</code>, and <b>parsing</b> a string back into an
object with <code>JSON.parse</code>. Two methods, all of
JSON.</p>

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

<p>Follow the block. <code>stringify(user)</code> turns the object
into one long string with quoted keys. <code>parse</code> reverses it
— afterwards <code>parsed.name</code> is the string
<code>"Ada"</code> again. The third call fills stringify's two
optional arguments: <code>null</code> (a key filter, unused here) and
<code>2</code>, the indent width — that pretty-prints the output with
line breaks, exactly what you want in logs. The last line passes an
array as that second argument instead: an allow-list, so only
<code>"name"</code> and <code>"active"</code> survive serialization.</p>

<p>JSON is deliberately tiny, and stringify follows its rules:
functions and <code>undefined</code> are dropped, <code>Date</code>
objects become ISO strings, circular references throw a TypeError,
and there are no comments or trailing commas.</p>

<p>Gotcha: <code>JSON.parse(JSON.stringify(obj))</code> was the
classic deep-clone trick, but it silently destroys anything JSON
cannot represent — Dates, Maps, Sets, functions. Modern engines give
you <code>structuredClone(obj)</code>, which handles all of those;
reserve JSON round-tripping for when you truly want plain
data.</p>
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
<p>When something goes wrong in JavaScript, what gets thrown is an
object — an <code>Error</code> carrying a <code>message</code> and a
<code>name</code>. The built-ins name the kind of failure:
<code>TypeError</code> for wrong value types,
<code>ReferenceError</code> for unknown variables,
<code>RangeError</code> for out-of-range numbers,
<code>SyntaxError</code> for unparseable code. Extending
<code>Error</code> lets a <code>catch</code> block tell YOUR failures
apart from the engine's — and carry extra context.</p>

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

<p>Walk the class. <code>extends Error</code> inherits all Error
behaviour, including the stack trace. <code>super(message)</code>
passes the message up to the parent constructor — skip it and
<code>e.message</code> comes out empty. Setting
<code>this.name</code> makes logs print
<code>ValidationError</code> instead of the generic
<code>Error</code>, and the extra <code>field</code> property carries
context a generic error cannot. In the <code>catch</code> block,
<code>instanceof</code> routes the error, so this code logs
<code>Field "email": Invalid email format</code>.</p>

<p><b>Promise</b> is a placeholder for a value that will exist later —
the foundation of async JavaScript, covered deeply in Phase 7. You
will meet promises as the return value of <code>fetch()</code> and
every modern async API. Two facts to hold onto now: a promise starts
<b>pending</b>, then settles into <b>fulfilled</b> (with a value) or
<b>rejected</b> (with an error) — and once settled, its state never
changes again.</p>

<p>Gotcha: never <code>throw "a string"</code> — a string has no
<code>.message</code> and no stack trace, and
<code>instanceof</code> checks cannot route it. Always throw real
<code>Error</code> instances.</p>
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
<p>JavaScript runs on a single thread: one line at a time, nothing in
parallel. <b>Synchronous</b> code respects that fully — each line
waits for the previous one to finish. Fine for arithmetic,
disastrous for slow work: a network request taking 2 seconds would
freeze the page for 2 seconds. <b>Asynchronous</b> code schedules
work for later and moves on, keeping the thread free. Predict what
the block below prints before you read the answer.</p>

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

<p>The first group prints <code>"1"</code>, <code>"2"</code>,
<code>"3"</code> in order — no surprises. But the second group prints
<code>"start"</code>, then <code>"end"</code>, and only then
<code>"later"</code> — even though the timeout delay is 0! That is
the event loop at work: JavaScript always finishes ALL synchronous
code first, then processes queued callbacks. A
<code>setTimeout</code> callback, however short its delay, is queued
for a later turn.</p>

<p>Two queues feed that loop: the <b>macrotask queue</b> (timers,
events) and the <b>microtask queue</b> (promise callbacks). After
each slice of synchronous code, the loop drains every microtask
before running the next macrotask — which is why promise callbacks
execute before <code>setTimeout</code> callbacks scheduled at the
same time.</p>

<p>Gotcha: a long synchronous loop — say, building a 100,000-row
table in one go — blocks everything: clicks, animation, even
rendering. If a chunk of work cannot finish in about 50ms, split it
up or move it off the thread.</p>
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
<p>How do you run code after a slow operation finishes? The oldest
answer: pass a <b>callback</b> — a function the operation calls when
it is done. Callbacks still power <code>setTimeout</code> and event
listeners, but chained for multi-step work they nest indentation
deeper and deeper, the shape programmers call <b>callback
hell</b>:</p>

<pre class="code">// callback hell (the problem)
getUser(id, (user) =&gt; {
  getPosts(user.id, (posts) =&gt; {
    getComments(posts[0].id, (comments) =&gt; {
      console.log(comments);   // deeply nested!
    });
  });
});</pre>

<p>Each level exists only to wait for the previous one: to get posts
you need a user, to get comments you need the first post. Three
steps in, the code is three brackets deep — and error handling is
missing entirely.</p>

<p>A <b>Promise</b> is the fix: an object representing a value that
will arrive later. It starts <b>pending</b>, then settles as
<b>fulfilled</b> (with a value) or <b>rejected</b> (with an error) —
and once settled, its state never changes. You will mostly
<i>consume</i> promises, but here is what creating one looks
like:</p>

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

<p>The function passed to <code>new Promise</code> runs immediately
and receives two tools: <code>resolve</code> to finish successfully,
<code>reject</code> to fail. Here a 1-second timer decides which one
to call. The consumer side reads top-down: <code>.then()</code> runs
on fulfillment, <code>.catch()</code> on rejection — so this prints
<code>"got: data!"</code>.</p>

<p>Promises chain: each <code>.then()</code> receives the previous
one's return value, so a flat chain of links replaces nested
callbacks — the same three steps, one indentation level, errors
handled in one place.</p>

<p>Gotcha: if you forget to <code>return</code> inside a
<code>.then()</code>, the next link receives
<code>undefined</code> instead of your data — the most common
broken-chain bug.</p>
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
<p>Every promise comes with three instance methods, and together they
form a pipeline you read top to bottom: <code>.then()</code> handles
success, <code>.catch()</code> handles failure,
<code>.finally()</code> runs either way. The key mental model is that
each method returns a NEW promise — that is why you can keep linking
them into a chain.</p>

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

<p>Trace the happy path: <code>fetchData()</code> resolves, the first
<code>.then()</code> logs the data and returns <code>data.id</code>,
the second <code>.then()</code> receives that id and logs it, and
<code>.finally()</code> prints <code>"done"</code>. Now trace a
failure anywhere above — a rejected <code>fetchData()</code> or a
thrown error inside any <code>.then()</code>: execution jumps past
the remaining <code>.then()</code> links straight to
<code>.catch()</code>, which logs <code>"failed: ..."</code>, and
<code>.finally()</code> still runs. <code>.catch()</code> is like a
<code>try/catch</code> wrapped around everything above it.</p>

<p><code>.finally()</code> is deliberately limited: it receives no
result, and whatever it returns is ignored (unless it throws). It
exists for cleanup that must happen regardless of outcome — hiding a
loading spinner, closing a connection, re-enabling a button.</p>

<p>Gotchas: a <code>.catch()</code> only guards what is ABOVE it in
the same chain. Writing <code>p.then(a); p.catch(b)</code> creates
two separate chains, so <code>b</code> will not catch errors thrown
in <code>a</code> — chain them: <code>p.then(a).catch(b)</code>.</p>
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
<p>Real apps rarely await one thing at a time — a dashboard needs
users, posts and comments. Awaiting them one by one wastes time, so
JavaScript gives you four static methods for running promises
<b>in parallel</b> and combining the results. They differ in one
question each: who decides when the whole thing settles, and what
counts as success.</p>

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

<p><code>Promise.all</code> is the everyday choice: it resolves with
an array of every value — here destructured into
<code>users</code>, <code>posts</code>, <code>comments</code> — but
it is fail-fast: if ANY input rejects, the whole call rejects with
that first error and the other results are lost.
<code>Promise.allSettled</code> never rejects; it waits for everyone
and reports each outcome as
<code>{status: "fulfilled", value: ...}</code> or
<code>{status: "rejected", reason: ...}</code>.
<code>Promise.race</code> settles with whichever promise settles
first — even a rejection, which is what makes it good for timeouts.
<code>Promise.any</code> waits for the first SUCCESS, ignoring
rejections along the way, and rejects only when every input has
failed.</p>

<ul>
<li><b>all</b> — fail-fast: one rejection rejects the whole thing</li>
<li><b>allSettled</b> — never rejects; gives status for each</li>
<li><b>race</b> — first settled (even if rejected) wins</li>
<li><b>any</b> — first fulfilled wins; rejects only if ALL reject</li>
</ul>

<p>Rule of thumb: use <code>all</code> when the results only make
sense together, <code>allSettled</code> for independent operations
you want a full report on, <code>race</code> for timeouts,
<code>any</code> for fallbacks across mirrors.</p>

<p>Gotcha: the promises in the array START the moment you build it —
so pass actual calls like <code>fetchUsers()</code>, not bare
function references like <code>fetchUsers</code> (that waits for
nothing useful). And <code>Promise.all([])</code> resolves
immediately with an empty array.</p>
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
<p><code>async/await</code> is friendlier syntax for promises: code
that reads top-to-bottom like synchronous code while staying fully
asynchronous underneath. Mark a function <code>async</code> and you
may use <code>await</code> inside it to pause at any promise until
it settles. Chains of <code>.then()</code> become plain lines, and
errors move back into the familiar <code>try/catch</code>.</p>

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

<p>Three facts unlock the block. First, an <code>async</code>
function ALWAYS returns a promise: <code>getData()</code> returning
<code>42</code> really hands callers <code>Promise.resolve(42)</code>.
Second, <code>await</code> pauses only that function — the thread is
not blocked, so the rest of the app keeps running while
<code>fetchUser(1)</code> is in flight. Third, a rejected awaited
promise throws at exactly the <code>await</code> line, which is why
<code>try/catch/finally</code> works just like synchronous
code.</p>

<p>Now the subtlety: <code>await</code> is sequential. In
<code>main()</code>, <code>fetchPosts</code> does not even start
until <code>fetchUser</code> finishes. If the two calls are
independent, start them together and await the pair — the
<code>efficient()</code> example passes both promises to
<code>Promise.all</code>, so they run in parallel and the total wait
is the slower one, not the sum.</p>

<p><code>await</code> is only valid inside <code>async</code>
functions (or top-level in modules). Gotcha: never
<code>await</code> inside a <code>forEach</code> callback — the loop
does not wait. Use <code>for...of</code> when each step depends on
the previous one.</p>
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
<p>Async errors are sneaky: a <code>try/catch</code> around a promise
call without <code>await</code> catches nothing, because the error
happens long after the catch block has finished. Each async pattern
has its own error channel — <code>.catch()</code> for chains,
<code>try/catch</code> for <code>await</code> — and mixing them up
is the number-one source of "unhandled" errors.</p>

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

<p>The first two sections are the correct pair: with plain promises,
attach <code>.catch()</code>; with <code>await</code>, wrap the call
in <code>try/catch</code> — the rejection surfaces as a thrown error
at exactly the <code>await</code> line. Now study
<code>buggy()</code>: it calls <code>riskyOperation()</code> without
<code>await</code>, so all it receives is a promise object that
starts failing in the background. The <code>catch</code> block never
runs — the error is unhandled. The fix is one word:
<code>await</code>.</p>

<p>The <code>fetchAll()</code> section covers the parallel case.
<code>Promise.all</code> fails fast, so for independent operations
where partial success is acceptable, use
<code>Promise.allSettled</code>: it returns a report you can filter
on <code>status</code>, splitting results into
<code>values</code> and <code>errors</code> like the example
does.</p>

<p>Always give async errors a home: an unhandled promise rejection
crashes modern Node.js and logs ugly console errors in browsers. As
a safety net, register an <code>unhandledrejection</code> listener on
<code>window</code> so strays get reported instead of lost:
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
<p>Scripts pasted into one giant <code>&lt;script&gt;</code> tag share
one global scope: any variable can collide with any other, and load
order is a manual guessing game. <b>ES modules</b> solve this — each
file is its own scope that explicitly <code>export</code>s what it
wants to share, and importers say exactly what they take. The
dependency graph becomes visible, and unused branches can even be
removed at build time (tree-shaking).</p>

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

<p>The export side has two flavours. <b>Named exports</b> —
<code>export const PI</code>, <code>export function circleArea</code>
— can be numerous per file and are imported by their exact names
inside braces. The <b>default export</b> is a module's single "main
thing"; the importer picks any local name for it and writes no
braces. Then import in whichever style fits: pull the pieces you
need (<code>{ PI, circleArea }</code>), or grab the whole module as
one namespace object (<code>* as math</code>) and read
<code>math.PI</code> from it. Predict the last three lines: they log
<code>3.14159</code>, then <code>12.57</code> (PI times 2 squared,
rounded), then <code>3.14159</code> again via the namespace.</p>

<p>Modules also change runtime behaviour for free: they are
<b>strict mode</b> by default, <b>deferred</b> (they run after HTML
parsing, like <code>defer</code>), and <b>cached</b> — the first
import executes the module, and every other importer receives that
same shared instance. Together these give you code organization,
dependency management, and tree-shaking.</p>

<p>In the browser, load one with
<code>&lt;script type="module" src="app.js"&gt;</code>. In Node.js,
use the <code>.mjs</code> extension or set
<code>"type": "module"</code> in package.json.</p>

<p>Gotcha: browser imports need the full path —
<code>from './math'</code> fails, <code>from './math.js'</code>
works. Unlike bundlers, the browser does no extension guessing, and
it resolves relative paths against the importing file.</p>
""",
            },
            {
                "title": "Dynamic import() & Module Resolution",
                "html": """
<p>Static imports at the top of a file all load up front — even code
your user may never touch, like a charting library behind a button or
an admin panel behind a login. <b>Dynamic import</b> flips that:
calling <code>import('./module.js')</code> downloads and evaluates
the module at that moment and returns a <b>Promise</b> for its
namespace. This is how code splitting and lazy loading work.</p>

<pre class="code">// static import: loaded immediately
import { heavy } from './heavy.js';

// dynamic import: loaded when needed
button.addEventListener('click', async () =&gt; {
  const { chart } = await import('./chart.js');
  chart.render();     // chart.js only loaded now!
});</pre>

<p>Compare the two halves. The static
<code>import { heavy } from './heavy.js'</code> is resolved and
loaded before your first line runs — its network cost is paid on
every visit. The dynamic version sits inside a click handler:
nothing about <code>chart.js</code> is fetched until the user
clicks, then <code>await</code> pauses until the module arrives, and
its exports are destructured straight out of the resolved namespace.
Users who never click never pay the download.</p>

<p>Resolution follows browser rules worth knowing. Relative paths
like <code>./utils.js</code> resolve against the importing file's
URL. Bare specifiers such as <code>lodash</code> do not work in raw
browsers — an <b>import map</b> must map the name to a URL first.
And the file extension is required, because the browser does no
guessing. MDN's guide covers the finer details.</p>

<p>Gotcha: a dynamic import can fail at runtime — offline, bad path,
server error — so its promise REJECTS. Wrap it in
<code>try/catch</code> and show the user something, instead of
letting a lazy chunk fail silently.</p>
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
