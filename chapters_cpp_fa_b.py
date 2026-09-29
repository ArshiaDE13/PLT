"""Persian variants of C++ Tutor chapters 9-44 (chapters_cpp_b/c/d/e)."""

FA_CPP_B = {
    "cpp09": {"title": "مرجع‌ها", "lessons": [
        {"title": "مرجع‌ها و مرجع‌های const", "html": """
<p>یک <b>مرجع</b> نامی دیگر برای متغیر موجود است — بعد از اتصال هرگز به
شیء دیگری ارجاع نمی‌دهد:</p>

[[code0]]

<p><b>مرجع‌های const</b> فقط می‌خوانند و می‌توانند به مقدارهای موقت هم
بسپارند. pass-by-const-reference استانداردِ انتقالِ شیءهای بزرگ است
(بدون کپی، بدون تغییر).</p>
""",},
        {"title": "مرجع در برابر اشاره‌گر و const با اشاره‌گرها", "html": """
<p>مرجع‌ها و اشاره‌گرها هر دو به شیء اشاره می‌کنند اما:</p>

<ul>
<li>مرجع‌ها باید مقداردهی شوند و هرگز تغییر مقصد نمی‌دهند</li>
<li>اشاره‌گرها می‌توانند null باشند، دوباره تنظیم شوند و حسابِ اشاره‌گر داشته باشند</li>
</ul>

<p><b>const با اشاره‌گرها</b> — سه ترکیب، از راست به چپ بخوان:</p>

<p>‏const int* p1 — اشاره‌گر به intِ ثابت. int* const p2 — اشاره‌گرِ ثابت به int. const int* const p3 — هر دو ثابت.</p>
""",},
    ], "quiz": [
        {"question": "مرجع می‌تواند به شیء دیگری بازتنظیم شود.",
         "options": ["درست", "غلط"], "answer": 1, "explain": "مرجع‌ها در مقداردهی اولیه اتصال می‌یابند و هرگز تغییر نمی‌کنند."},
    ],
},

    "cpp10": {"title": "اشاره‌گرها", "lessons": [
        {"title": "پایه‌های اشاره‌گر", "html": """
<p>یک <b>اشاره‌گر</b> آدرس حافظهٔ متغیر دیگری را نگه می‌دارد:</p>

[[code0]]

<p><b>حساب اشاره‌گر</b> — به اندازهٔ sizeof(عنصر) جلو می‌رود نه ۱
بایت:</p>

<p>همیشه از <code>nullptr</code> استفاده کن نه NULL یا 0.</p>
""",},
    ], "quiz": [
        {"question": "*ptr چه می‌کند؟",
         "options": ["اشاره‌گر اعلام می‌کند", "بازگشایی می‌کند (مقدار در آدرس را می‌خواند)", "آدرس می‌دهد", "هیچ"],
         "answer": 1, "explain": "* عملگر بازگشایی است."},
        {"question": "کلیدواژهٔ C++11 برای اشاره‌گرِ null <code>____</code> است.",
         "answers": ["nullptr"], "explain": "همیشه nullptr نه NULL و نه 0."},
    ],
},

    "cpp11": {"title": "کلاس‌ها و شیءها", "lessons": [
        {"title": "پایه‌های کلاس و مشخص‌کننده‌های دسترسی", "html": """
<p>یک <b>کلاس</b> داده (اعضا) و رفتار (متدها) را با کنترل دسترسی جمع
می‌کند:</p>

[[code0]]

<ul>
<li><b>private</b> — پیش‌فرض برای کلاس‌ها؛ کپسوله‌سازی</li>
<li><b>public</b> — رابط عمومی</li>
<li><b>protected</b> — مثل private اما برای کلاس‌های فرزند</li>
</ul>
""",},
    ], "quiz": [
        {"question": "سطح دسترسیِ پیش‌فرضِ اعضای کلاس ____ است.",
         "options": ["public", "private", "protected", "internal"],
         "answer": 1, "explain": "کلاس‌ها به‌طور پیش‌فرض private هستند برای کپسوله‌سازی."},
        {"question": "تابع عضوِ ____ قول می‌دهد شیء را تغییر ندهد.",
         "answers": ["const"], "explain": "void print() const — const در انتها یعنی فقط-خواندنی."},
    ],
},

    "cpp12": {"title": "سازنده‌ها و ویرانگرها", "lessons": [
        {"title": "سازنده‌ها و لیست مقداردهی اعضا", "html": """
<p><b>سازنده‌ها</b> شیءها را مقداردهی اولیه می‌کنند. <b>لیست مقداردهی
اعضا</b> راهِ ترجیحی است:</p>

[[code0]]

<p><b>ویرانگرها</b> وقتی شیء می‌میرد پاک‌سازی می‌کنند — خودکار در خروجِ
scope. این بنیادِ RAII است.</p>
""",},
    ], "quiz": [
        {"question": "ویرانگر کی صدا زده می‌شود؟",
         "options": ["هنگام ساخت", "خودکار وقتی شیء از scope خارج می‌شود", "فقط با delete", "هرگز"],
         "answer": 1, "explain": "ویرانگر در خروجِ scope خودکار اجرا می‌شود — بنیادِ RAII."},
    ],
},

    "cpp13": {"title": "کپسوله‌سازی و طراحی کلاس", "lessons": [
        {"title": "کپسوله‌سازی، getter و setter", "html": """
<p><b>کپسوله‌سازی</b> = داده را پنهان کن، رفتار را آشکار کن. اعضا خصوصی
هستند؛ رابط عمومی قواعد را اجرا می‌کند. اعضای static به کلاس تعلق
دارند و friend دسترسیِ خصوصی می‌دهد.</p>
""",},
    ], "quiz": [
        {"question": "کپسوله‌سازی یعنی:",
         "options": ["همه‌چیز public باشد", "داده پنهان، رابطِ کنترل‌شده آشکار", "استفاده از اشاره‌گر", "وراثت از پایه"],
         "answer": 1, "explain": "داده خصوصی + متدهای عمومی که قواعد را اجرا می‌کنند."},
    ],
},

    "cpp14": {"title": "وراثت", "lessons": [
        {"title": "وراثت و override متدها", "html": """
<p>با <code>extends</code> (در ++C: <code>: public Base</code>) کلاس فرزند
از پدر به ارث می‌برد. همیشه از <code>override</code> و
<b>ویرانگرِ مجازی</b> استفاده کن:</p>

[[code0]]
""",},
    ], "quiz": [
        {"question": "کلیدواژه‌ای که به کامپایلر می‌گوید واقعاً داری override می‌کنی <code>____</code> است.",
         "answers": ["override"], "explain": "void speak() const override — کامپیلر چک می‌کند پایه virtual داشته باشد."},
    ],
},

    "cpp15": {"title": "چندریختی", "lessons": [
        {"title": "توابع مجازی و چندریختی", "html": """
<p><b>چندریختی</b> — یک رابط، پیاده‌سازی‌های متعدد. توابع مجازی
dispatch زمان‌اجرایی را ممکن می‌کنند:</p>

[[code0]]

<p><b>مجازی خالص</b> (= 0) کلاس را انتزاعی می‌کند — قابل نمونه‌سازی
نیست. کلاس انتزاعی با فقط توابع مجازی خالص یک <b>رابط</b> است. همیشه
ویرانگرِ مجازی در پایه داشته باش.</p>
""",},
    ], "quiz": [
        {"question": "تابع مجازی با = 0 یک تابع مجازی ____ نامیده می‌شود.",
         "answers": ["خالص", "pure"], "explain": "مجازیِ خالص = 0 کلاس را انتزاعی می‌کند."},
        {"question": "چرا پایه به ویرانگرِ مجازی نیاز دارد؟",
         "options": ["لازم ندارد", "تا delete از طریق اشاره‌گرِ پایه، شیء فرزند را درست نابود کند", "برای کارایی", "برای کپسوله‌سازی"],
         "answer": 1, "explain": "بدون ویرانگرِ مجازی، حذف از طریق پایه* رفتار تعریف‌نشده است."},
    ],
},

    "cpp16": {"title": "حافظه پویا", "lessons": [
        {"title": "new، delete و نشت حافظه", "html": """
<p>حافظهٔ پویا روی <b>heap</b> زندگی می‌کند (در برابر stack برای محلی‌ها).
فراموش‌کردن delete یعنی نشت حافظه. حذفِ دوباره یعنی رفتار تعریف‌نشده.
قاعدهٔ مدرن: <b>هرگز raw new/delete استفاده نکن</b> — از
make_unique/make_shared استفاده کن.</p>
""",},
    ], "quiz": [
        {"question": "فراموش‌کردن delete باعث:",
         "options": ["خطای کامپایل", "نشت حافظه", "پاک‌سازی خودکار", "کرش فوری"],
         "answer": 1, "explain": "حافظه تخصیص‌شده تا خروجِ برنامه باقی می‌ماند."},
    ],
},
}

