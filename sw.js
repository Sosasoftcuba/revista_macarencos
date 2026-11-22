/* Service worker de Macarenco.
   Hace dos cosas:
   1) Activa la opción "Instalar aplicación" en el menú del teléfono.
   2) Guarda las páginas e imágenes visitadas: si no hay conexión,
      la revista se abre igual con lo último que se descargó. */
var CACHE = 'macarenco-v1';

self.addEventListener('install', function (e) {
    self.skipWaiting();
});

self.addEventListener('activate', function (e) {
    e.waitUntil(
        caches.keys().then(function (claves) {
            return Promise.all(
                claves.filter(function (c) { return c !== CACHE; })
                      .map(function (c) { return caches.delete(c); })
            );
        }).then(function () { return self.clients.claim(); })
    );
});

self.addEventListener('fetch', function (e) {
    if (e.request.method !== 'GET') return;
    e.respondWith(
        caches.match(e.request).then(function (cacheado) {
            var desdeRed = fetch(e.request).then(function (respuesta) {
                if (respuesta && respuesta.status === 200 && respuesta.type === 'basic') {
                    var copia = respuesta.clone();
                    caches.open(CACHE).then(function (c) { c.put(e.request, copia); });
                }
                return respuesta;
            }).catch(function () {
                return cacheado; /* sin conexión: sirve lo guardado */
            });
            return cacheado || desdeRed;
        })
    );
});
