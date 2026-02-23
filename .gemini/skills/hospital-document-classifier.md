---
name: hospital-document-classifier
description: Classifies and organizes hospital documents by type, unit, and date using file metadata and content analysis
---

# Hospital Document Classifier

Skill for classifying hospital documents (administrative, clinical references, manuals) into the SAIA directory structure.

## When to Use
- When processing new batches of documents from hospital units
- When organizing files from network drives (e.g., Drive H)
- When performing audit of document organization

## Classification Categories

| Category | Directory Pattern | Examples |
|----------|------------------|----------|
| Administrative | `Administrativos/{Year}/` | Memos, circulars, resolutions |
| Clinical Manuals | `Manuales/` | Protocols, procedures, guides |
| Reports | `Reportes/{Year}/` | Monthly reports, audit results |
| Regulatory | `Normativa/` | MINSAL norms, legal docs |
| Training | `Capacitacion/{Year}/` | Training materials, certificates |

## Steps

1. **Read file metadata**: Extract filename, extension, creation date, modification date
2. **Analyze content** (if PDF/image): Use OCR or text extraction to identify document type
3. **Classify**: Match against the category table above
4. **Determine destination**: Build target path using `Type/Year/` pattern
5. **Verify**: Check for duplicates using SHA-256 hash before moving

## Rules
- NEVER delete original files — use Copy-Verify-Delete pattern
- NEVER process files containing patient data without explicit confirmation
- Always log actions to `docs/DEVLOG.md`
- Always generate a report in `docs/audit/` after batch processing

## Integration
This skill works with:
- `scripts/organize_drive_h.py` — Base classification
- `scripts/organize_admin_deep.py` — Deep organization
- `scripts/verify_ingestion.py` — Integrity verification
- `.agent/skills/document_processing/` — PDF/Image metadata extraction
