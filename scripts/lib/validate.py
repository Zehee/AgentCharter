"""
File content validation and cross-reference checking for AgentCharter collaboration files.

Validates:
- Required header fields exist within the first 40 lines of each .md file.
- Cross-references to TASK_NNN / REPORT_NNN / REVISION_NNN files are
  resolvable in the inbox or archive directories.
- Filename naming conventions (via the ``naming`` module).

Path resolution
---------------
``scripts/lib/validate.py`` → ``../../../collaboration/``

Pure Python stdlib, zero external dependencies.
"""

import json
import os
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# Allow running as ``python lib/validate.py ...`` from the ``scripts/`` dir.
_THIS_DIR = Path(__file__).resolve().parent  # scripts/lib
_SCRIPTS_DIR = _THIS_DIR.parent  # scripts
_PROJECT_ROOT = _SCRIPTS_DIR.parent  # AgentCharter root

# Import sibling module ``naming``
sys.path.insert(0, str(_SCRIPTS_DIR))
from lib.naming import classify, validate_name  # noqa: E402

# ---------------------------------------------------------------------------
# Expected header fields
# ---------------------------------------------------------------------------

EXPECTED_HEADERS: Dict[str, List[str]] = {
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

# ---------------------------------------------------------------------------
# Cross-reference patterns
# ---------------------------------------------------------------------------

# Regex: matches TASK_NNN, REPORT_NNN, REVISION_NNN in the content
_XREF_PATTERNS: Dict[str, str] = {
    "TASK": r"TASK_\d{3}",
    "REPORT": r"REPORT_\d{3}",
    "REVISION": r"REVISION_\d{3}",
}

# Directories to search, relative to project root
_XREF_DIRS: Dict[str, List[str]] = {
    "TASK": [
        "collaboration/inbox",
        "collaboration/archive/inbox",
    ],
    "REPORT": [
        "collaboration/inbox",
        "collaboration/archive/inbox",
    ],
    "REVISION": [
        "collaboration/inbox",
        "collaboration/archive/inbox",
    ],
}


# ---------------------------------------------------------------------------
# validate_content
# ---------------------------------------------------------------------------

def validate_content(filepath: Path, file_type: str) -> List[str]:
    """Check that all required header fields appear in the first 40 lines.

    Args:
        filepath: Path to the .md file.
        file_type: One of the ``EXPECTED_HEADERS`` keys.

    Returns:
        A list of missing field names (empty when all are present).
    """
    required = EXPECTED_HEADERS.get(file_type, [])
    if not required:
        return []

    try:
        text = filepath.read_text(encoding="utf-8")
    except Exception:
        return [f"<cannot read file>"]

    head = "\n".join(text.splitlines()[:40])
    missing = [field for field in required if field not in head]
    return missing


# ---------------------------------------------------------------------------
# validate_cross_ref
# ---------------------------------------------------------------------------

def validate_cross_ref(filepath: Path, file_type: str) -> List[str]:
    """Verify that cross-referenced files exist on disk.

    Scans the file content for references like ``TASK_042``, ``REPORT_013``,
    or ``REVISION_005``, then checks whether a file with that exact prefix
    exists in any of the configured inbox / archive directories.

    Args:
        filepath: Path to the .md file.
        file_type: Ignored (all cross-ref types are always checked).

    Returns:
        A list of missing reference descriptions (e.g. ``TASK_042``).
    """
    try:
        text = filepath.read_text(encoding="utf-8")
    except Exception:
        return [f"<cannot read {filepath.name}>"]

    missing: List[str] = []

    for ref_type, pattern in _XREF_PATTERNS.items():
        for match in re.finditer(pattern, text):
            ref_name = match.group()
            # Build candidate filenames: TASK_042.md, TASK_042_*.md, etc.
            candidates = _candidate_filenames(ref_name)
            if not _any_exists(candidates, _XREF_DIRS[ref_type]):
                missing.append(ref_name)

    return missing


def _candidate_filenames(ref_name: str) -> List[str]:
    """Return possible filenames for a cross-reference."""
    # e.g. TASK_042 → TASK_042.md, TASK_042_*.md  (but we check prefix)
    return [ref_name]


def _any_exists(ref_names: List[str], search_dirs: List[str]) -> bool:
    """Return True if *any* filename matching a ref prefix exists in *search_dirs*."""
    for rel_dir in search_dirs:
        search_path = _PROJECT_ROOT / rel_dir
        if not search_path.is_dir():
            continue
        for fpath in search_path.iterdir():
            if not fpath.is_file():
                continue
            name = fpath.stem  # filename without .md
            # Check if the reference (e.g. TASK_042) is a prefix of the filename
            for ref in ref_names:
                if name.startswith(ref):
                    return True
    return False


# ---------------------------------------------------------------------------
# validate_all / validate_file
# ---------------------------------------------------------------------------

ValidationResult = Dict[str, object]


def validate_all(directory: Path) -> List[ValidationResult]:
    """Scan all ``.md`` files in *directory* and validate each one.

    For every file:
    1. Validate the filename via ``naming.validate_name``.
    2. If the type is recognised, run ``validate_content`` and
       ``validate_cross_ref``.

    Args:
        directory: A pathlib.Path pointing to a directory of .md files.

    Returns:
        A list of per-file result dicts.
    """
    results: List[ValidationResult] = []

    if not directory.is_dir():
        return [{"filepath": str(directory), "error": "Directory not found"}]

    md_files = sorted(directory.glob("*.md"))
    if not md_files:
        return [{"filepath": str(directory), "warning": "No .md files found"}]

    for fp in md_files:
        results.append(validate_file(fp))

    return results


def validate_file(filepath: Path) -> ValidationResult:
    """Validate a single file: name, content headers, and cross-references.

    Args:
        filepath: Path to the .md file.

    Returns:
        A dict with keys: ``filepath``, ``file_type``, ``name_valid``,
        ``name_error``, ``missing_headers``, ``missing_refs``.
    """
    result: ValidationResult = {
        "filepath": str(filepath),
        "file_type": "UNKNOWN",
        "name_valid": False,
        "name_error": "",
        "missing_headers": [],
        "missing_refs": [],
    }

    name = filepath.name
    is_template = "templates" in str(filepath).lower()

    name_valid, detected, name_err = validate_name(name, is_template=is_template)
    result["file_type"] = detected
    result["name_valid"] = name_valid
    result["name_error"] = name_err

    if detected != "UNKNOWN":
        result["missing_headers"] = validate_content(filepath, detected)
        result["missing_refs"] = validate_cross_ref(filepath, detected)

    return result


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> int:
    """Entry point for ``python lib/validate.py PATH``.

    - If *PATH* is a single file, validate it and print JSON.
    - If *PATH* is a directory, validate all ``.md`` files inside and print JSON.
    """
    if len(sys.argv) < 2:
        print("Usage: python lib/validate.py <file.md | directory>", file=sys.stderr)
        return 1

    target = Path(sys.argv[1])

    if target.is_file():
        results = [validate_file(target)]
    elif target.is_dir():
        results = validate_all(target)
    else:
        print(f"Error: {target} is neither a file nor a directory", file=sys.stderr)
        return 1

    # Summary
    total = len(results)
    passed = sum(1 for r in results if r["name_valid"] and not r["missing_headers"] and not r["missing_refs"])
    errors = total - passed

    output = {
        "summary": {"total": total, "passed": passed, "failed": errors},
        "files": results,
    }

    json.dump(output, sys.stdout, ensure_ascii=False, indent=2)
    print()

    return 0 if errors == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
