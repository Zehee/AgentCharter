# REVIEW_REPORT_{{NNN}}: {{review_target}} — {{conclusion}}

> **文件名**: `REVIEW_REPORT_{{NNN}}_DATE_{{author}}@{{recipient}}.md`
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

## 详细审查意见

> 格式：`[🔴严重/🟡一般/💡建议] | 文件:行号 | 问题描述 | 修复建议`

### 🔴 严重

> - `文件:行号` | 问题描述 | 修复建议

### 🟡 一般

> - `文件:行号` | 问题描述 | 修复建议

### 💡 建议

> - `文件:行号` | 问题描述 | 修复建议
