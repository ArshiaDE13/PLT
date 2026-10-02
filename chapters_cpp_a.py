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
<p><b>C++</b> is a general-purpose, compiled programming language created by Bjarne Stroustrup in the early 1980s as an extension of C. The idea behind it: keep C's speed and low-level control, but add tools for organizing large programs — classes, generic code, and a large standard library. The name is literally "C incremented". It supports multiple paradigms — procedural, object-oriented, and generic — and C++23 is the current standard.</p>

<p>Three words describe how C++ treats your code:</p>

<ul>
<li><b>Compiled</b> — source code is translated directly to machine code before the program ever runs. Nothing interprets it line by line at runtime.</li>
<li><b>Statically typed</b> — every variable's type is checked at compile time, so type mistakes are caught before you can run anything.</li>
<li><b>Zero-cost abstractions</b> — high-level features (classes, templates, RAII and smart pointers) compile down to machine code as fast as the hand-written version.</li>
</ul>

<p>So where is C++ used? Game engines, operating systems, browsers, embedded systems, financial trading — anywhere the computer must respond in microseconds and every byte of memory is budgeted.</p>

<p>What actually happens when you build a program? Follow the pipeline below from top to bottom:</p>

<pre class="code">Source Code (.cpp)
     ↓
Compiler (g++, clang++)
     ↓
Object Code (.o / .obj)
     ↓
Linker
     ↓
Executable</pre>

<p>You write <b>source code</b> in a <code>.cpp</code> file. The <b>compiler</b> (g++ or clang++) reads it, checks every type and every semicolon, and translates it into <b>object code</b> — raw machine instructions in a <code>.o</code> file. Your file alone is not a program yet: it still needs the standard library and any other units you reference. The <b>linker</b> stitches all of those object files together into one <b>executable</b> you can actually run.</p>

<p>Rules of thumb worth keeping:</p>

<ul>
<li>Most C++ mistakes die at compile time, not in production — the compiler is your first code reviewer.</li>
<li>When compilation fails, read the <i>first</i> error; later errors are usually fallout from it.</li>
<li>"It compiles" and "it works" are different claims — C++ gives you speed, not immunity from logic bugs.</li>
</ul>
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
<p>Every program is a list of instructions, and C++ gives those instructions precise names. A <b>statement</b> is one instruction — "do this" — and it ends with a semicolon. An <b>expression</b> is any combination of values and operators that <i>produces a value</i>. The relationship between them: statements contain expressions. When the program runs, statements execute one after another, top to bottom.</p>

<p>Walk through this example slowly, line by line:</p>

<pre class="code">int x = 5 + 3;    // statement: "5 + 3" is the expression
x = x * 2;         // another statement</pre>

<p>Line 1 does three things in order: the expression <code>5 + 3</code> is evaluated first and produces <code>8</code>; a new <code>int</code> variable named <code>x</code> is created; then <code>8</code> is stored in it. Line 2 reads <code>x</code>, evaluates <code>x * 2</code> — that's <code>16</code> — and writes the result back into <code>x</code>. Before moving on: could you have predicted that <code>x</code> ends at 16? That predicting habit is exactly the skill this course builds.</p>

<p>Comments come in two forms, <code>//</code> (to end of line) and <code>/* */</code> (multi-line) — same as C. The compiler deletes every comment before compiling, so they cost nothing at runtime. They exist for the next reader, which in six months is you.</p>

<p>Where do statements live? Inside functions — and every C++ program starts in <b>main()</b>:</p>

<pre class="code">int main() {
    return 0;
}</pre>

<p>The operating system calls <code>main()</code> when your program launches, and execution begins at its first statement. Its return type is <code>int</code>: the value you return goes back to the operating system, and <code>0</code> is the convention for "finished successfully". Any non-zero value signals that something went wrong.</p>

<p>Common beginner traps:</p>

<ul>
<li>Forgetting a semicolon — the compiler often points at the <i>next</i> line, not the real culprit.</li>
<li><code>=</code> assigns a value; <code>==</code> compares two values. Mixing them up compiles more often than you'd expect.</li>
<li>A lone expression like <code>5 + 3;</code> is a legal statement — it computes 8 and throws the result away.</li>
</ul>
""",
            },
            {
                "title": "Header Files & iostream",
                "html": """
<p>A program that only computes and never talks to anyone is useless. You need a way to print results and read user input — and in C++ that machinery lives in the standard header <code>&lt;iostream&gt;</code> (input/output stream). Header files <i>declare</i> functions and types: they tell the compiler "these things exist". The <code>#include</code> line pastes the header's content into your file before compiling, which is exactly why the compiler then knows what <code>std::cout</code> is.</p>

<p>Read this program line by line and try to predict what it prints:</p>

<pre class="code">#include &lt;iostream&gt;    // input/output streaming

