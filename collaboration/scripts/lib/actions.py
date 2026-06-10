"""
actions.py — Read ACTIONS.md to validate agent identity, determine roles,
and check file flow compliance.

All paths are relative to the project root (parent of ``scripts/``).
The ``collaboration/`` directory is at ``../collaboration/`` relative to
``scripts/``.

CLI usage::

    python lib/actions.py KIMI          → validate agent, print JSON
    python lib/actions.py KIMI REPORT   → validate flow for REPORT
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

# ── Path resolution ──────────────────────────────────────────────────────────
# scripts/lib/actions.py  →  scripts/  →  project root (parent of scripts/)
_SCRIPT_DIR = Path(__file__).resolve().parent          # scripts/lib/
_SCRIPTS_DIR = _SCRIPT_DIR.parent                      # scripts/
_PROJECT_ROOT = _SCRIPTS_DIR.parent                    # project root
_ACTIONS_PATH = _PROJECT_ROOT / "collaboration" / "ACTIONS.md"

# ── Regex helpers ────────────────────────────────────────────────────────────
_RE_TABLE_ROW = re.compile(
    r"^\|\s*(.*?)\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|$"
)
_RE_DIRECTION = re.compile(
    r"(\S[^→↔]*(?:\s*\S))\s*([→↔])\s*(\S[^→↔]*(?:\s*\S))"
)

# ── Internal helpers ─────────────────────────────────────────────────────────


def _strip_backticks(value: str) -> str:
    """Remove surrounding backticks from a Markdown inline-code value."""
    return value.strip("`").strip()


def _find_section(lines, heading_exact):
    """Return the line index of the first heading that matches *heading_exact*
    (e.g. ``"## 协作链路"``), or ``-1``."""
    for i, line in enumerate(lines):
        if line.rstrip() == heading_exact:
            return i
    return -1


def _parse_table_after_line(lines, start, header_keywords):
    """Starting at *start*, find the first table whose header contains all
    *header_keywords* and return a list of row dicts.

    Skips the separator row (|---|---|---|). Stops at the next heading
    (``##``) or end of file.  Table cells have backticks stripped.
    """
    i = start
    while i < len(lines):
        line = lines[i]
        # Detect a table header by looking for a line starting with "|"
        # whose next line is a separator row.
        if (
            line.lstrip().startswith("|")
            and i + 1 < len(lines)
            and re.match(r"^\|[\s\-:]+\|", lines[i + 1])
        ):
            header = line.strip()
            # Check if all keywords appear in the header
            if all(kw in header for kw in header_keywords):
                # Parse header cells
                header_match = _RE_TABLE_ROW.match(header)
                if not header_match:
                    i += 1
                    continue
                header_cells = [
                    _strip_backticks(c.strip())
                    for c in header_match.groups()
                ]
                rows = []
                i += 2  # skip separator
                while i < len(lines):
                    row_line = lines[i].strip()
                    if not row_line.startswith("|"):
                        break
                    # Stop at next heading
                    if row_line.startswith("##"):
                        break
                    m = _RE_TABLE_ROW.match(row_line)
                    if m:
                        cells = [
                            _strip_backticks(c.strip())
                            for c in m.groups()
                        ]
                        # Skip empty rows (all cells empty)
                        if any(c for c in cells):
                            row = dict(zip(header_cells, cells))
                            rows.append(row)
                    i += 1
                return rows
        i += 1
    return []


def _parse_channel_types(lines):
    """Parse the 通道类型 table (the first table with columns 通道/用途/方向)."""
    return _parse_table_after_line(lines, 0, ["通道", "用途", "方向"])


def _parse_collaboration_links(lines):
    """Parse the 协作链路 table — the table under ``## 协作链路`` heading."""
    idx = _find_section(lines, "## 协作链路")
    if idx < 0:
        return []
    return _parse_table_after_line(lines, idx, ["动作", "发起方", "接收方", "通道"])


def _parse_direction_parts(direction: str):
    """Parse a direction string like ``"TPM → 执行者"`` or ``"TPM ↔ Sub-Agent"``
    and return ``(from_role, arrow, to_role)`` or ``None``.

    Arrow can be → (one-way) or ↔ (bidirectional).
    """
    m = _RE_DIRECTION.match(direction)
    if m:
        return m.group(1).strip(), m.group(2), m.group(3).strip()
    return None


def _load_data():
    """Read and parse ``ACTIONS.md``, returning cached data dict.

    Returns::

        {
            "channels": [
                {"channel": "inbox/TASK", "用途": "任务分派", "方向": "TPM → 执行者"},
                ...
            ],
            "links": [
                {"动作": "分配任务", "发起方 → 接收方": "TPM → Alice", "通道": "inbox/TASK"},
                ...
            ],
            "agents": {"Alice", "Bob", "Charlie", "TPM"},
            "channel_map": {"TASK": ..., "REPORT": ..., ...},
        }
    """
    if not _ACTIONS_PATH.is_file():
        return {"channels": [], "links": [], "agents": set(), "channel_map": {}}

    text = _ACTIONS_PATH.read_text(encoding="utf-8")
    lines = text.splitlines()

    # ── Parse 通道类型 table ────────────────────────────────────────────────
    channels = _parse_channel_types(lines)

    # ── Parse 协作链路 table ────────────────────────────────────────────────
    links = _parse_collaboration_links(lines)

    # ── Build agent set from 协作链路 ───────────────────────────────────────
    agents: set[str] = set()
    for link in links:
        direction_col = link.get("发起方 → 接收方", "")
        parts = _parse_direction_parts(direction_col)
        if parts:
            from_role, _arrow, to_role = parts
            agents.add(from_role)
            agents.add(to_role)

    # ── Also collect roles from 通道类型 direction column ───────────────────
    for ch in channels:
        direction = ch.get("方向", "")
        parts = _parse_direction_parts(direction)
        if parts:
            from_role, arrow, to_role = parts
            agents.add(from_role)
            agents.add(to_role)
            if arrow == "↔":
                # Bidirectional — both sides are equivalent
                pass

    # ── Build channel map: file type (short) → channel info ─────────────────
    channel_map: dict[str, dict] = {}
    for ch in channels:
        chan = ch.get("channel", ch.get("通道", ""))
        # Extract the short name after the last /
        short = chan.rsplit("/", 1)[-1] if "/" in chan else chan
        channel_map[short] = ch

    return {
        "channels": channels,
        "links": links,
        "agents": agents,
        "channel_map": channel_map,
    }


def _agent_role(name: str, data: dict) -> str:
    """Determine the role of *name* by inspecting how they appear in the
    协作链路 and 通道类型 tables.

    Roles are derived from the 方向 column patterns in 通道类型:
    e.g. ``"TPM → 执行者"`` → roles are ``TPM`` and ``执行者``.
    """
    # If name appears as a role in the 方向 column, return it directly
    for ch in data["channels"]:
        direction = ch.get("方向", "")
        parts = _parse_direction_parts(direction)
        if parts:
            from_role, arrow, to_role = parts
            if name == from_role or name == to_role:
                return name  # e.g. "TPM", "执行者", "Reviewer"

    # Otherwise, look up specific agents in the 协作链路 table and infer
    # their role from the channels they use.
    if not data["links"]:
        # Fallback: if name is in the agents set, call it "External Agent"
        if name in data["agents"]:
            return "External Agent"
        return "Unknown"

    # Collect all channels this agent sends/receives on
    sends_to: dict[str, list[str]] = {}  # channel → [targets]
    receives_from: dict[str, list[str]] = {}

    for link in data["links"]:
        direction_col = link.get("发起方 → 接收方", "")
        channel = link.get("通道", "")
        parts = _parse_direction_parts(direction_col)
        if not parts:
            continue
        from_agent, _arrow, to_agent = parts
        if from_agent == name:
            sends_to.setdefault(channel, []).append(to_agent)
        if to_agent == name:
            receives_from.setdefault(channel, []).append(from_agent)

    # Map channels to roles using the 通道类型 table
    for ch in data["channels"]:
        chan_name = ch.get("channel", ch.get("通道", ""))
        direction = ch.get("方向", "")
        parts = _parse_direction_parts(direction)
        if not parts:
            continue
        from_role, arrow, to_role = parts

        # If name receives on this channel, name is the target role
        if chan_name in receives_from:
            return to_role
        # If name sends on this channel, name is the source role
        if chan_name in sends_to:
            return from_role

    # Fallback
    if name in data["agents"]:
        return "External Agent"
    return "Unknown"


def _allowed_commands_for_role(role: str, data: dict) -> list[str]:
    """Return a list of allowed commands for a given role, based on the
    通道类型 table."""
    commands = []
    for ch in data["channels"]:
        direction = ch.get("方向", "")
        parts = _parse_direction_parts(direction)
        if not parts:
            continue
        from_role, arrow, to_role = parts
        chan = ch.get("channel", ch.get("通道", ""))
        short = chan.rsplit("/", 1)[-1] if "/" in chan else chan

        if arrow == "↔":
            # Bidirectional — both roles can do this
            if role == from_role or role == to_role:
                commands.append(short)
        else:
            if role == from_role:
                commands.append(f"send:{short}")
            if role == to_role:
                commands.append(f"receive:{short}")
    return commands


# ── Public API ───────────────────────────────────────────────────────────────


def validate_agent(name: str):
    """Check if *name* appears as a recognised agent or role in ACTIONS.md.

    Returns the name (string) if found, or ``None``.
    """
    data = _load_data()
    if name in data["agents"]:
        return name
    return None


def get_role(name: str) -> dict:
    """Return a dict describing the role of *name*::

        {"name": "Alice", "role": "执行者", "allowed_commands": ["send:REPORT", "receive:TASK"]}
    """
    data = _load_data()
    role = _agent_role(name, data)
    cmds = _allowed_commands_for_role(role, data)
    return {
        "name": name,
        "role": role,
        "allowed_commands": cmds,
    }


def validate_flow(file_type: str, from_agent: str, to_agent: str):
    """Check whether a flow of *file_type* from *from_agent* to *to_agent*
    is permitted according to the 通道类型 table.

    Returns ``(True, reason)`` or ``(False, reason)``.
    """
    data = _load_data()
    ch = data["channel_map"].get(file_type)
    if ch is None:
        return False, f"Unknown file type: {file_type!r}"

    direction = ch.get("方向", "")
    parts = _parse_direction_parts(direction)
    if not parts:
        return False, f"Could not parse direction: {direction!r}"

    from_role, arrow, to_role = parts
    from_r = _agent_role(from_agent, data)
    to_r = _agent_role(to_agent, data)

    channel_name = ch.get("channel", ch.get("通道", ""))

    if arrow == "↔":
        # Bidirectional: both roles can send to each other
        if {from_r, to_r} == {from_role, to_role}:
            return (
                True,
                f"{from_agent}({from_r}) → {to_agent}({to_r}) via {channel_name} [bidirectional]",
            )
        return (
            False,
            f"Flow {from_agent}({from_r}) → {to_agent}({to_r}) not allowed for {channel_name} "
            f"(requires {from_role} ↔ {to_role})",
        )
    else:
        # One-way: from_role → to_role
        if from_r == from_role and to_r == to_role:
            return (
                True,
                f"{from_agent}({from_r}) → {to_agent}({to_r}) via {channel_name}",
            )
        return (
            False,
            f"Flow {from_agent}({from_r}) → {to_agent}({to_r}) not allowed for {channel_name} "
            f"(requires {from_role} → {to_role})",
        )


def get_flow_rule(file_type: str) -> dict | None:
    """Return the flow rule for *file_type*::

        {"channel": "inbox/TASK", "direction": "TPM → 执行者"}

    Returns ``None`` if the file type is unknown.
    """
    data = _load_data()
    ch = data["channel_map"].get(file_type)
    if ch is None:
        return None
    return {
        "channel": ch.get("channel", ch.get("通道", "")),
        "direction": ch.get("方向", ""),
    }


def get_allowed_writers(file_type: str) -> list[str]:
    """Return a list of roles that can write (send) a file of *file_type*.

    Determined from the 通道类型 table — the sending side of the direction.
    """
    data = _load_data()
    ch = data["channel_map"].get(file_type)
    if ch is None:
        return []

    direction = ch.get("方向", "")
    parts = _parse_direction_parts(direction)
    if not parts:
        return []

    from_role, arrow, to_role = parts
    if arrow == "↔":
        return [from_role, to_role]
    return [from_role]


def is_tpm(name: str) -> bool:
    """Quick check whether *name* is the TPM."""
    data = _load_data()
    # Check if name appears as a role "TPM" in the direction column
    for ch in data["channels"]:
        direction = ch.get("方向", "")
        parts = _parse_direction_parts(direction)
        if parts:
            from_role, _arrow, _to_role = parts
            if from_role == name and from_role == "TPM":
                return True
    # Check if name appears as "TPM" in the 协作链路 table
    for link in data["links"]:
        direction_col = link.get("发起方 → 接收方", "")
        parts = _parse_direction_parts(direction_col)
        if parts:
            from_agent, _arrow, _to_agent = parts
            if from_agent == name and name == "TPM":
                return True
    return name == "TPM"


# ── CLI ──────────────────────────────────────────────────────────────────────


def main():
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"):
        print("Usage:", file=sys.stderr)
        print("  python lib/actions.py AGENT_NAME", file=sys.stderr)
        print("  python lib/actions.py AGENT_NAME FILE_TYPE", file=sys.stderr)
        sys.exit(1)

    name = sys.argv[1]

    if len(sys.argv) >= 3:
        # Validate flow
        file_type = sys.argv[2]
        # Try to determine from/to agents from the 协作链路 table
        data = _load_data()
        ch = data["channel_map"].get(file_type)
        if ch is None:
            result = {"valid": False, "reason": f"Unknown file type: {file_type!r}"}
        else:
            direction = ch.get("方向", "")
            parts = _parse_direction_parts(direction)
            if not parts:
                result = {"valid": False, "reason": f"Could not parse direction: {direction!r}"}
            else:
                from_role, arrow, to_role = parts
                from_r = _agent_role(name, data)
                result = {
                    "valid": from_r == from_role,
                    "agent": name,
                    "agent_role": from_r,
                    "file_type": file_type,
                    "channel": ch.get("channel", ch.get("通道", "")),
                    "expected_direction": direction,
                    "reason": (
                        f"{name} role is {from_r}, expected {from_role} → {to_role}"
                        if from_r != from_role
                        else f"{name}({from_r}) can send {file_type} via {direction}"
                    ),
                }
        json.dump(result, sys.stdout, ensure_ascii=False, indent=2)
        sys.stdout.write("\n")
    else:
        # Validate agent
        info = get_role(name)
        valid = validate_agent(name) is not None
        result = {
            "valid": valid,
            **info,
        }
        json.dump(result, sys.stdout, ensure_ascii=False, indent=2)
        sys.stdout.write("\n")


if __name__ == "__main__":
    main()
