# Collaboration Link Table

> Maintained by the TPM. Everyone else: read-only.

Each row defines one collaboration channel: who passes what to whom, through which medium.

---

## Channel Types

| Channel | Purpose | Direction |
|---------|---------|-----------|
| `inbox/TASK` | Task dispatch | TPM → Executor |
| `inbox/TASK_TEST` | Test dispatch | TPM → Tester |
| `inbox/REVISION` | Review rework | TPM → Executor |
| `inbox/REVIEW_TASK` | Review delegation (delegated paradigm) | TPM → Reviewer |
| `inbox/REVIEW_REPORT` | Review conclusion (self-loop paradigm) | Reviewer → Executor |
| `inbox/NOTICE` | System notice | TPM → All |
| `outbox/REPORT` | Task completion report | Executor → TPM |
| `outbox/REPORT_R1/R2` | Revision report | Executor → Reviewer |
| `outbox/TEST_REPORT` | Test completion report | Tester → TPM |
| `outbox/PROACTIVE_REPORT` | Proactive report (no TASK) | Anyone → TPM |
| `outbox/REVIEW_REPORT` | Review conclusion (delegated paradigm) | Reviewer → TPM |
| `outbox/BLOCKING` | Blocking notice | Anyone → Blocked party |
| `outbox/BLOCKING_REPLY` | Blocking resolution reply | Blocked party → Blocker |

> Channel names are self-describing. The Action column is for human readability only — scripts validate against channels, not action names.

---

## Collaboration Links

| Action | From → To | Channel |
|--------|-----------|---------|
| | | |
