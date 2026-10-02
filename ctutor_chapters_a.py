"""C Tutor chapters 1-5, distilled from Beej's Guide to C Programming."""

CHAPTERS_CT_A = [
    # ------------------------------------------------------------------ c01
    {
        "id": "c01",
        "title": "Syntax & Basics",
        "emoji": "🚀",
        "lessons": [
            {
                "title": "Variables",
                "html": """
<p>A <b>variable</b> is a named box in memory that holds a value. In C you
must declare a variable before using it, and every variable has a fixed
<b>type</b> chosen up front:</p>

<p>Why the ceremony? The compiler must reserve a real box of exactly the
right size and remember its type, so it can check every later use. Assign
a <code>double</code> to an <code>int</code> and the compiler either
applies a conversion rule or warns you — that checking is the type system
earning its keep.</p>

<pre class="code">int height;          // declare
height = 176;        // assign
int width = 42;      // declare and assign at once</pre>

<p>Walk the three lines: line 1 creates an <code>int</code>-sized box named
<code>height</code> but puts nothing in it yet — declaring and assigning
are separate steps. Line 2 fills the box with 176. Line 3 does both at
once; that is <b>initialisation</b>, and it is the style to prefer.
Careful: a local variable declared but never assigned holds garbage.
Reading it before the first assignment is undefined behaviour — the value
is not zero, it is nothing sensible at all.</p>

<p><b>Variable names</b> can use letters, digits and the underscore, but
may not start with a digit. C is case-sensitive: <code>score</code> and
<code>Score</code> are different variables.</p>

<p>Common built-in types:</p>

<ul>
<li><code>char</code> — a single byte, often used for characters</li>
<li><code>int</code> — the everyday integer</li>
<li><code>float</code> — single-precision decimal</li>
<li><code>double</code> — double-precision decimal (the default choice)</li>
</ul>

<p>C also has a real boolean type, <code>bool</code>, from
<code>&lt;stdbool.h&gt;</code>, which can be <code>true</code> or
<code>false</code>:</p>

<pre class="code">#include &lt;stdbool.h&gt;

bool done = false;
int attempts = 0;

while (!done) {
    attempts++;
    if (attempts == 3) done = true;
}</pre>

<p>Two gotchas: the compiler will not stop you from using
<code>height</code> before you assign it — initialise at the point of
declaration. And names are case-sensitive, so <code>height</code> and
<code>Height</code> are two different boxes.</p>

<p>Unlike Python, a variable in C cannot change its type later. The
compiler reserves exactly one box of one size, and that is what you get.
This strictness is what makes C fast — and what makes its type system
worth mastering.</p>
""",
                "tryit": """#include <stdio.h>
#include <stdbool.h>

int main(void) {
    int age = 22;
    double gpa = 3.75;
    char grade = 'A';
    bool passed = true;

    printf("age=%d gpa=%.2f grade=%c passed=%d\\n",
           age, gpa, grade, passed);
    return 0;
}
""",
            },
            {
                "title": "Types",
                "html": """
<p>Every C type has a <b>size</b>, measured with the <code>sizeof</code>
operator in bytes. The exact sizes can vary between systems, but a typical
64-bit platform looks like this:</p>

<p>Size decides range and memory: a 4-byte <code>int</code> tops out near
±2 billion, and a billion of them cost 4 GB. Knowing sizes is not trivia —
it is how you predict overflow and budget memory.</p>

<ul>
<li><code>char</code> — 1 byte</li>
<li><code>short</code> — 2 bytes</li>
<li><code>int</code> — 4 bytes</li>
<li><code>long</code> and <code>long long</code> — 8 bytes</li>
<li><code>float</code> — 4 bytes, <code>double</code> — 8 bytes</li>
<li>any pointer — 8 bytes</li>
</ul>

<p>Integers come in <b>signed</b> and <b>unsigned</b> flavours. A signed
32-bit <code>int</code> holds about ±2 billion; an
<code>unsigned int</code> holds 0 to about 4.2 billion. Unsigned
arithmetic wraps around:</p>

<pre class="code">unsigned int u = 0;
u = u - 1;           // wraps to 4294967295!

printf("%u\\n", u);</pre>

<p>Trace it: <code>u</code> starts at 0, and <code>0 - 1</code> cannot go
negative in unsigned land — unsigned arithmetic is modular, so it wraps to
the largest value, 4294967295. That wrap is <i>defined</i> behaviour.
Signed overflow, by contrast, is undefined, which is far scarier: the
compiler may assume it never happens and optimise accordingly.</p>

<p>Characters are just small integers — <code>'A'</code> is really the
number 65. That is why C can do arithmetic on characters:</p>

<pre class="code">char c = 'a';
c = c + 1;           // now 'b'</pre>

<p>So <code>'a' + 1</code> is really 97 + 1 = 98, which prints as
<code>'b'</code>. This is exactly how library functions like
<code>toupper</code> do their work underneath.</p>

<p>When a type matters for portability (file formats, protocols), use the
fixed-width types from <code>&lt;stdint.h&gt;</code>:
<code>int32_t</code>, <code>uint8_t</code>, <code>int64_t</code> and
friends — the number in the name is guaranteed to be the size in bits.</p>

<p>Gotcha: never hard-code "an int is 4 bytes" into your thinking. The
standard only guarantees minimums — <code>int</code> is <i>at least</i> 16
bits. On this course's sandbox an <code>int</code> is 4 bytes and a
pointer is 8, but portable code asks the compiler with
<code>sizeof</code> or uses the fixed-width types above.</p>

<p>Use <code>sizeof</code> to let the compiler tell you the truth on any
machine:</p>

<pre class="code">printf("int is %zu bytes\\n", sizeof(int));</pre>
""",
                "tryit": """#include <stdio.h>
#include <stdint.h>

int main(void) {
    printf("char   : %zu byte(s)\\n", sizeof(char));
    printf("short  : %zu\\n", sizeof(short));
    printf("int    : %zu\\n", sizeof(int));
    printf("double : %zu\\n", sizeof(double));
    printf("int32_t: %zu\\n", sizeof(int32_t));

    unsigned int u = 0;
    u = u - 1;
    printf("0 - 1 unsigned = %u\\n", u);
    return 0;
}
""",
            },
            {
                "title": "Operators",
                "html": """
<p>C's operator set will feel familiar, with a few additions:</p>

<ul>
<li><b>Arithmetic:</b> <code>+ - * / %</code> — note that
<code>7 / 2</code> is <code>3</code> when both sides are integers!
Integer division truncates. Use <code>7 / 2.0</code> to get
<code>3.5</code>.</li>
<li><b>Increment/decrement:</b> <code>i++</code> adds one,
<code>i--</code> subtracts one. The prefix form
(<code>++i</code>) changes the value <i>before</i> it is used, the
postfix form <i>after</i>.</li>
<li><b>Comparison:</b> <code>== != &lt; &gt; &lt;= &gt;=</code> — a single
<code>=</code> assigns, <code>==</code> compares. Mixing these up is the
classic C bug.</li>
<li><b>Logical:</b> <code>&amp;&amp;</code> (and), <code>||</code> (or),
<code>!</code> (not) — these <b>short-circuit</b>: the right side is not
evaluated if the left side already decides the answer.</li>
<li><b>Ternary:</b> <code>condition ? a : b</code> — a tiny one-line
if/else that is an expression.</li>
<li><b>Compound assignment:</b> <code>x += 2</code> means
<code>x = x + 2</code>; the same works for <code>-= *= /= %=</code> and
the bitwise operators.</li>
<li><b>sizeof:</b> gives the size of a type or expression in bytes.</li>
</ul>

<pre class="code">int i = 5;
int j = i++;        // j is 5, i becomes 6
int k = ++i;        // i becomes 7, k is 7

int m = (i &gt; 3) ? i : 0;   // ternary: m is 7

int x = 7, y = 2;
printf("%d %d\\n", x / y, x % y);   // 3 1
printf("%.1f\\n", x / 2.0);        // 3.5</pre>

<p>Walk the lines: <code>i++</code> hands the old value 5 to
<code>j</code> and <i>then</i> bumps <code>i</code> to 6.
<code>++i</code> bumps first, so <code>i</code> is 7 and <code>k</code>
receives 7. The ternary reads "if i is greater than 3, use i, else 0".
The last two printfs show integer division 7/2 = 3 with remainder
7%2 = 1, and true division 3.5 once one operand is a double.</p>

<p>Two classic traps: <code>if (x = 5)</code> assigns instead of
comparing — it is always true — while <code>==</code> is the comparison
you meant. And never modify the same variable twice in one expression
(<code>i++ + ++i</code>) — that is undefined behaviour, not "left to
right".</p>

<p>Precedence matters: <code>*</code> and <code>/</code> bind tighter than
<code>+/-</code>, comparisons bind tighter than <code>&amp;&amp;</code> and
<code>||</code>. When in doubt, add parentheses — they cost nothing.</p>
""",
                "tryit": """#include <stdio.h>

int main(void) {
    int i = 5;
    int j = i++;
    int k = ++i;
    printf("j=%d k=%d i=%d\\n", j, k, i);

    int x = 7, y = 2;
    printf("7 / 2   = %d\\n", x / y);
    printf("7 %% 2   = %d\\n", x % y);
    printf("7 / 2.0 = %.1f\\n", x / 2.0);

    int m = (i > 3) ? i : 0;
    printf("ternary m=%d\\n", m);

    int online = 1, ok = 0;
    if (online && !ok) printf("online but not ok\\n");
    return 0;
}
""",
            },
            {
                "title": "Control Flow",
                "html": """
<p>C has the classic family of control-flow statements. The condition of
an <code>if</code>, <code>while</code> or <code>for</code> is any number —
zero means false, anything else means true.</p>

<p>Why care? Control flow is how a flat list of instructions becomes a
program that makes decisions and repeats work. Every one of these forms
evaluates a condition, and in C any number can be that condition, because
C has no real boolean underneath: 0 is false, everything else is true.</p>

<pre class="code">if (temperature &gt; 30) {
    printf("hot\\n");
} else if (temperature &gt; 20) {
    printf("nice\\n");
} else {
    printf("cold\\n");
}</pre>

<p>The <b>while</b> loop repeats while its condition holds;
<b>do-while</b> runs the body first and checks afterwards, so it always
runs at least once:</p>

<pre class="code">int i = 10;
do {
    printf("%d ", i);
    i++;
} while (i &lt; 13);        // prints 10 11 12</pre>

<p>Read the output 10 11 12: the body runs, <code>i</code> climbs, and
only when the check fails at 13 does the loop end. Swap in a plain
<code>while</code> with a starting value of 13 and the body would be
skipped entirely — that is the whole difference between the two.</p>

<p>The <b>for</b> loop bundles initialisation, condition and step
together, and its loop variable can be declared right in the header
(C99):</p>

<pre class="code">for (int i = 0; i &lt; 5; i++) {
    printf("%d ", i);
}</pre>

<p><b>switch</b> jumps to the matching <code>case</code> and — importantly
— <b>falls through</b> to the next case unless you <code>break</code>:</p>

<pre class="code">switch (choice) {
    case 1:
        printf("one\\n");
        break;
    case 2:
    case 3:
        printf("two or three\\n");
        break;
    default:
        printf("something else\\n");
}</pre>

<p>Read a switch as "jump to the label that matches, then keep going
downward". Case 2 and case 3 share a body because case 2 falls straight
through; forgetting a <code>break</code> is the most common switch bug in
C, so some programmers write the <code>break</code> first.</p>

<p>Gotcha: <code>=</code> inside a condition strikes here too —
<code>if (x = 0)</code> assigns zero and tests false. And use braces: an
unbraced <code>if</code> owns only the very next statement, which is how
the infamous "dangling else" confuses people.</p>

<p><code>break</code> leaves the nearest loop or switch;
<code>continue</code> jumps to the next iteration.</p>
""",
                "tryit": """#include <stdio.h>

int main(void) {
    for (int i = 1; i <= 5; i++) {
        if (i % 2 == 0) continue;
        printf("odd: %d\\n", i);
    }

    int n = 3;
    switch (n) {
        case 1: printf("one\\n"); break;
        case 3: printf("three\\n"); break;
        default: printf("other\\n");
    }

    int i = 10;
    do { printf("%d ", i); i++; } while (i < 13);
    printf("\\n");
    return 0;
}
""",
            },
        ],
        "quiz": [
            {
                "type": "mc",
                "question": "Which line declares a variable correctly in C?",
                "options": [
                    "x = 10;",
                    "int x = 10;",
                    "let x = 10;",
                    "var x int = 10;",
                ],
                "answer": 1,
                "explain": "C requires an explicit type before the name: int x = 10; — variables cannot be used undeclared.",
            },
            {
                "type": "blank",
                "question": "The operator that gives the size of a type in bytes is <code>____</code>.",
                "answers": ["sizeof", "sizeof()", "sizeof ()"],
                "explain": "sizeof(int) yields the size of int in bytes.",
            },
            {
                "type": "mc",
                "question": "What does <code>7 / 2</code> evaluate to when both operands are <code>int</code>?",
                "options": ["3.5", "4", "3", "0"],
                "answer": 2,
                "explain": "Integer division truncates toward zero, so 7 / 2 is 3. Use 7 / 2.0 for 3.5.",
            },
            {
                "type": "mc",
                "question": "What does <code>unsigned int u = 0; u = u - 1;</code> produce?",
                "options": [
                    "-1",
                    "0",
                    "4294967295 (wraps around)",
                    "Undefined behaviour",
                ],
                "answer": 2,
                "explain": "Unsigned arithmetic is modular: 0 - 1 wraps to the largest unsigned int, 4294967295.",
            },
            {
                "type": "codefill",
                "question": "Complete this classic for-loop so it prints 0 to 4:",
                "code": [
                    "for (", { "blank": "int i = 0", "answers": ["int i = 0"] },
                    "; i < 5; ", { "blank": "i++", "answers": ["i++", "++i", "i += 1", "i = i + 1"] },
                    ") {",
                    "    printf(\"%d \", i);",
                    "}",
                ],
                "explain": "for (int i = 0; i < 5; i++) — C99 allows declaring the loop variable in the header.",
            },
        ],
    },

    # ------------------------------------------------------------------ c02
    {
        "id": "c02",
        "title": "Functions",
        "emoji": "🧩",
        "lessons": [
            {
                "title": "Defining and Calling",
                "html": """
<p>A function packages a piece of behaviour behind a name. C functions
declare the type of every parameter and the type of the value they
return:</p>

<p>Functions are how you keep a program readable: name a chunk of
behaviour once, test it once, reuse it everywhere. The parameter list is
the function's input contract, and the return type is its output
contract.</p>

<pre class="code">int add(int a, int b) {
    return a + b;
}

double area(double r) {
    return 3.14159265358979 * r * r;
}</pre>

<p>A call like <code>add(2, 3)</code> copies the arguments 2 and 3 into
the parameters <code>a</code> and <code>b</code>, runs the body, and the
<code>return</code> value replaces the whole call expression — so
<code>printf("%d", add(2, 3))</code> prints 5.</p>

<p><code>void</code> as the return type means "returns nothing"; C has no
default return value like Python's <code>None</code>.</p>

<pre class="code">void greet(const char *name) {
    printf("Hello, %s!\\n", name);
}</pre>

<p>Functions may call themselves — <b>recursion</b> works just like in
Python, and is the classic way to express problems like factorial or
fibonacci:</p>

<pre class="code">int fib(int n) {
    if (n &lt; 2) return n;
    return fib(n - 1) + fib(n - 2);
}</pre>

<p>Find the base case first when you read recursion: <code>fib</code>
answers 0 and 1 directly, and every other call shrinks <code>n</code>
until it lands there. No base case means infinite recursion — which on
real hardware ends as a <b>stack overflow</b> crash, not a friendly
error message.</p>

<p>Gotcha: if a non-<code>void</code> function can finish without hitting
a <code>return</code>, and the caller then uses that missing value, that
is undefined behaviour. Compilers warn about this — treat every warning
as a bug.</p>

<p>One rule surprises newcomers: functions must be <b>declared</b> before
the line that calls them. If <code>main</code> sits at the top of the
file, either move the helpers above it, or write a prototype (next
lesson). This is how the compiler checks every call against its
signature.</p>
""",
                "tryit": """#include <stdio.h>

int add(int a, int b) {
    return a + b;
}

int fib(int n) {
    if (n < 2) return n;
    return fib(n - 1) + fib(n - 2);
}

int main(void) {
    printf("2 + 3 = %d\\n", add(2, 3));
    printf("fib(15) = %d\\n", fib(15));
    return 0;
}
""",
            },
            {
                "title": "Passing by Value",
                "html": """
<p>Here is the single most important fact about C function calls:
<b>arguments are copied</b>. The function receives its own private copy of
each argument, so changing a parameter never changes the caller's
variable:</p>

<pre class="code">void broken(int n) {
    n = 99;             // modifies only the copy
}

int main(void) {
    int x = 1;
    broken(x);
    printf("%d\\n", x);  // still 1!
}</pre>

<p>Trace it: <code>broken</code> receives a fresh box named
<code>n</code> containing a copy of 1, sets that copy to 99, and throws
it away on return. The caller's <code>x</code> never hears about it. This
differs from Python more than you would expect — Python copies
references, C copies the value itself.</p>

<p>To let a function change a caller's variable, pass the <b>address</b>
of the variable instead. The function receives a pointer to the original
box and can write through it:</p>

<pre class="code">void swap(int *a, int *b) {
    int tmp = *a;
    *a = *b;
    *b = tmp;
}

int main(void) {
    int x = 1, y = 2;
    swap(&amp;x, &amp;y);       // pass addresses
    printf("%d %d\\n", x, y);   // 2 1
}</pre>

<p>Follow <code>swap(&amp;x, &amp;y)</code> step by step: <code>&amp;x</code>
computes the address of x's box, so <code>a</code> points at x and
<code>b</code> points at y. <code>*a</code> means "the box a points at",
so the three lines shuttle the two values through <code>tmp</code> —
inside the originals themselves. After the call, x is 2 and y is 1.</p>

<p>This "pass by pointer" is C's version of out-parameters, and it is
everywhere in real code. Structs, by the way, are also passed by value —
the whole struct is copied, which is usually what you want for small
records.</p>

<p>Rule of thumb: <code>scanf("%d", &amp;x)</code> needs that
<code>&amp;</code> for exactly this reason — scanf must reach back into
your variable. Forgetting it compiles cleanly and then corrupts memory,
one of the most famous C crashes there is.</p>
""",
                "tryit": """#include <stdio.h>

void broken(int n) { n = 99; }

void swap(int *a, int *b) {
    int tmp = *a;
    *a = *b;
    *b = tmp;
}

int main(void) {
    int x = 1;
    broken(x);
    printf("after broken: %d\\n", x);

    int y = 2;
    swap(&x, &y);
    printf("after swap: %d %d\\n", x, y);
    return 0;
}
""",
            },
            {
                "title": "Prototypes and Declarations",
                "html": """
<p>Because C is compiled top-to-bottom, a function must be known before
it is called. When two functions call <i>each other</i>, neither can be
written first — so C lets you declare a function without defining it.
This is a <b>prototype</b>:</p>

<p>A prototype is the function's signature with a semicolon instead of a
body. It is a promise: "this function exists — here is its name, return
type and parameter types; the body comes later, or in another file."</p>

<pre class="code">int is_even(int n);     // prototype: ends with ;

int is_odd(int n) {
    if (n == 0) return 0;
    return is_even(n - 1);      // fine: is_even is declared
}

int is_even(int n) {
    if (n == 0) return 1;
    return is_odd(n - 1);
}</pre>

<p>Notice <code>is_odd</code> calls <code>is_even</code> with confidence
because the prototype above it made the name known. Without that first
line, the compiler reaches <code>is_even(n - 1)</code> having never heard
of the function, and modern C rejects the program outright.</p>

<p>The prototype tells the compiler the function's name, return type and
parameter types; the definition can live further down the file (or in a
completely different file — that is how headers work, covered in
Program Organization).</p>

<p>A parameter list of <code>(void)</code> explicitly means "takes no
arguments". An empty list <code>()</code> in an old-style declaration
means "unspecified", so modern style always writes
<code>int main(void)</code> rather than <code>int main()</code>.</p>

<pre class="code">int main(void) {
    for (int i = 0; i &lt; 4; i++) {
        printf("%d is %s\\n", i, is_even(i) ? "even" : "odd");
    }
    return 0;
}</pre>

<p>Gotchas: the prototype must match the definition exactly — a
mismatched return type or parameter list is a compile error. And write
<code>(void)</code> for "no parameters": in an old-style declaration,
empty parentheses mean "unchecked", which disables the very checking
prototypes exist for.</p>
""",
                "tryit": """#include <stdio.h>

int is_even(int n);   /* prototype — defined below */

int is_odd(int n) {
    if (n == 0) return 0;
    return is_even(n - 1);
}

int is_even(int n) {
    if (n == 0) return 1;
    return is_odd(n - 1);
}

int main(void) {
    for (int i = 0; i < 4; i++) {
        printf("%d is %s\\n", i, is_even(i) ? "even" : "odd");
    }
    return 0;
}
""",
            },
        ],
        "quiz": [
            {
                "type": "mc",
                "question": "After calling <code>broken(x)</code> from the lesson, what is <code>x</code>?",
                "options": ["99 — the function changed it", "1 — arguments are copied", "0", "It depends on the compiler"],
                "answer": 1,
                "explain": "C passes arguments by value: the function gets a copy, and the caller's variable is untouched.",
            },
            {
                "type": "mc",
                "question": "How do you let a function modify the caller's variable?",
                "options": [
                    "Declare the parameter static",
                    "Pass the variable's address and use a pointer parameter",
                    "Use the return value only",
                    "You cannot in C",
                ],
                "answer": 1,
                "explain": "Pass &x and declare the parameter as int *p — the function can write through the pointer to the caller's box.",
            },
            {
                "type": "codefill",
                "question": "Complete swap so it exchanges two ints through pointers:",
                "code": [
                    "void swap(int *a, int *b) {",
                    "    int tmp = ", { "blank": "*a", "answers": ["*a"] }, ";",
                    "    *a = *b;",
                    "    *b = tmp;",
                    "}",
                ],
                "explain": "*a reads the value that a points at; save it before overwriting.",
            },
            {
                "type": "blank",
                "question": "A function declaration without a body, ending in a semicolon, is called a <code>____</code>.",
                "answers": ["prototype", "forward declaration", "declaration"],
                "explain": "A prototype tells the compiler a function's signature before its definition appears.",
            },
        ],
    },

    # ------------------------------------------------------------------ c03
    {
        "id": "c03",
        "title": "Memory",
        "emoji": "🧠",
        "lessons": [
            {
                "title": "Pointers",
                "html": """
<p>Pointers are the heart of C. A <b>pointer</b> is a variable whose value
is the <i>address</i> of another variable in memory. Two operators do all
the work:</p>

<p>Why learn them? Pointers are how a function modifies your data, how
<code>malloc</code> hands you memory, and how linked lists and trees get
built. Master this lesson and half of C opens up.</p>

<ul>
<li><code>&amp;x</code> — the <b>address-of</b> operator: "where does
<code>x</code> live?"</li>
<li><code>*p</code> — the <b>dereference</b> operator: "the value stored
at the address <code>p</code> holds".</li>
</ul>

<pre class="code">int x = 42;
int *p = &amp;x;        // p holds the address of x

printf("%d\\n", *p); // 42 — follow the arrow
*p = 99;            // writes through the pointer
printf("%d\\n", x);  // 99 — x itself changed!</pre>

<p>Draw two boxes: one named <code>x</code> containing 42, one named
<code>p</code> containing x's address. <code>*p</code> follows the arrow
to x, so printing it shows 42 — and <code>*p = 99</code> writes 99 into
x's box. No copy is involved; the pointer reaches the original.</p>

<p>The declaration <code>int *p</code> reads "p is a pointer to int". The
type matters: a <code>double *</code> knows its target is 8 bytes wide,
which is how pointer arithmetic (later in this chapter) works
correctly.</p>

<p>The special value <code>NULL</code> means "points at nothing". Good C
code checks for it before dereferencing:</p>

<pre class="code">int *p = NULL;
if (p != NULL) {
    printf("%d\\n", *p);   // only if it is safe
}</pre>

<p>Here <code>p</code> is NULL, so the guard skips the print. Delete the
<code>if</code> and the program dereferences NULL — an instant
segmentation fault.</p>

<p>Gotcha: an uninitialised pointer holds a random address, and
dereferencing it corrupts memory in ways that may not crash until much
later. Set pointers to <code>NULL</code> when they have nothing to point
at, and check before dereferencing.</p>

<p>Dereferencing NULL (or a wild address) is the famous
<b>segmentation fault</b> — the operating system stops your program
because it touched memory it must not.</p>
""",
                "tryit": """#include <stdio.h>

int main(void) {
    int x = 42;
    int *p = &x;

    printf("x lives at %p\\n", (void *)p);
    printf("*p = %d\\n", *p);

    *p = 99;
    printf("after *p = 99, x = %d\\n", x);
    return 0;
}
""",
            },
            {
                "title": "Arrays",
                "html": """
<p>An array is a fixed-length row of boxes of the same type, stored side
by side in memory:</p>

<pre class="code">int scores[4];              // four ints, uninitialized
int fib[5] = {1, 1, 2, 3, 5};   // with an initializer

printf("%d\\n", fib[2]);     // 2 — indexing starts at 0</pre>

<p><code>fib[2]</code> is the third box, because indexing starts at 0 —
the single most common off-by-one mistake in the language. A loop that
walks the 5 elements of <code>fib</code> runs <code>i</code> from 0 to
4, and the usual idiom for the count is <code>sizeof(fib) /
sizeof(fib[0])</code>.</p>

<p>Two facts define arrays in C:</p>

<ul>
<li><b>No bounds checking.</b> <code>fib[7]</code> compiles happily and
reads/writes memory past the end — a classic source of bugs and security
holes. The language trusts you completely.</li>
<li><b>The size is part of the type</b> and must be known (or computed at
runtime for VLAs — see Advanced C).</li>
</ul>

<p>Gotcha: C will not stop you at the edge. <code>fib[9] = 1;</code> on a
5-element array compiles and quietly tramples whatever lives next door —
other variables, or the bookkeeping that keeps your program alive.</p>

<p>Multidimensional arrays are arrays of arrays:</p>

<pre class="code">int grid[2][3] = {
    {1, 2, 3},
    {4, 5, 6},
};
printf("%d\\n", grid[1][2]);   // 6</pre>

<p>Memory is one continuous strip: <code>grid</code> stores row 0's three
values, then row 1's. That layout is why <code>grid[1][2]</code> means
"row 1, column 2", and why passing <code>grid</code> to a function
requires telling it the column count.</p>

<p>Arrays have a deep relationship with pointers: in most expressions the
name of an array <b>decays</b> to a pointer to its first element. So
<code>fib</code> and <code>&amp;fib[0]</code> mean the same thing, and
functions that receive arrays actually receive a pointer (next two
lessons cover what that implies).</p>

<p>Decay has a price: once an array becomes a pointer, the size
information is gone, which is why <code>sizeof</code> stops reporting the
array's total size inside functions. Pass the length as a separate
argument — that is the C convention.</p>
""",
                "tryit": """#include <stdio.h>

int main(void) {
    int fib[5] = {1, 1, 2, 3, 5};
    for (int i = 0; i < 5; i++) {
        printf("%d ", fib[i]);
    }
    printf("\\n");

    int grid[2][3] = {{1, 2, 3}, {4, 5, 6}};
    printf("grid[1][2] = %d\\n", grid[1][2]);
    return 0;
}
""",
            },
            {
                "title": "Pointer Arithmetic",
                "html": """
<p>You can do math on pointers — but it is <b>element-wise</b>, not
byte-wise. Adding 1 to a pointer moves it forward by one element of its
type:</p>

<pre class="code">int a[] = {10, 20, 30, 40};
int *p = a;         // points at a[0]

p++;                // now points at a[1] — moved 4 bytes
printf("%d\\n", *p); // 20

p += 2;             // now points at a[3]
printf("%d\\n", *p); // 40</pre>

<p>The step is scaled: on this 4-byte <code>int</code> array,
<code>p++</code> moves the address forward 4 bytes, landing exactly on
the next element. Add 2 more and <code>p</code> sits on
<code>a[3]</code>. The address changes by bytes, but the meaning is
always in elements.</p>

<p>The compiler multiplies the step by <code>sizeof(element)</code>: on an
<code>int *</code>, <code>p + 1</code> advances 4 bytes; on a
<code>double *</code>, 8. This is why the pointer's type matters.</p>

<p>Two pointers into the same array can be subtracted, giving the number
of elements between them:</p>

<pre class="code">int *q = &amp;a[3];
printf("%d\\n", (int)(q - a));   // 3</pre>

<p>Subtraction gives the distance in <i>elements</i>, not bytes — here 3.
This only makes sense for two pointers into the <b>same</b> array;
comparing or subtracting pointers into different arrays is undefined.</p>

<p>Because arrays decay to pointers to their first element, indexing is
defined in terms of pointer arithmetic:
<code>a[i]</code> is exactly <code>*(a + i)</code>. This also means
pointer arithmetic is how you walk arrays in C:</p>

<pre class="code">int *end = a + 4;
for (int *p = a; p &lt; end; p++) {
    printf("%d ", *p);
}</pre>

<p>The loop starts on the first element and stops the moment
<code>p</code> reaches <code>end</code> — the classic one-past-the-end
pattern. Pointing one past the last element is legal; dereferencing it
is not.</p>

<p>Pointer arithmetic outside an array (or past its end) is undefined
behaviour — the sandbox in this course will catch it and tell you.</p>

<p>Rule of thumb: use indexes for clarity, pointer walks for hot inner
loops, and keep every pointer's arithmetic inside the one array it came
from.</p>
""",
                "tryit": """#include <stdio.h>

int main(void) {
    int a[] = {10, 20, 30, 40};
    int *p = a;

    p++;
    printf("*p after p++  = %d\\n", *p);
    p += 2;
    printf("*p after p+=2 = %d\\n", *p);

    int *q = &a[3];
    printf("q - a = %d elements\\n", (int)(q - a));

    for (int *w = a; w < a + 4; w++) printf("%d ", *w);
    printf("\\n");
    return 0;
}
""",
            },
            {
                "title": "Dynamic Allocation",
                "html": """
<p>Arrays you declare have a fixed size. When you need memory whose size
is only known at runtime — or that must outlive the current function —
you allocate it from the <b>heap</b> with <code>malloc</code>:</p>

<p>The stack, where locals live, is fast but small and dies when the
function returns. The heap is big, shared, and lasts until you free it —
that combination is why <code>malloc</code> exists.</p>

<pre class="code">#include &lt;stdlib.h&gt;

int *scores = malloc(n * sizeof(int));   // space for n ints
if (scores == NULL) {
    // allocation failed — handle it
}</pre>

<p>If <code>malloc</code> cannot find <code>n * sizeof(int)</code>
contiguous bytes it returns <code>NULL</code>, and dereferencing that
crashes. The check is two lines; the crash it prevents can take hours to
find.</p>

<p>Read the idiom carefully: <code>n * sizeof(int)</code> bytes, cast
implicitly to <code>int *</code>. Always check for <code>NULL</code> —
malloc returns it when out of memory.</p>

<p>The heap family:</p>

<ul>
<li><code>malloc(bytes)</code> — allocate, contents <b>uninitialised</b></li>
<li><code>calloc(count, size)</code> — allocate and <b>zero</b></li>
<li><code>realloc(ptr, bytes)</code> — grow/shrink a block, keeping the data</li>
<li><code>free(ptr)</code> — return the block; after this, do not touch it</li>
</ul>

<p>The rules that keep C programs alive:</p>

<ul>
<li>Every <code>malloc</code> gets exactly one <code>free</code> — no more, no less.</li>
<li>Using memory after <code>free</code> ("use after free") is undefined.</li>
<li>Losing the last pointer to a block without freeing it is a <b>memory leak</b>.</li>
</ul>

<p>Gotcha: the popular shortcut <code>p = realloc(p, bigger)</code> has a
hole — if realloc fails it returns <code>NULL</code>, and you have just
overwritten your only pointer to the old block. Realloc into a temporary
first: <code>int *tmp = realloc(p, n); if (tmp) p = tmp;</code></p>

<pre class="code">int *p = calloc(4, sizeof(int));    // {0, 0, 0, 0}
p = realloc(p, 8 * sizeof(int));    // grow to 8 ints
p[7] = 77;
free(p);</pre>

<p>Read the last block top to bottom: <code>calloc</code> hands back four
zeroed ints, <code>realloc</code> grows the block to eight (moving and
copying the data if it must), we use slot 7, and <code>free</code>
returns everything. Exactly one <code>free</code> per allocation —
calling it twice corrupts the allocator.</p>
""",
                "tryit": """#include <stdio.h>
#include <stdlib.h>

int main(void) {
    int n = 5;
    int *squares = malloc(n * sizeof(int));
    if (squares == NULL) {
        printf("out of memory\\n");
        return 1;
    }

    for (int i = 0; i < n; i++) squares[i] = i * i;
    for (int i = 0; i < n; i++) printf("%d ", squares[i]);
    printf("\\n");

    squares = realloc(squares, 8 * sizeof(int));
    squares[7] = 49;
    printf("grown: %d\\n", squares[7]);

    free(squares);
    printf("freed\\n");
    return 0;
}
""",
            },
        ],
        "quiz": [
            {
                "type": "mc",
                "question": "After <code>int x = 42; int *p = &amp;x; *p = 99;</code> what is <code>x</code>?",
                "options": ["42", "99", "undefined", "the address of p"],
                "answer": 1,
                "explain": "*p = 99 writes through the pointer into x's box, so x becomes 99.",
            },
            {
                "type": "blank",
                "question": "The operator <code>&amp;</code> is called the address-____ operator.",
                "answers": ["of"],
                "explain": "&x is the address-of operator; *p is the dereference (indirection) operator.",
            },
            {
                "type": "mc",
                "question": "If <code>int *p</code> points into an int array, what does <code>p + 1</code> mean?",
                "options": [
                    "One byte further in memory",
                    "One int element further (4 bytes on typical systems)",
                    "It is a syntax error",
                    "The next array in memory",
                ],
                "answer": 1,
                "explain": "Pointer arithmetic scales by sizeof(element): p + 1 advances one int, i.e. 4 bytes on typical systems.",
            },
            {
                "type": "codefill",
                "question": "Allocate space for 10 doubles and handle failure:",
                "code": [
                    "double *d = ", { "blank": "malloc", "answers": ["malloc", "calloc"] },
                    "(10 * sizeof(double));",
                    "if (d == ", { "blank": "NULL", "answers": ["NULL", "0"] }, ") return 1;",
                ],
                "explain": "malloc(10 * sizeof(double)); a NULL return means the allocation failed.",
            },
            {
                "type": "order",
                "question": "Order the dynamic-memory lifecycle correctly:",
                "lines": [
                    "int *p = malloc(4 * sizeof(int));",
                    "p[0] = 42;",
                    "p = realloc(p, 8 * sizeof(int));",
                    "free(p);",
                ],
                "explain": "Allocate, use, (optionally grow with realloc), then free — exactly once.",
            },
        ],
    },

    # ------------------------------------------------------------------ c04
    {
        "id": "c04",
        "title": "Data Structures",
        "emoji": "📦",
        "lessons": [
            {
                "title": "Strings",
                "html": """
<p>C has no string type. A <b>string</b> is a convention: an array of
<code>char</code> ending with the <b>NUL terminator</b>
<code>'\\0'</code> — a byte of all zeros that marks the end:</p>

<pre class="code">char name[6] = {'B', 'e', 'e', 'j', '\\0'};   // explicit
char name[6] = "Beej";                        // shorthand — same thing</pre>

<p>Count the boxes in <code>"Beej"</code>: five, not four — B, e, e, j,
and the invisible terminator. <code>strlen</code> answers 4 because it
stops before that byte. Every library function taking a
<code>char *</code> relies on the zero byte to know where the string
stops — feed it an array without one and it runs off the end.</p>

<p>The shorthand form quietly adds the <code>'\\0'</code> for you. A
string literal like <code>"hi"</code> is actually an array of 3 chars:
<code>'h'</code>, <code>'i'</code>, <code>'\\0'</code>.</p>

<p>All string handling goes through <code>&lt;string.h&gt;</code>:</p>

<ul>
<li><code>strlen(s)</code> — length, <b>not</b> counting the terminator</li>
<li><code>strcpy(dst, src)</code> — copy (dst must be big enough!)</li>
<li><code>strcat(dst, src)</code> — append src to dst</li>
<li><code>strcmp(a, b)</code> — 0 if equal, negative/positive otherwise</li>
<li><code>strchr(s, c)</code> — find first occurrence of a character</li>
<li><code>strstr(s, sub)</code> — find a substring</li>
</ul>

<pre class="code">char title[32] = "C ";
strcat(title, "Programming");
printf("%s has %zu letters\\n", title, strlen(title) - 1);

if (strcmp(title, "C Programming") == 0) {
    printf("match!\\n");
}</pre>

<p>Walk it: <code>strcat</code> walks <code>title</code> to its
terminator and copies <code>"Programming"</code> over it, so
<code>title</code> becomes <code>"C Programming"</code> — 13 characters
plus the terminator, well inside the 32-box buffer. <code>strcmp</code>
returns 0 for equal, so equality tests read <code>== 0</code>, which
looks backwards until you have written it a dozen times.</p>

<p>The golden rule: the destination buffer must be large enough.
<code>strcpy</code> and <code>strcat</code> cannot know its size — that
trust is the source of the infamous <b>buffer overflow</b>. Safer
variants (<code>strncpy</code>, <code>strncat</code>) take an explicit
limit.</p>

<p>Rule of thumb: prefer <code>snprintf</code> when building strings — it
always writes the terminator and never writes past the limit you give
it.</p>
""",
                "tryit": """#include <stdio.h>
#include <string.h>

int main(void) {
    char title[32] = "C ";
    strcat(title, "Programming");

    printf("%s\\n", title);
    printf("length = %zu\\n", strlen(title));

    if (strcmp(title, "C Programming") == 0) printf("match!\\n");
    printf("first P at: %s\\n", strchr(title, 'P'));
    return 0;
}
""",
            },
            {
                "title": "struct",
                "html": """
<p>A <code>struct</code> bundles related values into one named box —
C's record type:</p>

<p>Why bundle? A point is one idea carrying two numbers; passing
<code>p.x</code> and <code>p.y</code> separately scatters the idea across
your program. A struct gives the idea a name and one type, so functions
take a single argument, arrays hold whole records, and the compiler
keeps the fields together in memory.</p>

<pre class="code">struct point {
    double x;
    double y;
};

struct point p = {3.0, 4.0};    // initialize in order
p.x = 10.0;                     // dot accesses a field</pre>

<p>The first block defines the <i>shape</i> and reserves no memory. The
second line creates an actual variable with that shape and fills it
field by field, in order. <code>p.x = 10.0;</code> then reaches into one
field through the dot operator.</p>

<p>Structs are true values: you can assign them (the whole thing is
copied), pass them to functions by value, and return them:</p>

<pre class="code">struct point scale(struct point v, double k) {
    v.x *= k;           // safe: v is a private copy
    v.y *= k;
    return v;           // returns the modified copy
}</pre>

<p>Inside <code>scale</code>, <code>v</code> is a fresh copy of the
caller's point — by-value rules apply to whole structs. The original is
untouched, and the modified copy travels back through
<code>return</code>.</p>

<p>When you have a <b>pointer to a struct</b> (very common — e.g. from
<code>malloc</code>), a dedicated operator <code>-&gt;</code> accesses
fields through the pointer:</p>

<pre class="code">struct point *pp = &amp;p;
pp-&gt;x = 42.0;               // same as (*pp).x

struct point *heap = malloc(sizeof(struct point));
heap-&gt;y = 7.0;
free(heap);</pre>

<p>The arrow <code>pp-&gt;x</code> is shorthand for <code>(*pp).x</code> —
dereference, then dot. The malloc line shows the everyday pattern: no
struct variable at all, just a pointer to a heap block big enough for
one.</p>

<p>Structs can nest, contain arrays, and even contain pointers to their
own type — the building block of linked lists and trees:</p>

<pre class="code">struct node {
    int value;
    struct node *next;    // pointer to the next node
};</pre>

<p><code>struct node</code> contains a pointer to its own type — legal
because a pointer is a fixed size even while the struct is still being
defined. Chain nodes through <code>next</code> and you have a linked
list; add two child pointers and you have a binary tree.</p>

<p>Gotchas: every struct definition ends with a semicolon — <code>};</code>
— and forgetting it makes the compiler complain about a line far away.
And remember assignment copies all fields, but the copy is shallow: two
structs with a pointer field end up pointing at the same target.</p>
""",
                "tryit": """#include <stdio.h>
#include <stdlib.h>

struct point { double x, y; };

struct point scale(struct point v, double k) {
    v.x *= k;
    v.y *= k;
    return v;
}

int main(void) {
    struct point p = {3.0, 4.0};
    struct point big = scale(p, 2.0);
    printf("big = (%.1f, %.1f)\\n", big.x, big.y);

    struct point *pp = &big;
    pp->x = 42.0;
    printf("pp->x = %.1f\\n", big.x);
    return 0;
}
""",
            },
            {
                "title": "union",
                "html": """
<p>A <code>union</code> looks like a struct, but all its fields share the
<b>same</b> memory. Write one field, and you have overwritten the
others:</p>

<pre class="code">union value {
    int i;
    float f;
    char bytes[4];
};

union value v;
v.i = 65;
printf("%d\\n", v.bytes[0]);   // 65 — same memory, read as a byte</pre>

<p>Both <code>v.i</code> and <code>v.bytes</code> start at the same
address. Storing 65 puts the byte 65 in the lowest slot; reading
<code>bytes[0]</code> shows 65 back. Nothing was converted — it is the
same 4 bytes viewed through two different lenses.</p>

<p>The union's size is the size of its largest field. A union stores
<b>one of</b> its alternatives at a time — which one is up to you to
track (often with a companion "tag" field).</p>

<p>Two classic uses:</p>

<ul>
<li><b>Saving memory</b> when only one variant is ever active — e.g. a
number that is either an int or a float, never both.</li>
<li><b>Type punning</b> — inspecting the raw bytes of a value, as the
example above does with <code>bytes[0]</code>. On little-endian machines
the low byte comes first.</li>
</ul>

<pre class="code">union value v;
v.f = 1.0f;
// the raw bytes of 1.0f: 00 00 80 3f on little-endian
printf("low byte: %d\\n", v.bytes[0]);</pre>

<p>The float 1.0f has the bit pattern 0x3F800000, which sits in memory as
00 00 80 3f on a little-endian machine — low byte first. The example is
really peeking at the machine's byte order, and
<code>sizeof(union value)</code> reports 4: the size of the largest
field, not the sum of them.</p>

<p>Reading a field other than the one last written is technically
implementation-defined, but it is the standard trick for looking at
representations — and a favourite interview question.</p>

<p>Gotcha: the union only remembers what <i>you</i> last wrote. Write
<code>v.f</code> and read <code>v.i</code> and you get the float's bits
reinterpreted — fine for experiments, a real bug in ordinary code. Big
unions paired with a tag field (an enum saying which member is live) are
the disciplined pattern.</p>
""",
                "tryit": """#include <stdio.h>

union value {
    int i;
    float f;
    char bytes[4];
};

int main(void) {
    union value v;
    v.i = 65;
    printf("after i=65, bytes[0] = %d\\n", v.bytes[0]);

    v.f = 1.0f;
    printf("after f=1.0: %02x %02x %02x %02x\\n",
           v.bytes[0] & 0xff, v.bytes[1] & 0xff,
           v.bytes[2] & 0xff, v.bytes[3] & 0xff);
    printf("sizeof(union value) = %zu\\n", sizeof(union value));
    return 0;
}
""",
            },
            {
                "title": "enum",
                "html": """
<p>An <code>enum</code> creates named integer constants — a safe,
readable alternative to scattering magic numbers through the code:</p>

<p>Why not just write 0, 1, 2? Because <code>RED</code> carries meaning
at every call site, the debugger shows the name instead of a number, and
adding a colour later means changing one line — not hunting literals
through the codebase.</p>

<pre class="code">enum color { RED, GREEN, BLUE };

enum color c = GREEN;
printf("%d\\n", c);     // 1</pre>

<p>The compiler silently numbers the names 0, 1, 2 — so GREEN prints as
1. An enum variable is really just an <code>int</code> wearing nicer
clothes.</p>

<p>By default the first name is 0 and each following name is one more.
You can choose values, and counting continues from there:</p>

<pre class="code">enum level { LOW = 1, MEDIUM, HIGH };   // 1, 2, 3
enum flags { A = 1, B = 4, C = 8 };</pre>

<p>Setting LOW to 1 shifts the automatic counting: MEDIUM becomes 2 and
HIGH becomes 3. The flags line shows the numbers may jump freely — enum
values do not have to be consecutive, which is handy for bit flags.</p>

<p>Enums are plain <code>int</code>s under the hood — no type safety
guarantees, but they document intent and give the debugger a name to
show. Switch statements love them:</p>

<pre class="code">enum state { IDLE, RUNNING, DONE };

switch (s) {
    case IDLE:   printf("idle\\n");   break;
    case RUNNING: printf("running\\n"); break;
    case DONE:   printf("done\\n");   break;
}</pre>

<p>The switch reads cleanly, and many compilers warn you if a new state
is added but not handled here — a free safety net as your program
grows.</p>

<p>A common idiom is adding a <b>count</b> member at the end:</p>

<pre class="code">enum color { RED, GREEN, BLUE, COLOR_COUNT };
// COLOR_COUNT == 3 — handy for array sizes</pre>

<p>Because COLOR_COUNT lands one past the last real colour, it doubles as
the array length: add a colour and every array sized with COLOR_COUNT
grows with it, exactly like the tryit example does with
<code>names[]</code>.</p>

<p>Gotcha: enum names share the namespace with variables — an enum
<code>color</code> and a variable <code>color</code> cannot coexist. And
C will happily assign 999 to an enum variable; the "type" is advisory,
not enforced.</p>
""",
                "tryit": """#include <stdio.h>

enum level { LOW = 1, MEDIUM, HIGH };
enum color { RED, GREEN, BLUE, COLOR_COUNT };

int main(void) {
    printf("LOW=%d MEDIUM=%d HIGH=%d\\n", LOW, MEDIUM, HIGH);

    const char *names[COLOR_COUNT] = {"red", "green", "blue"};
    for (int c = RED; c < COLOR_COUNT; c++) {
        printf("%d = %s\\n", c, names[c]);
    }
    return 0;
}
""",
            },
            {
                "title": "typedef",
                "html": """
<p><code>typedef</code> gives an existing type a new name. It does not
create a type — it creates an <b>alias</b>:</p>

<pre class="code">typedef unsigned long ulong;
typedef struct point point_t;

ulong big = 999999999;
point_t origin = {0.0, 0.0};</pre>

<p>Neither line invents anything new: <code>ulong</code> <i>is</i>
<code>unsigned long</code> under another name, and the two are
interchangeable everywhere. Typedefs mostly buy readability —
<code>point_t origin</code> says what it is better than
<code>struct point origin</code>.</p>

<p>The classic combination is typedef plus an anonymous struct, giving
the struct a single short name with no <code>struct</code> keyword
needed afterwards:</p>

<pre class="code">typedef struct {
    const char *name;
    int age;
} person;

person ada = {"Ada", 36};</pre>

<p>The struct here is anonymous — it has no tag at all, so
<code>struct ???</code> is impossible to write. The typedef is now its
only name, and declarations read like <code>person ada</code>: no
<code>struct</code> keyword anywhere.</p>

<p>typedef really shines for unreadable types — especially function
pointer types (Low-Level C chapter) — and for portability: platform code
can typedef <code>real</code> to <code>float</code> or <code>double</code>
in one place.</p>

<pre class="code">typedef int (*compare_fn)(const void *, const void *);
compare_fn cmp;    // reads like a normal variable!</pre>

<p>That line names a "pointer to a function taking two
<code>const void *</code> and returning int". Without the typedef you
would write <code>int (*cmp)(const void *, const void *);</code> for
every variable — and misplace a parenthesis. With it, <code>cmp</code>
looks like any other variable.</p>

<p>Style note: many projects end typedef names with <code>_t</code>
(<code>point_t</code>, <code>size_t</code> — which is itself a typedef of
an unsigned type provided by <code>&lt;stddef.h&gt;</code>).</p>

<p>Gotcha: typedef hides complexity, which cuts both ways. A pointer
typedef (<code>typedef int *int_ptr;</code>) makes
<code>const int_ptr</code> mean something subtle — const pointer, not
pointer-to-const. Common style: typedef structs and function pointers,
but keep raw pointer types visible.</p>
""",
                "tryit": """#include <stdio.h>

typedef unsigned long ulong;
typedef struct {
    const char *name;
    int age;
} person;

int main(void) {
    person ada = {"Ada", 36};
    printf("%s is %d\\n", ada.name, ada.age);
    printf("sizeof(ulong) = %zu\\n", sizeof(ulong));
    printf("sizeof(person) = %zu\\n", sizeof(person));
    return 0;
}
""",
            },
        ],
        "quiz": [
            {
                "type": "blank",
                "question": "Every C string ends with the <code>____</code> character (written <code>'\\\\0'</code>).",
                "answers": ["nul", "null", "nul terminator", "null terminator", "\\0"],
                "explain": "The NUL terminator '\\0' (a zero byte) marks the end of a C string.",
            },
            {
                "type": "mc",
                "question": "What does <code>strlen(\"hello\")</code> return?",
                "options": ["5", "6", "4", "whatever fits the buffer"],
                "answer": 0,
                "explain": "strlen counts characters before the NUL terminator: 5.",
            },
            {
                "type": "mc",
                "question": "With <code>struct point *pp</code>, which accesses field <code>x</code> through the pointer?",
                "options": ["pp.x", "*pp.x", "pp->x", "pp::x"],
                "answer": 2,
                "explain": "The arrow operator pp->x is shorthand for (*pp).x.",
            },
            {
                "type": "mc",
                "question": "After <code>union value v; v.i = 65;</code>, what is <code>v.bytes[0]</code> on a little-endian machine?",
                "options": ["65", "0", "undefined and always 0", "'A' as a string"],
                "answer": 0,
                "explain": "Union fields share memory; on little-endian, 65 stored as int has its low byte (65) first.",
            },
            {
                "type": "blank",
                "question": "The keyword that creates a new name for an existing type is <code>____</code>.",
                "answers": ["typedef"],
                "explain": "typedef unsigned long ulong; makes ulong an alias for unsigned long.",
            },
        ],
    },

    # ------------------------------------------------------------------ c05
    {
        "id": "c05",
        "title": "Type System",
        "emoji": "🏷️",
        "lessons": [
            {
                "title": "Conversions",
                "html": """
<p>C converts values between types constantly — sometimes silently. The
rules are worth knowing:</p>

<ul>
<li><b>Assignment:</b> the right side is converted to the left side's
type. <code>int i = 3.99;</code> stores <code>3</code> (truncation, not
rounding).</li>
<li><b>Integer promotion:</b> in any expression, <code>char</code> and
<code>short</code> are automatically promoted to <code>int</code> before
arithmetic.</li>
<li><b>Usual arithmetic conversions:</b> when two types meet in a binary
operation, the "smaller" one is converted to the bigger one:
<code>int + double</code> makes the int a double first.</li>
</ul>

<pre class="code">int i = 7;
double d = i / 2;       // 3.0 — division happened in int first!
double e = i / 2.0;     // 3.5 — 2.0 promotes i to double first</pre>

<p>The first line is the trap: <code>i / 2</code> runs as integer
division — both operands are int — and only <i>then</i> does the 3
become 3.0. Converting the result never recovers the 0.5 you already
lost.</p>

<p>Conversions can lose information silently: a big value narrowed to a
small type wraps or truncates, and float-to-int drops the fraction.</p>

<pre class="code">int big = 300;
char c = big;           // 44 — 300 doesn't fit a signed char
printf("%d\\n", c);</pre>

<p>300 does not fit a signed char (range −128 to 127), so the conversion
keeps the low 8 bits: 300 mod 256 = 44. No warning is even required —
narrowing is silent by design.</p>

<p>Strings convert to numbers with <code>atoi</code>, <code>atof</code>
and the more careful <code>strtol</code>/<code>strtod</code>; numbers
convert to strings with <code>sprintf</code> or <code>snprintf</code> —
there is no built-in implicit string conversion anywhere in C.</p>

<p>Gotcha: signed/unsigned mixing bites here too. In
<code>-1 &lt; 1u</code> the −1 is converted to a huge unsigned number
first, so the comparison is false. Convert explicitly when types
disagree, and treat every silent narrowing as a review flag.</p>
""",
                "tryit": """#include <stdio.h>
#include <stdlib.h>

int main(void) {
    int i = 7;
    printf("i / 2   = %.1f (int division first!)\\n", i / 2);
    printf("i / 2.0 = %.1f\\n", i / 2.0);

    int big = 300;
    char c = big;
    printf("300 as char = %d\\n", c);

    printf("atoi(\\"123xyz\\") = %d\\n", atoi("123xyz"));
    printf("atof(\\"2.5abc\\") = %g\\n", atof("2.5abc"));
    return 0;
}
""",
            },
            {
                "title": "Casting",
                "html": """
<p>When you want an explicit, deliberate conversion, write a <b>cast</b>:
the target type in parentheses before the value:</p>

<pre class="code">double d = 3.99;
int i = (int)d;              // 3 — truncation, on purpose

int total = 17, count = 2;
double avg = (double)total / count;   // 8.5 — cast BEFORE dividing</pre>

<p>That last line is the most useful cast in the language: casting one
operand to <code>double</code> forces floating-point division instead of
integer division. The cast happens <i>before</i> the division, so the
other operand is promoted too and 8.5 comes out.</p>


<p>Common cast uses:</p>

<ul>
<li><code>(int)</code>, <code>(double)</code> — numeric conversions</li>
<li><code>(char)</code> — narrowing an int to a byte</li>
<li><code>(void *)</code> — a "generic" pointer, convertible to and from
any object pointer type (how <code>malloc</code> and <code>qsort</code>
work)</li>
<li><code>(void)</code> — deliberately discard a value</li>
</ul>

<pre class="code">void *generic = &amp;some_int;
int *ip = (int *)generic;    // cast back to the real type</pre>

<p><code>void *</code> is C's generic pointer: any object pointer
converts to it and back. The round trip is safe only if you cast back to
the <i>original</i> type — store a double pointer, read it as an int
pointer, and the same bits come back as nonsense.</p>

<p>Casts do <b>not</b> change the underlying bits for pointers — they
change how the compiler treats them. Casting away errors (e.g. casting
an <code>int</code> to a pointer type "to silence a warning") hides bugs
rather than fixing them. A cast is a promise to the compiler: make it a
true statement.</p>

<p>Gotcha: <code>(int)3.99</code> is 3 — casts truncate toward zero, they
do not round. For nearest-integer behaviour use <code>round()</code>
from <code>&lt;math.h&gt;</code>. And never cast just to silence a
warning; find out why the warning fired instead.</p>
""",
                "tryit": """#include <stdio.h>

int main(void) {
    double d = 3.99;
    printf("(int)3.99        = %d\\n", (int)d);

    int total = 17, count = 2;
    printf("17/2     = %.1f\\n", total / count);
    printf("(double) = %.1f\\n", (double)total / count);

    char c = (char)321;
    printf("(char)321 = %d\\n", c);

    void *g = &d;
    double *dp = (double *)g;
    printf("through void*: %.2f\\n", *dp);
    return 0;
}
""",
            },
            {
                "title": "const",
                "html": """
<p><code>const</code> marks a value as read-only. Attempts to assign to
it are compile errors:</p>

<pre class="code">const int max_users = 100;
max_users = 5;          // compile error</pre>

<p>The compiler enforces this at compile time — there is no runtime cost
at all. Note the difference from <code>#define</code>: here
<code>max_users</code> has a type and obeys scope rules like any other
variable.</p>

<p>Unlike <code>#define</code>, a const variable is a real variable: it
has a type, obeys scope rules, and shows up in the debugger. Prefer it
for named constants.</p>

<p>The interesting part is <code>const</code> with pointers — read the
declaration from right to left:</p>

<ul>
<li><code>const int *p</code> — pointer to const int: the <b>value</b> is
read-only (<code>*p = 1</code> is an error, <code>p = q</code> is fine)</li>
<li><code>int *const p</code> — const pointer to int: the <b>pointer</b>
is read-only (<code>p = q</code> is an error, <code>*p = 1</code> is fine)</li>
<li><code>const int *const p</code> — both read-only</li>
</ul>

<p>Reading right to left makes the placement of <code>const</code>
speakable: "p is a pointer to an int that is const" versus "p is a const
pointer to an int". Say it out loud and you will never mix them up
again.</p>

<pre class="code">const char *msg = "hi";     // string literals are const!
// msg[0] = 'H';            // would be a write to read-only data</pre>

<p>So <code>msg</code> is a pointer to const chars: the pointer can move,
the letters cannot change. <code>fixed</code> is the opposite — the
pointer is welded to <code>value</code>, but the value itself updates
freely. String literals being const is why parameters that receive them
are declared <code>const char *</code>.</p>

<p><code>const</code> is also documentation: a parameter declared
<code>const char *s</code> promises the caller "I will not modify your
string" — the basis of C's read-only conventions.</p>

<p>Gotcha: casting away <code>const</code> and then writing through the
pointer is undefined behaviour if the object was truly defined const —
the compiler may have placed it in read-only memory. Const is a promise
with teeth.</p>
""",
                "tryit": """#include <stdio.h>

int total_length(const char *s, const char *t) {
    int n = 0;
    while (s[n]) n++;
    int m = 0;
    while (t[m]) m++;
    return n + m;
}

int main(void) {
    const int max_users = 100;
    printf("max_users = %d\\n", max_users);

    const char *msg = "hello";
    printf("%s + %s = %d chars\\n", msg, "world", total_length(msg, "world"));

    int value = 5;
    int *const fixed = &value;   // const pointer...
    *fixed = 7;                  // ...to a mutable int
    printf("value = %d\\n", value);
    return 0;
}
""",
            },
            {
                "title": "volatile",
                "html": """
<p><code>volatile</code> tells the compiler: <b>this variable may change
behind your back — every read and write must actually happen, in
order</b>.</p>

<pre class="code">volatile int *status_reg = (volatile int *)0x4000;</pre>

<p>That line turns a raw number into a pointer the compiler must treat
carefully — typical for embedded code talking to hardware at fixed
addresses.</p>

<p>Why it exists: compilers optimise by caching values in registers and
removing "redundant" reads. That is normally great — but it breaks when
the variable is changed by something the compiler cannot see:</p>

<ul>
<li><b>Hardware registers</b> — memory-mapped device status that hardware
updates asynchronously</li>
<li><b>Interrupt service routines</b> — a flag set between two statements
of the main flow</li>
<li><b>setjmp/longjmp</b> — locals modified between setjmp and longjmp
should be volatile to survive the jump</li>
</ul>

<pre class="code">volatile int quit = 0;
while (!quit) {
    // ... do work ... (an interrupt may set quit = 1)
}</pre>

<p>With <code>volatile</code> in place, every iteration of that loop
re-fetches <code>quit</code> from memory and sees the interrupt's write.
Without it, the loop may spin forever on a cached zero.</p>

<p>Without <code>volatile</code>, the compiler may read <code>quit</code>
once, see it never changes in the loop body, and turn the loop into
<code>while (1)</code>. With it, every iteration re-reads the real
variable.</p>

<p>Note what volatile is <b>not</b>: it is not a synchronisation or
thread-safety tool (that is atomics — see the Modern C chapter), and it
does not make operations atomic. It only disables caching and reordering
for that one variable.</p>

<p>Rule of thumb: volatile for hardware registers and interrupt flags,
atomics for threads — and never "just to be safe" everywhere, because
volatile disables optimisations. Sprinkle it and your code gets slower
without getting safer.</p>
""",
            },
            {
                "title": "restrict",
                "html": """
<p><code>restrict</code> is a promise you make to the compiler about
pointers: <b>for the lifetime of this pointer, it is the only way the
object it points to is accessed</b>. No other pointer in scope writes or
reads that memory.</p>

<pre class="code">void copy(char *restrict dst, const char *restrict src, int n) {
    for (int i = 0; i &lt; n; i++) {
        dst[i] = src[i];
    }
}</pre>

<p>Nothing in the body looks special — the promise lives in the
parameters. The compiler may now assume <code>dst[i]</code> never
touches what <code>src</code> points at, so it can preload values and
copy in vector-sized chunks.</p>

<p>Why promise this? <b>Speed.</b> Without it, the compiler must assume
<code>dst</code> and <code>src</code> might overlap — so every write to
<code>dst</code> could change <code>src</code>'s data, forcing it to
reload values and blocking optimisations. With <code>restrict</code>, it
can vectorise and reorder freely.</p>

<p>The standard library uses it everywhere you look:
<code>memcpy</code> takes restrict pointers — that is why
<code>memcpy</code> is undefined for overlapping ranges, while its
non-restricted sibling <code>memmove</code> handles overlap safely.</p>

<pre class="code">memcpy(dst, src, n);      // restrict: caller guarantees no overlap
memmove(dst, src, n);     // no restrict: overlap is fine</pre>

<p>The two functions are twins with different contracts:
<code>memcpy</code> trusts your promise and runs flat out;
<code>memmove</code> checks for overlap and takes the safe path when it
must.</p>

<p>If you break the promise — access the same object through two
different restrict pointers — behaviour is undefined. Use restrict in
hot numeric/array code where you know the data does not alias; skip it
everywhere else.</p>

<p>Rule of thumb: if a caller could reasonably pass overlapping buffers,
do not take restrict — you would be writing an invisible time bomb.</p>
""",
            },
            {
                "title": "Storage Classes",
                "html": """
<p>Every variable in C has a <b>storage class</b> that controls its
lifetime, linkage, and where it lives. The keywords:</p>

<ul>
<li><code>auto</code> — the default for locals: created on block entry,
destroyed on exit. (Nobody writes this keyword; it exists for
completeness.)</li>
<li><code>static</code> — two meanings depending on where it appears
(see below)</li>
<li><code>extern</code> — "this variable lives in another file; here is
its declaration" — the linker joins them up</li>
<li><code>register</code> — a hint that this variable is used heavily;
modern compilers ignore it, and you cannot take its address</li>
<li><code>_Thread_local</code> — one copy per thread (Modern C chapter)</li>
</ul>

<p><code>static</code> is the interesting one. On a <b>local
variable</b>, it moves the variable from the stack to permanent storage —
it is created once and keeps its value between calls:</p>

<pre class="code">int counter(void) {
    static int n = 0;    // initialised once, remembers between calls
    n++;
    return n;
}</pre>

<p>Call <code>counter()</code> three times and it answers 1, 2, 3: the
initialiser ran once, before <code>main</code> even started, and
<code>n</code> simply persists between calls. Its scope is still local —
no other function can see it.</p>

<p>On a <b>global variable or function</b>, static means "private to this
file" — the name is not exported to the linker. It is C's tool for
information hiding in multi-file projects.</p>

<pre class="code">static int helper_count = 0;   // only this .c file can see it
static void helper(void) { }   // likewise</pre>

<p>Gotchas: static locals make a function un-reentrant — two threads
calling <code>counter</code> race on the same <code>n</code>. And on
globals, reach for static by default: anything you do not export cannot
be accidentally depended on by another file.</p>
""",
                "tryit": """#include <stdio.h>

int counter(void) {
    static int n = 0;
    n++;
    return n;
}

int main(void) {
    printf("%d ", counter());
    printf("%d ", counter());
    printf("%d\\n", counter());   // 1 2 3 — it remembers!
    return 0;
}
""",
            },
        ],
        "quiz": [
            {
                "type": "mc",
                "question": "What is <code>(int)3.99</code>?",
                "options": ["4", "3", "3.99 rounds to 4 only with (int)", "undefined"],
                "answer": 1,
                "explain": "Float-to-int conversion truncates toward zero: 3.",
            },
            {
                "type": "mc",
                "question": "Which declaration makes the POINTED-TO value read-only?",
                "options": ["int *const p", "const int *p", "int const const p", "int p *const"],
                "answer": 1,
                "explain": "const int *p — the int is const (can't write *p), the pointer itself can move.",
            },
            {
                "type": "mc",
                "question": "Why does memcpy use restrict parameters while memmove does not?",
                "options": [
                    "Historical accident",
                    "restrict promises no overlap, letting memcpy be faster; memmove must handle overlap",
                    "restrict makes them thread-safe",
                    "There is no difference",
                ],
                "answer": 1,
                "explain": "restrict promises the buffers don't overlap, unlocking optimisation; memmove pays the cost of handling overlap.",
            },
            {
                "type": "mc",
                "question": "What does <code>static</code> do to a local variable?",
                "options": [
                    "Makes it const",
                    "Makes it visible to other files",
                    "Gives it permanent storage that keeps its value between calls",
                    "Puts it in a register",
                ],
                "answer": 2,
                "explain": "A static local is created once and keeps its value across function calls.",
            },
            {
                "type": "blank",
                "question": "The keyword promising \"this variable changes outside the compiler's sight; re-read it every time\" is <code>____</code>.",
                "answers": ["volatile"],
                "explain": "volatile disables caching/reordering for that variable — essential for hardware registers and interrupt flags.",
            },
        ],
    },
]
