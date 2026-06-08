# REVIEW_REPORT_NNN: Review Subject

> **Filename**: `REVIEW_REPORT_NNN[_R{N}]_DATE_AUTHOR.md`
> **Location**: `reviews/`
> **Naming**: segments separated by `_`, within segments use `-`. `NNN` = task number, `R{N}` = revision round (R1, R2), `DATE` = review date `YYYYMMDD`, `AUTHOR` = reviewer identifier (UPPERCASE)

**Reviewer**: [AUTHOR]
**Date**: YYYY-MM-DD
**Corresponding**: TASK_NNN / REPORT_NNN

> **Summary flow**: [Review Summary] is mandatory. First round: write only `### R0`. Subsequent rounds: copy all historical text from the executor's REPORT_RN [Review Summary], append this round at the bottom. Must not modify historical text.

---

## [Review Summary] (mandatory)

### R0 (YYYY-MM-DD)
- Score: X/10
- This round: 🔴 N | 🟡 N | 💡 N
- Status: 🔄 Revision Needed / ✅ ACCEPT
- One-liner: ...

| Dimension | Score | Notes |
|------|------|------|
| Code Quality | 9 | |
| Logic Correctness | 8 | |
| Type Safety | 9 | |
| Test Coverage | 8 | |
| **Overall** | **X** | |

## Issues Found

| # | Severity | File | Issue | Suggestion |
|---|--------|------|------|------|
| 1 | 🔴 | `src/file.rs:42` | | |
| 2 | 🟡 | | | |
| 3 | 💡 | | | |

## Specialized Checks (P2/P3 mandatory)

| Check | Result | Notes |
|------|------|------|
| Cross-module consistency | ✅ / ❌ | |
| Type safety | ✅ / ❌ | |
| Error handling | ✅ / ❌ | |
| State management | ✅ / ❌ | |

## Merge Recommendation

**✅ Recommend Accept** / **🔄 Revision Needed**
