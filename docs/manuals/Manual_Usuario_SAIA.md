# Manual de Usuario - SAIA (Sistema de Archivo Inteligente Auditado)

**Unidad de Gestión de Cuidados Oncológicos (UGCO)**

## 1. Introducción
El Sistema SAIA organiza automáticamente sus documentos en la unidad `H:`. 
A diferencia de un "ordenar" tradicional, SAIA **propone** cambios antes de hacerlos y **registra** todo lo que hace.

## 2. Nueva Estructura del Disco
Sus archivos se moverán gradualmente a:
`H:\_UGCO_Disco G_PC_Jefatura\_Estructura_Final_SAIA\`

Esta carpeta contiene:
- 📂 **02_Administrativo_Central**: Toda la documentación institucional.
  - 📂 **2024**
    - 📂 **Memorandums**
    - 📂 **Resoluciones**
  - 📂 **2025**
    - ...
- 📂 **01_Personal**: Archivos privados (Fotos, Whatsapp) aislados.
- 📂 **03_Clinico**: Fichas de pacientes aisladas (Seguridad de la Información).

## 3. Cómo usar el Sistema

### Paso 1: Escaneo (Automático)
El sistema revisa qué archivos nuevos han aparecido.
*Comando*: `python saia_cli.py scan`

### Paso 2: Análisis Inteligente (Opcional)
Si hay PDFs escaneados (imágenes), el sistema intenta leer el texto para saber qué son.
*Comando*: `python saia_cli.py enrich`

### Paso 3: Generar Propuesta
El sistema crea un Plan de Ordenamiento. **No mueve nada aún.**
*Comando*: `python saia_cli.py plan`
*Salida*: Crea un archivo `migration_proposal.yaml` que usted puede abrir con el Bloc de Notas.

### Paso 4: Aprobar el Plan
Usted lee el archivo `yaml`. Si está de acuerdo con los movimientos propuestos (Ej: "Mover memo.pdf a carpeta 2024/Memorandums"), ejecuta la orden.
*Comando*: `python saia_cli.py execute --target migration_proposal.yaml`

## 4. Preguntas Frecuentes

**¿Qué pasa si me equivoco?**
SAIA guarda un registro de todo. En la versión 2.0 se habilitará el botón de "Deshacer". Por ahora, los archivos originales se mantienen hasta que usted verifique la copia.

**¿Dónde están mis programas?**
SAIA detecta carpetas con programas (.exe) y **no las toca** para evitar que dejen de funcionar.

**¿Qué es la carpeta `_Audit`?**
Es una carpeta oculta. ¡No la borre! Contiene la memoria del sistema.
