# Documento Técnico SAIA: Sistema de Archivo Inteligente Auditado

**Versión**: 1.0.0
**Fecha**: 03/02/2026
**Autor**: Antigravity (Agente Arquitecto)

## 1. Visión General
SAIA es una plataforma desarrollada para la organización autónoma y segura de documentos administrativos hospitalarios. A diferencia de scripts simples, utiliza un modelo de "Trust First" basado en hashes criptográficos y confirmación humana.

## 2. Arquitectura de Componentes

### 2.1. Audit Vault (`src/audit/vault.py`)
- **Tipo**: Base de Datos SQLite Oculta (`_Audit/audit.db`).
- **Función**: Almacena el "Inventario Maestro".
- **Esquema**:
  - `inventory`: Tabla principal con rutas, hashes SHA256, tamaño y fechas.
  - `operations_log`: Registro inmutable de transacciones (Scan, Move, Rollback).

### 2.2. Intelligent Scanners
- **Inventory Scanner** (`src/scanners/inventory.py`):
  - Escanea recursivamente el disco H:.
  - Calcula hashes SHA256 para detectar duplicados exactos.
  - Alimenta el Vault.
- **Content Scanner** (`src/scanners/content.py`):
  - (En Desarrollo) Usa OCR y Regex para extraer metadatos de documentos "Unknown".

### 2.3. Structure Architect (`src/architect/planner.py`)
- **Motor de Decisión**: No mueve archivos, propone movimientos.
- **Salida**: Genera un archivo `migration_proposal.yaml` legible por humanos.
- **Lógica Heurística**:
  - Detecta Año por nombre de archivo o carpeta.
  - Detecta Tipo Documental (Memo, Oficio, Factura) por regex.
  - Preserva integridad de carpetas de software (.exe).

### 2.4. Migration Engine (`src/engine/executor.py`)
- **Ejecutor Seguro**: Lee el YAML aprobado y copia los archivos.
- **Seguridad**:
  - Verificación Hash-to-Hash post-copia (Planeado v2).
  - Logs de transacción para futuro Rollback.

## 3. Flujo de Trabajo (Workflow)

1.  **SCAN**: `python saia_cli.py scan` -> Llena la DB.
2.  **(Opcional) ENRICH**: `python saia_cli.py enrich` -> Analiza PDFs.
3.  **PLAN**: `python saia_cli.py plan` -> Genera `migration_proposal.yaml`.
4.  **REVIEW**: El usuario (Jefatura) revisa el YAML.
5.  **EXECUTE**: `python saia_cli.py execute --target migration_proposal.yaml` -> Aplica cambios.

## 4. Estructura de Directorios Final
H:\_UGCO_Disco G_PC_Jefatura\
├── _Audit (OCULTO)
├── _Estructura_Final_SAIA (NUEVO)
│   ├── 02_Administrativo_Central
│   │   ├── 2024
│   │   │   ├── Memorandums
│   │   │   ├── Resoluciones
│   │   │   └── ...
│   │   └── ...
└── (Carpetas Originales) -> Se mantienen hasta verificar éxito.

## 5. Auditoría y Trazabilidad
Cada movimiento queda registrado en `_Audit/audit.db`. Esto permite responder:
- "¿Dónde quedó el archivo X?"
- "¿Quién movió este archivo?" (Agente vs Humano)
- "¿Estaba duplicado?"
