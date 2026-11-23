# Macarenco — Revista de la Asociación de Pedagogos de Cuba, Filial Santiago de Cuba

Sitio estático (PWA instalable) que se publica en GitHub Pages. Para publicar
artículos, lee **COMO_PUBLICAR.md**: la portada y el buscador se rellenan
solos desde `articulos/indice.json`.

## Mapa del sitio

| Archivo o carpeta | Qué es |
|---|---|
| `index.html` | Portada. Carrusel y novedades automáticos (lee `articulos/indice.json`). Tarjetas fijas de Evento y Patrimonio se editan a mano (cambian rara vez). |
| `articulos_publicados.html` | Buscador de artículos. Automático: lee el índice. |
| `acerca-de.html` | Quiénes somos y secciones de la redacción. |
| `contacto.html` | Contacto y envío de artículos. |
| `articulos/` | Los artículos (uno por archivo, con sus metadatos dentro), `plantilla.html`, `indice.json` y su respaldo `indice.js` (para abrir el sitio con doble clic, sin servidor). |
| `hacer_indice.py` | Publicador: regenera el índice (`indice.json` + `indice.js`) y crea borradores (`python hacer_indice.py nuevo "Título" "Sección"`). |
| `.github/workflows/indice.yml` | (Opcional) GitHub Action que regenera el índice al subir artículos. |
| `manifest.webmanifest`, `sw.js`, `imagen/` | Instalación en el teléfono, caché sin conexión e imágenes del sitio (logo del encabezado, créditos del pie, lupa e iconos). Las fotos de los artículos van enlazadas desde Wikimedia Commons y no ocupan espacio aquí. |

## Número de lanzamiento (noviembre de 2026)

Diez artículos reales, con hechos verificados y fuentes citadas al pie:
Alfabetización de 1961 · Pedagogía 2027 · Universidad de Oriente · Inclusión
en cifras · Formación de maestros · Primera infancia · Olimpiadas de
matemática · Cultura y enseñanza artística · Biblioteca Elvira Cape ·
La escuela tras el huracán Melissa.

Las imágenes van enlazadas desde Wikimedia Commons (no ocupan espacio en el
repositorio); cada una acredita a su autor y su licencia.
