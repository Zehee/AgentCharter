"""
Filename generation and naming validation for AgentCharter collaboration files.

Handles the ``_author@recipient`` naming convention for all defined file types.
Pure Python stdlib only — zero external dependencies.
"""

import re
from datetime import date as _date
from typing import Optional, Tuple

# ---------------------------------------------------------------------------
# Regex patterns — actual files (real numbers, dates, uppercase identifiers)
# ---------------------------------------------------------------------------
NAME_PATTERNS: dict[str, str] = {
    "TASK": r"^TASK_\d{3}_[A-Z0-9-]+_[A-Z]+@[A-Z]+\.md$",
    "REPORT": r"^REPORT_\d{3}(_R\d+)?_\d{8}_[A-Z]+@[A-Z]+\.md$",
    "REVIEW_REPORT": r"^REVIEW_REPORT_\d{3}(_R\d+)?_\d{8}_[A-Z]+@[A-Z]+\.md$",
    "DECISION": r"^DECISION_\d{3}_\d{8}_[A-Z]+\.md$",
    "PROACTIVE_REPORT": r"^PROACTIVE_REPORT_\d{3}_[A-Z0-9-]+_\d{8}_[A-Z]+@[A-Z]+\.md$",
    "BLOCKING": r"^BLOCKING_\d{3}_\d{8}_[A-Z]+@[A-Z]+\.md$",
    "BLOCKING_REPLY": r"^BLOCKING_REPLY_\d{3}_\d{8}_[A-Z]+@[A-Z]+\.md$",
    "NOTICE": r"^NOTICE_\d{3}_[A-Z0-9-]+_\d{8}_[A-Z]+@[A-Z]+\.md$",
    "REPLY": r"^REPLY_\d{3}_[A-Z0-9-]+_\d{8}_[A-Z]+@[A-Z]+\.md$",
    "REVISION": r"^REVISION_\d{3}[A-Z]?(_R\d+)?_\d{8}_[A-Z]+@[A-Z]+\.md$",
    "REVIEW_TASK": r"^REVIEW_TASK_\d{3}_[A-Z]+@[A-Z]+\.md$",
    "TASK_TEST": r"^TASK_TEST_\d{3}_[A-Z0-9-]+_[A-Z]+@[A-Z]+\.md$",
    "TEST_REPORT": r"^TEST_REPORT_\d{3}_\d{8}_[A-Z]+@[A-Z]+\.md$",
    "TODO": r"^TODO_\d{3}_[A-Z0-9-]+_[A-Z0-9-]+\.md$",
    "LOG_ENTRY": r"^LOG_ENTRY\.md$",
}

# ---------------------------------------------------------------------------
# Template base patterns — use placeholders NNN, DATE, lower-case identifiers
# ---------------------------------------------------------------------------
TEMPLATE_BASE_PATTERNS: dict[str, str] = {
    "TASK": r"^TASK_NNN_[A-Z0-9-]+_[a-z]+@[a-z]+\.md$",
    "REPORT": r"^REPORT_NNN(_R[0-9]+)?_DATE_[a-z]+@[a-z]+\.md$",
    "REVIEW_REPORT": r"^REVIEW_REPORT_NNN(_R[0-9]+)?_DATE_[a-z]+@[a-z]+\.md$",
    "DECISION": r"^DECISION_NNN_DATE_[A-Z]+\.md$",
    "PROACTIVE_REPORT": r"^PROACTIVE_REPORT_NNN_[A-Z0-9-]+_DATE_[a-z]+@[a-z]+\.md$",
    "BLOCKING": r"^BLOCKING_NNN_DATE_[a-z]+@[a-z]+\.md$",
    "BLOCKING_REPLY": r"^BLOCKING_REPLY_NNN_DATE_[a-z]+@[a-z]+\.md$",
    "NOTICE": r"^NOTICE_NNN_[A-Z0-9-]+_DATE_[a-z]+@[a-z]+\.md$",
    "REPLY": r"^REPLY_NNN_[A-Z0-9-]+_DATE_[a-z]+@[a-z]+\.md$",
    "REVISION": r"^REVISION_NNN[A-Z]?(_R[0-9]+)?_DATE_[a-z]+@[a-z]+\.md$",
    "REVIEW_TASK": r"^REVIEW_TASK_NNN_[a-z]+@[a-z]+\.md$",
    "TASK_TEST": r"^TASK_TEST_NNN_[A-Z0-9-]+_[a-z]+@[a-z]+\.md$",
    "TEST_REPORT": r"^TEST_REPORT_NNN_DATE_[a-z]+@[a-z]+\.md$",
    "TODO": r"^TODO_NNN_[A-Z0-9-]+_[A-Z0-9-]+\.md$",
    "LOG_ENTRY": r"^LOG_ENTRY\.md$",
}

