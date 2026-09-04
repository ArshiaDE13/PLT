"""SVG diagram generators.

Every lesson image is drawn as pure SVG text, so the app needs no image
files at all. Each function returns a complete <svg> element as a string.
"""

# ---- colour palette -------------------------------------------------------
PY_BLUE = "#3776AB"
PY_YELLOW = "#FFD43B"
LIGHT = "#E8F1F9"
GREEN = "#2E8B57"
RED = "#C0392B"
GRAY = "#5B6B7A"
DARK = "#263238"

FONT = "Consolas, Menlo, monospace"


def _svg(w, h, body):
    return ('<svg viewBox="0 0 %d %d" width="%d" height="%d" '
            'xmlns="http://www.w3.org/2000/svg" role="img" '
            'style="max-width:100%%;height:auto;display:block;margin:0 auto">'
            '%s</svg>') % (w, h, w, h, body)


def _rect(x, y, w, h, fill, rx=8, stroke=None, sw=2, dash=None):
    d = ' stroke-dasharray="%s"' % dash if dash else ""
    s = ' stroke="%s" stroke-width="%d"' % (stroke, sw) if stroke else ""
    return ('<rect x="%d" y="%d" width="%d" height="%d" rx="%d" fill="%s"%s%s/>'
            % (x, y, w, h, rx, fill, s, d))


def _text(x, y, s, size=15, fill=DARK, anchor="start", bold=False, mono=True):
    fw = ' font-weight="bold"' if bold else ""
    fm = "font-family:%s;" % FONT if mono else ""
    return ('<text x="%d" y="%d" font-size="%d" fill="%s" text-anchor="%s" '
            'style="%s"%s>%s</text>'
            % (x, y, size, fill, anchor, fm, fw, s))


def _arrow(x1, y1, x2, y2, color=GRAY, w=2, marker=True):
    m = (' marker-end="url(#arrowhead)"' if marker else "")
    return ('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" '
            'stroke-width="%d"%s/>' % (x1, y1, x2, y2, color, w, m))


def _arrowhead_def():
    return ('<defs><marker id="arrowhead" markerWidth="8" markerHeight="6" '
            'refX="8" refY="3" orient="auto">'
            '<polygon points="0 0, 8 3, 0 6" fill="%s"/></marker></defs>'
            % GRAY)


def _char_cell(x, y, ch, label, color=PY_BLUE, fill=LIGHT):
    """A square cell with a character and an index label below/above."""
    out = [_rect(x, y, 44, 44, fill, rx=6, stroke=color)]
    out.append(_text(x + 22, y + 28, ch, size=20, bold=True, anchor="middle"))
    out.append(_text(x + 22, y + 66, str(label), size=13, fill=GRAY,
                     anchor="middle"))
    return "".join(out)


# ---- 1. REPL shell --------------------------------------------------------
def repl_shell():
    b = [_svg(520, 300, "")]
    inner = []
    inner.append(_rect(20, 14, 480, 60, PY_BLUE, rx=10))
    inner.append(_text(36, 47, "Python 3.14 interactive shell", size=16,
                       fill="white", bold=True))
    inner.append(_text(300, 47, "\u2014  type code, get answers instantly",
                       size=12, fill="#DCE9F5"))
    lines = [
        (">>> 2 + 2", "4"),
        (">>> print('Hello, Python!')", "Hello, Python!"),
        (">>> [n ** 2 for n in range(5)]", "[0, 1, 4, 9, 16]"),
    ]
    yy = 108
    for prompt, answer in lines:
        inner.append(_rect(40, yy, 440, 48, LIGHT, rx=8))
        inner.append(_text(58, yy + 30, prompt, size=15, fill=DARK, bold=True))
        inner.append(_text(430, yy + 30, answer, size=14, fill=GREEN,
                           anchor="end"))
        yy += 60
    inner.append(_text(40, 286, "No editor, no script \u2014 the prompt runs "
                       "your code line by line.", size=13, fill=GRAY))
    return _svg(520, 300, _arrowhead_def() + "".join(inner))


# ---- 2. Running a script --------------------------------------------------
def run_flow():
    b = []
    b.append(_rect(30, 50, 150, 60, "#FFF4D6", rx=10, stroke=PY_YELLOW))
    b.append(_text(105, 84, "hello.py", size=16, bold=True, anchor="middle"))
    b.append(_text(105, 102, "source file", size=12, fill=GRAY,
                   anchor="middle"))
    b.append(_arrow(180, 80, 220, 80))
    b.append(_text(205, 68, "python hello.py", size=13, fill=PY_BLUE,
                   bold=True))
    b.append(_rect(220, 50, 160, 60, PY_BLUE, rx=10))
    b.append(_text(300, 84, "CPython", size=16, fill="white", bold=True,
                   anchor="middle"))
    b.append(_text(300, 102, "interpreter", size=12, fill="#DCE9F5",
                   anchor="middle"))
    b.append(_arrow(380, 80, 420, 80))
    b.append(_rect(420, 50, 150, 60, "#E7F6EC", rx=10, stroke=GREEN))
    b.append(_text(495, 78, "Hello, world!", size=14, fill=GREEN, bold=True,
                   anchor="middle"))
    b.append(_text(495, 96, "printed output", size=12, fill=GRAY,
                   anchor="middle"))
    b.append(_text(30, 180,
                   "The interpreter reads hello.py top to bottom, "
                   "runs each statement,", size=14, fill=DARK))
    b.append(_text(30, 202, "and prints anything the code asks it to.",
                   size=14, fill=DARK))
    return _svg(600, 220, _arrowhead_def() + "".join(b))


# ---- 3. String indices ----------------------------------------------------
def string_index():
    s = "Python"
    inner = []
    inner.append(_text(30, 40,
                       "Each character has a position (index). Indexing "
                       "starts at 0:", size=14, fill=DARK))
    x0, y0 = 40, 110
    for i, ch in enumerate(s):
        inner.append(_char_cell(x0 + i * 56, y0, ch, str(i)))
    inner.append(_text(30, 205,
                       "Negative indices count from the end: s[-1] is the "
                       "last character.", size=14, fill=DARK))
    x1, y1 = 40, 235
    for i, ch in enumerate(s):
        inner.append(_char_cell(x1 + i * 56, y1, ch, str(i - len(s)),
                                color=GREEN, fill="#E7F6EC"))
    inner.append(_text(30, 322, ">>> s = 'Python'", size=14, mono=True))
    inner.append(_text(30, 344, ">>> s[0], s[3], s[-1], s[-6]",
                       size=14, mono=True))
    inner.append(_text(30, 366, "'P'  'h'  'n'  'P'", size=14, fill=GREEN,
                       bold=True, mono=True))
    return _svg(600, 380, _arrowhead_def() + "".join(inner))


# ---- 4. String slicing ----------------------------------------------------
def string_slice():
    s = "Python"
    inner = []
    inner.append(_rect(40, 60, 44, 44, "#FFF4D6", rx=6, stroke=PY_YELLOW))
    inner.append(_text(62, 88, "P", size=20, bold=True, anchor="middle"))
    for i, ch in enumerate(s[1:4]):
        inner.append(_rect(84 + i * 44, 60, 44, 44, "#FFE28A", rx=6,
                           stroke=PY_YELLOW))
        inner.append(_text(106 + i * 44, 88, ch, size=20, bold=True,
                           anchor="middle"))
    for i, ch in enumerate(s[4:]):
        inner.append(_rect(216 + i * 44, 60, 44, 44, "#FFF4D6", rx=6,
                           stroke=PY_YELLOW))
        inner.append(_text(238 + i * 44, 88, ch, size=20, bold=True,
                           anchor="middle"))
    inner.append(_text(62, 124, "0", size=13, fill=GRAY, anchor="middle"))
    inner.append(_text(106, 124, "1", size=13, fill=GRAY, anchor="middle"))
    inner.append(_text(150, 124, "2", size=13, fill=GRAY, anchor="middle"))
    inner.append(_text(194, 124, "3", size=13, fill=GRAY, anchor="middle"))
    inner.append(_text(238, 124, "4", size=13, fill=GRAY, anchor="middle"))
    inner.append(_text(282, 124, "5", size=13, fill=GRAY, anchor="middle"))
    inner.append(_arrow(40, 150, 40, 190))
    inner.append(_text(30, 215, "slice [1:4]", size=13, fill=RED, bold=True))
    inner.append(_arrow(286, 150, 286, 190))
    inner.append(_text(330, 205, "[1:4] means: start at 1, stop before 4",
                       size=14, fill=DARK))
    inner.append(_text(330, 228, ">>> s[1:4]  ->  'yth'", size=15, fill=GREEN,
                       bold=True, mono=True))
    inner.append(_text(30, 268, "Slices never include the stop index. "
                                "s[:3] = 'Pyt', s[3:] = 'hon'.", size=14,
                       fill=DARK))
    return _svg(620, 290, _arrowhead_def() + "".join(inner))


