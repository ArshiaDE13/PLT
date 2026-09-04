"""Quiz answer checking and a sandboxed Python code runner.

All quiz checks are deterministic (no execution of user code), so they work
identically in dev and in frozen builds. The code *runner* used by the
"Try it" editor executes user code in a subprocess when running under a
real Python interpreter, and degrades gracefully otherwise.
"""

import re
import sys
import subprocess

# --------------------------------------------------------------------------
# normalization helpers
# --------------------------------------------------------------------------

def normalize(text):
    """Lowercase, strip, and collapse internal whitespace."""
    if not isinstance(text, str):
        return ""
    return re.sub(r"\s+", " ", text.strip().lower())


def _match_any(answers, given):
    g = normalize(given)
    for a in answers:
        if normalize(a) == g:
            return True
    return False


# --------------------------------------------------------------------------
# question checks — each returns (correct: bool, explain: str)
# --------------------------------------------------------------------------

def check_mc(q, answer):
    correct = isinstance(answer, int) and answer == q["answer"]
    return correct, q.get("explain", "")


def check_blank(q, answer):
    correct = _match_any(q["answers"], answer)
    return correct, q.get("explain", "")


def check_order(q, answer):
    """answer is a list of indices in the order the user picked them."""
    expected = list(range(len(q["lines"])))
    correct = isinstance(answer, list) and answer == expected
    return correct, q.get("explain", "")


def check_codefill(q, answer):
    """answer is a list of strings, one per blank in the code template."""
    blanks = [item for item in q["code"] if isinstance(item, dict)]
    if not isinstance(answer, list) or len(answer) != len(blanks):
        return False, q.get("explain", "")
    for blank, given in zip(blanks, answer):
        if not _match_any(blank.get("answers", []), given):
            return False, q.get("explain", "")
    return True, q.get("explain", "")


CHECKERS = {
    "mc": check_mc,
    "blank": check_blank,
    "order": check_order,
    "codefill": check_codefill,
}


def check_question(q, answer):
    fn = CHECKERS.get(q.get("type"))
    if fn is None:
        return False, "Unknown question type: %r" % q.get("type")
    return fn(q, answer)


# --------------------------------------------------------------------------
# sandboxed code runner (used by the "Try it" editor)
# --------------------------------------------------------------------------

_RUN_TIMEOUT = 5  # seconds


def run_code(code):
    """Execute user code and return {"ok": bool, "output": str}.

    Uses a fresh Python subprocess with isolation flags so nothing the user
    types can touch this app. If execution is not possible (e.g. inside a
    frozen executable), returns a friendly message instead of crashing.
    """
    if not code or not code.strip():
        return {"ok": True, "output": ""}
    frozen = getattr(sys, "frozen", False)
    if frozen:
        # Subprocesses can't be spawned from a frozen one-file app; fall
        # back to a simple in-process check that never executes the code.
        try:
            compile(code, "<user_code>", "exec")
            return {"ok": True, "output": "(code compiled — live execution "
                    "is disabled in this packaged build; install Python to "
                    "run code here)"}
        except SyntaxError as exc:
            return {"ok": False, "output": "SyntaxError: %s" % exc.msg}
    try:
        proc = subprocess.run(
            [sys.executable, "-I", "-c", code],
            capture_output=True,
            text=True,
            timeout=_RUN_TIMEOUT,
        )
    except subprocess.TimeoutExpired:
        return {"ok": False, "output": "Timed out after %d seconds."
                % _RUN_TIMEOUT}
    except OSError as exc:
        return {"ok": False, "output": "Could not start Python: %s" % exc}

    output = proc.stdout
    if proc.stderr:
        output += (output and "\n" or "") + proc.stderr
    return {"ok": proc.returncode == 0, "output": output.rstrip("\n")}
