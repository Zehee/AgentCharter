# AgentCharter

> File-based governance for multi-agent teams.

A file-driven, multi-agent collaboration framework. Agents communicate through directory structure, naming conventions, and a collaboration link table — no platform or protocol dependencies.

**AgentCharter is not egalitarian.** It uses a **centralized dispatch model** — the team has one supreme manager (TPM) who oversees, orchestrates, and decides. Other Agents report to them. This differs fundamentally from the "peer-to-peer agents" paradigm of AutoGen or CrewAI.

---

## Quick Start

### 1. Copy the framework into your project

```bash
cp -r collaboration/ /my-project/
```

### 2. Tell your core Agent one sentence

```
You are TPM. Analyze the collaboration directory and initialize.
```

The TPM will analyze the directory structure, read the docs, understand the framework, then:
1. Sign their name in the 👑 section
2. Fill in `PROJECT.md` (team config, tech stack, build commands)
3. Fill in `CHARTER.md` (cooperation charter — a summary of all rules)
4. Move `CHARTER.md` to the project root

You never need to touch another file.

### 3. How do other Agents join?

Tell other Agents:

```
Analyze the collaboration directory and onboard.
```

The Agent reads `collaboration/README.md` → 👑 already has the TPM's name → follows `REGISTER.md` to self-onboard. No intervention needed.

---

## Why AgentCharter?

AI multi-agent collaboration currently has three mainstream approaches. AgentCharter is the fourth.

### Comparison

| | Manual Dispatch | Orchestration Frameworks | Shared Session | **AgentCharter** |
|--|---------|---------|---------|-----------------|
| **Example** | You manually direct in ChatGPT/Claude | AutoGen, CrewAI | Multiple Agents chatting in the same IDE | — |
| **Workflow Definition** | Verbal every time | Code (`RoundRobinGroupChat`) | Undefined, ad-hoc | **File (ACTIONS.md table)** |
| **Coordination Overhead** | High (you are the router) | Low (code auto-routes) | None | **Zero (files ARE the routing)** |
| **LLM Cost** | Every round burns all | Every round burns all | Single context, all consume | **Zero coordination calls** |
| **Audit Trail** | Chat logs, hard to search | Memory, lost on close | Single context, messy | **Filesystem, Git-searchable** |
| **Cross-model** | Platform-dependent | SDK-dependent, model-locked | IDE-dependent, runtime-locked | **Zero binding to any model or platform** |
| **Human Presence** | Forced full-time | Set initial params only | Spectator | **Read files anytime, intervene anytime** |
| **Workflow Customization** | Flexible but unstructured | Limited by framework API | Unstructured | **Edit one table = change the whole chain** |
| **Agent Independence** | None | Bound to host process | Same process, cross-interference | **Fully independent execution** |
| **Runtime Location** | Same platform | Same process/network | Same IDE | **Any environment, any physical location, cross-region** |

### Core Advantages

**1. Files are the route. Zero coordination overhead.**

Other frameworks consume LLM tokens just to coordinate — deciding "who speaks next" costs an inference round. AgentCharter delegates this to the filesystem: an Agent writes a file to a directory; downstream Agents discover it by scanning. Zero-token routing.

**2. The collaboration chain is one table — that you never need to write.**

AutoGen's `GroupChat` and CrewAI's `SequentialProcess` require you to write Python to define flows. AgentCharter goes further: you don't even maintain the table. Just discuss the workflow with the TPM — "Bob writes code, Alice reviews, Charlie cross-checks" — and the TPM understands, updating ACTIONS.md accordingly:
```
| Review | Alice → Bob   | REPORT → REVIEW_REPORT |
| Review | Charlie → Bob | REPORT → REVIEW_REPORT | (cross-module)
```

**3. The full audit trail lives in Git, not in memory.**

Other frameworks' communication vanishes when the session ends. AgentCharter's inbox/outbox/reviews/logs are all files. A human can `git log -- collaboration/archive/` to trace any decision chain, any time.

**4. Zero binding to model, platform, or IDE.**

An External Agent can run on any AI tool that reads and writes files — Claude Code, Cursor, terminal CLI. AgentCharter doesn't care who you are; it only cares about the files.

**5. Agents can run anywhere.**

An External Agent doesn't need to share the same IDE, machine, or even country with the TPM. The communication medium is files — as long as an Agent can read and write to the filesystem, it participates. Your frontend Agent on Cursor, backend Agent on a terminal CLI, test Agent on a CI machine — they talk through the same `collaboration/` directory, unaware of and indifferent to each other's location.

---

### How does this compare to MCP?

Many first-time observers ask: "Isn't this just a file-based MCP?"

