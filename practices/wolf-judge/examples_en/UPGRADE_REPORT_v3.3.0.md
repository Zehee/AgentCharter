# AgentCharter v3.3.0 Framework Upgrade Report

> Source: wolf-judge project, executed by TPM DSpro
> Date: 2026-06-10
> Note: This is the first external instance to complete an upstream v3.2 → v3.3 upgrade. Demonstrates how a TPM independently scans upstream, evaluates diffs, makes tradeoffs, and submits a report.

---

## Upgrade Source

Upstream [Zehee/AgentCharter](https://github.com/Zehee/AgentCharter) released v3.3.0 on 2026-06-10. DSpro evaluated and adopted 5 changes.

## New Files (2)

**`collaboration/templates/DECISION_NNN_DATE_AUTHOR.md`** — 15th file template
- Records the complete reasoning chain during human-AI pair deliberation
- Format: `decisions/DECISION_NNN_DATE_AUTHOR.md`

**`docs/decision-protocol.md`** — Decision recording protocol
- 8 chapters covering motivation, format, triggers, information flow, relationships, archive rules, and design philosophy

## Modified Files (3)

**`collaboration/README.md`**
- Version: v3.2 → v3.3
- Templates: 14 → 15 (added DECISION)
- Directory tree: added `decisions/`

**`collaboration/ACTIONS.md`**
- Channel type table: added `decisions/DECISION` row

**`CHARTER.md`**
- Quick reference: added decision recording entry

## Declined Changes (2)

| Upstream Decision | Rejection Reason |
|---------|---------|
| Delete `scripts/` | `file-gen.js` is the only tool for External Agent (DSpro) to generate files without Reasonix skill |
| `AGENTS.md` → `TPM.md` | Project-root `AGENTS.md` is designed for DSpro (external CLI auto-load) — upstream doesn't support this scenario |

## Change Summary

| Type | Count | Notes |
|------|------|------|
| Added | 2 | Template + protocol doc |
| Modified | 3 | README / ACTIONS / CHARTER |
| Deleted | 0 | — |
| Deferred | 2 | scripts/ kept, AGENTS.md untouched |

## Follow-up

The DECISION template and protocol doc are in place but not mandatory. When a human-AI pair produces a decision with meaningful reasoning chains, create `decisions/DECISION_NNN` following the protocol. It'll be used when it's needed.
