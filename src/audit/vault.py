import json
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional


class AuditVault:
    def __init__(self, project_root: str):
        self.root = Path(project_root)
        self.audit_dir = self.root / "_Audit"
        self.db_path = self.audit_dir / "audit.db"
        self._setup()

    def _setup(self):
        """Initialize the hidden audit directory and database."""
        if not self.audit_dir.exists():
            self.audit_dir.mkdir(parents=True)
            # On Windows, setting hidden attribute could be added here if strictly needed

        self.logs_dir = self.audit_dir / "logs"
        if not self.logs_dir.exists():
            self.logs_dir.mkdir()

        self._init_db()

    def _init_db(self):
        """Create database schema if not exists."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Table: Files Inventory
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS inventory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                file_path TEXT UNIQUE NOT NULL,
                file_hash TEXT NOT NULL,
                size_bytes INTEGER,
                last_modified REAL,
                first_seen_at TEXT,
                last_scanned_at TEXT,
                status TEXT DEFAULT 'active' -- active, moved, deleted
            )
        """)

        # Table: Operations Log (Reflexive Audit)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS operations_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                operation_type TEXT, -- SCAN, PROPOSE, MOVE, ROLLBACK
                details TEXT, -- JSON blob
                user_approved BOOLEAN DEFAULT 0
            )
        """)

        conn.commit()
        conn.close()

    def register_file(self, path: str, file_hash: str, size: int, mtime: float):
        """Upsert a file record into inventory."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        now = datetime.now().isoformat()

        try:
            # Check if exists
            cursor.execute(
                "SELECT id, file_hash FROM inventory WHERE file_path = ?", (path,)
            )
            row = cursor.fetchone()

            if row:
                # Update
                if row[1] != file_hash:
                    # Content changed?
                    pass
                cursor.execute(
                    """
                    UPDATE inventory 
                    SET file_hash=?, size_bytes=?, last_modified=?, last_scanned_at=?, status='active'
                    WHERE file_path=?
                """,
                    (file_hash, size, mtime, now, path),
                )
            else:
                # Insert
                cursor.execute(
                    """
                    INSERT INTO inventory (file_path, file_hash, size_bytes, last_modified, first_seen_at, last_scanned_at, status)
                    VALUES (?, ?, ?, ?, ?, ?, 'active')
                """,
                    (path, file_hash, size, mtime, now, now),
                )

            conn.commit()
        except Exception as e:
            print(f"[Vault Error] Failed to register {path}: {e}")
        finally:
            conn.close()

    def log_operation(
        self, op_type: str, details: Dict[str, Any], approved: bool = False
    ):
        """Log a systemic operation."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO operations_log (timestamp, operation_type, details, user_approved)
            VALUES (?, ?, ?, ?)
        """,
            (datetime.now().isoformat(), op_type, json.dumps(details), approved),
        )
        conn.commit()
        conn.close()

    def get_duplicate_hashes(self) -> List[str]:
        """Find file hashes that appear more than once."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT file_hash, COUNT(*) as c 
            FROM inventory 
            WHERE status='active' 
            GROUP BY file_hash 
            HAVING c > 1
        """)
        dupes = [row[0] for row in cursor.fetchall()]
        conn.close()
        return dupes
