// Fast Service Worker with robust offline support
const CACHE_NAME = 'school-ms-v1.4.0';
const OFFLINE_URL = '/offline';

// Essential files to cache (only what we know exists)
const ESSENTIAL_FILES = [
  '/',
  '/login',
  '/static/css/mobile.css'
];

// Install immediately - cache only essential files
self.addEventListener('install', event => {
  console.log('SW: Installing v1.4.0');
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => {
        // Cache offline page first (most important)
        return cache.add('/offline').catch(err => {
          console.log('SW: Offline page not found, using fallback');
          return cache.put('/offline', new Response(
            `<!DOCTYPE html>
            <html><head><title>Offline</title>
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <style>body{font-family:Arial,sans-serif;text-align:center;padding:50px;background:#f5f5f5}
            .offline{background:white;padding:40px;border-radius:10px;box-shadow:0 2px 10px rgba(0,0,0,0.1)}
            .icon{font-size:48px;margin-bottom:20px}h1{color:#333;margin-bottom:15px}
            p{color:#666;line-height:1.5}</style></head>
            <body><div class="offline"><div class="icon">📡</div>
            <h1>You're Offline</h1><p>The School Management System will work again when your connection is restored.</p>
            <p>Try refreshing the page or check your internet connection.</p></div></body></html>`,
            { headers: { 'Content-Type': 'text/html' } }
          ));
        });
      })
      .then(() => {
        console.log('SW: Essential files cached');
        return self.skipWaiting();
      })
      .catch(err => {
        console.log('SW: Install error (non-critical):', err);
        return self.skipWaiting(); // Continue anyway
      })
  );
});

// Activate immediately and clean old caches
self.addEventListener('activate', event => {
  console.log('SW: Activating v1.4.0');
  event.waitUntil(
    caches.keys()
      .then(cacheNames => {
        return Promise.all(
          cacheNames
            .filter(cacheName => cacheName.startsWith('school-ms-') && cacheName !== CACHE_NAME)
            .map(cacheName => {
              console.log('SW: Deleting old cache:', cacheName);
              return caches.delete(cacheName);
            })
        );
      })
      .then(() => {
        console.log('SW: Activated and claimed');
        return self.clients.claim();
      })
  );
});

// Fast fetch handler with smart caching
self.addEventListener('fetch', event => {
  const { request } = event;
  const url = new URL(request.url);

  // Skip non-GET requests
  if (request.method !== 'GET') return;

  // Skip external requests (except known CDNs)
  if (url.origin !== location.origin && 
      !url.hostname.includes('cdn.jsdelivr.net') && 
      !url.hostname.includes('cdnjs.cloudflare.com') &&
      !url.hostname.includes('bootstrap') &&
      !url.hostname.includes('fontawesome')) {
    return;
  }

  event.respondWith(
    fetch(request)
      .then(response => {
        // If successful, optionally cache it
        if (response.ok && url.origin === location.origin) {
          const responseClone = response.clone();
          caches.open(CACHE_NAME).then(cache => {
            cache.put(request, responseClone).catch(err => {
              console.log('SW: Cache put failed (non-critical):', err);
            });
          });
        }
        return response;
      })
      .catch(() => {
        // Network failed, try cache
        return caches.match(request)
          .then(cachedResponse => {
            if (cachedResponse) {
              console.log('SW: Serving from cache:', request.url);
              return cachedResponse;
            }
            
            // For navigation, show offline page
            if (request.mode === 'navigate') {
              return caches.match('/offline');
            }
            
            // For other requests, return basic error response
            return new Response('Network Error', {
              status: 408,
              headers: { 'Content-Type': 'text/plain' }
            });
          });
      })
  );
});

// Background sync for offline functionality
self.addEventListener('sync', event => {
  console.log('SW: Background sync event:', event.tag);
  
  if (event.tag === 'attendance-sync') {
    event.waitUntil(syncOfflineData('attendance'));
  } else if (event.tag === 'grades-sync') {
    event.waitUntil(syncOfflineData('grades'));
  } else if (event.tag === 'notifications-sync') {
    event.waitUntil(syncOfflineData('notifications'));
  }
});

// Simple sync function
async function syncOfflineData(type) {
  try {
    console.log('SW: Syncing offline', type, 'data');
    
    // Get offline data from localStorage or IndexedDB
    const data = await getOfflineData(type);
    
    if (data && data.length > 0) {
      // Send to server
      const response = await fetch(`/api/sync/${type}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data)
      });
      
      if (response.ok) {
        await clearOfflineData(type);
        console.log('SW: Sync successful for', type);
      }
    }
  } catch (error) {
    console.log('SW: Sync failed for', type, '(will retry):', error);
    throw error; // Re-throw to retry sync later
  }
}

// Helper functions (simplified for now)
async function getOfflineData(type) {
  try {
    const stored = localStorage.getItem(`offline_${type}`);
    return stored ? JSON.parse(stored) : [];
  } catch {
    return [];
  }
}

async function clearOfflineData(type) {
  try {
    localStorage.removeItem(`offline_${type}`);
  } catch (error) {
    console.log('SW: Error clearing offline data:', error);
  }
}

// Push notifications (if supported)
self.addEventListener('push', event => {
  const title = 'School Management System';
  const options = {
    body: event.data ? event.data.text() : 'New notification available',
    icon: '/static/images/icon-192.png',
    badge: '/static/images/icon-72.png',
    vibrate: [200, 100, 200],
    tag: 'school-notification'
  };

  event.waitUntil(
    self.registration.showNotification(title, options)
  );
});

self.addEventListener('notificationclick', event => {
  event.notification.close();
  
  event.waitUntil(
    clients.matchAll({ type: 'window' }).then(clientList => {
      for (let client of clientList) {
        if (client.url === '/' && 'focus' in client) {
          return client.focus();
        }
      }
      if (clients.openWindow) {
        return clients.openWindow('/');
      }
    })
  );
});

console.log('SW: Fast service worker loaded and ready!');