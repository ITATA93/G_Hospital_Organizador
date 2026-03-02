# TODO — G_Hospital_Organizador (SAIA)

> Prioritized task list. Update regularly.

## High Priority

(No pending high-priority items)

## Medium Priority

- [ ] Add more community skills as needed
- [ ] Implement real-time folder monitoring with watchdog
- [ ] Add OCR pipeline for scanned PDF classification
- [ ] Create dashboard de metricas de organizacion documental

## Low Priority

- [ ] Add openpyxl metadata extraction for Excel files
- [ ] Implement rollback feature in MigrationEngine
- [ ] Add support for .msg (Outlook) email classification

## Completed

- [x] Implement File Organizer Logic (Python/Pandas) (2026-03-01: `src/organizer.py`) <!-- id: hospital-1 -->
- [x] Define "Unidades Hospitalarias" folder structure (2026-03-01: `config/folder_structure.yaml`) <!-- id: hospital-2 -->
- [x] **Popular Knowledge Vault**: Migrar documentos a `docs/knowledge_vault/` (2026-03-01) <!-- id: doc-1 -->
  - [x] Estructurar Protocolos de Urgencias (2026-03-01: `docs/protocolos_urgencias.md`) <!-- id: doc-2 -->
  - [x] Documentar Arquitectura HIS (2026-03-01: `docs/arquitectura_his.md`) <!-- id: doc-3 -->
- [x] Configure MCP servers for external integrations (2026-03-01: `.claude/mcp.json` verified)
- [x] Set up CI/CD pipeline (GitHub Actions) (2026-03-01: `.github/workflows/ci.yml` enhanced)
- [x] Add project-specific skills to .gemini/skills/ (2026-02-18: `hospital-document-classifier.md`)
- [x] Create custom workflows for common tasks (2026-02-18: `turbo-ops.md` + `autonomous_maintenance.md`)
- [x] Add official Anthropic skills (Claude skills present in `.claude/skills/official/`)
- [x] Fix F-05: Define JSON Schemas for Agent outputs
- [x] Fix F-04: Implement RequestID tracing middleware
- [x] Fix F-06: Robust relative paths in config
- [x] Fix F-01: Accept Danger Mode risk
- [x] Fix F-02: Implement Persistent Memory System (sync script)
- [x] Fix F-03/F-04: Implement API Security (Auth & CORS)
- [x] Normalize Workspace & Global Profile
- [x] Create /help command (Multi-Vendor)
- [x] Complete initial workspace setup
- [x] Verify all sub-agents are functional
- [x] Create global profile structure
- [x] Define 6 specialized sub-agents (now 7 with researcher)
- [x] Set up Claude Code commands
- [x] Create project template
- [x] Run `gemini /bootstrap` (Pre-configured by Agent)

---

Last updated: 2026-03-01
