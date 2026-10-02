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
<p>A <b>lambda</b> is a function you write inline, right where it is
used, without giving it a name. That solves a real problem: STL
algorithms need small pieces of custom logic — "compare descending",
"is this even?" — and defining a whole named function for each one
clutters the code. The general shape is <code>[capture](parameters) {
body }</code>: the parentheses and body look like an ordinary function,
and the square brackets in front are the lambda's signature feature —
they say which outside variables the body may use.</p>

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

<p>Read the block top to bottom. <code>add</code> is a lambda stored in
a variable, so you call it like any function: <code>add(2, 3)</code>
prints <code>5</code>. Then <code>x = 10</code> is captured two ways:
<code>[x]</code> copies the value at the moment the lambda is created,
so later changes to the outside <code>x</code> are invisible to it,
while <code>[&amp;x]</code> holds a reference — calling
<code>byRef()</code> really doubles the original, and <code>x</code>
becomes <code>20</code>. The shorthands <code>[=]</code> and
<code>[&amp;]</code> capture everything the body uses, by value or by
reference, and <code>mutable</code> lifts the const-ness of a by-value
copy so the counter can run <code>++count</code> on its own private
copy.</p>

<p>Gotcha: a by-reference capture keeps pointing at the original
variable. If that variable goes out of scope before the lambda runs,
the lambda touches dead memory — for anything that outlives the current
scope (stored callbacks, threads), prefer <code>[=]</code>.</p>

<p>Lambdas plus STL algorithms is the classic pairing: the algorithm
handles the loop, and your lambda supplies the one-line decision:</p>

<pre class="code">std::vector&lt;int&gt; v = {5, 2, 8, 1};
std::sort(v.begin(), v.end(), [](int a, int b) { return a &gt; b; });  // descending
auto evens = std::count_if(v.begin(), v.end(), [](int n) { return n % 2 == 0; });</pre>

<p>Inside <code>std::sort</code>, the lambda
<code>[](int a, int b) { return a &gt; b; }</code> is called for every
pair the algorithm considers, and returning <code>a &gt; b</code> flips
the order to descending: <code>{8, 5, 2, 1}</code>. Then
<code>std::count_if</code> walks that sorted vector and asks the second
lambda "is <code>n % 2 == 0</code>?" for each element — only 8 and 2
qualify, so it reports <code>2</code>. Neither lambda needs a capture
here, which is why the brackets are empty.</p>
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
<p>A <b>functor</b> is an object of a class that defines
<code>operator()</code>, which lets you call the object as if it were a
function. Why reach for one instead of a plain function? Because an
object can carry state: a function gets every piece of information
through its parameters, while a functor remembers settings from its
construction and applies them on every call — and it can still be
passed to STL algorithms like any other callable.</p>

<pre class="code">class Multiplier {
    int factor;
public:
    Multiplier(int f) : factor(f) {}
    int operator()(int n) const { return n * factor; }
};

Multiplier double_it(2);
std::cout &lt;&lt; double_it(5);   // 10 — called like a function!</pre>

<p>Walk through it: constructing <code>Multiplier double_it(2)</code>
stores <code>2</code> in the private <code>factor</code> member. The
call <code>double_it(5)</code> looks like a function call, but the
compiler turns it into <code>double_it.operator()(5)</code>, which
returns <code>5 * 2</code> — so <code>10</code> prints. Nothing stops
you from also building <code>Multiplier triple_it(3)</code>: two
objects, two behaviors, one class. Marking <code>operator()</code>
<code>const</code> is good style — a call should not change the stored
state.</p>

<p><b>std::function</b> solves a different problem: storing a callable
in a variable of one fixed type. A lambda's real type is known only to
the compiler, so you cannot write its type by hand.
<code>std::function&lt;int(int, int)&gt;</code> means "any callable
that takes two ints and returns an int" — a plain function, a lambda,
or a functor all fit:</p>

<pre class="code">#include &lt;functional&gt;

std::function&lt;int(int, int)&gt; op;

op = [](int a, int b) { return a + b; };
std::cout &lt;&lt; op(2, 3);    // 5

op = [](int a, int b) { return a * b; };
std::cout &lt;&lt; op(2, 3);    // 6</pre>

