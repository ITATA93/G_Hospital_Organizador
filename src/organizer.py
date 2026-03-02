"""Organizador de archivos hospitalarios para SAIA.

Clasifica documentos administrativos del Hospital Provincial del Limari
por tipo (protocolos, manuales, normas, actas, informes) en una jerarquia
de carpetas estructurada por Unidad Hospitalaria / Ano / Tipo.

Utiliza pathlib para manejo de rutas y pandas para extraccion de metadatos
desde archivos CSV/Excel.

Uso:
    from src.organizer import classify_document, organize_directory, generate_report

    # Clasificar un documento individual
    resultado = classify_document(Path("Memorandum_123.pdf"))

    # Organizar un directorio completo
    resultados = organize_directory(Path("./entrada"), Path("./salida"))

    # Generar reporte de organizacion
    reporte_df = generate_report(resultados)
"""

from __future__ import annotations

import logging
import re
import shutil
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any

import yaml

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Configuracion de tipos de documentos hospitalarios
# ---------------------------------------------------------------------------

TIPOS_DOCUMENTO: dict[str, list[str]] = {
    "Protocolos": [
        r"protocolo",
        r"prot[\._-]",
        r"guia[\s_-]clinica",
        r"guia[\s_-]practica",
    ],
    "Manuales": [
        r"manual",
        r"instructivo",
        r"procedimiento",
    ],
    "Normas": [
        r"norma",
        r"normativa",
        r"reglamento",
        r"regulacion",
        r"decreto",
    ],
    "Actas": [
        r"acta",
        r"minuta",
        r"registro[\s_-]reunion",
    ],
    "Informes": [
        r"informe",
        r"reporte",
        r"analisis",
        r"evaluacion",
        r"diagnostico",
    ],
    "Memorandums": [
        r"memo",
        r"memorandum",
        r"memorando",
    ],
    "Ordinarios": [
        r"ord[\._\s]",
        r"ordinario",
        r"oficio",
    ],
    "Resoluciones": [
        r"res[\._\s]",
        r"resolucion",
        r"rex[\._\s]",
    ],
    "Circulares": [
        r"circular",
        r"comunicado",
    ],
    "Contratos": [
        r"contrato",
        r"convenio",
        r"honorario",
        r"licitacion",
    ],
    "Facturas": [
        r"factura",
        r"boleta",
        r"orden[\s_-]compra",
        r"cotizacion",
    ],
    "Planillas": [
        r"planilla",
        r"registro",
        r"inventario",
    ],
    "Presentaciones": [
        r"presentacion",
        r"capacitacion",
        r"charla",
    ],
}

# Mapeo de unidades hospitalarias basado en palabras clave en la ruta
UNIDADES_HOSPITALARIAS: dict[str, list[str]] = {
    "Urgencia": [r"urgencia", r"urg[\._-]", r"emergencia"],
    "Pabellon": [r"pabellon", r"quirofano", r"cirugia[\s_-]mayor"],
    "UCI": [r"uci", r"cuidados[\s_-]intensivos", r"uti"],
    "Medicina": [r"medicina", r"med[\._-]interna"],
    "Cirugia": [r"cirugia", r"cir[\._-]"],
    "Pediatria": [r"pediatria", r"ped[\._-]", r"neonatologia"],
    "Maternidad": [r"maternidad", r"obstetricia", r"ginecologia"],
    "Imagenologia": [r"imagenologia", r"radiologia", r"ecografia", r"ris", r"pacs"],
    "Laboratorio": [r"laboratorio", r"lab[\._-]", r"lis"],
    "Farmacia": [r"farmacia", r"farm[\._-]", r"medicamento"],
    "Direccion": [r"direccion", r"dir[\._-]", r"subdirecci"],
    "Calidad": [r"calidad", r"acreditacion", r"iaas", r"infecciones"],
    "RRHH": [r"rrhh", r"recursos[\s_-]humanos", r"personal", r"dotacion"],
    "Abastecimiento": [r"abastecimiento", r"bodega", r"compra", r"adquisicion"],
    "OIRS": [r"oirs", r"reclamo", r"solicitud[\s_-]ciudadana"],
    "Informatica": [r"informatica", r"tic", r"sistemas", r"his"],
}

EXTENSIONES_POR_TIPO: dict[str, str] = {
    ".xlsx": "Planillas",
    ".xls": "Planillas",
    ".csv": "Planillas",
    ".pptx": "Presentaciones",
    ".ppt": "Presentaciones",
}


# ---------------------------------------------------------------------------
# Dataclasses de resultado
# ---------------------------------------------------------------------------