int main() {
    std::cout &lt;&lt; "Output to console\\n";
    int age;
    std::cin &gt;&gt; age;           // read from user
    std::cout &lt;&lt; "You are " &lt;&lt; age &lt;&lt; std::endl;
    return 0;
}</pre>

<p>Line 1 includes the header. Then <code>main()</code> begins. <code>std::cout &lt;&lt; "Output to console\\n"</code> sends text to the console — the <code>&lt;&lt;</code> arrow shows data flowing outward. Next, <code>std::cin &gt;&gt; age</code> pauses and waits for the user to type something; whatever number they enter is extracted (note the arrow now points <i>into</i> the variable) and stored in <code>age</code>. The final line chains three insertions: the fixed text, then the value of <code>age</code>, then <code>std::endl</code>. If the user types 30, the output is <code>You are 30</code>.</p>

<p>Here is the cast, piece by piece:</p>

<ul>
<li><code>std::cout</code> — character output (the console)</li>
<li><code>std::cin</code> — character input (the keyboard)</li>
<li><code>std::endl</code> — newline + flush</li>
<li><code>&lt;&lt;</code> — insertion operator (streams data out)</li>
<li><code>&gt;&gt;</code> — extraction operator (streams data in)</li>
</ul>

<p>What is that <code>std::</code> prefix? Everything in the standard library lives inside the namespace <code>std</code> ("standard"), and the prefix tells the compiler where to look. You will type it a lot — that is deliberate: it keeps library names from colliding with names you invent.</p>

<ul>
<li>Forgetting <code>#include &lt;iostream&gt;</code> produces errors like "cout was not declared" — the fix is the include, not cout.</li>
<li>Inside loops prefer <code>"\\n"</code>; <code>std::endl</code> also flushes the output buffer every time, which is slower.</li>
<li><code>std::cin &gt;&gt; age</code> stops at the first space — it reads one "word", not a whole line.</li>
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
<p>A <b>variable</b> is a named slot of memory that holds a value of a fixed type. Before you use one, you should <b>initialize</b> it — give it its first value. C++ offers three forms of initialization, and they are not interchangeable: each has different rules about which conversions it accepts. Choosing the right form is one of the cheapest safety wins in the language.</p>

<p>Study the three forms, then the difference between them:</p>

<pre class="code">int a = 10;     // copy initialization
int b{20};      // list (uniform) initialization — prevents narrowing!
int c(30);      // direct initialization

// narrowing is blocked by {} — this is a compile error:
// int x{3.14};  // error: narrowing conversion

int d = 3.14;   // OK but SILENTLY truncates to 3 (bad!)</pre>

<p>The first line is <b>copy initialization</b>: the value on the right is copied into <code>a</code>. The second is <b>list initialization</b> (also called uniform initialization) using braces. The third is <b>direct initialization</b> with parentheses. All three produce a working <code>int</code> here — so why prefer braces? Look at the last two lines of the block. <code>int x{3.14}</code> is a <i>compile error</i>, because braces refuse <b>narrowing conversions</b> — conversions that silently throw information away. But <code>int d = 3.14</code> compiles without a peep and silently truncates to <code>3</code>. No error, no warning at runtime — just a wrong value flowing through your program. That is the exact bug class braces exist to prevent.</p>

<p>Modern C++ style therefore prefers list initialization: if the value fits, <code>{}</code> behaves exactly like <code>=</code>; if it doesn't, the compiler stops you at build time instead of letting the bug run.</p>

<p>You can also declare several variables in one statement:</p>

<pre class="code">int x = 1, y = 2, z = 3;   // legal but less readable</pre>

<p>This is legal — <code>x</code> gets 1, <code>y</code> gets 2, <code>z</code> gets 3, each with its own initializer. It saves typing but hurts readability and makes it easy to initialize one variable and forget another. Most style guides (and most teams) prefer one declaration per line.</p>

<p>Gotchas worth memorizing:</p>

<ul>
<li>A variable declared without an initializer (just <code>int n;</code>) holds garbage — reading it is undefined behavior.</li>
<li>Braces block narrowing; <code>=</code> and <code>()</code> allow it silently.</li>
<li>Truncation cuts toward zero: <code>3.9</code> becomes <code>3</code>, and <code>-3.9</code> becomes <code>-3</code>.</li>
</ul>
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
<p>Every variable in C++ has a type, and the type decides two things: how many bytes the object occupies and which values fit inside it. Pick a type that is too small and values overflow; pick one needlessly large and you waste memory. So a working programmer knows the fundamental types the way a carpenter knows their tools. They come in families:</p>

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

<p>The <code>sizeof</code> operator answers the size question for your exact platform — no guessing:</p>

<pre class="code">int s = -42;              // signed (default)
unsigned int u = 42;      // unsigned (0 to ~4 billion)

sizeof(int)      // 4 bytes
sizeof(double)   // 8 bytes
sizeof(bool)     // 1 byte</pre>