<p>The same variable <code>op</code> first runs the addition version
(printing <code>5</code>) and is then reassigned to the multiplication
version (printing <code>6</code>) — the type never changes, only the
callable inside it. Two gotchas: a default-constructed
<code>std::function</code> is empty, and calling it throws
<code>std::bad_function_call</code>, so test with <code>if (op)</code>
first. And because <code>std::function</code> hides the real type
behind an indirect call, it carries small runtime overhead — when a
lambda is used once, in place, a plain <code>auto</code> variable is
the cheaper choice.</p>
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
<p><b>Templates</b> are the foundation of generic programming: you write
one blueprint, and the compiler stamps out a version of it for every
type you use. Without templates you would write
<code>maximum_int</code>, <code>maximum_double</code>,
<code>maximum_string</code> — the same logic copy-pasted three times.
A template turns that "same logic" into one piece of code where the
type is a placeholder named <code>T</code>:</p>

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

<p>Trace the calls. In <code>maximum(3, 7)</code> the compiler sees two
<code>int</code> arguments and generates <code>maximum&lt;int&gt;</code>;
in <code>maximum(3.14, 2.71)</code> it generates
<code>maximum&lt;double&gt;</code>. This is called template
instantiation, and it happens silently at compile time. One surprise
hides in the third call: with <code>const char*</code> arguments the
comparison <code>a &gt; b</code> compares <b>pointers</b>, not the text
— a classic beginner trap. Class templates work the same way, but you
name the type explicitly because the compiler cannot guess it:
<code>Box&lt;int&gt;</code> and <code>Box&lt;std::string&gt;</code>
become two separate, complete classes.</p>

<p>Instantiation is a compile-time event, so there is no runtime cost —
the binary contains ordinary, fully-typed code. A template can take
several type parameters at once, and parameters do not have to be types
at all: a <b>non-type parameter</b> is a compile-time constant baked
into the type itself:</p>

<pre class="code">template &lt;typename T, int N&gt;
class Array {
    T data[N];
public:
    constexpr int size() const { return N; }
};</pre>

<p>Here <code>N</code> is not a type but a value:
<code>Array&lt;int, 10&gt;</code> and <code>Array&lt;int, 20&gt;</code>
are different types, each knowing its own length through
<code>size()</code>. Rule of thumb: a type parameter says "works for
any type", a non-type parameter says "this value is part of the
type".</p>
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
<p>A <b>variadic template</b> is a template that accepts any number of
arguments — zero, three, or thirty. Ordinary functions need one
overload per argument count; a variadic template needs exactly one.
This is how <code>std::make_unique</code>,
<code>emplace_back</code> and printf-style wrappers accept arbitrary
argument lists. The dot syntax <code>typename... Args</code> declares a
<b>parameter pack</b>: a bundle of types that expands to however many
arguments the caller actually passed:</p>

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

<p>Follow <code>print(1, "hello", 3.14)</code>. The fold expression
<code>(std::cout &lt;&lt; ... &lt;&lt; args)</code> (C++17) expands to
<code>((std::cout &lt;&lt; 1) &lt;&lt; "hello") &lt;&lt; 3.14</code> —
one chained statement printing <code>1hello3.14</code>, and the
<code>"\\n"</code> ends the line. The C++14 style below unpacks the
pack the old way: the one-argument overload is the <b>base case</b>
that stops the recursion, and the general overload prints the first
argument and calls itself with one fewer argument each time.</p>

<p>Two gotchas: the pack must be the last template parameter, and every
recursive unpacking needs a base case — forget it and the compiler
peels arguments forever, then errors out. Use
<code>sizeof...(args)</code> whenever you need to know how many
arguments a pack holds — for <code>print(1, "hello", 3.14)</code> it
reports <code>3</code>. Note that a variadic template happily accepts
zero arguments too: <code>print()</code> compiles, the pack is simply
empty, and the fold turns into a no-op.</p>
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
<p>Templates accept any type — but most code only works for types that
can do specific things. A <b>concept</b> (C++20) is a named, checkable
requirement such as "T must be an integer type" or "T must support
<code>+</code>". Before C++20 you could only document such rules in a
comment; pass the wrong type and you got a page of template error text.
Concepts turn that documentation into a compile-time contract, with an
error message a human can read:</p>

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

