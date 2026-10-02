"""C++ Tutor chapters 9-16 (References through Smart Pointers)."""

CHAPTERS_CPP_B = [
    {
        "id": "cpp09",
        "title": "References",
        "emoji": "🔗",
        "lessons": [
            {
                "title": "References & const References",
                "html": """
<p>Imagine you want to give a variable a second name — not a copy, but
the <i>same</i> object under a different label. That is exactly what a
<b>reference</b> is: an alias for an existing variable. You reach for
references whenever you want a function to modify the caller's data,
or when you want to pass a large object around without paying for a
copy.</p>

<p>How it works: when you write <code>int&amp; ref = x;</code>, the
compiler makes <code>ref</code> another name for <code>x</code>. From
that moment the two names denote one object — anything you do to one,
you do to both. A reference must be initialized when it is created, and
it can never be reseated onto a different variable later.</p>

<p>Walk through the example. We create <code>x</code> holding 10, bind
<code>ref</code> to it, then assign 20 through the reference:</p>

<pre class="code">int x = 10;
int&amp; ref = x;     // ref is an alias for x

ref = 20;         // modifies x!
std::cout &lt;&lt; x;   // 20 — same object!</pre>

<p>Assigning to <code>ref</code> did not touch some copy — it wrote
into <code>x</code> itself, so the printout shows 20. There is exactly
one int in memory; <code>ref</code> and <code>x</code> are two names
for it.</p>

<p><b>Const references</b> (<code>const int&amp;</code>) can read but
not modify, and they have one superpower plain references lack: they
can bind to temporaries and literals:</p>

<pre class="code">const int&amp; cref = 42;    // OK — binds to a temporary
// cref = 99;            // error: read-only

void print(const std::string&amp; s) {   // no copy, no modification
    std::cout &lt;&lt; s;
}</pre>

<p><code>cref</code> binds to the literal 42 (the compiler creates a
temporary and keeps it alive), but writing to it is a compile error.
In the function, the parameter <code>const std::string&amp;</code> uses
the caller's string in place: no copy is made, and the compiler stops
you from modifying it.</p>

<p>Gotchas and rules of thumb:</p>

<ul>
<li>Pass large objects (<code>std::string</code>,
<code>std::vector</code>) by <b>const reference</b>; pass small types
(<code>int</code>, <code>double</code>) by value — copying them is
cheaper than going through a reference.</li>
<li>Returning a reference to a local variable is a dangling bug: the
local dies when the function ends.</li>
<li><code>ref = other;</code> does not reseat the reference — it copies
the <i>value</i> of <code>other</code> into the shared object.</li>
</ul>
""",
                "tryit": """#include <iostream>
#include <string>

void modify(int& ref) { ref *= 2; }
void print(const std::string& s) { std::cout << s << "\\n"; }

int main() {
    int x = 10;
    modify(x);
    std::cout << "x = " << x << "\\n";  // 20

    std::string msg = "Hello from a const reference!";
    print(msg);
    return 0;
}
""",
            },
            {
                "title": "Reference vs Pointer & const with Pointers",
                "html": """
<p>References and pointers look similar — both let you reach an object
through another name — but they behave very differently, and choosing
the right one matters. A <b>reference</b> must be initialized when it
is created, can never be reseated, and is always assumed valid. A
<b>pointer</b> can be null, can be reassigned to point elsewhere, and
supports arithmetic. That flexibility is exactly why pointers can go
wrong.</p>

<p>Rule of thumb: prefer references for function parameters ("this
function needs an object to work with") and reach for a pointer when
"no object yet" is a real state, or when you need to move the pointer
itself around — linked lists, optional targets, array traversal.</p>

<p>The trickiest part is <b>const</b> combined with pointers. C++ can
freeze the pointed-to value, the pointer itself, or both. Read each
declaration <b>right to left</b> and the meaning falls out:</p>

<pre class="code">const int* p1;        // pointer to const int (can't modify *p1)
int* const p2 = &amp;x;  // const pointer to int (can't move p2)
const int* const p3 = &amp;x;  // both const</pre>

<p>Reading right-to-left: <code>p1</code> is "pointer to const int" —
you may move <code>p1</code>, but you cannot write through it.
<code>p2</code> is "const pointer to int" — you may write through it,
but <code>p2</code> is glued to <code>x</code> forever (which is why it
must be initialized on the spot). <code>p3</code> allows neither:
neither moving nor writing.</p>

<p>Common beginner mistakes:</p>

<ul>
<li>Declaring <code>int* p;</code> and using it right away — an
uninitialized pointer holds garbage, and dereferencing it is undefined
behavior. At minimum, write <code>int* p = nullptr;</code>.</li>
<li>Swapping <code>const int*</code> and <code>int* const</code> — the
side of <code>*</code> that <code>const</code> sits on decides what is
frozen.</li>
<li>Expecting <code>ref = other;</code> to rebind a reference — it
compiles, but it assigns values, not bindings.</li>
</ul>
""",
            },
        ],
        "quiz": [
            {"type": "mc", "question": "A reference can be reseated to refer to a different object.",
             "options": ["True", "False"], "answer": 1, "explain": "References are bound at initialization and cannot be changed."},
        ],
    },

    {
        "id": "cpp10",
        "title": "Pointers",
        "emoji": "📍",
        "lessons": [
            {
                "title": "Pointer Basics",
                "html": """
<p>Every variable lives somewhere in memory, and that place has a
number: its address. A <b>pointer</b> is a variable that stores such an
address. This one idea unlocks most of C++ — dynamic memory, arrays,
polymorphism, data structures — so it is worth slowing down here. You
need a pointer when a function must modify the caller's variable, when
an object must outlive its scope, or when several parts of a program
must share one object.</p>

<p>Two operators do all the work. <code>&amp;</code> ("address-of")
turns a variable into its address. <code>*</code> ("dereference") goes
the other way: given an address, it gives you the object living there,
which you can read or write:</p>

<pre class="code">int x = 42;
int* ptr = &amp;x;      // ptr holds the address of x

std::cout &lt;&lt; *ptr;  // 42 — dereference
*ptr = 99;           // modifies x through the pointer
std::cout &lt;&lt; x;      // 99

int* null_ptr = nullptr;  // C++11: always use nullptr, not NULL or 0</pre>

<p>Step by step: <code>ptr</code> holds x's address; <code>*ptr</code>
reads 42 through that address; <code>*ptr = 99</code> writes into that
same memory, so printing <code>x</code> shows 99. One variable, two
ways in. The last line introduces <code>nullptr</code> — the honest
"points to nothing" value. Always initialize pointers; an uninitialized
one holds garbage.</p>

<p>Pointers also support <b>arithmetic</b> — and here is the surprise
worth remembering: adding 1 does not move the address by one byte, it
moves by one <i>element</i>, jumping exactly <code>sizeof(int)</code>
(usually 4) bytes:</p>

<pre class="code">int arr[] = {10, 20, 30, 40};
int* p = arr;        // points to arr[0]
p++;                 // now points to arr[1]
std::cout &lt;&lt; *p;     // 20</pre>

<p>An array name decays to a pointer to its first element, so
<code>p</code> starts on <code>arr[0]</code>; after <code>p++</code> it
lands on <code>arr[1]</code> and the printout is 20. In fact
<code>*(p + i)</code> and <code>arr[i]</code> are the same operation —
subscripting is defined in terms of pointer arithmetic.</p>

<p>Gotchas:</p>

<ul>
<li>Dereferencing <code>nullptr</code> or garbage is undefined behavior
— usually a crash, sometimes silent corruption.</li>
<li><code>p++</code> past the last element walks off the array;
out-of-range positions may be compared but never dereferenced.</li>
<li>Prefer <code>nullptr</code> over <code>NULL</code>/<code>0</code> —
it has a real pointer type, so overloading and type checking work
correctly.</li>
</ul>
""",
                "tryit": """#include <iostream>

int main() {
    int x = 42;
    int* ptr = &x;
    std::cout << "value: " << *ptr << "\\n";
    std::cout << "address: " << ptr << "\\n";

    *ptr = 99;
    std::cout << "after *ptr=99, x = " << x << "\\n";

    int arr[] = {10, 20, 30};
    int* p = arr;
    std::cout << "arr[1] via pointer: " << *(p + 1) << "\\n";
    return 0;
}
""",
            },
        ],
        "quiz": [
            {"type": "mc", "question": "What does *ptr do?",
             "options": ["Declares a pointer", "Dereferences (reads the value at the address)", "Gets the address", "Nothing"],
             "answer": 1, "explain": "* is the dereference operator when used on an existing pointer."},
            {"type": "blank", "question": "The C++11 keyword for a null pointer is <code>____</code>.",
             "answers": ["nullptr"], "explain": "Always use nullptr, not NULL or 0."},
        ],
    },

    {
        "id": "cpp11",
        "title": "Classes & Objects",
        "emoji": "🏛️",
        "lessons": [
            {
                "title": "Class Basics & Access Specifiers",
                "html": """
<p>So far your data and functions have lived apart: a health variable
here, a function that damages it there, and nothing stopping any line
of code from setting health to -500. A <b>class</b> fixes this by
bundling data (<b>members</b>) and the functions that operate on it
(<b>methods</b>) into one type, with <b>access specifiers</b> deciding
who may touch what. This is the foundation of object-oriented C++.</p>

<p>The pattern to internalize: keep data <code>private</code> so only
class code can see it, and expose a <code>public</code> interface of
safe operations. Then no outsider can push the object into a bad state,
because every change goes through your rules:</p>

<pre class="code">class Player {
private:               // only accessible inside the class
    int health;
    std::string name;

public:                // accessible from anywhere
    Player(std::string n, int h) : name(n), health(h) {}

    void takeDamage(int dmg) {
        health -= dmg;
        if (health &lt; 0) health = 0;
    }

    void print() const {      // const: doesn't modify the object
        std::cout &lt;&lt; name &lt;&lt; ": " &lt;&lt; health &lt;&lt; " HP\\n";
    }
};

Player hero("Hero", 100);
hero.takeDamage(30);
hero.print();      // "Hero: 70 HP"</pre>

<p>Follow the flow: the constructor initializes <code>name</code> and
<code>health</code>; <code>takeDamage</code> subtracts and clamps at 0,
so health can never go negative; <code>print</code> shows the state.
After <code>hero.takeDamage(30)</code> the output is "Hero: 70 HP".
The <code>const</code> after <code>print()</code> is a promise that the
method only reads — and it lets the method be called on const
objects.</p>

<p>The three specifiers, one line each:</p>

<ul>
<li><b>private</b> — the default for classes; visible only inside the
class. Encapsulation lives here.</li>
<li><b>public</b> — visible everywhere; this is the class's
interface.</li>
<li><b>protected</b> — like private, but derived classes can see it
too (relevant once inheritance appears).</li>
</ul>

<p>Gotchas:</p>

<ul>
<li>Forgetting <code>public:</code> leaves everything private, and the
compiler rejects every call — a very common first-compile surprise.</li>
<li>A <b>struct</b> is the same thing as a class except its default
access is <code>public</code>.</li>
<li>Mark every read-only method <code>const</code> — retrofitting
const-correctness later is painful.</li>
</ul>
""",
            },
        ],
        "quiz": [
            {"type": "mc", "question": "The default access level for class members is:",
             "options": ["public", "private", "protected", "internal"],
             "answer": 1, "explain": "Classes default to private for encapsulation."},
            {"type": "blank", "question": "A ____ member function promises not to modify the object.",
             "answers": ["const"], "explain": "void print() const — const at the end means read-only."},
        ],
    },

    {
        "id": "cpp12",
        "title": "Constructors & Destructors",
        "emoji": "🏗️",
        "lessons": [
            {
                "title": "Constructors & Member Init List",
                "html": """
<p>When an object is born, something must give its members real values —
otherwise <code>health</code> starts as garbage. The <b>constructor</b>
is a special method that runs automatically at creation: same name as
the class, no return type. The <b>destructor</b>
(<code>~ClassName</code>) is its mirror; it runs automatically when the
object dies. Together they let a class manage its own lifetime — the
idea nearly all resource-managing C++ is built on.</p>

<p>The preferred way to initialize members is the <b>member
initialization list</b> — the <code>: name(n), health(h)</code> part
after the parameter list. Members are constructed directly with their
final values instead of being default-built and then assigned.
<code>const</code> members and reference members <i>require</i> this
list:</p>

<pre class="code">class Player {
    std::string name;
    int health;
public:
    // member init list (preferred — direct initialization)
    Player(std::string n, int h) : name(n), health(h) {}

    // delegating constructor
    Player() : Player("Unknown", 100) {}

    // default (compiler-generated if not declared)
    Player() = default;

    // deleted — prevent copying
    Player(const Player&amp;) = delete;
};</pre>

<p>This block packs four tools: the init list; a <b>delegating</b>
constructor that forwards to another constructor so defaults live in
one place; <code>= default</code>, which keeps the compiler-generated
version explicitly; and <code>= delete</code>, which forbids copying.
(The two <code>Player()</code> lines are alternatives — pick one, not
both.)</p>

<p>Destructors run in a beautifully reliable place — scope exit:</p>

<pre class="code">class Resource {
public:
    Resource()  { std::cout &lt;&lt; "acquired\\n"; }
    ~Resource() { std::cout &lt;&lt; "released\\n"; }  // destructor
};

void demo() {
    Resource r;
}   // destructor called here — automatic cleanup!</pre>

<p>When <code>demo()</code> ends — by reaching the closing brace
<i>or</i> by an exception unwinding — the destructor prints
"released". You never call it by hand. This guaranteed
acquire-in/release-out pairing is called RAII, and chapter 17 turns it
into a design philosophy.</p>

<p>Gotchas:</p>

<ul>
<li>Members initialize in <b>declaration order</b>, not in the order
you write the init list — keep the two orders identical.</li>
<li>Declaring any constructor removes the compiler's default one; add
<code>Player() = default;</code> if you still want it.</li>
<li>Never call a destructor manually — the same object will be
destroyed again at scope exit, which is undefined behavior.</li>
</ul>
""",
            },
        ],
        "quiz": [
            {"type": "mc", "question": "When is a destructor called?",
             "options": ["When the object is created", "Automatically when the object goes out of scope", "Only with delete", "Never"],
             "answer": 1, "explain": "Destructors run automatically at scope exit — the foundation of RAII."},
        ],
    },

    {
        "id": "cpp13",
        "title": "Encapsulation & Class Design",
        "emoji": "🔒",
        "lessons": [
            {
                "title": "Encapsulation, Getters & Setters",
                "html": """
<p><b>Encapsulation</b> is the discipline of hiding data and exposing
behavior. The goal is not secrecy — it is <b>invariants</b>: rules that
must always hold, like "a balance is never negative". If
<code>balance</code> is public, any stray line can set it to -9999 and
break the class's meaning. If it is private and every change passes
through methods that enforce the rules, violating them becomes
impossible:</p>

<pre class="code">class BankAccount {
    double balance = 0;   // invariant: balance >= 0
public:
    void deposit(double amount) {
        if (amount &gt; 0) balance += amount;
    }
    bool withdraw(double amount) {
        if (amount &gt; balance) return false;
        balance -= amount;
        return true;
    }
    double getBalance() const { return balance; }
};</pre>

<p>Watch how the class defends itself: <code>deposit</code> rejects
negative amounts, <code>withdraw</code> refuses to overdraw and reports
success as a <code>bool</code>, and <code>getBalance</code> is
<code>const</code> — read-only access. Notice what is <i>missing</i>:
no public <code>setBalance</code>, because "set the balance to
anything" would destroy the invariant. Design getters and setters by
asking "which rules must survive?" and expose only operations that
preserve them.</p>

<p>Two more tools round out class design. <b>Static members</b> belong
to the class itself, not to any single object — one shared copy,
addressed as <code>MathHelper::counter</code>. A <b>friend</b>
declaration deliberately punches a hole in encapsulation for one named
outsider:</p>

<pre class="code">class MathHelper {
public:
    static int counter;      // class-level variable
    static int add(int a, int b) { return a + b; }
};
int MathHelper::counter = 0;

class A { friend class B; };  // B can access A's private members</pre>

<p>Statics need a two-step dance: declare inside the class, then define
once outside (<code>int MathHelper::counter = 0;</code>). Static
methods have no <code>this</code>, so they cannot touch ordinary
members — <code>add</code> works only on its arguments.
<code>friend class B;</code> lets B reach A's private members; it is
mostly used for operators and tightly-coupled helper classes.</p>

<p>Gotchas:</p>

<ul>
<li>Do not generate a getter/setter pair for every member on autopilot
— that is encapsulation in name only.</li>
<li>Keep friends rare: every friend is one more piece of code your
invariants must trust.</li>
<li>The in-class initializer (<code>double balance = 0;</code>) sets
the starting value for any constructor that does not set the member
explicitly.</li>
</ul>
""",
            },
        ],
        "quiz": [
            {"type": "mc", "question": "Encapsulation means:",
             "options": ["Making everything public", "Hiding data, exposing a controlled interface", "Using pointers", "Inheriting from base classes"],
             "answer": 1, "explain": "Private data + public methods that enforce invariants."},
        ],
    },

    {
        "id": "cpp14",
        "title": "Inheritance",
        "emoji": "🧬",
        "lessons": [
            {
                "title": "Inheritance & Method Overriding",
                "html": """
<p>Inheritance answers a recurring problem: several types share the
same core — every animal has a name, every widget can be drawn — and
you do not want to write that core three times. A <b>derived class</b>
inherits all members of its <b>base class</b>, adds its own, and may
<b>override</b> inherited behavior with its own version. The base
describes what all animals can do; each derived class decides how.</p>

<p>How it works: mark a base method <code>virtual</code> to say
"derived classes may replace this". The derived class writes the same
signature plus <code>override</code>, and the compiler now verifies
that a base method with exactly this signature exists. A typo in the
name or a missing <code>const</code> becomes a compile error instead of
a silent bug:</p>

<pre class="code">class Animal {
public:
    virtual void speak() const { std::cout &lt;&lt; "...\\n"; }
    virtual ~Animal() = default;   // ALWAYS virtual destructor!
};

class Dog : public Animal {
public:
    void speak() const override {    // override = compiler checks
        std::cout &lt;&lt; "Woof!\\n";
    }
};

class Cat : public Animal {
public:
    void speak() const override { std::cout &lt;&lt; "Meow!\\n"; }
};</pre>

<p><code>Dog</code> and <code>Cat</code> both replace
<code>Animal::speak</code>. Each <code>override</code> keeps the exact
signature — change one character and the compiler complains. The line
<code>virtual ~Animal() = default;</code> is not decoration: when you
delete a <code>Dog</code> through an <code>Animal*</code>, a
non-virtual destructor would destroy only the Animal part — undefined
behavior. With a virtual base destructor, the whole object is destroyed
correctly, every time.</p>

<p>Two more rules worth knowing now:</p>

<ul>
<li><code>final</code> stops further overriding — write
<code>void speak() const final</code> on a method, or
<code>class Dog final : public Animal</code> on a whole class.</li>
<li>The <code>public</code> in <code>class Dog : public Animal</code>
matters: class inheritance defaults to <code>private</code>, which
would hide everything inherited — forgetting that keyword is a classic
silent mistake.</li>
</ul>
""",
            },
        ],
        "quiz": [
            {"type": "blank", "question": "The keyword that tells the compiler to check you're actually overriding is <code>____</code>.",
             "answers": ["override"], "explain": "void speak() const override — compiler verifies the base has a virtual speak."},
        ],
    },

    {
        "id": "cpp15",
        "title": "Polymorphism",
        "emoji": "🎭",
        "lessons": [
            {
                "title": "Virtual Functions & Polymorphism",
                "html": """
<p>Here is the problem polymorphism solves: you hold a mixed list of
animals and want to call <code>speak()</code> on each — without asking
"dog or cat?" first. <b>Polymorphism</b> means "many forms": one call
site, many implementations, and the right one chosen <i>at runtime</i>
from the object's real type. Without it, you end up sprinkling
switch-on-type code everywhere and forgetting a case with every new
animal.</p>

<p>The mechanics: a <b>pure virtual</b> function — declared with
<code>= 0</code> instead of a body — is an operation the base class
refuses to implement. That makes <code>Animal</code> <b>abstract</b>:
you cannot create an Animal, only dogs and cats, and every derived
class is forced to supply the missing piece:</p>

<pre class="code">class Animal {
public:
    virtual void speak() const = 0;   // pure virtual = abstract
    virtual ~Animal() = default;
};

class Dog : public Animal {
public:
    void speak() const override { std::cout &lt;&lt; "Woof!\\n"; }
};

class Cat : public Animal {
public:
    void speak() const override { std::cout &lt;&lt; "Meow!\\n"; }
};

// polymorphic call — the RIGHT speak() is called at runtime
Animal* animals[] = { new Dog(), new Cat() };
for (Animal* a : animals) {
    a-&gt;speak();    // "Woof!" then "Meow!"
}</pre>

<p>The interesting part is the loop. The array holds
<code>Animal*</code> pointers, yet <code>a-&gt;speak()</code> runs
Dog's version for the dog and Cat's for the cat. Each object secretly
carries a table of its virtual functions, and the call is dispatched
through the object itself — the same line of source produces different
behavior per element. That is the entire payoff.</p>

<p>An abstract class with only pure virtual functions is an
<b>interface</b>: a pure contract with no data. Code written against
the interface keeps working for every class that implements it —
including classes that do not exist yet.</p>

<p>Gotchas:</p>

<ul>
<li>Always write <code>override</code> on derived versions. Without it,
a signature mismatch silently creates a <i>new</i> function, and the
base's version runs instead — a bug that hides until runtime.</li>
<li>Keep the virtual destructor in every polymorphic base; deleting
through <code>Animal*</code> without one is undefined behavior.</li>
<li>Virtual dispatch needs a pointer or reference. Calling
<code>speak()</code> through a plain <code>Animal</code> value slices
the object and always calls Animal's version.</li>
</ul>
""",
            },
        ],
        "quiz": [
            {"type": "blank", "question": "A virtual function with = 0 is called a ____ virtual function.",
             "answers": ["pure"], "explain": "Pure virtual = 0 makes the class abstract."},
            {"type": "mc", "question": "Why does a base class need a virtual destructor?",
             "options": ["It doesn't", "So delete through a base pointer correctly destroys derived objects", "For performance", "For encapsulation"],
             "answer": 1, "explain": "Without virtual destructor, deleting via base* is undefined behavior."},
        ],
    },

    {
        "id": "cpp16",
        "title": "Dynamic Memory",
        "emoji": "💾",
        "lessons": [
            {
                "title": "new, delete & Memory Leaks",
                "html": """
<p>Variables on the <b>stack</b> die automatically when their scope
ends — perfect for locals, useless when an object must outlive the
function that created it. The <b>heap</b> is the fix: memory you
allocate with <code>new</code> and own until you free it with
<code>delete</code>. Total control — and total responsibility. You
need the heap when a size is only known at runtime, when an object's
lifetime spans multiple functions, or when building self-growing
containers like <code>std::vector</code>.</p>

<p>Two forms exist, and the difference of one character matters
enormously:</p>

<pre class="code">int* p = new int(42);       // allocate
delete p;                    // free — ALWAYS pair with new

int* arr = new int[10];     // array allocation
delete[] arr;                // array delete (note the brackets!)</pre>

<p><code>new int(42)</code> creates one int holding 42 and hands you
its address; <code>delete</code> returns that memory.
<code>new int[10]</code> allocates ten ints in a row and demands
<code>delete[]</code> — the bracket form runs each element's
destructor. Mixing them up (plain <code>delete</code> on an array,
<code>delete[]</code> on a single object) is undefined behavior.</p>

<p>Now the three classic ways this goes wrong. <b>Forget</b>
<code>delete</code>: the allocation stays reserved until the program
exits — a <b>memory leak</b>. Leak inside a loop and the program eats
memory until the OS kills it. <b>Delete twice</b>: undefined behavior,
usually heap corruption that surfaces far from the cause. <b>Use the
pointer after delete</b>: a <b>dangling pointer</b> — the memory may
already have been handed to someone else, so you read garbage or
crash, sometimes much later.</p>

<p>This is exactly why the modern rule exists: <b>never write raw
<code>new</code>/<code>delete</code></b> in application code. Use
<code>std::make_unique</code>/<code>std::make_shared</code>, which free
automatically (chapter 18), and <code>std::vector</code> instead of
<code>new int[n]</code>. Understanding this chapter tells you what
those tools are doing for you under the hood.</p>
""",
            },
        ],
        "quiz": [
            {"type": "mc", "question": "Forgetting delete on a new allocation causes:",
             "options": ["A compile error", "A memory leak", "Automatic cleanup", "A crash immediately"],
             "answer": 1, "explain": "The memory stays allocated until the program exits."},
        ],
    },
]
