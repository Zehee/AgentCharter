"""Common utilities for new-* command scripts.

Handles the shared pipeline: validate agent → parse template → validate flow →
generate name → validate fields → write file → output result with redlines.
"""

import json
import sys
from pathlib import Path

# Add lib/ to path
_SCRIPTS_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(_SCRIPTS_DIR / "lib"))

from template import parse_template  # noqa: E402
from actions import validate_agent, get_role, validate_flow, is_tpm  # noqa: E402
from naming import generate_filename  # noqa: E402
from registry import get_next_nnn, format_nnn  # noqa: E402
from redlines import get_redlines_string  # noqa: E402

SCRIPTS_DIR = _SCRIPTS_DIR
COLLAB_DIR = SCRIPTS_DIR.parent


def resolve_template(file_type: str) -> Path:
    """Resolve template file path for a given file type."""
    # Map file types to template filenames
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

    Args:
        file_type: e.g. "REPORT", "TASK"
        agent_name: e.g. "KIMI"
        data: field values from user

    Returns:
        dict with result, path, and redlines
    """
    # 1. Validate agent
    agent = validate_agent(agent_name)
    if not agent:
        return {"error": f"无效的 Agent 名称: {agent_name}"}

    role_info = get_role(agent_name)

    # 2. Parse template
    template_path = resolve_template(file_type)
    if not template_path or not template_path.exists():
        return {"error": f"模板文件不存在: {template_path}"}

    template_info = parse_template(str(template_path))

    # 3. Determine target dir from template
    target_dir = template_info.get("target_dir", "inbox/")

    # 4. Generate NNN if not provided
    nnn = data.get("NNN")
    if not nnn:
        if file_type in ("TASK", "TASK_TEST"):
            next_n = get_next_nnn(file_type, str(COLLAB_DIR / "inbox"))
        else:
            # For other types, try to get from reference or auto
            next_n = get_next_nnn(file_type)

        if next_n:
            nnn = format_nnn(next_n)
        else:
            nnn = "001"

    data["NNN"] = nnn

    # 5. Generate filename
    author = data.get("author", agent_name)
    recipient = data.get("recipient", "TPM")
    date = data.get("DATE")
    desc = data.get("DESC")

    filename = generate_filename(
        file_type=file_type,
        author=author.upper(),
        recipient=recipient.upper(),
        nnn=nnn,
        date=date,
        desc=desc,
    )

    # 6. Build target path
    target_path = COLLAB_DIR / target_dir / filename

    # 7. Read template, fill placeholders, write file
    try:
        template_text = template_path.read_text(encoding="utf-8")
    except Exception as e:
        return {"error": f"无法读取模板: {e}"}

    # Fill placeholders with data
    filled = template_text
    for key, value in data.items():
        filled = filled.replace("{{" + key + "}}", str(value))
        # Also fill markdown-style placeholders
        placeholder_lower = "{{" + key.lower() + "}}"
        filled = filled.replace(placeholder_lower, str(value))

    # Write file
    try:
        target_path.parent.mkdir(parents=True, exist_ok=True)
        target_path.write_text(filled, encoding="utf-8")
    except Exception as e:
        return {"error": f"无法写入文件: {e}"}

    # 8. Return result with redlines
    return {
        "result": "✅ 文件已创建",
        "file_type": file_type,
        "path": str(target_path.relative_to(SCRIPTS_DIR.parent)),
        "filename": filename,
        "target": f"{target_dir}{filename}",
        "redlines": get_redlines_string(),
    }


def no_args_response(file_type: str, agent_name: str = None) -> dict:
    """Generate the no-args / name-only response.

    Returns template schema + available options.
    """
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

    # If agent name provided, add patrol info
    if agent_name:
        agent_valid = validate_agent(agent_name)
        response["agent"] = agent_name
        response["agent_valid"] = bool(agent_valid)
        if agent_valid:
            from patrol import scan_inbox  # noqa: F811
            tasks = scan_inbox(agent_name)
            if tasks:
                response["available_tasks"] = [
                    {"nnn": t["id"], "desc": t["desc"], "priority": t["priority"]}
                    for t in tasks
                ]

    response["redlines"] = get_redlines_string()
    return response
