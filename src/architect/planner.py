import re
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

import yaml

from src.audit.vault import AuditVault


class StructureArchitect:
    def __init__(self, vault: AuditVault):
        self.vault = vault
        # Heuristics for Document Type
        self.doc_types = {
            "Memorandums": [r"memo", r"memorandum"],
            "Ordinarios": [r"ord\.", r"ordinario", r"oficio"],
            "Resoluciones": [r"res\.", r"resolucion", r"decreto", r"rex"],
            "Informes": [r"informe", r"reporte", r"analisis", r"evaluacion"],
            "Planillas_Excel": [r"\.xlsx$", r"\.xls$", r"\.csv$"],
            "Presentaciones": [r"\.pptx$", r"\.ppt$", r"presentacion"],
            "Contratos_RRHH": [r"contrato", r"honorario", r"cv", r"curriculum"],
            "Compras_Finanzas": [r"factura", r"boleta", r"compra", r"cotizacion"],
            "Protocolos_Manuales": [r"protocolo", r"manual", r"guia", r"norma"],
            "Cartas_Solicitudes": [r"carta", r"solicitud", r"peticion"],
        }

    def generate_proposal(self) -> Dict[str, Any]:
        """Query the Vault and generate a migration plan."""
        proposal = {
            "plan_id": f"SAIA-{datetime.now().strftime('%Y%m%d-%H%M')}",
            "created_at": datetime.now().isoformat(),
            "summary": {
                "total_files": 0,
                "moves_proposed": 0,
                "clusters_detected": 0,
                "warnings": [],
            },
            "actions": [],
        }

        conn = sqlite3.connect(self.vault.db_path)
        cursor = conn.cursor()

        # 0. Detect Software Clusters (Cohesion)
        clusters = self._identify_clusters(cursor)
        proposal["summary"]["clusters_detected"] = len(clusters)

        # 1. Fetch active files (including last_modified)
        cursor.execute(
            "SELECT file_path, file_hash, first_seen_at, last_modified FROM inventory WHERE status='active'"
        )
        rows = cursor.fetchall()

        proposal["summary"]["total_files"] = len(rows)

        for row in rows:
            path_str, fhash, seen, mtime = row
            path = Path(path_str)

            # Skip Audit folder and other hidden system files
            if "_Audit" in path.parts or any(p.startswith(".") for p in path.parts):
                continue

            # Check if file belongs to a Cluster
            cluster_root = self._get_cluster_root(path, clusters)

            # Construct Destination Root
            try:
                anchor_idx = path.parts.index("_UGCO_Disco G_PC_Jefatura")
                drive_root = Path(*path.parts[: anchor_idx + 1])
                dest_root = drive_root / "_Estructura_Final_SAIA"
            except ValueError:
                dest_root = path.parent.parent / "_Estructura_Final_SAIA"

            if cluster_root:
                # STRATEGY: Move the entire cluster to 01_Software
                # We normalize the relative path from the cluster root
                rel_path = path.relative_to(cluster_root.parent)
                dest_path = dest_root / "01_Software_Detectado" / rel_path
                reason = f"Cluster: {cluster_root.name}"
            else:
                # STRATEGY: Administrative Organization
                year = self._extract_year(path, mtime) or "SinFecha"
                doc_type = self._extract_doc_type(path.name)

                # Heuristic: Personal
                if "personal" in str(path).lower() or doc_type == "Contratos_RRHH":
                    category = "_Personal"
                else:
                    category = "02_Administrativo_Central"

                dest_path = dest_root / category / doc_type / year / path.name
                reason = f"Heuristic: Type={doc_type}, Year={year}"

            # Add Move Action if source != dest
            if str(path.resolve()).lower() != str(dest_path.resolve()).lower():
                # Avoid moving if it's already in the structure (idempotency)
                if "_Estructura_Final_SAIA" in str(path):
                    continue

                proposal["actions"].append(
                    {
                        "move": {
                            "src": str(path),
                            "dest": str(dest_path),
                            "reason": reason,
                        }
                    }
                )
                proposal["summary"]["moves_proposed"] += 1

        conn.close()
        return proposal

    def _identify_clusters(self, cursor: sqlite3.Cursor) -> List[Path]:
        """Find directories that contain software-like files."""
        software_indicators = [
            ".exe",
            ".msi",
            ".dll",
            ".bin",
            ".py",
            ".js",
            ".git",
            ".jar",
        ]

        # SQL to find folders with these extensions
        placeholders = ",".join(["?"] * len(software_indicators))
        query = f"""
            SELECT file_path FROM inventory 
            WHERE status='active' 
            AND (
                {" OR ".join([f"file_path LIKE '%{ext}'" for ext in software_indicators])}
            )
        """
        # Note: SQLite LIKE is case-insensitive by default in some builds, but better assume explicit if needed.
        # Actually checking extension in python might be safer/easier if parsing paths.

        cursor.execute("SELECT file_path FROM inventory WHERE status='active'")
        rows = cursor.fetchall()

        cluster_candidates = set()

        for (p_str,) in rows:
            p = Path(p_str)
            if p.suffix.lower() in software_indicators:
                # The PARENT folder is a candidate for a cluster
                cluster_candidates.add(p.parent)

        # TODO: Refine logic to merge nested clusters (if parent and child are clusters, take parent)
        # For Phase 2, flat list of parents containing exe is a good start.
        return list(cluster_candidates)

    def _get_cluster_root(self, file_path: Path, clusters: List[Path]) -> Any:
        # Check if file_path is inside any cluster folder
        for cluster in clusters:
            try:
                file_path.relative_to(cluster)
                return cluster
            except ValueError:
                continue
        return None

    def _extract_year(self, path: Path, mtime: float = None) -> str:
        # 1. Try filename
        match = re.search(r"\b(20[1-2][0-9])\b", path.name)
        if match:
            return match.group(1)
        # 2. Try parent folder
        match_parent = re.search(r"\b(20[1-2][0-9])\b", path.parent.name)
        if match_parent:
            return match_parent.group(1)

        # 3. Fallback: Use file modification time
        if mtime:
            dt = datetime.fromtimestamp(mtime)
            if 2010 <= dt.year <= 2030:
                return str(dt.year)

        return None

    def _extract_doc_type(self, filename: str) -> str:
        name = filename.lower()
        for dtype, patterns in self.doc_types.items():
            for p in patterns:
                if re.search(p, name):
                    return dtype
        return "Varios"

    def save_proposal(
        self, proposal: Dict[str, Any], output_path: str = "migration_proposal.yaml"
    ):
        with open(output_path, "w", encoding="utf-8") as f:
            yaml.dump(proposal, f, default_flow_style=False, sort_keys=False)
        print(f"Proposal saved to {output_path}")
