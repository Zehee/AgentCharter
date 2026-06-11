#!/usr/bin/env python3
"""agent.py — 外部 Agent 入口。巡检只扫 @自己，可用命令为子集。

用法:
    python agent.py               → 框架信息
    python agent.py NAME          → 身份 + 巡检（@NAME 过滤）
    python agent.py NAME command  → 执行命令
"""

import json
import subprocess
import sys
from pathlib import Path

# Fix Windows GBK encoding issue
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR / "lib"))

from actions import validate_agent, get_role
from patrol import patrol
from redlines import get_redlines_string

# 外部 Agent 可用命令（TPM 独占的 new-task/new-revision/new-review-task 不在此列）
COMMANDS = [
    "new-report.py",
    "new-review-report.py",
    "new-decision.py",
    "new-blocking.py",
    "new-blocking-reply.py",
    "validate-file.py",
]


def show_framework_info():
    redlines = get_redlines_string()
    print(json.dumps({
        "framework": "AgentCharter",
        "entry": "agent.py — 外部 Agent 入口",
        "available_commands": COMMANDS,
        "usage": "python agent.py <你的名字>",
        "example": "python agent.py KIMI",
        "note": "协议层是基石，脚本层是增强。没有 Python？协议层本身运转完好。",
        "tpm_entry": "TPM 请使用 python tpm.py",
        "redlines": redlines,
    }, ensure_ascii=False, indent=2))


def show_agent_info(agent_name: str):
    agent = validate_agent(agent_name)
    if not agent:
        print(json.dumps({"error": f"无效的 Agent 名称: {agent_name}"}, ensure_ascii=False))
        sys.exit(1)

    role_info = get_role(agent_name)
    patrol_result = patrol(agent_name)  # 只扫 @agent_name
    redlines = get_redlines_string()

    pending = patrol_result.get("total_pending", 0)
    suggested = f"你有 {pending} 个待办任务。" if pending > 0 else "当前无待办任务。"

    print(json.dumps({
        "agent": agent_name,
        "role": role_info.get("role", "?"),
        "available_commands": COMMANDS,
        "patrol": patrol_result,
        "suggested": suggested,
        "redlines": redlines,
    }, ensure_ascii=False, indent=2))


def forward_command(agent_name: str, cmd: str, json_data: str = None):
    cmd_path = SCRIPT_DIR / cmd
    if not cmd_path.exists():
        print(json.dumps({"error": f"命令不存在: {cmd}"}, ensure_ascii=False))
        sys.exit(1)

    cmd_args = [sys.executable, str(cmd_path), agent_name]
    if json_data:
        cmd_args.append(json_data)

    result = subprocess.run(cmd_args, capture_output=True, text=True, timeout=30)
    print(result.stdout)
    if result.stderr:
        print(result.stderr, file=sys.stderr)

    # 外部 Agent 调 new-decision 时自动追加 PROACTIVE_REPORT
    if cmd in ("new-decision.py", "new-decision") and result.returncode == 0:
        _auto_proactive_report(agent_name, json_data)

    sys.exit(result.returncode)


def _auto_proactive_report(agent_name: str, decision_json: str = None):
    """外部 Agent 创建 DECISION 后自动追加 PROACTIVE_REPORT。"""
    pro_path = SCRIPT_DIR / "new-proactive-report.py"
    if not pro_path.exists():
        return

    pro_data = decision_json  # 复用 DECISION 的 JSON 数据
    pro_args = [sys.executable, str(pro_path), agent_name]
    if pro_data:
        pro_args.append(pro_data)

    try:
        pro_result = subprocess.run(pro_args, capture_output=True, text=True, timeout=30)
        if pro_result.returncode == 0:
            pro_output = json.loads(pro_result.stdout) if pro_result.stdout else {}
            print(json.dumps({
                "auto_proactive_report": "✅ PROACTIVE_REPORT 已自动创建（外部 Agent 决策需递交 TPM）",
                "proactive_report": pro_output.get("path", "?"),
            }, ensure_ascii=False, indent=2))
    except Exception:
        pass


def main():
    args = sys.argv[1:]

    if not args:
        show_framework_info()
        return

    agent_name = args[0].upper()

    if len(args) == 1:
        show_agent_info(agent_name)
        return

    cmd = args[1]
    json_data = args[2] if len(args) > 2 else None

    cmd_map = {name.replace(".py", ""): name for name in COMMANDS}
    script = cmd_map.get(cmd, cmd if cmd.endswith(".py") else f"{cmd}.py")
    forward_command(agent_name, script, json_data)


if __name__ == "__main__":
    main()
