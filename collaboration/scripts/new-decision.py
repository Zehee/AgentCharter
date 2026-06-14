#!/usr/bin/env python3
"""new-decision.py — 创建 DECISION（body 模式）

外部 Agent 创建 DECISION 后自动追加 PROACTIVE_REPORT 递交 TPM。
TPM 调用时只生成 DECISION。

用法:
    python new-decision.py NAME < body.md
    python new-decision.py NAME --body body.md
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import charterTool, get_role
from redlines import get_redlines_string


def _read_body(args: list[str]) -> tuple[str | None, str]:
    """解析 --body，返回 (ref, body)。DECISION 自增，不需要 ref。"""
    body_file = None
    i = 1
    while i < len(args):
        if args[i] == "--body" and i + 1 < len(args):
            body_file = args[i + 1]
            i += 2
        else:
            i += 1

    if body_file and body_file != "-":
        body = Path(body_file).read_text(encoding="utf-8")
    else:
        # Windows 下 stdin 默认编码可能为 GBK，强制按 UTF-8 读取
        body = sys.stdin.buffer.read().decode("utf-8")

    return None, body


if __name__ == "__main__":
    args = sys.argv[1:]
    agent = args[0].upper() if args else None

    if not agent:
        result = {"error": "缺少 Agent 名称"}
        print(json.dumps(result, ensure_ascii=False, indent=2))
        sys.exit(1)

    for a in args[1:]:
        if a.startswith("{"):
            print(json.dumps({
                "error": "JSON 传入方案已废除。",
                "hint": "请使用 body 模式：cat decision.md | python new-decision.py NAME，或调用 charterTool('NAME', 'DECISION', body='...')",
                "redlines": get_redlines_string(),
            }, ensure_ascii=False, indent=2))
            sys.exit(1)

    _, body = _read_body(args)
    if not body.strip():
        result = {"error": "body 为空", "hint": "请通过 stdin 或 --body 传入 markdown 正文"}
        print(json.dumps(result, ensure_ascii=False, indent=2))
        sys.exit(1)

    # 创建 DECISION
    result = charterTool(agent, "DECISION", body=body)
    print(json.dumps(result, ensure_ascii=False, indent=2))

    # 外部 Agent 创建 DECISION 后自动追加 PROACTIVE_REPORT
    role = get_role(agent)
    if "error" not in result and role and role.get("role") != "TPM":
        decision_path = result.get("path", "")
        pro_body = f"""# PROACTIVE_REPORT: 决策递交

<!-- DESC: DECISION-HANDOFF -->

**提交人**: {agent}
**日期**: {__import__('datetime').date.today().strftime('%Y%m%d')}
**关联决策**: {Path(decision_path).name if decision_path else 'DECISION_NNN'}

## 范围与目标

> 将外部 Agent 记录的决策递交 TPM 审阅与决策。

## 发现

> 见 {decision_path or '关联 DECISION 文件'}。

## 建议

> 请 TPM 审阅该决策并转化为 TASK/TODO 或归档。
"""
        pro_result = charterTool(agent, "PROACTIVE_REPORT", body=pro_body)
        print(json.dumps({
            "auto_proactive_report": "✅ 已自动创建 PROACTIVE_REPORT",
            "proactive_report": pro_result,
            "redlines": get_redlines_string(),
        }, ensure_ascii=False, indent=2))

    if "error" in result:
        sys.exit(1)
