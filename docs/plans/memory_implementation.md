# Plan de Implementación: Sistema de Memoria Persistente (Fix F-02)

**Objetivo:** Automatizar la captura de conocimiento al cierre de sesión para poblar `.gemini/brain` y dotar a los agentes de memoria a largo plazo.

## 1. Estrategia de Datos (Knowledge Items - KIs)
Estructuraremos la memoria en `.gemini/brain` bajo el concepto de **KIs (Knowledge Items)**.
No guardaremos solo "logs", guardaremos "conocimiento".

### Estructura de Directorios
```
.gemini/brain/
├── episodes/           → Logs de sesión crudos (por fecha)
│   └── session_2026-02-02.md
├── knowledge/          → KIs destilados por tema
│   ├── architecture/
│   ├── configuration/
│   ├── troubleshooting/
│   └── domain/
└── index.json          → Índice maestro para búsqueda rápida
```

## 2. Script de Sincronización (`scripts/memory_sync.py`)
Crearemos un script en Python (para portabilidad y manejo de texto) que:
1.  **Input:** Recibe el resumen de la sesión actual (o lee `docs/DEVLOG.md`).
2.  **Episodic Memory:** Guarda una copia del log en `episodes/`.
3.  **Semantic Memory (Simulada):**
    *   Detecta "tags" o "temas" en el log.
    *   (Fase 1) Sugiere al usuario dónde guardar la info.
    *   (Fase 2 - Futura) Actualiza automáticamente los KIs.

## 3. Integración con Workflow
Modificaremos `.gemini/workflows/session-end.md` para incluir el paso:
```yaml
### 6. Sync Memory
gemini -e code-analyst "Resuma los puntos clave de esta sesión y guárdelos en .gemini/brain/episodes/..."
```

## Pasos de Ejecución
1.  [ ] Crear estructura de directorios en `.gemini/brain`.
2.  [ ] Crear script `scripts/memory_sync.py` (Versión MVP: Guarda Episodios).
3.  [ ] Actualizar `session-end.md`.
4.  [ ] Probar ejecutando un cierre de sesión simulado.

## Criterio de Éxito
- Al terminar una sesión, aparece un archivo en `.gemini/brain/episodes/`.
- El archivo existe y es legible.
