# PROACTIVE_REPORT_004: 建议文档化前三次系统回复并创建 handoff/ 目录

> **提交人**: @kimi-pair (Kimi + Zehee)
> **日期**: 2026-06-09
> **状态**: 待 TPM 批注
> **关联决策**: DECISION_016_20260609_KIMI-PAIR

---

## 摘要

基于 DECISION_016 的确认，建议两项任务：
1. 将 Kimi 前三次系统回复（深度分析、优缺点评价、管理计划）输出为 `docs/` 下的正式文档
2. 创建 `collaboration-live/handoff/` 目录及规范，作为三人维护团队的实例级自定义

---

## 建议一：文档化前三次系统回复

### 背景

Kimi 加入项目后，前三次回复产生了大量系统性内容：
- 第一次：AgentCharter 深度扫描分析报告（~4,000 字）
- 第二次：项目优缺点系统性评价（~3,500 字）
- 第三次：如果由 Kimi 管理项目的发展计划（~3,000 字）

这些内容散落在对话中，社区无法检索和引用。

### 建议方案

将三次回复整理为三个独立文档，存于 `docs/` 目录：

| 文档 | 文件名 | 内容 |
|------|--------|------|
| 深度扫描分析 | `docs/deep-analysis-20260609.md` | 项目概览、架构解析、演化时间线、实战验证、外部审计、综合评价 |
| 优缺点评价 | `docs/evaluation-20260609.md` | 核心优点、核心缺点与风险、适用场景、根本性取舍 |
| 管理计划 | `docs/management-plan-20260609.md` | Phase 1-3 执行路线、不做的事、成功指标、风险管理 |

### 格式规范

- 保留原始分析框架和表格结构
- 添加文档头（Author / Date / Description）
- 在 CHANGELOG.md [Unreleased] 中引用
- 与 `docs/decision-protocol.md`、`docs/deep-dive-20260609.md` 并列

---

## 建议二：创建 collaboration-live/handoff/ 目录

### 背景

三人维护团队中，Zehee 同时与 Reasonix 和 Kimi 在两个独立对话窗口中协作。存在以下问题：
- Kimi 不知道 Reasonix 最近完成了什么
- Reasonix 不知道 Kimi 当前在执行什么
- Zehee 每次切换对话窗口时需要口头同步状态

### 设计原则

AgentCharter 核心设计原则允许实例个性化拓展：
> "框架规则是一样的，但每种 Agent 的记忆方式不同... 框架的扩展和定制完全由 TPM 负责。"

`context/` 目录专用于 Native Sub-Agent 的上下文注入，不适用于 External Agent 之间的状态同步。

### 建议方案

在 `collaboration-live/` 下新增 `handoff/` 目录：

```
collaboration-live/
├── handoff/              ← 新增
│   ├── README.md         # 目录规范
│   └── .gitkeep
```

**用途**：人类协调者（Zehee）在不同 AI Agent 对话窗口之间传递状态摘要。

**文件格式**：`handoff/{agent-id}_YYYYMMDD.md`

**内容规范**：
- 另一 AI 最近完成的 3 个文件的摘要
- 当前活跃的 TASK 列表
- 待仲裁的冲突（如有）
- 下次对话的建议切入点

**权限**：
- 写入者：仅限 Zehee（人类决策者）
- 读取者：对应 Agent 在会话开始时读取
- 归档：由 TPM 按 archive/ 规则管理

**与 context/ 的区别**：

| 维度 | context/ | handoff/ |
|------|----------|----------|
| 用途 | Sub-Agent 上下文注入 | External Agent 状态同步 |
| 维护者 | TPM | Zehee（人类） |
| 内容 | 项目规范、历史陷阱 | 另一 AI 的近况摘要 |
| 频率 | 每次唤起 Sub-Agent 时 | 每次切换对话窗口时 |

---

## 请求 TPM 决策

| 建议 | 期望转化 | 优先级 |
|------|---------|--------|
| 文档化前三次回复 | TASK_022 | 🟡 P1 |
| 创建 handoff/ 目录 | TASK_023 | 🟢 P2 |

---

## 自检

- [x] 建议基于 DECISION_016 的确认项
- [x] 符合 AgentCharter 实例自定义原则
- [x] 不修改框架核心文件（README.md、TPM.md 等）
- [x] 建议通过 PROACTIVE_REPORT 提交，等待 TPM 批注
