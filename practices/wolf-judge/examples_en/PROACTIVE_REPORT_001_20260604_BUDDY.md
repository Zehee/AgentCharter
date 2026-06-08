<!--
  File Type: Proactive Report
  Author: Reporter (Buddy, double role)
  Nature: No corresponding TASK, does not go through inbox task system
  Handling: TPM read-and-burn — read → decide → annotate → archive
-->

# 🔍 PROACTIVE_REPORT_001: Game Rules Test Cases for All 6 Board Types

> **Filename**: `PROACTIVE_REPORT_001_BOARD-RULES-TESTCASE_20260604_BUDDY.md`
> **Nature**: Proactive Report (no corresponding TASK)
> **Author**: Buddy
> **Date**: 2026-06-04

---

## 1. Scope & Objective

**Scope**: Game rules test cases for all 6 board types in the project's `boards.json`, covering role lineups, night order, special abilities, edge cases, and win conditions.

**Target Audience**: TPM (Kimi), for reference in subsequent TASK_107 and new board type test tasks.

**Sources**:
- Project `src/data/boards/boards.json` board config (authoritative)
- Web search — werewolves.games / Zhihu / Baidu Encyclopedia (rule supplements)

| Board | id | Players | Difficulty |
|------|-----|------|------|
| Witch Hunter Classic | `pre_witch_hunter` | 12 | standard |
| Witch Guard | `pre_witch_guard` | 12 | standard |
| Cupid Lovers | `cupid_lovers` | 12 | advanced |
| White Werewolf Knight | `white_werewolf_knight` | 12 | advanced |
| Werewolf Beauty Guard | `werewolf_beauty_guard` | 12 | advanced |
| Stone Gargoyle Gravekeeper | `stone_gargoyle_gravekeeper` | 12 | advanced |

---

## 2. Analysis Method

1. **Extract boards.json rules** — role list, night order, special constraints from `rules` field for each board
2. **Cross-reference standard rules** — compare with community-standard rules
3. **Design test scenarios** — per board: role lineup verification, night order correctness, special ability triggers, edge cases, win condition validation

*(Detailed test case tables for all 6 boards omitted for brevity — see [CN version](../examples/PROACTIVE_REPORT_001_20260604_BUDDY.md) for full content)*

---

## 3. Summary of Findings

| Category | Count | Key Issues |
|------|------|------|
| Test scenarios designed | 45+ | Across all 6 board types |
| Edge cases identified | 12 | Including simultaneous abilities, order conflicts |
| Rules discrepancies found | 3 | Between implementation and community rules |

## 4. Recommendation

Use these test cases as the baseline for TASK_107 E2E regression testing. Each board type should have its core scenarios verified before MVP release.

---

## TPM Processing

**Date**: 2026-06-04
**Decision**: ✅ Accept — test cases adopted as baseline; incorporated into TASK_107 scope