<p>Three usage forms appear here, all serving one goal. First,
<code>std::integral T</code> replaces <code>typename T</code> with a
standard concept from <code>&lt;concepts&gt;</code> — calling
<code>double_it</code> with a <code>double</code> is now a clean,
one-line error. Second, <code>Addable</code> is a custom concept: the
<code>requires(T a, T b) { a + b; }</code> block simply asks "does
<code>a + b</code> compile for this type?" — any type with a working
<code>operator+</code> satisfies it. Third, a standalone
<code>requires</code> clause after the template header can hold any
boolean condition, here <code>std::floating_point&lt;T&gt;</code>.</p>

<p>Gotchas: concepts are checked entirely at compile time and cost
nothing at runtime; a concept body only asks "does this compile" — no
side effects; and concepts combine with <code>&amp;&amp;</code> and
<code>||</code> like boolean expressions. Together they replace the old
SFINAE and <code>std::enable_if</code> tricks with constraints that are
readable, reusable, and compile-time checked.</p>
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
<p>Every keyword in this block moves work from runtime to <b>compile
time</b>. The payoff is simple: a computation done at compile time
costs nothing at runtime — the executable just contains the finished
result. The trick is picking the keyword whose promise matches your
intent, because each one promises something different:</p>

<ul>
<li><b>constexpr</b> — the function <i>may</i> run at compile time: it
will when called with constants, and quietly falls back to a normal
runtime call when it isn't.</li>
<li><b>consteval</b> — the function <i>must</i> run at compile time;
calling it with a runtime value is a compile error.</li>
<li><b>constinit</b> — the variable is initialized at compile time, so
it is never lazily zero-initialized at startup.</li>
<li><b>if constexpr</b> — the compiler keeps only the branch whose
condition is true; the discarded branch is not even compiled. Essential
inside templates.</li>
</ul>

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

<p>Reading the block: <code>constexpr int s = square(5);</code> asks
for a compile-time result, so the compiler folds it to <code>25</code>.
But call the same <code>square</code> with a value read from the user
and it silently becomes a normal runtime function — that flexibility is
constexpr's design. <code>alwaysCompiletime</code> is the strict
sibling: <code>consteval</code> rejects any call it cannot fold, which
is why the commented-out line would not compile.
<code>constinit int globalCounter = 0;</code> guarantees the global is
truly initialized before <code>main</code> runs — useful when globals
are read before any code of yours executes. In <code>process</code>,
<code>if constexpr (std::is_integral_v&lt;T&gt;)</code> checks the type
once at compile time and compiles only the matching return: an
<code>int</code> gets doubled, a <code>std::string</code> comes back
unchanged, and no runtime <code>if</code> remains.</p>

<p>Gotcha: <code>constexpr</code> on a function does not force
compile-time evaluation — only the way you call it does. If you need
proof, assert it with <code>static_assert(square(5) == 25);</code>.</p>
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
<p>Three standard types answer three flavors of the same question:
"what if the value isn't there?" <code>std::optional</code> handles
"maybe nothing", <code>std::variant</code> handles "one of these known
types", and <code>std::any</code> handles "literally anything".
Together they replace sentinel hacks like returning <code>-1</code>, an
empty string, or a null pointer — hacks that fail silently the moment a
caller forgets to check.</p>

<p><b>std::optional&lt;int&gt;</b> is a box that either contains an
<code>int</code> or is empty. The function below returns
<code>42</code> for user 1 and <code>std::nullopt</code> — the
officially empty box — for everyone else:</p>

<pre class="code">std::optional&lt;int&gt; findUser(int id) {
    if (id == 1) return 42;
    return std::nullopt;    // "no value"
}

auto result = findUser(1);
if (result) std::cout &lt;&lt; *result;      // 42
std::cout &lt;&lt; result.value_or(0);       // 42 or 0</pre>