FA_CPP_C = {
    "cpp17": {"title": "RAII", "lessons": [
        {"title": "RAII", "html": """
<p><b>RAII</b> بنیادی‌ترین اصطلاحِ ++C است: عمرِ هر منبع را به عمرِ یک
شیء گره بزن. سازنده می‌گیرد؛ ویرانگر آزاد می‌کند — خودکار، حتی وقتی
استثنا پرتاب می‌شود. برای همهٔ منابع: حافظه، فایل، قفل، سوکت. اشاره‌گرهای
هوشمند RAII برای حافظه‌اند.</p>
""",},
    ], "quiz": [
        {"question": "‏RAII مخفف چیست؟",
         "options": ["Random Access Iteration Interface", "Resource Acquisition Is Initialization", "Runtime Allocation", "Rapid Application Interface"],
         "answer": 1, "explain": "سازنده می‌گیرد، ویرانگر آزاد می‌کند — پاک‌سازی خودکار."},
    ],
},

    "cpp18": {"title": "اشاره‌گرهای هوشمند", "lessons": [
        {"title": "unique_ptr، shared_ptr و weak_ptr", "html": """
<p>اشاره‌گرهای هوشمند پوشش‌های RAII برای حافظهٔ heap هستند — بدون delete
دستی:</p>

<ul>
<li><b>unique_ptr</b> — مالکیتِ انحصاری (انتخابِ پیش‌فرض)</li>
<li><b>shared_ptr</b> — مالکیتِ مشترک (شمارشِ ارجاع)</li>
<li><b>weak_ptr</b> — مشاهده بدون مالکیت (شکندنِ چرخه‌ها)</li>
</ul>

<p><b>قاعده:</b> به‌طور پیش‌فرض unique_ptr. shared_ptr فقط وقتی
مالکیت واقعاً مشترک است. weak_ptr برای شکستنِ چرخه‌ها.</p>
""",},
    ], "quiz": [
        {"question": "به‌طور پیش‌فرض از کدام اشاره‌گر هوشمند استفاده کنی؟",
         "options": ["shared_ptr", "unique_ptr", "weak_ptr", "اشاره‌گر خام"],
         "answer": 1, "explain": "unique_ptr = مالکیت انحصاری، صفر سربار، پیش‌فرض."},
        {"question": "‏weak_ptr چه مشکلی را حل می‌کند؟",
         "options": ["دسترسی کند", "ارجاع‌های چرخه‌ای با shared_ptr", "همترازی حافظه", "امنیت نخ"],
         "answer": 1, "explain": "دو shared_ptr که به هم اشاره کنند = count هرگز صفر نمی‌شود. weak_ptr می‌شکندش."},
    ],
},

    "cpp19": {"title": "معناشناسی کپی", "lessons": [
        {"title": "سازندهٔ کپی، قاعدهٔ ۳/۵/۰", "html": """
<p>وقتی کلاسی منبعی را مدیریت می‌کند، باید کپی‌کردن را تعریف کند:
<b>قاعدهٔ ۳</b> (ویرانگر، سازندهٔ کپی، عملگر انتساب کپی)،
<b>قاعدهٔ ۵</b> (+ سازندهٔ انتقال، عملگر انتساب انتقال)،
<b>قاعدهٔ ۰</b> (از اشاره‌گر هوشمند/ظرف استفاده کن — بهترین!).</p>
""",},
    ], "quiz": [
        {"question": "بهترین قاعده برای ++C مدرن:",
         "options": ["قاعدهٔ ۳", "قاعدهٔ ۵", "قاعدهٔ ۰ — از اشاره‌گر هوشمند و ظرف استفاده کن", "قاعدهٔ ۷"],
         "answer": 2, "explain": "قاعدهٔ ۰: بگذار std::vector و std::string و اشاره‌گرهای هوشمند همه‌چیز را هندل کنند."},
    ],
},

    "cpp20": {"title": "معناشناسی انتقال", "lessons": [
        {"title": "سازندهٔ انتقال و std::move", "html": """
<p><b>معناشناسی انتقال</b> (‏C++11) منابع را به‌جای کپی <b>منتقل</b>
می‌کند — برای شیءهای بزرگ بسیار سریع‌تر. <code>std::move</code> واقعاً
منتقل نمی‌کند — به مرجعِ rvalue تبدیل می‌کند و سازندهٔ انتقال را فعال
می‌کند. <b>Copy elision</b> (‏C++17) خودکار کپی‌ها را حذف می‌کند.</p>
""",},
    ], "quiz": [
        {"question": "std::move واقعاً چه می‌کند؟",
         "options": ["داده را منتقل می‌کند", "به مرجع rvalue تبدیل می‌کند و انتقال را فعال می‌کند", "کپی و حذف می‌کند", "حافظه تخصیص می‌دهد"],
         "answer": 1, "explain": "std::move فقط یک cast است — شیء را movable علامت می‌زند."},
        {"question": "سازندهٔ انتقال پارامتری از نوع <code>____</code> می‌گیرد.",
         "answers": ["مرجع rvalue", "T&&", "rvalue"],
         "explain": "Buffer(Buffer&& other) — && مرجعِ rvalue را نشان می‌دهد."},
    ],
},

    "cpp21": {"title": "STL", "lessons": [
        {"title": "کتابخانهٔ قالب استاندارد", "html": """
<p><b>STL</b> مهم‌ترین بخشِ ++C مدرن است: ظرف‌ها، iteratorها،
الگوریتم‌ها و ابزارها — همه بر پایهٔ templates. برنامه‌نویسیِ عمومی
همان چیزی است که ++C را منحصربه‌فرد می‌کند.</p>
""",},
    ],
},

    "cpp22": {"title": "ظرف‌های STL", "lessons": [
        {"title": "ظرف‌های ترتیبی", "html": """
<p>‏vector (آرایهٔ پویا — انتخابِ پیش‌فرض)، deque (صفِ دوسر)، list
(فهرستِ پیوندی)، array (اندازه ثابت). <b>قاعده:</b> vector مگر دلیلِ
خاص.</p>
""",},
        {"title": "ظرف‌های انجمنی و بدون‌ترتیب", "html": """
<p><b>map</b> (درخت قرمز-سیاه، مرتب)، <b>unordered_map</b> (جدول هش،
سریع‌تر بدون ترتیب)، <b>set</b> (مقادیر یکتای مرتب)،
<b>unordered_set</b>. آداپتورها: stack (LIFO)، queue (FIFO)،
priority_queue (max-heap).</p>
""",},
    ], "quiz": [
        {"question": "به‌طور پیش‌فرض از کدام ظرف استفاده کنی؟",
         "options": ["list", "vector", "map", "set"],
         "answer": 1, "explain": "vector cache-friendly، دسترسی O(1)، و تقریباً همه‌جا سریع."},
        {"question": "map در برابر unordered_map:",
         "options": ["map سریع‌تر است", "map مرتب است (درخت)، unordered_map هش‌شده — جست‌وجوی سریع‌تر بدون ترتیب", "یکسان‌اند", "unordered_map همیشه حافظه بیشتر مصرف می‌کند"],
         "answer": 1, "explain": "map: O(log n) مرتب؛ unordered_map: O(1) میانگین، هش."},
    ],
},

    "cpp23": {"title": "iteratorها", "lessons": [
        {"title": "iteratorها", "html": """
<p>iteratorها اشاره‌گرها را تعمیم می‌دهند — ظرف‌ها را به الگوریتم‌ها
وصل می‌کنند. <code>begin()</code> به اولین عنصر و <code>end()</code> به
بعد از آخرین اشاره می‌کند. iterator نامعتبر: تغییر دادن vector ممکن است
iteratorهای موجود را نامعتبر کند.</p>
""",},
    ],
},

    "cpp24": {"title": "الگوریتم‌های STL", "lessons": [
        {"title": "الگوریتم‌های STL", "html": """
<p>‏std::sort، std::find، std::transform، std::accumulate،
std::count_if، std::max_element — و binary_search، lower_bound برای
جست‌وجو. الگوریتم‌ها با iterator کار می‌کنند و با هر ظرفی سازگارند.
‏C++20 رنج‌ها را اضافه کرد: <code>std::ranges::sort(v)</code> تمیزتر و
امن‌تر است.</p>
""",},
    ], "quiz": [
        {"question": "کدام سربرگ sort، find و transform را می‌دهد؟",
         "options": ["<numeric>", "<algorithm>", "<container>", "<iterator>"],
         "answer": 1, "explain": "#include <algorithm> — سربرگِ الگوریتم‌ها."},
        {"question": "برای جمعِ همهٔ عناصر از <code>std::____</code> استفاده کن.",
         "answers": ["accumulate"], "explain": "std::accumulate(begin, end, initial_value)."},
    ],
},
}

