# Plan de Implementación: Sistema de Archivo Inteligente y Auditado (SAIA)

**Fecha**: 2026-02-03
**Solicitado por**: Usuario (Jefatura)
**Contexto**: Evolución desde un ordenamiento heurístico a un sistema analítico, trazable y basado en aprobación.

## 1. Análisis de Brechas (Gap Analysis)

| Requerimiento | Estado Actual | Solución Propuesta |
| :--- | :--- | :--- |
| **1. Inventario y Mapeo** | Listado simple recursivo | **Nuevo Script**: `inventory_mapper.py` (Hash SHA256, Size, Path). |
| **2. Análisis de Contenido** | Heurística por nombre | **Mejora Skill**: Integración de OCR (Tesseract/EasyOCR) y Análisis NLP ligero. |
| **3. Integridad de Directorios** | No existe | **Algoritmo de Cohesión**: Detectar carpetas de software/proyectos para no fragmentarlas. |
| **4. Descripción de Niveles** | No existe | **Generador de Resúmenes**: Agente `code-analyst` leyendo muestras de cada carpeta. |
| **5. Detección de Conocimiento** | No existe | **Motor de Inferencia**: Comparar inventario vs. Ontología Hospitalaria (RAG ligero). |
| **6. Propuesta de Organización y Separación Personal** | Lógica hardcodeada | **Generador de Plan (YAML)**: Script que genera un `migration_plan.yml` para revisión humana. |
| **7. Aprobación Usuario** | Informal | **Gate de Aprobación**: El sistema se pausa esperando confirmación sobre el YAML. |
| **8. Ejecución Controlada** | Mover archivos (destructivo) | **Modo Copia Segura**: `Robocopy` logic en Python. Nuevo directorio destino, preservar original. |
| **9. Documento Técnico** | Reporte básico | **Reporte Técnico Estructurado**: PDF/MD con estadísticas y decisiones. |
| **10. Manual de Usuario** | Readme simple | **Manual de Navegación**: Guía explicativa de la nueva estructura. |
| **11. Auditoría y Trazabilidad** | No existe | **Sistema Audit Vault**: Carpeta `_Audit` oculta con logs JSONL versionados hash-a-hash. |

## 2. Arquitectura de la Solución

### Componentes Nuevos
1.  **`inventory_scanner.py`**:
    *   Genera una base de datos SQLite temporal (`audit.db`) en `_Audit`.
    *   Calcula hash de archivos para deduplicación y tracking.
2.  **`content_analyzer.py`**:
    *   Actualiza la DB con metadatos: `DocType`, `Date`, `Entities`, `IsPersonal`.
    *   Usa OCR para PDFs escaneados.
3.  **`structure_architect.py`**:
    *   Consulta la DB y genera `proposal_v1.yaml`.
    *   Identifica "Knowledge Gaps" (Ej: "Hay facturas pero no Órdenes de Compra").
4.  **`migration_engine.py`**:
    *   Lee `proposal_v1.yaml` (aprobado).
    *   Ejecuta copias a `H:\_UGCO_Disco G_PC_Jefatura\_Estructura_Final_2026`.
    *   Escribe logs transaccionales en `_Audit/logs/run_{timestamp}.jsonl`.

## 3. Hoja de Ruta (Roadmap)

### Fase 1: Infraestructura de Auditoría y Escaneo (Días 1-2)
- [x] Crear estructura de directorios `_Audit` en raíz del proyecto.
- [x] Desarrollar `inventory_scanner.py` (Mapeo + Hashing).
- [x] Instalar/Configurar dependencias de OCR (evaluar `easyocr` vs `pytesseract`).

### Fase 2: Inteligencia y Clasificación (Días 3-4)
- [x] Actualizar Skill `document-processor` con lógica de agrupación de directorios (Cohesión).
- [x] Desarrollar `structure_architect.py` para generar descripciones por nivel.
- [x] Implementar heurística de detección de documentos personales y folios.

### Fase 3: Interfaz de Propuesta y Ejecución (Día 5)
- [x] Diseñar formato de `proposal.yaml` legible por humanos.
- [x] Construir `migration_engine.py` con validación de integridad "pre-flight" y "post-flight".

### Fase 4: Documentación y Entrega
- [ ] Generación automática de Manuales y docs técnicos.

## 4. Requerimientos de Recursos
- **Agentes**:
    - `librarian-core`: (Nuevo rol virtual) Encargado de la taxonomía y hashing.
    - `compliance-officer`: (Agente auditor) Verifica que el Log coincida con la realidad.
- **Librerías Python**: `pandas`, `sqlite3`, `pypdf`, `pytesseract` (o `easyocr`), `pyyaml`, `watchdog`.

## 5. Próximo Paso Inmediato
Solicito aprobación para comenzar la **Fase 1**: Crear la estructura de `_Audit` y el script de inventario seguro (`inventory_scanner.py`).
