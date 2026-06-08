# Collaboration Link Table

> Maintained by the TPM. Everyone else: read-only.

Each row defines one collaboration channel: who passes what to whom, through which medium.

---

## Field Reference

| Field | Meaning | Allowed Values |
|------|------|--------|
| **Action** | What to do | `Assign Task` `Submit Report` `Review Code` `Review Conclusion` `Blocking Notice` `Blocking Reply` `Submit Proactive Report` `Quality Confirmation` ... |
| **From → To** | Who to whom | Agent identifier (e.g., `TPM` `Alice` `Bob`) or `ALL` |
| **Channel** | Through what | See table below |

## Channel Types

| Channel | Purpose | Direction |
|------|------|------|
| `inbox/TASK` | Task dispatch | TPM → Executor |
| `inbox/TASK_TEST` | Test dispatch | TPM → Tester |
| `outbox/REPORT` | Task completion report | Executor → TPM |
| `outbox/TEST_REPORT` | Test completion report | Tester → TPM |
| `outbox/PROACTIVE_REPORT` | Proactive report (no TASK) | Anyone → TPM |
| `outbox/BLOCKING` | Blocking notice | Blocker → Blocked party |
| `outbox/BLOCKING_REPLY` | Blocking resolution reply | Resolver → Blocker |
| `reviews/REVIEW_REPORT` | Review conclusion | Reviewer → Executor |
| `Internal Channel` | Realtime delivery (code diff / review notification) | TPM ↔ Sub-Agent |

## Example

Below is a workflow configuration for a small team:

| Action | From → To | Channel |
|------|----------------|------|
| Assign Task | TPM → Alice | inbox/TASK |
| Submit Report | Alice → TPM | outbox/REPORT |
| Review Code | Bob → Alice | REPORT → REVIEW_REPORT |
| Review Conclusion | Bob → Alice | reviews/REVIEW_REPORT |
| Quality Confirmation | Bob → TPM | Internal Channel |
| Blocking Notice | Alice → Charlie | outbox/BLOCKING |

---

## Collaboration Links

| Action | From → To | Channel |
|------|----------------|------|
| | | |
