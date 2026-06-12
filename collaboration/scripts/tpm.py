#!/usr/bin/env python3
"""tpm.py — TPM 入口。巡检全览 + @TPM 过滤，包含 TPM 专属命令。

用法:
    python tpm.py                     → TPM 工具集信息
    python tpm.py TPM                 → 全览巡检 + @TPM 任务
    python tpm.py TPM command ...     → 执行 TPM 命令
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

from actions import validate_agent, is_tpm
from patrol import scan_inbox, tpm_overview
from redlines import get_redlines_string

# TPM 可用命令（外部 Agent 子集 + TPM 独占命令）
COMMANDS = [
    # TPM 独占
    "new-task.py",
    "new-review-task.py",
    "new-revision.py",
    "new-notice.py",
    "new-reply.py",
    "new-blocking.py",
    "new-blocking-reply.py",
    "archive.py",
    "daily-check.py",
    "validate-all.py",
    # 共享
    "new-decision.py",
    "new-report.py",
    "new-review-report.py",
    "validate-file.py",
]


def show_framework_info():
    redlines = get_redlines_string()
    print(json.dumps({
        "entry": "tpm.py — TPM 入口",
        "available_commands": COMMANDS,
        "usage": "python tpm.py TPM",
        "note": "TPM 使用此入口。外部 Agent 请用 agent.py。",
        "redlines": redlines,
    }, ensure_ascii=False, indent=2))


def show_overview(agent_name: str):
    """全览巡检：总览 + @TPM 过滤 + 命令清单。"""
    result = tpm_overview(agent_name, available_commands=COMMANDS)
    if "error" in result:
        print(json.dumps(result, ensure_ascii=False))
        sys.exit(1)
    print(json.dumps(result, ensure_ascii=False, indent=2))


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
    sys.exit(result.returncode)


def main():
    args = sys.argv[1:]

    if not args:
        show_framework_info()
        return

    agent_name = args[0].upper()

    if len(args) == 1:
        show_overview(agent_name)
        return

    cmd = args[1]
    json_data = args[2] if len(args) > 2 else None

    cmd_map = {name.replace(".py", ""): name for name in COMMANDS}
    script = cmd_map.get(cmd, cmd if cmd.endswith(".py") else f"{cmd}.py")
    forward_command(agent_name, script, json_data)


if __name__ == "__main__":
    main()