<p>Read the output as a budget. <code>sizeof(int)</code> is 4 bytes — 32 bits — which is why a signed <code>int</code> tops out around ±2.1 billion. <code>double</code> spends its 8 bytes on precision, roughly 15-17 significant decimal digits, which is why it is the default choice for decimals. <code>bool</code> needs only one byte even though it holds just two states. In the first lines of the block, <code>s</code> is <b>signed</b> (the default), so -42 is fine; <code>u</code> is <b>unsigned</b> — it gives up negatives and in return covers 0 to about 4.29 billion.</p>

<p>Things that surprise beginners:</p>

<ul>
<li>These sizes are typical, not guaranteed — the standard only fixes minimums. <code>char</code> is the one type that is exactly 1 byte by definition.</li>
<li>Unsigned arithmetic wraps around: <code>0u - 1</code> is <code>4294967295</code>, not -1.</li>
<li>Signed overflow is undefined behavior — the compiler is allowed to assume it never happens.</li>
<li>Rule of thumb: <code>int</code> for counting, <code>double</code> for decimals, and don't reach for <code>unsigned</code> just because values "can't be negative".</li>
</ul>
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
<p>Arithmetic is the first thing any language must do well, and C++ hands you a compact operator set — essentially C's, plus a few C++ conveniences. Five operators cover basic math, five <i>compound</i> operators cover "update this variable in place", and the increment/decrement family handles the most common update of all: adding or subtracting 1. These appear in virtually every line of real code, so learn them properly now.</p>

<p>Read the block top to bottom, tracking the value of <code>a</code> as you go:</p>

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

<p>Start with <code>a = 10, b = 3</code>. Addition, subtraction, multiplication behave as expected: 13, 7, 30. Then come the two that bite beginners. <code>a / b</code> is <code>3</code>, not 3.33 — when both operands are integers, C++ performs <b>integer division</b> and truncates the fraction. And <code>a % b</code> is <code>1</code>, because 10 = 3 × 3 + 1: the modulo operator returns the remainder. Now the compound section — each line reads "modify <code>a</code> using its own value" — and since they run in order, watch <code>a</code> change: <code>a += 5</code> makes 15, <code>a -= 2</code> makes 13, <code>a *= 3</code> makes 39, <code>a /= 4</code> truncates to 9 (integer division again!), and <code>a %= 7</code> leaves 2. Finally the increment family: both <code>++a</code> and <code>a++</code> add 1 to <code>a</code>, but as <i>expressions</i> they differ — pre-increment yields the new value, post-increment hands you the old one and updates afterward.</p>

<p>That pre/post distinction deserves a concrete rule. On a line of its own, <code>a++;</code> and <code>++a;</code> are identical. Inside a larger expression, <code>int c = a++;</code> copies the <i>old</i> value into <code>c</code>, while <code>int d = ++a;</code> copies the <i>new</i> one. When in doubt, use pre-increment — it never surprises.</p>

<ul>
<li><code>7 / 2</code> is 3. For 3.5, make one operand floating-point: <code>7.0 / 2</code>.</li>
<li>Modulo with negatives: the result takes the sign of the left operand (<code>-7 % 3</code> is -1).</li>
<li>Integer division by zero is undefined behavior — check your divisor.</li>
</ul>
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
<p>Three operator families drive decision-making and bit-level work. <b>Comparison</b> operators (<code>== != &lt; &gt; &lt;= &gt;=</code>) ask yes/no questions and produce a <code>bool</code>. <b>Logical</b> operators (<code>&amp;&amp;</code> AND, <code>||</code> OR, <code>!</code> NOT) combine those yes/no answers into bigger conditions — with short-circuiting. <b>Bitwise</b> operators (<code>&amp;</code> AND, <code>|</code> OR, <code>^</code> XOR, <code>~</code> NOT, <code>&lt;&lt;</code> shift left, <code>&gt;&gt;</code> shift right) ignore numeric meaning and manipulate the raw bits of an integer. Mixing the families up is a classic bug.</p>

<p>The block computes all six bitwise results for <code>a = 12</code> and <code>b = 10</code>. Predict each line before reading the explanation:</p>

<pre class="code">int a = 12, b = 10;   // 1100, 1010
a &amp; b    // 8    (1000)
a | b    // 14   (1110)
a ^ b    // 6    (0110)
~a       // -13
a &lt;&lt; 2   // 48   (110000)
a &gt;&gt; 2   // 3    (11)</pre>

<p>Write both numbers in binary: 12 is <code>1100</code>, 10 is <code>1010</code>. AND keeps only bits that are 1 in <i>both</i> numbers: <code>1000</code> = 8. OR keeps bits that are 1 in <i>either</i>: <code>1110</code> = 14. XOR keeps bits where the two differ: <code>0110</code> = 6. NOT flips every bit of 12; in two's-complement arithmetic that lands on <code>-13</code> — a handy identity: <code>~a</code> equals <code>-a - 1</code>. Shifting left by 2 appends two zeros: <code>110000</code> = 48 — each left shift doubles the value. Shifting right by 2 drops the low two bits: <code>11</code> = 3 — each right shift halves the value, discarding remainders.</p>

