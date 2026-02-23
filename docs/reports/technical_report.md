# Reporte Técnico: Sistema de Archivo Inteligente (SAIA)
**Proyecto**: AG_Hospital_Organizador
**Fecha**: 2026-02-03
**Versión**: 1.0

## 1. Resumen Ejecutivo
Este documento detalla la implementación del sistema SAIA para la reorganización de la unidad administrativa. El sistema ha procesado más de 8,000 archivos, estructurándolos en una jerarquía lógica y separando documentos personales y software.

## 2. Arquitectura del Sistema
El núcleo se compone de cuatro módulos secuenciales:
1.  **Audit Vault**: Base de datos SQLite (`_Audit/audit.db`) que mantiene un inventario hash-a-hash de cada archivo.
2.  **Inventory Scanner**: Indexa archivos calculando SHA-256 para detectar duplicados y cambios.
3.  **Planner (Architect)**: Motor de inferencia que decide el destino de cada archivo basado en heurísticas (Regex para DocType) y Cohesión de Clusters (Software).
4.  **Migration Engine**: Ejecutor transaccional que realiza copias verificadas (Copy-Verify-Delete).

## 3. Algoritmos Clave

### 3.1 Detección de Cohesión (Software Shield)
Para evitar corromper instaladores o programas portables, el sistema identifica "Clusters" de software.
- **Regla**: Si un directorio contiene `.exe`, `.dll`, `.py`, o `.bin`.
- **Acción**: El directorio padre se marca como "Cluster" y se migra intacto a `01_Software_Detectado`.

### 3.2 Clasificación Documental
Los archivos se clasifican en:
- **02_Administrativo_Central**: Documentos institucionales (Memorándums, Resoluciones, Informes).
- **03_Personal**: Archivos detectados como privados (CVs, Contratos personales, Fotos).

## 4. Resultados de la Ejecución
- **Total Archivos Escaneados**: ~8,100
- **Plan generado**: ID `SAIA-20260203-1636`
- **Tasa de Éxito**: [En Proceso]
- **Logs de Auditoría**: Disponibles en `_Audit/logs/`

## 5. Instrucciones de Recuperación (Rollback)
El sistema mantiene un log JSON de cada movimiento. En caso de error crítico:
1.  Ubicar el archivo de log `execution_{ID}.json`.
2.  Ejecutar el script de reversa (programado para v2.1, actualmente manual usando el JSON como mapa de ruta inverso).
