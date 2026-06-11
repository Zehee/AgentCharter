#!/usr/bin/env python3
"""new-decision.py — 创建 DECISION。

角色分流逻辑已移除至入口层（agent.py / tpm.py）。
外部 Agent 入口（agent.py）自动追加 PROACTIVE_REPORT。
TPM 入口（tpm.py）只生成 DECISION。

本脚本始终只创建 DECISION 文件。
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import run_and_exit

if __name__ == "__main__":
    args = sys.argv[1:]
    agent = args[0].upper() if args else None
    data = args[1] if len(args) > 1 else None
    run_and_exit("DECISION", agent, data)
