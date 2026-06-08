# AgentCharter

> 🗂️ File-based governance for multi-agent teams.

[English](./README.md) · [中文](./README_CN.md)

A file-driven collaboration framework where AI Agents communicate through a shared directory — no SDK, no server, no platform lock-in. **Drop in `collaboration/`, tell your Agent it's the TPM, done.**

---

## 🚀 Quick Start

### 1. Copy

```bash
cp -r collaboration_en/ /my-project/
```

### 2. Tell your core Agent

> Paste this directly into your AI — wherever you normally talk to it (IDE chat, terminal, web). Yes, it's that simple.

```
You are TPM. Read the collaboration directory and start working.
```

The TPM reads the framework, signs 👑, fills `PROJECT.md` + `CHARTER.md`, and moves the charter to your project root. **That's it.**

<details>
<summary>👇 What exactly happens when you say that?</summary>

The Agent reads `collaboration/` and discovers:
1. **👑 signs itself in** — replaces the placeholder in `README.md` with its name
2. **Fills `PROJECT.md`** — asks you for the project name, tech stack, build commands, team members
3. **Fills `CHARTER.md`** — summarizes key rules from `README.md` and `TPM.md` into the cooperation charter
4. **Moves `CHARTER.md` to project root** — now every Agent (including humans) can read the supreme rules
5. **Reads `TPM.md`** — learns its full authority: dispatch tasks, drive reviews, own Git, update dashboard

From this point forward, no Agent touches `src/` without a `TASK` file. No Agent runs `git` except the TPM. Everything is a file in `inbox/` → `outbox/` → `reviews/` → `archive/`.

</details>

### 3. Bring in more Agents

> Same thing — paste this to each new Agent:

```
Read the collaboration directory and join the team.
```

They read 👑, see they're not TPM, follow `REGISTER.md` to self-onboard. You never touch a file again.

---

## 🧠 How It Works

AgentCharter is built around one central role — the **TPM (Task Planning Manager)**. The TPM doesn't write code. It plans, dispatches, reviews, and reports.

### Three Roles, One Brain

| Role | Nature | Responsibility |
|------|--------|----------------|
| 👑 **TPM** | Your project's manager Agent | Breaks down work into TASK files, assigns them, drives reviews, owns Git, updates the human dashboard |
| 📁 **External Agent** | Runs anywhere, any tool | Scans `inbox/` for TASKs with their name, codes, submits REPORT files |
| 🔗 **Sub-Agent (Native)** | Background worker, same runtime | Waits for TPM dispatch, delivers code diffs directly, drops REPORT files for audit |

### T-P-M: What the TPM Actually Does

| | T · Task | P · Planning | M · Manager |
|--|----------|-------------|------------|
| **Creates** | TASK files in inbox/ | Task manifests with acceptance criteria | Collaboration link table (ACTIONS.md) |
| **Drives** | State transitions (ASSIGNED → REVIEW_PENDING → DONE) | Code standards, review levels (P0–P3) | Review loops, final approvals, Git commits |
| **Maintains** | Patrol outbox/ for new REPORTs | Dashboard for humans, Sub-Agent context memory | Archive, Agent onboarding, framework extensions |

```
                         ┌────────────────────────────────┐
                         │   TPM (Task Planning Manager)   │
                         │     Task · Planning · Manager   │
                         │     Only Git access · Final     │
                         └───────────┬────────┬───────────┘
                                     │        │
                     File Channel    │        │  Internal Channel
                     (inbox/outbox)  │        │  (realtime diff/review)
                                     │        │
                         ┌───────────┘        └───────────┐
                         ▼                                ▼
              ┌───────────────────┐          ┌───────────────────┐
              │   External Agent  │          │ Sub-Agent (Native) │
              │  Independent env  │          │  Background worker │
              │  Scans inbox for  │          │  Waits for TPM     │
              │  tasks · REPORTs  │          │  Delivers diff     │
              └───────────────────┘          └───────────────────┘
```

### Workflows Are Defined by a Table, Not Code

The collaboration chain is a single file — `ACTIONS.md`. Add a row, add a channel:

| Action   | From → To      | Channel        |
|----------|----------------|----------------|
| Assign   | TPM → Alice    | inbox/TASK     |
| Review   | Bob → Alice    | REVIEW_REPORT  |
| Report   | Alice → TPM    | outbox/REPORT  |

Change one row, change one collaboration channel. Agents read the table and know exactly who they talk to and how. No Python scripts, no framework API calls.

