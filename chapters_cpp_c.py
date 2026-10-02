"""C++ Tutor chapters 17-24 (RAII through STL Algorithms)."""

CHAPTERS_CPP_C = [
    {
        "id": "cpp17",
        "title": "RAII",
        "emoji": "🔐",
        "lessons": [
            {
                "title": "Resource Acquisition Is Initialization",
                "html": """
<p>Every resource — heap memory, an open file, a mutex, a socket — has
the same shape: you acquire it, you use it, and you <i>must</i> release
it. Manual release fails in practice: early returns skip the cleanup
lines, and exceptions skip everything after the throw. <b>RAII</b>
(Resource Acquisition Is Initialization) is the C++ answer: tie the
resource's lifetime to an object's lifetime and let the language's
guaranteed destructor call do the releasing. The constructor acquires;
the destructor releases — automatically, on every exit path,
exceptions included.</p>

<p>The recipe is short: acquire in the constructor, release in the
destructor, and forbid copying if copying would mean closing the same
resource twice:</p>

<pre class="code">class FileHandle {
    FILE* file;
public:
    FileHandle(const char* path) : file(fopen(path, "r")) {}
    ~FileHandle() { if (file) fclose(file); }   // automatic cleanup!
    // no copy — prevent double-close
    FileHandle(const FileHandle&amp;) = delete;
    FileHandle&amp; operator=(const FileHandle&amp;) = delete;
};

void demo() {
    FileHandle f("data.txt");
    // use f...
}   // destructor runs here — file always closed, even on exception!</pre>

<p>Follow the flow in <code>demo()</code>: the constructor runs at the
declaration and opens the file; the code uses the file; then the
function ends — normally <i>or</i> via an exception — and the
destructor runs right there, closing the file. The copy operations are
<code>= delete</code> so two handles can never own one file and close
it twice; the sanctioned way to transfer such an object is move
semantics (chapter 20).</p>

<p>The power of RAII is that it scales: wrap <i>any</i> resource in
this pattern and cleanup stops being your problem. The standard library
already did it for the common cases — smart pointers are RAII for
memory (chapter 18), <code>std::lock_guard</code> is RAII for mutexes,
<code>std::vector</code> is RAII for its element array, and
<code>std::fstream</code> for files.</p>

<p>Rule of thumb: if it needs cleanup, it deserves a class. "Acquire"
in the constructor and "release" in the destructor means the compiler
writes the cleanup calls for you — in exactly the right places,
forever.</p>
""",
            },
        ],
        "quiz": [
            {"type": "mc", "question": "RAII stands for:",
             "options": ["Random Access Iteration Interface", "Resource Acquisition Is Initialization", "Runtime Allocation and Instant Initialization", "Rapid Application Integration Interface"],
             "answer": 1, "explain": "Constructor acquires, destructor releases — automatic cleanup."},
        ],
    },

    {
        "id": "cpp18",
        "title": "Smart Pointers",
        "emoji": "🧠",
        "lessons": [
            {
                "title": "unique_ptr, shared_ptr & weak_ptr",
                "html": """
<p>Chapter 16 ended with the problem: raw <code>new</code> and
<code>delete</code> leak, dangle, and double-free. <b>Smart pointers</b>
are the fix — RAII wrappers around heap memory that delete the object
automatically when its last owner goes away. You still use heap
allocation, but the question "who deletes this?" disappears, because
exactly one policy answers it. The three types differ only in their
ownership policy:</p>

<ul>
<li><b>unique_ptr</b> — one owner, no copying. Your default choice:
zero size overhead over a raw pointer, and ownership can be
<i>transferred</i> (not copied) with <code>std::move</code>.</li>
<li><b>shared_ptr</b> — many owners; an internal reference count drops
each time an owner dies, and the last one deletes the object.</li>
<li><b>weak_ptr</b> — points at a shared object <i>without</i> owning
it; used to observe safely or to break ownership cycles.</li>
</ul>

<p>The code demonstrates all three in ten lines:</p>

<pre class="code">#include &lt;memory&gt;

// unique_ptr: exclusive ownership (default choice)
auto p = std::make_unique&lt;int&gt;(42);
auto q = std::move(p);      // transfer ownership (p becomes nullptr)

// shared_ptr: shared ownership (reference counted)
auto s1 = std::make_shared&lt;int&gt;(100);
auto s2 = s1;                // both point to same object
s1.use_count();              // 2 (two owners)

// weak_ptr: observes without owning (breaks cycles)
std::weak_ptr&lt;int&gt; w = s1;
if (auto locked = w.lock()) {
    std::cout &lt;&lt; *locked;    // object still alive
}</pre>

<p>Read it in thirds. <code>p</code> owns one int; after
<code>std::move(p)</code>, <code>q</code> owns it and <code>p</code>
has become <code>nullptr</code> — ownership moved, never duplicated.
In the shared section, copying <code>s1</code> into <code>s2</code>
raises <code>use_count()</code> to 2; both may use the object, and
whoever survives last frees it. In the weak section, <code>w</code>
does not keep the object alive; <code>w.lock()</code> asks "still
here?" and hands back a shared_ptr you can safely use — or an empty
one you can test.</p>

<p>Guidelines that keep you out of trouble: default to
<code>unique_ptr</code>; reach for <code>shared_ptr</code> only when
ownership is genuinely split among parts of the program (it costs an
atomic count and a control block); and remember that raw pointers and
references are still perfect for "I'm just looking, not owning".</p>

<p>Gotcha: two shared_ptrs pointing at each other form a cycle — each
keeps the other's count above zero, so both leak. Make one side a
<code>weak_ptr</code> (typically: parent owns child, child observes
parent).</p>
""",
            },
        ],
        "quiz": [
            {"type": "mc", "question": "Which smart pointer should you use by default?",
             "options": ["shared_ptr", "unique_ptr", "weak_ptr", "raw pointer"],
             "answer": 1, "explain": "unique_ptr = exclusive ownership, zero overhead, the default."},
            {"type": "mc", "question": "What problem does weak_ptr solve?",
             "options": ["Slower access", "Circular references with shared_ptr", "Memory alignment", "Thread safety"],
             "answer": 1, "explain": "Two shared_ptrs pointing at each other = reference count never reaches 0. weak_ptr breaks the cycle."},
        ],
    },

    {
        "id": "cpp19",
        "title": "Copy Semantics",
        "emoji": "📋",
        "lessons": [
            {
                "title": "Copy Constructor, Rule of 3/5/0",
                "html": """
<p>When a class owns a resource — like this <code>Buffer</code>, which
holds an array from <code>new[]</code> — the compiler's default copying
becomes a bug. The default <b>copy constructor</b> and <b>copy
assignment</b> copy each member one by one, and for a raw pointer that
means copying the <i>address</i>, not the array. Two Buffers then point
at one allocation, both destructors call <code>delete[]</code> on it,
and you get a double-free. So when you manage a resource, you must
define the copy yourself.</p>

<p>The fix is a <b>deep copy</b>: allocate a new array and copy the
<i>elements</i>. Look at the copy constructor first — it allocates its
own array in the init list, then <code>std::copy</code> fills it:</p>

<pre class="code">class Buffer {
    int* data;
    size_t size;
public:
    Buffer(size_t s) : data(new int[s]), size(s) {}
    ~Buffer() { delete[] data; }

    // Rule of 3: copy ctor, copy assign, destructor
    Buffer(const Buffer&amp; other)                    // copy ctor — deep copy
        : data(new int[other.size]), size(other.size) {
        std::copy(other.data, other.data + size, data);
    }
    Buffer&amp; operator=(const Buffer&amp; other) {      // copy assign
        if (this != &amp;other) {
            delete[] data;
            size = other.size;
            data = new int[size];
            std::copy(other.data, other.data + size, data);
        }
        return *this;
    }
};</pre>

<p>The copy <i>assignment</i> operator does the same job for an object
that already exists, so it has two extra chores. The
<code>if (this != &amp;other)</code> check handles <code>b = b;</code> —
without it we would delete the very array we are about to copy from.
Deleting the old array first releases the memory this object no longer
needs. Returning <code>*this</code> by reference allows chained
assignments like <code>a = b = c;</code>.</p>

<p>The <b>Rule of 3</b> falls out of this: if you need any one of
{destructor, copy constructor, copy assignment}, you almost certainly
need all three — they exist together to manage one resource. The
<b>Rule of 5</b> adds the move constructor and move assignment (next
chapter) so the class can also transfer efficiently.</p>

<p>But the best rule in modern C++ is the <b>Rule of 0</b>: store
resources in <code>std::vector</code>, <code>std::string</code>, or
smart pointers, and write none of these functions. The members already
copy, move, and clean up correctly, so the compiler-generated defaults
do exactly the right thing. Reserve Rules 3 and 5 for classes that
directly wrap a resource — like the ones the library already gives
you.</p>
""",
            },
        ],
        "quiz": [
            {"type": "mc", "question": "The best rule for modern C++ is:",
             "options": ["Rule of 3", "Rule of 5", "Rule of 0 — use smart pointers and containers", "Rule of 7"],
             "answer": 2, "explain": "Rule of 0: let std::vector, std::string, and smart pointers handle everything."},
        ],
    },

    {
        "id": "cpp20",
        "title": "Move Semantics",
        "emoji": "🚀",
        "lessons": [
            {
                "title": "Move Constructor & std::move",
                "html": """
<p>Copies of big objects are expensive: <code>Buffer b2 = b1;</code>
allocates memory and copies every element. Yet often the source is a
temporary you will never use again — a function's return value, or a
variable on its last assignment. <b>Move semantics</b> (C++11) exploit
that: instead of copying the resource, <i>transfer</i> it. The move
constructor steals the source's pointer and size, then leaves the
source empty-but-valid. A move is a few pointer assignments — constant
time, no allocation, no element copies.</p>

<p>A move constructor takes an <b>rvalue reference</b>
(<code>Buffer&amp;&amp;</code>) — it binds to "things that are about to
disappear". Here is the full picture:</p>

<pre class="code">class Buffer {
    int* data; size_t size;
public:
    // move constructor — "steal" the resources
    Buffer(Buffer&amp;&amp; other) noexcept
        : data(other.data), size(other.size) {
        other.data = nullptr;   // leave other in a valid state
        other.size = 0;
    }

    // move assignment
    Buffer&amp; operator=(Buffer&amp;&amp; other) noexcept {
        if (this != &amp;other) {
            delete[] data;
            data = other.data;
            size = other.size;
            other.data = nullptr;
            other.size = 0;
        }
        return *this;
    }
};

Buffer createBuffer() {
    Buffer b(1024);
    return b;    // move (or elided) — no copy!
}

Buffer b1(100);
Buffer b2 = std::move(b1);   // explicit move — b1 is now "empty"</pre>

<p>Walk the move constructor: it grabs <code>other.data</code> and
<code>other.size</code>, then nulls the source out. That nulling is not
politeness — when <code>other</code>'s destructor later runs, it must
not <code>delete[]</code> the memory we now own. The move assignment
adds the usual self-assignment check and releases <i>this</i> object's
old resource first. <code>noexcept</code> matters too: containers like
vector only use moves during reallocation if they are guaranteed not
to throw.</p>

<p><code>std::move</code> needs demystifying: it moves nothing. It is
just a cast to an rvalue reference that says "treat this object as
disposable", which selects the move constructor. After
<code>Buffer b2 = std::move(b1);</code>, <code>b1</code> exists but is
empty — give it a new value before reading it. Also note
<code>createBuffer</code>: returning the local <code>b</code> needs no
<code>std::move</code> — copy elision (guaranteed since C++17)
constructs the object directly in its destination.</p>

<p>Gotchas: do not use an object after moving from it (beyond
assigning or destroying it); do not write <code>std::move</code> on a
const object — it silently falls back to a copy; and do not sprinkle
<code>std::move</code> on locals in return statements, which can defeat
elision.</p>
""",
            },
        ],
        "quiz": [
            {"type": "mc", "question": "What does std::move actually do?",
             "options": ["Moves the data", "Casts to an rvalue reference, enabling move", "Copies and deletes", "Allocates memory"],
             "answer": 1, "explain": "std::move is just a cast — it marks the object as movable."},
            {"type": "blank", "question": "The move constructor takes a parameter of type <code>____</code>.",
             "answers": ["rvalue reference", "T&&", "rvalue"], "explain": "Buffer(Buffer&& other) — the && marks an rvalue reference."},
        ],
    },

    {
        "id": "cpp21",
        "title": "STL Overview",
        "emoji": "🛠️",
        "lessons": [
            {
                "title": "Standard Template Library",
                "html": """
<p>Writing your own linked list or sort routine is a fine exercise and
a bad habit: every hand-rolled container is one more place for bugs.
The <b>Standard Template Library</b> (STL) is the C++ standard
library's collection of ready-made, tested, fast building blocks —
containers that store data, algorithms that process it, and iterators
that connect the two. Since roughly C++11, "modern C++" mostly means
"use the STL"; it is the part of the language you will touch every
single day.</p>

<p>The STL has four pillars, and it pays to see how they interlock:</p>

<ul>
<li><b>Containers</b> store data: <code>vector</code>, <code>map</code>,
<code>set</code>, <code>array</code>, <code>deque</code>... Each one
trades off speed, ordering, and memory differently (chapter 22).</li>
<li><b>Iterators</b> generalize pointers: they walk through a container
element by element, and every container hands them out via
<code>begin()</code>/<code>end()</code> (chapter 23).</li>
<li><b>Algorithms</b> are about 100 ready operations —
<code>sort</code>, <code>find</code>, <code>transform</code>,
<code>accumulate</code>... — that work on <i>any</i> container through
those iterators (chapter 24).</li>
<li><b>Utilities</b> — <code>pair</code>, <code>tuple</code>,
<code>optional</code>, <code>variant</code> — handle the small
mechanical jobs of everyday code.</li>
</ul>

<p>The glue that makes this work is <b>templates</b> (generic
programming). <code>std::vector&lt;int&gt;</code> and
<code>std::vector&lt;std::string&gt;</code> are generated from one
source pattern; <code>std::sort</code> does not know or care whether it
is sorting ints or strings — it just moves elements via iterators. So
an algorithm written once works with every container, present and
future, and the compiler stamps out a specialized, inlined version for
your exact types. That is why STL code is both shorter and usually
<i>faster</i> than the hand-written loop it replaces.</p>

<p>Practical starting points: default to <code>std::vector</code>,
learn <code>sort</code> and <code>find</code> first, and prefer named
algorithms over manual loops — each one you swap in is a loop you no
longer have to debug.</p>
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
        "id": "cpp22",
        "title": "STL Containers",
        "emoji": "📚",
        "lessons": [
            {
                "title": "Sequence Containers",
                "html": """
<p>Sequence containers keep elements in the order you put them — first,
second, third. C++ gives you four, and choosing between them is mostly
about answering two questions: "do I need fast access by position?"
and "where do I insert and remove?" Each container optimizes for a
different answer:</p>

<ul>
<li><b>vector</b> — a dynamic array: O(1) access by index, fast appends
at the end. The default.</li>
<li><b>deque</b> — double-ended queue: fast at <i>both</i> ends.</li>
<li><b>list</b> — doubly-linked list: O(1) insert/erase anywhere, but
no positional access.</li>
<li><b>array</b> — fixed size known at compile time; like a C array
with a full STL interface.</li>
</ul>

<pre class="code">#include &lt;vector&gt;
#include &lt;deque&gt;
#include &lt;list&gt;
#include &lt;array&gt;

std::vector&lt;int&gt; vec = {1, 2, 3};     // dynamic array (DEFAULT choice)
vec.push_back(4);                       // add to end
vec[0];                                 // O(1) access

std::deque&lt;int&gt; dq = {1, 2, 3};       // double-ended queue
dq.push_front(0);                       // add to front too!

std::list&lt;int&gt; lst = {1, 2, 3};       // doubly-linked list
lst.push_front(0);                      // O(1) insert anywhere

std::array&lt;int, 5&gt; arr = {1, 2, 3, 4, 5};  // fixed size</pre>

<p>Read each stanza. The <code>vector</code> block shows the daily
workflow — create with an initializer list, <code>push_back</code> to
grow, index with <code>[]</code> — and <code>vec[0]</code> is O(1)
because elements sit contiguously in memory; the CPU cache loves that
layout. The <code>deque</code> adds <code>push_front</code>, which a
vector cannot do cheaply (everything would shift). The
<code>list</code> inserts in the middle without moving anything — the
price is that <code>lst[2]</code> must walk node by node, and each node
costs an extra allocation plus two pointers. The <code>array</code> is
just <code>int arr[5]</code> with conveniences like
<code>.size()</code>.</p>

<p>One number to remember: <code>vector</code> beats <code>list</code>
in the majority of real workloads, even ones with insertions, because
contiguous memory wins the cache battles. So the standing rule: use
<code>vector</code> unless you have a measured reason not to.</p>

<p>Gotchas: indexing past the end is undefined behavior — use
<code>at()</code> while debugging to get a thrown exception instead;
and once <code>push_back</code> grows a vector's capacity, all
iterators and references to its elements may be invalid.</p>
""",
            },
            {
                "title": "Associative & Unordered Containers",
                "html": """
<p>Sequence containers answer "what is at position 3?" — but half of
real programming asks "what belongs to key <i>Grace</i>?"
<b>Associative containers</b> store by key instead of by position. The
two families split on one design choice: <code>map</code> and
<code>set</code> keep keys <b>sorted</b> in a balanced tree
(O(log n), everything in order), while
<code>unordered_map</code>/<code>unordered_set</code> use a
<b>hash table</b> (O(1) on average, no ordering at all).</p>

<pre class="code">#include &lt;map&gt;
#include &lt;set&gt;
#include &lt;unordered_map&gt;
#include &lt;unordered_set&gt;

// map: sorted key-value pairs (red-black tree)
std::map&lt;std::string, int&gt; ages;
ages["Ada"] = 36;
ages["Grace"] = 45;

// unordered_map: hash table (faster lookup, no ordering)
std::unordered_map&lt;std::string, int&gt; fast;
fast["key"] = 42;

// set: sorted unique values
std::set&lt;int&gt; s = {3, 1, 4, 1, 5};
// s = {1, 3, 4, 5} — sorted, no duplicates

// unordered_set: hash-based unique values
std::unordered_set&lt;int&gt; us = {3, 1, 4, 1, 5};
// same elements, different order</pre>

<p>The <code>map</code> stanza shows the nicest syntax in the STL:
<code>ages["Ada"] = 36;</code> looks like array indexing, but the index
is a string — and if the key does not exist yet, <code>operator[]</code>
<i>creates</i> it. That convenience is also a trap (see below). The
<code>unordered_map</code> stanza is the same interface with a
different engine underneath. The <code>set</code> stanza demonstrates
two behaviors at once: the two <code>1</code>s collapse into one, and
the result comes out sorted — {1, 3, 4, 5}. The
<code>unordered_set</code> holds identical elements, but its iteration
order is unspecified and can change between runs.</p>

<p>Choosing between them: default to <code>unordered_map</code> for raw
lookup speed; choose <code>map</code> when you need keys in order
(ranges, "smallest key first", printing a sorted phone book) or when
hashing is expensive. Both offer <code>find()</code>, which returns
<code>end()</code> when the key is absent — that is the non-creating
lookup.</p>

<p>Above these sit the <b>container adapters</b>: <code>stack</code>
(last in, first out), <code>queue</code> (first in, first out), and
<code>priority_queue</code> (always pops the largest). They
deliberately expose a narrow interface on top of another container.</p>

<p>Gotcha: <code>ages["Bob"]</code> on a missing key silently inserts
Bob with a zero-initialized value — use <code>find()</code> or
<code>at()</code> when you only want to look.</p>
""",
            },
        ],
        "quiz": [
            {"type": "mc", "question": "Which container should you use by default?",
             "options": ["list", "vector", "map", "set"],
             "answer": 1, "explain": "vector is cache-friendly, O(1) access, and fast for almost everything."},
            {"type": "mc", "question": "map vs unordered_map:",
             "options": [
                 "map is faster",
                 "map is sorted (tree), unordered_map is hashed — faster lookup but no ordering",
                 "They're identical",
                 "unordered_map uses more memory always",
             ],
             "answer": 1, "explain": "map: O(log n) sorted; unordered_map: O(1) average, hashed."},
        ],
    },

    {
        "id": "cpp23",
        "title": "Iterators",
        "emoji": "➡️",
        "lessons": [
            {
                "title": "Iterators",
                "html": """
<p>Every container needs a way to visit its elements, and every
algorithm needs a way to say "work from here to there".
<b>Iterators</b> solve both problems at once: they behave like pointers
into a container, and they are the common currency between containers
and algorithms. Learn iterators, and <code>sort</code>,
<code>find</code> and friends become usable on any container.</p>

<p>The core convention: <code>begin()</code> returns an iterator to the
<b>first</b> element, while <code>end()</code> points to a
<b>one-past-the-last</b> position — never dereference it. The valid
range is the half-open interval <code>[begin, end)</code>:</p>

<pre class="code">std::vector&lt;int&gt; v = {1, 2, 3, 4, 5};

auto it = v.begin();       // points to first element
auto end = v.end();         // points PAST the last element

std::cout &lt;&lt; *it;           // 1 (dereference)
++it;                        // advance
std::cout &lt;&lt; *it;           // 2

// range: [begin, end) — end is NOT included
for (auto it = v.begin(); it != v.end(); ++it) {
    std::cout &lt;&lt; *it &lt;&lt; " ";
}

// const iterators (read-only)
auto cit = v.cbegin();

// reverse iterators
for (auto rit = v.rbegin(); rit != v.rend(); ++rit) {
    std::cout &lt;&lt; *rit &lt;&lt; " ";  // 5 4 3 2 1
}</pre>

<p>Walk it: <code>*it</code> dereferences like a pointer (prints 1)
and <code>++it</code> advances to the next element (prints 2). The
canonical loop runs <code>it != end</code> — note <code>!=</code>, not
<code>&lt;</code> — and stops at the past-the-end position, having
printed all five elements. <code>cbegin()</code> is the read-only
flavor, and the reverse pair <code>rbegin()/rend()</code> walks from
last to first — that loop prints <code>5 4 3 2 1</code> while still
using <code>++</code>, because a reverse iterator's increment moves
backwards.</p>

<p>Why half-open ranges? They make empty ranges natural
(<code>begin == end</code>), compose cleanly (one range's
<code>end</code> is a valid place to continue from), and remove
off-by-one thinking from every algorithm signature like
<code>sort(v.begin(), v.end())</code>.</p>

<p>Gotchas:</p>

<ul>
<li><b>Invalidation:</b> <code>push_back</code>/<code>insert</code> on
a vector may reallocate — all existing iterators go stale. Re-fetch
them or <code>reserve()</code> capacity first.</li>
<li>Never dereference <code>end()</code>; it is a sentinel, not an
element.</li>
<li>Use prefix <code>++it</code> by habit — postfix can be slower for
non-trivial iterator types.</li>
</ul>
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
        "id": "cpp24",
        "title": "STL Algorithms",
        "emoji": "⚙️",
        "lessons": [
            {
                "title": "STL Algorithms",
                "html": """
<p>Most code you write by hand is a loop with a tiny idea inside:
compare, count, transform. The STL already contains about 100 of these
ideas as tested, optimized, named functions in
<code>&lt;algorithm&gt;</code> and <code>&lt;numeric&gt;</code>. They
all take iterator ranges, so they work with any container. Replacing a
manual loop with a named algorithm shrinks the code, removes
off-by-one bugs, and tells the reader your <i>intent</i> in one
word.</p>

<pre class="code">#include &lt;algorithm&gt;
#include &lt;numeric&gt;

std::vector&lt;int&gt; v = {5, 2, 8, 1, 9, 3};

// sorting
std::sort(v.begin(), v.end());           // ascending
std::sort(v.begin(), v.end(), std::greater&lt;int&gt;{});  // descending

// searching (requires sorted for binary_search)
auto it = std::find(v.begin(), v.end(), 8);
std::sort(v.begin(), v.end());
bool found = std::binary_search(v.begin(), v.end(), 8);
auto lb = std::lower_bound(v.begin(), v.end(), 5);

// counting
int evens = std::count_if(v.begin(), v.end(),
    [](int n) { return n % 2 == 0; });

// transforming
std::vector&lt;int&gt; doubled;
std::transform(v.begin(), v.end(), std::back_inserter(doubled),
    [](int n) { return n * 2; });

// accumulating
int sum = std::accumulate(v.begin(), v.end(), 0);

// min / max
auto min_it = std::min_element(v.begin(), v.end());
auto max_it = std::max_element(v.begin(), v.end());</pre>

<p>Take the block family by family. <b>Sorting</b>:
<code>std::sort</code> orders ascending by default; pass
<code>std::greater&lt;int&gt;{}</code> as the third argument to flip to
descending. <b>Searching</b>: <code>std::find</code> scans any range
for a value and returns <code>end()</code> if absent;
<code>binary_search</code> and <code>lower_bound</code> are far faster
but demand a <i>sorted</i> range — note the extra <code>std::sort</code>
call right before, easy to forget. <b>Counting</b>:
<code>count_if</code> plus a lambda
(<code>[](int n){ return n % 2 == 0; }</code>) counts elements matching
a condition. <b>Transforming</b>: <code>transform</code> applies the
lambda to every element and writes results into <code>doubled</code> —
<code>back_inserter</code> makes the destination grow as needed.
<b>Accumulating</b>: <code>accumulate</code> starts from 0 and folds
the whole range into one sum (the initial value matters — start from
<code>0.0</code> for averages). <b>Extremes</b>:
<code>min_element</code>/<code>max_element</code> return iterators, so
dereference them for the value.</p>

<p>C++20 adds <b>ranges</b> as the ergonomic upgrade:
<code>std::ranges::sort(v)</code> takes the container directly — no
begin/end pair to get wrong, and the compiler catches mismatches. New
code should prefer it.</p>

<p>Rule of thumb: before writing any loop, check whether a named
algorithm already does it — <code>all_of</code>,
<code>any_of</code>, <code>remove_if</code>, <code>unique</code>, and
<code>reverse</code> are probably on the list.</p>
""",
            },
        ],
        "quiz": [
            {"type": "mc", "question": "Which header provides sort, find, and transform?",
             "options": ["<numeric>", "<algorithm>", "<container>", "<iterator>"],
             "answer": 1, "explain": "#include <algorithm> — the algorithms header."},
            {"type": "blank", "question": "To sum all elements, use <code>std::____</code> from <numeric>.",
             "answers": ["accumulate"], "explain": "std::accumulate(begin, end, initial_value)."},
        ],
    },
]
