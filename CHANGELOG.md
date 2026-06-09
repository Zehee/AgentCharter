# Changelog

Format based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).
This project follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Versioning Policy

- **`collaboration/README.md`** carries the runtime version (`v3.3`) — Agents see this. Updated on every release.
- **`CHANGELOG.md`** carries the full history with patch versions (`3.2.1`). The `[Unreleased]` section accumulates changes between releases.
- **Git tags** mark releases (e.g. `v3.2.1`).
- **`README.md` (outer)** is a marketing page — it does not carry a version number.

## [Unreleased]

### Added

- **Template validator CLI** (`extras/template-validator/`) — optional tool to validate 15 template formats and naming conventions
- **CHANGELOG automation script** (`extras/changelog-automation/`) — project-only tool to generate Keep a Changelog drafts from Git commits
- **wolf-judge examples index** (`practices/wolf-judge/examples/README.md`) — bilingual navigation page for real-world collaboration files
- **Deep analysis doc** (`docs/deep-analysis-20260609.md`) — systematic project scan: architecture, evolution, real-world validation, external audit
- **Evaluation doc** (`docs/evaluation-20260609.md`) — strengths, weaknesses, applicability, fundamental trade-offs
- **Management plan doc** (`docs/management-plan-20260609.md`) — three-phase execution roadmap if managed by Kimi
- **Governance sharding analysis** (`docs/governance-sharding-20260609.md`) — compression vs sharding strategies for rule governance as the framework scales

### Changed

- **Quick reference expanded** (`collaboration/README.md` §12 / `collaboration_en/README.md` §12) — added 3 entries: pick up revision, pick up test task, check backlog

## [3.3.0] - 2026-06-10

### Added

- **DECISION file type**: 15th template (`DECISION_NNN_DATE_AUTHOR.md`) — structured records of human-AI pair decisions with verbatim reasoning chains
- **collaboration-live/**: the framework's own collaboration instance — 9 DECISIONs, 12 TASKs, 2 TODOs, open to the community
- **Pair decision recording guidelines** in `collaboration/README.md` §6
- **TPM principle #10**: strategic decisions must be filed as DECISION files
- **`docs/decision-protocol.md`**: complete optional spec
- **`docs/deep-dive-20260609.md`**: 21-round dialogue analysis with DeepSeek

### Changed

- **Human-AI pair is now first-class**: TPM and External Agent explicitly labeled as "default human-AI pair." Sub-Agent (Native) as "pure AI"
- **Bidirectional reference chain**: TASK/PROACTIVE_REPORT/TODO all link back to DECISION files
- **README.md / README_CN.md rewritten**: "Trust, not control" philosophy front and center, human-AI pair narrative replaces framework-feature narrative
- **collaboration/README.md v3.2 → v3.3**: DECISION type in quick reference, archive rules, directory tree. 14 → 15 templates

### Philosophy

- **Trust, not control**: the framework's foundational belief — agents follow the protocol by reading files, not by code-level enforcement
- **Every byte traceable**: from DECISION → TASK → REPORT, the full causal chain is preserved in immutable Markdown files

### Added

- **Bilingual support**: English `collaboration_en/` + `README.md` (EN) + `README_CN.md` (CN)
- **Cooperation Charter**: `collaboration/CHARTER.md`, moved to project root by TPM on init as the supreme global rules
- **ACTIONS.md**: built-in empty template with field reference, channel type quick reference, and examples
- **GitHub community files**: Issue templates (bug + feature), PR template, SECURITY.md
- **TPM Core Principles rewritten**: 8 new principles — project partner, full lifecycle ownership, Agent manager, transparent reporting, tooling ownership, no business code, sole Git authority, concise output
- **CHARTER.md root migration**: TPM moves CHARTER.md to project root `../CHARTER.md` on init; all Agents share the same supreme rules
- **Sub-Agent background loop**: explicitly states Native Sub-Agents should be created in background mode with in-memory loop scanning

### Changed

- **AGENTS.md → TPM.md**: prevents AI tools from auto-loading it into non-TPM Agent prompts
- **Guard statement**: TPM.md top line `🛑 Your user must have explicitly told you "You are the TPM"`
- **Initialization extracted**: moved from §1 to standalone `## Initialization` section (6 steps)
- **TPM init command**: `You are TPM. Read the collaboration directory and start working.`
- **Agent onboarding command**: `Read the collaboration directory and join the team.`
- **TPM authority tabularized**: §2 rewritten as T-P-M 3D authority table (18 items + 6 red lines)
- **Outer README rewritten**: philosophy, TPM-centric mode, comparison table (4 types × 9 dimensions), MCP comparison (7 dimensions), extensibility, zero-touch onboarding, user project structure
- **collaboration/README.md streamlined**: 580 → 268 lines, removed marketing language, Agent-focused
- **Deleted scripts/**: runtime tools violate the framework's "files-only" philosophy
- **CONTRIBUTING.md rewritten**: updated project structure, Agent-perspective rules

### Fixed

- TPM.md §3.1 patrol flow residual "keep for one day" (abolished)
- TPM.md §5.5 stale section reference → §5, Task Lifecycle
- REGISTER.md stale REVIEW_TASK references → REPORT → REVIEW_REPORT direct-write pattern
- PROJECT.md TPM role description updated to "Task Planning Manager"
- TPM.md §10 .gitignore description changed from blanket to tiered exclusion
- .gitignore comment stale name AGENTS

## [3.2.0] - 2026-06-06

### Added

- **Practice case system**: `practices/` directory for community practice cases
  - First case: wolf-judge (5-person team, full-stack project, 120+ tasks)
  - Practice contribution guide

### Changed

- **collaboration/README.md major expansion**: 106 → 430+ lines, 4 → 13 sections
  - Completed general rules, task & reports, role definitions, onboarding, best practices
- **REGISTER.md upgraded**: 3 → 5 actions (added proactive report, blocking dependencies)
- **5 templates generalized**: NOTICE/LOG_ENTRY/REPLY/TASK_TEST/TODO had instance references removed

## [0.1.0] - 2026-05-30

### Initial Release

- Framework spec, 8 file templates, registration form, project config
