---
name: crear-pdf
description: Genera PDFs con buen diseño a partir de Markdown o HTML (resúmenes, reportes, formularios imprimibles, entregables). Úsalo siempre que el usuario pida "crea/entrégame un PDF", "exporta a PDF", "versión imprimible" o cuando un flujo del proyecto termine en un entregable PDF.
---

# Skill: crear-pdf

Convierte `.md` o `.html` en PDF usando Chrome/Chromium en modo headless (soporta emojis,
tablas, imágenes y CSS de impresión). No requiere paquetes de Python adicionales.

## Uso

```bash
python3 .claude/skills/crear-pdf/scripts/crear_pdf.py ENTRADA.md|.html -o SALIDA.pdf \
  [--titulo "Título"] [--css estilo.css] [--horizontal]
```

- **Markdown** → se convierte a HTML con `pandoc` (o el paquete `markdown` de Python si no hay pandoc)
  y se le aplica `assets/estilo.css` (estilo ejecutivo, A4/Letter, encabezados limpios).
- **HTML** → se imprime tal cual; el HTML controla su propio estilo (`@page`, `@media print`).
- Las rutas relativas de imágenes se resuelven desde la carpeta del archivo de entrada.

## Reglas
1. Guarda el PDF **dentro de la carpeta del proyecto** (por defecto junto a la entrada o en `entregables/`),
   nunca solo en `/tmp`, y entrega la ruta al usuario.
2. Antes de entregar, verifica el resultado: `python3 -c "import pypdf,sys;r=pypdf.PdfReader(sys.argv[1]);print(len(r.pages),'páginas')" SALIDA.pdf`
   y, si es posible, renderiza la primera página a PNG para revisarla visualmente.
3. Si falta Chrome o se cuelga: define `CREAR_PDF_CHROME` con la ruta del binario (en macOS:
   `/Applications/Google Chrome.app/Contents/MacOS/Google Chrome`).

## Usar en otros proyectos
Copia la carpeta `.claude/skills/crear-pdf/` a la raíz del otro repositorio
(o a `~/.claude/skills/crear-pdf/` en tu equipo para tenerla en todos los proyectos).