<p>The logical operators add one more behavior: they <b>short-circuit</b>. <code>&amp;&amp;</code> stops evaluating if its left side is already false; <code>||</code> stops if the left side is already true. That is not just an optimization — it is a control-flow tool. The condition <code>x != 0 &amp;&amp; 10 / x &gt; 2</code> is safe precisely because the division never runs when <code>x</code> is 0.</p>

<ul>
<li><code>&amp;</code> and <code>&amp;&amp;</code> are different operators: bitwise AND versus logical AND. Same for <code>|</code> and <code>||</code>.</li>
<li>Precedence trap: <code>&amp;</code> binds <i>looser</i> than <code>==</code>, so <code>a &amp; b == 8</code> means <code>a &amp; (b == 8)</code>. Parenthesize bit tests.</li>
<li>Precedence, strongest to weakest: <code>* / %</code>, then <code>+ -</code>, then comparisons, then <code>&amp;&amp;</code>, then <code>||</code>. When in doubt, add parentheses — they cost nothing.</li>
</ul>
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
<p>Real programs mix types constantly: an <code>int</code> count divided by another <code>int</code>, a <code>double</code> price assigned to a whole-number variable, an expression combining both. C++ permits these mixtures, and the compiler quietly inserts <b>implicit conversions</b> wherever the types don't match. Some of those conversions are safe (widening: <code>int</code> to <code>double</code> loses nothing); some destroy data (narrowing: <code>double</code> to <code>int</code> chops the fraction off). Knowing which is which is the whole game.</p>

<p>Watch both kinds in action:</p>

<pre class="code">// implicit (compiler does it)
int i = 3.99;           // 3 — silently truncates!
double d = 5;           // 5.0

// explicit — the C++ way: static_cast
double pi = 3.14159;
int truncated = static_cast&lt;int&gt;(pi);     // 3
double exact = static_cast&lt;double&gt;(7) / 2; // 3.5 (not 3!)

// C-style cast (avoid — no type checking)
int old = (int)pi;</pre>

<p>The first section is the compiler working alone. <code>int i = 3.99;</code> compiles — and <code>i</code> becomes <code>3</code>. No warning at runtime, no exception: the fraction is simply gone. Meanwhile <code>double d = 5;</code> is harmless widening — 5 becomes 5.0 and nothing is lost. The middle section is <i>you</i> taking responsibility: <code>static_cast&lt;int&gt;(pi)</code> converts 3.14159 to 3 — the same truncation, but now the conversion is loud, visible, and searchable in the code. The line to really study is the next one: <code>static_cast&lt;double&gt;(7) / 2</code> gives <code>3.5</code>, not 3. The cast runs <i>first</i>, turning 7 into 7.0, and only then does the division happen — and 7.0 / 2 is floating-point division. Compare the C-style cast <code>(int)pi</code> at the bottom: same effect, but impossible to grep for and unchecked in complex cases.</p>

<p>Here is the mistake that costs beginners hours. You write <code>double avg = total / count;</code> where both <code>total</code> and <code>count</code> are integers — so <code>total / count</code> is <i>integer division</i> and truncates <i>before</i> the result is ever handed to the <code>double</code>. Storing it in a <code>double</code> comes too late; the damage is already done. The fix is to cast one operand first, exactly as the example does for <code>exact</code>.</p>

<ul>
<li>Cast to floating-point <i>before</i> dividing, not after.</li>
<li>Prefer <code>static_cast&lt;&gt;</code> over C-style casts: type-checked and grep-able.</li>
<li>Narrowing conversions (double→int, long→int) always risk data loss — make them explicit.</li>
</ul>
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
<p>A program that runs the same way every time is barely a program. Real software makes decisions: if the score is high, print a grade; if the user picked option 2, run that feature. C++ gives you two main tools for this. <code>if</code>/<code>else</code> evaluates a condition and picks a branch — best for ranges and complex tests. <code>switch</code> compares one expression against a list of constant values — best when one variable has a handful of discrete cases.</p>

<p>Read the block and predict what prints for <code>score = 85</code>:</p>

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

<p>The <code>if</code> chain checks conditions top to bottom and runs the <i>first</i> true branch only. For a score of 85: <code>score &gt;= 90</code> is false, <code>score &gt;= 80</code> is true, so <code>B</code> prints and the chain ends — the final <code>else</code> never runs. Notice the trick in the ordering: by checking the highest threshold first, each branch needs only one comparison. In the <code>switch</code>, the value of <code>choice</code> is matched against each <code>case</code> label; on a match, execution jumps there and runs until it hits <code>break</code>, which exits the switch. If nothing matches, <code>default</code> runs — its job is "none of the above". The last lines show a C++17 feature: <code>if (auto value = getValue(); value &gt; 10)</code> declares <code>value</code> inside the if itself. That variable exists only within this if/else — it cannot leak into the rest of the function, which keeps names local and intentions clear.</p>

