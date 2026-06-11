#!/usr/bin/env python3
"""daily-check.py — 全量巡检：检查 inbox/outbox/decisions 全部协作文件。

检查三项：
  1. 命名规范 — 文件名是否符合 `{TYPE}_{NNN}_{DATE}_{author}@recipient.md` 格式
  2. 流向校验 — 文件存放位置是否与 ACTIONS.md 定义的通道方向一致
     （例如 inbox/TASK 应来自 TPM → 执行者，outbox/REPORT 应来自执行者 → TPM）
  3. 模板内容 — 文件是否保留了未填充的 {{变量}} 标记（表明 Agent 遗漏了字段）

不依赖 @name 过滤，扫描全部。
"""

import json
import re
import sys
from pathlib import Path

# Fix Windows GBK encoding issue
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

SCRIPT_DIR = Path(__file__).resolve().parent
COLLAB_DIR = SCRIPT_DIR.parent
sys.path.insert(0, str(SCRIPT_DIR / "lib"))
from naming import classify  # noqa: E402


# ---------- 检查 1：命名规范 ----------

def check_naming(filepath: Path) -> dict:
    """检查文件名是否符合规范。"""
    from naming import validate_name
    is_valid, detected_type, error_msg = validate_name(filepath.name)
    return {
        "file": str(filepath.relative_to(COLLAB_DIR)),
        "type": detected_type,
        "valid": is_valid,
        "error": error_msg if not is_valid else None,
    }


# ---------- 检查 2：流向校验 ----------

def _check_notice_sender(filename: str) -> dict:
    """NOTICE 特殊校验：发起方必须是 TPM，接收方可以是 ALL 或已知 Agent。"""
    m = re.match(r"NOTICE_\d{3}_[A-Z0-9-]+_\d{8}_([A-Z]+)@([A-Z]+)\.md$", filename)
    if not m:
        return {"ok": False, "note": f"NOTICE 文件名无法解析 author/recipient: {filename}"}
    author, recipient = m.group(1), m.group(2)
    if author != "TPM":
        return {"ok": False, "note": f"❌ NOTICE 发起方必须是 TPM，当前: {author}"}
    if recipient == "ALL":
        return {"ok": True, "note": f"正确：NOTICE 广播给 ALL（发起方 TPM）"}
    try:
        from actions import validate_agent
        if validate_agent(recipient):
            return {"ok": True, "note": f"正确：NOTICE 发给 {recipient}（发起方 TPM）"}
    except Exception:
        pass
    return {"ok": False, "note": f"❌ NOTICE 接收方无效: {recipient}"}


# 硬编码的常用流向规则（备用，在 ACTIONS.md 读不到时使用）
FALLBACK_FLOWS = {
    "TASK": "inbox",
    "TASK_TEST": "inbox",
    "REPORT": "outbox",
    "REVISION": "inbox",
    "REVIEW_TASK": "inbox",
    "REVIEW_REPORT": "outbox",
    "PROACTIVE_REPORT": "outbox",
    "DECISION": "decisions",
    "NOTICE": "inbox",
    "REPLY": "inbox",
    "BLOCKING": "outbox",
    "BLOCKING_REPLY": "outbox",
    "TEST_REPORT": "outbox",
    "TODO": "todos",
    "LOG_ENTRY": "logs",
}

# REVIEW_REPORT 的特殊路径（两种范式）
REVIEW_FLOWS = ("inbox", "outbox")


