<!--
  文件类型: 主动报告处理回执
  维护者: TPM
  用途: 通知主动报告提交者处理结果
  创建时机: TPM 处理完主动报告后
  命名规范: REPLY_NNN_DESC_DATE_AUTHOR.md
    - NNN: 对应主动报告编号
    - DATE: 处理日期 `YYYYMMDD`
    - AUTHOR: 报告提交者标识（大写）
-->

# REPLY_NNN: {{title}}

> **文件名**: `REPLY_NNN_DESC_DATE_author@recipient.md`
> **存放位置**: `inbox/`
> **命名约束**: 段间 `_`，段内 `-`。`NNN`=对应主动报告编号，`DATE`=处理日期 `YYYYMMDD`，`AUTHOR`=报告提交者标识（大写）

**来源报告**: {{ref_nnn}}
**处理日期**: {{DATE}}
**提交人**: {{author}}

---

## 处理结果摘要

| 状态 | 数量 | 说明 |
|------|------|------|
| 📋 任务 | {{task_count}} | {{task_note}} |
| 📅 排期 | {{scheduled_count}} | {{scheduled_note}} |
| ✅ 采纳 | {{accepted_count}} | {{accepted_note}} |
| ❌ 忽略 | {{ignored_count}} | {{ignored_note}} |
| ✓ 已处理 | {{processed_count}} | {{processed_note}} |

**详细批注**: {{detailed_notes}}

---

## 关键决策（可选）

> - 决策 1：...
> - 决策 2：...
{{key_decisions}}

---

**处理人**: {{handler}}
**日期**: {{DATE}}
