"""NNN sequence registry — tracks and allocates file sequence numbers.

All path resolution is relative from scripts/ to collaboration/.
Pure Python stdlib, zero deps.
"""

import json
import os
import re
import sys
from pathlib import Path


SCRIPTS_DIR = Path(__file__).resolve().parent.parent
PROJECT_DIR = SCRIPTS_DIR.parent
COLLAB_DIR = PROJECT_DIR / "collaboration"


def get_next_nnn(file_type: str, inbox_dir: str | None = None) -> int:
    """Scan directory for existing files of the given type and return max NNN + 1.

    Args:
        file_type: e.g. "TASK", "REPORT", "REVISION"
        inbox_dir: optional override, defaults to collaboration/inbox/

    Returns:
        int: next available sequence number (1-based, zero-padded to 3 digits)
    """
    if inbox_dir is None:
        inbox_dir = str(COLLAB_DIR / "inbox")

    target = Path(inbox_dir)
    if not target.exists():
        return 1

    max_nnn = 0
    pattern = re.compile(rf"{re.escape(file_type)}_(\d{{3}})", re.IGNORECASE)

    for f in target.iterdir():
        if f.is_file() and f.suffix == ".md":
            m = pattern.search(f.name)
            if m:
                n = int(m.group(1))
                if n > max_nnn:
                    max_nnn = n

    return max_nnn + 1


def format_nnn(n: int) -> str:
    """Format an integer as a zero-padded 3-digit string."""
    return f"{n:03d}"


def main():
    """CLI: python lib/registry.py TASK [inbox_path]"""
    if len(sys.argv) < 2:
        print(json.dumps({"error": "Usage: python lib/registry.py FILE_TYPE [inbox_path]"}, ensure_ascii=False))
        sys.exit(1)

    file_type = sys.argv[1].upper()
    inbox_dir = sys.argv[2] if len(sys.argv) > 2 else None
    next_n = get_next_nnn(file_type, inbox_dir)

    print(json.dumps({
        "file_type": file_type,
        "next_nnn": next_n,
        "formatted": format_nnn(next_n),
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
