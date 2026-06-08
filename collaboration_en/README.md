# AgentCharter

A file-driven, multi-agent collaboration framework. Files are the sole communication channel and audit trail.

> **No file = it didn't happen.**

**Version**: v3.2 | **Updated**: 2026-06-07

---

## 👑 Supreme Commander (TPM)

  - The TPM of this project is **[replace this with your name if explicitly told you are the TPM]**

> If you are not the TPM, read `REGISTER.md` to onboard.

---

## 1. Framework Rules

### 1.1 Communication Channels

| Channel | Who Uses It | Method | Rule |
|------|------|------|------|
| **File Channel** | TPM, External Agent | inbox/outbox read/write | Async, traceable |
| **Internal Channel** | TPM ↔ Sub-Agent (Native) | Host direct connection | Realtime diff delivery |

### 1.2 Three Roles

| Role | Responsibility | Channel |
|------|------|------|
| **TPM** | Dispatch tasks (T), orchestrate plans (P), approve & coordinate (M), sole Git authority | File + Internal |
| **External Agent** | Scan inbox/ for tasks, code, submit REPORT | File channel |
| **Sub-Agent (Native)** | Wait for TPM internal dispatch, code, deliver diff via internal channel + outbox/REPORT for audit | Internal + File |

### 1.3 Communication Protocols

Collaboration flows are defined by `ACTIONS.md`, not hardcoded by the framework. Two basic file exchange modes:

**Task-driven**: TPM writes TASK → inbox/ → executor picks up → codes → writes REPORT → review → archive

**Proactive Report**: Anyone writes PROACTIVE_REPORT → TPM reviews and decides → archive

### 1.4 Hard Rules

