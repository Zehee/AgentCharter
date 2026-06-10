"""Redlines module — reads redline rules from CHARTER.md.

CHARTER.md format (§七、红线):
```
## 七、红线

> 以下为不可触碰的规则。脚本每次调用末尾自动输出此清单。

```
规则描述 — 具体内容 ！
另一条规则 — 具体内容 ！
```

> 用户可添加、删除、修改。保持每行以 `！` 结尾即可被脚本自动识别。
```

Script extracts text between `—` and `！`, joins with `！`.

Path resolution: scripts/lib/redlines.py → scripts/ → project root → collaboration/CHARTER.md
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


def read_redlines() -> list[str]:
    """Read redlines from CHARTER.md §七、红线.

    Returns list of rule descriptions extracted between `—` and `！`.
    """
    charter_path = COLLAB_DIR / "CHARTER.md"
    if not charter_path.exists():
        return ["未找到 CHARTER.md"]

    text = charter_path.read_text(encoding="utf-8", errors="ignore")
    lines = text.splitlines()

    in_section = False
    in_code_block = False
    redlines = []

    # Find ## 七、红线 section and its code block
    for line in lines:
        stripped = line.strip()

        if stripped.startswith("## ") and "红线" in stripped:
            in_section = True
            continue

        if in_section:
            if stripped.startswith("```"):
                in_code_block = not in_code_block
                continue

            if in_code_block and stripped:
                # Extract text between — and ！
                m = re.search(r"—\s*(.+?)\s*！", stripped)
                if m:
                    redlines.append(m.group(1).strip())

            # Exit section at next ## heading
            if not in_code_block and stripped.startswith("## "):
                break

    return redlines


def get_redlines_string() -> str:
    """Get redlines as a single string joined by ！."""
    rules = read_redlines()
    if not rules:
        return "无红线规则"
    return "！".join(rules)


def main():
    """CLI: python lib/redlines.py"""
    rules = read_redlines()
    print(json.dumps({
        "redlines": rules,
        "joined": get_redlines_string(),
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
