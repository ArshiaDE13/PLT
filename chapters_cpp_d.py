"""C++ Tutor chapters 25-32 (Lambdas through Utility Types)."""

CHAPTERS_CPP_D = [
    {
        "id": "cpp25",
        "title": "Lambda Expressions",
        "emoji": "λ",
        "lessons": [
            {
                "title": "Lambda Syntax & Capture",
                "html": """
<p>Lambdas are anonymous functions defined inline — essential for STL algorithms:</p>

<pre class="code">auto add = [](int a, int b) { return a + b; };
std::cout &lt;&lt; add(2, 3);   // 5

// capture by value — copies at lambda creation
int x = 10;
auto byValue = [x]() { return x; };    // x is copied

// capture by reference — sees changes
auto byRef = [&amp;x]() { x *= 2; };
byRef();    // x is now 20

// capture everything
auto allByVal = [=]() { return x; };
auto allByRef = [&amp;]() { return x; };

// mutable: modify captured-by-value copies
auto counter = [count = 0]() mutable { return ++count; };</pre>

<p>Lambdas + STL algorithms = the heart of modern C++:</p>

<pre class="code">std::vector&lt;int&gt; v = {5, 2, 8, 1};
std::sort(v.begin(), v.end(), [](int a, int b) { return a &gt; b; });  // descending
auto evens = std::count_if(v.begin(), v.end(), [](int n) { return n % 2 == 0; });</pre>
""",
                "tryit": """#include <iostream>
#include <vector>
#include <algorithm>

int main() {
    std::vector<int> v = {5, 2, 8, 1, 9};

    std::sort(v.begin(), v.end(), [](int a, int b) {
        return a > b;
    });

    std::cout << "descending: ";
    for (int n : v) std::cout << n << " ";
    std::cout << "\\n";

    int threshold = 5;
    auto count = std::count_if(v.begin(), v.end(),
        [threshold](int n) { return n > threshold; });
    std::cout << "above " << threshold << ": " << count << "\\n";
    return 0;
}
""",
            },
        ],
        "quiz": [
            {"type": "mc", "question": "To modify a captured-by-value variable inside a lambda, add:",
             "options": ["const", "mutable", "static", "volatile"],
             "answer": 1, "explain": "[x]() mutable { ++x; } — mutable allows modifying the copy."},
        ],
    },

    {
        "id": "cpp26",
        "title": "Function Objects & std::function",
        "emoji": "🔧",
        "lessons": [
            {
                "title": "Functors & std::function",
                "html": """
<p><b>Functors</b> are objects with <code>operator()</code> — callable like functions but can hold state:</p>

<pre class="code">class Multiplier {
    int factor;
public:
    Multiplier(int f) : factor(f) {}
    int operator()(int n) const { return n * factor; }
};

Multiplier double_it(2);
std::cout &lt;&lt; double_it(5);   // 10 — called like a function!</pre>

<p><b>std::function</b> is a type-erased wrapper that can hold ANY callable — functions, lambdas, functors, function pointers:</p>

<pre class="code">#include &lt;functional&gt;

std::function&lt;int(int, int)&gt; op;

op = [](int a, int b) { return a + b; };
std::cout &lt;&lt; op(2, 3);    // 5

op = [](int a, int b) { return a * b; };
std::cout &lt;&lt; op(2, 3);    // 6</pre>
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
        "id": "cpp27",
        "title": "Templates",
        "emoji": "📐",
        "lessons": [
            {
                "title": "Function & Class Templates",
                "html": """
<p><b>Templates</b> generate code for any type — the foundation of generic programming:</p>

<pre class="code">// function template
template &lt;typename T&gt;
T maximum(T a, T b) {
    return (a &gt; b) ? a : b;
}

maximum(3, 7);        // T = int
maximum(3.14, 2.71);  // T = double
maximum("abc", "abd"); // T = const char*

// class template
template &lt;typename T&gt;
class Box {
    T value;
public:
    Box(T v) : value(v) {}
    T get() const { return value; }
};

Box&lt;int&gt; intBox(42);
Box&lt;std::string&gt; strBox("hello");</pre>

<p>Templates are <b>compile-time</b> — the compiler generates a separate
function/class for each type used. No runtime cost. Multiple template
parameters and non-type parameters are supported:</p>

<pre class="code">template &lt;typename T, int N&gt;
class Array {
    T data[N];
public:
    constexpr int size() const { return N; }
};</pre>
""",
            },
        ],
        "quiz": [
            {"type": "blank", "question": "Templates are resolved at ____ time, not runtime.",
             "answers": ["compile", "compile-time"], "explain": "The compiler generates code for each type used."},
        ],
    },

    {
        "id": "cpp28",
        "title": "Variadic Templates",
        "emoji": "📐",
        "lessons": [
            {
                "title": "Parameter Packs & Fold Expressions",
                "html": """
<p>Variadic templates accept any number of arguments:</p>

<pre class="code">template &lt;typename... Args&gt;
void print(Args... args) {
    (std::cout &lt;&lt; ... &lt;&lt; args) &lt;&lt; "\\n";   // fold expression (C++17)
}

print(1, "hello", 3.14);   // 1hello3.14

// recursive unpacking (C++14 style)
template &lt;typename T&gt;
void printEach(T t) { std::cout &lt;&lt; t &lt;&lt; "\\n"; }

template &lt;typename T, typename... Rest&gt;
void printEach(T first, Rest... rest) {
    std::cout &lt;&lt; first &lt;&lt; " ";
    printEach(rest...);      // recurse with one less
}</pre>
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
        "id": "cpp29",
        "title": "Concepts — C++20/23",
        "emoji": "✅",
        "lessons": [
            {
                "title": "Concepts & Constraints",
                "html": """
<p><b>Concepts</b> (C++20) are named requirements for template
parameters — better error messages and cleaner code:</p>

<pre class="code">#include &lt;concepts&gt;

// using standard concepts
template &lt;std::integral T&gt;
T double_it(T x) { return x * 2; }

// custom concept
template &lt;typename T&gt;
concept Addable = requires(T a, T b) {
    a + b;      // must support operator+
};

template &lt;Addable T&gt;
T add(T a, T b) { return a + b; }

// requires clause
template &lt;typename T&gt;
    requires std::floating_point&lt;T&gt;
double precision_square(T x) { return x * x; }</pre>

<p>Concepts replace SFINAE and <code>std::enable_if</code> with readable,
compile-time-checked constraints. If a type doesn't satisfy the concept,
you get a clear error instead of a template wall of text.</p>
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
        "id": "cpp30",
        "title": "constexpr, consteval, constinit",
        "emoji": "⚡",
        "lessons": [
            {
                "title": "Compile-Time Evaluation",
                "html": """
<pre class="code">// constexpr: can be evaluated at compile time (if possible)
constexpr int square(int n) { return n * n; }
constexpr int s = square(5);       // compile time!

// consteval: MUST be evaluated at compile time
consteval int alwaysCompiletime(int n) { return n * n; }
// int runtime = alwaysCompiletime(someRuntimeValue); // ERROR!

// constinit: guarantees static initialization
constinit int globalCounter = 0;   // initialized at compile time

// if constexpr: compile-time branching
template &lt;typename T&gt;
auto process(T value) {
    if constexpr (std::is_integral_v&lt;T&gt;) {
        return value * 2;
    } else {
        return value;
    }
}</pre>
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
        "id": "cpp31",
        "title": "std::optional, std::variant, std::any",
        "emoji": "🎁",
        "lessons": [
            {
                "title": "optional, variant & any",
                "html": """
<p><b>std::optional</b> — a value that may or may not exist:</p>

<pre class="code">std::optional&lt;int&gt; findUser(int id) {
    if (id == 1) return 42;
    return std::nullopt;    // "no value"
}

auto result = findUser(1);
if (result) std::cout &lt;&lt; *result;      // 42
std::cout &lt;&lt; result.value_or(0);       // 42 or 0</pre>

<p><b>std::variant</b> — holds one of several types (type-safe union):</p>

<pre class="code">std::variant&lt;int, std::string, double&gt; data;
data = 42;
data = "hello";         // now holds a string

if (std::holds_alternative&lt;int&gt;(data)) {
    std::cout &lt;&lt; std::get&lt;int&gt;(data);
}</pre>

<p><b>std::any</b> — type-erased value of ANY type:</p>

<pre class="code">std::any anything = 42;
anything = "now a string";
anything = 3.14;
auto val = std::any_cast&lt;double&gt;(anything);</pre>
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
        "id": "cpp32",
        "title": "std::string_view & Utility Types",
        "emoji": "🔖",
        "lessons": [
            {
                "title": "string_view, span, pair & tuple",
                "html": """
<p><b>std::string_view</b> — non-owning read-only view of a string. No
copy, no allocation:</p>

<pre class="code">void print(std::string_view sv) {   // takes string, literal, or view
    std::cout &lt;&lt; sv &lt;&lt; "\\n";
}
print("hello");           // no copy!
print(std::string("world")); // no copy!</pre>

<p><b>std::span</b> — non-owning view of contiguous data (C++20):</p>

<pre class="code">void process(std::span&lt;int&gt; data) {   // takes vector, array, etc.
    for (auto&amp; x : data) x *= 2;
}</pre>

<p><b>std::pair</b> and <b>std::tuple</b> — heterogeneous groups:</p>

<pre class="code">auto [name, age] = std::pair{"Ada", 36};
auto [a, b, c] = std::tuple{1, 2.5, "three"};</pre>
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
