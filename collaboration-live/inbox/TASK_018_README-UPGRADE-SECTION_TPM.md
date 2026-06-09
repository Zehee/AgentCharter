# TASK_018: 外层 README 新增"如何升级"小节

> **文件名**: `TASK_018_README-UPGRADE-SECTION_TPM.md`
> **存放位置**: `inbox/`

**分派人**: TPM
**执行人**: TPM
**优先级**: 🟡 P1
**决策来源**: DECISION_013

---

## 目标

在外层 README（给人看的）中新增"如何升级"小节，告诉用户框架升级不需要装包。

### 放置位置
📦 仓库结构 之后，📋 License 之前。简短一段即可。

### 内容
> **如何升级**：不需要 `pip install`，不需要迁移脚本。告诉你的 TPM：
> ```
> 读取 AgentCharter 仓库的最新版本，对比我们的项目，应用更新
> ```
> TPM 会自行读取上游、列出差异、建 TASK 执行变更、写 REPORT。涉及影响现有流程的改动，TPM 会向你确认。

## 验收标准

- [ ] EN README 含升级小节
- [ ] CN README 同步
- [ ] 提交 `outbox/REPORT_016_018_20260610_TPM.md`
