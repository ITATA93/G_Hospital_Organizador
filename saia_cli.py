import argparse
import os
import sys
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

# Ensure project root is in path
sys.path.append(os.getcwd())

from src.audit.vault import AuditVault
from src.config import get_settings
from src.scanners.inventory import InventoryScanner


def main():
    parser = argparse.ArgumentParser(description="SAIA - Hospital Archiver CLI")
    parser.add_argument(
        "action",
        choices=["scan", "enrich", "plan", "execute"],
        help="Action to perform",
    )
    parser.add_argument(
        "--target", help="Target directory to scan (Overrides config)", default=None
    )
    parser.add_argument(
        "--limit", type=int, help="Limit number of files to process", default=None
    )

    args = parser.parse_args()

    settings = get_settings()
    # Default to data_dir from config if not specified
    target_dir = args.target if args.target else settings.data_dir
    project_root = os.getcwd()

    print(f"Initializing SAIA Vault in {project_root}")
    vault = AuditVault(project_root)

    if args.action == "scan":
        if not target_dir:
            print(
                "Error: No target directory. Set DATA_DIR in .env or provide --target"
            )
            return

        # HARDENING: Validate target path relative to execution or explicit override
        safe_path = Path(target_dir).resolve()
        if not safe_path.exists():
             logger.error(f"Target directory does not exist: {safe_path}")
             return
        
        logger.info(f"Scanning target: {safe_path}")
        scanner = InventoryScanner(str(safe_path), vault)
        scanner.scan()

    elif args.action == "enrich":
        import sqlite3

        from src.scanners.content import ContentAnalyzer

        print("Enriching metadata (OCR/Regex)...")
        analyzer = ContentAnalyzer()
        conn = sqlite3.connect(vault.db_path)
        cursor = conn.cursor()

        # Select files that haven't been enriched yet (simplified for now as just all active)
        # In v2, add 'last_enriched' column
        cursor.execute("SELECT id, file_path FROM inventory WHERE status='active'")
        rows = cursor.fetchall()

        count = 0
        limit = args.limit if args.limit else 999999

        for row in rows:
            if count >= limit:
                break

            fid, fpath = row
            try:
                meta = analyzer.analyze_file(Path(fpath))
                if meta["doc_type"] != "Unknown" or meta["extracted_date"]:
                    print(
                        f"[{meta['doc_type']}] {Path(fpath).name} -> {meta['extracted_date']}"
                    )
                    # Store in DB (TODO: Add metadata table)
            except Exception as e:
                logger.error(f"Failed to process {fpath}: {str(e)}")
            count += 1

    elif args.action == "plan":
        from src.architect.planner import StructureArchitect

        print("Designing folder structure...")
        architect = StructureArchitect(vault)
        proposal = architect.generate_proposal()
        architect.save_proposal(proposal)

    elif args.action == "execute":
        if not args.target:  # Use target as plan file here
            print("Error: Provide plan file with --target")
            return

        from src.engine.executor import MigrationEngine

        print(f"Executing migration plan from {args.target}...")
        engine = MigrationEngine(
            vault, dry_run=False
        )  # Add --dry-run arg support later
        engine.execute_plan(args.target)


if __name__ == "__main__":
    main()
