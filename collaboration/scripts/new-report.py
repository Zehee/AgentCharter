#!/usr/bin/env python3
"""new-report.py — 创建 REPORT"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import run_create_flow, no_args_response


def main():
    args = sys.argv[1:]

    if not args:
        result = no_args_response("REPORT")
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    agent_name = args[0].upper()

    if len(args) == 1:
        result = no_args_response("REPORT", agent_name)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    try:
        data = json.loads(args[1])
    except json.JSONDecodeError as e:
        print(json.dumps({"error": f"JSON 解析错误: {e}"}, ensure_ascii=False))
        sys.exit(1)

    data["author"] = data.get("author", agent_name)
    data["recipient"] = data.get("recipient", "TPM")

    result = run_create_flow("REPORT", agent_name, data)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if "error" in result:
        sys.exit(1)


if __name__ == "__main__":
    main()
