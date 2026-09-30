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
<p><b>RAII</b> is THE fundamental C++ idiom: tie every resource's
lifetime to an object's lifetime. The constructor acquires; the
destructor releases — automatically, even when exceptions are
thrown:</p>

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

<p>RAII applies to ALL resources: memory, files, locks, sockets, database
connections. Smart pointers are RAII for memory. <code>std::lock_guard</code>
is RAII for mutexes. If it needs cleanup, wrap it in an RAII class.</p>
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
<p>Smart pointers are RAII wrappers for heap memory — no manual
delete:</p>

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

<p><b>Rule:</b> use <code>unique_ptr</code> by default.
<code>shared_ptr</code> only when ownership is truly shared.
<code>weak_ptr</code> to break circular references.</p>
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
<p>When a class manages a resource, you must define how it's copied:</p>

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

<ul>
<li><b>Rule of 0</b> — if you use smart pointers/containers, define
nothing (best!)</li>
<li><b>Rule of 3</b> — if you define one of {destructor, copy ctor, copy
assign}, define all three</li>
<li><b>Rule of 5</b> — also add move ctor and move assign (next
chapter)</li>
</ul>
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
<p><b>Move semantics</b> (C++11) transfer resources instead of copying
them — dramatically faster for large objects:</p>

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

<p><code>std::move</code> doesn't move — it casts to an rvalue
reference, enabling the move constructor. <b>Copy elision</b> (C++17)
automatically eliminates copies in many cases — the compiler constructs
the object directly in its destination.</p>
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
<p>The <b>STL</b> is C++'s standard library of containers, iterators,
algorithms, and utilities — the most important part of modern C++:</p>

<ul>
<li><b>Containers</b> — store data: <code>vector</code>, <code>map</code>,
<code>set</code>, <code>array</code>, <code>deque</code>...</li>
<li><b>Iterators</b> — generalize pointers for traversing containers</li>
<li><b>Algorithms</b> — ~100 ready-made operations: <code>sort</code>,
<code>find</code>, <code>transform</code>, <code>accumulate</code>...</li>
<li><b>Utilities</b> — <code>pair</code>, <code>tuple</code>,
<code>optional</code>, <code>variant</code>...</li>
</ul>

<p>The STL is built on <b>templates</b> — containers work with any type,
algorithms work with any container. This generic programming is what
makes C++ uniquely powerful.</p>
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

<p><b>Rule:</b> use <code>vector</code> unless you have a specific
reason not to. It's cache-friendly and fast for almost everything.</p>
""",
            },
            {
                "title": "Associative & Unordered Containers",
                "html": """
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

<p>Container adapters: <code>stack</code> (LIFO), <code>queue</code>
(FIFO), <code>priority_queue</code> (max-heap).</p>
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
<p>Iterators generalize pointers — they connect containers to
algorithms:</p>

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

<p>Iterator invalidation: modifying a vector (push_back, insert) may
invalidate existing iterators. Be careful when modifying while
iterating.</p>
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

<p>Modern C++20 adds <b>ranges</b> — <code>std::ranges::sort(v)</code>
instead of <code>std::sort(v.begin(), v.end())</code>. Cleaner and
safer.</p>
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
