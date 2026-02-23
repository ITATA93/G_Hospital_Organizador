import hashlib
import json
import os
import shutil
from datetime import datetime
from pathlib import Path
from typing import Any, Dict

import structlog
import yaml

from src.audit.vault import AuditVault

logger = structlog.get_logger()


class MigrationEngine:
    def __init__(self, vault: AuditVault, dry_run: bool = False):
        self.vault = vault
        self.dry_run = dry_run

    def execute_plan(self, plan_path: Path):
        with open(plan_path, "r", encoding="utf-8") as f:
            plan = yaml.safe_load(f)

        plan_id = plan.get("plan_id", "Unknown")
        print(f"Executing Plan: {plan_id}")
        actions = plan.get("actions", [])

        transaction_log = []
        success_count = 0
        fail_count = 0

        for action in actions:
            if "move" in action:
                if self._handle_move(action["move"], transaction_log):
                    success_count += 1
                else:
                    fail_count += 1

        # Save Transaction Log for Undo
        if not self.dry_run:
            self.vault.log_operation(
                "EXECUTE",
                {
                    "plan_id": plan_id,
                    "ops_attempted": len(actions),
                    "success": success_count,
                    "fail": fail_count,
                },
            )

            # Also save to file for manual inspection
            log_path = self.vault.logs_dir / f"execution_{plan_id}.json"
            with open(log_path, "w", encoding="utf-8") as f:
                json.dump(transaction_log, f, indent=2)
            print(f"Execution Log saved to {log_path}")

    def _handle_move(self, move_action: Dict, log: list) -> bool:
        src = Path(move_action["src"])
        dest = Path(move_action["dest"])

        if not src.exists():
            logger.warning("source_missing", path=str(src))
            return False

        if self.dry_run:
            print(f"[DRY-RUN] Move {src.name} -> {dest}")
            return True

        try:
            # 1. Prepare Destination
            dest.parent.mkdir(parents=True, exist_ok=True)

            # 2. Safe Copy
            shutil.copy2(src, dest)

            # 3. VERIFY INTEGRITY (Vital)
            src_hash = self._get_file_hash(src)
            dest_hash = self._get_file_hash(dest)

            if src_hash != dest_hash:
                logger.error("integrity_check_failed", src=str(src), dest=str(dest))
                # Rollback copy
                os.remove(dest)
                return False

            # 4. Delete Source (Atomic Move completed)
            os.remove(src)

            # 5. Update Audit Vault
            self._update_vault(src, dest, src_hash)

            log.append(
                {
                    "op": "move",
                    "src": str(src),
                    "dest": str(dest),
                    "hash": src_hash,
                    "timestamp": datetime.now().isoformat(),
                }
            )
            print(f"[OK] {src.name} -> {dest.parent.name}")
            return True

        except Exception as e:
            logger.error("move_failed", src=str(src), error=str(e))
            # Attempt cleanup of dest if it exists/half-written
            if dest.exists():
                try:
                    os.remove(dest)
                except:
                    pass
            return False

    def _get_file_hash(self, path: Path) -> str:
        sha256 = hashlib.sha256()
        with open(path, "rb") as f:
            while chunk := f.read(8192):
                sha256.update(chunk)
        return sha256.hexdigest()

    def _update_vault(self, src: Path, dest: Path, fhash: str):
        conn = None
        try:
            conn = self.vault._connect()  # Assuming accessible or use sqlite3 directly
        except:
            import sqlite3

            conn = sqlite3.connect(self.vault.db_path)

        cursor = conn.cursor()
        now = datetime.now().isoformat()

        # Mark Old as Moved
        cursor.execute(
            "UPDATE inventory SET status='moved', last_scanned_at=? WHERE file_path=?",
            (now, str(src)),
        )

        # Insert New
        # Get metadata from stored? or just simple insert?
        # Ideally we copy metadata from the old row.
        # For speed/simplicity here:
        stat = dest.stat()
        cursor.execute(
            """
            INSERT INTO inventory (file_path, file_hash, size_bytes, last_modified, first_seen_at, last_scanned_at, status)
            VALUES (?, ?, ?, ?, ?, ?, 'active')
            """,
            (str(dest), fhash, stat.st_size, stat.st_mtime, now, now),
        )

        conn.commit()
        conn.close()

    def rollback(self, transaction_id: str):
        print("Rollback feature coming in v2.1")
