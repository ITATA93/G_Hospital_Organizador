# Análisis: Automatización de la Creación de "Profile" (Global vs Local)

**Fecha**: 2026-02-02
**Estado**: Borrador de Diseño

## 1. Situación Actual
Actualmente, la configuración global de los agentes ("Profile") reside en `_global-profile/` dentro del repositorio `AG_Plantilla`.
Para que los agentes (Gemini/Claude CLI) reconozcan estos cambios, el usuario debe ejecutar manualmente:
- `install-global.ps1` (Windows)
- `install-global.sh` (Linux/Mac)

Esta operación realiza una **COPIA FÍSICA** de `_global-profile/.gemini` a `~/.gemini` (User Home).

### Problemas Detectados
1.  **Desincronización (Drift)**: Si editamos un agente en `_global-profile/`, no tendrá efecto hasta reinstalar.
2.  **Fricción**: El desarrollador olvida ejecutar el script de instalación tras actualizaciones.
3.  **Redundancia**: Tenemos definiciones duplicadas en `AG_Plantilla` y en `~/.gemini`.

### Importancia Crítica: Herramientas y Configuración
Más allá de los agentes (que suelen sobrescribirse por proyecto), la descoordinación es crítica en:
-   **Scripts Globales** (`scripts/deep-research.sh`, etc.): Si se corrige un bug en el repo pero no se actualiza en global, fallará en todos los proyectos.
-   **Configuración Base** (`settings.json`): Nuevos flags experimentales o cambios en timeouts requieren actualización inmediata.
-   **Reglas Globales**: Normas de seguridad o estilo que deben aplicar transversalmente.

## 2. Propuesta de Automatización

¿Es necesario automatizarlo? **SÍ**, pero con matices.

### Opción A: Enlaces Simbólicos (Recomendada para Devs)
En lugar de copiar, crear un enlace simbólico (Symlink/Junction) desde `~/.gemini` apuntando a `_global-profile/.gemini`.
*   **Pros**: Sincronización inmediata. Editamos en el repo y el agente global se actualiza al instante.
*   **Contras**: Riesgo de romper el agente global si borramos el repo.

### Opción B: "Sync on Session Start" (Recomendada para Usuarios)
Agregar un paso en el workflow `session-start` de Gemini que verifique si hay cambios en el perfil global y ofrezca actualizarlos.
*   **Pros**: Seguro, controlado.
*   **Contras**: Añade latencia al inicio de sesión.

### Opción C: "Project-Local Priority" (Arquitectura Actual)
Antigravity ya prioriza la configuración local (`.gemini/` en la raíz del proyecto) sobre la global.
*   **Ventaja**: Si el proyecto tiene su propio `.gemini/agents`, no necesita tocar el perfil global.
*   **Limitación**: Los skills globales y herramientas core sí dependen del global.

## 3. Conclusión y Recomendación

No deberíamos "automatizar la creación" ciega (sobrescribir silenciosamente), sino **automatizar la sincronización**.

**Recomendación**:
1.  **Modificar `install-global.ps1`** para soportar un modo `--link` (Symlink) para desarrolladores del core.
2.  **Mantener la copia para usuarios finales**, pero agregar un check de versión en el inicio de sesión.

**Veredicto**: La automatización es necesaria para evitar la divergencia de configuración, pero debe ser explícita (Links o Sync), no mágica.
