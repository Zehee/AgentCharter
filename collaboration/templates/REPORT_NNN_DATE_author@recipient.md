# REPORT_NNN: {{title}}

> **文件名**: `REPORT_NNN_DATE_author@recipient.md`
> **存放位置**: `outbox/`
> **命名约束**: 段间 `_`，段内 `-`，后缀 `author@recipient`。`NNN`=任务序号，`DATE`=提交日期 `YYYYMMDD`，`author`=作者标识（大写），`tpm`=接收 TPM 标识（大写）

**提交人**: {{author}}
**日期**: {{DATE}}
**状态**: REVIEW_PENDING
**对应**: {{ref_nnn}}
**报告性质**: {{report_type}}

---

<!--
## 【审查摘要】（多轮修复时取消注释）
从 REVIEW_REPORT 的【摘要】节复制全部历史原文到此处，
在每轮下方追加你的修复回应。首轮 REPORT 无需此节。

### R0 (YYYY-MM-DD)
- 评分：X/10 | 状态：🔄 需修复
- 回应：
  - 🔴/🟡 问题描述：✅ 已修复 / 🔄 未修复（说明原因）
-->

## 完成情况

| 任务 | 状态 | 说明 |
|------|------|------|
| {{task_1}} | ✅ | {{description_1}} |
| {{task_2}} | ✅ | {{description_2}} |

## 改动的文件

| 文件 | 修改内容 |
|------|----------|
| `{{file_path}}` | {{change_description}} |

## 待确认（可选）

- [ ] {{debug_note}}

## 补充说明（可选）

{{custom_content}}

---

## 构建结果

| 命令 | 结果 |
|------|------|
| `{{type_check_cmd}}` | ✅ {{type_check_result}} |
| `{{build_cmd}}` | ✅ {{build_result}} |
| `{{backend_check_cmd}}` | ✅ {{backend_check_result}} |

---

**当前状态**: {{status}} — 等待 {{tpm_name}} 审查

---

## Native Sub-Agent 专用格式（可选）

> 以下格式供 Native Sub-Agent 参考。Native 的报告是审计记录，受众是人类开发者。

```markdown
# REPORT_NNN: {{title}}

> **报告性质**: {{audit_note}}
> 受众：{{audience}}

## 执行摘要
- 任务 ID: {{task_id}}
- 状态: {{status}}
- 核心目标: {{core_goal}}

## 核心改动
> 自然语言描述，不贴全量代码，只列文件和改动性质
{{core_changes}}

## 决策理由
> 解释 WHY，这是最有价值的部分
{{decision_rationale}}

## 风险点 & 需人工确认
- [ ] {{risk_item_1}}
- [ ] {{risk_item_2}}

## 自检清单
- [x] {{check_item_1}}
- [x] {{check_item_2}}
```
