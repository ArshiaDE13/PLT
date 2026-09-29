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
<p>C++ error handling: <b>exceptions</b> (traditional) and
<b>std::expected</b> (C++23, the modern alternative):</p>

<pre class="code">// traditional exceptions
try {
    throw std::runtime_error("something failed");
} catch (const std::exception&amp; e) {
    std::cout &lt;&lt; e.what() &lt;&lt; "\\n";
}

// noexcept: promises this function won't throw
void fast_function() noexcept { /* no exceptions here */ }</pre>

<p><b>std::expected</b> (C++23) — returns a value OR an error, no exceptions needed:</p>

<pre class="code">std::expected&lt;int, std::string&gt; parse(std::string_view s) {
    auto result = /* parse */;
    if (result.has_value()) return result.value();
    return std::unexpected("parse failed");
}

auto result = parse("42");
if (result) std::cout &lt;&lt; result.value();
else std::cout &lt;&lt; result.error();</pre>
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
<p><b>Ranges</b> (C++20) unify containers and algorithms with composable views:</p>

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

<p>Views are <b>lazy</b> — they don't create new containers, they adapt
the iteration. Zero allocation, composable, readable.</p>
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
<p><b>Modules</b> (C++20) replace header files with a cleaner import
system:</p>

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

<p>Advantages over headers: faster compilation (parsed once), no
include guards needed, no macro leakage, explicit exports. Still
adopting across build systems.</p>
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
<p>Coroutines (C++20) are functions that can <b>suspend and resume</b>:</p>

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

<p>Three keywords: <code>co_await</code> (wait for async),
<code>co_yield</code> (produce a value), <code>co_return</code> (return
and finish). Coroutines require library support (promise types) — the
language provides the mechanism, frameworks provide the policies.</p>
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

<p>Always prefer <code>std::atomic</code> for simple counters and
<code>std::lock_guard</code> for scoped locking (RAII). Never use raw
<code>lock()</code>/<code>unlock()</code> — an exception between them
deadlocks.</p>
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
<p><b>Value categories</b> — the foundation of move semantics:</p>

<ul>
<li><b>lvalue</b> — has an identity, can be addressed: <code>x</code>,
<code>*p</code>, <code>arr[0]</code></li>
<li><b>prvalue</b> — a temporary: <code>42</code>,
<code>x + y</code>, <code>makeObject()</code></li>
<li><b>xvalue</b> — expiring: <code>std::move(x)</code></li>
</ul>

<p><b>Lifetime extension</b>: a const reference to a temporary extends
its lifetime:</p>

<pre class="code">const std::string&amp; s = std::string("hello");
// temporary is NOT destroyed — s extends its lifetime</pre>

<p><b>Undefined behavior (UB)</b>: dereferencing null, buffer overflow,
use-after-free, signed overflow, data races... The compiler assumes UB
doesn't happen and optimizes accordingly — UB bugs are the worst kind.
Use sanitizers (<code>-fsanitize=address</code>) to catch them.</p>
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
<p><b>Template metaprogramming</b> — computing at compile time with
types. <b>Type traits</b> query type properties:</p>

<pre class="code">static_assert(std::is_integral_v&lt;int&gt;);       // compile-time check
static_assert(std::is_same_v&lt;int, int32_t&gt;);  // type comparison

// decltype: deduce the type of an expression
int x = 42;
decltype(x) y = 10;     // y is int</pre>

<p><b>Perfect forwarding</b> — pass arguments through while preserving
value category (lvalue stays lvalue, rvalue stays rvalue):</p>

<pre class="code">template &lt;typename... Args&gt;
auto make_object(Args&amp;&amp;... args) {
    return std::make_unique&lt;MyClass&gt;(std::forward&lt;Args&gt;(args)...);
}
// lvalues are copied, rvalues are moved — exactly as intended</pre>
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
<p><b>Forwarding references</b> (<code>T&amp;&amp;</code> in a deduced context)
bind to both lvalues and rvalues. <code>std::forward</code> preserves
the original value category:</p>

<pre class="code">template &lt;typename T&gt;
void wrapper(T&amp;&amp; arg) {
    // if arg was an lvalue, forward as lvalue (copy)
    // if arg was an rvalue, forward as rvalue (move)
    process(std::forward&lt;T&gt;(arg));
}

wrapper(42);         // rvalue → moved
int x = 10;
wrapper(x);          // lvalue → copied</pre>

<p><b>Reference collapsing</b>: <code>T&amp;&amp;</code> + <code>T&amp;</code> =
<code>T&amp;</code>; <code>T&amp;&amp;</code> + <code>T&amp;&amp;</code> =
<code>T&amp;&amp;</code>. This is what makes forwarding references work for
both value categories.</p>
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
<p>C++23 key features — the standard you're targeting:</p>

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

<p>Other additions: <code>std::flat_map</code>,
<code>std::flat_set</code>, <code>std::generator</code>,
<code>std::stacktrace</code>, <code>std::byteswap</code>, improved
<code>std::ranges</code>, and more.</p>
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
<p>The C++23 standard library headers you should know:</p>

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
<p>The <b>C++ Core Guidelines</b> (by Stroustrup and Sutter) codify
best practices. Key principles:</p>

<ul>
<li><b>RAII everywhere</b> — every resource owned by an object</li>
<li><b>Express intent</b> — <code>const</code>, <code>constexpr</code>,
<code>noexcept</code>, <code>enum class</code></li>
<li><b>No raw new/delete</b> — use make_unique/make_shared</li>
<li><b>Pass by const&amp; for read-only, by value for small types</b></li>
<li><b>Use concepts for template constraints</b></li>
<li><b>Prefer spans/string_views for parameters</b></li>
<li><b>Zero as the ideal number of resource-management rules</b>
(Rule of 0)</li>
</ul>

<p>Tools that enforce the guidelines: C++ Core Guidelines Checker,
clang-tidy, cppcheck, sanitizers.</p>
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
<p>Going from learning C++ to shipping C++:</p>

<ul>
<li><b>Build systems</b> — CMake is the industry standard</li>
<li><b>Testing</b> — Google Test, Catch2, doctest</li>
<li><b>Debugging</b> — GDB, LLDB, Visual Studio debugger</li>
<li><b>Profiling</b> — perf, Valgrind, Intel VTune</li>
<li><b>Static analysis</b> — clang-tidy, cppcheck, PVS-Studio</li>
<li><b>Sanitizers</b> — AddressSanitizer, UndefinedBehaviorSanitizer,
ThreadSanitizer</li>
<li><b>Package managers</b> — vcpkg, Conan</li>
<li><b>CI/CD</b> — GitHub Actions, GitLab CI</li>
</ul>

<p>Code organization: separate interface (.h/.hpp) from implementation
(.cpp), one class per file when reasonable, use namespaces to prevent
collisions, and document with Doxygen.</p>

<p>You've completed the journey from "what is C++?" to
professional-grade C++23. Keep learning — the language evolves every
three years, and the ecosystem is always growing.</p>
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
