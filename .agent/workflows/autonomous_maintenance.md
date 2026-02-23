---
description: Autonomous Maintenance of Drive H
---
# Mantenimiento Autónomo de Unidad H

Este flujo de trabajo está configurado para ejecutarse sin solicitar confirmación en cada paso (Modo Turbo), optimizando la autonomía del agente.

// turbo-all
1. Ejecutar script de clasificación base
   `python scripts/organize_drive_h.py`

2. Ejecutar organización profunda (Año/Tipo)
   `python scripts/organize_admin_deep.py`

3. Verificar integridad de datos
   `python scripts/verify_ingestion.py`

4. Generar reporte de estado
   `Get-Date > docs/audit/last_organization_run.txt`