@dataclass
class ClasificacionDocumento:
    """Resultado de la clasificacion de un documento individual."""

    ruta_original: Path
    tipo_documento: str
    unidad_hospitalaria: str
    anio: str
    nombre_archivo: str
    extension: str
    tamano_bytes: int
    fecha_modificacion: datetime
    confianza: str  # "alta", "media", "baja"
    metadatos_extra: dict[str, Any] = field(default_factory=dict)

    @property
    def ruta_destino_relativa(self) -> Path:
        """Genera la ruta de destino relativa: Unidad/Ano/TipoDocumento/archivo."""
        return Path(self.unidad_hospitalaria) / self.anio / self.tipo_documento / self.nombre_archivo


@dataclass
class ResultadoOrganizacion:
    """Resultado global de organizar un directorio."""

    directorio_origen: Path
    directorio_destino: Path
    archivos_procesados: int = 0
    archivos_movidos: int = 0
    archivos_omitidos: int = 0
    errores: int = 0
    clasificaciones: list[ClasificacionDocumento] = field(default_factory=list)
    lista_errores: list[dict[str, str]] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Funciones principales
# ---------------------------------------------------------------------------


def classify_document(
    file_path: Path,
    config_path: Path | None = None,
) -> ClasificacionDocumento:
    """Clasifica un documento individual segun su nombre y ruta.

    Analiza el nombre del archivo y la ruta completa para determinar:
    - Tipo de documento (protocolo, manual, norma, acta, informe, etc.)
    - Unidad hospitalaria de origen
    - Ano del documento

    Args:
        file_path: Ruta al archivo a clasificar.
        config_path: Ruta opcional a folder_structure.yaml para tipos custom.

    Returns:
        ClasificacionDocumento con toda la metadata extraida.
    """
    if not file_path.exists():
        raise FileNotFoundError(f"Archivo no encontrado: {file_path}")

    # Cargar configuracion custom si existe
    tipos = TIPOS_DOCUMENTO
    unidades = UNIDADES_HOSPITALARIAS
    if config_path and config_path.exists():
        custom = _cargar_config(config_path)
        if "tipos_documento" in custom:
            tipos = {**TIPOS_DOCUMENTO, **custom["tipos_documento"]}
        if "unidades" in custom:
            unidades = {**UNIDADES_HOSPITALARIAS, **custom["unidades"]}

    nombre = file_path.name
    nombre_lower = nombre.lower()
    ruta_str = str(file_path).lower()
    stat = file_path.stat()

    # 1. Detectar tipo de documento
    tipo, confianza_tipo = _detectar_tipo(nombre_lower, file_path.suffix.lower(), tipos)

    # 2. Detectar unidad hospitalaria
    unidad = _detectar_unidad(ruta_str, unidades)

    # 3. Extraer ano
    anio = _extraer_anio(nombre, file_path.parent.name, stat.st_mtime)

    # 4. Extraer metadatos adicionales de CSV/Excel si aplica
    metadatos_extra: dict[str, Any] = {}
    if file_path.suffix.lower() in (".csv", ".xlsx", ".xls"):
        metadatos_extra = _extraer_metadatos_tabular(file_path)

    # Determinar confianza global
    confianza = "alta" if confianza_tipo == "alta" and unidad != "General" else (
        "media" if confianza_tipo == "alta" or unidad != "General" else "baja"
    )

    return ClasificacionDocumento(
        ruta_original=file_path,
        tipo_documento=tipo,
        unidad_hospitalaria=unidad,
        anio=anio,
        nombre_archivo=nombre,
        extension=file_path.suffix,
        tamano_bytes=stat.st_size,
        fecha_modificacion=datetime.fromtimestamp(stat.st_mtime),
        confianza=confianza,
        metadatos_extra=metadatos_extra,
    )


