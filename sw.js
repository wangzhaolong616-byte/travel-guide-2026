/* 中国旅行宝典 2026 · Service Worker
 * 策略：HTML 网络优先（保证内容最新，离线回退缓存）；静态资源缓存优先。
 * 更新内容后请把 CACHE 版本号 +1（如 ctw-v2），旧缓存会在 activate 阶段自动清理。 */
const CACHE = "ctw-v1";
const ASSETS = [
  "./",
  "./index.html",
  "./manifest.json",
  "./icons/icon-192.png",
  "./icons/icon-512.png",
  "./icons/icon-maskable-512.png",
  "./icons/apple-touch-icon.png",
  "./icons/favicon-32.png"
];

self.addEventListener("install", e => {
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(ASSETS)).then(() => self.skipWaiting()));
});

self.addEventListener("activate", e => {
  e.waitUntil(
    caches.keys()
      .then(ks => Promise.all(ks.filter(k => k !== CACHE).map(k => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener("fetch", e => {
  if (e.request.method !== "GET") return;
  const url = new URL(e.request.url);
  if (url.origin !== location.origin) return;
  const isHTML = url.pathname.endsWith(".html") || url.pathname === "/" || url.pathname.endsWith("/");
  if (isHTML) {
    // HTML：网络优先，离线回退
    e.respondWith(
      fetch(e.request).then(r => {
        const cp = r.clone();
        caches.open(CACHE).then(c => c.put(e.request, cp));
        return r;
      }).catch(() => caches.match(e.request).then(m => m || caches.match("./index.html")))
    );
  } else {
    // 静态资源：缓存优先
    e.respondWith(
      caches.match(e.request).then(m => m || fetch(e.request).then(r => {
        const cp = r.clone();
        caches.open(CACHE).then(c => c.put(e.request, cp));
        return r;
      }))
    );
  }
});
