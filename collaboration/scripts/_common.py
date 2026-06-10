"""Common utilities for new-* command scripts.

Handles the shared pipeline: validate agent → parse template → validate flow →
generate name → validate fields → write file → output result with redlines.
All exceptions are caught and returned as clean JSON errors.
"""

import json
import re
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

# 文件类型 → 应关联的源文件类型 → 源文件所在的扫描目录
REF_MAP = {
    "REPORT": ["TASK", "REVISION"],        # REPORT 对应 TASK 或 REVISION
    "REVISION": ["REVIEW_REPORT"],         # REVISION 对应 REVIEW_REPORT
    "REVIEW_REPORT": ["TASK", "REPORT"],   # REVIEW_REPORT 对应 TASK 或 REPORT
    "REVIEW_TASK": ["TASK"],               # REVIEW_TASK 对应 TASK
    "BLOCKING_REPLY": ["BLOCKING"],        # BLOCKING_REPLY 对应 BLOCKING
    "TEST_REPORT": ["TASK_TEST"],          # TEST_REPORT 对应 TASK_TEST
    # 以下类型不需要关联校验（有自增编号或无编号）：
    # TASK, TASK_TEST, DECISION — 自增编号（AUTO_NNN_TYPES）
    # PROACTIVE_REPORT, NOTICE, REPLY — 无关联，无 ref_nnn
    # BLOCKING — 发起方自由声明
    # TODO, LOG_ENTRY — 非协作文件
}


def _check_ref_exists(ref_nnn: str, file_type: str) -> str | None:
    """验证 ref_nnn 对应的源文件是否存在。返回错误信息或 None。"""
    source_types = REF_MAP.get(file_type, [])
    if not source_types:
        return None  # 不自增也无关联校验的类型（NOTICE、TODO 等）

    # 每种源类型可能有多个目录（活跃/归档）
    search_dirs_map = {
        "TASK": ["inbox", "archive/inbox"],
        "REVISION": ["inbox", "archive/inbox"],
        "REVIEW_REPORT": ["inbox", "outbox", "archive/inbox", "archive/outbox"],
        "REPORT": ["outbox", "archive/outbox"],
        "BLOCKING": ["outbox"],
        "TASK_TEST": ["inbox", "archive/inbox"],
    }

    for src_type in source_types:
        dirs = search_dirs_map.get(src_type, ["inbox"])
        for d in dirs:
            search_dir = COLLAB_DIR / d
            if not search_dir.exists():
                continue
            for f in search_dir.iterdir():
                if f.is_file() and f.suffix == ".md" and f"{src_type}_{ref_nnn}" in f.name:
                    return None  # 找到了
        # 没找到 → 继续试下一个源类型

    expected = " 或 ".join(source_types)
    return f"未找到 {expected}_{ref_nnn} 文件——请先创建对应的 {expected} 或确认编号正确"


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
            ref = data.get("ref_nnn")
            if ref and file_type not in AUTO_NNN_TYPES:
                nnn = ref
            elif file_type in AUTO_NNN_TYPES:
                try:
                    nnn = format_nnn(get_next_nnn(file_type))
                except Exception as e:
                    return {"error": f"无法获取下一个编号: {e}"}
            else:
                return {"error": f"缺少 NNN 字段。{file_type} 不自增编号，请提供 ref_nnn，例如：new-report.py KIMI '{{\"ref_nnn\":\"042\"}}'"}
        data["NNN"] = nnn

        # 4b. Verify referenced source file exists（BLOCKING_REPLY→BLOCKING、REPORT→TASK……）
        if file_type in REF_MAP:
            ref_err = _check_ref_exists(nnn, file_type)
            if ref_err:
                return {"error": ref_err}

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

        # 8. 校验必填变量 + 警告可选字段遗漏
        import re
        name_pattern = template_info.get("name_pattern", "")
        name_vars = set(re.findall(r'\{\{(\w+)\}\}', name_pattern))
        unreplaced = set(re.findall(r'\{\{(\w+)\}\}', filled))
        missing_required = [v for v in name_vars if v in unreplaced]
        if missing_required:
            return {"error": f"必填字段未提供（影响文件名生成）: {', '.join(missing_required)}"}

        # 正文可选字段遗漏 → 不阻断，记录 warning
        body_unfilled = [v for v in unreplaced if v not in name_vars]
        body_warning = None
        if body_unfilled:
            body_warning = f"以下正文字段未填写，建议补充后更新文件: {', '.join(body_unfilled)}"

        try:
            target_path.parent.mkdir(parents=True, exist_ok=True)
            target_path.write_text(filled, encoding="utf-8")
        except PermissionError:
            return {"error": f"无权限写入: {target_path}"}
        except OSError as e:
            return {"error": f"写入文件失败: {e}"}

        # 9. Return result with redlines
        result = {
            "result": "✅ 文件已创建",
            "file_type": file_type,
            "path": str(target_path.relative_to(COLLAB_DIR)) if target_path.exists() else str(target_path),
            "filename": filename,
            "target": f"{target_dir}{filename}",
            "redlines": get_redlines_string(),
        }
        if body_warning:
            result["warning"] = body_warning
        return result

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
                # 按 file_type 选择正确的关联源提示
                from patrol import scan_inbox, scan_review_reports, scan_blockings

                assoc_map = {
                    "REPORT": ("available_tasks", scan_inbox),
                    "REVISION": ("available_review_reports", scan_review_reports),
                    "REVIEW_REPORT": ("available_tasks", scan_inbox),
                    "BLOCKING_REPLY": ("available_blockings", scan_blockings),
                    "TEST_REPORT": ("available_tasks", scan_inbox),
                }
                hint_key, scanner = assoc_map.get(file_type, ("available_tasks", scan_inbox))
                items = scanner(agent_name)
                if items:
                    response[hint_key] = [
                        {"nnn": t["id"], "desc": t.get("desc", ""), "priority": t.get("priority", "—")}
                        for t in items
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
