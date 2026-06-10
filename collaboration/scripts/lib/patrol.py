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
    """Scan collaboration/inbox/ for TASK files assigned to agent_name.

    Returns list of dicts with id, desc, priority, filename.
    """
    inbox = COLLAB_DIR / "inbox"
    results = []
    if not inbox.exists():
        return results

    pattern = re.compile(r"TASK_(\d{3})_(.+)_" + re.escape(agent_name) + r"@.*\.md", re.IGNORECASE)
    priority_pattern = re.compile(r"\*\*优先级\*\*:\s*(.+)")

    for f in sorted(inbox.iterdir()):
        if not f.is_file() or f.suffix != ".md":
            continue
        m = pattern.search(f.name)
        if m:
            nnn = m.group(1)
            desc = m.group(2)
            # Try to extract priority from file content
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
                "priority": priority,
                "filename": f.name,
            })

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
    """扫描 outbox/ 和 inbox/ 中发给 agent_name 的 REVIEW_REPORT。"""
    pattern = re.compile(r"REVIEW_REPORT_(\d{3})_\d{8}_.*@" + re.escape(agent_name) + r"\.md", re.IGNORECASE)
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
    """扫描 outbox/ 中发给 agent_name 的 BLOCKING。"""
    pattern = re.compile(r"BLOCKING_(\d{3})_\d{8}_.*@" + re.escape(agent_name) + r"\.md", re.IGNORECASE)
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


def main():
    """CLI: python lib/patrol.py KIMI"""
    if len(sys.argv) < 2:
        print(json.dumps({"error": "Usage: python lib/patrol.py AGENT_NAME"}, ensure_ascii=False))
        sys.exit(1)

    result = patrol(sys.argv[1].upper())
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