---

## 📊 How It Compares

| | Manual Dispatch | AutoGen / CrewAI | MCP | **AgentCharter** |
|--|-----------------|-------------------|-----|-----------------|
| **What it does** | You route tasks by hand | Agents auto-chat via code | Agent↔Tool (vertical) | Agent↔Agent (horizontal) |
| **Workflow defined by** | Verbal ad-hoc | Python scripts | Server config | **ACTIONS.md table** |
| **Coordination cost** | Your time | LLM tokens per round | Server runtime | **Zero — files ARE the routing** |
| **Audit trail** | Chat logs | Memory, lost on close | None | **Filesystem, Git-searchable** |
| **Cross-model** | Platform-locked | SDK-locked | Protocol-locked | **Anything that reads/writes files** |
| **Workflow flexibility** | Unstructured | Limited by framework API | None (stateless) | **Edit a table row** |
| **Agents can run…** | Same platform | Same process/network | Needs live server | **Anywhere — cross-machine, cross-region** |

**In one sentence**: MCP teaches an Agent to use tools. AgentCharter forms a crew — blueprint (TPM), build (Sub-Agent), inspect (Reviewer) — and every instruction is a file the foreman can flip through anytime.

### 🔧 The Framework Grows with Your Team

Need a new TASK type? A new state? A new template? Tell the TPM. It reads `templates/`, mimics the pattern, updates `ACTIONS.md`, and the new flow takes effect on the next task. No framework release needed. The 14 templates and 12 chapters in this repo grew out of 120+ real-world tasks — yours will too.

---

## 📚 Practice Cases

See it working in a real project:

| Case | Team | Stack | Highlights |
|------|------|-------|------------|
| [wolf-judge](./practices/wolf-judge/README_en.md) | 5 Agents | Tauri + Rust + Vue 3 | P0–P3 tiered review, Sub-Agent memory injection, 120+ tasks closed — [see real files](./practices/wolf-judge/examples_en/) |

---

## 📦 File Hierarchy (Highest → Lowest)

```
/CHARTER.md              ← Project charter — authored by TPM from template, moved to root; supreme rules for all Agents
/collaboration/
  ├── README.md          ← Agent operating manual — defines rules and processes, not project-specific decisions
  ├── TPM.md             ← TPM code of conduct
  ├── PROJECT.md         ← Project config
  ├── REGISTER.md        ← Agent registration
  ├── ACTIONS.md         ← Collaboration link table
  └── inbox/ outbox/ reviews/ logs/ ...  ← Runtime communication space
```

> **Key distinction**: `collaboration/README.md` defines "how to collaborate"; `/CHARTER.md` defines "what our specific project chose".

## 📦 Repository Structure

```
AgentCharter/
├── collaboration/           # Framework core (CN) — copy to your project root
│   ├── README.md                # Agent-side spec (12 chapters)
│   ├── CHARTER.md               # Charter template → moved to root by TPM
│   ├── TPM.md                    # TPM code of conduct
│   ├── PROJECT.md               # Project config (fill-in)
│   ├── REGISTER.md              # Agent registration
│   ├── ACTIONS.md               # Collaboration link table (empty template)
│   ├── dashboard.md             # Human-readable progress report
│   ├── templates/               # 14 file templates
│   └── inbox/ outbox/ reviews/ logs/ todos/ archive/
│
├── collaboration_en/        # Same as above, English
├── practices/               # Community practice cases
│   └── wolf-judge/              # 5-person team, full-stack
│
├── .github/                 # Issue & PR templates
├── CHANGELOG.md
└── LICENSE (MIT)
```

> **Deployment**: copy `collaboration/` (CN) or `collaboration_en/` (EN) to your project root.
>
> **`.gitignore`**: Add `inbox/ outbox/ logs/ reviews/ context/ todos/` — these are runtime state. Tracking them causes harm (`git checkout` would roll back live task assignments and review progress). **But keep `archive/` in Git** — completed TASKs, REPORTs, and REVIEW_REPORTs are permanent audit trails. Framework files (`TPM.md`, `README.md`, etc.) are tracked normally.
>
> **After initialization**, your project looks like:
> ```
> my-project/
> ├── CHARTER.md              # ← Global charter (moved by TPM)
> ├── collaboration/          # ← Framework (Agent workspace)
> ├── src/                    # ← Your code
> └── .gitignore
> ```

---

## 📋 License

MIT — see [LICENSE](./LICENSE).
