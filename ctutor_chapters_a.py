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

<pre class="code">int height;          // declare
height = 176;        // assign
int width = 42;      // declare and assign at once</pre>

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

<p>Characters are just small integers — <code>'A'</code> is really the
number 65. That is why C can do arithmetic on characters:</p>

<pre class="code">char c = 'a';
c = c + 1;           // now 'b'</pre>

<p>When a type matters for portability (file formats, protocols), use the
fixed-width types from <code>&lt;stdint.h&gt;</code>:
<code>int32_t</code>, <code>uint8_t</code>, <code>int64_t</code> and
friends — the number in the name is guaranteed to be the size in bits.</p>

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

<pre class="code">int add(int a, int b) {
    return a + b;
}

double area(double r) {
    return 3.14159265358979 * r * r;
}</pre>

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

<p>This "pass by pointer" is C's version of out-parameters, and it is
everywhere in real code. Structs, by the way, are also passed by value —
the whole struct is copied, which is usually what you want for small
records.</p>
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

<pre class="code">int is_even(int n);     // prototype: ends with ;

int is_odd(int n) {
    if (n == 0) return 0;
    return is_even(n - 1);      // fine: is_even is declared
}

int is_even(int n) {
    if (n == 0) return 1;
    return is_odd(n - 1);
}</pre>

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

<p>Two facts define arrays in C:</p>

<ul>
<li><b>No bounds checking.</b> <code>fib[7]</code> compiles happily and
reads/writes memory past the end — a classic source of bugs and security
holes. The language trusts you completely.</li>
<li><b>The size is part of the type</b> and must be known (or computed at
runtime for VLAs — see Advanced C).</li>
</ul>

<p>Multidimensional arrays are arrays of arrays:</p>

<pre class="code">int grid[2][3] = {
    {1, 2, 3},
    {4, 5, 6},
};
printf("%d\\n", grid[1][2]);   // 6</pre>

<p>Arrays have a deep relationship with pointers: in most expressions the
name of an array <b>decays</b> to a pointer to its first element. So
<code>fib</code> and <code>&amp;fib[0]</code> mean the same thing, and
functions that receive arrays actually receive a pointer (next two
lessons cover what that implies).</p>
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

<p>The compiler multiplies the step by <code>sizeof(element)</code>: on an
<code>int *</code>, <code>p + 1</code> advances 4 bytes; on a
<code>double *</code>, 8. This is why the pointer's type matters.</p>

<p>Two pointers into the same array can be subtracted, giving the number
of elements between them:</p>

<pre class="code">int *q = &amp;a[3];
printf("%d\\n", (int)(q - a));   // 3</pre>

<p>Because arrays decay to pointers to their first element, indexing is
defined in terms of pointer arithmetic:
<code>a[i]</code> is exactly <code>*(a + i)</code>. This also means
pointer arithmetic is how you walk arrays in C:</p>

<pre class="code">int *end = a + 4;
for (int *p = a; p &lt; end; p++) {
    printf("%d ", *p);
}</pre>

<p>Pointer arithmetic outside an array (or past its end) is undefined
behaviour — the sandbox in this course will catch it and tell you.</p>
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

<pre class="code">#include &lt;stdlib.h&gt;

int *scores = malloc(n * sizeof(int));   // space for n ints
if (scores == NULL) {
    // allocation failed — handle it
}</pre>

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

<pre class="code">int *p = calloc(4, sizeof(int));    // {0, 0, 0, 0}
p = realloc(p, 8 * sizeof(int));    // grow to 8 ints
p[7] = 77;
free(p);</pre>
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

<p>The golden rule: the destination buffer must be large enough.
<code>strcpy</code> and <code>strcat</code> cannot know its size — that
trust is the source of the infamous <b>buffer overflow</b>. Safer
variants (<code>strncpy</code>, <code>strncat</code>) take an explicit
limit.</p>
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

<pre class="code">struct point {
    double x;
    double y;
};

struct point p = {3.0, 4.0};    // initialize in order
p.x = 10.0;                     // dot accesses a field</pre>

<p>Structs are true values: you can assign them (the whole thing is
copied), pass them to functions by value, and return them:</p>

<pre class="code">struct point scale(struct point v, double k) {
    v.x *= k;           // safe: v is a private copy
    v.y *= k;
    return v;           // returns the modified copy
}</pre>

<p>When you have a <b>pointer to a struct</b> (very common — e.g. from
<code>malloc</code>), a dedicated operator <code>-&gt;</code> accesses
fields through the pointer:</p>

