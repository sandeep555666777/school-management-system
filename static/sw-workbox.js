// Professional Workbox Service Worker for School Management System
// Based on PWA Builder with custom enhancements

const CACHE = "school-ms-workbox-v1.0.0";
const OFFLINE_URL = '/offline';

// Import Workbox from CDN
importScripts('https://storage.googleapis.com/workbox-cdn/releases/5.1.2/workbox-sw.js');

// Enable Workbox logging in development
if (workbox) {
  console.log('Workbox loaded successfully');
  workbox.setConfig({
    debug: false // Set to true for development debugging
  });
} else {
  console.log('Workbox failed to load');
}

// Skip waiting and claim clients immediately
self.addEventListener("message", (event) => {
  if (event.data && event.data.type === "SKIP_WAITING") {
    self.skipWaiting();
  }
});

// Precache offline page
workbox.precaching.precacheAndRoute([
  { url: OFFLINE_URL, revision: '1.0.0' }
]);

// Cache strategy for HTML pages (StaleWhileRevalidate)
workbox.routing.registerRoute(
  ({ request }) => request.destination === 'document',
  new workbox.strategies.StaleWhileRevalidate({
    cacheName: `${CACHE}-pages`,
    plugins: [
      {
        cacheWillUpdate: async ({ response }) => {
          return response.status === 200 ? response : null;
        }
      }
    ]
  })
);

// Cache strategy for CSS and JS files (StaleWhileRevalidate)
workbox.routing.registerRoute(
  ({ request }) => 
    request.destination === 'style' || 
    request.destination === 'script',
  new workbox.strategies.StaleWhileRevalidate({
    cacheName: `${CACHE}-assets`,
    plugins: [
      new workbox.expiration.ExpirationPlugin({
        maxEntries: 50,
        maxAgeSeconds: 30 * 24 * 60 * 60 // 30 days
      })
    ]
  })
);

// Cache strategy for images (CacheFirst)
workbox.routing.registerRoute(
  ({ request }) => request.destination === 'image',
  new workbox.strategies.CacheFirst({
    cacheName: `${CACHE}-images`,
    plugins: [
      new workbox.expiration.ExpirationPlugin({
        maxEntries: 100,
        maxAgeSeconds: 7 * 24 * 60 * 60 // 7 days
      })
    ]
  })
);

// Cache strategy for Google Fonts
workbox.routing.registerRoute(
  /^https:\/\/fonts\.googleapis\.com/,
  new workbox.strategies.StaleWhileRevalidate({
    cacheName: `${CACHE}-google-fonts-stylesheets`
  })
);

workbox.routing.registerRoute(
  /^https:\/\/fonts\.gstatic\.com/,
  new workbox.strategies.CacheFirst({
    cacheName: `${CACHE}-google-fonts-webfonts`,
    plugins: [
      new workbox.expiration.ExpirationPlugin({
        maxEntries: 30,
        maxAgeSeconds: 60 * 60 * 24 * 365 // 1 year
      })
    ]
  })
);

// Cache strategy for CDN resources (Bootstrap, FontAwesome)
workbox.routing.registerRoute(
  /^https:\/\/cdn\.jsdelivr\.net/,
  new workbox.strategies.StaleWhileRevalidate({
    cacheName: `${CACHE}-jsdelivr-cdn`,
    plugins: [
      new workbox.expiration.ExpirationPlugin({
        maxEntries: 30,
        maxAgeSeconds: 30 * 24 * 60 * 60 // 30 days
      })
    ]
  })
);

workbox.routing.registerRoute(
  /^https:\/\/cdnjs\.cloudflare\.com/,
  new workbox.strategies.StaleWhileRevalidate({
    cacheName: `${CACHE}-cloudflare-cdn`,
    plugins: [
      new workbox.expiration.ExpirationPlugin({
        maxEntries: 30,
        maxAgeSeconds: 30 * 24 * 60 * 60 // 30 days
      })
    ]
  })
);

