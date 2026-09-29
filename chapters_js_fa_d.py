"""Persian variants of JS Tutor chapters 9-10 (chapters_js_d).

[[codeN]] is spliced from the English lesson's N-th <pre class="code">
block at build time.
"""

FA_JS_D = {
    "js09": {
        "title": "جاوااسکریپت مرورگر",
        "lessons": [
            {
                "title": "DOM و انتخاب عنصرها",
                "html": """
<p><b>DOM (Document Object Model)</b> درختی زنده از شیءهاست که HTML را
آینه می‌کند. جاوااسکریپت آن را می‌خواند و دستکاری می‌کند تا صفحه‌ها
تعاملی شوند:</p>

[[code0]]

<ul>
<li><code>querySelector</code> — با سلکتورهای CSS کار می‌کند، اولین
تطبیق را می‌دهد (یا null)</li>
<li><code>querySelectorAll</code> — یک NodeList ثابت برمی‌گرداند (با
<code>forEach</code> یا spread به آرایه استفاده کن)</li>
<li><code>getElementById</code> — سریع‌ترین، اما فقط برای IDها</li>
</ul>
""",
            },
            {
                "title": "ساخت و تغییر عنصرها",
                "html": """
<p>جاوااسکریپت عنصرهای DOM را پویا می‌سازد، تغییر می‌دهد و حذف
می‌کند:</p>

[[code0]]

<p>برای دادهٔ عرضه‌شده از کاربر همیشه <code>textContent</code> را به
<code>innerHTML</code> ترجیح بده — innerHTML کد HTML را پارس می‌کند و
شماره‌یکِ آسیب‌پذیریِ XSS است.</p>
""",
            },
            {
                "title": "رخدادها و Event Listenerها",
                "html": """
<p><b>رخدادها</b> عمل‌های کاربرند: کلیک، فشردنِ کلید، اسکرول.
<code>addEventListener</code> راهِ پاسخ‌دادن است:</p>

[[code0]]

<p>شیءِ رخداد <code>event.target</code> دارد (چه چیزی کلیک شد)،
<code>event.key</code> (کدام کلید) و
<code>event.preventDefault()</code> برای توقفِ رفتار پیش‌فرض (ارسال فرم،
ناوبری لینک).</p>
""",
            },
            {
                "title": "حباب‌زدنِ رخداد و delegation",
                "html": """
<p>وقتی روی عنصری تودرتو کلیک می‌کنی، رخداد از هدف به پدرها <b>حباب
می‌زند</b>. این <b>event delegation</b> را ممکن می‌کند — یک listener
روی پدر، رخدادهای همهٔ فرزندان (حال و آینده) را هندل می‌کند:</p>

[[code0]]

<p>delegation چطور لیست‌های پویا کار می‌کنند — آیتم‌هایی که بعداً
اضافه می‌شوند خودکار هندل می‌شوند. <code>event.stopPropagation()</code>
وقتی لازم است حباب‌زدن را متوقف می‌کند.</p>
""",
            },
            {
                "title": "Fetch API و درخواست‌های HTTP",
                "html": """
<p><code>fetch()</code> درخواست‌های HTTP می‌فرستد — جایگزینِ مدرنِ
XMLHttpRequest:</p>

[[code0]]

<p>‏fetch یک Promise برمی‌گرداند که به شیءِ Response حل می‌شود. باید
<code>response.ok</code> را چک کنی — fetch فقط روی خطای شبکه رد
می‌شود، نه خطاهای HTTP (۴۰۴ و ۵۰۰ هم resolve می‌شوند!). متدها:
<code>.json()</code>، <code>.text()</code>، <code>.blob()</code>.</p>
""",
            },
            {
                "title": "Web Storage و کوکی‌ها",
                "html": """
<p><b>Web Storage</b> (localStorage + sessionStorage) جفت‌های
کلید-مقدار در مرورگر ذخیره می‌کند — از کوکی ساده‌تر:</p>

[[code0]]

<ul>
<li><b>localStorage</b> — تا حذفِ دستی دوام دارد</li>
<li><b>sessionStorage</b> — با بسته‌شدنِ تب می‌میرد</li>
<li><b>کوکی‌ها</b> — با هر درخواست به سرور می‌روند (محدودیت ۴KB،
سازوکارِ قدیمی؛ برای توکن‌های احرازِ هویت، نه داده)</li>
</ul>

<p>این اپ از localStorage برای نام، پیشرفت، زبان و کدِ playground
استفاده می‌کند — devtools → Application → Local Storage را ببین!</p>
""",
            },
            {
                "title": "APIهای مرورگر",
                "html": """
<p>مرورگر فراتر از DOM، APIهای زیادی می‌دهد. پرتکرارترین‌ها:</p>

<ul>
<li><b>setTimeout / setInterval / requestAnimationFrame</b> — زمان‌بندی و
انیمیشن</li>
<li><b>Geolocation</b> — مکانِ کاربر (با اجازه)</li>
<li><b>Clipboard</b> — کپی/پیست</li>
<li><b>Intersection Observer</b> — تشخیصِ ورودِ عنصر به viewport (لودِ
تنبل، انیمیشن)</li>
<li><b>Notifications</b> — اعلان‌های سیستم</li>
<li><b>Web Workers</b> — نخ‌های پس‌زمینه (در فصل HTML پوشش داده
شد)</li>
<li><b>History</b> — pushState/back (مسیریابی SPA)</li>
<li><b>Console</b> — log، warn، error، table، time...</li>
</ul>

<p>اینها زیرِ <b>Web APIs</b> در MDN مستند شده‌اند — جدا از خودِ زبانِ
جاوااسکریپت. هرکدام صفحهٔ MDN و اطلاعاتِ پشتیبانیِ مرورگرهای خودش را
دارد.</p>
""",
            },
        ],
        "quiz": [
            {
                "question": "querySelector چه برمی‌گرداند؟",
                "options": ["همهٔ عنصرهای منطبق", "اولین عنصرِ منطبق", "یک آرایه", "یک رشته"],
                "answer": 1,
                "explain": "querySelector اولین تطبیق را می‌دهد؛ querySelectorAll همه را.",
            },
            {
                "question": "راهِ امنِ ست‌کردنِ متن (بدون پارسِ HTML) <code>____</code> است.",
                "answers": ["textContent"],
                "explain": "textContent امن است؛ innerHTML کد HTML را پارس می‌کند و خطرِ XSS دارد.",
            },
            {
                "question": "event delegation یعنی:",
                "options": [
                    "فرستادنِ رخداد به سرور",
                    "یک listener روی پدر، رخدادهای همهٔ فرزندان را هندل می‌کند",
                    "حذفِ همهٔ listenerها",
                    "فقط استفاده از event.target",
                ],
                "answer": 1,
                "explain": "رخدادها به پدرها حباب می‌زنند — listener پدری، فرزندانِ آینده را هم می‌پوشاند.",
            },
            {
                "question": "‏fetch فقط روی خطاهای ____ رد می‌شود، نه HTTP 404/500.",
                "answers": ["شبکه"],
                "explain": "همیشه response.ok را چک کن — fetch حتی برای ۴۰۴/۵۰۰ هم resolve می‌شود.",
            },
        ],
    },

    "js10": {
        "title": "موضوعات پیشرفته",
        "lessons": [
            {
                "title": "مدیریت حافظه و garbage collection",
                "html": """
<p>JS مدیریت حافظهٔ خودکار دارد — <b>garbage collector (GC)</b>
شیءهایی را که دیگر قابل‌دسترس نیستند پیدا و حافظه‌شان را آزاد می‌کند.
مثل C لازم نیست <code>free()</code> صدا بزنی، اما هنوز می‌توانی حافظه
نشت بدهی:</p>

[[code0]]

<p>‏GC الگوریتم <b>mark-and-sweep</b> را به کار می‌گیرد: از ریشه‌ها (شیء
سراسری، متغیرهای محلیِ تابع فعلی) شروع می‌کند، همهٔ شیءهای
قابل‌دسترس را علامت می‌زند، بعد غیرقابل‌دسترس‌ها را جارو می‌کند. اگر
شیءی از یک ریشه قابل‌دسترس باشد، جمع‌آوری نمی‌شود — حتی اگر هیچ‌کس
«استفاده‌اش» نکند.</p>
""",
            },
            {
                "title": "Proxy، Reflect و فرaprogramming",
                "html": """
<p><b>Proxy</b> یک شیء را می‌پیچد و عملیات‌های رویش را رهگیری می‌کند —
دسترسی به ویژگی، انتساب، فراخوانی تابع. <b>Reflect</b> رفتارِ
پیش‌فرضِ این عملیات‌ها را می‌دهد:</p>

[[code0]]

<p>کاربردهای Proxy: اعتبارسنجی، لاگ، کنترل دسترسی، سیستم‌های
reactive (‏Vue.js از آن استفاده می‌کند!). <code>Reflect</code>
پیاده‌سازی‌های پیش‌فرض را می‌دهد تا داخل رهگیرهایت صدا بزنی.</p>
""",
            },
            {
                "title": "descriptorهای ویژگی و تغییرناپذیری",
                "html": """
<p>هر ویژگیِ شیء یک <b>descriptor</b> دارد با صفات:
<code>value</code>، <code>writable</code>، <code>enumerable</code> و
<code>configurable</code>. می‌توانی آن‌ها را ببینی و عوض کنی:</p>

[[code0]]

<p><b>enumerability</b> تعیین می‌کند که ویژگی در <code>for...in</code>،
<code>Object.keys()</code> و JSON دیده شود یا نه. متدهای داخلی (مثل
<code>toString</code>) غیرقابل‌شمارش‌اند — برای همین حلقه‌هایت را
شلوغ نمی‌کنند.</p>
""",
            },
            {
                "title": "بین‌المللی‌سازی، Typed Arrayها و بیشتر",
                "html": """
<p><b>بین‌المللی‌سازی (i18n)</b> — شیء <code>Intl</code> تاریخ، اعداد و
رشته‌ها را برای localeهای مختلف قالب‌بندی می‌کند:</p>

[[code0]]

<p><b>Typed Arrayها</b> — دادهٔ باینری با نوع‌های عددیِ اندازه‌ثابت برای
کدهای حساس به کارایی (canvas، WebGL، مدیریت فایل):</p>

[[code1]]

<p>این موضوعات تحصیلاتِ JS تو را کامل می‌کنند. راهنماهای MDN عمیق
پوشششان می‌دهند — تو حالا بنیادی داری که همه‌شان را بفهمی.</p>
""",
            },
        ],
        "quiz": [
            {
                "question": "garbage collectorِ JS از کدام الگوریتم استفاده می‌کند؟",
                "options": ["فقط شمارشِ ارجاع", "Mark-and-sweep", "free() دستی", "کپی collection"],
                "answer": 1,
                "explain": "شیءهای قابل‌دسترس را از ریشه‌ها علامت می‌زند، غیرقابل‌دسترس‌ها را جارو می‌کند.",
            },
            {
                "question": "Proxy می‌تواند چه چیزی را رهگیری کند؟",
                "options": [
                    "فقط خواندنِ ویژگی",
                    "خواندن، نوشتن، فراخوانی تابع و بیشتر",
                    "فقط درخواست‌های شبکه",
                    "فقط رخدادهای DOM",
                ],
                "answer": 1,
                "explain": "هندلرهای Proxy می‌توانند get، set، apply، has، delete و بیشتر را رهگیری کنند.",
            },
            {
                "question": "Object.____ شیء را کاملاً تغییرناپذیر می‌کند (نه افزودن، نه تغییر، نه حذف).",
                "answers": ["freeze"],
                "explain": "Object.freeze سخت‌گیرانه‌ترین است؛ Object.seal اجازهٔ تغییر می‌دهد اما نه افزودن/حذف.",
            },
        ],
    },
}
