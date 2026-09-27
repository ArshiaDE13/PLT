"use strict";

/* Shared in-browser C runner: the CEngine interpreter (cengine.js) inside
   a Web Worker with a kill switch, so a stuck program (infinite loop) is
   killed after RUN_TIMEOUT_MS instead of freezing the page. The engine
   itself is pure JS and ships with the site — nothing is downloaded, and
   startup is instant. Used by both the lesson "Try it" boxes (app.js)
   and the C Playground window (playground-c.js).

   window.CRunner
     .run(code [, input]) -> Promise<{ok, output, err, error}>
         err is null on a normal run, "load" if the engine could not be
         started, or "timeout" if the kill switch fired. Callers map the
         err codes to their own localized messages.
     .status    -> "idle" | "loading" | "ready"
     .addListener(fn)  called on every status change
     .RUN_TIMEOUT_MS  exposed for timeout messages
*/

(function () {
  const RUN_TIMEOUT_MS = 10000;
  const LOAD_TIMEOUT_MS = 20000;

  let cWorker = null;
  let cLoadPromise = null;
  let status = "idle";
  const listeners = [];

  function setStatus(next) {
    status = next;
    listeners.forEach((fn) => {
      try { fn(next); } catch (e) { /* listener bugs must not break runs */ }
    });
  }

  function workerSource(engineJs) {
    // the engine is concatenated into the worker source: blob workers
    // cannot resolve relative importScripts() URLs
    return engineJs + "\n" + [
      "self.onmessage = (e) => {",
      "  try {",
      "    if (e.data.msg === 'load') {",
      "      self.postMessage({ msg: 'loaded' });",
      "    } else if (e.data.msg === 'run') {",
      "      const res = CEngine.run(e.data.code, { input: e.data.input || '' });",
      "      let output = res.output || '';",
      "      if (!res.ok && res.error) {",
      "        output = (output ? output + '\\n' : '') + res.error;",
      "      }",
      "      self.postMessage({",
      "        msg: 'done',",
      "        ok: !!res.ok,",
      "        output: output,",
      "        exit: res.exit !== undefined ? res.exit : null,",
      "      });",
      "    }",
      "  } catch (err) {",
      "    self.postMessage({ msg: 'loadError', error: String((err && err.message) || err) });",
      "  }",
      "};",
    ].join("\n");
  }

  function makeCWorker(engineJs) {
    const url = URL.createObjectURL(
      new Blob([workerSource(engineJs)], { type: "text/javascript" }));
    return new Worker(url);
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

  async function getCWorker() {
    if (cLoadPromise) return cLoadPromise;
    cLoadPromise = (async () => {
      if (typeof CEngine === "undefined") {
        throw new Error("the C engine failed to load");
      }
      // fetch the engine text so it can be concatenated into the worker
      const resp = await fetch("cengine.js");
      if (!resp.ok) throw new Error("cengine.js not found");
      const engineJs = await resp.text();
      const w = makeCWorker(engineJs);
      cWorker = w;
      setStatus("loading");
      const res = await askWorker(w, { msg: "load" }, LOAD_TIMEOUT_MS);
      if (res.msg !== "loaded") {
        w.terminate();
        cWorker = null;
        cLoadPromise = null;
        throw new Error(res.error || "the C engine failed to start");
      }
      setStatus("ready");
      return w;
    })();
    return cLoadPromise;
  }

  function resetCEngine() {
    if (cWorker) {
      try { cWorker.terminate(); } catch (e) { /* non-fatal */ }
      cWorker = null;
    }
    cLoadPromise = null;
    setStatus("idle");
  }

  async function run(code, input) {
    if (!code || !code.trim()) return { ok: true, output: "", err: null };
    let worker;
    try {
      worker = await getCWorker();
    } catch (e) {
      resetCEngine();
      return {
        ok: false, output: "", err: "load",
        error: String((e && e.message) || e),
      };
    }
    try {
      const res = await askWorker(worker, { msg: "run", code, input: input || "" },
        RUN_TIMEOUT_MS);
      return {
        ok: !!res.ok,
        output: res.output || "",
        exit: res.exit,
        err: null,
      };
    } catch (e) {
      resetCEngine(); // the worker may have been killed by the timeout
      return { ok: false, output: "", err: "timeout" };
    }
  }

  window.CRunner = {
    run,
    addListener(fn) { listeners.push(fn); },
    get status() { return status; },
    RUN_TIMEOUT_MS,
  };
})();
