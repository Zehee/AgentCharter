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

# REPLY_NNN: Proactive Report Processing Reply

> **Filename**: `REPLY_NNN_DESC_DATE_author@recipient.md`
> **Location**: `inbox/`
> **Naming**: segments separated by `_`, within segments use `-`. `NNN`=corresponding report number, `DATE`=processing date `YYYYMMDD`, `AUTHOR`=submitter identifier (UPPERCASE)

**Source Report**: {{ref_nnn}}
**Processing Date**: {{DATE}}
**Submitter**: {{author}}

---

## Result Summary

| Status | Count | Notes |
|------|------|------|
| 📋 Task | N | Incorporated into existing tasks or new TASK/REVISION |
| 📅 Backlog | N | TODO file created; scheduled for later |
| ✅ Accept | N | Accepted directly; no extra task |
| ❌ Reject | N | Not adopted (reason in detailed annotation) |
| ✓ Done | N | Already implemented/fixed |

**Detailed annotation**: see `archive/outbox/{source report filename}`

---

## Key Decisions (optional)

- Decision 1: ...
- Decision 2: ...

---

**Processor**: TPM  
**Date**: YYYY-MM-DD
