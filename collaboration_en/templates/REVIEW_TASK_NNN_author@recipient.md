<!-- Used under the delegated review paradigm. Not needed under the self-loop review paradigm. -->

# REVIEW_TASK_NNN: {{review_target}}

> **Filename**: `REVIEW_TASK_NNN_author@recipient.md`
> **Location**: `inbox/`
> **Naming**: segments separated by `_`, within segments use `-`. `NNN` = review task number

**Reviewer**: {{author}}
**Reviewee**: {{assignee}}
**Priority**: {{priority}}

---

## Review Scope

| File | Path | Notes |
|------|------|------|
| {{file_name}} | `{{file_path}}` | {{review_reason}} |

## Review Focus

- [ ] {{check_item_1}}
- [ ] {{check_item_2}}

## Output Requirements

Submit `outbox/REVIEW_REPORT_NNN_DATE_author@recipient.md` (to TPM under delegated review), containing:
1. Overall score (1-10)
2. Issues found (🔴 Critical / 🟡 General / 💡 Suggestion)
3. Merge recommendation (Approve / Revision Needed)
