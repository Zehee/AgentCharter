# DECISION_013: 框架升级的用户操作方式——"让 TPM 去读取上游仓库"

**结对**: @tpm-pair (Reasonix + Zehee)
**时间**: 2026-06-10

---

## 决策

AgentCharter 的版本升级不需要 `pip install`、不需要迁移脚本。用户告诉 TPM "读取上游仓库 `https://github.com/Zehee/AgentCharter`，应用更新"即可。TPM 自动对比差异、建 TASK、执行变更、写 REPORT。

需要在文档中明确：这是 AgentCharter 的**标准升级方式**——不是临时变通，是框架设计意图。

## 推理链

- **Zehee**: "一个项目已经应用了 AgentCharter，有重大更新（如 DECISION 引入），用户对 TPM 说读取上游仓库应用更新——这种方法可行吗？"
- **Reasonix**: "完全可行。TPM 自己会读上游、理解变化、建 TASK、执行——和 DeepSeek 回来扫描 v3.3.0 一模一样的逻辑。"
- **Zehee**: "把对话记录下来，写成任务，然后更新文档，告诉用户这种更新方式。"

## 替代方案

1. 提供迁移脚本或 CLI → 违反零运行时哲学，否决
2. 只在 CHANGELOG 里描述变更，让人类手动操作 → 低效，违背"TPM 会自动做"的信任理念，否决

---

## 最终产物

| 类型 | 编号 | 说明 |
|------|------|------|
| TASK | 016 | 在 `collaboration/README.md` 新增"框架升级"章节（CN+EN） |
| TASK | 017 | 在 TPM.md 原则/§二 新增升级操作指引 |
| TASK | 018 | 在外层 README 新增"如何升级"小节 |
| REPORT | 016-018 | 合并完成报告 |
