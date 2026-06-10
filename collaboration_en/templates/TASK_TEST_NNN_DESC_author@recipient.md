# TASK_TEST_NNN: {{title}}

> **Filename**: `TASK_TEST_NNN_DESC_author@recipient.md`
> **Location**: `inbox/`
> **Naming**: segments separated by `_`, within segments use `-`. `NNN` = test round number, `DESC` = short English description, `ASSIGNEE` = tester identifier (UPPERCASE)

**Dispatcher**: {{author}}
**Tester**: {{assignee}}
**Date**: {{DATE}}
**Priority**: {{priority}}
**Related**: {{ref_nnn}}
**Test Round**: {{test_round}}

---

## Test Objective

> One sentence describing what this test verifies and why now.
{{test_goal}}

---

## Environment Requirements

> Environmental conditions that must be confirmed before testing begins.

| Item | Requirement |
|---|---|
| **OS** | {{os_requirement}} |
| **App Version** | {{app_version}} |
| **Run Mode** | {{run_mode}} |
| **Screen Resolution** | {{screen_resolution}} |
| **Test Type** | {{test_type}} |
| **Preconditions** | {{prerequisites}} |

---

## Verification Checklist

> Grouped by functional module. Each item must have a result. Populate results in `outbox/TEST_REPORT_NNN_DATE_author@recipient.md`.

### {{module_name_1}}

| # | Scenario | Steps | Expected Result |
|---|------|----------|----------|
| {{test_num_1_1}} | {{scenario_1_1}} | {{steps_1_1}} | {{expected_1_1}} |
| {{test_num_1_2}} | {{scenario_1_2}} | {{steps_1_2}} | {{expected_1_2}} |

### {{module_name_2}}

| # | Scenario | Steps | Expected Result |
|---|------|----------|----------|
| {{test_num_2_1}} | {{scenario_2_1}} | {{steps_2_1}} | {{expected_2_1}} |

---

## Regression Items (if applicable)

> Historical issues to verify in this round — ensure fixed and not regressed.

| Historical Bug | Fix Version | Verification Scenario | Method |
|----------|----------|----------|----------|
| {{bug_id}} | {{revision_ref}} | {{verification_scenario}} | {{verification_method}} |

---

## Known Risks & Exclusions

> Declare what won't be tested upfront to avoid wasting tester time.

| # | Risk / Exclusion | Explanation | Plan |
|---|-------------|------|------|
| {{risk_num}} | {{risk_item}} | {{risk_note}} | {{risk_plan}} |

---

## Minimum Pass Criteria

- [ ] {{pass_criteria_a}}
- [ ] {{pass_criteria_b}}
- [ ] {{pass_criteria_c}}
- [ ] {{pass_criteria_d}}

> Failing minimum pass criteria = this round **FAILED**, needs fix and retest.

---

## Feedback Requirements

Submit `outbox/TEST_REPORT_NNN_DATE_author@recipient.md`, must include:
1. Verification checklist results (PASS / FAIL / BLOCK / N/A)
2. Defect list (🔴 / 🟡 / 💡, with repro steps)
3. Environment confirmation
4. Overall conclusion (Pass / Conditional Pass / Blocked)

---

## Notes

> (Anything the tester should pay special attention to)
{{notes}}