<p>Beginners fall into the same pits here every year:</p>

<ul>
<li>Missing <code>break</code> in a switch: execution <i>falls through</i> into the next case. Deliberate fall-through is legal but rare — comment it when you mean it.</li>
<li><code>if (x = 5)</code> assigns instead of comparing — the condition becomes 5, which counts as true. Write <code>==</code>.</li>
<li><code>switch</code> needs integer-like values (ints, chars, enums). For strings or ranges, use <code>if</code>/<code>else</code>.</li>
<li>Prefer brace blocks even for single statements — future-you will add a line there someday.</li>
</ul>
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
<p>Computers earn their keep by repeating work a million times without complaint. C++ gives you four ways to loop — the skill is picking the right one: <code>while</code> when you don't know how many rounds you need; <code>do...while</code> when the body must run at least once; <code>for</code> when you do know the count (or have a counter); and the <b>range-based for</b> (C++11) when you just want each element. All four re-test a condition every round, and all four can be cut short with <code>break</code> or skip a round with <code>continue</code>.</p>

<p>Walk each example and predict its output before reading on:</p>

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

<p>The <code>while</code> loop prints <code>0 1 2 3 4</code>: the condition <code>i &lt; 5</code> is tested <i>before</i> every pass, so if <code>i</code> had started at 5, the body would never run at all. The <code>do...while</code> is the opposite — the body executes <i>first</i>, then the condition is checked. That's why with <code>j = 100</code> it prints <code>100</code> once even though <code>100 &lt; 5</code> is false — the guaranteed first pass is why menus use this form. The <code>for</code> loop bundles the same three ingredients onto one line — initialize <code>k</code> to 0, keep going while <code>k &lt; 5</code>, add 1 after each pass — and prints <code>0 1 2 3 4</code>. The range-based for reads as "for each <code>x</code> in this list" — no counter, no index arithmetic, no off-by-one, and it prints <code>1 2 3 4 5</code>. Finally, trace the last loop: n=0 is even, printed; n=1 hits <code>continue</code> and skips the print; odds keep skipping; at n=7, <code>break</code> exits — output <code>0 2 4 6</code>.</p>

<p>Loops fail in the same predictable ways:</p>

<ul>
<li>The classic infinite loop: forgetting to update the counter (<code>i++</code>) inside a <code>while</code>.</li>
<li>Off-by-one errors come from <code>&lt;</code> versus <code>&lt;=</code>. Decide whether the last index is included, then match the operator to it.</li>
<li>Prefer range-based for when you have a container and don't need the index — it eliminates an entire bug class.</li>
<li><code>continue</code> skips only the current round; <code>break</code> leaves the loop for good.</li>
</ul>
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
<p>The moment your program repeats a calculation twice, it is asking for a <b>function</b>: a named, reusable block of code that takes inputs and returns a result. Functions turn copy-pasted logic into a few readable lines. C++ splits the idea in two: a <b>declaration</b> (prototype) tells the compiler a function exists — its name, parameter types, and return type — while a <b>definition</b> supplies the actual body. This split lets you call a function from code that appears before its body is even written.</p>

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

<p>Line by line: the first snippet is the declaration — note the semicolon where the body would be. It is a promise: "a function named <code>add</code> exists, takes two <code>int</code>s, and returns an <code>int</code>". The second snippet keeps that promise with a body that returns <code>a + b</code>. Inside <code>main()</code>, the line <code>int result = add(3, 4);</code> is the <b>call</b>: execution jumps into <code>add</code>, the values 3 and 4 are copied into the parameters <code>a</code> and <code>b</code>, the body computes 7, and <code>return</code> hands 7 back — where it is stored in <code>result</code>. The compiler checked this call against the declaration before the definition was even seen — that is the point of prototypes.</p>

<p>Two vocabulary distinctions the rest of this course leans on. First, <b>parameters</b> are the variables in the declaration (<code>a</code> and <code>b</code>); <b>arguments</b> are the actual values you pass at the call site (<code>3</code> and <code>4</code>). Second, a function that returns nothing declares <code>void</code> — it still runs when called, it just hands back no value.</p>

<p>And one habit to build early: variables created inside a function are <b>local</b> — born when the function starts, destroyed when it returns. Globals are visible everywhere but best avoided: any line in any file can change them, which makes bugs nearly untraceable.</p>

<ul>
<li>Arguments are copied into parameters — modifying <code>a</code> inside <code>add</code> does not change the caller's variable. (Passing by reference, coming later, changes that.)</li>
<li>A missing prototype means the compiler meets the call first and errors out — declare before use.</li>
</ul>
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
<p>Adding two ints and adding two doubles is conceptually the same operation — why make the reader learn two names for it? <b>Function overloading</b> lets you define several functions that share a name but differ in their parameter list (types, count, or both). The compiler examines each call's arguments at compile time and picks the matching version. Overloading plus <b>default arguments</b> — fallback values for parameters the caller omits — keep call sites short and APIs pleasant.</p>

