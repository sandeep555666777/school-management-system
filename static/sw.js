// Service Worker for School Management System PWA
const CACHE_NAME = 'school-ms-v1.0.0';
const STATIC_CACHE = 'school-ms-static-v1.0.0';
const DYNAMIC_CACHE = 'school-ms-dynamic-v1.0.0';

// Files to cache immediately
const STATIC_FILES = [
  '/',
  '/login',
  '/static/css/mobile.css',
  '/static/manifest.json',
  'https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css',
  'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css',
  'https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js'
];

// Files to cache dynamically
const DYNAMIC_FILES = [
  '/dashboard',
  '/admin/dashboard',
  '/teacher/dashboard',
  '/student/dashboard',
  '/admin/students',
  '/admin/teachers',
  '/admin/library',
  '/admin/fees',
  '/teacher/attendance',
  '/teacher/grades',
  '/student/attendance',
  '/student/grades',
  '/student/fees',
  '/student/library'
];

// Install event - cache static files
self.addEventListener('install', event => {
  console.log('Service Worker: Installing...');
  event.waitUntil(
    caches.open(STATIC_CACHE)
      .then(cache => {
        console.log('Service Worker: Caching static files');
        return cache.addAll(STATIC_FILES);
      })
      .then(() => {
        console.log('Service Worker: Static files cached');
        return self.skipWaiting();
      })
      .catch(error => {
        console.error('Service Worker: Error caching static files', error);
      })
  );
});

// Activate event - clean up old caches
self.addEventListener('activate', event => {
  console.log('Service Worker: Activating...');
  event.waitUntil(
    caches.keys()
      .then(cacheNames => {
        return Promise.all(
          cacheNames.map(cacheName => {
            if (cacheName !== STATIC_CACHE && cacheName !== DYNAMIC_CACHE) {
              console.log('Service Worker: Deleting old cache', cacheName);
              return caches.delete(cacheName);
            }
          })
        );
      })
      .then(() => {
        console.log('Service Worker: Activated');
        return self.clients.claim();
      })
  );
});

// Fetch event - serve from cache, fallback to network
self.addEventListener('fetch', event => {
  const { request } = event;
  const url = new URL(request.url);

  // Skip non-GET requests
  if (request.method !== 'GET') {
    return;
  }

  // Skip external requests (except CDN resources)
  if (url.origin !== location.origin && 
      !url.hostname.includes('cdn.jsdelivr.net') && 
      !url.hostname.includes('cdnjs.cloudflare.com')) {
    return;
  }

  event.respondWith(
    caches.match(request)
      .then(cachedResponse => {
        if (cachedResponse) {
          console.log('Service Worker: Serving from cache', request.url);
          return cachedResponse;
        }

        // Clone the request for caching
        const fetchRequest = request.clone();

        return fetch(fetchRequest)
          .then(response => {
            // Check if response is valid
            if (!response || response.status !== 200 || response.type !== 'basic') {
              return response;
            }

            // Clone the response for caching
            const responseToCache = response.clone();

            // Cache dynamic content
            if (DYNAMIC_FILES.some(path => request.url.includes(path))) {
              caches.open(DYNAMIC_CACHE)
                .then(cache => {
                  console.log('Service Worker: Caching dynamic content', request.url);
                  cache.put(request, responseToCache);
                });
            }

            return response;
          })
          .catch(error => {
            console.error('Service Worker: Fetch failed', error);
            
            // Return offline page for navigation requests
            if (request.destination === 'document') {
              return caches.match('/offline.html');
            }
            
            // Return cached version if available
            return caches.match(request);
          });
      })
  );
});

// Background sync for offline actions
self.addEventListener('sync', event => {
  console.log('Service Worker: Background sync', event.tag);
  
  if (event.tag === 'attendance-sync') {
    event.waitUntil(syncAttendance());
  } else if (event.tag === 'grades-sync') {
    event.waitUntil(syncGrades());
  }
});

// Push notification handling
self.addEventListener('push', event => {
  console.log('Service Worker: Push received');
  
  const options = {
    body: event.data ? event.data.text() : 'New notification from School Management System',
    icon: '/static/images/icon-192.png',
    badge: '/static/images/badge-72.png',
    vibrate: [200, 100, 200],
    data: {
      dateOfArrival: Date.now(),
      primaryKey: 1
    },
    actions: [
      {
        action: 'explore',
        title: 'Open App',
        icon: '/static/images/checkmark.png'
      },
      {
        action: 'close',
        title: 'Close',
        icon: '/static/images/xmark.png'
      }
    ]
  };

  event.waitUntil(
    self.registration.showNotification('School Management System', options)
  );
});

// Notification click handling
self.addEventListener('notificationclick', event => {
  console.log('Service Worker: Notification clicked');
  
  event.notification.close();

  if (event.action === 'explore') {
    event.waitUntil(
      clients.openWindow('/')
    );
  }
});

// Helper functions for background sync
async function syncAttendance() {
  try {
    // Get pending attendance data from IndexedDB
    const pendingAttendance = await getPendingAttendance();
    
    for (const attendance of pendingAttendance) {
      await fetch('/api/attendance', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(attendance)
      });
    }
    
    // Clear pending data after successful sync
    await clearPendingAttendance();
    console.log('Service Worker: Attendance synced successfully');
  } catch (error) {
    console.error('Service Worker: Attendance sync failed', error);
  }
}

async function syncGrades() {
  try {
    // Get pending grades data from IndexedDB
    const pendingGrades = await getPendingGrades();
    
    for (const grade of pendingGrades) {
      await fetch('/api/grades', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(grade)
      });
    }
    
    // Clear pending data after successful sync
    await clearPendingGrades();
    console.log('Service Worker: Grades synced successfully');
  } catch (error) {
    console.error('Service Worker: Grades sync failed', error);
  }
}

// IndexedDB helper functions (simplified)
async function getPendingAttendance() {
  // Implementation would use IndexedDB to get pending data
  return [];
}

async function clearPendingAttendance() {
  // Implementation would clear IndexedDB pending data
}

async function getPendingGrades() {
  // Implementation would use IndexedDB to get pending data
  return [];
}

async function clearPendingGrades() {
  // Implementation would clear IndexedDB pending data
}

console.log('Service Worker: Loaded successfully');