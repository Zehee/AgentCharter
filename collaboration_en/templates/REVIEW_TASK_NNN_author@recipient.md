# REVIEW_TASK_NNN: Review Subject

> **Filename**: `REVIEW_TASK_NNN.md`
> **Location**: `inbox/`
> **Naming**: segments separated by `_`, within segments use `-`. `NNN` = review task number

**Dispatcher**: TPM
**Reviewer**: [ASSIGNEE]
**Date**: YYYY-MM-DD
**Review Scope**: (what REPORT / code to review)
**Review Level**: P1 / P2 / P3

---

## Review Requirements

- Read the corresponding REPORT in `outbox/`
- Verify the actual code changes (do not rely solely on REPORT descriptions)
- Run build verification commands
- Output `inbox/REVIEW_REPORT_NNN_DATE_author@recipient.md` with scores, issues (file:line), and merge recommendation
