import re
from pathlib import Path
from typing import Any, Dict, List

import structlog

# Optional OCR import
try:
    import pypdf

    HAS_PYPDF = True
except ImportError:
    HAS_PYPDF = False

logger = structlog.get_logger()


class ContentAnalyzer:
    def __init__(self):
        # Regex patterns for Hospital Entities
        self.patterns = {
            "rut": r"\b\d{1,2}\.?\d{3}\.?\d{3}-[\dkK]\b",
            "date": r"\b\d{1,2}[-/]\d{1,2}[-/]\d{2,4}\b",
            "unit": [
                r"Unidad de [\w\s]+",
                r"Servicio de [\w\s]+",
                r"Departamento de [\w\s]+",
            ],
            "doc_type": [
                r"MEMORANDUM",
                r"RESOLUCION",
                r"ORDINARIO",
                r"INFORME",
                r"FACTURA",
                r"BOLETA",
            ],
        }

    def analyze_file(self, file_path: Path) -> Dict[str, Any]:
        """Deep analysis of file content to extract metadata."""
        ext = file_path.suffix.lower()
        metadata = {
            "doc_type": "Unknown",
            "extracted_date": None,
            "entities": [],
            "needs_ocr": False,
        }

        if ext == ".pdf":
            text = self._extract_pdf_text(file_path)
            if not text or len(text) < 50:
                metadata["needs_ocr"] = True
            else:
                self._extract_from_text(text, metadata)

        elif ext in [".txt", ".log", ".md"]:
            try:
                text = file_path.read_text(errors="ignore")
                self._extract_from_text(text, metadata)
            except:
                pass

        return metadata

    def _extract_pdf_text(self, path: Path) -> str:
        if not HAS_PYPDF:
            return ""
        try:
            reader = pypdf.PdfReader(path)
            text = ""
            # Read first 3 pages usually enough for header/dates
            for page in reader.pages[:3]:
                text += page.extract_text() + "\n"
            return text
        except Exception as e:
            logger.warning("pdf_read_error", file=str(path), error=str(e))
            return ""

    def _extract_from_text(self, text: str, metadata: Dict):
        text_upper = text.upper()

        # Doc Type
        for dtype in self.patterns["doc_type"]:
            if dtype in text_upper:
                metadata["doc_type"] = dtype.title()
                break

        # Units (Heuristic)
        for pattern in self.patterns["unit"]:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for m in matches:
                if len(m) < 50:  # Avoid capturing too long noise
                    metadata["entities"].append(m.strip())

        # Dates (Naive)
        dates = re.findall(self.patterns["date"], text)
        if dates:
            metadata["extracted_date"] = dates[0]
