# Antigravity Quick Start Guide

Guía rápida para usar el sistema de desarrollo multi-agente Antigravity.

## Instalación Rápida

### 1. Instalar Herramientas

```bash
# Gemini CLI
npm install -g @anthropic-ai/gemini-cli

# Claude Code CLI
npm install -g @anthropic-ai/claude-code

# GitHub CLI (para migración automática)
# Windows: winget install GitHub.cli
# Mac: brew install gh
# Linux: https://github.com/cli/cli/releases
```

### 2. Instalar Perfil Global

```powershell
# Windows
cd AG_Plantilla\_global-profile
.\install-global.ps1

# Linux/Mac
cd AG_Plantilla/_global-profile
chmod +x install-global.sh
./install-global.sh
```

### 3. Verificar Instalación

```bash
gemini 'Hello, verify installation'
gemini -e code-analyst 'List available agents'
```

---

## Uso Diario

### Comandos Gemini Principales

| Comando | Descripción |
|---------|-------------|
| `gemini "pregunta"` | Pregunta directa |
| `gemini -e agent "tarea"` | Usar agente específico |
| `gemini /migrate` | Migrar proyecto a AG_ |
| `gemini /session:start` | Iniciar sesión de trabajo |
| `gemini /session:end` | Finalizar sesión |

### Agentes Disponibles

| Agente | Uso |
|--------|-----|
| `code-analyst` | Analizar código, explicar arquitectura |
| `doc-writer` | Escribir documentación |
| `code-reviewer` | Revisar código, buscar bugs |
| `test-writer` | Crear tests |
| `db-analyst` | Consultas SQL, esquemas |
| `deployer` | Docker, CI/CD |

### Ejemplos de Uso

```bash
# Analizar código
gemini -e code-analyst 'Explica la arquitectura de este proyecto'

# Revisar seguridad
gemini -e code-reviewer 'Busca vulnerabilidades en src/'

# Crear documentación
gemini -e doc-writer 'Actualiza el README con las nuevas features'

# Crear tests
gemini -e test-writer 'Crea tests unitarios para src/utils/'
```

---

## Migrar Proyecto Existente

### Método Rápido

```powershell
# Windows
cd AG_Plantilla\_template
.\migrate-project.ps1 -ProjectPath "C:\mi-proyecto"

# Linux/Mac
cd AG_Plantilla/_template
./migrate-project.sh /path/to/mi-proyecto
```

### Resultado

```
mi-proyecto (original - SIN CAMBIOS)
    ↓
AG_mi-proyecto (copia con Antigravity)
    ↓
GitHub: AG_mi-proyecto (repositorio privado)
```

### Post-Migración

1. `cd AG_mi-proyecto`
2. Editar `GEMINI.md` con contexto del proyecto
3. Probar: `gemini 'Analiza este proyecto'`

---

## Clasificador de Complejidad

Antes de cada tarea, clasifica:

| Nivel | Criterio | Acción |
|-------|----------|--------|
| **NIVEL 1** | 0-1 archivos, pregunta simple | Respuesta directa |
| **NIVEL 2** | 2-3 archivos, tarea definida | 1 agente especializado |
| **NIVEL 3** | 4+ archivos, tarea ambigua | Pipeline de agentes |

### Ejemplo de Pipeline (NIVEL 3)

```bash
# 1. Entender el problema
gemini -e code-analyst 'Analiza el módulo de autenticación'

# 2. Implementar solución
gemini -e code-writer 'Refactoriza según el análisis anterior'

# 3. Validar resultado
gemini -e code-reviewer 'Revisa los cambios realizados'
```

---

## Estructura de Proyecto AG_

```
AG_mi-proyecto/
├── .gemini/              # Configuración Gemini
│   ├── agents/           # Agentes del proyecto
│   ├── commands/         # Comandos personalizados
│   ├── rules/            # Reglas del proyecto
│   └── settings.json     # Configuración
├── .claude/              # Configuración Claude
│   └── commands/         # Comandos para Claude
├── .subagents/           # Manifest de sub-agentes
│   └── manifest.json
├── docs/                 # Documentación
├── GEMINI.md             # Instrucciones para Gemini
├── CLAUDE.md             # Instrucciones para Claude
└── CHANGELOG.md          # Historial de cambios
```

---

## Archivos Clave

### GEMINI.md
Instrucciones para Gemini CLI. Incluye:
- Contexto del proyecto
- Reglas específicas
- Agentes disponibles
- Clasificador de complejidad

### CLAUDE.md
Instrucciones para Claude Code. Incluye:
- Descripción del proyecto
- Comandos rápidos
- Estructura del código

### manifest.json
Configuración de sub-agentes:
```json
{
  "project": "AG_mi-proyecto",
  "agents": [
    { "name": "code-analyst", "triggers": ["analiza", "explica"] },
    { "name": "doc-writer", "triggers": ["documenta", "README"] }
  ]
}
```

---

## Tips y Buenas Prácticas

### 1. Lee antes de escribir
```bash
# Siempre analiza primero
gemini -e code-analyst 'Explica cómo funciona X'
# Luego modifica
gemini 'Ahora modifica X para hacer Y'
```

### 2. Usa el agente correcto
- **code-analyst** para entender
- **code-reviewer** para validar
- **doc-writer** para documentar

### 3. Commits atómicos
```
feat(auth): add login endpoint
fix(api): handle null response
docs(readme): update installation steps
```

### 4. Actualiza docs/
Después de cambios significativos:
```bash
gemini -e doc-writer 'Actualiza CHANGELOG.md'
gemini -e doc-writer 'Actualiza docs/DEVLOG.md'
```

---

## Solución de Problemas

### Agente no responde
```bash
# Verifica configuración
gemini -v -e code-analyst 'test'
```

### Error de permisos GitHub
```bash
gh auth login
gh auth status
```

### Configuración no se aplica
```bash
# Reinstalar perfil global
cd _global-profile
./install-global.sh --force
```

---

## Recursos

- **Workspace**: `AG_Plantilla/`
- **Perfil Global**: `_global-profile/`
- **Plantillas**: `_template/`
- **Recursos Oficiales**: `_resources/`

---

*Antigravity Multi-Agent Development System*
