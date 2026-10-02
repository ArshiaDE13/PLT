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

<p>Why reach for it? Python was designed so that programs read almost like
English: where other languages bury an idea under punctuation and
boilerplate, Python keeps the idea in front. Scientists, teachers and
automation engineers pick it for that reason.</p>

<p>You interact with Python in two ways. The first is the <b>interactive
shell</b> (or REPL): you type a line, press Enter, and Python answers
immediately. Since Python 3.13 this shell has been a modern, colorful
interactive editor.</p>

[[diag:repl_shell]]

<p>The second way is to write a <b>script</b> — a plain text file ending in
<code>.py</code> — and run it with the <code>python</code> command. You will
learn both styles in this course.</p>

<p>How it works: Python is an <b>interpreted</b> language. The interpreter
reads your source top to bottom and runs it right away — no separate
compile-and-link step like in C. That means instant feedback: change a
line, run again, see the result. The trade-off is that some mistakes only
surface when a line actually runs, so you test as you go.</p>

<p>One gotcha before you start: on some Linux and macOS machines the
command <code>python</code> still points to the old Python 2, so you must
type <code>python3</code>. Check with <code>python --version</code> — this
course assumes Python 3.14, and everything in it needs a 3.x interpreter.</p>
""",
            },
            {
                "title": "Why people love it",
                "html": """
<p>The Python tutorial opens with a promise: it is easy to read, and its
design philosophy values clarity. Code is indentation-based, so the structure
of a program is visible at a glance — there are no braces to balance and no
semicolons to forget.</p>

<ul>
<li><b>Readable:</b> <code>for fruit in fruits:</code> reads like English.</li>
<li><b>Batteries included:</b> the standard library covers most daily needs.</li>
<li><b>Interactive:</b> try things instantly in the REPL before committing.</li>
<li><b>Universal:</b> the same language powers data science, web apps,
automation and education.</li>
</ul>

<p>Why do these points matter in practice? Readability means a colleague (or
you, six months from now) can open a file and understand it without a decoder
ring. Batteries included means you write <code>import json</code> instead of
hunting for a third-party library. Interactive means you can test one small
idea — "how does this function behave?" — without building a whole program
around it.</p>

<p>A classic first program:</p>

<pre class="code">print("Hello, world!")</pre>

<p>Walk through it: <code>print</code> is a built-in function that takes
whatever you give it, converts it to text, and writes it to the screen. This
single line is a complete, runnable Python program — save it as
<code>hello.py</code>, run <code>python hello.py</code>, and you have written
real software. In many languages the same job needs a class declaration, a
main function and a compile step; here it is one line. That economy is why
people fall in love with the language.</p>
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

<p>Here is how a REPL session goes: you type a line, Python evaluates it,
and if the line produced a value, that value is printed back. Type
<code>2 + 2</code> and you see <code>4</code>. Type <code>x = 5</code> and
you see nothing — assignment produces no value, but <code>x</code> now
exists for the rest of the session. The REPL is the fastest way to answer
small questions, which is why experienced Pythonistas keep one open all
day.</p>

[[diag:run_flow]]

<p>To run a script instead of typing interactively, give the file as an
argument:</p>

<pre class="code">python hello.py</pre>

<p>The interpreter reads the file from top to bottom and executes every
statement — output appears as each <code>print</code> runs, and the process
exits when the last line finishes. When the file is the first argument, the
directory it lives in is added to <code>sys.path</code>, which matters for
imports (Chapter 6). Use the REPL to experiment; use scripts for anything
you want to keep and run again.</p>

<p>You can also execute a single piece of code directly:</p>

<pre class="code">python -c "print(2 ** 10)"</pre>

<p>The <code>-c</code> flag means "run this string as Python code". Here it
prints <code>1024</code>, because <code>**</code> is the power operator: 2
to the 10th is 1024. The trick is handy in shell pipelines and for quick
calculations without opening the REPL at all.</p>
""",
            },
            {
                "title": "Arguments, encoding and comments",
                "html": """
<p>To quit the interactive shell on Windows, press <code>Ctrl-Z</code>
followed by Enter. On macOS and Linux it's <code>Ctrl-D</code>.</p>

<p>Python 3 reads source files as <b>UTF-8</b> by default, so you can use
any Unicode characters — including emoji — directly in your code and
strings. If you ever see a <code>UnicodeDecodeError</code>, the file was
saved in some other encoding (often Windows-1252); re-save it as UTF-8 and
the problem disappears.</p>

