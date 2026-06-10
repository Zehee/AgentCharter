"""
template.py — Parse AgentCharter Markdown templates.

Scans a template file for ``{{variable}}`` placeholders and extracts:
  - field definitions (key, label, required)
  - target directory (from ``> **存放位置**: ``)
  - name pattern (from ``> **文件名**: ``)

Usage:
    python lib/template.py PATH   → print JSON dict with fields, target_dir, name_pattern
"""

import json
import re
import sys

# ── known variable → Chinese label mappings ──────────────────────────────
_KNOWN_LABELS = {
    "NNN": "序号",
    "DATE": "日期",
    "author": "作者标识",
    "recipient": "接收者标识",
    "AUTHOR": "作者标识",
    "DESC": "简短描述",
    "assignee": "执行人标识",
    "TASK_NNN": "关联任务编号",
    "REVISION_NNN": "关联修订编号",
    "REVIEW_REPORT_NNN": "关联审查报告编号",
    "BLOCKING_NNN": "关联阻塞编号",
    "PROACTIVE_REPORT_NNN": "关联主动报告编号",
    "DECISION_NNN": "关联决策编号",
    "TODO_NNN": "关联待办编号",
    "summary": "摘要",
    "TITLE": "标题",
    "标题": "标题",
    "DESCRIPTION": "描述",
    "SOURCE": "来源",
    "target_dir": "存放位置",
    "name_pattern": "文件名模式",
}


def _infer_label(var_name: str) -> str:
    """Return a human-readable label for *var_name*."""
    name = var_name.strip()
    if name in _KNOWN_LABELS:
        return _KNOWN_LABELS[name]
    # Fallback: underscores → spaces, then title-case
    return name.replace("_", " ").title()


def parse_template(path: str) -> dict:
    """Parse a template file and return ``{fields, target_dir, name_pattern}``.

    *fields* is a list of dicts::

        {"key": "VAR_NAME", "label": "…", "required": true|false}
    """
    with open(path, encoding="utf-8") as fh:
        text = fh.read()

    # ── extract header metadata ───────────────────────────────────────────
    target_dir = ""
    name_pattern = ""

    for line in text.splitlines():
        stripped = line.strip()
        # > **存放位置**: `value`
        m = re.match(r'>\s*\*\*存放位置\*\*:\s*`([^`]*)`', stripped)
        if m:
            target_dir = m.group(1).strip()
        # > **文件名**: `value`
        m = re.match(r'>\s*\*\*文件名\*\*:\s*`([^`]*)`', stripped)
        if m:
            name_pattern = m.group(1).strip()

    # ── extract {{…}} placeholders ───────────────────────────────────────
    seen: dict[str, dict] = {}  # var_name → field dict

    # Track which section we are in for optional detection
    lines = text.splitlines()
    in_optional_section = False

    for i, line in enumerate(lines):
        stripped = line.strip()

        # Detect optional sections (Chinese/English markers)
        if re.search(r'（可选）|\(optional\)|##\s+待确认|##\s+Pending', stripped, re.IGNORECASE):
            in_optional_section = True
        elif stripped.startswith("## ") and not re.search(r'（可选）|\(optional\)', stripped):
            # A new non-optional heading resets the flag (unless the heading itself is optional)
            in_optional_section = False

        for match in re.finditer(r'\{\{(\w+)\}\}', stripped):
            var_name = match.group(1)
            if var_name not in seen:
                label = _infer_label(var_name)
                seen[var_name] = {
                    "key": var_name,
                    "label": label,
                    "required": not in_optional_section,
                }
            else:
                # If it was previously optional but now appears in a required section → upgrade
                if seen[var_name]["required"] is False and not in_optional_section:
                    seen[var_name]["required"] = True

    # Variables that appear in the name-pattern are always required
    for match in re.finditer(r'\{\{(\w+)\}\}', name_pattern):
        var_name = match.group(1)
        if var_name in seen:
            seen[var_name]["required"] = True

    fields = list(seen.values())
    # Stable sort: required fields first, then alphabetical by key
    fields.sort(key=lambda f: (not f["required"], f["key"]))

    return {
        "fields": fields,
        "target_dir": target_dir,
        "name_pattern": name_pattern,
    }


def main():
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"):
        print("Usage: python lib/template.py PATH", file=sys.stderr)
        sys.exit(1)

    path = sys.argv[1]
    result = parse_template(path)
    json.dump(result, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
