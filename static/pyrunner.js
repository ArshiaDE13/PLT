"use strict";

/* Shared in-browser Python runner: Pyodide (CPython 3.14 → WebAssembly)
   inside a Web Worker, so a stuck program (infinite loop, input()) is
   killed after RUN_TIMEOUT_MS instead of freezing the page. The engine
   (~10 MB) is fetched from a CDN on the first Run click, then cached by
   the browser. Used by both the lesson "Try it" boxes (app.js) and the
   Playground window (playground.js).

   window.PyRunner
     .run(code) -> Promise<{ok, output, err, error}>
         err is null on a normal run, "load" if the engine could not be
         fetched, or "timeout" if the kill switch fired. Callers map the
         err codes to their own localized messages.
     .status    -> "idle" | "loading" | "ready"
     .addListener(fn)  called on every status change
     .RUN_TIMEOUT_MS  exposed for timeout messages
*/

(function () {
  const PYODIDE_VERSION = "v314.0.6";
  const PYODIDE_CDN = "https://cdn.jsdelivr.net/pyodide/" + PYODIDE_VERSION +
    "/full/";
  const RUN_TIMEOUT_MS = 10000;
  const LOAD_TIMEOUT_MS = 60000;

  let pyWorker = null;
  let pyLoadPromise = null;
  let status = "idle";
  const listeners = [];

  function setStatus(next) {
    status = next;
    listeners.forEach((fn) => {
      try { fn(next); } catch (e) { /* listener bugs must not break runs */ }
    });
  }

  function pyWorkerSource() {
    return [
      'import { loadPyodide } from "' + PYODIDE_CDN + 'pyodide.mjs";',
      "let pyodide = null;",
      "self.onmessage = async (e) => {",
      "  try {",
      "    if (e.data.msg === 'load') {",
      "      pyodide = await loadPyodide({ indexURL: '" + PYODIDE_CDN + "' });",
      "      self.postMessage({ msg: 'loaded' });",
      "    } else if (e.data.msg === 'run') {",
      "      let out = '';",
      "      pyodide.setStdout({ batched: (s) => { out += s + '\\n'; } });",
      "      try {",
      "        await pyodide.runPythonAsync(e.data.code);",
      "        self.postMessage({ msg: 'done', ok: true, output: out.replace(/\\n+$/, '') });",
      "      } catch (err) {",
      "        self.postMessage({ msg: 'done', ok: false, output: String((err && err.message) || err) });",
      "      }",
      "    }",
      "  } catch (err) {",
      "    self.postMessage({ msg: 'loadError', error: String((err && err.message) || err) });",
      "  }",
      "};",
    ].join("\n");
  }

  function makePyWorker() {
    // Pyodide 314.x only runs inside a MODULE worker (ESM); the blob itself
    // must still be a plain JS MIME type.
    const url = URL.createObjectURL(
      new Blob([pyWorkerSource()], { type: "text/javascript" }));
    return new Worker(url, { type: "module" });
  }

  function askWorker(worker, msg, timeoutMs) {
    return new Promise((resolve, reject) => {
      const timer = setTimeout(() => {
        cleanup();
        reject(new Error("timeout"));
      }, timeoutMs);
      function onMsg(e) { cleanup(); resolve(e.data); }
      function onErr(err) { cleanup(); reject(err); }
      function cleanup() {
        clearTimeout(timer);
        worker.removeEventListener("message", onMsg);
        worker.removeEventListener("error", onErr);
      }
      worker.addEventListener("message", onMsg);
      worker.addEventListener("error", onErr);
      worker.postMessage(msg);
    });
  }

  async function getPyWorker() {
    if (pyLoadPromise) return pyLoadPromise;
    pyLoadPromise = (async () => {
      const w = makePyWorker();
      pyWorker = w;
      setStatus("loading");
      const res = await askWorker(w, { msg: "load" }, LOAD_TIMEOUT_MS);
      if (res.msg !== "loaded") {
        w.terminate();
        pyWorker = null;
        pyLoadPromise = null;
        throw new Error(res.error || "the Python engine failed to start");
      }
      setStatus("ready");
      return w;
    })();
    return pyLoadPromise;
  }

  function resetPyEngine() {
    if (pyWorker) {
      try { pyWorker.terminate(); } catch (e) { /* non-fatal */ }
      pyWorker = null;
    }
    pyLoadPromise = null;
    setStatus("idle");
  }

  async function run(code) {
    if (!code || !code.trim()) return { ok: true, output: "", err: null };
    let worker;
    try {
      worker = await getPyWorker();
    } catch (e) {
      resetPyEngine();
      return {
        ok: false, output: "", err: "load",
        error: String((e && e.message) || e),
      };
    }
    try {
      const res = await askWorker(worker, { msg: "run", code }, RUN_TIMEOUT_MS);
      return { ok: !!res.ok, output: res.output || "", err: null };
    } catch (e) {
      resetPyEngine(); // the worker may have been killed by the timeout
      return { ok: false, output: "", err: "timeout" };
    }
  }

  window.PyRunner = {
    run,
    addListener(fn) { listeners.push(fn); },
    get status() { return status; },
    RUN_TIMEOUT_MS,
  };
})();