<p>Three overloads of <code>add</code>, and three calls that each resolve differently:</p>

<pre class="code">int add(int a, int b) { return a + b; }
double add(double a, double b) { return a + b; }
int add(int a, int b, int c) { return a + b + c; }

add(1, 2);       // calls int version
add(1.5, 2.5);   // calls double version
add(1, 2, 3);    // calls 3-arg version</pre>

<p>All three functions share the name <code>add</code>. At each call the compiler matches arguments against parameter lists: <code>add(1, 2)</code> passes two ints, so the two-<code>int</code> version runs; <code>add(1.5, 2.5)</code> passes doubles, so the <code>double</code> version runs; <code>add(1, 2, 3)</code> passes three arguments, so the three-parameter version runs. The results are 3, 4.0, and 6. This resolution happens entirely at compile time — there is no runtime searching, no overhead.</p>

<p>Default arguments remove the need to write a one-use overload:</p>

<pre class="code">void greet(std::string name = "guest", int times = 1) {
    for (int i = 0; i &lt; times; i++)
        std::cout &lt;&lt; "Hello, " &lt;&lt; name &lt;&lt; "!\\n";
}

greet();           // "Hello, guest!"
greet("Ada");     // "Hello, Ada!"
greet("Ada", 3);  // 3 times</pre>

<p>Both parameters have defaults: <code>"guest"</code> and <code>1</code>. Call <code>greet()</code> and both defaults fill in — <code>Hello, guest!</code> prints once. Call <code>greet("Ada")</code> and the name is replaced while <code>times</code> keeps its default. Call <code>greet("Ada", 3)</code> and nothing is defaulted — the greeting prints three times. The rule to remember: arguments fill left to right, so defaulted parameters must sit at the <i>end</i> of the parameter list.</p>

<p>Finally, <code>constexpr</code> moves work from runtime to compile time:</p>

<pre class="code">constexpr int square(int n) { return n * n; }
constexpr int s = square(5);  // computed at COMPILE TIME (25)</pre>

<p>When <code>square</code> is called with a constant like 5, the compiler evaluates it <i>during compilation</i> — the binary simply contains 25. In the context shown (initializing a <code>constexpr int</code>), compile-time evaluation is guaranteed, and the runtime cost is zero.</p>

<ul>
<li>You cannot overload on return type alone — <code>int f()</code> and <code>double f()</code> conflict.</li>
<li>Default arguments belong in the declaration (the header), written exactly once.</li>
<li>If two overloads match a call equally well, the compiler reports an ambiguity error rather than guessing.</li>
</ul>
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
<p>Three questions govern every variable: <i>where</i> can its name be used, <i>when</i> does the object exist, and <i>how</i> is its memory allocated? These are three separate concepts — <b>scope</b>, <b>lifetime</b>, and <b>storage duration</b> — and beginners who conflate them write code that "should work". Keep them separate and the compiler's behavior stops being mysterious. Scope is a region of source code; lifetime is a stretch of running time; duration is the strategy by which memory is reserved (automatic, static, or dynamic).</p>

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

<p>Trace each variable through this block. <code>globalVar</code> lives outside any function: its scope is the whole file, and its duration is <b>static</b> — memory reserved before <code>main()</code> runs and held until the program exits. <code>localVar</code> is the opposite: <b>automatic</b> duration — created fresh every time <code>demo()</code> is called, destroyed the instant the function returns. <code>staticVar</code> is the hybrid that surprises people: declared inside the function (block scope!) but with <b>static</b> duration — it is created once, on the first call, and every <code>staticVar++</code> accumulates across calls. Finally, <code>blockVar</code> exists only between its own braces: the moment the inner block ends, the object is destroyed and the name is gone.</p>

<p>The keyword <code>static</code> thus means different things by position: on a <i>local</i> variable it changes duration — created once, persists between calls. On a <i>global</i> variable it changes linkage instead — the name becomes private to this file, invisible to other translation units. Same keyword, two different jobs.</p>

<ul>
<li><b>Shadowing:</b> an inner variable with the same name as an outer one hides it — legal, but a reliable source of confusion. Avoid reusing names.</li>
<li>A <code>static</code> local is initialized exactly once, even if the function runs a thousand times.</li>
<li>Default to the narrowest scope that works: fewer things alive at once means fewer things that can go wrong.</li>
</ul>
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
<p>Whenever you need several values of the same kind — five test scores, twelve months, a board of cells — an array bundles them under one name. C++ inherits two tools for the fixed-size case. The <b>C-style array</b> is the raw, bare-metal version: fast, built into the language, and completely unsupervised. <code>std::array</code> (C++11) wraps the exact same memory in a safer, smarter interface. Both store elements side by side and are indexed from 0 — but they differ sharply in what they know about themselves.</p>

