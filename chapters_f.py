"""Chapters 28-31 of the course, distilled from the Python 3.14
Language Reference.

The reference is a lookup document, not a tutorial — so, per the
course philosophy, these chapters are a TOUR of the parts that
matter day to day: the data model, scopes & execution, expressions
& operators, and the import system. The full grammar and lexical
spec stay in the real reference for lookup.
"""

CHAPTERS_F = [
    # ------------------------------------------------------------------ 28
    {
        "id": "ch28",
        "title": "The Data Model",
        "title_fa": "مدل داده",
        "emoji": "\U0001f4e6",
        "lessons": [
            {
                "title": "Objects: identity, type, value",
                "html": """
<p>Everything in Python is an <b>object</b> — numbers, strings,
functions, even modules. The reference gives every object three
properties:</p>

<ul>
<li><b>Identity</b> — the object's address in memory, fixed for
  its lifetime. The <code>is</code> operator tests identity;
  <code>id(x)</code> returns it as an integer.</li>
<li><b>Type</b> — decides what you can do with it
  (<code>len()</code>? iterate? add?). <code>type(x)</code>
  returns it, and it never changes.</li>
<li><b>Value</b> — the data it holds.</li>
</ul>

[[diag:object_model]]

<p>The classic confusion: <code>==</code> compares <b>values</b>,
<code>is</code> compares <b>identities</b>:</p>

<pre class="code">a = [1, 2, 3]
b = [1, 2, 3]
a == b      # True   -&gt; same values
a is b      # False  -&gt; two different list objects

c = a       # c now points at the SAME object as a
a is c      # True</pre>

<p>Objects are <b>mutable</b> or <b>immutable</b>: numbers, strings
and tuples can't change once created; lists, dicts and sets can.
The subtle case — a tuple holding a list is still immutable as a
container, but its value <em>appears</em> to change when the list
inside changes:</p>

<pre class="code">t = ([1], [2])
t[0].append(3)     # t is still a tuple, but now holds ([1, 3], [2])</pre>

<p>When an object becomes unreachable, Python garbage-collects it
— but the docs are explicit: <b>don't rely on when</b>. That's why
files and sockets have explicit <code>close()</code> methods and
the <code>with</code> statement exists. Two reference gotchas worth
remembering:</p>

<ul>
<li><code>e = f = []</code> assigns the SAME list to both names
  (not two lists) — the reference calls this out explicitly.</li>
<li>Since 3.14, using <code>NotImplemented</code> in a boolean
  context (<code>if x == y is NotImplemented:</code>) now raises
  <code>TypeError</code> instead of silently being truthy.</li>
</ul>
""",
            },
            {
                "title": "Special methods — classes that act like builtins",
                "html": """
<p>Double-underscore ("dunder") methods are Python's contract for
"make my class behave like a built-in". The interpreter calls them
for you when you use syntax — so defining a few makes your objects
print nicely, support <code>len()</code>, indexing, iteration, and
operators:</p>

<pre class="code">class Point:
    def __init__(self, x, y):       # called by Point(3, 4)
        self.x, self.y = x, y

    def __repr__(self):             # friendly string for print()
        return f'Point({self.x}, {self.y})'

    def __eq__(self, other):        # powers ==
        return (self.x, self.y) == (other.x, other.y)

    def __add__(self, other):       # powers +
        return Point(self.x + other.x, self.y + other.y)

p1 = Point(3, 4)
p2 = Point(3, 4)
print(p1)               # -&gt; Point(3, 4)      (thanks to __repr__)
p1 == p2                # -&gt; True             (thanks to __eq__)
p1 + p2                 # -&gt; Point(6, 8)      (thanks to __add__)</pre>

[[diag:dunder_power]]

<p>The most useful ones, and the syntax they power:</p>

<pre class="code">__init__(self, ...)    # Point(3, 4)          construction
__repr__ / __str__     # print(obj), str(obj) display
__len__                # len(obj)             size
__getitem__ / __setitem__  # obj[0], obj[0] = x  indexing
__iter__ / __next__    # for x in obj:        iteration
__contains__           # x in obj             membership
__call__               # obj()                callable objects
__eq__ / __lt__        # == &lt;                comparisons</pre>

<p>That's the whole trick behind dataclasses (chapter 21): the
decorator writes these methods for you. When you see a built-in
type doing something, some dunder is doing the work.</p>
""",
            },
        ],
        "quiz": [
            {
                "type": "mc",
                "question": "What does the == operator compare?",
                "options": [
                    "the objects' identities (memory addresses)",
                    "the objects' values",
                    "the objects' types",
                    "the objects' variable names",
                ],
                "answer": 1,
                "explain": "== compares values; is compares identity. Two equal lists are not the same object.",
            },
            {
                "type": "blank",
                "question": "Test whether two names point at the same object: a ____ b",
                "answers": ["is"],
                "explain": "is compares identity — True only if both names reference the very same object.",
            },
            {
                "type": "codefill",
                "question": "Give the class a friendly repr so print() shows something nice:",
                "code": [
                    "class Point:",
                    "    def __init__(self, x, y):",
                    "        self.x, self.y = x, y",
                    "    def __",
                    {"blank": "repr", "answers": ["repr"], "hint": "the dunder for a display string"},
                    "__(self):",
                    "        return f'Point({self.x}, {self.y})'",
                ],
                "explain": "def __repr__(self) tells the interpreter how to display the object — print(p) then shows Point(3, 4).",
            },
            {
                "type": "mc",
                "question": "Which of these is immutable?",
                "options": ["list", "dict", "tuple", "set"],
                "answer": 2,
                "explain": "Tuples are immutable — though a tuple holding a list can appear to change when that list is modified.",
            },
        ],
    },

    # ------------------------------------------------------------------ 29
    {
        "id": "ch29",
        "title": "Scopes & How Programs Run",
        "title_fa": "اسکوپ‌ها و نحوهٔ اجرای برنامه‌ها",
        "emoji": "\U0001f333",
        "lessons": [
            {
                "title": "Names, binding and scopes",
                "html": """
<p>Names <b>refer to objects</b>; they don't contain them. The
reference calls the act of pointing a name at an object
<b>binding</b>, and lists what binds names: assignment,
<code>def</code>, <code>class</code>, <code>import</code>, the
<code>for</code> loop header, <code>with ... as</code>, and
<code>except ... as</code>.</p>

<p>Here's the rule that surprises everyone: <b>if a name is
assigned anywhere in a function, it's local to the whole
function</b> — even before the assignment. That's the
<code>UnboundLocalError</code> trap:</p>

<pre class="code">count = 10

def buggy():
    print(count)      # UnboundLocalError!
    count = 5         # 'count' is local because of this line

def fine():
    global count      # now 'count' means the module-level one
    print(count)      # -&gt; 10
    count = 5</pre>

[[diag:global_nonlocal]]

<p>Names resolve in the <b>nearest enclosing scope</b> — local,
then enclosing functions, then global, then builtins. To write to
an outer function's variable from a nested function, say so:</p>

<pre class="code">def counter():
    n = 0
    def bump():
        nonlocal n        # n lives in the enclosing function
        n += 1
        return n
    return bump

c = counter()
c()   # -&gt; 1
c()   # -&gt; 2</pre>

<p>Two more scope rules from the reference: a <code>class</code>
block binds names, but they live <b>only</b> inside the class
block — methods can't see them implicitly, and neither can
comprehensions inside the class. And a missing name raises
<code>NameError</code>; using a local before it's bound raises its
subclass <code>UnboundLocalError</code>.</p>
""",
            },
            {
                "title": "Blocks, frames and the call stack",
                "html": """
<p>How does a program actually <em>run</em>? The reference's
answer: a Python program is made of <b>code blocks</b> — a module,
a function body, a class body, one line typed at the REPL, a
<code>-c</code> command. Each block runs inside an <b>execution
frame</b>, which is a fancy name for "a namespace plus a
bookmark saying where execution is".</p>

<pre class="code"># every script runs as the module called __main__
print(__name__)          # -&gt; '__main__'   when run directly</pre>

<p>Function calls stack up: <code>main()</code> calls
<code>work()</code>, which calls <code>helper()</code>. Each gets
its own frame with its own locals. When a function returns, its
frame is discarded — that's why locals vanish afterwards.</p>

<p><b>Exceptions</b> use the same stack: when one is raised and
not caught, Python walks up the frames looking for a matching
<code>except</code>. If nothing catches it, the program ends and
Python prints the <b>traceback</b> — which is literally a map of
those frames:</p>

<pre class="code">def helper():
    return 1 / 0          # ZeroDivisionError raised here

def work():
    return helper()       # ...propagates up here

def main():
    return work()         # ...and here

main()                    # traceback shows all three frames</pre>

<p>Reading a traceback bottom-up is the skill: the last lines show
<b>where</b> it happened (file, line, function), the first line
tells you <b>what</b> happened. Three things that keep objects
alive longer than you'd expect (from the reference): an open
traceback, an exception bound in <code>except</code>, and a
function's default arguments — a classic pitfall:</p>

<pre class="code">def append(item, items=[]):    # the default list is created ONCE
    items.append(item)
    return items

append(1)   # -&gt; [1]
append(2)   # -&gt; [1, 2]   surprise! It's the same list.</pre>

<p>The fix: <code>def append(item, items=None):</code> and create
the list inside. That's the reference's model in one lesson:
blocks, frames, a stack for calls, and the same stack for
exceptions.</p>
""",
            },
        ],
        "quiz": [
            {
                "type": "mc",
                "question": "You assign to a name anywhere inside a function. What is true of that name?",
                "options": [
                    "it is local throughout the whole function",
                    "it is global unless declared otherwise",
                    "it is only local after the assignment line",
                    "it raises a SyntaxError",
                ],
                "answer": 0,
                "explain": "A name bound anywhere in a block is local to the whole block — using it before the assignment raises UnboundLocalError.",
            },
            {
                "type": "blank",
                "question": "Write to a module-level variable from inside a function: ____ count",
                "answers": ["global", "global count", "global count;"],
                "explain": "The global statement says 'this name refers to the module-level binding', letting you read and write it.",
            },
            {
                "type": "codefill",
                "question": "Let the inner function modify the outer function's variable:",
                "code": [
                    "def counter():",
                    "    n = 0",
                    "    def bump():",
                    "        ",
                    {"blank": "nonlocal n", "answers": ["nonlocal n", "nonlocal"], "hint": "the keyword for the nearest enclosing function scope"},
                    "        n += 1",
                    "        return n",
                    "    return bump",
                ],
                "explain": "nonlocal n makes n refer to the enclosing function's binding, so n += 1 updates it instead of creating a new local.",
            },
            {
                "type": "mc",
                "question": "Where do names bound inside a class block live?",
                "options": [
                    "they are visible automatically to the class's methods",
                    "only inside the class block — not in its methods",
                    "they become module globals",
                    "they are deleted when the class is created",
                ],
                "answer": 1,
                "explain": "A class block has its own scope; its names don't leak into methods (or comprehensions inside the class).",
            },
        ],
    },

    # ------------------------------------------------------------------ 30
    {
        "id": "ch30",
        "title": "Expressions & Operators",
        "title_fa": "عبارت‌ها و عملگرها",
        "emoji": "\u2795",
        "lessons": [
            {
                "title": "Operator precedence — who binds first?",
                "html": """
<p>Expressions are the sentences of Python, and operators decide
how they're grouped. The reference's precedence table, from the
tightest binding to the loosest:</p>

<pre class="code">( )  [ ]  { }     atoms: literals, names, calls, indexing
**                 power (right-associative!)
+x  -x  ~x         unary plus/minus/bitwise-not
*  /  //  %  @     multiplication, division, modulo
+  -               addition, subtraction
&lt;&lt;  &gt;&gt;             shifts
&amp;                  bitwise and
^                  bitwise xor
|                  bitwise or
in  not in  is  is not  &lt;  &lt;=  &gt;  &gt;=  ==  !=   comparisons
not x              boolean not
and                boolean and
or                 boolean or
if – else          conditional expression
:=                 assignment expression (walrus)
lambda             anonymous functions</pre>

[[diag:operator_precedence]]

<p>Two lines trip people up more than any others:</p>

<pre class="code">2 ** 3 ** 2      # -&gt; 512    ** is RIGHT-associative: 2 ** (3 ** 2)
-3 ** 2          # -&gt; -9     unary minus binds looser than **: -(3 ** 2)</pre>

<p>Comparisons <b>chain</b> like math — one <code>x</code>, two
checks, evaluated left to right:</p>

<pre class="code">x = 5
0 &lt; x &lt; 10       # -&gt; True    (0 &lt; x and x &lt; 10, x evaluated once)
'a' &lt; 'b' &lt; 'c'  # -&gt; True    works on strings too</pre>

<p>Truthiness decides <code>and</code>/<code>or</code>:
<code>and</code> returns the first falsy value, else the last;
<code>or</code> returns the first truthy value, else the last.
That's why <code>name or 'guest'</code> works as a default.</p>
""",
            },
            {
                "title": "Atoms, comprehensions and the walrus",
                "html": """
<p>At the bottom of every expression sit the <b>atoms</b>: literals
(<code>42</code>, <code>'hi'</code>, <code>[1,2]</code>,
<code>{'a':1}</code>), names, and parenthesized groups. Everything
else is built on them.</p>

<p>Comprehensions deserve their own mention in the reference
because they're functions in disguise: each has its <b>own
scope</b>, so the loop variable doesn't leak (this changed years
ago — in old Python, <code>[n for n in range(3)]</code> left
<code>n</code> around afterward):</p>

<pre class="code">squares = [n * n for n in range(4)]   # -&gt; [0, 1, 4, 9]
n                                     # -&gt; NameError (contained!)

pairs = {(a, b) for a in 'xy' for b in range(2)}   # set of tuples
total = sum(n for n in range(101))                # generator</pre>

<p>The <b>walrus</b> <code>:=</code> assigns and returns in one
step — the reference added it in 3.8 and it earns its place in
loops and conditions:</p>

<pre class="code">line = input('&gt; ')
while (line := input('&gt; ')) != 'quit':
    print('you said', line)</pre>

<p>Slices are expressions too: <code>s[i:j]</code> is
<code>s[slice(i, j)]</code> — that's why custom classes implement
<code>__getitem__</code> with a <code>slice</code> object to
support them. And calls: <code>f(*args, **kwargs)</code> unpacks
positional and keyword arguments, the mirror image of
<code>def f(*args, **kwargs)</code>.</p>

<p>When in doubt about grouping, the reference has a one-word
answer: parentheses. They never hurt, and they make your intent
obvious to the next reader — including future you.</p>
""",
            },
        ],
        "quiz": [
            {
                "type": "mc",
                "question": "Which operator binds TIGHTEST?",
                "options": ["or", "==", "**", "lambda"],
                "answer": 2,
                "explain": "Atoms and ** bind tightest; or and lambda bind loosest of all.",
            },
            {
                "type": "blank",
                "question": "A comparison written as 0 &lt; x &lt; 10 is called a ____ comparison",
                "answers": ["chained"],
                "explain": "Comparisons chain: 0 < x < 10 means (0 < x) and (x < 10), with x evaluated once.",
            },
            {
                "type": "codefill",
                "question": "What does this expression print? 2 + 3 * 4",
                "code": [
                    "result = 2 + 3 * 4    # * binds tighter than +",
                    "print(result)         # ",
                    {"blank": "14", "answers": ["14"], "hint": "the computed value"},
                ],
                "explain": "3 * 4 = 12, then 2 + 12 = 14 — multiplication binds tighter than addition.",
            },
            {
                "type": "mc",
                "question": "After this line runs, what is the value of n?\n[n * 2 for n in range(3)]",
                "options": [
                    "2 — the last value from the loop",
                    "a NameError — the comprehension has its own scope",
                    "0 — the first value",
                    "None",
                ],
                "answer": 1,
                "explain": "Comprehensions run in their own scope, so the loop variable doesn't leak into the enclosing code.",
            },
        ],
    },

    # ------------------------------------------------------------------ 31
    {
        "id": "ch31",
        "title": "The Import System",
        "title_fa": "سیستم import",
        "emoji": "\U0001f4e4",
        "lessons": [
            {
                "title": "How import finds your code",
                "html": """
<p>You've used <code>import</code> since lesson one — here's what
actually happens, per the reference's <code>import</code>
chapter. When you write <code>import os</code>, Python:</p>

<ol>
<li><b>Checks the cache</b> — <code>sys.modules</code>, a dict of
  already-imported modules. If it's there, you get it instantly.</li>
<li><b>Searches <code>sys.path</code></b> — in order: the current
  directory / script's folder, everything in
  <code>PYTHONPATH</code>, the standard library, and
  <code>site-packages</code> for third-party packages.</li>
<li><b>Runs the module's code once</b>, then stores the result in
  <code>sys.modules</code> so every later import is free.</li>
</ol>

[[diag:import_search]]

<pre class="code">import sys
sys.path[:3]      # look at where Python will search</pre>

<p>The "runs once" part explains a lot of real-world behavior:
module-level code executes on first import, so keep side effects
out of modules — put them in functions. And if two modules import
each other (a cycle), the half-finished module is what the second
one sees.</p>

<p><code>import</code> also binds a name: <code>import os</code>
gives you <code>os</code>; <code>from os import path</code> binds
<code>path</code> directly. Want everything?
<code>from module import *</code> binds every public name — but
the reference notes it's only allowed at module level and is best
avoided in your own code.</p>
""",
            },
            {
                "title": "Packages, relative imports and __main__",
                "html": """
<p>A <b>package</b> is a folder of modules — the way real projects
organize code. To make a folder importable, give it an
<code>__init__.py</code> (it can be empty; it marks the folder as a
package and runs when the package is imported):</p>

<pre class="code">mypkg/
    __init__.py
    utils.py
    models/
        __init__.py
        user.py

import mypkg.utils          # full path
from mypkg.models.user import User</pre>

<p>Inside a package, <b>relative imports</b> use dots — one dot for
the current package, two for the parent:</p>

<pre class="code"># inside mypkg/utils.py
from . import helpers           # mypkg/helpers.py
from ..models import user       # parent package's models

# WRONG: plain 'import helpers' would look in sys.path, not the package</pre>

<p>Every script you run becomes the module <code>__main__</code> —
and that's the secret behind the most common idiom in Python:</p>

<pre class="code">def main():
    print('doing the thing')

if __name__ == '__main__':   # only when run directly
    main()</pre>

<p>Run directly (<code>python tool.py</code>):
<code>__name__</code> is <code>'__main__'</code>, so
<code>main()</code> runs. Imported by another file:
<code>__name__</code> is <code>'tool'</code>, so nothing runs —
the file acts as a library. The same guard makes scripts safe to
test and reuse. And <code>python -m mypkg.utils</code> runs a
module "as main" — the -m flag you met in chapter 17.</p>
""",
            },
        ],
        "quiz": [
            {
                "type": "order",
                "question": "Put the import pipeline in order:",
                "lines": [
                    "Python checks sys.modules (the import cache)",
                    "if absent, it searches sys.path for the module",
                    "it executes the module's code once",
                    "the module's names become available",
                ],
                "explain": "Cache first, then search sys.path, then run once — later imports of the same module are free.",
            },
            {
                "type": "blank",
                "question": "A script run directly is executed as the module ____",
                "answers": ["__main__"],
                "explain": "Directly-run scripts get __name__ == '__main__', which is what the if __name__ == '__main__' guard checks.",
            },
            {
                "type": "mc",
                "question": "Why does importing the same module twice cost almost nothing?",
                "options": [
                    "the module is cached in sys.modules after the first import",
                    "Python compiles it to a .pyc file and skips execution",
                    "the interpreter forbids importing twice",
                    "it's re-executed but very fast",
                ],
                "answer": 0,
                "explain": "sys.modules caches the loaded module; a second import looks it up and returns it without re-running the code.",
            },
            {
                "type": "codefill",
                "question": "Run main() only when the script is executed directly:",
                "code": [
                    "def main():",
                    "    print('hi')",
                    "",
                    "if __name__ == '",
                    {"blank": "__main__", "answers": ["__main__"], "hint": "the special name of the directly-run module"},
                    "':",
                    "    main()",
                ],
                "explain": "When run directly __name__ is '__main__', so main() runs; when imported, the guard keeps it a library.",
            },
        ],
    },
]
