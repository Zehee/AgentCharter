#!/usr/bin/env python3
"""new-review-report.py — 创建 REVIEW_REPORT（body 模式）

范式推导（不依赖 ACTIONS.md）：
  1. 按 @reviewer 过滤 inbox/ → 是否有 REVIEW_TASK？
     ✅ 有 → 委派范式：写入 outbox/（给 TPM），编号来自 REVIEW_TASK
     ❌ 无 → 自循环范式：扫描 outbox/ 中 REPORT，写入 inbox/（给 coder）

用法:
    python new-review-report.py NAME < body.md
    python new-review-report.py NAME --body body.md
    python new-review-report.py NAME --ref NNN --body body.md
"""

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import charterTool, no_args_response
from patrol import scan_inbox

SCRIPT_DIR = Path(__file__).resolve().parent
COLLAB_DIR = SCRIPT_DIR.parent


def _detect_reviewer_mode(agent_name: str) -> dict:
    """用倒推法检测审查范式，返回范式信息和可选编号列表。"""
    inbox_dir = COLLAB_DIR / "inbox"
    outbox_dir = COLLAB_DIR / "outbox"

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
        return {
            "mode": "delegated",
            "hint": "从 inbox 中的 REVIEW_TASK 获取审查任务",
            "target_dir": "outbox",
            "recipient": "TPM",
            "available": found_tasks,
        }

    report_pattern = re.compile(r"REPORT_(\d{3})_\d{8}_.*@.*\.md")
    found_reports = []

    if outbox_dir.exists():
        for f in sorted(outbox_dir.iterdir(), reverse=True):
            if f.is_file() and f.suffix == ".md":
                m = report_pattern.search(f.name)
                if m:
                    nnn = m.group(1)
                    if not any(r["id"] == nnn for r in found_reports):
                        found_reports.append({
                            "id": nnn,
                            "filename": f.name,
                            "source": "REPORT",
                        })

    coder = "coder"
    if found_reports:
        latest = found_reports[0]["filename"]
        m = re.match(r"REPORT_\d{3}_\d{8}_(.+)@.*\.md", latest)
        if m:
            coder = m.group(1).upper()

    if not found_reports:
        return {
            "mode": "self_loop",
            "hint": "无 REVIEW_TASK，且 outbox 中无 REPORT。无法推断审查对象，请显式提供 --ref 和 body 中的 recipient",
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


def _read_body(args: list[str]) -> tuple[str | None, str | None]:
    """解析 --ref 和 --body，返回 (ref, body)。"""
    ref = None
    body_file = None
    i = 1
    while i < len(args):
        if args[i] == "--ref" and i + 1 < len(args):
            ref = args[i + 1]
            i += 2
        elif args[i] == "--body" and i + 1 < len(args):
            body_file = args[i + 1]
            i += 2
        else:
            i += 1

    if body_file and body_file != "-":
        body = Path(body_file).read_text(encoding="utf-8")
    else:
        # Windows 下 stdin 默认编码可能为 GBK，强制按 UTF-8 读取
        body = sys.stdin.buffer.read().decode("utf-8")

    return ref, body


def main():
    args = sys.argv[1:]
    agent = args[0].upper() if args else None

    if not agent:
        result = no_args_response("REVIEW_REPORT")
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    for a in args[1:]:
        if a.startswith("{"):
            print(json.dumps({
                "error": "JSON 传入方案已废除。",
                "hint": "请使用 body 模式：cat body.md | python new-review-report.py NAME --ref NNN，或调用 charterTool('NAME', 'REVIEW_REPORT', body='...', ref='...')",
                "redlines": get_redlines_string(),
            }, ensure_ascii=False, indent=2))
            sys.exit(1)

    context = _detect_reviewer_mode(agent)

    if len(args) < 2:
        result = no_args_response("REVIEW_REPORT", agent)
        result["paradigm"] = context["mode"]
        result["hint"] = context["hint"]
        result["target_dir"] = context["target_dir"]
        result["recipient"] = context["recipient"]
        result["available_references"] = context["available"]
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    ref, body = _read_body(args)
    if not body.strip():
        result = {"error": "body 为空", "hint": "请通过 stdin 或 --body 传入 markdown 正文"}
        print(json.dumps(result, ensure_ascii=False, indent=2))
        sys.exit(1)

    # 委派范式下 ref 必须来自 REVIEW_TASK；自循环下来自 REPORT
    if ref is None:
        if context["available"]:
            ref = context["available"][0]["id"]
        else:
            result = {"error": "无法推断 ref：请提供 --ref NNN"}
            print(json.dumps(result, ensure_ascii=False, indent=2))
            sys.exit(1)

    # 若 body 未指定 recipient，在自循环模式下注入推断的 recipient
    if context["recipient"] and "**recipient**" not in body.lower() and not re.search(r"<!--\s*RECIPIENT:", body, re.IGNORECASE):
        # 在 body 顶部注入 recipient 元信息
        body = f"<!-- RECIPIENT: {context['recipient']} -->\n\n" + body

    result = charterTool(agent, "REVIEW_REPORT", body=body, ref=ref)
    result["target_dir"] = context["target_dir"]
    result["paradigm"] = context["mode"]
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if "error" in result:
        sys.exit(1)


if __name__ == "__main__":
    main()
