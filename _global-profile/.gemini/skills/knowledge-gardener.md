# Skill: Knowledge Gardener

## Purpose
Proactively analyze the codebase to identify documentation gaps, outdated information, and missing architectural records.
Think of this as a "Linter for your Documentation".

## Capabilities
- **Gap Analysis**: Compare `src/` vs `docs/`.
- **Drift Detection**: Identify docs that haven't been touched in months while code changed.
- **Structure Enforcement**: Ensure `docs/` hierarchy follows `CORE_CONCEPTS.md`.

## Requirements
- Access to `codebase_search` (Gemini) or comprehensive `grep` (Claude).

## Usage
```bash
gemini /garden
```

## Process (The Algorithm)
1.  **Inventory**: List all files in `src/` and `docs/`.
2.  **API Audit**:
    *   Find all API endpoints (e.g., `@app.get`, `router.post`).
    *   Check if `docs/api/` contains corresponding references.
3.  **DB Audit**:
    *   Find all models (e.g., `class User(Model)`).
    *   Check if `docs/database/` reflects the current schema.
4.  **Freshness Check**:
    *   Find docs older than 30 days.
    *   Check if linked code has changed recently (git blame).
5.  **Report Generation**:
    *   Create `docs/audit/knowledge_gap_report.md`.
    *   List "Missing Docs" (High Priority).
    *   List "Stale Docs" (Medium Priority).

## Output Example
```markdown
# Knowledge Gap Report
_Date: 2026-02-02_

## 🚨 Critical Gaps (Undocumented Code)
- `src/routers/auth.py`: No corresponding implementation detail in `docs/api/`.
- `recipies_db`: Table exists in code but not in Schema doc.

## ⚠️ Stale Documentation
- `docs/architecture/legacy.md`: Last updated 6 months ago. Core code changed yesterday.

## 🌱 Recommendations
1. Run `gemini /doc src/routers/auth.py` to fix auth documentation.
```
