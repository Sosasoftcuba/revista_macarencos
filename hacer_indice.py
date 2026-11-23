#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Macarenco — publicador de artículos.

Con este script la portada y el buscador se rellenan SOLOS. Ya no hace
falta editar index.html ni articulos_publicados.html para publicar.

USO (desde la carpeta del sitio, donde está este archivo):

    python hacer_indice.py
        Revisa todos los archivos articulos/articulo_*.html, lee los
        metadatos que cada uno lleva dentro (bloque "application/ld+json")
        y reconstruye articulos/indice.json y articulos/indice.js (este
        último es el respaldo para abrir el sitio con doble clic, sin
        servidor). La portada muestra los más recientes y el buscador los
        encuentra todos.

    python hacer_indice.py nuevo "Título del artículo" "Sección"
        Crea articulos/articulo_N.html a partir de la plantilla, con el
        número siguiente y la fecha de hoy. Después solo tienes que:
        1) abrir el archivo y escribir el contenido (sigue los comentarios),
        2) volver a ejecutar  python hacer_indice.py
        3) subir la carpeta articulos/ al repositorio.
"""
import glob
import json
import os
import re
import sys
from datetime import date

# Mensajes con acentos correctos también en la consola de Windows
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

AQUI = os.path.dirname(os.path.abspath(__file__))
CARPETA = os.path.join(AQUI, "articulos")
INDICE = os.path.join(CARPETA, "indice.json")
INDICE_JS = os.path.join(CARPETA, "indice.js")
PLANTILLA = os.path.join(CARPETA, "plantilla.html")

MESES = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio",
         "agosto", "septiembre", "octubre", "noviembre", "diciembre"]

PASOS = """
Pasos siguientes:
  1) Abre articulos/{nombre} y escribe el artículo siguiendo los comentarios
     (borra los ejemplos y los comentarios al terminar).
  2) Rellena los marcadores que faltan (los que empiezan y terminan por __).
  3) Ejecuta de nuevo:  python hacer_indice.py
  4) Sube la carpeta articulos/ (y indice.json) al repositorio.
"""


def leer_meta(ruta):
    """Devuelve el bloque JSON-LD de un artículo, o None si no existe."""
    with open(ruta, encoding="utf-8") as fh:
        html = fh.read()
    m = re.search(r'<script type="application/ld\+json">\s*(.*?)\s*</script>', html, re.S)
    if not m:
        return None
    try:
        return json.loads(m.group(1))
    except ValueError:
        return None


def hacer_indice():
    if not os.path.isdir(CARPETA):
        print("ERROR: no encontré la carpeta articulos/ junto a este script.")
        sys.exit(1)
    archivos = sorted(glob.glob(os.path.join(CARPETA, "articulo_*.html")))
    if not archivos:
        print("AVISO: la carpeta articulos/ no tiene artículos todavía.")
    entradas = []
    vistos = set()
    for ruta in archivos:
        nombre = os.path.basename(ruta)
        meta = leer_meta(ruta)
        if meta is None:
            print("AVISO: %s no tiene un bloque de metadatos válido; se omite." % nombre)
            continue
        if "__" in json.dumps(meta, ensure_ascii=False):
            print("AVISO: %s todavía tiene marcadores __SIN_RELLENAR__; se omite "
                  "hasta que los completes." % nombre)
            continue
        if "num" not in meta or "titulo" not in meta or "cat" not in meta:
            print("AVISO: %s no tiene num/titulo/cat en sus metadatos; se omite." % nombre)
            continue
        if meta["num"] in vistos:
            print("AVISO: hay dos artículos con el número %s (revisa %s)." % (meta["num"], nombre))
        vistos.add(meta["num"])
        meta["url"] = "articulo_%d.html" % int(meta["num"])
        meta["pdf"] = meta["url"] + "?imprimir=1"
        entradas.append(meta)
    # Más recientes primero
    entradas.sort(key=lambda d: (str(d.get("fecha", "")), int(d["num"])), reverse=True)
    with open(INDICE, "w", encoding="utf-8") as fh:
        json.dump(entradas, fh, ensure_ascii=False, indent=2)
    # Respaldo con los mismos datos para abrir el sitio con doble clic
    # (file://): el navegador bloquea fetch() sobre archivos locales, pero
    # una etiqueta <script> sí puede leer este .js. La portada y el buscador
    # lo usan solos cuando indice.json no se puede leer.
    with open(INDICE_JS, "w", encoding="utf-8") as fh:
        fh.write("// Respaldo de articulos/indice.json para abrir el sitio con doble\n")
        fh.write("// clic (file://), donde fetch() no funciona. Mismos datos,\n")
        fh.write("// otra forma de leerlos. Lo genera hacer_indice.py: no editar a mano.\n")
        fh.write("window.INDICE_ARTICULOS = ")
        fh.write(json.dumps(entradas, ensure_ascii=False, indent=2))
        fh.write(";\n")
    print("indice.json actualizado: %d artículos (más el respaldo indice.js)." % len(entradas))
    for e in entradas[:6]:
        print("   - %s  ·  %s" % (e.get("fecha", "????-??-??"), e["titulo"][:66]))


def nuevo(titulo, cat):
    if not os.path.exists(PLANTILLA):
        print("ERROR: no encontré articulos/plantilla.html.")
        sys.exit(1)
    nums = [0]
    for ruta in glob.glob(os.path.join(CARPETA, "articulo_*.html")):
        m = re.search(r"articulo_(\d+)\.html$", os.path.basename(ruta))
        if m:
            nums.append(int(m.group(1)))
    num = max(nums) + 1
    hoy = date.today()
    fechatxt = "%d de %s de %d" % (hoy.day, MESES[hoy.month - 1], hoy.year)
    with open(PLANTILLA, encoding="utf-8") as fh:
        texto = fh.read()
    reemplazos = {
        "__NUM__": str(num),
        "__TITULO__": titulo,
        "__CAT__": cat,
        "__FECHA__": "%04d-%02d-%02d" % (hoy.year, hoy.month, hoy.day),
        "__FECHATXT__": fechatxt,
        "__MIN__": "4 min de lectura",
        "__AUTOR__": "Redacción Macarenco",
    }
    for viejo, nuevo_valor in reemplazos.items():
        texto = texto.replace(viejo, nuevo_valor)
    nombre = "articulo_%d.html" % num
    salida = os.path.join(CARPETA, nombre)
    with open(salida, "w", encoding="utf-8") as fh:
        fh.write(texto)
    print("Creado articulos/%s  (número %d, sección \"%s\", %s)." % (nombre, num, cat, fechatxt))
    print(PASOS.format(nombre=nombre))


def main():
    if len(sys.argv) >= 2 and sys.argv[1].lower() == "nuevo":
        if len(sys.argv) < 3:
            print("Uso: python hacer_indice.py nuevo \"Título del artículo\" \"Sección\"")
            sys.exit(1)
        titulo = sys.argv[2]
        cat = sys.argv[3] if len(sys.argv) > 3 else "General"
        nuevo(titulo, cat)
    else:
        hacer_indice()


if __name__ == "__main__":
    main()
