# REVIEW_REPORT_NNN: {{review_target}} — {{conclusion}}

> **Filename**: `REVIEW_REPORT_NNN[_R{N}]_DATE_author@recipient.md`
> **Location**: Paradigm-dependent — delegated review: `outbox/` (to TPM), self-loop review: `inbox/` (to coder)
> **Naming**: segments separated by `_`, within segments use `-`. `NNN` = review number, `DATE` = review date `YYYYMMDD`, `AUTHOR` = reviewer identifier (UPPERCASE), `RECIPIENT` = recipient identifier (UPPERCASE)

**Reviewer**: {{author}}
**Date**: {{DATE}}
**Corresponding**: {{ref_nnn}}
**Recipient**: {{recipient}}

> **Summary flow**: [Review Summary] is mandatory. First round: write only `### R0`. Subsequent rounds: copy all historical text from the executor's REPORT_RN [Review Summary], append this round at the bottom. Must not modify historical text.

---

## [Review Summary] (mandatory)

### R0 ({{review_date}})
- Score: {{score}}/10
- This round: 🔴 {{red_count}} / 🟡 {{yellow_count}} / 💡 {{lightbulb_count}}
- Status: {{status}}
- One-liner: {{summary_line}}

| Dimension | Score | Notes |
|------|------|------|
| Code Quality | {{code_quality_score}} | {{code_quality_note}} |
| Logic Correctness | {{logic_score}} | {{logic_note}} |
| Type Safety | {{type_safety_score}} | {{type_safety_note}} |
| Test Coverage | {{test_coverage_score}} | {{test_coverage_note}} |
| **Overall** | **{{overall_score}}** | **{{overall_note}}** |

## Issues Found

| # | Severity | File | Issue | Suggestion |
|---|--------|------|------|------|
| {{issue_num_1}} | {{severity_1}} | `{{file_1}}` | {{problem_1}} | {{suggestion_1}} |
| {{issue_num_2}} | {{severity_2}} | `{{file_2}}` | {{problem_2}} | {{suggestion_2}} |
| {{issue_num_3}} | {{severity_3}} | `{{file_3}}` | {{problem_3}} | {{suggestion_3}} |

## Specialized Checks (P2/P3 mandatory)

| Check | Result | Notes |
|------|------|------|
| Cross-module consistency | {{cross_platform_result}} | {{cross_platform_note}} |
| Type safety | {{type_safety_check_result}} | {{type_safety_check_note}} |
| Error handling | {{error_handling_result}} | {{error_handling_note}} |
| State management | {{state_management_result}} | {{state_management_note}} |

## Merge Recommendation

**{{merge_decision}}**
