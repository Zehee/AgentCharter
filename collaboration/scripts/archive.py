#!/usr/bin/env python3
"""archive.py — 链式归档（TPM 独占）

用法:
    python archive.py <filepath>           → 单文件归档
    python archive.py --chain <filepath>   → 链式归档（关联文件一并归档）

归档规则：
- 文件移入 archive/ 下对应子目录（inbox/ outbox/ decisions/）
- 在原位置保留一个软链接？不，直接移动，追加归档标记
- 在文件末尾追加 `> ✅ 已归档 YYYY-MM-DD` 标记
"""

import json
import re
import sys
from pathlib import Path

# Fix Windows GBK encoding issue
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

SCRIPT_DIR = Path(__file__).resolve().parent
COLLAB_DIR = SCRIPT_DIR.parent
sys.path.insert(0, str(SCRIPT_DIR / "lib"))

from naming import classify  # noqa: E402
from redlines import get_redlines_string  # noqa: E402


# 文件类型 → 活跃目录 → 归档目录
DIR_MAP = {
    "inbox": "archive/inbox",
    "outbox": "archive/outbox",
    "decisions": "archive/decisions",
    "todos": "archive/todos",
}


def _get_archive_dir(file_path: Path) -> Path | None:
    """根据文件当前位置确定归档目标目录。"""
    parent = file_path.parent.name
    archive_rel = DIR_MAP.get(parent)
    if archive_rel:
        return COLLAB_DIR / archive_rel
    return None


def archive_single(file_path: Path) -> dict:
    """归档单个文件。返回结果字典。"""
    if not file_path.exists():
        return {"error": f"文件不存在: {file_path}"}

    archive_dir = _get_archive_dir(file_path)
    if not archive_dir:
        return {"error": f"无法确定归档目录: {file_path.parent.name}"}

    target = archive_dir / file_path.name

    try:
        archive_dir.mkdir(parents=True, exist_ok=True)

        # 归档前后路径（rename 前计算）
        try:
            from_path = str(file_path.relative_to(COLLAB_DIR))
        except ValueError:
            from_path = str(file_path)
        try:
            to_path = str(target.relative_to(COLLAB_DIR))
        except ValueError:
            to_path = str(target)

        # 追加归档标记
        text = file_path.read_text(encoding="utf-8")
        from datetime import date
        archive_mark = f"\n\n> ✅ 已归档 {date.today().isoformat()}\n"
        if archive_mark.strip() not in text:
            text += archive_mark
            file_path.write_text(text, encoding="utf-8")

        # 移动文件
        file_path.rename(target)

        return {
            "result": "✅ 已归档",
            "from": from_path,
            "to": to_path,
        }
    except Exception as e:
        return {"error": f"归档失败: {e}"}


def _find_linked_files(file_path: Path, file_type: str) -> list[Path]:
    """查找与给定文件关联的其他文件（最小实现）。"""
    linked = []
    text = file_path.read_text(encoding="utf-8", errors="ignore")

    # 简单扫描：查找 TASK_NNN / REPORT_NNN / REVISION_NNN / REVIEW_REPORT_NNN 引用
    refs = re.findall(r"(TASK|REPORT|REVISION|REVIEW_REPORT|DECISION)_\d{3}[A-Z]?", text)
    seen = set()
    for ref in refs:
        if ref in seen:
            continue
        seen.add(ref)
        # 在各活跃目录中搜索匹配的文件
        for d in ["inbox", "outbox", "decisions"]:
            search_dir = COLLAB_DIR / d
            if not search_dir.exists():
                continue
            for f in search_dir.iterdir():
                if f.is_file() and f.suffix == ".md" and ref in f.name:
                    linked.append(f)
    return linked


def archive_chain(file_path: Path) -> dict:
    """链式归档：归档目标文件及其关联文件。"""
    if not file_path.exists():
        return {"error": f"文件不存在: {file_path}"}

    file_type = classify(file_path.name)
    results = []

    # 先归档主文件
    main_result = archive_single(file_path)
    if "error" in main_result:
        return main_result
    results.append(main_result)

    # 查找关联文件
    linked = _find_linked_files(file_path, file_type)
    for linked_file in linked:
        if linked_file.exists():
            r = archive_single(linked_file)
            results.append(r)

    return {
        "result": "✅ 链式归档完成",
        "archived_count": len(results),
        "details": results,
    }


def main():
    args = sys.argv[1:]
    if not args:
        print(json.dumps({
            "usage": "python archive.py <filepath> [--chain]",
            "example": "python archive.py inbox/TASK_042_ADD-LOGIN_TPM@KIMI.md",
            "note": "TPM 独占命令",
            "redlines": get_redlines_string(),
        }, ensure_ascii=False, indent=2))
        sys.exit(1)

    chain_mode = "--chain" in args
    file_args = [a for a in args if not a.startswith("--")]

    if not file_args:
        print(json.dumps({"error": "缺少文件路径"}, ensure_ascii=False))
        sys.exit(1)

    file_path = Path(file_args[0])
    if not file_path.exists():
        alt = COLLAB_DIR / file_path
        if alt.exists():
            file_path = alt
        else:
            print(json.dumps({"error": f"文件不存在: {file_path}（尝试 {alt} 也未找到）"}, ensure_ascii=False))
            sys.exit(1)

    if chain_mode:
        result = archive_chain(file_path)
    else:
        result = archive_single(file_path)

    result["redlines"] = get_redlines_string()
    print(json.dumps(result, ensure_ascii=False, indent=2))
    sys.exit(0 if "error" not in result else 1)


if __name__ == "__main__":
    main()
