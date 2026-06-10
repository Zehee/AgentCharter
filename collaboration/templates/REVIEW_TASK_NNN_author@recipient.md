<!-- 委派审查范式下使用。自循环审查范式下不需要此模板。 -->

# REVIEW_TASK_NNN: 审查对象简述

> **文件名**: `REVIEW_TASK_NNN_author@recipient.md`
> **存放位置**: `inbox/`
> **命名约束**: 段间 `_`，段内 `-`，后缀 `author@recipient`。`NNN`=被审查的任务序号

**审查人**: {{author}}
**被审查人**: {{assignee}}
**优先级**: {{priority}}

---

## 审查范围

| 文件 | 路径 | 说明 |
|------|------|------|
| 文件名 | `src/xxx` | 为什么审查 |

## 审查重点

- [ ] 检查项 1
- [ ] 检查项 2

## 输出要求

提交 `outbox/REVIEW_REPORT_NNN_DATE_author@recipient.md`（委派审查下给 TPM），包含：
1. 总体评分（1-10）
2. 发现的问题（🔴严重 / 🟡一般 / 💡建议）
3. 是否建议合并（通过 / 需修订）
