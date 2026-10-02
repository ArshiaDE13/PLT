"""Chapters 20-23 of the course, distilled from the Python 3.14
Library Reference.

The library is huge, so — following the course philosophy
(Tutorial -> Practice -> Project -> Library -> HowTo -> Reference) —
these chapters teach the everyday-toolkit modules a learner reaches
for when building real projects, not the whole reference.
"""

CHAPTERS_D = [
    # ------------------------------------------------------------------ 20
    {
        "id": "ch20",
        "title": "Files & Paths (pathlib)",
        "title_fa": "فایل‌ها و مسیرها (pathlib)",
        "emoji": "\U0001f4be",
        "lessons": [
            {
                "title": "Meet Path — paths without string surgery",
                "html": """
<p>For years, paths meant juggling strings and slashes &mdash; and the
string code that joined <code>'data' + '/' + name</code> broke the day
your script moved from Windows (backslash) to Unix (slash). The
<code>pathlib</code> module ended all that: paths are <b>objects</b>
with methods. Create one with <code>Path(...)</code>, then build
children with the <code>/</code> operator:</p>

<pre class="code">from pathlib import Path

p = Path('data') / 'notes' / 'todo.txt'
p           # -&gt; PosixPath('data/notes/todo.txt') on Unix
            # -&gt; WindowsPath('data\\notes\\todo.txt') on Windows</pre>

<p>Walk through it: the <code>/</code> operator glues segments together,
and the printed class name shows which platform flavor you got &mdash;
same code, correct separators everywhere. The same object adapts to the
platform you run on. Common starting points: <code>Path.cwd()</code>
(current directory) and <code>Path.home()</code> (your home folder).</p>

<p>Every part of a path is a property, so you never parse strings by
hand:</p>

<pre class="code">q = Path('/home/ada/projects/notes.txt')
q.name     # -&gt; 'notes.txt'
q.stem     # -&gt; 'notes'
q.suffix   # -&gt; '.txt'
q.parent   # -&gt; Path('/home/ada/projects')</pre>

<p>Read the properties as a dissection: <code>name</code> is the last
component, <code>stem</code> is the name minus its final extension,
<code>suffix</code> is that extension (note the dot), and
<code>parent</code> is everything before the last component. Need
<code>'notes.csv'</code> instead? <code>q.with_suffix('.csv')</code> &mdash;
no string slicing.</p>

[[diag:path_parts]]

<p>Checking what something is, is one call each:</p>

<pre class="code">q.exists()   # True / False
q.is_dir()   # is it a folder?
q.is_file()  # is it a regular file?</pre>

<p>In Python 3.14 these checks return <code>False</code> instead of
raising <code>OSError</code> on broken paths — so
<code>if p.exists():</code> is safe to write anywhere.</p>

<p>To find files, use <b>glob patterns</b> — the same
<code>*</code>/<code>?</code> wildcards you know from the shell:</p>

<pre class="code">list(Path('.').glob('*.py'))     # python files here
list(Path('.').glob('**/*.py'))  # ... and in every subfolder</pre>

<p><code>*</code> matches any text in one name; <code>**</code> crosses
folder boundaries and needs <code>glob()</code> to recurse. One caution:
a <code>Path</code> is not a string &mdash; old APIs that insist on a
string take <code>str(p)</code>, though almost everything modern accepts
paths directly.</p>
""",
            },
            {
                "title": "Read, write, walk, copy",
                "html": """
<p>Reading and writing files is two methods, no
<code>open()</code> bookkeeping:</p>

<pre class="code">p = Path('hello.txt')
p.write_text('Hello, Python!')   # creates the file
p.read_text()                    # -&gt; 'Hello, Python!'

p.write_bytes(b'\\x00\\x01')      # binary files too
p.read_bytes()                   # -&gt; b'\\x00\\x01'</pre>

<p><code>write_text</code> creates the file (or <em>replaces</em> it) and
returns the character count; <code>read_text</code> slurps the whole file
into one string. The bytes pair does the same for images and other binary
formats. Gotcha: <code>write_text</code> overwrites from byte zero &mdash;
if you mean to add to a file, open it with <code>open(p, 'a')</code>
instead.</p>

<p>Need a real file handle? <code>p.open()</code> behaves exactly
like the built-in <code>open()</code>, so <code>with p.open() as
f:</code> works the same way.</p>

<p>Folders: <code>mkdir()</code> creates one. Give it
<code>parents=True, exist_ok=True</code> and it creates every
missing level, like <code>mkdir -p</code>:</p>

<pre class="code">Path('reports/2026/jan').mkdir(parents=True, exist_ok=True)</pre>

<p>Plain <code>mkdir()</code> errors if the folder already exists;
<code>exist_ok=True</code> says "don't complain" and
<code>parents=True</code> builds the intermediate <code>reports</code>
and <code>2026</code> folders too. This exact line is how scripts set
up output directories safely.</p>

<p>To see what's inside a folder, iterate it:</p>

<pre class="code">for child in Path('.').iterdir():
    print(child.name)</pre>

<p><code>iterdir()</code> yields one Path per entry &mdash; files and
subfolders alike &mdash; and <code>child.name</code> prints just the last
component.</p>

<p>Want the whole tree, recursively? <code>walk()</code> (since
3.12) yields <code>(dirpath, dirnames, filenames)</code> triples —
the modern replacement for <code>os.walk()</code>:</p>

<pre class="code">for root, dirs, files in Path('src').walk():
    for name in files:
        print(root / name)</pre>

<p>Each triple is one visited folder: <code>root</code> is a Path, and
joining it with each name in <code>files</code> rebuilds full paths
without any string surgery.</p>

<p>And the big news for 3.14: pathlib finally grows built-in
<b>copy</b> methods. No more <code>shutil</code> for the simple
cases:</p>

<pre class="code">p.copy('backup.txt')          # copy a file (or a whole tree)
p.copy_into('backup/')        # copy INTO a directory</pre>

<p><code>copy</code> copies <em>to the exact target</em>;
<code>copy_into</code> keeps the file name and places it inside the
folder. That distinction is the whole API.</p>

<p><b>Mini-project idea:</b> total size of all <code>.py</code>
files in a tree, in three lines:</p>

<pre class="code">total = sum(f.stat().st_size
            for f in Path('.').glob('**/*.py'))
print(total)</pre>

<p>Walk through it: the glob yields every <code>.py</code> file,
<code>f.stat().st_size</code> is its size in bytes, and
<code>sum()</code> adds them up &mdash; your first real file-reporting
tool, no shell needed.</p>
""",
            },
        ],
        "quiz": [
            {
                "type": "mc",
                "question": "Which property gives the file name WITHOUT its extension?",
                "options": ["p.name", "p.stem", "p.suffix", "p.parent"],
                "answer": 1,
                "explain": "notes.txt -&gt; name 'notes.txt', stem 'notes', suffix '.txt'. stem strips the last suffix.",
            },
            {
                "type": "blank",
                "question": "Build child paths with the operator: p = Path('data') ____ 'notes.txt'",
                "answers": ["/"],
                "explain": "The / operator joins path segments: Path('data') / 'notes.txt'.",
            },
            {
                "type": "codefill",
                "question": "Count the Python files in the current folder:",
                "code": [
                    "from pathlib import ",
                    {"blank": "Path", "answers": ["Path"], "hint": "the main pathlib class"},
                    "",
                    "count = len(list(Path('.').glob('*.",
                    {"blank": "py", "answers": ["py"], "hint": "the file extension"},
                    "')))",
                    "print(count)",
                ],
                "explain": "Path('.').glob('*.py') finds every file ending in .py in the current directory.",
            },
            {
                "type": "mc",
                "question": "Which file operation is BRAND NEW in Python 3.14?",
                "options": ["p.read_text()", "p.copy_into('backup/')", "p.glob('*.py')", "p.mkdir()"],
                "answer": 1,
                "explain": "copy() and copy_into() were added in 3.14 — pathlib finally copies files without shutil.",
            },
        ],
    },

    # ------------------------------------------------------------------ 21
    {
        "id": "ch21",
        "title": "Supercharged Containers",
        "title_fa": "ظرف‌های پیشرفته",
        "emoji": "\U0001f9f0",
        "lessons": [
            {
                "title": "Counter, defaultdict, namedtuple",
                "html": """
<p>The <code>collections</code> module is your toolbox of smarter
containers. First: <b>counting</b> things — votes, words, log levels —
which is so common it gets its own class.</p>

<pre class="code">from collections import Counter

words = ['red', 'blue', 'red', 'green', 'blue', 'blue']
c = Counter(words)
c                       # -&gt; Counter({'blue': 3, 'red': 2, 'green': 1})
c['blue']               # -&gt; 3   (missing keys return 0, no KeyError)
c.most_common(2)        # -&gt; [('blue', 3), ('red', 2)]
c.total()               # -&gt; 6   (all counts summed, 3.10+)</pre>

<p>Walk through it: constructing a Counter from any iterable counts every
element once. Lookups behave like a dict, except a missing key quietly
gives <code>0</code> instead of raising &mdash;
<code>c['purple']</code> is just <code>0</code>.
<code>most_common(2)</code> sorts by count and hands back the top two as
<code>(item, count)</code> pairs. Counting characters works too:
<code>Counter('banana')</code> gives <code>{'a': 3, 'n': 2, 'b': 1}</code>.</p>

[[diag:counter_flow]]

<p>Second: <b>dictionaries that build their own defaults</b>.
<code>defaultdict(factory)</code> calls the factory whenever a key
is missing — so grouping never needs an <code>if key in d</code>
check:</p>

<pre class="code">from collections import defaultdict

d = defaultdict(list)
for word in ['cat', 'dog', 'cat', 'bird']:
    d[word].append(len(word))
d   # -&gt; defaultdict(list, {'cat': [3, 3], 'dog': [3], 'bird': [4]})</pre>

<p>The trick is <code>defaultdict(list)</code>: the first time a word is
seen, Python calls <code>list()</code> to make an empty list, then the
append runs. What used to be a three-line dance of "is it there? create
it; else append" becomes one line. Use <code>defaultdict(int)</code> for
counters and <code>defaultdict(set)</code> for unique members.</p>

<p>Third: <b>tuples with names</b>. A regular tuple is
<code>(11, 22)</code>; a namedtuple makes the meaning explicit:</p>

<pre class="code">from collections import namedtuple

Point = namedtuple('Point', ['x', 'y'])
p = Point(11, y=22)     # fields by name or position
p.x, p.y                # -&gt; 11 22
p._replace(x=33)        # new tuple with x changed
p._asdict()             # -&gt; {'x': 11, 'y': 22}</pre>

<p><code>p.x</code> reads far better than <code>p[0]</code>, and
<code>_replace</code> hands back a <em>new</em> tuple &mdash;
namedtuples are still immutable. Note the underscore on those helper
methods: they're reserved so they can never clash with a field name.</p>

<p>Namedtuples cost no more memory than plain tuples — perfect for
rows of data (the docs even suggest them for
<code>csv</code> and <code>sqlite3</code> results).</p>
""",
            },
            {
                "title": "itertools, functools, dataclasses",
                "html": """
<p><code>itertools</code> is the standard library's function
garden — lazy, memory-friendly iterators that combine like
building blocks. "Lazy" means values are produced one at a time, only
when asked, so a chain over two million-item lists never materializes
either list twice.</p>

<pre class="code">from itertools import chain, batched, combinations

list(chain('ABC', 'DEF'))        # -&gt; ['A','B','C','D','E','F']
list(batched('ABCDEFG', 3))      # -&gt; [('A','B','C'), ('D','E','F'), ('G',)]
list(combinations('ABCD', 2))    # -&gt; AB AC AD BC BD CD</pre>

<p>Walk through it: <code>chain</code> treats several iterables as one
long stream. <code>batched</code> chops the stream into tuples of at most
3 &mdash; the last one may be short. <code>combinations</code> yields
every unordered pair (order within a pair doesn't matter, so no 'BA').</p>

[[diag:itertools_flow]]

<p><code>batched()</code> (since 3.12) groups any stream into
fixed-size chunks — ideal for paging or batching work.
<code>count()</code>, <code>cycle()</code> and
<code>repeat()</code> never end, so combine them with
<code>islice()</code> or a <code>for</code> loop that stops.</p>

<p><code>functools</code> holds function helpers. Two you'll use
constantly:</p>

<pre class="code">from functools import lru_cache, partial

@lru_cache(maxsize=None)          # remember results
def fib(n):
    return n if n &lt; 2 else fib(n - 1) + fib(n - 2)

fib(40)     # instant, even though it recurses hugely

greet = partial(print, 'Hello,')  # pre-fill arguments
greet('Ada')                      # -&gt; Hello, Ada</pre>

<p><code>lru_cache</code> memoizes: each argument combination is computed
once and stored, which turns the exponential tree of
<code>fib</code> calls into a straight line &mdash; <code>fib(40)</code>
answers instantly. Gotcha: cached arguments must be hashable (no lists or
dicts), and an unbounded cache keeps everything forever, so give
<code>maxsize</code> a number for large inputs. <code>partial</code>
freezes the leading arguments of a function, producing a new callable
ready for the rest.</p>

<p>And <code>dataclasses</code> removes the boilerplate from
plain data classes — the decorator writes
<code>__init__</code>, <code>__repr__</code> and
<code>__eq__</code> for you:</p>

<pre class="code">from dataclasses import dataclass

@dataclass
class Book:
    title: str
    author: str
    pages: int = 0

b = Book('The Manual', 'Python', 200)
b            # -&gt; Book(title='The Manual', author='Python', pages=200)</pre>

<p>The annotations describe the fields; <code>pages: int = 0</code> gives
a default, so <code>Book('X', 'Y')</code> is legal. The generated
<code>__repr__</code> is why printing <code>b</code> shows every field,
and the generated <code>__eq__</code> makes two books with equal data
compare equal. When a class exists mostly to hold data, a dataclass is
the modern default.</p>
""",
            },
        ],
        "quiz": [
            {
                "type": "mc",
                "question": "What does Counter.most_common(3) return?",
                "options": [
                    "the 3 most common keys, unranked",
                    "a list of (item, count) pairs, most common first",
                    "a dict of the 3 most common items",
                    "a set of the 3 most common keys",
                ],
                "answer": 1,
                "explain": "most_common(n) returns a list of (element, count) tuples, sorted from most to least common.",
            },
            {
                "type": "blank",
                "question": "Group values without 'if key in d' checks using: defaultdict(____)",
                "answers": ["list", "list)", "list]"],
                "explain": "defaultdict(list) auto-creates an empty list for each new key, so d[k].append(v) just works.",
            },
            {
                "type": "mc",
                "question": "Which itertools function chunks a stream into fixed-size tuples?",
                "options": ["chain", "batched", "cycle", "combinations"],
                "answer": 1,
                "explain": "batched('ABCDEFG', 3) yields ('A','B','C'), ('D','E','F'), ('G',) — the last batch may be short.",
            },
            {
                "type": "codefill",
                "question": "Cache this function's results with a decorator:",
                "code": [
                    "from functools import ",
                    {"blank": "lru_cache", "answers": ["lru_cache"], "hint": "the caching decorator"},
                    "",
                    "@",
                    {"blank": "lru_cache(maxsize=None)", "answers": ["lru_cache(maxsize=None)", "lru_cache"], "hint": "decorator call form"},
                    "",
                    "def fib(n):",
                    "    return n if n < 2 else fib(n - 1) + fib(n - 2)",
                ],
                "explain": "@lru_cache(maxsize=None) memoizes every call, so the exponential recursion runs in linear time.",
            },
        ],
    },

    # ------------------------------------------------------------------ 22
    {
        "id": "ch22",
        "title": "Data Formats & the Internet",
        "title_fa": "فرمت‌های داده و اینترنت",
        "emoji": "\U0001f310",
        "lessons": [
            {
                "title": "JSON & CSV",
                "html": """
<p>Programs talk to each other in <b>JSON</b> — the web's
universal data format. Python dicts and JSON are almost the same
thing, so the <code>json</code> module is two functions:</p>

<pre class="code">import json

data = {"name": "Ada", "skills": ["python", "math"], "age": 36}

text = json.dumps(data, indent=2)   # dict -&gt; JSON string
loaded = json.loads(text)           # JSON string -&gt; dict
loaded['name']                      # -&gt; 'Ada'</pre>

<p>Walk through it: <code>dumps</code> ("dump to string") serializes the
dict, <code>loads</code> parses it back &mdash; a perfect round trip, and
<code>loaded</code> is a brand-new dict equal to the original. The S at
the end of each name means <em>string</em>; without it,
<code>json.dump</code>/<code>json.load</code> work directly on files.</p>

[[diag:json_roundtrip]]

<p><code>indent=2</code> pretty-prints it for humans; without it
you get one compact line. <code>ensure_ascii=False</code> keeps
non-ASCII characters readable instead of escaping them.</p>

<p>Read a JSON file: <code>json.load(open('data.json'))</code>.
Write one: <code>json.dump(data, open('out.json', 'w'),
indent=2)</code>.</p>

<p>One mapping caveat: JSON has no tuples or sets, and its
<code>true</code>/<code>false</code>/<code>null</code> become Python's
<code>True</code>/<code>False</code>/<code>None</code>. If round-tripping
exact types matters, check what came back.</p>

<p><b>CSV</b> (spreadsheets) is just as easy. Reading with a
<code>DictReader</code> uses the header row as keys:</p>

<pre class="code">import csv

with open('people.csv', newline='') as f:
    for row in csv.DictReader(f):
        print(row['name'], row['age'])</pre>

<p>Each <code>row</code> is a dict built from the header line, so
<code>row['name']</code> and <code>row['age']</code> read naturally. Two
gotchas: every value is a <b>string</b> &mdash; compute with
<code>int(row['age'])</code> &mdash; and the
<code>newline=''</code> argument is not optional: csv's own newline
handling otherwise mangles Windows files.</p>

<p>Writing is symmetric &mdash;
<code>csv.writer(f).writerow([...])</code>, or
<code>DictWriter</code> with a <code>fieldnames=</code> list.
The collections docs pair namedtuples with csv rows nicely:</p>

<pre class="code">Employee = namedtuple('Employee', 'name, title')
for emp in map(Employee._make, csv.reader(f)):
    print(emp.name)</pre>

<p><code>Employee._make</code> converts each plain row list into a
namedtuple, so the rest of the code says <code>emp.name</code> instead
of <code>row[0]</code> &mdash; self-documenting for free.</p>
""",
            },
            {
                "title": "Talk to the web",
                "html": """
<p>Fetching a web page takes three lines with
<code>urllib.request</code> — no third-party packages needed:</p>

<pre class="code">from urllib.request import urlopen

with urlopen('https://example.com') as resp:
    html = resp.read().decode('utf-8')
print(html[:120])</pre>

<p>Walk through it: <code>urlopen</code> performs the HTTP GET and hands
you a response object that works as a context manager, so the connection
closes reliably. <code>resp.read()</code> returns raw <b>bytes</b> &mdash;
the network speaks bytes, not text &mdash; so
<code>.decode('utf-8')</code> converts them into a printable, searchable
string. If you skip the decode, you'll see <code>b'&lt;!doctype html&gt;...'
</code> and wonder why every comparison fails.</p>

<p><code>urlopen</code> gives you a response object; the page
comes back as <b>bytes</b>, so <code>.decode('utf-8')</code>
turns it into text.</p>

<p>Now the fun part — combine it with the
<code>json</code> module from the last lesson and you can call
<b>public web APIs</b>:</p>

<pre class="code">import json
from urllib.request import urlopen

with urlopen('https://api.github.com/users/python') as resp:
    data = json.load(resp)          # decode JSON straight in

print(data['name'], data['followers'], 'followers')</pre>

<p>Here <code>json.load</code> reads and decodes the response in one
step, and the API's answer &mdash; a JSON object &mdash; arrives as a
plain dict you can index. That single pattern &mdash; fetch, decode
JSON, use the dict &mdash; powers weather apps, news bots, and stock
trackers. Try it in the playground with a free API of your choice.</p>

<p>Two cautions from the docs: <code>urlopen</code> raises
<code>HTTPError</code> for bad responses, so wrap network calls in
<code>try/except</code>; and never call an API inside a tight loop
without thinking about how often you really need fresh data. Add a
<code>timeout=</code> argument as well &mdash; without it a stuck server
can hang your program forever.</p>
""",
            },
        ],
        "quiz": [
            {
                "type": "mc",
                "question": "Which function turns a Python dict into a JSON string?",
                "options": ["json.loads", "json.dumps", "json.stringify", "json.encode"],
                "answer": 1,
                "explain": "dumps = dump to string (dict -> str); loads = load from string (str -> dict).",
            },
            {
                "type": "blank",
                "question": "Pretty-print JSON with: json.dumps(data, ____=2)",
                "answers": ["indent"],
                "explain": "indent=2 inserts newlines and two-space indents so the JSON is human-readable.",
            },
            {
                "type": "mc",
                "question": "Which reader uses the CSV header row as dictionary keys?",
                "options": ["csv.reader", "csv.DictReader", "csv.KeyReader", "csv.RowReader"],
                "answer": 1,
                "explain": "DictReader maps the header row to keys, so each row is a dict: row['name'], row['age'].",
            },
            {
                "type": "codefill",
                "question": "Fetch a page and turn the bytes into text:",
                "code": [
                    "from urllib.request import urlopen",
                    "",
                    "with urlopen('https://example.com') as resp:",
                    "    html = resp.read().",
                    {"blank": "decode('utf-8')", "answers": ["decode('utf-8')", "decode('utf8')", "decode()"], "hint": "bytes to str"},
                    "",
                    "print(html)",
                ],
                "explain": "resp.read() returns bytes; .decode('utf-8') converts them to a str you can print and search.",
            },
        ],
    },

    # ------------------------------------------------------------------ 23
    {
        "id": "ch23",
        "title": "Your First Real Programs",
        "title_fa": "اولین برنامه‌های واقعی تو",
        "emoji": "\U0001f680",
        "lessons": [
            {
                "title": "Command-line tools (argparse + subprocess)",
                "html": """
<p>Real programs are tools you run from the terminal. The
<code>argparse</code> module turns a plain script into a proper
command with <code>--flags</code> and built-in
<code>--help</code>:</p>

<pre class="code">import argparse

parser = argparse.ArgumentParser(description='Say hello')
parser.add_argument('--name', default='world')
parser.add_argument('--shout', action='store_true')
args = parser.parse_args()

msg = f'Hello, {args.name}!'
print(msg.upper() if args.shout else msg)</pre>

<p>Walk through it: you describe the arguments once, and argparse does
the rest &mdash; parsing <code>sys.argv</code>, applying the default
<code>'world'</code> when <code>--name</code> is absent, and exposing
everything as attributes of <code>args</code>.</p>

[[diag:cli_flow]]

<p>Run it: <code>python greet.py --name Ada</code> prints
<code>Hello, Ada!</code>. <code>--shout</code> is a
<code>store_true</code> flag — its mere presence means
<code>True</code>. And <code>python greet.py --help</code> prints
a usage summary for free. Type a bad option and argparse exits with a
clear error before your code runs a single line.</p>

<p>Sometimes your Python program needs to run <em>another</em>
program. <code>subprocess</code> does that safely:</p>

<pre class="code">import subprocess

result = subprocess.run(['python', '-c', 'print(6 * 7)'],
                        capture_output=True, text=True)
print(result.stdout)     # -&gt; 42

result = subprocess.run(['ls', 'missing.txt'],
                        capture_output=True, text=True)
print(result.returncode) # non-zero means the command failed</pre>

<p>The first run captures the child program's output: with
<code>text=True</code>, <code>result.stdout</code> is the string
<code>42</code> (with its trailing newline), ready to use. The second run
shows the error channel: <code>returncode</code> is <code>0</code> on
success and something else on failure &mdash; the Unix convention.</p>

<p><code>capture_output=True</code> grabs the output,
<code>text=True</code> returns it as a string instead of bytes,
and <code>check=True</code> makes failures raise instead of
silently continuing. Prefer a list of arguments (not a shell
string) — no quoting bugs, no shell injection. And never build that
list from raw user input without checking it; the list form protects
you only when you control the parts.</p>
""",
            },
            {
                "title": "Databases, logs & tests (sqlite3 + logging + unittest)",
                "html": """
<p>Real programs keep data in a database. Python ships
<code>sqlite3</code> — a full SQL engine in a single file:</p>

<pre class="code">import sqlite3

conn = sqlite3.connect('app.db')          # creates the file
conn.execute('CREATE TABLE IF NOT EXISTS users (name TEXT, age INT)')
conn.execute('INSERT INTO users VALUES (?, ?)', ('Ada', 36))
conn.commit()                             # save the changes

for row in conn.execute('SELECT * FROM users'):
    print(row)                            # -&gt; ('Ada', 36)</pre>

<p>Walk through it: <code>connect</code> opens (or creates) the database
file. The <code>IF NOT EXISTS</code> clause makes the setup line safe to
rerun. Each selected row comes back as a tuple, which you can unpack:
<code>for name, age in conn.execute(...)</code>.</p>

[[diag:sqlite_tables]]

<p>The <code>?</code> placeholders are non-negotiable: values are
passed as arguments, never glued into the SQL string — that's how
you avoid injection bugs. <code>commit()</code> makes writes
permanent; forget it and your inserts vanish when the connection
closes.</p>

<p><b>Logging</b> beats <code>print()</code> for anything real.
With one line you get timestamps, levels, and the ability to mute
noise:</p>

<pre class="code">import logging
logging.basicConfig(level=logging.INFO)

logging.info('started')
logging.warning('disk almost full')
logging.error('something broke')</pre>

<p>Levels run <code>DEBUG &lt; INFO &lt; WARNING &lt; ERROR
&lt; CRITICAL</code>; <code>basicConfig(level=...)</code> decides
what shows. With <code>level=INFO</code> the info line prints, debug
calls stay silent, and the warning and error appear &mdash; one switch,
no deleting prints. Sending logs to a file is one more argument:
<code>basicConfig(filename='app.log', level=logging.INFO)</code>.</p>

<p>Finally, <b>tests</b>. <code>unittest</code> is built in —
write a <code>TestCase</code>, run with
<code>python -m unittest</code>:</p>

<pre class="code">import unittest

def double(x):
    return x * 2

class TestDouble(unittest.TestCase):
    def test_doubles(self):
        self.assertEqual(double(3), 6)
        self.assertEqual(double(0), 0)

if __name__ == '__main__':
    unittest.main()</pre>

<p>Each <code>test_</code> method is one check; <code>assertEqual</code>
compares actual with expected and names the exact line if they differ.
Run the file and unittest reports <code>OK</code> &mdash; or a precise
failure. The habit to build: write the test before the fix, so a bug can
never quietly return.</p>

<p>That's the whole loop of a real program: <b>parse arguments,
do the work, store the data, log what happened, test it
works</b>.</p>
""",
            },
        ],
        "quiz": [
            {
                "type": "mc",
                "question": "How should values be inserted into a sqlite3 query?",
                "options": [
                    "glued into the SQL with an f-string",
                    "as ? placeholders with values passed as arguments",
                    "there is no safe way",
                    "only with the .format() method",
                ],
                "answer": 1,
                "explain": "? placeholders + separate arguments keep SQL safe from injection and quoting bugs.",
            },
            {
                "type": "blank",
                "question": "Make writes permanent in sqlite3 with: conn.____()",
                "answers": ["commit"],
                "explain": "commit() saves pending transactions to the database file; without it, changes are lost.",
            },
            {
                "type": "codefill",
                "question": "Finish the argparse setup so the flag value is available:",
                "code": [
                    "import argparse",
                    "parser = argparse.ArgumentParser()",
                    "parser.add_argument('--name')",
                    "args = parser.",
                    {"blank": "parse_args()", "answers": ["parse_args()", "parse_args"], "hint": "the method that reads sys.argv"},
                    "",
                    "print('Hi', args.name)",
                ],
                "explain": "parser.parse_args() reads the command line and returns a namespace; flags become attributes like args.name.",
            },
            {
                "type": "mc",
                "question": "Run every test in a file with: python -m ____",
                "options": ["testing", "unittest", "pytest", "test"],
                "answer": 1,
                "explain": "python -m unittest discovers and runs all TestCase classes in the current folder.",
            },
        ],
    },
]