def organize_directory(
    source_dir: Path,
    dest_dir: Path,
    *,
    dry_run: bool = True,
    config_path: Path | None = None,
    extensiones_incluidas: set[str] | None = None,
) -> ResultadoOrganizacion:
    """Organiza todos los archivos de un directorio segun la taxonomia SAIA.

    Recorre recursivamente source_dir, clasifica cada archivo y lo copia
    (o mueve, segun dry_run) a la estructura dest_dir/Unidad/Ano/Tipo/.

    Args:
        source_dir: Directorio de origen a organizar.
        dest_dir: Directorio raiz de destino (estructura SAIA).
        dry_run: Si True, solo clasifica sin mover archivos. Default True.
        config_path: Ruta a folder_structure.yaml para config custom.
        extensiones_incluidas: Set de extensiones a procesar (ej. {".pdf", ".docx"}).
            Si None, procesa todas las extensiones comunes.

    Returns:
        ResultadoOrganizacion con el detalle de la operacion.
    """
    if not source_dir.exists():
        raise FileNotFoundError(f"Directorio de origen no encontrado: {source_dir}")

    if not source_dir.is_dir():
        raise NotADirectoryError(f"La ruta no es un directorio: {source_dir}")

    extensiones_default = {
        ".pdf", ".docx", ".doc", ".xlsx", ".xls", ".csv",
        ".pptx", ".ppt", ".txt", ".odt", ".ods", ".odp",
        ".jpg", ".jpeg", ".png", ".tiff", ".bmp",
    }
    extensiones = extensiones_incluidas or extensiones_default

    resultado = ResultadoOrganizacion(
        directorio_origen=source_dir,
        directorio_destino=dest_dir,
    )

    for file_path in source_dir.rglob("*"):
        if not file_path.is_file():
            continue

        # Omitir archivos ocultos y directorios de sistema
        if any(part.startswith(".") for part in file_path.parts):
            continue
        if any(part.startswith("_") for part in file_path.relative_to(source_dir).parts):
            continue

        if file_path.suffix.lower() not in extensiones:
            resultado.archivos_omitidos += 1
            continue

        resultado.archivos_procesados += 1

        try:
            clasificacion = classify_document(file_path, config_path)
            resultado.clasificaciones.append(clasificacion)

            if not dry_run:
                ruta_final = dest_dir / clasificacion.ruta_destino_relativa
                ruta_final.parent.mkdir(parents=True, exist_ok=True)

                # Manejar colisiones de nombre
                ruta_final = _resolver_colision(ruta_final)

                shutil.copy2(file_path, ruta_final)
                resultado.archivos_movidos += 1
                logger.info(
                    "Archivo organizado: %s -> %s",
                    file_path.name,
                    ruta_final,
                )

        except Exception as e:
            resultado.errores += 1
            resultado.lista_errores.append({
                "archivo": str(file_path),
                "error": str(e),
            })
            logger.error("Error clasificando %s: %s", file_path, e)

    return resultado


def generate_report(resultado: ResultadoOrganizacion) -> Any:
    """Genera un reporte en formato pandas DataFrame de la organizacion.

    El reporte incluye:
    - Archivo original
    - Tipo de documento detectado
    - Unidad hospitalaria asignada
    - Ano extraido
    - Ruta destino propuesta
    - Nivel de confianza
    - Tamano del archivo

    Args:
        resultado: ResultadoOrganizacion obtenido de organize_directory().

    Returns:
        pandas.DataFrame con el reporte. Si pandas no esta disponible,
        retorna una lista de dicts.
    """
    registros = []
    for c in resultado.clasificaciones:
        registros.append({
            "archivo_original": str(c.ruta_original),
            "nombre": c.nombre_archivo,
            "tipo_documento": c.tipo_documento,
            "unidad_hospitalaria": c.unidad_hospitalaria,
            "anio": c.anio,
            "extension": c.extension,
            "tamano_kb": round(c.tamano_bytes / 1024, 1),
            "confianza": c.confianza,
            "ruta_destino": str(c.ruta_destino_relativa),
            "fecha_modificacion": c.fecha_modificacion.isoformat(),
        })

    try:
        import pandas as pd

        df = pd.DataFrame(registros)

        if not df.empty:
            # Agregar estadisticas de resumen
            resumen = {
                "total_archivos": resultado.archivos_procesados,
                "archivos_movidos": resultado.archivos_movidos,
                "archivos_omitidos": resultado.archivos_omitidos,
                "errores": resultado.errores,
                "por_tipo": df["tipo_documento"].value_counts().to_dict() if not df.empty else {},
                "por_unidad": df["unidad_hospitalaria"].value_counts().to_dict() if not df.empty else {},
                "por_confianza": df["confianza"].value_counts().to_dict() if not df.empty else {},
            }
            df.attrs["resumen"] = resumen

        return df

    except ImportError:
        logger.warning("pandas no disponible; retornando lista de dicts.")
        return registros


def generate_report_csv(resultado: ResultadoOrganizacion, output_path: Path) -> Path:
    """Genera el reporte y lo guarda como archivo CSV.

    Args:
        resultado: ResultadoOrganizacion obtenido de organize_directory().
        output_path: Ruta donde guardar el CSV.

    Returns:
        Path al archivo CSV generado.
    """
    reporte = generate_report(resultado)

    try:
        import pandas as pd

        if isinstance(reporte, pd.DataFrame):
            reporte.to_csv(output_path, index=False, encoding="utf-8-sig")
        else:
            # Fallback sin pandas
            _guardar_csv_manual(reporte, output_path)
    except ImportError:
        _guardar_csv_manual(reporte, output_path)

    logger.info("Reporte CSV generado: %s", output_path)
    return output_path


# ---------------------------------------------------------------------------
# Funciones internas
# ---------------------------------------------------------------------------


