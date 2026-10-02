"use strict";

/* CEngine — a small C interpreter written in pure JavaScript.
   ==============================================================

   WHY: the Python course runs real Python via Pyodide (WASM, ~10 MB,
   CDN). For C there is no equivalent lightweight engine, so the C tutor
   ships its own interpreter: zero download, instant start, fully
   self-contained — same philosophy as the rest of this static site.

   WHAT IT SUPPORTS (a generous teaching subset of ISO C):
   - the full core language: all operators, if/else, switch, loops,
     goto/labels, functions, recursion, pointers (incl. pointer
     arithmetic on a REAL byte-addressed memory), arrays (1-D/2-D/VLA),
     strings, struct/union/enum/typedef, const, casts, sizeof,
     function pointers, compound literals, _Generic selections,
     incomplete types, setjmp/longjmp
   - a faithful memory model: little-endian bytes, natural struct
     alignment/padding (so offsetof and "memory layout" lessons are
     truthful), malloc/calloc/realloc/free on a heap region
   - a small in-memory filesystem so fopen/fgets/fwrite... actually run
   - standard headers: stdio, stdlib, string, stddef, stdbool, stdint,
     ctype, math, time, errno, assert, limits, setjmp, locale (minimal)
   - the preprocessor: #include, #define (object + function-like,
     # / ## operators), #undef, conditional compilation
     (#if/#ifdef/#ifndef/#elif/#else/#endif, defined()), #error

   WHAT IT DELIBERATELY DOES NOT SUPPORT (fails with a clear,
   localized-friendly message instead of misbehaving): variadic
   *definitions* (va_list), multithreading, atomics, signals, wide
   characters, and OS-level features a browser sandbox cannot provide.

   Model notes: LP64 (long/long long/pointer = 8 bytes), char is signed,
   long long arithmetic is exact up to 2^53 (JS number limits).

   window.CEngine.run(source, opts) ->
       { ok:true,  output, exit }   normal end (exit = return code)
       { ok:false, output, error, phase: "compile" | "runtime" }
   opts: { input: "text for stdin", argv: ["prog", ...], maxSteps }
   ======================================================================== */

