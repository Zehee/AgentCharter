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

# 🔍 PROACTIVE_REPORT_NNN: {{title}}

> **Filename**: `PROACTIVE_REPORT_NNN_DESC_DATE_author@recipient.md`
> **Location**: `outbox/`
> **Naming**: segments separated by `_`, within segments use `-`. `NNN` = sequential number, `DESC` = short English description, `DATE` = submission date `YYYYMMDD`, `AUTHOR` = author identifier (UPPERCASE)

**Author**: {{author}}
**Date**: {{DATE}}
**Linked Decisions**: {{ref_nnn}}

---

## Scope & Objective

> Describe the scope and target audience of this audit/analysis/proposal.
{{scope_and_goal}}

---

## Analysis Method (optional)

> Describe the analysis approach, reference standards, comparison targets, etc.
{{analysis_method}}

---

## Findings & Analysis

### {{module_name}} — Score: {{module_score}}/10

| # | Issue | Severity | Location | Notes |
|---|------|----------|------|------|
| {{issue_num}} | {{issue_desc}} | {{severity}} | {{location}} | {{details}} |

**Improvement suggestions**:
{{improvement_suggestions}}

---

## Priority Improvement List

### 🔴 P0 — Fix Immediately
{{p0_items}}

### 🟡 P1 — Fix Soon
{{p1_items}}

### 💡 P2 — Suggested Improvement
{{p2_items}}

---

## Summary

**Overall Score**: {{overall_score}}/10

**Strengths**:
{{strengths}}

**Areas for Improvement**:
{{improvements}}

**Recommended Actions**:
{{suggested_actions}}

---

**Author**: {{author}}
**Date**: {{DATE}}