<p>Comments start with <code>#</code> and run to the end of the line.
They are ignored by the interpreter but invaluable for readers — including
future you:</p>

<pre class="code"># compute the area of a circle
radius = 2.5
area = 3.14159 * radius ** 2
print(area)</pre>

<p>Walk through it: the first line is a comment, skipped entirely. Then
<code>radius</code> is bound to 2.5, and <code>area</code> is computed with
<code>**</code> (power) before <code>*</code> (multiply) — so this is 3.14159
times 6.25, and the program prints <code>19.6349375</code>. Comments should
explain <em>why</em>, not restate the code: <code># radius in cm</code>
helps; <code># set radius</code> does not.</p>

<p>If a script needs command-line arguments, they are available in
<code>sys.argv</code> — a list where <code>argv[0]</code> is the script
name itself, and the user's arguments follow. Run
<code>python demo.py hello 42</code> and inside the script
<code>sys.argv</code> is <code>['demo.py', 'hello', '42']</code>. Note the
trap: every argument arrives as a <b>string</b>, so convert with
<code>int()</code> before doing math on it.</p>
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
floating-point numbers (<code>float</code>) behave as you'd expect — but
each operator has a precise meaning you should know on sight:</p>

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

<p>Walk through the output: <code>2 + 3</code> is ordinary addition.
<code>7 / 2</code> is <code>3.5</code> — true division, always a float.
<code>7 // 2</code> is <code>3</code> — floor division, which throws the
fraction away. <code>7 % 2</code> is <code>1</code>, the remainder — this is
how you test even and odd: <code>n % 2 == 0</code> means even.
<code>2 ** 10</code> is <code>1024</code>: the power operator, the reason a
million is written <code>10 ** 6</code>.</p>

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

<p>Two more facts worth keeping. First, Python ints never overflow:
<code>2 ** 200</code> returns an exact 61-digit number, because Python
quietly switches to big integers. Second, floats are binary approximations —
<code>0.1 + 0.2</code> prints <code>0.30000000000000004</code>, a surprise we
dissect in Chapter 15. Rule of thumb: count with <code>int</code>, and never
compare floats with <code>==</code>.</p>
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

<p>Walk through it: <code>+</code> glues strings together and <code>*</code>
repeats them — <code>'ab' * 3</code> is <code>'ababab'</code>.
<code>len(s)</code> counts characters, spaces and punctuation included.
Mixing types is an error: <code>'age: ' + 30</code> raises a
<code>TypeError</code>, so convert first with <code>str(30)</code> or use an
f-string (Chapter 7).</p>

<p>Every character has a position called an <b>index</b>, counting from 0.
Negative indices count from the end:</p>

[[diag:string_index]]

<p>Slicing extracts a piece of a string. <code>s[start:stop]</code> gives
everything from <code>start</code> up to — but never including —
<code>stop</code>:</p>

[[diag:string_slice]]

<p>The rule that makes slices predictable: the length of <code>s[a:b]</code>
is always <code>b - a</code>. Omit <code>start</code> to begin at the start
of the string, omit <code>stop</code> to run to the end — so
<code>s[:3]</code> is <code>'Pyt'</code> and <code>s[3:]</code> is
<code>'hon'</code>.</p>

<p>Strings are immutable — you cannot change one character in place. You
build a new string instead.</p>

<p>That immutability bites beginners: <code>s[0] = 'J'</code> raises
<code>TypeError</code>. Build a new string — <code>s = 'J' + s[1:]</code> —
and remember that methods like <code>upper()</code> and <code>strip()</code>
return a <em>new</em> string: <code>name.upper()</code> alone never changes
<code>name</code> unless you assign the result back.</p>
""",
            },
            {
                "title": "Lists",
                "html": """
<p>A <b>list</b> is an ordered collection of values, written with square
brackets. Whenever you need to keep "many things" — scores, names, rows of
a table — you reach for a list. Unlike strings, lists are <b>mutable</b>:
you can change their contents without building a new object:</p>

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

