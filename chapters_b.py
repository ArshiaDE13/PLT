"""Chapters 9-16 of the course, distilled from the Python 3.14 tutorial."""

CHAPTERS_B = [
    # ------------------------------------------------------------------ 09
    {
        "id": "ch09",
        "title": "Classes",
        "emoji": "🏛️",
        "lessons": [
            {
                "title": "Classes and objects",
                "html": """
<p>A <b>class</b> is a blueprint for objects. When your program starts
juggling related data plus the functions that act on it — a player with
health and position, a bank account with balance and owner — you bundle
them into a class. Objects bundle data (attributes) with functions that act
on it (methods). The special method <code>__init__</code> sets up each new
instance:</p>

<pre class="code">class Dog:
    def __init__(self, name):
        self.name = name      # attribute

    def bark(self):           # method
        return f"{self.name} says Woof!"

d = Dog("Rex")
print(d.name)      # Rex
print(d.bark())    # Rex says Woof!</pre>

<p>Walk through it: <code>Dog("Rex")</code> creates a new object and calls
<code>__init__</code> with that object as <code>self</code> and
<code>"Rex"</code> as <code>name</code>; the line <code>self.name =
name</code> stores the value <em>on the instance</em>. Then
<code>d.name</code> reads it back as <code>Rex</code>, and
<code>d.bark()</code> runs the method, returning <code>Rex says Woof!</code>.
Every method takes <code>self</code> first — the instance itself. You
never pass it yourself; Python does.</p>

<p>Classes support <b>inheritance</b>: a child class reuses everything
from its parent and can override or extend it. Multiple inheritance is
possible (a class can have several parents), and every class ultimately
derives from <code>object</code>.</p>

<pre class="code">class Puppy(Dog):
    def bark(self):
        return "yip yip!"

print(Puppy("Scooby").bark())   # yip yip!</pre>

<p><code>Puppy</code> inherits <code>__init__</code> from <code>Dog</code>
unchanged but replaces <code>bark</code> with its own version — that is
overriding. Rule of thumb: reach for a class when several functions all
touch the same blob of data; if you are only passing data around, plain
functions and dicts are simpler.</p>
""",
            },
            {
                "title": "Scopes, name mangling and iterators",
                "html": """
<p>Python resolves names with the <b>LEGB</b> rule — search Local, then
Enclosing, then Global, then Built-in. When you read a name, Python checks
these four levels in order and stops at the first hit; that's why a local
variable can temporarily shadow a global one:</p>

[[diag:scope_le]]

<pre class="code">def outer():
    x = 10
    def inner():
        nonlocal x      # refers to the enclosing scope's x
        x += 1
        return x
    return inner()</pre>

<p>Normally <code>inner</code> could only <em>read</em> the enclosing
<code>x</code>; assigning would create a brand-new local. The
<code>nonlocal</code> statement says "write through to the enclosing scope",
so <code>x += 1</code> bumps the outer <code>x</code> to 11. Without it this
code raises <code>UnboundLocalError</code> — one of the most common scope
errors you will meet.</p>

<p>Variables inside a class are still found through normal scopes —
methods don't automatically see class attributes; use
<code>self.attribute</code>. To avoid accidental name clashes, a
double-underscore prefix triggers <b>name mangling</b>:
<code>self.__secret</code> becomes <code>self._ClassName__secret</code>.
It is not privacy — a determined caller can still reach it — but a subclass
won't clobber it by accident.</p>

<p>Finally, anything with <code>__iter__</code> and <code>__next__</code>
is <b>iterable</b> and can drive a <code>for</code> loop. The easiest way
to build one is a <b>generator</b> — a function with <code>yield</code>,
which pauses and resumes:</p>

<pre class="code">def countdown(n):
    while n &gt; 0:
        yield n
        n -= 1

for x in countdown(3):
    print(x)    # 3, 2, 1</pre>

<p>Calling <code>countdown(3)</code> runs no body yet — it returns a
generator object. Each loop pass asks for the next value: the function runs
to <code>yield</code>, hands out 3, freezes, and resumes where it stopped.
That is why the loop prints <code>3, 2, 1</code> and then stops cleanly.
Generators produce values lazily, so a generator over a billion numbers
uses almost no memory.</p>
""",
            },
        ],
        "quiz": [
            {
                "type": "mc",
                "question": "What is the first parameter of every instance method?",
                "options": ["this", "self", "me", "instance"],
                "answer": 1,
                "explain": "Methods receive the instance as their first parameter, conventionally named self.",
            },
            {
                "type": "codefill",
                "question": "Complete the constructor so the instance stores its name:",
                "code": [
                    "class Cat:",
                    "    def __init__(self, name):",
                    "        ",
                    {"blank": "self.name = name", "answers": ["self.name = name"], "hint": "assign the parameter to an attribute on self"},
                ],
                "explain": "self.name = name stores the argument on the instance so other methods can use it.",
            },
            {
                "type": "blank",
                "question": "A function that uses <code>yield</code> instead of <code>return</code> is called a ____.",
                "answers": ["generator", "generator function"],
                "explain": "A generator yields values one at a time, pausing between yields — ideal for iterating without building a full list.",
            },
            {
                "type": "mc",
                "question": "In LEGB scope resolution, which scope is searched LAST?",
                "options": ["Local", "Enclosing", "Global", "Built-in"],
                "answer": 3,
                "explain": "Python looks in Local, then Enclosing, then Global, and finally Built-in (len, print, ...).",
            },
        ],
    },

    # ------------------------------------------------------------------ 10
    {
        "id": "ch10",
        "title": "Standard Library Tour I",
        "emoji": "📚",
        "lessons": [
            {
                "title": "Files, patterns and arguments",
                "html": """
<p>The standard library is Python's superpower — no downloads needed.
Three everyday questions are "where am I, what files are here, what did
the user type?", and <code>os</code>, <code>glob</code> and <code>sys</code>
answer them:</p>

<pre class="code">import os, glob, sys

os.getcwd()                    # current directory
os.walk('.')                   # walk a directory tree

for name in glob.glob('*.txt'):   # filename patterns
    print(name)

print(sys.argv)                # command-line arguments</pre>

<p>Walk through it: <code>os.getcwd()</code> returns the directory your
script runs from, and <code>os.walk('.')</code> yields every subfolder and
file under it — ideal for batch renames or searches.
<code>glob.glob('*.txt')</code> applies a shell-style wildcard and lists
matching names like <code>notes.txt</code>, <code>todo.txt</code>.
<code>sys.argv</code> is the raw list of command-line words, script name
first.</p>

<p>For proper command-line programs, <code>argparse</code> parses options
and generates help:</p>

<pre class="code">import argparse

p = argparse.ArgumentParser(prog='greet')
p.add_argument('name')
p.add_argument('--loud', action='store_true')
args = p.parse_args()

msg = f"Hello, {args.name}"
print(msg.upper() if args.loud else msg)</pre>

<p>What did that buy you? Run <code>python greet.py Ada</code> and it
prints <code>Hello, Ada</code>. Run <code>python greet.py Ada --loud</code>
and it prints <code>HELLO, ADA</code> — the flag arrives as
<code>args.loud == True</code>. Omit the name and argparse prints a usage
error and exits; add <code>-h</code> and you get a help page you never
wrote. Hand-rolling that with <code>sys.argv</code> would take dozens of
lines and more edge cases than you think.</p>

<p>Rule of thumb: <code>sys.argv</code> for throwaway scripts;
<code>argparse</code> the moment a tool has options or is used by someone
else. Chapter 23 builds on this into a complete command-line pattern, with
subcommands, defaults and type-checked values.</p>
""",
            },
            {
                "title": "Regular expressions and math",
                "html": """
<p><code>re</code> is the regular-expression engine — pattern matching on
text. A pattern is a tiny language of its own: <code>\\d+</code> means "one
or more digits", <code>\\s+</code> means "one or more whitespace
characters", <code>^</code> anchors the match to the start of the
string:</p>

<pre class="code">import re

re.findall(r'\\d+', 'Room 404, floor 7')   # ['404', '7']
re.sub(r'\\s+', ' ', 'a    b  c')          # 'a b c'
if re.search(r'^cat', 'catalog'):
    print("starts with cat")</pre>

<p>Walk through it: <code>findall</code> returns every match as a list, so
the first line gives <code>['404', '7']</code> — both numbers in the
sentence. <code>sub</code> replaces every run of whitespace with a single
space, collapsing <code>'a    b  c'</code> into <code>'a b c'</code>.
<code>search</code> returns a match object (truthy) or <code>None</code>,
so it drops neatly into an <code>if</code>: <code>'catalog'</code> starts
with <code>cat</code>, so the message prints. Always write patterns as raw
strings — with the leading <code>r</code> — so backslashes survive
intact.</p>

<p>The <code>math</code> module covers common math, and
<code>statistics</code> handles everyday stats:</p>

<pre class="code">import math, statistics

math.sqrt(16)              # 4.0
math.hypot(3, 4)           # 5.0
math.isclose(0.1 + 0.2, 0.3, rel_tol=1e-9)   # True

statistics.mean([1, 2, 3, 4])    # 2.5
statistics.median([1, 2, 3])     # 2
statistics.variance([1, 2, 3])   # 1.0</pre>

<p><code>sqrt(16)</code> is 4.0, and <code>hypot(3, 4)</code> computes the
long side of a 3-4 right triangle: 5.0. The third line matters most:
<code>math.isclose</code> is the correct way to compare floats (Chapter
15), and it says <code>True</code> where <code>==</code> would say
<code>False</code>. The statistics calls give the average of
<code>[1, 2, 3, 4]</code> as 2.5, the middle of <code>[1, 2, 3]</code> as
2, and the variance as 1.0.</p>

<p>For random values use <code>random</code>: <code>random.choice(items)</code>,
<code>random.sample(items, k)</code>, <code>random.randrange(6)</code>.</p>

<p><code>choice</code> picks one item, <code>sample</code> picks k without
repeats (card games, raffles), and <code>randrange(6)</code> gives 0
through 5 — a die. One warning: never use <code>random</code> for
passwords or tokens; that is what the <code>secrets</code> module is
for.</p>

[[diag:stdlib_shelf]]
""",
            },
        ],
        "quiz": [
            {
                "type": "mc",
                "question": "Which module handles command-line arguments for a script?",
                "options": ["os", "sys", "argparse", "glob"],
                "answer": 2,
                "explain": "argparse parses command-line options, while sys.argv just lists the raw arguments.",
            },
            {
                "type": "blank",
                "question": "To find all files matching a wildcard pattern like <code>*.txt</code>, use the <code>____</code> module.",
                "answers": ["glob"],
                "explain": "glob.glob('*.txt') returns all matching filenames.",
            },
            {
                "type": "mc",
                "question": "Which call checks whether two floats are 'close enough'?",
                "options": [
                    "math.close(0.1 + 0.2, 0.3)",
                    "math.isclose(0.1 + 0.2, 0.3)",
                    "0.1 + 0.2 == 0.3",
                    "statistics.approx(0.3)",
                ],
                "answer": 1,
                "explain": "math.isclose(a, b) compares floats with a tolerance — the right way to compare approximate values.",
            },
        ],
    },

    # ------------------------------------------------------------------ 11
    {
        "id": "ch11",
        "title": "Standard Library Tour II",
        "emoji": "🧰",
        "lessons": [
            {
                "title": "Printing, text and threads",
                "html": """
<p>More tools from the treasure chest. <code>pprint</code> pretty-prints
complex data, <code>textwrap</code> wraps paragraphs, and
<code>string.Template</code> offers simple $-based substitution:</p>

<pre class="code">import pprint, textwrap
from string import Template

pprint.pprint({'a': [1, 2, 3], 'b': {'c': [4, 5]}})

textwrap.fill("a very long sentence...", width=30)

t = Template('Hello, $name!')
t.substitute(name='Ada')       # 'Hello, Ada!'</pre>

<p><code>pprint</code> prints the nested dict one item per line, indented,
instead of one unreadable 90-character blob — the first tool to reach for
when a data structure looks wrong. <code>textwrap.fill</code> reflows a
long string to 30 columns, which is how console reports stay inside the
window. <code>Template.substitute</code> fills placeholders and is safe
with user-supplied templates, because — unlike an f-string — a template
string cannot execute expressions.</p>

<p><code>threading</code> runs work in parallel. Threads share memory, so
they're great for I/O-bound tasks (waiting on network or files):</p>

<pre class="code">import threading, time

def worker(name):
    time.sleep(0.5)
    print(f"{name} done")

for name in ['a', 'b']:
    threading.Thread(target=worker, args=(name,)).start()</pre>

<p>The loop starts two threads, each sleeping half a second and then
printing. Total wait is about 0.5 seconds, not 1.0, because the sleeps
overlap — that is the win. Gotcha: CPython's GIL (Global Interpreter Lock)
lets only one thread run Python bytecode at a time, so threads speed up
<em>waiting</em>, never computation. For CPU-heavy work use
<code>multiprocessing</code>, and any data both threads write needs a
<code>threading.Lock</code> to avoid races.</p>

<p>And <code>logging</code> replaces <code>print</code> for serious
programs — timestamps, levels, and multiple destinations out of the box:</p>

<pre class="code">import logging
logging.basicConfig(level=logging.INFO)
logging.info("job started")</pre>

<p>With <code>basicConfig</code> set to <code>INFO</code>, the line appears
with a timestamp and a level prefix. When something goes wrong later, you
switch the level to <code>DEBUG</code> in one place instead of hunting down
forty <code>print</code> calls.</p>
""",
            },
            {
                "title": "Efficient data structures and exact numbers",
                "html": """
<p>When lists aren't quite right, the <code>collections</code> module has
specialized containers. A <code>deque</code> grows fast at both ends:</p>

[[diag:deque]]

<pre class="code">from collections import deque
dq = deque('abc')
dq.append('d'); dq.appendleft('z')
dq.popleft()          # 'z' — instant removal</pre>

<p><code>deque('abc')</code> builds a double-ended queue from the
characters. <code>append</code> and <code>appendleft</code> add to either
end in constant time, and <code>popleft()</code> removes <code>'z'</code>
instantly — the exact operation that costs O(n) on a list. Reach for a
deque whenever items enter and leave at the front: queues, sliding windows,
"keep the last N lines".</p>

<p>For keeping data sorted or always taking the smallest item:</p>

<pre class="code">import bisect, heapq

bisect.insort(sorted_list, 5)      # insert, keeping order
heapq.heappush(heap, 3)            # priority queue
heapq.heappop(heap)                # smallest first</pre>

<p><code>bisect.insort</code> drops 5 into the right slot of an
already-sorted list — one ordered insertion, no re-sorting.
<code>heapq</code> maintains a min-heap: <code>heappush</code> adds a value
and <code>heappop</code> always returns the <em>smallest</em>, both in
O(log n). That "next most urgent item" trick is how schedulers and
Dijkstra's algorithm stay fast. Gotcha: a heap's internal order is not
sorted order — only the element at index 0 is guaranteed to be the
smallest.</p>

<p>Floating-point arithmetic is inexact (Chapter 15). When you need exact
decimal math — money, accounting — use <code>decimal</code>:</p>

<pre class="code">from decimal import Decimal
Decimal('0.1') + Decimal('0.2')    # Decimal('0.3') — exact!</pre>

<p><code>Decimal('0.1') + Decimal('0.2')</code> gives exactly
<code>Decimal('0.3')</code>, because decimals store base-10 digits instead
of binary fractions. Note the quotes: build a Decimal from a <em>string</em>
— <code>Decimal(0.1)</code> faithfully stores the binary approximation you
were trying to escape. Rule of thumb: floats for measurements, Decimal for
money, <code>fractions.Fraction</code> when you need exact ratios like
1/3.</p>
""",
            },
        ],
        "quiz": [
            {
                "type": "mc",
                "question": "Which container is best for fast appends AND fast pops from the front?",
                "options": ["list", "deque", "tuple", "set"],
                "answer": 1,
                "explain": "deque is optimized for fast appends/pops at both ends; popping the front of a list is O(n).",
            },
            {
                "type": "mc",
                "question": "Which module gives exact decimal arithmetic?",
                "options": ["math", "decimal", "fractions", "statistics"],
                "answer": 1,
                "explain": "decimal.Decimal performs exact base-10 arithmetic — ideal for money. (fractions does exact rationals.)",
            },
            {
                "type": "blank",
                "question": "The module that pretty-prints nested data structures is ____.",
                "answers": ["pprint"],
                "explain": "pprint.pprint() formats lists and dicts in a readable, indented layout.",
            },
        ],
    },

    # ------------------------------------------------------------------ 12
    {
        "id": "ch12",
        "title": "Virtual Environments and Packages",
        "emoji": "🏝️",
        "lessons": [
            {
                "title": "Why virtual environments?",
                "html": """
<p>A <b>virtual environment</b> is an isolated folder holding its own
installed packages. Each project gets its own env, so version clashes
disappear — project A can use requests 2.31 while project B uses 2.32.
Without environments, every <code>pip install</code> lands in one shared
pile, and upgrading a package for one project silently breaks
another.</p>

[[diag:venv_boxes]]

<p>Create and use one:</p>

<pre class="code">python -m venv myenv</pre>

<p>This makes a folder called <code>myenv</code> containing a private copy
of the interpreter, <code>pip</code>, and its own <code>site-packages</code>
directory. Nothing outside the folder is touched.</p>

<p>Then <b>activate</b> it so its commands take over your shell:</p>

<pre class="code"># Windows
myenv\\Scripts\\activate

# macOS / Linux
source myenv/bin/activate</pre>

<p>Activation does exactly two things: it puts <code>myenv/Scripts</code>
(or <code>myenv/bin</code>) at the front of your <code>PATH</code>, and it
sets environment variables so Python finds that copy first. Your prompt
changes to show the environment. From now on, <code>python</code> and
<code>pip</code> mean <em>that</em> environment's copies — anything you
install stays inside it. When you're done, <code>deactivate</code> leaves
it.</p>

<p>Two gotchas: activation only affects the current terminal — a new
terminal must activate again. And never commit the <code>myenv</code>
folder to git; it is machine-specific and huge. Commit
<code>requirements.txt</code> instead, which the next lesson covers.</p>
""",
            },
            {
                "title": "pip and requirements.txt",
                "html": """
<p>Inside an active environment, <code>pip</code> installs packages from
the Python Package Index (PyPI) — over half a million packages written by
other people, from <code>requests</code> for HTTP to <code>numpy</code>
for numeric work:</p>

<pre class="code">pip install requests
pip list                     # what's installed
pip search "query"           # search PyPI</pre>

<p><code>pip install requests</code> downloads the package <em>into the
active environment</em> — nowhere shared. <code>pip list</code> shows what
is installed there. Two notes: the <code>pip search</code> command has been
disabled (PyPI shut its search API down), so browse pypi.org to find
packages; and prefer <code>python -m pip install ...</code> — it guarantees
the pip that runs belongs to the same Python you will use.</p>

<p>To make your project reproducible, record its dependencies in
<code>requirements.txt</code> and install them with one command:</p>

<pre class="code">pip freeze &gt; requirements.txt
pip install -r requirements.txt</pre>

<p><code>pip freeze</code> writes every installed package with its exact
version, like <code>requests==2.32.3</code>, into the file. The second
command reads that list and installs the same versions anywhere — your
teammate's laptop, a server, a container. Anyone — on any machine — can
then recreate your exact setup. That's why environments plus a
requirements file are the standard way to ship Python projects.</p>

<p>Gotcha: run <code>pip freeze</code> inside the project's environment,
not the global one, or you will record every package on your machine. And
commit the file to version control — it is tiny, and it is the recipe for
rebuilding everything else.</p>
""",
            },
        ],
        "quiz": [
            {
                "type": "mc",
                "question": "What does <code>python -m venv myenv</code> do?",
                "options": [
                    "Installs the Python interpreter into myenv",
                    "Creates an isolated environment folder for packages",
                    "Deletes the myenv folder",
                    "Starts the REPL inside myenv",
                ],
                "answer": 1,
                "explain": "venv creates an isolated directory with its own Python and package storage — your project's private sandbox.",
            },
            {
                "type": "blank",
                "question": "The command that installs a package from PyPI is <code>____ install requests</code>.",
                "answers": ["pip", "python -m pip"],
                "explain": "pip install requests downloads and installs the package into the active environment.",
            },
            {
                "type": "mc",
                "question": "Which file lists a project's dependencies so others can install them?",
                "options": ["README.md", "requirements.txt", "setup.cfg", "pyproject.yaml"],
                "answer": 1,
                "explain": "requirements.txt lists dependencies; pip install -r requirements.txt installs them all at once.",
            },
        ],
    },

    # ------------------------------------------------------------------ 13
    {
        "id": "ch13",
        "title": "What Now?",
        "emoji": "🧭",
        "lessons": [
            {
                "title": "Where to go from here",
                "html": """
<p>You've finished the tutorial — congratulations! You now know the core of
the language: syntax, data structures, functions, classes, modules, files
and errors. The tutorial itself points to the next steps of your
journey:</p>

<ul>
<li><b>The Python Standard Library reference</b> — the complete catalog of
built-in modules. This is the book you'll consult daily.</li>
<li><b>The Language Reference</b> — the precise, formal grammar of Python,
for when you need the exact rules.</li>
<li><b>Installing Python Modules</b> — a deeper guide to pip, virtual
environments and packaging.</li>
<li><b>Distributing Python Modules</b> — how to publish your own packages
so others can pip install them.</li>
</ul>

<p>How to actually use these: the Library reference is not for reading
cover to cover — it answers "which module does X?" and "what are this
function's arguments?". The Language Reference settles arguments about
what Python <em>really</em> does. The two module guides matter the day you
install or publish something nontrivial.</p>

<p>Reading is good, but <b>building is better</b>. The best next step is
to pick a small project — a to-do list, a web scraper, a quiz game — and
write it. A real project forces you through the whole loop: make a plan,
hit a wall, look it up, fix it, repeat. When you get stuck, the
interactive shell is your friend: try the piece, then assemble the
whole.</p>

<p>Practical advice: keep each project small enough to finish in a week,
put it on GitHub, and rewrite it once you know a better way. Three small
finished projects teach more than one grand unfinished one.</p>
""",
            },
        ],
        "quiz": [
            {
                "type": "mc",
                "question": "What does the tutorial recommend after finishing it?",
                "options": [
                    "Stop programming forever",
                    "Read the library reference and start building projects",
                    "Rewrite the tutorial in another language",
                    "Only use the interactive shell forever",
                ],
                "answer": 1,
                "explain": "The tutorial points to the library and language references, and emphasizes learning by building.",
            },
            {
                "type": "blank",
                "question": "The complete catalog of built-in modules is called the Python Standard ____ reference.",
                "answers": ["library", "library reference", "stdlib"],
                "explain": "The Python Standard Library reference documents every built-in module.",
            },
        ],
    },

    # ------------------------------------------------------------------ 14
    {
        "id": "ch14",
        "title": "Interactive Editing",
        "emoji": "⌨️",
        "lessons": [
            {
                "title": "The interactive shell's editing features",
                "html": """
<p>The modern interactive shell (in Python 3.13+) is a full editing
environment, not just a dumb prompt. It is multi-line: paste a function,
move through every line, fix a typo, and run it — all before anything
executes:</p>

[[diag:repl_shell]]

<ul>
<li><b>History:</b> press the <b>up arrow</b> to recall previous commands;
<b>Ctrl-R</b> searches backwards through history.</li>
<li><b>Completion:</b> press <b>Tab</b> to complete names — try typing
<code>str.</code> then Tab to see all string methods.</li>
<li><b>Edit in place:</b> move the cursor with the arrows, and edit any
line before pressing Enter.</li>
</ul>

<p>How completion helps in practice: type <code>impo</code>, press Tab, and
it finishes to <code>import</code>. Type <code>str.</code> and press Tab
twice, and you see every string method — a built-in cheat sheet. Ctrl-R is
incremental: press it, type two letters, and the most recent matching
command appears; press Ctrl-R again to cycle to older ones.</p>

<p>On startup, Python reads the <code>PYTHONSTARTUP</code> file (if set)
— you can auto-import modules you always want, or enable extra completion
features. On Windows you may also configure the readline-style editing in
your terminal settings.</p>

<p>These habits — recalling history, tab-completing, editing before
running — are what make the REPL fast to work in. One caution: the REPL is
for <em>exploring</em>, not for long programs; anything past a dozen lines
belongs in a <code>.py</code> file you can rerun and share.</p>
""",
            },
        ],
        "quiz": [
            {
                "type": "mc",
                "question": "Which key recalls your previous REPL commands?",
                "options": [
                    "The Tab key",
                    "The up arrow key",
                    "The F1 key",
                    "Ctrl-Z",
                ],
                "answer": 1,
                "explain": "The up arrow scrolls through command history; Ctrl-R searches it.",
            },
            {
                "type": "blank",
                "question": "The key that completes names in the interactive shell is ____.",
                "answers": ["tab", "tab key", "the tab key"],
                "explain": "Tab triggers completion — try it after typing a module name and a dot.",
            },
        ],
    },

    # ------------------------------------------------------------------ 15
    {
        "id": "ch15",
        "title": "Floating-Point Arithmetic",
        "emoji": "🎯",
        "lessons": [
            {
                "title": "Why 0.1 + 0.2 is not 0.3",
                "html": """
<p>Computers store numbers in <b>binary</b>, and binary cannot represent
0.1 exactly — just as base-10 can't write 1/3 exactly. So 0.1 becomes the
closest binary fraction, which is a tiny bit more than 0.1:</p>

[[diag:float_0_1]]

<p>Concretely: a float carries 53 bits of precision (the IEEE-754
<code>double</code>), and 0.1 in binary repeats forever, so the machine
keeps the nearest representable value. This is not a bug in Python — every
language using IEEE-754 floats behaves the same way. The consequences:</p>

<pre class="code">&gt;&gt;&gt; 0.1 + 0.2
0.30000000000000004
&gt;&gt;&gt; 0.1 + 0.2 == 0.3
False</pre>

<p>Walk through the output: the sum prints as
<code>0.30000000000000004</code> because that is the closest float to the
true sum of the two stored approximations — and comparing it to
<code>0.3</code> gives <code>False</code>. One float differs from the
"clean" value by roughly 5 parts in 10<sup>17</sup>, enough to fail an
<code>==</code> test.</p>

<p>But <code>repr()</code> is clever: it prints the <i>shortest</i> string
that round-trips to the same float, so you see <code>0.1</code>, not the
approximation.</p>

<p>What to do about it:</p>
<ul>
<li>Compare with tolerance: <code>math.isclose(a, b)</code>.</li>
<li>Display with formatting: <code>f"{value:.2f}"</code>.</li>
<li>For exactness (money!), use <code>decimal.Decimal</code>.</li>
<li>Inspect the true value:
<code>(0.1).as_integer_ratio()</code> or
<code>format(0.1, '.20f')</code>.</li>
<li>Sum floats accurately with <code>math.fsum([...])</code>.</li>
</ul>

<p>Rule of thumb to internalize: floats are fine for measurements,
graphics and averages; they are wrong for money and for anything where
"off by one part in 10<sup>17</sup>" matters. When you must be exact, work
in <code>Decimal</code> from the start — converting at the end is too
late, because the float has already lost the precision.</p>
""",
            },
        ],
        "quiz": [
            {
                "type": "mc",
                "question": "Why is <code>0.1 + 0.2 == 0.3</code> False?",
                "options": [
                    "Python is buggy",
                    "0.1 and 0.2 are stored as binary approximations, so the sum is 0.30000000000000004",
                    "Float addition is disabled for fractions",
                    "The == operator doesn't work on floats",
                ],
                "answer": 1,
                "explain": "Binary can't represent 0.1 exactly, so both operands are approximations — the sum differs from 0.3 by a tiny amount.",
            },
            {
                "type": "blank",
                "question": "The function that compares floats with a tolerance is <code>math.____</code>.",
                "answers": ["isclose"],
                "explain": "math.isclose(a, b, rel_tol=...) returns True when a and b are within the tolerance.",
            },
            {
                "type": "mc",
                "question": "Which type gives EXACT decimal arithmetic for money?",
                "options": ["float", "Decimal", "int", "bool"],
                "answer": 1,
                "explain": "decimal.Decimal stores exact base-10 values: Decimal('0.1') + Decimal('0.2') == Decimal('0.3').",
            },
        ],
    },

    # ------------------------------------------------------------------ 16
    {
        "id": "ch16",
        "title": "Appendix: Interactive Mode",
        "emoji": "🪶",
        "lessons": [
            {
                "title": "Making the REPL yours",
                "html": """
<p>Interactive mode is where you'll experiment forever. A few finishing
touches from the tutorial's appendix:</p>

<ul>
<li><b>Startup file:</b> set the <code>PYTHONSTARTUP</code> environment
variable to a file. Python runs it before the first prompt — perfect for
auto-importing modules or enabling tab completion:</li>
</ul>

<pre class="code"># in your startup file
import rlcompleter, readline
readline.parse_and_bind("tab: complete")
print("Welcome to your custom Python!")</pre>

<p>Walk through it: the file imports <code>rlcompleter</code> (the
completer) and <code>readline</code> (the line editor), binds Tab to
completion, and prints a banner. Save it — say as
<code>.pythonrc.py</code> — point <code>PYTHONSTARTUP</code> at its path,
and every future interactive session starts with completion already
working.</p>

<ul>
<li><b>Customization modules:</b> <code>sitecustomize</code> runs at every
Python startup (even scripts), letting you install hooks site-wide.</li>
<li><b>Quit:</b> Ctrl-Z + Enter on Windows, Ctrl-D on Unix.</li>
<li><b>Your history:</b> your commands are saved to a history file, so
the up arrow works across sessions.</li>
</ul>

<p>Note the boundary: <code>PYTHONSTARTUP</code> affects only the
interactive shell — scripts never run it, which is exactly why
<code>sitecustomize</code> exists for site-wide setup. And if your history
or completion misbehaves, remember the shell reads these settings once at
startup: fix the file, then restart the shell.</p>

<p>That's the whole tour — sixteen chapters, from your first
<code>print()</code> to exact decimal math. Keep experimenting, and let
the <code>&gt;&gt;&gt;</code> prompt be your playground.</p>

[[diag:repl_shell]]
""",
            },
        ],
        "quiz": [
            {
                "type": "mc",
                "question": "What does the PYTHONSTARTUP file do?",
                "options": [
                    "Replaces the Python interpreter",
                    "Runs automatically before the first interactive prompt",
                    "Stores all your installed packages",
                    "Is required for Python to start",
                ],
                "answer": 1,
                "explain": "PYTHONSTARTUP points to a script that runs when the interactive shell starts — great for auto-imports.",
            },
            {
                "type": "blank",
                "question": "To enable Tab completion in the classic REPL, you bind it in the ____ module.",
                "answers": ["readline", "rlcompleter"],
                "explain": "readline.parse_and_bind('tab: complete') wires the Tab key to the rlcompleter completion module.",
            },
        ],
    },
]
