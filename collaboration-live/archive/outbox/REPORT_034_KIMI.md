# REPORT_034: 审查流程重构——删除 reviews/、更新文档、迁移命名规范

> **提交人**: Kimi
> **日期**: 2026-06-10
> **状态**: ✅ COMPLETED
> **对应**: TASK_034_REVIEW-RESTRUCTURE_KIMI

---

## 完成情况

| # | 改动 | 文件 | 状态 |
|---|------|------|------|
| 1 | 删除 `reviews/` 目录 | `collaboration/reviews/` + `archive/reviews/` + `collaboration-live/reviews/` + `collaboration_en/reviews/` | ✅ |
| 2 | REVIEW_REPORT 模板路径改为范式相关 | `templates/REVIEW_REPORT_NNN_DATE_author@recipient.md` | ✅ |
| 3 | REVIEW_TASK 模板标注"委派审查可选" | `templates/REVIEW_TASK_NNN_author@recipient.md` | ✅ |
| 4 | 命名规范统一为双后缀 `_author@recipient.md` | 全部 14 个模板（不含 LOG_ENTRY/TODO） | ✅ |
| 5 | 模板内容中文件名引用同步更新 | 全部模板 | ✅ |
| 6 | README.md 全面更新 | `README.md` + EN | ✅ |
| 7 | TPM.md 全面更新 | `TPM.md` + EN | ✅ |
| 8 | 新建 review-guide.md | `collaboration/review-guide.md` + EN | ✅ |
| 9 | 验证器更新 | `extras/template-validator/validate.py` | ✅ |

---

## 命名规范最终统一

**通用规则**：所有协作文件统一使用双后缀 `_author@recipient.md`
- `author` = 写这个文件的人/角色
- `recipient` = 这个文件的预期接收者/读者

| 模板 | 旧文件名 | 新文件名 |
|------|---------|---------|
| TASK | `TASK_NNN_DESC_ASSIGNEE.md` | `TASK_NNN_DESC_author@recipient.md` |
| TASK_TEST | `TASK_TEST_NNN_DESC_ASSIGNEE.md` | `TASK_TEST_NNN_DESC_author@recipient.md` |
| REPORT | `REPORT_NNN_DATE_AUTHOR.md` | `REPORT_NNN_DATE_author@recipient.md` |
| TEST_REPORT | `TEST_REPORT_NNN_DATE_AUTHOR.md` | `TEST_REPORT_NNN_DATE_author@recipient.md` |
| REVISION | `REVISION_NNN_DATE_ASSIGNEE.md` | `REVISION_NNN_DATE_author@recipient.md` |
| REVIEW_REPORT | `REVIEW_REPORT_NNN_DATE_AUTHOR.md` | `REVIEW_REPORT_NNN_DATE_author@recipient.md` |
| REVIEW_TASK | `REVIEW_TASK_NNN.md` | `REVIEW_TASK_NNN_author@recipient.md` |
| PROACTIVE_REPORT | `PROACTIVE_REPORT_NNN_DESC_DATE_AUTHOR.md` | `PROACTIVE_REPORT_NNN_DESC_DATE_author@recipient.md` |
| NOTICE | `NOTICE_NNN_DESC_DATE_TARGET.md` | `NOTICE_NNN_DESC_DATE_author@recipient.md` |
| REPLY | `REPLY_NNN_DESC_DATE_AUTHOR.md` | `REPLY_NNN_DESC_DATE_author@recipient.md` |
| BLOCKING | `BLOCKING_NNN_DATE_TARGET.md` | `BLOCKING_NNN_DATE_author@recipient.md` |
| BLOCKING_REPLY | `BLOCKING_REPLY_NNN_DATE_AUTHOR.md` | `BLOCKING_REPLY_NNN_DATE_author@recipient.md` |
| DECISION | `DECISION_NNN_DATE_AUTHOR.md` | `DECISION_NNN_DATE_author@recipient.md` |
| TODO | `TODO_NNN_DESC_SOURCE.md` | 保持（`_SOURCE` 为来源标识）|
| LOG_ENTRY | `LOG_ENTRY.md` | 保持 |

---

## 验证结果

- **中文模板**：30 通过，0 错误，0 警告
- **英文模板**：30 通过，0 错误，13 警告（头部字段语言差异，已知问题）

---

**当前状态**: ✅ COMPLETED
