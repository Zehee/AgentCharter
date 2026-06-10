#!/usr/bin/env python3
"""new-review-report.py — 创建 REVIEW_REPORT（倒推法决定范式与路径）

范式推导（不依赖 ACTIONS.md）：
  1. 按 @reviewer 过滤 inbox/ → 是否有 REVIEW_TASK？
     ✅ 有 → 委派范式：写入 outbox/（给 TPM），编号来自 REVIEW_TASK
     ❌ 无 → 自循环范式：扫描 outbox/ 中 REPORT（按 @coder 或全部），写入 inbox/（给 coder）
"""

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import run_create_flow, no_args_response
from patrol import scan_inbox

SCRIPT_DIR = Path(__file__).resolve().parent
COLLAB_DIR = SCRIPT_DIR.parent


def _detect_reviewer_mode(agent_name: str) -> dict:
    """用倒推法检测审查范式，返回范式信息和可选编号列表。"""
    inbox_dir = COLLAB_DIR / "inbox"
    outbox_dir = COLLAB_DIR / "outbox"

    # 1. 先按 @agent_name 过滤 inbox/ 中的 REVIEW_TASK
    #    REVIEW_TASK_NNN_REVIEWER@AGENT.md — 例如 REVIEW_TASK_042_DSpro@KIMI.md
    review_task_pattern = re.compile(r"REVIEW_TASK_(\d{3})_.*@" + re.escape(agent_name) + r"\.md", re.IGNORECASE)

    found_tasks = []
    if inbox_dir.exists():
        for f in inbox_dir.iterdir():
            if f.is_file() and f.suffix == ".md":
                m = review_task_pattern.search(f.name)
                if m:
                    found_tasks.append({
                        "id": m.group(1),
                        "filename": f.name,
                        "source": "REVIEW_TASK",
                    })

    if found_tasks:
        # 委派范式：有 REVIEW_TASK → 写入 outbox/ 给 TPM
        return {
            "mode": "delegated",
            "hint": "从 inbox 中的 REVIEW_TASK 获取审查任务",
            "target_dir": "outbox",
            "recipient": "TPM",
            "available": found_tasks,
        }

    # 2. 无 REVIEW_TASK → 自循环范式
    #    扫描 outbox/ 中所有 REPORT（不按 @agent 过滤，因为 coder 写的不是 @reviewer）
    report_pattern = re.compile(r"REPORT_(\d{3})_\d{8}_.*@.*\.md")
    found_reports = []

    if outbox_dir.exists():
        for f in sorted(outbox_dir.iterdir(), reverse=True):  # 最新的在前
            if f.is_file() and f.suffix == ".md":
                m = report_pattern.search(f.name)
                if m:
                    nnn = m.group(1)
                    # 避免重复报告同一编号（取最新）
                    if not any(r["id"] == nnn for r in found_reports):
                        found_reports.append({
                            "id": nnn,
                            "filename": f.name,
                            "source": "REPORT",
                        })

    # 推断 coder（从 REPORT 文件名取 author）
    coder = "coder"
    if found_reports:
        # 从最新 REPORT 文件名提取 author（REPORT_NNN_DATE_AUTHOR@RECIPIENT.md）
        latest = found_reports[0]["filename"]
        m = re.match(r"REPORT_\d{3}_\d{8}_(.+)@.*\.md", latest)
        if m:
            coder = m.group(1).upper()

    if not found_reports:
        return {
            "mode": "self_loop",
            "hint": "无 REVIEW_TASK，且 outbox 中无 REPORT。无法推断审查对象，请显式提供 recipient 和 ref_nnn",
            "target_dir": "inbox",
            "recipient": None,
            "available": [],
        }
    return {
        "mode": "self_loop",
        "hint": "无 REVIEW_TASK，推定自循环。从 outbox 中 REPORT 获取审查对象",
        "target_dir": "inbox",
        "recipient": coder,
        "available": found_reports,
    }


def main():
    args = sys.argv[1:]
    agent = args[0].upper() if args else None

    if not agent:
        # 无参 → 模板 Schema
        result = no_args_response("REVIEW_REPORT")
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    # 检测范式，获得可选编号
    context = _detect_reviewer_mode(agent)
    data_str = args[1] if len(args) > 1 else None

    if not data_str:
        # 仅名字 → Schema + 上下文 + 可选编号
        result = no_args_response("REVIEW_REPORT", agent)
        result["paradigm"] = context["mode"]
        result["hint"] = context["hint"]
        result["target_dir"] = context["target_dir"]
        result["recipient"] = context["recipient"]
        result["available_references"] = context["available"]
        # 移除冗余的 fields 降低噪音
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    # 名字 + JSON → 创建文件
    try:
        data = json.loads(data_str)
    except json.JSONDecodeError as e:
        result = {"error": f"JSON 解析失败: {e}", "hint": "请传入合法的 JSON 字符串"}
        print(json.dumps(result, ensure_ascii=False, indent=2))
        sys.exit(1)

    data["author"] = data.get("author", agent)
    # 自循环下无法推断 recipient 时阻断
    if context["recipient"] is None and not data.get("recipient"):
        result = {"error": "无法推断 recipient：outbox 中无 REPORT，请显式提供 recipient"}
        print(json.dumps(result, ensure_ascii=False, indent=2))
        sys.exit(1)
    data["recipient"] = data.get("recipient", context["recipient"])

    # 让 _common.run_create_flow 写文件，target_dir 由我们指定
    result = run_create_flow("REVIEW_REPORT", agent, data)
    result["target_dir"] = context["target_dir"]
    result["paradigm"] = context["mode"]

    print(json.dumps(result, ensure_ascii=False, indent=2))
    if "error" in result:
        sys.exit(1)


if __name__ == "__main__":
    main()
