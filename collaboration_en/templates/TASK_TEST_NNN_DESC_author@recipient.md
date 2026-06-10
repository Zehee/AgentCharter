# TASK_TEST_NNN: Test Task Title

> **Filename**: `TASK_TEST_NNN_DESC_author@recipient.md`
> **Location**: `inbox/`
> **Naming**: segments separated by `_`, within segments use `-`. `NNN` = test round number, `DESC` = short English description, `ASSIGNEE` = tester identifier (UPPERCASE)

**Dispatcher**: TPM
**Tester**: {{assignee}}
**Date**: {{DATE}}
**Priority**: 🔴 P0 | 🟡 P1 | 🟢 P2
**Related**: TASK_NNN (functional dev task) / REVISION_NNN (fix verification)
**Test Round**: Round X (Regression / Acceptance / Exploratory)

---

## 1. Test Objective

One sentence describing what this test verifies and why now.

## 2. Environment Requirements

| Item | Requirement |
|---|---|
| **OS** | Windows 11 / macOS / Linux |
| **App Version** | Commit `abc1234` / packaged binary |
| **Run Mode** | `command` / release build |
| **Resolution** | Recommended ≥ 1920×1080 |
| **Preconditions** | Previous issues fixed / new feature merged |

## 3. Verification Checklist

### 3.1 [Module Name]

| # | Scenario | Steps | Expected Result |
|---|------|----------|----------|
| 1 | | | |

## 4. Regression Items (if applicable)

| Historical Bug | Fix Version | Verification Scenario | Method |
|----------|----------|----------|----------|

## 5. Known Risks & Exclusions

| # | Risk / Exclusion | Explanation | Plan |
|---|-------------|------|------|

## 6. Minimum Pass Criteria

- [ ] Category A (regression): all PASS, or 🔴 defects ≤ 0
- [ ] Category B (core flow): PASS rate ≥ 80%, no 🔴 defects
- [ ] Category C (new feature): PASS rate ≥ 60%, no 🔴 defects
- [ ] Complete core user flow from start to finish

## 7. Feedback Requirements

Submit `outbox/TEST_REPORT_NNN_DATE_author@recipient.md`, must include:
1. Verification checklist results (PASS / FAIL / BLOCK / N/A)
2. Defect list (🔴 / 🟡 / 💡, with repro steps)
3. Environment confirmation
4. Overall conclusion (Pass / Conditional Pass / Blocked)
