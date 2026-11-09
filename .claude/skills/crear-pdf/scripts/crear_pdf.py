#!/usr/bin/env python3
"""Convierte Markdown o HTML en PDF con Chrome/Chromium headless.

Uso: crear_pdf.py ENTRADA(.md|.html) [-o SALIDA.pdf] [--titulo T] [--css archivo.css] [--horizontal]
"""
import argparse, glob, html, os, shutil, subprocess, sys, tempfile
from pathlib import Path

AQUI = Path(__file__).resolve().parent
CSS_DEFECTO = AQUI.parent / "assets" / "estilo.css"

CANDIDATOS_CHROME = [
    os.environ.get("CREAR_PDF_CHROME"),  # forzar un navegador concreto
    # Playwright: el "headless shell" imprime sin abrir ventana ni intentar conectarse a Google.
    *sorted(glob.glob(os.path.expanduser("~/.cache/ms-playwright/chromium_headless_shell-*/*/chrome-headless-shell")), reverse=True),
    *sorted(glob.glob("/opt/pw-browsers/chromium_headless_shell-*/*/chrome-headless-shell"), reverse=True),
    os.environ.get("CHROME_PATH"),
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
]
NOMBRES_CHROME = ["google-chrome", "google-chrome-stable", "chromium", "chromium-browser", "chrome", "msedge"]


def buscar_chrome() -> str:
    for c in CANDIDATOS_CHROME:
        if c and Path(c).exists():
            return c
    for n in NOMBRES_CHROME:
        p = shutil.which(n)
        if p:
            return p
    sys.exit("No se encontró Chrome/Chromium. Define CREAR_PDF_CHROME con la ruta del navegador.")


def md_a_html(md: str) -> str:
    if shutil.which("pandoc"):
        r = subprocess.run(["pandoc", "-f", "gfm", "-t", "html"], input=md, capture_output=True, text=True, check=True)
        return r.stdout
    try:
        import markdown  # type: ignore
        return markdown.markdown(md, extensions=["tables", "fenced_code", "sane_lists"])
    except ImportError:
        sys.exit("Para convertir Markdown instala pandoc o `pip install markdown`.")


def envolver(cuerpo: str, titulo: str, css: str, horizontal: bool) -> str:
    extra = "@page { size: A4 landscape; }" if horizontal else ""
    return (f"<!doctype html><html lang='es'><head><meta charset='utf-8'><title>{html.escape(titulo)}</title>"
            f"<style>{css}\n{extra}</style></head><body>{cuerpo}</body></html>")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("entrada")
    ap.add_argument("-o", "--salida")
    ap.add_argument("--titulo")
    ap.add_argument("--css", help="CSS propio para Markdown (por defecto assets/estilo.css)")
    ap.add_argument("--horizontal", action="store_true")
    ap.add_argument("--query", default="", help="Parámetros de URL para el HTML, ej. 'en-blanco' (sin '?')")
    ap.add_argument("--timeout", type=int, default=90, help="Segundos máximos de espera (por defecto 90)")
    a = ap.parse_args()

    entrada = Path(a.entrada).resolve()
    if not entrada.exists():
        sys.exit(f"No existe: {entrada}")
    salida = Path(a.salida).resolve() if a.salida else entrada.with_suffix(".pdf")
    salida.parent.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory() as tmp:
        if entrada.suffix.lower() in (".md", ".markdown"):
            css = Path(a.css or CSS_DEFECTO).read_text(encoding="utf-8")
            doc = envolver(md_a_html(entrada.read_text(encoding="utf-8")), a.titulo or entrada.stem, css, a.horizontal)
            # El HTML temporal vive junto a la entrada para que las imágenes relativas resuelvan.
            html_tmp = entrada.parent / f".{entrada.stem}.crear-pdf.html"
            html_tmp.write_text(doc, encoding="utf-8")
        else:
            html_tmp = entrada
        try:
            uri = html_tmp.as_uri() + (f"?{a.query.lstrip('?')}" if a.query else "")
            cmd = [buscar_chrome(), "--headless", "--no-sandbox", "--disable-gpu", "--no-first-run",
                   "--no-default-browser-check", "--disable-background-networking", "--disable-component-update",
                   "--disable-extensions", f"--user-data-dir={tmp}", "--no-pdf-header-footer",
                   f"--print-to-pdf={salida}", uri]
            try:
                r = subprocess.run(cmd, capture_output=True, text=True, timeout=a.timeout)
            except subprocess.TimeoutExpired:
                sys.exit(f"Chrome no terminó en {a.timeout}s. Prueba con otro binario vía CREAR_PDF_CHROME "
                         "(p. ej. chrome-headless-shell de Playwright).")
        finally:
            if html_tmp != entrada:
                html_tmp.unlink(missing_ok=True)
    if not salida.exists() or salida.stat().st_size == 0:
        sys.exit(f"Falló la generación del PDF.\n{r.stderr[-2000:]}")
    print(f"PDF creado: {salida}")


if __name__ == "__main__":
    main()