<p>Walk through it: <code>squares[0]</code> is <code>1</code> because
indexing starts at 0, and <code>squares[-1]</code> is <code>25</code> because
a negative index counts from the end. The slice <code>squares[2:4]</code>
returns a <em>new</em> list, <code>[9, 16]</code> — the stop index is never
included. Then <code>append(36)</code> grows the list in place, and
<code>squares[0] = 100</code> replaces the first item. (The REPL echoes each
result; in a script you would need <code>print(...)</code> to see them.)</p>

<p>Lists can hold mixed types — even other lists. <code>len()</code>,
<code>in</code> and <code>for</code> work on them just like on strings.</p>

<pre class="code">&gt;&gt;&gt; 'python' in ['python', 'java']
True
&gt;&gt;&gt; [1, 2] + [3, 4]    # concatenation
[1, 2, 3, 4]</pre>

<p>The first line asks a question — "is <code>'python'</code> one of the
options?" — and gets <code>True</code>. The second builds a third list from
two: <code>+</code> concatenation never modifies its operands.</p>

<p>Gotcha to carry with you: <code>append()</code> returns <code>None</code>
because it changes the list in place. Write <code>x =
squares.append(36)</code> and <code>x</code> is <code>None</code>, not the
list — a classic beginner bug. And a list stores <em>references</em>, not
copies; Chapter 5 shows what happens when two names share one list.</p>
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
<p>The <code>if</code> statement makes decisions. Python checks each
condition top to bottom and runs the <em>first</em> true branch — everything
else is skipped. Notice the colon and the <b>indentation</b> — indentation
is how Python groups statements; four spaces is the convention, and mixing
tabs with spaces is an error:</p>

[[diag:if_flow]]

<pre class="code">if x &gt; 0:
    print('positive')
elif x == 0:
    print('zero')
else:
    print('negative')</pre>

<p>With <code>x = 5</code> this prints <code>positive</code>; with
<code>x = -2</code> it prints <code>negative</code>. Exactly one of the three
branches ever runs.</p>

<p><code>for</code> loops over any <b>iterable</b> — a list, a string, or a
range of numbers. <code>range(n)</code> produces 0 up to n-1:</p>

[[diag:for_loop]]

<pre class="code">for i in range(5):
    print(i)

for letter in 'abc':
    print(letter)</pre>

<p>The first loop prints <code>0</code> through <code>4</code>, one per line
— five numbers, never 5 itself. The second prints <code>a</code>,
<code>b</code>, <code>c</code>: looping over a string gives you its
characters one at a time.</p>

<p><code>while</code> repeats as long as a condition is true. A loop's
<code>else</code> clause runs when the loop finishes <i>without</i> a
<code>break</code>. And <code>pass</code> does nothing — it's a placeholder
for code you haven't written yet.</p>

<pre class="code">n = 5
while n &gt; 0:
    n -= 1
    print(n)</pre>

<p>Trace it: <code>n</code> starts at 5 and the body subtracts 1 each pass,
so it prints <code>4, 3, 2, 1, 0</code>. The classic mistake is forgetting
to change the loop variable — if the body never moves <code>n</code> toward
0, the condition stays true forever and the program hangs. When a while
loop seems stuck, check that first.</p>
""",
            },
            {
                "title": "Functions, defaults and lambdas",
                "html": """
<p>Functions are defined with <code>def</code>. A function takes
parameters, does work, and optionally <code>return</code>s a value.
Every function call runs in a fresh local scope: names you create inside
vanish when the function returns.</p>

<pre class="code">def greet(name, greeting="Hello"):
    '''Print a friendly greeting.'''
    return f"{greeting}, {name}!"

print(greet("Ada"))            # Hello, Ada!
print(greet("Bob", "Hi"))      # Hi, Bob!</pre>

<p>Walk through it: the first call passes only <code>name</code>, so
<code>greeting</code> falls back to its default and you get
<code>Hello, Ada!</code>. The second call overrides the default and prints
<code>Hi, Bob!</code>. One distinction to burn in: <code>return</code> hands
a value back to the caller, while <code>print</code> just displays text. A
function with no <code>return</code> gives back <code>None</code> — so
<code>x = print("hi")</code> sets <code>x</code> to <code>None</code>, a bug
beginners hit constantly.</p>

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

<p><code>lambda x: x * x</code> takes one input and returns its square, so
<code>square(5)</code> is <code>25</code>. A lambda is limited to a single
expression — no statements. Rule of thumb: if the logic needs a name or more
than one line, write a normal <code>def</code>; save lambdas for one-shot
spots like <code>sorted(data, key=lambda item: item[1])</code>.</p>
""",
            },
            {
                "title": "match and more",
                "html": """