**Similarity**: both are protocols that enable AI-to-AI interaction, both pursue cross-platform and cross-model compatibility. AgentCharter's registry concept (REGISTER.md → ACTIONS.md) is structurally similar to MCP server registration.

**Fundamental difference**:

| | MCP | AgentCharter |
|--|-----|-------------|
| **Problem solved** | How an Agent calls **external tools** | How Agents **collaborate with each other** |
| **Communication** | Agent ↔ Tool (vertical) | Agent ↔ Agent (horizontal) |
| **Core concept** | Server exposes Tools/Resources/Prompts | TPM dispatches TASKs, executors submit REPORTs |
| **Workflow** | None (each call is independent) | Full lifecycle (TASK → REPORT → Review → Archive) |
| **Human intervention** | Not in scope | File channel natively supports human reading and intervention at any time |
| **Transport** | JSON-RPC over stdio/HTTP | Filesystem (anything that can read/write files) |
| **Runtime** | Requires a running MCP Server process | **Zero runtime — no server process needed** |

**In one sentence**: MCP teaches an Agent to use hammers and saws. AgentCharter forms a crew — someone draws the blueprint (TPM), someone builds (Sub-Agent), someone inspects (Reviewer). All instructions and reports are files on the construction site, and the foreman can flip through them anytime.

---

### Extensibility: the framework grows with your team

AgentCharter's templates and rules are not frozen — they are files maintained by the TPM, living in `collaboration/`.

If your workflow needs a **new node type** (e.g., "security audit" after all P3 tasks), **new state transitions** (e.g., "awaiting client approval" → "reopened"), or **new file templates** (e.g., `SAFETY_REPORT`), don't wait for a framework release. The process is:

```
You → tell the TPM: "We need a new X, like existing Y, but with an extra Z field"
  → TPM reads templates/ to understand the spec → mimics an existing template to create the new one
  → TPM updates ACTIONS.md with the new link row
  → TPM updates TPM.md with the new rule
  → The new flow takes effect from the next TASK
```

**The framework provides the blueprint and constraints; the TPM derives as needed.** The 14 templates and 12 chapters of rules in this repo grew out of 120+ tasks in the wolf-judge project — your project will grow its own variants too.

---

## Philosophy: TPM-Centric

AgentCharter is built around the **TPM (Task Planning Manager)** — a centralized scheduling model.

### T-P-M: Three Dimensions, One Brain

| Dimension | Letter | Meaning | Manifestation |
|------|------|------|----------|
| **Task** | T | Creation and orchestration of tasks | Creates TASKs, assigns to the right Agent, drives state transitions (ASSIGNED → REVIEW_PENDING → DONE) |
| **Planning** | P | Planning and constraints | Operates in plan mode, generates task manifests, defines acceptance criteria, code standards, review levels (P0-P3) |
| **Manager** | M | Approval and coordination | Monopolizes final review authority and Git operations, coordinates Native Sub-Agents and External Agents |

### Collaboration Topology

```
                    ┌──────────────────────────────┐
                    │  TPM (Task Planning Manager)  │
                    │                              │
                    │    Task · Planning · Manager  │
                    │    Only Git access · Final    │
                    └──────────┬───────┬───────────┘
                               │       │
               File Channel    │       │  Internal Channel
          (inbox/outbox)       │       │  (realtime diff/review)
                               │       │
                    ┌──────────┘       └──────────┐
                    ▼                              ▼
         ┌──────────────────┐        ┌──────────────────┐
         │  External Agent   │        │ Sub-Agent (Native)│
         │                  │        │                  │
         │  Independent env  │        │  Same runtime,    │
         │  Scans inbox for  │        │  background       │
         │  tasks            │        │  Waits for TPM    │
         │  Files REPORT     │        │  Delivers diff    │
         └──────────────────┘        └──────────────────┘
```

**In one sentence**: The TPM is the only Agent with global awareness — they don't write code. They manage "who does what, how, and is it done." All communication passes through them; all code is approved by them.

### Workflows are not hardcoded

AgentCharter has **no hardcoded workflows**. The topology above is just the simplest example — your team can be entirely different.

The real definition of collaboration relationships lives in `ACTIONS.md`. It's a freely editable table:

```
| Action     | From → To     | Channel        |
| Assign     | TPM → Alice   | inbox/TASK     |
| Review     | Bob → Alice   | REVIEW_REPORT  |
| Report     | Alice → TPM   | outbox/REPORT  |
| ...        | Anyone → Anyone | Any channel  |
```

**You can**:
- Let a Reviewer directly review code authors without routing through TPM
- Set up serial review chains for cross-module changes (A reviews → B reviews → TPM decides)
- Give a single Agent dual roles as both "developer" and "reviewer"
- Let Agents review each other directly, with TPM only notified on ACCEPT

