#!/usr/bin/env python3
"""validate-file.py — 校验单个协作文件。

用法:
    python validate-file.py collaboration/inbox/TASK_042_ADD-LOGIN_KIMI@TPM.md
"""

import json
import sys
from pathlib import Path

# Fix Windows GBK encoding issue
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR / "lib"))

from validate import validate_file  # noqa: E402
from redlines import get_redlines_string  # noqa: E402


def main():
    args = sys.argv[1:]

    if not args:
        print(json.dumps({
            "usage": "python validate-file.py <filepath>",
            "example": "python validate-file.py collaboration/inbox/TASK_042_ADD-LOGIN_KIMI@TPM.md",
        }, ensure_ascii=False, indent=2))
        sys.exit(1)

    filepath = Path(args[0])
    if not filepath.exists():
        print(json.dumps({
            "error": f"文件不存在: {filepath}",
            "redlines": get_redlines_string(),
        }, ensure_ascii=False, indent=2))
        sys.exit(1)

    result = validate_file(str(filepath))
    result["redlines"] = get_redlines_string()

    print(json.dumps(result, ensure_ascii=False, indent=2))
    has_error = (
        not result.get("name_valid", True)
        or result.get("missing_headers", [])
        or result.get("missing_refs", [])
    )
    sys.exit(1 if has_error else 0)


if __name__ == "__main__":
    main()
