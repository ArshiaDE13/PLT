"""Persian variants of JS Tutor chapters 6-8 (chapters_js_c).

[[codeN]] is spliced from the English lesson's N-th <pre class="code">
block at build time.
"""

FA_JS_C = {
    "js06": {
        "title": "شیءهای داخلی",
        "lessons": [
            {
                "title": "ابزارهای سراسری Object و Array",
                "html": """
<p>شیءهای سراسری <code>Object</code> و <code>Array</code> متدهای
کاربردیِ static می‌دهند:</p>

[[code0]]

<p>متدهای نمونهٔ آرایه که باید بشناسی:
<code>at(-1)</code> (آخرین عنصر)، <code>flat()</code>،
<code>flatMap()</code>، <code>includes()</code>،
<code>indexOf()</code>، <code>fill()</code>، <code>reverse()</code> و
<code>splice()</code> (تغییر می‌دهد!).</p>
""",
            },
            {
                "title": "ابزارهای سراسری String و Number",
                "html": """
<p>شیءهای سراسری <code>String</code> و <code>Number</code> متدهای
تبدیل و کاربردی می‌دهند:</p>

[[code0]]
""",
            },
            {
                "title": "Math",
                "html": """
<p>شیء <code>Math</code> ثابت‌ها و توابع ریاضی می‌دهد — همیشه موجود و
هرگز نمونه‌سازی نمی‌شود:</p>

[[code0]]

<p>الگوهای رایج:</p>

[[code1]]
""",
            },
            {
                "title": "Date",
                "html": """
<p>شیء <code>Date</code> تاریخ و زمان را مدیریت می‌کند. ماه‌ها از صفر
شروع می‌شوند (۰ = ژانویه) — تلهٔ کلاسیک!</p>

[[code0]]

<p>قالب‌بندی با <code>toLocaleString</code> و
<code>Intl.DateTimeFormat</code>:</p>

[[code1]]
""",
            },
            {
                "title": "RegExp",
                "html": """
<p>عبارات باقاعده در رشته‌ها الگو می‌گیرند — با نگارهٔ
<code>/الگو/پرچم‌ها</code> یا <code>new RegExp("الگو")</code>:</p>

[[code0]]
""",
            },
            {
                "title": "Map، Set، WeakMap و WeakSet",
                "html": """
<p><b>Map</b> ذخیرهٔ کلید-مقدار است که کلیدها می‌توانند هر نوعی باشند
(نه فقط رشته مثل شیءها):</p>

[[code0]]

<p><b>Set</b> مجموعه‌ای از مقدارهای یکتاست:</p>

[[code1]]

<p><b>WeakMap/WeakSet</b> — کلیدها باید شیء باشند و <i>ضعیف</i> نگه
داشته می‌شوند: اگر شیءِ کلید garbage-collect شود، ورودی خودکار حذف
می‌شود. برای کش و فراداده بدون نشتِ حافظه.</p>
""",
            },
            {
                "title": "JSON",
                "html": """
<p><b>JSON (نمادگذاری شیء جاوااسکریپت)</b> قالبِ همگانیِ داده برای
APIهاست. دو متد همه‌کار می‌کنند:</p>

[[code0]]

<p>محدودیت‌های JSON: بدون تابع، بدون undefined، بدون کامنت، بدون
ارجاعِ چرخه‌ای (خطا می‌دهد). تاریخ‌ها رشته می‌شوند.</p>
""",
            },
            {
                "title": "Error و Promise (پیش‌نمایش)",
                "html": """
<p>شیءهای <b>Error</b> اطلاعاتِ خطا را حمل می‌کنند. انواع داخلی:
<code>Error</code>، <code>TypeError</code>،
<code>ReferenceError</code>، <code>RangeError</code> و
<code>SyntaxError</code>. با extend، خطای سفارشی بساز:</p>

[[code0]]

<p><b>Promise</b> مقداری را نمایندگی می‌کند که بعداً در دسترس خواهد بود
— بنیانِ جاوااسکریپتِ ناهمگام (فصل ۷ کاملش را دارد). Promise را از
<code>fetch()</code>، پوشش‌های <code>setTimeout()</code> و هر API
async مدرن برمی‌گردنده می‌بینی.</p>
""",
            },
        ],
        "quiz": [
            {
                "question": "کدام متد تکراری‌های آرایه را حذف می‌کند؟",
                "options": ["arr.unique()", "[...new Set(arr)]", "arr.distinct()", "arr.filter()"],
                "answer": 1,
                "explain": "Set فقط مقدارهای یکتا نگه می‌دارد؛ بازگستردنش آرایهٔ بدون تکرار می‌دهد.",
            },
            {
                "question": "متدِ تبدیل شیء به رشتهٔ JSON، <code>JSON.____</code> است.",
                "answers": ["stringify"],
                "explain": "JSON.stringify سریال می‌کند؛ JSON.parse برمی‌گرداند.",
            },
            {
                "question": "مزیتِ اصلی WeakMap نسبت به Map چیست؟",
                "options": [
                    "سریع‌تر است",
                    "کلید می‌تواند هر نوعی باشد",
                    "ورودی‌ها با نابودیِ شیءِ کلید، garbage-collect می‌شوند",
                    "متدهای بیشتری دارد",
                ],
                "answer": 2,
                "explain": "ارجاع‌های ضعیف، وقتی شیءهای کلید دیگر لازم نیستند، از نشت حافظه جلوگیری می‌کنند.",
            },
        ],
    },

    "js07": {
        "title": "جاوااسکریپت ناهمگام",
        "lessons": [
            {
                "title": "همگام در برابر ناهمگام",
                "html": """
<p>JS <b>تکنخی</b> است — فقط یک کار هم‌زمان. کدِ <b>همگام</b>
می‌بندد: هر خط منتظرِ قبلی می‌ماند. کدِ <b>ناهمگام</b> کار را برای بعد
زمان‌بندی می‌کند بدون بستن:</p>

[[code0]]

<p>حلقهٔ رخداد: JS اول کدِ sync را اجرا می‌کند، بعد <b>صفِ callback</b>
(تایمرها، رخدادها) و <b>صفِ میکروتسک</b> (promiseها) را پردازش می‌کند.
میکروتسک‌ها همیشه قبل از تایمرِ بعدی اجرا می‌شوند. برای همین callbackهای
promise قبل از callbackهای setTimeout اجرا می‌شوند.</p>
""",
            },
            {
                "title": "callbackها و Promiseها",
                "html": """
<p><b>callbackها</b> الگوی اصلیِ async بودند — تابعی بده که وقتی عملیات
تمام شد صدا زده شود. callbackهای تودرتو برای عملیات ترتیبی
<b>جهنمِ callback</b> می‌سازند:</p>

[[code0]]

<p>یک <b>Promise</b> مقداری را نمایندگی می‌کند که بعداً در دسترس خواهد
بود. سه وضعیت دارد: <b>pending</b> → <b>fulfilled</b> (با مقدار) یا
<b>rejected</b> (با خطا). وقتی settle شد، وضعیتش دیگر هرگز عوض
نمی‌شود:</p>

[[code1]]

<p>promiseها زنجیر می‌شوند — هر <code>.then()</code> مقدارِ برگشتیِ
قبلی را می‌گیرد و جهنمِ callback را به زنجیره‌ای خوانا
تخت می‌کند.</p>
""",
            },
            {
                "title": "then()‎، catch()‎ و finally()‎",
                "html": """
<p>سه متدِ نمونه که هر promise‌ای دارد:</p>

[[code0]]

<p><code>.catch()</code> خطاها از <b>هر</b> then قبلی را می‌گیرد — مثل
try/catch برای کلِ زنجیره. <code>.finally()</code> نتیجه را نمی‌گیرد؛
برای پاک‌سازی است (پنهان‌کردن اسپینر، بستنِ اتصال).</p>
""",
            },
            {
                "title": "Promise.all()‎، allSettled()‎، race()‎ و any()‎",
                "html": """
<p>چهار متدِ static برای مدیریتِ <b>چند promise</b>:</p>

[[code0]]

<ul>
<li><b>all</b> — سریع‌شکن: یک رد، کل را رد می‌کند</li>
<li><b>allSettled</b> — هرگز رد نمی‌شود؛ وضعیتِ هرکدام را می‌دهد</li>
<li><b>race</b> — اولین settleشده (حتی رد‌شده) می‌برد</li>
<li><b>any</b> — اولین fulfilled می‌برد؛ فقط اگر همه رد شوند رد
می‌شود</li>
</ul>
""",
            },
            {
                "title": "async و await",
                "html": """
<p><code>async/await</code> شکرِ نحوی روی promiseهاست که کد async را
<b>شبیه کد همگام</b> نشان می‌دهد و می‌خوانَد:</p>

[[code0]]

<p><code>await</code> فقط داخل توابع <code>async</code> (یا سطحِ ماژول)
کار می‌کند. تابع async را مکث می‌دهد نه کل نخ را — بقیهٔ کد ادامه
می‌یابد.</p>
""",
            },
            {
                "title": "مدیریت خطا در کد async",
                "html": """
<p>خطاهای async با try/catch معمولی گرفته نمی‌شوند — بسته به الگو،
مدیریتِ خاص می‌خواهند:</p>

[[code0]]

<p>همیشه خطاهای async را هندل کن: یک rejectionِ مدیریت‌نشده، Node.js
مدرن را کرش می‌کند و در مرورگر خطاهای زشتِ console می‌سازد. به‌عنوان
تورِ نجات، هندلر سراسری اضافه کن:
<code>window.addEventListener("unhandledrejection", e =&gt; ...)</code></p>
""",
            },
        ],
        "quiz": [
            {
                "question": "تابع async همیشه چه برمی‌گرداند؟",
                "options": ["undefined", "یک Promise", "مقدارِ resolveشده", "یک iterator"],
                "answer": 1,
                "explain": "توابع async مقدارِ برگشتی‌شان را در Promise.resolve() می‌پیچند.",
            },
            {
                "question": "عملگری که داخل تابع async مکث می‌کند <code>____</code> است.",
                "answers": ["await", "عملگر await"],
                "explain": "await تابع async را تا settle شدنِ promise نگه می‌دارد.",
            },
            {
                "question": "Promise.all() کی رد می‌شود؟",
                "options": ["وقتی همه رد شوند", "وقتی هر promiseای رد شود", "وقتی اولین settle شود", "هرگز"],
                "answer": 1,
                "explain": "Promise.all سریع‌شکن است: یک رد، کلِ بسته را رد می‌کند.",
            },
            {
                "question": "اشتباهِ شمارهٔ ۱ در مدیریت خطای async/await:",
                "options": [
                    "استفاده از try/catch",
                    "جا انداختنِ await قبل از فراخوانی promise",
                    "استفاده از catch.()",
                    "پرتابِ خطای زیاد",
                ],
                "answer": 1,
                "explain": "بدون await، try/catch خطای async را نمی‌بیند — مدیریت‌نشده می‌ماند.",
            },
            {
                "question": "کدام متد Promise هرگز رد نمی‌شود؟",
                "options": ["Promise.all()", "Promise.race()", "Promise.allSettled()", "Promise.any()"],
                "answer": 2,
                "explain": "allSettled همیشه با {status, value/reason} برای هر promise	resolve می‌شود.",
            },
        ],
    },

    "js08": {
        "title": "ماژول‌ها",
        "lessons": [
            {
                "title": "ماژول‌ها: export و import",
                "html": """
<p><b>ماژول‌ها</b> فایل‌های خودبسنده‌ای هستند که مقدارها را برای import
کردنِ فایل‌های دیگر export می‌کنند. JS مدرن ماژول‌های ES را بومی
دارد:</p>

[[code0]]

<p>ماژول‌ها به‌طور پیش‌فرض <b>strict mode</b>ند، <b>deferred</b> (بعد از
پارس HTML لود می‌شوند) و <b>کش</b> می‌شوند (یک بار import، بین همهٔ
importerها مشترک). سازمان‌دهی کد، مدیریت وابستگی و tree-shaking (حذف
کد بلااستفاده هنگام build) را ممکن می‌کنند.</p>

<p>در مرورگر: <code>&lt;script type="module" src="app.js"&gt;</code>. در
Node.js: پسوند <code>.mjs</code> یا <code>"type": "module"</code> در
package.json.</p>
""",
            },
            {
                "title": "import()‎ پویا و تفکیک ماژول",
                "html": """
<p><b>import پویا</b> ماژول را در لحظهٔ نیاز لود می‌کند — یک Promise
برمی‌گرداند. همین، تقسیم کد و لودِ تنبل را ممکن می‌کند:</p>

[[code0]]

<p>تفکیک ماژول: مرورگر مسیرهای نسبی (<code>./utils.js</code>) را حل
می‌کند، مسیرهای خالی به import map نیاز دارند و پسوند فایل در مرورگرها
الزامی است (برخلاف بعضی bundlerها).</p>
""",
            },
        ],
        "quiz": [
            {
                "question": "یک ماژول چند default export می‌تواند داشته باشد؟",
                "options": ["صفر", "یکی", "نامحدود", "یکی به‌ازای هر نوع"],
                "answer": 1,
                "explain": "هر ماژول دقیقاً یک default export دارد (به‌علاوهٔ هر تعداد named export).",
            },
            {
                "question": "import پویا یک ____ برمی‌گرداند.",
                "answers": ["promise", "Promise"],
                "explain": "import() یک Promise برمی‌گرداند که به namespace ماژول resolve می‌شود.",
            },
        ],
    },
}