def _cargar_config(config_path: Path) -> dict[str, Any]:
    """Carga configuracion YAML personalizada."""
    try:
        with open(config_path, encoding="utf-8") as f:
            return yaml.safe_load(f) or {}
    except Exception as e:
        logger.warning("No se pudo cargar config %s: %s", config_path, e)
        return {}


def _detectar_tipo(nombre_lower: str, extension: str, tipos: dict[str, list[str]]) -> tuple[str, str]:
    """Detecta el tipo de documento basandose en el nombre y extension.

    Returns:
        Tupla (tipo, confianza) donde confianza es "alta" o "media".
    """
    # Primero verificar por extension directa
    if extension in EXTENSIONES_POR_TIPO:
        tipo_por_ext = EXTENSIONES_POR_TIPO[extension]
        # Pero si el nombre coincide con un tipo mas especifico, preferirlo
        for tipo, patrones in tipos.items():
            for patron in patrones:
                if re.search(patron, nombre_lower):
                    return tipo, "alta"
        return tipo_por_ext, "media"

    # Buscar por patrones en el nombre
    for tipo, patrones in tipos.items():
        for patron in patrones:
            if re.search(patron, nombre_lower):
                return tipo, "alta"

    return "Varios", "baja"


def _detectar_unidad(ruta_lower: str, unidades: dict[str, list[str]]) -> str:
    """Detecta la unidad hospitalaria a partir de la ruta completa."""
    for unidad, patrones in unidades.items():
        for patron in patrones:
            if re.search(patron, ruta_lower):
                return unidad
    return "General"


def _extraer_anio(nombre: str, nombre_carpeta: str, mtime: float) -> str:
    """Extrae el ano del documento desde el nombre, carpeta o fecha de modificacion."""
    # Pattern uses lookarounds instead of \b to handle underscores and dots
    # correctly (e.g., "informe_2025.pdf" or "2026_memo")
    year_pattern = r"(?<![0-9])(20[1-3][0-9])(?![0-9])"

    # 1. Buscar en nombre de archivo
    match = re.search(year_pattern, nombre)
    if match:
        return match.group(1)

    # 2. Buscar en nombre de carpeta padre
    match = re.search(year_pattern, nombre_carpeta)
    if match:
        return match.group(1)

    # 3. Fallback: fecha de modificacion
    if mtime:
        dt = datetime.fromtimestamp(mtime)
        if 2010 <= dt.year <= 2030:
            return str(dt.year)

    return "SinFecha"


def _extraer_metadatos_tabular(file_path: Path) -> dict[str, Any]:
    """Extrae metadatos basicos de archivos CSV/Excel usando pandas.

    Extrae: numero de filas, columnas, y nombres de columnas.
    """
    metadatos: dict[str, Any] = {}
    try:
        import pandas as pd

        ext = file_path.suffix.lower()
        if ext == ".csv":
            df = pd.read_csv(file_path, nrows=5, encoding="utf-8", on_bad_lines="skip")
        elif ext in (".xlsx", ".xls"):
            df = pd.read_excel(file_path, nrows=5)
        else:
            return metadatos

        metadatos["num_columnas"] = len(df.columns)
        metadatos["columnas"] = list(df.columns[:20])  # Limitar a 20 columnas
        metadatos["num_filas_estimadas"] = _contar_filas_rapido(file_path, ext)
        metadatos["formato"] = ext.replace(".", "").upper()

    except Exception as e:
        metadatos["error_lectura"] = str(e)
        logger.debug("No se pudieron extraer metadatos de %s: %s", file_path, e)

    return metadatos


def _contar_filas_rapido(file_path: Path, ext: str) -> int | str:
    """Cuenta filas de forma rapida sin cargar todo el archivo en memoria."""
    try:
        if ext == ".csv":
            count = 0
            with open(file_path, encoding="utf-8", errors="ignore") as f:
                for _ in f:
                    count += 1
            return max(0, count - 1)  # Restar header
        else:
            import pandas as pd
            # Para Excel, openpyxl puede dar el numero sin cargar todo
            df = pd.read_excel(file_path, nrows=0)
            return "desconocido"
    except Exception:
        return "desconocido"


def _resolver_colision(ruta: Path) -> Path:
    """Si el archivo destino ya existe, agrega un sufijo numerico."""
    if not ruta.exists():
        return ruta

    stem = ruta.stem
    suffix = ruta.suffix
    parent = ruta.parent
    contador = 1

    while ruta.exists():
        ruta = parent / f"{stem}_{contador}{suffix}"
        contador += 1

    return ruta


def _guardar_csv_manual(registros: list[dict], output_path: Path) -> None:
    """Guarda registros como CSV sin depender de pandas."""
    import csv

    if not registros:
        output_path.write_text("Sin datos\n", encoding="utf-8-sig")
        return

    with open(output_path, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=registros[0].keys())
        writer.writeheader()
        writer.writerows(registros)