<p>Since Python 3.10 you can use <code>match</code> — a pattern-matching
statement that is more powerful than a chain of if/elif. Where if/elif can
only ask "is this equal to that?", a <code>case</code> can check the
<em>shape</em> of a value: its type, its length, even the pieces inside
it:</p>

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

<p>Walk through it: <code>describe(0)</code> hits <code>case 0</code> and
returns <code>"zero"</code>. <code>describe([1, 2])</code> matches
<code>case [x, y]</code> because the value is a two-item list — and the
pattern <em>binds</em> its items to <code>x</code> and <code>y</code>, so
the f-string prints <code>a list of two: 1, 2</code>. That capture is the
superpower: destructuring while matching. A three-item list would skip this
case and fall through.</p>

<p>The underscore <code>_</code> matches anything — it's the default case.
Order matters: Python tries the cases top to bottom and runs the first one
that fits, so put specific patterns before general ones. Omitting
<code>case _</code> is allowed — a value matching nothing simply falls out
of the match untouched.</p>

<p>Also worth knowing: the <code>range</code> function can take a start, a
stop and a step — <code>range(0, 10, 2)</code> is <code>0, 2, 4, 6, 8</code>.
A negative step counts down: <code>range(5, 0, -1)</code> gives
<code>5, 4, 3, 2, 1</code>.</p>

<p>Rule of thumb: use if/elif for simple true-or-false checks, and reach for
<code>match</code> when the real question is "what <em>kind</em> of thing is
this?"</p>
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

