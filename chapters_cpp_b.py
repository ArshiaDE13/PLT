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
<p>A <b>reference</b> is an alias — another name for an existing variable.
Once bound, it can never refer to a different object:</p>

<pre class="code">int x = 10;
int&amp; ref = x;     // ref is an alias for x

ref = 20;         // modifies x!
std::cout &lt;&lt; x;   // 20 — same object!</pre>

<p><b>Const references</b> can read but not modify — they can also bind
to temporaries and literals:</p>

<pre class="code">const int&amp; cref = 42;    // OK — binds to a temporary
// cref = 99;            // error: read-only

void print(const std::string&amp; s) {   // no copy, no modification
    std::cout &lt;&lt; s;
}</pre>

<p>Pass-by-const-reference is the standard way to pass large objects
(no copy overhead, can't accidentally modify). Pass-by-value for small
types (int, double).</p>
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
<p>References and pointers both "point to" objects, but differ:</p>

<ul>
<li>References must be initialized and can't be reseated</li>
<li>Pointers can be null, reassigned, and do arithmetic</li>
<li>References are safer for function parameters</li>
</ul>

<p><b>const with pointers</b> — three combinations, read right-to-left:</p>

<pre class="code">const int* p1;        // pointer to const int (can't modify *p1)
int* const p2 = &amp;x;  // const pointer to int (can't move p2)
const int* const p3 = &amp;x;  // both const</pre>
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
<p>A <b>pointer</b> stores the memory address of another variable:</p>

<pre class="code">int x = 42;
int* ptr = &amp;x;      // ptr holds the address of x

std::cout &lt;&lt; *ptr;  // 42 — dereference
*ptr = 99;           // modifies x through the pointer
std::cout &lt;&lt; x;      // 99

int* null_ptr = nullptr;  // C++11: always use nullptr, not NULL or 0</pre>

<p><b>Pointer arithmetic</b> — advances by sizeof(element), not by 1 byte:</p>

<pre class="code">int arr[] = {10, 20, 30, 40};
int* p = arr;        // points to arr[0]
p++;                 // now points to arr[1]
std::cout &lt;&lt; *p;     // 20</pre>
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
<p>A <b>class</b> bundles data (members) and behaviour (methods) with
access control:</p>

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

<ul>
<li><b>private</b> — default for classes; encapsulation</li>
<li><b>public</b> — the interface</li>
<li><b>protected</b> — like private, but visible to derived classes</li>
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
<p><b>Constructors</b> initialize objects. The <b>member initialization
list</b> is the preferred way:</p>

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

<p><b>Destructors</b> clean up when objects die — called automatically
at scope exit:</p>

<pre class="code">class Resource {
public:
    Resource()  { std::cout &lt;&lt; "acquired\\n"; }
    ~Resource() { std::cout &lt;&lt; "released\\n"; }  // destructor
};

void demo() {
    Resource r;
}   // destructor called here — automatic cleanup!</pre>
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
<p><b>Encapsulation</b> = hide data, expose behaviour. Members are
private; the public interface enforces invariants:</p>

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

<p><b>Static members</b> belong to the class; <b>friend</b> grants
access to private members:</p>

<pre class="code">class MathHelper {
public:
    static int counter;      // class-level variable
    static int add(int a, int b) { return a + b; }
};
int MathHelper::counter = 0;

class A { friend class B; };  // B can access A's private members</pre>
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

<p>Always use <code>override</code> (compiler catches mistakes) and
<code>final</code> (prevent further overriding). Always use a
<b>virtual destructor</b> in base classes — otherwise deleting through
a base pointer is undefined behavior.</p>
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
<p><b>Polymorphism</b> — one interface, many implementations. Virtual
functions enable runtime dispatch:</p>

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

<p><b>Pure virtual</b> (= 0) makes the class abstract — can't be
instantiated. Derived classes MUST implement it. An abstract class with
only pure virtual functions is an <b>interface</b>.</p>
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
<p>Dynamic memory lives on the <b>heap</b> (vs stack for locals):</p>

<pre class="code">int* p = new int(42);       // allocate
delete p;                    // free — ALWAYS pair with new

int* arr = new int[10];     // array allocation
delete[] arr;                // array delete (note the brackets!)</pre>

<p><b>Danger:</b> forgetting delete = memory leak. Deleting twice =
undefined behavior. Using after delete = dangling pointer. These bugs
are why smart pointers exist (next chapter).</p>

<p>Modern C++ rule: <b>never use raw new/delete</b> — use
<code>std::make_unique</code>/<code>std::make_shared</code> (RAII
chapter).</p>
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
