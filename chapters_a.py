"""Chapters 1-8 of the course, distilled from the Python 3.14 tutorial."""

CHAPTERS_A = [
    # ------------------------------------------------------------------ 01
    {
        "id": "ch01",
        "title": "Whetting Your Appetite",
        "emoji": "🐍",
        "lessons": [
            {
                "title": "What is Python?",
                "html": """
<p>Python is a general-purpose programming language that is easy to read,
easy to write, and runs on almost anything — your laptop, a server, or a
tiny board. It comes with a huge standard library, so you can do real work
(sending email, parsing files, running web servers) without installing
anything extra.</p>

<p>You interact with Python in two ways. The first is the <b>interactive
shell</b> (or REPL): you type a line, press Enter, and Python answers
immediately. Since Python 3.13 this shell has been a modern, colorful
interactive editor.</p>

[[diag:repl_shell]]

<p>The second way is to write a <b>script</b> — a plain text file ending in
<code>.py</code> — and run it with the <code>python</code> command. You will
learn both styles in this course.</p>
""",
            },
            {
                "title": "Why people love it",
                "html": """
<p>The Python tutorial opens with a promise: it is easy to read, and its
design philosophy values clarity. Code is indentation-based, so the structure
of a program is visible at a glance.</p>

<ul>
<li><b>Readable:</b> <code>for fruit in fruits:</code> reads like English.</li>
<li><b>Batteries included:</b> the standard library covers most daily needs.</li>
<li><b>Interactive:</b> try things instantly in the REPL before committing.</li>
<li><b>Universal:</b> the same language powers data science, web apps,
automation and education.</li>
</ul>

<p>A classic first program:</p>

<pre class="code">print("Hello, world!")</pre>

<p>That single line is a complete, runnable Python program.</p>
""",
            },
        ],
        "quiz": [
            {
                "type": "mc",
                "question": "Which of these is <b>not</b> a way to run Python code?",
                "options": [
                    "Typing it into the interactive shell",
                    "Running a .py script with the python command",
                    "Compiling it to machine code with a C compiler",
                    "Writing a script and executing it from your IDE",
                ],
                "answer": 2,
                "explain": "Python is interpreted, not compiled like C. You use the interactive shell, run scripts, or let an IDE run them for you.",
            },
            {
                "type": "blank",
                "question": "Python script files end with the file extension <code>____</code>.",
                "answers": [".py", "py"],
                "explain": "Script files use the .py extension, e.g. hello.py.",
            },
            {
                "type": "mc",
                "question": "What does the Python tutorial promise about the language?",
                "options": [
                    "It is hard to learn but very fast",
                    "It is easy to read and the standard library is huge",
                    "It only works on Windows",
                    "It cannot run interactively",
                ],
                "answer": 1,
                "explain": "The tutorial says Python is easy to read, and 'batteries included' means the standard library covers most needs.",
            },
        ],
    },

    # ------------------------------------------------------------------ 02
    {
        "id": "ch02",
        "title": "Using the Python Interpreter",
        "emoji": "⚙️",
        "lessons": [
            {
                "title": "The interpreter and the REPL",
                "html": """
<p>The interpreter is the program that reads and runs your Python code.
On Windows you can start it from the command prompt by typing
<code>python</code> (the <code>py</code> launcher also works). You'll see
the <code>&gt;&gt;&gt;</code> prompt, ready for input.</p>

[[diag:run_flow]]

<p>To run a script instead of typing interactively, give the file as an
argument:</p>

<pre class="code">python hello.py</pre>

<p>The interpreter reads the file from top to bottom and executes every
statement. When the file is the first argument, the directory it lives in
is added to <code>sys.path</code>, which matters for imports (Chapter 6).</p>

<p>You can also execute a single piece of code directly:</p>

<pre class="code">python -c "print(2 ** 10)"</pre>
""",
            },
            {
                "title": "Arguments, encoding and comments",
                "html": """
<p>To quit the interactive shell on Windows, press <code>Ctrl-Z</code>
followed by Enter. On macOS and Linux it's <code>Ctrl-D</code>.</p>

<p>Python 3 reads source files as <b>UTF-8</b> by default, so you can use
any Unicode characters — including emoji — directly in your code and
strings.</p>

<p>Comments start with <code>#</code> and run to the end of the line.
They are ignored by the interpreter but invaluable for readers — including
future you:</p>

<pre class="code"># compute the area of a circle
radius = 2.5
area = 3.14159 * radius ** 2
print(area)</pre>

<p>If a script needs command-line arguments, they are available in
<code>sys.argv</code> — a list where <code>argv[0]</code> is the script
name itself.</p>
""",
            },
        ],
        "quiz": [
            {
                "type": "mc",
                "question": "What does the <code>&gt;&gt;&gt;</code> prompt mean?",
                "options": [
                    "The script has a syntax error",
                    "Python is waiting for your input in the interactive shell",
                    "The interpreter is busy compiling",
                    "You need to install Python again",
                ],
                "answer": 1,
                "explain": ">>> is the primary prompt of the interactive shell, telling you Python is ready for the next line.",
            },
            {
                "type": "blank",
                "question": "On Windows, you exit the interactive shell by pressing Ctrl-Z followed by ____.",
                "answers": ["enter", "return", "the enter key", "return key"],
                "explain": "Windows uses Ctrl-Z + Enter; Unix-like systems use Ctrl-D.",
            },
            {
                "type": "order",
                "question": "Put these steps of running a script in the correct order:",
                "lines": [
                    "Write code in a file named hello.py",
                    "Type: python hello.py",
                    "The interpreter reads the file top to bottom",
                    "Each statement is executed and output appears",
                ],
                "explain": "First you write the file, then you invoke the interpreter with it, which reads then executes it.",
            },
        ],
    },

    # ------------------------------------------------------------------ 03
    {
        "id": "ch03",
        "title": "An Informal Introduction",
        "emoji": "🔢",
        "lessons": [
            {
                "title": "Numbers",
                "html": """
<p>Python can be your calculator. Integers (<code>int</code>) and
floating-point numbers (<code>float</code>) behave as you'd expect:</p>

<pre class="code">&gt;&gt;&gt; 2 + 3
5
&gt;&gt;&gt; 7 / 2        # division always gives a float
3.5
&gt;&gt;&gt; 7 // 2       # floor division
3
&gt;&gt;&gt; 7 % 2        # remainder
1
&gt;&gt;&gt; 2 ** 10      # power
1024</pre>

<p>Three things to remember:</p>
<ul>
<li><code>/</code> always returns a float, even when the result is whole
(e.g. <code>4 / 2</code> is <code>2.0</code>).</li>
<li><code>//</code> floors toward minus infinity: <code>-7 // 2</code> is
<code>-4</code>, not <code>-3</code>.</li>
<li><code>**</code> is the power operator; <code>%</code> gives the
remainder.</li>
</ul>

<p>Numbers are <b>immutable</b>: operations create new values, they never
change the original.</p>
""",
            },
            {
                "title": "Strings",
                "html": """
<p>Text is stored in <b>strings</b>. You can write them with single quotes,
double quotes, or triple quotes (for multi-line text):</p>

<pre class="code">&gt;&gt;&gt; s = 'Python'
&gt;&gt;&gt; s + ' rocks'     # concatenation
'Python rocks'
&gt;&gt;&gt; 'ab' * 3         # repetition
'ababab'
&gt;&gt;&gt; len(s)           # how many characters
6</pre>

<p>Every character has a position called an <b>index</b>, counting from 0.
Negative indices count from the end:</p>

[[diag:string_index]]

<p>Slicing extracts a piece of a string. <code>s[start:stop]</code> gives
everything from <code>start</code> up to — but never including —
<code>stop</code>:</p>

[[diag:string_slice]]

<p>Strings are immutable — you cannot change one character in place. You
build a new string instead.</p>
""",
            },
            {
                "title": "Lists",
                "html": """
<p>A <b>list</b> is an ordered collection of values, written with square
brackets. Unlike strings, lists are <b>mutable</b> — you can change their
contents:</p>

<pre class="code">&gt;&gt;&gt; squares = [1, 4, 9, 16, 25]
&gt;&gt;&gt; squares[0]
1
&gt;&gt;&gt; squares[-1]
25
&gt;&gt;&gt; squares[2:4]     # slicing works on lists too
[9, 16]
&gt;&gt;&gt; squares.append(36)   # add at the end
&gt;&gt;&gt; squares
[1, 4, 9, 16, 25, 36]
&gt;&gt;&gt; squares[0] = 100       # replace an item
[100, 4, 9, 16, 25, 36]</pre>

<p>Lists can hold mixed types — even other lists. <code>len()</code>,
<code>in</code> and <code>for</code> work on them just like on strings.</p>

<pre class="code">&gt;&gt;&gt; 'python' in ['python', 'java']
True
&gt;&gt;&gt; [1, 2] + [3, 4]    # concatenation
[1, 2, 3, 4]</pre>
""",
            },
        ],
        "quiz": [
            {
                "type": "mc",
                "question": "What is the value of <code>7 // 2</code>?",
                "options": ["3.5", "3", "4", "1"],
                "answer": 1,
                "explain": "// is floor division: 7 // 2 = 3 (the remainder 1 comes from 7 % 2).",
            },
            {
                "type": "codefill",
                "question": "Complete the expression so it computes 3 to the power 4:",
                "code": [
                    ">>> 3",
                    {"blank": "**", "answers": ["**", "3 ** 4"], "hint": "the power operator"},
                    " 4",
                ],
                "explain": "3 ** 4 is 81. The ** operator computes powers.",
            },
            {
                "type": "blank",
                "question": "For the string <code>s = 'Python'</code>, what is <code>s[-1]</code>? Type the character.",
                "answers": ["n"],
                "explain": "Negative indices count from the end: s[-1] is the last character, 'n'.",
            },
            {
                "type": "mc",
                "question": "Which expression returns <code>[9, 16]</code> from <code>squares = [1, 4, 9, 16, 25]</code>?",
                "options": [
                    "squares[2:4]",
                    "squares[3:5]",
                    "squares[2:3]",
                    "squares[9, 16]",
                ],
                "answer": 0,
                "explain": "squares[2:4] starts at index 2 (9) and stops before index 4 — the stop index is never included.",
            },
        ],
    },

    # ------------------------------------------------------------------ 04
    {
        "id": "ch04",
        "title": "More Control Flow",
        "emoji": "🔀",
        "lessons": [
            {
                "title": "if, for, while and friends",
                "html": """
<p>The <code>if</code> statement makes decisions. Notice the colon and the
<b>indentation</b> — indentation is how Python groups statements:</p>

[[diag:if_flow]]

<pre class="code">if x &gt; 0:
    print('positive')
elif x == 0:
    print('zero')
else:
    print('negative')</pre>

<p><code>for</code> loops over any <b>iterable</b> — a list, a string, or a
range of numbers. <code>range(n)</code> produces 0 up to n-1:</p>

[[diag:for_loop]]

<pre class="code">for i in range(5):
    print(i)

for letter in 'abc':
    print(letter)</pre>

<p><code>while</code> repeats as long as a condition is true. A loop's
<code>else</code> clause runs when the loop finishes <i>without</i> a
<code>break</code>. And <code>pass</code> does nothing — it's a placeholder
for code you haven't written yet.</p>

<pre class="code">n = 5
while n &gt; 0:
    n -= 1
    print(n)</pre>
""",
            },
            {
                "title": "Functions, defaults and lambdas",
                "html": """
<p>Functions are defined with <code>def</code>. A function takes
parameters, does work, and optionally <code>return</code>s a value.
Every function call runs in a fresh local scope:</p>

<pre class="code">def greet(name, greeting="Hello"):
    '''Print a friendly greeting.'''
    return f"{greeting}, {name}!"

print(greet("Ada"))            # Hello, Ada!
print(greet("Bob", "Hi"))      # Hi, Bob!</pre>

<p>Key ideas:</p>
<ul>
<li>Parameters can have <b>default values</b> — here <code>greeting</code>
defaults to <code>"Hello"</code>.</li>
<li>The string right after <code>def</code> is the <b>docstring</b>;
<code>help(greet)</code> shows it.</li>
<li>Arguments can be passed by position <i>or</i> by keyword:
<code>greet(name="Ada")</code>.</li>
<li>Default values are evaluated once at definition time — never use a
mutable default like <code>def f(x=[])</code>.</li>
</ul>

<p>A <b>lambda</b> is a tiny anonymous function, handy where a function is
needed briefly:</p>

<pre class="code">square = lambda x: x * x
print(square(5))        # 25</pre>
""",
            },
            {
                "title": "match and more",
                "html": """
<p>Since Python 3.10 you can use <code>match</code> — a pattern-matching
statement that is more powerful than a chain of if/elif:</p>

<pre class="code">def describe(value):
    match value:
        case 0:
            return "zero"
        case [x, y]:
            return f"a list of two: {x}, {y}"
        case _:
            return "something else"

print(describe(0))             # zero
print(describe([1, 2]))        # a list of two: 1, 2</pre>

<p>The underscore <code>_</code> matches anything — it's the default case.</p>

<p>Also worth knowing: the <code>range</code> function can take a start, a
stop and a step — <code>range(0, 10, 2)</code> is <code>0, 2, 4, 6, 8</code>.</p>
""",
            },
        ],
        "quiz": [
            {
                "type": "mc",
                "question": "What does <code>range(5)</code> produce?",
                "options": [
                    "1, 2, 3, 4, 5",
                    "0, 1, 2, 3, 4",
                    "0, 1, 2, 3, 4, 5",
                    "5, 4, 3, 2, 1",
                ],
                "answer": 1,
                "explain": "range(n) gives 0 up to n-1, so range(5) is 0, 1, 2, 3, 4.",
            },
            {
                "type": "codefill",
                "question": "Fill in the blank so this loop prints each letter of 'abc':",
                "code": [
                    "for letter",
                    {"blank": "in", "answers": ["in"], "hint": "the keyword that feeds values from an iterable"},
                    " 'abc':",
                    "    print(letter)",
                ],
                "explain": "for x in iterable: is the standard loop over an iterable.",
            },
            {
                "type": "blank",
                "question": "Complete the function header: <code>def greet(name, greeting=____):</code> so the greeting is optional. Type the default value.",
                "answers": ['"hello"', "'hello'", "hello"],
                "explain": "A default value makes a parameter optional: def greet(name, greeting='Hello').",
            },
            {
                "type": "mc",
                "question": "Which loop's <code>else</code> clause runs?",
                "options": [
                    "A loop that ends with a break",
                    "A loop that finishes without a break",
                    "A while loop with a false condition",
                    "Both B and C",
                ],
                "answer": 3,
                "explain": "A loop's else runs when the loop completes without hitting break — including a while loop whose condition is immediately false.",
            },
        ],
    },

    # ------------------------------------------------------------------ 05
    {
        "id": "ch05",
        "title": "Data Structures",
        "emoji": "🧱",
        "lessons": [
            {
                "title": "Lists: stacks, queues and references",
                "html": """
<p>Lists are the workhorse of Python. Handy methods:</p>

<pre class="code">fruits = ['orange', 'apple', 'pear']
fruits.append('banana')     # add at the end
fruits.insert(0, 'kiwi')    # insert at position 0
fruits.remove('apple')      # remove first match
fruits.pop()                # remove & return the last item
fruits.sort()               # sort in place
fruits.index('pear')        # position of an item
'pear' in fruits            # membership test -> True</pre>

<p><b>Important:</b> assigning a list to another name does <b>not</b> copy
it — both names point at the same list. Use a slice <code>[:]</code> or
<code>list()</code> to copy:</p>

[[diag:list_aliasing]]

<pre class="code">a = [1, 2, 3]
b = a          # same list!
b.append(4)    # a is also changed
c = a[:]       # a real copy</pre>

<p>Use a list as a <b>stack</b> with <code>append()</code> and
<code>pop()</code>. For a <b>queue</b> (fast removal from the front), use
<code>collections.deque</code> instead — popping index 0 of a long list is
slow.</p>
""",
            },
            {
                "title": "Tuples, sets and dictionaries",
                "html": """
<p>A <b>tuple</b> is an immutable sequence — write it with parentheses (or
just commas). It's perfect for fixed records like coordinates:</p>

<pre class="code">point = (3, 4)
x, y = point          # unpacking
single = (1,)         # trailing comma needed!</pre>

<p>A <b>set</b> stores unique values and answers membership tests in a
blink. Create one with <code>{}</code> or <code>set()</code>:</p>

<pre class="code">basket = {'apple', 'orange', 'apple'}
len(basket)           # 2  (duplicates vanish)
'apple' in basket     # True
basket &amp; {'apple', 'pear'}   # intersection
basket | {'pear'}             # union</pre>

<p>A <b>dictionary</b> maps keys to values:</p>

[[diag:dict_map]]

<pre class="code">d = {'name': 'Ada', 'age': 36}
d['city'] = 'London'        # add a key
d.get('name')               # 'Ada' (None if missing)
d.keys(), d.values()        # views of the mapping
for k, v in d.items():      # loop over pairs
    print(k, v)</pre>

<p>Dictionary keys must be immutable — strings, numbers, tuples of
immutables. That's why a list can't be a key.</p>
""",
            },
            {
                "title": "Comprehensions and looping tricks",
                "html": """
<p>A <b>list comprehension</b> builds a list in one readable line:</p>

<pre class="code">squares = [x ** 2 for x in range(10)]
# [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]

evens = [x for x in range(20) if x % 2 == 0]</pre>

<p>There are dict and set comprehensions too, plus nested ones:</p>

<pre class="code">{x: x ** 2 for x in range(5)}
{x for x in 'abracadabra' if x not in 'abc'}</pre>

<p>Handy tools when looping:</p>

<pre class="code">for i, v in enumerate(['a', 'b']):   # index and value
for a, b in zip(xs, ys):             # pair up two lists
for x in reversed(xs):               # backwards
for x in sorted(xs):                 # sorted copy</pre>

<p>To loop over a dictionary's keys and values together, use
<code>d.items()</code>.</p>
""",
            },
        ],
        "quiz": [
            {
                "type": "mc",
                "question": "Given <code>a = [1, 2, 3]</code> then <code>b = a</code>, which statement is true?",
                "options": [
                    "b is a copy of a; changing b leaves a alone",
                    "a and b are two different lists",
                    "b points to the same list as a; changing one changes both",
                    "b can never be modified",
                ],
                "answer": 2,
                "explain": "b = a copies the reference, not the list. Both names see the same object. Use a[:] for a copy.",
            },
            {
                "type": "blank",
                "question": "A ____ is an immutable sequence written with commas — often with parentheses.",
                "answers": ["tuple"],
                "explain": "Tuples are immutable: t = (1, 2) or even 1, 2.",
            },
            {
                "type": "mc",
                "question": "What does <code>[x * 2 for x in range(4)]</code> produce?",
                "options": [
                    "[0, 2, 4, 6]",
                    "[2, 4, 6, 8]",
                    "[0, 2, 4, 6, 8]",
                    "An error: you can't multiply in a comprehension",
                ],
                "answer": 0,
                "explain": "range(4) is 0..3, each doubled: [0, 2, 4, 6].",
            },
            {
                "type": "codefill",
                "question": "Fill the blank so this builds a set of unique letters from the word:",
                "code": [
                    "word = 'hello'",
                    "letters = ",
                    {"blank": "{c for c in word}", "answers": ["{c for c in word}", "set(c for c in word)", "set(word)"], "hint": "a set comprehension, or set()"},
                ],
                "explain": "A set comprehension {c for c in word} keeps unique letters: {'h', 'e', 'l', 'o'}. set(word) does the same.",
            },
        ],
    },

    # ------------------------------------------------------------------ 06
    {
        "id": "ch06",
        "title": "Modules",
        "emoji": "📦",
        "lessons": [
            {
                "title": "Importing modules",
                "html": """
<p>A <b>module</b> is a file of Python code you can reuse. Once a module
is imported, its functions become available:</p>

<pre class="code">import math
print(math.sqrt(16))        # 4.0

from math import sqrt, pi   # import specific names
print(sqrt(16), pi)

import math as m            # alias
print(m.factorial(5))</pre>

<p>Where does Python look for modules? It searches the list in
<code>sys.path</code>, in order: the script's own directory, then
<code>PYTHONPATH</code>, then the standard library and site-packages.</p>

[[diag:module_syspath]]

<p>To see everything a module offers, use <code>dir(module)</code>. To
inspect what a function does, use <code>help(module.function)</code>.</p>
""",
            },
            {
                "title": "Packages and relative imports",
                "html": """
<p>A <b>package</b> is a folder of modules that groups related code. Each
folder traditionally contains an <code>__init__.py</code> file (possibly
empty) to mark it as a package — though Python 3 also supports
"namespace packages" without it:</p>

<pre class="code">sound/                  # top-level package
    __init__.py
    formats/
        __init__.py
        wavread.py
    effects/
        __init__.py
        echo.py</pre>

<p>Import with dots:</p>

<pre class="code">import sound.effects.echo
from sound.effects import echo
from sound.effects.echo import echofilter</pre>

<p>Inside a package, a module can use <b>relative imports</b> with leading
dots: <code>from .. import formats</code> means "the parent package".
The <code>dir()</code> function lists all names in a module — run
<code>dir()</code> with no argument to see what you've defined.</p>
""",
            },
        ],
        "quiz": [
            {
                "type": "mc",
                "question": "Which line imports only the name <code>sqrt</code> from math?",
                "options": [
                    "import math.sqrt",
                    "from math import sqrt",
                    "import sqrt from math",
                    "include sqrt from math",
                ],
                "answer": 1,
                "explain": "The syntax is 'from module import name' — it imports just that name into your namespace.",
            },
            {
                "type": "blank",
                "question": "The list of directories Python searches for modules is stored in <code>sys.____</code>.",
                "answers": ["path", "sys.path"],
                "explain": "sys.path is the list of directories searched, in order, when you import a module.",
            },
            {
                "type": "codefill",
                "question": "Import the <code>random</code> module so the call works:",
                "code": [
                    {"blank": "import random", "answers": ["import random"], "hint": "the import statement"},
                    "",
                    "print(random.choice(['a', 'b', 'c']))",
                ],
                "explain": "import random makes the module available as random, so random.choice works.",
            },
        ],
    },

    # ------------------------------------------------------------------ 07
    {
        "id": "ch07",
        "title": "Input and Output",
        "emoji": "📤",
        "lessons": [
            {
                "title": "Formatting output",
                "html": """
<p><b>f-strings</b> are the modern way to build strings with values
embedded. Put an <code>f</code> before the quote and wrap expressions in
curly braces:</p>

<pre class="code">name = 'Ada'
age = 36
print(f"{name} is {age} years old")
# Ada is 36 years old</pre>

<p>The <code>=</code> trick prints the expression and its value — ideal
for debugging:</p>

[[diag:fstring_eq]]

<p>You can control alignment and padding with format specifiers:</p>

<pre class="code">print(f"{'left':&lt;10}|")      # pad to width 10
print(f"{3.14159:.2f}")       # 3.14
print(f"{42:04d}")            # 0042</pre>

<p>Older styles still exist: <code>"{} {}".format(a, b)</code> and the
<code>%</code> operator — you'll see them in old code, but f-strings are
the recommended choice today.</p>
""",
            },
            {
                "title": "Files and JSON",
                "html": """
<p>Reading and writing files uses the built-in <code>open()</code> — almost
always inside a <code>with</code> block, which closes the file for you even
if an error occurs:</p>

<pre class="code">with open('notes.txt', 'w') as f:
    f.write('Hello, file!\n')

with open('notes.txt', 'r') as f:
    for line in f:
        print(line, end='')</pre>

<p>Modes: <code>'r'</code> read (default), <code>'w'</code> write (creates
or overwrites), <code>'a'</code> append, <code>'b'</code> binary.
By default, reading text decodes UTF-8.</p>

<p>To share data between programs, JSON is the lingua franca. Python makes
it trivial:</p>

<pre class="code">import json

data = {'name': 'Ada', 'age': 36}
with open('data.json', 'w') as f:
    json.dump(data, f)

with open('data.json') as f:
    loaded = json.load(f)     # {'name': 'Ada', 'age': 36}</pre>
""",
            },
        ],
        "quiz": [
            {
                "type": "blank",
                "question": "Given <code>n = 42</code>, write an f-string that prints <code>n = 42</code> (the name and its value). Type it exactly.",
                "answers": ['f"{n=}"', 'f"{n =}"', 'f"{n = }"'],
                "explain": "The = specifier prints the expression and its value: f\"{n=}\" → n=42.",
            },
            {
                "type": "mc",
                "question": "What does <code>print(f\"{3.14159:.2f}\")</code> print?",
                "options": ["3.14", "3.14159", "3.1", "3.142"],
                "answer": 0,
                "explain": ".2f rounds to 2 decimal places: 3.14.",
            },
            {
                "type": "codefill",
                "question": "Complete this code so the file is automatically closed after the block:",
                "code": [
                    "with open('data.txt', 'w')",
                    {"blank": "as f:", "answers": ["as f:", "as f"], "hint": "the with...as syntax"},
                    "    f.write('hi')",
                ],
                "explain": "with open(...) as f: guarantees the file is closed when the block ends, even on errors.",
            },
        ],
    },

    # ------------------------------------------------------------------ 08
    {
        "id": "ch08",
        "title": "Errors and Exceptions",
        "emoji": "🚨",
        "lessons": [
            {
                "title": "try / except / else / finally",
                "html": """
<p>Errors are normal — even good programs run into them. Python's answer is
<b>exceptions</b>: when something goes wrong, an exception is raised, and
if nothing catches it, the program stops with a traceback.</p>

<p>You can handle exceptions with <code>try</code>/<code>except</code>:</p>

<pre class="code">try:
    number = int(input("Enter a number: "))
except ValueError:
    print("That was not a number!")

try:
    result = 10 / 0
except ZeroDivisionError:
    print("Can't divide by zero")
except (TypeError, ValueError) as err:
    print("Something else:", err)</pre>

<p>Remember: <code>except</code> only catches the listed exception types —
a bare <code>except:</code> catches everything, including
<code>KeyboardInterrupt</code>, so it's rarely what you want.</p>

<p>The full pattern has two extra clauses: <code>else</code> runs when
<em>no</em> exception happened, and <code>finally</code> always runs —
perfect for cleanup:</p>

<pre class="code">try:
    risky_operation()
except OSError:
    print("operation failed")
else:
    print("operation succeeded")
finally:
    print("this always runs")</pre>
""",
            },
            {
                "title": "Raising, chaining and groups",
                "html": """
<p>You can raise exceptions yourself with <code>raise</code>:</p>

<pre class="code">def set_age(age):
    if age &lt; 0:
        raise ValueError("age must be positive")
    return age</pre>

<p>Exceptions form a <b>hierarchy</b> — catching a parent catches all its
children:</p>

[[diag:exception_tree]]

<p><code>raise ... from ...</code> chains an exception to its cause, so you
can translate a low-level error into a friendlier one without losing the
details:</p>

<pre class="code">try:
    data = open("missing.txt").read()
except OSError as err:
    raise RuntimeError("could not load config") from err</pre>

<p>Modern Python also gives you <b>exception groups</b> — several
exceptions raised at once — handled with <code>except*</code>, and the
<code>add_note()</code> method to attach extra context to any exception.</p>

<pre class="code">try:
    raise ExceptionGroup("both failed", [ValueError("a"), TypeError("b")])
except* ValueError:
    print("handled the ValueError part")</pre>
""",
            },
        ],
        "quiz": [
            {
                "type": "mc",
                "question": "Which clause ALWAYS runs, whether or not an exception happened?",
                "options": ["except", "else", "finally", "raise"],
                "answer": 2,
                "explain": "finally runs no matter what — exception or not, break or return — making it ideal for cleanup.",
            },
            {
                "type": "blank",
                "question": "The keyword that intentionally triggers an exception is ____.",
                "answers": ["raise"],
                "explain": "raise ValueError('message') creates and throws an exception of the given type.",
            },
            {
                "type": "codefill",
                "question": "Catch the error so the program doesn't crash. Fill the blank:",
                "code": [
                    "try:",
                    "    x = 1 / 0",
                    "except",
                    {"blank": "ZeroDivisionError:", "answers": ["zerodivisionerror:", "zerodivisionerror"], "hint": "the exception raised by division by zero"},
                    "    print('oops')",
                ],
                "explain": "except ZeroDivisionError: catches exactly that error (and its subclasses).",
            },
            {
                "type": "order",
                "question": "Arrange these lines so that 'always' prints regardless of errors:",
                "lines": [
                    "try:",
                    "    x = 1 / 0",
                    "except ZeroDivisionError:",
                    "    print('oops')",
                    "finally:",
                    "    print('always')",
                ],
                "explain": "try ... except ... finally: the finally block always executes, even when an exception is raised and caught.",
            },
        ],
    },
]
