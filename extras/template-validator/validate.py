#!/usr/bin/env python3
"""
AgentCharter Template Validator
验证协作文件是否符合框架命名规范和内容格式。

用法:
    python validate.py [path ...]

默认验证 collaboration/templates/ 和 collaboration_en/templates/。
可传入任意目录验证用户项目中的协作文件。
"""

import os
import re
import sys
from pathlib import Path
from typing import List, Tuple

# Windows UTF-8 输出支持
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

# ---------- 命名规范正则 ----------
NAME_PATTERNS = {
    "TASK": r"^TASK_\d{3}_[A-Z0-9-]+_[A-Z]+\.md$",
    "REPORT": r"^REPORT_\d{3}_\d{8}_[A-Z]+\.md$",
    "REVIEW_REPORT": r"^REVIEW_REPORT_\d{3}_\d{8}_[A-Z]+\.md$",
    "DECISION": r"^DECISION_\d{3}_\d{8}_[A-Z]+\.md$",
    "PROACTIVE_REPORT": r"^PROACTIVE_REPORT_\d{3}_[A-Z0-9-]+_\d{8}_[A-Z]+\.md$",
    "BLOCKING": r"^BLOCKING_\d{3}_\d{8}_[A-Z]+\.md$",
    "BLOCKING_REPLY": r"^BLOCKING_REPLY_\d{3}_\d{8}_[A-Z]+\.md$",
    "NOTICE": r"^NOTICE_\d{3}_[A-Z0-9-]+_\d{8}_(ALL|[A-Z]+)\.md$",
    "REPLY": r"^REPLY_\d{3}_[A-Z0-9-]+_\d{8}_[A-Z]+\.md$",
    "REVISION": r"^REVISION_\d{3}[A-Z]?_\d{8}_[A-Z]+\.md$",
    "REVIEW_TASK": r"^REVIEW_TASK_\d{3}\.md$",
    "TASK_TEST": r"^TASK_TEST_\d{3}_[A-Z0-9-]+_[A-Z]+\.md$",
    "TEST_REPORT": r"^TEST_REPORT_\d{3}_\d{8}_[A-Z]+\.md$",
    "TODO": r"^TODO_\d{3}_[A-Z0-9-]+_[A-Z0-9-]+\.md$",
    "LOG_ENTRY": r"^LOG_ENTRY\.md$",
}

# 模板基准文件名（使用占位符 NNN/DATE/ASSIGNEE 等）
TEMPLATE_BASE_PATTERNS = {
    "TASK": r"^TASK_NNN_[A-Z0-9-]+_[A-Z]+\.md$",
    "REPORT": r"^REPORT_NNN_DATE_[A-Z]+\.md$",
    "REVIEW_REPORT": r"^REVIEW_REPORT_NNN_DATE_[A-Z]+\.md$",
    "DECISION": r"^DECISION_NNN_DATE_[A-Z]+\.md$",
    "PROACTIVE_REPORT": r"^PROACTIVE_REPORT_NNN_[A-Z0-9-]+_DATE_[A-Z]+\.md$",
    "BLOCKING": r"^BLOCKING_NNN_DATE_[A-Z]+\.md$",
    "BLOCKING_REPLY": r"^BLOCKING_REPLY_NNN_DATE_[A-Z]+\.md$",
    "NOTICE": r"^NOTICE_NNN_[A-Z0-9-]+_DATE_(ALL|[A-Z]+)\.md$",
    "REPLY": r"^REPLY_NNN_[A-Z0-9-]+_DATE_[A-Z]+\.md$",
    "REVISION": r"^REVISION_NNN[A-Z]?_DATE_[A-Z]+\.md$",
    "REVIEW_TASK": r"^REVIEW_TASK_NNN\.md$",
    "TASK_TEST": r"^TASK_TEST_NNN_[A-Z0-9-]+_[A-Z]+\.md$",
    "TEST_REPORT": r"^TEST_REPORT_NNN_DATE_[A-Z]+\.md$",
    "TODO": r"^TODO_NNN_[A-Z0-9-]+_[A-Z0-9-]+\.md$",
    "LOG_ENTRY": r"^LOG_ENTRY\.md$",
}