(function () {

  /* ============================ diagnostics ============================= */

  function CErr(message, line, phase) {
    this.message = message;
    this.line = line || 0;
    this.phase = phase || "compile";
  }
  CErr.prototype = Object.create(Error.prototype);

  function err(msg, line) { throw new CErr(msg, line, "compile"); }
  function rerr(msg, line) { throw new CErr(msg, line, "runtime"); }

  /* =========================== preprocessor ============================= */

  /* Strip // and /* ... *​/ comments, preserving newlines (block comments
     may hide '#' directives, so they must go before directive scanning). */
  function stripComments(src) {
    let out = "", i = 0, n = src.length;
    while (i < n) {
      const c = src[i], d = i + 1 < n ? src[i + 1] : "";
      if (c === "/" && d === "/") {
        while (i < n && src[i] !== "\n") out += " ", i++;
      } else if (c === "/" && d === "*") {
        out += "  "; i += 2;
        while (i < n && !(src[i] === "*" && i + 1 < n && src[i + 1] === "/")) {
          out += src[i] === "\n" ? "\n" : " ";
          i++;
        }
        if (i >= n) err("unterminated /* comment");
        out += "  "; i += 2;
      } else if (c === '"' || c === "'") {
        // copy the literal untouched (a "//" inside a string is not a comment)
        const quote = c;
        out += c; i++;
        while (i < n && src[i] !== quote) {
          if (src[i] === "\\") { out += src[i] + (src[i + 1] || ""); i += 2; }
          else { out += src[i]; i++; }
        }
        if (i >= n) err("unterminated " + (quote === '"' ? "string" : "character") + " literal");
        out += quote; i++;
      } else {
        out += c; i++;
      }
    }
    return out;
  }

  const KNOWN_HEADERS = {
    "stdio.h": 1, "stdlib.h": 1, "string.h": 1, "stddef.h": 1,
    "stdbool.h": 1, "stdint.h": 1, "inttypes.h": 1, "ctype.h": 1,
    "math.h": 1, "time.h": 1, "errno.h": 1, "assert.h": 1,
    "limits.h": 1, "float.h": 1, "setjmp.h": 1, "locale.h": 1,
    "unistd.h": 1,
    // includable, but the functions these declare cannot run in a browser
    "signal.h": 1, "threads.h": 1, "stdatomic.h": 1,
    "wchar.h": 1, "uchar.h": 1,
  };
  const RESTRICTED_HEADERS = { "signal.h": 1, "threads.h": 1, "stdatomic.h": 1 };

  /* ------------------- minimal C++ lowering -------------------------------
     The sandbox runs a C interpreter, but the C++ course's runnable seeds
     use a small C++ subset. Before preprocessing we lower it to C:
       - <iostream> and friends are aliased to their C equivalents
       - `using namespace std;` is dropped, `std::` is stripped
       - string::npos becomes a builtin constant
     The runtime side (cout/endl, a string type with methods, references)
     lives in the interpreter proper. Anything outside this subset (classes,
     templates, STL containers) fails with a normal parse error. */
  const CPP_HEADER_ALIAS = {
    "iostream": "stdio.h", "string": "string.h", "cstring": "string.h",
    "cstdlib": "stdlib.h", "cmath": "math.h", "cctype": "ctype.h",
    "climits": "limits.h", "cfloat": "float.h", "cassert": "assert.h",
    "ctime": "time.h", "cstddef": "stddef.h", "cstdint": "stdint.h",
    "cinttypes": "inttypes.h", "cerrno": "errno.h",
  };
  const CPP_IGNORE_HEADERS = {
    "vector": 1, "memory": 1, "algorithm": 1, "numeric": 1, "functional": 1,
    "stdexcept": 1, "utility": 1, "map": 1, "set": 1, "unordered_map": 1,
    "unordered_set": 1, "array": 1, "iterator": 1, "chrono": 1,
    "initializer_list": 1, "string_view": 1, "optional": 1, "variant": 1,
    "any": 1, "tuple": 1, "typeinfo": 1, "new": 1, "compare": 1,
    "numbers": 1, "concepts": 1, "ranges": 1, "span": 1, "format": 1,
  };
  const CPP_RE = /\bstd\s*::|<iostream>|<string>|<vector>|<memory>|<algorithm>|<numeric>|<string_view>|<utility>|<functional>|<map>|<set>|<array>|<optional>|<variant>|<tuple>|<chrono>|<format>|<ranges>|<span>|<concepts>|<compare>|<numbers>|\busing\s+namespace\b|\bnamespace\b|\bclass\s+[A-Za-z_]|\bcout\b|\bcin\b|\bendl\b|\barray\s*<|\bvector\s*</;

  /* is a C++ program at all (drives cppMode even when nothing needs
     rewriting) vs. the textual lowering itself */
  function isCppSource(src) {
    return CPP_RE.test(src);
  }

  /* Split a line into string-literal and code parts, lower only the code. */
  function lowerCppLine(line) {
    const parts = line.split(/("(?:[^"\\]|\\.)*")/);
    for (let i = 0; i < parts.length; i += 2) {
      parts[i] = parts[i]
        .replace(/\bstd\s*::\s*/g, "")
        .replace(/\busing\s+namespace\s+\w+\s*;/g, "")
        .replace(/\bstring\s*::\s*npos\b/g, "npos")
        // C++ cast syntax -> C cast: static_cast<int>(x) becomes ((int)(x))
        .replace(/\b(?:static_cast|dynamic_cast|const_cast|reinterpret_cast)\s*<\s*([^<>]*)\s*>/g,
                 "($1)");
    }
    return parts.join("");
  }

  function lowerCppSource(src) {
    if (!CPP_RE.test(src)) return src;
    return src.split("\n").map(lowerCppLine).join("\n");
  }

  /* Parse directive lines and produce (a) the expanded plain-C text,
     (b) the set of included headers, (c) a macro table. Macros are stored
     as {args:[..]|null, body:"raw replacement text", line}. */
  function preprocess(src, cppMode) {
    const text = stripComments(src);
    const lines = text.split("\n");
    const outLines = [];
    const macros = {};          // name -> {args, body, line}
    const headers = [];         // included header names
    const condStack = [];       // {active, taken, seenElse}
    let lineNo = 0;
    if (cppMode) {
      macros["bool"] = { args: null, body: "_Bool", line: 0 };
      macros["npos"] = { args: null, body: "((int)-1)", line: 0 };
    }

    function skipping() {
      for (const c of condStack) if (!c.active) return true;
      return false;
    }
    function evalCondExpr(expr, line) {
      // replace defined(X) / defined X with 0/1, expand macros, then
      // evaluate the resulting integer constant expression
      expr = expr.replace(/defined\s*\(\s*([A-Za-z_]\w*)\s*\)/g,
        (_, id) => (macros[id] !== undefined ? 1 : 0));
      expr = expr.replace(/defined\s+([A-Za-z_]\w*)/g,
        (_, id) => (macros[id] !== undefined ? 1 : 0));
      expr = expandMacrosInText(expr, macros, line);
      if (!expr.trim()) err("#if with empty expression", line);
      return evalConstExprText(expr, line);
    }

    for (const raw of lines) {
      lineNo++;
      const line = raw;
      const m = line.match(/^\s*#\s*([A-Za-z]+)\s*(.*)$/);

      if (m) {
        const dir = m[1], rest = m[2].trim();
        if (dir === "ifdef" || dir === "ifndef") {
          if (skipping()) { condStack.push({ active: false, taken: true, seenElse: false }); continue; }
          const id = rest.split(/\s+/)[0];
          if (!/^[A-Za-z_]\w*$/.test(id)) err("#" + dir + " needs an identifier", lineNo);
          const has = macros[id] !== undefined;
          const active = dir === "ifdef" ? has : !has;
          condStack.push({ active, taken: active, seenElse: false });
          continue;
        }
        if (dir === "if") {
          if (skipping()) { condStack.push({ active: false, taken: true, seenElse: false }); continue; }
          const active = !!evalCondExpr(rest, lineNo);
          condStack.push({ active, taken: active, seenElse: false });
          continue;
        }
        if (dir === "elif") {
          const top = condStack[condStack.length - 1];
          if (!top || top.seenElse) err("#elif without #if", lineNo);
          if (top.taken) { top.active = false; }
          else if (!skipping()) {
            const active = !!evalCondExpr(rest, lineNo);
            top.active = active; top.taken = top.taken || active;
          } else top.active = false;
          continue;
        }
        if (dir === "else") {
          const top = condStack[condStack.length - 1];
          if (!top || top.seenElse) err("#else without #if", lineNo);
          top.seenElse = true;
          top.active = !skipping() && !top.taken;
          top.taken = top.taken || top.active;
          continue;
        }
        if (dir === "endif") {
          if (!condStack.pop()) err("#endif without #if", lineNo);
          continue;
        }
        if (skipping()) continue;

        if (dir === "include") {
          const inc = rest.match(/^[<"]([^>"]+)[>"]$/);
          if (!inc) err("#include expects <header> or \"header\"", lineNo);
          let name = inc[1];
          if (!KNOWN_HEADERS[name] && CPP_HEADER_ALIAS[name]) {
            name = CPP_HEADER_ALIAS[name]; // <iostream> -> stdio.h, etc.
          }
          if (!KNOWN_HEADERS[name]) {
            if (CPP_IGNORE_HEADERS[name]) continue; // accepted, but a no-op
            err("the browser sandbox does not have the header <" + inc[1] +
                ">. Available: " + Object.keys(KNOWN_HEADERS).join(", ") +
                " and the C++ versions of these (iostream, cstring, ...)",
                lineNo);
          }
          if (headers.indexOf(name) === -1) headers.push(name);
          injectHeaderMacros(name, macros);
          continue;
        }
        if (dir === "define") {
          const dm = rest.match(/^([A-Za-z_]\w*)(\(([^)]*)\))?\s*(.*)$/);
          if (!dm) err("bad #define", lineNo);
          const name = dm[1];
          let args = null;
          if (dm[2] !== undefined) {
            args = dm[3].trim() === "" ? [] :
              dm[3].split(",").map((a) => a.trim());
            for (const a of args) {
              if (!/^[A-Za-z_]\w*$/.test(a)) err("bad macro parameter " + a, lineNo);
            }
          }
          macros[name] = { args, body: dm[4].trim(), line: lineNo };
          continue;
        }
        if (dir === "undef") {
          const id = rest.split(/\s+/)[0];
          if (macros[id] !== undefined) delete macros[id];
          continue;
        }
        if (dir === "error") {
          err("#error " + rest, lineNo);
        }
        if (dir === "pragma" || dir === "line" || dir === "warning") continue;
        err("unknown preprocessor directive #" + dir, lineNo);
      }

      if (!skipping()) outLines.push(expandMacrosInText(line, macros, lineNo));
    }
    if (condStack.length) err("missing #endif");

    return { text: outLines.join("\n"), headers, macros };
  }

  /* Macros a real system header would predefine for you. */
  function injectHeaderMacros(name, macros) {
    if (["stdio.h", "stdlib.h", "string.h", "stddef.h", "time.h",
         "locale.h", "setjmp.h", "unistd.h"].indexOf(name) !== -1) {
      if (macros["NULL"] === undefined) {
        macros["NULL"] = { args: null, body: "((void*)0)", line: 0 };
      }
    }
    if (name === "stddef.h" && macros["offsetof"] === undefined) {
      // the classic definition — address arithmetic, no dereference
      macros["offsetof"] = { args: ["t", "m"],
        body: "((size_t)&(((t*)0)->m))", line: 0 };
    }
    if (name === "assert.h") {
      if (macros["NDEBUG"] !== undefined) {
        macros["assert"] = { args: ["x"], body: "((void)0)", line: 0 };
      } else {
        macros["assert"] = { args: ["x"],
          body: "__assert((x), #x, __LINE__)", line: 0 };
      }
    }
    if (name === "stdbool.h" && macros["bool"] === undefined) {
      macros["bool"] = { args: null, body: "_Bool", line: 0 };
    }
  }

  /* Expand macros inside a plain text fragment (used by #if lines). */
  function expandMacrosInText(text, macros, line) {
    let guard = 0;
    for (;;) {
      const next = expandOnceInText(text, macros, line);
      if (next === text) return text;
      text = next;
      if (++guard > 100) err("macro expansion too deep", line);
    }
  }

  function expandOnceInText(text, macros, line) {
    // operate on the text with a simple scanner; string/char literals
    // are skipped so their contents never expand
    let out = "", i = 0;
    while (i < text.length) {
      const c = text[i];
      if (c === '"' || c === "'") {
        const q = c; out += c; i++;
        while (i < text.length && text[i] !== q) {
          if (text[i] === "\\") { out += text[i] + (text[i + 1] || ""); i += 2; }
          else out += text[i++];
        }
        out += q; i++;
        continue;
      }
      const idm = text.slice(i).match(/^[A-Za-z_]\w*/);
      if (!idm) { out += c; i++; continue; }
      const id = idm[0];
      if (id === "__LINE__") { out += String(line); i += id.length; continue; }
      if (id === "__FILE__") { out += '"main.c"'; i += id.length; continue; }
      const mac = macros[id];
      if (!mac) { out += id; i += id.length; continue; }
      if (mac.args === null) {
        out += mac.body; // no added parens (they would break sizeof(type))
        i += id.length;
        continue;
      }
      // function-like: expand only when followed by '('
      let j = i + id.length;
      while (j < text.length && /\s/.test(text[j])) j++;
      if (text[j] !== "(") { out += id; i += id.length; continue; }
      const call = readMacroCall(text, j);
      if (!call) { out += id; i += id.length; continue; }
      out += substituteMacro(mac, call.args, line);
      i = call.end;
    }
    return out;
  }

  function readMacroCall(text, open) {
    // returns {args: [string], end: indexAfterClose} or null if unbalanced
    let depth = 0, args = [], cur = "", i = open;
    for (; i < text.length; i++) {
      const c = text[i];
      if (c === "(") { depth++; if (depth === 1) continue; }
      else if (c === ")") { depth--; if (depth === 0) { args.push(cur); return { args, end: i + 1 }; } }
      else if (c === "," && depth === 1) { args.push(cur); cur = ""; continue; }
      cur += c;
    }
    return null;
  }

  function substituteMacro(mac, argTexts, line) {
    if (argTexts.length !== mac.args.length) {
      err("macro expects " + mac.args.length + " argument(s), got " +
          argTexts.length, line);
    }
    let body = mac.body;
    // paste: a ## b — the raw argument texts joined token-to-token.
    // (paste runs BEFORE stringize so its '#' pair is never mistaken
    // for the stringize operator)
    body = body.replace(/([A-Za-z_]\w*)\s*##\s*([A-Za-z_]\w*)/g, (m, p1, p2) => {
      const i1 = mac.args.indexOf(p1), i2 = mac.args.indexOf(p2);
      const r1 = i1 >= 0 ? argTexts[i1].trim() : p1;
      const r2 = i2 >= 0 ? argTexts[i2].trim() : p2;
      return r1 + r2;
    });
    // stringize: #param (raw spelling of the argument)
    mac.args.forEach((a, k) => {
      body = body.replace(new RegExp("#\\s*" + a + "\\b", "g"),
        () => '"' + argTexts[k].trim().replace(/([\\"])/g, "\\$1") + '"');
    });
    // substitute the remaining parameters (plain textual replacement, like
    // a real preprocessor — no extra parens, or casts like (t*)0 would
    // break) — but never inside string/char literals
    const sorted = mac.args.slice().sort((a, b) => b.length - a.length);
    let outBody = "", bi = 0;
    while (bi < body.length) {
      const c = body[bi];
      if (c === '"' || c === "'") {
        const q = c;
        outBody += c; bi++;
        while (bi < body.length && body[bi] !== q) {
          if (body[bi] === "\\") { outBody += body[bi] + (body[bi + 1] || ""); bi += 2; }
          else { outBody += body[bi]; bi++; }
        }
        outBody += q; bi++;
        continue;
      }
      const idm = body.slice(bi).match(/^[A-Za-z_]\w*/);
      if (idm) {
        const k = sorted.indexOf(idm[0]);
        if (k >= 0) { outBody += argTexts[mac.args.indexOf(sorted[k])]; }
        else { outBody += idm[0]; }
        bi += idm[0].length;
        continue;
      }
      outBody += c; bi++;
    }
    return outBody;
  }

  /* Evaluate an integer constant expression coming from #if lines.
     Supports + - * / % << >> & | ^ < > <= >= == != && || ! ~ () and
     decimal/hex/octal literals. Enough for real-world guard code. */
  function evalConstExprText(text, line) {
    const toks = text.match(/<<|>>|<=|>=|==|!=|&&|\|\||[-+*/%&|^<>!~()?]?:|\d+\.?\d*(?:[eE][+-]?\d+)?|0[xX][0-9a-fA-F]+|[A-Za-z_]\w*/g) || [];
    let p = 0;
    function peek() { return toks[p]; }
    function eat(t) { if (toks[p] === t) { p++; return true; } return false; }
    function prim() {
      const t = toks[p];
      if (t === "(") { p++; const v = ternary(); if (!eat(")")) err("bad #if expression", line); return v; }
      if (t === "!") { p++; return prim() ? 0 : 1; }
      if (t === "~") { p++; return ~prim(); }
      if (t === "-") { p++; return -prim(); }
      if (t === "+") { p++; return prim(); }
      if (/^0[xX]/.test(t)) { p++; return parseInt(t, 16); }
      if (/^\d/.test(t)) { p++; return parseInt(t, /^0\d+$/.test(t) ? 8 : 10); }
      if (/^[A-Za-z_]/.test(t)) { p++; return 0; } // unknown ids are 0 (C rules)
      err("bad #if expression near " + t, line);
    }
    function mul() {
      let v = prim();
      for (;;) {
        if (eat("*")) v = v * prim();
        else if (eat("/")) { const d = prim(); if (d === 0) err("division by zero in #if", line); v = Math.trunc(v / d); }
        else if (eat("%")) { const d = prim(); if (d === 0) err("division by zero in #if", line); v = v % d; }
        else return v;
      }
    }
    function add() {
      let v = mul();
      for (;;) {
        if (eat("+")) v = v + mul();
        else if (eat("-")) v = v - mul();
        else return v;
      }
    }
    function shift() {
      let v = add();
      for (;;) {
        if (eat("<<")) v = v << add();
        else if (eat(">>")) v = v >> add();
        else return v;
      }
    }
    function rel() {
      let v = shift();
      for (;;) {
        if (eat("<=")) v = v <= shift() ? 1 : 0;
        else if (eat(">=")) v = v >= shift() ? 1 : 0;
        else if (eat("<")) v = v < shift() ? 1 : 0;
        else if (eat(">")) v = v > shift() ? 1 : 0;
        else return v;
      }
    }
    function eq() {
      let v = rel();
      for (;;) {
        if (eat("==")) v = v === rel() ? 1 : 0;
        else if (eat("!=")) v = v !== rel() ? 1 : 0;
        else return v;
      }
    }
    function bitAnd() { let v = eq(); while (eat("&")) v = v & eq(); return v; }
    function bitXor() { let v = bitAnd(); while (eat("^")) v = v ^ bitAnd(); return v; }
    function bitOr() { let v = bitXor(); while (eat("|")) v = v | bitXor(); return v; }
    function logAnd() { let v = bitOr(); while (eat("&&")) { const r = bitOr(); v = (v && r) ? 1 : 0; } return v; }
    function logOr() { let v = logAnd(); while (eat("||")) { const r = logAnd(); v = (v || r) ? 1 : 0; } return v; }
    function ternary() {
      const c = logOr();
      if (eat("?")) { const a = ternary(); if (!eat(":")) err("bad #if ?: ", line); const b = ternary(); return c ? a : b; }
      return c;
    }
    const v = ternary();
    return v;
  }

  /* =============================== lexer ================================ */

  const KEYWORDS = {};
  ("auto break case char const continue default do double else enum extern " +
   "float for goto if inline int long register restrict return short signed " +
   "sizeof static struct switch typedef union unsigned void volatile while " +
   "_Bool _Complex _Generic _Alignof _Alignas _Noreturn constexpr").split(" ")
    .forEach((k) => { KEYWORDS[k] = 1; });

  const PUNCTS = [
    "...", "<<=", ">>=", "->", "++", "--", "<<", ">>", "<=", ">=", "==",
    "!=", "&&", "||", "+=", "-=", "*=", "/=", "%=", "&=", "|=", "^=",
    "+", "-", "*", "/", "%", "=", "<", ">", "!", "~", "&", "|", "^",
    "?", ":", ";", ",", ".", "(", ")", "[", "]", "{", "}",
  ];

  function lex(src) {
    const toks = [];
    let i = 0, line = 1;
    const n = src.length;

    function push(k, v, extra) {
      const t = { k, v, line };
      if (extra) for (const key of Object.keys(extra)) t[key] = extra[key];
      toks.push(t);
    }

    while (i < n) {
      const c = src[i];
      if (c === "\n") { line++; i++; continue; }
      if (/\s/.test(c)) { i++; continue; }

      // identifiers / keywords
      if (/[A-Za-z_]/.test(c)) {
        let j = i;
        while (j < n && /[A-Za-z0-9_]/.test(src[j])) j++;
        const word = src.slice(i, j);
        if (KEYWORDS[word]) push("kw", word);
        else push("id", word);
        i = j;
        continue;
      }

      // numbers: hex, octal, decimal, floats, suffixes
      if (/[0-9]/.test(c) || (c === "." && /[0-9]/.test(src[i + 1] || ""))) {
        let j = i, isFloat = false, isU = false, isL = false, base = 10;
        if (c === "0" && /[xX]/.test(src[i + 1] || "")) {
          base = 16; j = i + 2;
          while (j < n && /[0-9a-fA-F]/.test(src[j])) j++;
        } else if (c === "0" && /[0-7]/.test(src[i + 1] || "")) {
          base = 8; j = i + 1;
          while (j < n && /[0-7]/.test(src[j])) j++;
        } else {
          while (j < n && /[0-9]/.test(src[j])) j++;
          if (src[j] === "." ) { isFloat = true; j++; while (j < n && /[0-9]/.test(src[j])) j++; }
          if (/[eE]/.test(src[j] || "") && /[0-9+\-]/.test(src[j + 1] || "")) {
            isFloat = true; j += 2; while (j < n && /[0-9]/.test(src[j])) j++;
          }
        }
        let text = src.slice(i, j);
        // suffixes
        while (j < n && /[uUlLfF]/.test(src[j])) {
          if (/[uU]/.test(src[j])) isU = true;
          else if (src[j] === "f" || src[j] === "F") isFloat = true;
          else isL = true;
          j++;
        }
        let value;
        if (isFloat) value = parseFloat(text);
        else value = parseInt(text.replace(/[uUlL]+$/g, ""), base);
        if (isNaN(value)) err("bad number literal " + text, line);
        push("num", value, { isFloat, isU, isL, text });
        i = j;
        continue;
      }

      // string literal
      if (c === '"') {
        let j = i + 1, s = "";
        while (j < n && src[j] !== '"') {
          if (src[j] === "\\") {
            const pair = readEscape(src, j, line);
            s += pair.text; j = pair.next;
          } else { s += src[j]; j++; }
        }
        if (j >= n) err("unterminated string literal", line);
        push("str", s, { line });
        i = j + 1;
        continue;
      }

      // character literal
      if (c === "'") {
        let j = i + 1, s = "";
        while (j < n && src[j] !== "'") {
          if (src[j] === "\\") {
            const pair = readEscape(src, j, line);
            s += pair.text; j = pair.next;
          } else { s += src[j]; j++; }
        }
        if (j >= n) err("unterminated character literal", line);
        if (s.length === 0) err("empty character literal", line);
        // multi-char literals take the last char's value (like most compilers)
        push("num", s.charCodeAt(s.length - 1), { text: "'" + s + "'" });
        i = j + 1;
        continue;
      }

      // punctuators (longest match first)
      let matched = null;
      for (const p of PUNCTS) {
        if (src.startsWith(p, i)) { matched = p; break; }
      }
      if (matched) { push("punct", matched); i += matched.length; continue; }

      err("stray character " + JSON.stringify(c) + " in source", line);
    }
    push("eof", "", { line });
    return toks;
  }

  function readEscape(src, i, line) {
    // src[i] is the backslash; returns {text, next}
    const c = src[i + 1];
    const simple = { n: "\n", t: "\t", r: "\r", "0": "\0", "\\": "\\", '"': '"', "'": "'", a: "\x07", b: "\b", f: "\f", v: "\v", "?": "?" };
    if (c in simple) return { text: simple[c], next: i + 2 };
    if (c === "x") {
      let j = i + 2, hex = "";
      while (j < src.length && /[0-9a-fA-F]/.test(src[j])) hex += src[j++];
      if (!hex) err("bad \\x escape", line);
      return { text: String.fromCharCode(parseInt(hex, 16)), next: j };
    }
    if (/[0-7]/.test(c)) {
      let j = i + 1, oct = "";
      while (j < src.length && /[0-7]/.test(src[j]) && oct.length < 3) oct += src[j++];
      return { text: String.fromCharCode(parseInt(oct, 8)), next: j };
    }
    if (c === "u" || c === "U") {
      err("universal character escapes (\\u/\\U) are not supported in the sandbox", line);
    }
    err("unknown escape sequence \\" + c, line);
  }

  /* =============================== parser =============================== */

  /* Types are plain objects:
     {k:'int', size, signed, name} | {k:'float', size, name} | {k:'void'}
     {k:'ptr', to} | {k:'arr', of, n} | {k:'fn', ret, params, variadic}
     {k:'rec', tag, name, fields, size, align, complete} | {k:'enumT', name}
     `const` rides along as .const = true on any type. */

  const PENDING = { k: "pending" }; // placeholder inside nested declarators

  function makeParser(toks, unit, seedTypedefs, cppMode) {
    let p = 0;
    const typedefs = Object.assign({}, seedTypedefs || {});   // name -> type

    function peek(o) { return toks[p + (o || 0)]; }
    function next() { return toks[p++]; }
    function atPunct(v, o) { const t = peek(o || 0); return t.k === "punct" && t.v === v; }
    function atKw(v, o) { const t = peek(o || 0); return t.k === "kw" && t.v === v; }
    function expectPunct(v) {
      const t = next();
      if (t.k !== "punct" || t.v !== v) err("expected '" + v + "' but found " +
        (t.k === "eof" ? "end of file" : "'" + (t.text || t.v) + "'"), t.line);
      return t;
    }
    function expectId(what) {
      const t = next();
      if (t.k !== "id") err("expected " + (what || "identifier") + " but found " +
        (t.k === "eof" ? "end of file" : "'" + (t.text || t.v) + "'"), t.line);
      return t.v;
    }
    function line() { return peek().line; }

    /* ---------- type specifiers ---------- */

    function isTypeStart(t) {
      if (t.k === "kw") {
        return ["void", "char", "short", "int", "long", "float", "double",
          "signed", "unsigned", "_Bool", "struct", "union", "enum",
          "const", "volatile", "static", "extern", "register", "inline",
          "restrict", "typedef", "_Complex", "_Alignas", "_Noreturn",
          "_Thread_local", "auto", "constexpr"].indexOf(t.v) !== -1;
      }
      if (t.k === "id") {
        if (typedefs[t.v] !== undefined) return true;
        // std::array<...> reaches the parser as `array` (std:: stripped)
        if (cppMode && t.v === "array") return true;
        return false;
      }
      return false;
    }

    function parseStructSpec() {
      // 'struct'/'union' already consumed
      const tag = peek().v === "struct" ? "struct" : "union";
      next(); // consume kw again (we peeked before calling)
      let name = null;
      if (peek().k === "id") name = next().v;
      if (!atPunct("{")) {
        if (!name) err("anonymous " + tag + " needs a body", line());
        // a bare reference — or a forward declaration like `struct Node;` —
        // yields the (possibly still incomplete) type
        const ref = unit.findRec(tag, name);
        if (ref) return ref;
        const fresh = { k: "rec", tag, name, fields: [], size: 0, align: 1, complete: false };
        unit.registerRec(fresh);
        return fresh;
      }
      expectPunct("{");
      const rec = unit.findRec(tag, name); // may exist as incomplete forward decl
      const self = rec || { k: "rec", tag, name, fields: [], size: 0, align: 1, complete: false };
      if (!rec) unit.registerRec(self);
      let off = 0, maxAlign = 1;
      while (!atPunct("}")) {
        if (atKw("_Alignas")) { next(); skipParens(); }
        const base = parseDeclSpecifiers();
        do {
          const d = parseDeclarator(base, false);
          if (!d.name) err(tag + " field needs a name", line());
          let bits = null;
          if (atPunct(":")) {
            next();
            bits = evalConstExprForUnit(parseAssignExpr(), "bit-field width");
            if (bits < 0 || bits > typeSize(d.type) * 8) {
              err("bit-field width " + bits + " does not fit in its type", line());
            }
          }
          if (self.fields.some((f) => f.name === d.name)) {
            err("duplicate field " + d.name + " in " + tag, line());
          }
          self.fields.push({ name: d.name, type: d.type, off: -1, bits });
        } while (atPunct(",") && next());
        expectPunct(";");
      }
      expectPunct("}");
      // layout: struct = sequential w/ natural alignment, union = overlay.
      // Bit-fields pack LSB-first within their declared-type storage units
      // (the usual little-endian layout), so offsetof/size match real
      // compilers for the everyday cases taught in the course.
      if (tag === "struct") {
        let bitCarry = -1; // remaining free bits in the current unit
        let carryOff = 0;
        for (const f of self.fields) {
          if (f.bits !== null && f.bits !== undefined) {
            const unitSize = typeSize(f.type);
            const unitAlign = Math.max(1, typeAlign(f.type));
            const unitBits = unitSize * 8;
            if (bitCarry < f.bits) {
              off = Math.ceil(off / unitAlign) * unitAlign;
              carryOff = off;
              off += unitSize;
              bitCarry = unitBits;
              if (unitAlign > maxAlign) maxAlign = unitAlign;
            }
            f.off = carryOff;
            f.bitOff = unitBits - bitCarry;
            f.unitSize = unitSize;
            bitCarry -= f.bits;
            continue;
          }
          bitCarry = -1;
          const al = Math.max(1, typeAlign(f.type));
          off = Math.ceil(off / al) * al;
          f.off = off;
          off += typeSize(f.type);
          if (al > maxAlign) maxAlign = al;
        }
      } else {
        for (const f of self.fields) {
          f.off = 0;
          if (f.bits !== null && f.bits !== undefined) {
            f.bitOff = 0;
            f.unitSize = typeSize(f.type);
          }
          const al = Math.max(1, typeAlign(f.type));
          if (al > maxAlign) maxAlign = al;
          off = Math.max(off, typeSize(f.type));
        }
      }
      self.align = maxAlign;
      self.size = Math.ceil(off / maxAlign) * maxAlign;
      self.complete = true;
      return self;
    }

    function parseEnumSpec() {
      next(); // 'enum'
      let name = null;
      if (peek().k === "id") name = next().v;
      if (!atPunct("{")) {
        if (!name) err("anonymous enum needs a body", line());
        return { k: "enumT", name };
      }
      expectPunct("{");
      let auto = 0;
      do {
        const id = expectId("enumerator");
        if (atPunct("=")) {
          next();
          auto = evalConstExprForUnit(parseAssignExpr(), "enum value");
        }
        unit.consts[id] = { v: auto, line: line() };
        auto++;
      } while (atPunct(",") && next());
      // allow the C99 trailing comma
      expectPunct("}");
      return { k: "enumT", name: name || ("enum@" + line()) };
    }

    function parseDeclSpecifiers() {
      let type = null, sign = null, longCount = 0, shortSeen = false;
      let isFloat = false, isDouble = false, isChar = false, isVoid = false, isBool = false;
      let constSeen = false, volatileSeen = false, staticSeen = false;
      for (;;) {
        const t = peek();
        if (t.k === "kw") {
          switch (t.v) {
            case "const": constSeen = true; next(); continue;
            case "volatile": volatileSeen = true; next(); continue;
            case "static": staticSeen = true; next(); continue;
            case "restrict": case "register": case "extern":
            case "inline": case "auto": case "_Noreturn": case "_Thread_local":
            case "constexpr":
              next(); continue;
            case "_Alignas": next(); skipParens(); continue;
            case "_Complex":
              err("the browser sandbox does not support _Complex; see the "
                  + "Complex Numbers chapter for how it works on a real compiler",
                  t.line);
              break;
            case "void": isVoid = true; next(); continue;
            case "char": isChar = true; next(); continue;
            case "short": shortSeen = true; next(); continue;
            case "int": next(); continue;
            case "long": longCount++; next(); continue;
            case "float": isFloat = true; next(); continue;
            case "double": isDouble = true; next(); continue;
            case "signed": sign = true; next(); continue;
            case "unsigned": sign = false; next(); continue;
            case "_Bool": isBool = true; next(); continue;
            case "struct": case "union": {
              if (type) break;
              type = parseStructSpec(); // consumes the keyword itself
              // in C++ the tag name is itself a type name: Player p;
              if (cppMode && type.k === "rec" && type.name) {
                typedefs[type.name] = type;
              }
              continue;
            }
            case "enum": {
              if (type) break;
              type = parseEnumSpec();
              if (cppMode && type.k === "enumT" && type.name &&
                  type.name.indexOf("enum@") !== 0) {
                typedefs[type.name] = type;
              }
              continue;
            }
          }
          break;
        }
        if (t.k === "id" && !type && typedefs[t.v] !== undefined) {
          type = typedefs[t.v];
          next();
          continue;
        }
        // C++ std::array<ELEM, N> -> a plain C array of N elements
        if (cppMode && !type && t.k === "id" && t.v === "array" &&
            peek(1).k === "punct" && peek(1).v === "<") {
          next(); next(); // 'array' '<'
          const elemT = parseDeclSpecifiers();
          expectPunct(",");
          // the size is a bare integer literal — parsing it as an
          // expression would read `N > var` as a comparison
          const nT = peek();
          if (nT.k !== "num") {
            err("std::array size must be an integer constant", t.line);
          }
          next();
          expectPunct(">");
          type = { k: "arr", of: elemT, n: Math.trunc(nT.v) };
          continue;
        }
        break;
      }
      if (!type) {
        if (isVoid) type = { k: "void" };
        else if (isBool) type = makeInt(1, false, "_Bool");
        else if (isChar) type = makeInt(1, sign !== false, "char");
        else if (shortSeen) type = makeInt(2, sign !== false, "short");
        else if (longCount >= 2 && !isDouble) type = makeInt(8, sign !== false, "long long");
        else if (longCount === 1 && !isDouble) type = makeInt(8, sign !== false, "long");
        else if (longCount === 1 && isDouble) type = { k: "float", size: 8, name: "long double" };
        else if (isDouble) type = { k: "float", size: 8, name: "double" };
        else if (isFloat) type = { k: "float", size: 4, name: "float" };
        else type = makeInt(4, sign !== false, "int");
      }
      if (constSeen) type = Object.assign({}, type, { const: true });
      if (volatileSeen) type = Object.assign({}, type, { volatile: true });
      if (staticSeen) type = Object.assign({}, type, { staticLocal: true });
      return type;
    }

    /* ---------- declarators ---------- */

    function parsePointers(base) {
      while (atPunct("*")) {
        next();
        base = { k: "ptr", to: base };
        while (atKw("const") || atKw("volatile") || atKw("restrict")) {
          if (atKw("const")) base = Object.assign({}, base, { const: true });
          next();
        }
      }
      // C++ references: `int& r` / `int&& r` behave as auto-deref pointers
      while (atPunct("&") || atPunct("&&")) {
        next();
        base = { k: "ref", to: base };
      }
      return base;
    }

    /* C++ range-for range: a braced list becomes an anonymous array
       (compound literal), anything else is evaluated as an expression. */
    function parseRangeExpr(elemType) {
      if (atPunct("{")) {
        const items = parseInitializerList(() => parseAssignExpr())
          .map((e2) => ({ k: "expr", e: e2 }));
        return { x: "compound", type: { k: "arr", of: elemType, n: null },
                 inits: items };
      }
      return parseAssignExpr();
    }

    /* Parse a declarator. Returns {name, type}. If abstract, the name is
       optional and inner parens contain an abstract declarator. */
    function parseDeclarator(base, abstract) {
      base = parsePointers(base);
      return parseDirectDeclarator(base, abstract);
    }

    /* Classic declarator algorithm: parse `*`s over the base type, then an
       optional name or a parenthesised nested declarator, then array /
       function suffixes applied to the base, and finally substitute the
       suffixed type into the nested declarator's PENDING slot. This gives
       C's inside-out reading for free: `int (*fp)(int)` is a pointer to a
       function, `int *a[3]` is an array of pointers. */
    function parseDirectDeclarator(base, abstract) {
      let name = null, inner = null;

      if (peek().k === "id") {
        name = next().v;
      } else if (atPunct("(") && declaratorAhead()) {
        next();
        inner = parseDeclarator(PENDING, abstract);
        expectPunct(")");
      }

      const suffixes = [];
      for (;;) {
        if (atPunct("[")) {
          next();
          let n = null, vlaExpr = null;
          if (!atPunct("]")) {
            const e = parseAssignExpr();
            if (e.x === "num") n = Math.trunc(e.v);
            else vlaExpr = e; // VLA — size evaluated at runtime
          }
          expectPunct("]");
          suffixes.push({ kind: "arr", n, vla: vlaExpr });
        } else if (atPunct("(")) {
          next();
          const params = [];
          let variadic = false;
          if (atKw("void") && atPunct(")", 1)) { next(); }
          else if (!atPunct(")")) {
            do {
              if (atPunct("...")) { next(); variadic = true; break; }
              const pb = parseDeclSpecifiers();
              const pd = parseDeclarator(pb, true);
              params.push({ name: pd.name, type: pd.type });
            } while (atPunct(",") && next());
          }
          expectPunct(")");
          suffixes.push({ kind: "fn", params, variadic });
        } else break;
      }
      /* the FIRST suffix after the identifier is the OUTERMOST array
         dimension: int m[2][3] is "array 2 of array 3 of int" — so the
         suffixes wrap around the base in reverse collection order */
      let type = base;
      for (let i = suffixes.length - 1; i >= 0; i--) {
        const sfx = suffixes[i];
        if (sfx.kind === "arr") {
          type = { k: "arr", of: type, n: sfx.n };
          if (sfx.vla) type.vlaExpr = sfx.vla;
        } else {
          type = { k: "fn", ret: type, params: sfx.params, variadic: sfx.variadic };
        }
      }

      if (inner) {
        type = substituteType(inner.type, PENDING, type);
        name = name || inner.name;
      }
      return { name, type };

      function declaratorAhead() {
        // '(' starts a nested declarator if the next token is id, '*' or '('
        const t = peek(1);
        return t.k === "id" || (t.k === "punct" && (t.v === "*" || t.v === "("));
      }
    }

    function substituteType(type, pending, repl) {
      if (type === pending) return repl;
      if (type && type.k === "ptr") {
        return { k: "ptr", to: substituteType(type.to, pending, repl),
                 const: type.const, cppstr: type.cppstr };
      }
      if (type && type.k === "ref") {
        return { k: "ref", to: substituteType(type.to, pending, repl),
                 const: type.const };
      }
      if (type && type.k === "arr") return { k: "arr", of: substituteType(type.of, pending, repl), n: type.n, vlaExpr: type.vlaExpr };
      if (type && type.k === "fn") {
        return {
          k: "fn", ret: substituteType(type.ret, pending, repl),
          params: type.params, variadic: type.variadic,
        };
      }
      return type;
    }

    /* ---------- initializers ---------- */

    function parseInitializerList(elemFn) {
      expectPunct("{");
      const items = [];
      if (!atPunct("}")) {
        do {
          if (atPunct("}")) break; // trailing comma
          items.push(elemFn());
        } while (atPunct(",") && next());
      }
      expectPunct("}");
      return items;
    }

    function parseInitializer(type) {
      if (type && type.k === "arr" && type.of && type.of.k === "int" &&
          type.of.size === 1 && peek().k === "str") {
        return { k: "str", s: next().v };
      }
      if (atPunct("{")) {
        return parseInitializerList(() => parseInitializer(null));
      }
      return { k: "expr", e: parseAssignExpr() };
    }

    /* ---------- declarations ---------- */

    function parseDeclaration(allowFuncDef) {
      // returns {kind:'func', decl} | {kind:'vars', items} | null (just ';')
      const base = parseDeclSpecifiers();
      if (atPunct(";")) { next(); return { kind: "vars", items: [] }; }
      const first = parseDeclarator(base, false);
      if (first.type.k === "fn" && atPunct("{") && allowFuncDef) {
        const body = parseBlock();
        return { kind: "func", name: first.name, type: first.type, body };
      }
      const items = [{ name: first.name, type: first.type, init: parseOptInit(first.type) }];
      while (atPunct(",") && next()) {
        const d = parseDeclarator(base, false);
        items.push({ name: d.name, type: d.type, init: parseOptInit(d.type) });
      }
      expectPunct(";");
      // infer implicit array sizes from their initializers: int a[] = {...}
      for (const it of items) {
        if (it.type && it.type.k === "arr" && it.type.n === null && !it.type.vlaExpr) {
          const initItems = Array.isArray(it.init) ? it.init
            : (it.init && it.init.items);
          if (it.init && it.init.k === "str") {
            it.type = Object.assign({}, it.type, { n: it.init.s.length + 1 });
          } else if (initItems) {
            it.type = Object.assign({}, it.type, { n: initItems.length });
          }
        }
      }
      return { kind: "vars", items };
    }

    function parseOptInit(type) {
      if (atPunct("=")) {
        next();
        return parseInitializer(type);
      }
      // C++ brace initialization: Player p{"Mage", 50};
      if (atPunct("{") && !(type && type.k === "fn")) {
        return parseInitializer(type);
      }
      return null;
    }

    function parseTypedef() {
      next(); // 'typedef'
      const base = parseDeclSpecifiers();
      do {
        const d = parseDeclarator(base, false);
        if (!d.name) err("typedef needs a name", line());
        typedefs[d.name] = d.type;
      } while (atPunct(",") && next());
      expectPunct(";");
    }

    /* ---------- statements ---------- */

    function parseBlock() {
      expectPunct("{");
      const stmts = [];
      while (!atPunct("}")) {
        if (peek().k === "eof") err("missing '}' — unexpected end of file", line());
        stmts.push(parseStatement());
      }
      expectPunct("}");
      return { x: "block", stmts };
    }

    function parseStatement() {
      const t = peek();
      if (t.k === "punct" && t.v === "{") return parseBlock();
      if (t.k === "kw") {
        switch (t.v) {
          case "if": {
            next(); expectPunct("(");
            const c = parseExpr();
            expectPunct(")");
            const then = parseStatement();
            let els = null;
            if (atKw("else")) { next(); els = parseStatement(); }
            return { x: "if", c, then, els, line: t.line };
          }
          case "while": {
            next(); expectPunct("(");
            const c = parseExpr();
            expectPunct(")");
            return { x: "while", c, body: parseStatement(), line: t.line };
          }
          case "do": {
            next();
            const body = parseStatement();
            if (!atKw("while")) err("do loop needs while", t.line);
            next(); expectPunct("(");
            const c = parseExpr();
            expectPunct(")"); expectPunct(";");
            return { x: "do", body, c, line: t.line };
          }
          case "for": {
            next(); expectPunct("(");
            let init = null;
            if (!atPunct(";")) {
              if (isTypeStart(peek())) {
                // C++ range-based for: for (T x : range) body
                const base = parseDeclSpecifiers();
                const d = parseDeclarator(base, false);
                if (cppMode && d.name && atPunct(":")) {
                  next(); // ':'
                  const range = parseRangeExpr(d.type);
                  expectPunct(")");
                  return { x: "rangeFor", varName: d.name, varType: d.type,
                           range, body: parseStatement(), line: t.line };
                }
                const items = [{ name: d.name, type: d.type, init: parseOptInit(d.type) }];
                while (atPunct(",") && next()) {
                  const d2 = parseDeclarator(base, false);
                  items.push({ name: d2.name, type: d2.type, init: parseOptInit(d2.type) });
                }
                expectPunct(";");
                init = { x: "decl", items, line: t.line };
              } else { init = { x: "expr", e: parseExpr() }; expectPunct(";"); }
            } else next();
            let c = null;
            if (!atPunct(";")) c = parseExpr();
            expectPunct(";");
            let step = null;
            if (!atPunct(")")) step = parseExpr();
            expectPunct(")");
            return { x: "for", init, c, step, body: parseStatement(), line: t.line };
          }
          case "switch": {
            next(); expectPunct("(");
            const ctrl = parseExpr();
            expectPunct(")");
            const body = parseStatement();
            return { x: "switch", ctrl, body, line: t.line };
          }
          case "case": {
            next();
            const v = parseAssignExpr();
            if (atPunct("...")) { next(); parseAssignExpr(); err("case ranges are a GNU extension and are not supported", t.line); }
            expectPunct(":");
            return { x: "case", v, line: t.line };
          }
          case "default": {
            next(); expectPunct(":");
            return { x: "case", v: null, line: t.line };
          }
          case "break": next(); expectPunct(";"); return { x: "break", line: t.line };
          case "continue": next(); expectPunct(";"); return { x: "continue", line: t.line };
          case "return": {
            next();
            let e = null;
            if (!atPunct(";")) e = parseExpr();
            expectPunct(";");
            return { x: "return", e, line: t.line };
          }
          case "goto": {
            next();
            const name = expectId("label");
            expectPunct(";");
            return { x: "goto", name, line: t.line };
          }
          case "typedef": parseTypedef(); return { x: "nop" };
        }
      }
      if (t.k === "id" && peek(1).k === "punct" && peek(1).v === ":" &&
          !(typedefs[t.v] !== undefined)) {
        const name = next().v;
        next(); // ':'
        return { x: "label", name, line: t.line };
      }
      if (t.k === "punct" && t.v === ";") { next(); return { x: "nop" }; }
      if (isTypeStart(t)) {
        const d = parseDeclaration(false);
        return { x: "decl", items: d.items, line: t.line };
      }
      const e = parseExpr();
      expectPunct(";");
      return { x: "expr", e, line: t.line };
    }

    /* ---------- expressions ---------- */

    function parseExpr() {
      let e = parseAssignExpr();
      while (atPunct(",")) { next(); e = { x: "comma", l: e, r: parseAssignExpr() }; }
      return e;
    }

    function parseAssignExpr() {
      const lhs = parseTernary();
      const t = peek();
      if (t.k === "punct" && ["=", "+=", "-=", "*=", "/=", "%=", "<<=", ">>=", "&=", "|=", "^="].indexOf(t.v) !== -1) {
        next();
        return { x: "assign", op: t.v, l: lhs, r: parseAssignExpr(), line: t.line };
      }
      return lhs;
    }

    function parseTernary() {
      const c = parseBinary(0);
      if (atPunct("?")) {
        next();
        const a = parseAssignExpr();
        expectPunct(":");
        return { x: "cond", c, a, b: parseAssignExpr(), line: peek().line };
      }
      return c;
    }

    const BIN_LEVELS = [
      ["||"], ["&&"], ["|"], ["^"], ["&"],
      ["==", "!="], ["<", ">", "<=", ">="], ["<<", ">>"],
      ["+", "-"], ["*", "/", "%"],
    ];

    function parseBinary(level) {
      if (level >= BIN_LEVELS.length) return parseUnary();
      let l = parseBinary(level + 1);
      for (;;) {
        const t = peek();
        if (t.k === "punct" && BIN_LEVELS[level].indexOf(t.v) !== -1) {
          next();
          l = { x: "bin", op: t.v, l, r: parseBinary(level + 1), line: t.line };
        } else return l;
      }
    }

    function parseUnary() {
      const t = peek();
      if (t.k === "punct") {
        if (t.v === "++" || t.v === "--") {
          next();
          return { x: "un", op: t.v, e: parseUnary(), line: t.line };
        }
        if (t.v === "&" || t.v === "*" || t.v === "+" || t.v === "-" || t.v === "!" || t.v === "~") {
          next();
          return { x: "un", op: t.v, e: parseUnary(), line: t.line };
        }
        if (t.v === "(") {
          // could be a cast: ( type ) expr
          const save = p;
          next();
          if (isTypeStart(peek())) {
            const type = parseTypeName();
            expectPunct(")");
            if (atPunct("{")) {
              // compound literal: (type){...}
              const inits = parseInitializerList(() => parseInitializer(null));
              return { x: "compound", type, inits, line: t.line };
            }
            return { x: "cast", type, e: parseUnary(), line: t.line };
          }
          p = save; // not a cast
        }
      }
      if (t.k === "kw") {
        if (t.v === "sizeof") {
          next();
          if (atPunct("(") && isTypeStart(peek(1))) {
            next();
            const type = parseTypeName();
            expectPunct(")");
            return { x: "sizeofT", type, line: t.line };
          }
          const e = parseUnary();
          return { x: "sizeofE", e, line: t.line };
        }
        if (t.v === "_Generic") {
          next(); expectPunct("(");
          const ctrl = parseAssignExpr();
          const cases = [];
          while (atPunct(",") && next()) {
            if (atKw("default")) { next(); expectPunct(":"); cases.push({ type: null, e: parseAssignExpr() }); }
            else {
              const ty = parseTypeName();
              expectPunct(":");
              cases.push({ type: ty, e: parseAssignExpr() });
            }
          }
          expectPunct(")");
          if (!cases.length) err("_Generic needs at least one association", t.line);
          return { x: "generic", ctrl, cases, line: t.line };
        }
      }
      return parsePostfix();
    }

    function parseTypeName() {
      const base = parseDeclSpecifiers();
      const d = parseDeclarator(base, true);
      return d.type;
    }

    function parsePostfix() {
      let e = parsePrimary();
      // C concatenates adjacent string literals: "abc" "def"
      while (peek().k === "str") {
        e = { x: "str", s: e.s + next().v, line: e.line };
      }
      for (;;) {
        const t = peek();
        if (t.k !== "punct") return e;
        if (t.v === "(") {
          next();
          const args = [];
          if (!atPunct(")")) {
            do { args.push(parseAssignExpr()); } while (atPunct(",") && next());
          }
          expectPunct(")");
          e = { x: "call", fn: e, args, line: t.line };
        } else if (t.v === "[") {
          next();
          const idx = parseExpr();
          expectPunct("]");
          e = { x: "index", arr: e, idx, line: t.line };
        } else if (t.v === ".") {
          next();
          e = { x: "member", obj: e, name: expectId("struct member"), arrow: false, line: t.line };
        } else if (t.v === "->") {
          next();
          e = { x: "member", obj: e, name: expectId("struct member"), arrow: true, line: t.line };
        } else if (t.v === "++" || t.v === "--") {
          next();
          e = { x: "post", op: t.v, e, line: t.line };
        } else return e;
      }
    }

    function parsePrimary() {
      const t = next();
      if (t.k === "num") return { x: "num", v: t.v, isFloat: !!t.isFloat, line: t.line };
      if (t.k === "str") return { x: "str", s: t.v, line: t.line };
      if (t.k === "id") return { x: "id", name: t.v, line: t.line };
      if (t.k === "kw" && t.v === "_Bool") err("unexpected _Bool", t.line);
      if (t.k === "punct" && t.v === "(") {
        const e = parseExpr();
        expectPunct(")");
        return e;
      }
      err("unexpected " + (t.k === "eof" ? "end of file" : "'" + (t.text || t.v) + "'"), t.line);
    }

    function skipParens() {
      expectPunct("(");
      let depth = 1;
      while (depth) {
        const t = next();
        if (t.k === "eof") err("unbalanced parentheses", t.line);
        if (t.k === "punct" && t.v === "(") depth++;
        if (t.k === "punct" && t.v === ")") depth--;
      }
    }

    /* Constant folding for enum values, case labels, global initializers,
       and static array sizes. Returns a JS number (or string address via
       cb hook for globals — handled by the interpreter instead). */
    function evalConstExprForUnit(e, what) {
      switch (e.x) {
        case "num": return e.v;
        case "un": {
          const v = evalConstExprForUnit(e.e, what);
          switch (e.op) {
            case "-": return -v;
            case "+": return v;
            case "~": return ~v;
            case "!": return v ? 0 : 1;
          }
          break;
        }
        case "bin": {
          const a = evalConstExprForUnit(e.l, what), b = evalConstExprForUnit(e.r, what);
          switch (e.op) {
            case "+": return a + b; case "-": return a - b;
            case "*": return a * b;
            case "/": return Math.trunc(a / b);
            case "%": return a % b;
            case "<<": return a << b; case ">>": return a >> b;
            case "&": return a & b; case "|": return a | b; case "^": return a ^ b;
            case "==": return a === b ? 1 : 0; case "!=": return a !== b ? 1 : 0;
            case "<": return a < b ? 1 : 0; case ">": return a > b ? 1 : 0;
            case "<=": return a <= b ? 1 : 0; case ">=": return a >= b ? 1 : 0;
            case "&&": return a && b ? 1 : 0; case "||": return a || b ? 1 : 0;
          }
          break;
        }
        case "cond": return evalConstExprForUnit(e.c, what)
          ? evalConstExprForUnit(e.a, what) : evalConstExprForUnit(e.b, what);
        case "cast": return evalConstExprForUnit(e.e, what);
        case "comma": return evalConstExprForUnit(e.r, what);
        case "id":
          if (unit.consts[e.name]) return unit.consts[e.name].v;
          err(what + " must be a constant (" + e.name + " is not)", e.line || line());
          break;
        case "sizeofT": return typeSizeComplete(e.type);
        case "sizeofE": err(what + ": sizeof of an expression is not constant-folded here", e.line); break;
      }
      err(what + " must be a compile-time constant", e.line || line());
    }

    return {
      parseUnit() {
        const funcs = [];
        while (peek().k !== "eof") {
          if (atKw("typedef")) { parseTypedef(); continue; }
          if (atPunct(";")) { next(); continue; }
          const d = parseDeclaration(true);
          if (d.kind === "func") funcs.push(d);
          else if (d.items.length) unit.globals.push(d.items);
        }
        return { funcs, typedefs };
    },
    };
  }

  /* ============================ type helpers ============================ */

  function makeInt(size, signed, name) {
    return { k: "int", size, signed: !!signed, name: name || (size === 4 ? "int" : "int" + size * 8 + "_t") };
  }
  const T_CHAR = () => makeInt(1, true, "char");
  const T_UCHAR = () => makeInt(1, false, "unsigned char");
  const T_INT = () => makeInt(4, true, "int");
  const T_UINT = () => makeInt(4, false, "unsigned int");
  const T_LONG = () => makeInt(8, true, "long");
  const T_ULONG = () => makeInt(8, false, "unsigned long");
  const T_LLONG = () => makeInt(8, true, "long long");
  const T_ULLONG = () => makeInt(8, false, "unsigned long long");
  const T_SHORT = () => makeInt(2, true, "short");
  const T_USHORT = () => makeInt(2, false, "unsigned short");
  const T_FLOAT = () => ({ k: "float", size: 4, name: "float" });
  const T_DOUBLE = () => ({ k: "float", size: 8, name: "double" });
  const T_VOID = () => ({ k: "void" });
  const T_VOIDPTR = () => ({ k: "ptr", to: { k: "void" } });
  const T_SIZET = () => makeInt(8, false, "size_t");

  /* C++ layer types: `string` is a char* tagged cppstr; cout/endl/cin are
     singleton marker types intercepted in binaryValue(). */
  const T_CPPSTR = () => ({ k: "ptr", to: T_CHAR(), cppstr: true });
  const T_COUT = () => ({ k: "cout" });
  const T_ENDL = () => ({ k: "endl" });
  const T_CIN = () => ({ k: "cin" });
  function isCppStr(t) { return !!t && t.cppstr === true; }

  function typeAlign(t) {
    switch (t.k) {
      case "int": return t.size;
      case "float": return Math.min(t.size, 8);
      case "void": return 1;
      case "ptr": return 8;
      case "ref": return 8;
      case "arr": return typeAlign(t.of);
      case "rec": return t.complete ? t.align : err("sizeof of incomplete type " + recName(t));
      case "fn": return 8;
      case "enumT": return 4;
      default: return 1;
    }
  }

  function typeSize(t) {
    switch (t.k) {
      case "int": return t.size;
      case "float": return t.size;
      case "void": return err("sizeof of void is not valid C");
      case "ptr": return 8;
      case "ref": return 8;
      case "enumT": return 4;
      case "fn": return 8;
      case "arr":
        if (t.vlaExpr) err("size of a variable-length array is not a constant");
        if (t.n === null) err("sizeof of an incomplete array (flexible/unknown size)");
        return t.n * typeSize(t.of);
      case "rec":
        if (!t.complete) err("invalid use of incomplete type " + recName(t));
        return t.size;
      default: return 1;
    }
  }

  function recName(t) {
    return (t.tag === "struct" ? "struct " : "union ") + (t.name || "<anonymous>");
  }

  function isIntType(t) { return t.k === "int" || t.k === "enumT"; }
  function isFloatType(t) { return t.k === "float"; }
  function isArith(t) { return isIntType(t) || isFloatType(t); }
  function isPtr(t) { return t.k === "ptr"; }
  function isFnPtr(t) { return isPtr(t) && t.to && t.to.k === "fn"; }

  /* C integer ranks: char < short < int < long < long long */
  function intRank(t) {
    if (t.k === "enumT") return 2;
    if (t.size === 1) return 1;
    if (t.size === 2) return 2;
    if (t.size === 4) return 3;
    return 4;
  }

  /* usual arithmetic conversions — returns the common type of a binary op */
  function usualArith(a, b) {
    if (isFloatType(a) || isFloatType(b)) {
      if (a.size === 8 || b.size === 8) return T_DOUBLE();
      return T_FLOAT();
    }
    // integer promotion first
    let ia = intRank(a) < 3 ? T_INT() : a;
    let ib = intRank(b) < 3 ? T_INT() : b;
    if (intRank(ia) === intRank(ib)) {
      const signed = ia.signed && ib.signed;
      return makeInt(ia.size, signed, ia.name);
    }
    const big = intRank(ia) > intRank(ib) ? ia : ib;
    const small = intRank(ia) > intRank(ib) ? ib : ia;
    if (big.size > small.size) {
      // the bigger type can represent all of the smaller one unless an
      // unsigned of the bigger rank meets a signed of the same rank... the
      // practical rule for teaching: if either is unsigned at the bigger
      // size, the result is unsigned
      return makeInt(big.size, big.signed && small.signed, big.name);
    }
    return big.signed ? big : makeInt(big.size, false, big.name);
  }

  /* =============================== memory =============================== */

  class Mem {
    constructor(bytes) {
      this.bytes = bytes || new Uint8Array(1 << 20);
      this.dv = new DataView(this.bytes.buffer);
      this.high = 0; // highest written byte (for wild-pointer detection)
    }
    ensure(addr, len) {
      if (addr < 0) rerr("invalid memory access (negative address)");
      if (addr + len > this.bytes.length) {
        let size = this.bytes.length;
        while (size < addr + len) size *= 2;
        const nb = new Uint8Array(size);
        nb.set(this.bytes);
        this.bytes = nb;
        this.dv = new DataView(nb.buffer);
      }
      if (addr + len > this.high) this.high = addr + len;
    }
    i8(a, v) { this.ensure(a, 1); if (v === undefined) return this.dv.getInt8(a); this.dv.setInt8(a, v); }
    u8(a, v) { this.ensure(a, 1); if (v === undefined) return this.dv.getUint8(a); this.dv.setUint8(a, v); }
    i16(a, v) { this.ensure(a, 2); if (v === undefined) return this.dv.getInt16(a, true); this.dv.setInt16(a, v, true); }
    u16(a, v) { this.ensure(a, 2); if (v === undefined) return this.dv.getUint16(a, true); this.dv.setUint16(a, v, true); }
    i32(a, v) { this.ensure(a, 4); if (v === undefined) return this.dv.getInt32(a, true); this.dv.setInt32(a, v, true); }
    u32(a, v) { this.ensure(a, 4); if (v === undefined) return this.dv.getUint32(a, true); this.dv.setUint32(a, v, true); }
    i64(a, v) { this.ensure(a, 8); if (v === undefined) return this.dv.getBigInt64(a, true); this.dv.setBigInt64(a, v, true); }
    f32(a, v) { this.ensure(a, 4); if (v === undefined) return this.dv.getFloat32(a, true); this.dv.setFloat32(a, v, true); }
    f64(a, v) { this.ensure(a, 8); if (v === undefined) return this.dv.getFloat64(a, true); this.dv.setFloat64(a, v, true); }
    getBytes(a, len) { this.ensure(a, len); return this.bytes.slice(a, a + len); }
    setBytes(a, bytes) { this.ensure(a, bytes.length); this.bytes.set(bytes, a); }
  }

  /* read/write a C value of type t at address a */
  function memRead(mem, a, t) {
    if (!isArith(t) && !isPtr(t)) return a; // rec/arr: value is its address
    if (isPtr(t)) return Number(mem.i64(a));
    if (isFloatType(t)) return t.size === 4 ? mem.f32(a) : mem.f64(a);
    switch (t.size) {
      case 1: return t.signed ? mem.i8(a) : mem.u8(a);
      case 2: return t.signed ? mem.i16(a) : mem.u16(a);
      case 4: return t.signed ? mem.i32(a) : mem.u32(a);
      default: return Number(mem.i64(a));
    }
  }

  function wrapInt(v, t) {
    v = Math.trunc(v);
    if (!isFinite(v)) return 0;
    if (t.size === 8) {
      // NOTE: ((v % 2^64) + 2^64) % 2^64 is WRONG in JS doubles — 2^64 + a
      // small value rounds back to 2^64 (spacing at 2^64 is 4096), turning
      // every small wrap into 0. Keep v in (-2^64, 2^64) with single ops.
      const TWO64 = 18446744073709551616;
      const TWO63 = 9223372036854775808;
      v = v % TWO64;
      if (v >= TWO63) v -= TWO64;
      else if (v < -TWO63) v = v + TWO64; // exact: both operands are huge
      return v; // signed representation
    }
    if (t.size === 4) return t.signed ? (v | 0) : (v >>> 0);
    if (t.size === 2) { v &= 0xffff; return t.signed ? (v << 16) >> 16 : v; }
    v &= 0xff;
    return t.signed ? (v << 24) >> 24 : v;
  }

  function memWrite(mem, a, v, t) {
    if (isFloatType(t)) {
      if (t.size === 4) mem.f32(a, v); else mem.f64(a, v);
      return;
    }
    if (isPtr(t)) { mem.i64(a, BigInt(Math.trunc(v) || 0)); return; }
    v = wrapInt(v, t);
    switch (t.size) {
      case 1: mem.u8(a, v & 0xff); break;
      case 2: mem.u16(a, v & 0xffff); break;
      case 4: mem.u32(a, v >>> 0); break;
      default: mem.i64(a, BigInt(Math.trunc(v) || 0)); break;
    }
  }

  /* ============================ interpreter ============================= */

  const FN_BASE = 0x40000000;   // function-pointer addresses live here
  const STACK_TOP = 0x02000000; // 32 MB in: the stack grows down from here
  const STACK_LIMIT = 0x01000000; // 16 MB: heap may not grow past this

  function createInterp(source, opts) {
    const input = (opts && opts.input) || "";
    const maxSteps = (opts && opts.maxSteps) || 40000000;
    const mem = new Mem();
    const out = { text: "" };
    let errnoAddr = 0; // allocated once the heap helpers exist
    let stdinPos = 0;
    let steps = 0;
    let sp = STACK_TOP;
    let heapPtr = STACK_LIMIT; // grows up, adjusted after globals
    let fnCount = 0;
    const funcs = {};        // name -> {decl, fnAddr}
    const overloads = {};    // C++: name -> [{key, params}] in definition order
    const fnByAddr = {};     // fnAddr -> {decl|builtin}
    const literals = {};     // deduped string literal -> address
    let roPtr = 16;
    const files = {};        // address -> file record
    let nextFileAddr = 0x30000000;
    const atexitFns = [];
    const jmpTargets = {};   // buf address -> token
    let jmpTokenSeq = 1;
    let exitCode = 0;
    const staticSlots = new WeakMap(); // decl item -> persistent slot

    const unit = {
      recs: {},   // "struct X" -> rec
      consts: {}, // enum constants + injected macros-as-constants
      globals: [],
      findRec(tag, name) { return this.recs[tag + " " + name] || null; },
      registerRec(rec) { this.recs[rec.tag + " " + rec.name] = rec; },
    };

    /* ---------------- program loading ---------------- */

      const headers = {};
      let macroText;
      const cppMode = isCppSource(source);
      const lowered = cppMode ? lowerCppSource(source) : source;
      try {
        const pre = preprocess(lowered, cppMode);
        macroText = pre.text;
        pre.headers.forEach((h) => { headers[h] = 1; });
      } catch (e) {
      if (e instanceof CErr) throw e;
      throw new CErr(String(e && e.message || e), 0, "compile");
    }

    // inject typedefs/constants that real system headers would provide
    const parserTypedefs = {};
    function seedTypedefsForHeaders() {
      const add = (name, t) => { parserTypedefs[name] = t; };
      const anyOf = ["stdio.h", "stdlib.h", "string.h", "stddef.h", "time.h",
        "locale.h", "setjmp.h", "stdint.h", "inttypes.h", "unistd.h"];
      if (anyOf.some((h) => headers[h])) {
        add("size_t", T_ULONG());
        add("ptrdiff_t", T_LONG());
        add("ssize_t", T_LONG());
        add("wchar_t", T_INT());
      }
      if (headers["stdint.h"] || headers["inttypes.h"]) {
        add("int8_t", T_CHAR()); add("int16_t", T_SHORT());
        add("int32_t", T_INT()); add("int64_t", T_LLONG());
        add("uint8_t", T_UCHAR()); add("uint16_t", T_USHORT());
        add("uint32_t", T_UINT()); add("uint64_t", T_ULLONG());
        add("intptr_t", T_LONG()); add("uintptr_t", T_ULONG());
        add("intmax_t", T_LLONG()); add("uintmax_t", T_ULLONG());
      }
      if (headers["time.h"]) {
        add("time_t", T_LONG()); add("clock_t", T_LONG());
      }
      if (headers["setjmp.h"]) {
        // jmp_buf is opaque; setjmp() just remembers the buffer's address
        add("jmp_buf", { k: "arr", of: T_LONG(), n: 32 });
      }
      if (headers["stdbool.h"]) {
        add("bool", makeInt(1, false, "_Bool"));
        unit.consts["true"] = { v: 1 };
        unit.consts["false"] = { v: 0 };
      }
      if (headers["stdio.h"] || headers["unistd.h"]) {
        // FILE is an opaque incomplete type — only FILE* is ever used
        if (!unit.findRec("struct", "FILE")) {
          unit.registerRec({ k: "rec", tag: "struct", name: "FILE",
            fields: [], size: 0, align: 1, complete: false });
        }
        add("FILE", unit.findRec("struct", "FILE"));
      }
      if (headers["time.h"]) {
        const tm = { k: "rec", tag: "struct", name: "tm", fields: [], size: 0, align: 4, complete: true };
        ["tm_sec", "tm_min", "tm_hour", "tm_mday", "tm_mon", "tm_year",
         "tm_wday", "tm_yday", "tm_isdst"].forEach((n, i) => {
          tm.fields.push({ name: n, type: T_INT(), off: i * 4 });
        });
        tm.size = 36;
        unit.registerRec(tm);
        add("struct tm", tm); // allow `struct tm` written as a typedef name too
        const ts = { k: "rec", tag: "struct", name: "timespec", fields: [], size: 0, align: 8, complete: true };
        ts.fields.push({ name: "tv_sec", type: T_LONG(), off: 0 });
        ts.fields.push({ name: "tv_nsec", type: T_LONG(), off: 8 });
        ts.size = 16;
        unit.registerRec(ts);
      }
      if (headers["locale.h"]) {
        const lc = { k: "rec", tag: "struct", name: "lconv", fields: [], size: 0, align: 8, complete: true };
        ["decimal_point", "thousands_sep", "grouping", "int_curr_symbol",
         "currency_symbol", "mon_decimal_point", "mon_thousands_sep",
         "positive_sign", "negative_sign"].forEach((n, i) => {
          lc.fields.push({ name: n, type: { k: "ptr", to: T_CHAR() }, off: i * 8 });
        });
        lc.size = 72;
        unit.registerRec(lc);
      }
    }
    seedTypedefsForHeaders();

    // the C++ layer: a `string` type (a tagged char*), plus true/false
    if (cppMode) {
      parserTypedefs["string"] = T_CPPSTR();
      unit.consts["true"] = { v: 1 };
      unit.consts["false"] = { v: 0 };
    }

    // numeric constants from headers
    function seedConstsForHeaders() {
      const C = unit.consts;
      if (headers["stdio.h"]) {
        C["EOF"] = { v: -1 };
        C["SEEK_SET"] = { v: 0 }; C["SEEK_CUR"] = { v: 1 }; C["SEEK_END"] = { v: 2 };
        C["BUFSIZ"] = { v: 1024 };
      }
      if (headers["stdlib.h"]) {
        C["EXIT_SUCCESS"] = { v: 0 }; C["EXIT_FAILURE"] = { v: 1 };
        C["RAND_MAX"] = { v: 2147483647 };
      }
      if (headers["limits.h"]) {
        C["CHAR_BIT"] = { v: 8 };
        C["SCHAR_MIN"] = { v: -128 }; C["SCHAR_MAX"] = { v: 127 };
        C["UCHAR_MAX"] = { v: 255 };
        C["CHAR_MIN"] = { v: -128 }; C["CHAR_MAX"] = { v: 127 };
        C["SHRT_MIN"] = { v: -32768 }; C["SHRT_MAX"] = { v: 32767 };
        C["USHRT_MAX"] = { v: 65535 };
        C["INT_MIN"] = { v: -2147483648 }; C["INT_MAX"] = { v: 2147483647 };
        C["UINT_MAX"] = { v: 4294967295 };
        C["LONG_MIN"] = { v: -9223372036854775808 };
        C["LONG_MAX"] = { v: 9223372036854775807 };
        C["ULONG_MAX"] = { v: 18446744073709551615 };
      }
      if (headers["math.h"]) {
        C["M_PI"] = { v: Math.PI }; C["M_E"] = { v: Math.E };
        C["M_SQRT2"] = { v: Math.SQRT2 }; C["M_LN2"] = { v: Math.LN2 };
        C["M_LN10"] = { v: Math.LN10 };
      }
      if (headers["float.h"]) {
        C["FLT_MAX"] = { v: 3.4028234663852886e+38 };
        C["FLT_MIN"] = { v: 1.1754943508222875e-38 };
        C["DBL_MAX"] = { v: Number.MAX_VALUE };
        C["DBL_MIN"] = { v: Number.MIN_VALUE };
        C["FLT_DIG"] = { v: 6 }; C["DBL_DIG"] = { v: 15 };
      }
      if (headers["time.h"]) C["CLOCKS_PER_SEC"] = { v: 1000 };
      if (headers["locale.h"]) {
        C["LC_ALL"] = { v: 0 }; C["LC_COLLATE"] = { v: 1 };
        C["LC_CTYPE"] = { v: 2 }; C["LC_MONETARY"] = { v: 3 };
        C["LC_NUMERIC"] = { v: 4 }; C["LC_TIME"] = { v: 5 };
      }
      if (headers["stdint.h"] || headers["inttypes.h"]) {
        C["INT8_MIN"] = { v: -128 }; C["INT8_MAX"] = { v: 127 };
        C["INT16_MIN"] = { v: -32768 }; C["INT16_MAX"] = { v: 32767 };
        C["INT32_MIN"] = { v: -2147483648 }; C["INT32_MAX"] = { v: 2147483647 };
        C["UINT32_MAX"] = { v: 4294967295 };
        C["INT64_MAX"] = { v: 9223372036854775807 };
      }
      if (headers["inttypes.h"]) {
        // string macros: represented as string-valued constants
        [["PRId8", '"d"'], ["PRId16", '"d"'], ["PRId32", '"d"'], ["PRId64", '"lld"'],
         ["PRIi32", '"i"'], ["PRIu8", '"u"'], ["PRIu16", '"u"'], ["PRIu32", '"u"'],
         ["PRIu64", '"llu"'], ["PRIx32", '"x"'], ["PRIx64", '"llx"'],
         ["PRIX32", '"X"']].forEach(([n, s]) => {
          C[n] = { s: s.slice(1, -1) };
        });
      }
      if (headers["errno.h"]) C["errno"] = { v: 0, isErrno: true };
    }
    seedConstsForHeaders();
    errnoAddr = heapAlloc(4, 4); // the errno object lives here

    const P = makeParser(lex(macroText), unit, parserTypedefs, cppMode);
    let parsed;
    try {
      parsed = P.parseUnit();
    } catch (e) {
      if (e instanceof CErr) throw e;
      throw new CErr(String(e && e.message || e), 0, "compile");
    }

    // typedef names are resolved inside the parser via `typedefs`; the
    // seeded ones were injected through parserTypedefs (see makeParser).

    for (const f of parsed.funcs) registerFunction(f);

    function registerFunction(decl) {
      if (funcs[decl.name]) {
        if (!cppMode) err("redefinition of function " + decl.name, 0);
        // C++ overloading: keep every definition, dispatch by arg types
        const id = fnCount++;
        const addr = FN_BASE + id * 8;
        const key = decl.name + "##" + id;
        funcs[key] = { decl, addr };
        fnByAddr[addr] = { user: decl };
        overloads[decl.name].push({ key, params: decl.type.params.map((p) => p.type) });
        return addr;
      }
      const id = fnCount++;
      const addr = FN_BASE + id * 8;
      funcs[decl.name] = { decl, addr };
      fnByAddr[addr] = { user: decl };
      overloads[decl.name] = [{ key: decl.name, params: decl.type.params.map((p) => p.type) }];
      return addr;
    }

    function addLiteral(s) {
      if (literals[s] !== undefined) return literals[s];
      const addr = roPtr;
      const bytes = [];
      for (const ch of s) {
        const cp = ch.codePointAt(0);
        if (cp < 128) bytes.push(cp);
        else { // UTF-8 encode so %s and files handle non-ASCII sanely
          if (cp < 0x800) bytes.push(0xc0 | (cp >> 6), 0x80 | (cp & 63));
          else if (cp < 0x10000) bytes.push(0xe0 | (cp >> 12), 0x80 | ((cp >> 6) & 63), 0x80 | (cp & 63));
          else bytes.push(0xf0 | (cp >> 18), 0x80 | ((cp >> 12) & 63), 0x80 | ((cp >> 6) & 63), 0x80 | (cp & 63));
        }
      }
      bytes.push(0);
      mem.setBytes(addr, new Uint8Array(bytes));
      roPtr += bytes.length;
      literals[s] = addr;
      return addr;
    }

    /* ---------------- allocation ---------------- */

    function heapAlloc(size, align) {
      align = align || 8;
      heapPtr = Math.ceil(heapPtr / align) * align;
      const addr = heapPtr;
      heapPtr += Math.max(1, size);
      if (heapPtr > sp) rerr("out of memory: the heap collided with the stack");
      mem.ensure(addr, size);
      return addr;
    }

    function stackAlloc(size, align) {
      align = align || 16;
      sp = Math.floor((sp - Math.max(1, size)) / align) * align;
      if (sp < heapPtr) rerr("out of memory (stack overflow)");
      mem.ensure(sp, size);
      return sp;
    }

    /* addresses that are legal to read/write: rodata (string literals),
       globals+heap [STACK_LIMIT, heapPtr), and the live stack [sp, STACK_TOP) */
    function inDataRange(addr, size) {
      if (addr < 0 || addr + size > STACK_TOP) return false;
      if (addr >= 16 && addr + size <= roPtr) return true;
      if (addr < STACK_LIMIT) return false;
      return (addr + size <= heapPtr) || (addr >= sp && addr + size <= STACK_TOP);
    }

    function checkAddr(addr, size, what) {
      if (addr === 0) {
        rerr("segmentation fault: " + (what || "dereference") +
             " of a NULL pointer");
      }
      if (isFnAddr(addr)) {
        rerr("invalid memory access: used a function pointer as data");
      }
      if (!inDataRange(addr, size)) {
        rerr("invalid memory access at address " + addr +
             " — the pointer is wild or out of bounds");
      }
    }

    function isFnAddr(v) { return v >= FN_BASE; }

    /* ---------------- globals ---------------- */

    const globalVars = {}; // name -> {addr, type}

    function initGlobals() {
      // zero-allocate everything first (so initializers may reference others)
      for (const group of unit.globals) {
        for (const item of group) {
          if (!item.name) continue;
          if (item.type.k === "fn") continue; // prototype
          if (globalVars[item.name]) err("redefinition of global " + item.name, 0);
          let size, align;
          try {
            size = typeSize(item.type) || 1;
            align = typeAlign(item.type);
          } catch (e) {
            if (String(e.message).indexOf("incomplete") !== -1 || String(e.message).indexOf("void") !== -1) {
              err("global " + item.name + " has an incomplete type", 0);
            }
            throw e;
          }
          if (item.type.k === "arr" && item.type.vlaExpr) {
            err("global arrays cannot have variable sizes", 0);
          }
          const addr = heapAlloc(size, align);
          globalVars[item.name] = { addr, type: item.type };
        }
      }
      // run the initializers in declaration order
      for (const group of unit.globals) {
        for (const item of group) {
          if (!item.name || !item.init || item.type.k === "fn") continue;
          const gv = globalVars[item.name];
          writeInit(gv.addr, item.type, item.init);
        }
      }
    }

    /* write an initializer tree (from parseInitializer) to memory */
    function writeInit(addr, type, init) {
      if (Array.isArray(init)) init = { items: init };
      if (!init) { zeroRange(addr, typeSize(type)); return; }
      if (type.k === "arr") {
        const es = typeSize(type.of);
        if (init.k === "str") {
          // char arr[] = "..."
          const s = init.s;
          const bytes = [];
          for (const ch of s) {
            const cp = ch.codePointAt(0);
            if (cp < 128) bytes.push(cp);
            else if (cp < 0x800) bytes.push(0xc0 | (cp >> 6), 0x80 | (cp & 63));
            else if (cp < 0x10000) bytes.push(0xe0 | (cp >> 12), 0x80 | ((cp >> 6) & 63), 0x80 | (cp & 63));
            else bytes.push(0xf0 | (cp >> 18), 0x80 | ((cp >> 12) & 63), 0x80 | ((cp >> 6) & 63), 0x80 | (cp & 63));
          }
          bytes.push(0);
          if (type.n !== null && bytes.length > type.n) {
            err("string initializer is longer than its char array");
          }
          mem.setBytes(addr, new Uint8Array(bytes));
          if (type.n !== null && bytes.length < type.n) zeroRange(addr + bytes.length, type.n - bytes.length);
          return;
        }
        const items = init.items || [];
        if (type.n === null) {
          err("array size cannot be inferred here — give it an explicit size");
        }
        for (let i = 0; i < type.n; i++) {
          if (i < items.length) writeInit(addr + i * es, type.of, items[i]);
          else zeroRange(addr + i * es, es);
        }
        return;
      }
      if (type.k === "rec" && type.tag === "struct") {
        const items = (init && init.items) || [];
        type.fields.forEach((f, i) => {
          if (f.bits !== null && f.bits !== undefined) {
            // bit-field init: evaluate scalar, pack via member write
            if (i < items.length && items[i].k === "expr") {
              const v = evalExpr(items[i].e, { vars: {} }).v;
              writeMember(addr, f, v);
            }
            return;
          }
          if (i < items.length) writeInit(addr + f.off, f.type, items[i]);
          else zeroRange(addr + f.off, typeSize(f.type));
        });
        return;
      }
      if (type.k === "rec" && type.tag === "union") {
        const first = type.fields[0];
        const items = (init && init.items) || [];
        if (first && items.length) writeInit(addr + first.off, first.type, items[0]);
        return;
      }
      if (init.k === "expr") {
        const v = evalExpr(init.e, { vars: {} });
        storeValue(addr, type, v);
        return;
      }
      err("bad initializer for this type");
    }

    function zeroRange(addr, len) {
      if (len <= 0) return;
      mem.ensure(addr, len);
      mem.bytes.fill(0, addr, addr + len);
    }

    function storeValue(addr, type, rv) {
      const v = convertValue(rv.v, rv.t, type);
      if (type.k === "rec" || type.k === "arr") {
        checkAddr(v, 1, "copy of a struct/array");
        const size = typeSize(type);
        const src = mem.getBytes(rv.addr !== undefined ? rv.addr : v, size);
        mem.setBytes(addr, src);
        return;
      }
      memWrite(mem, addr, v, type);
    }

    /* ---------------- conversions ---------------- */

    function convertValue(v, from, to) {
      if (to.k === "void") return 0;
      if (isPtr(to)) {
        if (isPtr(from) || isIntType(from)) return Math.trunc(v);
        if (isFloatType(from)) rerr("cannot convert float to pointer");
        return v;
      }
      if (isFloatType(to)) return Number(v);
      if (isIntType(to)) {
        if (isFloatType(from)) return wrapInt(Math.trunc(v), to);
        if (isIntType(from)) return wrapInt(v, to);
        if (isPtr(from)) return wrapInt(v, to);
        return wrapInt(v, to);
      }
      if (to.k === "rec" || to.k === "arr") return v; // address copy handled by caller
      return v;
    }

    function truthy(v) { return !!v; }

    /* ---------------- frames & scope ---------------- */

    function newFrame(fnName) {
      return { fnName, vars: {}, scopes: [], spMark: sp, retSlot: null };
    }
    function enterScope(frame) { frame.scopes.push({ spMark: sp, vars: frame.vars, varsNew: {} }); frame.vars = Object.create(frame.vars); }
    function exitScope(frame) {
      const s = frame.scopes.pop();
      sp = s.spMark;
      frame.vars = s.vars;
    }
    function declareVar(frame, name, type, addr) {
      frame.vars[name] = { addr, type };
      if (frame.scopes.length) frame.scopes[frame.scopes.length - 1].varsNew[name] = 1;
    }

    /* ---------------- expression evaluation ---------------- */

    function tick(line) {
      if (++steps > maxSteps) {
        rerr("the program ran too long — it may be stuck in an infinite loop", line);
      }
    }

    /* evalLValue: returns {addr, type, constq} or null if not an lvalue.
       NOTE: lvalue evaluation only computes ADDRESSES; the memory checks
       happen when a value is actually read (decayed) or written, so that
       address-only idioms like offsetof's ((t*)0)->m stay legal. */
    function evalLValue(e, frame) {
      tick(e.line);
      switch (e.x) {
        case "id": {
          const local = frame && frame.vars[e.name];
          if (local) return { addr: local.addr, type: local.type };
          const g = globalVars[e.name];
          if (g) return { addr: g.addr, type: g.type };
          const cst = unit.consts[e.name];
          if (cst) {
            if (cst.isErrno) return { addr: errnoAddr, type: T_INT() };
            return null; // other constants are not lvalues
          }
          // functions, builtins and stdin/stdout/stderr are not data lvalues
          return null;
        }
        case "un": {
          if (e.op === "*") {
            const p = evalExpr(e.e, frame);
            if (!isPtr(p.t)) err("cannot dereference a non-pointer", e.line);
            return { addr: p.v, type: p.t.to };
          }
          break;
        }
        case "index": {
          const base = evalExpr(e.arr, frame);
          const idx = evalExpr(e.idx, frame);
          const elemT = arrayElemType(base.t, e.line);
          const addr = base.v + Math.trunc(idx.v) * typeSize(elemT);
          return { addr, type: elemT };
        }
        case "member": {
          let addr, rec;
          if (e.arrow) {
            const p = evalExpr(e.obj, frame);
            if (!isPtr(p.t) || p.t.to.k !== "rec") {
              err("-> used on something that is not a pointer to a struct", e.line);
            }
            rec = p.t.to;
            addr = p.v;
          } else {
            const o = evalLValue(e.obj, frame);
            if (!o) err(". used on something that is not a struct", e.line);
            if (o.type.k === "ref") {
              // member access through a reference: auto-deref the base
              const target = memRead(mem, o.addr, T_VOIDPTR());
              rec = o.type.to;
              const f0 = rec.fields.find((x) => x.name === e.name);
              if (!f0) err(recName(rec) + " has no field named " + e.name, e.line);
              return { addr: target + f0.off, type: f0.type, field: f0 };
            }
            if (o.type.k !== "rec") {
              err(". used on something that is not a struct", e.line);
            }
            rec = o.type;
            addr = o.addr;
          }
          const f = rec.fields.find((x) => x.name === e.name);
          if (!f) err(recName(rec) + " has no field named " + e.name, e.line);
          return { addr: addr + f.off, type: f.type, field: f };
        }
        case "compound": {
          const { addr, type } = evalCompound(e, frame);
          return { addr, type };
        }
        case "str": {
          const a = addLiteral(e.s);
          return { addr: a, type: { k: "ptr", to: makeInt(1, true, "char") } };
        }
      }
      return null;
    }

    function typeSizeSafe(t) {
      try { return typeSize(t) || 1; } catch (e2) { return 8; }
    }

    function arrayElemType(t, line) {
      if (isPtr(t)) return t.to;
      if (t.k === "arr") return t.of;
      err("subscripted value is not an array or pointer", line);
    }

    function evalCompound(e, frame) {
      let type = e.type;
      // (int[]){...}: infer the element count from the initializer list
      if (type.k === "arr" && type.n === null && !type.vlaExpr) {
        if (e.inits && e.inits.length) type = Object.assign({}, type, { n: e.inits.length });
      }
      const size = typeSize(type);
      const align = typeAlign(type);
      const addr = stackAlloc(size, align);
      zeroRange(addr, size);
      if (type.k === "arr" || (type.k === "rec")) {
        writeInit(addr, type, { items: e.inits });
      }
      return { addr, type };
    }

    /* evaluate an expression to a typed rvalue {v, t} (arrays decay) */
    function evalExpr(e, frame) {
      tick(e.line);
      switch (e.x) {
        case "num": {
          const t = e.isFloat ? T_DOUBLE() : T_INT();
          return { v: e.v, t };
        }
        case "str": {
          const a = addLiteral(e.s);
          return { v: a, t: { k: "ptr", to: T_CHAR() } };
        }
        case "id": {
          const lv = evalLValue(e, frame);
          if (lv) return decayed(lv);
          const c = unit.consts[e.name];
          if (c) {
            if (c.s !== undefined) return { v: addLiteral(c.s), t: { k: "ptr", to: T_CHAR() } };
            if (c.isErrno) return { v: mem.i32(errnoAddr), t: T_INT() };
            return { v: c.v, t: guessConstType(c.v) };
          }
          const f = funcs[e.name];
          if (f) return { v: f.addr, t: fnPtrType(e.name) };
          const b = BUILTINS[e.name];
          if (b) return { v: b.fnAddr, t: b.type };
          if (SPECIAL_VARS[e.name]) return SPECIAL_VARS[e.name];
          err("use of undeclared identifier " + e.name, e.line);
          break;
        }
        case "comma": evalExpr(e.l, frame); return evalExpr(e.r, frame);
        case "assign": return evalAssign(e, frame);
        case "cond": {
          const c = evalExpr(e.c, frame);
          return c.v ? evalExpr(e.a, frame) : evalExpr(e.b, frame);
        }
        case "bin": return evalBinary(e, frame);
        case "un": return evalUnary(e, frame);
        case "post": return evalPost(e, frame);
        case "index": {
          const lv = evalLValue(e, frame);
          if (lv) return decayed(lv);
          break;
        }
        case "member": {
          const lv = evalLValue(e, frame);
          if (lv) return decayed(lv);
          break;
        }
        case "call": return evalCall(e, frame);
        case "cast": {
          const v = evalExpr(e.e, frame);
          if (e.type.k === "void") return { v: 0, t: { k: "void" } };
          if (e.type.k === "rec" || e.type.k === "arr") return { v: v.v, t: e.type, addr: v.addr !== undefined ? v.addr : v.v };
          return { v: convertValue(v.v, v.t, e.type), t: e.type };
        }
        case "sizeofT": return { v: typeSize(e.type), t: T_SIZET() };
        case "sizeofE": {
          try {
            return { v: typeSize(inferType(e.e, frame)), t: T_SIZET() };
          } catch (e1) {
            // sizeof of a VLA is computed at runtime from its allocation
            if (e.e.x === "id") {
              const vr = (frame && frame.vars[e.e.name]) || globalVars[e.e.name];
              if (vr && vr.vlaSize !== undefined) {
                return { v: vr.vlaSize, t: T_SIZET() };
              }
            }
            throw e1;
          }
        }
        case "compound": {
          const c = evalCompound(e, frame);
          if (c.type.k === "rec" || c.type.k === "arr") {
            return { v: c.addr, t: { k: "ptr", to: c.type }, addr: c.addr, rawType: c.type };
          }
          // a scalar compound literal is an lvalue whose rvalue is its value
          return { v: memRead(mem, c.addr, c.type), t: c.type };
        }
        case "generic": return evalGeneric(e, frame);
      }
      err("cannot evaluate this expression", e.line);
    }

    function guessConstType(v) {
      if (!Number.isInteger(v)) return T_DOUBLE();
      return Math.abs(v) <= 2147483647 ? T_INT() : T_LONG();
    }

    /* array/function decay: value of an array expr = its address */
    function decayed(lv) {
      if (lv.type.k === "ref") {
        // a reference slot stores the referent's address: auto-deref
        const target = memRead(mem, lv.addr, T_VOIDPTR());
        const to = lv.type.to;
        if (to.k === "rec" || to.k === "arr") {
          return { v: target, t: to, addr: target, rawType: to.k === "rec" ? to : undefined };
        }
        if (lv.field && lv.field.bits !== null && lv.field.bits !== undefined) {
          const f2 = lv.field;
          checkAddr(target - f2.off, f2.unitSize || 4, "bit-field read");
          const base = readUnit(target - f2.off, f2);
          let val = Math.floor(base / Math.pow(2, f2.bitOff)) % Math.pow(2, f2.bits);
          if (f2.type.signed && val >= Math.pow(2, f2.bits - 1)) val -= Math.pow(2, f2.bits);
          return { v: val, t: f2.type };
        }
        checkAddr(target, typeSizeSafe(to), "reference read");
        return { v: memRead(mem, target, to), t: to };
      }
      if (lv.type.k === "arr") return { v: lv.addr, t: { k: "ptr", to: lv.type.of } };
      if (lv.field && lv.field.bits !== null && lv.field.bits !== undefined) {
        // bit-field: extract from its storage unit, sign-extend if signed
        const f = lv.field;
        checkAddr(lv.addr - f.off, f.unitSize || 4, "bit-field read");
        const base = readUnit(lv.addr - f.off, f);
        let val = Math.floor(base / Math.pow(2, f.bitOff)) % Math.pow(2, f.bits);
        if (f.type.signed && val >= Math.pow(2, f.bits - 1)) {
          val -= Math.pow(2, f.bits);
        }
        return { v: val, t: f.type };
      }
      if (lv.type.k === "rec") {
        return { v: lv.addr, t: lv.type, addr: lv.addr, rawType: lv.type };
      }
      if (lv.type.k === "fn") return { v: lv.addr, t: { k: "ptr", to: lv.type } };
      checkAddr(lv.addr, typeSizeSafe(lv.type), "read");
      return { v: memRead(mem, lv.addr, lv.type), t: lv.type };
    }

    function fnPtrType(name) {
      const f = funcs[name];
      return { k: "ptr", to: f.decl.type };
    }

    function evalAssign(e, frame) {
      let lv = evalLValue(e.l, frame);
      if (!lv) err("expression before = is not assignable", e.line);
      if (lv.type.k === "ref") {
        lv = { addr: memRead(mem, lv.addr, T_VOIDPTR()), type: lv.type.to };
      }
      if (lv.type.const) err("cannot assign to a const variable", e.line);
      let rv = evalExpr(e.r, frame);
      if (e.op !== "=") {
        if (lv.field && lv.field.bits !== null && lv.field.bits !== undefined) {
          checkAddr(lv.addr - lv.field.off, lv.field.unitSize || 4, "bit-field write");
        } else {
          checkAddr(lv.addr, typeSizeSafe(lv.type), "assignment");
        }
        const cur = { v: memRead(mem, lv.addr, lv.type), t: lv.type };
        const op = e.op.slice(0, -1);
        rv = binaryValue(op, cur, rv, e.line);
      }
      const v = convertValue(rv.v, rv.t, lv.type);
      if (lv.type.k === "rec" || lv.type.k === "arr") {
        const size = typeSize(lv.type);
        checkAddr(lv.addr, size, "assignment");
        const src = mem.getBytes(rv.addr !== undefined ? rv.addr : v, size);
        mem.setBytes(lv.addr, src);
      } else if (lv.field && lv.field.bits !== null && lv.field.bits !== undefined) {
        writeMember(lv.addr - lv.field.off, lv.field, v);
      } else {
        checkAddr(lv.addr, typeSizeSafe(lv.type), "assignment");
        memWrite(mem, lv.addr, v, lv.type);
      }
      return { v, t: lv.type };
    }

    function writeMember(recAddr, f, value) {
      if (f.bits === null || f.bits === undefined) {
        memWrite(mem, recAddr + f.off, value, f.type);
        return;
      }
      const mask = Math.pow(2, f.bits) - 1;
      const shifted = (Math.trunc(value) & mask) * Math.pow(2, f.bitOff);
      const keepMask = ~(mask * Math.pow(2, f.bitOff));
      writeUnit(recAddr, f, (readUnit(recAddr, f) & keepMask) + shifted);
    }
    function readUnit(addr, f) {
      const t = f.type;
      switch (f.unitSize) {
        case 1: return t.signed ? mem.i8(addr + f.off) : mem.u8(addr + f.off);
        case 2: return t.signed ? mem.i16(addr + f.off) : mem.u16(addr + f.off);
        case 4: return t.signed ? mem.i32(addr + f.off) : mem.u32(addr + f.off);
        default: return Number(mem.i64(addr + f.off));
      }
    }
    function writeUnit(addr, f, v) {
      const t = f.type;
      switch (f.unitSize) {
        case 1: mem.u8(addr + f.off, v & 0xff); break;
        case 2: mem.u16(addr + f.off, v & 0xffff); break;
        case 4: mem.u32(addr + f.off, v >>> 0); break;
        default: mem.i64(addr + f.off, BigInt(Math.trunc(v) || 0)); break;
      }
    }

    function evalBinary(e, frame) {
      if (e.op === "&&" || e.op === "||") {
        const l = evalExpr(e.l, frame);
        if (e.op === "&&" && !truthy(l.v)) return { v: 0, t: T_INT() };
        if (e.op === "||" && truthy(l.v)) return { v: 1, t: T_INT() };
        const r = evalExpr(e.r, frame);
        return { v: truthy(r.v) ? 1 : 0, t: T_INT() };
      }
      const l = evalExpr(e.l, frame);
      if (e.op === ">>" && l.t && l.t.k === "cin") return evalCinChain(e.r, frame);
      const r = evalExpr(e.r, frame);
      return binaryValue(e.op, l, r, e.line);
    }

    function binaryValue(op, l, r, line) {
      /* ---- C++ layer: streams and strings (before C pointer rules) ---- */
      if (op === "<<" && l.t && l.t.k === "cout") {
        out.text += coutFormat(r);
        return l;
      }
      if (op === "+" && (isCppStr(l.t) || isCppStr(r.t))) {
        return cppStrConcat(l, r, line);
      }
      if ((op === "==" || op === "!=" || op === "<" || op === ">" ||
           op === "<=" || op === ">=") &&
          (isCppStr(l.t) || isCppStr(r.t)) &&
          (isPtr(l.t) || isPtr(r.t)) && (isPtr(l.t) === isPtr(r.t))) {
        const ls = cppStrText(l, line), rs = cppStrText(r, line);
        const cmp = ls === rs ? 0 : (ls < rs ? -1 : 1);
        const res = op === "==" ? cmp === 0 : op === "!=" ? cmp !== 0 :
                    op === "<" ? cmp < 0 : op === ">" ? cmp > 0 :
                    op === "<=" ? cmp <= 0 : cmp >= 0;
        return { v: res ? 1 : 0, t: T_INT() };
      }
      // pointer arithmetic
      if (isPtr(l.t) && (op === "+" || op === "-")) {
        if (op === "+" && isArith(r.t)) {
          const elem = typeSizeSafe(l.t.to) || 1;
          return { v: l.v + Math.trunc(r.v) * elem, t: l.t };
        }
        if (op === "-" && isArith(r.t)) {
          const elem = typeSizeSafe(l.t.to) || 1;
          return { v: l.v - Math.trunc(r.v) * elem, t: l.t };
        }
        if (op === "-" && isPtr(r.t)) {
          const elem = typeSizeSafe(l.t.to) || 1;
          return { v: Math.trunc((l.v - r.v) / elem), t: T_LONG() };
        }
      }
      if (isPtr(r.t) && op === "+" && isArith(l.t)) {
        const elem = typeSizeSafe(r.t.to) || 1;
        return { v: r.v + Math.trunc(l.v) * elem, t: r.t };
      }
      if ((op === "==" || op === "!=" || op === "<" || op === ">" ||
           op === "<=" || op === ">=") && (isPtr(l.t) || isPtr(r.t))) {
        let res;
        switch (op) {
          case "==": res = l.v === r.v; break;
          case "!=": res = l.v !== r.v; break;
          case "<": res = l.v < r.v; break;
          case ">": res = l.v > r.v; break;
          case "<=": res = l.v <= r.v; break;
          default: res = l.v >= r.v; break;
        }
        return { v: res ? 1 : 0, t: T_INT() };
      }
      if (!isArith(l.t) || !isArith(r.t)) {
        if (op === "+" && isPtr(l.t)) return { v: l.v, t: l.t };
        err("invalid operands to binary " + op, line);
      }
      if ((op === "<<" || op === ">>" || op === "&" || op === "|" || op === "^") &&
          (isFloatType(l.t) || isFloatType(r.t))) {
        err("bitwise operation on a floating-point value", line);
      }
      const ct = usualArith(l.t, r.t);
      const a = convertValue(l.v, l.t, ct);
      const b = convertValue(r.v, r.t, ct);
      let v;
      switch (op) {
        case "+": v = a + b; break;
        case "-": v = a - b; break;
        case "*": v = a * b; break;
        case "/":
          if (b === 0 && !isFloatType(ct)) rerr("division by zero", line);
          v = a / b; break;
        case "%":
          if (b === 0) rerr("division by zero", line);
          v = a % b; break;
        case "<<": v = shiftL(a, b); break;
        case ">>": v = shiftR(a, b, ct); break;
        case "&": v = bitwise(a, b, ct, (x, y) => x & y); break;
        case "|": v = bitwise(a, b, ct, (x, y) => x | y); break;
        case "^": v = bitwise(a, b, ct, (x, y) => x ^ y); break;
        case "==": return { v: a === b ? 1 : 0, t: T_INT() };
        case "!=": return { v: a !== b ? 1 : 0, t: T_INT() };
        case "<": case ">": case "<=": case ">=": {
          let res;
          if (isFloatType(ct)) res = op === "<" ? a < b : op === ">" ? a > b : op === "<=" ? a <= b : a >= b;
          else if (!ct.signed) res = cmpUnsigned(op, a, b, ct.size);
          else res = op === "<" ? a < b : op === ">" ? a > b : op === "<=" ? a <= b : a >= b;
          return { v: res ? 1 : 0, t: T_INT() };
        }
        default: err("unknown operator " + op, line);
      }
      if (isFloatType(ct)) return { v, t: ct };
      return { v: wrapInt(v, ct), t: ct };
    }

    /* ---- C++ layer helpers: cout formatting, strings, cin ---- */

    function cppStrText(s, line) {
      if ((isCppStr(s.t) || (isPtr(s.t) && s.t.to && s.t.to.k === "int" &&
           s.t.to.size === 1 && !s.t.to.const))) {
        // cppstr values and plain char* both print their bytes; only
        // cppstr can legally be null (empty)
        if (s.v === 0 && isCppStr(s.t)) return "";
        return readCString(s.v, 1048576);
      }
      err("invalid operands: expected a string value", line);
    }

    function cppStrConcat(l, r, line) {
      const ls = cppStrText(l, line);
      let rs;
      if (isPtr(r.t)) rs = cppStrText(r, line);
      else if (r.t && r.t.k === "int" && r.t.size === 1) {
        rs = String.fromCharCode(r.v & 0xff);
      } else err("invalid operands to binary + with a string", line);
      const s = ls + rs;
      const buf = heapAlloc(s.length + 1, 1);
      writeCString(buf, s);
      return { v: buf, t: T_CPPSTR() };
    }

    function coutFormat(r) {
      if (!r || !r.t) return String(r && r.v);
      if (r.t.k === "endl") return "\n";
      if (isCppStr(r.t)) return r.v === 0 ? "" : readCString(r.v, 1048576);
      if (isPtr(r.t) && r.t.to && r.t.to.k === "int" && r.t.to.size === 1) {
        return readCString(r.v, 1048576);
      }
      if (r.t.k === "int" && r.t.size === 1 && r.t.name === "char") {
        return String.fromCharCode(r.v & 0xff);
      }
      if (isFloatType(r.t)) return formatC("%g", [r]);
      if (isArith(r.t)) {
        if (r.t.signed === false && r.t.size === 8) {
          const TWO64 = 18446744073709551616;
          let u = r.v % TWO64;
          if (u < 0) u += TWO64;
          return String(u);
        }
        if (r.t.signed === false && r.t.size === 4) return String(r.v >>> 0);
        return String(Math.trunc(r.v));
      }
      if (isPtr(r.t)) return "0x" + (r.v >>> 0).toString(16);
      return String(r.v);
    }

    /* `cin >> x [>> y ...]` — one target per call; chaining works because
       the returned marker is a cin again. Reads a whitespace-delimited
       token from the sandbox's stdin. */
    function evalCinChain(e, frame) {
      const lv = evalLValue(e, frame);
      if (!lv) err("std::cin can only read into a variable", e.line);
      let addr = lv.addr, t = lv.type;
      if (t.k === "ref") { addr = memRead(mem, addr, T_VOIDPTR()); t = t.to; }
      if (lv.field && lv.field.bits !== null && lv.field.bits !== undefined) {
        err("std::cin cannot read into a bit-field", e.line);
      }
      if (isCppStr(t)) {
        const word = readStdinWord();
        const buf = heapAlloc(word.length + 1, 1);
        writeCString(buf, word);
        memWrite(mem, addr, buf, T_VOIDPTR());
      } else if (isFloatType(t)) {
        scanC("%lf", fileRecs[FILE_STDIN], [{ v: addr }], [t]);
      } else if (isIntType(t) || isPtr(t)) {
        scanC(t.signed === false ? "%u" : "%d", fileRecs[FILE_STDIN],
              [{ v: addr }], [isPtr(t) ? { k: "ptr", to: t } : t]);
      } else {
        err("std::cin cannot read into this type", e.line);
      }
      return { v: 2, t: T_CIN() };
    }

    function readStdinWord() {
      const rec = fileRecs[FILE_STDIN];
      let s = "";
      for (;;) {
        const b = rec.pos < rec.bytes.length ? rec.bytes[rec.pos++] : -1;
        if (b === -1) break;
        const ch = String.fromCharCode(b);
        if (/\s/.test(ch)) {
          if (s.length) break;
          continue; // skip leading whitespace
        }
        s += ch;
      }
      return s;
    }

    function cmpUnsigned(op, a, b, size) {
      const range = size === 4 ? 4294967296 : 18446744073709551616;
      let ua = a % range, ub = b % range;
      if (ua < 0) ua = range + ua;   // exact: see wrapInt's 64-bit note
      if (ub < 0) ub = range + ub;
      return op === "<" ? ua < ub : op === ">" ? ua > ub : op === "<=" ? ua <= ub : ua >= ub;
    }

    function shiftL(a, b) {
      b = b & 63;
      if (b <= 31) return a * Math.pow(2, b);
      return a * Math.pow(2, b);
    }
    function shiftR(a, b, t) {
      b = b & 63;
      if (t.signed) return Math.floor(a / Math.pow(2, b));
      const range = t.size === 4 ? 4294967296 : 18446744073709551616;
      let ua = a % range;
      if (ua < 0) ua = range + ua; // exact (see wrapInt's 64-bit note)
      return Math.floor(ua / Math.pow(2, b));
    }
    function bitwise(a, b, t, f) {
      if (t.size <= 4) {
        return t.signed ? (f(a | 0, b | 0)) : (f(a >>> 0, b >>> 0) >>> 0);
      }
      // 64-bit: split into 32-bit halves
      const ah = Math.floor(a / 4294967296), al = a % 4294967296 | 0;
      const bh = Math.floor(b / 4294967296), bl = b % 4294967296 | 0;
      const h = f(ah | 0, bh | 0) | 0;
      const l = f(al | 0, bl | 0) >>> 0;
      return h * 4294967296 + l;
    }

    function evalUnary(e, frame) {
      switch (e.op) {
        case "!": {
          const v = evalExpr(e.e, frame);
          return { v: truthy(v.v) ? 0 : 1, t: T_INT() };
        }
        case "~": {
          const v = evalExpr(e.e, frame);
          if (isFloatType(v.t)) err("~ on a floating-point value", e.line);
          const t = intRank(v.t) < 3 ? T_INT() : v.t;
          const x = convertValue(v.v, v.t, t);
          return { v: wrapInt(~x, t), t };
        }
        case "-": {
          const v = evalExpr(e.e, frame);
          if (isFloatType(v.t)) return { v: -v.v, t: v.t };
          const t = intRank(v.t) < 3 ? T_INT() : v.t;
          return { v: wrapInt(-convertValue(v.v, v.t, t), t), t };
        }
        case "+": {
          const v = evalExpr(e.e, frame);
          const t = isFloatType(v.t) ? v.t : (intRank(v.t) < 3 ? T_INT() : v.t);
          return { v: convertValue(v.v, v.t, t), t };
        }
        case "&": {
          const lv = evalLValue(e.e, frame);
          if (!lv) {
            // &function is legal C
            if (e.e.x === "id") {
              const fn = funcs[e.e.name];
              if (fn) return { v: fn.addr, t: { k: "ptr", to: fn.decl.type } };
              const bl = BUILTINS[e.e.name];
              if (bl) return { v: bl.fnAddr, t: { k: "ptr", to: bl.type } };
            }
            err("cannot take the address of this expression", e.line);
          }
          if (lv.type.k === "ref") {
            // &reference yields the referent's address (C++ semantics)
            return { v: memRead(mem, lv.addr, T_VOIDPTR()),
                     t: { k: "ptr", to: lv.type.to } };
          }
          return { v: lv.addr, t: { k: "ptr", to: lv.type } };
        }
        case "*": {
          const v = evalExpr(e.e, frame);
          const d = derefValue(v, e.line);
          return decayed({ addr: d.addr, type: d.type });
        }
        case "++": case "--": {
          let lv = evalLValue(e.e, frame);
          if (!lv) err("operand of " + e.op + " is not assignable", e.line);
          if (lv.type.k === "ref") {
            lv = { addr: memRead(mem, lv.addr, T_VOIDPTR()), type: lv.type.to };
          }
          if (lv.type.const) err("cannot modify a const variable", e.line);
          checkAddr(lv.addr, typeSizeSafe(lv.type), "increment");
          const cur = { v: memRead(mem, lv.addr, lv.type), t: lv.type };
          const nv = incDecValue(e.op === "++" ? 1 : -1, cur, lv.type);
          memWrite(mem, lv.addr, nv, lv.type);
          return { v: nv, t: lv.type };
        }
      }
      err("unknown unary operator " + e.op, e.line);
    }

    function derefValue(v, line) {
      if (!isPtr(v.t)) err("cannot dereference a non-pointer", line);
      const to = v.t.to;
      checkAddr(v.v, typeSizeSafe(to), "dereference");
      return { addr: v.v, type: to };
    }

    function incDecValue(dir, cur, t) {
      if (isPtr(t)) {
        const elem = typeSizeSafe(t.to) || 1;
        return cur.v + dir * elem;
      }
      if (isFloatType(t)) return cur.v + dir;
      const ct = intRank(t) < 3 ? T_INT() : t;
      return wrapInt(convertValue(cur.v, cur.t, ct) + dir, ct);
    }

    function evalPost(e, frame) {
      let lv = evalLValue(e.e, frame);
      if (!lv) err("operand of " + e.op + " is not assignable", e.line);
      if (lv.type.k === "ref") {
        lv = { addr: memRead(mem, lv.addr, T_VOIDPTR()), type: lv.type.to };
      }
      if (lv.type.const) err("cannot modify a const variable", e.line);
      checkAddr(lv.addr, typeSizeSafe(lv.type), "increment");
      const cur = { v: memRead(mem, lv.addr, lv.type), t: lv.type };
      const old = cur.v;
      const nv = incDecValue(e.op === "++" ? 1 : -1, cur, lv.type);
      memWrite(mem, lv.addr, nv, lv.type);
      return { v: old, t: lv.type };
    }

    /* static type inference for sizeof(expr) — never evaluates the operand */
    function inferType(e, frame) {
      switch (e.x) {
        case "num": return e.isFloat ? T_DOUBLE() : T_INT();
        case "str": return { k: "ptr", to: T_CHAR() };
        case "id": {
          const local = frame && frame.vars[e.name];
          if (local) return local.type;
          const g = globalVars[e.name];
          if (g) return g.type;
          if (unit.consts[e.name]) return guessConstType(unit.consts[e.name].v);
          const f = funcs[e.name];
          if (f) return { k: "ptr", to: f.decl.type };
          const b = BUILTINS[e.name];
          if (b) return b.type;
          if (SPECIAL_VARS[e.name]) return SPECIAL_VARS[e.name].t;
          err("use of undeclared identifier " + e.name, e.line);
          break;
        }
        case "cast": return e.type;
        case "sizeofT": case "sizeofE": return T_SIZET();
        case "bin": {
          if (["==", "!=", "<", ">", "<=", ">=", "&&", "||"].indexOf(e.op) !== -1) return T_INT();
          if (isPtr(inferType(e.l, frame)) || isPtr(inferType(e.r, frame))) {
            const pt = inferType(e.l, frame);
            return isPtr(pt) ? pt : inferType(e.r, frame);
          }
          return usualArith(inferType(e.l, frame), inferType(e.r, frame));
        }
        case "un": {
          if (e.op === "!") return T_INT();
          if (e.op === "&") {
            const inner = inferType(e.e, frame);
            return { k: "ptr", to: inner };
          }
          if (e.op === "*") {
            const inner = inferType(e.e, frame);
            if (isPtr(inner)) return inner.to;
            if (inner.k === "arr") return inner.of;
            err("cannot dereference this", e.line);
          }
          const t = inferType(e.e, frame);
          return isFloatType(t) ? t : (intRank(t) < 3 ? T_INT() : t);
        }
        case "index": {
          const base = inferType(e.arr, frame);
          return arrayElemType(base, e.line);
        }
        case "member": {
          let rec;
          if (e.arrow) {
            const pt = inferType(e.obj, frame);
            if (!isPtr(pt) || pt.to.k !== "rec") err("-> on a non-struct-pointer", e.line);
            rec = pt.to;
          } else {
            rec = inferType(e.obj, frame);
            if (rec.k === "ref") rec = rec.to;
          }
          if (rec.k === "arr" && (e.name === "size" || e.name === "empty" ||
              e.name === "at" || e.name === "front" || e.name === "back")) {
            if (e.name === "size") return T_SIZET();
            if (e.name === "empty") return makeInt(1, false, "_Bool");
            return rec.of;
          }
          if (rec.k !== "rec") err(". on a non-struct", e.line);
          const f = rec.fields.find((x) => x.name === e.name);
          if (!f) err(recName(rec) + " has no field named " + e.name, e.line);
          return f.type;
        }
        case "assign": return inferType(e.l, frame);
        case "cond": {
          const a = inferType(e.a, frame), b = inferType(e.b, frame);
          if (isArith(a) && isArith(b)) return usualArith(a, b);
          return a;
        }
        case "comma": return inferType(e.r, frame);
        case "post": {
          const t = inferType(e.e, frame);
          return isPtr(t) ? t : (isFloatType(t) ? t : (intRank(t) < 3 ? T_INT() : t));
        }
        case "call": {
          const ft = inferType(e.fn, frame);
          const target = isFnPtr(ft) ? ft.to : (ft.k === "fn" ? ft : null);
          if (target) return target.ret;
          err("calling something that is not a function", e.line);
          break;
        }
        case "compound": return { k: "ptr", to: e.type };
      }
      err("cannot determine the type of this expression", e.line);
    }

    function evalGeneric(e, frame) {
      const t = decayRuntimeType(evalExpr(e.ctrl, frame).t);
      let def = null, hit = null;
      for (const c of e.cases) {
        if (c.type === null) { def = c; continue; }
        if (typesCompatible(t, c.type)) { hit = c; break; }
      }
      const chosen = hit || def;
      if (!chosen) err("_Generic: no matching association for this type", e.line);
      return evalExpr(chosen.e, frame);
    }

    function decayRuntimeType(t) {
      if (t.k === "arr") return { k: "ptr", to: t.of };
      return t;
    }

    function typesCompatible(a, b) {
      a = decayRuntimeType(a); b = decayRuntimeType(b);
      if (a.k === "ptr" && b.k === "ptr") return typesCompatible(a.to, b.to);
      if (a.k === "int" && b.k === "int") return a.size === b.size && a.signed === b.signed;
      if (a.k === "enumT" && b.k === "int") return true;
      if (a.k === "int" && b.k === "enumT") return true;
      if (a.k !== b.k) return false;
      if (a.k === "float") return a.size === b.size;
      if (a.k === "void") return true;
      return false;
    }

  /* --------------------------- calls & frames --------------------------- */

  function evalCall(e, frame) {
    // C++ string methods: s.length(), s.substr(a, b), s.find(x), ...
    if (e.fn.x === "member" && !e.fn.arrow) {
      let bt = null;
      try { bt = inferType(e.fn.obj, frame); } catch (e1) { /* not a cppstr */ }
      if (bt && isCppStr(bt)) return cppStrMethod(e, frame);
      if (bt && bt.k === "arr") return cppArrMethod(e, frame, bt);
      if (bt && bt.k === "arr") return cppArrMethod(e, frame, bt);
    }
    // C++ overloading: pick the definition whose parameters best match
    if (e.fn.x === "id" && overloads[e.fn.name]) {
      const key = pickOverload(e.fn.name, e.args, frame, e.line);
      if (key && key !== e.fn.name) {
        return evalCall({ x: "call", fn: { x: "id", name: key, line: e.fn.line },
                          args: e.args, line: e.line }, frame);
      }
    }
    const callee = evalExpr(e.fn, frame);
    const target = callee.v >= FN_BASE ? fnByAddr[callee.v] : null;
    if (callee.v === 0) {
      rerr("segmentation fault: called a NULL function pointer", e.line);
    }
    if (!target) err("call through an unknown function pointer", e.line);

    const args = e.args.map((a) => evalExpr(a, frame));

    if (target.builtin) {
      return target.builtin.fn(args, frame, e);
    }

    const ft = target.user.type; // user function definitions carry fn types
    if (!ft || ft.k !== "fn") err("calling something that is not a function", e.line);

    const decl = target.user;
    if (ft.variadic || decl.type.variadic) {
      err("functions with a variable argument list (...) cannot be " +
          "defined in the browser sandbox — call them with explicit arguments", e.line);
    }
    if (args.length !== decl.type.params.length) {
      err("function " + decl.name + " expects " + decl.type.params.length +
          " argument(s), got " + args.length, e.line);
    }
    const params = decl.type.params;
    const ret = decl.type.ret;

    // reference parameters bind to the argument's lvalue (C++ semantics)
    params.forEach((pm, i) => {
      if (pm.type && pm.type.k === "ref") {
        const lv = evalLValue(e.args[i], frame);
        if (!lv) {
          err("cannot bind a non-lvalue to reference parameter " +
              (pm.name || "#" + (i + 1)), e.line);
        }
        const addr = lv.type.k === "ref"
          ? memRead(mem, lv.addr, T_VOIDPTR()) : lv.addr;
        args[i] = { v: addr, t: { k: "ptr", to: pm.type.to } };
      }
    });

    // struct/array returns go through a caller-allocated temporary slot
    let retSlot = null;
    if (ret.k === "rec" || ret.k === "arr") {
      retSlot = stackAlloc(typeSize(ret), typeAlign(ret));
      zeroRange(retSlot, typeSize(ret));
    }
    const result = runUserFunction(decl, args, params, retSlot, e.line);
    if (ret.k === "rec" || ret.k === "arr") {
      return { v: retSlot, t: ret, addr: retSlot };
    }
    return result;
  }

  /* C++ overload resolution: prefer exact parameter matches, then any
     convertible arithmetic/pointer combination; first definition wins ties. */
  function pickOverload(name, args, frame, line) {
    let best = null, bestScore = -1;
    for (const c of overloads[name]) {
      if (c.params.length !== args.length) continue;
      let score = 0, ok = true;
      for (let i = 0; i < args.length; i++) {
        let at;
        try { at = inferType(args[i], frame); } catch (e1) { ok = false; break; }
        at = decayRuntimeType(at);
        const pt = decayRuntimeType(c.params[i]);
        if (typesCompatible(at, pt)) score += 2;
        else if ((isArith(at) || isPtr(at)) && (isArith(pt) || isPtr(pt))) score += 1;
        else { ok = false; break; }
      }
      if (ok && score > bestScore) { bestScore = score; best = c; }
    }
    return best ? best.key : null;
  }

  /* std::array lowered to a C array keeps a few member calls: size(), etc. */
  function cppArrMethod(e, frame, at) {
    const name = e.fn.name;
    const obj = evalExpr(e.fn.obj, frame); // arrays decay: v is the data addr
    if (name === "size") return { v: at.n, t: T_SIZET() };
    if (name === "empty") {
      return { v: at.n === 0 ? 1 : 0, t: makeInt(1, false, "_Bool") };
    }
    if (name === "at" || name === "front" || name === "back") {
      let i;
      if (name === "at") i = Math.trunc(evalExpr(e.args[0], frame).v);
      else if (name === "front") i = 0;
      else i = at.n - 1;
      if (i < 0 || i >= at.n) rerr("std::array::at: index out of range", e.line);
      const es = Math.max(1, typeSize(at.of));
      return { v: memRead(mem, obj.v + i * es, at.of), t: at.of };
    }
    err("the sandbox std::array supports size(), empty(), at(), front() and " +
        "back() — not " + name + "()", e.line);
  }

  /* The sandbox `string` type: a tagged char* with the methods the C++
     course's runnable examples actually use. */
  function cppStrMethod(e, frame) {
    const obj = evalExpr(e.fn.obj, frame);
    if (!isCppStr(obj.t)) err("this is not a string value", e.line);
    const s = obj.v === 0 ? "" : readCString(obj.v, 1048576);
    const name = e.fn.name;
    const arg = (i) => evalExpr(e.args[i], frame);
    const cstrArg = (i) => {
      const a = arg(i);
      if (isPtr(a.t)) return a.v === 0 ? "" : readCString(a.v, 1048576);
      if (a.t && a.t.k === "int" && a.t.size === 1) {
        return String.fromCharCode(a.v & 0xff);
      }
      err("the sandbox string methods take a string or char argument", e.line);
    };
    switch (name) {
      case "length": case "size":
        if (e.args.length) err(name + "() takes no arguments", e.line);
        return { v: s.length, t: T_SIZET() };
      case "empty":
        return { v: s.length === 0 ? 1 : 0, t: makeInt(1, false, "_Bool") };
      case "c_str": case "data":
        return { v: obj.v, t: { k: "ptr", to: T_CHAR() } };
      case "substr": {
        const pos = Math.trunc(arg(0).v);
        const n = e.args.length > 1 ? Math.trunc(arg(1).v) : s.length - pos;
        if (pos < 0 || pos > s.length) {
          rerr("std::string::substr: position out of range", e.line);
        }
        const part = s.slice(pos, pos + Math.max(0, n));
        const buf = heapAlloc(part.length + 1, 1);
        writeCString(buf, part);
        return { v: buf, t: T_CPPSTR() };
      }
      case "find": case "rfind": {
        const pos = e.args.length > 1 ? Math.trunc(arg(1).v) : 0;
        const needle = cstrArg(0);
        let idx;
        if (name === "find") {
          idx = s.indexOf(needle, Math.min(Math.max(pos, 0), s.length));
        } else {
          idx = s.lastIndexOf(needle, pos < 0 ? s.length - 1 : Math.min(pos, s.length - 1));
        }
        return { v: idx, t: T_INT() };
      }
      case "at": {
        const i = Math.trunc(arg(0).v);
        if (i < 0 || i >= s.length) {
          rerr("std::string::at: index out of range", e.line);
        }
        return { v: s.charCodeAt(i), t: T_CHAR() };
      }
      default:
        err("the sandbox string type supports length(), substr(), find(), " +
            "rfind(), at(), empty() and c_str() — not " + name + "()", e.line);
    }
  }

  function runUserFunction(decl, args, params, retSlot, line) {
    if (jsDepth > 400) rerr("stack overflow: recursion went too deep", line);
    jsDepth++;
    const frame = newFrame(decl.name);
    frame.retSlot = retSlot;
    try {
      enterScope(frame); // parameter scope
      params.forEach((pm, i) => {
        // array parameters decay to pointers, exactly like a real compiler
        const pt = pm.type.k === "arr" ? { k: "ptr", to: pm.type.of } : pm.type;
        const size = typeSizeSafe(pt);
        const addr = stackAlloc(size, typeAlign(pt) || 8);
        declareVar(frame, pm.name || "__arg" + i, pt, addr);
        const rv = args[i];
        if (pt.k === "ref") {
          // the slot holds the referent's address; uses auto-deref
          memWrite(mem, addr, rv.v, T_VOIDPTR());
        } else if (pt.k === "rec") {
          const src = rv.addr !== undefined ? rv.addr : rv.v;
          mem.setBytes(addr, mem.getBytes(src, size));
        } else {
          memWrite(mem, addr, convertValue(rv.v, rv.t, pt), pt);
        }
      });
      const bodySp = sp; // replay marker (setjmp/longjmp)
      let result = null;
      for (;;) {
        try {
          execStmt(decl.body, frame);
          result = { v: 0, t: decl.type.ret }; // fell off the end: 0, like main
          break;
        } catch (sig) {
          if (sig && sig.ret) {
            const ret = decl.type.ret;
            if (!sig.rv) {
              result = { v: 0, t: ret };
            } else if (ret.k === "rec" || ret.k === "arr") {
              const src = sig.rv.addr !== undefined ? sig.rv.addr : sig.rv.v;
              mem.setBytes(retSlot, mem.getBytes(src, typeSize(ret)));
              result = { v: retSlot, t: ret, addr: retSlot };
            } else {
              result = { v: convertValue(sig.rv.v, sig.rv.t, ret), t: ret };
            }
            break;
          }
          if (sig && sig.jmpId !== undefined && frame.setjmps &&
              frame.setjmps.indexOf(sig.jmpId) !== -1) {
            // longjmp landed at one of THIS function's setjmp() calls:
            // replay the body — the setjmp builtin hands back the value
            let bufAddr = 0;
            for (const k of Object.keys(jmpTargets)) {
              if (jmpTargets[k] === sig.jmpId) { bufAddr = Number(k); break; }
            }
            if (!frame.jmpPending) frame.jmpPending = {};
            frame.jmpPending[bufAddr] = sig.val === 0 ? 1 : Math.trunc(sig.val || 1);
            sp = bodySp;
            continue;
          }
          throw sig;
        }
      }
      return result;
    } finally {
      sp = frame.spMark;
      jsDepth--;
    }
  }

  /* ---------------------------- statements ------------------------------ */

  const BREAK_SIG = { brk: true };
  const CONT_SIG = { cont: true };

  function execStmt(s, frame) {
    if (!s) return;
    tick(s.line);
    switch (s.x) {
      case "nop": case "case": case "label": return;

      case "block": {
        enterScope(frame);
        const stmts = s.stmts;
        let pc = 0, jump = null;
        try {
          while (pc < stmts.length) { execStmt(stmts[pc], frame); pc++; }
        } catch (sig) {
          if (sig && sig.gotoLabel) jump = sig;
          else { exitScope(frame); throw sig; }
        }
        if (jump) {
          const idx = stmts.findIndex((st) => st.x === "label" && st.name === jump.gotoLabel);
          if (idx < 0) { exitScope(frame); throw jump; }
          try {
            let q = idx + 1;
            while (q < stmts.length) { execStmt(stmts[q], frame); q++; }
          } catch (sig2) {
            exitScope(frame);
            throw sig2; // goto out of this block (or a second goto)
          }
        }
        exitScope(frame);
        return;
      }

      case "decl": {
        for (const item of s.items) {
          if (!item.name) continue;
          if (item.type.k === "fn") continue; // prototype
          let type = item.type;
          if (type.staticLocal) {
            // static locals live on the heap and persist across calls
            let slot = staticSlots.get(item);
            if (!slot) {
              const sz = typeSizeSafe(type);
              const sa = heapAlloc(sz, typeAlign(type) || 8);
              zeroRange(sa, sz);
              if (item.init) writeInit(sa, type, item.init);
              slot = { addr: sa };
              staticSlots.set(item, slot);
            }
            declareVar(frame, item.name, type, slot.addr);
            continue;
          }
          if (type.k === "arr" && type.vlaExpr) {
            const n = Math.max(0, Math.trunc(evalExpr(type.vlaExpr, frame).v));
            const es = typeSize(type.of);
            const addr = stackAlloc(Math.max(1, n * es), typeAlign(type.of));
            zeroRange(addr, Math.max(1, n * es));
            declareVar(frame, item.name, type, addr);
            frame.vars[item.name].vlaSize = Math.max(1, n * es);
            if (item.init) {
              // initializers arrive as a raw array ({...} list), {items},
              // or {k:"str"} — normalize before walking (writeInitLocal
              // does the same for fixed-size arrays)
              const norm = Array.isArray(item.init) ? { items: item.init }
                : item.init;
              if (norm.k === "str") {
                if (norm.s.length + 1 > n) {
                  err("initializer string is longer than the array", s.line);
                }
                writeInit(addr, type, norm);
              } else {
                const items = norm.items || [];
                for (let i = 0; i < n && i < items.length; i++) {
                  writeInit(addr + i * es, type.of, items[i]);
                }
              }
            }
            continue;
          }
          const size = typeSizeSafe(type);
          const addr = stackAlloc(size, typeAlign(type) || 8);
          zeroRange(addr, size);
          declareVar(frame, item.name, type, addr);
          if (type.k === "ref") {
            // int& r = x; — bind the address, not the value
            if (!item.init || item.init.k !== "expr") {
              err("a reference " + item.name + " must be initialized", s.line);
            }
            const lv = evalLValue(item.init.e, frame);
            if (!lv) err("cannot bind a non-lvalue to reference " + item.name, s.line);
            const target = lv.type.k === "ref"
              ? memRead(mem, lv.addr, T_VOIDPTR()) : lv.addr;
            memWrite(mem, addr, target, T_VOIDPTR());
          } else if (item.init) writeInitLocal(addr, type, item.init, frame);
        }
        return;
      }

      case "expr": evalExpr(s.e, frame); return;

      case "if": {
        const c = evalExpr(s.c, frame);
        if (truthy(c.v)) execStmt(s.then, frame);
        else if (s.els) execStmt(s.els, frame);
        return;
      }

      case "while": {
        for (;;) {
          tick(s.line);
          const c = evalExpr(s.c, frame);
          if (!truthy(c.v)) return;
          try {
            enterScope(frame);
            try { execStmt(s.body, frame); }
            finally { exitScope(frame); }
          } catch (sig) {
            if (sig === BREAK_SIG) return;
            if (sig !== CONT_SIG) throw sig;
          }
        }
      }

      case "rangeFor": {
        // C++ range-based for over a sized array or braced list
        enterScope(frame);
        try {
          const rv = evalExpr(s.range, frame);
          let n = null, base = rv.v, elemT = s.varType;
          if (s.range.x === "compound") {
            if (rv.rawType && rv.rawType.k === "arr") {
              n = rv.rawType.n;
              elemT = rv.rawType.of;
            }
          } else {
            const st = inferType(s.range, frame);
            if (st.k === "arr") { n = st.n; elemT = st.of; }
          }
          if (n === null || n === undefined) {
            err("the sandbox range-for needs a sized array or a braced list",
                s.line);
          }
          const es = Math.max(1, typeSize(elemT));
          for (let i = 0; i < n; i++) {
            tick(s.line);
            try {
              enterScope(frame);
              try {
                const size = typeSizeSafe(s.varType);
                const addr = stackAlloc(size, typeAlign(s.varType) || 8);
                zeroRange(addr, size);
                declareVar(frame, s.varName, s.varType, addr);
                mem.setBytes(addr, mem.getBytes(base + i * es, Math.max(es, 1)));
                execStmt(s.body, frame);
              } finally { exitScope(frame); }
            } catch (sig) {
              if (sig === BREAK_SIG) break;
              if (sig !== CONT_SIG) throw sig;
            }
          }
        } finally { exitScope(frame); }
        return;
      }

      case "do": {
        for (;;) {
          tick(s.line);
          try {
            enterScope(frame);
            try { execStmt(s.body, frame); }
            finally { exitScope(frame); }
          } catch (sig) {
            if (sig === BREAK_SIG) break;
            if (sig !== CONT_SIG) throw sig;
          }
          const c = evalExpr(s.c, frame);
          if (!truthy(c.v)) return;
        }
      }

      case "for": {
        enterScope(frame); // scope for the init declaration
        try {
          if (s.init) execStmt(s.init, frame);
          for (;;) {
            tick(s.line);
            if (s.c) {
              const c = evalExpr(s.c, frame);
              if (!truthy(c.v)) return;
            }
            try {
              enterScope(frame);
              try { execStmt(s.body, frame); }
              finally { exitScope(frame); }
            } catch (sig) {
              if (sig === BREAK_SIG) return;
              if (sig !== CONT_SIG) throw sig;
            }
            if (s.step) evalExpr(s.step, frame);
          }
        } finally { exitScope(frame); }
      }

      case "switch": {
        const cv = evalExpr(s.ctrl, frame);
        const body = s.body;
        const stmts = body.x === "block" ? body.stmts : [body];
        let start = -1, defaultIdx = -1;
        for (let i = 0; i < stmts.length; i++) {
          const st = stmts[i];
          if (st.x !== "case") continue;
          if (st.v === null) { if (defaultIdx < 0) defaultIdx = i; continue; }
          const v = evalExpr(st.v, frame);
          if (v.v === cv.v) { start = i; break; }
        }
        if (start < 0) start = defaultIdx;
        if (start < 0) return;
        try {
          for (let i = start; i < stmts.length; i++) {
            if (stmts[i].x === "case") continue;
            execStmt(stmts[i], frame);
          }
        } catch (sig) {
          if (sig !== BREAK_SIG) throw sig;
        }
        return;
      }

      case "break": throw BREAK_SIG;
      case "continue": throw CONT_SIG;
      case "goto": throw { gotoLabel: s.name };

      case "return": {
        const rv = s.e ? evalExpr(s.e, frame) : null;
        throw { ret: true, rv, line: s.line };
      }
    }
    err("unknown statement kind " + s.x, s.line);
  }

  /* like writeInit but evaluates expressions in the current frame */
  function writeInitLocal(addr, type, init, frame) {
    if (Array.isArray(init)) init = { items: init };
    if (!init) return;
    if (type.k === "arr") {
      const es = typeSize(type.of);
      if (init.k === "str") { writeInit(addr, type, init); return; }
      const items = init.items || [];
      const n = type.n !== null ? type.n : items.length;
      for (let i = 0; i < n; i++) {
        if (i < items.length) writeInitLocal2(addr + i * es, type.of, items[i], frame);
        else zeroRange(addr + i * es, es);
      }
      return;
    }
    if (type.k === "rec") {
      if (init.k === "expr") { storeValue(addr, type, evalExpr(init.e, frame)); return; }
      const items = (init && init.items) || [];
      type.fields.forEach((f, i) => {
        if (i < items.length) writeInitLocal2(addr + f.off, f.type, items[i], frame);
      });
      return;
    }
    if (type.k === "rec" && type.tag === "union") {
      if (init.k === "expr") { storeValue(addr, type, evalExpr(init.e, frame)); return; }
    }
    if (init.k === "expr") {
      const v = evalExpr(init.e, frame);
      storeValue(addr, type, v);
      return;
    }
    // C++ brace init of a scalar: int b{20}; / int x{}; (zero)
    if (init.items) {
      if (init.items.length) writeInitLocal2(addr, type, init.items[0], frame);
      return;
    }
    err("bad initializer");
  }
  function writeInitLocal2(addr, type, init, frame) {
    if (init.k === "expr") {
      storeValue(addr, type, evalExpr(init.e, frame));
      return;
    }
    writeInit(addr, type, init); // nested brace lists without expressions
  }

  /* ========================= standard library =========================== */

  let jsDepth = 0;
  const BUILTINS = {};

  function defineBuiltin(name, type, fn) {
    const id = fnCount++;
    const addr = FN_BASE + id * 8;
    const spec = { fn, type, fnAddr: addr };
    BUILTINS[name] = spec;
    fnByAddr[addr] = { builtin: spec };
  }

  /* ---- small helpers over memory ---- */

  function readCString(addr, maxLen) {
    if (addr === 0) return "(null)";
    checkAddr(addr, 1, "string read");
    let s = "";
    const limit = maxLen || 4096;
    for (let i = 0; i < limit; i++) {
      const b = mem.u8(addr + i);
      if (b === 0) break;
      s += String.fromCharCode(b);
    }
    return s;
  }

  function writeCString(addr, s) {
    const bytes = [];
    for (const ch of s) bytes.push(ch.charCodeAt(0) & 0xff);
    bytes.push(0);
    mem.setBytes(addr, new Uint8Array(bytes));
    return bytes.length;
  }

  function c_strlen(addr) {
    let n = 0;
    while (mem.u8(addr + n) !== 0) n++;
    return n;
  }

  function argNum(a, line) {
    if (!a || !isArith(a.t) && !isPtr(a.t)) {
      rerr("expected a numeric argument", line);
    }
    return a.v;
  }

  /* ------------------------------ stdio --------------------------------- */

  // the three standard streams live at fixed pseudo-addresses
  const FILE_STDIN = 0x30000000, FILE_STDOUT = 0x30000008, FILE_STDERR = 0x30000010;
  let nextFileSlot = 0;
  const fileRecs = {};

  function newFileRec(name, bytes, mode) {
    const addr = 0x30000100 + (nextFileSlot++) * 8;
    const rec = {
      name, bytes: bytes || new Uint8Array(0), pos: 0, mode,
      read: mode.indexOf("r") !== -1 || mode.indexOf("+") !== -1,
      write: mode.indexOf("w") !== -1 || mode.indexOf("a") !== -1 || mode.indexOf("+") !== -1,
      append: mode.indexOf("a") !== -1,
      eof: false, err: false, closed: false,
    };
    fileRecs[addr] = rec;
    return addr;
  }

  fileRecs[FILE_STDIN] = {
    name: "<stdin>", bytes: new TextEncoder().encode(input), pos: 0,
    mode: "r", read: true, write: false, append: false, eof: false, err: false,
  };
  fileRecs[FILE_STDOUT] = {
    name: "<stdout>", bytes: null, pos: 0, mode: "w",
    read: false, write: true, append: false, eof: false, err: false, isOut: true,
  };
  fileRecs[FILE_STDERR] = {
    name: "<stderr>", bytes: null, pos: 0, mode: "w",
    read: false, write: true, append: false, eof: false, err: false, isOut: true, isErr: true,
  };

  const vfs = {}; // path -> Uint8Array
  vfs["story.txt"] = new TextEncoder().encode(
    "Once upon a time, a small program dreamed of pointers.\n" +
    "It dereferenced carefully, freed every malloc, and never\n" +
    "wrote one byte out of bounds. The other programs laughed\n" +
    "at how cautious it was - right up until the great segfault.\n" +
    "Only our little program was still standing. The end.\n");
  vfs["numbers.txt"] = new TextEncoder().encode("10 20 30 40 50\n");
  vfs["names.txt"] = new TextEncoder().encode("Ada\nGrace\nLinus\nMargaret\n");
  vfs["data.bin"] = new Uint8Array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]);

  function getRec(f, needRead, line) {
    const rec = fileRecs[f];
    if (!rec || rec.closed) rerr("file operations on a closed or invalid FILE*", line);
    if (needRead && !rec.read) rerr("this FILE* was not opened for reading", line);
    return rec;
  }

  function fputcInto(rec, byte) {
    if (rec.isOut) {
      out.text += String.fromCharCode(byte);
      return byte;
    }
    if (rec.append) {
      const nb = new Uint8Array(rec.bytes.length + 1);
      nb.set(rec.bytes); nb[rec.bytes.length] = byte & 0xff;
      rec.bytes = nb; rec.pos = rec.bytes.length;
    } else {
      if (rec.pos >= rec.bytes.length) {
        const nb = new Uint8Array(rec.bytes.length + 1);
        nb.set(rec.bytes); rec.bytes = nb;
      }
      rec.bytes[rec.pos++] = byte & 0xff;
    }
    return byte & 0xff;
  }

  /* printf-family formatting */
  function formatC(fmt, args, argTypes) {
    let outS = "", ai = 0, i = 0;
    function nextArg() { return args[ai++]; }
    while (i < fmt.length) {
      const c = fmt[i++];
      if (c !== "%") { outS += c; continue; }
      if (fmt[i] === "%") { outS += "%"; i++; continue; }
      // flags
      let flags = "";
      while ("-0+ #".indexOf(fmt[i]) !== -1) flags += fmt[i++];
      // width
      let width = 0;
      if (fmt[i] === "*") { width = Math.trunc(argNum(nextArg())); i++; }
      else while (/[0-9]/.test(fmt[i] || "")) width = width * 10 + (+fmt[i++]);
      // precision
      let prec = -1;
      if (fmt[i] === ".") {
        i++; prec = 0;
        if (fmt[i] === "*") { prec = Math.trunc(argNum(nextArg())); i++; }
        else while (/[0-9]/.test(fmt[i] || "")) prec = prec * 10 + (+fmt[i++]);
      }
      // length modifiers
      let len = "";
      while ("hljztL".indexOf(fmt[i]) !== -1) len += fmt[i++];
      const conv = fmt[i++];
      if (!conv) break;

      const pad = (s, w, right) => {
        if (w === 0 || s.length >= w) return s;
        const filler = flags.indexOf("0") !== -1 && right && prec < 0 ? "0" : " ";
        const fill = filler.repeat(w - s.length);
        return right ? fill + s : s + fill;
      };
      const sign = (neg) => neg ? "-" : (flags.indexOf("+") !== -1 ? "+" : flags.indexOf(" ") !== -1 ? " " : "");

      if (conv === "d" || conv === "i") {
        let v = Math.trunc(argNum(nextArg()));
        if (len === "hh") v = ((v & 0xff) << 24) >> 24;
        else if (len === "h") v = ((v & 0xffff) << 16) >> 16;
        const neg = v < 0;
        let digits = String(Math.abs(v));
        if (prec >= 0) digits = digits.padStart(prec, "0");
        outS = outS + pad(sign(neg) + digits, width, flags.indexOf("-") === -1);
      } else if (conv === "u" || conv === "o" || conv === "x" || conv === "X") {
        let v = Math.trunc(argNum(nextArg()));
        let range = 4294967296;
        if (len === "l" || len === "ll" || len === "j" || len === "z" || len === "t") range = 18446744073709551616;
        v = v % range;
        if (v < 0) v = range + v; // exact for the values we can represent
        let digits;
        if (conv === "u") digits = String(v);
        else if (conv === "o") digits = v.toString(8);
        else digits = v.toString(16);
        if (conv === "X") digits = digits.toUpperCase();
        if (prec >= 0) digits = digits.padStart(prec, "0");
        let prefix = "";
        if (flags.indexOf("#") !== -1) {
          if (conv === "x" && v !== 0) prefix = "0x";
          if (conv === "X" && v !== 0) prefix = "0X";
          if (conv === "o" && digits[0] !== "0") prefix = "0";
        }
        outS = outS + pad(prefix + digits, width, flags.indexOf("-") === -1);
      } else if (conv === "c") {
        const v = Math.trunc(argNum(nextArg())) & 0xff;
        outS = outS + pad(String.fromCharCode(v), width, flags.indexOf("-") === -1);
      } else if (conv === "s") {
        const a = nextArg();
        const s = a && isPtr(a.t) || (a && a.t && a.t.k === "arr") ? readCString(a.v) : String(a ? a.v : "");
        let s2 = s;
        if (prec >= 0) s2 = s.slice(0, prec);
        outS = outS + pad(s2, width, flags.indexOf("-") === -1);
      } else if (conv === "p") {
        const a = nextArg();
        const v = (a ? a.v : 0) >>> 0;
        outS = outS + pad("0x" + v.toString(16), width, flags.indexOf("-") === -1);
      } else if (conv === "f" || conv === "F" || conv === "e" || conv === "E" ||
                 conv === "g" || conv === "G") {
        const v = Number(argNum(nextArg()));
        let s;
        if (conv === "f" || conv === "F") {
          const p2 = prec < 0 ? 6 : prec;
          s = v.toFixed(p2);
          if (prec < 0 && flags.indexOf("#") !== -1) s += ""; // keep default
        } else if (conv === "e" || conv === "E") {
          const p2 = prec < 0 ? 6 : prec;
          s = v.toExponential(p2);
          s = s.replace(/e([+-])(\d)$/, "e$10$2");
          if (conv === "E") s = s.toUpperCase();
        } else {
          const p2 = prec < 0 ? 6 : Math.max(1, prec);
          if (v === 0) s = "0";
          else {
            const exp = Math.floor(Math.log10(Math.abs(v)));
            if (exp < -4 || exp >= p2) {
              s = v.toExponential(p2 - 1).replace(/e([+-])(\d)$/, "e$10$2");
              if (flags.indexOf("#") === -1) s = s.replace(/\.?0+e/, "e");
              if (conv === "G") s = s.toUpperCase();
            } else {
              s = String(parseFloat(v.toFixed(Math.max(0, p2 - 1 - exp))));
              if (flags.indexOf("#") !== -1 && s.indexOf(".") === -1) s += ".";
            }
          }
        }
        const neg = v < 0 || Object.is(v, -0);
        if (neg && s[0] !== "-") s = "-" + s;
        if (!neg && (flags.indexOf("+") !== -1 || flags.indexOf(" ") !== -1) && s[0] !== "-") {
          s = (flags.indexOf("+") !== -1 ? "+" : " ") + s;
        }
        outS = outS + pad(s, width, flags.indexOf("-") === -1);
      } else if (conv === "n") {
        err("the %n format specifier is not supported in the sandbox");
      } else {
        outS += "%" + (flags + (width || "") + (prec >= 0 ? "." + prec : "") + len + conv);
      }
    }
    return outS;
  }

  function scanC(fmt, rec, args, argTypes) {
    /* rec: {bytes, pos} source; returns number of conversions */
    let ai = 0, i = 0, matched = 0, any = false;
    const len = rec.bytes.length;
    function peekByte() { return rec.pos < len ? rec.bytes[rec.pos] : -1; }
    function skipWs() { while (peekByte() !== -1 && /\s/.test(String.fromCharCode(peekByte()))) rec.pos++; }
    function target(k) {
      const a = args[ai++];
      return a ? a.v : 0;
    }
    while (i < fmt.length) {
      const c = fmt[i++];
      if (/\s/.test(c)) { skipWs(); continue; }
      if (c !== "%") {
        if (peekByte() === -1) { if (!any) return -1; break; }
        if (String.fromCharCode(peekByte()) !== c) break;
        rec.pos++; continue;
      }
      let suppress = false;
      if (fmt[i] === "*") { suppress = true; i++; }
      let width = 0;
      while (/[0-9]/.test(fmt[i] || "")) width = width * 10 + (+fmt[i++]);
      while ("hljztL".indexOf(fmt[i]) !== -1) i++;
      const conv = fmt[i++];
      if (!conv) break;

      if (conv !== "c" && conv !== "[") skipWs();
      if (conv !== "%" && peekByte() === -1 && !suppress) { if (!any) return -1; break; }

      if (conv === "d" || conv === "i" || conv === "u" || conv === "x" || conv === "o") {
        let j = rec.pos;
        if (conv !== "u" && (String.fromCharCode(peekByte()) === "+" || String.fromCharCode(peekByte()) === "-")) j++;
        if (conv === "x") { if (String.fromCharCode(rec.bytes[j]) === "0" && /[xX]/.test(String.fromCharCode(rec.bytes[j + 1] || 0))) j += 2; while (j < len && /[0-9a-fA-F]/.test(String.fromCharCode(rec.bytes[j]))) j++; }
        else if (conv === "o") { while (j < len && /[0-7]/.test(String.fromCharCode(rec.bytes[j]))) j++; }
        else { while (j < len && /[0-9]/.test(String.fromCharCode(rec.bytes[j]))) j++; }
        if (j === rec.pos || (j === rec.pos + 1 && /[+-]/.test(String.fromCharCode(rec.bytes[rec.pos])))) {
          if (!any) return -1; break;
        }
        const text = String.fromCharCode.apply(null, rec.bytes.slice(rec.pos, j));
        rec.pos = j;
        let v = conv === "x" ? parseInt(text, 16) : conv === "o" ? parseInt(text, 8) : parseInt(text, 10);
        if (!suppress) {
          // size the write by the target's declared type when the call
          // site reveals it (scanf targets are pointers). NOTE: target()
          // has not consumed the argument yet, so the current target's
          // type lives at argTypes[ai] — NOT [ai - 1].
          const at = argTypes && argTypes[ai];
          const pt = at && at.k === "ptr" ? at.to : null;
          const tt = (pt && isIntType(pt)) ? pt : T_LONG();
          memWrite(mem, target(), v, tt);
          matched++; any = true;
        }
      } else if (conv === "f" || conv === "e" || conv === "g" || conv === "a") {
        let j = rec.pos;
        if (String.fromCharCode(peekByte()) === "+" || String.fromCharCode(peekByte()) === "-") j++;
        let sawDigit = false;
        while (j < len && /[0-9]/.test(String.fromCharCode(rec.bytes[j]))) { j++; sawDigit = true; }
        if (String.fromCharCode(rec.bytes[j]) === ".") { j++; while (j < len && /[0-9]/.test(String.fromCharCode(rec.bytes[j]))) { j++; sawDigit = true; } }
        if (/[eE]/.test(String.fromCharCode(rec.bytes[j] || 0))) { j++; if (/[+-]/.test(String.fromCharCode(rec.bytes[j] || 0))) j++; while (j < len && /[0-9]/.test(String.fromCharCode(rec.bytes[j]))) { j++; sawDigit = true; } }
        if (!sawDigit) { if (!any) return -1; break; }
        const text = String.fromCharCode.apply(null, rec.bytes.slice(rec.pos, j));
        rec.pos = j;
        if (!suppress) {
          const at = argTypes && argTypes[ai]; // target not consumed yet
          const pt = at && at.k === "ptr" ? at.to : null;
          const t = target();
          if (pt && isFloatType(pt) && pt.size === 4) mem.f32(t, parseFloat(text));
          else mem.f64(t, parseFloat(text));
          matched++; any = true;
        }
      } else if (conv === "s") {
        let j = rec.pos;
        while (j < len && !/\s/.test(String.fromCharCode(rec.bytes[j]))) j++;
        if (j === rec.pos) { if (!any) return -1; break; }
        const text = String.fromCharCode.apply(null, rec.bytes.slice(rec.pos, j));
        rec.pos = j;
        if (!suppress) {
          const t = target();
          const bound = bufferBound(argTypes && argTypes[ai - 1]);
          writeCStringBounded(t, text, bound);
          matched++; any = true;
        }
      } else if (conv === "c") {
        if (peekByte() === -1) { if (!any) return -1; break; }
        const n = width || 1;
        let text = "";
        for (let k = 0; k < n && peekByte() !== -1; k++) {
          text += String.fromCharCode(rec.bytes[rec.pos++]);
        }
        if (!suppress) {
          const t = target();
          for (let k = 0; k < text.length; k++) mem.u8(t + k, text.charCodeAt(k));
          matched++; any = true;
        }
      } else if (conv === "[") {
        let negate = false;
        if (fmt[i] === "^") { negate = true; i++; }
        let set = "";
        if (fmt[i] === "]") { set += "]"; i++; }
        while (i < fmt.length && fmt[i] !== "]") set += fmt[i++];
        i++; // closing ]
        const rx = new RegExp(negate ? "[^" + escapeSet(set) + "]" : "[" + escapeSet(set) + "]");
        let j = rec.pos, text = "";
        while (j < len && rx.test(String.fromCharCode(rec.bytes[j]))) { text += String.fromCharCode(rec.bytes[j]); j++; }
        if (!text) { if (!any) return -1; break; }
        rec.pos = j;
        if (!suppress) {
          const t = target();
          const bound = bufferBound(argTypes && argTypes[ai - 1]);
          writeCStringBounded(t, text, bound);
          matched++; any = true;
        }
      } else if (conv === "%") {
        skipWs();
        if (String.fromCharCode(peekByte()) === "%") rec.pos++;
      }
      void suppress;
    }
    return matched;
  }

  function escapeSet(s) {
    return s.replace(/\\/g, "\\\\").replace(/\]/g, "\\]").replace(/\^/g, "\\^").replace(/-/g, "\\-");
  }

  /* how many bytes may scanf write into this pointer target? */
  function bufferBound(t) {
    try {
      if (!t) return 4096;
      if (t.k === "ptr" && t.to && t.to.k === "int" && t.to.size === 1) return 4096;
      if (t.k === "arr" && t.of && t.of.k === "int" && t.of.size === 1) {
        return t.n !== null ? t.n : 4096;
      }
      if (t.k === "ptr" && t.to && t.to.k === "arr" && t.to.n !== null) return t.to.n;
    } catch (e) { /* fall through */ }
    return 4096;
  }

  function writeCStringBounded(addr, s, bound) {
    const max = Math.max(0, (bound || 4096) - 1);
    const clipped = s.slice(0, max);
    writeCString(addr, clipped);
  }

  /* ------------------------------ stdlib -------------------------------- */

  let randState = 1;
  function c_rand() {
    // a simple LCG with glibc-like constants; deterministic per run
    randState = (1103515245 * randState + 12345) % 2147483648;
    return randState;
  }

  const EXIT_SIG = { exit: true };

  function doExit(code) {
    // run atexit handlers in reverse registration order
    while (atexitFns.length) {
      const fnAddr = atexitFns.pop();
      try {
        const target = fnByAddr[fnAddr];
        if (target && target.user) {
          runUserFunction(target.user, [], target.user.type.params, null, 0);
        }
      } catch (e) { /* an atexit crash must not stop the exit */ }
    }
    exitCode = code;
    throw EXIT_SIG;
  }

  defineBuiltin("malloc", T_VOIDPTR(), (args) => {
    const size = Math.max(1, Math.trunc(argNum(args[0])));
    if (size > STACK_LIMIT) rerr("malloc of " + size + " bytes is too large for the sandbox");
    return { v: heapAlloc(size, 16), t: T_VOIDPTR() };
  });
  defineBuiltin("calloc", T_VOIDPTR(), (args) => {
    const n = Math.trunc(argNum(args[0])), sz = Math.trunc(argNum(args[1]));
    const size = Math.max(1, n * sz);
    const addr = heapAlloc(size, 16);
    zeroRange(addr, size);
    return { v: addr, t: T_VOIDPTR() };
  });
  defineBuiltin("realloc", T_VOIDPTR(), (args) => {
    const old = argNum(args[0]);
    const size = Math.max(1, Math.trunc(argNum(args[1])));
    const addr = heapAlloc(size, 16);
    zeroRange(addr, size);
    if (old) {
      // the sandbox cannot know the old block's size; it keeps whole pages.
      // copy what is plausibly there (up to the new size) — good enough for
      // the realloc() lesson patterns, which grow a block they just filled.
      const oldStart = findOldBlockSize(old);
      const n = Math.min(size, oldStart);
      mem.setBytes(addr, mem.getBytes(old, n));
    }
    return { v: addr, t: T_VOIDPTR() };
  });
  function findOldBlockSize(old) {
    // blocks are bump-allocated; the "old size" is the distance to the next
    // allocated block or the current heap top
    let end = heapPtr;
    for (const a of Object.keys(fileRecs)) { void a; }
    return Math.max(0, Math.min(end - old, 1 << 20));
  }
  defineBuiltin("free", { k: "void" }, () => ({ v: 0, t: { k: "void" } }));

  defineBuiltin("exit", { k: "void" }, (args) => { doExit(Math.trunc(argNum(args[0])) & 0xff); });
  defineBuiltin("_Exit", { k: "void" }, (args) => { exitCode = Math.trunc(argNum(args[0])) & 0xff; throw EXIT_SIG; });
  defineBuiltin("_exit", { k: "void" }, (args) => { exitCode = Math.trunc(argNum(args[0])) & 0xff; throw EXIT_SIG; });
  defineBuiltin("quick_exit", { k: "void" }, (args) => { exitCode = Math.trunc(argNum(args[0])) & 0xff; throw EXIT_SIG; });
  defineBuiltin("abort", { k: "void" }, () => {
    out.text += "Aborted (core dumped)\n";
    exitCode = 134;
    EXIT_SIG.errorMsg = "program aborted";
    throw EXIT_SIG;
  });
  defineBuiltin("atexit", T_INT(), (args) => {
    if (args[0] && args[0].v >= FN_BASE) { atexitFns.push(args[0].v); return { v: 0, t: T_INT() }; }
    return { v: -1, t: T_INT() };
  });
  defineBuiltin("abs", T_INT(), (args) => ({ v: Math.abs(Math.trunc(argNum(args[0]))), t: T_INT() }));
  defineBuiltin("labs", T_LONG(), (args) => ({ v: Math.abs(Math.trunc(argNum(args[0]))), t: T_LONG() }));
  defineBuiltin("llabs", T_LLONG(), (args) => ({ v: Math.abs(Math.trunc(argNum(args[0]))), t: T_LLONG() }));
  defineBuiltin("atoi", T_INT(), (args) => {
    const s = readCString(argNum(args[0]));
    const m = s.match(/^\s*[+-]?\d+/);
    return { v: m ? parseInt(m[0], 10) : 0, t: T_INT() };
  });
  defineBuiltin("atol", T_LONG(), (args) => BUILTINS["atoi"].fn(args));
  defineBuiltin("atof", T_DOUBLE(), (args) => {
    const s = readCString(argNum(args[0]));
    const m = s.match(/^\s*[+-]?(\d+\.?\d*|\.\d+)([eE][+-]?\d+)?/);
    return { v: m ? parseFloat(m[0]) : 0, t: T_DOUBLE() };
  });
  defineBuiltin("strtol", T_LONG(), (args) => {
    const s = readCString(argNum(args[0]));
    // strtol(str, endptr, base) — the base is the THIRD argument
    const base = args[2] && args[2].v ? Math.trunc(argNum(args[2])) : 10;
    const m = base === 10 ? s.match(/^\s*[+-]?\d+/) : s.match(/^\s*(0[xX][0-9a-fA-F]+|[0-9a-fA-F]+)/);
    if (!m) return { v: 0, t: T_LONG() };
    if (args[1] && args[1].v) memWrite(mem, argNum(args[1]), 0, T_LONG());
    return { v: parseInt(m[0].trim(), base), t: T_LONG() };
  });
  defineBuiltin("strtod", T_DOUBLE(), (args) => {
    const s = readCString(argNum(args[0]));
    const m = s.match(/^\s*[+-]?(\d+\.?\d*|\.\d+)([eE][+-]?\d+)?/);
    if (args[1]) memWrite(mem, argNum(args[1]), 0, T_INT());
    return { v: m ? parseFloat(m[0]) : 0, t: T_DOUBLE() };
  });
  defineBuiltin("rand", T_INT(), () => ({ v: c_rand(), t: T_INT() }));
  defineBuiltin("srand", { k: "void" }, (args) => {
    randState = (Math.trunc(argNum(args[0])) % 2147483648 + 2147483648) % 2147483648 || 1;
    return { v: 0, t: { k: "void" } };
  });
  defineBuiltin("getenv", { k: "ptr", to: T_CHAR() }, (args) => {
    const name = readCString(argNum(args[0]));
    // the sandbox has no real environment; expose a couple of sane values
    const fake = { LANG: "C.UTF-8", PATH: "/sandbox/bin", HOME: "/sandbox", USER: "sandbox" };
    if (fake[name] !== undefined) return { v: addLiteral(fake[name]), t: { k: "ptr", to: T_CHAR() } };
    return { v: 0, t: { k: "ptr", to: T_CHAR() } };
  });
  defineBuiltin("system", T_INT(), () => {
    rerr("system() cannot run shell commands inside a browser sandbox");
  });

  function cmpInvoke(cmpAddr, a, b, size, line) {
    const target = fnByAddr[cmpAddr];
    if (!target) rerr("bad comparison function pointer", line);
    const pa = heapAlloc(size, 8), pb = heapAlloc(size, 8);
    mem.setBytes(pa, mem.getBytes(a, size));
    mem.setBytes(pb, mem.getBytes(b, size));
    let r;
    if (target.builtin) {
      r = target.builtin.fn([{ v: pa, t: T_VOIDPTR() }, { v: pb, t: T_VOIDPTR() }], null, { line });
    } else {
      const decl = target.user;
      r = runUserFunction(decl,
        [{ v: pa, t: T_VOIDPTR() }, { v: pb, t: T_VOIDPTR() }],
        decl.type.params, null, line);
    }
    return Math.trunc(r.v);
  }

  defineBuiltin("qsort", { k: "void" }, (args, frame, e) => {
    const base = argNum(args[0]);
    const n = Math.trunc(argNum(args[1]));
    const size = Math.trunc(argNum(args[2]));
    const cmpAddr = argNum(args[3]);
    const idx = Array.from({ length: n }, (_, i) => i);
    idx.sort((a, b) => cmpInvoke(cmpAddr, base + a * size, base + b * size, size, e.line));
    const tmp = heapAlloc(Math.max(1, n * size), 8);
    idx.forEach((old, i) => mem.setBytes(tmp + i * size, mem.getBytes(base + old * size, size)));
    mem.setBytes(base, mem.getBytes(tmp, n * size));
    return { v: 0, t: { k: "void" } };
  });
  defineBuiltin("bsearch", T_VOIDPTR(), (args, frame, e) => {
    const key = argNum(args[0]);
    const base = argNum(args[1]);
    const n = Math.trunc(argNum(args[2]));
    const size = Math.trunc(argNum(args[3]));
    const cmpAddr = argNum(args[4]);
    let lo = 0, hi = n - 1;
    while (lo <= hi) {
      const mid = (lo + hi) >> 1;
      const c = cmpInvoke(cmpAddr, key, base + mid * size, size, e.line);
      if (c === 0) return { v: base + mid * size, t: T_VOIDPTR() };
      if (c < 0) hi = mid - 1; else lo = mid + 1;
    }
    return { v: 0, t: T_VOIDPTR() };
  });

  /* ------------------------------ string.h ------------------------------ */

  defineBuiltin("strlen", T_SIZET(), (args) => ({ v: c_strlen(argNum(args[0])), t: T_SIZET() }));
  defineBuiltin("strcpy", { k: "ptr", to: T_CHAR() }, (args) => {
    const dst = argNum(args[0]), src = argNum(args[1]);
    const n = c_strlen(src) + 1;
    mem.setBytes(dst, mem.getBytes(src, n));
    return { v: dst, t: { k: "ptr", to: T_CHAR() } };
  });
  defineBuiltin("strncpy", { k: "ptr", to: T_CHAR() }, (args) => {
    const dst = argNum(args[0]), src = argNum(args[1]);
    const n = Math.trunc(argNum(args[2]));
    const sl = c_strlen(src);
    for (let i = 0; i < n; i++) {
      mem.u8(dst + i, i < sl ? mem.u8(src + i) : 0);
    }
    return { v: dst, t: { k: "ptr", to: T_CHAR() } };
  });
  defineBuiltin("strcat", { k: "ptr", to: T_CHAR() }, (args) => {
    const dst = argNum(args[0]), src = argNum(args[1]);
    const dl = c_strlen(dst), sl = c_strlen(src) + 1;
    mem.setBytes(dst + dl, mem.getBytes(src, sl));
    return { v: dst, t: { k: "ptr", to: T_CHAR() } };
  });
  defineBuiltin("strncat", { k: "ptr", to: T_CHAR() }, (args) => {
    const dst = argNum(args[0]), src = argNum(args[1]);
    const n = Math.trunc(argNum(args[2]));
    const dl = c_strlen(dst);
    let k = 0;
    for (; k < n && mem.u8(src + k) !== 0; k++) mem.u8(dst + dl + k, mem.u8(src + k));
    mem.u8(dst + dl + k, 0);
    return { v: dst, t: { k: "ptr", to: T_CHAR() } };
  });
  function memcmpBytes(a, b, n) {
    for (let i = 0; i < n; i++) {
      const x = mem.u8(a + i), y = mem.u8(b + i);
      if (x !== y) return x < y ? -1 : 1;
    }
    return 0;
  }
  defineBuiltin("strcmp", T_INT(), (args) => {
    const a = argNum(args[0]), b = argNum(args[1]);
    let i = 0;
    for (;;) {
      const x = mem.u8(a + i), y = mem.u8(b + i);
      if (x !== y) return { v: x < y ? -1 : 1, t: T_INT() };
      if (x === 0) return { v: 0, t: T_INT() };
      i++;
    }
  });
  defineBuiltin("strncmp", T_INT(), (args) => {
    const a = argNum(args[0]), b = argNum(args[1]);
    const n = Math.trunc(argNum(args[2]));
    for (let i = 0; i < n; i++) {
      const x = mem.u8(a + i), y = mem.u8(b + i);
      if (x !== y) return { v: x < y ? -1 : 1, t: T_INT() };
      if (x === 0) break;
    }
    return { v: 0, t: T_INT() };
  });
  defineBuiltin("strchr", { k: "ptr", to: T_CHAR() }, (args) => {
    const a = argNum(args[0]);
    const c = Math.trunc(argNum(args[1])) & 0xff;
    let i = 0;
    for (;;) {
      const x = mem.u8(a + i);
      if (x === c) return { v: a + i, t: { k: "ptr", to: T_CHAR() } };
      if (x === 0) return { v: 0, t: { k: "ptr", to: T_CHAR() } };
      i++;
    }
  });
  defineBuiltin("strrchr", { k: "ptr", to: T_CHAR() }, (args) => {
    const a = argNum(args[0]);
    const c = Math.trunc(argNum(args[1])) & 0xff;
    let found = 0;
    for (let i = 0; ; i++) {
      const x = mem.u8(a + i);
      if (x === c) found = a + i;
      if (x === 0) break;
    }
    return { v: found, t: { k: "ptr", to: T_CHAR() } };
  });
  defineBuiltin("strstr", { k: "ptr", to: T_CHAR() }, (args) => {
    const hay = readCString(argNum(args[0]));
    const needle = readCString(argNum(args[1]));
    const idx = hay.indexOf(needle);
    return { v: idx < 0 ? 0 : argNum(args[0]) + idx, t: { k: "ptr", to: T_CHAR() } };
  });
  defineBuiltin("strdup", { k: "ptr", to: T_CHAR() }, (args) => {
    const src = argNum(args[0]);
    const n = c_strlen(src) + 1;
    const dst = heapAlloc(n, 8);
    mem.setBytes(dst, mem.getBytes(src, n));
    return { v: dst, t: { k: "ptr", to: T_CHAR() } };
  });
  defineBuiltin("strspn", T_SIZET(), (args) => {
    const s = readCString(argNum(args[0])), set = readCString(argNum(args[1]));
    let i = 0;
    while (i < s.length && set.indexOf(s[i]) !== -1) i++;
    return { v: i, t: T_SIZET() };
  });
  defineBuiltin("strcspn", T_SIZET(), (args) => {
    const s = readCString(argNum(args[0])), set = readCString(argNum(args[1]));
    let i = 0;
    while (i < s.length && set.indexOf(s[i]) === -1) i++;
    return { v: i, t: T_SIZET() };
  });
  defineBuiltin("strpbrk", { k: "ptr", to: T_CHAR() }, (args) => {
    const s = readCString(argNum(args[0])), set = readCString(argNum(args[1]));
    for (let i = 0; i < s.length; i++) {
      if (set.indexOf(s[i]) !== -1) return { v: argNum(args[0]) + i, t: { k: "ptr", to: T_CHAR() } };
    }
    return { v: 0, t: { k: "ptr", to: T_CHAR() } };
  });
  defineBuiltin("strtok", { k: "ptr", to: T_CHAR() }, (args) => {
    let strAddr = argNum(args[0]);
    const set = readCString(argNum(args[1]));
    if (strAddr) strtokState.ptr = strAddr;
    if (!strtokState.ptr) return { v: 0, t: { k: "ptr", to: T_CHAR() } };
    let p = strtokState.ptr;
    while (mem.u8(p) !== 0 && set.indexOf(String.fromCharCode(mem.u8(p))) !== -1) p++;
    if (mem.u8(p) === 0) { strtokState.ptr = 0; return { v: 0, t: { k: "ptr", to: T_CHAR() } }; }
    const start = p;
    while (mem.u8(p) !== 0 && set.indexOf(String.fromCharCode(mem.u8(p))) === -1) p++;
    if (mem.u8(p) !== 0) { mem.u8(p, 0); p++; }
    strtokState.ptr = p;
    return { v: start, t: { k: "ptr", to: T_CHAR() } };
  });
  const strtokState = { ptr: 0 };
  defineBuiltin("memcpy", T_VOIDPTR(), (args) => {
    const dst = argNum(args[0]), src = argNum(args[1]), n = Math.trunc(argNum(args[2]));
    checkAddr(dst, n, "memcpy destination");
    checkAddr(src, n, "memcpy source");
    mem.setBytes(dst, mem.getBytes(src, n));
    return { v: dst, t: T_VOIDPTR() };
  });
  defineBuiltin("memmove", T_VOIDPTR(), (args) => BUILTINS["memcpy"].fn(args));
  defineBuiltin("memset", T_VOIDPTR(), (args) => {
    const dst = argNum(args[0]), c = Math.trunc(argNum(args[1])) & 0xff;
    const n = Math.trunc(argNum(args[2]));
    checkAddr(dst, n, "memset destination");
    mem.bytes.fill(c, dst, dst + n);
    return { v: dst, t: T_VOIDPTR() };
  });
  defineBuiltin("memcmp", T_INT(), (args) => {
    const r = memcmpBytes(argNum(args[0]), argNum(args[1]), Math.trunc(argNum(args[2])));
    return { v: r, t: T_INT() };
  });

  /* ------------------------------- ctype -------------------------------- */

  function charArg(a) { return Math.trunc(argNum(a)) & 0xff; }
  defineBuiltin("isalpha", T_INT(), (a) => ({ v: /[a-zA-Z]/.test(String.fromCharCode(charArg(a[0]))) ? 1 : 0, t: T_INT() }));
  defineBuiltin("isdigit", T_INT(), (a) => ({ v: /[0-9]/.test(String.fromCharCode(charArg(a[0]))) ? 1 : 0, t: T_INT() }));
  defineBuiltin("isalnum", T_INT(), (a) => ({ v: /[a-zA-Z0-9]/.test(String.fromCharCode(charArg(a[0]))) ? 1 : 0, t: T_INT() }));
  defineBuiltin("isspace", T_INT(), (a) => ({ v: /\s/.test(String.fromCharCode(charArg(a[0]))) ? 1 : 0, t: T_INT() }));
  defineBuiltin("isupper", T_INT(), (a) => ({ v: /[A-Z]/.test(String.fromCharCode(charArg(a[0]))) ? 1 : 0, t: T_INT() }));
  defineBuiltin("islower", T_INT(), (a) => ({ v: /[a-z]/.test(String.fromCharCode(charArg(a[0]))) ? 1 : 0, t: T_INT() }));
  defineBuiltin("ispunct", T_INT(), (a) => ({ v: /[!-\/:-@\[-`{-~]/.test(String.fromCharCode(charArg(a[0]))) ? 1 : 0, t: T_INT() }));
  defineBuiltin("isprint", T_INT(), (a) => ({ v: charArg(a[0]) >= 32 && charArg(a[0]) < 127 ? 1 : 0, t: T_INT() }));
  defineBuiltin("isgraph", T_INT(), (a) => ({ v: charArg(a[0]) > 32 && charArg(a[0]) < 127 ? 1 : 0, t: T_INT() }));
  defineBuiltin("iscntrl", T_INT(), (a) => ({ v: charArg(a[0]) < 32 || charArg(a[0]) === 127 ? 1 : 0, t: T_INT() }));
  defineBuiltin("isxdigit", T_INT(), (a) => ({ v: /[0-9a-fA-F]/.test(String.fromCharCode(charArg(a[0]))) ? 1 : 0, t: T_INT() }));
  defineBuiltin("tolower", T_INT(), (a) => ({ v: String.fromCharCode(charArg(a[0])).toLowerCase().charCodeAt(0), t: T_INT() }));
  defineBuiltin("toupper", T_INT(), (a) => ({ v: String.fromCharCode(charArg(a[0])).toUpperCase().charCodeAt(0), t: T_INT() }));

  /* -------------------------------- math -------------------------------- */

  const MATH1 = {
    sin: Math.sin, cos: Math.cos, tan: Math.tan,
    asin: Math.asin, acos: Math.acos, atan: Math.atan,
    sinh: Math.sinh, cosh: Math.cosh, tanh: Math.tanh,
    exp: Math.exp, log: Math.log, log10: Math.log10, log2: Math.log2,
    sqrt: Math.sqrt, floor: Math.floor, ceil: Math.ceil,
    fabs: Math.abs, round: Math.round, trunc: Math.trunc,
    cbrt: Math.cbrt, expm1: Math.expm1, log1p: Math.log1p,
  };
  for (const name of Object.keys(MATH1)) {
    defineBuiltin(name, T_DOUBLE(), (args) => ({ v: MATH1[name](Number(argNum(args[0]))), t: T_DOUBLE() }));
  }
  defineBuiltin("atan2", T_DOUBLE(), (a) => ({ v: Math.atan2(Number(argNum(a[0])), Number(argNum(a[1]))), t: T_DOUBLE() }));
  defineBuiltin("pow", T_DOUBLE(), (a) => ({ v: Math.pow(Number(argNum(a[0])), Number(argNum(a[1]))), t: T_DOUBLE() }));
  defineBuiltin("fmod", T_DOUBLE(), (a) => ({ v: Number(argNum(a[0])) % Number(argNum(a[1])), t: T_DOUBLE() }));
  defineBuiltin("fmin", T_DOUBLE(), (a) => ({ v: Math.min(Number(argNum(a[0])), Number(argNum(a[1]))), t: T_DOUBLE() }));
  defineBuiltin("fmax", T_DOUBLE(), (a) => ({ v: Math.max(Number(argNum(a[0])), Number(argNum(a[1]))), t: T_DOUBLE() }));
  defineBuiltin("hypot", T_DOUBLE(), (a) => ({ v: Math.hypot(Number(argNum(a[0])), Number(argNum(a[1]))), t: T_DOUBLE() }));

  /* -------------------------------- stdio -------------------------------- */

  defineBuiltin("printf", T_INT(), (args) => {
    const fmt = readCString(argNum(args[0]));
    out.text += formatC(fmt, args.slice(1));
    return { v: out.text.length, t: T_INT() };
  });
  defineBuiltin("fprintf", T_INT(), (args) => {
    const rec = getRec(argNum(args[0]), false);
    const fmt = readCString(argNum(args[1]));
    const s = formatC(fmt, args.slice(2));
    if (rec.isOut) out.text += s;
    else if (rec.write) for (let i = 0; i < s.length; i++) fputcInto(rec, s.charCodeAt(i));
    else rerr("fprintf on a FILE* not opened for writing");
    return { v: s.length, t: T_INT() };
  });
  defineBuiltin("sprintf", T_INT(), (args) => {
    const buf = argNum(args[0]);
    const fmt = readCString(argNum(args[1]));
    const s = formatC(fmt, args.slice(2));
    writeCString(buf, s);
    return { v: s.length, t: T_INT() };
  });
  defineBuiltin("snprintf", T_INT(), (args) => {
    const buf = argNum(args[0]);
    const size = Math.trunc(argNum(args[1]));
    const fmt = readCString(argNum(args[2]));
    const s = formatC(fmt, args.slice(3)).slice(0, Math.max(0, size - 1));
    writeCString(buf, s);
    return { v: s.length, t: T_INT() };
  });
  defineBuiltin("puts", T_INT(), (args) => {
    out.text += readCString(argNum(args[0])) + "\n";
    return { v: 1, t: T_INT() };
  });
  defineBuiltin("putchar", T_INT(), (args) => {
    const c = Math.trunc(argNum(args[0])) & 0xff;
    out.text += String.fromCharCode(c);
    return { v: c, t: T_INT() };
  });
  defineBuiltin("fputs", T_INT(), (args) => {
    const rec = getRec(argNum(args[1]), false);
    const s = readCString(argNum(args[0]));
    if (rec.isOut) out.text += s;
    else if (rec.write) for (let i = 0; i < s.length; i++) fputcInto(rec, s.charCodeAt(i));
    else rerr("fputs on a FILE* not opened for writing");
    return { v: 1, t: T_INT() };
  });
  defineBuiltin("fputc", T_INT(), (args) => {
    const rec = getRec(argNum(args[1]), false);
    return { v: fputcInto(rec, Math.trunc(argNum(args[0])) & 0xff), t: T_INT() };
  });
  defineBuiltin("putc", T_INT(), (args) => BUILTINS["fputc"].fn(args));

  function stdinByte() {
    const rec = fileRecs[FILE_STDIN];
    if (rec.pushback !== undefined) { const b = rec.pushback; rec.pushback = undefined; return b; }
    if (rec.pos >= rec.bytes.length) return -1;
    return rec.bytes[rec.pos++];
  }
  defineBuiltin("getchar", T_INT(), () => ({ v: stdinByte(), t: T_INT() }));
  defineBuiltin("getc", T_INT(), (args) => {
    const rec = getRec(argNum(args[0]), true);
    if (rec.addr === FILE_STDIN || rec === fileRecs[FILE_STDIN]) return { v: stdinByte(), t: T_INT() };
    if (rec.pos >= rec.bytes.length) { rec.eof = true; return { v: -1, t: T_INT() }; }
    return { v: rec.bytes[rec.pos++], t: T_INT() };
  });
  defineBuiltin("fgetc", T_INT(), (args) => BUILTINS["getc"].fn(args));
  defineBuiltin("ungetc", T_INT(), (args) => {
    const rec = getRec(argNum(args[1]), true);
    rec.pushback = Math.trunc(argNum(args[0])) & 0xff;
    return { v: rec.pushback, t: T_INT() };
  });
  defineBuiltin("fgets", { k: "ptr", to: T_CHAR() }, (args) => {
    const buf = argNum(args[0]);
    const n = Math.trunc(argNum(args[1]));
    const rec = getRec(argNum(args[2]), true);
    let s = "";
    while (s.length < n - 1) {
      let b;
      if (rec === fileRecs[FILE_STDIN]) { b = stdinByte(); }
      else { b = rec.pos < rec.bytes.length ? rec.bytes[rec.pos++] : -1; }
      if (b === -1) break;
      s += String.fromCharCode(b);
      if (b === 10) break;
    }
    if (!s.length) { rec.eof = true; return { v: 0, t: { k: "ptr", to: T_CHAR() } }; }
    writeCString(buf, s);
    return { v: buf, t: { k: "ptr", to: T_CHAR() } };
  });
  defineBuiltin("gets", { k: "ptr", to: T_CHAR() }, () => {
    rerr("gets() is unsafe and is not supported — use fgets() instead");
  });

  defineBuiltin("scanf", T_INT(), (args, frame, e) => {
    const fmt = readCString(argNum(args[0]));
    const rec = fileRecs[FILE_STDIN];
    const targets = args.slice(1);
    const types = e.args.slice(1).map((n) => { try { return inferType(n, frame); } catch (e2) { return null; } });
    return { v: scanC(fmt, rec, targets, types), t: T_INT() };
  });
  defineBuiltin("fscanf", T_INT(), (args, frame, e) => {
    const rec = getRec(argNum(args[0]), true);
    const fmt = readCString(argNum(args[1]));
    const targets = args.slice(2);
    const types = e.args.slice(2).map((n) => { try { return inferType(n, frame); } catch (e2) { return null; } });
    return { v: scanC(fmt, rec, targets, types), t: T_INT() };
  });
  defineBuiltin("sscanf", T_INT(), (args, frame, e) => {
    const str = readCString(argNum(args[0]));
    const fmt = readCString(argNum(args[1]));
    const targets = args.slice(2);
    const types = e.args.slice(2).map((n) => { try { return inferType(n, frame); } catch (e2) { return null; } });
    const rec = { bytes: new TextEncoder().encode(str), pos: 0 };
    return { v: scanC(fmt, rec, targets, types), t: T_INT() };
  });
  defineBuiltin("perror", { k: "void" }, (args) => {
    const s = readCString(argNum(args[0]));
    out.text += s + ": success\n";
    return { v: 0, t: { k: "void" } };
  });
  defineBuiltin("setlocale", { k: "ptr", to: T_CHAR() }, (args) => {
    // the sandbox is always in the "C" locale; setlocale(LC_*, NULL) and
    // any set attempt both report that
    return { v: addLiteral("C"), t: { k: "ptr", to: T_CHAR() } };
  });
  let localeconvAddr = 0;
  defineBuiltin("localeconv", { k: "ptr", to: T_VOIDPTR() }, () => {
    const rec = unit.findRec("struct", "lconv");
    if (!rec) rerr("localeconv() needs #include <locale.h>");
    if (!localeconvAddr) {
      // one static lconv, filled with the classic "C" locale values
      localeconvAddr = heapAlloc(typeSize(rec), typeAlign(rec));
      const set = (name, s) => {
        const fld = rec.fields.find((x) => x.name === name);
        if (fld) memWrite(mem, localeconvAddr + fld.off, addLiteral(s), fld.type);
      };
      set("decimal_point", "."); set("thousands_sep", "");
      set("grouping", ""); set("mon_decimal_point", ".");
      set("mon_thousands_sep", ""); set("mon_grouping", "");
      set("positive_sign", ""); set("negative_sign", "-");
      set("currency_symbol", ""); set("int_curr_symbol", "");
    }
    return { v: localeconvAddr, t: { k: "ptr", to: rec } };
  });
  defineBuiltin("fflush", T_INT(), () => ({ v: 0, t: T_INT() }));
  defineBuiltin("setvbuf", T_INT(), () => ({ v: 0, t: T_INT() }));

  defineBuiltin("fopen", { k: "ptr", to: { k: "rec", tag: "struct", name: "FILE" } }, (args) => {
    const name = readCString(argNum(args[0]));
    const mode = readCString(argNum(args[1]));
    let data = vfs[name];
    const wantsWrite = /^[wab+]/.test(mode) && mode.indexOf("r") !== 0 || mode.indexOf("+") !== -1;
    const wantsRead = mode[0] === "r" || mode.indexOf("+") !== -1;
    if (mode[0] === "r" && mode.indexOf("+") === -1 && !data) {
      return { v: 0, t: { k: "ptr", to: unit.findRec("struct", "FILE") || T_INT() } };
    }
    if (mode[0] === "w") data = new Uint8Array(0);
    if (mode[0] === "a" && data) data = data.slice(0);
    if (!data) data = new Uint8Array(0);
    const rec = {
      name, bytes: data, pos: mode[0] === "a" ? data.length : 0, mode,
      read: wantsRead, write: wantsWrite || mode[0] === "w" || mode[0] === "a",
      append: mode[0] === "a", eof: false, err: false, closed: false,
      inVfs: vfs[name] === data || mode[0] === "w" || mode[0] === "a",
    };
    const addr = newFileRec("", data, mode);
    fileRecs[addr] = rec;
    rec.sync = () => { vfs[name] = rec.bytes; };
    return { v: addr, t: { k: "ptr", to: unit.findRec("struct", "FILE") } };
  });
  defineBuiltin("fclose", T_INT(), (args) => {
    const f = argNum(args[0]);
    const rec = fileRecs[f];
    if (rec && rec.sync) rec.sync();
    if (rec) rec.closed = true;
    delete fileRecs[f];
    return { v: 0, t: T_INT() };
  });
  defineBuiltin("fread", T_SIZET(), (args) => {
    const buf = argNum(args[0]);
    const size = Math.trunc(argNum(args[1]));
    const n = Math.trunc(argNum(args[2]));
    const rec = getRec(argNum(args[3]), true);
    const want = size * n;
    const avail = Math.max(0, rec.bytes.length - rec.pos);
    const got = Math.min(want, avail);
    mem.setBytes(buf, rec.bytes.slice(rec.pos, rec.pos + got));
    rec.pos += got;
    if (got < want) rec.eof = true;
    return { v: size ? Math.floor(got / size) : 0, t: T_SIZET() };
  });
  defineBuiltin("fwrite", T_SIZET(), (args) => {
    const buf = argNum(args[0]);
    const size = Math.trunc(argNum(args[1]));
    const n = Math.trunc(argNum(args[2]));
    const rec = getRec(argNum(args[3]), false);
    const total = size * n;
    const data = mem.getBytes(buf, total);
    if (rec.append) {
      const nb = new Uint8Array(rec.bytes.length + total);
      nb.set(rec.bytes); nb.set(data, rec.bytes.length);
      rec.bytes = nb;
      rec.pos = rec.bytes.length;
    } else {
      const end = rec.pos + total;
      if (end > rec.bytes.length) {
        const nb = new Uint8Array(end);
        nb.set(rec.bytes);
        rec.bytes = nb;
      }
      rec.bytes.set(data, rec.pos);
      rec.pos = end;
    }
    if (rec.sync) rec.sync();
    return { v: n, t: T_SIZET() };
  });
  defineBuiltin("fseek", T_INT(), (args) => {
    const rec = getRec(argNum(args[0]), false);
    const off = Math.trunc(argNum(args[1]));
    const whence = Math.trunc(argNum(args[2]));
    rec.pos = whence === 0 ? off : whence === 1 ? rec.pos + off : rec.bytes.length + off;
    rec.pos = Math.max(0, rec.pos);
    rec.eof = false;
    return { v: 0, t: T_INT() };
  });
  defineBuiltin("ftell", T_LONG(), (args) => {
    const rec = getRec(argNum(args[0]), false);
    return { v: rec.pos, t: T_LONG() };
  });
  defineBuiltin("rewind", { k: "void" }, (args) => {
    const rec = getRec(argNum(args[0]), false);
    rec.pos = 0;
    rec.eof = false;
    return { v: 0, t: { k: "void" } };
  });
  defineBuiltin("feof", T_INT(), (args) => {
    const rec = fileRecs[argNum(args[0])];
    return { v: rec && rec.eof ? 1 : 0, t: T_INT() };
  });
  defineBuiltin("ferror", T_INT(), (args) => {
    const rec = fileRecs[argNum(args[0])];
    return { v: rec && rec.err ? 1 : 0, t: T_INT() };
  });
  defineBuiltin("remove", T_INT(), (args) => {
    delete vfs[readCString(argNum(args[0]))];
    return { v: 0, t: T_INT() };
  });
  defineBuiltin("rename", T_INT(), (args) => {
    const a = readCString(argNum(args[0])), b = readCString(argNum(args[1]));
    if (vfs[a] !== undefined) { vfs[b] = vfs[a]; delete vfs[a]; }
    return { v: 0, t: T_INT() };
  });

  /* ------------------------------ setjmp -------------------------------- */

  defineBuiltin("setjmp", T_INT(), (args, frame) => {
    const bufAddr = argNum(args[0]);
    // second return after a longjmp: replay mode hands back the value
    if (frame && frame.jmpPending && frame.jmpPending[bufAddr] !== undefined) {
      const v = frame.jmpPending[bufAddr];
      delete frame.jmpPending[bufAddr];
      return { v, t: T_INT() };
    }
    const token = jmpTokenSeq++;
    jmpTargets[bufAddr] = token;
    if (frame) {
      if (!frame.setjmps) frame.setjmps = [];
      frame.setjmps.push(token);
    }
    return { v: 0, t: T_INT() };
  });
  defineBuiltin("longjmp", { k: "void" }, (args) => {
    const bufAddr = argNum(args[0]);
    const val = args[1] ? Math.trunc(argNum(args[1])) : 1;
    const token = jmpTargets[bufAddr];
    if (!token) rerr("longjmp() called without a setjmp() on that jmp_buf");
    throw { jmpId: token, val: val === 0 ? 1 : val };
  });

  /* -------------------------------- time -------------------------------- */

  defineBuiltin("time", T_LONG(), (args) => {
    const v = Math.floor(Date.now() / 1000);
    if (args[0] && args[0].v) memWrite(mem, args[0].v, v, T_LONG());
    return { v, t: T_LONG() };
  });
  defineBuiltin("clock", T_LONG(), () => ({ v: Math.floor(performanceNow() * 1000), t: T_LONG() }));
  function performanceNow() {
    return (typeof performance !== "undefined" && performance.now) ? performance.now() : Date.now();
  }
  defineBuiltin("difftime", T_DOUBLE(), (a) => ({ v: Number(argNum(a[0])) - Number(argNum(a[1])), t: T_DOUBLE() }));

  function fillTm(d, utc) {
    const rec = unit.findRec("struct", "tm");
    const addr = heapAlloc(rec.size, 8);
    zeroRange(addr, rec.size);
    const get = utc
      ? { s: d.getUTCSeconds(), m: d.getUTCMinutes(), h: d.getUTCHours(), md: d.getUTCDate(), mo: d.getUTCMonth(), y: d.getUTCFullYear(), wd: d.getUTCDay() }
      : { s: d.getSeconds(), m: d.getMinutes(), h: d.getHours(), md: d.getDate(), mo: d.getMonth(), y: d.getFullYear(), wd: d.getDay() };
    const jan1 = new Date(d.getFullYear(), 0, 1);
    const yday = Math.floor((d - jan1) / 86400000);
    memWrite(mem, addr + 0, get.s, T_INT());
    memWrite(mem, addr + 4, get.m, T_INT());
    memWrite(mem, addr + 8, get.h, T_INT());
    memWrite(mem, addr + 12, get.md, T_INT());
    memWrite(mem, addr + 16, get.mo, T_INT());
    memWrite(mem, addr + 20, get.y - 1900, T_INT());
    memWrite(mem, addr + 24, get.wd, T_INT());
    memWrite(mem, addr + 28, yday, T_INT());
    memWrite(mem, addr + 32, -1, T_INT());
    return addr;
  }
  defineBuiltin("localtime", { k: "ptr", to: { k: "rec", tag: "struct", name: "tm" } }, (args) => {
    const secs = Number(argNum(args[0]));
    return { v: fillTm(new Date(secs * 1000), false), t: { k: "ptr", to: unit.findRec("struct", "tm") } };
  });
  defineBuiltin("gmtime", { k: "ptr", to: { k: "rec", tag: "struct", name: "tm" } }, (args) => {
    const secs = Number(argNum(args[0]));
    return { v: fillTm(new Date(secs * 1000), true), t: { k: "ptr", to: unit.findRec("struct", "tm") } };
  });
  defineBuiltin("mktime", T_LONG(), (args) => {
    const addr = argNum(args[0]);
    const gi = (o) => mem.i32(addr + o);
    const d = new Date(gi(20) + 1900, gi(16), gi(12), gi(8), gi(4), gi(0));
    return { v: Math.floor(d.getTime() / 1000), t: T_LONG() };
  });

  const WDAY = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];
  const MON = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
  const WDAY_FULL = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];
  const MON_FULL = ["January", "February", "March", "April", "May", "June", "July",
    "August", "September", "October", "November", "December"];
  defineBuiltin("strftime", T_SIZET(), (args) => {
    const buf = argNum(args[0]);
    const max = Math.trunc(argNum(args[1]));
    const fmt = readCString(argNum(args[2]));
    const addr = argNum(args[3]);
    const gi = (o) => mem.i32(addr + o);
    const y = gi(20) + 1900, mo = gi(16), md = gi(12), h = gi(8), mi = gi(4), s = gi(0);
    const wd = gi(24), yd = gi(28);
    let outS = "";
    for (let i = 0; i < fmt.length; i++) {
      if (fmt[i] !== "%") { outS += fmt[i]; continue; }
      const c = fmt[++i];
      const p2 = (n) => String(n).padStart(2, "0");
      switch (c) {
        case "Y": outS += y; break;
        case "y": outS += p2(y % 100); break;
        case "m": outS += p2(mo + 1); break;
        case "d": outS += p2(md); break;
        case "H": outS += p2(h); break;
        case "M": outS += p2(mi); break;
        case "S": outS += p2(s); break;
        case "a": outS += WDAY[wd] || "?"; break;
        case "A": outS += WDAY_FULL[wd] || "?"; break;
        case "b": case "h": outS += MON[mo] || "?"; break;
        case "B": outS += MON_FULL[mo] || "?"; break;
        case "p": outS += h < 12 ? "AM" : "PM"; break;
        case "I": outS += p2(((h + 11) % 12) + 1); break;
        case "j": outS += String(yd + 1).padStart(3, "0"); break;
        case "%": outS += "%"; break;
        default: outS += "%" + c;
      }
    }
    writeCStringBounded(buf, outS, max);
    return { v: outS.length, t: T_SIZET() };
  });
  defineBuiltin("timespec_get", T_INT(), (args) => {
    const tsAddr = argNum(args[0]);
    mem.i64(tsAddr, BigInt(Math.floor(Date.now() / 1000)));
    mem.i64(tsAddr + 8, BigInt((Date.now() % 1000) * 1000000));
    return { v: 1, t: T_INT() };
  });

  defineBuiltin("__assert", { k: "void" }, (args) => {
    const cond = args[1] ? readCString(argNum(args[1])) : "?";
    const lineNo = args[2] ? Math.trunc(argNum(args[2])) : 0;
    out.text += "Assertion failed: " + cond + ", file main.c:" + lineNo + "\n";
    exitCode = 134;
    EXIT_SIG.errorMsg = "assertion failed";
    throw EXIT_SIG;
  });
  defineBuiltin("raise", T_INT(), (args) => {
    const sig = Math.trunc(argNum(args[0]));
    rerr("raise(" + sig + ") — real signals need an operating system; " +
         "the browser sandbox cannot deliver them");
  });
  defineBuiltin("signal", { k: "ptr", to: { k: "void" } }, () => {
    rerr("signal handlers need an operating system; the browser sandbox " +
         "cannot deliver real signals");
  });
  defineBuiltin("thrd_create", T_INT(), () => {
    rerr("threads need a real operating system — the browser sandbox is " +
         "single-threaded by design");
  });

  /* stdio stream "variables" (stdin/stdout/stderr) */
  const SPECIAL_VARS = {
    stdin: { v: FILE_STDIN, t: { k: "ptr", to: unit.findRec("struct", "FILE") || T_INT() } },
    stdout: { v: FILE_STDOUT, t: { k: "ptr", to: unit.findRec("struct", "FILE") || T_INT() } },
    stderr: { v: FILE_STDERR, t: { k: "ptr", to: unit.findRec("struct", "FILE") || T_INT() } },
    // C++ layer: singleton stream markers (see binaryValue / evalCall)
    cout: { v: 1, t: T_COUT() },
    cin: { v: 2, t: T_CIN() },
    endl: { v: 10, t: T_ENDL() },
    flush: { v: 0, t: T_ENDL() },
  };

  /* --------------------------- program start ---------------------------- */

  function startMain() {
    const mf = funcs["main"];
    if (!mf) err("no main() function — every C program needs one");
    const decl = mf.decl;
    const params = decl.type.params;
    initGlobals(); // allocate + initialize global variables before main

    // build argv in memory: argv[0] = "main", then extras, then NULL
    const argvNames = ["main"].concat(((opts && opts.argv) || []).slice(1));
    const strAddrs = argvNames.map((n) => addLiteral(n));
    const argvArr = heapAlloc((argvNames.length + 1) * 8, 8);
    for (let i = 0; i < argvNames.length; i++) {
      memWrite(mem, argvArr + i * 8, strAddrs[i], T_VOIDPTR());
    }
    memWrite(mem, argvArr + argvNames.length * 8, 0, T_VOIDPTR());

    let args;
    if (params.length === 0) args = [];
    else if (params.length >= 2) {
      args = [
        { v: argvNames.length, t: T_INT() },
        { v: argvArr, t: { k: "ptr", to: { k: "ptr", to: T_CHAR() } } },
      ];
      if (params.length >= 3) args.push({ v: 0, t: { k: "ptr", to: { k: "void" } } });
    } else {
      args = [{ v: 0, t: T_INT() }];
    }

    let retSlot = null;
    const ret = decl.type.ret;
    if (ret.k === "rec" || ret.k === "arr") {
      retSlot = heapAlloc(typeSize(ret), typeAlign(ret));
    }
    const result = runUserFunction(decl, args, params, retSlot, 0);
    return Math.trunc(result.v) & 0xff;
  }

  /* ------------------------------- the API ------------------------------ */

  function run() {
    let output = "", failed = false, failMsg = "", phase = "runtime", exit = 0;
    try {
      exit = startMain();
    } catch (e) {
      if (e === EXIT_SIG) {
        exit = exitCode;
        if (EXIT_SIG.errorMsg) {
          failed = true;
          failMsg = EXIT_SIG.errorMsg;
          EXIT_SIG.errorMsg = null;
        }
      } else if (e instanceof CErr) {
        failed = true; failMsg = e.message; phase = e.phase; exit = 1;
        if (typeof window !== "undefined") window.CEngine._lastError = e;
      } else {
        failed = true;
        failMsg = String(e && e.message || e);
        if (/stack size exceeded|too much recursion/i.test(failMsg)) {
          failMsg = "stack overflow: recursion went too deep";
        }
        window.CEngine._lastError = e; // dev debugging hook
      }
    }
    output = out.text;
    if (failed) return { ok: false, output, error: failMsg, phase, exit };
    return { ok: true, output, exit };
  }

  return { run, _unit: unit, _mem: mem, _globals: () => globalVars };
}

/* ============================ public export ============================= */

/* A fresh interpreter is created per run, so programs cannot influence
   each other through module state. */

const CE_GLOBAL = (typeof globalThis !== "undefined") ? globalThis
  : (typeof self !== "undefined") ? self : this;

CE_GLOBAL.CEngine = {
  version: "1.0",
  run(source, opts) {
    let engine;
    try {
      engine = createInterp(source, opts || {});
    } catch (e) {
      // compile-time failures (preprocessor, lexer, parser) throw here
      if (typeof window !== "undefined") window.CEngine._lastEngine = null;
      if (e instanceof CErr) {
        return { ok: false, output: "", error: e.message, phase: e.phase, exit: 1 };
      }
      return { ok: false, output: "", error: String(e && e.message || e), phase: "compile", exit: 1 };
    }
    if (typeof window !== "undefined") window.CEngine._lastEngine = engine;
    return engine.run();
  },
};

})();
