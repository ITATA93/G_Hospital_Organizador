# G_Hospital_Organizador

> Satellite project in the Antigravity ecosystem — Gemini CLI variant.

**Domain:** `01_HOSPITAL_PRIVADO`
**Status:** Active
**Orchestrator:** GEN_OS
**Prefix:** G_
**AG Counterpart:** `AG_Hospital_Organizador`

## Proposito

Sistema SAIA (Sistema de Archivado Inteligente Automatizado) para organizar
documentos administrativos hospitalarios. Categoriza Memorandums, Resoluciones,
Informes y Facturas con extraccion automatica de metadatos.

- Monitoreo automatizado de carpetas (escritorio, descargas)
- Extraccion de metadatos: tipo de documento, materia, fechas
- Archivado estructurado: `Unidad/Ano/TipoDocumento/`
- Habilidad agentica `document-processor` para formatos administrativos

> **Nota**: NO organiza Registros Clinicos Electronicos (RCE) ni datos de
> pacientes. Solo documentos administrativos de unidades hospitalarias.

## Arquitectura

```
G_Hospital_Organizador/
├── .gemini/              # Configuracion Gemini CLI
├── .claude/              # Configuracion Claude Code + skills
├── .subagents/           # Dispatch multi-vendor
├── src/                  # Codigo fuente
│   ├── api/              # Rutas FastAPI
│   ├── services/         # Logica de negocio (monitor, procesador)
│   ├── utils/            # Logging y utilidades
│   └── main.py           # Punto de entrada de la App
├── config/               # Configuracion del proyecto
├── scripts/              # Scripts de ayuda
├── tests/                # Tests unitarios e integracion
├── docs/                 # Documentacion y estandares
├── _Estructura_Final_SAIA/ # Estructura SAIA de referencia
└── exports/              # Exportaciones de sesion
```

## Uso con Gemini CLI

```bash
# Clasificar documentos en una carpeta
gemini "Clasifica los documentos en la carpeta de descargas por tipo"

# Extraer metadatos de un documento
gemini "Extrae tipo, materia y fecha del documento Memorandum_123.pdf"

# Organizar archivos
gemini "Organiza los archivos pendientes en la estructura Unidad/Ano/Tipo"

# Revisar estructura SAIA
gemini "Muestra el estado actual de la estructura de archivado SAIA"
```

## Scripts

| Script | Ubicacion | Funcion |
|--------|-----------|---------|
| `saia_cli.py` | Raiz | CLI principal del sistema SAIA |
| `debug_planner.py` | Raiz | Depuracion del planificador |
| `main.py` | `src/` | Servidor FastAPI (uvicorn) |

## Configuracion

- `GEMINI.md` -- Perfil del proyecto para Gemini CLI
- `CLAUDE.md` -- Instrucciones para Claude Code
- `.env.example` -- Template de variables de entorno (directorios I/O)
- `requirements.txt` -- Dependencias Python
- `migration_proposal.yaml` -- Propuesta de migracion SAIA

## Tipos de Documentos Soportados

| Tipo | Descripcion |
|------|-------------|
| Memorandum | Comunicaciones internas oficiales |
| Ordinario | Comunicaciones externas oficiales |
| Circular | Instrucciones generales |
| Resolucion | Actos administrativos |
| Informe | Reportes tecnicos y de gestion |
| Factura | Documentos tributarios |

## Proyectos Relacionados

| Proyecto | Sinergia |
|----------|----------|
| `G_Hospital` | Documentacion y procesos hospitalarios |
| `G_Informatica_Medica` | Transformacion digital |
| `G_Lists_Agent` | Gestion de tareas asociadas |
