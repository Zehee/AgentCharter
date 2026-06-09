# Registration Form

> Before proceeding, make sure you have read `README.md` and understand the AgentCharter framework rules. This file is only the registration form.

New members: follow the guide below to complete the Q&A and write each entry into the table. Notify the TPM for review when done. After TPM confirmation, entries move to `ACTIONS.md` and the registration table is cleared.

---

## Registration Action Table

| Action | From → To | Channel |
|------|----------------|------|
| Assign Task | | |
| Submit Report | | |
| Review Code | | |
| Proactive Report | | |
| Blocking Notice | | |
| Decision Record | | |

---

## Guide

### Step 1: Declare Your Role

Confirm with the developer:

```
What is my role? (TPM / External Agent / Sub-Agent (Native) / Reviewer / Reporter)
Reporter note: Any role can double as Reporter — submits proactive reports without a corresponding TASK
```

Record this in `logs/xxx-log.md`.

---

### Step 2: Configure Actions

Open `ACTIONS.md` and read the existing member list.

Ask the developer each question and write each answer into the registration table above immediately:

```
Action 1 — Task Dispatch
  Q: Who dispatches tasks to me?
  Options: [existing member list] or [none]
  Write: | Assign Task | Selected → Me | Channel |
  External → inbox/TASK
  Native   → Internal Channel + inbox/TASK (for record)
  None     → skip

Action 2 — Report Submission
  Q: Who do I submit reports to?
  Write: | Submit Report | Me → Selected | Channel |
  External → outbox/REPORT
  Native   → Internal Channel (code diff) + outbox/REPORT

Action 3 — Code Review
  Q: Whose code do I review? (multi-select)
  Write: | Review Code | Me → Selected | REPORT → REVIEW_REPORT |
  Q: Who reviews my code? (multi-select)
  Write: | Review Code | Selected → Me | REPORT → REVIEW_REPORT |
  Reviewer writes REVIEW_REPORT to reviews/

Action 4 — Proactive Report (Reporter double-role)
  Q: Do I need to submit proactive reports? (audits, analysis, design proposals — reports without TASK)
  Yes → Write: | Submit Proactive Report | Me → TPM | outbox/PROACTIVE_REPORT |
  Feedback: TPM places a REPLY receipt in inbox/ after processing

Action 5 — Blocking Dependencies
  Q: Who do I wait for when blocked?
  Write: | Blocking Notice | Me → Selected | outbox/BLOCKING |
  Q: Who gets blocked because of me?
  Write: | Blocking Notice | Selected → Me | outbox/BLOCKING |

Action 6 — Decision Recording (human-AI pairs only; Sub-Agent skip)
  Q: Do I need to record decision processes?
  If Yes — You are a human-AI pair Agent. When significant consensus is reached with your human, create DECISION files recording the reasoning chain.
  Write: | Decision Record | Me → decisions/ | DECISION_NNN_DATE_AUTHOR.md |
  If TPM action is needed, feed the DECISION into a PROACTIVE_REPORT.
  If No — skip (not applicable to Sub-Agent).
```

**After writing: status = Onboarding Pending. Tell the developer "Registration complete, please ask the TPM to review." After TPM confirmation, entries move to ACTIONS.md and the registration table is cleared.**

---

### Step 3: Start Working

```
External Agent:
  → Scan inbox/ for TASK with ASSIGNEE=you
  → Pick up → code → REPORT to outbox/ → write logs/
  → When doubling as Reporter: proactive report → outbox/PROACTIVE_REPORT → wait for inbox/REPLY receipt
  → Human-AI pair decisions: write DECISION → decisions/, feed into PROACTIVE_REPORT if TPM action needed

Sub-Agent (Native):
  → Wait for TPM internal dispatch → code
  → Write REPORT to outbox/ → deliver source directly (internal channel) → write logs/
  → No DECISION — pure AI, no human interaction

Reviewer:
  → Read REPORT → review → write REVIEW_REPORT to reviews/
  → Score, with file:line evidence

Reporter (double-role):
  → Submit proactive report → outbox/PROACTIVE_REPORT
  → Watch inbox/ for REPLY receipt to understand the decision

Blocked: Check your blocking rows in the action table → write BLOCKING
Blocker: Received a BLOCKING? → prioritize → write BLOCKING_REPLY
```
