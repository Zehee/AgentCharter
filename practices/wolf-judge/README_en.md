# Practice: Wolf Judge (wolf-judge-assistant)

> 5-person team · Tauri v2 + Rust + Vue 3 · Desktop app · 120+ tasks closed
>
> This case demonstrates a **frontend/backend split, multi-Agent hybrid type** collaboration paradigm.
>
> 📂 [See real file examples](./examples/) — TASK_113 → REPORT_113 → REVIEW_REPORT_113 + ACTIONS.md + PROJECT.md + dashboard.md

---

## 1. Project Background

**Wolf Judge** is a desktop assistant for the Werewolf party game, helping manage rounds, roles, voting, and replays. Tech stack: Tauri v2 (desktop shell) + Rust (backend state machine) + Vue 3 (frontend UI).

Why AgentCharter: the project has clear frontend/backend division and multiple Agent runtime environments, requiring a framework that lets multiple AIs collaborate in the same codebase without stepping on each other.

---

## 2. Role Setup & Responsibility Matrix

### 2.1 Team Landscape

```
                           ┌──────────────────────────────┐
                           │         Kimi (TPM)            │
                           │  Native Host · Only Git Access│
                           │  Decide · Dispatch · Approve  │
                           └────────┬──────────┬──────────┘
                                    │          │
                   ┌────────────────┼──────────┼──────────────────┐
                   │                │          │                  │
                   ▼                ▼          ▼                  ▼
         ┌─────────────────┐ ┌──────────┐ ┌──────────┐ ┌─────────────────┐
         │ flash (External) │ │  Peter   │ │   Jim    │ │Designer(External)│
         │ Frontend Vue/TS  │ │ (Native) │ │ (Native) │ │  Visual Review   │
         │  Special Review  │ │ Backend  │ │ Backend  │ │   + Reporter     │
         └───────┬─────────┘ └────┬─────┘ │CodeReview │ └───────┬─────────┘
                 │               │       └────┬─────┘         │
                 │               │            │               │
                 ▼               ▼            ▼               ▼
         ┌────────────────────────────────────────────────────────────┐
         │                     buddy (External)                       │
         │              Manual Testing · E2E Verification             │
         └────────────────────────────────────────────────────────────┘
```

### 2.2 Role Responsibility Table

| Agent | Type | Runtime | Core Responsibility | Double Role |
|-------|------|--------|----------|----------|
| **Kimi** | TPM (Native Host) | Current IDE | Task dispatch, architecture decisions, Git, final approval, archive | Sub-Agent host |
| **flash** | External Agent | Independent env | Vue 3 components, TypeScript, UI/UX, frontend testing, cross-module review | — |
| **Peter** | Native Sub-Agent | Same IDE, bg | Rust backend, state machine, SQLite, IPC commands | — |
| **Jim** | Native Sub-Agent | Same IDE, bg | Rust backend, database migrations | **CodeReviewer** (reviews all code) |
| **Designer** | External Agent | Independent env | Frontend visual review, interaction analysis, design proposals, UI specs | **Reporter** (proactive reports) |
| **buddy** | External Agent | Independent env | Manual testing, regression validation, E2E execution | — |

### 2.3 Why This Setup?

**Why is Peter a Native Sub-Agent?**
- Backend changes need realtime diff delivery to Kimi (internal channel is more efficient)
- Same runtime means Kimi can directly review diff quality, reducing file channel roundtrips

**Why is flash an External Agent?**
- Frontend development is stable and can handle multiple parallel tasks
- External Agents don't depend on Kimi's context, can run independently for long periods
- Frontend changes are frequent; the async file channel model fits better

**Why does Jim wear two hats?**
- Code review doesn't need continuous work; makes good use of idle time
- Review requires deep backend code understanding; having a backend developer double as reviewer makes the most sense
- Review conclusions delivered via internal channel to Kimi with zero latency

**Why is Designer a Reporter?**
- A designer's workflow is "discover → propose", not "claim task → code"
- Proactive report (read-and-burn) naturally matches the design review scenario
- Doesn't enter the standard task flow, doesn't occupy the inbox queue

