"""Common utilities for new-* command scripts.

Handles the shared pipeline: validate agent → parse template → validate flow →
generate name → validate fields → write file → output result with redlines.
All exceptions are caught and returned as clean JSON errors.
"""

import json
import re
import sys
import traceback
from datetime import date
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

# 创建权限表（用于 charterTool body 模式）
TPM_ONLY_TYPES = {
    "TASK", "TASK_TEST", "REVISION", "NOTICE",
    "REVIEW_TASK", "REPLY", "TODO",
}
EXTERNAL_CREATABLE_TYPES = {
    "REPORT", "TEST_REPORT", "REVIEW_REPORT", "PROACTIVE_REPORT",
    "BLOCKING", "BLOCKING_REPLY", "DECISION",
}
CREATABLE_TYPES = TPM_ONLY_TYPES | EXTERNAL_CREATABLE_TYPES

# 需要从 body 中提取 DESC 的文件类型
_TYPES_NEED_DESC = {"TASK", "PROACTIVE_REPORT", "NOTICE", "REPLY", "TODO", "TASK_TEST"}


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


# 支持多轮次的文件类型
_ROUND_SUPPORTED = {"REPORT", "REVIEW_REPORT", "REVISION"}


def _detect_existing_round(file_type: str, nnn: str, target_dir: str) -> tuple[int, str]:
    """检测同 NNN 已有文件的最大轮次。返回 (max_round, hint)。

    max_round=-1 表示没有同 NNN 文件（可以创建首轮）。
    max_round=0  表示已有首轮文件，建议创建 _R1。
    max_round=1  表示已有 _R1，建议创建 _R2。
    """
    if file_type not in _ROUND_SUPPORTED:
        return -1, ""

    search_dir = COLLAB_DIR / target_dir
    if not search_dir.exists():
        return -1, ""

    pattern = re.compile(rf"{re.escape(file_type)}_{re.escape(nnn)}(_R(\d+))?_.*\.md")
    max_round = -1
    for f in search_dir.iterdir():
        if not f.is_file():
            continue
        m = pattern.match(f.name)
        if m:
            r = int(m.group(2)) if m.group(2) else 0  # 首轮文件 = 轮次 0
            if r > max_round:
                max_round = r
    if max_round == -1:
        return -1, ""
    next_round = max_round + 1
    if max_round == 0:
        return 0, f"已有首轮 {file_type}_{nnn}，建议创建 _R1"
    return max_round, f"已有 _R{max_round}，建议创建 _R{next_round}"


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


def _extract_title(body: str) -> str:
    """从 markdown 正文提取标题。优先取第一行 # 标题。"""
    for line in body.splitlines():
        line = line.strip()
        if line.startswith("#"):
            return line.lstrip("#").strip()
    # 无标题则取第一行非空文本
    for line in body.splitlines():
        line = line.strip()
        if line:
            return line
    return ""


def _extract_desc(body: str) -> str | None:
    """从 body 中提取 DESC（用于文件名）。

    优先级：
    1. HTML 注释 `<!-- DESC: ENGLISH-DESC -->`
    2. 加粗元信息 `**DESC**: ENGLISH-DESC`
    3. 独立行 `DESC: ENGLISH-DESC`
    """
    patterns = [
        r"<!--\s*DESC:\s*([A-Z0-9-]+)\s*-->",
        r"\*\*DESC\*\*:\s*([A-Z0-9-]+)",
        r"^DESC:\s*([A-Z0-9-]+)\s*$",
    ]
    for pat in patterns:
        m = re.search(pat, body, re.MULTILINE | re.IGNORECASE)
        if m:
            return m.group(1).upper()
    return None


