"""C Tutor chapters 6-9, distilled from Beej's Guide to C Programming."""

CHAPTERS_CT_B = [
    # ------------------------------------------------------------------ c06
    {
        "id": "c06",
        "title": "Program Organization",
        "emoji": "🗂️",
        "lessons": [
            {
                "title": "Header Files",
                "html": """
<p>A <b>header file</b> (extension <code>.h</code>) is the public
interface of a piece of code: function prototypes, type definitions and
macros, ready to be shared:</p>

<pre class="code">// geometry.h
#ifndef GEOMETRY_H
#define GEOMETRY_H

typedef struct { double x, y; } point;

double distance(point a, point b);

#endif</pre>

<p>Every <code>.c</code> file that wants the interface writes
<code>#include "geometry.h"</code> — and the compiler literally pastes
the header's text into the file at that point (that is all
<code>#include</code> does).</p>

<p>Two include forms:</p>

<ul>
<li><code>#include &lt;stdio.h&gt;</code> — angle brackets: search the
<b>system</b> include directories</li>
<li><code>#include "geometry.h"</code> — quotes: search the
<b>project</b> directory first</li>
</ul>

<p>The <code>#ifndef / #define / #endif</code> sandwich is an
<b>include guard</b>: if the header is included twice in one
compilation, the second copy is skipped because the guard macro is
already defined. Without it, duplicate definitions cause compile errors
in bigger projects.</p>

<p>Rule of thumb: headers declare, sources define. A header should
compile on its own and never contain function bodies (with the
exception of small <code>static inline</code> helpers).</p>
""",
            },
            {
                "title": "Multiple Files",
                "html": """
<p>Real projects split code across many <code>.c</code> files, each
responsible for one area. The compiler compiles each file
independently; they meet only at link time.</p>

<pre class="code">// main.c
#include "geometry.h"
#include &lt;stdio.h&gt;

int main(void) {
    point a = {0, 0}, b = {3, 4};
    printf("%f\\n", distance(a, b));
    return 0;
}

// geometry.c
#include "geometry.h"
#include &lt;math.h&gt;

double distance(point a, point b) {
    return sqrt((a.x-b.x)*(a.x-b.x) + (a.y-b.y)*(a.y-b.y));
}</pre>

<p>What makes a name visible across files?</p>

<ul>
<li>A normal global variable or function is <b>external</b> — other
files can declare it with <code>extern</code> and use it.</li>
<li><code>static</code> makes a function or global <b>private to its
file</b> — the linker never sees it. This is C's information
hiding.</li>
</ul>

<pre class="code">// counters.c
int public_total = 0;          // shared
static int internal_hits = 0;  // private

// main.c
extern int public_total;       // declaration, not definition</pre>

<p>Good structure: each <code>.c</code> pairs with a header that exposes
its public names; everything else is <code>static</code>. This keeps
interfaces small and prevents accidental coupling.</p>
""",
            },
            {
                "title": "Object Files",
                "html": """
<p>Between source and executable sits an intermediate form: the
<b>object file</b> (extension <code>.o</code> on Unix, <code>.obj</code>
on Windows). Compiling one file means:</p>

<pre class="code">gcc -c geometry.c     # produces geometry.o
gcc -c main.c         # produces main.o</pre>

<p>The <code>-c</code> flag says "compile only — do not link". An object
file contains machine code plus a table of <b>symbols</b>: names it
defines, and names it still needs.</p>

<pre class="code">nm geometry.o
# T distance        — "T" = defined text (code) symbol
# U sqrt            — "U" = undefined: still needs sqrt</pre>

<p>Why split compilation from linking?</p>

<ul>
<li><b>Speed:</b> when you edit one file, only that file is recompiled —
this is exactly what <code>make</code> automates.</li>
<li><b>Distribution:</b> libraries ship as compiled objects; you link
against them without their source.</li>
</ul>

<p>A typical build with separate steps:</p>

<pre class="code">gcc -c main.c geometry.c
gcc main.o geometry.o -o app -lm</pre>

<p>Here <code>-lm</code> tells the linker to also pull in the math
library (where <code>sqrt</code> lives). Each object file only ever
sees its own source — headers provide the cross-file type information
the compiler needs.</p>
""",
            },
            {
                "title": "Linking",
                "html": """
<p>The <b>linker</b> (<code>ld</code>, invoked by your compiler driver)
takes object files and libraries and welds them into one executable.
Its core job is <b>symbol resolution</b>: matching every "undefined"
symbol in one object to a "defined" symbol in another.</p>

<pre class="code">main.o:  U distance  U printf
geometry.o:  T distance   U sqrt
libm:        T sqrt
            ─────────────
app: all U symbols resolved</pre>

<p>When resolution fails, you get the classic link errors:</p>

<ul>
<li><code>undefined reference to 'distance'</code> — you called it but
never linked the object that defines it (forgot the <code>.c</code>
file, or the function is <code>static</code>)</li>
<li><code>multiple definition of 'total'</code> — two objects both
define the same global; usually a variable defined in a header instead
of declared there</li>
</ul>

<p>After resolution, the linker lays out the final memory image: the
<b>text segment</b> (code, read-only), <b>data segment</b> (initialised
globals), <b>bss</b> (zero-initialised globals), and metadata the OS
loader uses to start the program.</p>

<p>Static vs dynamic linking: statically linked programs copy library
code into the executable (self-contained, bigger); dynamically linked
ones record "I need libm.so" and load it at startup (smaller, shared,
but depends on the system having the library).</p>
""",
            },
        ],
        "quiz": [
            {
                "type": "mc",
                "question": "What does #include actually do?",
                "options": [
                    "Imports a module like Python",
                    "Pastes the included file's text into the source at that point",
                    "Links a library",
                    "Creates a namespace",
                ],
                "answer": 1,
                "explain": "The preprocessor literally substitutes the header's text where #include appears.",
            },
            {
                "type": "mc",
                "question": "Why wrap a header in #ifndef/#define/#endif?",
                "options": [
                    "To make compilation faster",
                    "As an include guard: a second inclusion is skipped",
                    "To mark it as C instead of C++",
                    "It is only stylistic",
                ],
                "answer": 1,
                "explain": "The guard macro makes a second inclusion expand to nothing, preventing duplicate definitions.",
            },
            {
                "type": "mc",
                "question": "static on a global function means:",
                "options": [
                    "It cannot be called",
                    "It is private to its .c file — the linker never exports it",
                    "It runs faster",
                    "It keeps its value between calls",
                ],
                "answer": 1,
                "explain": "File-scope static = internal linkage: the name is invisible outside its translation unit.",
            },
            {
                "type": "blank",
                "question": "A file of compiled machine code plus a symbol table, produced by gcc -c, is called an <code>____</code> file.",
                "answers": ["object", ".o", "obj"],
                "explain": "Object files (.o/.obj) hold machine code and symbols; the linker resolves them into an executable.",
            },
            {
                "type": "mc",
                "question": "What causes 'undefined reference to distance' at link time?",
                "options": [
                    "distance was declared in a header",
                    "The object file defining distance was never linked",
                    "distance is too long a name",
                    "You forgot a semicolon",
                ],
                "answer": 1,
                "explain": "A declaration is not a definition — the linker needs the object that actually contains the code.",
            },
        ],
    },

    # ------------------------------------------------------------------ c07
    {
        "id": "c07",
        "title": "Input / Output",
        "emoji": "🔌",
        "lessons": [
            {
                "title": "Console I/O",
                "html": """
<p>Console I/O lives in <code>&lt;stdio.h&gt;</code>. You already know
<code>printf</code>; the format specifiers are worth mastering:</p>

<pre class="code">printf("%d %s %c %.2f %zu\\n", 42, "hi", 'x', 3.14159, sizeof(int));
#   %d int   %s string   %c char   %f float   %zu size_t</pre>

<p>Between <code>%</code> and the letter you can add <b>width</b>,
<b>precision</b> and flags:</p>

<pre class="code">printf("[%5d] [%-5d] [%05d]\\n", 42, 42, 42);
printf("[%10.3f]\\n", 3.14159);     // 10 wide, 3 decimals</pre>

<p>Reading input is <code>scanf</code> — it takes <b>addresses</b> to
fill in, and returns the number of items successfully read (or
<code>EOF</code>):</p>

<pre class="code">int age;
if (scanf("%d", &amp;age) == 1) {
    printf("you are %d\\n", age);
}</pre>

<p>Character-level I/O uses <code>getchar()</code> and
<code>putchar(c)</code> — the standard idiom to process all input:</p>

<pre class="code">int c;                       // int, not char — must hold EOF
while ((c = getchar()) != EOF) {
    putchar(c);
}</pre>

<p>Two habits to keep: always check <code>scanf</code>'s return value
(input may not match), and remember that <code>scanf("%s", buf)</code>
cannot limit length — prefer <code>scanf("%15s", buf)</code> with a
width matching your buffer.</p>
""",
                "tryit": """#include <stdio.h>

int main(void) {
    printf("[%5d] [%-5d] [%05d]\\n", 42, 42, 42);
    printf("[%10.3f]\\n", 3.14159);

    int lines = 0;
    int c;
    while ((c = getchar()) != EOF) {
        if (c == '\\n') lines++;
    }
    printf("saw %d newline(s)\\n", lines);
    return 0;
}
""",
            },
            {
                "title": "Files",
                "html": """
<p>File I/O revolves around one opaque type: <code>FILE *</code>. You
open a file, get a handle, read/write through it, and close it:</p>

<pre class="code">FILE *f = fopen("names.txt", "r");   // "r" = read
if (f == NULL) {
    printf("cannot open\\n");
    return 1;
}
// ... use f ...
fclose(f);</pre>

<p>Mode strings: <code>"r"</code> read, <code>"w"</code> write (truncates
or creates), <code>"a"</code> append, plus <code>+</code> for update and
<code>b</code> for binary (<code>"rb+"</code> etc).</p>

<p>Reading text line by line — <code>fgets</code> reads up to n-1 chars,
stops at a newline, keeps the newline, and NUL-terminates. It returns
NULL at end of file:</p>

<pre class="code">char line[64];
while (fgets(line, sizeof line, f) != NULL) {
    printf("read: %s", line);    // line still has its \\n
}</pre>

<p>Writing mirrors printing: <code>fprintf(f, ...)</code>,
<code>fputs</code>, <code>fputc</code>. And always close —
<code>fclose</code> flushes buffered output and releases the handle.</p>

<pre class="code">FILE *out = fopen("log.txt", "w");
if (out) {
    fprintf(out, "n=%d\\n", 42);
    fclose(out);
}</pre>

<p>Handy companions: <code>feof(f)</code> (end reached?),
<code>ferror(f)</code>, <code>rewind(f)</code>, <code>fseek</code>/
<code>ftell</code> for jumping around inside a file.</p>
""",
                "tryit": """#include <stdio.h>

int main(void) {
    FILE *f = fopen("names.txt", "r");
    if (f == NULL) { printf("cannot open\\n"); return 1; }

    char line[64];
    while (fgets(line, sizeof line, f) != NULL) {
        printf("hi %s", line);
    }
    fclose(f);

    FILE *out = fopen("greet.txt", "w");
    if (out) {
        fprintf(out, "written by the sandbox\\n");
        fclose(out);
    }
    return 0;
}
""",
            },
            {
                "title": "Binary I/O",
                "html": """
<p>Text files store characters; <b>binary files</b> store raw bytes —
the exact memory image of your data. C gives you two functions that
move blocks of memory to and from files:</p>

<pre class="code">size_t fread(void *ptr, size_t size, size_t count, FILE *f);
size_t fwrite(const void *ptr, size_t size, size_t count, FILE *f);</pre>

<p>They return the number of complete items transferred. The classic
round trip for an array of numbers:</p>

<pre class="code">int v[4] = {10, 20, 30, 40};

FILE *f = fopen("data.bin", "wb");     // b = binary
fwrite(v, sizeof(int), 4, f);
fclose(f);

int back[4] = {0};
FILE *g = fopen("data.bin", "rb");
fread(back, sizeof(int), 4, g);
fclose(g);</pre>

<p>Structs can be written the same way — <code>fwrite(&amp;s, sizeof s,
1, f)</code> — which leads to the caveats Beej warns about:</p>

<ul>
<li><b>Padding:</b> the bytes between struct fields (see Memory Layout)
are written too, and differ between compilers — so the file is not
portable across platforms.</li>
<li><b>Endianness:</b> a little-endian machine writes its ints
byte-reversed compared to a big-endian one.</li>
<li><b>Text vs binary mode:</b> on Windows, text mode translates
<code>\\n</code>; binary mode does not. For data files, always open
with <code>b</code>.</li>
</ul>

<p>This is why real file formats (PNG, SQLite...) specify exact byte
layouts instead of dumping structs — they serialize field by field.</p>
""",
                "tryit": """#include <stdio.h>

int main(void) {
    int v[4] = {10, 20, 30, 40};

    FILE *f = fopen("numbers.bin", "wb");
    if (f == NULL) { printf("cannot write\\n"); return 1; }
    fwrite(v, sizeof(int), 4, f);
    fclose(f);

    int back[4] = {0};
    FILE *g = fopen("numbers.bin", "rb");
    if (g == NULL) { printf("cannot read\\n"); return 1; }
    size_t got = fread(back, sizeof(int), 4, g);
    fclose(g);

    printf("read %zu items:", got);
    for (int i = 0; i < 4; i++) printf(" %d", back[i]);
    printf("\\n");
    return 0;
}
""",
            },
        ],
        "quiz": [
            {
                "type": "mc",
                "question": "What does fopen return when the file cannot be opened for reading?",
                "options": ["An empty FILE", "NULL", "-1", "It crashes"],
                "answer": 1,
                "explain": "fopen returns NULL on failure — always check before using the handle.",
            },
            {
                "type": "codefill",
                "question": "Read one line safely into a 64-byte buffer:",
                "code": [
                    "char line[64];",
                    "while (",
                    { "blank": "fgets", "answers": ["fgets"] },
                    "(line, sizeof line, f) != NULL) {",
                    "    printf(\"%s\", line);",
                    "}",
                ],
                "explain": "fgets reads at most n-1 chars, stops at newline, and NUL-terminates.",
            },
            {
                "type": "mc",
                "question": "Why is getchar()'s return value stored in an int, not a char?",
                "options": [
                    "Style",
                    "It must be able to represent EOF (typically -1) as well as every char",
                    "chars are too slow",
                    "It is not — char works fine",
                ],
                "answer": 1,
                "explain": "EOF is negative; a plain char may not hold it alongside all 256 byte values.",
            },
            {
                "type": "mc",
                "question": "Writing a struct with fwrite() to share across machines is risky because:",
                "options": [
                    "fwrite is slow",
                    "Padding bytes and endianness may differ on the reader's machine",
                    "Files must be named .bin",
                    "Structs cannot be written",
                ],
                "answer": 1,
                "explain": "Raw struct dumps bake in padding and byte order — real formats serialize field by field.",
            },
        ],
    },

    # ------------------------------------------------------------------ c08
    {
        "id": "c08",
        "title": "The Preprocessor",
        "emoji": "⚙️",
        "lessons": [
            {
                "title": "#include",
                "html": """
<p>The preprocessor is a text-manipulation program that runs
<b>before</b> the compiler. Its simplest directive is
<code>#include</code> — paste a file's contents right here:</p>

<pre class="code">#include &lt;stdio.h&gt;      // system header
#include "myutils.h"    // your header</pre>

<p>That is the entire magic behind headers: textual inclusion. The
compiler never sees your 20 include lines — it sees one big file with
everything pasted in.</p>

<p>The preprocessor also defines a set of built-in macros, useful for
debug output:</p>

<pre class="code">printf("file %s, line %d\\n", __FILE__, __LINE__);</pre>

<ul>
<li><code>__FILE__</code> — the current file name</li>
<li><code>__LINE__</code> — the current line number</li>
<li><code>__DATE__</code>, <code>__TIME__</code> — compilation time</li>
<li><code>__STDC__</code> — defined in standard C compilers</li>
</ul>

<p>Remember: the preprocessor knows <b>nothing about C</b>. It cannot
check types, does not understand expressions, and will happily paste
nonsense. It is a text tool — the compiler afterwards is what gives the
result meaning.</p>
""",
                "tryit": """#include <stdio.h>

int main(void) {
    printf("this is %s, line %d\\n", __FILE__, __LINE__);
    printf("still line %d\\n", __LINE__);
    return 0;
}
""",
            },
            {
                "title": "Macros",
                "html": """
<p><code>#define</code> creates a macro — a name the preprocessor
replaces with text before compilation:</p>

<pre class="code">#define MAX_USERS 100
#define GREETING "hello"

if (users &gt; MAX_USERS) { ... }</pre>

<p><b>Function-like macros</b> take arguments and are the ones that bite.
Always parenthesise the body and every parameter:</p>

<pre class="code">#define SQUARE(x)   ((x) * (x))     // good
#define BAD(x)      x * x           // trouble

int a = SQUARE(2 + 3);   // ((2+3)*(2+3)) = 25
int b = BAD(2 + 3);      // 2+3*2+3       = 11!</pre>

<p>Without inner parens, operator precedence corrupts the expansion.
This is why real macros look over-parenthesised.</p>

<p>Two special operators exist inside function-like macros:</p>

<ul>
<li><code>#x</code> — <b>stringize</b>: turn the argument's text into a
string literal</li>
<li><code>a##b</code> — <b>paste</b>: glue two tokens into one</li>
</ul>

<pre class="code">#define STR(x) #x
#define CAT(a, b) a##b

printf("%s\\n", STR(hello there));   // "hello there"
int CAT(va, r) = 7;                  // declares: int var = 7;</pre>

<p>Multi-line macros join with backslashes, and modern advice is clear:
prefer <code>const</code> variables and real functions when they can do
the job — macros have no types, no scope, and evaluate arguments
repeatedly.</p>
""",
                "tryit": """#include <stdio.h>

#define SQUARE(x) ((x) * (x))
#define BAD(x) x * x
#define STR(x) #x
#define CAT(a, b) a##b

int main(void) {
    printf("SQUARE(2+3) = %d\\n", SQUARE(2 + 3));
    printf("BAD(2+3)    = %d\\n", BAD(2 + 3));
    printf("%s\\n", STR(hello there));

    int CAT(va, r) = 7;
    printf("var = %d\\n", var);
    return 0;
}
""",
            },
            {
                "title": "Conditional Compilation",
                "html": """
<p>The preprocessor can include or discard code before compilation —
the tool behind "debug builds", cross-platform code and configuration:</p>

<pre class="code">#define DEBUG 1

#if DEBUG
    printf("debug mode\\n");
#endif

#ifdef DEBUG          // is DEBUG defined at all?
    ...
#endif

#ifndef NDEBUG        // "if not NDEBUG" — the assert idiom
    ...
#endif</pre>

<p>The directive family:</p>

<ul>
<li><code>#if expr</code> / <code>#elif</code> / <code>#else</code> /
<code>#endif</code> — evaluate an integer constant expression</li>
<li><code>#ifdef NAME</code> / <code>#ifndef NAME</code> — defined or not
defined</li>
<li><code>defined(NAME)</code> — usable inside <code>#if</code>
expressions</li>
<li><code>#undef NAME</code> — forget a macro</li>
<li><code>#error message</code> — deliberately stop with your own
message (e.g. "this code needs C11")</li>
</ul>

<pre class="code">#include &lt;stdio.h&gt;

#define USE_FAST_MATH 1

int main(void) {
#if USE_FAST_MATH
    printf("fast path\\n");
#else
    printf("portable path\\n");
#endif

#ifndef VERSION
#define VERSION "dev"
#endif
    printf("version %s\\n", VERSION);
    return 0;
}</pre>

<p>Discarded branches must still be lexically sane, but they are never
compiled — this is how the same source supports different platforms
with <code>#ifdef _WIN32</code> ... <code>#else</code> ... blocks.</p>
""",
                "tryit": """#include <stdio.h>

#define USE_FAST_MATH 1

int main(void) {
#if USE_FAST_MATH
    printf("fast path\\n");
#else
    printf("portable path\\n");
#endif

#ifndef VERSION
#define VERSION "dev"
#endif
    printf("version %s\\n", VERSION);
    return 0;
}
""",
            },
        ],
        "quiz": [
            {
                "type": "mc",
                "question": "Which macro expands correctly for SQUARE(2 + 3) with result 25?",
                "options": ["#define SQUARE(x) x * x", "#define SQUARE(x) ((x) * (x))", "#define SQUARE(x) (x) * (x)", "#define SQUARE (x) x*x"],
                "answer": 1,
                "explain": "Every parameter and the whole body need parentheses, or precedence corrupts the expansion.",
            },
            {
                "type": "blank",
                "question": "The macro operator that turns an argument into a string literal is <code>____</code> (one symbol).",
                "answers": ["#", "stringize"],
                "explain": "#x inside a macro produces the literal spelling of the argument as a string.",
            },
            {
                "type": "mc",
                "question": "#ifdef DEBUG is true when:",
                "options": [
                    "DEBUG equals 1",
                    "DEBUG has been #defined at all (even as 0)",
                    "DEBUG is a variable",
                    "The program is compiled with -g",
                ],
                "answer": 1,
                "explain": "#ifdef only asks whether the name is defined; #if DEBUG additionally tests its value.",
            },
            {
                "type": "mc",
                "question": "What does the preprocessor know about C types?",
                "options": ["Everything — it type-checks macros", "Nothing — it only manipulates text", "Only int and float", "Whatever headers define"],
                "answer": 1,
                "explain": "The preprocessor is a text tool; the compiler that runs afterwards sees only the pasted result.",
            },
        ],
    },

    # ------------------------------------------------------------------ c09
    {
        "id": "c09",
        "title": "Low-Level C",
        "emoji": "🔬",
        "lessons": [
            {
                "title": "Bitwise Operations",
                "html": """
<p>C lets you work on the individual bits of an integer — the toolset of
drivers, protocols, packing and flags:</p>

<ul>
<li><code>&amp;</code> AND — 1 only where <i>both</i> bits are 1</li>
<li><code>|</code> OR — 1 where <i>either</i> bit is 1</li>
<li><code>^</code> XOR — 1 where bits <i>differ</i></li>
<li><code>~</code> NOT — flips every bit</li>
<li><code>&lt;&lt;</code> shift left — <code>x &lt;&lt; n</code> is
<code>x * 2^n</code> (for unsigned)</li>
<li><code>&gt;&gt;</code> shift right — <code>x &gt;&gt; n</code> is
<code>x / 2^n</code> (for unsigned)</li>
</ul>

<pre class="code">int a = 12;          // binary 1100
int b = 10;          // binary 1010

printf("%d\\n", a &amp; b);   // 8    (1000)
printf("%d\\n", a | b);   // 14   (1110)
printf("%d\\n", a ^ b);   // 6    (0110)
printf("%d\\n", a &lt;&lt; 2);  // 48   (110000)
printf("%d\\n", a &gt;&gt; 2);  // 3    (11)</pre>

<p>The everyday patterns:</p>

<pre class="code">flags |= 0x04;           // set bit 2
flags &amp;= ~0x04;          // clear bit 2
if (flags &amp; 0x04) ...    // test bit 2
x &amp;= 0xFF;               // keep only the low byte</pre>

<p>Bite-sized tricks worth knowing: <code>x &amp; 1</code> tests odd/even,
<code>x &gt;&gt; 1</code> halves, and XOR-ing twice with the same value
restores the original. Shift counts must be less than the width —
<code>x &lt;&lt; 32</code> on an int is undefined.</p>
""",
                "tryit": """#include <stdio.h>

int main(void) {
    int a = 12, b = 10;   /* 1100, 1010 */
    printf("a & b  = %d\\n", a & b);
    printf("a | b  = %d\\n", a | b);
    printf("a ^ b  = %d\\n", a ^ b);
    printf("~a     = %d\\n", ~a);
    printf("a << 2 = %d\\n", a << 2);
    printf("a >> 2 = %d\\n", a >> 2);

    unsigned flags = 0;
    flags |= 0x04;                  // set bit 2
    printf("bit2 set? %d\\n", (flags & 0x04) != 0);
    flags &= ~0x04;                 // clear bit 2
    printf("bit2 set? %d\\n", (flags & 0x04) != 0);
    return 0;
}
""",
            },
            {
                "title": "Function Pointers",
                "html": """
<p>Functions live in memory too, and a <b>function pointer</b> stores a
function's address — letting you pass behaviour around like data:</p>

<pre class="code">int add(int a, int b) { return a + b; }
int mul(int a, int b) { return a * b; }

int (*op)(int, int) = add;    // pointer named op
printf("%d\\n", op(3, 4));     // 7 — call through it
op = mul;
printf("%d\\n", op(3, 4));     // 12</pre>

<p>Read the declaration inside-out: <code>op</code> is a pointer to a
function taking two ints and returning int. The parentheses around
<code>*op</code> are mandatory — without them it declares a function
returning a pointer.</p>

<p>The killer application: <b>callbacks</b>. <code>qsort</code> sorts any
type by asking <i>you</i> for the comparison function:</p>

<pre class="code">#include &lt;stdlib.h&gt;

int cmp(const void *a, const void *b) {
    return *(const int *)b - *(const int *)a;   // descending
}

int v[] = {5, 1, 9, 3, 7};
qsort(v, 5, sizeof(int), cmp);   // pass the function itself</pre>

<p>Arrays of function pointers make dispatch tables — a clean
replacement for long switch statements:</p>

<pre class="code">int (*ops[2])(int, int) = {add, mul};
printf("%d\\n", ops[choice](6, 7));</pre>

<p>Tip: typedef the type once and the code reads normally —
<code>typedef int (*op_fn)(int, int);</code></p>
""",
                "tryit": """#include <stdio.h>
#include <stdlib.h>

int add(int a, int b) { return a + b; }
int mul(int a, int b) { return a * b; }

int cmp_desc(const void *a, const void *b) {
    return *(const int *)b - *(const int *)a;
}

int main(void) {
    int (*op)(int, int) = add;
    printf("op(3,4) = %d\\n", op(3, 4));
    op = mul;
    printf("op(3,4) = %d\\n", op(3, 4));

    int v[] = {5, 1, 9, 3, 7};
    qsort(v, 5, sizeof(int), cmp_desc);
    for (int i = 0; i < 5; i++) printf("%d ", v[i]);
    printf("\\n");
    return 0;
}
""",
            },
            {
                "title": "Pointer-to-Pointer",
                "html": """
<p>A pointer is itself a variable, so it has an address — which another
pointer can store. That is a <b>pointer to a pointer</b>:</p>

<pre class="code">int x = 5;
int *p = &amp;x;
int **pp = &amp;p;

printf("%d\\n", **pp);   // 5 — dereference twice
**pp = 7;               // changes x, two levels deep</pre>

<p>Picture the chain: <code>pp</code> holds the address of
<code>p</code>, which holds the address of <code>x</code>.</p>

<p>The practical use is <b>out-parameters that return pointers</b> — a
function that allocates and hands the new pointer back:</p>

<pre class="code">int make_array(int n, int **out) {
    *out = malloc(n * sizeof(int));    // write into the caller's pointer
    return *out != NULL;
}

int main(void) {
    int *data;
    if (make_array(5, &amp;data)) {
        data[0] = 1;
        free(data);
    }
}</pre>

<p>Pointer-to-pointer is also the natural type of <b>argv</b> —
<code>char *argv[]</code> is an array of string pointers, i.e. a
<code>char **</code> — and of two-dimensional dynamic grids. Each extra
<code>*</code> adds one level of "follow this arrow first":</p>

<pre class="code">char *names[] = {"Ada", "Grace", NULL};
char **p = names;
printf("%s\\n", p[0]);    // Ada</pre>
""",
                "tryit": """#include <stdio.h>
#include <stdlib.h>

int make_array(int n, int **out) {
    *out = malloc(n * sizeof(int));
    return *out != 0;
}

int main(void) {
    int x = 5;
    int *p = &x;
    int **pp = &p;
    printf("**pp = %d\\n", **pp);
    **pp = 7;
    printf("x is now %d\\n", x);

    int *data;
    if (make_array(3, &data)) {
        data[2] = 9;
        printf("data[2] = %d\\n", data[2]);
        free(data);
    }
    return 0;
}
""",
            },
            {
                "title": "Bit Fields",
                "html": """
<p>Struct members can be declared with a <b>bit width</b> — a bit field.
The compiler packs neighbouring fields into the bits of their storage
unit:</p>

<pre class="code">struct flags {
    unsigned int visible : 1;   // 1 bit  — 0 or 1
    unsigned int kind    : 3;   // 3 bits — 0..7
    unsigned int level   : 5;   // 5 bits — 0..31
};

struct flags f = {1, 5, 19};
printf("%u %u %u\\n", f.visible, f.kind, f.level);
printf("sizeof = %zu\\n", sizeof(struct flags));  // 4 — one int</pre>

<p>Three one-bit + three-bit + five-bit fields = 9 bits — all packed
into a single 32-bit <code>unsigned int</code>. Same data, quarter of
the naive space — handy for hardware registers, file formats and
millions of small records.</p>

<p>The rules and gotchas:</p>

<ul>
<li>Bit fields must be an integer type (<code>unsigned int</code> is the
portable choice; a plain <code>int</code> field can hold negative
values).</li>
<li>A field cannot exceed its type's width — 32 bits for
<code>int</code>.</li>
<li>Unnamed fields (<code>int : 3;</code>) insert padding;
zero-width (<code>int : 0;</code>) forces the next field onto a new
storage unit.</li>
<li><b>Layout is implementation-defined</b> — how bits flow across
bytes differs between compilers. Never dump bit-field structs straight
into a file format; pack bits yourself for that.</li>
<li>You cannot take the address of a bit field — it may not start on a
byte boundary.</li>
</ul>
""",
                "tryit": """#include <stdio.h>
#include <stddef.h>

struct flags {
    unsigned int visible : 1;
    unsigned int kind    : 3;
    unsigned int level   : 5;
};

int main(void) {
    struct flags f = {1, 5, 19};
    printf("%u %u %u\\n", f.visible, f.kind, f.level);
    printf("sizeof = %zu bytes\\n", sizeof(struct flags));

    f.kind = 7;      /* max for 3 bits */
    f.level = 31;    /* max for 5 bits */
    printf("maxed: %u %u\\n", f.kind, f.level);
    return 0;
}
""",
            },
            {
                "title": "Memory Layout",
                "html": """
<p>Where exactly do struct fields sit in memory? The compiler inserts
invisible <b>padding bytes</b> so that each field sits at its natural
<b>alignment</b> — the CPU reads aligned types faster (or at all):</p>

<pre class="code">struct S {
    char  c;    // offset 0
                // 3 bytes padding
    int   i;    // offset 4
    char  c2;   // offset 8
                // 3 bytes padding (struct size rounds up)
};
printf("%zu\\n", sizeof(struct S));   // 12 — not 6!</pre>

<p>The rules: each field's offset is rounded up to a multiple of its
alignment (int → 4, double → 8, pointers → 8), and the struct's total
size rounds up to its largest alignment so arrays of the struct stay
aligned.</p>

<p>You can measure layout precisely with <code>offsetof</code> from
<code>&lt;stddef.h&gt;</code>:</p>

<pre class="code">#include &lt;stddef.h&gt;
printf("%zu %zu\\n", offsetof(struct S, i), offsetof(struct S, c2));</pre>

<p>Ordering fields from largest to smallest keeps padding minimal:</p>

<pre class="code">struct good { double d; int i; char c; };    // 16 bytes
struct bad  { char c; double d; int i; };    // 24 bytes — same data!</pre>

<p>And remember from the Data Structures chapter: <code>union</code> puts
every field at offset 0, and bit fields pack sub-byte fields together.
The sandbox implements exactly this little-endian, naturally-aligned
model — so the lessons you run here reflect a real 64-bit machine.</p>
""",
                "tryit": """#include <stdio.h>
#include <stddef.h>

struct S { char c; int i; char c2; };
struct T { double d; int i; char c; };
struct U { char c; double d; int i; };

int main(void) {
    printf("S: size=%zu i@%zu c2@%zu\\n",
           sizeof(struct S), offsetof(struct S, i), offsetof(struct S, c2));
    printf("T (ordered):  %zu bytes\\n", sizeof(struct T));
    printf("U (unordered): %zu bytes\\n", sizeof(struct U));
    return 0;
}
""",
            },
        ],
        "quiz": [
            {
                "type": "mc",
                "question": "If a = 12 (binary 1100) and b = 10 (binary 1010), what is a & b?",
                "options": ["14", "8", "6", "120"],
                "answer": 1,
                "explain": "AND keeps only bits set in both: 1100 & 1010 = 1000 = 8.",
            },
            {
                "type": "codefill",
                "question": "Set bit 2 of flags (counting from 0):",
                "code": [
                    "flags ", { "blank": "|=", "answers": ["|=", "|= "] },
                    " 0x04;",
                ],
                "explain": "flags |= 0x04 turns bit 2 on; flags &= ~0x04 turns it off.",
            },
            {
                "type": "mc",
                "question": "What does qsort's 4th argument take?",
                "options": [
                    "The sort direction",
                    "A function pointer to a comparison function",
                    "The array's type",
                    "A struct describing the sort",
                ],
                "answer": 1,
                "explain": "qsort calls your comparison function through a function pointer to decide the order.",
            },
            {
                "type": "mc",
                "question": "struct flags { unsigned a:1; unsigned b:3; }; — sizeof is typically:",
                "options": ["1 byte", "2 bytes", "4 bytes", "8 bytes"],
                "answer": 2,
                "explain": "Both fields pack into one 32-bit unsigned int storage unit.",
            },
            {
                "type": "blank",
                "question": "The macro that gives a struct field's byte offset is <code>____</code>.",
                "answers": ["offsetof", "offsetof()"],
                "explain": "offsetof(struct S, field) from <stddef.h> returns the field's byte offset.",
            },
        ],
    },
]