<p>Walk through the verbs: <code>append</code> adds one item at the end,
<code>insert(0, 'kiwi')</code> squeezes an item in at position 0 and shifts
everything else right, <code>remove</code> deletes the <em>first</em> match
(and raises <code>ValueError</code> if it isn't there), <code>pop</code>
removes and hands back the last item, <code>sort</code> orders the list in
place, and <code>index</code> reports where an item lives. Note the split:
methods like <code>sort</code> and <code>append</code> change the list and
return <code>None</code>.</p>

<p><b>Important:</b> assigning a list to another name does <b>not</b> copy
it — both names point at the same list. Use a slice <code>[:]</code> or
<code>list()</code> to copy:</p>

[[diag:list_aliasing]]

<pre class="code">a = [1, 2, 3]
b = a          # same list!
b.append(4)    # a is also changed
c = a[:]       # a real copy</pre>

<p>Trace it: after <code>b = a</code> there is still <em>one</em> list with
two labels. Appending through <code>b</code> is visible through <code>a</code>
— print both and each shows <code>[1, 2, 3, 4]</code>. But <code>c =
a[:]</code> builds a second, independent list; later changes to <code>a</code>
leave <code>c</code> alone. Aliasing bites every programmer once — make it
your once.</p>

<p>Use a list as a <b>stack</b> with <code>append()</code> and
<code>pop()</code>. For a <b>queue</b> (fast removal from the front), use
<code>collections.deque</code> instead — popping index 0 of a long list is
slow.</p>

<p>Why slow? A list is one contiguous block, so removing the front item
forces Python to slide every remaining element left by one — a million-item
list pays for a million moves. A <code>deque</code> pops from both ends in
constant time.</p>
""",
            },
            {
                "title": "Tuples, sets and dictionaries",
                "html": """
<p>A <b>tuple</b> is an immutable sequence — write it with parentheses (or
just commas). It's perfect for fixed records like coordinates: once created,
nothing can be added, removed or reordered, which makes tuples safe to share
and to use as dictionary keys:</p>

<pre class="code">point = (3, 4)
x, y = point          # unpacking
single = (1,)         # trailing comma needed!</pre>

<p><code>x, y = point</code> is <b>unpacking</b>: Python pulls the tuple
apart into two names, so <code>x</code> is <code>3</code> and <code>y</code>
is <code>4</code>. The trailing comma in <code>(1,)</code> is not decoration
— <code>(1)</code> is just the number 1 in parentheses; the comma is what
makes the tuple. This is the classic tuple typo.</p>

<p>A <b>set</b> stores unique values and answers membership tests in a
blink. Create one with <code>{}</code> or <code>set()</code>:</p>

<pre class="code">basket = {'apple', 'orange', 'apple'}
len(basket)           # 2  (duplicates vanish)
'apple' in basket     # True
basket &amp; {'apple', 'pear'}   # intersection
basket | {'pear'}             # union</pre>

<p>The duplicate <code>'apple'</code> evaporates — <code>len(basket)</code>
is <code>2</code>. Membership (<code>in</code>) stays fast even in huge
collections, because sets are hashed. <code>&amp;</code> keeps values present
in both sets (intersection); <code>|</code> merges them (union). And an empty
set is <code>set()</code>, not <code>{}</code> — bare braces mean an empty
dictionary.</p>

<p>A <b>dictionary</b> maps keys to values:</p>

[[diag:dict_map]]

<pre class="code">d = {'name': 'Ada', 'age': 36}
d['city'] = 'London'        # add a key
d.get('name')               # 'Ada' (None if missing)
d.keys(), d.values()        # views of the mapping
for k, v in d.items():      # loop over pairs
    print(k, v)</pre>

<p>Think of it as an index-card file: <code>d['city'] = 'London'</code> files
a new card, and <code>d.get('name')</code> looks one up — politely returning
<code>None</code> when the key is missing, while <code>d['missing']</code>
would raise <code>KeyError</code>. The loop at the end prints
<code>name Ada</code>, then <code>age 36</code>, then <code>city London</code>.</p>

<p>Dictionary keys must be immutable — strings, numbers, tuples of
immutables. That's why a list can't be a key.</p>
""",
            },
            {
                "title": "Comprehensions and looping tricks",
                "html": """
<p>A <b>list comprehension</b> builds a list in one readable line. Read it
as a sentence: "for every x in range(10), give me x squared". It replaces a
three-line loop — create, append, return — with a single expression:</p>

<pre class="code">squares = [x ** 2 for x in range(10)]
# [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]

evens = [x for x in range(20) if x % 2 == 0]</pre>

<p>The first line produces <code>[0, 1, 4, 9, 16, 25, 36, 49, 64, 81]</code>.
The second adds a filter: the <code>if</code> clause keeps only the values
that pass the test, so <code>evens</code> holds <code>0, 2, 4, ..., 18</code>.
Comprehensions are also a little faster than the equivalent loop, because the
iteration runs in optimized C code.</p>

<p>There are dict and set comprehensions too, plus nested ones:</p>

<pre class="code">{x: x ** 2 for x in range(5)}
{x for x in 'abracadabra' if x not in 'abc'}</pre>

<p>The first builds <code>{0: 0, 1: 1, 2: 4, 3: 9, 4: 16}</code> — keys
mapped to their squares. The second keeps the characters of
<code>'abracadabra'</code> that are not in <code>'abc'</code>, yielding
<code>{'r', 'd'}</code>. Swap the brackets to pick your container:
<code>[]</code> list, <code>{}</code> set or dict, <code>()</code> a lazy
generator that produces values on demand.</p>

<p>Handy tools when looping:</p>

<pre class="code">for i, v in enumerate(['a', 'b']):   # index and value
for a, b in zip(xs, ys):             # pair up two lists
for x in reversed(xs):               # backwards
for x in sorted(xs):                 # sorted copy</pre>

<p><code>enumerate</code> hands you the index and the value together, so you
can stop writing <code>range(len(xs))</code> — that pattern is considered
un-Pythonic. <code>zip</code> pairs two sequences item by item, stopping at
the shorter one; <code>reversed</code> and <code>sorted</code> give you a
backwards or an ordered pass. All four work in any <code>for</code> loop,
not just comprehensions.</p>

<p>To loop over a dictionary's keys and values together, use
<code>d.items()</code>.</p>

<p>Two rules of thumb: don't nest comprehensions more than one level deep —
past that, a plain loop reads better — and don't rely on the loop variable
after a comprehension finishes; in Python 3 its scope stays inside the
comprehension.</p>
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
<p>A <b>module</b> is a file of Python code you can reuse. The standard
library ships with hundreds — <code>math</code>, <code>random</code>,
<code>json</code>, <code>datetime</code> — and importing one makes
everything in it available under the module's own name, which keeps your
namespace tidy:</p>

<pre class="code">import math
print(math.sqrt(16))        # 4.0

from math import sqrt, pi   # import specific names
print(sqrt(16), pi)

import math as m            # alias
print(m.factorial(5))</pre>

<p>Three styles, one result: <code>import math</code> gives you the whole
module — call <code>math.sqrt(16)</code> and get <code>4.0</code>.
<code>from math import sqrt, pi</code> copies just two names in, so you call
plain <code>sqrt(16)</code>. <code>import math as m</code> gives the module
a short alias. All three run the module's code exactly once — a second
import of the same module is free, because Python caches it in
<code>sys.modules</code>.</p>

<p>Where does Python look for modules? It searches the list in
<code>sys.path</code>, in order: the script's own directory, then
<code>PYTHONPATH</code>, then the standard library and site-packages.</p>

[[diag:module_syspath]]

<p>To see everything a module offers, use <code>dir(module)</code>. To
inspect what a function does, use <code>help(module.function)</code>.</p>

<p>Two gotchas. First, never name your own file after a module you use: a
file called <code>math.py</code> in your folder shadows the real
<code>math</code>, because the script's directory is searched first — and
suddenly <code>math.sqrt</code> "doesn't exist". Second, avoid
<code>from math import *</code>: dumping every name into your namespace
hides where names come from and can silently overwrite your own
variables.</p>
""",
            },
            {
                "title": "Packages and relative imports",
                "html": """
<p>A <b>package</b> is a folder of modules that groups related code. As a
project grows past a handful of files, you stop dumping everything in one
directory and start arranging it into packages. Each folder traditionally
contains an <code>__init__.py</code> file (possibly empty) to mark it as a
package — though Python 3 also supports "namespace packages" without it:</p>

<pre class="code">sound/                  # top-level package
    __init__.py
    formats/
        __init__.py
        wavread.py
    effects/
        __init__.py
        echo.py</pre>

<p>Read the tree top-down: <code>sound</code> is the top-level package, and
it contains the subpackage <code>formats</code> (with <code>wavread.py</code>)
and the subpackage <code>effects</code> (with <code>echo.py</code>). The full
dotted name of the echo module is <code>sound.effects.echo</code> — the
folder structure <em>is</em> the import path.</p>

<p>Import with dots:</p>

<pre class="code">import sound.effects.echo
from sound.effects import echo
from sound.effects.echo import echofilter</pre>

<p>All three lines load the same module. The first keeps the whole chain,
so you must call <code>sound.effects.echo.echofilter(...)</code> spelled out
in full. The second binds the short name <code>echo</code>. The third copies
just the function itself — the most convenient, and the easiest way to lose
track of where a name came from.</p>

<p>Inside a package, a module can use <b>relative imports</b> with leading
dots: <code>from .. import formats</code> means "the parent package". One
dot is the current package, two dots the parent. Relative imports only work
<em>inside</em> a package — run such a module directly as a script and they
fail with "attempted relative import with no known parent package".</p>

<p>The <code>dir()</code> function lists all names in a module — run
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
curly braces — and note <em>expressions</em>, not just variables:
<code>f"{age * 12} months"</code> computes inside the braces:</p>

<pre class="code">name = 'Ada'
age = 36
print(f"{name} is {age} years old")
# Ada is 36 years old</pre>

<p>At run time Python evaluates each braced expression and splices the
result into the string, so this prints <code>Ada is 36 years old</code>.
Anything Python can evaluate — arithmetic, method calls, function calls —
works inside the braces.</p>

<p>The <code>=</code> trick prints the expression and its value — ideal
for debugging:</p>

[[diag:fstring_eq]]

<p><code>f"{n=}"</code> expands to <code>n=42</code>, name and value in one
shot — much faster than typing the label yourself.</p>

<p>You can control alignment and padding with format specifiers — the part
after the colon:</p>

<pre class="code">print(f"{'left':&lt;10}|")      # pad to width 10
print(f"{3.14159:.2f}")       # 3.14
print(f"{42:04d}")            # 0042</pre>

<p>Walk through it: <code>:&lt;10</code> left-aligns in a field 10 characters
wide — good for tables. <code>:.2f</code> rounds to 2 decimal places and
prints <code>3.14</code>. <code>:04d</code> zero-pads an integer to 4 digits,
printing <code>0042</code> — perfect for file names and timestamps that must
sort correctly.</p>

<p>Older styles still exist: <code>"{} {}".format(a, b)</code> and the
<code>%</code> operator — you'll see them in old code, but f-strings are
the recommended choice today. Rule of thumb: reach for an f-string unless
the template itself comes from outside your program; then use
<code>.format()</code>, because a template from elsewhere cannot execute
expressions.</p>
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

<p>The first block opens <code>notes.txt</code> in write mode and drops in
one line. The second reopens it for reading and prints it back: looping over
a file object yields one line at a time, and <code>end=''</code> suppresses
<code>print</code>'s extra newline because each line already ends with
<code>\n</code>. For a small file you could call <code>f.read()</code> and
get everything at once; the loop is what you want for a multi-gigabyte log.</p>

<p>Modes: <code>'r'</code> read (default), <code>'w'</code> write (creates
or overwrites), <code>'a'</code> append, <code>'b'</code> binary.
By default, reading text decodes UTF-8.</p>

<p>Encoding gotchas: <code>'w'</code> destroys the file the instant it
opens — open a 500-line file for writing and close it, and you have an
empty file. If you mean to add to it, use <code>'a'</code>. And when writing
text that other tools will read, pass <code>encoding='utf-8'</code>
explicitly; otherwise Python may use the machine's local encoding and your
file shows mojibake elsewhere.</p>

<p>To share data between programs, JSON is the lingua franca. Python makes
it trivial:</p>

<pre class="code">import json

data = {'name': 'Ada', 'age': 36}
with open('data.json', 'w') as f:
    json.dump(data, f)

with open('data.json') as f:
    loaded = json.load(f)     # {'name': 'Ada', 'age': 36}</pre>

<p><code>json.dump</code> writes the dictionary as JSON text;
<code>json.load</code> reads it back into a brand-new dictionary. The round
trip preserves strings, numbers, lists, dicts, booleans and <code>None</code>
(written as <code>null</code>) — but not tuples, sets or your own objects.
For those you need a different format.</p>
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
if nothing catches it, the program stops with a traceback. A traceback is
not a monster — read it bottom-up: the last line names the error, the lines
above show exactly where it happened.</p>

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

<p>Walk through it: if the user types <code>abc</code>, <code>int()</code>
raises <code>ValueError</code>, control jumps into the handler, and the
program prints <code>That was not a number!</code> instead of crashing. The
second example guards a division — dividing by zero raises
<code>ZeroDivisionError</code> — and shows that one <code>try</code> can
have several <code>except</code> clauses, including a tuple of types bound
to a name with <code>as err</code>. After an exception, the rest of the
<code>try</code> body is skipped; execution never falls through it.</p>

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

<p>On success you see "operation succeeded" then "this always runs"; on
failure, "operation failed" then "this always runs". Rule of thumb: keep
only the risky line inside <code>try</code>, put the code that depends on
its success in <code>else</code>, and reserve <code>finally</code> (or
better, <code>with</code>) for cleanup.</p>
""",
            },
            {
                "title": "Raising, chaining and groups",
                "html": """
<p>You can raise exceptions yourself with <code>raise</code> — this is how
functions refuse bad input early, instead of producing nonsense
downstream:</p>

<pre class="code">def set_age(age):
    if age &lt; 0:
        raise ValueError("age must be positive")
    return age</pre>

<p>Call <code>set_age(-5)</code> and the function stops immediately with
<code>ValueError: age must be positive</code>. The message exists for the
human who has to fix the call — <code>raise ValueError("bad input")</code>
tells you nothing six months later, so always say what was wrong.</p>

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

<p>If <code>missing.txt</code> doesn't exist, the <code>OSError</code> is
caught and a <code>RuntimeError</code> is raised in its place — but the
traceback still shows the original error underneath, labeled as the direct
cause. That chain is gold when you're debugging why config loading broke.</p>

<p>Modern Python also gives you <b>exception groups</b> — several
exceptions raised at once — handled with <code>except*</code>, and the
<code>add_note()</code> method to attach extra context to any exception.</p>

<pre class="code">try:
    raise ExceptionGroup("both failed", [ValueError("a"), TypeError("b")])
except* ValueError:
    print("handled the ValueError part")</pre>

<p>Groups matter mostly in concurrent code, where several tasks can fail at
the same time. <code>except*</code> runs once for <em>each</em> matching
kind inside the group, so this prints its message even though a TypeError
is also in flight. You won't create groups for a while — just recognize
<code>except*</code> when you see it.</p>
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
