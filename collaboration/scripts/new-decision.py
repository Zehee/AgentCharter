#!/usr/bin/env python3
"""new-decision.py — 创建 DECISION（TPM）/ DECISION + PROACTIVE_REPORT（外部 Agent）"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent / "lib"))

from actions import is_tpm  # noqa: E402
from redlines import get_redlines_string  # noqa: E402
from _common import run_create_flow, no_args_response  # noqa: E402


def main():
    args = sys.argv[1:]

    if not args:
        result = no_args_response("DECISION")
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    agent_name = args[0].upper()

    if len(args) == 1:
        result = no_args_response("DECISION", agent_name)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    try:
        data = json.loads(args[1])
    except json.JSONDecodeError as e:
        print(json.dumps({"error": f"JSON 解析错误: {e}"}, ensure_ascii=False))
        sys.exit(1)

    data["author"] = data.get("author", agent_name)

    if is_tpm(agent_name):
        # TPM → 只写 DECISION
        data["recipient"] = data.get("recipient", "ARCHIVE")
        result = run_create_flow("DECISION", agent_name, data)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        # 外部 Agent → DECISION + PROACTIVE_REPORT
        data["recipient"] = data.get("recipient", "ARCHIVE")
        result_dec = run_create_flow("DECISION", agent_name, data)
        print(json.dumps({
            "step": "DECISION",
            "result": result_dec,
        }, ensure_ascii=False, indent=2))

        # 创建 PROACTIVE_REPORT
        pro_data = {
            "author": agent_name,
            "recipient": "TPM",
            "DESC": data.get("DESC", f"FROM-DECISION-{data.get('NNN', '')}"),
            "NNN": data.get("NNN", ""),
            "DATE": data.get("DATE", ""),
        }
        result_pro = run_create_flow("PROACTIVE_REPORT", agent_name, pro_data)
        redlines = get_redlines_string()
        print(json.dumps({
            "step": "PROACTIVE_REPORT",
            "result": result_pro,
            "redlines": redlines,
        }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
