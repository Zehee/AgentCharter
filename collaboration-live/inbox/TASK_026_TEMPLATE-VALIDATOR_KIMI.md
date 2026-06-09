# TASK_026: 实现模板验证器 CLI（可选工具）

> **文件名**: `TASK_026_TEMPLATE-VALIDATOR_KIMI.md`
> **存放位置**: `inbox/`

**分派人**: TPM Reasonix
**执行人**: Kimi
**优先级**: 🟢 P2
**决策来源**: PROACTIVE_REPORT_003（Zehee 修正）

---

## 目标

实现一个模板验证器 CLI（约 200 行），验证 `collaboration/templates/` 和 `collaboration_en/templates/` 中的 15 个模板格式和命名规范，放在 `extras/` 目录下（框架核心不依赖）。

## 验收标准

- [ ] 代码放在 `extras/template-validator/`，不污染框架核心
- [ ] 验证通过
- [ ] 提交 `outbox/REPORT_026_KIMI.md`
