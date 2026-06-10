# AgentCharter

> ⚠️ This is the **Agent Operating Manual**, NOT the project charter. The project charter is authored by the TPM and lives at `/CHARTER.md` (project root). This file defines rules and processes. The charter defines your specific project's decisions.

A file-driven, multi-agent collaboration framework. Files are the sole communication channel and audit trail.

> **No file = it didn't happen.**

**Version**: v3.3 | **Updated**: 2026-06-10

---

## 👑 Supreme Commander (TPM)

  - The TPM of this project is **[replace this with your name if explicitly told you are the TPM]**

> You are TPM → sign your name → read `TPM.md` and start working
> You are not TPM → read the rest of this file FIRST to understand the framework → then read `REGISTER.md` to join the team

---

## 1. Framework Rules

### 1.1 Communication Channels

| Channel | Who Uses It | Method | Rule |
|------|------|------|------|
| **File Channel** | TPM, External Agent | inbox/outbox read/write | Async, traceable |
| **Internal Channel** | TPM ↔ Sub-Agent (Native) | Host direct connection | Realtime diff delivery |

### 1.2 Three Roles

| Role | Responsibility | Channel | Human-AI Pair |
|------|------|------|----------|
| **TPM** | Dispatch tasks (T), orchestrate plans (P), approve & coordinate (M), sole Git authority | File + Internal | ✅ Default pairing — human + AI collaborate in same conversation |
| **External Agent** | Scan inbox/ for tasks, code, submit REPORT | File channel | ✅ Default pairing — human + AI collaborate in same conversation |
| **Sub-Agent (Native)** | Wait for TPM internal dispatch, code, deliver diff via internal channel + outbox/REPORT for audit | Internal + File | ❌ Pure AI — no conversation interface, background worker |

> **Human-AI Pair**: The TPM and External Agent are, by default, "human-AI pair composites" — behind either role can be an AI running alone, a human operating alone, or a human + AI collaborating in conversation. When significant decisions emerge, record the reasoning chain via `DECISION` files. Sub-Agent (Native) is pure AI, cannot directly interact with humans, and does not produce DECISION files.

### 1.3 Communication Protocols

Collaboration flows are defined by `ACTIONS.md`, not hardcoded by the framework. Two basic file exchange modes:

**Task-driven**: TPM writes TASK → inbox/ → executor picks up → codes → writes REPORT → review → archive

**Proactive Report**: Anyone writes PROACTIVE_REPORT → TPM reviews and decides → archive

> **On scale**: scanning a directory with 100 files costs roughly the same as scanning one with 1,000 — the bottleneck is your LLM's context window, not filesystem I/O. The framework's flat directory structure is the index. Start using it, optimize when you hit the wall.

> **Incremental file chain**: the entire task lifecycle is not one file being modified — it's a chain of incremental files stitched together. `TASK_NNN` → `REPORT_NNN` → `REVIEW_REPORT_NNN` → `REPORT_NNN_R1` → … Each Agent writes **new files** only in its own namespace, never modifying or overwriting anyone else's. History is a chain of immutable, append-only files — non-repudiable by design.

### 1.4 Hard Rules

| Rule | Content |
|------|------|
| **Files are the Contract** | All tasks, reports, reviews, and blocks must go through files |
| **Concurrency safety** | Every file an Agent writes is **directed, unique, and incremental**. `ACTIONS.md` pre-assigns channels — inbox/ is TPM-only, outbox/ each Agent has its own namespace. Every write creates a new file (TASK_NNN, REPORT_NNN_DATE_AUTHOR, etc.). There is no overwrite, no append to shared files, no shared write targets. File conflict is eliminated at the design level |
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
├── dashboard.md           TPM-maintained progress report for humans; humans can write instructions here, TPM reads them during patrol
├── context/               Sub-Agent context memory (TPM maintained, for Sub-Agent injection only. TPM and External Agents use their own local memory systems)
├── decisions/             DECISION records (written by human-AI pair Agents)
├── inbox/                 TASK / REVISION / NOTICE / REPLY
├── outbox/                REPORT / PROACTIVE_REPORT / BLOCKING
├── reviews/               REVIEW_REPORT (Reviewer writes, all read)
├── logs/                  One exclusive operation log per person
├── todos/                 TODO backlog (TPM maintains)
├── templates/             15 file templates (read-only reference)
└── archive/               Completed archive (inbox / outbox / reviews / decisions / events)
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
| Decision Record | `DECISION_NNN_DATE_AUTHOR.md` | decisions/ | Human-AI Pair Agent |
| Review Report | `REVIEW_REPORT_NNN_DATE_AUTHOR.md` | reviews/ | Reviewer |
| Blocking Notice | `BLOCKING_NNN_DATE_TARGET.md` | outbox/ | Blocker |
| Blocking Reply | `BLOCKING_REPLY_NNN_DATE_AUTHOR.md` | outbox/ | Resolver |
| Todo | `TODO_NNN_DESC_SOURCE.md` | todos/ | TPM |
| Log | `{identifier}-log.md` | logs/ | Per person |

