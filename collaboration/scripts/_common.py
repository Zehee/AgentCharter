"""Common utilities for new-* command scripts.

Handles the shared pipeline: validate agent → parse template → validate flow →
generate name → validate fields → write file → output result with redlines.
All exceptions are caught and returned as clean JSON errors.
"""

import json
import sys
import traceback
from pathlib import Path

# Add lib/ to path
_SCRIPTS_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(_SCRIPTS_DIR / "lib"))

from template import parse_template  # noqa: E402
from actions import validate_agent, get_role, is_tpm  # noqa: E402
from naming import generate_filename  # noqa: E402
from registry import get_next_nnn, format_nnn, AUTO_NNN_TYPES  # noqa: E402
from redlines import get_redlines_string  # noqa: E402

SCRIPTS_DIR = _SCRIPTS_DIR
COLLAB_DIR = SCRIPTS_DIR.parent


def resolve_template(file_type: str) -> Path:
    """Resolve template file path for a given file type."""
    type_to_template = {
        "TASK": "TASK_NNN_DESC_author@recipient.md",
        "REPORT": "REPORT_NNN_DATE_author@recipient.md",
        "REVISION": "REVISION_NNN_DATE_author@recipient.md",
        "DECISION": "DECISION_NNN_DATE_AUTHOR.md",
        "PROACTIVE_REPORT": "PROACTIVE_REPORT_NNN_DESC_DATE_author@recipient.md",
        "REVIEW_REPORT": "REVIEW_REPORT_NNN_DATE_author@recipient.md",
        "REVIEW_TASK": "REVIEW_TASK_NNN_author@recipient.md",
        "NOTICE": "NOTICE_NNN_DESC_DATE_author@recipient.md",
        "REPLY": "REPLY_NNN_DESC_DATE_author@recipient.md",
        "BLOCKING": "BLOCKING_NNN_DATE_author@recipient.md",
        "BLOCKING_REPLY": "BLOCKING_REPLY_NNN_DATE_author@recipient.md",
        "TASK_TEST": "TASK_TEST_NNN_DESC_author@recipient.md",
        "TEST_REPORT": "TEST_REPORT_NNN_DATE_author@recipient.md",
        "TODO": "TODO_NNN_DESC_SOURCE.md",
    }
    template_name = type_to_template.get(file_type)
    if not template_name:
        return None
    return COLLAB_DIR / "templates" / template_name


