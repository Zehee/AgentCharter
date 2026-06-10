# REVISION_NNN: Fix Issues Found in REVIEW_NNN

> **Filename**: `REVISION_NNN_DATE_author@recipient.md`
> **Location**: `inbox/`
> **Naming**: segments separated by `_`, within segments use `-`. `NNN`=corresponding review number, `DATE`=creation date `YYYYMMDD`, `ASSIGNEE`=executor identifier (UPPERCASE)

**Dispatcher**: {{author}}
**Executor**: {{assignee}}
**Date**: {{DATE}}
**Priority**: {{priority}}
**Corresponding**: {{ref_nnn}}

---

## Goal

One sentence describing what needs to be fixed.

## Issue List

| # | Issue | File/Location | Fix Requirement |
|---|------|----------|---------|
| 1 | Issue description | `xxx:line` | Expected behavior |
| 2 | Issue description | `xxx:line` | Expected behavior |

## Acceptance Criteria

- [ ] Fix item 1
- [ ] Fix item 2
- [ ] `[type check command]` 0 errors
- [ ] Submit `outbox/REPORT_NNN_R1_DATE_author@recipient.md`
