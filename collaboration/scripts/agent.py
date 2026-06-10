#!/usr/bin/env python3
"""agent.py — ★ 总入口。Agent 只需记住这一个脚本。

用法:
    python agent.py               → 项目框架信息
    python agent.py KIMI          → 角色、链路、命令、巡检
    python agent.py KIMI new-report '{"key":"val"}'  → 执行命令（透传）
"""

import json
import subprocess
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR / "lib"))

from actions import validate_agent, get_role  # noqa: E402
from patrol import patrol  # noqa: E402
from redlines import get_redlines_string  # noqa: E402


COMMANDS = [
    "new-task.py", "new-report.py", "new-revision.py",
    "new-decision.py", "new-review-report.py",
    "validate-file.py", "validate-all.py",
    "daily-check.py",
]


def show_framework_info():
    """Show project framework info (no-args mode)."""
    redlines = get_redlines_string()
    print(json.dumps({
        "framework": "AgentCharter",
        "scripts_dir": str(SCRIPT_DIR),
        "available_commands": COMMANDS,
        "usage": "python agent.py <你的名字>",
        "example": "python agent.py KIMI",
        "note": "协议层是基石，脚本层是增强。没有 Python？目录结构、命名规范、链路表照常运转。",
        "redlines": redlines,
    }, ensure_ascii=False, indent=2))


def show_agent_info(agent_name: str):
    """Show agent info + patrol results."""
    # Validate agent
    agent = validate_agent(agent_name)
    if not agent:
        print(json.dumps({
            "error": f"无效的 Agent 名称: {agent_name}",
            "note": "请检查 ACTIONS.md 中注册的角色名称",
        }, ensure_ascii=False, indent=2))
        sys.exit(1)

    role_info = get_role(agent_name)
    patrol_result = patrol(agent_name)
    redlines = get_redlines_string()

    # Build suggested action
    pending = patrol_result.get("total_pending", 0)
    if pending > 0:
        suggested = f"你有 {pending} 个未完成任务。执行 new-report.py {agent_name} 提交完成报告。"
    else:
        suggested = f"当前无待办任务。执行 new-task.py TPM '...' 分配新任务。"

    print(json.dumps({
        "agent": agent_name,
        "role": role_info.get("role", "?"),
        "links": role_info.get("allowed_commands", []),
        "available_commands": COMMANDS,
        "patrol": patrol_result,
        "suggested": suggested,
        "redlines": redlines,
    }, ensure_ascii=False, indent=2))


def forward_command(agent_name: str, cmd: str, json_data: str = None):
    """Forward to a specific command script with given args."""
    cmd_path = SCRIPT_DIR / cmd
    if not cmd_path.exists():
        print(json.dumps({"error": f"命令不存在: {cmd}"}, ensure_ascii=False))
        sys.exit(1)

    cmd_args = [sys.executable, str(cmd_path), agent_name]
    if json_data:
        cmd_args.append(json_data)

    result = subprocess.run(cmd_args, capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print(result.stderr, file=sys.stderr)
    sys.exit(result.returncode)


def main():
    args = sys.argv[1:]

    if not args:
        show_framework_info()
        return

    agent_name = args[0].upper()

    if len(args) == 1:
        show_agent_info(agent_name)
        return

    # agent.py NAME COMMAND [JSON]
    cmd = args[1]
    json_data = args[2] if len(args) > 2 else None

    # Map short names to script files
    cmd_map = {
        name.replace(".py", ""): name
        for name in COMMANDS
    }

    if cmd in cmd_map:
        forward_command(agent_name, cmd_map[cmd], json_data)
    else:
        # Try as-is
        forward_command(agent_name, cmd if cmd.endswith(".py") else f"{cmd}.py", json_data)


if __name__ == "__main__":
    main()
