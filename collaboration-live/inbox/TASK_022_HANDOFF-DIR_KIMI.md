# TASK_022: 创建 collaboration-live/handoff/ 目录及规范

> **文件名**: `TASK_022_HANDOFF-DIR_KIMI.md`
> **存放位置**: `inbox/`

**分派人**: TPM Reasonix
**执行人**: Kimi
**优先级**: 🟡 P1
**决策来源**: DECISION_016 / PROACTIVE_REPORT_004

---

## 目标

在 `collaboration-live/` 下创建 `handoff/` 目录，用于三人协作团队（Zehee ↔ Reasonix ↔ Kimi）在不同 AI 对话窗口间传递状态摘要。

### 规范
- 每次交替工作前写 `handoff/STATE_YYYYMMDD_AUTHOR.md`
- 内容含：最后做的工作、当前待办、上下文中可能丢失的关键信息
- 读者读完后在顶部标注 ✅ 已读，无需回复

## 验收标准

- [ ] `collaboration-live/handoff/` 目录已创建
- [ ] 第一份状态摘要已写入（示范格式）
- [ ] 提交 `outbox/REPORT_022_KIMI.md`
