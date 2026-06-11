# REVIEW_REPORT_NNN: {{review_target}} — {{conclusion}}

> **文件名**: `REVIEW_REPORT_NNN_DATE_author@recipient.md`
> **存放位置**: 范式相关——委派审查放 `outbox/`（给 TPM），自循环审查放 `inbox/`（给 coder）
> **命名约束**: 段间 `_`，段内 `-`，后缀 `author@recipient`。`NNN`=审查序号，`DATE`=提交日期 `YYYYMMDD`，`author`=审查人标识（大写），`recipient`=接收者标识（大写）

**审查人**: {{author}}
**日期**: {{DATE}}
**轮次**: {{round}}
**对应**: {{ref_nnn}}
**接收者**: {{recipient}}

> **摘要流转规则**：【摘要】节必填。首轮只写 `### R0`，后续轮次从执行者的 REPORT_RN【审查摘要】复制全部历史原文，底部追加本轮，不得修改历史原文。

---

## 【审查摘要】（必填）

### R0 ({{review_date}})
- 评分：{{score}}/10
- 本轮：🔴 {{red_count}} / 🟡 {{yellow_count}} / 💡 {{lightbulb_count}}
- 状态：{{status}}
- 一句话：{{summary_line}}

| 维度 | 评分 | 说明 |
|------|------|------|
| 代码质量 | {{code_quality_score}} | {{code_quality_note}} |
| 逻辑正确性 | {{logic_score}} | {{logic_note}} |
| 类型安全 | {{type_safety_score}} | {{type_safety_note}} |
| 测试覆盖 | {{test_coverage_score}} | {{test_coverage_note}} |
| **总体** | **{{overall_score}}** | **{{overall_note}}** |

## 发现的问题

| # | 严重度 | 文件 | 问题 | 建议 |
|---|--------|------|------|------|
| {{issue_num_1}} | {{severity_1}} | `{{file_1}}` | {{problem_1}} | {{suggestion_1}} |
| {{issue_num_2}} | {{severity_2}} | `{{file_2}}` | {{problem_2}} | {{suggestion_2}} |
| {{issue_num_3}} | {{severity_3}} | `{{file_3}}` | {{problem_3}} | {{suggestion_3}} |

## 专项核查（P2/P3 必填）

| 检查项 | 结果 | 说明 |
|------|------|------|
| 跨端一致性 | {{cross_platform_result}} | {{cross_platform_note}} |
| 类型安全 | {{type_safety_check_result}} | {{type_safety_check_note}} |
| 错误处理 | {{error_handling_result}} | {{error_handling_note}} |
| 状态管理 | {{state_management_result}} | {{state_management_note}} |

## 合并建议

**{{merge_decision}}**
