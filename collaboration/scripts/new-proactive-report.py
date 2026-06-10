#!/usr/bin/env python3
"""new-proactive-report.py — 创建 PROACTIVE_REPORT"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import run_and_exit

if __name__ == "__main__":
    args = sys.argv[1:]
    agent = args[0].upper() if args else None
    data = args[1] if len(args) > 1 else None
    run_and_exit("PROACTIVE_REPORT", agent, data)
