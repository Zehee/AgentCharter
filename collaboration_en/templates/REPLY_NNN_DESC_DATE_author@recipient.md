<!--
  File Type: Proactive Report Processing Reply
  Maintainer: TPM
  Purpose: Notify proactive report submitter of processing results
  Created: After TPM processes a proactive report
  Naming: REPLY_NNN_DESC_DATE_author@recipient.md
    - NNN: corresponding proactive report number
    - DATE: processing date `YYYYMMDD`
    - AUTHOR: report submitter identifier (UPPERCASE)
-->

# REPLY_NNN: {{title}}

> **Filename**: `REPLY_NNN_DESC_DATE_author@recipient.md`
> **Location**: `inbox/`
> **Naming**: segments separated by `_`, within segments use `-`. `NNN` = corresponding report number, `DATE` = processing date `YYYYMMDD`, `AUTHOR` = submitter identifier (UPPERCASE)

**Source Report**: {{ref_nnn}}
**Processing Date**: {{DATE}}
**Submitter**: {{author}}

---

## Result Summary

| Status | Count | Notes |
|------|------|------|
| 📋 Task | {{task_count}} | {{task_note}} |
| 📅 Backlog | {{scheduled_count}} | {{scheduled_note}} |
| ✅ Accept | {{accepted_count}} | {{accepted_note}} |
| ❌ Reject | {{ignored_count}} | {{ignored_note}} |
| ✓ Done | {{processed_count}} | {{processed_note}} |

**Detailed annotation**: {{detailed_notes}}

---

## Key Decisions (optional)

> - Decision 1: ...
> - Decision 2: ...
{{key_decisions}}

---

**Processor**: {{handler}}
**Date**: {{DATE}}
