"use strict";

/* Shared in-browser C runner for the C course.
   The CEngine interpreter ships with the site as a plain <script>
   (cengine.js), so there is NOTHING to fetch and nothing to download:
   runs work on any host, including file:// previews.

   Long-running programs are bounded by the engine's built-in step limit
   (maxSteps), which stops infinite loops in about a second — the same
   job the Pyodide worker's kill switch does for Python.

   window.CRunner
     .run(code [, input]) -> Promise<{ok, output, exit, err}>
         err is null on every normal run (compile/runtime errors are part
         of the output, like a compiler's stderr), or "load" if the
         engine script itself is missing.
     .status    -> "ready" (always — the engine loads with the page)
     .addListener(fn)  called on every status change
     .RUN_TIMEOUT_MS  kept for message parity with the Python runner
*/

(function () {
  const RUN_TIMEOUT_MS = 10000;

  let status = "ready";
  const listeners = [];

  function setStatus(next) {
    status = next;
    listeners.forEach((fn) => {
      try { fn(next); } catch (e) { /* listener bugs must not break runs */ }
    });
  }

  async function run(code, input) {
    if (!code || !code.trim()) return { ok: true, output: "", err: null };
    if (typeof CEngine === "undefined") {
      return {
        ok: false, output: "", err: "load",
        error: "the C engine failed to load",
      };
    }
    // yield a tick so the "Running…" state paints before we block
    await new Promise((r) => setTimeout(r, 0));
    try {
      const res = CEngine.run(code, {
        input: input || "",
        maxSteps: 15000000, // ~1-2s worst case, then "ran too long"
      });
      let output = res.output || "";
      if (!res.ok && res.error) {
        output = (output ? output + "\n" : "") + res.error;
      }
      return { ok: !!res.ok, output, exit: res.exit, err: null };
    } catch (e) {
      return {
        ok: false,
        output: String((e && e.message) || e),
        exit: null,
        err: null,
      };
    }
  }

  window.CRunner = {
    run,
    addListener(fn) { listeners.push(fn); },
    get status() { return status; },
    RUN_TIMEOUT_MS,
  };
})();
