"""C Tutor content assembly: combine chapters, merge Persian, validate.

Mirrors content.py but for the C course (no diagrams — C lessons use
ASCII art in <pre> blocks instead of [[diag:...]] placeholders). The
result is written to static/data-c.js by build_static.py as
window.COURSE_DATA_C.
"""

import re
from copy import deepcopy

from ctutor_chapters_a import CHAPTERS_CT_A
from ctutor_chapters_b import CHAPTERS_CT_B
from ctutor_chapters_c import CHAPTERS_CT_C
from ctutor_fa_a import FA_CT_A
from ctutor_fa_b import FA_CT_B
from ctutor_fa_c import FA_CT_C

# Persian variants for every chapter, merged by chapter id. English content
# stays the canonical source; the browser picks the fa variant at render time.
FA_CONTENT = {}
FA_CONTENT.update(FA_CT_A)   # chapters 1-5   (Syntax & Basics .. Type System)
FA_CONTENT.update(FA_CT_B)   # chapters 6-9   (Organization .. Low-Level)
FA_CONTENT.update(FA_CT_C)   # chapters 10-13 (Advanced .. Modern)

CHAPTERS = CHAPTERS_CT_A + CHAPTERS_CT_B + CHAPTERS_CT_C

QUIZ_TYPES = {"mc", "blank", "order", "codefill"}

_PRE_BLOCK_RE = re.compile(r'<pre class="code">.*?</pre>', re.S)
_CODE_TOKEN_RE = re.compile(r'\[\[code(\d+)\]\]')


def splice_code_blocks(english_html, fa_html):
    """Replace [[codeN]] tokens in Persian lesson HTML with the N-th
    <pre class="code"> block taken verbatim from the English lesson, so
    code samples stay byte-identical across languages."""
    blocks = _PRE_BLOCK_RE.findall(english_html)
    if not blocks:
        return fa_html

    def repl(match):
        idx = int(match.group(1))
        return blocks[idx] if idx < len(blocks) else match.group(0)

    return _CODE_TOKEN_RE.sub(repl, fa_html)


def build_content():
    """Return the full C course as plain data ready for JSON serialization.

    When a Persian variant exists in FA_CONTENT it is attached as
    title_fa / html_fa (lessons) or a ``fa`` override dict (quiz
    questions); the browser picks it at render time.
    """
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
                if fq.get("question"):
                    entry["question"] = fq["question"]
                if fq.get("options"):
                    entry["options"] = fq["options"]
                if fq.get("explain"):
                    entry["explain"] = fq["explain"]
                if fq.get("lines"):
                    entry["lines"] = fq["lines"]
                if fq.get("code"):
                    entry["code"] = fq["code"]
                if entry:
                    q["fa"] = entry
    return chapters


def validate():
    """Raise ValueError if the C content data is malformed."""
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
                errors.append("%s: C lessons must not use [[diag:...]]" % cid)
            if lesson.get("tryit") is not None and not lesson["tryit"].strip():
                errors.append("%s: empty tryit in %r" % (cid, lesson.get("title")))
        if not ch.get("quiz"):
            errors.append("%s: no quiz" % cid)
        for i, q in enumerate(ch["quiz"]):
            if q.get("type") not in QUIZ_TYPES:
                errors.append("%s quiz[%d]: unknown type %r"
                              % (cid, i, q.get("type")))
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
        raise ValueError("C content validation failed:\n- " + "\n- ".join(errors))
    return CHAPTERS
