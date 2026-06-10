# CHARTER.md — Project Cooperation Charter

> This file is a template. Filled out by the TPM during initialization, then stays inside `collaboration/` as project-level compressed rules alongside the framework general rules.
> The completed CHARTER.md becomes project-level compressed rules, alongside framework general rules (`collaboration/README.md`), not governed by the framework.
> Your project can adjust, simplify, or extend any content in this template.
>
> Filled in by the TPM during initialization. After completion, becomes the supreme rules shared by all Agents.
>
> **Version**: v1.0  
> **Effective Date**: [YYYY-MM-DD]  
> **Scope**: All AI Agents and human developers in this project  
> **Priority**: This document > TPM.md > other documents

---

## 1. Collaboration Framework

### 1.1 Communication

**Sole communication channel**: the file system under `collaboration/`.

| Directory | Purpose | Permission |
|------|------|------|
| `inbox/` | Task dispatch, notices, replies | TPM writes, executor reads |
| `outbox/` | Report submission, blocking notices | Executor writes, TPM reads |
| `reviews/` | Review reports | Reviewer writes, all read |
| `logs/` | Operation logs | Exclusive per person |
| `todos/` | Backlog items | TPM writes |
| `context/` | Sub-Agent memory, injection only | TPM maintains |
| `archive/` | Completed archive | TPM manages |

### 1.2 Naming Conventions

- **Segments separated by `_`**, **within segments use `-`**
- `NNN` = 3-digit sequence number (001, 042, 049C_R1)
- Identifiers in **ALL CAPS**
- `DATE` = `YYYYMMDD`

### 1.3 File Templates

See `templates/`. Copy the corresponding template, replace placeholders before writing.

---

## 2. Roles & Responsibilities

| Role | Type | Responsibility | Red Line |
|------|------|------|------|
| **[TPM]** | Host Agent | Task dispatch, architecture decisions, final approval, Git operations | No business code |
| **[Agent1]** | [External / Sub-Agent] | [description] | [red line] |
| **[Agent2]** | [External / Sub-Agent] | [description] | [red line] |
| **[Agent3]** | [External / Sub-Agent] | [description] | [red line] |

> TPM fills this table upon initialization. Update on every new Agent onboarding.

---

## 3. Task Lifecycle

### 3.1 TASK Tiering

| Level | Definition | Review Requirement |
|------|------|---------|
| **P0** | Micro (single file, no logic change) | TPM directly commits |
| **P1** | Standard change | Reviewer reviews |
| **P2** | Cross-module / new interface | Reviewer full review + specialized checks |
| **P3** | Architecture / security / core flow | Reviewer reviews + TPM deep assessment |

### 3.2 Standard Flow

```
TPM creates TASK → inbox/
  → Executor picks up → codes → REPORT → outbox/
  → TPM determines level
    ├── P0 → directly commit
    └── P1/P2/P3 → Reviewer reviews → writes REVIEW_REPORT → reviews/
         → ACCEPT → commit → archive
         → Revision needed → REPORT_R1 → re-review → loop
```

### 3.3 Proactive Report

Any Agent may submit a proactive report (PROACTIVE_REPORT, no corresponding TASK):

```
Submit → TPM reads → decides (Accept / Reject / Task / Backlog) → annotate → REPLY → archive
```

---

## 4. Review Mechanism

### 4.1 Review Standards

| Level | Meaning |
|------|------|
| 🔴 Critical | Functional error, security vulnerability, data loss. Must fix |
| 🟡 General | Style inconsistency, inadequate error handling, missing tests. Recommended fix |
| 💡 Suggestion | Readability optimization, comment supplementation. Optional fix |

### 4.2 Review Summary Flow

```
Reviewer writes REVIEW_REPORT (with R0 summary)
  → Executor copies summary to REPORT_R1 → appends fix responses
  → Reviewer copies summary to REVIEW_REPORT_R1 → appends R1 conclusion
  → Loop until ACCEPT
```

**Hard rule**: Must not modify historical round text.

---

## 5. Archive Rules

| File Type | Archive Timing |
|----------|----------|
| TASK / TODO | Immediately upon completion |
| NOTICE / REPLY | After recipient has read |
| REPORT / REVIEW_REPORT / PROACTIVE_REPORT | After relevant parties have marked as read |

**Read marker**: Add `> ✅ Read BY {AGENT} @ {DATE}` at file top

---

## 6. Git Ban

**Any Agent is strictly forbidden from executing any git command**. Including status, log, diff, checkout, commit, push, etc. Sole exception: TPM executing `git add` and `git commit`.

---

## 7. Technical Baseline

| Check Item | Command | Pass Standard |
|--------|------|---------|
| [type check] | `[command]` | [standard] |
| [build] | `[command]` | [standard] |
| [test] | `[command]` | [standard] |

---

## 8. Revision History

| Date | Version | Change |
|------|------|------|
| [YYYY-MM-DD] | v1.0 | TPM initialization |
