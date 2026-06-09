#!/usr/bin/env python3
"""
AgentCharter CHANGELOG 自动化生成器
基于 Git commit 历史生成 Keep a Changelog 格式草稿。

用法:
    python generate.py [version] > CHANGELOG.new.md

默认生成自上次 tag 以来的变更。可传入目标版本号覆盖。
"""

import re
import subprocess
import sys
from datetime import datetime
from typing import Dict, List

CATEGORIES = {
    "Added": [],
    "Changed": [],
    "Fixed": [],
    "Philosophy": [],
    "Removed": [],
    "Deprecated": [],
    "Security": [],
}

PREFIX_MAP = {
    "add": "Added",
    "added": "Added",
    "feat": "Added",
    "feature": "Added",
    "new": "Added",
    "change": "Changed",
    "changed": "Changed",
    "update": "Changed",
    "refactor": "Changed",
    "rewrite": "Changed",
    "fix": "Fixed",
    "fixed": "Fixed",
    "bugfix": "Fixed",
    "remove": "Removed",
    "removed": "Removed",
    "delete": "Removed",
    "deprecate": "Deprecated",
    "deprecated": "Deprecated",
    "security": "Security",
    "secure": "Security",
    "philosophy": "Philosophy",
    "philosophical": "Philosophy",
}


def get_last_tag() -> str:
    """获取最新的 git tag。"""
    try:
        result = subprocess.run(
            ["git", "describe", "--tags", "--abbrev=0"],
            capture_output=True,
            text=True,
            check=True,
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        return ""


def get_commits(since_tag: str = "") -> List[Dict[str, str]]:
    """获取 commit 列表。"""
    cmd = ["git", "log", "--format=%H|%s|%ad", "--date=short"]
    if since_tag:
        cmd.append(f"{since_tag}..HEAD")
    result = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace", check=False)
    if result.returncode != 0 or not result.stdout:
        return []
    commits = []
    for line in result.stdout.strip().splitlines():
        parts = line.split("|", 2)
        if len(parts) == 3:
            commits.append({"hash": parts[0][:8], "subject": parts[1], "date": parts[2]})
    return commits


def classify_commit(subject: str) -> str:
    """根据 commit message 前缀分类。"""
    lower = subject.lower()
    # 尝试匹配 "Category: message" 或 "category: message" 格式
    m = re.match(r"^([\w-]+)\s*[:，]\s*(.+)$", subject)
    if m:
        prefix = m.group(1).lower().replace("-", " ")
        for key, cat in PREFIX_MAP.items():
            if key in prefix:
                return cat
    # 尝试匹配括号格式如 "[Added] xxx" 或 "(fix) xxx"
    m = re.match(r"^[\[(]([\w-]+)[\])]\s*(.+)$", subject)
    if m:
        prefix = m.group(1).lower()
        for key, cat in PREFIX_MAP.items():
            if key in prefix:
                return cat
    # 关键词 fallback
    if "fix" in lower or "bug" in lower:
        return "Fixed"
    if "add" in lower or "new" in lower:
        return "Added"
    if "change" in lower or "update" in lower or "rewrite" in lower:
        return "Changed"
    if "remove" in lower or "delete" in lower:
        return "Removed"
    return "Changed"  # 默认分类


def generate(version: str = "", since_tag: str = "") -> str:
    """生成 CHANGELOG 草稿。"""
    if not since_tag:
        since_tag = get_last_tag()
    commits = get_commits(since_tag)
    if not commits:
        return "# 无变更\n\n自上次发布以来没有新的 commit。\n"

    categories = {k: [] for k in CATEGORIES}
    for c in commits:
        cat = classify_commit(c["subject"])
        if cat in categories:
            categories[cat].append(c)

    lines = []
    ver = version if version else "[Unreleased]"
    date_str = datetime.now().strftime("%Y-%m-%d")
    if version:
        lines.append(f"## {ver} - {date_str}")
    else:
        lines.append(f"## {ver}")
    lines.append("")

    for cat, items in categories.items():
        if not items:
            continue
        lines.append(f"### {cat}")
        lines.append("")
        for item in items:
            msg = item["subject"]
            # 去重已有的 hash 引用
            msg = re.sub(r"\s*\([a-f0-9]{8}\)\s*$", "", msg)
            lines.append(f"- {msg} ({item['hash']})")
        lines.append("")

    return "\n".join(lines)


def main() -> int:
    version = sys.argv[1] if len(sys.argv) > 1 else ""
    output = generate(version)
    print(output)
    return 0


if __name__ == "__main__":
    sys.exit(main())