<p>The C-style version first:</p>

<pre class="code">int numbers[5] = {1, 2, 3, 4, 5};
numbers[0] = 10;    // first element
// numbers[5] = 99; // NO bounds check — undefined behavior!</pre>

<p><code>int numbers[5]</code> reserves five consecutive <code>int</code>s, and the initializer fills them 1 through 5. Valid indexes run from <code>0</code> to <code>4</code> — the size is 5, but the last element is <code>numbers[4]</code>, and that asymmetry trips everyone once. The line <code>numbers[0] = 10</code> overwrites the first element, so the array now holds <code>10, 2, 3, 4, 5</code>. The commented-out line is the important one: <code>numbers[5]</code> is past the end, and C-style arrays perform <b>no bounds check</b> — the write would silently corrupt whatever memory sits next door. That is <b>undefined behavior</b>: it may crash, may appear to work, may fail on another machine.</p>

<p><code>std::array</code> keeps the same layout but adds self-knowledge:</p>

<pre class="code">#include &lt;array&gt;

std::array&lt;int, 5&gt; arr = {1, 2, 3, 4, 5};
arr.size()          // 5
arr.at(2)           // 3 (with bounds checking!)
arr.fill(0)         // set all to 0</pre>

<p>The type carries the element type and the size: <code>std::array&lt;int, 5&gt;</code>. Now <code>arr.size()</code> reports 5 — the array knows its own length, which C-style arrays forget the moment you pass them anywhere. <code>arr.at(2)</code> returns the element at index 2 (the value 3), but it <i>checks the index first</i> and throws an exception if you are out of bounds — a loud, debuggable failure instead of silent corruption. <code>arr.fill(0)</code> overwrites every element with 0 in one call.</p>

<p>The modern rule is simple: fixed size known at compile time — <code>std::array</code>; size decided at runtime — <code>std::vector</code>.</p>

<ul>
<li>Use <code>.at()</code> while developing — its exception pinpoints the bad index immediately.</li>
<li>C-style arrays "decay" to a bare pointer when passed to functions, losing their size; <code>std::array</code> does not.</li>
<li>Both are zero-overhead: <code>std::array</code> compiles down to the same memory as the raw array.</li>
</ul>
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
<p>Text seems simple until you store it. C represents a string as an array of <code>char</code> ending with a terminator byte <code>'\\0'</code> — the string "knows" where it ends only because something wrote that byte. Every C-style string bug you have heard of (buffer overflows above all) traces back to that convention. C++ wraps the same idea in <code>std::string</code>: an object that manages its own memory, grows on demand, and offers real operations. Learn both — you will read C-style strings in old code and interfaces forever — but write <code>std::string</code>.</p>

<pre class="code">char name[20] = "Ada";    // C-style — careful with overflow!</pre>

<p><code>char name[20]</code> sets aside 20 bytes and copies in <code>A</code>, <code>d</code>, <code>a</code>, and the invisible <code>'\\0'</code> terminator — 4 bytes used, 16 reserved. The danger: nothing stops you from putting a 25-character name into this 20-byte buffer. The array will happily overflow into neighboring memory — no exception, no error message, just corruption.</p>

<p>Now the C++ way — read the operations and predict each result:</p>

<pre class="code">#include &lt;string&gt;

std::string name = "Ada";
std::string full = name + " Lovelace";   // concatenation
name += " (Byron)";                        // append
full.length()            // length
full.substr(0, 3)        // substring "Ada"
full.find("Love")        // index or npos
full[0]                  // 'A' (character access)
full == "Ada"            // comparison</pre>

<p><code>std::string name = "Ada"</code> creates a string that manages itself. <code>name + " Lovelace"</code> builds a <i>new</i> string — <code>"Ada Lovelace"</code> — without touching <code>name</code>; then <code>name += " (Byron)"</code> appends in place, leaving <code>name</code> as <code>"Ada (Byron)"</code>. <code>full.length()</code> reports the character count (12 for <code>"Ada Lovelace"</code> — the terminator is managed for you and not counted). <code>full.substr(0, 3)</code> copies the 3 characters starting at index 0: <code>"Ada"</code>. <code>full.find("Love")</code> returns the starting index of the first match, or the special constant <code>npos</code> if there is none. <code>full[0]</code> gives the character <code>'A'</code>, and <code>full == "Ada"</code> compares <i>content</i> — character by character — not memory addresses.</p>

<p>Modern C++ always uses <code>std::string</code> over C-style strings, and <code>std::string_view</code> (C++17) adds non-owning read-only views — covered in the Utility Types chapter.</p>

