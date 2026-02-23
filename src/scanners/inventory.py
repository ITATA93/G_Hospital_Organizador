import hashlib
import os
from pathlib import Path

import structlog

from src.audit.vault import AuditVault

logger = structlog.get_logger()


class InventoryScanner:
    def __init__(self, root_dir: str, vault: AuditVault):
        self.root_dir = Path(root_dir)
        self.vault = vault
        self.chunk_size = 8192

    def calculate_hash(self, file_path: Path) -> str:
        sha256 = hashlib.sha256()
        try:
            with open(file_path, "rb") as f:
                while chunk := f.read(self.chunk_size):
                    sha256.update(chunk)
            return sha256.hexdigest()
        except OSError as e:
            logger.error("read_error", file=str(file_path), error=str(e))
            return "ERROR_READING_FILE"

    def scan(self):
        """Walk the directory and register every file."""
        print(f"Scanning {self.root_dir}...")
        count = 0

        for root, _, files in os.walk(self.root_dir):
            # Skip the Audit folder itself
            if "_Audit" in root:
                continue

            for file in files:
                file_path = Path(root) / file
                try:
                    stats = file_path.stat()
                    file_hash = self.calculate_hash(file_path)

                    self.vault.register_file(
                        path=str(file_path),
                        file_hash=file_hash,
                        size=stats.st_size,
                        mtime=stats.st_mtime,
                    )
                    count += 1
                    if count % 100 == 0:
                        print(f"Scanned {count} files...", end="\r")
                except Exception as e:
                    logger.error("scan_error", file=str(file_path), error=str(e))

        self.vault.log_operation(
            "SCAN", {"root": str(self.root_dir), "files_scanned": count}
        )
        print(f"\nScan complete. Processed {count} files.")
