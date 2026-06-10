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

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR / "lib"))

from actions import validate_agent, is_tpm
from patrol import scan_inbox
from redlines import get_redlines_string

# TPM 可用命令（外部 Agent 子集 + TPM 独占命令）
COMMANDS = [
    # TPM 独占
    "new-task.py",
    "new-revision.py",
    "daily-check.py",
    "validate-all.py",
    # 共享
    "new-decision.py",
    "new-report.py",
    "new-review-report.py",
    "new-blocking.py",
    "new-blocking-reply.py",
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
    agent = validate_agent(agent_name)
    if not agent:
        print(json.dumps({"error": f"无效的 TPM 名称: {agent_name}"}, ensure_ascii=False))
        sys.exit(1)

    if not is_tpm(agent_name):
        print(json.dumps({"error": f"{agent_name} 不是 TPM", "hint": "外部 Agent 请使用 agent.py"}, ensure_ascii=False))
        sys.exit(1)

    redlines = get_redlines_string()
    inbox_dir = SCRIPT_DIR.parent / "inbox"
    outbox_dir = SCRIPT_DIR.parent / "outbox"
    decisions_dir = SCRIPT_DIR.parent / "decisions"

    def count_files(d):
        return len([f for f in d.iterdir() if f.suffix == ".md" and f.name != ".gitkeep"]) if d.exists() else 0

    # 全览
    total_inbox = count_files(inbox_dir)
    total_outbox = count_files(outbox_dir)
    total_decisions = count_files(decisions_dir)

    # @TPM 过滤
    tpm_tasks = scan_inbox(agent_name) if inbox_dir.exists() else []

    print(json.dumps({
        "agent": agent_name,
        "role": "TPM",
        "overview": {
            "inbox_total": total_inbox,
            "outbox_total": total_outbox,
            "decisions_total": total_decisions,
        },
        "my_tasks_in_inbox": tpm_tasks,
        "available_commands": COMMANDS,
        "suggested": f"inbox 中有 {total_inbox} 个文件，其中 {len(tpm_tasks)} 个分配给 TPM。"
                     f"outbox 中有 {total_outbox} 个报告待审阅。运行 daily-check.py 做全量校验。",
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
