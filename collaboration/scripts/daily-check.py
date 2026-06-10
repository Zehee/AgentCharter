#!/usr/bin/env python3
"""daily-check.py — 全量巡检：扫描 inbox/outbox/decisions 全部文件，检查命名+内容+交叉引用。

用法:
    python daily-check.py                   → 扫描全部
    python daily-check.py inbox/            → 只扫 inbox
    python daily-check.py inbox/ outbox/    → 扫指定目录
"""

import json
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_DIR = SCRIPT_DIR.parent
COLLAB_DIR = PROJECT_DIR / "collaboration"

sys.path.insert(0, str(SCRIPT_DIR / "lib"))

from validate import validate_all, validate_file  # noqa: E402
from redlines import get_redlines_string  # noqa: E402


def main():
    args = sys.argv[1:]

    if not args:
        # Default: scan inbox + outbox + decisions
        dirs = [
            COLLAB_DIR / "inbox",
            COLLAB_DIR / "outbox",
            COLLAB_DIR / "decisions",
        ]
    else:
        dirs = []
        for d in args:
            p = Path(d)
            if not p.is_absolute():
                p = COLLAB_DIR / p
            dirs.append(p)

    all_results = []
    total_passed = 0
    total_failed = 0

    for d in dirs:
        if not d.exists():
            all_results.append({
                "directory": str(d),
                "error": "目录不存在",
            })
            total_failed += 1
            continue

        result = validate_all(str(d))
        all_results.append(result)

        if "summary" in result:
            total_passed += result["summary"].get("passed", 0)
            total_failed += result["summary"].get("failed", 0)

    redlines = get_redlines_string()

    output = {
        "checked_directories": [str(d) for d in dirs],
        "summary": {
            "total": total_passed + total_failed,
            "passed": total_passed,
            "failed": total_failed,
        },
        "details": all_results,
        "redlines": redlines,
    }

    print(json.dumps(output, ensure_ascii=False, indent=2))
    sys.exit(0 if total_failed == 0 else 1)


if __name__ == "__main__":
    main()
