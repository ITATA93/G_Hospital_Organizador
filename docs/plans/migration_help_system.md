# Plan de Implementación: Comando Universal @Ayuda

**Objetivo:** Crear un punto de entrada amigable (`@Ayuda`) que explique al usuario cómo operar el sistema, los pasos iniciales y guías de migración.

## Estrategia
Implementaremos un "Comando Custom" en Gemini/Claude que responda a la invocación de ayuda. Como el sistema usa archivos `.toml` para comandos en Gemini y `.md` para Claude, crearemos ambos para compatibilidad total.

## 1. Archivo de contenido de Ayuda (`docs/GUIDE.md`)
Primero, centralizaremos el contenido "educativo" en un archivo markdown bien estructurado.
- **Secciones:**
    1.  **Bienvenida**: Qué es Antigravity.
    2.  **Primeros Pasos**: Configuración básica.
    3.  **Cómo funciono**: Explicación del sistema de Agentes y Triggers.
    4.  **Guía de Migración**: El flujo "Analiza -> Planifica -> Ejecuta".
    5.  **Comando útiles**: Tabla de comandos frecuentes.

## 2. Comando Gemini (`.gemini/commands/help.toml`)
Configuraremos un comando `/help` (o `@Ayuda` simulado vía alias si el CLI lo permite, o simplemente instruyendo al usuario a usar `/help`) que lea y resuma `docs/GUIDE.md`.

## 3. Comando Claude (`.claude/commands/help.md`)
Configuraremos un comando slash `/help` para Claude que inyecte el mismo contexto.

## Pasos de Ejecución
1.  [ ] Crear `docs/GUIDE.md` con el contenido educativo.
2.  [ ] Crear `.gemini/commands/help.toml`.
3.  [ ] Crear `.claude/commands/help.md`.
4.  [ ] Verificar que la estructura sea válida.

## Verificación
- Ejecutaré una validación de sintaxis sobre los archivos creados.
