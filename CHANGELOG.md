# Changelog

Format based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).
This project follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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
