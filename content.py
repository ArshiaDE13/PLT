"""Content assembly: combine chapters, validate structure, render diagrams."""

import re
from copy import deepcopy

from chapters_a import CHAPTERS_A
from chapters_b import CHAPTERS_B
from chapters_c import CHAPTERS_C
from chapters_d import CHAPTERS_D
from chapters_e import CHAPTERS_E
from chapters_f import CHAPTERS_F
from fa_howto import FA_HOWTO
from fa_library import FA_LIBRARY
from fa_reference import FA_REFERENCE
from fa_tutorial import FA_CONTENT as FA_TUTORIAL_CONTENT
from fa_using import FA_USING
import diagrams

# Persian variants for every section, merged by chapter id. English content
# stays the canonical source; the browser picks the fa variant at render time.
FA_CONTENT = {}
FA_CONTENT.update(FA_TUTORIAL_CONTENT)   # chapters 1-16  (Tutorial)
FA_CONTENT.update(FA_USING)              # chapters 17-19  (Using Python)
FA_CONTENT.update(FA_LIBRARY)            # chapters 20-23  (Library Reference)
FA_CONTENT.update(FA_HOWTO)              # chapters 24-27  (HowTo)
FA_CONTENT.update(FA_REFERENCE)          # chapters 28-31  (Language Reference)

QUIZ_TYPES = {"mc", "blank", "order", "codefill"}

CHAPTERS = (CHAPTERS_A + CHAPTERS_B + CHAPTERS_C + CHAPTERS_D
            + CHAPTERS_E + CHAPTERS_F)


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
    """Return the full course as plain data ready for JSON serialization.

    Lesson HTML still contains [[diag:name]] placeholders at this point;
    they are replaced by SVG markup here. When a Persian variant exists in
    FA_CONTENT it is attached as title_fa / html_fa (lessons) or a ``fa``
    override dict (quiz questions); the browser picks it at render time,
    so English stays the canonical source.

    Persian lessons reference English code listings as [[codeN]] placeholders
    (the N-th <pre class="code"> block); those are spliced verbatim so the
    code renders byte-identical in both languages.
    """
    chapters = deepcopy(CHAPTERS)
    overrides = FA_CONTENT
    for chapter in chapters:
        over = overrides.get(chapter["id"]) or {}
        if over.get("title"):
            chapter["title_fa"] = over["title"]
        fa_lessons = over.get("lessons") or []
        for i, lesson in enumerate(chapter["lessons"]):
            lesson["html"] = diagrams.render(lesson["html"])
            if i < len(fa_lessons) and fa_lessons[i].get("html"):
                fa_html = fa_lessons[i]["html"]
                # splice English code listings into the Persian lesson
                fa_html = splice_code_blocks(lesson["html"], fa_html)
                lesson["title_fa"] = fa_lessons[i].get("title") or lesson.get("title")
                lesson["html_fa"] = diagrams.render(fa_html)
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
                if entry:
                    q["fa"] = entry
    return chapters


def validate():
    """Raise ValueError if the content data is malformed."""
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
            for name in re.findall(r"\[\[diag:([a-z_0-9]+)\]\]", html):
                if name not in diagrams.DIAGRAMS:
                    errors.append("%s: unknown diagram [[diag:%s]]"
                                  % (cid, name))
            if not html.strip():
                errors.append("%s: empty lesson %r" % (cid, lesson.get("title")))
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
        raise ValueError("content validation failed:\n- " + "\n- ".join(errors))
    return CHAPTERS
