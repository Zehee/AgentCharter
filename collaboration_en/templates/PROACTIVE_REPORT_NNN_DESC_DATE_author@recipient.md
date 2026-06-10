<!--
  File Type: Proactive Report
  Author: Reporter (any role can double as one)
  Nature: No corresponding TASK, bypasses inbox task system
  Handling: TPM read-and-burn — read → decide → annotate → archive
  Naming: PROACTIVE_REPORT_NNN_DESC_DATE_author@recipient.md
    - NNN: sequential number (independent of task numbers)
    - DESC: short English description, within segment use `-`
    - DATE: submission date `YYYYMMDD`
    - AUTHOR: author identifier (UPPERCASE)
-->

# 🔍 PROACTIVE_REPORT_NNN: Report Title

> **Filename**: `PROACTIVE_REPORT_NNN_DESC_DATE_author@recipient.md`
> **Location**: `outbox/`
> **Naming**: segments separated by `_`, within segments use `-`. `NNN`=sequential number, `DESC`=short English description, `DATE`=submission date `YYYYMMDD`, `AUTHOR`=author identifier (UPPERCASE)

**Author**: {{author}}
**Date**: {{DATE}}
**Linked Decisions**: {{ref_nnn}}

---

## Scope & Objective

Describe the scope and target audience of this audit/analysis/proposal.

---

## Analysis Method (optional)

Describe the analysis approach, reference standards, comparison targets, etc.

---

## Findings & Analysis

### [Module/Page/Topic] — Score: X/10

| # | Issue | Severity | Location | Notes |
|---|------|----------|------|------|
| 1 | Issue description | 🔴/🟡/💡 | File:line | Details |

**Improvement suggestions**:
- Suggestion 1
- Suggestion 2

---

## Priority Improvement List

### 🔴 P0 — Fix Immediately
1. **Issue**: ... | **Suggestion**: ...

### 🟡 P1 — Fix Soon
1. **Issue**: ... | **Suggestion**: ...

### 💡 P2 — Suggested Improvement
1. **Issue**: ... | **Suggestion**: ...

---

## Summary

**Overall Score**: X/10

**Strengths**:
- ...

**Areas for Improvement**:
- ...

**Recommended Actions**:
1. ...
2. ...

---

**Author**: {{author}}
**Date**: {{DATE}}
