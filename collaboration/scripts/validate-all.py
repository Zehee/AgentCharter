#!/usr/bin/env python3
"""validate-all.py — 校验全部协作文件。

用法:
    python validate-all.py                  → 校验收件箱、发件箱、决策
    python validate-all.py inbox/ outbox/   → 校验指定目录
"""

import json
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_DIR = SCRIPT_DIR.parent          # collaboration/
COLLAB_DIR = PROJECT_DIR                 # scripts/ 在 collaboration/ 内

sys.path.insert(0, str(SCRIPT_DIR / "lib"))

from validate import validate_all  # noqa: E402
from redlines import get_redlines_string  # noqa: E402


def main():
    args = sys.argv[1:]

    if not args:
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

    output = {
        "summary": {
            "total": total_passed + total_failed,
            "passed": total_passed,
            "failed": total_failed,
        },
        "details": all_results,
        "redlines": get_redlines_string(),
    }

    print(json.dumps(output, ensure_ascii=False, indent=2))
    sys.exit(0 if total_failed == 0 else 1)


if __name__ == "__main__":
    main()