def _title_to_desc(title: str) -> str:
    """将标题转换为大写英文简短描述（仅保留字母/数字/空格/连字符）。"""
    # 移除 markdown 标记，但保留下划线作为分段符
    title = re.sub(r"[#*`\[\]()<>]", "", title)
    # 将下划线/冒号替换为空格，便于分词
    title = title.replace("_", " ").replace(":", " ")
    # 保留 ASCII 字母数字和空格
    cleaned = re.sub(r"[^A-Za-z0-9\s-]", "", title)
    parts = [p for p in cleaned.split() if p]
    if not parts:
        return "GENERATED"
    return "-".join(parts[:6]).upper()


def _infer_recipient(file_type: str, body: str, ref: str | None, author: str) -> str:
    """根据文件类型和 body 推断 recipient。"""
    # 优先从 body 元信息读取
    for pat in [r"<!--\s*RECIPIENT:\s*([A-Z]+)\s*-->",
                r"\*\*recipient\*\*:\s*([A-Z]+)",
                r"^RECIPIENT:\s*([A-Z]+)\s*$"]:
        m = re.search(pat, body, re.MULTILINE | re.IGNORECASE)
        if m:
            return m.group(1).upper()

    if file_type == "NOTICE":
        return "ALL"

    if file_type in {"DECISION", "TODO", "LOG_ENTRY"}:
        # 这些类型在文件名中没有 @recipient
        return ""

    # 任务类文件：收件人为执行人/测试员/被审查人
    if file_type in {"TASK", "TASK_TEST", "REVISION", "REVIEW_TASK"}:
        assignee = _extract_assignee_from_text(body)
        if assignee:
            return assignee
        return "TPM"

    if file_type == "REVIEW_REPORT" and ref:
        # 尝试从对应 TASK 提取 assignee 作为 recipient（自循环）
        task_file = _find_ref_file("TASK", ref)
        if task_file:
            assignee = _extract_assignee(task_file)
            if assignee:
                return assignee.upper()
        # 委派审查默认给 TPM
        return "TPM"

    if file_type == "BLOCKING":
        # 尝试从 body 中的「目标受众」/ TARGET 提取
        m = re.search(r"\*\*目标受众\*\*:\s*([A-Z]+)", body, re.IGNORECASE)
        if m:
            return m.group(1).upper()
        return "TPM"

    # 默认 TPM
    return "TPM"


def _find_ref_file(file_type: str, nnn: str) -> Path | None:
    """在活跃目录中查找指定类型和编号的文件。"""
    for d in ["inbox", "outbox", "decisions"]:
        search_dir = COLLAB_DIR / d
        if not search_dir.exists():
            continue
        for f in search_dir.iterdir():
            if f.is_file() and f.suffix == ".md" and f.name.startswith(f"{file_type}_{nnn}_"):
                return f
    return None


def _extract_assignee(file_path: Path) -> str | None:
    """从 TASK/REVIEW_TASK 文件中提取执行人。"""
    try:
        text = file_path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return None
    return _extract_assignee_from_text(text)


def _extract_assignee_from_text(text: str) -> str | None:
    """从文本中提取执行人/测试员/被审查人。"""
    patterns = [
        r"\*\*执行人\*\*:\s*([A-Za-z0-9_-]+)",
        r"\*\*测试员\*\*:\s*([A-Za-z0-9_-]+)",
        r"\*\*被审查人\*\*:\s*([A-Za-z0-9_-]+)",
        r"\*\*Assignee\*\*:\s*([A-Za-z0-9_-]+)",
    ]
    for pat in patterns:
        m = re.search(pat, text, re.IGNORECASE)
        if m:
            return m.group(1).strip().upper()
    return None