### File Writing Rules

> Teams typically start with 3-4 templates (TASK, REPORT, REVIEW_REPORT) and introduce more as needs grow. The 15 templates are the framework's maximum set, not a checklist.

1. Copy the corresponding template from `templates/` to the target location, replacing placeholders
2. Strictly follow the naming convention at the top of each template
3. Do not modify `templates/` itself — report defects via a proactive report to the TPM
4. **Save your context**: templates are fixed boilerplate — re-reading them wastes tokens. Every Agent should leverage their platform's shortcut capabilities — whether prompt memory, snippets, rules, skills, or other mechanisms — to cache high-frequency template structures and generate files directly without opening `templates/` from scratch. Whatever shortcut you use, the file you produce MUST conform to the template format and naming conventions. Efficiency suggestion, not mandatory.

---

> 📎 The following is a reference grading pattern provided by the framework, based on wolf-judge real-world experience.
> The number of levels and specific criteria are defined by your project in `../CHARTER.md`.

## 5. Task Lifecycle

> **The only final artifacts are TASK and TODO** — no matter how complex the collaboration chain gets (DECISION → PROACTIVE_REPORT → TPM processing), it always lands as a TASK (executable work) or TODO (backlog item). Intermediate files are evidence, not endpoints.

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
> **The TPM is not exempt**: the TPM's own changes must also go through TASK → REPORT, with the same traceability as every other Agent.

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

**Lifecycle**: TODO gets scheduled → TPM converts to TASK in inbox/ → original TODO archived. Expired or discarded TODOs are archived directly. Long-unstarted TODOs remain in todos/ as a reminder for the TPM to review periodically.

---

### `decisions/` Directory — Pair Decision Records

> The TPM and External Agent are, by default, "human-AI pair composites." When significant decisions emerge during conversation, record the reasoning chain via `DECISION` files.

**PROACTIVE_REPORT records the product; DECISION records the process.** The moment the human says "send it out," the pair's AI should automatically determine whether a DECISION file is needed first:

```
Discussion ends, human says "send it" —

  ├── Multi-round reasoning, clear chain → AI writes DECISION first (verbatim) → then PROACTIVE_REPORT (linked to DECISION)
  ├── One-line decision, no reasoning → PROACTIVE_REPORT only (no DECISION)
  └── Info alignment only, no decision made → no DECISION, no PROACTIVE_REPORT. Not a decision — just confirmation
```

**Trigger principle: the AI must proactively recognize, the human doesn't need to ask twice.** The pair AI continuously senses decision signals during conversation — the moment the human says "OK, let's go with that," "agreed on this approach," or "write it up and send," the AI automatically completes the judgment. DECISION files are not an extra step; they're a natural extension of the conversation.

**How the AI distinguishes a decision from a discussion (sensing guide)**:

| This IS a decision (write DECISION) | This is NOT a decision (don't write) |
|------|------|
| Human says "OK, let's go with this approach" | "What are the pros and cons of this approach?" |
| Human says "Agreed — prioritize A, defer B" | "Which do you think is faster, A or B?" |
| Human says "Note this down: we're going with option C" | "Can you look up the data for option C?" |
| Human says "Confirmed, use this architecture" | "How does this architecture work?" |
| AI challenges → human explains → consensus reached | Pure information briefing, no choice made |
| Multiple options explicitly rejected, one selected | Options still being explored, not yet converged |

**One-liner**: When **options are eliminated and a choice is made** during discussion, write a DECISION. When it's just **exploring, understanding, or syncing information**, don't.

**DECISION flow**:
- TPM's own DECISION → directly converted to TASK / TODO
- External Agent's DECISION → fed into PROACTIVE_REPORT → TPM annotates → creates TASK / TODO
- No DECISION means no DECISION — info alignment, read confirmation, and context sync conversations where no choice was made do not produce a DECISION. DECISION is a decision record, not meeting minutes

**Key constraints**:
- If TPM action is needed, a PROACTIVE_REPORT is mandatory — DECISION is evidence, PROACTIVE_REPORT is the action request
- No reasoning chain → no DECISION needed — it's an optional quality enhancement, not a mandatory step
- DECISION archive timing: after all linked TASK/TODOs complete, move to `archive/decisions/`
- **Final artifacts are TASK and TODO only** — every decision ultimately lands as a TASK (executable work) or TODO (backlog item). DECISION, PROACTIVE_REPORT, and REVIEW_REPORT are intermediate evidence, not final artifacts

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
| TASK / REVISION | Immediately upon completion |
| NOTICE / REPLY | After recipient has read |
| BLOCKING / BLOCKING_REPLY | After block is resolved |
| REPORT | After TPM reads and decides |
| REVIEW_REPORT | After ACCEPT or REVISION_NEEDED conclusion |
| PROACTIVE_REPORT | After TPM annotates and places REPLY |
| DECISION | After all linked TASK/TODOs are complete |
| TODO | When converted to TASK / expired and discarded |

**Target paths**: `archive/inbox/` / `archive/outbox/` / `archive/reviews/` / `archive/decisions/` / `archive/events/`

---

## 10. Role Definitions

### TPM

**Responsibilities**: Create and dispatch TASKs, orchestrate plans, final review, Git operations, maintain ACTIONS.md / dashboard.md / todos/, archive, inject context for Sub-Agents

**Red lines**: Task-first, never modify outbox/, delegate reviews to Reviewer, never write business code

> **Single point isn't mandatory**: the simplest team has one TPM. If your TPM hallucinates or crashes, add a backup TPM row in `ACTIONS.md` — review and Git authority can be held by multiple people. The framework doesn't force a single keyholder.
> **Human managers talk to the TPM directly**: no file channel needed, no dashboard required. The human and the TPM are in the same conversation window — the human says "add an export feature next week," the TPM breaks it into TASKs in inbox/, then tells the human how it's going. This is the most direct human–agent collaboration entry point.

### External Agent

**After onboarding**: Scan inbox/ for TASK with ASSIGNEE=you → pick up → code → REPORT → outbox/

**Rules**: Git commands strictly forbidden. Block? Write BLOCKING.

> **External Agents can be human–AI pairs**: behind an External Agent label could be pure AI, or a human developer + AI partner working together. The human reads the REPORT in an IDE, writes code, has the AI generate the diff, then submits. The framework doesn't distinguish — it only cares whether the file format is correct.

### Sub-Agent (Native)

**After onboarding**: Wait for TPM internal dispatch → code → deliver diff via internal channel → REPORT to outbox/ for audit → after completion, read the next TASK with ASSIGNEE=you from inbox/

**Rules**: Can read/write all collaboration files but cannot proactively scan. Git commands strictly forbidden. Must not modify files outside your responsibility. Context provided by `context/{name}-memory.md`.

---

## 11. Onboarding Process

1. Confirm your role (TPM / External / Sub-Agent / Reviewer), write first log entry
2. Follow `REGISTER.md` to answer questions and fill in the registration action table
3. TPM confirms, moves to `ACTIONS.md`; onboarding complete

**Reporter is not a standalone role** — any role can double as one. When you submit a `PROACTIVE_REPORT`, you are the Reporter.

**Human-AI pair Agents (TPM and External Agent) should additionally read** `templates/DECISION_NNN_DATE_AUTHOR.md` after onboarding to understand the decision recording format. Sub-Agents do not need this.

---

### Memory Management — How Each Agent Type Persists Rule Knowledge

**Core principle: the framework rules are the same, but how each Agent remembers them differs.** The `context/` directory has only one role in AgentCharter: preparing context injection files for Native Sub-Agents.

| Agent Type | Memory System | Maintained By |
|-----------|---------|---------|
| **TPM** | Runtime environment's local memory (Reasonix memory, Claude project memory, etc.) | TPM self |
| **External Agent** | Same — their own local memory system. Write the framework's key rules into memory immediately after onboarding | Each Agent self |
| **Sub-Agent (Native)** | `context/{name}-memory.md` — TPM injects before every session | TPM |
| **Reviewer** | `context/reviewer-memory.md` — same as above | TPM |

**Example**: You are a TPM running in Reasonix. After onboarding, persist the key rules into your local memory (the memory directory managed by `reasonix.toml`). You are an External Agent running in Cursor — write key rules into your IDE rules file. A Sub-Agent cannot do this — so the TPM prepares `context/` files on its behalf.

---

## 12. Quick Reference

| I want to... | Action |
|---------|------|
| Claim identity | Read 👑 → You are TPM: sign → read `TPM.md` / You are not TPM → read `REGISTER.md` |
| Get a task | Check `ACTIONS.md` for your dispatch row → scan inbox/ or wait for internal dispatch |
| Submit a report | Write `outbox/REPORT_NNN_DATE_AUTHOR.md` |
| Submit a proactive report | Write `outbox/PROACTIVE_REPORT_NNN_DESC_DATE_AUTHOR.md` |
| Record a decision | Write `decisions/DECISION_NNN_DATE_AUTHOR.md` (human-AI pair) |
| Write a review conclusion | Write `reviews/REVIEW_REPORT_NNN_DATE_AUTHOR.md` with file:line + severity |
| Report a block | Write `outbox/BLOCKING_NNN_DATE_TARGET.md` (state the unblock condition) |
| Resolve a block | Write `outbox/BLOCKING_REPLY_NNN_DATE_AUTHOR.md` |
| Write a log | Append to `logs/{identifier}-log.md` |
| Check a template | Read the corresponding file in `templates/` |
| Pick up a revision | Check inbox/REVISION_NNN → read corresponding REVIEW_REPORT → fix → write REPORT_NNN_R1 (copy [Review Summary] from previous round + append fix response) |
| Pick up a test task | Check inbox/TASK_TEST_NNN → run tests → write `outbox/TEST_REPORT_NNN_DATE_AUTHOR.md` |
| Check backlog | Read TODO files in `todos/` |
| See progress (human) | Read `dashboard.md` |

---

## 13. Framework Upgrades

AgentCharter version upgrades don't need installers or migration scripts. The framework is pure files — templates, rules, and principles are all readable and editable. **The user tells the TPM one sentence; the TPM handles the rest.**

### User Operation

```
You are TPM. Read the latest AgentCharter repository, compare it to our project, and apply the updates.
```

### What the TPM Does Automatically

1. Reads the upstream `collaboration/` directory (templates, README, TPM.md, etc.)
2. Compares against the project's own `collaboration/` and lists differences
3. Creates a TASK for each change (new templates, rule changes, new directories, etc.)
4. Executes the changes — copies templates, updates docs, creates directories. **Core principle: merge, don't overwrite.** New templates are copied directly. New rule sections are inserted into documents — never overwrite user-customized PROJECT.md, ACTIONS.md, CHARTER.md, or other instance files
5. Confirms with the human for anything affecting project-level decisions (e.g., enabling human-AI pair mode)
6. Writes a REPORT when done, and archives

### Why This Works

AgentCharter's "installation" is fundamentally `cp -r collaboration/`. Upgrades are fundamentally the TPM reading upstream files and applying diffs. No runtime, no database migrations, no API version compatibility issues — just Markdown files and an Agent that understands the protocol.

**Key distinction: framework specs vs project instances**. The TPM must distinguish these two categories during an upgrade:

| Mergeable Updates (Framework Specs) | Never Overwrite (Project Instances) |
|------|------|
| `templates/` — add new templates | `PROJECT.md` — user's populated project config |
| `README.md` — insert new rule sections | `ACTIONS.md` — user's configured collaboration links |
| `TPM.md` — insert new principles and capabilities | `CHARTER.md` — user's signed project charter |
| | `REGISTER.md` — existing onboarding records |
| | `dashboard.md` — user's live project dashboard |

> 📂 **Real-world reference**: The wolf-judge project was the first external instance to complete a v3.2 → v3.3 upgrade. Its TPM independently scanned upstream, evaluated diffs (5 adopted, 2 declined), and submitted a full upgrade report. Available in the AgentCharter repo under `practices/`.