---

## 3. Collaboration Relationship Map

### 3.1 Task Dispatch Flow

```
User needs / Kimi decision
        │
        ▼
    Kimi judges: whose job is this?
        │
        ├── Frontend → write inbox/TASK_NNN_xxx_FLASH.md → flash scans and picks up
        ├── Backend → internal channel dispatch + inbox/TASK record → Peter picks up
        ├── Testing → write inbox/TASK_TEST_NNN_xxx_BUDDY.md → buddy scans and picks up
        └── Design → user directly assigns → Designer submits PROACTIVE_REPORT on completion
```

### 3.2 Standard Task Lifecycle

```
  Kimi writes TASK
    │
    ▼
┌──────────┐    ┌──────────────┐    ┌────────────────┐
│ Dispatch │ → │ Executor picks│ →  │   Coding       │
│ inbox/   │    │ IN_PROGRESS  │    │  code + log    │
└──────────┘    └──────────────┘    └───────┬────────┘
                                            │
  ┌─────────────────────────────────────────┘
  │
  ▼
┌───────────────────┐
│ Executor writes   │
│ outbox/REPORT_NNN │
└───────┬───────────┘
        │
        ▼
┌─────────────────────────────────────────────────┐
│          Kimi determines review level            │
│                                                  │
│  P0 (UI/style only)│  P1-P3 (involves logic)    │
│       │                         │                 │
│       ▼                         ▼                 │
│  Kimi directly commits  Wake Jim (REPORT number)  │
│       │                         │                 │
│       │                         ▼                 │
│       │              Jim reads REPORT → reviews   │
│       │                         │                 │
│       │                 Writes REVIEW_REPORT      │
│       │                    to reviews/             │
│       │                         │                 │
│       │              ┌──────────┴──────────┐      │
│       │              │                     │      │
│       │         ✅ ACCEPT           🔴 Fix needed  │
│       │              │                     │      │
│       │              ▼                     ▼      │
│       │       Jim notifies Kimi   Executor reads   │
│       │       (internal channel)  fix → REPORT_R1  │
│       │              │           (with [Summary])  │
│       │              │                     │      │
│       │              │              Jim re-reviews │
│       │              │             loop til ACCEPT │
└───────┴──────────────┴─────────────────────────────┘
        │
        ▼
  Kimi commit → archive
```

### 3.3 Complete Collaboration Link Table

| Action | From → To | Channel | Notes |
|------|----------------|------|------|
| Assign Task | Kimi → flash | `inbox/TASK` | flash scans autonomously |
| Assign Task | Kimi → Peter | Internal channel + `inbox/TASK`(record) | Peter waits for injection |
| Assign Task | Kimi → buddy | `inbox/TASK_TEST` | buddy scans autonomously |
| Assign Design | User → Designer | Direct assignment | Not through inbox |
| Submit Report | flash → Kimi | `outbox/REPORT` | File channel |
| Submit Report | Peter → Kimi | Internal channel(diff) + `outbox/REPORT` | For audit |
| Submit Design Report | Designer → Kimi | `outbox/PROACTIVE_REPORT` | Read-and-burn |
| Submit Test Report | buddy → Kimi | `outbox/TEST_REPORT` | File channel |
| Wake Review | Kimi → Jim | Internal channel (REPORT number only) | Lightweight notice |
| Review Code | Jim → flash/Peter | `REPORT → REVIEW_REPORT` | Jim closes loop directly |
| Review Conclusion | Jim → flash/Peter | `reviews/REVIEW_REPORT` | Executor reads |
| Quality Confirmation | Jim → Kimi | Internal channel "ACCEPT notification" | Standardized format |
| P0 Pass | — | Kimi directly commits | No Jim involved |
| Blocking Notice | Any → Any | `outbox/BLOCKING` | Blocked party reads |
| Blocking Resolved | Resolver → Blocker | `outbox/BLOCKING_REPLY` | — |

### 3.4 Review Flow Diagram