def _can_create(agent_name: str, file_type: str) -> tuple[bool, str | None]:
    """检查 agent_name 是否有权限创建 file_type。"""
    if file_type not in CREATABLE_TYPES:
        return False, f"未知或不支持的文件类型: {file_type}"
    if file_type in TPM_ONLY_TYPES:
        if not is_tpm(agent_name):
            return False, f"{file_type} 为 TPM 独占，{agent_name} 无权创建"
    return True, None


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
        # 0. 输入 key 统一大写（大小写不敏感）
        data = {k.upper(): v for k, v in data.items()}

        # 1. Validate agent
        agent = validate_agent(agent_name)
        if not agent:
            return {"error": f"无效的 Agent 名称: {agent_name}，请在 ACTIONS.md 中检查已注册的角色"}

        # 2. Parse template (body 模式下仍需要 target_dir)
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
            ref = data.get("REF_NNN")
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
        author = data.get("AUTHOR", agent_name)
        default_recipient = "ALL" if file_type == "NOTICE" else "TPM"
        recipient = data.get("RECIPIENT", default_recipient)
        date_str = data.get("DATE")
        desc = data.get("DESC")

        # 将文件名相关字段写回 data，确保模板替换和校验能命中
        data["AUTHOR"] = author
        data["RECIPIENT"] = recipient
        data["DATE"] = date_str if date_str else date.today().strftime("%Y%m%d")
        if desc:
            data["DESC"] = desc

        # 5a. 自动推断轮次（多轮次文件类型）
        round_num = data.get("ROUND")
        if round_num is None and file_type in _ROUND_SUPPORTED:
            existing_round, round_hint = _detect_existing_round(file_type, nnn, target_dir)
            if existing_round >= 0:
                round_num = existing_round + 1
                data["round"] = round_num
                data["round_hint"] = round_hint
            else:
                data["round"] = ""
        elif round_num is None:
            data["round"] = ""

        try:
            filename = generate_filename(
                file_type=file_type,
                author=author.upper(),
                recipient=recipient.upper(),
                nnn=nnn,
                date=date_str,
                desc=desc,
                round=round_num,
            )
        except ValueError as e:
            return {"error": f"文件名生成失败: {e}"}

        # 6. Build target path
        target_path = COLLAB_DIR / target_dir / filename

        # 7. body 模式：直接写入 body
        body = data.get("BODY")
        if body is None:
            return {
                "error": "JSON 传入方案已废除。请使用 body 模式：charterTool(name, type, body='...', ref='...')",
                "hint": "body 中直接写 markdown 正文，脚本自动推断文件名、recipient、DESC 等字段",
                "redlines": get_redlines_string(),
            }

        # 校验是否仍有 {{}} 残留
        unreplaced = set(re.findall(r"\{\{(\w+)\}\}", body))
        if unreplaced:
            return {"error": f"body 不应包含模板变量残留: {', '.join(unreplaced)}"}

        try:
            target_path.parent.mkdir(parents=True, exist_ok=True)
            target_path.write_text(body, encoding="utf-8")
        except PermissionError:
            return {"error": f"无权限写入: {target_path}"}
        except OSError as e:
            return {"error": f"写入文件失败: {e}"}

        # 8. Return result with redlines
        result = {
            "result": "✅ 文件已创建",
            "file_type": file_type,
            "path": str(target_path.relative_to(COLLAB_DIR)) if target_path.exists() else str(target_path),
            "filename": filename,
            "target": f"{target_dir}{filename}",
            "redlines": get_redlines_string(),
        }
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

    JSON 模式已废除，此响应返回 body 模式用法与模板示例。
    """
    try:
        template_path = resolve_template(file_type)
        if not template_path or not template_path.exists():
            return {"error": f"模板文件不存在: {file_type}"}

        template_info = parse_template(str(template_path))
        target_dir = template_info.get("target_dir", "?")
        example = template_path.read_text(encoding="utf-8")

        response = {
            "file_type": file_type,
            "template": str(template_path.relative_to(COLLAB_DIR)),
            "target_dir": target_dir,
            "note": "JSON 传入方案已废除。创建文件请使用 body 模式。",
            "usage_api": f"charterTool('{agent_name or 'NAME'}', '{file_type}', body='# {file_type}_NNN: ...', ref='...')",
            "usage_cli": f"python new-{file_type.lower()}.py {agent_name or 'NAME'} --body body.md",
            "usage_stdin": f"cat body.md | python new-{file_type.lower()}.py {agent_name or 'NAME'}",
            "template_example": example,
        }

        if agent_name:
            agent_valid = validate_agent(agent_name)
            response["agent"] = agent_name
            response["agent_valid"] = bool(agent_valid)
            if agent_valid:
                # 按 file_type 选择正确的关联源提示
                from patrol import scan_inbox, scan_review_reports, scan_blockings

                if file_type == "NOTICE":
                    notices = scan_inbox(agent_name)
                    notices = [n for n in notices if n.get("type") == "NOTICE"]
                    if notices:
                        response["available_notices"] = [
                            {"nnn": n["id"], "desc": n.get("desc", ""), "filename": n["filename"]}
                            for n in notices
                        ]
                else:
                    assoc_map = {
                        "REPORT": ("available_tasks", scan_inbox),
                        "REVISION": ("available_review_reports", scan_review_reports),
                        "REVIEW_REPORT": ("available_tasks", scan_inbox),
                        "BLOCKING_REPLY": ("available_blockings", scan_blockings),
                        "TEST_REPORT": ("available_tasks", scan_inbox),
                    }
                    hint_key, scanner = assoc_map.get(file_type, ("available_tasks", scan_inbox))
                    items = scanner(agent_name)
                    if scanner == scan_inbox:
                        tasks = [t for t in items if t.get("type") == "TASK"]
                        notices = [t for t in items if t.get("type") == "NOTICE"]
                        if tasks:
                            response[hint_key] = [
                                {"nnn": t["id"], "desc": t.get("desc", ""), "priority": t.get("priority", "—")}
                                for t in tasks
                            ]
                        if notices:
                            response["available_notices"] = [
                                {"nnn": n["id"], "desc": n.get("desc", ""), "filename": n["filename"]}
                                for n in notices
                            ]
                    elif items:
                        response[hint_key] = [
                            {"nnn": t["id"], "desc": t.get("desc", ""), "priority": t.get("priority", "—")}
                            for t in items
                        ]

                # 多轮次文件：显示已有文件及建议轮次
                if file_type in _ROUND_SUPPORTED:
                    existing = []
                    for f in (COLLAB_DIR / target_dir).iterdir():
                        if f.is_file() and f.suffix == ".md" and file_type in f.name and agent_name in f.name:
                            existing.append(f.name)
                    if existing:
                        response["existing_files"] = sorted(existing)
                        latest = existing[-1]
                        m = re.search(rf"{re.escape(file_type)}_\d{{3}}(_R(\d+))?_.*", latest)
                        if m and m.group(2):
                            current_r = int(m.group(2))
                            response["round_hint"] = f"已有 _R{current_r}，建议创建 _R{current_r + 1}"
                        else:
                            response["round_hint"] = "已有首轮文件，建议创建 _R1"

        response["redlines"] = get_redlines_string()
        return response

    except Exception as e:
        return {"error": f"解析模板失败: {e}\n{traceback.format_exc()}"}


def run_and_exit(file_type: str, agent_name: str = None, json_data: str = None):
    """Unified entry for new-*.py scripts: dispatch no-args / name-only / full.

    JSON 传入方案已废除；如果仍收到 JSON 数据，返回明确错误提示。
    Prints JSON and exits with appropriate code.
    """
    # Fix Windows GBK encoding issue
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    if not agent_name:
        result = no_args_response(file_type)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    if not json_data:
        result = no_args_response(file_type, agent_name)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    # JSON 方案已废除
    result = {
        "error": "JSON 传入方案已废除。",
        "hint": f"请使用 body 模式：charterTool('{agent_name}', '{file_type}', body='...', ref='...')，或在 shell 中使用 new-{file_type.lower()}.py {agent_name} < ref.txt < body.md",
        "redlines": get_redlines_string(),
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    sys.exit(1)


def run_body_and_exit(file_type: str, agent_name: str, ref: str | None = None, body_file: str | None = None):
    """Body-mode CLI entry for new-*.py scripts.

    Reads body from a file (or stdin if body_file is '-') and calls charterTool.
    Prints JSON and exits with appropriate code.
    """
    # Fix Windows GBK encoding issue
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")

    try:
        if body_file and body_file != "-":
            body = Path(body_file).read_text(encoding="utf-8")
        else:
            # Windows 下 stdin 默认编码可能为 GBK，强制按 UTF-8 读取
            body = sys.stdin.buffer.read().decode("utf-8")
    except Exception as e:
        result = {"error": f"读取 body 失败: {e}", "redlines": get_redlines_string()}
        print(json.dumps(result, ensure_ascii=False, indent=2))
        sys.exit(1)

    if not body.strip():
        result = {"error": "body 为空", "hint": f"请通过 stdin 或 --body 文件传入 markdown 正文，例如：new-{file_type.lower()}.py {agent_name} --body report.md", "redlines": get_redlines_string()}
        print(json.dumps(result, ensure_ascii=False, indent=2))
        sys.exit(1)

    result = charterTool(agent_name, file_type, body=body, ref=ref)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if "error" in result:
        sys.exit(1)


# -----------------------------------------------------------------------------
# charterTool — 统一入口（TASK_039）
# -----------------------------------------------------------------------------

def _run_patrol(name: str) -> dict:
    """巡检态：外部 Agent 用 patrol()，TPM 用 tpm_overview()。"""
    from patrol import patrol, tpm_overview

    agent = validate_agent(name)
    if not agent:
        return {"error": f"无效的 Agent 名称: {name}"}

    if is_tpm(name):
        return tpm_overview(name)
    return patrol(name)


def _run_command(name: str, command: str) -> dict:
    """命令态：TPM 独占。支持 archive / validate-all。"""
    if not is_tpm(name):
        return {"error": "命令态 TPM 独占", "hint": "外部 Agent 请使用创建态 charterTool(name, type, body=...)", "redlines": get_redlines_string()}

    command = command.lower().replace(".py", "")

    if command == "validate-all":
        return _cmd_validate_all()

    if command == "archive":
        return _cmd_archive()

    return {"error": f"未知命令: {command}", "available_commands": ["archive", "validate-all"], "redlines": get_redlines_string()}


def _cmd_validate_all() -> dict:
    """调用 validate.validate_all 对 inbox/outbox/decisions 做全量校验。"""
    from validate import validate_all
    from redlines import get_redlines_string

    dirs = ["inbox", "outbox", "decisions"]
    details = []
    total_passed = 0
    total_failed = 0

    for d in dirs:
        target = COLLAB_DIR / d
        if not target.exists():
            details.append({"directory": str(d), "error": "目录不存在"})
            total_failed += 1
            continue
        result = validate_all(target)
        details.append(result)
        if "summary" in result:
            total_passed += result["summary"].get("passed", 0)
            total_failed += result["summary"].get("failed", 0)

    return {
        "result": "✅ 全量校验完成" if total_failed == 0 else "⚠️ 全量校验发现问题",
        "summary": {
            "total": total_passed + total_failed,
            "passed": total_passed,
            "failed": total_failed,
        },
        "details": details,
        "redlines": get_redlines_string(),
    }


def _cmd_archive() -> dict:
    """自动归档已完成关联链的文件。

    当前策略：
    - REPORT / REVIEW_REPORT / NOTICE / REPLY / PROACTIVE_REPORT / TEST_REPORT / BLOCKING_REPLY：
      文件顶部含 `> ✅ 已读 BY ...` 即视为可归档。
    - DECISION：关联 TASK/TODO 全部完成后归档（当前保守策略：不自动归档 DECISION）。
    - TASK / REVISION / REVIEW_TASK / TODO / BLOCKING：不自动归档，避免误删进行中任务。
    """
    from naming import classify

    auto_archive_types = {
        "REPORT", "REVIEW_REPORT", "NOTICE", "REPLY",
        "PROACTIVE_REPORT", "TEST_REPORT", "BLOCKING_REPLY",
    }
    archived = []
    skipped = []

    for d in ["inbox", "outbox"]:
        target = COLLAB_DIR / d
        if not target.exists():
            continue
        for f in target.iterdir():
            if not f.is_file() or f.suffix != ".md":
                continue
            file_type = classify(f.name)
            if file_type not in auto_archive_types:
                continue
            try:
                text = f.read_text(encoding="utf-8", errors="ignore")
            except Exception:
                continue
            if "> ✅ 已读 BY" in text:
                # 链式归档
                result = _archive_chain(f)
                if "error" in result:
                    skipped.append({"file": f.name, "reason": result["error"]})
                else:
                    archived.extend(result.get("details", [result]))
            else:
                skipped.append({"file": f.name, "reason": "缺少已读标识"})

    return {
        "result": "✅ 自动归档完成" if archived else "📭 无可归档文件",
        "archived_count": len(archived),
        "skipped_count": len(skipped),
        "archived": archived,
        "skipped": skipped,
        "redlines": get_redlines_string(),
    }


def _archive_chain(file_path: Path) -> dict:
    """调用 archive.py 的链式归档逻辑。"""
    # 直接复用 archive.py 的函数，避免子进程
    sys.path.insert(0, str(SCRIPTS_DIR / "lib"))
    try:
        from archive import archive_chain as _ac
        return _ac(file_path)
    except Exception as e:
        return {"error": f"链式归档失败: {e}"}


def _create_file(name: str, file_type: str, body: str, ref: str | None) -> dict:
    """创建态：权限 → 引用 → 文件名 → body 写入。"""
    file_type = file_type.upper()

    # 权限校验
    ok, err = _can_create(name, file_type)
    if not ok:
        return {"error": err, "redlines": get_redlines_string()}

    # 校验 body 不含 {{}} 残留
    if re.search(r"\{\{\w+\}\}", body):
        return {"error": "body 不应包含 {{变量}} 模板占位符，请直接写 markdown 正文", "redlines": get_redlines_string()}

    # 准备 data
    data = {
        "author": name,
        "DATE": date.today().strftime("%Y%m%d"),
        "body": body,
    }

    # 处理 ref / 自增
    if file_type in AUTO_NNN_TYPES:
        # 自增类型：忽略 ref
        pass
    else:
        if not ref:
            return {"error": f"{file_type} 需要提供 ref（对应源编号）", "redlines": get_redlines_string()}
        data["ref_nnn"] = ref

    # 从 body 提取 title / desc
    title = _extract_title(body)
    data["title"] = title
    desc = _extract_desc(body)
    if desc is None:
        desc = _title_to_desc(title)
    data["DESC"] = desc

    # 推断 recipient
    recipient = _infer_recipient(file_type, body, ref, name)
    if recipient:
        data["recipient"] = recipient

    return run_create_flow(file_type, name, data)


def charterTool(
    name: str,
    type: str | None = None,
    *,
    body: str | None = None,
    ref: str | None = None,
) -> dict:
    """统一工具入口：三态覆盖全功能。

    形态 1 — 巡检态：
        charterTool("KIMI") -> 返回该 Agent 的 patrol 结果

    形态 2 — 命令态（TPM 独占）：
        charterTool("TPM", "archive")       -> 自动归档已完成文件链
        charterTool("TPM", "validate-all")  -> 全量校验

    形态 3 — 创建态：
        charterTool("KIMI", "REPORT", body="...", ref="042")
        charterTool("TPM", "TASK", body="...")
    """
    name = name.upper()

    # 形态 1：无 type -> 巡检
    if type is None:
        return _run_patrol(name)

    # 形态 2：无 body -> 命令
    if body is None:
        return _run_command(name, type)

    # 形态 3：创建文件
    return _create_file(name, type, body, ref)
