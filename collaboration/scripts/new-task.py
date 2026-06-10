#!/usr/bin/env python3
"""new-task.py — 创建 TASK（自动编号）"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import run_create_flow, no_args_response


def main():
    args = sys.argv[1:]

    if not args:
        # No args: output template schema
        result = no_args_response("TASK")
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    agent_name = args[0].upper()

    if len(args) == 1:
        # Name only: output schema + patrol
        result = no_args_response("TASK", agent_name)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    # Name + JSON: create file
    try:
        data = json.loads(args[1])
    except json.JSONDecodeError as e:
        print(json.dumps({"error": f"JSON 解析错误: {e}"}, ensure_ascii=False))
        sys.exit(1)

    data["author"] = data.get("author", "TPM")
    data["recipient"] = data.get("recipient", agent_name)  # TASK goes to assignee

    result = run_create_flow("TASK", agent_name, data)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if "error" in result:
        sys.exit(1)


if __name__ == "__main__":
    main()