# 各模板类型期望的头部字段（前 30 行内搜索）
EXPECTED_HEADERS = {
    "TASK": ["分派人", "执行人", "优先级"],
    "REPORT": ["提交人", "日期", "状态", "对应"],
    "REVIEW_REPORT": ["审查人", "日期", "对应"],
    "DECISION": ["结对", "时间"],
    "PROACTIVE_REPORT": ["提交人", "日期"],
    "BLOCKING": ["提交人", "日期", "优先级"],
    "BLOCKING_REPLY": ["回复人", "日期"],
    "NOTICE": ["发布人", "日期", "目标受众", "优先级"],
    "REPLY": ["来源报告", "处理日期", "提交人"],
    "REVISION": ["分派人", "执行人", "日期", "优先级", "对应"],
    "REVIEW_TASK": ["审查人", "被审查人", "优先级"],
    "TASK_TEST": ["分派人", "测试员", "日期", "优先级", "关联"],
    "TEST_REPORT": ["测试员", "日期", "对应", "测试类型", "总体结论"],
    "TODO": [],
    "LOG_ENTRY": [],
}


class Validator:
    def __init__(self):
        self.errors: List[Tuple[str, str]] = []
        self.warnings: List[Tuple[str, str]] = []
        self.ok: int = 0

    def classify(self, filename: str, is_template: bool = False) -> str:
        """根据文件名判断模板类型。
        
        Args:
            filename: 文件名
            is_template: 是否在 templates/ 目录中（使用占位符命名）
        """
        # 优先匹配实际命名（含数字/日期）
        for ttype, pattern in NAME_PATTERNS.items():
            if re.match(pattern, filename):
                return ttype
        # 如果是模板目录，匹配基准占位符命名
        if is_template:
            for ttype, pattern in TEMPLATE_BASE_PATTERNS.items():
                if re.match(pattern, filename):
                    return ttype
        return "UNKNOWN"

    def validate_name(self, filepath: Path, is_template: bool = False) -> str:
        """验证文件名，返回检测到的类型或 UNKNOWN。"""
        name = filepath.name
        detected = self.classify(name, is_template=is_template)
        if detected == "UNKNOWN":
            self.errors.append((str(filepath), f"文件名不符合任何命名规范: {name}"))
            return detected
        # 模板文件使用基准模式验证，实际文件使用严格模式验证
        patterns = [NAME_PATTERNS.get(detected)]
        if is_template:
            patterns.append(TEMPLATE_BASE_PATTERNS.get(detected))
        matched = False
        for pattern in patterns:
            if pattern and re.match(pattern, name):
                matched = True
                break
        if not matched:
            self.errors.append((str(filepath), f"文件名格式错误: {name}"))
            return detected
        self.ok += 1
        return detected

    def validate_content(self, filepath: Path, ttype: str) -> None:
        """验证文件内容头部字段。"""
        if ttype not in EXPECTED_HEADERS:
            return
        required = EXPECTED_HEADERS[ttype]
        if not required:
            return
        try:
            text = filepath.read_text(encoding="utf-8")
        except Exception as e:
            self.errors.append((str(filepath), f"无法读取文件: {e}"))
            return
        head = "\n".join(text.splitlines()[:40])
        missing = []
        for field in required:
            if field not in head:
                missing.append(field)
        if missing:
            self.warnings.append((str(filepath), f"缺少头部字段: {', '.join(missing)}"))

    def validate_dir(self, directory: Path) -> None:
        """验证单个目录。"""
        if not directory.exists():
            self.errors.append((str(directory), "目录不存在"))
            return
        md_files = list(directory.glob("*.md"))
        if not md_files:
            self.warnings.append((str(directory), "目录中没有 .md 文件"))
            return
        is_template = "templates" in str(directory).lower()
        for fp in sorted(md_files):
            ttype = self.validate_name(fp, is_template=is_template)
            if ttype != "UNKNOWN":
                self.validate_content(fp, ttype)

    def report(self) -> int:
        """打印报告并返回退出码。"""
        total = self.ok + len(self.errors) + len(self.warnings)
        print(f"AgentCharter Template Validator")
        print(f"=" * 50)
        print(f"检查文件总数: {total}")
        print(f"  ✅ 通过: {self.ok}")
        print(f"  ❌ 错误: {len(self.errors)}")
        print(f"  ⚠️  警告: {len(self.warnings)}")
        print()
        if self.errors:
            print("错误详情:")
            for path, msg in self.errors:
                print(f"  ❌ {path}")
                print(f"     {msg}")
            print()
        if self.warnings:
            print("警告详情:")
            for path, msg in self.warnings:
                print(f"  ⚠️  {path}")
                print(f"     {msg}")
            print()
        if not self.errors and not self.warnings:
            print("🎉 全部通过!")
        return 1 if self.errors else 0


def main() -> int:
    args = sys.argv[1:]
    dirs = [Path(p) for p in args] if args else [
        Path("collaboration/templates"),
        Path("collaboration_en/templates"),
    ]
    v = Validator()
    for d in dirs:
        v.validate_dir(d)
    return v.report()


if __name__ == "__main__":
    sys.exit(main())
