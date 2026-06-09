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
- **Zehee**: "把对话记录下来，写成任务，然后更新文档，告诉用户这种更新方式。另外还要提醒 TPM 升级时不要覆盖项目已有的 md 规则——他们可能增加了很多自定义内容，要合并而不是覆盖。"
- **Reasonix**: "对。升级是合并，不是覆盖。需要明确哪些文件是框架规范（可合并更新），哪些是项目实例（绝不能覆盖）。补进 README §十三、TPM.md §二、和本 DECISION。"

## 替代方案

1. 提供迁移脚本或 CLI → 违反零运行时哲学，否决
2. 只在 CHANGELOG 里描述变更，让人类手动操作 → 低效，违背"TPM 会自动做"的信任理念，否决

---

## 最终产物

| 类型 | 编号 | 说明 |
|------|------|------|
| TASK | 016 | 在 `collaboration/README.md` 新增"框架升级"章节（CN+EN），含合并原则和不可覆盖清单 |
| TASK | 017 | 在 TPM.md §二 新增升级操作指引，标注"合并，不是覆盖" |
| TASK | 018 | 在外层 README 新增"如何升级"小节 |
| REPORT | 016-018 | 合并完成报告 |

### 关键修正：合并原则

- **可合并更新的框架规范**：`templates/`（新模板直接加入）、`README.md`（新规则插入，不删现有内容）、`TPM.md`（新原则插入）
- **绝不能覆盖的项目实例**：`PROJECT.md`（用户已填写）、`ACTIONS.md`（用户已配置协作链路）、`CHARTER.md`（用户已签发的宪章）、`REGISTER.md`（已有的入职记录）、`dashboard.md`（用户的实时进度）