# ---- 5. if/else flowchart -------------------------------------------------
def if_flow():
    b = []
    b.append(_rect(210, 20, 180, 50, PY_BLUE, rx=10))
    b.append(_text(300, 50, "x = 5", size=16, fill="white", bold=True,
                   anchor="middle"))
    b.append(_arrow(300, 70, 300, 105))
    b.append(_rect(190, 105, 220, 70, "#FFF4D6", rx=6, stroke=PY_YELLOW))
    b.append(_text(300, 135, "x > 0 ?", size=16, fill=DARK, bold=True,
                   anchor="middle"))
    b.append(_text(300, 158, "condition", size=12, fill=GRAY,
                   anchor="middle"))
    b.append(_arrow(190, 140, 110, 140))
    b.append(_text(150, 128, "True", size=13, fill=GREEN, bold=True))
    b.append(_rect(20, 115, 90, 50, "#E7F6EC", rx=8, stroke=GREEN))
    b.append(_text(65, 145, "positive", size=13, fill=GREEN, bold=True,
                   anchor="middle"))
    b.append(_arrow(410, 140, 490, 140))
    b.append(_text(450, 128, "False", size=13, fill=RED, bold=True))
    b.append(_rect(490, 115, 90, 50, "#FBE4E2", rx=8, stroke=RED))
    b.append(_text(535, 145, "non-positive", size=13, fill=RED, bold=True,
                   anchor="middle"))
    b.append(_text(30, 220,
                   "if  x > 0:", size=14, mono=True, bold=True))
    b.append(_text(30, 244, "    print('positive')", size=14, mono=True))
    b.append(_text(30, 266, "else:", size=14, mono=True, bold=True))
    b.append(_text(30, 288, "    print('non-positive')", size=14, mono=True))
    return _svg(620, 310, _arrowhead_def() + "".join(b))


# ---- 6. for loop ----------------------------------------------------------
def for_loop():
    b = []
    b.append(_text(30, 35, "for i in range(5):", size=16, fill=DARK,
                   bold=True, mono=True))
    b.append(_text(30, 57, "    print(i)", size=16, fill=DARK, mono=True))
    x = 30
    for n in range(5):
        b.append(_rect(x, 90, 52, 52, LIGHT, rx=8, stroke=PY_BLUE))
        b.append(_text(x + 26, 121, str(n), size=18, bold=True,
                       anchor="middle"))
        if n < 4:
            b.append(_arrow(x + 52, 116, x + 96, 116))
        x += 96
    b.append(_text(30, 180, "range(5) hands the loop body one value at a "
                            "time: 0, 1, 2, 3, 4.", size=14, fill=DARK))
    b.append(_text(30, 204, "The body runs once per value \u2014 five "
                            "prints total.", size=14, fill=DARK))
    b.append(_rect(30, 230, 460, 52, "#E7F6EC", rx=10, stroke=GREEN))
    b.append(_text(260, 262, "0  1  2  3  4", size=18, fill=GREEN,
                   bold=True, anchor="middle"))
    return _svg(560, 300, _arrowhead_def() + "".join(b))


# ---- 7. List aliasing -----------------------------------------------------
def list_aliasing():
    b = []
    b.append(_text(30, 35, "a = [1, 2, 3]", size=15, fill=DARK, bold=True,
                   mono=True))
    b.append(_text(30, 58, "b = a      # copy the reference, not the list",
                   size=14, fill=GRAY, mono=True))
    b.append(_text(30, 81, "c = a[:]   # copy the whole list",
                   size=14, fill=GRAY, mono=True))
    b.append(_rect(60, 120, 170, 46, PY_BLUE, rx=10))
    b.append(_text(145, 147, "a", size=16, fill="white", bold=True,
                   anchor="middle"))
    b.append(_rect(260, 120, 170, 46, PY_BLUE, rx=10))
    b.append(_text(345, 147, "b", size=16, fill="white", bold=True,
                   anchor="middle"))
    b.append(_arrow(145, 166, 145, 200))
    b.append(_arrow(345, 166, 345, 200))
    b.append(_rect(95, 200, 250, 52, LIGHT, rx=8, stroke=PY_BLUE))
    b.append(_text(220, 231, "[1, 2, 3]", size=16, fill=DARK, bold=True,
                   anchor="middle"))
    b.append(_text(220, 180, "both point at the SAME list",
                   size=12, fill=GRAY, anchor="middle"))
    b.append(_rect(430, 120, 170, 46, GREEN, rx=10))
    b.append(_text(515, 147, "c", size=16, fill="white", bold=True,
                   anchor="middle"))
    b.append(_arrow(515, 166, 515, 200))
    b.append(_rect(455, 200, 160, 52, "#E7F6EC", rx=8, stroke=GREEN))
    b.append(_text(535, 231, "[1, 2, 3]", size=16, fill=GREEN, bold=True,
                   anchor="middle"))
    b.append(_text(30, 285,
                   "b.append(4) changes the list for BOTH a and b. "
                   "c is a separate copy.", size=14, fill=DARK))
    return _svg(640, 310, _arrowhead_def() + "".join(b))


# ---- 8. Dict mapping ------------------------------------------------------
def dict_map():
    b = []
    b.append(_rect(30, 50, 170, 42, PY_BLUE, rx=10))
    b.append(_text(115, 76, "key: 'name'", size=15, fill="white", bold=True,
                   anchor="middle"))
    b.append(_rect(30, 110, 170, 42, PY_BLUE, rx=10))
    b.append(_text(115, 136, "key: 'age'", size=15, fill="white", bold=True,
                   anchor="middle"))
    b.append(_rect(30, 170, 170, 42, PY_BLUE, rx=10))
    b.append(_text(115, 196, "key: 'city'", size=15, fill="white", bold=True,
                   anchor="middle"))
    b.append(_arrow(200, 71, 260, 71))
    b.append(_arrow(200, 131, 260, 131))
    b.append(_arrow(200, 191, 260, 191))
    b.append(_rect(260, 50, 170, 42, "#FFF4D6", rx=10, stroke=PY_YELLOW))
    b.append(_text(345, 76, "'Ada'", size=15, fill=DARK, bold=True,
                   anchor="middle"))
    b.append(_rect(260, 110, 170, 42, "#FFF4D6", rx=10, stroke=PY_YELLOW))
    b.append(_text(345, 136, "36", size=15, fill=DARK, bold=True,
                   anchor="middle"))
    b.append(_rect(260, 170, 170, 42, "#FFF4D6", rx=10, stroke=PY_YELLOW))
    b.append(_text(345, 196, "'London'", size=15, fill=DARK, bold=True,
                   anchor="middle"))
    b.append(_text(30, 260, "d = {'name': 'Ada', 'age': 36, 'city': 'London'}",
                   size=14, fill=DARK, mono=True))
    b.append(_text(30, 284, ">>> d['name']  ->  'Ada'", size=15, fill=GREEN,
                   bold=True, mono=True))
    return _svg(460, 310, _arrowhead_def() + "".join(b))


