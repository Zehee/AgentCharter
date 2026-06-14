#!/usr/bin/env python3
"""new-proactive-report.py — 创建 PROACTIVE_REPORT（body 模式）

用法:
    python new-proactive-report.py NAME < body.md
    python new-proactive-report.py NAME --body body.md
    python new-proactive-report.py NAME --ref NNN --body body.md
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import run_body_and_exit, get_redlines_string
import json

if __name__ == "__main__":
    args = sys.argv[1:]
    agent = args[0].upper() if args else None
    ref = None
    body_file = None
    i = 1
    while i < len(args):
        if args[i].startswith("{"):
            print(json.dumps({
                "error": "JSON 传入方案已废除。",
                "hint": f"请使用 body 模式：cat body.md | python new-proactive-report.py NAME --ref NNN，或调用 charterTool('NAME', 'PROACTIVE_REPORT', body='...', ref='...')",
                "redlines": get_redlines_string(),
            }, ensure_ascii=False, indent=2))
            sys.exit(1)
        if args[i] == "--ref" and i + 1 < len(args):
            ref = args[i + 1]
            i += 2
        elif args[i] == "--body" and i + 1 < len(args):
            body_file = args[i + 1]
            i += 2
        else:
            i += 1
    run_body_and_exit("PROACTIVE_REPORT", agent, ref=ref, body_file=body_file)