```
          Code Producers                  Reviewer                Decision Maker
    ┌──────────────┐                ┌──────────────┐          ┌──────────────┐
    │    Peter     │───REPORT──────→│              │          │              │
    │   (Backend)  │                │     Jim      │─ACCEPT─→│    Kimi      │
    └──────────────┘                │  (CodeRev)   │          │    (TPM)     │
                                    │              │          │              │
    ┌──────────────┐                │   Writes     │          │   P0: direct │
    │    flash     │───REPORT──────→│  REVIEW      │          │   commit     │
    │  (Frontend)  │                │  _REPORT     │          │   P1-P3:     │
    └──────────────┘                └──────────────┘          │   approve    │
           │                                                   └──────────────┘
           │                                                          │
           └─── Cross-module? flash special review ←── Kimi ─────────┘

    Designer's track:
    ┌──────────────┐        PROACTIVE_REPORT        ┌──────────────┐
    │   Designer   │ ──────────────────────────────→ │    Kimi      │
    │   (Design)   │                                 │   Decide     │
    └──────────────┘                                 └──────────────┘
```

---

## 4. Custom Rules Explained

The rules below **evolved within this project instance** and are not mandated by the AgentCharter framework.

### 4.1 Discipline Red Lines

Hard constraints set for specific roles and the codebase structure:

| Rule | Content | Scope | Origin |
|------|------|----------|----------|
| **Git Ban** | Any agent strictly forbidden from any git command (status, log, commit, diff, checkout, etc.), absolute, no whitelist | All agents | Prevent agents from auto-committing incomplete code |
| **Frontend Isolation** | Peter must not modify any frontend files (`api/index.ts`, `views/`, `components/`, `stores/`, etc.) | Peter | History of multiple frontend violations |
| **Boundary Report** | Immediately report workspace issues and permission problems to Kimi; do not resolve autonomously | Peter, Jim | Sub-Agents lack global judgment |

### 4.2 Review Division Matrix

| Producer | Code Reviewer | Design Reviewer | Final Decision |
|--------|-----------|-----------|----------|
| Peter (Backend) | Jim (CodeReviewer) | — | Kimi |
| flash (Frontend) | Jim (CodeReviewer) | Designer | Kimi |
| Designer (Design) | — | Kimi | Kimi |

**Cross-module special flow** (new/modified IPC commands, data structure changes, shared model changes):
```
Jim code review → flash special review (frontend verification) → Kimi final decision
```

### 4.3 Task Dispatch Strategy

> Core goal: keep agents busy, but prevent Sub-Agent timeout.

| Agent | Strategy | Concurrency Limit | Notes |
|-------|------|----------|------|
| **Peter** (Native Sub-Agent) | Minimize | 1-2 | Native Sub-Agent context insufficient, prone to timeout |
| **flash** (External) | Can be more | Unlimited | Independent env, stable execution |
| **Jim** (Native Sub-Agent) | Wake on demand | Not through inbox | Kimi wakes after code production |
| **Designer** (External) | Active assignment | Unlimited | User assigns → completes → submits proactive report |

**Dispatch principles**:
1. Assign new tasks immediately when inbox is empty, keep things flowing
2. Every member should hold ≥2 tasks (except Peter)
3. Write all confirmed requirements as TASKs in the queue to avoid forgetting
4. Break complex tasks down to 1-2 days deliverable

### 4.4 P0-P3 Tiered Review

> This is an **instance-specific customization** of the framework's review mechanism.

| Level | Criteria | Review Depth | Kimi Cost |
|------|----------|----------|-----------|
| **P0** | Single file, pure UI/style/copy/formatting | No review, Kimi directly commits | 0 |
| **P1** | 2-3 files, component-level logic | Jim reviews → summary | 5-10 lines |
| **P2** | Cross-module, data flow, new IPC | Jim reviews → full report → Kimi confirms | Summary + opinion |
| **P3** | Architecture/security/core flow | Jim reviews → Kimi deep verification | Full engagement |

**P0 whitelist** (strict, prefer higher when in doubt): CSS adjustments, copy changes, icon replacement, layout tweaks, config non-logic changes, formatting

