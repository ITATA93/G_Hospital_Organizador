"""Unit tests for src/organizer.py — SAIA file organizer."""

import os
import tempfile
from pathlib import Path

import pytest

# Ensure test env vars are set before importing app code
os.environ.setdefault("API_KEY", "test-api-key-not-real")
os.environ.setdefault("APP_ENV", "development")

from src.organizer import (
    ClasificacionDocumento,
    ResultadoOrganizacion,
    classify_document,
    generate_report,
    organize_directory,
)


@pytest.fixture
def temp_dir():
    """Create a temporary directory with sample files for testing."""
    with tempfile.TemporaryDirectory() as tmpdir:
        root = Path(tmpdir)

        # Create sample hospital documents
        (root / "memorandum_001_2026.pdf").write_bytes(b"%PDF-fake")
        (root / "informe_gestion_urgencia_2025.docx").write_bytes(b"fake-docx")
        (root / "protocolo_triage_2026.pdf").write_bytes(b"%PDF-fake")
        (root / "resolucion_rex_123_2026.pdf").write_bytes(b"%PDF-fake")
        (root / "acta_comite_calidad_2026.docx").write_bytes(b"fake-docx")
        (root / "planilla_dotacion.xlsx").write_bytes(b"fake-xlsx")
        (root / "factura_proveedor_2026.pdf").write_bytes(b"%PDF-fake")
        (root / "circular_005_2026.pdf").write_bytes(b"%PDF-fake")
        (root / "documento_sin_tipo.pdf").write_bytes(b"%PDF-fake")

        # Create a subdirectory mimicking a hospital unit path
        urgencia_dir = root / "urgencia"
        urgencia_dir.mkdir()
        (urgencia_dir / "manual_urgencia_2026.pdf").write_bytes(b"%PDF-fake")

        yield root


