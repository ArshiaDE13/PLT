"""C++ Tutor chapters 33-44 (Error Handling through Professional C++)."""

CHAPTERS_CPP_E = [
    {
        "id": "cpp33",
        "title": "Error Handling",
        "emoji": "🚨",
        "lessons": [
            {
                "title": "Exceptions, noexcept & std::expected",
                "html": """
<p>C++ gives you two ways to report failure: <b>exceptions</b>, the
traditional mechanism, and <b>std::expected</b> (C++23), which returns
the error as a normal value. They solve the same problem — telling the
caller "this didn't work" — with very different mechanics. Exceptions
unwind the call stack until some caller chooses to handle the problem;
<code>expected</code> makes the error part of the return type, so no
caller can miss it:</p>

<pre class="code">// traditional exceptions
try {
    throw std::runtime_error("something failed");
} catch (const std::exception&amp; e) {
    std::cout &lt;&lt; e.what() &lt;&lt; "\\n";
}

// noexcept: promises this function won't throw
void fast_function() noexcept { /* no exceptions here */ }</pre>

<p>The <code>try</code> block wraps risky code; <code>throw</code>
exits it immediately, and control lands in
<code>catch (const std::exception&amp; e)</code> — catch by
<code>const&amp;</code> to avoid copying and to catch derived exception
types through the base class. <code>e.what()</code> then prints the
message <code>"something failed"</code>. Along the way from
<code>throw</code> to <code>catch</code>, every local object is
destroyed properly — that is stack unwinding.
<code>noexcept</code> is a promise, checked neither at compile time nor
at runtime: if an exception escapes a <code>noexcept</code> function
anyway, the program ends instantly with <code>std::terminate</code>.</p>

<p><b>std::expected&lt;int, std::string&gt;</b> (C++23) is a return
type that is either the value (<code>int</code>) or the error
(<code>std::string</code>). The error travels in the ordinary return
channel, so it is visible in the function signature:</p>

<pre class="code">std::expected&lt;int, std::string&gt; parse(std::string_view s) {
    auto result = /* parse */;
    if (result.has_value()) return result.value();
    return std::unexpected("parse failed");
}

auto result = parse("42");
if (result) std::cout &lt;&lt; result.value();
else std::cout &lt;&lt; result.error();</pre>

<p>Checking <code>if (result)</code> asks "did it succeed?"; then
<code>result.value()</code> yields <code>42</code> and
<code>result.error()</code> yields the message. Rule of thumb: throw
exceptions for truly exceptional, rare failures — out of memory, broken
invariants — and return <code>std::expected</code> (or
<code>std::optional</code>) for ordinary, anticipated outcomes like bad
input or "not found". Gotcha: calling <code>.value()</code> on an
expected that holds an error throws
<code>std::bad_expected_access</code> — check first, exactly as with
optional.</p>
""",
            },
        ],
        "quiz": [
            {"type": "mc", "question": "std::expected (C++23) represents:",
             "options": ["A future value", "Success with a value OR failure with an error", "An optional string", "A promise"],
             "answer": 1, "explain": "Expected = value or error, without exceptions."},
        ],
    },

    {
        "id": "cpp34",
        "title": "C++20/23 Ranges",
        "emoji": "🔄",
        "lessons": [
            {
                "title": "Ranges, Views & Pipelines",
                "html": """
<p><b>Ranges</b> (C++20) modernize how you talk to algorithms in two
ways. First, algorithms accept the container directly:
<code>std::ranges::sort(v)</code> instead of
<code>std::sort(v.begin(), v.end())</code>. Second, <b>views</b> chain
together with <code>|</code> into pipelines that filter, transform, and
slice data — without writing a single loop or building a single
intermediate container:</p>

<pre class="code">#include &lt;ranges&gt;
#include &lt;vector&gt;

std::vector&lt;int&gt; v = {1, 2, 3, 4, 5, 6, 7, 8};

// filter + transform pipeline
auto result = v
    | std::views::filter([](int n) { return n % 2 == 0; })
    | std::views::transform([](int n) { return n * n; });

for (int n : result) std::cout &lt;&lt; n &lt;&lt; " ";   // 4 16 36 64

// take / drop
auto first3 = v | std::views::take(3);    // {1, 2, 3}
auto skip2 = v | std::views::drop(2);     // {3, 4, 5, 6, 7, 8}

// ranges::sort (cleaner than std::sort)
std::ranges::sort(v);</pre>

<p>Follow the pipeline. The filter view passes only even numbers —
<code>2, 4, 6, 8</code> — and the transform view squares whatever comes
through, so the loop prints <code>4 16 36 64</code>. Then
<code>take(3)</code> keeps the first three elements
(<code>{1, 2, 3}</code>) and <code>drop(2)</code> skips the first two
(<code>{3, 4, 5, 6, 7, 8}</code>) — both are windows on <code>v</code>,
not copies of it. Finally, <code>std::ranges::sort(v)</code> sorts the
same vector with no iterator ceremony.</p>

<p>Views are <b>lazy</b>: they create no containers and compute nothing
until you iterate, which means zero allocation and free composability.
The gotcha that follows: a view does not own its data, so a view of a
temporary container dangles. Keep the source container alive for as
long as the view exists. Used that way, a pipeline reads like a
sentence — "take v, filter evens, square them" — and every stage plugs
into the next with <code>|</code>.</p>
""",
            },
        ],
        "quiz": [
            {"type": "mc", "question": "Range views are:",
             "options": ["Eager — they copy data", "Lazy — they adapt iteration without copying", "Always slower", "Thread-unsafe"],
             "answer": 1, "explain": "Views compose lazily — no intermediate containers created."},
        ],
    },

    {
        "id": "cpp35",
        "title": "Modules",
        "emoji": "📦",
        "lessons": [
            {
                "title": "C++20 Modules",
                "html": """
<p>Since 1998 C++ has shared code through <b>headers</b>: every
<code>#include</code> literally copy-pastes the header's text into your
file, and the compiler re-parses the same standard headers millions of
times across a large project. <b>Modules</b> (C++20) fix this: a module
is compiled once into a binary artifact that <code>import</code> loads
directly — faster builds, no include guards, and nothing crosses the
boundary unless you explicitly <code>export</code> it:</p>

<pre class="code">// math.cppm — module interface
export module math;

export namespace math {
    constexpr double PI = 3.14159;
    double circle_area(double r) { return PI * r * r; }
}

// main.cpp — import it
import math;

int main() {
    std::cout &lt;&lt; math::circle_area(5.0);
}</pre>

<p>Reading it: the interface file starts with <code>export module
math;</code>, and only the names marked <code>export</code> — here
<code>PI</code> and <code>circle_area</code> — are visible to
importers; everything else stays private to the module. The consumer
writes <code>import math;</code> and calls
<code>math::circle_area(5.0)</code>, which prints <code>78.5397</code>.
Note what is missing: no include guards, no duplicated declarations
between a header and a source file, and macros defined in
<code>math</code> cannot leak into your code — <code>export</code> is
an explicit contract, so accidental dependencies simply stop
compiling.</p>

<p>Gotcha: toolchain support is still maturing. File extensions
(<code>.cppm</code>, <code>.ixx</code>) differ between compilers, and
your build system needs module-aware rules to compile the interface
before anything that imports it. The language design is solid; the
adoption lag is in the tooling, so follow your build tool's module
recipe when wiring a real project.</p>
""",
            },
        ],
        "quiz": [
            {"type": "mc", "question": "Which concept is covered in this chapter?",
             "options": ["Core C++ feature", "HTML styling", "Database queries", "Network protocols"],
             "answer": 0, "explain": "This chapter covers a core C++ concept."},
        ],
    },

    {
        "id": "cpp36",
        "title": "Coroutines",
        "emoji": "🌀",
        "lessons": [
            {
                "title": "Coroutines: co_await, co_yield, co_return",
                "html": """
<p>A <b>coroutine</b> (C++20) is a function that can pause itself in
the middle and later resume exactly where it stopped. An ordinary
function runs start to finish; a coroutine can hand a value to its
caller, go to sleep keeping all its local variables alive, and pick up
on the next line when asked. That one ability powers two big use
cases: lazy sequence generators, and asynchronous code that reads like
ordinary sequential code:</p>

<pre class="code">generator&lt;int&gt; fibonacci() {
    int a = 0, b = 1;
    while (true) {
        co_yield a;          // pause here, return a
        [a, b] = [b, a + b]; // resume here
    }
}

// async coroutine
task&lt;std::string&gt; fetch_data() {
    auto response = co_await async_http_get("...");
    co_return response.body;
}</pre>

<p>Watch <code>fibonacci()</code> run: it starts with
<code>a, b = 0, 1</code>, hits <code>co_yield a</code>, and pauses —
handing <code>0</code> to whoever asked. Each time the caller asks for
the next value, execution resumes at the assignment and yields
<code>1, 1, 2, 3, 5...</code> one number at a time. The
<code>while (true)</code> is not a bug: a generator is lazy, doing work
only when pulled. In the <code>task</code> version,
<code>co_await</code> suspends the function while the HTTP call runs
elsewhere and resumes it with the response — the code reads top to
bottom, yet the thread was never blocked.</p>

<p>Gotcha: containing any of the three keywords —
<code>co_await</code> (wait for something asynchronous),
<code>co_yield</code> (produce a value and pause),
<code>co_return</code> (return and finish) — automatically makes a
function a coroutine, and a coroutine needs a return type with library
support (a promise type such as <code>generator&lt;int&gt;</code> or
<code>task&lt;T&gt;</code>; <code>std::generator</code> arrives in
C++23). The language provides the mechanism; the library provides the
policies, so use library types rather than writing promise types
yourself.</p>
""",
            },
        ],
        "quiz": [
            {"type": "mc", "question": "Which concept is covered in this chapter?",
             "options": ["Core C++ feature", "HTML styling", "Database queries", "Network protocols"],
             "answer": 0, "explain": "This chapter covers a core C++ concept."},
        ],
    },

    {
        "id": "cpp37",
        "title": "Concurrency",
        "emoji": "🧵",
        "lessons": [
            {
                "title": "Threads, Mutexes & Atomics",
                "html": """
<p>When two threads run <code>increment()</code> at the same time, they
both read, add to, and write the same counters — and without
synchronization that overlap corrupts data. The example deliberately
races two counters side by side: one protected by a
<code>std::mutex</code>, one by <code>std::atomic</code>, to show both
fixes and what happens without them:</p>

<pre class="code">#include &lt;thread&gt;
#include &lt;mutex&gt;
#include &lt;atomic&gt;

std::mutex mtx;
std::atomic&lt;int&gt; atomic_counter{0};
int unsafe_counter = 0;

void increment() {
    for (int i = 0; i &lt; 100000; i++) {
        mtx.lock();           // or: std::lock_guard&lt;std::mutex&gt; lock(mtx);
        unsafe_counter++;
        mtx.unlock();
        atomic_counter++;      // atomic — no lock needed!
    }
}

std::thread t1(increment);
std::thread t2(increment);
t1.join();
t2.join();
// atomic_counter == 200000 (correct!)
// unsafe_counter might be less (data race!)</pre>

<p>Both threads do 100000 iterations, so a correct counter must end at
<code>200000</code>. <code>atomic_counter++</code> is a single
indivisible read-modify-write, so it always lands exactly there. The
plain <code>unsafe_counter++</code> is really three steps — read, add,
write — and two threads can interleave those steps so updates get lost;
the final value comes out short and differs from run to run. That is a
<b>data race</b>, and it is undefined behavior, not merely "a wrong
number".</p>

<p>Gotchas: prefer <code>std::atomic</code> for simple counters and
flags — it needs no lock. For larger shared data, lock a
<code>std::mutex</code>, but through
<code>std::lock_guard&lt;std::mutex&gt; lock(mtx);</code> (RAII) rather
than raw <code>lock()</code>/<code>unlock()</code>: the guard releases
the mutex in its destructor even when an exception flies through, while
the raw pair deadlocks in exactly that case. Also note the example
locks on every loop pass — realistic, but slow; in real code, lock once
around a whole batch of work.</p>
""",
            },
        ],
        "quiz": [
            {"type": "mc", "question": "What is a data race?",
             "options": ["Two threads reading the same data", "Two threads writing the same data without synchronization", "Fast code", "A benchmark"],
             "answer": 1, "explain": "Unsynchronized concurrent writes = undefined behavior. Use atomics or mutexes."},
        ],
    },

    {
        "id": "cpp38",
        "title": "Object Lifetime & Advanced Memory",
        "emoji": "⏳",
        "lessons": [
            {
                "title": "Object Lifetime & Value Categories",
                "html": """
<p>Every expression in C++ belongs to a <b>value category</b>, and that
classification decides what the compiler lets you do with it — bind it
to a reference, move from it, take its address. It is the foundation
that move semantics, and with it all modern C++ resource handling,
stands on. Three categories matter:</p>

<ul>
<li><b>lvalue</b> — has an identity, can be addressed: <code>x</code>,
<code>*p</code>, <code>arr[0]</code></li>
<li><b>prvalue</b> — a temporary: <code>42</code>,
<code>x + y</code>, <code>makeObject()</code></li>
<li><b>xvalue</b> — expiring: <code>std::move(x)</code></li>
</ul>

<p><b>Lifetime</b> runs from constructor to destructor, and most
objects follow scope rules: born at their declaration, destroyed when
the closing brace passes. One deliberate exception — binding a
<b>const reference</b> to a temporary keeps that temporary alive as
long as the reference lives:</p>

<pre class="code">const std::string&amp; s = std::string("hello");
// temporary is NOT destroyed — s extends its lifetime</pre>

<p>Without this rule the temporary <code>std::string("hello")</code>
would die at the end of the statement and <code>s</code> would dangle;
instead it lives until <code>s</code> does. Gotcha: the extension
applies to const references (and rvalue references) in direct
initialization — pass a temporary to a function taking
<code>const std::string&amp;</code> and the extension lasts only for
that call.</p>

<p><b>Undefined behavior (UB)</b> is the deepest water in C++:
dereferencing null, buffer overflow, use-after-free, signed overflow,
data races. The standard defines no behavior at all for these, so the
compiler assumes they never happen and optimizes on that assumption —
results range from a wrong number to code that mysteriously vanishes
under optimization. Use-after-free usually traces back to a lifetime
mistake like the dangling view discussed earlier. Run tests under
sanitizers (<code>-fsanitize=address</code>,
<code>-fsanitize=undefined</code>) — they turn silent corruption into
loud, line-numbered crashes.</p>
""",
            },
        ],
        "quiz": [
            {"type": "mc", "question": "Which concept is covered in this chapter?",
             "options": ["Core C++ feature", "HTML styling", "Database queries", "Network protocols"],
             "answer": 0, "explain": "This chapter covers a core C++ concept."},
        ],
    },

    {
        "id": "cpp39",
        "title": "Advanced Templates",
        "emoji": "🎓",
        "lessons": [
            {
                "title": "Metaprogramming, SFINAE & Perfect Forwarding",
                "html": """
<p><b>Template metaprogramming</b> means computing with types at
compile time: the compiler resolves types, checks, and even numeric
results while building the binary, leaving zero runtime work.
<b>Type traits</b> are its basic vocabulary — small templates from
<code>&lt;type_traits&gt;</code> that answer yes/no questions about a
type as compile-time constants:</p>

<pre class="code">static_assert(std::is_integral_v&lt;int&gt;);       // compile-time check
static_assert(std::is_same_v&lt;int, int32_t&gt;);  // type comparison

// decltype: deduce the type of an expression
int x = 42;
decltype(x) y = 10;     // y is int</pre>

<p><code>static_assert(std::is_integral_v&lt;int&gt;)</code> makes the
compiler verify the claim while compiling — if it were false, the build
would fail right there. The <code>_v</code> suffix (C++17) is shorthand
for the trait's <code>::value</code> member.
<code>decltype(x)</code> asks the compiler "what type is this
expression?", answers <code>int</code>, and so <code>y</code> is an
<code>int</code> without you writing the type.</p>

<p><b>Perfect forwarding</b> is the plumbing underneath
<code>make_unique</code>, <code>emplace_back</code> and every wrapper
that constructs an object for you. The wrapper must pass arguments
along without disturbing them: an lvalue argument should be copied, an
rvalue moved — precisely as the caller intended:</p>

<pre class="code">template &lt;typename... Args&gt;
auto make_object(Args&amp;&amp;... args) {
    return std::make_unique&lt;MyClass&gt;(std::forward&lt;Args&gt;(args)...);
}
// lvalues are copied, rvalues are moved — exactly as intended</pre>

<p>The pack <code>Args&amp;&amp;... args</code> accepts any number of
arguments of any value category, and
<code>std::forward&lt;Args&gt;(args)...</code> re-delivers each one
with its original category intact. Get this wrong — pass
<code>args</code> along plainly — and every argument silently becomes
an lvalue: extra copies everywhere, with no compile error to warn you.
That invisibility is exactly why forwarding is easy to break and worth
understanding once, properly.</p>
""",
            },
        ],
        "quiz": [
            {"type": "mc", "question": "Which concept is covered in this chapter?",
             "options": ["Core C++ feature", "HTML styling", "Database queries", "Network protocols"],
             "answer": 0, "explain": "This chapter covers a core C++ concept."},
        ],
    },

    {
        "id": "cpp40",
        "title": "Perfect Forwarding",
        "emoji": "➡️",
        "lessons": [
            {
                "title": "Forwarding References & std::forward",
                "html": """
<p>A <b>forwarding reference</b> is <code>T&amp;&amp;</code> written in
a context where <code>T</code> is being deduced — a function template's
type parameter. It is the only kind of reference that binds to
<i>both</i> lvalues and rvalues: pass <code>42</code> and
<code>T</code> deduces as <code>int</code>; pass the named variable
<code>x</code> and <code>T</code> deduces as <code>int&amp;</code>.
But binding is only half the job — inside the wrapper, <code>arg</code>
is itself a named variable, hence an lvalue, so forwarding it plainly
would lose the caller's intent. <code>std::forward</code> restores
it:</p>

<pre class="code">template &lt;typename T&gt;
void wrapper(T&amp;&amp; arg) {
    // if arg was an lvalue, forward as lvalue (copy)
    // if arg was an rvalue, forward as rvalue (move)
    process(std::forward&lt;T&gt;(arg));
}

wrapper(42);         // rvalue → moved
int x = 10;
wrapper(x);          // lvalue → copied</pre>

<p>So <code>wrapper(42)</code> forwards <code>arg</code> as an rvalue
and <code>process</code> receives it ready to be moved, while
<code>wrapper(x)</code> forwards it as an lvalue and it gets copied.
The engine behind this is <b>reference collapsing</b>: references in
C++ cannot stack, so <code>T&amp;&amp;</code> with
<code>T = int&amp;</code> collapses to plain <code>int&amp;</code>,
while with <code>T = int</code> it stays <code>int&amp;&amp;</code> —
which is exactly what lets one function serve both value
categories.</p>

<p>Two gotchas. First, <code>Widget&amp;&amp; w</code> in a regular
function — where the type is fixed, not deduced — is just an ordinary
rvalue reference with no forwarding magic. Second, forgetting
<code>std::forward</code> never causes an error, only silent copies:
the code works, just slower. When in doubt inside a forwarding
wrapper, forward.</p>
""",
            },
        ],
        "quiz": [
            {"type": "mc", "question": "Which concept is covered in this chapter?",
             "options": ["Core C++ feature", "HTML styling", "Database queries", "Network protocols"],
             "answer": 0, "explain": "This chapter covers a core C++ concept."},
        ],
    },

    {
        "id": "cpp41",
        "title": "C++23 Features",
        "emoji": "🆕",
        "lessons": [
            {
                "title": "C++23 Highlights",
                "html": """
<p>C++23 is the standard this course targets. Its additions share one
theme: taking C++20's machinery and making it pleasant for daily use.
The five features below are the ones you will meet first — formatted
printing, errors as values, one function covering every qualification
combination, multidimensional views, and compile-time branching:</p>

<pre class="code">// std::print / std::println — formatted output (no iostream needed)
std::println("Hello, {}! You are {} years old.", "Ada", 36);

// std::expected — value or error without exceptions
std::expected&lt;int, std::string&gt; result = parse("42");

// deducing this — explicit object parameter
struct S {
    void func(this S&amp;&amp; self) { /* ... */ }
};

// std::mdspan — multidimensional array view
std::mdspan md(data.data(), 3, 4);

// if consteval — compile-time only branch
if consteval { /* compile-time path */ } else { /* runtime path */ }</pre>

<p>Line by line: <code>std::println</code> formats its arguments into
the <code>{}</code> slots — type-safe, powered by
<code>std::format</code>, no <code>std::cout</code> stream machinery —
and prints <code>Hello, Ada! You are 36 years old.</code> with a
newline. <code>std::expected</code> you met in the error-handling
chapter: value or error, no exceptions. "Deducing this" writes the
object parameter explicitly — <code>void func(this S&amp;&amp;
self)</code> — so one function definition serves const, non-const,
lvalue and rvalue objects instead of four overloads.
<code>std::mdspan</code> wraps a flat buffer as a 3×4 grid, giving you
rows and columns without copying anything. And <code>if
consteval</code> asks "am I compiling right now?", picking the
compile-time or the runtime path accordingly.</p>

<p>Beyond these: <code>std::flat_map</code> and
<code>std::flat_set</code> (sorted, cache-friendly storage),
<code>std::generator</code> for coroutines,
<code>std::stacktrace</code>, <code>std::byteswap</code>, and a large
batch of range improvements. Gotcha: compiler and library support for
C++23 is still rolling out — check your toolchain's feature table
before relying on a specific feature.</p>
""",
            },
        ],
        "quiz": [
            {"type": "mc", "question": "Which concept is covered in this chapter?",
             "options": ["Core C++ feature", "HTML styling", "Database queries", "Network protocols"],
             "answer": 0, "explain": "This chapter covers a core C++ concept."},
        ],
    },

    {
        "id": "cpp42",
        "title": "C++23 Standard Library",
        "emoji": "📚",
        "lessons": [
            {
                "title": "Standard Library Tour",
                "html": """
<p>You do not memorize the standard library — you learn <i>where
things live</i>. Each <code>#include</code> header below is a drawer in
a toolbox, and the comments name the tools inside it. Skim the list
once, then use the grouping after the block to find any tool in
seconds:</p>

<pre class="code">&lt;algorithm&gt;    sort, find, transform, ...
&lt;vector&gt;       dynamic array
&lt;string&gt;       std::string
&lt;string_view&gt;  non-owning string view
&lt;map&gt; / &lt;set&gt;  ordered associative
&lt;unordered_map&gt; / &lt;unordered_set&gt;  hashed
&lt;memory&gt;       unique_ptr, shared_ptr, allocator
&lt;optional&gt;     optional&lt;T&gt;
&lt;variant&gt;      variant&lt;Types...&gt;
&lt;expected&gt;     expected&lt;T, E&gt; (C++23)
&lt;span&gt;         non-owning contiguous view
&lt;ranges&gt;       views and range algorithms
&lt;concepts&gt;     std::integral, std::movable...
&lt;format&gt;       std::format, std::print (C++23)
&lt;thread&gt;       std::thread
&lt;mutex&gt;        std::mutex, lock_guard
&lt;atomic&gt;       std::atomic
&lt;filesystem&gt;   std::filesystem::path
&lt;chrono&gt;       time and duration</pre>

<p>Group the headers by job. Containers and strings:
<code>&lt;vector&gt;</code>, <code>&lt;string&gt;</code>,
<code>&lt;map&gt;</code>/<code>&lt;set&gt;</code> (tree-ordered) and the
<code>unordered_*</code> pair (hash-based, faster lookup, no ordering).
Adapters and views: <code>&lt;optional&gt;</code>,
<code>&lt;variant&gt;</code>, <code>&lt;expected&gt;</code>,
<code>&lt;string_view&gt;</code>, <code>&lt;span&gt;</code>.
Processing: <code>&lt;algorithm&gt;</code> for classic algorithms and
<code>&lt;ranges&gt;</code> for pipelines.
<code>&lt;memory&gt;</code> owns the smart pointers;
<code>&lt;concepts&gt;</code> constrains templates;
<code>&lt;format&gt;</code> prints; the trio
<code>&lt;thread&gt;</code>, <code>&lt;mutex&gt;</code>,
<code>&lt;atomic&gt;</code> handles concurrency;
<code>&lt;filesystem&gt;</code> walks directories;
<code>&lt;chrono&gt;</code> measures time. When a program needs
something, ask "is it a container, a view, an algorithm, a thread tool
or a time tool?" and you have already narrowed 100+ headers down to
one or two candidates.</p>

<p>Two gotchas: standard headers carry no <code>.h</code> suffix — it
is <code>#include &lt;string&gt;</code>, never
<code>#include &lt;string.h&gt;</code> (that is the C header, a
different beast entirely) — and include every header you actually use
instead of counting on one header pulling another in for you. That
habit costs seconds now and saves mysterious compile errors later,
when an indirect include silently disappears in an upgrade.</p>
""",
            },
        ],
        "quiz": [
            {"type": "mc", "question": "Which concept is covered in this chapter?",
             "options": ["Core C++ feature", "HTML styling", "Database queries", "Network protocols"],
             "answer": 0, "explain": "This chapter covers a core C++ concept."},
        ],
    },

    {
        "id": "cpp43",
        "title": "C++ Core Guidelines",
        "emoji": "📏",
        "lessons": [
            {
                "title": "Core Guidelines",
                "html": """
<p>The <b>C++ Core Guidelines</b>, curated by Bjarne Stroustrup and
Herb Sutter, distill decades of C++ practice into named, linkable
rules. You will not memorize them; you absorb the principles below,
and the tools check the rest. What matters most is the reasoning
behind each rule:</p>

<ul>
<li><b>RAII everywhere</b> — every resource (memory, file, lock,
socket) is owned by an object whose destructor releases it, so cleanup
happens automatically even when exceptions fly through.</li>
<li><b>Express intent</b> — <code>const</code> says "I won't change
this", <code>constexpr</code> says "compute me early",
<code>noexcept</code> says "I won't throw", <code>enum class</code>
says "these are named values, not ints". Readers and compilers both
benefit.</li>
<li><b>No raw new/delete</b> — ownership goes through
<code>make_unique</code>/<code>make_shared</code>, so each allocation
frees itself exactly once.</li>
<li><b>Pass by const&amp; for read-only, by value for small types</b> —
copying an <code>int</code> or a view is cheaper than the indirection
of a reference.</li>
<li><b>Use concepts for template constraints</b> — readable
requirements and readable error messages instead of SFINAE
arcana.</li>
<li><b>Prefer spans/string_views for parameters</b> — the function
then works on any container, without copies and without being coupled
to one type.</li>
<li><b>Zero as the ideal number of resource-management rules (Rule of
0)</b> — write no custom destructors or copy rules at all: let
<code>vector</code>, <code>string</code> and smart pointers manage
everything.</li>
</ul>

<p>Enforcement is not manual: run the C++ Core Guidelines Checker,
clang-tidy, or cppcheck in CI so violations surface before code review.
Treat their warnings as things to fix, not noise to silence — the
guidelines only work when a machine helps you keep them.</p>
""",
            },
        ],
        "quiz": [
            {"type": "mc", "question": "Which concept is covered in this chapter?",
             "options": ["Core C++ feature", "HTML styling", "Database queries", "Network protocols"],
             "answer": 0, "explain": "This chapter covers a core C++ concept."},
        ],
    },

    {
        "id": "cpp44",
        "title": "Professional C++",
        "emoji": "🏆",
        "lessons": [
            {
                "title": "Professional C++",
                "html": """
<p>Writing C++ you can ship means knowing the surrounding machinery as
well as the language. Here is the standard professional toolkit, and
what each piece does for you:</p>

<ul>
<li><b>Build systems</b> — CMake is the industry standard: one
description of your project builds it on Windows, Linux and macOS and
fetches its dependencies.</li>
<li><b>Testing</b> — Google Test, Catch2 and doctest let you assert
behavior in fast unit tests you rerun on every change.</li>
<li><b>Debugging</b> — GDB, LLDB and the Visual Studio debugger set
breakpoints, inspect variables, and step through live code.</li>
<li><b>Profiling</b> — perf, Valgrind and Intel VTune show where time
and memory actually go, so you optimize measurements, not guesses.</li>
<li><b>Static analysis</b> — clang-tidy, cppcheck and PVS-Studio find
bugs in the source without running it.</li>
<li><b>Sanitizers</b> — AddressSanitizer,
UndefinedBehaviorSanitizer and ThreadSanitizer catch memory, UB and
data-race bugs at runtime in test builds.</li>
<li><b>Package managers</b> — vcpkg and Conan install libraries
reproducibly instead of hand-vendored downloads.</li>
<li><b>CI/CD</b> — GitHub Actions and GitLab CI build, test and
analyze every commit automatically.</li>
</ul>

<p>Organize code accordingly: separate the interface
(<code>.h</code>/<code>.hpp</code>) from the implementation
(<code>.cpp</code>), keep one class per file when reasonable, put
everything in namespaces to prevent name collisions, and document with
Doxygen so the next reader — usually you — understands the intent.</p>

<p>You've completed the journey from "what is C++?" to
professional-grade C++23. Keep learning — the language evolves every
three years, and the ecosystem is always growing. The tools above are
where you go next.</p>
""",
            },
        ],
        "quiz": [
            {"type": "mc", "question": "Which concept is covered in this chapter?",
             "options": ["Core C++ feature", "HTML styling", "Database queries", "Network protocols"],
             "answer": 0, "explain": "This chapter covers a core C++ concept."},
        ],
    },
]
