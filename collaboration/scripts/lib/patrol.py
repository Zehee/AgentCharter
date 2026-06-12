"""Patrol module — scans inbox/outbox for pending tasks and reports.

Path resolution: scripts/lib/patrol.py → scripts/ → project root → collaboration/
Pure Python stdlib, zero deps.
"""

import json
import re
import sys
from pathlib import Path


SCRIPTS_DIR = Path(__file__).resolve().parent.parent
COLLAB_DIR = SCRIPTS_DIR.parent


def scan_inbox(agent_name: str) -> list[dict]:
    """Scan collaboration/inbox/ for TASK and NOTICE files assigned to agent_name.

    Returns list of dicts with id, desc, type, priority, filename.
    """
    inbox = COLLAB_DIR / "inbox"
    results = []
    if not inbox.exists():
        return results

    # TASK patterns — support old format, new format author=agent, and new format recipient=agent
    task_pattern = re.compile(
        r"TASK_(\d{3})_(.+?)_" + re.escape(agent_name) + r"(?:@.*)?\.md$",
        re.IGNORECASE,
    )
    task_pattern_recipient = re.compile(
        r"TASK_(\d{3})_(.+?)_.*@" + re.escape(agent_name) + r"\.md$",
        re.IGNORECASE,
    )
    # NOTICE patterns — direct to agent OR broadcast to ALL
    notice_pattern_agent = re.compile(
        r"NOTICE_(\d{3})_(.+?)_\d{8}_" + re.escape(agent_name) + r"@.*\.md$",
        re.IGNORECASE,
    )
    notice_pattern_all = re.compile(
        r"NOTICE_(\d{3})_(.+?)_\d{8}_.*@ALL\.md$",
        re.IGNORECASE,
    )
    priority_pattern = re.compile(r"\*\*优先级\*\*:\s*(.+)")

    for f in sorted(inbox.iterdir()):
        if not f.is_file() or f.suffix != ".md":
            continue

        # Try TASK (old format, new format author=agent, or new format recipient=agent)
        m = task_pattern.match(f.name) or task_pattern_recipient.match(f.name)
        if m:
            nnn = m.group(1)
            desc = m.group(2)
            priority = "—"
            try:
                text = f.read_text(encoding="utf-8", errors="ignore")
                pm = priority_pattern.search(text)
                if pm:
                    priority = pm.group(1).strip()
            except Exception:
                pass
            results.append({
                "id": nnn,
                "desc": desc,
                "type": "TASK",
                "priority": priority,
                "filename": f.name,
            })
            continue

        # Try NOTICE directed to agent
        m = notice_pattern_agent.match(f.name)
        if m:
            nnn = m.group(1)
            desc = m.group(2)
            results.append({
                "id": nnn,
                "desc": desc,
                "type": "NOTICE",
                "priority": "—",
                "filename": f.name,
            })
            continue

        # Try NOTICE broadcast to ALL
        m = notice_pattern_all.match(f.name)
        if m:
            nnn = m.group(1)
            desc = m.group(2)
            results.append({
                "id": nnn,
                "desc": desc,
                "type": "NOTICE",
                "priority": "—",
                "filename": f.name,
            })
            continue

    return results


def scan_outbox(agent_name: str) -> list[dict]:
    """Scan collaboration/outbox/ for REPORT files authored by agent_name.

    Returns list of dicts with id, status, filename.
    """
    outbox = COLLAB_DIR / "outbox"
    results = []
    if not outbox.exists():
        return results

    pattern = re.compile(r"REPORT_(\d{3})_\d{8}_" + re.escape(agent_name) + r"@.*\.md", re.IGNORECASE)

    for f in sorted(outbox.iterdir()):
        if not f.is_file() or f.suffix != ".md":
            continue
        m = pattern.search(f.name)
        if m:
            nnn = m.group(1)
            results.append({
                "id": nnn,
                "filename": f.name,
            })

    return results


