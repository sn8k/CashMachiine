/* ui service worker v0.3.5 (2025-08-20) */
const CACHE_NAME = 'ui-cache-v1';
const OFFLINE_URLS = ['/'];
self.addEventListener('install', event => {
  event.waitUntil(caches.open(CACHE_NAME).then(cache => cache.addAll(OFFLINE_URLS)));
});
self.addEventListener('fetch', event => {
  event.respondWith(caches.match(event.request).then(r => r || fetch(event.request)));
});
self.addEventListener('push', event => {
  const data = event.data?.json() || {};
  event.waitUntil(
    self.registration.showNotification(data.title || 'CashMachiine', {
      body: data.body || 'Notification'
    })
  );
});
