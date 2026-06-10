# TEST_REPORT_NNN: {{title}} — {{overall_conclusion}}

> **Filename**: `TEST_REPORT_NNN_DATE_author@recipient.md`
> **Location**: `outbox/`
> **Naming**: segments separated by `_`, within segments use `-`. `NNN` = corresponding test task number, `DATE` = submission date `YYYYMMDD`, `AUTHOR` = tester identifier (UPPERCASE)

**Tester**: {{author}}
**Date**: {{DATE}}
**Related**: {{ref_nnn}}
**Test Type**: {{test_type}}
**Overall Conclusion**: {{conclusion}}

---

## Environment

| Item | Value |
|---|---|
| **OS** | {{os_value}} |
| **App Version** | {{app_version_value}} |
| **Run Mode** | {{run_mode_value}} |
| **Screen Resolution** | {{screen_resolution_value}} |
| **Browser/CDP** | {{browser_cdp_value}} |
| **Backend Build** | {{backend_build_value}} |
| **Frontend Build** | {{frontend_build_value}} |

---

## Verification Checklist

> Execute test scenarios one by one, mark results. PASS=meets expectation, FAIL=does not meet, N/A=not applicable, BLOCK=cannot execute.

### {{module_name_1}}

| # | Scenario | Steps | Expected Result | Result | Notes |
|---|------|----------|----------|------|------|
| {{test_num_1_1}} | {{scenario_1_1}} | {{steps_1_1}} | {{expected_1_1}} | {{result_1_1}} | {{note_1_1}} |
| {{test_num_1_2}} | {{scenario_1_2}} | {{steps_1_2}} | {{expected_1_2}} | {{result_1_2}} | {{note_1_2}} |

### {{module_name_2}}

| # | Scenario | Steps | Expected Result | Result | Notes |
|---|------|----------|----------|------|------|
| {{test_num_2_1}} | {{scenario_2_1}} | {{steps_2_1}} | {{expected_2_1}} | {{result_2_1}} | {{note_2_1}} |

---

## Defect List

> All FAIL/BLOCK items must be recorded here. If no defects found, write "No defects found in this test."

### 🔴 {{bug_title_1}}

| Field | Detail |
|------|------|
| **Severity** | {{severity_1}} |
| **Phase** | {{phase_1}} |
| **Repro Steps** | {{repro_steps_1}} |
| **Actual Behavior** | {{actual_behavior_1}} |
| **Expected Behavior** | {{expected_behavior_1}} |
| **Screenshot/Recording** | {{screenshot_1}} |
| **Root Cause** | {{root_cause_1}} |
| **Fix Suggestion** | {{fix_suggestion_1}} |
| **Related Task** | {{related_task_1}} |

### 🟡 {{bug_title_2}}

{{bug_2_details}}

---

## Confirmed Features (Pass Summary)

> Record key functionality verified in this test for future regression reference.

| # | Feature | Verification Method | Result |
|---|--------|----------|------|
| {{confirmed_num}} | {{feature_point}} | {{verification_method}} | {{result}} |

---

## Known Limitations & Untested Items

| # | Limitation/Untested | Reason | Plan |
|---|-------------|------|------|
| {{limit_num}} | {{limit_item}} | {{limit_reason}} | {{limit_plan}} |

---

## Test Statistics

| Metric | Value |
|------|------|
| Total Test Items | {{total_items}} |
| PASS | {{pass_count}} |
| FAIL | {{fail_count}} |
| BLOCK | {{block_count}} |
| N/A | {{na_count}} |
| 🔴 Critical | {{critical_count}} |
| 🟡 Major | {{major_count}} |
| 💡 Suggestion | {{suggestion_count}} |

---

## Conclusion & Recommendations

**Overall Conclusion**: {{final_conclusion}}

**Reason**:
{{conclusion_reason}}

**Next Steps**:
- [ ] {{next_action_1}}
- [ ] {{next_action_2}}
- [ ] {{next_action_3}}

---

## Appendix

### A. Screenshot Directory
```
{{screenshot_dir}}
```

### B. Automated Test Output (if applicable)
```
> (Paste test framework output summary, or note the output file location)
{{auto_test_output}}
```

### C. Notes
> (Any supplementary information not suitable for the main body)
{{appendix_notes}}
