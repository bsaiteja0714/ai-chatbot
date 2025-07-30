self.addEventListener('install', e => {
  e.waitUntil(
    caches.open('chatbot-cache').then(cache => {
      return cache.addAll([
        '/',
        '/static/css/style.css',
        '/static/js/service-worker.js'
      ]);
    })
  );
});

self.addEventListener('fetch', e => {
  e.respondWith(
    caches.match(e.request).then(response => {
      return response || fetch(e.request);
    })
  );
});
