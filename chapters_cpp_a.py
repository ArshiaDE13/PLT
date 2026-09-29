"""C++ Tutor chapters 1-8 (Basics through User-defined Types), grounded in learncpp.com."""

CHAPTERS_CPP_A = [
    {
        "id": "cpp01",
        "title": "Introduction to C++",
        "emoji": "🔷",
        "lessons": [
            {
                "title": "What is C++?",
                "html": """
<p><b>C++</b> is a general-purpose, compiled programming language created by Bjarne Stroustrup as an extension of C. It supports multiple paradigms: procedural, object-oriented, and generic programming. C++23 is the current standard.</p>

<p>Key characteristics:</p>

<ul>
<li><b>Compiled</b> — source code is translated directly to machine code (unlike interpreted languages)</li>
<li><b>Statically typed</b> — types are checked at compile time</li>
<li><b>Zero-cost abstractions</b> — high-level features don't slow you down</li>
<li><b>Manual + automatic memory management</b> — RAII and smart pointers</li>
</ul>

<p>C++ is used for: game engines, operating systems, browsers, embedded systems, financial trading, and more.</p>

<p>The build pipeline:</p>

<pre class="code">Source Code (.cpp)
     ↓
Compiler (g++, clang++)
     ↓
Object Code (.o / .obj)
     ↓
Linker
     ↓
Executable</pre>
""",
                "tryit": """#include <iostream>

int main() {
    std::cout << "Hello, C++23!\\n";
    std::cout << "Compiled, statically typed, and fast.\\n";
    return 0;
}
""",
            },
            {
                "title": "Statements, Expressions & Comments",
                "html": """
<p>A <b>statement</b> is an instruction that ends with a semicolon. An
<b>expression</b> is a combination of values and operators that produces a result:</p>

<pre class="code">int x = 5 + 3;    // statement: "5 + 3" is the expression
x = x * 2;         // another statement</pre>

<p>Comments are <code>//</code> (single line) and <code>/* */</code> (multi-line) — same as C.</p>

<p><b>main()</b> is the entry point of every C++ program. It returns an
<code>int</code> (0 = success):</p>

<pre class="code">int main() {
    return 0;
}</pre>
""",
            },
            {
                "title": "Header Files & iostream",
                "html": """
<p>Header files declare functions and types. <code>#include</code> pastes the header's content into your file:</p>

<pre class="code">#include &lt;iostream&gt;    // input/output streaming

int main() {
    std::cout &lt;&lt; "Output to console\\n";
    int age;
    std::cin &gt;&gt; age;           // read from user
    std::cout &lt;&lt; "You are " &lt;&lt; age &lt;&lt; std::endl;
    return 0;
}</pre>

<ul>
<li><code>std::cout</code> — character output (the console)</li>
<li><code>std::cin</code> — character input (the keyboard)</li>
<li><code>std::endl</code> — newline + flush</li>
<li><code>&lt;&lt;</code> — insertion operator (streams data out)</li>
<li><code>&gt;&gt;</code> — extraction operator (streams data in)</li>
</ul>
""",
                "tryit": """#include <iostream>

int main() {
    std::cout << "Name: ";
    // (stdin isn't available in the sandbox, so we hardcode)
    std::string name = "Ada";
    int age = 36;

    std::cout << "Hello, " << name << "!\\n";
    std::cout << "You are " << age << " years old." << std::endl;
    return 0;
}
""",
            },
        ],
        "quiz": [
            {"type": "mc", "question": "What does #include <iostream> provide?",
             "options": ["Math functions", "Input/output streaming", "String handling", "Memory management"],
             "answer": 1, "explain": "iostream gives std::cout, std::cin, std::endl."},
            {"type": "mc", "question": "What is the entry point of every C++ program?",
             "options": ["start()", "init()", "main()", "run()"],
             "answer": 2, "explain": "main() is where execution begins — it returns int."},
            {"type": "blank", "question": "The operator that sends data to std::cout is <code>____</code>.",
             "answers": ["<<", "<< operator"], "explain": "<< is the insertion operator."},
        ],
    },

    {
        "id": "cpp02",
        "title": "Variables & Data Types",
        "emoji": "📐",
        "lessons": [
            {
                "title": "Variables & Initialization",
                "html": """
<p>C++ has <b>three forms of initialization</b> — each has different rules:</p>

<pre class="code">int a = 10;     // copy initialization
int b{20};      // list (uniform) initialization — prevents narrowing!
int c(30);      // direct initialization

// narrowing is blocked by {} — this is a compile error:
// int x{3.14};  // error: narrowing conversion

int d = 3.14;   // OK but SILENTLY truncates to 3 (bad!)</pre>

<p>Modern C++ style prefers <b>list initialization</b> (<code>{}</code>)
because it prevents accidental narrowing.</p>

<p>Multiple variables can be declared on one line:</p>

<pre class="code">int x = 1, y = 2, z = 3;   // legal but less readable</pre>
""",
                "tryit": """#include <iostream>

int main() {
    int a = 10;       // copy init
    int b{20};        // list init (preferred)
    double d = 3.14;
    int truncated = d;    // silently truncates!

    std::cout << "a=" << a << " b=" << b << "\\n";
    std::cout << "d=" << d << " truncated=" << truncated << "\\n";
    return 0;
}
""",
            },
            {
                "title": "Fundamental Types & sizeof",
                "html": """
<p>C++ fundamental types, with typical sizes:</p>

<ul>
<li><b>Integers:</b> <code>short</code> (2), <code>int</code> (4),
<code>long</code> (4/8), <code>long long</code> (8)</li>
<li><b>Floating:</b> <code>float</code> (4), <code>double</code> (8),
<code>long double</code> (8/16)</li>
<li><b>Character:</b> <code>char</code> (1), <code>wchar_t</code>,
<code>char8_t</code>, <code>char16_t</code>, <code>char32_t</code></li>
<li><b>Boolean:</b> <code>bool</code> (1) — true/false</li>
<li><b>void</b> — "no type" (for functions that return nothing)</li>
<li><b>nullptr_t</b> — type of <code>nullptr</code></li>
</ul>

<p><b>Signed vs unsigned:</b> signed types can hold negatives;
unsigned types cannot:</p>

<pre class="code">int s = -42;              // signed (default)
unsigned int u = 42;      // unsigned (0 to ~4 billion)

sizeof(int)      // 4 bytes
sizeof(double)   // 8 bytes
sizeof(bool)     // 1 byte</pre>
""",
                "tryit": """#include <iostream>

int main() {
    std::cout << "int:    " << sizeof(int) << " bytes\\n";
    std::cout << "double: " << sizeof(double) << " bytes\\n";
    std::cout << "char:   " << sizeof(char) << " byte\\n";
    std::cout << "bool:   " << sizeof(bool) << " byte\\n";

    int s = -42;
    unsigned int u = 42;
    std::cout << "signed: " << s << ", unsigned: " << u << "\\n";
    return 0;
}
""",
            },
        ],
        "quiz": [
            {"type": "mc", "question": "Which initialization form prevents narrowing conversions?",
             "options": ["int x = 3.14;", "int x{3.14};", "int x(3.14);", "int x;"],
             "answer": 1, "explain": "List initialization {} blocks narrowing — a compile error instead of silent truncation."},
            {"type": "blank", "question": "The operator that returns a type's size in bytes is <code>____</code>.",
             "answers": ["sizeof"], "explain": "sizeof(int) gives the byte count."},
        ],
    },

    {
        "id": "cpp03",
        "title": "Operators & Expressions",
        "emoji": "➕",
        "lessons": [
            {
                "title": "Arithmetic & Assignment Operators",
                "html": """
<p>The operator set (same as C with a few C++ additions):</p>

<pre class="code">int a = 10, b = 3;

a + b    // 13     addition
a - b    // 7      subtraction
a * b    // 30     multiplication
a / b    // 3      integer division (truncates!)
a % b    // 1      modulo (remainder)

// compound assignment
a += 5;  // a = a + 5
a -= 2;  // a = a - 2
a *= 3;  // a = a * 3
a /= 4;  // a = a / 4
a %= 7;  // a = a % 7

// increment / decrement
++a;     // pre-increment (increment THEN use)
a++;     // post-increment (use THEN increment)
--a;     // pre-decrement
a--;     // post-decrement</pre>

<p>Integer division truncates: <code>7 / 2 = 3</code> not 3.5. Use
<code>7.0 / 2</code> for floating-point division.</p>
""",
                "tryit": """#include <iostream>

int main() {
    int a = 10, b = 3;
    std::cout << "a / b = " << a / b << "\\n";     // 3
    std::cout << "a % b = " << a % b << "\\n";     // 1
    std::cout << "a / 2.0 = " << a / 2.0 << "\\n"; // 5.0

    int c = a++;
    int d = ++a;
    std::cout << "c=" << c << " d=" << d << "\\n"; // 10, 12
    return 0;
}
""",
            },
            {
                "title": "Comparison, Logical & Bitwise",
                "html": """
<p><b>Comparison:</b> <code>== != &lt; &gt; &lt;= &gt;=</code></p>
<p><b>Logical:</b> <code>&amp;&amp;</code> (AND), <code>||</code> (OR),
<code>!</code> (NOT) — short-circuiting</p>
<p><b>Bitwise:</b> <code>&amp;</code> AND, <code>|</code> OR, <code>^</code> XOR,
<code>~</code> NOT, <code>&lt;&lt;</code> shift left, <code>&gt;&gt;</code> shift right</p>

<pre class="code">int a = 12, b = 10;   // 1100, 1010
a &amp; b    // 8    (1000)
a | b    // 14   (1110)
a ^ b    // 6    (0110)
~a       // -13
a &lt;&lt; 2   // 48   (110000)
a &gt;&gt; 2   // 3    (11)</pre>

<p><b>Operator precedence:</b> <code>* / %</code> bind tighter than
<code>+ -</code>, which bind tighter than comparisons, which bind tighter
than <code>&amp;&amp;</code>, which binds tighter than <code>||</code>.
Use parentheses when in doubt.</p>
""",
                "tryit": """#include <iostream>

int main() {
    int a = 12, b = 10;
    std::cout << "a & b  = " << (a & b) << "\\n";
    std::cout << "a | b  = " << (a | b) << "\\n";
    std::cout << "a ^ b  = " << (a ^ b) << "\\n";
    std::cout << "a << 2 = " << (a << 2) << "\\n";
    std::cout << "a >> 2 = " << (a >> 2) << "\\n";

    bool x = true, y = false;
    std::cout << "x && y = " << (x && y) << "\\n";
    std::cout << "x || y = " << (x || y) << "\\n";
    return 0;
}
""",
            },
            {
                "title": "Type Conversions",
                "html": """
<p>C++ has <b>implicit</b> (automatic) and <b>explicit</b> (manual)
conversions:</p>

<pre class="code">// implicit (compiler does it)
int i = 3.99;           // 3 — silently truncates!
double d = 5;           // 5.0

// explicit — the C++ way: static_cast
double pi = 3.14159;
int truncated = static_cast&lt;int&gt;(pi);     // 3
double exact = static_cast&lt;double&gt;(7) / 2; // 3.5 (not 3!)

// C-style cast (avoid — no type checking)
int old = (int)pi;</pre>

<p>Modern C++ prefers <code>static_cast&lt;&gt;</code> over C-style casts
because it's searchable and type-checked.</p>
""",
                "tryit": """#include <iostream>

int main() {
    double pi = 3.14159;
    int trunc = pi;                              // implicit
    int cast = static_cast<int>(pi);             // explicit

    int total = 17, count = 2;
    double avg1 = total / count;                  // 8 (integer division!)
    double avg2 = static_cast<double>(total) / count; // 8.5

    std::cout << "implicit: " << trunc << "\\n";
    std::cout << "explicit: " << cast << "\\n";
    std::cout << "int div: " << avg1 << "\\n";
    std::cout << "cast div: " << avg2 << "\\n";
    return 0;
}
""",
            },
        ],
        "quiz": [
            {"type": "mc", "question": "What does 7 / 2 evaluate to in C++ (integer operands)?",
             "options": ["3.5", "3", "4", "Error"], "answer": 1,
             "explain": "Integer division truncates toward zero."},
            {"type": "mc", "question": "Which cast is preferred in modern C++?",
             "options": ["(int)x", "static_cast<int>(x)", "int(x)", "dynamic_cast<int>(x)"],
             "answer": 1, "explain": "static_cast is type-checked and searchable."},
        ],
    },

    {
        "id": "cpp04",
        "title": "Control Flow",
        "emoji": "🔀",
        "lessons": [
            {
                "title": "if / else & switch",
                "html": """
<pre class="code">if (score &gt;= 90) {
    std::cout &lt;&lt; "A\\n";
} else if (score &gt;= 80) {
    std::cout &lt;&lt; "B\\n";
} else {
    std::cout &lt;&lt; "F\\n";
}

switch (choice) {
    case 1:  std::cout &lt;&lt; "one\\n"; break;
    case 2:  std::cout &lt;&lt; "two\\n"; break;
    default: std::cout &lt;&lt; "other\\n";
}

// C++17: init-statement inside if
if (auto value = getValue(); value &gt; 10) {
    // value only visible here!
}</pre>
""",
                "tryit": """#include <iostream>

int main() {
    int score = 85;
    if (score >= 90)      std::cout << "A\\n";
    else if (score >= 80) std::cout << "B\\n";
    else                  std::cout << "F\\n";

    switch (score / 10) {
        case 10: case 9:  std::cout << "Excellent\\n"; break;
        case 8:           std::cout << "Good\\n"; break;
        default:          std::cout << "Keep going\\n";
    }
    return 0;
}
""",
            },
            {
                "title": "Loops & Range-based for",
                "html": """
<pre class="code">// while
int i = 0;
while (i &lt; 5) { std::cout &lt;&lt; i &lt;&lt; " "; i++; }

// do...while (runs at least once)
int j = 100;
do { std::cout &lt;&lt; j; j++; } while (j &lt; 5);

// for
for (int k = 0; k &lt; 5; k++) { std::cout &lt;&lt; k &lt;&lt; " "; }

// range-based for (C++11) — the modern way
for (int x : {1, 2, 3, 4, 5}) {
    std::cout &lt;&lt; x &lt;&lt; " ";
}

// break and continue work the same as C
for (int n = 0; n &lt; 10; n++) {
    if (n % 2) continue;    // skip odds
    if (n &gt; 6) break;       // stop
    std::cout &lt;&lt; n &lt;&lt; " ";   // 0 2 4 6
}</pre>
""",
                "tryit": """#include <iostream>

int main() {
    for (int i = 1; i <= 3; i++) {
        for (int j = 1; j <= 3; j++) {
            std::cout << i << "x" << j << "=" << i*j << " ";
        }
        std::cout << "\\n";
    }

    // range-based for
    for (int x : {10, 20, 30}) std::cout << x << " ";
    std::cout << "\\n";
    return 0;
}
""",
            },
        ],
        "quiz": [
            {"type": "mc", "question": "Which loop always runs at least once?",
             "options": ["for", "while", "do...while", "range-based for"],
             "answer": 2, "explain": "do...while checks after the body — always runs at least once."},
            {"type": "blank", "question": "The C++11 loop for iterating containers is the ____ for loop.",
             "answers": ["range-based", "range"], "explain": "for (auto x : container) — no index needed."},
        ],
    },

    {
        "id": "cpp05",
        "title": "Functions",
        "emoji": "🧩",
        "lessons": [
            {
                "title": "Function Declaration, Definition & Call",
                "html": """
<p>A <b>function declaration</b> (prototype) tells the compiler what
exists. A <b>definition</b> provides the body:</p>

<pre class="code">// declaration (prototype) — usually in a header file
int add(int a, int b);

// definition — usually in a .cpp file
int add(int a, int b) {
    return a + b;
}

int main() {
    int result = add(3, 4);   // call
    return 0;
}</pre>

<p><b>Parameters</b> are in the declaration; <b>arguments</b> are what
you pass. Functions with no return value use <code>void</code>.</p>

<p><b>Local variables</b> exist only inside the function. <b>Global
variables</b> exist everywhere (avoid them when possible).</p>
""",
                "tryit": """#include <iostream>

int add(int a, int b) { return a + b; }

int main() {
    std::cout << "3 + 4 = " << add(3, 4) << "\\n";
    std::cout << "10 + 20 = " << add(10, 20) << "\\n";
    return 0;
}
""",
            },
            {
                "title": "Overloading & Default Arguments",
                "html": """
<p><b>Function overloading</b> — same name, different parameter types.
The compiler picks the right one:</p>

<pre class="code">int add(int a, int b) { return a + b; }
double add(double a, double b) { return a + b; }
int add(int a, int b, int c) { return a + b + c; }

add(1, 2);       // calls int version
add(1.5, 2.5);   // calls double version
add(1, 2, 3);    // calls 3-arg version</pre>

<p><b>Default arguments</b> provide fallback values:</p>

<pre class="code">void greet(std::string name = "guest", int times = 1) {
    for (int i = 0; i &lt; times; i++)
        std::cout &lt;&lt; "Hello, " &lt;&lt; name &lt;&lt; "!\\n";
}

greet();           // "Hello, guest!"
greet("Ada");     // "Hello, Ada!"
greet("Ada", 3);  // 3 times</pre>

<p><b>constexpr functions</b> can be evaluated at compile time:</p>

<pre class="code">constexpr int square(int n) { return n * n; }
constexpr int s = square(5);  // computed at COMPILE TIME (25)</pre>
""",
                "tryit": """#include <iostream>

int add(int a, int b) { return a + b; }
double add(double a, double b) { return a + b; }

constexpr int square(int n) { return n * n; }

int main() {
    std::cout << add(1, 2) << "\\n";       // int version
    std::cout << add(1.5, 2.5) << "\\n";   // double version
    std::cout << square(5) << "\\n";       // compile-time!
    constexpr int s = square(10);          // guaranteed compile-time
    std::cout << s << "\\n";
    return 0;
}
""",
            },
        ],
        "quiz": [
            {"type": "mc", "question": "Function overloading requires:",
             "options": ["Different return types", "Different parameter types or counts", "Different names", "Different access levels"],
             "answer": 1, "explain": "Same name, different parameters — the compiler picks by argument types."},
            {"type": "blank", "question": "Functions evaluated at compile time use the keyword <code>____</code>.",
             "answers": ["constexpr"], "explain": "constexpr functions can be computed at compile time."},
        ],
    },

    {
        "id": "cpp06",
        "title": "Scope, Storage & Lifetime",
        "emoji": "🗂️",
        "lessons": [
            {
                "title": "Scope, Lifetime & Storage Duration",
                "html": """
<p>Three distinct concepts that beginners often confuse:</p>

<ul>
<li><b>Scope</b> — WHERE in the code a name is visible</li>
<li><b>Lifetime</b> — WHEN an object exists (born to destroyed)</li>
<li><b>Storage duration</b> — HOW memory is allocated (automatic, static, dynamic)</li>
</ul>

<pre class="code">int globalVar = 1;         // global scope, static duration

void demo() {
    int localVar = 2;      // block scope, automatic duration
    static int staticVar = 0;  // block scope, STATIC duration
    staticVar++;           // persists between calls!
}

int main() {
    {   // inner block
        int blockVar = 3;  // block scope
    }   // blockVar destroyed here
    // blockVar not visible here
}</pre>

<p><b>static</b> on a local variable: created once, persists between
calls. <b>static</b> on a global: internal linkage (file-private).</p>
""",
                "tryit": """#include <iostream>

void counter() {
    static int count = 0;   // created ONCE, persists
    count++;
    std::cout << "call #" << count << "\\n";
}

int main() {
    counter();  // call #1
    counter();  // call #2
    counter();  // call #3
    return 0;
}
""",
            },
        ],
        "quiz": [
            {"type": "mc", "question": "A static local variable:",
             "options": ["Is created fresh each call", "Persists between function calls", "Is global", "Can't be modified"],
             "answer": 1, "explain": "Created once, keeps its value across calls."},
        ],
    },

    {
        "id": "cpp07",
        "title": "Arrays & Strings",
        "emoji": "📝",
        "lessons": [
            {
                "title": "C-style Arrays & std::array",
                "html": """
<p><b>C-style arrays</b> are fixed-size, no bounds checking:</p>

<pre class="code">int numbers[5] = {1, 2, 3, 4, 5};
numbers[0] = 10;    // first element
// numbers[5] = 99; // NO bounds check — undefined behavior!</pre>

<p><b>std::array</b> (C++11) — safer, knows its size, works with STL:</p>

<pre class="code">#include &lt;array&gt;

std::array&lt;int, 5&gt; arr = {1, 2, 3, 4, 5};
arr.size()          // 5
arr.at(2)           // 3 (with bounds checking!)
arr.fill(0)         // set all to 0</pre>

<p>Modern C++ prefers <code>std::array</code> for fixed-size, and
<code>std::vector</code> for dynamic arrays.</p>
""",
                "tryit": """#include <iostream>
#include <array>

int main() {
    std::array<int, 5> arr = {1, 2, 3, 4, 5};
    std::cout << "size: " << arr.size() << "\\n";
    std::cout << "first: " << arr[0] << "\\n";
    std::cout << "last: " << arr[4] << "\\n";

    // range-based for works with std::array
    for (int x : arr) std::cout << x << " ";
    std::cout << "\\n";
    return 0;
}
""",
            },
            {
                "title": "C-style Strings & std::string",
                "html": """
<p><b>C-style strings</b> are char arrays ending with <code>'\\0'</code>:</p>

<pre class="code">char name[20] = "Ada";    // C-style — careful with overflow!</pre>

<p><b>std::string</b> (C++) — dynamic, safe, feature-rich:</p>

<pre class="code">#include &lt;string&gt;

std::string name = "Ada";
std::string full = name + " Lovelace";   // concatenation
name += " (Byron)";                        // append
full.length()            // length
full.substr(0, 3)        // substring "Ada"
full.find("Love")        // index or npos
full[0]                  // 'A' (character access)
full == "Ada"            // comparison</pre>

<p>Modern C++ always uses <code>std::string</code> over C-style strings.
<code>std::string_view</code> (C++17) provides non-owning read-only
access — covered in the Utility Types chapter.</p>
""",
                "tryit": """#include <iostream>
#include <string>

int main() {
    std::string first = "Ada";
    std::string last = "Lovelace";
    std::string full = first + " " + last;

    std::cout << "full: " << full << "\\n";
    std::cout << "length: " << full.length() << "\\n";
    std::cout << "first 3: " << full.substr(0, 3) << "\\n";
    std::cout << "contains 'Love': " << (full.find("Love") != std::string::npos) << "\\n";
    return 0;
}
""",
            },
        ],
        "quiz": [
            {"type": "mc", "question": "Which is preferred in modern C++ for fixed-size arrays?",
             "options": ["int arr[5]", "std::array<int, 5>", "malloc(5)", "new int[5]"],
             "answer": 1, "explain": "std::array knows its size, works with STL, and has bounds-checked at()."},
        ],
    },

    {
        "id": "cpp08",
        "title": "Structs, Enums & User-defined Types",
        "emoji": "📦",
        "lessons": [
            {
                "title": "struct",
                "html": """
<p>A <b>struct</b> bundles related data into one named type:</p>

<pre class="code">struct Player {
    std::string name;
    int score;
    double health;
};

Player p;              // create an instance
p.name = "Hero";       // dot operator
p.score = 100;
p.health = 100.0;

// initialization
Player p2 = {"Mage", 50, 75.0};
Player p3{"Rogue", 80, 90.0};    // list init

// passing to functions
void print(const Player&amp; p) {     // const reference — no copy!
    std::cout &lt;&lt; p.name &lt;&lt; ": " &lt;&lt; p.score &lt;&lt; "\\n";
}</pre>
""",
                "tryit": """#include <iostream>
#include <string>

struct Player {
    std::string name;
    int score;
};

void print(const Player& p) {
    std::cout << p.name << ": " << p.score << "\\n";
}

int main() {
    Player p1 = {"Hero", 100};
    Player p2{"Mage", 50};
    print(p1);
    print(p2);
    return 0;
}
""",
            },
            {
                "title": "enum, enum class & Type Aliases",
                "html": """
<p><b>enum</b> — named integer constants (unscoped, implicitly convert
to int):</p>

<pre class="code">enum Color { Red, Green, Blue };   // Red=0, Green=1, Blue=2
Color c = Green;
int n = c;     // OK — implicitly converts (can be dangerous!)</pre>

<p><b>enum class</b> (C++11) — scoped, type-safe, no implicit
conversion:</p>

<pre class="code">enum class Color { Red, Green, Blue };
enum class Fruit { Apple, Orange };

Color c = Color::Green;
// int n = c;              // ERROR — no implicit conversion!
// if (c == Fruit::Apple)  // ERROR — different types!
int n = static_cast&lt;int&gt;(c);  // explicit only</pre>

<p><b>Type aliases</b> — new names for existing types:</p>

<pre class="code">using Score = int;         // modern (preferred)
typedef int Score;          // legacy (same effect)

using PlayerMap = std::map&lt;std::string, Player&gt;;  // much cleaner!</pre>

<p>Modern C++ always uses <code>enum class</code> over plain
<code>enum</code> and <code>using</code> over
<code>typedef</code>.</p>
""",
                "tryit": """#include <iostream>

enum class Color { Red, Green, Blue };

int main() {
    Color c = Color::Green;

    switch (c) {
        case Color::Red:   std::cout << "red\\n"; break;
        case Color::Green: std::cout << "green\\n"; break;
        case Color::Blue:  std::cout << "blue\\n"; break;
    }

    // explicit conversion
    int value = static_cast<int>(c);
    std::cout << "value: " << value << "\\n";  // 1
    return 0;
}
""",
            },
        ],
        "quiz": [
            {"type": "mc", "question": "Why is enum class preferred over plain enum?",
             "options": ["It's shorter", "Scoped and type-safe — no implicit conversion", "It's faster", "It supports strings"],
             "answer": 1, "explain": "enum class prevents accidental comparisons between different enum types."},
        ],
    },
]
