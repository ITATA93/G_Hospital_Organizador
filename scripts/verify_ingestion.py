import os
import sys
from pathlib import Path

# Add project root to path
sys.path.append(os.getcwd())

from src.config import get_settings


def verify_access():
    settings = get_settings()
    data_dir = Path(settings.data_dir)

    print(f"Checking access to: {data_dir}")

    if not data_dir.exists():
        print("[ERROR] Data directory not found!")
        return

    print("[OK] Directory exists.")

    # Count files by year
    years = sorted([d.name for d in data_dir.iterdir() if d.is_dir()])
    print(f"Found {len(years)} year folders: {years}")

    total_files = 0
    for year in years:
        year_path = data_dir / year
        count = sum(1 for _ in year_path.rglob("*") if _.is_file())
        total_files += count
        if count > 0:
            print(f"  - {year}: {count} documents")

    print(
        f"\n[SUCCESS] Application config is correctly pointing to {total_files} organized administrative documents."
    )


if __name__ == "__main__":
    verify_access()