def scan_files(directory_name: str, pattern: re.Pattern) -> list[dict]:
    """通用目录扫描：扫描指定目录下匹配正则的文件。"""
    target = COLLAB_DIR / directory_name
    results = []
    if not target.exists():
        return results
    for f in sorted(target.iterdir()):
        if not f.is_file() or f.suffix != ".md":
            continue
        m = pattern.search(f.name)
        if m:
            results.append({
                "id": m.group(1),
                "filename": f.name,
            })
    return results


def scan_review_reports(agent_name: str) -> list[dict]:
    """扫描 outbox/ 和 inbox/ 中发给 agent_name 或 @ALL 的 REVIEW_REPORT。"""
    pattern = re.compile(
        r"REVIEW_REPORT_(\d{3})_\d{8}_.*@(?:" + re.escape(agent_name) + r"|ALL)\.md",
        re.IGNORECASE,
    )
    outbox_items = scan_files("outbox", pattern)
    inbox_items = scan_files("inbox", pattern)
    seen = set()
    merged = []
    for item in outbox_items + inbox_items:
        if item["id"] not in seen:
            seen.add(item["id"])
            merged.append(item)
    return merged


def scan_blockings(agent_name: str) -> list[dict]:
    """扫描 outbox/ 中发给 agent_name 或 @ALL 的 BLOCKING。"""
    pattern = re.compile(
        r"BLOCKING_(\d{3})_\d{8}_.*@(?:" + re.escape(agent_name) + r"|ALL)\.md",
        re.IGNORECASE,
    )
    return scan_files("outbox", pattern)


def patrol(agent_name: str) -> dict:
    """Run full patrol for an agent.

    Returns dict with inbox_tasks, outbox_reports, total_pending.
    """
    inbox_tasks = scan_inbox(agent_name)
    outbox_reports = scan_outbox(agent_name)
    return {
        "agent": agent_name,
        "inbox": {
            "total": len(inbox_tasks),
            "tasks": inbox_tasks,
        },
        "outbox": {
            "total": len(outbox_reports),
            "reports": outbox_reports,
        },
        "total_pending": len(inbox_tasks) + len(outbox_reports),
    }


def tpm_overview(agent_name: str, available_commands: list[str] | None = None) -> dict:
    """TPM 全览巡检：总览 + @TPM 过滤 + 命令清单。

    从 tpm.py 提取为复用函数，供 charterTool 巡检态调用。
    """
    from actions import validate_agent, is_tpm  # 局部导入避免循环依赖
    from redlines import get_redlines_string

    agent = validate_agent(agent_name)
    if not agent:
        return {"error": f"无效的 Agent 名称: {agent_name}"}

    if not is_tpm(agent_name):
        return {"error": f"{agent_name} 不是 TPM", "hint": "外部 Agent 请使用 agent.py"}

    inbox_dir = COLLAB_DIR / "inbox"
    outbox_dir = COLLAB_DIR / "outbox"
    decisions_dir = COLLAB_DIR / "decisions"

    def count_files(d: Path) -> int:
        if not d.exists():
            return 0
        return len([f for f in d.iterdir() if f.suffix == ".md" and f.name != ".gitkeep"])

    total_inbox = count_files(inbox_dir)
    total_outbox = count_files(outbox_dir)
    total_decisions = count_files(decisions_dir)

    tpm_tasks = scan_inbox(agent_name) if inbox_dir.exists() else []

    return {
        "agent": agent_name,
        "role": "TPM",
        "overview": {
            "inbox_total": total_inbox,
            "outbox_total": total_outbox,
            "decisions_total": total_decisions,
        },
        "my_tasks_in_inbox": tpm_tasks,
        "available_commands": available_commands or [],
        "suggested": f"inbox 中有 {total_inbox} 个文件，其中 {len(tpm_tasks)} 个分配给 TPM。"
                     f"outbox 中有 {total_outbox} 个报告待审阅。运行 daily-check.py 做全量校验。",
        "redlines": get_redlines_string(),
    }


def main():
    """CLI: python lib/patrol.py KIMI"""
    if len(sys.argv) < 2:
        print(json.dumps({"error": "Usage: python lib/patrol.py AGENT_NAME"}, ensure_ascii=False))
        sys.exit(1)

    result = patrol(sys.argv[1].upper())
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