**The essential difference from fixed-workflow frameworks**: AutoGen's `RoundRobinGroupChat` and CrewAI's `SequentialProcess` require you to configure flows in code. AgentCharter uses ACTIONS.md as a contract — change one row, change one collaboration channel. Team members read the table and instantly know their upstream and downstream, without understanding the whole picture.

---

## Repository Structure

```
AgentCharter/
├── collaboration/                # ← Framework core (copy to user project root)
│   ├── README.md                     # Agent-side specification (12 chapters)
│   ├── CHARTER.md                     # Charter template (TPM fills, then moves to project root)
│   ├── TPM.md                         # TPM code of conduct
│   ├── PROJECT.md                    # Project config (fill-in template)
│   ├── REGISTER.md                   # Registration form
│   ├── ACTIONS.md                    # Collaboration link table (empty template, TPM maintains)
│   ├── dashboard.md                  # Dashboard — progress report for humans, maintained by TPM
│   ├── templates/                    # 14 file templates
│   ├── context/                      # Context memory files
│   ├── inbox/ outbox/ reviews/ logs/ todos/ archive/
│
├── collaboration_en/             # ← Same as above, English version
│
├── practices/                    # ← Community practice cases
│   └── wolf-judge/                   # 5-person team, full-stack case study
│
├── CHANGELOG.md
├── LICENSE (MIT)
└── README.md                     # This file
```

> **Deployment**: copy only `collaboration/` (or `collaboration_en/` for English) to your project root.
>
> **`.gitignore`**: exclude runtime communication directories (inbox/, outbox/, logs/, reviews/, context/, todos/). **Keep `archive/` in Git** — completed TASKs, REPORTs, and REVIEW_REPORTs are permanent audit trails. Framework files (TPM.md, README.md, etc.) are tracked normally.

---

## Core Concepts

### Three Roles

| Role | Core Responsibility | Communication |
|------|---------|---------|
| **TPM** (Task Planning Manager) | Task dispatch, plan orchestration, architecture decisions, Git operations, final approval | File channel + Internal channel |
| **External Agent** | Coding, testing, reviewing | File channel (inbox/outbox) |
| **Sub-Agent (Native)** | Coding (focused on specific tech stack) | Internal channel + File channel |

### File Exchange Protocols

The framework provides two file exchange modes, but **actual collaboration flows are defined by `ACTIONS.md`**:

**Task-driven**: TPM creates TASK → inbox/ → Agent picks up → codes → REPORT → ACTIONS.md-defined review chain → Archive
**Proactive Report**: Anyone submits a report → TPM decides → Archive

### Core Rules

| Rule | Description |
|------|------|
| Dual Review | Any code must be reviewed by another AI before merging |
| Git Isolation | Only the TPM can execute git commands |
| Files are the Contract | No file = it didn't happen |
| Append-Only Logs | Never modify history |

---

## Practice Cases

Frameworks are abstract; practice cases show real configurations.

| Case | Team Size | Tech Stack | Highlights |
|------|---------|--------|------|
| [wolf-judge](./practices/wolf-judge/README.md) | 5 | Tauri + Rust + Vue 3 | P0-P3 tiered review, Sub-Agent context memory, 120+ tasks closed |

> Contributions welcome. See `practices/README.md`.

---

## How It Works for Agents

Agents don't need to understand this repo — their entry points are the project root `CHARTER.md` (the cooperation charter, moved from `collaboration/` by the TPM during initialization) and the files in `collaboration/`.

TPM arrival: reads `collaboration/README.md` → signs 👑 → fills `CHARTER.md` + `PROJECT.md` → moves `CHARTER.md` to project root. Reads `TPM.md` → takes command.

Other Agent arrival: reads root `CHARTER.md` (global rules) → reads `collaboration/README.md` → 👑 is not them → reads `REGISTER.md` → self-onboards.

See `collaboration/README.md` for the full Agent-side specification (12 chapters).

---

## User's Project Structure (After Initialization)

```
my-project/
├── CHARTER.md                   # ← Global charter (TPM moved from collaboration/)
├── collaboration/               # ← Framework core
│   ├── README.md                    # Agent-side spec
│   ├── TPM.md                       # TPM rules
│   ├── PROJECT.md                   # Project config (filled)
│   ├── REGISTER.md                  # Registration
│   ├── ACTIONS.md                   # Link table (configured)
│   ├── dashboard.md                 # Human dashboard
│   ├── [runtime dirs]               # inbox/ outbox/ reviews/ logs/ ...
│
├── src/                          # Your source code
└── .gitignore                    # collaboration runtime dirs excluded
```

---

## License

MIT License — see `LICENSE`.

---

> 📖 中文版见 [README_CN.md](./README_CN.md)
