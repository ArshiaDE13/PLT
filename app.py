"""Python Tutor — interactive course based on the Python 3.14 tutorial.

Run it:              python app.py
Self-test:           python app.py --selftest
Change port:         python app.py --port 9000
No auto-open:        python app.py --no-browser
"""

import argparse
import sys
import threading
import webbrowser

import checker
import content
import server

# Windows consoles default to cp1252, which cannot encode emoji or the
# checkmark used below; reconfigure stdout so the app never crashes while
# printing its banner or self-test output.
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass

DEFAULT_PORT = 8765
HOST = "127.0.0.1"


def selftest():
    """Headless validation: content integrity + quiz checkers + runner."""
    failures = []

    def expect(cond, msg):
        if not cond:
            failures.append(msg)

    # 1. content structure
    try:
        content.validate()
    except ValueError as exc:
        print("FAIL: content validation\n%s" % exc)
        return 1
    # build_content returns rendered copies (diagrams inlined, Persian
    # variants attached); validate() left the source chapters untouched.
    chapters = content.build_content()
    total_q = sum(len(ch["quiz"]) for ch in chapters)
    total_lessons = sum(len(ch["lessons"]) for ch in chapters)
    print("content OK: %d chapters, %d lessons, %d quiz questions"
          % (len(chapters), total_lessons, total_q))

    # 2. diagrams render without leftover placeholders (both languages)
    for ch in chapters:
        for lesson in ch["lessons"]:
            for key in ("html", "html_fa"):
                html = lesson.get(key) or ""
                expect("[[diag:" not in html and "[[code" not in html,
                       "%s: leftover diagram/code placeholder" % ch["id"])

    # 3. every quiz question is answerable correctly by its own data
    for ch in chapters:
        for i, q in enumerate(ch["quiz"]):
            if q["type"] == "mc":
                ok, _ = checker.check_mc(q, q["answer"])
                wrong, _ = checker.check_mc(q, (q["answer"] + 1) % len(q["options"]))
            elif q["type"] == "blank":
                ok, _ = checker.check_blank(q, q["answers"][0])
                wrong, _ = checker.check_blank(q, "zzz definitely wrong zzz")
            elif q["type"] == "order":
                ok, _ = checker.check_order(q, list(range(len(q["lines"]))))
                wrong, _ = checker.check_order(q, [1, 0] + list(range(2, len(q["lines"]))))
            elif q["type"] == "codefill":
                blanks = [b for b in q["code"] if isinstance(b, dict)]
                answer = [b["answers"][0] for b in blanks]
                ok, _ = checker.check_codefill(q, answer)
                wrong = list(answer)
                if wrong:
                    wrong[0] = "zzz definitely wrong zzz"
                wrong, _ = checker.check_codefill(q, wrong)
            else:
                expect(False, "%s quiz[%d]: unexpected type" % (ch["id"], i))
                continue
            expect(ok, "%s quiz[%d]: correct answer rejected" % (ch["id"], i))
            expect(not wrong, "%s quiz[%d]: wrong answer accepted" % (ch["id"], i))
    print("quiz checkers OK: all %d questions accept the right answer and "
          "reject a wrong one" % total_q)

    # 4. code runner (only meaningful under a real interpreter)
    result = checker.run_code("print(2 + 3)\n")
    expect(result["ok"] and result["output"].strip() == "5",
           "runner: expected '5', got %r" % result)
    result2 = checker.run_code("print('hi')\n")
    expect(result2["ok"] and result2["output"].strip() == "hi",
           "runner: expected 'hi', got %r" % result2)
    if not getattr(sys, "frozen", False):
        print("code runner OK")

    if failures:
        print("\nFAILURES (%d):" % len(failures))
        for f in failures:
            print(" - " + f)
        return 1
    print("\nAll self-tests passed. ✔")
    return 0


def find_port(start):
    import socket
    for port in range(start, start + 50):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind((HOST, port))
                return port
            except OSError:
                continue
    raise OSError("no free port found near %d" % start)


def _fatal(message):
    """Show a start-up error even in a windowed (console-less) build."""
    if sys.platform.startswith("win"):
        try:
            import ctypes
            ctypes.windll.user32.MessageBoxW(
                0, message, "Python Tutor", 0x10)  # MB_ICONERROR
            return
        except Exception:
            pass
    print(message, file=sys.stderr)


def _main(argv=None):
    parser = argparse.ArgumentParser(description="Python Tutor course app")
    parser.add_argument("--port", type=int, default=DEFAULT_PORT,
                        help="port for the local web server (default %d)"
                             % DEFAULT_PORT)
    parser.add_argument("--no-browser", action="store_true",
                        help="do not open the web browser automatically")
    parser.add_argument("--selftest", action="store_true",
                        help="run headless self-tests and exit")
    args = parser.parse_args(argv)

    if args.selftest:
        return selftest()

    port = find_port(args.port)
    httpd = server.make_server(HOST, port)
    url = "http://%s:%d/" % (HOST, port)

    # Give a frozen one-file app time to unpack before opening the browser.
    if not args.no_browser:
        threading.Timer(1.5, lambda: webbrowser.open(url)).start()

    print("=" * 60)
    print("  🐍  Python Tutor — Learn Python 3.14 from the tutorial")
    print("  Serving at: %s" % url)
    print("  Close this window to stop the app.")
    print("=" * 60)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nBye!")
    return 0


def main(argv=None):
    try:
        return _main(argv)
    except Exception as exc:  # defensive: windowed builds have no console
        _fatal("Python Tutor failed to start:\n\n%s" % exc)
        return 1


if __name__ == "__main__":
    sys.exit(main())
