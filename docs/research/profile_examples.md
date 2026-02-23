# Ejemplos de Configuración de Perfiles en Antigravity

Antigravity permite dos niveles de configuración: **Global** (`~/.gemini/settings.json`) y **Por Proyecto** (`<proyecto>/.gemini/settings.json`).
La configuración del proyecto siempre sobrescribe a la global (Merge profundo).

Aquí tienes ejemplos de cómo configurar distintos "sabores" o perfiles para diferentes necesidades.

## 1. Perfil "Backend Hardcore" (Nivel Proyecto)
*Optimizado para python, bases de datos y seguridad. Desactiva herramientas de diseño.*

**Archivo**: `<proyecto>/.gemini/settings.json`

```json
{
  "profile": {
    "name": "backend-secure-profile",
    "description": "Perfil estricto para desarrollo Backend y API"
  },
  "agents": {
    "maxParallel": 2,          // Reducido para mayor control
    "autoDelegate": false      // Requiere aprobación manual para delegar
  },
  "codeExecution": {
    "enabled": true,
    "languages": ["python", "sql", "bash"], // Solo permite estos
    "sandbox": "strict"        // (Hipotético) Forzar sandbox containerizado
  },
  "experimental": {
    "codebaseInvestigatorSettings": {
      "maxTurns": 20,          // Mayor profundidad de análisis
      "maxTimeMinutes": 10
    }
  },
  "defaults": {
    "documentationLanguage": "en" // Forzar docs en inglés
  }
}
```

## 2. Perfil "Frontend Creativo" (Nivel Proyecto)
*Maximiza la velocidad y herramientas de UI. Permite ejecución de JS/TS.*

**Archivo**: `<proyecto>/.gemini/settings.json`

```json
{
  "profile": {
    "name": "frontend-creative-profile"
  },
  "agents": {
    "maxParallel": 6,          // Alta concurrencia para generar componentes
    "defaultTimeout": 600000   // Timeouts largos para tareas visuales
  },
  "codeExecution": {
    "enabled": true,
    "languages": ["javascript", "typescript", "css", "html"]
  },
  "mcpServers": {
    "figma": {                 // Servidor MCP específico (ejemplo)
      "command": "npx",
      "args": ["@mcp/figma-adapter"]
    }
  }
}
```

## 3. Perfil "Auditoría de Seguridad" (Global Alternativo)
*Diseñado para ser usado temporalmente durante auditorías. Solo lectura.*

**Archivo**: `~/.gemini/settings.json` (Intercambiable)

```json
{
  "profile": {
    "name": "security-auditor"
  },
  "codeExecution": {
    "enabled": false           // PROHIBIDO ejecutar código
  },
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["@anthropic-ai/mcp-filesystem", ".", "--readonly"] // Solo lectura
    }
  },
  "experimental": {
    "enableAgents": false      // Solo el agente principal, sin sub-agentes ruidosos
  }
}
```

## 4. Perfil "CI/CD Pipeline" (Headless)
*Para ejecución automática en Jenkins/GitHub Actions.*

**Archivo**: `ci-config.json` (Cargado via `gemini --config ci-config.json`)

```json
{
  "profile": {
    "name": "ci-robot"
  },
  "theme": "json",             // Salida parseable por máquinas
  "memory": {
    "persistent": false        // Sin memoria a largo plazo
  },
  "agents": {
    "autoDelegate": true
  },
  "defaults": {
    "codeLanguage": "en"
  }
}
```

## Cómo Gestionarlos
En la arquitectura actual de Antigravity:

1.  **Global vs Proyecto**: Es automático. Si creas `.gemini/settings.json` en tu carpeta de proyecto, hereda del global y sobrescribe lo que definas.
2.  **Multi-Global**: Si quieres tener varios perfiles globales (ej. "Personal" vs "Trabajo"), la mejor estrategia es usar **Symlinks** (referencia al análisis anterior):
    *   Tener `_global-profile/personal/settings.json`
    *   Tener `_global-profile/work/settings.json`
    *   Un script `switch-profile.ps1` que cambie el symlink `~/.gemini` a uno u otro.

## 5. Ejecución Dinámica (Run-time Switching)

¿Qué pasa si quiero usar el mismo proyecto con dos perfiles distintos sin cambiar archivos?

### A. Vía Argumento CLI (Recomendado)
Puedes inyectar un archivo de configuración específico al iniciar la sesión:

```bash
# Iniciar modo "Audit"
gemini /session:start --config .gemini/profiles/audit.json

# Iniciar modo "Dev Fast"
gemini /session:start --config .gemini/profiles/frontend-fast.json
```

### B. Vía Variables de Entorno
Útil para scripts o CI/CD donde no controlas los argumentos directos:

```bash
# Linux/Mac
GEMINI_PROFILE=ci-robot gemini /session:start

# Powershell
$env:GEMINI_PROFILE="backend-secure"; gemini /session:start
```

### C. Estructura de Carpetas Sugerida
Para mantener el orden, crea una carpeta `profiles/` en tu configuración:

```
.gemini/
├── settings.json       (Default)
├── profiles/
│   ├── security.json
│   ├── fast-dev.json
│   └── offline.json
```
