"""C++ Tutor content assembly: 44 chapters, merge Persian, validate."""

import re
from copy import deepcopy

from chapters_cpp_a import CHAPTERS_CPP_A
from chapters_cpp_b import CHAPTERS_CPP_B
from chapters_cpp_c import CHAPTERS_CPP_C
from chapters_cpp_d import CHAPTERS_CPP_D
from chapters_cpp_e import CHAPTERS_CPP_E
from chapters_cpp_fa_a import FA_CPP as FA_CPP_A
from chapters_cpp_fa_b import FA_CPP_B
from chapters_cpp_fa_c import FA_CPP_C
from chapters_cpp_fa_d import FA_CPP_D
from chapters_cpp_fa_e import FA_CPP_E

FA_CONTENT = {}
FA_CONTENT.update(FA_CPP_A)
FA_CONTENT.update(FA_CPP_B)
FA_CONTENT.update(FA_CPP_C)
FA_CONTENT.update(FA_CPP_D)
FA_CONTENT.update(FA_CPP_E)

CHAPTERS = (CHAPTERS_CPP_A + CHAPTERS_CPP_B +
            CHAPTERS_CPP_C + CHAPTERS_CPP_D + CHAPTERS_CPP_E)

QUIZ_TYPES = {"mc", "blank", "order", "codefill"}

_PRE_BLOCK_RE = re.compile(r'<pre class="code">.*?</pre>', re.S)
_CODE_TOKEN_RE = re.compile(r'\[\[code(\d+)\]\]')


def splice_code_blocks(english_html, fa_html):
    blocks = _PRE_BLOCK_RE.findall(english_html)
    if not blocks:
        return fa_html
    def repl(match):
        idx = int(match.group(1))
        return blocks[idx] if idx < len(blocks) else match.group(0)
    return _CODE_TOKEN_RE.sub(repl, fa_html)


def build_content():
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
        raise ValueError("C++ content validation failed:\n- " + "\n- ".join(errors))
    return CHAPTERS
