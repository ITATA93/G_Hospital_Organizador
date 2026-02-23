# Auditoría de Normalización — AG_Hospital_Organizador
> **Fecha**: 2026-02-18
> **Referencia**: AG_Plantilla (C:\_Repositorio\AG_Plantilla)

---

## Infraestructura

| Item | Antes | Notas |
|------|-------|-------|
| GEMINI.md en raíz | ✅ SI | Adaptado al proyecto (8.6 KB) |
| CLAUDE.md en raíz | ✅ SI | Adaptado al proyecto (7.9 KB) |
| README.md | ✅ SI | Actualizado (3.2 KB) |
| CHANGELOG.md | ✅ SI | Presente (323 B, pocas entradas) |
| docs/TASKS.md | ✅ SI | Formato unified (cross_task.py) |
| docs/DEVLOG.md | ✅ SI | Última entrada: 2026-02-02 |
| docs/standards/output_governance.md | ✅ SI | Presente (encoding issues en chars especiales) |
| .gitignore | ✅ SI | Cubre .env, credentials/, secrets/, *.pem, *.key |

## Agentes

| Item | Antes | Notas |
|------|-------|-------|
| .subagents/manifest.json | ✅ SI | 7 agentes definidos |
| .subagents/dispatch.sh | ✅ SI | Presente (6.6 KB) |
| .subagents/dispatch.ps1 | ❌ NO | Falta versión PowerShell |

### Agentes definidos (7/7)
| Agente | Vendor | Estado |
|--------|--------|--------|
| code-analyst | gemini | ✅ Configurado |
| doc-writer | gemini | ✅ Configurado |
| code-reviewer | claude | ✅ Configurado |
| test-writer | gemini | ✅ Configurado |
| db-analyst | claude | ✅ Configurado |
| deployer | gemini | ✅ Configurado |
| researcher | codex | ✅ Configurado |

## Skills

### .claude/skills/ (28 skills total)

#### Official (16)
| Skill | Clasificación |
|-------|---------------|
| algorithmic-art | NO_APLICA |
| brand-guidelines | NO_APLICA |
| canvas-design | NO_APLICA |
| doc-coauthoring | RELEVANTE |
| docx | RELEVANTE |
| frontend-design | NO_APLICA |
| internal-comms | NO_APLICA |
| mcp-builder | NO_APLICA |
| pdf | RELEVANTE |
| pptx | NO_APLICA |
| skill-creator | GENÉRICA |
| slack-gif-creator | NO_APLICA |
| theme-factory | NO_APLICA |
| web-artifacts-builder | NO_APLICA |
| webapp-testing | NO_APLICA |
| xlsx | RELEVANTE |

#### Community (12)
| Skill | Clasificación |
|-------|---------------|
| d3js-visualization | NO_APLICA |
| ffuf-fuzzing | NO_APLICA |
| ios-simulator | NO_APLICA |
| loki-mode | NO_APLICA |
| obra-superpowers | GENÉRICA |
| obra-superpowers-community | GENÉRICA |
| obra-superpowers-lab | GENÉRICA |
| playwright-testing | NO_APLICA |
| scientific-skills | NO_APLICA |
| skill-seekers-tool | GENÉRICA |
| trailofbits-security | GENÉRICA |
| web-asset-generator | NO_APLICA |

#### Referencia
- community-skills-reference.md (4.7 KB)
- official-skills-reference.md (1.3 KB)

### .claude/commands/ (5 commands)
| Comando | Descripción |
|---------|-------------|
| create-tests.md | Crear tests |
| help.md | Ayuda |
| project-status.md | Estado del proyecto |
| quick-review.md | Revisión rápida |
| update-docs.md | Actualizar documentación |

### .claude/internal-agents/
❌ No existe

### .gemini/skills/ (3 archivos)
| Skill | Tipo |
|-------|------|
| deep-research.md | Referencia (no ejecutable) |
| project-init.md | Referencia (no ejecutable) |
| project-memory.md | Referencia (no ejecutable) |

### .agent/skills/ (1 skill)
| Skill | Estado |
|-------|--------|
| document-processor (document_processing/) | ✅ RELEVANTE – Core SAIA skill |

## Workflows

### .agent/workflows/ (1 workflow)
| Workflow | Frontmatter | Funcional |
|----------|-------------|-----------|
| autonomous_maintenance.md | ✅ `description: Autonomous Maintenance of Drive H` | ✅ SI |

**Falta**: turbo-ops.md (existe en AG_Plantilla)

## Memoria y Config

| Item | Antes | Notas |
|------|-------|-------|
| .gemini/brain/ | ✅ SI | Directorio vacío |
| .gemini/settings.json | ✅ SI | Configurado (profile, agents, codeExecution) |
| .claude/settings.local.json | ❌ NO | No existe |
| .claude/mcp.json | ❌ NO | No existe |

## Seguridad

| Item | Antes | Notas |
|------|-------|-------|
| Credenciales hardcodeadas en src/ | ✅ LIMPIO | No se encontraron |
| Credenciales hardcodeadas en config/ | ✅ LIMPIO | No se encontraron |
| Credenciales hardcodeadas en scripts/ | ✅ LIMPIO | No se encontraron |
| .env.example | ✅ SI | Presente (713 B) |
| .gitignore cubre .env | ✅ SI | .env, .env.local, .env.*.local |
| .gitignore cubre credentials | ✅ SI | credentials/, secrets/, *.pem, *.key |

---

## Resumen Pre/Post-Normalización

| Categoría | Antes | Después | Δ |
|-----------|-------|---------|---|
| Infraestructura (archivos raíz) | 10 | 10 | — |
| TASKS.md formato | 10 | 10 | — |
| DEVLOG.md | 7 | 10 | +3 |
| Agentes (.subagents/) | 8 | 10 | +2 |
| Claude Skills | 3 | 9 | +6 |
| Gemini Skills | 4 | 8 | +4 |
| Antigravity Skills | 10 | 10 | — |
| Workflows | 5 | 10 | +5 |
| Memoria/Config | 6 | 8 | +2 |
| Seguridad | 10 | 10 | — |

**Score Antes: 73/100**
**Score Después: 95/100**
**Delta: +22 puntos**

### Acciones Realizadas
1. ✅ Archivadas 18 Claude skills NO_APLICA a `_archived/` (11 official, 7 community)
2. ✅ Creada skill Gemini `hospital-document-classifier.md` (dominio SAIA)
3. ✅ Copiado `turbo-ops.md` workflow desde AG_Plantilla
4. ✅ Copiado `dispatch.ps1` desde AG_Plantilla
5. ✅ Corregida encoding de `output_governance.md`
6. ✅ TASK-2026-0003 completada y marcada DONE
7. ✅ Actualizado DEVLOG.md con sesión de normalización
8. ✅ Actualizado CHANGELOG.md con registro de cambios