| Rule | Content |
|------|------|
| **Files are the Contract** | All tasks, reports, reviews, and blocks must go through files |
| **Git Isolation** | Only the TPM may execute any git command. All other Agents are forbidden. No exceptions |
| **Dual Review** | Any code must be reviewed by another AI before merging |
| **Append-Only Logs** | logs/, ACTIONS.md, dashboard.md — append only, never modify history |
| **inbox Write Domain** | TPM writes; executors read-only, must not delete |
| **outbox Write Domain** | Executors write; TPM read-only, must not modify or delete |
| **logs/** | One exclusive file per person: `{identifier}-log.md`. Others read-only |
| **ACTIONS.md / dashboard.md / todos/** | Only TPM may write |
| **Blocking** | Write `BLOCKING` to the blocked party's read directory; resolve with `BLOCKING_REPLY` |

---

## 2. Directory & Permissions

```
collaboration/
├── README.md              This file
├── CHARTER.md             Charter template (TPM fills then moves to project root)
├── TPM.md                 TPM code of conduct
├── PROJECT.md             Project config (tech stack, members, rules)
├── REGISTER.md            Registration form
├── ACTIONS.md             Collaboration link table (empty template, TPM maintains)
├── dashboard.md           TPM-maintained progress report for humans
├── context/               Sub-Agent context memory (TPM maintains)
├── inbox/                 TASK / REVISION / NOTICE / REPLY
├── outbox/                REPORT / PROACTIVE_REPORT / BLOCKING
├── reviews/               REVIEW_REPORT (Reviewer writes, all read)
├── logs/                  One exclusive operation log per person
├── todos/                 TODO backlog (TPM maintains)
├── templates/             14 file templates (read-only reference)
└── archive/               Completed archive (inbox / outbox / reviews / events)
```

| Path | Who Writes | Who Reads |
|------|------|------|
| `inbox/` | TPM | Executor, read-only |
| `outbox/` | Executor | TPM, read-only |
| `reviews/` | Reviewer + TPM | Everyone |
| `logs/` | Exclusive per person | Others, read-only |
| `ACTIONS.md` | TPM | Everyone |
| `dashboard.md` | TPM | Humans |
| `todos/` | TPM | Everyone |
| `context/` | TPM | Sub-Agent |

> Add `inbox/ outbox/ logs/ reviews/ context/ todos/` to .gitignore. Keep `archive/` in Git as a permanent audit trail.

---

## 3. Naming Conventions

- **Segments separated by `_`**, **within segments use `-`**
- `NNN` = 3-digit sequence number (001, 042, 049C_R1)
- `DESC` = short English description, within segment use `-`
- `ASSIGNEE` / `AUTHOR` / `TARGET` = identifiers in **ALL CAPS**
- `DATE` = `YYYYMMDD`

```
TASK_053_HUNTER-SHOOT-BACKEND_PETER.md
REPORT_053_20260530_PETER.md
REVISION_049C_20260530_FLASH.md
```

---

## 4. File Type Quick Reference

| File Type | Template | Location | Who Writes |
|----------|------|------|------|
| Task | `TASK_NNN_DESC_ASSIGNEE.md` | inbox/ | TPM |
| Test Task | `TASK_TEST_NNN_DESC_ASSIGNEE.md` | inbox/ | TPM |
| Revision Task | `REVISION_NNN_DATE_ASSIGNEE.md` | inbox/ | TPM |
| Notice | `NOTICE_NNN_DESC_DATE_TARGET.md` | inbox/ | TPM |
| Reply | `REPLY_NNN_DESC_DATE_AUTHOR.md` | inbox/ | TPM |
| Task Report | `REPORT_NNN_DATE_AUTHOR.md` | outbox/ | Executor |
| Test Report | `TEST_REPORT_NNN_DATE_AUTHOR.md` | outbox/ | Tester |
| Proactive Report | `PROACTIVE_REPORT_NNN_DESC_DATE_AUTHOR.md` | outbox/ | Anyone |
| Review Report | `REVIEW_REPORT_NNN_DATE_AUTHOR.md` | reviews/ | Reviewer |
| Blocking Notice | `BLOCKING_NNN_DATE_TARGET.md` | outbox/ | Blocker |
| Blocking Reply | `BLOCKING_REPLY_NNN_DATE_AUTHOR.md` | outbox/ | Resolver |
| Todo | `TODO_NNN_DESC_SOURCE.md` | todos/ | TPM |
| Log | `{identifier}-log.md` | logs/ | Per person |

### File Writing Rules

1. Copy the corresponding template from `templates/` to the target location, replacing placeholders
2. Strictly follow the naming convention at the top of each template
3. Do not modify `templates/` itself — report defects via a proactive report to the TPM

---

## 5. Task Lifecycle

```
TPM writes TASK → inbox/
  → Executor picks up → codes → writes REPORT → outbox/
  → Review → writes REVIEW_REPORT → reviews/
  → ACCEPTED → archive
  → Revision needed → write REPORT_R1 → re-review → loop until ACCEPTED
```

| Status | Meaning |
|------|------|
| 🔵 ASSIGNED | Dispatched, awaiting pickup |
| 🟡 IN_PROGRESS | In execution |
| 🟠 REVIEW_PENDING | Submitted, awaiting review |
| ✅ ACCEPTED | Review passed |
| 🔴 REVISION_NEEDED | Revision required |
| 🟢 DONE | Merged / closed |
| ⚪ CANCELLED | Cancelled |
| 🔴 BLOCKED | Blocked |
| ✅ RESOLVED | Resolved |

> Optional tiered review (P0-P3) is documented in `TPM.md`. The actual review chain is defined by `ACTIONS.md`.

---

## 6. Proactive Report (Read-and-Burn)

A report without a corresponding TASK. Anyone can submit a `PROACTIVE_REPORT` to outbox/.

```
Submit → TPM reads → decides → annotates at end of report → writes REPLY receipt → archive
```

**Why "Read-and-Burn"**: Proactive reports do not enter the standard task lifecycle. Once the TPM reads and decides, the report is archived. If the decision is 📋 Task or 📅 Backlog, the TPM creates a corresponding TASK or TODO separately.

| TPM Decision | Meaning |
|----------|------|
| ✅ Accept | Accepted directly |
| ❌ Reject | Not accepted |
| 📋 Task | TASK/REVISION created |
| 📅 Backlog | TODO created |
| ✓ Done | Already implemented/fixed |

---

### `todos/` Directory

A staging area for backlog items. When the TPM decides a requirement is **not for immediate execution, to be scheduled later**, create a `TODO_NNN_DESC_SOURCE.md` here.

**Sources**: 📅 Backlog decisions from proactive reports, deferred milestone items, low-priority ideas from users.

**Lifecycle**: TODO gets scheduled → TPM converts to TASK in inbox/ → original TODO archived. Long-unstarted TODOs remain in todos/ as a reminder for the TPM to review periodically.

---

## 7. Code Standards

| Rule | Description |
|------|------|
| New file header | Top 3 lines: `Author` / `Date` / `Description` |
| Change log, not file comments | Don't write modification comments in files; log changes to `logs/{identifier}-log.md` |
| Show diff for edits | When modifying existing files, show only the diff; full content only for new files |
| Strict typing | Core modules must not use loose types (TS: no `any`; Rust: no `unwrap()` on user input) |
| Minimal changes | Change only what's necessary; leave unrelated code alone |

---

## 8. Logging Standards

One exclusive file per person: `logs/{identifier}-log.md`, segmented by date. Operation types: `Create` / `Edit` / `Delete` / `Move` / `Read` / `Verify` / `Review` / `Dispatch` / `Install` / `Start` / `Stop`

```markdown
## YYYY-MM-DD

| Time | Operation | Target | Notes |
|------|------|------|------|
| 22:00 | Create | `src/xxx.vue` | Created component X |
```

---

## 9. Archive Rules

Only the TPM performs archiving. Archiving is a move operation; never modify content.

| File Type | Archive Timing |
|----------|----------|
| TASK / REVISION | Immediately after pickup |
| NOTICE / REPLY | After recipient has read |
| BLOCKING / BLOCKING_REPLY | After block is resolved |
| REPORT / REVIEW_REPORT / PROACTIVE_REPORT | After TPM has processed |

**Target paths**: `archive/inbox/` / `archive/outbox/` / `archive/reviews/` / `archive/events/`

---

## 10. Role Definitions

### TPM

**Responsibilities**: Create and dispatch TASKs, orchestrate plans, final review, Git operations, maintain ACTIONS.md / dashboard.md / todos/, archive, inject context for Sub-Agents

**Red lines**: Task-first, never modify outbox/, delegate reviews to Reviewer, never write business code

### External Agent

**After onboarding**: Scan inbox/ for TASK with ASSIGNEE=you → pick up → code → REPORT → outbox/

**Rules**: Git commands strictly forbidden. Block? Write BLOCKING.

### Sub-Agent (Native)

**After onboarding**: Wait for TPM internal dispatch → code → deliver diff via internal channel → REPORT to outbox/ for audit → after completion, read the next TASK with ASSIGNEE=you from inbox/

**Rules**: Can read/write all collaboration files but cannot proactively scan. Git commands strictly forbidden. Must not modify files outside your responsibility. Context provided by `context/{name}-memory.md`.

---

## 11. Onboarding Process

1. Confirm your role (TPM / External / Sub-Agent / Reviewer), write first log entry
2. Follow `REGISTER.md` to answer questions and fill in the registration action table
3. TPM confirms, moves to `ACTIONS.md`; onboarding complete

**Reporter is not a standalone role** — any role can double as one. When you submit a `PROACTIVE_REPORT`, you are the Reporter.

---

## 12. Quick Reference

| I want to... | Action |
|---------|------|
| Claim identity | Read 👑 → TPM reads `TPM.md` / non-TPM reads `REGISTER.md` |
| Get a task | Check `ACTIONS.md` for your dispatch row → scan inbox/ or wait for internal dispatch |
| Submit a report | Write `outbox/REPORT_NNN_DATE_AUTHOR.md` |
| Submit a proactive report | Write `outbox/PROACTIVE_REPORT_NNN_DESC_DATE_AUTHOR.md` |
| Write a review conclusion | Write `reviews/REVIEW_REPORT_NNN_DATE_AUTHOR.md` with file:line + severity |
| Report a block | Write `outbox/BLOCKING_NNN_DATE_TARGET.md` (state the unblock condition) |
| Resolve a block | Write `outbox/BLOCKING_REPLY_NNN_DATE_AUTHOR.md` |
| Write a log | Append to `logs/{identifier}-log.md` |
| Check a template | Read the corresponding file in `templates/` |
| See progress (human) | Read `dashboard.md` |