# ---------------------------------------------------------------------------
# Public helpers
# ---------------------------------------------------------------------------

ALL_TYPES: tuple[str, ...] = tuple(NAME_PATTERNS.keys())

# Types whose filename includes a free-text description segment
_TYPES_WITH_DESC = frozenset({"TASK", "PROACTIVE_REPORT", "NOTICE", "REPLY", "TODO"})


def get_type_pattern(file_type: str, is_template: bool = False) -> Optional[str]:
    """Return the regex pattern string for *file_type*.

    When *is_template* is ``True`` the template-base pattern is returned;
    otherwise the real-filename pattern is returned.  Returns ``None`` when
    *file_type* is unknown.
    """
    if is_template:
        return TEMPLATE_BASE_PATTERNS.get(file_type)
    return NAME_PATTERNS.get(file_type)


def generate_filename(
    file_type: str,
    author: str,
    recipient: str,
    nnn: Optional[str] = None,
    date: Optional[str] = None,
    desc: Optional[str] = None,
    round: Optional[int] = None,
) -> str:
    """Auto-generate a compliant filename for the given *file_type*.

    Parameters
    ----------
    file_type:
        One of the ``ALL_TYPES`` constants (e.g. ``"REPORT"``).
    author:
        Author identifier (uppercase, e.g. ``"KIMI"``).
    recipient:
        Recipient identifier (uppercase, e.g. ``"TPM"``).  Ignored for types
        that do not carry a ``@recipient`` suffix.
    nnn:
        Three-digit numeric sequence (or ``"NNN"`` placeholder).  When
        *None* it defaults to ``"NNN"``.
    date:
        Date in ``YYYYMMDD`` format.  When *None* today's date is used.
    desc:
        Description / short-name segment.  Only required (and used) for
        types that embed a free-text description: ``TASK``,
        ``PROACTIVE_REPORT``, ``NOTICE``, ``REPLY``, ``TODO``.

    round:
        Round number for multi-round review (e.g. ``1`` → ``_R1``).
        Only applicable to ``REPORT``, ``REVIEW_REPORT``, ``REVISION``.

    Returns
    -------
    str
        A fully-formed filename such as ``REPORT_042_20260610_KIMI@TPM.md``
        or ``REPORT_042_R1_20260610_KIMI@TPM.md``.
    """
    if file_type not in NAME_PATTERNS:
        raise ValueError(f"Unknown file type: {file_type!r}")

    nnn = nnn if nnn is not None else "NNN"
    date = date if date is not None else _date.today().strftime("%Y%m%d")

    # Normalise identifiers: uppercase, strip whitespace
    author = author.strip().upper()
    recipient = recipient.strip().upper()

    # Dispatch per type  —  each branch mirrors the corresponding regex.
    if file_type == "TASK":
        # TASK_NNN_DESC_AUTHOR@RECIPIENT.md
        _require_desc(desc, file_type)
        return f"TASK_{nnn}_{desc}_{author}@{recipient}.md"

    round_suffix = f"_R{round}" if round else ""

    if file_type == "REPORT":
        return f"REPORT_{nnn}{round_suffix}_{date}_{author}@{recipient}.md"

    if file_type == "REVIEW_REPORT":
        return f"REVIEW_REPORT_{nnn}{round_suffix}_{date}_{author}@{recipient}.md"

    if file_type == "DECISION":
        # No @recipient
        return f"DECISION_{nnn}_{date}_{author}.md"

    if file_type == "PROACTIVE_REPORT":
        _require_desc(desc, file_type)
        return f"PROACTIVE_REPORT_{nnn}_{desc}_{date}_{author}@{recipient}.md"

    if file_type == "BLOCKING":
        return f"BLOCKING_{nnn}_{date}_{author}@{recipient}.md"

    if file_type == "BLOCKING_REPLY":
        return f"BLOCKING_REPLY_{nnn}_{date}_{author}@{recipient}.md"

    if file_type == "NOTICE":
        _require_desc(desc, file_type)
        return f"NOTICE_{nnn}_{desc}_{date}_{author}@{recipient}.md"

    if file_type == "REPLY":
        _require_desc(desc, file_type)
        return f"REPLY_{nnn}_{desc}_{date}_{author}@{recipient}.md"

    if file_type == "REVISION":
        return f"REVISION_{nnn}{round_suffix}_{date}_{author}@{recipient}.md"

    if file_type == "REVIEW_TASK":
        return f"REVIEW_TASK_{nnn}_{author}@{recipient}.md"

    if file_type == "TASK_TEST":
        _require_desc(desc, file_type)
        return f"TASK_TEST_{nnn}_{desc}_{author}@{recipient}.md"

    if file_type == "TEST_REPORT":
        return f"TEST_REPORT_{nnn}_{date}_{author}@{recipient}.md"

    if file_type == "TODO":
        _require_desc(desc, file_type)
        # TODO has no @recipient; desc is the second segment
        return f"TODO_{nnn}_{desc}.md"

    if file_type == "LOG_ENTRY":
        return "LOG_ENTRY.md"

    # Should never reach here because of the early check above.
    raise ValueError(f"Unknown file type: {file_type!r}")