FA_CPP_D = {
    "cpp25": {"title": "عبارت‌های لامبدا", "lessons": [
        {"title": "نحو لامبدا و capture", "html": """
<p>لامبداها توابع بی‌نام درون‌خطی‌اند — حیاتی برای الگوریتم‌های STL.
‏capture by value کپی می‌کند؛ capture by reference تغییرات را می‌بیند؛
mutable اجازهٔ تغییرِ کپیِ captured را می‌دهد.</p>
""",},
    ], "quiz": [
        {"question": "برای تغییرِ متغیرِ captured-by-value داخل لامبدا، اضافه کن:",
         "options": ["const", "mutable", "static", "volatile"],
         "answer": 1, "explain": "[x]() mutable { ++x; } — mutable اجازهٔ تغییرِ کپی را می‌دهد."},
    ],
},

    "cpp26": {"title": "شیءهای تابعی و std::function", "lessons": [
        {"title": "functorها و std::function", "html": """
<p><b>functorها</b> شیءهایی با operator() هستند — مثل تابع قابل فراخوانی
اما با state. <b>std::function</b> هر callableای را می‌پوشاند — تابع،
لامبدا، functor، اشاره‌گرِ تابع.</p>
""",},
    ],
},

    "cpp27": {"title": "قالب‌ها (Templates)", "lessons": [
        {"title": "قالب‌های تابع و کلاس", "html": """
<p><b>قالب‌ها</b> کد را برای هر نوعی تولید می‌کنند — بنیادِ
برنامه‌نویسی عمومی. در زمانِ کامپایل حل می‌شوند — هیچ هزینهٔ runtime
ندارند. چند پارامتر قالب و پارامترهای غیر-نوعی هم پشتیبانی می‌شوند.</p>
""",},
    ], "quiz": [
        {"question": "قالب‌ها در ____ زمان حل می‌شوند، نه runtime.",
         "answers": ["کامپایل", "زمانِ کامپایل"], "explain": "کامپایلر برای هر نوع استفاده‌شده کد جدا تولید می‌کند."},
    ],
},

    "cpp28": {"title": "قالب‌های Variadic", "lessons": [
        {"title": "parameter packs و fold expressions", "html": """
<p>قالب‌های variadic هر تعداد آرگومان می‌پذیرند. fold expressions
(‏C++17) بازِ کردنِ parameter packs را خوانا می‌کنند.</p>
""",},
    ],
},

    "cpp29": {"title": "Concepts — ‏C++20/23", "lessons": [
        {"title": "concepts و constraints", "html": """
<p><b>concepts</b> (‏C++20) الزاماتِ نام‌دار برای پارامترهای قالب‌اند —
پیام‌های خطای بهتر و کدِ تمیزتر. جایگزینِ SFINAE و enable_if با
محدودیت‌های خوانا و compile-time-checked.</p>
""",},
    ],
},

    "cpp30": {"title": "constexpr، consteval و constinit", "lessons": [
        {"title": "ارزیابی زمان‌کامپایل", "html": """
<p><b>constexpr</b> — قابل ارزیابی در زمانِ کامپایل. <b>consteval</b> —
باید در زمانِ کامپایل ارزیابی شود. <b>if constexpr</b> — انشعاب در
زمانِ کامپایل. این‌ها ++C را به زبانی با محاسباتِ زمان-کامپایل واقعی
تبدیل می‌کنند.</p>
""",},
    ],
},

    "cpp31": {"title": "optional، variant و any", "lessons": [
        {"title": "optional، variant و any", "html": """
<p><b>std::optional</b> — مقداری که ممکن است باشد یا نه.
<b>std::variant</b> — یکی از چند نوعِ ممکن (union امن).
<b>std::any</b> — مقدارِ type-erased از هر نوعی. این سه، جایگزین‌های
مدرن برای الگوهای قدیمی‌اند.</p>
""",},
    ],
},

    "cpp32": {"title": "string_view و انواع کمکی", "lessons": [
        {"title": "string_view، span، pair و tuple", "html": """
<p><b>std::string_view</b> — نمایِ غیرمالکِ فقط-خواندنیِ رشته. بدون کپی
و بدون تخصیص. <b>std::span</b> — نمایِ غیرمالکِ دادهٔ پیوسته (C++20).
<b>std::pair</b> و <b>std::tuple</b> — گروه‌های ناهمگون.</p>
""",},
    ],
},
}