<p>Two safe ways to read the box: <code>if (result)</code> is true only
when a value is present, and <code>value_or(0)</code> hands back the
value or your fallback — <code>42</code> for user 1, <code>0</code> for
anyone else. Gotcha: <code>*result</code> on an empty optional is
undefined behavior, the same shape of bug as dereferencing a null
pointer. Always check first, or use <code>value_or</code>.</p>

<p><b>std::variant&lt;int, std::string, double&gt;</b> holds exactly one
of the three listed types — a type-safe union. Assigning
<code>data = "hello"</code> destroys the old <code>int</code> and
constructs a <code>std::string</code> in its place:</p>

<pre class="code">std::variant&lt;int, std::string, double&gt; data;
data = 42;
data = "hello";         // now holds a string

if (std::holds_alternative&lt;int&gt;(data)) {
    std::cout &lt;&lt; std::get&lt;int&gt;(data);
}</pre>

<p>You must ask which type currently lives inside before reading it:
<code>std::holds_alternative&lt;int&gt;(data)</code> returns true or
false, and only then is <code>std::get&lt;int&gt;(data)</code> safe —
asking for the wrong type throws <code>std::bad_variant_access</code>
at runtime.</p>

<p><b>std::any</b> goes one step further: it can store <b>any</b> type,
decided entirely at runtime. Reading it back requires
<code>std::any_cast</code> with the exact type you expect:</p>

<pre class="code">std::any anything = 42;
anything = "now a string";
anything = 3.14;
auto val = std::any_cast&lt;double&gt;(anything);</pre>

<p>The sequence <code>42</code> → <code>"now a string"</code> →
<code>3.14</code> shows one <code>any</code> object changing its
contents' type three times; the cast must name <code>double</code>
because that is what it holds last. Casting to any other type throws
<code>std::bad_any_cast</code>. Choosing between the three: prefer
<code>optional</code>, then <code>variant</code> — <code>any</code> is
the heaviest and the least type-safe, so save it for genuinely
open-ended cases like plugin interfaces.</p>
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
<p><b>std::string_view</b> is a read-only, <b>non-owning</b> window onto
characters that live somewhere else. "Non-owning" is the key phrase:
the view holds a pointer and a length, not the data — so passing a
string to a function by <code>string_view</code> copies nothing and
allocates nothing, no matter how long the string is:</p>

<pre class="code">void print(std::string_view sv) {   // takes string, literal, or view
    std::cout &lt;&lt; sv &lt;&lt; "\\n";
}
print("hello");           // no copy!
print(std::string("world")); // no copy!</pre>

<p>Both calls print normally: <code>print("hello")</code> wraps the
literal in a view, and <code>print(std::string("world"))</code> wraps
the string's internal buffer — zero copies either way. The gotcha you
must know: because the view does not own its characters, the source
must outlive the view. Returning a <code>string_view</code> to a local
<code>std::string</code> leaves the view pointing at freed memory — the
dangling-reference bug of the string world.</p>

<p><b>std::span&lt;int&gt;</b> (C++20) is the same idea for any
contiguous data — <code>std::vector</code>, <code>std::array</code>, a
C array — handed to a function together with its length:</p>

<pre class="code">void process(std::span&lt;int&gt; data) {   // takes vector, array, etc.
    for (auto&amp; x : data) x *= 2;
}</pre>

<p>Inside <code>process</code>, the range-for doubles each element with
<code>x *= 2</code>, and the change lands in the caller's original
buffer — the view writes through to the real data. Unlike a raw pointer
plus size, a span carries <code>data.size()</code>, so the function
always knows how many elements it received.</p>

<p><b>std::pair</b> and <b>std::tuple</b> bundle values of different
types into one object, and <b>structured bindings</b> (C++17) unpack
them into named variables in a single line:</p>

<pre class="code">auto [name, age] = std::pair{"Ada", 36};
auto [a, b, c] = std::tuple{1, 2.5, "three"};</pre>

<p>The first line gives you a <code>std::string</code> named
<code>name</code> and an <code>int</code> named <code>age</code> — the
compiler matches each member to a variable by position, so the count
and order must be right. Use <code>pair</code>/<code>tuple</code> for
quick, local groupings; the moment the group deserves a name, write a
small <code>struct</code> instead — named members beat
<code>a, b, c</code> for readability.</p>
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
