# Events — Aprendizaje y Seguimiento de Eventos

Repositorio donde el agente (ver `CLAUDE.md`) guarda el resumen de cada evento y su exportación a Apple Reminders.

```
formulario/index.html          → formulario para cargar el material del evento (funciona sin internet)
entregables/formulario-evento.pdf → versión en blanco para imprimir y llenar a mano
eventos/entrada/               → material recibido (evento.json + fotos)
eventos/                       → por evento: .md (resumen), .reminders.json (importación) y .pdf
plantillas/                    → formato base de ambos archivos
.claude/skills/crear-pdf/      → skill reutilizable para generar PDFs (ver abajo)
```

## Formulario
Abre `formulario/index.html` en el navegador (computador o iPhone desde la app Archivos). Funciona sin internet.
1. **Datos del evento**: nombre, fecha, tipo, tema, ponentes.
2. **Fotos**: tomar foto con la cámara o elegir varias de la galería (en computador también arrastrar o pegar). Cada foto admite una descripción opcional.
3. **Notas sueltas** (opcional): textos que no salgan en las fotos.

Pulsa **📦 Descargar paquete para el agente (.zip)** y envíalo al agente (o súbelo a `eventos/entrada/`).
El agente devuelve el entregable: ideas clave, insights, libros, tareas, el `.reminders.json` y el PDF del evento.
El borrador se guarda en el navegador hasta que pulses "Limpiar formulario".
Hoja en blanco para llenar a mano: `entregables/formulario-evento.pdf` (o `formulario/index.html?en-blanco`).

## Skill `crear-pdf` (para todos los proyectos)
```bash
python3 .claude/skills/crear-pdf/scripts/crear_pdf.py archivo.md -o entregables/archivo.pdf
python3 .claude/skills/crear-pdf/scripts/crear_pdf.py formulario/index.html --query en-blanco -o entregables/formulario-evento.pdf
```
Para usarla en otros repositorios, copia `.claude/skills/crear-pdf/` a la raíz de cada uno,
o a `~/.claude/skills/crear-pdf/` en tu equipo para que esté disponible en todos tus proyectos.

## Cómo usarlo
1. Llena el formulario (datos + fotos + notas) y envía el .zip al agente, o manda las fotos directo por el chat.
2. El agente genera `eventos/AAAA-MM-DD-evento.md`, `.reminders.json` y `.pdf` y hace push.
3. Importa a Recordatorios con cualquiera de estas dos vías:

### Opción A — Manual (rápida)
Abre el `.md` en GitHub desde el iPhone, copia cada bloque de la Sección 2 y pégalo en la lista correspondiente.
Tip: en Recordatorios, pegar varias líneas crea un recordatorio por línea.

### Opción B — Atajo de iOS (automática, una sola vez de configuración)
Crea en la app **Atajos** un atajo llamado "Importar Evento" con estas acciones:
1. **Obtener contenido de la URL** → URL *raw* del `.reminders.json` (o **Seleccionar archivo** si lo descargas a Archivos).
2. **Obtener valor del diccionario** → clave `recordatorios`.
3. **Repetir con cada** elemento:
   - **Obtener valor del diccionario** `titulo`, `notas`, `lista`, `prioridad`, `due`.
   - **Añadir recordatorio nuevo** → Título = `titulo`, Notas = `notas`, Lista = `lista`,
     Prioridad = `prioridad`, Alerta/Fecha = `due` (si no está vacío).
4. Fin de repetición.

> Crea antes en Recordatorios las listas exactamente con los nombres **📚 Libros por Leer** y **🎯 Tareas & Acciones**.
