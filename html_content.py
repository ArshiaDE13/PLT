"""HTML Tutor content assembly: combine chapters, merge Persian, validate.

Mirrors ctutor_content.py for the HTML course (MDN-based). The result is
written to static/data-html.js by build_static.py as
window.COURSE_DATA_HTML.
"""

import re
from copy import deepcopy

from chapters_html_a import CHAPTERS_HTML_A
from chapters_html_b import CHAPTERS_HTML_B
from chapters_html_c import CHAPTERS_HTML_C
from chapters_html_fa_a import FA_HTML_A
from chapters_html_fa_b import FA_HTML_B
from chapters_html_fa_c import FA_HTML_C

FA_CONTENT = {}
FA_CONTENT.update(FA_HTML_A)   # chapters 1-5
FA_CONTENT.update(FA_HTML_B)   # chapters 6-9
FA_CONTENT.update(FA_HTML_C)   # chapters 10-13

CHAPTERS = CHAPTERS_HTML_A + CHAPTERS_HTML_B + CHAPTERS_HTML_C

QUIZ_TYPES = {"mc", "blank", "order", "codefill"}

_PRE_BLOCK_RE = re.compile(r'<pre class="code">.*?</pre>', re.S)
_CODE_TOKEN_RE = re.compile(r'\[\[code(\d+)\]\]')


def splice_code_blocks(english_html, fa_html):
    """Replace [[codeN]] tokens in Persian lesson HTML with the N-th
    <pre class="code"> block from the English lesson."""
    blocks = _PRE_BLOCK_RE.findall(english_html)
    if not blocks:
        return fa_html

    def repl(match):
        idx = int(match.group(1))
        return blocks[idx] if idx < len(blocks) else match.group(0)

    return _CODE_TOKEN_RE.sub(repl, fa_html)


def build_content():
    """Return the full HTML course as plain data ready for JSON."""
    chapters = deepcopy(CHAPTERS)
    for chapter in chapters:
        over = FA_CONTENT.get(chapter["id"]) or {}
        if over.get("title"):
            chapter["title_fa"] = over["title"]
        fa_lessons = over.get("lessons") or []
        for i, lesson in enumerate(chapter["lessons"]):
            if i < len(fa_lessons) and fa_lessons[i].get("html"):
                fa_html = fa_lessons[i]["html"]
                fa_html = splice_code_blocks(lesson["html"], fa_html)
                lesson["title_fa"] = fa_lessons[i].get("title") or lesson.get("title")
                lesson["html_fa"] = fa_html
        fa_quiz = over.get("quiz") or []
        for i, q in enumerate(chapter.get("quiz", [])):
            if i < len(fa_quiz) and fa_quiz[i]:
                fq = fa_quiz[i]
                entry = {}
                for key in ("question", "options", "explain", "lines", "code"):
                    if fq.get(key):
                        entry[key] = fq[key]
                if entry:
                    q["fa"] = entry
    return chapters


def validate():
    """Raise ValueError if the HTML content data is malformed."""
    errors = []
    seen_ids = set()
    for ch in CHAPTERS:
        cid = ch.get("id")
        if not cid:
            errors.append("chapter missing id")
        if cid in seen_ids:
            errors.append("duplicate chapter id: %r" % cid)
        seen_ids.add(cid)
        if not ch.get("lessons"):
            errors.append("%s: no lessons" % cid)
        for lesson in ch["lessons"]:
            html = lesson.get("html", "")
            if not html.strip():
                errors.append("%s: empty lesson %r" % (cid, lesson.get("title")))
            if "[[diag:" in html:
                errors.append("%s: HTML lessons must not use [[diag:...]]" % cid)
            if lesson.get("tryit") is not None and not lesson["tryit"].strip():
                errors.append("%s: empty tryit in %r" % (cid, lesson.get("title")))
        if not ch.get("quiz"):
            errors.append("%s: no quiz" % cid)
        for i, q in enumerate(ch["quiz"]):
            if q.get("type") not in QUIZ_TYPES:
                errors.append("%s quiz[%d]: unknown type %r" % (cid, i, q.get("type")))
            if not q.get("question"):
                errors.append("%s quiz[%d]: missing question" % (cid, i))
            if q["type"] == "mc":
                if len(q.get("options", [])) < 2:
                    errors.append("%s quiz[%d]: mc needs options" % (cid, i))
                if not (0 <= q.get("answer", -1) < len(q["options"])):
                    errors.append("%s quiz[%d]: mc answer out of range" % (cid, i))
            elif q["type"] == "blank":
                if not q.get("answers"):
                    errors.append("%s quiz[%d]: blank needs answers" % (cid, i))
            elif q["type"] == "order":
                if len(q.get("lines", [])) < 2:
                    errors.append("%s quiz[%d]: order needs lines" % (cid, i))
            elif q["type"] == "codefill":
                code = q.get("code", [])
                if not code:
                    errors.append("%s quiz[%d]: codefill needs code" % (cid, i))
                for item in code:
                    if isinstance(item, dict) and not item.get("answers"):
                        errors.append("%s quiz[%d]: blank without answers" % (cid, i))
            if not q.get("explain"):
                errors.append("%s quiz[%d]: missing explanation" % (cid, i))
    if errors:
        raise ValueError("HTML content validation failed:\n- " + "\n- ".join(errors))
    return CHAPTERS