def run_create_flow(file_type: str, agent_name: str, data: dict) -> dict:
    """Run the standard create flow for a file type.

    All exceptions caught → returns {"error": "描述"} for clean JSON output.

    Args:
        file_type: e.g. "REPORT", "TASK"
        agent_name: e.g. "KIMI"
        data: field values from user

    Returns:
        dict with result, path, and redlines (or error key)
    """
    try:
        # 1. Validate agent
        agent = validate_agent(agent_name)
        if not agent:
            return {"error": f"无效的 Agent 名称: {agent_name}，请在 ACTIONS.md 中检查已注册的角色"}

        # 2. Parse template
        template_path = resolve_template(file_type)
        if not template_path or not template_path.exists():
            return {"error": f"模板文件不存在: {template_path}"}

        template_info = parse_template(str(template_path))

        # 3. Determine target dir from template
        target_dir = template_info.get("target_dir")
        if not target_dir:
            return {"error": f"模板 {template_path.name} 中未找到「存放位置」字段"}

        # 4. Generate or require NNN
        nnn = data.get("NNN")
        if not nnn:
            # 派生类型：ref_nnn → NNN（REPORT/REVISION 等关联的 TASK 编号就是文件名 NNN）
            ref = data.get("ref_nnn")
            if ref and file_type not in AUTO_NNN_TYPES:
                nnn = ref
                data["NNN"] = nnn
            elif file_type in AUTO_NNN_TYPES:
                try:
                    next_n = get_next_nnn(file_type)
                    nnn = format_nnn(next_n) if next_n else "001"
                    data["NNN"] = nnn
                except Exception as e:
                    return {"error": f"无法获取下一个编号: {e}"}
            else:
                return {"error": f"缺少 NNN 字段。{file_type} 不自增编号，请提供关联的任务编号，例如：new-report.py KIMI '{{\"ref_nnn\":\"042\"}}'"}
            except Exception as e:
                return {"error": f"无法获取下一个编号: {e}"}
        data["NNN"] = nnn

        # 5. Generate filename
        author = data.get("author", agent_name)
        recipient = data.get("recipient", "TPM")
        date = data.get("DATE")
        desc = data.get("DESC")

        try:
            filename = generate_filename(
                file_type=file_type,
                author=author.upper(),
                recipient=recipient.upper(),
                nnn=nnn,
                date=date,
                desc=desc,
            )
        except ValueError as e:
            return {"error": f"文件名生成失败: {e}"}

        # 6. Build target path
        target_path = COLLAB_DIR / target_dir / filename

        # 7. Read template, fill placeholders, write file
        try:
            template_text = template_path.read_text(encoding="utf-8")
        except Exception as e:
            return {"error": f"无法读取模板 {template_path.name}: {e}"}

        filled = template_text
        for key, value in data.items():
            filled = filled.replace("{{" + key + "}}", str(value))
            filled = filled.replace("{{" + key.lower() + "}}", str(value))

        # 8. Preserve unreplaced placeholders as hints
        import re
        unreplaced = re.findall(r'\{\{(\w+)\}\}', filled)
        if unreplaced:
            pass  # Template intentionally keeps some unfilled for manual editing

        try:
            target_path.parent.mkdir(parents=True, exist_ok=True)
            target_path.write_text(filled, encoding="utf-8")
        except PermissionError:
            return {"error": f"无权限写入: {target_path}"}
        except OSError as e:
            return {"error": f"写入文件失败: {e}"}

        # 9. Return result with redlines
        return {
            "result": "✅ 文件已创建",
            "file_type": file_type,
            "path": str(target_path.relative_to(COLLAB_DIR)) if target_path.exists() else str(target_path),
            "filename": filename,
            "target": f"{target_dir}{filename}",
            "redlines": get_redlines_string(),
        }

    except json.JSONDecodeError as e:
        return {"error": f"JSON 解析失败: {e}"}
    except FileNotFoundError as e:
        return {"error": f"文件未找到: {e}"}
    except PermissionError as e:
        return {"error": f"无权限: {e}"}
    except Exception as e:
        # 兜底异常捕获 — 确保 Agent 始终收到 JSON 而非 Python traceback
        return {"error": f"未知错误: {e}\n{traceback.format_exc()}"}


def no_args_response(file_type: str, agent_name: str = None) -> dict:
    """Generate the no-args / name-only response.

    Returns template schema + available options.
    """
    try:
        template_path = resolve_template(file_type)
        if not template_path or not template_path.exists():
            return {"error": f"模板文件不存在: {file_type}"}

        template_info = parse_template(str(template_path))
        response = {
            "file_type": file_type,
            "template": str(template_path.relative_to(COLLAB_DIR)),
            "target_dir": template_info.get("target_dir", "?"),
            "fields": template_info.get("fields", []),
        }

        if agent_name:
            agent_valid = validate_agent(agent_name)
            response["agent"] = agent_name
            response["agent_valid"] = bool(agent_valid)
            if agent_valid:
                from patrol import scan_inbox
                tasks = scan_inbox(agent_name)
                if tasks:
                    response["available_tasks"] = [
                        {"nnn": t["id"], "desc": t["desc"], "priority": t["priority"]}
                        for t in tasks
                    ]

        response["redlines"] = get_redlines_string()
        return response

    except Exception as e:
        return {"error": f"解析模板失败: {e}\n{traceback.format_exc()}"}


def run_and_exit(file_type: str, agent_name: str = None, json_data: str = None):
    """Unified entry for new-*.py scripts: dispatch no-args / name-only / full.

    Prints JSON and exits with appropriate code.
    """
    if not agent_name:
        result = no_args_response(file_type)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    if not json_data:
        result = no_args_response(file_type, agent_name)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    try:
        data = json.loads(json_data)
    except json.JSONDecodeError as e:
        result = {"error": f"JSON 解析失败: {e}", "hint": "请传入合法的 JSON 字符串，例如 new-report.py KIMI '{\"ref_nnn\":\"042\"}'"}
        print(json.dumps(result, ensure_ascii=False, indent=2))
        sys.exit(1)

    result = run_create_flow(file_type, agent_name, data)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if "error" in result:
        sys.exit(1)