### 4.5 Archive Rules (Refined Edition)

Built on top of framework defaults, this instance evolved a **read-confirmation system**:

```
Intermediate files (TASK/REVISION/BLOCKING/TODO)
  → Archive immediately on completion; value has dropped to zero

End-of-flow files (REPORT/REVIEW_REPORT/NOTICE/REPLY)
  → External agent marks "✅ Read BY {AGENT} @ {DATE}" at file top
  → Kimi confirms all relevant parties have read → archive
  → Exception: files that only reach Kimi can be archived immediately
```

### 4.6 Sub-Agent Context Memory

Native Sub-Agents (Peter/Jim) lose context on IDE restart. Solution:

- Each Sub-Agent has `context/{name}-memory.md`, maintained by Kimi
- Content includes: project tech stack baseline, historical pitfall list, discipline red lines, review standards, active task status
- Kimi injects memory file **in full at the top of the prompt** every time a Sub-Agent is woken
- Storage cap: 8KB; when exceeded, archive old decisions to `*-memory-archive.md`

### 4.7 Review Summary Flow

Mechanism for solving Reviewer context instability across multiple review rounds:

```
R0: Jim writes REVIEW_REPORT ([Review Summary] = R0 score + issues)
  ↓
R1: Executor writes REPORT_R1 (copies R0 original, appends R1 fix responses)
  ↓ Jim reads REPORT_R1, no need to check prior round files
R1: Jim writes REVIEW_REPORT_R1 (copies R0 + appends R1 conclusion)
  ↓
... Loop until ACCEPT
  ↓ Kimi only reads the last round's summary; 3+ rounds triggers attention
```

### 4.8 Development Model

| Dimension | Setting |
|------|------|
| Iteration Cycle | No fixed Sprint; dashboard-driven; task completes → deliver |
| Design Baseline | Changes go through lightweight review (Kimi fast approval) |
| Delivery Cadence | Continuous flow; complete → review → merge |
| Change Control | Heavy process eliminated; Kimi evaluates and dispatches directly |

---

## 5. Project Data

| Metric | Value |
|------|------|
| Cumulative Tasks | 120+ |
| Cumulative Reviews | 60+ REVIEW_REPORTs |
| Code Scale | Rust ~15K lines / Vue ~20K lines |
| IPC Commands | 44 |
| Review Score Baseline | 8.5/10 |
| Backend Test Baseline | 98 pass (cargo test) |
| Collaboration Docs | 180+ files (inbox/outbox/reviews/logs/archive) |
| Active Period | 2026-05 to present (continuous iteration) |

---

## 6. Why This Case is Worth Referencing

1. **Mixed Agent type demonstration** — Uses both External Agents (flash/Designer/buddy) and Native Sub-Agents (Peter/Jim) in the same project, showing the collaboration differences
2. **CodeReviewer dual-role model** — Jim both writes backend code and reviews others' code, proving the "one person, two roles" model works
3. **Tiered review system** — P0-P3 four-level review is the core innovation, dramatically saving TPM decision cost
4. **Proactive reports for design review** — Designer skips the standard task flow, using Proactive Report for read-and-burn interaction
5. **Discipline red lines** — Hard constraints tailored to the specific codebase, demonstrating how the framework adapts to project-specific risks

---

## 7. Lessons Learned

### ✅ Patterns Proven Effective

- **Review direct loop closure** — Jim faces the executor directly, no routing through Kimi, saving massive context
- **Native Sub-Agent for backend dev** — Internal channel diff delivery in realtime, audit files hold only records
- **Context memory files** — The real pain-point solution for Native Sub-Agents

### ⚠️ Pitfalls Encountered

- **Sub-Agent timeout** — Native instances prone to timeout with insufficient context; keep to 1-2 active tasks
- **Frontend/backend IPC desync** — Cross-module changes easy to miss in review; added flash special review
- **Archive timing chaos** — No rules early on; later established "intermediate files archive immediately, end-of-flow wait for read"
- **Agent boundary violations** — Peter once modified frontend files; set hard bans afterwards
