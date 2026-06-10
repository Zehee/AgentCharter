# REPORT_NNN: {{title}}

> **Filename**: `REPORT_NNN_DATE_author@recipient.md`
> **Location**: `outbox/`
> **Naming**: segments separated by `_`, within segments use `-`. `NNN` = task number, `DATE` = submission date `YYYYMMDD`, `AUTHOR` = author identifier (UPPERCASE), `TPM` = receiving TPM identifier (UPPERCASE)

**Author**: {{author}}
**Date**: {{DATE}}
**Status**: {{status}}
**Corresponding**: {{ref_nnn}}
**Report Type**: {{report_type}}

---

<!--
## [Review Summary] (uncomment for multi-round fixes)
Copy all historical text from REVIEW_REPORT's [Summary] section here,
append your fix response below each round. Not needed for first REPORT.

### R0 (YYYY-MM-DD)
- Score: X/10 | Status: 🔄 Revision Needed
- Response:
  - 🔴/🟡 Issue Description: ✅ Fixed / 🔄 Not Fixed (explain why)
-->

## Completion Status

| Task | Status | Notes |
|------|------|------|
| {{task_1}} | ✅ | {{description_1}} |
| {{task_2}} | ✅ | {{description_2}} |

## Changed Files

| File | Changes |
|------|----------|
| `{{file_path}}` | {{change_description}} |

## Pending Confirmation (optional)

- [ ] {{debug_note}}

## Additional Notes (optional)

{{custom_content}}

---

## Build Results

| Command | Result |
|------|------|
| `{{type_check_cmd}}` | ✅ {{type_check_result}} |
| `{{build_cmd}}` | ✅ {{build_result}} |
| `{{backend_check_cmd}}` | ✅ {{backend_check_result}} |

---

**Current Status**: {{status}} — Waiting for {{tpm_name}} review

---

## Native Sub-Agent Format (optional)

> The following format is for Native Sub-Agent reference. Native reports are audit records, targeted at human developers.

```markdown
# REPORT_NNN: {{title}}

> **Report Type**: {{audit_note}}
> Audience: {{audience}}

## Executive Summary
- Task ID: {{task_id}}
- Status: {{status}}
- Core Goal: {{core_goal}}

## Core Changes
> Natural language description, no full code dump, only files and nature of changes
{{core_changes}}

## Decision Rationale
> Explain WHY — this is the most valuable part
{{decision_rationale}}

## Risks & Manual Confirmation Needed
- [ ] {{risk_item_1}}
- [ ] {{risk_item_2}}

## Self-Checklist
- [x] {{check_item_1}}
- [x] {{check_item_2}}
```
