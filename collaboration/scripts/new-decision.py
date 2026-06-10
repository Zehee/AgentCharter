#!/usr/bin/env python3
"""new-decision.py — 创建 DECISION（TPM）/ DECISION + PROACTIVE_REPORT（外部 Agent）"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent / "lib"))

from actions import is_tpm
from _common import run_and_exit, run_create_flow, no_args_response


def main():
    args = sys.argv[1:]
    agent = args[0].upper() if args else None
    data_str = args[1] if len(args) > 1 else None

    if not agent:
        # No args: template schema
        result = no_args_response("DECISION")
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    if not data_str:
        # Name only: schema + patrol
        result = no_args_response("DECISION", agent)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    try:
        data = json.loads(data_str)
    except json.JSONDecodeError as e:
        result = {"error": f"JSON 解析失败: {e}"}
        print(json.dumps(result, ensure_ascii=False, indent=2))
        sys.exit(1)

    data["author"] = data.get("author", agent)

    if is_tpm(agent):
        # TPM → 只写 DECISION
        data["recipient"] = data.get("recipient", "ARCHIVE")
        result = run_create_flow("DECISION", agent, data)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        if "error" in result:
            sys.exit(1)
    else:
        # 外部 Agent → DECISION + PROACTIVE_REPORT
        data["recipient"] = data.get("recipient", "ARCHIVE")
        result_dec = run_create_flow("DECISION", agent, data)
        print(json.dumps({"step": "DECISION", "result": result_dec}, ensure_ascii=False, indent=2))

        pro_data = {
            "author": agent,
            "recipient": "TPM",
            "DESC": data.get("DESC", f"FROM-DECISION-{data.get('NNN', '')}"),
            "NNN": data.get("NNN", ""),
            "DATE": data.get("DATE", ""),
        }
        result_pro = run_create_flow("PROACTIVE_REPORT", agent, pro_data)
        from _common import get_redlines_string
        redlines = get_redlines_string()
        print(json.dumps({"step": "PROACTIVE_REPORT", "result": result_pro, "redlines": redlines}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
