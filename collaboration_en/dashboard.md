# Dashboard

> TPM-maintained progress report for humans. Updated daily alongside patrol.
> This is what humans read — keep it concrete, keep it current.

**Last Updated**: YYYY-MM-DD HH:MM  
**Project**: [Project Name]  
**Version**: [Version]

---

## Project Snapshot

| | |
|------|------|
| **Tech Stack** | [Frontend] / [Backend] — e.g. Vue 3 + TypeScript / Rust + Tauri |
| **Build** | Type Check: `[cmd]` \| Build: `[cmd]` \| Test: `[cmd]` |

### Team

| Role | Agent | Type | Notes |
|------|-------|------|------|
| TPM | [Name] | Native Host | Task Planning Manager |
| [Role] | [Agent] | [External / Sub-Agent] | [Brief responsibility] |

---

## Overview

| Dimension | Status | Notes |
|------|------|------|
| **Overall Progress** | 🟢 / 🟡 / 🔴 | e.g. 🟢 ~75% — Core features complete, entering testing phase |
| **Build Health** | 🟢 / 🟡 / 🔴 | e.g. 🟢 Healthy — `check` ✅ / `test` 98 pass ✅ / commit `abc1234` |
| **Active Tasks** | N | e.g. 3 — Alice: TASK_042 / Bob: TASK_043 / Charlie: TASK_TEST_010 |
| **Pending Review** | N | e.g. 1 — REPORT_041 awaiting review |
| **Blocked** | N | e.g. 0 — no BLOCKING |
| **Risk** | 🟢 / 🟡 / 🔴 | e.g. 🟡 Medium — performance concern on search module, investigation planned |

---

## Team Status

| Role | Current Work | Status |
|------|----------|------|
| **TPM** | Patrol, task dispatch, review approvals, dashboard update | 🟢 Active |
| **[Agent 1]** | TASK_042 — Search module optimization | 🔵 ASSIGNED |
| **[Agent 2]** | TASK_043 — User settings page | 🟡 IN_PROGRESS |
| **[Agent 3]** | Idle | ✅ Standby |
| **[User]** | — | ⚪ Observing |

---

## Active Tasks

| # | Task | Executor | Status | Review Level | Priority | Notes |
|------|------|--------|------|----------|--------|------|
| TASK_042 | Search module optimization | [Agent] | 🟡 IN_PROGRESS | P1 | 🟡 P1 | |
| TASK_043 | User settings page | [Agent] | 🔵 ASSIGNED | P1 | 🟢 P2 | |

---

## Recent Activity

> Most recent first. Each entry: date, what happened, who did it, outcome.

- **YYYY-MM-DD HH:MM** — TASK_041 completed: [Agent] submitted REPORT_041, Reviewer scored 9/10 ✅ ACCEPT, commit `abc1234`, archived
- **YYYY-MM-DD HH:MM** — REVIEW_REPORT_040: [Reviewer] flagged 🟡 issue in error handling → REVISION_040 created → [Agent] notified
- **YYYY-MM-DD HH:MM** — [Agent] submitted REPORT_040 for review

---

## Completed This Cycle

| # | Task | Executor | Score | Rounds | Status |
|---|------|--------|------|------|------|
| TASK_041 | [Description] | [Agent] | 9/10 | R0 | ✅ ACCEPT |
| REVISION_040 | Fix error handling edge case | [Agent] | 8/10 | R1 | ✅ ACCEPT |

---

## Known Issues

| Issue | Priority | Status |
|------|--------|------|
| Performance degradation on search with >10K records | 🟡 P1 | Investigating — TASK_045 planned |
| Login timeout under slow network | 🟡 P1 | ✅ REVISION_042 fixed |

## Decisions

| Item | Decision | Impact |
|------|------|------|
| Database query optimization strategy | **Batch prefetch** (Option A) | TASK_042 scope adjusted to include batch query rewrite |
| TEST_REPORT_005 conclusion | **🟡 Conditional pass** | 8 pending items → TASK_TEST_006; 2 bugs → TASK_046/047 |

---

## Milestones

| Milestone | Status | Completion |
|------|------|------|
| M0 — Framework Setup | ✅ | 100% |
| M1 — Core Features | ✅ | 95% |
| M2 — Polish & Performance | 🟡 | 60% |
| M3 — Public Release | 🔵 | 0% |

> **Archive**: completed tasks in `archive/inbox/` and `archive/outbox/`