<pre class="code">struct point *pp = &amp;p;
pp-&gt;x = 42.0;               // same as (*pp).x

struct point *heap = malloc(sizeof(struct point));
heap-&gt;y = 7.0;
free(heap);</pre>

<p>Structs can nest, contain arrays, and even contain pointers to their
own type — the building block of linked lists and trees:</p>

<pre class="code">struct node {
    int value;
    struct node *next;    // pointer to the next node
};</pre>
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

<p>Reading a field other than the one last written is technically
implementation-defined, but it is the standard trick for looking at
representations — and a favourite interview question.</p>
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

<pre class="code">enum color { RED, GREEN, BLUE };

enum color c = GREEN;
printf("%d\\n", c);     // 1</pre>

<p>By default the first name is 0 and each following name is one more.
You can choose values, and counting continues from there:</p>

<pre class="code">enum level { LOW = 1, MEDIUM, HIGH };   // 1, 2, 3
enum flags { A = 1, B = 4, C = 8 };</pre>

<p>Enums are plain <code>int</code>s under the hood — no type safety
guarantees, but they document intent and give the debugger a name to
show. Switch statements love them:</p>

<pre class="code">enum state { IDLE, RUNNING, DONE };

switch (s) {
    case IDLE:   printf("idle\\n");   break;
    case RUNNING: printf("running\\n"); break;
    case DONE:   printf("done\\n");   break;
}</pre>

<p>A common idiom is adding a <b>count</b> member at the end:</p>

<pre class="code">enum color { RED, GREEN, BLUE, COLOR_COUNT };
// COLOR_COUNT == 3 — handy for array sizes</pre>
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

<p>The classic combination is typedef plus an anonymous struct, giving
the struct a single short name with no <code>struct</code> keyword
needed afterwards:</p>

<pre class="code">typedef struct {
    const char *name;
    int age;
} person;

person ada = {"Ada", 36};</pre>

<p>typedef really shines for unreadable types — especially function
pointer types (Low-Level C chapter) — and for portability: platform code
can typedef <code>real</code> to <code>float</code> or <code>double</code>
in one place.</p>

<pre class="code">typedef int (*compare_fn)(const void *, const void *);
compare_fn cmp;    // reads like a normal variable!</pre>

<p>Style note: many projects end typedef names with <code>_t</code>
(<code>point_t</code>, <code>size_t</code> — which is itself a typedef of
an unsigned type provided by <code>&lt;stddef.h&gt;</code>).</p>
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

<p>Conversions can lose information silently: a big value narrowed to a
small type wraps or truncates, and float-to-int drops the fraction.</p>

<pre class="code">int big = 300;
char c = big;           // 44 — 300 doesn't fit a signed char
printf("%d\\n", c);</pre>

<p>Strings convert to numbers with <code>atoi</code>, <code>atof</code>
and the more careful <code>strtol</code>/<code>strtod</code>; numbers
convert to strings with <code>sprintf</code> or <code>snprintf</code> —
there is no built-in implicit string conversion anywhere in C.</p>
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
integer division.</p>

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

<p>Casts do <b>not</b> change the underlying bits for pointers — they
change how the compiler treats them. Casting away errors (e.g. casting
an <code>int</code> to a pointer type "to silence a warning") hides bugs
rather than fixing them. A cast is a promise to the compiler: make it a
true statement.</p>
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

<pre class="code">const char *msg = "hi";     // string literals are const!
// msg[0] = 'H';            // would be a write to read-only data</pre>

<p><code>const</code> is also documentation: a parameter declared
<code>const char *s</code> promises the caller "I will not modify your
string" — the basis of C's read-only conventions.</p>
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

<p>Without <code>volatile</code>, the compiler may read <code>quit</code>
once, see it never changes in the loop body, and turn the loop into
<code>while (1)</code>. With it, every iteration re-reads the real
variable.</p>

<p>Note what volatile is <b>not</b>: it is not a synchronisation or
thread-safety tool (that is atomics — see the Modern C chapter), and it
does not make operations atomic. It only disables caching and reordering
for that one variable.</p>
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

<p>If you break the promise — access the same object through two
different restrict pointers — behaviour is undefined. Use restrict in
hot numeric/array code where you know the data does not alias; skip it
everywhere else.</p>
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

<p>On a <b>global variable or function</b>, static means "private to this
file" — the name is not exported to the linker. It is C's tool for
information hiding in multi-file projects.</p>

<pre class="code">static int helper_count = 0;   // only this .c file can see it
static void helper(void) { }   // likewise</pre>
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
