# TASK_005: 同步 15 个模板 CN → EN

> **文件名**: `TASK_005_TEMPLATE-EN-SYNC_TPM.md`
> **存放位置**: `inbox/`

**分派人**: TPM
**执行人**: TPM
**优先级**: 🟢 P2
**决策来源**: DECISION_001 / DECISION_004

---

## 目标

确保 15 个模板在 collaboration/templates/ 和 collaboration_en/templates/ 中结构一致、关联字段一致。

## 当前状态

大部分已在本次改动中同步。需逐文件确认：
- TASK 模板的"决策来源"字段
- PROACTIVE_REPORT 模板的"关联决策"字段
- DECISION 模板（新增）
- TODO 模板的"来源类型"字段

## 验收标准

- [ ] 15 个模板在 CN/EN 两版中字段对齐
- [ ] 提交 `outbox/REPORT_005_YYYYMMDD_TPM.md`
