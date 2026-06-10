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

# DECISION_NNN: {{title}}

> **Filename**: `DECISION_NNN_DATE_AUTHOR.md`
> **Location**: `decisions/`
> **Naming**: segments separated by `_`, within segments use `-`. `NNN` = sequential number, `DATE` = decision date `YYYYMMDD`, `AUTHOR` = pair identifier (UPPERCASE)

**Pair**: {{pair}}
**Time**: {{DATE}}
**Linked Proactive Report**: {{ref_nnn}}

---

## Decision

> (One sentence: what was decided.)
{{decision}}

## Reasoning Chain

> (Original dialogue statements, verbatim. Preserve the back-and-forth reasoning between human and AI.)
{{reasoning_chain}}

## Alternatives Considered

> (Options that were considered but ultimately rejected, with rejection reasons.)
{{alternatives}}

---

## Final Artifacts (filled in by TPM or decision-maker later)

| Type | Number | Notes |
|------|------|------|
| {{artifact_type}} | {{artifact_nnn}} | {{artifact_description}} |