<ul>
<li><code>find()</code> returns <code>npos</code> (a huge unsigned value) on failure — test with <code>!= std::string::npos</code>, never <code>&gt;= 0</code>, which is always true.</li>
<li><code>std::string</code> grows as needed; a <code>char[20]</code> never does.</li>
<li><code>==</code> compares content for <code>std::string</code>, but only addresses for raw <code>char</code> pointers — a classic trap when mixing the two.</li>
</ul>
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
<p>A game has players, a bank has accounts, a chat has messages — and each of those things carries several pieces of data that belong together. Pass them around as loose variables and every function signature grows: <code>printPlayer(name, score, health)</code> becomes <code>createPlayer(name, score, health, level, items...)</code>. A <b>struct</b> solves this by bundling related data into one named type, so a <code>Player</code> is a single value you can create, copy, store, and pass. Structs are the first step from "writing statements" to "modeling the world".</p>

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

<p>Read the block in two halves. The top half is the <b>definition</b> — a blueprint, not memory. It says: the type <code>Player</code> consists of a <code>std::string name</code>, an <code>int score</code>, and a <code>double health</code>. Note the semicolon after the closing brace — forgetting it is a rite of passage. The lower half creates <i>instances</i>. <code>Player p;</code> reserves memory for one player with uninitialized members; the blueprint became an object. The dot operator then reaches inside member by member: <code>p.name = "Hero"</code>, <code>p.score = 100</code>, <code>p.health = 100.0</code>. The next two lines show shorthand: aggregate initialization fills members in declaration order — <code>p2</code> is a player named "Mage" with score 50 and health 75.0, and <code>p3</code> is the brace form of the same idea. Finally, <code>print</code> takes <code>const Player&amp;</code> — a <b>const reference</b>: the function sees the caller's actual object (no copy is made) but is forbidden from modifying it. For anything bigger than a couple of ints, pass structs this way.</p>

<ul>
<li>The struct definition needs its trailing semicolon — <code>};</code>.</li>
<li>Passing a struct <i>by value</i> copies every member (including strings); <code>const&amp;</code> avoids the copy.</li>
<li>Aggregate initialization matches members by <i>position</i> — reorder the struct and every initializer silently means something new.</li>
</ul>
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
<p>Code littered with bare numbers — <code>if (state == 3)</code> — is code nobody can review. What is 3? Where did 2 go? <b>Enums</b> fix this by giving names to a fixed set of values: a color is red, green, or blue, and nothing else. C++ has two enum flavors, and the difference between them is a small case study in language design. <b>Type aliases</b> solve the neighboring problem: types whose names have grown too long to read.</p>

<p>Plain <code>enum</code> first — and its sharp edges:</p>

<pre class="code">enum Color { Red, Green, Blue };   // Red=0, Green=1, Blue=2
Color c = Green;
int n = c;     // OK — implicitly converts (can be dangerous!)</pre>

<p>The compiler assigns values left to right: <code>Red = 0</code>, <code>Green = 1</code>, <code>Blue = 2</code>. But this flavor is <b>unscoped</b>: the names <code>Red</code>, <code>Green</code>, <code>Blue</code> are dumped into the surrounding scope — so a second enum nearby with a <code>Green</code> member is an immediate name collision. Worse, the last line compiles: a <code>Color</code> silently converts to plain <code>int</code>, meaning any function expecting a number will happily accept a color. That permissiveness is exactly what goes wrong in large codebases.</p>

<p><code>enum class</code> (C++11) closes both holes:</p>

<pre class="code">enum class Color { Red, Green, Blue };
enum class Fruit { Apple, Orange };

Color c = Color::Green;
// int n = c;              // ERROR — no implicit conversion!
// if (c == Fruit::Apple)  // ERROR — different types!
int n = static_cast&lt;int&gt;(c);  // explicit only</pre>

<p>Now the members live <i>inside</i> the enum: you must write <code>Color::Green</code>, so two enums can both define <code>Green</code> without conflict. The implicit conversion is gone too: <code>int n = c;</code> is now a compile error, and comparing a <code>Color</code> with a <code>Fruit</code> is also a compile error — two different types, no accidental mixing. When you genuinely need the number, you say so explicitly: <code>static_cast&lt;int&gt;(c)</code>.</p>

<p>Type aliases give existing types a new name:</p>

<pre class="code">using Score = int;         // modern (preferred)
typedef int Score;          // legacy (same effect)

using PlayerMap = std::map&lt;std::string, Player&gt;;  // much cleaner!</pre>

<p><code>using Score = int;</code> reads as "Score is another name for int" — and the modern <code>using</code> form is preferred over legacy <code>typedef</code> (they are otherwise equivalent). The real payoff is the last line: <code>PlayerMap</code> replaces a nested template spelling with a single readable name, and every future change to that type is made in exactly one place.</p>

<ul>
<li>Default to <code>enum class</code>; use plain <code>enum</code> only when you specifically want implicit int conversion.</li>
<li>Default to <code>using</code> over <code>typedef</code> — clearer to read and works with templates.</li>
</ul>
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
