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
COLLAB_DIR = SCRIPTS_DIR.parent

# 只有以下类型支持自动编号（未传 NNN 时自动生成）
# REVIEW_TASK/REPORT/REVISION 等派生类型不自增，NNN 必须来自关联任务
AUTO_NNN_TYPES = {"TASK", "TASK_TEST", "DECISION"}


def get_next_nnn(file_type: str, inbox_dir: str | None = None) -> int:
    """Scan directories for existing files and return max NNN + 1.

    For most file types: scans both the active dir and its archive counterpart.
    E.g. TASK → inbox/ + archive/inbox/; REPORT → outbox/ + archive/outbox/

    Args:
        file_type: e.g. "TASK", "REPORT", "REVISION"
        inbox_dir: optional override, defaults based on file type

    Returns:
        int: next available sequence number
    """
    # 文件类型 → (默认活跃目录, 是否同时扫描归档目录)
    # TASK 需要扫归档（编号唯一，不能冲突）
    # REPORT/REVISION/DECISION 等不扫归档（编号来源是关联的 TASK，非独立编号）
    type_dir_map = {
        "TASK": ("inbox", True),         # 编号唯一，必须扫描归档去重
        "TASK_TEST": ("inbox", True),
        "DECISION": ("decisions", True), # 编号独立自增，扫描归档去重
        # 以下类型不自增编号，NNN 来自关联的任务（REVIEW_TASK=关联TASK、REPORT=关联TASK 等）
        "REPORT": ("outbox", False),
        "REVISION": ("inbox", False),
        "REVIEW_REPORT": ("outbox", False),
        "REVIEW_TASK": ("inbox", False),
        "PROACTIVE_REPORT": ("outbox", False),
        "NOTICE": ("inbox", False),
        "REPLY": ("inbox", False),
        "BLOCKING": ("outbox", False),
        "BLOCKING_REPLY": ("outbox", False),
        "TEST_REPORT": ("outbox", False),
        "TODO": ("todos", False),
    }

    # 只有以下类型支持自动编号（未传 NNN 时自动生成）
    # REVIEW_TASK/REPORT/REVISION 等派生类型不自增，NNN 必须来自关联任务

    default_dir, scan_archive = type_dir_map.get(file_type, ("inbox", False))
    dirs_to_scan = []

    if inbox_dir:
        dirs_to_scan.append(inbox_dir)
    else:
        dirs_to_scan.append(str(COLLAB_DIR / default_dir))

    if scan_archive:
        archive_dir = COLLAB_DIR / "archive" / default_dir
        if archive_dir.exists():
            dirs_to_scan.append(str(archive_dir))

    max_nnn = 0
    pattern = re.compile(rf"{re.escape(file_type)}_(\d{{3}})", re.IGNORECASE)

    for d in dirs_to_scan:
        target = Path(d)
        if not target.exists():
            continue
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
