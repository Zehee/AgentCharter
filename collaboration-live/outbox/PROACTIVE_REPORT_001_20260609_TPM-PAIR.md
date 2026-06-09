# 🔍 PROACTIVE_REPORT_001: 决策记录协议开放实验

> **文件名**: `PROACTIVE_REPORT_001_20260609_TPM-PAIR.md`
> **存放位置**: `outbox/`
> **性质**: 主动报告（无对应 TASK）

**提交人**: @tpm-pair (Reasonix + Zehee)
**日期**: 2026-06-09
**关联决策**: DECISION_001, DECISION_002, DECISION_003, DECISION_004

---

## 范围与目标

**范围**：AgentCharter v3.2 框架的新增决策记录（DECISION）文件类型、新增"人机结对"角色声明、以及本项目的首批协作实例文件。

**目标受众**：
- 未来的 AgentCharter 社区贡献者
- 任何想了解"文件协作框架如何在真实项目中运行"的开发者

---

## 发现与分析

### 新增内容

1. **第 15 种文件模板**：`DECISION_NNN_DATE_AUTHOR.md`，存放在 `decisions/` 目录。人机结对 Agent 在对话中产生决策时，AI 提取推理链并写入。

2. **双向引用链**：TASK 新增 `决策来源` 字段，PROACTIVE_REPORT 新增 `关联决策` 字段，TODO 的 `来源类型` 新增 "决策" 选项。

3. **角色定义更新**：TPM 和 External Agent 明确标注为"默认人机结对"，Sub-Agent (Native) 明确标注为"纯 AI"。

4. **结对决策记录规范**：在 collaboration/README.md §六 旁边新增完整的使用说明章节。

5. **TPM 新核心原则**：TPM.md §一新增第 10 条——"你的战略决策也需要文件化"。

6. **首批协作实例**：`collaboration-live/` 目录包含本项目自身的 4 个 DECISION + 6 个 TASK + 2 个 TODO。每个文件都遵循框架模板格式，是活的参考范本。

7. **协议文档**：`docs/decision-protocol.md`，完整的可选规范文档，覆盖格式、触发条件、信息流、关联关系和归档规则。

---

## 优先级改进清单

### 🔴 P0 - 立即生效
1. **社区可见性**：本报告发布后，`collaboration-live/` 目录将成为社区的第一个协作实例参考。

### 🟡 P1 - 近期优化
1. **社区引导**：在 Discussions 中引导社区贡献者使用自己的 DECISION 和 PROACTIVE_REPORT 提交反馈。

### 💡 P2 - 建议改进
1. **社区工具**：CLI 辅助脚本、Dashboard 决策追溯视图——留给社区独立开发。
2. **更多实践案例**：wolf-judge 之外，期待社区提供其他项目的协作实例。

---

## 总结

**整体设计评分**：N/A — 自我评估由社区完成

**优势**：
- 用自己框架生产了第一批决策链文档，自证了"文件即协议"的可工作性
- 从 DECISION → TASK → 代码变更，形成完整的因果追溯链
- 人机结对作为一等公民，在文档和实例中双向体现

**待改进**：
- `collaboration-live/` 中的 TASK_001 到 TASK_006 需要继续执行并产出 REPORT
- PAIR_SESSION 概念留给社区试点

**建议行动**：
1. 社区成员：阅读 `docs/deep-dive-20260609_en.md` 了解本协议的来龙去脉
2. 贡献者：用自己的人机结对创建 DECISION → PROACTIVE_REPORT → 提交 Discussion
3. 所有人：`collaboration-live/` 是开放的——它不是一个只读展览，而是一个活的协作空间

---

**提交人**: @tpm-pair (Reasonix + Zehee)
**日期**: 2026-06-09