@pytest.fixture
def output_dir():
    """Create a temporary output directory."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


class TestClassifyDocument:
    """Tests for classify_document()."""

    def test_classify_memorandum(self, temp_dir: Path):
        result = classify_document(temp_dir / "memorandum_001_2026.pdf")
        assert result.tipo_documento == "Memorandums"
        assert result.anio == "2026"
        assert result.extension == ".pdf"
        assert isinstance(result, ClasificacionDocumento)

    def test_classify_informe(self, temp_dir: Path):
        result = classify_document(temp_dir / "informe_gestion_urgencia_2025.docx")
        assert result.tipo_documento == "Informes"
        assert result.anio == "2025"

    def test_classify_protocolo(self, temp_dir: Path):
        result = classify_document(temp_dir / "protocolo_triage_2026.pdf")
        assert result.tipo_documento == "Protocolos"

    def test_classify_resolucion(self, temp_dir: Path):
        result = classify_document(temp_dir / "resolucion_rex_123_2026.pdf")
        assert result.tipo_documento == "Resoluciones"

    def test_classify_acta(self, temp_dir: Path):
        result = classify_document(temp_dir / "acta_comite_calidad_2026.docx")
        assert result.tipo_documento == "Actas"

    def test_classify_factura(self, temp_dir: Path):
        result = classify_document(temp_dir / "factura_proveedor_2026.pdf")
        assert result.tipo_documento == "Facturas"

    def test_classify_circular(self, temp_dir: Path):
        result = classify_document(temp_dir / "circular_005_2026.pdf")
        assert result.tipo_documento == "Circulares"

    def test_classify_unknown_defaults_to_varios(self, temp_dir: Path):
        result = classify_document(temp_dir / "documento_sin_tipo.pdf")
        assert result.tipo_documento == "Varios"

    def test_classify_detects_unidad_from_path(self, temp_dir: Path):
        result = classify_document(temp_dir / "urgencia" / "manual_urgencia_2026.pdf")
        assert result.unidad_hospitalaria == "Urgencia"

    def test_classify_default_unidad_is_general(self, temp_dir: Path):
        result = classify_document(temp_dir / "memorandum_001_2026.pdf")
        assert result.unidad_hospitalaria == "General"

    def test_classify_nonexistent_file_raises(self, temp_dir: Path):
        with pytest.raises(FileNotFoundError):
            classify_document(temp_dir / "no_existe.pdf")

    def test_ruta_destino_relativa(self, temp_dir: Path):
        result = classify_document(temp_dir / "protocolo_triage_2026.pdf")
        expected_parts = [result.unidad_hospitalaria, "2026", "Protocolos", "protocolo_triage_2026.pdf"]
        assert result.ruta_destino_relativa == Path(*expected_parts)

    def test_classify_planilla_xlsx(self, temp_dir: Path):
        result = classify_document(temp_dir / "planilla_dotacion.xlsx")
        assert result.tipo_documento == "Planillas"

    def test_confianza_alta_when_type_and_unit_detected(self, temp_dir: Path):
        result = classify_document(temp_dir / "urgencia" / "manual_urgencia_2026.pdf")
        assert result.confianza == "alta"

    def test_confianza_baja_for_unknown(self, temp_dir: Path):
        result = classify_document(temp_dir / "documento_sin_tipo.pdf")
        assert result.confianza == "baja"


class TestOrganizeDirectory:
    """Tests for organize_directory()."""

    def test_dry_run_does_not_move_files(self, temp_dir: Path, output_dir: Path):
        result = organize_directory(temp_dir, output_dir, dry_run=True)
        assert isinstance(result, ResultadoOrganizacion)
        assert result.archivos_procesados > 0
        assert result.archivos_movidos == 0
        assert len(result.clasificaciones) > 0

    def test_actual_run_moves_files(self, temp_dir: Path, output_dir: Path):
        result = organize_directory(temp_dir, output_dir, dry_run=False)
        assert result.archivos_movidos > 0
        # Check that files were actually created in the destination
        moved_files = list(output_dir.rglob("*"))
        assert len([f for f in moved_files if f.is_file()]) > 0

    def test_nonexistent_source_raises(self, output_dir: Path):
        with pytest.raises(FileNotFoundError):
            organize_directory(Path("/ruta/que/no/existe"), output_dir)

    def test_file_as_source_raises(self, temp_dir: Path, output_dir: Path):
        with pytest.raises(NotADirectoryError):
            organize_directory(temp_dir / "memorandum_001_2026.pdf", output_dir)

    def test_skips_non_matching_extensions(self, output_dir: Path):
        with tempfile.TemporaryDirectory() as tmpdir:
            src = Path(tmpdir)
            (src / "script.py").write_text("print('hello')")
            (src / "readme.md").write_text("# Readme")
            result = organize_directory(src, output_dir, dry_run=True)
            # .py and .md are not in default extensions
            assert result.archivos_procesados == 0

    def test_custom_extensions_filter(self, output_dir: Path):
        with tempfile.TemporaryDirectory() as tmpdir:
            src = Path(tmpdir)
            (src / "notas.txt").write_text("notas del dia")
            result = organize_directory(
                src, output_dir, dry_run=True,
                extensiones_incluidas={".txt"},
            )
            assert result.archivos_procesados == 1

    def test_resultado_counts(self, temp_dir: Path, output_dir: Path):
        result = organize_directory(temp_dir, output_dir, dry_run=True)
        total = result.archivos_procesados + result.archivos_omitidos
        # Total should be > 0
        assert total > 0
        assert result.errores == 0


class TestGenerateReport:
    """Tests for generate_report()."""

    def test_report_returns_dataframe_or_list(self, temp_dir: Path, output_dir: Path):
        result = organize_directory(temp_dir, output_dir, dry_run=True)
        report = generate_report(result)

        try:
            import pandas as pd
            assert isinstance(report, pd.DataFrame)
            assert len(report) > 0
            assert "tipo_documento" in report.columns
            assert "unidad_hospitalaria" in report.columns
            assert "confianza" in report.columns
        except ImportError:
            assert isinstance(report, list)
            assert len(report) > 0

    def test_report_empty_result(self, output_dir: Path):
        result = ResultadoOrganizacion(
            directorio_origen=output_dir,
            directorio_destino=output_dir,
        )
        report = generate_report(result)
        try:
            import pandas as pd
            assert isinstance(report, pd.DataFrame)
            assert len(report) == 0
        except ImportError:
            assert isinstance(report, list)
            assert len(report) == 0
