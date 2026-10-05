/* PLT service worker: makes the course work offline.
   - Precaches the app shell + course data at install.
   - Cache-first for same-origin static assets (stale-while-revalidate).
   - Network-first for page navigations, falling back to the cached app
     so an internet outage never shows the browser's error page. */
const CACHE = "plt-cache-v4";
const CORE = [
  "./", "index.html", "style.css", "app.js",
  "data.js", "data-c.js", "data-html.js", "data-css.js", "data-js.js", "data-cpp.js",
  "pyrunner.js", "cengine.js", "crunner.js",
  "manifest.json", "icons/icon-192.png", "icons/icon-512.png",
];

self.addEventListener("install", (e) => {
  e.waitUntil(caches.open(CACHE)
    .then((c) => c.addAll(CORE)));
  // NO auto-skipWaiting: the page shows an "update available" toast and
  // triggers it via postMessage({action:"skipWaiting"}) when the user opts in
  self.addEventListener("message", (e) => {
    if (e.data && e.data.action === "skipWaiting") self.skipWaiting();
  });
});

self.addEventListener("activate", (e) => {
  e.waitUntil(caches.keys().then((keys) =>
    Promise.all(keys.filter((k) => k !== CACHE).map((k) => caches.delete(k)))
  ).then(() => self.clients.claim()));
});

self.addEventListener("fetch", (e) => {
  const req = e.request;
  if (req.method !== "GET" || new URL(req.url).origin !== self.location.origin) return;

  if (req.mode === "navigate") {
    // try the network, fall back to the cached app when offline
    e.respondWith(
      fetch(req).then((res) => {
        const copy = res.clone();
        caches.open(CACHE).then((c) => c.put("./", copy));
        return res;
      }).catch(() => caches.match("./"))
    );
    return;
  }

  // static assets: network-first (users always get the fresh build while
  // online), falling back to the cache only when the network is down
  e.respondWith(
    fetch(req).then((res) => {
      if (res && res.ok) {
        const copy = res.clone();
        caches.open(CACHE).then((c) => c.put(req, copy));
      }
      return res;
    }).catch(() => caches.match(req))
  );
});
