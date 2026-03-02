---
depends_on: []
impacts: []
---

# Changelog — G_Hospital_Organizador

All notable changes to this project will be documented in this file.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Added

- `src/organizer.py`: File organizer module with `classify_document()`,
  `organize_directory()`, and `generate_report()` functions. Classifies
  hospital documents by type (protocolos, manuales, normas, actas, informes,
  memorandums, resoluciones, circulares, contratos, facturas, planillas,
  presentaciones) using regex pattern matching. Supports pandas for
  CSV/Excel metadata extraction.
- `config/folder_structure.yaml`: Complete hospital unit folder hierarchy
  defining 16 units (Urgencia, Pabellon, UCI, Medicina, Cirugia, Pediatria,
  Maternidad, Imagenologia, Laboratorio, Farmacia, Direccion, Calidad,
  RRHH, Abastecimiento) with document types, retention rules, and
  keywords for automatic classification.
- `docs/protocolos_urgencias.md`: Structured emergency protocols including
  Triage (ESI), Codigo Azul (paro cardiorrespiratorio), Codigo Rojo
  (hemorragia obstetrica/trauma mayor), Atencion al Politraumatizado
  (ATLS), and Protocolo de Intoxicaciones (CITUC).
- `docs/arquitectura_his.md`: HIS architecture documentation covering
  TrakCare/InterSystems IRIS, SIDRA, ALMA, RIS/PACS, LIS, HL7 v2.5
  integrations, network infrastructure, and data flow diagrams.
- `docs/knowledge_vault/`: Populated vault with README indices for
  administracion, sistemas, normativa, and calidad sections.
- `tests/unit/test_organizer.py`: Unit test suite for the organizer module
  (20 tests covering classification, organization, and reporting).

### Changed

- `.github/workflows/ci.yml`: Enhanced CI pipeline with pip caching,
  YAML config validation step, ruff format check, and proper env vars.
- `docs/TODO.md`: All 7 pending items marked as completed.
- `docs/knowledge_vault/README.md`: Updated with complete vault structure,
  new sections (normativa, calidad), and proper frontmatter.

### Verified

- `.claude/mcp.json`: MCP server configuration confirmed matching the
  G_Plantilla template pattern (gen-memory, gen-tasks, gen-workflows,
  gen-prompts, filesystem, github, fetch).
- Governance audit: docs/TODO.md verified
- README.md enhanced with architecture and usage docs
- Gemini CLI integration validated

## [1.0.0] — 2026-02-23

### Initial Release

- Full GEN_OS mirror infrastructure migrated from AG_Hospital_Organizador.
- Multi-vendor dispatch: .subagents/, .claude/, .codex/, .gemini/, .agent/.
- Governance standards: docs/standards/.
- CI/CD workflows: .github/workflows/.
- All domain content preserved from AG_Hospital_Organizador.