def _require_desc(desc: Optional[str], file_type: str) -> None:
    if not desc:
        raise ValueError(
            f"A description segment is required for file type {file_type!r}"
        )


# ---------------------------------------------------------------------------
# Classification & validation
# ---------------------------------------------------------------------------

def classify(filename: str, is_template: bool = False) -> str:
    """Detect the file type from *filename*.

    Tries the real-filename patterns first; when *is_template* is ``True``
    and no real pattern matched, the template-placeholder patterns are
    attempted.  Returns the type string (e.g. ``"REPORT"``) or
    ``"UNKNOWN"``.
    """
    # Real filenames first
    for ttype, pattern in NAME_PATTERNS.items():
        if re.match(pattern, filename, re.IGNORECASE):
            return ttype
    # Template names (placeholders)
    if is_template:
        for ttype, pattern in TEMPLATE_BASE_PATTERNS.items():
            if re.match(pattern, filename, re.IGNORECASE):
                return ttype
    return "UNKNOWN"


def validate_name(
    filename: str, is_template: bool = False
) -> Tuple[bool, str, str]:
    """Validate a filename against the naming conventions.

    Returns
    -------
    (is_valid, detected_type, error_message)
        *is_valid* is ``True`` when the name matched any recognised pattern.
        *detected_type* is the matched type or ``"UNKNOWN"``.
        *error_message* is empty when valid, otherwise a human-readable
        description of why the name was rejected.
    """
    detected = classify(filename, is_template=is_template)

    if detected == "UNKNOWN":
        return False, "UNKNOWN", f"Filename does not match any known pattern: {filename!r}"

    # Verify it matches the appropriate pattern(s) for that type
    patterns_to_check = [NAME_PATTERNS.get(detected)]
    if is_template:
        patterns_to_check.append(TEMPLATE_BASE_PATTERNS.get(detected))

    for pat in patterns_to_check:
        if pat and re.match(pat, filename, re.IGNORECASE):
            return True, detected, ""

    return False, detected, f"Filename {filename!r} partially matches type {detected!r} but fails the exact pattern"


# ---------------------------------------------------------------------------
# Convenience: compiled lookup (optional pre-compilation for repeated use)
# ---------------------------------------------------------------------------
_COMPILED_NAME: dict[str, re.Pattern] = {}
_COMPILED_TEMPLATE: dict[str, re.Pattern] = {}


def _get_compiled(file_type: str, is_template: bool = False) -> Optional[re.Pattern]:
    """Return a cached compiled regex for *file_type*."""
    cache = _COMPILED_TEMPLATE if is_template else _COMPILED_NAME
    if file_type not in cache:
        raw = get_type_pattern(file_type, is_template=is_template)
        if raw is None:
            return None
        cache[file_type] = re.compile(raw)
    return cache[file_type]
