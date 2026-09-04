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
<p>A <b>class</b> is a blueprint for objects. Objects bundle data
(attributes) with functions that act on it (methods). The special method
<code>__init__</code> sets up each new instance:</p>

<pre class="code">class Dog:
    def __init__(self, name):
        self.name = name      # attribute

    def bark(self):           # method
        return f"{self.name} says Woof!"

d = Dog("Rex")
print(d.name)      # Rex
print(d.bark())    # Rex says Woof!</pre>

<p>Every method takes <code>self</code> first — the instance itself. You
never pass it yourself; Python does.</p>

<p>Classes support <b>inheritance</b>: a child class reuses everything
from its parent and can override or extend it. Multiple inheritance is
possible (a class can have several parents), and every class ultimately
derives from <code>object</code>.</p>

<pre class="code">class Puppy(Dog):
    def bark(self):
        return "yip yip!"

print(Puppy("Scooby").bark())   # yip yip!</pre>
""",
            },
            {
                "title": "Scopes, name mangling and iterators",
                "html": """
<p>Python resolves names with the <b>LEGB</b> rule — search Local, then
Enclosing, then Global, then Built-in:</p>

[[diag:scope_le]]

<pre class="code">def outer():
    x = 10
    def inner():
        nonlocal x      # refers to the enclosing scope's x
        x += 1
        return x
    return inner()</pre>

<p>Variables inside a class are still found through normal scopes —
methods don't automatically see class attributes; use
<code>self.attribute</code>. To avoid accidental name clashes, a
double-underscore prefix triggers <b>name mangling</b>:
<code>self.__secret</code> becomes <code>self._ClassName__secret</code>.</p>

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
Here are the tools for everyday scripting:</p>

<pre class="code">import os, glob, sys

os.getcwd()                    # current directory
os.walk('.')                   # walk a directory tree

for name in glob.glob('*.txt'):   # filename patterns
    print(name)

print(sys.argv)                # command-line arguments</pre>

<p>For proper command-line programs, <code>argparse</code> parses options
and generates help:</p>

<pre class="code">import argparse

p = argparse.ArgumentParser(prog='greet')
p.add_argument('name')
p.add_argument('--loud', action='store_true')
args = p.parse_args()

msg = f"Hello, {args.name}"
print(msg.upper() if args.loud else msg)</pre>
""",
            },
            {
                "title": "Regular expressions and math",
                "html": """
<p><code>re</code> is the regular-expression engine — pattern matching on
text:</p>

<pre class="code">import re

re.findall(r'\\d+', 'Room 404, floor 7')   # ['404', '7']
re.sub(r'\\s+', ' ', 'a    b  c')          # 'a b c'
if re.search(r'^cat', 'catalog'):
    print("starts with cat")</pre>

<p>The <code>math</code> module covers common math, and
<code>statistics</code> handles everyday stats:</p>

<pre class="code">import math, statistics

math.sqrt(16)              # 4.0
math.hypot(3, 4)           # 5.0
math.isclose(0.1 + 0.2, 0.3, rel_tol=1e-9)   # True

statistics.mean([1, 2, 3, 4])    # 2.5
statistics.median([1, 2, 3])     # 2
statistics.variance([1, 2, 3])   # 1.0</pre>

<p>For random values use <code>random</code>: <code>random.choice(items)</code>,
<code>random.sample(items, k)</code>, <code>random.randrange(6)</code>.</p>

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

<p><code>threading</code> runs work in parallel. Threads share memory, so
they're great for I/O-bound tasks (waiting on network or files):</p>

<pre class="code">import threading, time

def worker(name):
    time.sleep(0.5)
    print(f"{name} done")

for name in ['a', 'b']:
    threading.Thread(target=worker, args=(name,)).start()</pre>

<p>And <code>logging</code> replaces <code>print</code> for serious
programs — timestamps, levels, and multiple destinations out of the box:</p>

<pre class="code">import logging
logging.basicConfig(level=logging.INFO)
logging.info("job started")</pre>
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

<p>For keeping data sorted or always taking the smallest item:</p>

<pre class="code">import bisect, heapq

bisect.insort(sorted_list, 5)      # insert, keeping order
heapq.heappush(heap, 3)            # priority queue
heapq.heappop(heap)                # smallest first</pre>

<p>Floating-point arithmetic is inexact (Chapter 15). When you need exact
decimal math — money, accounting — use <code>decimal</code>:</p>

<pre class="code">from decimal import Decimal
Decimal('0.1') + Decimal('0.2')    # Decimal('0.3') — exact!</pre>
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
disappear — project A can use requests 2.31 while project B uses 2.32.</p>

[[diag:venv_boxes]]

<p>Create and use one:</p>

<pre class="code">python -m venv myenv</pre>

<p>Then <b>activate</b> it so its commands take over your shell:</p>

<pre class="code"># Windows
myenv\\Scripts\\activate

# macOS / Linux
source myenv/bin/activate</pre>

<p>Your prompt changes to show the environment. When you're done,
<code>deactivate</code> leaves it.</p>
""",
            },
            {
                "title": "pip and requirements.txt",
                "html": """
<p>Inside an active environment, <code>pip</code> installs packages from
the Python Package Index (PyPI):</p>

<pre class="code">pip install requests
pip list                     # what's installed
pip search "query"           # search PyPI</pre>

<p>To make your project reproducible, record its dependencies in
<code>requirements.txt</code> and install them with one command:</p>

<pre class="code">pip freeze &gt; requirements.txt
pip install -r requirements.txt</pre>

<p>Anyone — on any machine — can then recreate your exact setup. That's
why environments plus a requirements file are the standard way to ship
Python projects.</p>
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
<p>You've finished the tutorial — congratulations! The tutorial itself
points to the next steps of your journey:</p>

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

<p>Reading is good, but <b>building is better</b>. The best next step is
to pick a small project — a to-do list, a web scraper, a quiz game — and
write it. When you get stuck, the interactive shell is your friend: try
the piece, then assemble the whole.</p>
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
environment, not just a dumb prompt:</p>

[[diag:repl_shell]]

<ul>
<li><b>History:</b> press the <b>up arrow</b> to recall previous commands;
<b>Ctrl-R</b> searches backwards through history.</li>
<li><b>Completion:</b> press <b>Tab</b> to complete names — try typing
<code>str.</code> then Tab to see all string methods.</li>
<li><b>Edit in place:</b> move the cursor with the arrows, and edit any
line before pressing Enter.</li>
</ul>

<p>On startup, Python reads the <code>PYTHONSTARTUP</code> file (if set)
— you can auto-import modules you always want, or enable extra completion
features. On Windows you may also configure the readline-style editing in
your terminal settings.</p>

<p>These habits — recalling history, tab-completing, editing before
running — are what make the REPL fast to work in.</p>
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

<p>This is not a bug in Python — every language using IEEE-754 floats
behaves the same way. The consequences:</p>

<pre class="code">&gt;&gt;&gt; 0.1 + 0.2
0.30000000000000004
&gt;&gt;&gt; 0.1 + 0.2 == 0.3
False</pre>

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

<ul>
<li><b>Customization modules:</b> <code>sitecustomize</code> runs at every
Python startup (even scripts), letting you install hooks site-wide.</li>
<li><b>Quit:</b> Ctrl-Z + Enter on Windows, Ctrl-D on Unix.</li>
<li><b>Your history:</b> your commands are saved to a history file, so
the up arrow works across sessions.</li>
</ul>

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
