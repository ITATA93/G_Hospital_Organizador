# Guía de Usuario: Sistema Antigravity

¡Bienvenido al sistema operativo agéntico Antigravity! Esta guía te ayudará a navegar y operar tu entorno de desarrollo potenciado por IA.

## 🚀 Inicio Rápido

Para empezar una sesión de trabajo:
`gemini /session:start`

Para cerrar y documentar:
`gemini /session:end`

## 🧠 ¿Cómo funciono? (Agentes y Triggers)

No necesitas recordar comandos complejos. Solo dime qué necesitas, y yo (tu Agente Arquitecto) delegaré a los especialistas.

| Si dices... | Ejecuto a... | Para qué sirve |
| :--- | :--- | :--- |
| "Analiza este código..." | **code-analyst** | Entender arquitectura y lógica. |
| "Documenta esto..." | **doc-writer** | Crear README, Changelogs, Guías. |
| "Busca bugs/seguridad..." | **code-reviewer** | Auditoría y calidad de código. |
| "Crea tests..." | **test-writer** | Generar pruebas unitarias/e2e. |
| "Consulta la base de datos..." | **db-analyst** | Análisis SQL y esquemas. |
| "Configura el deploy..." | **deployer** | Docker, CI/CD, Infraestructura. |

## 📦 Migrando Proyectos Existentes

Si traes un proyecto de otro lado, el flujo recomendado es:

1.  **Analizar**:
    > "Analiza el proyecto en [ruta] para migrarlo a Antigravity."

2.  **Planificar**:
    Yo generaré un plan detallado (`docs/plans/migration_plan.md`) sugiriendo estructura y cambios.

3.  **Ejecutar**:
    Una vez apruebes el plan, ejecutaremos la migración paso a paso.

## 📂 Organización de Archivos

Mantenemos la higiene estricta:
- **`src/`**: Tu código fuente real.
- **`docs/`**: Documentación viva.
    - `docs/plans/`: Planes temporales.
    - `docs/audit/`: Reportes de auditoría.
- **`.gemini/` & `.claude/`**: Cerebros de los agentes.

## 🆘 Comandos Útiles

| Comando | Descripción |
| :--- | :--- |
| `/help` (o `@Ayuda`) | Muestra esta guía. |
| `/project:status` | Resumen del estado actual. |
| `/parallel:run` | Ejecuta múltiples agentes a la vez. |
