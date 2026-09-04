"""Persian variants of the Library Reference chapters (20-23).

[[codeN]] splices the English lesson's N-th <pre class="code"> block and
[[diag:...]] renders the shared SVG, so code and diagrams stay identical.
"""

FA_LIBRARY = {
    # ------------------------------------------------------------------ 20
    "ch20": {
        "lessons": [
            {
                "title": "آشنایی با Path — مسیرها بدون بازی با رشته",
                "html": """
<p>سال‌ها مسیر یعنی دست‌به‌گریبان شدن با رشته‌ها و اسلش‌ها. ماژول
<code>pathlib</code> به همهٔ این‌ها پایان داد: مسیرها <b>شیء</b>اند با متد.
یکی با <code>Path(...)</code> بساز و بعد فرزندها را با عملگر <code>/</code>
اضافه کن:</p>

[[code0]]

<p>همان شیء با پلتفرمی که رویش اجرا می‌شوی سازگار می‌شود. نقطه‌های شروع
رایج: <code>Path.cwd()</code> (پوشهٔ جاری) و <code>Path.home()</code>
(پوشهٔ خانگی تو).</p>

<p>هر جزء یک مسیر یک ویژگی است، پس هرگز رشته را با دست تجزیه نمی‌کنی:</p>

[[code1]]

[[diag:path_parts]]

<p>بررسی اینکه چیزی چیست، هر کدام یک فراخوانی است:</p>

[[code2]]

<p>در پایتون ۳٫۱۴ این بررسی‌ها روی مسیرهای خراب به‌جای پرتاب
<code>OSError</code> مقدار <code>False</code> می‌دهند — پس
<code>if p.exists():</code> را همه‌جا می‌توانی امن بنویسی.</p>

<p>برای پیدا کردن فایل‌ها از <b>الگوهای glob</b> استفاده کن — همان
wildcardهای <code>*</code>/<code>?</code> که از شل می‌شناسی:</p>

[[code3]]
""",
            },
            {
                "title": "خواندن، نوشتن، پیمایش و کپی",
                "html": """
<p>خواندن و نوشتن فایل دو متد است، بدون سر و کله‌زدن با <code>open()</code>:</p>

[[code0]]

<p>یک handle واقعی فایل لازم داری؟ <code>p.open()</code> دقیقاً مثل
<code>open()</code> داخلی رفتار می‌کند؛ پس <code>with p.open() as f:</code>
همان‌طور کار می‌کند.</p>

<p>پوشه‌ها: <code>mkdir()</code> یکی می‌سازد. با
<code>parents=True, exist_ok=True</code> همهٔ سطح‌های نبوده را هم می‌سازد،
مثل <code>mkdir -p</code>:</p>

[[code1]]

<p>برای دیدن محتویات یک پوشه، رویش پیمایش کن:</p>

[[code2]]

<p>کل درخت را به‌صورت بازگشتی می‌خواهی؟ <code>walk()</code> (از ۳٫۱۲)
سه‌تایی‌های <code>(dirpath, dirnames, filenames)</code> می‌دهد — جایگزین
مدرن <code>os.walk()</code>:</p>

[[code3]]

<p>و خبر بزرگ ۳٫۱۴: pathlib بالاخره متدهای <b>کپی</b> داخلی می‌گیرد. دیگر
برای کارهای ساده سراغ <code>shutil</code> نرو:</p>

[[code4]]

<p><b>ایدهٔ پروژهٔ کوچک:</b> حجم کل همهٔ فایل‌های <code>.py</code> یک درخت،
در سه خط:</p>

[[code5]]
""",
            },
        ],
        "quiz": [
            {
                "question": "کدام ویژگی نام فایل را بدون پسوندش می‌دهد؟",
                "options": ["p.name", "p.stem", "p.suffix", "p.parent"],
                "explain": "notes.txt یعنی name='notes.txt'، stem='notes'، suffix='.txt'. stem آخرین پسوند را حذف می‌کند.",
            },
            {
                "question": "مسیرهای فرزند را با این عملگر بساز: p = Path('data') ____ 'notes.txt'",
                "explain": "عملگر / بخش‌های مسیر را به هم می‌چسباند: Path('data') / 'notes.txt'.",
            },
            {
                "question": "فایل‌های پایتونِ پوشهٔ جاری را بشمار:",
                "explain": "Path('.').glob('*.py') همهٔ فایل‌هایی که به .py ختم می‌شوند را در پوشهٔ جاری پیدا می‌کند.",
            },
            {
                "question": "کدام عملیات فایل در پایتون ۳٫۱۴ کاملاً تازه است؟",
                "options": ["p.read_text()", "p.copy_into('backup/')", "p.glob('*.py')", "p.mkdir()"],
                "explain": "copy() و copy_into() در ۳٫۱۴ اضافه شده‌اند — pathlib بالاخره بدون shutil فایل کپی می‌کند.",
            },
        ],
    },

    # ------------------------------------------------------------------ 21
    "ch21": {
        "lessons": [
            {
                "title": "Counter، defaultdict و namedtuple",
                "html": """
<p>ماژول <code>collections</code> جعبه‌ابزار ظرف‌های هوشمندتر توست. اول:
<b>شمردن</b> چیزها، که آن‌قدر رایج است که کلاس خودش را دارد.</p>

[[code0]]

[[diag:counter_flow]]

<p>دوم: <b>دیکشنری‌هایی که پیش‌فرض خودشان را می‌سازند</b>.
<code>defaultdict(factory)</code> هر وقت کلیدی نبود تابع factory را صدا
می‌زند — پس گروه‌بندی هرگز به بررسی <code>if key in d</code> نیاز
ندارد:</p>

[[code1]]

<p>سوم: <b>تاپل‌های نام‌دار</b>. یک تاپل معمولی <code>(11, 22)</code>
است؛ namedtuple معنا را صریح می‌کند:</p>

[[code2]]

<p>namedtupleها بیشتر از تاپل ساده حافظه نمی‌گیرند — برای ردیف‌های داده عالی‌اند
(مستندات حتی برای نتیجهٔ <code>csv</code> و <code>sqlite3</code> پیشنهادشان
می‌دهند).</p>
""",
            },
            {
                "title": "itertools، functools و dataclasses",
                "html": """
<p><code>itertools</code> باغ تابع‌های کتابخانهٔ استاندارد است — تکرارگرهای
تنبل و کم‌حافظه که مثل بلوک‌های ساختمانی ترکیب می‌شوند.</p>

[[code0]]

[[diag:itertools_flow]]

<p><code>batched()</code> (از ۳٫۱۲) هر جریانی را به تکه‌های هم‌اندازه گروه
می‌کند — برای صفحه‌بندی یا دسته‌بندی کار ایده‌آل است. <code>count()</code>،
<code>cycle()</code> و <code>repeat()</code> هیچ‌وقت تمام نمی‌شوند؛ پس
آن‌ها را با <code>islice()</code> یا یک حلقهٔ <code>for</code> که می‌ایستد
ترکیب کن.</p>

<p><code>functools</code> کمکی‌های تابعی را نگه می‌دارد. دو تا که مدام
استفاده می‌کنی:</p>

[[code1]]

<p>و <code>dataclasses</code> boilerplate کلاس‌های دادهٔ ساده را حذف
می‌کند — دکوراتور <code>__init__</code>، <code>__repr__</code> و
<code>__eq__</code> را برایت می‌نویسد:</p>

[[code2]]
""",
            },
        ],
        "quiz": [
            {
                "question": "<code>Counter.most_common(3)</code> چه چیزی برمی‌گرداند؟",
                "options": [
                    "۳ کلید پرتکرار بدون رتبه‌بندی",
                    "فهرستی از جفت‌های (item, count) که پرتکرارترین اول است",
                    "یک دیکشنری از ۳ آیتم پرتکرار",
                    "یک ست از ۳ کلید پرتکرار",
                ],
                "explain": "most_common(n) فهرستی از تاپل‌های (element, count) برمی‌گرداند که از پرتکرارترین به کم‌تکرارترین مرتب شده‌اند.",
            },
            {
                "question": "بدون بررسی 'if key in d' مقدارها را گروه‌بندی کن: defaultdict(____)",
                "explain": "defaultdict(list) برای هر کلید تازه خودکار یک لیست خالی می‌سازد، پس d[k].append(v) همان‌طور کار می‌کند.",
            },
            {
                "question": "کدام تابع itertools یک جریان را به تاپل‌های هم‌اندازه تکه می‌کند؟",
                "options": ["chain", "batched", "cycle", "combinations"],
                "explain": "batched('ABCDEFG', 3) جفت‌های ('A','B','C')، ('D','E','F') و ('G',) می‌دهد — دستهٔ آخر ممکن است کوتاه باشد.",
            },
            {
                "question": "نتیجه‌های این تابع را با یک دکوراتور کش کن:",
                "explain": "@lru_cache(maxsize=None) هر فراخوانی را به خاطر می‌سپارد؛ پس بازگشت نمایی در زمان خطی اجرا می‌شود.",
            },
        ],
    },

    # ------------------------------------------------------------------ 22
    "ch22": {
        "lessons": [
            {
                "title": "JSON و CSV",
                "html": """
<p>برنامه‌ها با <b>JSON</b> با هم حرف می‌زنند — فرمت دادهٔ همگانی وب.
دیکشنری پایتون و JSON تقریباً یک چیزند، پس ماژول <code>json</code> دو تابع
است:</p>

[[code0]]

[[diag:json_roundtrip]]

<p><code>indent=2</code> آن را برای انسان‌ها مرتب چاپ می‌کند؛ بدونش یک خط
فشرده می‌گیری. <code>ensure_ascii=False</code> نویسه‌های غیر-ASCII را
خوانا نگه می‌دارد به‌جای escape کردنشان.</p>

<p>خواندن فایل JSON: <code>json.load(open('data.json'))</code>. نوشتن یکی:
<code>json.dump(data, open('out.json', 'w'), indent=2)</code>.</p>

<p><b>CSV</b> (صفحه‌گسترده‌ها) هم همین‌قدر آسان است. خواندن با
<code>DictReader</code> از ردیف سربرگ به‌عنوان کلید استفاده می‌کند:</p>

[[code1]]

<p><code>newline=''</code> مهم است: مدیریت خودِ csv برای خط جدید وگرنه
فایل‌های ویندوز را خراب می‌کند. نوشتن هم متقارن است — با
<code>csv.writer(f).writerow([...])</code> یا <code>DictWriter</code> با
فهرست <code>fieldnames=</code>. مستندات collections تاپل‌های نام‌دار را با
ردیف‌های csv خوب جفت می‌کنند:</p>

[[code2]]
""",
            },
            {
                "title": "گفت‌وگو با وب",
                "html": """
<p>گرفتن یک صفحهٔ وب سه خط برمی‌دارد با <code>urllib.request</code> — بدون
نیاز به هیچ بستهٔ شخص ثالث:</p>

[[code0]]

<p><code>urlopen</code> یک شیء پاسخ به تو می‌دهد؛ صفحه به‌صورت
<b>bytes</b> برمی‌گردد، پس <code>.decode('utf-8')</code> آن را به متن تبدیل
می‌کند.</p>

<p>حالا بخش بامزه — آن را با ماژول <code>json</code> درسِ قبل ترکیب کن تا
بتوانی <b>APIهای عمومی وب</b> را صدا بزنی:</p>

[[code1]]

<p>همین یک الگو — گرفتن، decode کردن JSON، استفاده از دیکشنری — اپ‌های آب‌وهوا،
ربات‌های خبر و ردیاب‌های سهام را تغذیه می‌کند. در playground با یک API رایگان
دلخواه امتحانش کن.</p>

<p>دو هشدار از مستندات: <code>urlopen</code> برای پاسخ‌های بد
<code>HTTPError</code> پرتاب می‌کند، پس فراخوانی‌های شبکه را در
<code>try/except</code> بپیچ؛ و هرگز بدون فکر کردن به اینکه واقعاً هر چند وقت
یک‌بار به دادهٔ تازه نیاز داری، داخل یک حلقهٔ فشرده API صدا نزن.</p>
""",
            },
        ],
        "quiz": [
            {
                "question": "کدام تابع یک دیکشنری پایتون را به رشتهٔ JSON تبدیل می‌کند؟",
                "options": ["json.loads", "json.dumps", "json.stringify", "json.encode"],
                "explain": "dumps یعنی dump به string (dict → str)؛ loads یعنی load از string (str → dict).",
            },
            {
                "question": "JSON را مرتب چاپ کن: json.dumps(data, ____=2)",
                "explain": "indent=2 خط جدید و تورفتگی دو فاصله‌ای اضافه می‌کند تا JSON برای انسان خوانا شود.",
            },
            {
                "question": "کدام reader ردیف سربرگ CSV را کلید دیکشنری می‌کند؟",
                "options": ["csv.reader", "csv.DictReader", "csv.KeyReader", "csv.RowReader"],
                "explain": "DictReader ردیف سربرگ را به کلیدها نگاشت می‌کند؛ پس هر ردیف دیکشنری است: row['name']، row['age'].",
            },
            {
                "question": "یک صفحه بگیر و bytes را به متن تبدیل کن:",
                "explain": "resp.read() bytes برمی‌گرداند؛ .decode('utf-8') آن‌ها را به str تبدیل می‌کند که بتوانی چاپ و جستجو کنی.",
            },
        ],
    },

    # ------------------------------------------------------------------ 23
    "ch23": {
        "lessons": [
            {
                "title": "ابزارهای خط فرمان (argparse + subprocess)",
                "html": """
<p>برنامه‌های واقعی ابزارهایی هستند که از ترمینال اجرا می‌کنی. ماژول
<code>argparse</code> یک اسکریپت ساده را به دستور واقعی با
<code>--flag</code> و <code>--help</code> داخلی تبدیل می‌کند:</p>

[[code0]]

[[diag:cli_flow]]

<p>اجرایش کن: <code>python greet.py --name Ada</code> چاپ می‌کند
<code>Hello, Ada!</code>. <code>--shout</code> یک flag از نوع
<code>store_true</code> است — همین که حاضر باشد یعنی <code>True</code>. و
<code>python greet.py --help</code> خلاصهٔ راهنما را رایگان چاپ می‌کند.</p>

<p>گاهی برنامهٔ پایتونی‌ات باید <em>برنامهٔ دیگری</em> را اجرا کند.
<code>subprocess</code> این کار را امن انجام می‌دهد:</p>

[[code1]]

<p><code>capture_output=True</code> خروجی را می‌گیرد، <code>text=True</code>
آن را به‌جای bytes به‌صورت رشته برمی‌گرداند و <code>check=True</code> باعث
می‌شود شکست‌ها پرتاب شوند به‌جای ادامهٔ بی‌صدا. فهرستی از آرگومان‌ها را ترجیح
بده (نه یک رشتهٔ شل) — بدون باگ کوتیشن، بدون تزریق شل.</p>
""",
            },
            {
                "title": "پایگاه داده، لاگ و آزمون (sqlite3 + logging + unittest)",
                "html": """
<p>برنامه‌های واقعی داده را در پایگاه داده نگه می‌دارند. پایتون با
<code>sqlite3</code> همراه است — یک موتور کامل SQL در یک فایل:</p>

[[code0]]

[[diag:sqlite_tables]]

<p>جای‌نگه‌دارهای <code>?</code> غیرقابل مذاکره‌اند: مقدارها به‌عنوان
آرگومان رد می‌شوند، هرگز داخل رشتهٔ SQL چسبانده نمی‌شوند — این‌طور از باگ
تزریق جلوگیری می‌کنی. <code>commit()</code> نوشتن‌ها را دائمی می‌کند.</p>

<p><b>لاگ‌گیری</b> برای هر چیز واقعی از <code>print()</code> بهتر است. با
یک خط زمان‌سنج، سطح‌بندی و امکان بی‌صدا کردن نویز را می‌گیری:</p>

[[code1]]

<p>سطح‌ها از <code>DEBUG &lt; INFO &lt; WARNING &lt; ERROR &lt; CRITICAL</code>
می‌گذرند؛ <code>basicConfig(level=...)</code> تصمیم می‌گیرد چه چیزی نشان
داده شود.</p>

<p>و در آخر <b>آزمون‌ها</b>. <code>unittest</code> داخلی است — یک
<code>TestCase</code> بنویس و با <code>python -m unittest</code> اجرا
کن:</p>

[[code2]]

<p>این کل چرخهٔ یک برنامهٔ واقعی است: <b>تجزیهٔ آرگومان‌ها، انجام کار،
ذخیرهٔ داده، لاگ کردن اتفاقات، و آزمون اینکه کار می‌کند</b>.</p>
""",
            },
        ],
        "quiz": [
            {
                "question": "مقدارها چطور باید در یک پرس‌وجوی sqlite3 وارد شوند؟",
                "options": [
                    "با f-string داخل SQL چسبانده شوند",
                    "به‌صورت جای‌نگه‌دار ? با مقدارهای جداگانه",
                    "راه امنی وجود ندارد",
                    "فقط با متد .format()",
                ],
                "explain": "جای‌نگه‌دارهای ? با آرگومان‌های جدا SQL را از تزریق و باگ کوتیشن امن نگه می‌دارند.",
            },
            {
                "question": "نوشتن‌ها را در sqlite3 دائمی کن: conn.____()",
                "explain": "commit() تراکنش‌های در انتظار را در فایل پایگاه داده ذخیره می‌کند؛ بدون آن تغییرها از دست می‌روند.",
            },
            {
                "question": "تنظیم argparse را کامل کن تا مقدار flag در دسترس باشد:",
                "explain": "parser.parse_args() خط فرمان را می‌خواند و یک namespace برمی‌گرداند؛ flagها صفت‌هایی مثل args.name می‌شوند.",
            },
            {
                "question": "همهٔ آزمون‌های یک فایل را اجرا کن: python -m ____",
                "options": ["testing", "unittest", "pytest", "test"],
                "explain": "python -m unittest همهٔ کلاس‌های TestCase پوشهٔ جاری را پیدا و اجرا می‌کند.",
            },
        ],
    },
}
