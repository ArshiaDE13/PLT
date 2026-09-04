"""Chapters 17-19 of the course, distilled from the Python 3.14
"Python Setup and Usage" (using) documentation.

These sit right after the tutorial chapters and cover: the python
command line, environment variables, Python on Windows (install
manager, py launcher, venvs), and other platforms + editors.
"""

CHAPTERS_C = [
    # ------------------------------------------------------------------ 17
    {
        "id": "ch17",
        "title": "Running Python",
        "title_fa": "اجرای پایتون",
        "emoji": "⚙️",
        "lessons": [
            {
                "title": "The python command",
                "html": """
<p>Every Python session starts the same way: you run the
<code>python</code> command. What it does next depends on what you
give it:</p>

<pre class="code">python hello.py             # run a script file
python -c "print(2 + 2)"    # run a short command
python -m http.server       # run a module as a script
python                      # drop into the interactive shell</pre>

[[diag:invoke_flow]]

<p>With <code>-c</code>, everything after it is executed as Python
code. With <code>-m</code>, Python locates a module the normal import
way and runs it as the main program &mdash; <code>python -m
timeit "1 + 1"</code> benchmarks code, and
<code>python -m json.tool</code> pretty-prints JSON from the
command line.</p>

<p>Arguments after the script name end up in <code>sys.argv</code>,
with the script itself in <code>sys.argv[0]</code>. A lone dash
(<code>python -</code>) reads the program from standard input, which
is handy for piping.</p>

<pre class="code">import sys
print(sys.argv)
# python hello.py one two   →   ['hello.py', 'one', 'two']</pre>
""",
            },
            {
                "title": "Options and environment variables",
                "html": """
<p>The interpreter understands a set of command-line options. The most
useful ones to know early:</p>

<pre class="code">python -V             # print the version and exit
python --help         # list every option
python -i script.py   # run the script, then stay in the shell
python -O script.py   # strip assert statements
python -u script.py   # unbuffered output (logs appear at once)
python -E script.py   # ignore all PYTHON* environment variables
python -W error       # turn warnings into errors</pre>

<p>Environment variables configure Python before your code even
starts. The big ones:</p>

<ul>
<li><code>PYTHONPATH</code> &mdash; extra directories where modules are searched for.</li>
<li><code>PYTHONSTARTUP</code> &mdash; a file of commands run before the first interactive prompt.</li>
<li><code>PYTHONUTF8=1</code> &mdash; force UTF-8 for input and output.</li>
<li><code>PYTHONHASHSEED</code> &mdash; fix the random hash seed (useful for reproducible runs).</li>
<li><code>PYTHONDONTWRITEBYTECODE=1</code> &mdash; the same as <code>-B</code>: no .pyc files.</li>
</ul>

[[diag:env_vars]]

<p>When both are set, command-line switches win over environment
variables. And since 3.13 you can control traceback colours directly:
<code>PYTHON_COLORS=0</code> turns them off, <code>NO_COLOR</code>
disables colour for all tools, <code>FORCE_COLOR</code> forces it
on.</p>
""",
            },
        ],
        "quiz": [
            {
                "type": "mc",
                "question": "Which command runs a module as a script?",
                "options": [
                    "python hello.py",
                    "python -c \"print('hi')\"",
                    "python -m timeit",
                    "python -",
                ],
                "answer": 2,
                "explain": "-m imports the module and runs it as the main program — python -m timeit benchmarks code, for example.",
            },
            {
                "type": "blank",
                "question": "The -m option runs a ____ as a script.",
                "answers": ["module"],
                "explain": "-m tells Python to locate a module through the normal import mechanism and execute it as __main__.",
            },
            {
                "type": "codefill",
                "question": "Complete the code that prints the interpreter version:",
                "code": [
                    "import sys",
                    "print(sys.____)",
                    {"blank": "version", "answers": ["version"], "hint": "the attribute holding the version string"},
                ],
                "explain": "sys.version holds the interpreter version, e.g. '3.14.0' — the same value python -V prints.",
            },
            {
                "type": "mc",
                "question": "Which environment variable adds folders to the module search path?",
                "options": ["PYTHONHOME", "PYTHONPATH", "PYTHONSTARTUP", "PYTHONUTF8"],
                "answer": 1,
                "explain": "PYTHONPATH augments the list of directories Python searches when you import a module.",
            },
        ],
    },

    # ------------------------------------------------------------------ 18
    {
        "id": "ch18",
        "title": "Python on Windows",
        "title_fa": "پایتون روی ویندوز",
        "emoji": "🪟",
        "lessons": [
            {
                "title": "Getting Python on Windows",
                "html": """
<p>Windows doesn't ship with Python, so you install it yourself. The
modern way is the <b>Python Install Manager</b> &mdash; download it
from python.org or install it from the Microsoft Store, and you get
three commands:</p>

<pre class="code">python      # launch the default runtime
py          # manage and run several versions
pymanager   # unambiguous version of py</pre>

[[diag:py_launcher]]

<p>Just type <code>python</code> and the current version runs; if
nothing is installed yet, the latest release installs itself
automatically. To control exactly which version runs, use
<code>py</code> with a version tag:</p>

<pre class="code">py -V:3.14              # run exactly 3.14
py list                 # see installed runtimes
py list --online 3.14   # what can be installed
py install 3.14         # add a runtime
py uninstall 3.14       # remove one</pre>

<p><code>pyw</code> and <code>pythonw</code> are windowless versions
for GUI scripts. The install manager updates itself, and uninstalling
it leaves your runtimes in place.</p>
""",
            },
            {
                "title": "Virtual environments and shebangs",
                "html": """
<p>The recommended workflow on Windows (and everywhere else): one
virtual environment per project.</p>

<pre class="code">python -m venv myenv     # create the environment
myenv\\Scripts\\Activate   # turn it on (Windows)
pip install requests     # packages go into myenv only</pre>

[[diag:win_venv]]

<p>Activating an environment redirects <code>python</code>,
<code>pip</code> and any installed commands into it, so different
projects can use different package versions without fighting. Inside
an active environment, <code>py</code> uses that environment by
default &mdash; one less thing to remember.</p>

<p>Windows also honours <b>shebang</b> lines &mdash; the first line of
a script. If it starts with <code>#! /usr/bin/env python3</code>, the
launcher finds the right interpreter for you, which keeps scripts
portable between Windows and Unix:</p>

<pre class="code">#! /usr/bin/env python3
print("Hello from any platform!")</pre>
""",
            },
        ],
        "quiz": [
            {
                "type": "mc",
                "question": "Which command runs exactly Python 3.14 on Windows?",
                "options": ["python 3.14", "py -V:3.14", "pymanager 3.14", "python -3.14"],
                "answer": 1,
                "explain": "py -V:&lt;tag&gt; selects a specific installed runtime; plain python always launches the default.",
            },
            {
                "type": "blank",
                "question": "Create a virtual environment with: python -m ____ myenv",
                "answers": ["venv"],
                "explain": "python -m venv myenv creates an isolated environment in the folder myenv.",
            },
            {
                "type": "mc",
                "question": "On Windows, you activate a virtual environment with:",
                "options": [
                    "source myenv/bin/activate",
                    "myenv\\Scripts\\Activate",
                    "activate myenv",
                    "myenv/activate",
                ],
                "answer": 1,
                "explain": "Windows keeps the activation script in Scripts; Unix uses bin/activate with 'source'.",
            },
            {
                "type": "codefill",
                "question": "Finish the portable shebang — the interpreter searched for on the PATH:",
                "code": [
                    "#! /usr/bin/env ",
                    {"blank": "python3", "answers": ["python3", "python"], "hint": "the interpreter name to search for"},
                    "",
                    "print('Hello!')",
                ],
                "explain": "env searches the PATH for python3 and hands the script to it — portable across Windows and Unix.",
            },
        ],
    },

    # ------------------------------------------------------------------ 19
    {
        "id": "ch19",
        "title": "Other Platforms & Editors",
        "title_fa": "پلتفرم‌های دیگر و ویرایشگرها",
        "emoji": "🖥️",
        "lessons": [
            {
                "title": "macOS and Unix",
                "html": """
<p>On <b>macOS</b>, the official installer from python.org is a
<code>.pkg</code> you double-click. It installs a
<code>Python 3.14</code> folder in Applications (with IDLE and Python
Launcher) and puts <code>python3.14</code> / <code>python3</code> on
your path. macOS already ships a <code>python3</code> in
<code>/usr/bin</code> for Apple's own tools &mdash; never modify or
delete that one; the two can coexist happily.</p>

<p>Many Mac users prefer <b>Homebrew</b>
(<code>brew install python@3.14</code>), or distributions like
Anaconda for data science. On <b>Linux</b>, Python is usually
preinstalled or one command away:</p>

<pre class="code">sudo apt install python3        # Debian / Ubuntu
sudo dnf install python3        # Fedora</pre>

<p>To run a script by name without typing <code>python3</code> every
time, make it executable and give it a shebang line that searches the
PATH:</p>

<pre class="code">chmod +x hello.py
#! /usr/bin/env python3
print("Hello, Unix!")</pre>

[[diag:shebang_unix]]

<p>If you ever build Python from source, the classic sequence is
<code>./configure</code>, <code>make</code>, then
<code>make altinstall</code> &mdash; altinstall avoids clobbering
your system's <code>python3</code>.</p>
""",
            },
            {
                "title": "Editors and IDEs",
                "html": """
<p>Python ships with <b>IDLE</b> &mdash; the Integrated Development
and Learning Environment &mdash; a simple editor with a built-in
shell. It's perfect for your first programs: write, press F5, see the
output.</p>

<p>As you grow, any serious editor works: VS Code, PyCharm, Sublime
Text, Neovim... Good tools give you syntax highlighting, debugging,
and PEP 8 checks, but remember &mdash; the interpreter is the same no
matter what you type into.</p>

<pre class="code"># a 'hello' in any editor
def greet(name):
    return f"Hello, {name}!"

print(greet("world"))</pre>

<p>One last trick from the tutorial's appendix: a startup file. Set
<code>PYTHONSTARTUP</code> to a file of commands and they run
automatically whenever you open the interactive shell &mdash; handy
for custom prompts or favourite imports.</p>
""",
            },
        ],
        "quiz": [
            {
                "type": "mc",
                "question": "Apple's /usr/bin/python3 belongs to Apple's own tooling. What should you do?",
                "options": [
                    "Upgrade it with the newest release",
                    "Leave it completely untouched",
                    "Delete it to save space",
                    "Symlink it to your new Python",
                ],
                "answer": 1,
                "explain": "That python3 is Apple-controlled and used by system software; install your own and let both coexist.",
            },
            {
                "type": "blank",
                "question": "On Unix, make a script executable with: chmod ____ hello.py",
                "answers": ["+x"],
                "explain": "chmod +x adds the execute permission so the script can be launched directly.",
            },
            {
                "type": "mc",
                "question": "Which shebang line searches the PATH for the interpreter?",
                "options": [
                    "#! /usr/bin/python3",
                    "#! /usr/bin/env python3",
                    "#! python3",
                    "#! /usr/local/bin/python3",
                ],
                "answer": 1,
                "explain": "/usr/bin/env looks the interpreter up in the PATH, so the same script works on many machines.",
            },
            {
                "type": "codefill",
                "question": "Add the runtime search path yourself — fill in the list attribute:",
                "code": [
                    "import sys",
                    "sys.____.append('/my/libs')",
                    {"blank": "path", "answers": ["path"], "hint": "the attribute that lists module search directories"},
                ],
                "explain": "sys.path lists every directory Python searches for imports; appending to it works at runtime.",
            },
        ],
    },
]
