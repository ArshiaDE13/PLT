"""Minimal stdlib HTTP server: serves the web UI and the quiz API."""

import json
import os
import sys
import urllib.parse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import checker
import content

# Locate the static folder: source tree in dev, bundled data when frozen.
BASE_DIR = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
STATIC_DIR = os.path.join(BASE_DIR, "static")

# Build the course once. Content validation errors crash loudly at startup.
CHAPTERS = content.validate()
CONTENT_JSON = json.dumps({"chapters": content.build_content()}, ensure_ascii=False)

MIME = {
    ".html": "text/html; charset=utf-8",
    ".css": "text/css; charset=utf-8",
    ".js": "application/javascript; charset=utf-8",
    ".svg": "image/svg+xml",
    ".json": "application/json; charset=utf-8",
}


class TutorHandler(BaseHTTPRequestHandler):
    server_version = "PythonTutor/1.0"

    # ---- helpers ---------------------------------------------------------
    def _send(self, code, body, ctype):
        if isinstance(body, str):
            body = body.encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def _send_json(self, obj, code=200):
        self._send(code, json.dumps(obj, ensure_ascii=False),
                   "application/json; charset=utf-8")

    def _read_json(self):
        length = int(self.headers.get("Content-Length", 0) or 0)
        if length <= 0:
            return {}
        try:
            return json.loads(self.rfile.read(length).decode("utf-8"))
        except (ValueError, UnicodeDecodeError):
            return {}

    def log_message(self, fmt, *args):
        # Keep the console quiet unless a real error occurs.
        pass

    # ---- routes ----------------------------------------------------------
    def do_GET(self):
        path = urllib.parse.urlparse(self.path).path
        if path == "/" or path == "/index.html":
            self._serve_file("index.html", ".html")
        elif path == "/style.css":
            self._serve_file("style.css", ".css")
        elif path == "/app.js":
            self._serve_file("app.js", ".js")
        elif path == "/api/content":
            self._send(200, CONTENT_JSON, MIME[".json"])
        elif path == "/favicon.ico":
            self.send_response(204)
            self.end_headers()
        else:
            self._send(404, "Not found", "text/plain; charset=utf-8")

    def _serve_file(self, name, ext):
        full = os.path.join(STATIC_DIR, name)
        try:
            with open(full, "rb") as fh:
                data = fh.read()
        except OSError:
            self._send(404, "Missing file: %s" % name,
                       "text/plain; charset=utf-8")
            return
        self._send(200, data, MIME.get(ext, "application/octet-stream"))

    def do_POST(self):
        path = urllib.parse.urlparse(self.path).path
        payload = self._read_json()
        if path == "/api/check":
            q, answer = payload.get("q"), payload.get("answer")
            if not isinstance(q, dict):
                self._send_json({"correct": False, "explain": "Bad request"})
                return
            correct, explain = checker.check_question(q, answer)
            self._send_json({"correct": correct, "explain": explain})
        elif path == "/api/run":
            result = checker.run_code(payload.get("code", ""))
            self._send_json(result)
        else:
            self._send_json({"error": "Not found"}, 404)


def make_server(host, port):
    return ThreadingHTTPServer((host, port), TutorHandler)
