# TASK_017: TPM.md 升级操作指引

> **文件名**: `TASK_017_TPM-UPGRADE-GUIDE_TPM.md`
> **存放位置**: `inbox/`

**分派人**: TPM
**执行人**: TPM
**优先级**: 🟡 P1
**决策来源**: DECISION_013

---

## 目标

在 TPM.md 中新增升级操作指引。

### 内容要点
- TPM 在被要求升级时，读取上游仓库的 `collaboration/` 目录
- 对比自己项目的 `collaboration/`，列出差异
- 对于模板/规则变更，自动建 TASK 并执行
- 对于涉及项目级决策的变更（如新的角色模式），向人类确认
- 完成后写 REPORT

### 放置位置
TPM.md §二（TPM 权限与工作范围）M·Manage 行新增"执行框架升级（读取上游 → 对比差异 → 建 TASK 执行）"，并在 §九 快捷命令区新增"框架升级"的说明。

## 验收标准

- [ ] CN TPM.md §二 M·Manage 行含升级操作
- [ ] CN TPM.md §九 快捷命令区含升级说明
- [ ] EN 版同步
- [ ] 提交 `outbox/REPORT_016_018_20260610_TPM.md`