# ---- 9. Exception hierarchy -----------------------------------------------
def exception_tree():
    def node(x, y, label, w=150, fill=LIGHT, color=PY_BLUE, size=13):
        return (_rect(x - w // 2, y, w, 30, fill, rx=6, stroke=color) +
                _text(x, y + 20, label, size=size, fill=DARK, bold=True,
                      anchor="middle"))
    b = []
    b.append(node(300, 25, "BaseException", 200, "#FFF4D6", PY_YELLOW))
    b.append(node(300, 75, "Exception", 160))
    b.append(node(90, 75, "KeyboardInterrupt", 190, "#FBE4E2", RED))
    b.append(node(300, 125, "ArithmeticError", 180))
    b.append(node(300, 175, "ZeroDivisionError", 200, "#E7F6EC", GREEN))
    b.append(node(90, 175, "LookupError", 170))
    b.append(node(30, 225, "IndexError", 140, "#E7F6EC", GREEN))
    b.append(node(170, 225, "KeyError", 130, "#E7F6EC", GREEN))
    b.append(node(500, 125, "ValueError", 150))
    b.append(node(500, 175, "TypeError", 140))
    b.append(_arrow(200, 60, 240, 60))
    b.append(_arrow(270, 55, 215, 75, marker=False))
    b.append(_arrow(330, 55, 385, 75, marker=False))
    b.append(_arrow(270, 105, 270, 155))
    b.append(_arrow(270, 155, 250, 155, marker=False))
    b.append(_arrow(250, 155, 235, 165, marker=False))
    b.append(_arrow(300, 155, 300, 165))
    b.append(_arrow(200, 55, 165, 75, marker=False))
    b.append(_arrow(80, 155, 60, 165))
    b.append(_arrow(110, 155, 100, 165))
    b.append(_arrow(450, 155, 470, 165))
    b.append(_text(30, 270,
                   "except ZeroDivisionError: catches only that branch.",
                   size=14, fill=DARK))
    b.append(_text(30, 294,
                   "except Exception: catches most errors, but not "
                   "KeyboardInterrupt.", size=14, fill=DARK))
    return _svg(620, 320, _arrowhead_def() + "".join(b))


# ---- 10. Scopes (LEGB) ----------------------------------------------------
def scope_le():
    def layer(x, y, w, h, label, sub, fill, stroke, size=15):
        return (_rect(x, y, w, h, fill, rx=8, stroke=stroke) +
                _text(x + w // 2, y + h // 2 - 6, label, size=size,
                      fill=DARK, bold=True, anchor="middle") +
                _text(x + w // 2, y + h // 2 + 14, sub, size=12, fill=GRAY,
                      anchor="middle"))
    b = []
    b.append(layer(150, 20, 300, 44, "Local", "inside the current function",
                   LIGHT, PY_BLUE))
    b.append(_arrow(300, 64, 300, 84))
    b.append(layer(150, 84, 300, 44, "Enclosing", "outer function of a "
                   "nested one", "#EAF4EC", GREEN))
    b.append(_arrow(300, 128, 300, 148))
    b.append(layer(150, 148, 300, 44, "Global", "the module top level",
                   "#FFF4D6", PY_YELLOW))
    b.append(_arrow(300, 192, 300, 212))
    b.append(layer(150, 212, 300, 44, "Built-in", "len, print, range, ...",
                   "#FBE4E2", RED))
    b.append(_text(150, 296,
                   "A name is looked up in this order: Local \u2192 "
                   "Enclosing \u2192 Global \u2192 Built-in.",
                   size=14, fill=DARK))
    return _svg(600, 320, _arrowhead_def() + "".join(b))


# ---- 11. Module / sys.path ------------------------------------------------
def module_syspath():
    b = []
    b.append(_rect(30, 40, 170, 50, PY_BLUE, rx=10))
    b.append(_text(115, 66, "main.py", size=15, fill="white", bold=True,
                   anchor="middle"))
    b.append(_text(115, 82, "import greet", size=13, fill="#DCE9F5",
                   anchor="middle"))
    b.append(_arrow(200, 65, 240, 65))
    b.append(_rect(240, 40, 170, 50, "#E7F6EC", rx=10, stroke=GREEN))
    b.append(_text(325, 66, "greet.py", size=15, fill=GREEN, bold=True,
                   anchor="middle"))
    b.append(_text(325, 82, "def hello(): ...", size=13, fill=GRAY,
                   anchor="middle"))
    b.append(_text(30, 135, "Where does Python look for greet.py? "
                            "It searches sys.path:", size=14, fill=DARK))
    b.append(_rect(30, 155, 520, 42, LIGHT, rx=8, stroke=PY_BLUE))
    b.append(_text(50, 182, "['', 'PYTHONPATH', ...stdlib site-packages]",
                   size=14, fill=DARK, mono=True))
    b.append(_text(30, 230,
                   "The empty string '' means: the directory of the "
                   "running script.", size=14, fill=DARK))
    return _svg(590, 260, _arrowhead_def() + "".join(b))


# ---- 12. f-string equals --------------------------------------------------
def fstring_eq():
    b = []
    b.append(_rect(30, 40, 460, 54, LIGHT, rx=10, stroke=PY_BLUE))
    b.append(_text(50, 70, "name = 'Ada'", size=16, fill=DARK, bold=True,
                   mono=True))
    b.append(_text(50, 90, "print(f\"{name = }\")", size=16, fill=DARK,
                   mono=True))
    b.append(_arrow(260, 94, 260, 120))
    b.append(_rect(120, 120, 280, 50, "#E7F6EC", rx=10, stroke=GREEN))
    b.append(_text(260, 151, "name = 'Ada'", size=16, fill=GREEN, bold=True,
                   anchor="middle", mono=True))
    b.append(_text(30, 210,
                   "The = inside an f-string prints both the expression "
                   "and its value \u2014", size=14, fill=DARK))
    b.append(_text(30, 234,
                   "handy for debugging: f\"{total=}\" shows total=42.",
                   size=14, fill=DARK))
    return _svg(540, 260, _arrowhead_def() + "".join(b))


# ---- 13. Standard library shelf -------------------------------------------
def stdlib_shelf():
    mods = ["os", "sys", "re", "math", "random", "datetime",
            "json", "argparse", "threading", "collections"]
    b = []
    b.append(_rect(30, 20, 540, 40, PY_BLUE, rx=10))
    b.append(_text(300, 46, "Python Standard Library \u2014 bundled modules",
                   size=16, fill="white", bold=True, anchor="middle"))
    x, y = 40, 85
    for m in mods:
        b.append(_rect(x, y, 96, 36, LIGHT, rx=8, stroke=PY_BLUE))
        b.append(_text(x + 48, y + 23, m, size=14, fill=DARK, bold=True,
                       anchor="middle"))
        x += 106
        if x > 470:
            x, y = 40, y + 46
    b.append(_text(40, 240,
                   "import os         \u2192  files & folders",
                   size=14, fill=DARK, mono=True))
    b.append(_text(40, 264,
                   "import json       \u2192  read & write JSON",
                   size=14, fill=DARK, mono=True))
    b.append(_text(40, 288,
                   "import statistics \u2192  mean, median, ...",
                   size=14, fill=DARK, mono=True))
    return _svg(590, 310, _arrowhead_def() + "".join(b))


# ---- 14. Deque ------------------------------------------------------------
def deque():
    b = []
    b.append(_text(30, 35, "from collections import deque", size=14,
                   fill=DARK, mono=True))
    b.append(_text(30, 58, "dq = deque([1, 2, 3])", size=14, fill=DARK,
                   mono=True))
    cells = ["1", "2", "3"]
    x = 140
    for c in cells:
        b.append(_rect(x, 100, 56, 56, LIGHT, rx=8, stroke=PY_BLUE))
        b.append(_text(x + 28, 134, c, size=18, bold=True, anchor="middle"))
        x += 66
    b.append(_arrow(120, 128, 134, 128))
    b.append(_arrow(x + 6, 128, x + 20, 128))
    b.append(_text(96, 118, "appendleft", size=11, fill=GREEN, bold=True,
                   anchor="end"))
    b.append(_text(x + 40, 118, "append / pop", size=11, fill=GREEN,
                   bold=True))
    b.append(_text(30, 200,
                   "deque (\"deck\") grows efficiently at BOTH ends \u2014 "
                   "fast popleft().", size=14, fill=DARK))
    b.append(_text(30, 226,
                   "d = deque('ghi')   d.popleft() -> 'g'", size=14,
                   fill=GRAY, mono=True))
    return _svg(560, 250, _arrowhead_def() + "".join(b))


# ---- 15. venv -------------------------------------------------------------
def venv_boxes():
    b = []
    b.append(_rect(30, 20, 260, 150, LIGHT, rx=12, stroke=PY_BLUE))
    b.append(_text(160, 50, "Project A (venv 'a')", size=15, fill=PY_BLUE,
                   bold=True, anchor="middle"))
    b.append(_rect(50, 65, 220, 34, "#FFF4D6", rx=8, stroke=PY_YELLOW))
    b.append(_text(160, 87, "requests == 2.31", size=14, fill=DARK,
                   bold=True, anchor="middle"))
    b.append(_rect(50, 110, 220, 34, "#FFF4D6", rx=8, stroke=PY_YELLOW))
    b.append(_text(160, 132, "flask == 3.0", size=14, fill=DARK,
                   bold=True, anchor="middle"))
    b.append(_rect(310, 20, 260, 150, LIGHT, rx=12, stroke=PY_BLUE))
    b.append(_text(440, 50, "Project B (venv 'b')", size=15, fill=PY_BLUE,
                   bold=True, anchor="middle"))
    b.append(_rect(330, 65, 220, 34, "#FFF4D6", rx=8, stroke=PY_YELLOW))
    b.append(_text(440, 87, "requests == 2.32", size=14, fill=DARK,
                   bold=True, anchor="middle"))
    b.append(_rect(330, 110, 220, 34, "#FFF4D6", rx=8, stroke=PY_YELLOW))
    b.append(_text(440, 132, "django == 5.0", size=14, fill=DARK,
                   bold=True, anchor="middle"))
    b.append(_text(300, 100, "\\", size=18, fill=GRAY, anchor="middle"))
    b.append(_rect(150, 195, 300, 46, "#E7F6EC", rx=10, stroke=GREEN))
    b.append(_text(300, 223, "one shared Python 3.14",
                   size=15, fill=GREEN, bold=True, anchor="middle"))
    b.append(_text(30, 280,
                   "Each project gets its own environment \u2014 different "
                   "versions never clash.", size=14, fill=DARK))
    return _svg(600, 310, _arrowhead_def() + "".join(b))


# ---- 16. Float 0.1 --------------------------------------------------------
def float_0_1():
    b = []
    b.append(_text(30, 35, "0.1 is NOT stored exactly as 0.1.",
                   size=16, fill=DARK, bold=True))
    b.append(_text(30, 62, "Binary can't represent 0.1 \u2014 the stored "
                           "value is the closest", size=14, fill=DARK))
    b.append(_text(30, 84, "approximation:", size=14, fill=DARK))
    b.append(_rect(30, 105, 540, 48, LIGHT, rx=8, stroke=PY_BLUE))
    b.append(_text(300, 135, "0.100000000000000005551115123125782702118158"
                             "3404541015625",
                   size=14, fill=DARK, bold=True, anchor="middle", mono=True))
    b.append(_arrow(300, 153, 300, 180))
    b.append(_text(300, 200, "repr() shows the SHORTEST string that "
                             "round-trips: \"0.1\"",
                   size=14, fill=GREEN, bold=True, anchor="middle"))
    b.append(_rect(30, 225, 540, 46, "#FFF4D6", rx=8, stroke=PY_YELLOW))
    b.append(_text(300, 253, "0.1 + 0.2  ==  0.30000000000000004",
                   size=16, fill=DARK, bold=True, anchor="middle", mono=True))
    b.append(_text(30, 305,
                   "Compare with math.isclose(a, b), use round(), or "
                   "Decimal for money.", size=14, fill=DARK))
    return _svg(600, 330, _arrowhead_def() + "".join(b))


# ---- 17. Invoking python ------------------------------------------------
def invoke_flow():
    b = []
    b.append(_rect(195, 15, 210, 46, PY_BLUE, rx=10))
    b.append(_text(300, 42, "python <args>", size=16, fill="white",
                   bold=True, anchor="middle"))
    b.append(_arrow(300, 61, 300, 88))
    b.append(_rect(40, 88, 130, 56, LIGHT, rx=8, stroke=PY_BLUE))
    b.append(_text(105, 114, "script.py", size=14, fill=DARK, bold=True,
                   anchor="middle"))
    b.append(_text(105, 132, "run a file", size=12, fill=GRAY,
                   anchor="middle"))
    b.append(_rect(235, 88, 130, 56, LIGHT, rx=8, stroke=PY_BLUE))
    b.append(_text(300, 114, "-c \"code\"", size=14, fill=DARK, bold=True,
                   anchor="middle"))
    b.append(_text(300, 132, "short command", size=12, fill=GRAY,
                   anchor="middle"))
    b.append(_rect(430, 88, 130, 56, LIGHT, rx=8, stroke=PY_BLUE))
    b.append(_text(495, 114, "-m module", size=14, fill=DARK, bold=True,
                   anchor="middle"))
    b.append(_text(495, 132, "run as main", size=12, fill=GRAY,
                   anchor="middle"))
    b.append(_rect(235, 170, 130, 56, "#FFF4D6", rx=8, stroke=PY_YELLOW))
    b.append(_text(300, 196, "(nothing)", size=14, fill=DARK, bold=True,
                   anchor="middle"))
    b.append(_text(300, 214, "interactive shell", size=12, fill=GRAY,
                   anchor="middle"))
    b.append(_arrow(105, 144, 105, 176))
    b.append(_arrow(300, 144, 300, 168))
    b.append(_arrow(495, 144, 495, 176))
    b.append(_arrow(300, 61, 300, 74))
    b.append(_text(30, 268,
                   "Arguments after the script name land in sys.argv; "
                   "a lone dash reads from stdin.", size=14, fill=DARK))
    return _svg(600, 290, _arrowhead_def() + "".join(b))


# ---- 18. Environment variables --------------------------------------------
def env_vars():
    b = []
    b.append(_text(30, 32, "Set before Python starts, read by the "
                           "interpreter at launch:", size=14, fill=DARK))
    rows = [
        ("PYTHONPATH", "extra module search directories"),
        ("PYTHONSTARTUP", "commands run before the first prompt"),
        ("PYTHONUTF8=1", "force UTF-8 input/output"),
        ("PYTHONHASHSEED", "fix the random hash seed"),
        ("PYTHONDONTWRITEBYTECODE", "no .pyc cache files"),
    ]
    y = 60
    for var, desc in rows:
        b.append(_rect(30, y, 220, 34, PY_BLUE, rx=8))
        b.append(_text(140, y + 22, var, size=13, fill="white", bold=True,
                       anchor="middle"))
        b.append(_text(270, y + 22, desc, size=13, fill=DARK))
        y += 42
    b.append(_text(30, 278, "Command-line switches always win over "
                            "environment variables.", size=14, fill=GRAY,
                   bold=True))
    return _svg(560, 300, _arrowhead_def() + "".join(b))


# ---- 19. py launcher -------------------------------------------------------
def py_launcher():
    b = []
    b.append(_text(30, 30, "Windows Install Manager gives you three "
                           "commands:", size=14, fill=DARK))
    cmds = [("python", "default runtime"),
            ("py", "manage versions"),
            ("pymanager", "unambiguous py")]
    x = 30
    for name, desc in cmds:
        b.append(_rect(x, 50, 170, 70, LIGHT, rx=10, stroke=PY_BLUE))
        b.append(_text(x + 85, 80, name, size=15, fill=PY_BLUE, bold=True,
                       anchor="middle"))
        b.append(_text(x + 85, 100, desc, size=12, fill=GRAY,
                       anchor="middle"))
        x += 180
    b.append(_text(30, 165, "Pick an exact runtime with py:", size=14,
                   fill=DARK))
    b.append(_rect(30, 180, 520, 42, "#FFF4D6", rx=8, stroke=PY_YELLOW))
    b.append(_text(290, 207, "py -V:3.14      py list      py install 3.14",
                   size=14, fill=DARK, bold=True, anchor="middle", mono=True))
    b.append(_text(30, 265, "pyw / pythonw are windowless versions for "
                            "GUI scripts.", size=14, fill=GRAY))
    return _svg(570, 285, _arrowhead_def() + "".join(b))


# ---- 20. Windows venv ------------------------------------------------------
def win_venv():
    b = []
    b.append(_text(30, 30, "One environment per project:", size=14,
                   fill=DARK))
    b.append(_rect(30, 48, 260, 44, PY_BLUE, rx=10))
    b.append(_text(160, 74, "python -m venv myenv", size=15, fill="white",
                   bold=True, anchor="middle"))
    b.append(_arrow(290, 70, 330, 70))
    b.append(_rect(330, 48, 220, 44, "#E7F6EC", rx=10, stroke=GREEN))
    b.append(_text(440, 74, "myenv\\Scripts\\Activate", size=13,
                   fill=GREEN, bold=True, anchor="middle"))
    b.append(_text(160, 122, "1. create", size=12, fill=GRAY,
                   anchor="middle"))
    b.append(_text(440, 122, "2. turn it on", size=12, fill=GRAY,
                   anchor="middle"))
    b.append(_arrow(300, 130, 300, 160))
    b.append(_rect(60, 160, 480, 46, "#FFF4D6", rx=10, stroke=PY_YELLOW))
    b.append(_text(300, 188, "pip install requests  \u2192  goes into myenv only",
                   size=15, fill=DARK, bold=True, anchor="middle"))
    b.append(_text(30, 250,
                   "While active, python / pip / py all point inside "
                   "myenv \u2014 projects stay isolated.", size=14,
                   fill=DARK))
    return _svg(580, 275, _arrowhead_def() + "".join(b))


# ---- 21. Unix shebang ------------------------------------------------------
def shebang_unix():
    b = []
    b.append(_rect(30, 40, 170, 50, "#FFF4D6", rx=10, stroke=PY_YELLOW))
    b.append(_text(115, 66, "hello.py", size=15, fill=DARK, bold=True,
                   anchor="middle"))
    b.append(_text(115, 82, "#! /usr/bin/env python3", size=11, fill=GRAY,
                   anchor="middle"))
    b.append(_arrow(200, 65, 240, 65))
    b.append(_rect(240, 40, 150, 50, LIGHT, rx=10, stroke=PY_BLUE))
    b.append(_text(315, 66, "env", size=15, fill=PY_BLUE, bold=True,
                   anchor="middle"))
    b.append(_text(315, 82, "finds python3 in PATH", size=11, fill=GRAY,
                   anchor="middle"))
    b.append(_arrow(390, 65, 430, 65))
    b.append(_rect(430, 40, 150, 50, PY_BLUE, rx=10))
    b.append(_text(505, 66, "python3", size=15, fill="white", bold=True,
                   anchor="middle"))
    b.append(_text(505, 82, "runs the script", size=11, fill="#DCE9F5",
                   anchor="middle"))
    b.append(_text(30, 145,
                   "chmod +x hello.py   \u2192   ./hello.py works from "
                   "any shell,", size=14, fill=DARK, mono=True))
    b.append(_text(30, 168,
                   "on Windows and Unix alike, because env does the "
                   "searching.", size=14, fill=DARK))
    return _svg(610, 195, _arrowhead_def() + "".join(b))


# ---- 22. Path anatomy -----------------------------------------------------
def path_parts():
    b = []
    b.append(_rect(30, 25, 540, 60, LIGHT, rx=10, stroke=PY_BLUE))
    b.append(_text(300, 62, "Path('/home/ada/projects/notes.txt')", size=16,
                   fill=DARK, bold=True, anchor="middle"))
    segs = [("/home/ada/projects", "parent", PY_BLUE),
            ("notes.txt", "name", GREEN),
            ("notes", "stem", PY_YELLOW),
            (".txt", "suffix", RED)]
    x = 40
    for label, tag, color in segs:
        w = 110 if tag != "name" else 130
        b.append(_rect(x, 110, w, 44, "#F4F8FC", rx=8, stroke=color))
        b.append(_text(x + w // 2, 137, label, size=13, fill=DARK, bold=True,
                       anchor="middle", mono=False))
        b.append(_text(x + w // 2, 178, tag, size=12, fill=color, bold=True,
                       anchor="middle"))
        x += w + 18
    b.append(_text(30, 225,
                   "name = last part, stem = name minus suffix, ",
                   size=14, fill=DARK))
    b.append(_text(30, 249,
                   "parent = the folder it lives in — all properties, ",
                   size=14, fill=DARK))
    b.append(_text(30, 273, "no string parsing needed.", size=14, fill=DARK))
    return _svg(600, 295, _arrowhead_def() + "".join(b))


# ---- 23. Counter flow ------------------------------------------------------
def counter_flow():
    b = []
    b.append(_text(30, 30, "words = ['red', 'blue', 'red', 'green', "
                           "'blue', 'blue']", size=14, fill=DARK, mono=True))
    b.append(_rect(30, 55, 150, 60, LIGHT, rx=10, stroke=PY_BLUE))
    b.append(_text(105, 81, "Counter(words)", size=13, fill=PY_BLUE,
                   bold=True, anchor="middle"))
    b.append(_text(105, 101, "count every word", size=11, fill=GRAY,
                   anchor="middle"))
    b.append(_arrow(180, 85, 220, 85))
    rows = [("blue", 3), ("red", 2), ("green", 1)]
    y = 55
    for word, n in rows:
        b.append(_rect(220, y, 110, 32, "#FFF4D6", rx=6, stroke=PY_YELLOW))
        b.append(_text(275, y + 21, word, size=13, fill=DARK, bold=True,
                       anchor="middle"))
        b.append(_rect(345, y + 6, n * 45, 20, GREEN, rx=4))
        b.append(_text(345 + n * 45 + 14, y + 21, str(n), size=13,
                       fill=GREEN, bold=True))
        y += 40
    b.append(_text(30, 220, "c['blue']  -&gt;  3", size=15, fill=GREEN, bold=True,
                   mono=True))
    b.append(_text(30, 246, "c.most_common(2)  -&gt;  [('blue', 3), ('red', 2)]",
                   size=14, fill=DARK, mono=True))
    b.append(_text(30, 272, "c.total()  -&gt;  6", size=14, fill=DARK, mono=True))
    return _svg(560, 295, _arrowhead_def() + "".join(b))


# ---- 24. itertools flow ----------------------------------------------------
def itertools_flow():
    b = []
    b.append(_text(30, 28, "chain('ABC', 'DEF')", size=14, fill=DARK,
                   bold=True, mono=True))
    b.append(_arrow(30, 40, 30, 58))
    cells = ["A", "B", "C", "D", "E", "F"]
    x = 40
    for c in cells:
        b.append(_rect(x, 58, 56, 40, LIGHT, rx=6, stroke=PY_BLUE))
        b.append(_text(x + 28, 83, c, size=15, bold=True, anchor="middle"))
        x += 64
    b.append(_text(30, 135, "batched('ABCDEFG', 3)", size=14, fill=DARK,
                   bold=True, mono=True))
    b.append(_arrow(30, 147, 30, 165))
    x = 40
    for i, chunk in enumerate(["ABC", "DEF", "G"]):
        w = 110 if i < 2 else 60
        b.append(_rect(x, 165, w, 40, "#E7F6EC", rx=6, stroke=GREEN))
        b.append(_text(x + w // 2, 190, chunk, size=15, fill=GREEN,
                       bold=True, anchor="middle"))
        if i < 2:
            b.append(_text(x + w + 8, 189, "+", size=14, fill=GRAY,
                           anchor="middle"))
        x += w + 22
    b.append(_text(30, 250,
                   "Iterators are lazy: they produce values one at a time, ",
                   size=14, fill=DARK))
    b.append(_text(30, 274, "so huge or infinite streams use almost no memory.",
                   size=14, fill=DARK))
    return _svg(580, 295, _arrowhead_def() + "".join(b))


# ---- 25. JSON round-trip ---------------------------------------------------
def json_roundtrip():
    b = []
    b.append(_rect(30, 55, 170, 70, PY_BLUE, rx=10))
    b.append(_text(115, 82, "Python dict", size=15, fill="white", bold=True,
                   anchor="middle"))
    b.append(_text(115, 104, "{'name': 'Ada'}", size=12, fill="#DCE9F5",
                   anchor="middle"))
    b.append(_text(40, 105, "dumps()", size=12, fill=GREEN, bold=True))
    b.append(_arrow(200, 90, 250, 90, GREEN))
    b.append(_rect(250, 55, 170, 70, "#E7F6EC", rx=10, stroke=GREEN))
    b.append(_text(335, 82, "JSON text", size=15, fill=GREEN, bold=True,
                   anchor="middle"))
    b.append(_text(335, 104, '{"name": "Ada"}', size=12, fill=DARK,
                   anchor="middle"))
    b.append(_text(430, 105, "loads()", size=12, fill=PY_BLUE, bold=True))
    b.append(_arrow(420, 90, 470, 90, PY_BLUE))
    b.append(_rect(470, 55, 150, 70, "#FFF4D6", rx=10, stroke=PY_YELLOW))
    b.append(_text(545, 82, "Python dict", size=15, fill=DARK, bold=True,
                   anchor="middle"))
    b.append(_text(545, 104, "{'name': 'Ada'}", size=12, fill=GRAY,
                   anchor="middle"))
    b.append(_text(30, 175, "dumps  = Dump to String   (dict -&gt; JSON text)",
                   size=14, fill=DARK, mono=True))
    b.append(_text(30, 199, "loads  = LOad from String (JSON text -&gt; dict)",
                   size=14, fill=DARK, mono=True))
    b.append(_text(30, 240, "JSON is the web's universal data format — ",
                   size=14, fill=DARK))
    b.append(_text(30, 264, "the same shape as a Python dict, so the ", size=14,
                   fill=DARK))
    b.append(_text(30, 288, "conversion is nearly lossless.", size=14,
                   fill=DARK))
    return _svg(650, 310, _arrowhead_def() + "".join(b))


# ---- 26. argparse flow -----------------------------------------------------
def cli_flow():
    b = []
    b.append(_rect(30, 40, 210, 52, LIGHT, rx=10, stroke=PY_BLUE))
    b.append(_text(135, 67, "python greet.py --name Ada", size=14,
                   fill=DARK, bold=True, anchor="middle", mono=True))
    b.append(_text(135, 84, "the command line", size=11, fill=GRAY,
                   anchor="middle"))
    b.append(_arrow(240, 66, 280, 66))
    b.append(_rect(280, 40, 150, 52, PY_BLUE, rx=10))
    b.append(_text(355, 67, "ArgumentParser", size=14, fill="white",
                   bold=True, anchor="middle"))
    b.append(_text(355, 84, "reads sys.argv", size=11, fill="#DCE9F5",
                   anchor="middle"))
    b.append(_arrow(430, 66, 470, 66))
    b.append(_rect(470, 40, 150, 52, "#E7F6EC", rx=10, stroke=GREEN))
    b.append(_text(545, 67, "args.name = 'Ada'", size=14, fill=GREEN,
                   bold=True, anchor="middle"))
    b.append(_text(545, 84, "the namespace", size=11, fill=GRAY,
                   anchor="middle"))
    b.append(_text(30, 145, "parser.add_argument('--name', default='world')",
                   size=13, fill=DARK, mono=True))
    b.append(_text(30, 170, "parser.add_argument('--shout', action='store_true')",
                   size=13, fill=DARK, mono=True))
    b.append(_text(30, 215,
                   "Flags become attributes on the parsed namespace: ",
                   size=14, fill=DARK))
    b.append(_text(30, 239, "--name Ada  -&gt;  args.name  ==  'Ada'",
                   size=14, fill=GREEN, bold=True, mono=True))
    return _svg(650, 265, _arrowhead_def() + "".join(b))


# ---- 27. sqlite tables -----------------------------------------------------
def sqlite_tables():
    b = []
    b.append(_rect(30, 30, 250, 40, PY_BLUE, rx=10))
    b.append(_text(155, 55, "app.db", size=16, fill="white", bold=True,
                   anchor="middle"))
    b.append(_text(155, 75, "one file, full SQL engine", size=11,
                   fill="#DCE9F5", anchor="middle"))
    b.append(_arrow(280, 50, 320, 50))
    b.append(_rect(320, 20, 260, 30, "#FFF4D6", rx=6, stroke=PY_YELLOW))
    b.append(_text(450, 40, "users", size=14, fill=DARK, bold=True,
                   anchor="middle"))
    headers = ["name", "age"]
    x = 320
    for h in headers:
        b.append(_rect(x, 50, 130, 26, PY_BLUE, rx=4))
        b.append(_text(x + 65, 67, h, size=12, fill="white", bold=True,
                       anchor="middle"))
        x += 130
    rows = [["'Ada'", "36"], ["'Guido'", "68"]]
    y = 76
    for r in rows:
        x = 320
        for v in r:
            b.append(_rect(x, y, 130, 26, LIGHT, rx=4, stroke="#C9D8E6"))
            b.append(_text(x + 65, y + 18, v, size=12, fill=DARK,
                           anchor="middle"))
            x += 130
        y += 26
    b.append(_text(30, 160,
                   "conn.execute('INSERT INTO users VALUES (?, ?)', ...)",
                   size=13, fill=DARK, mono=True))
    b.append(_text(30, 186,
                   "conn.commit()     # make writes permanent", size=13,
                   fill=DARK, mono=True))
    b.append(_text(30, 230,
                   "? placeholders keep values out of the SQL string ",
                   size=14, fill=DARK))
    b.append(_text(30, 254, "— safe from injection and quoting bugs.",
                   size=14, fill=DARK))
    return _svg(600, 280, _arrowhead_def() + "".join(b))


# ---- 28. Sorting key pipeline ---------------------------------------------
def sorting_flow():
    b = []
    b.append(_rect(30, 40, 150, 56, LIGHT, rx=10, stroke=PY_BLUE))
    b.append(_text(105, 64, "students", size=14, fill=DARK, bold=True,
                   anchor="middle"))
    b.append(_text(105, 84, "list of tuples", size=11, fill=GRAY,
                   anchor="middle"))
    b.append(_arrow(180, 68, 220, 68))
    b.append(_rect(220, 40, 150, 56, "#FFF4D6", rx=10, stroke=PY_YELLOW))
    b.append(_text(295, 64, "key=itemgetter(2)", size=13, fill=DARK,
                   bold=True, anchor="middle"))
    b.append(_text(295, 84, "pick the age", size=11, fill=GRAY,
                   anchor="middle"))
    b.append(_arrow(370, 68, 410, 68))
    b.append(_rect(410, 40, 150, 56, "#E7F6EC", rx=10, stroke=GREEN))
    b.append(_text(485, 64, "sorted list", size=14, fill=GREEN, bold=True,
                   anchor="middle"))
    b.append(_text(485, 84, "by age ascending", size=11, fill=GRAY,
                   anchor="middle"))
    b.append(_text(30, 150, "The key function runs ONCE per item, ",
                   size=14, fill=DARK))
    b.append(_text(30, 174, "producing the values actually compared.",
                   size=14, fill=DARK))
    b.append(_text(30, 215, "key=lambda s: s[2]", size=14, fill=DARK,
                   bold=True, mono=True))
    b.append(_text(30, 239, "reverse=True   # biggest first", size=14,
                   fill=DARK, mono=True))
    b.append(_text(30, 263, "Stable: equal keys keep their original order.",
                   size=14, fill=GREEN, bold=True))
    return _svg(590, 285, _arrowhead_def() + "".join(b))


# ---- 29. Regex flow --------------------------------------------------------
def regex_flow():
    b = []
    b.append(_rect(30, 45, 150, 56, "#FFF4D6", rx=10, stroke=PY_YELLOW))
    b.append(_text(105, 69, r"r'\d+'" , size=16, fill=DARK, bold=True,
                   anchor="middle", mono=True))
    b.append(_text(105, 89, "the pattern", size=11, fill=GRAY,
                   anchor="middle"))
    b.append(_rect(220, 45, 150, 56, LIGHT, rx=10, stroke=PY_BLUE))
    b.append(_text(295, 69, "\"Order 42 and 7\"", size=13, fill=DARK,
                   bold=True, anchor="middle"))
    b.append(_text(295, 89, "the text to search", size=11, fill=GRAY,
                   anchor="middle"))
    b.append(_arrow(180, 73, 218, 73))
    b.append(_arrow(370, 73, 408, 73))
    b.append(_rect(410, 45, 150, 56, "#E7F6EC", rx=10, stroke=GREEN))
    b.append(_text(485, 69, "['42', '7']", size=15, fill=GREEN, bold=True,
                   anchor="middle"))
    b.append(_text(485, 89, "the matches", size=11, fill=GRAY,
                   anchor="middle"))
    b.append(_text(30, 150, "re.search   first match (a match object)",
                   size=13, fill=DARK, mono=True))
    b.append(_text(30, 174, "re.findall  every match (a list)",
                   size=13, fill=DARK, mono=True))
    b.append(_text(30, 198, "re.sub      replace matches", size=13,
                   fill=DARK, mono=True))
    b.append(_text(30, 222, "re.split    split on matches", size=13,
                   fill=DARK, mono=True))
    b.append(_text(30, 262, "Use raw strings r'...' so \\ stays \\ .",
                   size=14, fill=DARK))
    return _svg(590, 285, _arrowhead_def() + "".join(b))


# ---- 30. argparse deeper ---------------------------------------------------
def argparse_deep():
    b = []
    b.append(_text(30, 30, "python tool.py report.txt -n 5 --color red",
                   size=14, fill=DARK, bold=True, mono=True))
    b.append(_rect(30, 55, 560, 42, LIGHT, rx=8, stroke=PY_BLUE))
    b.append(_text(50, 81, "positional:  args.path == 'report.txt'",
                   size=13, fill=DARK, mono=True))
    b.append(_rect(30, 105, 560, 42, "#FFF4D6", rx=8, stroke=PY_YELLOW))
    b.append(_text(50, 131, "type=int:    args.number == 5  (an int, not '5')",
                   size=13, fill=DARK, mono=True))
    b.append(_rect(30, 155, 560, 42, "#E7F6EC", rx=8, stroke=GREEN))
    b.append(_text(50, 181, "choices:     args.color in ['red','green','blue']",
                   size=13, fill=DARK, mono=True))
    b.append(_rect(30, 205, 560, 42, LIGHT, rx=8, stroke=PY_BLUE))
    b.append(_text(50, 231, "store_true:  --verbose  -&gt;  args.verbose is True",
                   size=13, fill=DARK, mono=True))
    b.append(_text(30, 272,
                   "Bad input is rejected with a clear error, and ",
                   size=14, fill=DARK))
    b.append(_text(30, 296, "--help is generated for free.", size=14,
                   fill=DARK))
    return _svg(620, 315, _arrowhead_def() + "".join(b))


# ---- 31. Unicode str/bytes -------------------------------------------------
def unicode_bytes():
    b = []
    b.append(_rect(30, 45, 170, 60, PY_BLUE, rx=10))
    b.append(_text(115, 73, "'h\u00e9llo'", size=16, fill="white",
                   bold=True, anchor="middle"))
    b.append(_text(115, 93, "str: code points", size=12, fill="#DCE9F5",
                   anchor="middle"))
    b.append(_text(70, 95, "encode('utf-8')", size=11, fill=GREEN,
                   bold=True))
    b.append(_arrow(200, 75, 250, 75, GREEN))
    b.append(_rect(250, 45, 190, 60, "#E7F6EC", rx=10, stroke=GREEN))
    b.append(_text(345, 73, "b'h\\xc3\\xa9llo'", size=15, fill=GREEN,
                   bold=True, anchor="middle"))
    b.append(_text(345, 93, "bytes: raw octets", size=12, fill=GRAY,
                   anchor="middle"))
    b.append(_text(455, 95, "decode('utf-8')", size=11, fill=PY_BLUE,
                   bold=True))
    b.append(_arrow(440, 75, 490, 75, PY_BLUE))
    b.append(_rect(490, 45, 150, 60, "#FFF4D6", rx=10, stroke=PY_YELLOW))
    b.append(_text(565, 73, "'h\u00e9llo'", size=16, fill=DARK, bold=True,
                   anchor="middle"))
    b.append(_text(565, 93, "str again", size=12, fill=GRAY,
                   anchor="middle"))
    b.append(_text(30, 155,
                   "UTF-8: 1-4 bytes per character, ASCII stays ",
                   size=14, fill=DARK))
    b.append(_text(30, 179, "identical, every code point supported.",
                   size=14, fill=DARK))
    b.append(_text(30, 225, "Wrong encoding  -&gt;  UnicodeDecodeError /",
                   size=14, fill=RED, bold=True))
    b.append(_text(30, 249, "UnicodeEncodeError. Decode on input, ",
                   size=14, fill=DARK))
    b.append(_text(30, 273, "encode on output, work in str in between.",
                   size=14, fill=DARK))
    return _svg(670, 295, _arrowhead_def() + "".join(b))


# ---- 32. Async event loop --------------------------------------------------
def async_loop():
    b = []
    b.append(_rect(210, 20, 180, 40, PY_BLUE, rx=10))
    b.append(_text(300, 46, "asyncio.run(main())", size=14, fill="white",
                   bold=True, anchor="middle"))
    b.append(_arrow(300, 60, 300, 85))
    b.append(_rect(120, 85, 360, 150, "#F4F8FC", rx=14, stroke=GREEN))
    b.append(_text(300, 110, "event loop", size=15, fill=GREEN, bold=True,
                   anchor="middle"))
    tasks = ["fetch('a.com')", "fetch('b.com')"]
    x = 150
    for t in tasks:
        b.append(_rect(x, 130, 140, 44, "#E7F6EC", rx=8, stroke=GREEN))
        b.append(_text(x + 70, 156, t, size=13, fill=GREEN, bold=True,
                       anchor="middle", mono=True))
        b.append(_arrow(x + 70, 174, x + 70, 195))
        b.append(_text(x + 70, 212, "await ...", size=11, fill=GRAY,
                       anchor="middle"))
        x += 170
    b.append(_text(30, 205, "await", size=12, fill=GRAY, bold=True))
    b.append(_arrow(150, 240, 150, 260))
    b.append(_arrow(320, 240, 320, 260))
    b.append(_text(30, 280,
                   "While one task waits, the loop runs another \u2014 ",
                   size=14, fill=DARK))
    b.append(_text(30, 304, "two slow fetches finish in ~1x the time.",
                   size=14, fill=DARK))
    return _svg(600, 325, _arrowhead_def() + "".join(b))


# ---- 33. Object model -----------------------------------------------------
def object_model():
    b = []
    b.append(_text(30, 28, "a = [1, 2, 3]   b = [1, 2, 3]   c = a",
                   size=14, fill=DARK, bold=True, mono=True))
    b.append(_rect(30, 55, 120, 50, PY_BLUE, rx=10))
    b.append(_text(90, 82, "a", size=16, fill="white", bold=True,
                   anchor="middle"))
    b.append(_rect(190, 55, 120, 50, PY_BLUE, rx=10))
    b.append(_text(250, 82, "b", size=16, fill="white", bold=True,
                   anchor="middle"))
    b.append(_rect(350, 55, 120, 50, PY_BLUE, rx=10))
    b.append(_text(410, 82, "c", size=16, fill="white", bold=True,
                   anchor="middle"))
    b.append(_arrow(90, 105, 90, 140))
    b.append(_arrow(250, 105, 250, 140))
    b.append(_arrow(410, 105, 410, 140))
    b.append(_rect(40, 140, 130, 52, "#E7F6EC", rx=8, stroke=GREEN))
    b.append(_text(105, 170, "[1, 2, 3]", size=15, fill=GREEN, bold=True,
                   anchor="middle"))
    b.append(_rect(190, 140, 130, 52, "#FFF4D6", rx=8, stroke=PY_YELLOW))
    b.append(_text(255, 170, "[1, 2, 3]", size=15, fill=DARK, bold=True,
                   anchor="middle"))
    b.append(_text(30, 225, "a == b   True     (same VALUES)",
                   size=14, fill=GREEN, bold=True, mono=True))
    b.append(_text(30, 249, "a is b   False    (two different objects)",
                   size=14, fill=RED, bold=True, mono=True))
    b.append(_text(30, 273, "a is c   True     (c points at a's object)",
                   size=14, fill=DARK, bold=True, mono=True))
    return _svg(600, 295, _arrowhead_def() + "".join(b))


# ---- 34. Dunder power ------------------------------------------------------
def dunder_power():
    b = []
    b.append(_text(30, 28, "Define these on a class, and the syntax just works:",
                   size=14, fill=DARK))
    rows = [
        ("Point(3, 4)", "__init__(self, x, y)"),
        ("print(obj)", "__repr__ / __str__"),
        ("len(obj)", "__len__"),
        ("obj[0]", "__getitem__ / __setitem__"),
        ("for x in obj", "__iter__ / __next__"),
        ("obj()", "__call__"),
        ("a == b", "__eq__"),
    ]
    y = 58
    for syntax, dunder in rows:
        b.append(_rect(30, y, 230, 26, LIGHT, rx=6, stroke=PY_BLUE))
        b.append(_text(145, y + 18, syntax, size=13, fill=DARK, bold=True,
                       anchor="middle", mono=True))
        b.append(_text(290, y + 18, dunder, size=13, fill=PY_BLUE,
                       bold=True, mono=True))
        y += 31
    b.append(_text(30, 283,
                   "The interpreter calls the dunder for you ",
                   size=14, fill=DARK))
    return _svg(560, 305, _arrowhead_def() + "".join(b))


# ---- 35. global / nonlocal -------------------------------------------------
def global_nonlocal():
    b = []
    b.append(_rect(30, 20, 280, 80, "#FFF4D6", rx=10, stroke=PY_YELLOW))
    b.append(_text(170, 44, "module namespace", size=14, fill=DARK,
                   bold=True, anchor="middle"))
    b.append(_text(170, 70, "x = 10", size=15, fill=DARK, bold=True,
                   anchor="middle", mono=True))
    b.append(_rect(360, 20, 240, 80, LIGHT, rx=10, stroke=PY_BLUE))
    b.append(_text(480, 44, "function fine()", size=14, fill=PY_BLUE,
                   bold=True, anchor="middle"))
    b.append(_text(480, 70, "global x  -&gt;  writes module x",
                   size=12, fill=DARK, anchor="middle", mono=True))
    b.append(_arrow(310, 60, 356, 60, PY_YELLOW))
    b.append(_text(333, 48, "reads & writes", size=11, fill=GRAY,
                   anchor="middle"))
    b.append(_rect(360, 130, 240, 90, "#E7F6EC", rx=10, stroke=GREEN))
    b.append(_text(480, 154, "function counter()", size=14, fill=GREEN,
                   bold=True, anchor="middle"))
    b.append(_text(480, 178, "n = 0", size=14, fill=DARK, bold=True,
                   anchor="middle", mono=True))
    b.append(_rect(390, 195, 180, 40, "#F4F8FC", rx=8, stroke=GREEN))
    b.append(_text(480, 220, "nonlocal n  -&gt;  bump() writes here",
                   size=11, fill=DARK, anchor="middle", mono=True))
    b.append(_arrow(480, 170, 480, 193))
    b.append(_text(30, 155,
                   "global   -&gt;  the module-level namespace",
                   size=14, fill=DARK, mono=True))
    b.append(_text(30, 179, "nonlocal -&gt;  the nearest enclosing function",
                   size=14, fill=DARK, mono=True))
    b.append(_text(30, 230,
                   "Without global/nonlocal, assignment inside a ",
                   size=14, fill=RED, bold=True))
    b.append(_text(30, 254, "function makes the name local \u2014 the ",
                   size=14, fill=RED, bold=True))
    b.append(_text(30, 278, "UnboundLocalError trap.", size=14, fill=RED,
                   bold=True))
    return _svg(640, 300, _arrowhead_def() + "".join(b))


# ---- 36. Operator precedence -----------------------------------------------
def operator_precedence():
    b = []
    rows = [
        ("( )  [ ]  { }  atoms, calls, indexing", PY_BLUE),
        ("**  power (right-associative)", PY_BLUE),
        ("+x  -x  ~x  unary operators", "#5B7B99"),
        ("*  /  //  %  @  multiply, divide, modulo", "#5B7B99"),
        ("+  -  add, subtract", "#5B7B99"),
        ("&lt;&lt;  &gt;&gt;  shifts   &amp;   ^   |  bitwise", "#5B7B99"),
        ("in  not in  is  &lt;  &lt;=  &gt;  &gt;=  ==  !=  comparisons", "#5B7B99"),
        ("not x   and   or   boolean logic", "#5B7B99"),
        ("if - else  conditional", "#5B7B99"),
        (":=  walrus    lambda  loosest", RED),
    ]
    y = 25
    for label, color in rows:
        b.append(_rect(30, y, 540, 26, "#F4F8FC", rx=6, stroke=color))
        b.append(_text(300, y + 18, label, size=12, fill=DARK, bold=True,
                       anchor="middle", mono=True))
        y += 29
    b.append(_text(30, 322, "Tight at the top, loose at the bottom.",
                   size=14, fill=DARK, bold=True))
    return _svg(600, 345, _arrowhead_def() + "".join(b))


# ---- 37. Import search -----------------------------------------------------
def import_search():
    b = []
    b.append(_rect(30, 40, 140, 50, PY_BLUE, rx=10))
    b.append(_text(100, 67, "import os", size=15, fill="white", bold=True,
                   anchor="middle"))
    b.append(_arrow(170, 65, 210, 65))
    b.append(_rect(210, 40, 150, 50, "#FFF4D6", rx=10, stroke=PY_YELLOW))
    b.append(_text(285, 62, "sys.modules?", size=13, fill=DARK, bold=True,
                   anchor="middle"))
    b.append(_text(285, 80, "already loaded?", size=11, fill=GRAY,
                   anchor="middle"))
    b.append(_arrow(360, 65, 400, 65))
    b.append(_rect(400, 40, 170, 50, LIGHT, rx=10, stroke=PY_BLUE))
    b.append(_text(485, 62, "search sys.path", size=13, fill=PY_BLUE,
                   bold=True, anchor="middle"))
    b.append(_text(485, 80, "cwd, PYTHONPATH, stdlib, site",
                   size=10, fill=GRAY, anchor="middle"))
    b.append(_arrow(485, 90, 485, 120))
    b.append(_rect(360, 120, 210, 50, "#E7F6EC", rx=10, stroke=GREEN))
    b.append(_text(465, 142, "run module code once", size=13, fill=GREEN,
                   bold=True, anchor="middle"))
    b.append(_text(465, 160, "store in sys.modules", size=11, fill=GRAY,
                   anchor="middle"))
    b.append(_text(30, 120, "next import of os is FREE", size=13,
                   fill=GREEN, bold=True, mono=True))
    b.append(_text(30, 210, "Side effects in module-level code ",
                   size=14, fill=DARK))
    b.append(_text(30, 234, "run once on first import \u2014 keep ",
                   size=14, fill=DARK))
    b.append(_text(30, 258, "them inside functions instead.",
                   size=14, fill=DARK))
    return _svg(620, 280, _arrowhead_def() + "".join(b))


# ---- registry -------------------------------------------------------------
DIAGRAMS = {
    "repl_shell": repl_shell,
    "run_flow": run_flow,
    "string_index": string_index,
    "string_slice": string_slice,
    "if_flow": if_flow,
    "for_loop": for_loop,
    "list_aliasing": list_aliasing,
    "dict_map": dict_map,
    "exception_tree": exception_tree,
    "scope_le": scope_le,
    "module_syspath": module_syspath,
    "fstring_eq": fstring_eq,
    "stdlib_shelf": stdlib_shelf,
    "deque": deque,
    "venv_boxes": venv_boxes,
    "float_0_1": float_0_1,
    "invoke_flow": invoke_flow,
    "env_vars": env_vars,
    "py_launcher": py_launcher,
    "win_venv": win_venv,
    "shebang_unix": shebang_unix,
    "path_parts": path_parts,
    "counter_flow": counter_flow,
    "itertools_flow": itertools_flow,
    "json_roundtrip": json_roundtrip,
    "cli_flow": cli_flow,
    "sqlite_tables": sqlite_tables,
    "sorting_flow": sorting_flow,
    "regex_flow": regex_flow,
    "argparse_deep": argparse_deep,
    "unicode_bytes": unicode_bytes,
    "async_loop": async_loop,
    "object_model": object_model,
    "dunder_power": dunder_power,
    "global_nonlocal": global_nonlocal,
    "operator_precedence": operator_precedence,
    "import_search": import_search,
}


def render(html):
    """Replace [[diag:name]] placeholders in lesson HTML with SVG markup."""
    for name, fn in DIAGRAMS.items():
        html = html.replace("[[diag:%s]]" % name, fn())
    return html
