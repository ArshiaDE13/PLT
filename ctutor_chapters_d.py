"""C Tutor chapters 14-15: undefined behavior / the memory model and the
modern standards (C11 -> C23), completing the 12-stage roadmap."""

CHAPTERS_CT_D = [
    # ------------------------------------------------------------------ c14
    {
        "id": "c14",
        "title": "Undefined Behavior & the Memory Model",
        "emoji": "🧨",
        "lessons": [
            {
                "title": "Undefined Behavior",
                "html": """
<p>The C standard defines some programs' behavior not as "an error
message" but as <b>undefined</b> — anything at all may happen. This is
not sloppiness: it is the price of C's speed. If the standard had to
define what happens on every mistake, every compiler would have to check
for those mistakes at runtime, and C would stop being C.</p>

<pre class="code">int arr[4];
arr[10] = 1;             // out of bounds: undefined
int x;                   
printf("%d\\n", x);       // reading an uninitialized value: undefined
int big = 2147483647;
big = big + 1;           // signed overflow: undefined
free(p); free(p);        // double free: undefined
*p = 5;                  // writing through NULL: undefined</pre>

<p>Beginners expect undefined behavior to <i>crash</i>. It often does not.
The standard's real rule is: <b>once your program does something
undefined, the compiler may assume it never happens</b> — and optimize
accordingly. A check like <code>if (p != NULL)</code> can be deleted
because "p was already dereferenced, so it can't be NULL". An overflow
check can be removed because "signed overflow never happens". The
notorious joke is that UB gives the compiler a license to make <a>nasal
demons</a> fly out of your nose — the point being: the outcome is not
merely weird, it is <i>unbounded</i>.</p>

<p>Note what the sandbox does with the try-it below: it <i>wraps</i>
INT_MAX to INT_MIN, because this interpreter defines the result. A real
compiler at <code>-O2</code> is allowed to do anything at all — delete
the check, assume the value is positive, or trap. Same source, different
behavior: that is exactly what "undefined" means.</p>

<p>Your defenses:</p>

<ul>
<li>Compile with warnings: <code>-Wall -Wextra</code> — many UB sources
are caught before you run anything.</li>
<li>Run sanitizers: <code>-fsanitize=address,undefined</code> turns UB
into a loud runtime report (the sandbox does something similar for out
of bounds memory).</li>
<li>Treat every red flag in this lesson as a bug, not a "it works on my
machine" pass.</li>
</ul>
""",
                "tryit": """#include <stdio.h>
#include <limits.h>

int main(void) {
    int big = INT_MAX;
    big = big + 1;
    printf("INT_MAX + 1 = %d\\n", big);
    printf("(the sandbox defines this as a wrap; real -O2 builds\\n");
    printf(" may do ANYTHING - signed overflow is undefined)\\n");
    return 0;
}
""",
            },
            {
                "title": "Unspecified & Implementation-Defined",
                "html": """
<p>Two gentler cousins of "undefined" appear on real projects, and the
roadmap wants you to tell all three apart:</p>

<ul>
<li><b>Unspecified</b> — the standard lists the allowed outcomes but
does not pick one, and your program must work with any of them. Example:
the order in which function arguments are evaluated is unspecified:
<code>f(i++, i++)</code> is a classic trap (and two unsequenced changes
to <code>i</code> tip it into undefined).</li>
<li><b>Implementation-defined</b> — like unspecified, but the compiler
vendor must <i>document</i> the choice. Example: how many bits
<code>int</code> has (16? 32? 64? — read your compiler's docs), whether
plain <code>char</code> is signed, and what <code>malloc(0)</code>
returns.</li>
<li><b>Undefined</b> — no constraints at all. Anything may happen,
including nothing wrong today and disaster after the next compiler
update.</li>
</ul>

<p>The sandbox's char is signed, so the try-it below prints "signed". On
a platform where plain char is unsigned it would print "unsigned" — both
compilers are correct, because the standard leaves this
implementation-defined. Portable code never relies on the choice: use
<code>signed char</code> or <code>unsigned char</code> explicitly when
the sign matters.</p>

<p>Practical habits: never write <code>f(i++, i++)</code>-style calls;
check <code>sizeof(int)</code> and friends instead of assuming; when you
need exact widths, use <code>&lt;stdint.h&gt;</code> types like
<code>int32_t</code>.</p>
""",
                "tryit": """#include <stdio.h>
#include <stddef.h>

int main(void) {
    printf("sizeof(int) = %zu bytes\\n", sizeof(int));
    char c = -1;
    printf("plain char is %s here\\n", c < 0 ? "signed" : "unsigned");
    printf("(the other answer is legal too - it is\\n");
    printf(" implementation-defined!)\\n");
    return 0;
}
""",
            },
            {
                "title": "Integer Overflow, Promotions & Signed/Unsigned",
                "html": """
<p>Two numeric rules cause most real-world integer bugs:</p>

<p><b>1. Unsigned arithmetic wraps; signed arithmetic overflows (and
that is undefined).</b> <code>unsigned int</code> arithmetic is defined
modulo 2<sup>32</sup>: <code>UINT_MAX + 1</code> is exactly 0. But
<code>INT_MAX + 1</code> is undefined — see the first lesson of this
chapter.</p>

<p><b>2. Small types promote to int.</b> In almost every expression,
<code>char</code> and <code>short</code> are first promoted to
<code>int</code> before any arithmetic happens. Consequences:</p>

<pre class="code">unsigned char a = 200, b = 100;
unsigned char sum = a + b;      // 300 wraps to 44 — promotion happened
printf("%d\\n", a + b);          // prints 300! the int result is not wrapped</pre>

<p>And the nastiest trap of all: when a <b>signed</b> value meets an
<b>unsigned</b> one in a comparison or operation, the signed side is
<i>converted to unsigned</i> first:</p>

<pre class="code">int x = -1;
unsigned u = 1;
if (x &lt; u) ...   // FALSE! -1 becomes 4294967295, which is not &lt; 1</pre>

<p>The try-it below prints exactly that surprise. This is why the
roadmap insists on understanding signed vs unsigned: comparing a length
returned as <code>-1</code> against an unsigned size silently passes.
Habit to keep: don't mix the two in one expression, and treat
<code>size_t</code> values as unsigned (they are).</p>
""",
                "tryit": """#include <stdio.h>

int main(void) {
    int x = -1;
    unsigned u = 1;

    if (x < u)
        printf("x < u: yes\\n");
    else
        printf("x < u: NO (-1 became 4294967295!)\\n");

    unsigned char a = 200, b = 100;
    printf("a + b as int   = %d\\n", a + b);
    printf("a + b as uchar = %d\\n", (unsigned char)(a + b));
    return 0;
}
""",
            },
            {
                "title": "Aliasing, Alignment & Object Representation",
                "html": """
<p>Three low-level ideas finish the "really understand C" list.</p>

<p><b>Object representation.</b> A value is not just its number — every
object is <code>sizeof(T)</code> bytes of memory, possibly including
<b>padding</b> bytes that hold no value at all. Two structs can compare
their members equal byte-for-byte yet differ in padding, which is why
you should never <code>memcmp</code> structs for equality and why
<code>= {0}</code> and assignment are not always byte-identical. Reading
padding bytes through a <code>char*</code> is legal; relying on their
content is not.</p>

<p><b>Strict aliasing.</b> The rule: you may only read an object's value
through a compatible type, and the one big exception is any
<code>char</code> type. Writing a <code>float</code>, then reading those
bytes through an <code>int*</code>, is undefined — the optimizer assumes
the two pointers cannot refer to the same memory and may reorder your
loads. Type punning must go through unions or <code>memcpy</code>:</p>

<pre class="code">float f = 1.0f;
int bad   = *(int *)&amp;f;                 // undefined (strict aliasing)
int good;
memcpy(&amp;good, &amp;f, sizeof good);         // defined: bytes are copied</pre>

<p><b>Alignment.</b> Every type has an alignment requirement: addresses
at which its objects may live. <code>alignof(T)</code> (C11) reports it,
<code>_Alignas</code> forces it, and the compiler inserts padding so
members line up — which is exactly what the <code>Memory Layout</code>
lesson measured with <code>offsetof</code>. malloc already returns
maximally-aligned memory, which is why you never call it a second time
"just to be aligned".</p>
""",
                "tryit": """#include <stdio.h>
#include <string.h>

int main(void) {
    float f = 1.0f;
    int via_memcpy;
    memcpy(&via_memcpy, &f, sizeof via_memcpy);
    printf("float 1.0f as bytes (memcpy, legal): %d\\n", via_memcpy);

    struct { char c; int i; } s;
    printf("sizeof struct = %zu (padding: %zu byte)\\n",
           sizeof s, sizeof s - 1 - sizeof(int));
    return 0;
}
""",
            },
        ],
        "quiz": [
            {
                "type": "mc",
                "question": "Which of these is <b>undefined</b> behavior?",
                "options": [
                    "UINT_MAX + 1u",
                    "INT_MAX + 1",
                    "Reading a documented sizeof(int) value",
                    "Calling malloc(0)",
                ],
                "answer": 1,
                "explain": "Unsigned wraparound is defined (modulo 2^32), but signed overflow is undefined — the compiler may assume it never happens.",
            },
            {
                "type": "mc",
                "question": "int x = -1; unsigned u = 1; What does x < u evaluate to?",
                "options": [
                    "1 (true) — normal integer comparison",
                    "0 (false) — x converts to a huge unsigned value first",
                    "Undefined behavior",
                    "Depends on sizeof(int) only",
                ],
                "answer": 1,
                "explain": "In a signed/unsigned comparison the signed side converts to unsigned: -1 becomes UINT_MAX, which is not less than 1.",
            },
            {
                "type": "mc",
                "question": "Why is *(int *)&f (reading a float through an int*) undefined?",
                "options": [
                    "Because floats are always 8 bytes",
                    "The strict aliasing rule — only compatible types (plus char) may access an object",
                    "Because &f is a NULL pointer",
                    "It is not undefined — memcpy is just faster",
                ],
                "answer": 1,
                "explain": "Strict aliasing lets the optimizer assume incompatible pointers never refer to the same memory. Use a union or memcpy for type punning.",
            },
            {
                "type": "blank",
                "question": "The standard leaves whether plain char is signed <code>____</code> — the compiler must document its choice, and portable code should not rely on it.",
                "answers": ["implementation-defined", "implementation defined"],
                "explain": "Implementation-defined behavior is a documented compiler choice; unspecified means any of the allowed outcomes; undefined means no rules at all.",
            },
        ],
    },

    # ------------------------------------------------------------------ c15
    {
        "id": "c15",
        "title": "Modern Standards: C11 → C23",
        "emoji": "📜",
        "lessons": [
            {
                "title": "C11 & C17",
                "html": """
<p><b>C11</b> (2011) brought C into the multi-core era and added the
tools you have already met in the deep chapters:</p>

<ul>
<li><b>Threads</b>: <code>&lt;threads.h&gt;</code> with
<code>thrd_create</code>/<code>thrd_join</code> (optional — see the
Multithreading lesson) and <b>atomics</b>:
<code>&lt;stdatomic.h&gt;</code>.</li>
<li><b>Type-generic math and code</b>: <code>_Generic</code> — the
selector you built expressions with in Advanced C.</li>
<li><b>Compile-time assertions</b>: <code>_Static_assert(cond, "msg")</code>
fails the build, not the run.</li>
<li><b>Thread-local storage</b>: <code>_Thread_local</code> gives every
thread its own copy of a variable.</li>
<li><b>Anonymous structs/unions</b> inside other structs — accessed
without a member name.</li>
<li><b>Alignment</b> made official: <code>alignof</code> /
<code>_Alignas</code>; VLAs became optional; <code>gets</code> was
removed from the standard for good.</li>
</ul>

<p><b>C17</b> (2017) is a <i>bug-fix</i> release: no new features at all
— its job was to keep C11 implementable and consistent. If you hear "we
use C17", it means C11 with defects resolved.</p>

<p>C23 then landed the big modernization — that is the next lesson.</p>
""",
            },
            {
                "title": "C23 Language Features",
                "html": """
<p><b>C23</b> (technically ISO/IEC 9899:2024) is the biggest change to
C's surface in over a decade. The highlights the roadmap calls out:</p>

<ul>
<li><b>nullptr</b> — a real null pointer constant of type
<code>nullptr_t</code>, finally distinct from the integer 0 (and from
<code>(void*)0</code>).</li>
<li><b>bool, true, false are keywords</b> — no
<code>&lt;stdbool.h&gt;</code> needed anymore.</li>
<li><b>typeof / typeof_unqual</b> — declare a variable with the type of
an expression: <code>typeof(x) y = x * 2;</code>. The unqual form strips
const/volatile.</li>
<li><b>constexpr</b> for objects — declare constants the compiler
verifies are computable at translation time.</li>
<li><b>auto</b> — type inference, like C++: <code>auto n = 42;</code>
makes n an int.</li>
<li><b>Binary literals and digit separators</b>:
<code>0b1010_1010</code> — the underscore groups digits in any
literal.</li>
<li><b>Attributes</b>: <code>[[deprecated]]</code>, <code>[[nodiscard]]</code>,
<code>[[maybe_unused]]</code>, <code>[[fallthrough]]</code>,
<code>[[noreturn]]</code> — machine-readable hints in the source.</li>
<li><b>Declarations got friendlier</b>: labels can precede declarations
(and statements), <code>= {}</code> empty-initializes, and
<code>static_assert</code> works without the underscore.</li>
<li><b>_BitInt(N)</b> — integer types with an exact width, even beyond
64 bits.</li>
<li><b>unreachable()</b> — promise the optimizer a spot never executes
(undefined if you lie!).</li>
</ul>

<p>The sandbox interpreter runs classic C — it understands
<code>NULL</code> but not C23's <code>nullptr</code> — so this lesson's
listings are for reading, not running. Real compilers (GCC 13+, Clang 15+,
MSVC 19.30+) accept most of this with <code>-std=c2x</code>/<code>-std=c23</code>.</p>
""",
            },
            {
                "title": "C23 Preprocessor & Library",
                "html": """
<p><b>The preprocessor</b> gained tools that remove old boilerplate:</p>

<ul>
<li><b>#embed</b> — drop a binary file's bytes straight into the source
at compile time (icons, fonts, tables) without 10 000-line byte
arrays.</li>
<li><b>#elifdef / #elifndef</b> — the long-missing else-if for
<code>#ifdef</code> chains.</li>
<li><b>#warning</b> — a formal, non-fatal warning directive.</li>
<li><b>__has_include</b> and <b>__has_c_attribute</b> — ask the
preprocessor whether a header or attribute exists before using it.</li>
</ul>

<p><b>The library</b> grew in two directions the roadmap names:</p>

<ul>
<li><b>&lt;stdbit.h&gt;</b> — bit manipulation as functions, not tricks:
<code>stdc_count_ones</code> (popcount), <code>stdc_leading_zeros</code>,
<code>bit_ceil</code>, <code>stdc_bit_floor</code> and friends, generic
over unsigned integer types.</li>
<li><b>&lt;stdckdint.h&gt;</b> — <b>checked integer arithmetic</b>:
<code>bool ckd_add(r, a, b)</code>, <code>ckd_sub</code>,
<code>ckd_mul</code> compute the exact result and return
<code>true</code> if it did not fit — the portable end of overflow
worries.</li>
</ul>

<p>C23 also <i>removed</i> things: K&amp;R-style function definitions
(the old parameter lists after the parentheses) and a few obsolete
traps. That is the pattern of a maturing standard: new tools in, proven
footguns out.</p>
""",
            },
            {
                "title": "The Standard Library Tour",
                "html": """
<p>The roadmap closes the basics with the headers you will touch in
almost every real program. You have used most of them in this course —
here is the whole map:</p>

<ul>
<li><b>&lt;stdio.h&gt;</b> — input/output: <code>printf</code>,
<code>scanf</code>, <code>fopen</code>/<code>fclose</code>,
<code>fread</code>/<code>fwrite</code>, <code>fseek</code>/<code>ftell</code>.</li>
<li><b>&lt;stdlib.h&gt;</b> — <code>malloc</code>/<code>calloc</code>/
<code>realloc</code>/<code>free</code>, <code>atoi</code>/<code>strtol</code>,
<code>qsort</code>, <code>rand</code>, <code>exit</code>.</li>
<li><b>&lt;string.h&gt;</b> — <code>strlen</code>, <code>strcpy</code>/
<code>strncpy</code>, <code>strcmp</code>, <code>strcat</code>,
<code>memcpy</code>, <code>memmove</code>, <code>strstr</code>.</li>
<li><b>&lt;math.h&gt;</b> — <code>sqrt</code>, <code>pow</code>,
<code>floor</code>/<code>ceil</code>, <code>sin</code>... plus
<code>isnan</code>/<code>isinf</code>.</li>
<li><b>&lt;ctype.h&gt;</b> — character classes: <code>isdigit</code>,
<code>isalpha</code>, <code>toupper</code>, <code>tolower</code>.</li>
<li><b>&lt;time.h&gt;</b> — <code>time</code>, <code>clock</code>,
<code>localtime</code>, <code>strftime</code> (see the Date &amp; Time
lesson).</li>
<li><b>&lt;stdbool.h&gt;</b> — <code>bool</code>/<code>true</code>/
<code>false</code> before C23 made them keywords.</li>
<li><b>&lt;stdint.h&gt;</b> — exact-width integers: <code>int32_t</code>,
<code>uint64_t</code>, <code>INT32_MAX</code>... use these when width
matters.</li>
<li><b>&lt;stddef.h&gt;</b> — <code>size_t</code>, <code>NULL</code>,
<code>offsetof</code>.</li>
<li><b>&lt;limits.h&gt;</b> — the integer ranges: <code>INT_MAX</code>,
<code>CHAR_BIT</code>, <code>ULONG_MAX</code>...</li>
<li><b>&lt;float.h&gt;</b> — floating-point limits:
<code>DBL_MAX</code>, <code>FLT_DIG</code>, <code>DBL_EPSILON</code>.</li>
</ul>

<p>The try-it prints the honest numbers from your machine (well, the
sandbox's — they match a typical 64-bit build). Knowing where to look up
a limit is what keeps your code portable.</p>
""",
                "tryit": """#include <stdio.h>
#include <limits.h>
#include <float.h>

int main(void) {
    printf("CHAR_BIT = %d bits per byte\\n", CHAR_BIT);
    printf("INT_MAX  = %d\\n", INT_MAX);
    printf("ULONG_MAX= %lu\\n", ULONG_MAX);
    printf("DBL_DIG  = %d (digits of precision)\\n", DBL_DIG);
    return 0;
}
""",
            },
        ],
        "quiz": [
            {
                "type": "mc",
                "question": "What does C23's <code>nullptr</code> give you that <code>NULL</code> did not?",
                "options": [
                    "It is faster at runtime",
                    "A null pointer constant with its own type (nullptr_t), no longer an integer",
                    "It works in every C version",
                    "It automatically frees memory",
                ],
                "answer": 1,
                "explain": "nullptr has type nullptr_t and is a true pointer constant — no more surprises from NULL being the integer 0.",
            },
            {
                "type": "mc",
                "question": "Which header does C23 provide for checked integer arithmetic?",
                "options": ["<stdbit.h>", "<stdckdint.h>", "<limits.h>", "<inttypes.h>"],
                "answer": 1,
                "explain": "<stdckdint.h> offers ckd_add/ckd_sub/ckd_mul, which compute the exact result and report overflow with a bool.",
            },
            {
                "type": "blank",
                "question": "C23's <code>____</code> directive embeds a binary file's bytes directly into the program at compile time.",
                "answers": ["#embed", "embed"],
                "explain": "#embed replaces giant generated byte arrays: the compiler reads the file and inserts its bytes as data.",
            },
            {
                "type": "mc",
                "question": "What changed between C11 and C17?",
                "options": [
                    "C17 added threads to the core language",
                    "C17 removed _Generic",
                    "Nothing new — C17 is a defect-fix release of C11",
                    "C17 renamed _Static_assert",
                ],
                "answer": 2,
                "explain": "C17 is purely a bug-fix/consistency revision — all new language work landed in C23.",
            },
        ],
    },
]
