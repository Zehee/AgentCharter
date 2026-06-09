# TASK_016: collaboration/README.md 新增"框架升级"章节

> **文件名**: `TASK_016_FRAMEWORK-UPGRADE-DOCS_TPM.md`
> **存放位置**: `inbox/`

**分派人**: TPM
**执行人**: TPM
**优先级**: 🟡 P1
**决策来源**: DECISION_013

---

## 目标

在 `collaboration/README.md` 中新增一节，告诉 Agent 和用户 AgentCharter 的升级方式不是装包、不是跑脚本，而是让 TPM 读取上游仓库并自行应用变更。

### 内容要点
- **升级命令**：用户对 TPM 说"读取上游仓库，应用更新"即可
- **TPM 自动做的事**：对比差异 → 建 TASK → 执行变更 → 写 REPORT
- **需要人类确认的事**：涉及项目级决策的变更（如启用人机结对模式）
- **为什么可以这样**：框架是纯文件——模板、规则、原则全部可读可改

### 放置位置
`collaboration/README.md` §十一 入职流程 之后，新 §十三。

## 验收标准

- [ ] CN 版新增"框架升级"章（§十三）
- [ ] EN 版同步
- [ ] 包含升级命令和 TPM 自动操作清单
- [ ] 提交 `outbox/REPORT_016_018_20260610_TPM.md`