def check_flow(filepath: Path, file_type: str) -> dict:
    """检查文件存放位置是否与类型要求的流向一致。"""
    parent_dir = filepath.parent.name  # inbox, outbox, decisions, 等
    expected = FALLBACK_FLOWS.get(file_type)

    if not expected:
        return {"flow_ok": None, "note": f"未知文件类型 {file_type}，跳过流向校验"}

    if file_type == "REVIEW_REPORT":
        # REVIEW_REPORT 可以放 inbox（自循环）或 outbox（委派）
        flow_ok = parent_dir in REVIEW_FLOWS
        note = f"REVIEW_REPORT 允许的目录: inbox/（自循环）或 outbox/（委派），当前: {parent_dir}/"
    elif parent_dir == expected:
        flow_ok = True
        note = f"正确：{file_type} 应在 {expected}/"
        if file_type == "NOTICE":
            notice_check = _check_notice_sender(filepath.name)
            if not notice_check["ok"]:
                flow_ok = False
            note = notice_check["note"]
    else:
        flow_ok = False
        note = f"❌ 可能不正确：{file_type} 应在 {expected}/，当前在 {parent_dir}/"
        # 尝试读 ACTIONS.md 做二次确认
        try:
            actions_path = COLLAB_DIR / "ACTIONS.md"
            if actions_path.exists():
                text = actions_path.read_text(encoding="utf-8", errors="ignore")
                for line in text.splitlines():
                    if file_type in line.upper() and parent_dir in line:
                        note = f"流向符合 ACTIONS.md 定义：{line.strip()}"
                        flow_ok = True
                        break
        except Exception:
            pass

    return {"flow_ok": flow_ok, "note": note}


# ---------- 检查 3：模板内容 ----------

def check_content(filepath: Path) -> dict:
    """检查文件中是否残留未填充的 {{变量}} 标记。"""
    try:
        text = filepath.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return {"unfilled_fields": [], "warn": "无法读取文件"}

    unfilled = re.findall(r'\{\{(\w+)\}\}', text)
    # 排除命名约束行中的 {{}}（模板头部说明不是填充字段）
    unfilled = [f for f in unfilled if f not in ("NNN", "DATE", "author", "recipient", "TYPE")]
    return {
        "unfilled_count": len(unfilled),
        "unfilled_fields": unfilled if unfilled else [],
        "warn": None if not unfilled else f"发现 {len(unfilled)} 个未填充的字段标记"
    }


# ---------- 主流程 ----------

def scan_directory(directory: Path) -> list:
    """扫描单个目录下的全部 .md 文件。"""
    results = []
    if not directory.exists():
        return results

    for f in sorted(directory.iterdir()):
        if not f.is_file() or f.suffix != ".md" or f.name == ".gitkeep":
            continue

        naming = check_naming(f)
        file_type = naming.get("type")
        flow = check_flow(f, file_type) if file_type and file_type != "UNKNOWN" else {}
        content = check_content(f)

        results.append({
            "file": naming["file"],
            "type": file_type or "UNKNOWN",
            "naming_valid": naming["valid"],
            "naming_error": naming.get("error"),
            **({"flow": flow.get("note")} if flow else {}),
            "unfilled_fields": content["unfilled_fields"],
        })

    return results


def main():
    args = sys.argv[1:]

    # 默认扫描目录
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
    stats = {"total": 0, "naming_ok": 0, "naming_errors": 0, "flow_issues": 0, "unfilled": 0}

    for d in dirs:
        if not d.exists():
            all_results.append({"directory": str(d), "error": "目录不存在"})
            continue

        files = scan_directory(d)
        all_results.append({"directory": str(d.relative_to(COLLAB_DIR)), "files": files})
        stats["total"] += len(files)
        for f in files:
            if f.get("naming_valid", True):
                stats["naming_ok"] += 1
            else:
                stats["naming_errors"] += 1
            flow = f.get("flow", "")
            if flow and flow.startswith("❌"):
                stats["flow_issues"] += 1

    # 汇总红线
    from redlines import get_redlines_string
    redlines = get_redlines_string()

    output = {
        "checked": [str(d.relative_to(COLLAB_DIR)) if d.exists() else str(d) for d in dirs],
        "summary": stats,
        "details": [r for r in all_results if "files" in r],
        "redlines": redlines,
    }

    print(json.dumps(output, ensure_ascii=False, indent=2))
    sys.exit(0 if stats["naming_errors"] == 0 else 1)


if __name__ == "__main__":
    main()