// Cache API requests with NetworkFirst strategy
workbox.routing.registerRoute(
  /^.*\/api\/.*/,
  new workbox.strategies.NetworkFirst({
    cacheName: `${CACHE}-api`,
    networkTimeoutSeconds: 5,
    plugins: [
      new workbox.expiration.ExpirationPlugin({
        maxEntries: 50,
        maxAgeSeconds: 5 * 60 // 5 minutes
      }),
      new workbox.backgroundSync.BackgroundSyncPlugin('api-sync', {
        maxRetentionTime: 24 * 60 // 24 hours
      })
    ]
  })
);

// Catch-all route for offline fallback
workbox.routing.setCatchHandler(({ event }) => {
  switch (event.request.destination) {
    case 'document':
      return caches.match(OFFLINE_URL);
    
    case 'image':
      return caches.match('/static/images/offline-fallback.svg');
    
    default:
      return Response.error();
  }
});

// Background sync for form submissions
const bgSync = new workbox.backgroundSync.BackgroundSyncPlugin('form-sync', {
  maxRetentionTime: 24 * 60 // Retry for up to 24 hours
});

// Register background sync for attendance
workbox.routing.registerRoute(
  /\/api\/attendance/,
  new workbox.strategies.NetworkOnly({
    plugins: [bgSync]
  }),
  'POST'
);

// Register background sync for grades
workbox.routing.registerRoute(
  /\/api\/grades/,
  new workbox.strategies.NetworkOnly({
    plugins: [bgSync]
  }),
  'POST'
);

// Push notification handling
self.addEventListener('push', event => {
  const title = 'School Management System';
  const options = {
    body: event.data ? event.data.text() : 'New notification available',
    icon: '/static/images/icon-192.png',
    badge: '/static/images/icon-72.png',
    vibrate: [200, 100, 200],
    tag: 'school-notification',
    data: {
      url: '/',
      timestamp: Date.now()
    },
    actions: [
      {
        action: 'open',
        title: 'Open App',
        icon: '/static/images/icon-72.png'
      },
      {
        action: 'close',
        title: 'Dismiss'
      }
    ]
  };

  event.waitUntil(
    self.registration.showNotification(title, options)
  );
});

// Notification click handling
self.addEventListener('notificationclick', event => {
  event.notification.close();

  if (event.action === 'open' || !event.action) {
    event.waitUntil(
      clients.matchAll({ type: 'window', includeUncontrolled: true }).then(clientList => {
        // Check if there is already a window/tab open with the target URL
        for (let client of clientList) {
          if (client.url === self.registration.scope && 'focus' in client) {
            return client.focus();
          }
        }
        // If not, open a new window/tab
        if (clients.openWindow) {
          return clients.openWindow('/');
        }
      })
    );
  }
});

// Install event
self.addEventListener('install', event => {
  console.log('Workbox Service Worker installing...');
  
  // Create offline fallback page if it doesn't exist
  event.waitUntil(
    caches.open(CACHE).then(cache => {
      return cache.add(OFFLINE_URL).catch(() => {
        console.log('Creating offline fallback page');
        return cache.put(OFFLINE_URL, new Response(
          `<!DOCTYPE html>
          <html><head><title>Offline - School Management System</title>
          <meta name="viewport" content="width=device-width, initial-scale=1">
          <style>body{font-family:Arial,sans-serif;text-align:center;padding:50px;background:#f5f5f5}
          .offline{background:white;padding:40px;border-radius:10px;box-shadow:0 2px 10px rgba(0,0,0,0.1)}
          .icon{font-size:48px;margin-bottom:20px}h1{color:#333;margin-bottom:15px}
          p{color:#666;line-height:1.5}.btn{background:#007bff;color:white;padding:10px 20px;
          border:none;border-radius:5px;cursor:pointer;text-decoration:none;display:inline-block}
          .btn:hover{background:#0056b3}</style></head>
          <body><div class="offline"><div class="icon">📚</div>
          <h1>You're Offline</h1><p>School Management System is currently unavailable.</p>
          <p>Please check your internet connection and try again.</p>
          <button class="btn" onclick="window.location.reload()">Retry</button>
          </div><script>window.addEventListener('online',()=>window.location.reload());</script>
          </body></html>`,
          { headers: { 'Content-Type': 'text/html' } }
        ));
      });
    })
  );
});

// Activate event
self.addEventListener('activate', event => {
  console.log('Workbox Service Worker activated');
  event.waitUntil(self.clients.claim());
});

console.log('Workbox Service Worker loaded successfully!');