self.addEventListener('install', function(event) {
    event.waitUntil(
      caches.open('your-app-cache-v1').then(function(cache) {
        return cache.addAll([
          '/',
          '/index.html',
          '/styles/main.css',
          '/scripts/main.js',
          '/images/logo.png'

        ]);
      })
    );
  });

self.addEventListener('fetch', function(event) {
event.respondWith(
    caches.match(event.request).then(function(response) {
    return response || fetch(event.request);
    })
);
});

self.addEventListener('activate', function(event) {
    event.waitUntil(
      caches.keys().then(function(cacheNames) {
        return Promise.all(
          cacheNames.filter(function(cacheName) {
            return cacheName.startsWith('your-app-cache-') && cacheName !== 'your-app-cache-v1';
          }).map(function(cacheName) {
            return caches.delete(cacheName);
          })
        );
      })
    );
  });
  