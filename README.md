# Events — Aprendizaje y Seguimiento de Eventos

Repositorio donde el agente (ver `CLAUDE.md`) guarda el resumen de cada evento y su exportación a Apple Reminders.

```
eventos/      → un .md (resumen) + un .reminders.json (importación) por evento
plantillas/   → formato base de ambos archivos
```

## Cómo usarlo
1. Envía al agente fotos, nota de voz transcrita, texto o transcripción del evento (indica nombre y fecha).
2. El agente genera `eventos/AAAA-MM-DD-evento.md` y `eventos/AAAA-MM-DD-evento.reminders.json` y hace push.
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
