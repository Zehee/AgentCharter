# REVISION_NNN: {{title}}

> **Filename**: `REVISION_NNN_DATE_author@recipient.md`
> **Location**: `inbox/`
> **Naming**: segments separated by `_`, within segments use `-`. `NNN` = corresponding review number, `DATE` = creation date `YYYYMMDD`, `TPM` = dispatching TPM identifier (UPPERCASE), `ASSIGNEE` = executor identifier (UPPERCASE)

**Dispatcher**: {{author}}
**Executor**: {{assignee}}
**Date**: {{DATE}}
**Priority**: {{priority}}
**Corresponding**: {{ref_nnn}}

---

## Goal

> One sentence describing what needs to be fixed.
{{goal}}

## Issue List

| # | Issue | File/Location | Fix Requirement |
|---|------|----------|---------|
| {{issue_number_1}} | {{issue_description_1}} | `{{issue_file_1}}` | {{issue_expectation_1}} |
| {{issue_number_2}} | {{issue_description_2}} | `{{issue_file_2}}` | {{issue_expectation_2}} |

## Acceptance Criteria

- [ ] {{acceptance_item_1}}
- [ ] {{acceptance_item_2}}
- [ ] `{{type_check_cmd}}` 0 errors
- [ ] Submit `{{report_submission}}`
