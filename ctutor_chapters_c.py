"""C Tutor chapters 10-13, distilled from Beej's Guide to C Programming."""

CHAPTERS_CT_C = [
    # ------------------------------------------------------------------ c10
    {
        "id": "c10",
        "title": "Advanced C",
        "emoji": "🎓",
        "lessons": [
            {
                "title": "VLA",
                "html": """
<p>A <b>variable-length array</b> (VLA) is an array whose size is
computed at runtime — allocated on the stack when the declaration
executes:</p>

<p>Why does this matter? User input decides buffer sizes constantly — reading
n numbers, building a matrix of given dimensions. Before C99 you reached for
<code>malloc</code> even when the array only needed to live for one function
call.</p>

<pre class="code">int n = 4;
int arr[n];                 // a VLA — size from a variable
for (int i = 0; i &lt; n; i++) arr[i] = i * 3;

printf("%zu\\n", sizeof(arr));   // 16 — sizeof works at runtime too</pre>

<p><code>sizeof(arr)</code> runs at runtime too and answers 16 — four ints.
The array disappears when the block ends: no <code>free</code>, no leak, no
NULL check.</p>

<p>Before C99 this was impossible: array sizes had to be constants, and
runtime-sized memory meant <code>malloc</code>. VLAs are perfect for
small, short-lived buffers — no <code>malloc</code>/<code>free</code>
pair to forget.</p>

<p>They also shine as function parameters, letting you write
two-dimensional matrices with real dimensions:</p>

<pre class="code">void print_matrix(int rows, int cols, int m[rows][cols]) {
    for (int r = 0; r &lt; rows; r++) {
        for (int c = 0; c &lt; cols; c++) printf("%d ", m[r][c]);
        printf("\\n");
    }
}</pre>

<p>The parameter list reads: <code>rows</code> and <code>cols</code> are
declared first, then used as the dimensions of <code>m</code>. C99 lets a
parameter borrow earlier parameters — the same function now works for any
matrix.</p>

<p>The caveats Beej emphasises:</p>

<ul>
<li>A VLA lives on the stack — a very large <code>n</code> can blow the
stack (no NULL check to save you here).</li>
<li>VLAs cannot be initialised with <code>{...}</code> at declaration.</li>
<li><code>goto</code> that jumps <i>over</i> a VLA declaration is not
allowed; longjmp out of a function with VLAs is dicey.</li>
<li>C11 made VLAs optional — real compilers may need a flag to enable
them.</li>
</ul>

<p>Rule of thumb: VLA for small, routine-sized buffers (a few KB at most);
<code>malloc</code> the moment the size can be big or must outlive the
function. And never write <code>int arr[n]</code> without bounding
<code>n</code> first.</p>
""",
                "tryit": """#include <stdio.h>

// VLA parameters CAN be 2-D (int m[rows][cols]) on a real compiler,
// but this sandbox limits them to one dimension -- so flatten:
void print_flat(int rows, int cols, int *m) {
    for (int r = 0; r < rows; r++) {
        for (int c = 0; c < cols; c++) printf("%d ", m[r * cols + c]);
        printf("\\n");
    }
}

int main(void) {
    int n = 4;
    int arr[n];                      // a 1-D VLA -- size from a variable
    for (int i = 0; i < n; i++) arr[i] = i * 3;
    printf("sizeof(arr) = %zu\\n", sizeof(arr));

    int flat[6] = {1, 2, 3, 4, 5, 6};
    print_flat(2, 3, flat);          // the same bytes, viewed as 2x3
    return 0;
}
""",
            },
            {
                "title": "Compound Literals",
                "html": """
<p>A <b>compound literal</b> creates an unnamed object on the fly —
cast-like syntax followed by an initializer list:</p>

<p>Think of it as inline object construction: the value is written exactly
where it is used, which keeps call sites tight and temporaries
nameless.</p>

<pre class="code">struct point { double x, y; };

draw((struct point){3.0, 9.0});   // pass a struct without a variable

int *a = (int[]){7, 8, 9};        // an unnamed array
printf("%d\\n", a[2]);             // 9</pre>

<p>Walk it: <code>(struct point){3.0, 9.0}</code> builds a real struct value
with x=3 and y=9 and hands it to <code>draw</code> — no named variable ever
exists. The second line makes an anonymous three-int array and points
<code>a</code> at it.</p>

<p>Before C99 you had to build a named temporary for every such value.
Compound literals are handy for:</p>

<ul>
<li><b>Passing "constructor" values</b> straight into a call</li>
<li><b>Array initialisation through a pointer</b> — the literal lives as
long as its enclosing block</li>
<li><b>Updating structs in one expression:</b></li>
</ul>

<pre class="code">p = (struct point){.x = 1.0, .y = 2.0};   // compound literal with designators</pre>

<p>Designators (<code>.x =</code>, <code>.y =</code>) name the fields being
set, so order no longer matters and unmentioned fields become zero.</p>

<p>Unlike a cast, a compound literal is a real object — you can take its
address (<code>&amp;(struct point){0, 0}</code>) and its fields can be
modified. Its lifetime follows the enclosing block: at file scope it
lives for the whole program; inside a function, until the block ends.</p>

<p>Gotcha: a pointer to a block-scope compound literal dangles once the block
ends — the same rules as a local variable. Never return
<code>&amp;(struct point){0, 0}</code> from the function that created it.</p>

<p>The pointer form <code>(int[]){...}</code> is how many C programs
build small lookup tables right where they are used.</p>
""",
                "tryit": """#include <stdio.h>

struct point { double x, y; };

void show(struct point p) { printf("(%.1f, %.1f)\\n", p.x, p.y); }

int main(void) {
    show((struct point){3.0, 9.0});

    int *a = (int[]){7, 8, 9};
    printf("%d %d %d\\n", a[0], a[1], a[2]);

    struct point p = {0, 0};
    p = (struct point){1.5, 2.5};
    show(p);
    return 0;
}
""",
            },
            {
                "title": "Generic Selections",
                "html": """
<p><b>Generic selections</b> (<code>_Generic</code>, C11) pick an
expression based on a value's <i>type</i> — compile-time overloading for
macros:</p>

<p>Why? Because C macros are type-blind: <code>ABS(x)</code> calling
<code>abs(x)</code> works for int and breaks for double. <code>_Generic</code>
lets one macro name dispatch to the right expression per type — without
generating any code of its own.</p>

<pre class="code">#define TYPENAME(x) _Generic((x), \\
    int: "int", \\
    double: "double", \\
    char *: "char *", \\
    default: "other")

printf("%s\\n", TYPENAME(42));      // int
printf("%s\\n", TYPENAME(3.14));    // double</pre>

<p><code>TYPENAME(42)</code> sees an int and becomes <code>"int"</code>;
<code>TYPENAME(3.14)</code> sees a double. Only the matching expression is
used — the rest is discarded at compile time.</p>

<p>How to read it: <code>_Generic(control, type1: expr1, type2: expr2,
...)</code> — the compiler looks at the control expression's type and
substitutes the matching expression. Exactly one branch is chosen; the
others are not evaluated. <code>default:</code> catches everything
else.</p>

<p>The classic use is <b>type-generic macros</b> — one name, correct
behaviour per type, like the <code>cbrt</code>/<code>cbrtf</code>
family unified:</p>

<pre class="code">#define ABS(x) _Generic((x), \\
    int: abs(x), \\
    long: labs(x), \\
    double: fabs(x), \\
    default: (x))

printf("%d %g\\n", ABS(-5), ABS(-2.5));</pre>

<p><code>ABS(-5)</code> expands to <code>abs(-5)</code>;
<code>ABS(-2.5)</code> to <code>fabs(-2.5)</code>. One macro name, two
different library calls — chosen by type, before compilation.</p>

<p>Compare with C++ overloading: <code>_Generic</code> selects an
expression at compile time inside a macro — no functions are generated,
and C stays C. The control expression itself is not evaluated, only its
type inspected.</p>

<p>Gotcha: <code>_Generic</code> matches exact types after lvalue conversion —
<code>char</code> and <code>short</code> promote to <code>int</code>, so list
them under int. And every type you might receive needs a branch or a
<code>default:</code>, or the program is ill-formed.</p>
""",
                "tryit": """#include <stdio.h>
#include <stdlib.h>
#include <math.h>

#define TYPENAME(x) _Generic((x), \
    int: "int", \
    double: "double", \
    char *: "char *", \
    default: "other")

#define ABS(x) _Generic((x), \
    int: abs(x), \
    double: fabs(x), \
    default: (x))

int main(void) {
    int i = 42;
    double d = 3.14;
    char *s = "text";
    printf("%s %s %s\\n", TYPENAME(i), TYPENAME(d), TYPENAME(s));
    printf("ABS(-5)=%d ABS(-2.5)=%g\\n", ABS(-5), ABS(-2.5));
    return 0;
}
""",
            },
            {
                "title": "Incomplete Types",
                "html": """
<p>A type is <b>incomplete</b> when the compiler knows its name but not
its size or layout. You get one by declaring a struct without a
body:</p>

<p>Why would you want an incomplete type on purpose? Two reasons: to break
circular references between types, and to hide implementation details —
both are daily tools in real C projects.</p>

<pre class="code">struct widget;          // incomplete: forward declaration
struct widget *w;       // fine — all POINTERS have the same size
// struct widget w;     // error: incomplete type!</pre>

<p>Line 1 announces the name; line 2 succeeds because a pointer's size is
known no matter what it points at; line 3 fails because a struct variable
needs a real size.</p>

<p>You can always use pointers to an incomplete type; you just cannot
create one, dereference it, or take its size — until the type is
completed later with its full definition.</p>

<p>The most famous use: <b>self-referential structures</b> — linked
lists, trees:</p>

<pre class="code">struct node {
    int value;
    struct node *next;    // pointer to own (still incomplete) type
};</pre>

<p>The definition is still being read at the moment <code>next</code> is
declared — the struct is incomplete right there. The pointer does not
care.</p>

<p>Inside its own definition, <code>struct node</code> is incomplete —
but a pointer to it is fine, which is all <code>next</code> needs.</p>

<p>The second big use is <b>opaque types</b> — information hiding across
files. A public header declares the type and functions; the private
<code>.c</code> file completes it. Callers can hold and pass pointers
but can never touch the internals directly:</p>

<pre class="code">// stack.h
typedef struct stack stack;          // incomplete on purpose
stack *stack_new(void);
void   stack_push(stack *s, int v);

// users only ever handle stack* — implementation stays private</pre>

<p>The FILE* type from stdio.h works exactly this way: you hold it, you
pass it, but you never open it up.</p>

<p>Gotcha: with opaque types every access must go through your API — callers
will inevitably try <code>sizeof</code> and field access, and each attempt is
a compile error doing exactly its job.</p>
""",
            },
            {
                "title": "goto",
                "html": """
<p><code>goto</code> jumps to a labelled statement anywhere in the same
function:</p>

<pre class="code">while (read(&amp;row)) {
    for (int i = 0; i &lt; 10; i++) {
        if (error_at(i)) goto cleanup;   // jump out of BOTH loops
    }
}
cleanup:
free_resources();</pre>

<p>Read the jump: <code>error_at(i)</code> fires deep inside two nested loops,
and <code>cleanup</code> runs immediately — a <code>break</code> could only
have left the inner loop.</p>

<p>Beej's guide is refreshingly honest about goto: it is both infamous
and genuinely useful — the problem is <i>unstructured</i> jumps, not the
keyword itself. Modern C style blesses exactly these patterns:</p>

<ul>
<li><b>Multi-level cleanup / error handling</b> — the snippet above:
breaking out of nested loops straight to the cleanup code. This is
ubiquitous in the Linux kernel.</li>
<li><b>Retry loops</b> — jumping back to try an operation again.</li>
<li><b>Labeled break/continue</b> — C lacks them; goto provides them.</li>
</ul>

<pre class="code">restart:
    result = try_operation();
    if (result == RETRY_ME) goto restart;</pre>

<p>Retry loops read the same way: jump back to the label and try again. Keep
the retry condition explicit, or the loop can spin forever.</p>

<p>The rules: you can jump within a function, but not over a VLA
declaration, and jumping into a scope past initialisation leaves
variables in an iffy state. Keep jumps <b>forward</b> and downward to
cleanup, and the code stays readable:</p>

<p>Gotcha: never jump backwards into a loop body, and never jump over an
initialisation you then rely on — the variable exists but holds nothing
sensible.</p>

<pre class="code">FILE *f = fopen(path, "r");
if (!f) goto fail;
char *buf = malloc(size);
if (!buf) goto close_file;
/* ... work ... */
close_file:
    fclose(f);
fail:
    return err;</pre>

<p>Walk the chain: <code>malloc</code> fails, so we jump to
<code>close_file</code>, which closes f and falls through to
<code>fail</code> — each label cleans up only what has actually succeeded so
far. That discipline is the kernel's error-handling style.</p>
""",
                "tryit": """#include <stdio.h>
#include <stdlib.h>

int main(void) {
    int *p = malloc(10 * sizeof(int));
    if (p == 0) return 1;

    for (int i = 0; i < 10; i++) {
        if (i == 4) goto cleanup;   /* pretend an error happened */
        p[i] = i;
    }
    printf("not reached\\n");

cleanup:
    printf("bailing out early (i reached 4)\\n");
    free(p);
    return 0;
}
""",
            },
            {
                "title": "setjmp / longjmp",
                "html": """
<p><code>setjmp</code> and <code>longjmp</code> (from
<code>&lt;setjmp.h&gt;</code>) perform a <b>non-local jump</b>: from deep
inside nested calls, straight back to an earlier point — C's way to
escape N levels of functions at once, like an exception without
exceptions:</p>

<pre class="code">#include &lt;setjmp.h&gt;

jmp_buf env;

void deep(int n) {
    if (n == 0) longjmp(env, 42);   // jump back to setjmp!
    deep(n - 1);
}

int main(void) {
    int r = setjmp(env);            // returns 0 first time...
    if (r == 0) {
        deep(5);                    // ...42 after the longjmp
    } else {
        printf("jumped %d\\n", r);
    }
}</pre>

<p>The output is "jumped 42": <code>deep(0)</code> triggers the longjmp, five
call frames vanish in one step, and main's <code>setjmp</code> returns
again — this time with 42 instead of 0.</p>

<p><code>setjmp(env)</code> marks the spot and returns 0. Any later
<code>longjmp(env, val)</code> unwinds back to that spot, and
<code>setjmp</code> then returns <code>val</code> — which is why the
code always checks the return value to tell the two visits apart.</p>

<p>The pitfalls Beej devotes a section to:</p>

<ul>
<li>Non-volatile locals modified after <code>setjmp</code> may come back
with stale values after the jump — make them <code>volatile</code> if
you need their current values.</li>
<li>Never <code>longjmp</code> from a signal handler, or with a
<code>jmp_buf</code> whose <code>setjmp</code> function has already
returned — the jump target is gone.</li>
<li>Anything the jumped-over frames should have freed... doesn't get
freed. Cleanup is your problem (often handled by jumping to a cleanup
block, like goto).</li>
</ul>

<p>Where you will meet it: implementers of interpreters, exception
libraries, and coroutine frameworks.</p>

<p>The volatile rule comes from the abstract machine: after a longjmp, locals
without <code>volatile</code> have indeterminate values — the compiler was
free to keep them only in registers.</p>

<p>Rule of thumb: setjmp/longjmp is a framework author's tool, not an
application tool. In ordinary code, return codes plus <code>goto</code>
cleanup say the same thing and stay readable.</p>
""",
                "tryit": """#include <stdio.h>
#include <setjmp.h>

jmp_buf env;

void deep(int n) {
    if (n == 0) longjmp(env, 42);
    deep(n - 1);
}

int main(void) {
    int r = setjmp(env);
    if (r == 0) {
        printf("calling deep(5)...\\n");
        deep(5);
        printf("not reached\\n");
    } else {
        printf("jumped back with %d\\n", r);
    }
    return 0;
}
""",
            },
        ],
        "quiz": [
            {
                "type": "mc",
                "question": "Where does a VLA allocate its memory?",
                "options": ["The heap (like malloc)", "The stack, at declaration time", "Global memory", "It depends on the optimizer"],
                "answer": 1,
                "explain": "A VLA is stack-allocated when its declaration executes — no malloc/free needed, but stack overflow is possible.",
            },
            {
                "type": "mc",
                "question": "What does _Generic select on?",
                "options": ["The value of the expression", "The TYPE of the expression, at compile time", "The return of a function", "A runtime string"],
                "answer": 1,
                "explain": "_Generic inspects the control expression's type and substitutes the matching expression — compile-time selection.",
            },
            {
                "type": "mc",
                "question": "Why is struct node { int v; struct node *next; }; legal while node is being defined?",
                "options": [
                    "next is only a pointer, and pointers to an incomplete type are fine",
                    "structs are always complete",
                    "next is optional",
                    "It is not legal",
                ],
                "explain": "Inside its own definition the struct is incomplete — but a pointer to an incomplete type has known size.",
                "answer": 0,
            },
            {
                "type": "mc",
                "question": "The blessed modern use of goto is:",
                "options": [
                    "Jumping backwards to build loops",
                    "Forward jumps to cleanup/error-handling code",
                    "Replacing all for loops",
                    "Jumping between functions",
                ],
                "answer": 1,
                "explain": "Forward goto to a cleanup label — e.g. escaping nested loops to free resources — is idiomatic and common (the kernel uses it everywhere).",
            },
            {
                "type": "mc",
                "question": "After longjmp(env, 42), what does the original setjmp(env) return?",
                "options": ["0 again", "42", "-1", "It does not return"],
                "answer": 1,
                "explain": "setjmp returns 0 the first time and the longjmp value on the jump back — that is how the code tells the two visits apart.",
            },
        ],
    },

    # ------------------------------------------------------------------ c11
    {
        "id": "c11",
        "title": "System-Level Programming",
        "emoji": "🖥️",
        "lessons": [
            {
                "title": "Command Line",
                "html": """
<p><code>main</code> can take parameters — the <b>command line</b> your
program was launched with:</p>

<p>Why does this matter? Almost every serious tool takes arguments — file
names, flags, sizes. <code>argv</code> is your first and most important
interface with the person running your program.</p>

<pre class="code">int main(int argc, char *argv[]) {
    printf("program: %s\\n", argv[0]);   // the program's own name
    for (int i = 1; i &lt; argc; i++) {
        printf("arg %d: %s\\n", i, argv[i]);
    }
    return 0;
}</pre>

<p>For <code>./app hello 42</code> the loop prints <code>arg 1: hello</code>
and <code>arg 2: 42</code> — user arguments start at index 1, because
<code>argv[0]</code> holds the program name.</p>

<ul>
<li><code>argc</code> — argument <b>count</b>: how many strings, including
the program name itself.</li>
<li><code>argv</code> — the arguments as an array of strings.
<code>argv[0]</code> is the program name, <code>argv[argc]</code> is
guaranteed to be <code>NULL</code> — which lets you loop with
<code>while (*argv++)</code> instead of counting.</li>
</ul>
<p>argc is always at least 1 — even with no arguments, <code>argv[0]</code>
names the program.</p>

<p>Running <code>./app hello 42</code> gives
<code>argc = 3</code>, <code>argv = {"./app", "hello", "42"}</code>.
Note everything arrives as <b>strings</b> — convert with
<code>atoi</code>/<code>strtol</code>:</p>

<p><code>argv[1]</code> is the string <code>"42"</code>; <code>atoi</code>
turns it into the number 42 and squaring works. Had the user typed
<code>abc</code>, <code>atoi</code> would quietly return 0 —
<code>strtol</code> is the version that lets you detect and report
that.</p>

<pre class="code">if (argc &gt; 1) {
    int n = atoi(argv[1]);
    printf("n squared: %d\\n", n * n);
}</pre>

<p>Real programs check <code>argc</code> first and print a usage message
when the user got it wrong — the first defensive habit of system
programming.</p>

<p>Gotcha: never index argv beyond argc — there is no bounds checking.
<code>argv[argc]</code> being NULL is safe to <i>test</i>, fatal to print
with <code>%s</code>.</p>
""",
            },
            {
                "title": "Environment Variables",
                "html": """
<p>Every process inherits a set of <b>environment variables</b> —
<code>PATH</code>, <code>HOME</code>, <code>LANG</code> and friends,
set by the shell or the parent process:</p>

<p>Why care? Programs find their configuration through this channel — which
editor to launch, where the home directory is, which language to speak.
Reading it is the same in every C program.</p>

<pre class="code">#include &lt;stdlib.h&gt;

char *home = getenv("HOME");
if (home != NULL) {
    printf("home is %s\\n", home);
}</pre>

<p>If HOME is set, <code>home</code> points at a string like
<code>/home/ada</code>; if not, you get NULL — so the check is not
optional.</p>

<p><code>getenv</code> returns a pointer to the variable's value, or
<code>NULL</code> if it is not set — always check before using. The
returned string belongs to the environment: do not modify or free it,
and copy it if you plan to keep it around.</p>

<p>The whole environment is also handed to <code>main</code> as a third
parameter on most systems:</p>

<pre class="code">int main(int argc, char *argv[], char *envp[]) {
    for (char **e = envp; *e != NULL; e++) {
        printf("%s\\n", *e);      // "KEY=value" strings
    }
}</pre>

<p>Each entry is a <code>KEY=value</code> string; the array ends at a NULL
pointer, which is exactly what the loop tests.</p>

<p>Setting variables <i>for your own children</i> is done with
<code>setenv("NAME", "value", 1)</code> (or the simpler
<code>putenv</code>) — changes only affect processes you spawn, never
the shell that launched you.</p>

<p>Gotcha: the result of <code>getenv</code> can go stale if
<code>setenv</code> runs later — copy anything you plan to keep. Rules of
thumb: read the environment once at startup, treat everything in it as
untrusted input (the user controls it), and prefer command-line arguments
for anything the program cannot run without.</p>

<p>The browser sandbox in this course has no real environment —
<code>getenv</code> there returns NULL for most names, which is itself
a lesson: the environment is an operating-system feature, not a
language feature.</p>
""",
            },
            {
                "title": "Exit Handling",
                "html": """
<p>A program can end in more ways than falling off the end of
<code>main</code>:</p>

<ul>
<li><code>return n;</code> from main — the normal exit; the value goes
to the operating system (0 = success)</li>
<li><code>exit(n);</code> — end now, from anywhere; runs cleanup
handlers and flushes stdio</li>
<li><code>atexit(fn);</code> — register a function to run automatically
at exit (in reverse registration order)</li>
<li><code>quick_exit(n);</code> — a quicker exit: runs only
<code>at_quick_exit</code> handlers, no stdio flush</li>
<li><code>_Exit(n);</code> — the sledgehammer: stop immediately, run
<i>nothing</i></li>
<li><code>abort();</code> — abnormal termination (this is what a failed
<code>assert</code> does)</li>
</ul>

<p>The list is a politeness spectrum: <code>return</code> and
<code>exit</code> run their handlers and flush stdio;
<code>quick_exit</code> skips the flushing; <code>_Exit</code> and
<code>abort</code> skip everything.</p>

<pre class="code">#include &lt;stdlib.h&gt;

void save_state(void) { printf("saving...\\n"); }

int main(void) {
    atexit(save_state);
    printf("running\\n");
    exit(0);            // prints "saving..." then exits
}</pre>

<p>The output is <code>running</code> then <code>saving...</code> —
<code>exit(0)</code> runs the registered handler before stopping. Register
three handlers and they run last-registered-first, stack order, so cleanup
mirrors construction.</p>

<p>Exit status conventions: <code>EXIT_SUCCESS</code> (0) and
<code>EXIT_FAILURE</code> (usually 1) from <code>&lt;stdlib.h&gt;</code>
— scripts and other programs use these to judge your result.</p>

<p>For debugging, <code>assert(cond)</code> from
<code>&lt;assert.h&gt;</code> prints the failed expression, file and
line, then aborts — a runtime sanity check you can disable in release
builds by defining <code>NDEBUG</code>:</p>

<pre class="code">assert(divisor != 0);   // screams if violated</pre>

<p>Gotchas: never put required work inside an <code>assert</code> expression —
with NDEBUG defined the whole call vanishes, and the work with it. And
calling <code>exit</code> from inside an atexit handler is undefined.</p>
""",
            },
            {
                "title": "Signals",
                "html": """
<p>A <b>signal</b> is the operating system interrupting your program
asynchronously: Ctrl-C sends <code>SIGINT</code>, division by zero may
raise <code>SIGFPE</code>, kill sends <code>SIGTERM</code>, and so
on.</p>

<p>Why care? Graceful shutdown is signal handling: a server catches SIGTERM
to flush state, an editor restores the terminal after Ctrl-C. Programs that
ignore signals get killed mid-write.</p>

<pre class="code">#include &lt;signal.h&gt;

void on_interrupt(int sig) {
    printf("got signal %d\\n", sig);
    // keep it tiny: set a flag and return
}

signal(SIGINT, on_interrupt);   // install the handler</pre>

<p>From this line on, Ctrl-C no longer kills the program — it calls
<code>on_interrupt</code> instead. That is both the power and the
danger.</p>

<p><code>signal(sig, handler)</code> registers a function to run when
that signal arrives. What handlers may safely do is severely limited —
Beej's chapter title says it plainly: <i>"Friends Don't Let Friends
signal()"</i>. A handler runs at an arbitrary moment, so the safe moves
are: set a volatile flag and return, or call only the tiny list of
async-signal-safe functions.</p>

<pre class="code">volatile sig_atomic_t got_signal = 0;

void handler(int sig) {
    got_signal = sig;      // just note it
}

int main(void) {
    signal(SIGINT, handler);
    while (!got_signal) {
        /* work; the flag turns true between iterations */
    }
}</pre>

<p>The handler writes the signal number into <code>got_signal</code> and
returns immediately. The main loop notices between iterations and exits
cleanly — no library calls from inside the handler, nothing racy.</p>

<p>The default behaviour for most signals terminates the program. You
can also ignore a signal (<code>signal(SIGINT, SIG_IGN)</code>) or
restore the default (<code>SIG_DFL</code>). Real signals need an
operating system to deliver them — the browser sandbox cannot generate
them, so this chapter's lesson code runs on a real machine, not here.</p>

<p>Rule of thumb: a handler should do nothing but set a
<code>sig_atomic_t</code> flag. <code>printf</code> inside a handler can
deadlock the very stream it interrupted — that is why the flag pattern above
exists.</p>
""",
            },
        ],
        "quiz": [
            {
                "type": "mc",
                "question": "For ./app hello 42, what is argv[0]?",
                "options": ["hello", "42", "./app", "argc"],
                "answer": 2,
                "explain": "argv[0] is the program's own name; user arguments start at argv[1].",
            },
            {
                "type": "mc",
                "question": "getenv returns NULL when:",
                "options": ["The value is empty", "The variable is not set", "The variable is longer than 1024 chars", "Never"],
                "answer": 1,
                "explain": "No such variable means NULL — check before dereferencing.",
            },
            {
                "type": "mc",
                "question": "Functions registered with atexit() run:",
                "options": [
                    "In registration order when exit() is called",
                    "In reverse registration order at exit",
                    "Immediately when registered",
                    "Never — atexit is broken",
                ],
                "answer": 1,
                "explain": "exit() runs atexit handlers in reverse registration order (last registered, first run), then flushes stdio.",
            },
            {
                "type": "blank",
                "question": "Ctrl-C at the terminal sends the signal <code>____</code>.",
                "answers": ["sigint", "SIGINT"],
                "explain": "SIGINT — 'signal interrupt'. SIGTERM is what kill sends by default; SIGFPE comes from bad arithmetic.",
            },
        ],
    },

    # ------------------------------------------------------------------ c12
    {
        "id": "c12",
        "title": "Text & Internationalization",
        "emoji": "🌐",
        "lessons": [
            {
                "title": "Unicode",
                "html": """
<p><b>Unicode</b> assigns every character in every language a number — a
<b>code point</b>, conventionally written U+XXXX: 'A' is U+0041, the
snowman ☃ is U+2603. What Unicode does <i>not</i> define is how those
numbers become bytes — that is <b>encoding</b>, and C's relationship
with it is... historical.</p>

<p>The core vocabulary:</p>

<ul>
<li><b>Code point</b> — a number from 0 to 0x10FFFF</li>
<li><b>Encoding</b> — the byte recipe for a code point: UTF-8, UTF-16,
UTF-32</li>
<li><b>Glyph</b> — what the user sees on screen</li>
</ul>

<p>One glyph can even need several code points — accents can be separate
combining marks — which is why "character count" is not always one
number.</p>

<p>C's plain <code>char</code> holds <i>bytes</i>, not characters. A
string like <code>"héllo"</code> in a UTF-8 file really contains the
bytes <code>68 C3 A9 6C 6C 6F 00</code> — <code>é</code> is
<i>two</i> bytes. C functions like <code>strlen</code> count bytes, so
<code>strlen("héllo")</code> is 6, not 5.</p>

<p>Decode that example byte by byte: <code>h</code> is 68, <code>é</code> is
the pair C3 A9, then 6C 6C 6F and the terminator — six bytes, five
characters. Every "character" question in C is really two questions: bytes
or code points?</p>

<p>The good news: <b>UTF-8 is byte-transparent</b> — bytes that belong
together never contain bytes that look like ASCII, and the NUL
terminator never appears inside a character. So plain C string handling
passes UTF-8 through safely; only counting, slicing and case-folding
need encoding awareness.</p>

<p>Modern C adds real character types — <code>char16_t</code>,
<code>char32_t</code> (from <code>&lt;uchar.h&gt;</code>) — plus
<code>u"..."</code>, <code>U"..."</code> and <code>u8"..."</code> string
literals that promise specific encodings.</p>

<p>Rule of thumb: keep your source files UTF-8, treat every string as bytes,
and decode only when you must count, slice, or fold case.</p>
""",
            },
            {
                "title": "UTF-8",
                "html": """
<p><b>UTF-8</b> is the encoding that won the world (the web is >98%
of it). Its scheme:</p>

<ul>
<li>U+0000–U+007F → <b>1 byte</b>: <code>0xxxxxxx</code> — identical to
ASCII</li>
<li>U+0080–U+07FF → <b>2 bytes</b>: <code>110xxxxx 10xxxxxx</code></li>
<li>U+0800–U+FFFF → <b>3 bytes</b>: <code>1110xxxx 10xxxxxx 10xxxxxx</code></li>
<li>U+10000+ → <b>4 bytes</b>: <code>11110xxx 10... 10... 10...</code></li>
</ul>

<p>Every continuation byte starts with <code>10</code>, and no lead byte
ever does. Consequences worth internalising:</p>

<ul>
<li><b>Self-synchronising:</b> given any random byte you can tell if it
starts a character; scanning backwards finds character boundaries.</li>
<li><b>ASCII-compatible:</b> old ASCII files and code are valid UTF-8;
<code>strcmp</code>, <code>printf("%s")</code>, and file handling all
pass UTF-8 through untouched.</li>
<li><b>No endianness:</b> one byte order everywhere.</li>
</ul>

<p>Working with UTF-8 in C means decoding by hand or via helpers. A
minimal code-point decoder walks the lead byte to learn the length:</p>

<pre class="code">int utf8_len(unsigned char b) {
    if (b &lt; 0x80) return 1;          // 0xxxxxxx
    if ((b &amp; 0xE0) == 0xC0) return 2; // 110xxxxx
    if ((b &amp; 0xF0) == 0xE0) return 3; // 1110xxxx
    if ((b &amp; 0xF8) == 0xF0) return 4; // 11110xxx
    return 1;                         // stray byte — skip
}</pre>

<p>Test it: <code>'A'</code> is 0x41, under 0x80, so 1 byte.
<code>'é'</code> starts with 0xC3, which matches the 0xC0 mask, so 2 bytes.
A stray 0xFF matches no mask and is skipped.</p>

<p>Always validate: truncated sequences and overlong encodings are how
attackers sneak bytes past naive parsers (Beej devotes a section to
this; the fix is to decode rather than trust).</p>

<p>Two rules to keep: <code>strlen</code> gives bytes — right for memory, wrong
for display; decide which you need before writing the loop. And never trust
user-supplied bytes as UTF-8 without validating — one bad sequence and your
downstream counting splits characters.</p>
""",
            },
            {
                "title": "Wide Characters",
                "html": """
<p>Before UTF-8 took over, C's answer to big character sets was
<b>wide characters</b>: one fixed-size unit per character.</p>

<ul>
<li><code>wchar_t</code> — from <code>&lt;wchar.h&gt;</code>; 16 or 32
bits depending on the platform (not portable!)</li>
<li><code>char16_t</code> / <code>char32_t</code> — exact-width types
from <code>&lt;uchar.h&gt;</code> (C11): UTF-16 and UTF-32 units</li>
</ul>

<p>Each has its own literal prefix and its own parallel library:</p>

<pre class="code">wchar_t *ws = L"wide";
char16_t *u16 = u"utf-16";
char32_t *u32 = U"utf-32";   // one code point per unit — easy indexing

wprintf(L"wide: %ls\\n", ws);      // note %ls for wide strings
size_t n = wcslen(ws);            // wcs* mirrors str*</pre>

<p>The prefixes: <code>L</code> makes a wide literal, <code>u</code> UTF-16 and
<code>U</code> UTF-32. And note <code>%ls</code> — printing a wide string with
plain <code>%s</code> is a bug the compiler usually warns about.</p>

<p>The wide world in one table: <code>strlen→wcslen</code>,
<code>strcpy→wcscpy</code>, <code>strcmp→wcscmp</code>,
<code>printf→wprintf</code>, <code>scanf→wscanf</code>. UTF-32 strings
even give O(1) indexing — each element is one code point.</p>

<p>The <code>wcs*</code> functions mirror the <code>str*</code> ones one for
one, so the habits transfer — the units change, not the patterns.</p>

<p>The trade-offs Beej points out: wide strings double or quadruple
memory, <code>wchar_t</code>'s size is platform-dependent (16 bits on
Windows, 32 on Linux), and I/O streams have an <b>orientation</b> —
after the first wide or byte operation, the stream sticks to that
side until reopened. That is why mixing <code>printf</code> and
<code>wprintf</code> on the same stream misbehaves.</p>

<p>Modern consensus: store and transmit UTF-8 in plain
<code>char</code> strings; use <code>char32_t</code> when you need to
<i>compute</i> on individual code points.</p>

<p>Gotcha: switching a stream's orientation by accident is the classic
wide-char bug — pick byte or wide for each stream near program start and
stay there.</p>
""",
            },
            {
                "title": "Locale",
                "html": """
<p>Programs around the world differ in small ways: is the decimal
separator <code>3.14</code> or <code>3,14</code>? What is the currency
symbol? Which order do names print in? C models this with
<b>locales</b> from <code>&lt;locale.h&gt;</code>:</p>

<pre class="code">#include &lt;locale.h&gt;

setlocale(LC_ALL, "");     // adopt the user's environment settings
setlocale(LC_ALL, "C");    // the default minimal locale
setlocale(LC_ALL, NULL);   // just query the current one</pre>

<p>Empty string adopts the user's environment; <code>"C"</code> resets to the
minimal default; NULL only asks. <code>setlocale</code> returns the new (or
current) locale's name, or NULL on failure.</p>

<p>Categories can be switched individually:</p>

<ul>
<li><code>LC_ALL</code> — everything</li>
<li><code>LC_NUMERIC</code> — decimal point in printf/scanf</li>
<li><code>LC_TIME</code> — names of days and months in strftime</li>
<li><code>LC_MONETARY</code> — currency formatting</li>
<li><code>LC_CTYPE</code> — what counts as a letter for
<code>isalpha</code> etc.</li>
</ul>

<p>By default a C program runs in the <code>"C"</code> locale —
periods for decimals, ASCII letters only — <i>regardless</i> of the
user's country. That is why <code>printf("%.1f", 3.14)</code> prints
<code>3.1</code> until you call <code>setlocale</code>.</p>

<p>The <code>localeconv()</code> function returns a struct of formatting
facts — decimal point, thousands separator, currency symbol:</p>

<pre class="code">struct lconv *lc = localeconv();
printf("decimal point: '%s'\\n", lc-&gt;decimal_point);</pre>

<p>In the <code>"C"</code> locale that prints a period; on a German machine it
would print a comma — the whole point of the exercise.</p>

<p>Locale-aware code is a contract with your users; locale-unaware code
is a bug report waiting to happen. (The sandbox here stays in the
"C" locale — real machines are where <code>""</code> comes alive.)</p>

<p>Gotcha: call <code>setlocale(LC_ALL, "")</code> early in <code>main</code>
or not at all — switching locale mid-program changes printf output and
parsing both, a nasty trap for file readers.</p>
""",
                "tryit": """#include <stdio.h>
#include <locale.h>
#include <time.h>

int main(void) {
    printf("current locale: %s\\n", setlocale(LC_ALL, NULL));

    struct lconv *lc = localeconv();
    printf("decimal point: '%s'\\n", lc->decimal_point);

    struct tm tm = {0};
    tm.tm_year = 126; tm.tm_mon = 8; tm.tm_mday = 27;
    char buf[64];
    strftime(buf, sizeof buf, "%Y-%m-%d (%a)", &tm);
    printf("formatted: %s\\n", buf);
    return 0;
}
""",
            },
        ],
        "quiz": [
            {
                "type": "mc",
                "question": "strlen(\"héllo\") in a UTF-8 file returns 6, because:",
                "options": [
                    "strlen is buggy",
                    "é is stored as 2 bytes and strlen counts bytes",
                    "strings are counted differently in C",
                    "It returns 5",
                ],
                "answer": 1,
                "explain": "strlen counts bytes; é takes 2 bytes in UTF-8, so 6 total. Characters vs bytes!",
            },
            {
                "type": "mc",
                "question": "Why did UTF-8 win over UTF-16/32 for storage and transmission?",
                "options": [
                    "It is newer",
                    "ASCII-compatible, self-synchronising, no endianness, compact for Latin text",
                    "It is the only one C supports",
                    "It encodes every char in one byte",
                ],
                "answer": 1,
                "explain": "UTF-8 keeps ASCII programs working, resyncs from any byte, and has a single byte order.",
            },
            {
                "type": "mc",
                "question": "The literal L\"wide\" creates:",
                "options": ["A long integer", "A wide (wchar_t) string", "A lowercase string", "A locale"],
                "answer": 1,
                "explain": "The L prefix makes a wchar_t string, paired with wprintf/wcs* functions and %ls.",
            },
            {
                "type": "blank",
                "question": "By default (before any setlocale call) a C program runs in the <code>____</code> locale.",
                "answers": ["c", "\"c\""],
                "explain": "The \"C\" locale: period decimals, ASCII letters only — regardless of the user's country.",
            },
        ],
    },

    # ------------------------------------------------------------------ c13
    {
        "id": "c13",
        "title": "Modern / Advanced C",
        "emoji": "⚛️",
        "lessons": [
            {
                "title": "Complex Numbers",
                "html": """
<p>C has native <b>complex numbers</b> (C99) via
<code>&lt;complex.h&gt;</code>. The keyword <code>_Complex</code> builds
a complex type out of any floating-point type, and <code>complex</code>
is a friendlier macro for it:</p>

<p>Why native complex? Because computing z1 * z2 by hand with separate real
and imaginary parts is exactly the error-prone bookkeeping the compiler can
do for you.</p>

<pre class="code">#include &lt;complex.h&gt;
#include &lt;stdio.h&gt;

double complex z = 3.0 + 4.0 * I;    // 3 + 4i

printf("re=%g im=%g\\n", creal(z), cimag(z));   // parts
printf("|z|=%g\\n", cabs(z));                   // magnitude = 5</pre>

<p><code>z</code> holds two doubles: real 3, imaginary 4. <code>creal</code>
and <code>cimag</code> read the parts back, and <code>cabs</code> computes
sqrt(9+16) = 5 — the magnitude Pythagoras promises.</p>

<p>The <code>I</code> constant is the imaginary unit. Arithmetic is
native — the operators just work:</p>

<pre class="code">double complex a = 1.0 + 2.0 * I;
double complex b = 3.0 - 1.0 * I;

double complex sum = a + b;        // 4 + 1i
double complex prod = a * b;       // 5 + 5i — (1+2i)(3-1i)
printf("prod = %g + %gi\\n", creal(prod), cimag(prod));</pre>

<p>Check the product by hand: (1+2i)(3-1i) = 3 - 1i + 6i - 2i² = 5 + 5i. The
operators do the algebra; you just read the result.</p>

<p>The math library comes along: <code>cexp</code>, <code>clog</code>,
<code>csqrt</code>, <code>csin</code>, <code>cpow</code> — complex
versions of every transcendental function, plus
<code>conj(z)</code> (conjugate) and <code>carg(z)</code> (angle).</p>

<p>Under the hood a complex number is just two doubles — the imaginary
part stored after the real one — so passing and returning them is as
cheap as a two-element struct. Electrical engineering, signal
processing and fractal renderers are the classic customers.</p>

<p>Gotchas: complex works with floating types only — there is no complex int.
And <code>I</code> is a macro from the header, so a variable named I in your
own code is asking for trouble.</p>
""",
            },
            {
                "title": "Date & Time",
                "html": """
<p>C's time toolbox lives in <code>&lt;time.h&gt;</code> and is built on
two representations:</p>

<ul>
<li><code>time_t</code> — a single number: seconds since the epoch
(Jan 1 1970, UTC) — compact, easy to compare and store</li>
<li><code>struct tm</code> — a human calendar: seconds, minutes, hours,
day, month, year (year − 1900!), weekday and more</li>
</ul>

<p>Why two forms? <code>time_t</code> is for storage and arithmetic — one
number, trivially compared. <code>struct tm</code> is for humans — named
fields. Real code converts between the two constantly.</p>

<pre class="code">#include &lt;time.h&gt;

time_t now = time(NULL);              // right now, in seconds
struct tm *lt = localtime(&amp;now);      // broken down, local time
struct tm *gt = gmtime(&amp;now);         // broken down, UTC

printf("year: %d\\n", lt-&gt;tm_year + 1900);
printf("month: %d\\n", lt-&gt;tm_mon + 1);    // months are 0-11!</pre>

<p>Both functions take a pointer to <code>time_t</code> and return a pointer
to an internal struct — the <i>next</i> call overwrites it, so copy it if
you need localtime and gmtime at the same time.</p>

<p>Conversions run both ways: <code>localtime</code>/<code>gmtime</code>
turn a <code>time_t</code> into a <code>struct tm</code>;
<code>mktime</code> turns a <code>struct tm</code> back into a
<code>time_t</code> (also normalising out-of-range fields — a neat
date-arithmetic trick). <code>difftime</code> measures the seconds
between two <code>time_t</code>s.</p>

<p>Formatting is <code>strftime</code> — printf for dates:</p>

<pre class="code">char buf[64];
strftime(buf, sizeof buf, "%Y-%m-%d %H:%M (%a)", lt);
printf("%s\\n", buf);     // 2026-09-27 14:05 (Sun)</pre>

<p>For sub-second precision, <code>timespec_get(&amp;ts, TIME_UTC)</code>
fills a <code>struct timespec</code> with seconds
<strong>and</strong> nanoseconds; <code>clock()</code> measures
processor time used by the program — the classic stopwatch for
benchmarking a loop.</p>

<p>Gotchas worth tattooing: <code>tm_year</code> counts from 1900 and
<code>tm_mon</code> from 0 — the two classic off-by-constants bugs, both
visible in the tryit example. And <code>mktime</code>'s normalising makes
date arithmetic easy: stuff today+90 days into a struct roughly, and
<code>mktime</code> lands you on the real calendar date.</p>
""",
                "tryit": """#include <stdio.h>
#include <time.h>

int main(void) {
    time_t epoch = 86400;                      /* Jan 2 1970, 00:00 UTC */
    struct tm *gt = gmtime(&epoch);
    printf("epoch+1day: %04d-%02d-%02d %02d:%02d:%02d UTC\\n",
           gt->tm_year + 1900, gt->tm_mon + 1, gt->tm_mday,
           gt->tm_hour, gt->tm_min, gt->tm_sec);

    struct tm tm = {0};
    tm.tm_year = 126; tm.tm_mon = 8; tm.tm_mday = 27;
    char buf[64];
    strftime(buf, sizeof buf, "%Y-%m-%d (%a)", &tm);
    printf("formatted: %s\\n", buf);

    time_t a = 1000000, b = 2000000;
    printf("difference: %.0f seconds\\n", difftime(b, a));
    return 0;
}
""",
            },
            {
                "title": "Multithreading",
                "html": """
<p>C11 added an optional standard thread library,
<code>&lt;threads.h&gt;</code> — the concepts matter even where the
header is missing (POSIX <code>pthread</code> is the classic
alternative with the same shapes).</p>

<p>Why threads? One core per heavy task: one thread decodes video while
another serves the network and a third repaints the UI. Threads are how one
process does several things at once.</p>

<pre class="code">#include &lt;threads.h&gt;

int worker(void *arg) {
    int id = *(int *)arg;
    printf("thread %d running\\n", id);
    return 0;
}

thrd_t t;
thrd_create(&amp;t, worker, &amp;some_arg);   // start
thrd_join(t, NULL);                   // wait for it</pre>

<p><code>thrd_create</code> starts <code>worker</code> and returns
immediately — two streams of execution now share the process's memory.
<code>thrd_join</code> blocks until the thread finishes, collecting its
return code, like a join in Python or Rust.</p>

<p>The mental model: each thread runs the given function concurrently
with the rest of the program, sharing the same global memory. That
sharing is the whole problem:</p>

<ul>
<li><b>Data races:</b> two threads writing the same variable at once —
undefined behaviour. The fix is <b>mutexes</b>:
<code>mtx_lock(&amp;m)</code> / <code>mtx_unlock(&amp;m)</code> around
every touch of shared data.</li>
<li><b>Condition variables</b> (<code>cnd_wait</code>/
<code>cnd_signal</code>) let threads sleep until something worth doing
appears, instead of spinning.</li>
<li><code>_Thread_local</code> gives each thread its own private copy of
a global.</li>
<li><code>thrd_detach</code> lets a thread be fire-and-forget; threads
return an <code>int</code> code collected by <code>thrd_join</code>.</li>
</ul>

<p>Beej's chapter builds up to the rule that rules them all: identify
the shared data, and guard every access. The browser sandbox is
single-threaded by design — threads are a real-operating-system
feature — so this chapter is reading, not running.</p>

<p>Gotcha: passing <code>&amp;local_variable</code> to a thread that outlives
the block is the classic race — the thread reads dead stack. Allocate or
copy whatever the thread needs to own.</p>
""",
            },
            {
                "title": "Atomics",
                "html": """
<p>When threads share data, the cheapest safe tool is an
<b>atomic</b> variable (C11, <code>&lt;stdatomic.h&gt;</code>) —
operations on it are indivisible: no thread can ever see a half-done
update.</p>

<pre class="code">#include &lt;stdatomic.h&gt;

atomic_int counter = 0;

// on each thread, safely:
counter++;                    // atomic read-modify-write
int now = atomic_load(&amp;counter);
atomic_store(&amp;counter, 5);</pre>

<p>Why not just <code>counter++</code> on a plain int? Because
<code>++</code> is three steps — read, add, write — and two threads can
interleave them, losing increments. Atomics make the whole sequence
one unbreakable step.</p>

<p>The toolbox:</p>

<ul>
<li><code>atomic_load</code> / <code>atomic_store</code> /
<code>atomic_exchange</code> — the basics</li>
<li><code>atomic_fetch_add</code> / <code>atomic_fetch_or</code> ... —
atomic arithmetic returning the old value</li>
<li><code>atomic_compare_exchange_weak/strong</code> — "if it still
holds the old value, swap in the new one" — the foundation of
lock-free algorithms</li>
<li><code>atomic_flag</code> — the minimal guaranteed lock-free type,
usable to build a spinlock</li>
<li>memory orders (<code>memory_order_acquire</code>,
<code>release</code>, <code>relaxed</code>...) — controlling how
visible writes are to other threads; the default
<code>seq_cst</code> is the safe choice</li>
</ul>

<p>The rule of thumb from Beej's chapter: reach for a mutex first — it
is easier to reason about. Atomics are for hot counters, flags and
lock-free data structures where the mutex's cost actually shows up.
Like threads, atomics need real hardware — the sandbox simulates
single-threaded execution, so this chapter runs nowhere but in your
imagination (for now!).</p>
""",
            },
        ],
        "quiz": [
            {
                "type": "mc",
                "question": "A complex number is stored as:",
                "options": ["A string like \"3+4i\"", "Two floating-point values (real, then imaginary)", "A pointer to math.h data", "Three values: magnitude, angle, and type"],
                "answer": 1,
                "explain": "double complex is literally two doubles back to back — creal and cimag read them out.",
            },
            {
                "type": "mc",
                "question": "struct tm's tm_mon counts months starting from:",
                "options": ["0 (January = 0)", "1 (January = 1)", "-1", "It stores a string"],
                "answer": 0,
                "explain": "tm_mon is 0-based (add 1 for humans); tm_year is years since 1900 — the two classic traps.",
            },
            {
                "type": "mc",
                "question": "Two threads run counter++ on a plain int 100 times each. The result can be:",
                "options": ["Always exactly 200", "Less than 200 — updates can interleave and be lost", "More than 200", "Undefined compile error"],
                "answer": 1,
                "explain": "counter++ is read-modify-write; interleaving loses updates. atomic_int (or a mutex) fixes it.",
            },
            {
                "type": "mc",
                "question": "The recommended first tool for protecting shared data between threads is:",
                "options": ["A mutex (mtx_lock/mtx_unlock)", "volatile", "goto", "getchar()"],
                "answer": 0,
                "explain": "Mutexes are easiest to reason about; atomics come second for hot paths. volatile does NOT make operations atomic.",
            },
        ],
    },
]
