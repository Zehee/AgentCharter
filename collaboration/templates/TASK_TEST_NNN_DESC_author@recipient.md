# TASK_TEST_NNN: {{title}}

> **文件名**: `TASK_TEST_NNN_DESC_author@recipient.md`
> **存放位置**: `inbox/`
> **命名约束**: 段间 `_`，段内 `-`。`NNN`=测试轮次序号，`DESC`=英文简短描述，`ASSIGNEE`=测试员标识（大写）

**分派人**: {{author}}
**测试员**: {{assignee}}
**日期**: {{DATE}}
**优先级**: {{priority}}
**关联**: {{ref_nnn}}
**测试轮次**: {{test_round}}

---

## 测试目标

> 一句话描述本次测试要验证什么、为什么现在做。
{{test_goal}}

---

## 环境要求

> 测试开始前必须确认的环境条件。

| 项 | 要求 |
|---|---|
| **操作系统** | {{os_requirement}} |
| **App 版本** | {{app_version}} |
| **运行方式** | {{run_mode}} |
| **屏幕分辨率** | {{screen_resolution}} |
| **测试版型** | {{test_type}} |
| **前置条件** | {{prerequisites}} |

---

## 验证清单

> 按功能模块分组，每项必须填写结果。测试完成后将结果列填入 `outbox/TEST_REPORT_NNN_DATE_AUTHOR.md`。

### {{module_name_1}}

| # | 场景 | 操作步骤 | 预期结果 |
|---|------|----------|----------|
| {{test_num_1_1}} | {{scenario_1_1}} | {{steps_1_1}} | {{expected_1_1}} |
| {{test_num_1_2}} | {{scenario_1_2}} | {{steps_1_2}} | {{expected_1_2}} |

### {{module_name_2}}

| # | 场景 | 操作步骤 | 预期结果 |
|---|------|----------|----------|
| {{test_num_2_1}} | {{scenario_2_1}} | {{steps_2_1}} | {{expected_2_1}} |

---

## 回归项（如适用）

> 本轮需要验证的历史问题，确保已修复未复发。

| 历史 Bug | 修复版本 | 验证场景 | 验证方式 |
|----------|----------|----------|----------|
| {{bug_id}} | {{revision_ref}} | {{verification_scenario}} | {{verification_method}} |

---

## 已知风险 & 未测项

> 提前声明哪些不测、为什么，避免测试员浪费时间。

| # | 风险/未测项 | 说明 | 计划 |
|---|-------------|------|------|
| {{risk_num}} | {{risk_item}} | {{risk_note}} | {{risk_plan}} |

---

## 最低通过标准

- [ ] {{pass_criteria_a}}
- [ ] {{pass_criteria_b}}
- [ ] {{pass_criteria_c}}
- [ ] {{pass_criteria_d}}

> 不满足最低通过标准 = 本轮测试 **不通过**，需修复后重新测试。

---

## 反馈要求

测试完成后提交 `outbox/TEST_REPORT_NNN_DATE_AUTHOR.md`，必须包含：
1. 验证清单结果（PASS / FAIL / BLOCK / N/A）
2. 缺陷清单（🔴 / 🟡 / 💡，附复现步骤）
3. 环境信息确认
4. 总体结论（通过 / 有条件通过 / 阻塞）

---

## 备注

> （任何需要测试员特别注意的事项）
{{notes}}
