# PROJECT: Wolf Judge

> Maintained by the TPM. Records basic project info, team members, tech stack, and build commands.
> General collaboration framework: see `README.md`.

---

## Project Info

- **Name**: Wolf Judge (Werewolf Judge Assistant)
- **Version**: v2.0
- **Tech Stack**: Frontend Vue 3 + TypeScript / Backend Rust + Tauri

## Team Members

| Role | Identifier | Type | Notes |
|------|------|------|------|
| TPM | Kimi | Native Host | Task Planning Manager, also Native Sub-Agent host |
| External Agent | flash | External | Frontend development, testing, special review |
| Sub-Agent | Peter | Native | Backend Rust development |
| Sub-Agent | Jim | Native Sub-Agent (resident) | Backend Rust development, **dual-role as CodeReviewer** |
| External Agent | buddy | External | Tester, manual and end-to-end testing |
| External Agent | Designer | External | Frontend visual/interaction review, design proposals, **dual-role as Reporter** (proactive reports) |

## Build Commands

| Type | Command |
|------|------|
| Frontend type check | `vue-tsc --noEmit` |
| Frontend build | `vite build` |
| Backend check | `cargo check` |
| Backend test | `cargo test` |

## Project-Specific Rules

1. **Frontend/backend division**: Frontend handles UI/animation; backend Rust manages state/logic/storage; IPC is the sole bridge
2. **TypeScript strict types**: core modules forbid `any`
3. **Backend IPC interface**: 44 IPC commands (`docs/tech/ipc-contract.md`)
4. **Dual review**: any code must be reviewed by another AI before merging
5. **Native Sub-Agent communication**: Peter/Jim can read/write all collaboration files (same as External Agents), following the loop-reading rules specified in their memory files

### Discipline Red Lines

| Rule | Description | Scope |
|------|------|---------|
| **Git Ban** | Any agent strictly forbidden from any git command (status, log, diff, checkout, restore, reset, stash, etc.), absolute, no whitelist | All agents |
| **Frontend Isolation** | Peter must not modify any frontend files (api/index.ts, views/, components/, stores/, etc.) | Peter |
| **Boundary Report** | Workspace issues, permission problems — immediately report to Kimi; do not resolve autonomously | Peter, Jim |

### Review Division

| Producer | Code Review | Design Review | Final Decision |
|--------|---------|---------|---------|
| Peter | Jim (CodeReviewer) | — | Kimi |
| flash | Jim (CodeReviewer) | Designer | Kimi |
| Designer | — | Kimi | Kimi |

**Cross-module changes** (IPC/data structures/shared models): Jim review → flash special review → Kimi final decision

---

## Instance-Specific Rules

### Dashboard & Archive

| Rule | Setting | Notes |
|------|------|------|
| Dashboard update frequency | **Daily** (not real-time) | Updated alongside daily patrol |
| Archive retention period | By file type (see README.md §3.6) | TASK/REVISION archived immediately after pickup; REPORT/REVIEW_REPORT kept 1 day; NOTICE archived promptly |
| Report format | Maintain detailed template format | Ensures traceability and human readability |

### Task Dispatch Principles

**Core goal**: Keep agents busy, but prevent Sub-Agent timeout.

| Agent | Strategy | Notes |
|-------|------|------|
| **Peter** (Native Sub-Agent) | **Minimize** | Sub-agents unstable, prone to timeout. Keep 1-2 active tasks |
| **flash** (External) | **Can be more** | Stable, can handle multiple parallel tasks |
| **Jim** (Native Sub-Agent) | Wake on demand | Not dispatched through inbox; Kimi wakes after code production |
| **Designer** (External) | **Active assignment** | Different from flash's passive pickup. Kimi actively assigns design tasks; Designer submits proactive reports on completion |

**Dispatch principles**:
1. **Active dispatch** — Immediately assign new tasks when inbox is empty
2. **At least 2 each** — Ensure each member has ≥2 tasks (except Peter)
3. **No upper limit** — flash and Designer have no cap
4. **Confirmed needs first** — All confirmed requirements must be dispatched as tasks with priority to avoid forgetting
5. **Task granularity** — Break down complex scenarios (1-2 days deliverable); keep simple scenarios intact

## Development Model

**Agile Incremental**

| Principle | Description |
|------|------|
| Iteration cycle | **No fixed Sprint**; dashboard-driven; task completes → deliver |
| Design baseline | `PRODUCT_DESIGN` / `INTERACTION_SPEC` / `USER_FLOWS` as baseline reference; changes go through lightweight review (Kimi fast approval) |
| Task granularity | TPM judges case by case; complex split fine, simple kept complete |
| Delivery cadence | Continuous flow; no batch review; complete → review → merge |
| Change control | CHANGE_REQ heavy process abolished; design/requirement changes evaluated and dispatched directly by Kimi |
