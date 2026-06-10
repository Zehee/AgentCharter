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
# REPORT_NNN: Task Title

> **Report Type**: [Audit Only] This report is an execution record. TPM has been informed via internal channel.
> Audience: Human developers (retrospective, QA review).

## Executive Summary
- Task ID: NNN
- Status: ✅ Success / ⚠️ Manual Confirmation Needed
- Core Goal: One sentence explaining what was done.

## Core Changes
- `file path` — Added Y function, replaced old Z implementation.

## Decision Rationale
- Why was plan A chosen over plan B?

## Risks & Manual Confirmation Needed
- [ ] Concurrent logic not fully verified, needs manual review.
```
