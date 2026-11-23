# Cómo publicar en Macarenco (guía de la redacción)

Esta revista ya **no se edita página por página**. La portada y el buscador se
rellenan solos a partir de la carpeta `articulos/`. Publicar un artículo son
dos pasos; el resto lo hace el sistema.

## Cómo funciona

```
articulos/
├── plantilla.html        ← molde para artículos nuevos (no se publica)
├── articulo_1.html       ← cada artículo lleva dentro sus metadatos
├── articulo_2.html          (un bloque "application/ld+json" con título,
├── ...                      sección, fecha, resumen e imagen)
├── articulo_7000.html     ← dentro de dos años, sigue siendo igual de fácil
├── indice.json           ← la lista que leen la portada y el buscador
│                            (lo genera hacer_indice.py; no se edita a mano)
└── indice.js             ← la misma lista como respaldo, para poder abrir
                             el sitio con doble clic, sin internet ni servidor
```

- **index.html** muestra automáticamente los 3 artículos más recientes en el
  carrusel y los 2 siguientes en «Novedades». No se toca nunca más.
- **articulos_publicados.html** (el buscador) encuentra solo todos los
  artículos que estén en `indice.json`, con búsqueda por título, sección,
  resumen y fecha.
- Cada artículo muestra al final, sin esfuerzo tuyo, tres artículos
  relacionados (prioriza su propia sección).
- La raíz del repositorio **no crece**: los artículos viven en `articulos/`
  y las imágenes se enlazan desde internet (Wikimedia Commons), así que no
  gastan espacio en GitHub.
- El sitio funciona también **desde el disco o una USB**: al abrirlo con
  doble clic (sin servidor), la portada y el buscador leen el respaldo
  `indice.js` en vez de `indice.json`, porque los navegadores bloquean la
  lectura directa de archivos locales. En GitHub Pages siempre se usa
  `indice.json`.

## Publicar un artículo nuevo (con Python instalado)

1. Crea el borrador (se numera solo y lleva la fecha de hoy):

   ```
   python hacer_indice.py nuevo "Título del artículo" "Sección"
   ```

2. Abre `articulos/articulo_N.html` y escribe el artículo siguiendo los
   comentarios de la plantilla. Rellena los marcadores `__ASÍ__` que queden
   (imagen, pie de foto, resumen…). Un artículo con marcadores sin rellenar
   **no se publica** (el script te avisa): es la red de seguridad para que
   nunca salga un borrador a medias.

3. Reconstruye la lista y sube la carpeta `articulos/` al repositorio:

   ```
   python hacer_indice.py
   ```

Eso es todo. La portada, el buscador y los relacionados se actualizan solos.

## Publicar sin instalar nada (opción GitHub)

Si editas directamente en la web de GitHub, añade una vez el archivo
`.github/workflows/indice.yml` (está incluido en esta entrega, junto a esta
guía). A partir de ese momento, cada vez que subas o edites un artículo en
la carpeta `articulos/`, GitHub ejecuta `hacer_indice.py` él solo y guarda
el `indice.json` actualizado. No tienes que correr nada en tu máquina.

Para crearlo desde la web: en tu repositorio → *Add file → Create new file*
→ nómbralo exactamente `.github/workflows/indice.yml` → pega el contenido
del archivo incluido → *Commit changes*.

## Escribir el artículo (reglas de la casa)

- **No borres el bloque de metadatos** `application/ld+json` del principio:
  de ahí salen el título, la sección y la fecha que ven la portada y el
  buscador. Sí puedes corregir sus valores.
- El cuerpo admite: párrafos `<p>…</p>`, subtítulos `<h2>…</h2>`, citas
  destacadas `<blockquote>«…»</blockquote>`.
- **Verifica cada dato** y pon las fuentes reales en la sección «Fuentes
  consultadas» con su enlace. Nada de cifras inventadas.
- **Imágenes**: enlázalas de Wikimedia Commons (licencia libre y sin gastar
  espacio). Truco: en la página del archivo, botón derecho sobre la imagen
  → *Copiar dirección de imagen*. Pon el crédito y la licencia en el pie.
  Si prefieres una imagen propia, súbela dentro de `articulos/` (p. ej.
  `imagen-12.jpg`) y refiérela como `src="imagen-12.jpg"`.
- Si cambias la imagen, el título o la fecha de un artículo ya publicado,
  vuelve a ejecutar `hacer_indice.py` para refrescar la lista.

## Problemas frecuentes

| Síntoma | Causa | Solución |
|---|---|---|
| El artículo no aparece en la portada ni el buscador | `indice.json` desactualizado | Ejecuta `python hacer_indice.py` (o sube el Action) |
| El script avisa «marcadores __SIN_RELLENAR__» | Falta completar imagen, resumen, pie… | Abre el archivo y sustituye los marcadores `__…__` |
| La portada dice «No se pudo cargar el índice» | Faltan `articulos/indice.json` e `indice.js` en el repositorio | Súbelos (se regeneran con el script o el Action) |
| Abro la página con doble clic y no salen los artículos | La carpeta abierta no es la del sitio completo (sin `articulos/`) | Comprueba que `articulos/indice.js` esté junto a las páginas; con doble clic se usa ese respaldo |
| Una imagen no se ve | URL mal copiada o caída | Comprueba la URL en el navegador y regenera el índice |
| Cambié de sección un artículo | — | Edita su metadato `cat` y regenera el índice |

## Por qué así no se llena la raíz

Dentro de dos años, con el artículo 7000 publicado, el repositorio tendrá
exactamente lo mismo en la raíz que hoy: `index.html`, las tres páginas
fijas, `manifest.webmanifest`, `sw.js`, los iconos, esta guía y
`hacer_indice.py`. Solo crecen la carpeta `articulos/` y su par de archivos
de índice (`indice.json` + `indice.js`, unos pocos KB cada mil artículos).
