# REVISION_NNN: {{title}}

> **文件名**: `REVISION_NNN_DATE_author@recipient.md`
> **存放位置**: `inbox/`
> **命名约束**: 段间 `_`，段内 `-`，后缀 `author@recipient`。`NNN`=对应审查序号，`DATE`=创建日期 `YYYYMMDD`，`tpm`=分派 TPM 标识（大写），`assignee`=领取者标识（大写）

**分派人**: {{author}}
**执行人**: {{assignee}}
**日期**: {{DATE}}
**优先级**: {{priority}}
**对应**: {{ref_nnn}}

---

## 目标

> 一句话说明要修复什么。
{{goal}}

## 问题清单

| # | 问题 | 文件/位置 | 修复要求 |
|---|------|----------|---------|
| {{issue_number_1}} | {{issue_description_1}} | `{{issue_file_1}}` | {{issue_expectation_1}} |
| {{issue_number_2}} | {{issue_description_2}} | `{{issue_file_2}}` | {{issue_expectation_2}} |

## 验收标准

- [ ] {{acceptance_item_1}}
- [ ] {{acceptance_item_2}}
- [ ] {{type_check_cmd}}
- [ ] {{report_submission}}