FA_CPP_E = {
    "cpp33": {"title": "مدیریت خطا", "lessons": [
        {"title": "استثناها، noexcept و std::expected", "html": """
<p>مدیریت خطا در ++C: <b>استثناها</b> (سنتی) و <b>std::expected</b>
(‏C++23، جایگزینِ مدرن). expected یک مقدار یا یک خطا را برمی‌گرداند
بدون استثنا.</p>
""",},
    ], "quiz": [
        {"question": "std::expected (‏C++23) نمایندگی می‌کند:",
         "options": ["مقدارِ آینده", "موفقیت با مقدار یا شکست با خطا", "رشتهٔ اختیاری", "یک promise"],
         "answer": 1, "explain": "Expected = مقدار یا خطا، بدون استثنا."},
    ],
},

    "cpp34": {"title": "رنج‌های C++20/23", "lessons": [
        {"title": "رنج‌ها، viewها و pipelineها", "html": """
<p><b>رنج‌ها</b> (‏C++20) ظرف‌ها و الگوریتم‌ها را با viewهای
ترکیب‌پذیر یکسان می‌کنند. viewها <b>تنبل</b>ند — ظرفِ جدید نمی‌سازند،
تکرار را وفق می‌دهند. صفر تخصیص، ترکیب‌پذیر، خوانا.</p>
""",},
    ], "quiz": [
        {"question": "range viewها هستند:",
         "options": ["مشتاق — داده کپی می‌کنند", "تنبل — تکرار را وفق می‌دهند بدون کپی", "همیشه کندتر", "thread-unsafe"],
         "answer": 1, "explain": "viewها تنبل ترکیب می‌شوند — ظرفِ واسط ساخته نمی‌شود."},
    ],
},

    "cpp35": {"title": "ماژول‌ها", "lessons": [
        {"title": "ماژول‌های C++20", "html": """
<p><b>ماژول‌ها</b> (‏C++20) فایل‌های سربرگ را با سیستمِ import تمیزتری
جایگزین می‌کنند: کامپایلِ سریع‌تر، بدون include guard، بدون نشتِ macro،
export صریح.</p>
""",},
    ],
},

    "cpp36": {"title": "coroutineها", "lessons": [
        {"title": "coroutineها", "html": """
<p>‏coroutineها (‏C++20) توابعی هستند که می‌توانند <b>مکث و ادامه
دهند</b>: co_await (انتظار برای async)، co_yield (تولید مقدار)،
co_return (بازگشت و پایان). زبان سازوکار می‌دهد؛ کتابخانه‌ها سیاست
می‌دهند.</p>
""",},
    ],
},

    "cpp37": {"title": "همزمانی", "lessons": [
        {"title": "نخ‌ها، mutexها و atomicها", "html": """
<p><b>نخ‌ها</b> اجرای موازی ممکن می‌کنند. <b>mutexها</b> داده مشترک را
محافظت می‌کنند. <b>atomicها</b> عملیات‌های تقسیم‌ناپذیر بدون قفل.
همیشه lock_guard (RAII) را به lock()/unlock() خام ترجیح بده. همیشه
atomic را برای شمارنده‌های ساده ترجیح بده.</p>
""",},
    ], "quiz": [
        {"question": "data race چیست؟",
         "options": ["دو نخ یک داده را می‌خوانند", "دو نخ بدون همگام‌سازی روی همان داده می‌نویسند", "کدِ سریع", "یک benchmark"],
         "answer": 1, "explain": "نوشتنِ هم‌زمانِ بدون همگام‌سازی = رفتار تعریف‌نشده. از atomic یا mutex استفاده کن."},
    ],
},

    "cpp38": {"title": "lifetime شیء و حافظهٔ پیشرفته", "lessons": [
        {"title": "lifetime شیء و دسته‌های مقدار", "html": """
<p><b>دسته‌های مقدار</b> — بنیادِ معناشناسی انتقال: lvalue (دارد
هویت)، prvalue (موقت)، xvalue (در حال انقضا). <b>رفتار تعریف‌نشده</b>:
بازگشاییِ null، سرریز بافر، استفاده بعد از آزادسازی... کامپایلر فرض
می‌کند UB رخ نمی‌دهد — Use sanitizers برای یافتنشان.</p>
""",},
    ],
},

    "cpp39": {"title": "قالب‌های پیشرفته", "lessons": [
        {"title": "فرaprogramming، SFINAE و perfect forwarding", "html": """
<p><b>فرaprogramming با قالب‌ها</b> — محاسبه در زمانِ کامپایل با نوع‌ها.
<b>type traits</b> ویژگی‌های نوع را می‌پرسند. <b>perfect forwarding</b>
آرگومان‌ها را با حفظِ دستهٔ مقدار عبور می‌دهد.</p>
""",},
    ],
},

    "cpp40": {"title": "perfect forwarding", "lessons": [
        {"title": "مرجع‌های forwarding و std::forward", "html": """
<p><b>مرجع‌های forwarding</b> (‏T&& در زمینهٔ استنتاج) به هم lvalue و هم
rvalue می‌سپارند. <code>std::forward</code> دستهٔ مقدارِ اصلی را حفظ
می‌کند — lvalue کپی می‌شود، rvalue منتقل می‌شود.</p>
""",},
    ],
},

    "cpp41": {"title": "قابلیت‌های C++23", "lessons": [
        {"title": "نکات برجستهٔ C++23", "html": """
<p><b>‏C++23</b>: std::print/std::println (خروجی قالب‌بندی‌شده)،
std::expected، deducing this، std::mdspan، std::generator،
std::stacktrace، std::flat_map/flat_set، بهبودهای ranges و views، if
consteval، std::byteswap و بیشتر.</p>
""",},
    ],
},

    "cpp42": {"title": "کتابخانهٔ استاندارد C++23", "lessons": [
        {"title": "گشت‌وگذار در کتابخانهٔ استاندارد", "html": """
<p>سربرگ‌های مهم: algorithm، vector، string، string_view، map، set،
unordered_map/unordered_set، memory، optional، variant، expected، span،
ranges، concepts، format، thread، mutex، atomic، filesystem، chrono —
هرکدام ابزاری در جعبه‌ابزارِ ++C مدرن.</p>
""",},
    ],
},

    "cpp43": {"title": "راهنماهای اصلیِ C++", "lessons": [
        {"title": "راهنماهای اصلیِ C++", "html": """
<p><b>راهنماهای اصلیِ C++</b> (استراستروپ و ساتر) بهترین شیوه‌ها را
کدبندی می‌کنند: RAII همه‌جا، بیانِ نیت (const، constexpr، noexcept)،
بدون raw new/delete، pass by const& برای خواندن، concepts برای قیدهای
قالب، spans/string_viewها برای پارامترها، و قاعدهٔ ۰ به‌عنوان ایده‌آل.</p>
""",},
    ],
},

    "cpp44": {"title": "‏C++ حرفه‌ای", "lessons": [
        {"title": "‏C++ حرفه‌ای", "html": """
<p>از یادگیریِ ++C تا ارسالِ ++C: سیستم‌های build (‏CMake)، تست (‏Google
Test، Catch2)، دیباگ (‏GDB، LLDB)، پروفایلینگ (perf، Valgrind)، تحلیل
ایستا (clang-tidy)، sanitizerها، مدیران بسته (vcpkg، Conan)، و CI/CD.
سازمان‌دهی: رابط (.hpp) جدا از پیاده‌سازی (.cpp)، namespace برای
جلوگیری از تصادم، مستندسازی با Doxygen.</p>

<p>شما سفر را از «‏C++ چیست؟» تا ++C23 حرفه‌ای کامل کرده‌اید. ادامه
دهید — زبان هر سه سال تکامل می‌یابد و اکوسیستم همیشه در حالِ
رشد است.</p>
""",},
    ],
},
}
