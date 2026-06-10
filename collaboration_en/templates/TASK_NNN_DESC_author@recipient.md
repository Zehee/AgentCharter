# TASK_{{NNN}}: {{title}}

> **Filename**: `TASK_{{NNN}}_DESC_author@recipient.md`
> **Location**: `inbox/`
> **Naming**: segments separated by `_`, within segments use `-`. `NNN` = task number, `DESC` = short English description, `AUTHOR` = dispatcher identifier (UPPERCASE, typically TPM), `ASSIGNEE` = executor identifier (UPPERCASE)

**Dispatcher**: {{author}}
**Executor**: {{assignee}}
**Priority**: {{priority}}
**Dependency**: {{dependency}}
> Optional: related TASK number

**Decision Source**: {{decision_source}}
> Optional: DECISION_NNN / PROACTIVE_REPORT_NNN

---

## Goal

> One sentence describing what this task aims to achieve.
{{goal}}

## Current Status

> What exists already, what is missing, why this task is needed.
{{current_status}}

## Detailed Requirements

> Break down sub-modules by functionality, specify involved files and key logic.
{{requirements}}

## Acceptance Criteria

> Acceptance items + [type check command] 0 errors.
{{acceptance_criteria}}

## Reference Files

> Frontend/backend source paths.
{{reference_files}}
