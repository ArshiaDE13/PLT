"""Chapters 24-27 of the course, distilled from the Python 3.14
HowTo documentation.

HowTos are short, practical guides — exactly the course's style. Of
the 28 files, these chapters cover the ones a builder reaches for
most: sorting, regular expressions, deeper argparse/logging/enum,
and unicode + a first look at async. The rest (cporting, gdb_helpers,
perf_profiling, free-threading, ...) are niche/advanced and skipped,
per the course philosophy.
"""

CHAPTERS_E = [
    # ------------------------------------------------------------------ 24
    {
        "id": "ch24",
        "title": "Sorting Like a Pro",
        "title_fa": "مرتب‌سازی حرفه‌ای",
        "emoji": "\U0001f5c2\ufe0f",
        "lessons": [
            {
                "title": "sorted() and key functions",
                "html": """
<p>Sorting is one of the most-used skills in real code. Python gives
you two tools: <code>list.sort()</code>, which sorts the list
<b>in place</b> (and returns <code>None</code>), and the
<code>sorted()</code> function, which returns a <b>new</b> sorted
list from any iterable:</p>

<pre class="code">nums = [5, 2, 3, 1, 4]
sorted(nums)          # -&gt; [1, 2, 3, 4, 5]   (new list)
nums.sort()           # sorts nums itself, returns None

sorted({3: 'x', 1: 'y'})   # works on ANY iterable: -&gt; [1, 3]</pre>

<p>The superpower is the <code>key</code> parameter: a function that
turns each item into the value you actually compare. It runs exactly
once per item, so it's fast:</p>

<pre class="code">words = "This is a test string".split()
sorted(words, key=str.casefold)   # case-insensitive

students = [('john', 'A', 15), ('jane', 'B', 12), ('dave', 'B', 10)]
sorted(students, key=lambda s: s[2])   # sort tuples by age</pre>

[[diag:sorting_flow]]

<p>Want biggest first? <code>reverse=True</code>:</p>

<pre class="code">sorted(students, key=lambda s: s[2], reverse=True)</pre>

<p>Python's sort is <b>stable</b>: records with equal keys keep their
original order. That means you can sort by two fields in two passes —
the secondary sort first, then the primary:</p>

<pre class="code">s = sorted(students, key=lambda s: s[2])          # by age
sorted(s, key=lambda s: s[1], reverse=True)       # then by grade</pre>

<p>When you only need the top few, skip the full sort:
<code>min()</code>, <code>max()</code>,
<code>heapq.nsmallest()</code> and <code>heapq.nlargest()</code>
do a single pass and keep only what they need.</p>
""",
            },
            {
                "title": "operator helpers & sorting objects",
                "html": """
<p>Writing <code>lambda s: s[2]</code> all day is tiresome — the
<code>operator</code> module has ready-made accessors that are also
faster:</p>

<pre class="code">from operator import itemgetter, attrgetter

sorted(students, key=itemgetter(2))            # index 2
sorted(students, key=itemgetter(1, 2))         # grade, then age

sorted(student_objects, key=attrgetter('age'))  # attribute
sorted(student_objects, key=attrgetter('grade', 'age'))</pre>

<p><code>itemgetter</code> works on anything subscriptable (tuples,
dicts, lists); <code>attrgetter</code> works on objects with
attributes — including dataclasses and namedtuples, so define your
records with those and sorting gets easy.</p>

<p>Sorting your <b>own</b> class: the sort routines compare with
<code>&lt;</code>, so implement <code>__lt__</code> and use the
<code>@functools.total_ordering</code> decorator to fill in the
rest:</p>

<pre class="code">from functools import total_ordering

@total_ordering
class Student:
    def __init__(self, name, age):
        self.name, self.age = name, age
    def __lt__(self, other):
        return self.age &lt; other.age
    def __eq__(self, other):
        return self.age == other.age

sorted([Student('ada', 36), Student('guido', 68)])</pre>

<p>Three traps from the docs, with easy fixes:</p>

<ul>
<li><b>Mixed types</b> raise <code>TypeError</code> — coerce first:
  <code>sorted(map(str, data))</code>.</li>
<li><b><code>NaN</code></b> compares unordered with everything —
  filter it out first: <code>sorted(x for x in data if not
  isnan(x))</code>.</li>
<li><b><code>None</code></b> isn't comparable — drop it:
  <code>sorted(x for x in data if x is not None)</code>.</li>
</ul>
""",
            },
        ],
        "quiz": [
            {
                "type": "mc",
                "question": "What's the difference between sorted() and list.sort()?",
                "options": [
                    "sorted() returns a new list; sort() modifies the list in place and returns None",
                    "they are identical",
                    "sort() returns a new list; sorted() modifies in place",
                    "sorted() only works on numbers",
                ],
                "answer": 0,
                "explain": "list.sort() mutates the list and returns None; sorted() accepts any iterable and builds a new list.",
            },
            {
                "type": "blank",
                "question": "Sort case-insensitively: sorted(words, key=str.____)",
                "answers": ["casefold"],
                "explain": "key=str.casefold makes comparisons case-insensitive — the docs' recommended way.",
            },
            {
                "type": "codefill",
                "question": "Sort these tuples by age (index 2) using itemgetter:",
                "code": [
                    "from operator import itemgetter",
                    "students = [('john', 'A', 15), ('jane', 'B', 12), ('dave', 'B', 10)]",
                    "by_age = sorted(students, key=itemgetter(",
                    {"blank": "2", "answers": ["2"], "hint": "the index of the age field"},
                    "))",
                    "print(by_age[0][0])",
                ],
                "explain": "itemgetter(2) picks the third element of each tuple (the age), so the list sorts by age: dave, jane, john.",
            },
            {
                "type": "mc",
                "question": "A sort being 'stable' means:",
                "options": [
                    "equal-key records keep their original relative order",
                    "it never raises exceptions",
                    "the result is always deterministic across Python versions",
                    "only lists can be sorted",
                ],
                "answer": 0,
                "explain": "Stability lets you sort by secondary keys first, then primary — equal primaries keep the secondary order.",
            },
        ],
    },

    # ------------------------------------------------------------------ 25
    {
        "id": "ch25",
        "title": "Regular Expressions",
        "title_fa": "عبارت‌های باقاعده",
        "emoji": "\U0001f9f5",
        "lessons": [
            {
                "title": "Patterns — a mini-language inside Python",
                "html": """
<p>Regular expressions ("regexes") are a tiny programming language
for describing <b>patterns of text</b>. The <code>re</code> module
lets you ask: does this string contain a phone number? Extract all
the prices? Split on commas-or-semicolons?</p>

<p>Patterns are written as <b>raw strings</b> so backslashes stay
literal — no double-escaping:</p>

<pre class="code">import re
phone = r"\\d{3}-\\d{4}"     # three digits, dash, four digits</pre>

<p>Core building blocks:</p>

<pre class="code">r"test"      # letters match themselves
r"[a-z]"     # character class: any lowercase letter
r"[^0-9]"    # complement: anything that is NOT a digit
r"\\d"        # any digit   (same as [0-9])
r"\\w"        # letter/digit/underscore
r"\\s"        # whitespace (space, tab, newline)
r"."         # any character except newline</pre>

[[diag:regex_flow]]

<p>Quantifiers say <b>how many</b>:</p>

<pre class="code">r"ca*t"     # 'c', then ZERO or more 'a', then 't'  -&gt; ct, cat, caaat
r"ca+t"     # one or more 'a'
r"ca?t"     # zero or one 'a'
r"\\d{3}"    # exactly three digits
r"\\d{2,4}"  # two to four digits</pre>

<p>Anchors pin the match to a position: <code>^</code> is the start
of the string, <code>$</code> the end.</p>

<pre class="code">r"^\\d{5}$"   # a whole line of exactly 5 digits (a zip code)</pre>

<p>Greedy quantifiers grab as much as they can, then back off if the
rest of the pattern needs it. When text gets complicated, remember
the docs' advice: if your pattern turns into a monster, plain Python
string code is often clearer and just as good.</p>
""",
            },
            {
                "title": "re functions — search, findall, sub",
                "html": """
<p>Now the functions that run your patterns:</p>

<pre class="code">import re

re.search(r"\\d+", "Order 42 shipped")   # find the FIRST match
re.findall(r"\\d+", "3 apples, 12 pears") # -&gt; ['3', '12']
re.sub(r"\\d+", "#", "a1 b22")            # replace -&gt; 'a# b#'
re.split(r"[,;]", "a,b;c")                # -&gt; ['a', 'b', 'c']</pre>

<p><code>search()</code> scans anywhere in the string and returns a
<b>match object</b> (or <code>None</code>) — check it like a
boolean. <code>match()</code> only checks the very start,
<code>fullmatch()</code> requires the whole string.</p>

<pre class="code">m = re.search(r"\\d+", "Order 42")
if m:
    print(m.group())     # -&gt; '42'
    print(m.start(), m.end())   # -&gt; 6 8</pre>

<p><b>Groups</b> capture parts of a match with parentheses:</p>

<pre class="code">m = re.search(r"(\\d+)-(\\d+)", "call 12-34")
m.group(1)     # -&gt; '12'   first group
m.group(2)     # -&gt; '34'   second group
m.groups()     # -&gt; ('12', '34')</pre>

<p>Compile a pattern you reuse many times — it's cached anyway, but
compiling keeps your code tidy and lets you set flags once:</p>

<pre class="code">pattern = re.compile(r"\\w+", re.IGNORECASE)
pattern.findall("Hello WORLD")   # -&gt; ['Hello', 'WORLD']</pre>

<p>If you reach for <code>\\</code> spam often, pause: simple cases
like "starts with" / "ends with" are one call on plain strings —
<code>startswith()</code>, <code>endswith()</code>,
<code>split()</code>, <code>replace()</code>.</p>
""",
            },
        ],
        "quiz": [
            {
                "type": "mc",
                "question": "Why write regex patterns as raw strings like r'\\d+'?",
                "options": [
                    "backslashes are kept literally, so pattern escapes aren't double-processed",
                    "raw strings match faster",
                    "it's required for the re module to work at all",
                    "it turns the pattern into bytes",
                ],
                "answer": 0,
                "explain": "In a raw string, \\d stays \\d. In a normal string you'd have to write '\\\\d' to get the same thing.",
            },
            {
                "type": "blank",
                "question": "A pattern for one or more digits: r'____'",
                "answers": ["\\d+"],
                "explain": "\\d matches a digit, + means one or more — so r'\\d+' matches any run of digits.",
            },
            {
                "type": "codefill",
                "question": "Extract all the words from a string:",
                "code": [
                    "import re",
                    "words = re.findall(r'",
                    {"blank": "\\w+", "answers": ["\\w+", "\\w"], "hint": "one or more word characters"},
                    "', 'hello brave world')",
                    "print(words)",
                ],
                "explain": "\\w+ matches one or more letters/digits/underscores, so findall returns ['hello', 'brave', 'world'].",
            },
            {
                "type": "mc",
                "question": "Which re function returns a list of every non-overlapping match?",
                "options": ["re.search", "re.match", "re.findall", "re.sub"],
                "answer": 2,
                "explain": "findall returns a list of all matches; search and match return a single match object; sub replaces.",
            },
        ],
    },

    # ------------------------------------------------------------------ 26
    {
        "id": "ch26",
        "title": "Deeper Tools: argparse, logging, enum",
        "title_fa": "ابزارهای پیشرفته‌تر: argparse، logging و enum",
        "emoji": "\U0001f527",
        "lessons": [
            {
                "title": "argparse & logging, properly",
                "html": """
<p>Chapter 23 introduced <code>argparse</code> and
<code>logging</code>. Real tools use more of them. First,
<code>argparse</code> beyond simple flags:</p>

<pre class="code">import argparse

parser = argparse.ArgumentParser()
parser.add_argument('path')                # POSITIONAL argument
parser.add_argument('-n', '--number', type=int, default=10)
parser.add_argument('--color', choices=['red', 'green', 'blue'])
parser.add_argument('--verbose', action='store_true')
args = parser.parse_args()

print(args.path, args.number, args.color)</pre>

<p><code>type=int</code> converts the value automatically
(<code>--number 5</code> gives the int <code>5</code>, not the
string <code>'5'</code>). <code>choices=</code> rejects anything
outside the list with a clear error. <code>action='store_true'</code>
turns a flag's presence into <code>True</code>.</p>

[[diag:argparse_deep]]

<p>Now <code>logging</code>. The five levels, in order of severity:</p>

<pre class="code">DEBUG &lt; INFO &lt; WARNING &lt; ERROR &lt; CRITICAL</pre>

<p>The default level is <code>WARNING</code>, so plain
<code>logging.info(...)</code> prints nothing until you configure it.
The docs' rule of thumb: use <code>print()</code> for ordinary
console output, a logger for events worth tracking, and raise an
exception for errors. To log to a file with a timestamp:</p>

<pre class="code">import logging

logging.basicConfig(
    filename='app.log',
    encoding='utf-8',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
)

logging.info('started')     # -&gt; 2026-08-16 09:14:02,331 INFO started</pre>

<p>In bigger programs, create your own logger per module with
<code>logger = logging.getLogger(__name__)</code> — that's the
idiom the howto recommends, because then you control each module's
logging level independently.</p>
""",
            },
            {
                "title": "enum — named constants done right",
                "html": """
<p>Constants that are just numbers or strings are a classic bug
source — is <code>1</code> red, or is it on? The <code>enum</code>
module gives you real named members:</p>

<pre class="code">from enum import Enum

class Color(Enum):
    RED = 1
    GREEN = 2
    BLUE = 3

Color.RED          # -&gt; &lt;Color.RED: 1&gt;
Color.RED.name     # -&gt; 'RED'
Color.RED.value    # -&gt; 1
list(Color)        # -&gt; [&lt;Color.RED: 1&gt;, ...]  (iteration order)</pre>

<p>Members are singletons: <code>Color.RED is Color.RED</code> is
<code>True</code>, so comparisons are simple and safe:</p>

<pre class="code">def describe(color):
    if color is Color.RED:
        return 'stop'
    return 'go'

describe(Color.RED)     # -&gt; 'stop'</pre>

<p>Don't want to invent values? <code>auto()</code> numbers them for
you:</p>

<pre class="code">from enum import Enum, auto

class Status(Enum):
    PENDING = auto()
    RUNNING = auto()
    DONE = auto()

Status.DONE.value    # -&gt; 3</pre>

<p>Use an enum anywhere a fixed set of choices exists — days of the
week, file modes, HTTP statuses, player classes — and typos become
<code>AttributeError</code>s instead of silent wrong behavior.</p>
""",
            },
        ],
        "quiz": [
            {
                "type": "mc",
                "question": "Which add_argument options restrict values to a fixed set?",
                "options": ["type & default", "choices & required", "nargs & action", "dest & help"],
                "answer": 1,
                "explain": "choices=['red','green'] rejects any other value; required=True forces the argument to be given.",
            },
            {
                "type": "order",
                "question": "Put the argparse pipeline in the correct order:",
                "lines": [
                    "import argparse",
                    "parser = argparse.ArgumentParser()",
                    "parser.add_argument('--name')",
                    "args = parser.parse_args()",
                ],
                "explain": "Create the parser, declare each argument, then parse_args() reads the command line into the namespace.",
            },
            {
                "type": "codefill",
                "question": "Configure logging to a file at the most verbose level:",
                "code": [
                    "import logging",
                    "logging.basicConfig(filename='app.log', level=logging.",
                    {"blank": "DEBUG", "answers": ["DEBUG"], "hint": "the lowest, most verbose level"},
                    ")",
                    "logging.info('started')",
                ],
                "explain": "level=logging.DEBUG makes everything from DEBUG upward visible; default is WARNING, which would hide the INFO line.",
            },
            {
                "type": "blank",
                "question": "Number enum members automatically with: class Color(Enum): RED = ____()",
                "answers": ["auto"],
                "explain": "auto() assigns the next value automatically — PENDING=1, RUNNING=2, DONE=3 in order.",
            },
        ],
    },

    # ------------------------------------------------------------------ 27
    {
        "id": "ch27",
        "title": "Unicode & a First Look at Async",
        "title_fa": "یونیکد و اولین نگاه به Async",
        "emoji": "\U0001f30d",
        "lessons": [
            {
                "title": "Unicode — text, bytes, and UTF-8",
                "html": """
<p>Every character you can type — including 😀 — has a number
assigned by the Unicode standard. That number is its <b>code
point</b>, written like <code>U+1F600</code>. Python strings are
sequences of code points, so they hold any language, emoji included,
with zero extra work:</p>

<pre class="code">s = "héllo 😀"
len(s)          # -&gt; 7  (each character counts as one)</pre>

<p>But files and networks deal in <b>bytes</b>, so the string must
be <b>encoded</b> — translated to bytes by a character encoding.
The dominant one is <b>UTF-8</b>, which represents every code point
using 1 to 4 bytes and keeps plain ASCII identical to itself:</p>

<pre class="code">text = "héllo"
raw = text.encode('utf-8')      # str -&gt; bytes
raw                             # -&gt; b'h\\xc3\\xa9llo'
back = raw.decode('utf-8')      # bytes -&gt; str
back == text                    # -&gt; True</pre>

[[diag:unicode_bytes]]

<p>That one idea explains most "encoding" bugs you'll ever see:</p>

<ul>
<li><code>UnicodeDecodeError</code> — you decoded bytes with the
  wrong encoding (or none).</li>
<li><code>UnicodeEncodeError</code> — you tried to encode a
  character the target encoding can't represent (e.g. emoji in
  ASCII).</li>
<li>Mojibake — text was encoded with one encoding and decoded with
  another.</li>
</ul>

<p>Modern Python defaults to UTF-8 nearly everywhere, and
<code>open()</code> accepts an <code>encoding=</code> argument —
<code>open('f.txt', encoding='utf-8')</code>. The golden rule:
<b>decode on input, encode on output, and work in strings in
between.</b></p>
""",
            },
            {
                "title": "A first look at asyncio",
                "html": """
<p>Some programs wait a lot — for network replies, file reads, user
input. While waiting, the CPU sits idle. <b>asyncio</b> lets one
program juggle many waiting tasks, like a host seating tables at a
restaurant: seat one, attend another, keep everyone moving.</p>

<p>You write <b>coroutines</b> — functions declared with
<code>async def</code> that can pause themselves with
<code>await</code>:</p>

<pre class="code">import asyncio

async def fetch(url):
    print('fetching', url)
    await asyncio.sleep(1)      # pretend it's a slow network call
    return url + ' data'

async def main():
    # run two fetches AT THE SAME TIME
    results = await asyncio.gather(
        fetch('a.com'),
        fetch('b.com'),
    )
    print(results)

asyncio.run(main())     # the entry point</pre>

[[diag:async_loop]]

<p><code>asyncio.run(main())</code> starts the <b>event loop</b>,
which schedules coroutines: whenever one hits <code>await</code>,
the loop switches to another that's ready. The two fetches take
~1 second total, not 2 — that's the whole point.</p>

<p>Four things worth knowing before you dive deeper:</p>

<ul>
<li><code>await</code> only works inside <code>async def</code> —
  it's a syntax error elsewhere.</li>
<li>If a coroutine never awaits, it never runs — call it from
  <code>gather()</code> or the loop, not as a plain function.</li>
<li>As of 3.11, <code>asyncio.TaskGroup</code> is the recommended
  way to manage several tasks with proper cleanup.</li>
<li>Reading a file or doing CPU math does NOT release the loop —
  async shines for I/O waits, not number crunching.</li>
</ul>

<p>Asyncio is a big topic; this is just the mental model. When you
need it (web servers, scrapers, chat bots), start with
<code>asyncio.run</code> + <code>gather</code> and grow from
there.</p>
""",
            },
        ],
        "quiz": [
            {
                "type": "mc",
                "question": "What is a Unicode code point?",
                "options": [
                    "a byte in the encoded file",
                    "the unique number Unicode assigns to a character",
                    "a glyph, i.e. a shape drawn by a font",
                    "another name for UTF-8",
                ],
                "answer": 1,
                "explain": "A code point is the integer (like U+1F600) that identifies a character; encodings map code points to bytes.",
            },
            {
                "type": "blank",
                "question": "Turn a str into bytes: text.____('utf-8')",
                "answers": ["encode"],
                "explain": "encode() converts str to bytes; decode() converts bytes back to str. Decode on input, encode on output.",
            },
            {
                "type": "mc",
                "question": "Which keyword turns a function into a coroutine?",
                "options": ["await", "async def", "yield", "defer"],
                "answer": 1,
                "explain": "async def declares a coroutine; await is the keyword used inside it to pause and wait.",
            },
            {
                "type": "codefill",
                "question": "Run a coroutine with the event loop entry point:",
                "code": [
                    "import asyncio",
                    "",
                    "async def main():",
                    "    print('hi')",
                    "",
                    "asyncio.",
                    {"blank": "run(main())", "answers": ["run(main())", "run(main)"], "hint": "the function that starts the event loop"},
                ],
                "explain": "asyncio.run(main()) creates the event loop, runs the coroutine to completion, and cleans up.",
            },
        ],
    },
]
