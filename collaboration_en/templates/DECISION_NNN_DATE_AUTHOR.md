<!--
  File Type: Decision Record
  Author: Human-AI pair Agent (AI portion of TPM or External Agent)
  Purpose: Record significant decisions made during human-AI pair discussions, preserving reasoning chain and audit evidence
  Created: When AI detects a decision signal confirmed by human during conversation; or human explicitly says "record this decision"
  Naming: DECISION_NNN_DATE_AUTHOR.md
    - NNN: sequential number (independent of task numbers)
    - DATE: decision date YYYYMMDD
    - AUTHOR: pair identifier (UPPERCASE)
-->

# DECISION_NNN: Decision Title

> **Filename**: `DECISION_NNN_DATE_AUTHOR.md`
> **Location**: `decisions/`
> **Naming**: segments separated by `_`, within segments use `-`. `NNN`=sequential number, `DATE`=decision date `YYYYMMDD`, `AUTHOR`=pair identifier (UPPERCASE)

**Pair**: [pair identifier, e.g. @backend-pair]
**Time**: YYYY-MM-DD HH:MM
**Linked Proactive Report**: PROACTIVE_REPORT_NNN (if this decision will feed into a proactive report; optional for TPM's own decisions)

---

## Decision

(One sentence: what was decided.)

## Reasoning Chain

(Original dialogue statements, verbatim. Preserve the back-and-forth reasoning between human and AI.)

- **[Human Name]**: "original statement…"
- **[AI Name]**: "original statement…"
- ...

## Alternatives Considered

(Options that were considered but ultimately rejected, with rejection reasons.)

1. Option A → rejected because
2. Option B → rejected because

---

## Final Artifacts (filled in by TPM or decision-maker later)

| Type | Number | Notes |
|------|------|------|
| TASK / TODO | NNN | (tasks or backlog items created from this decision) |
