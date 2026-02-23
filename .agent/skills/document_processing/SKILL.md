---
name: document-processor
description: Extracts metadata and content from hospital documents (PDFs, Images).
---

# Document Processor Skill

This skill provides capabilities to analyze hospital documents and extract structured data.

## Capabilities

1.  **PDF Text Extraction**: Extract raw text from PDF files.
2.  **Metadata Extraction**: Identify administrative fields:
    -   **Document Type**: "Memorandum", "Ordinario", "Resolución", "Informe", "Protocolo", "Factura".
    -   **Date**: Extract dates (Document date, not patient DOB).
    -   **Subject/Ref**: Look for "Ant:", "Mat:", "Asunto:", "Ref:".
    -   **Department/Unit**: Identify origin or destination unit.
3.  **Document Classification**: Categorize based on administrative function (HR, Finance, Operations).
4.  **Directory Cohesion (Software Clusters)**:
    -   **Rule**: If a folder contains `.exe`, `.dll`, `.py`, `.js` (code/binaries), mark it as a "Cluster".
    -   **Action**: DO NOT migrate individual files inside a cluster. Move the WHOLE folder as-is.

## Usage

When automating organization:
1.  **Check Cohesion**: Is the parent folder a Software Cluster?
    -   YES: Mark for "Cluster Move".
    -   NO: Proceed to file analysis.
2.  **Scan File**:
    -   Attempt text extraction (native).
    -   If empty/scan -> Use OCR (Tesseract).
3.  **Enrich**: Identify DocType (e.g., "MEMORANDUM N°") + Date.
4.  **Return**: `Category/Year/Month/DocType` OR `Software/ClusterName`.
