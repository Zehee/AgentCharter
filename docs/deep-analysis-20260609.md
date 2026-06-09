# AgentCharter 深度扫描分析报告

> **Author**: Kimi (External Agent, @kimi-pair)
> **Date**: 2026-06-09
> **Description**: 基于完整源码、文档、实战案例和演化历史的系统性深度分析

---

## 一、项目概览

| 维度 | 数据 |
|------|------|
| **项目** | AgentCharter — 基于文件的 AI 多智能体协作框架 |
| **作者** | Zehee |
| **当前版本** | v3.3.0（2026-06-10） |
| **仓库** | https://github.com/Zehee/AgentCharter |
| **许可证** | MIT |
| **规模** | 162 文件 / 129 个 Markdown / ~9,800 行 |
| **Git 提交** | 70 次 |
| **语言** | 双语（中文 `collaboration/` + 英文 `collaboration_en/`） |
| **开发周期** | 2026-05-30 至今（11 天，高频迭代） |

---

## 二、核心定位

> **"Trust, Not Control"（信任，而非控制）**

AgentCharter 不是传统意义上的 AI Agent 框架。它**零运行时、零 SDK、零 API 调用**——唯一的基础设施是文件系统 + Markdown + Git。

> "Most AI frameworks assume agents are untrusted — they need API keys, sandboxing, permission tiers. AgentCharter takes the opposite approach: trust that agents will read and follow the protocol, the same way we trust humans to follow Git conventions."

这是一个根本性的哲学翻转：不通过代码强制执行约束，而是通过文件协议建立共识。约束不是锁链，而是共识。

---

## 三、架构深度解析

### 3.1 三元角色模型

| 角色 | 本质 | 通信通道 | 记忆方式 |
|------|------|----------|----------|
| **TPM** (Task Planning Manager) | 人机结对综合体 | 文件 + 内部通道 | 运行环境本地记忆 |
| **External Agent** | 人机结对综合体 | 文件通道 (inbox/outbox) | 运行环境本地记忆 |
| **Sub-Agent (Native)** | 纯 AI，无对话入口 | 内部通道 + 文件留痕 | `context/{name}-memory.md` 注入 |

**关键洞察**：TPM 和 External Agent 默认都是"人机结对"——一个人类 + 一个 AI 在同一对话窗口中协作。

### 3.2 文件即通信渠道

```
collaboration/
├── README.md          # Agent 操作手册（12 章，404 行）
├── TPM.md             # TPM 行为准则（10 章，430 行）
├── CHARTER.md         # 项目宪章模板 → 初始化后移至项目根目录
├── PROJECT.md         # 项目配置（技术栈、成员、规则）
├── REGISTER.md        # Agent 入职登记表
├── ACTIONS.md         # 协作链路表（谁→谁，通过什么通道）
├── dashboard.md       # 给人类看的进度报告
├── templates/         # 15 个标准文件模板
├── inbox/             # TPM 写，执行者读（TASK/REVISION/NOTICE/REPLY）
├── outbox/            # 执行者写，TPM 读（REPORT/PROACTIVE_REPORT/BLOCKING）
├── reviews/           # Reviewer 写，所有人读（REVIEW_REPORT）
├── decisions/         # 人机结对决策记录（DECISION）
├── logs/              # 每人独占一份操作日志
├── todos/             # TPM 维护的排期事项
├── context/           # Sub-Agent 上下文记忆（TPM 注入用）
└── archive/           # 永久审计线索（纳入 Git）
```

### 3.3 15 个标准模板

框架提供 15 个文件模板（v3.3 新增 DECISION 为第 15 个）。团队通常从 3-4 个开始，随需求增长逐步引入。

### 3.4 增量文件链 = 天然不可否认

**任务状态不靠修改文件，而靠创建新文件推进**：

```
TASK_053 → REPORT_053 → REVIEW_REPORT_053 → REPORT_053_R1 → REVIEW_REPORT_053_R1 → ACCEPT
```

每个 Agent 只在自己的命名空间里写入**新文件**，不修改、不覆盖他人文件。历史是一串不可篡改的增量文件链。

### 3.5 并发安全：设计层消除冲突

| 传统方案 | AgentCharter |
|---------|-------------|
| 运行时文件锁 / 数据库事务 | 文件名唯一性（`NNN_DATE_AUTHOR`）|
| 状态机管理 | 增量文件链 |
| 权限系统（RBAC/ACL）| 目录写域隔离（inbox 仅 TPM 写，outbox 仅执行者写）|
| 覆盖冲突检测 | 设计为只追加、不修改 |

> DeepSeek 外部审计评价："不是'忘了做并发控制'，而是设计阶段就把冲突可能消除了。比运行时文件锁高一维。"

### 3.6 P0-P3 分级审查体系

| 级别 | 判定标准 | 审查深度 | TPM 介入度 |
|------|----------|----------|------------|
| **P0** | 单文件、纯 UI/样式/文案 | 无 Reviewer，TPM 直接 commit | 0 |
| **P1** | 2-3 文件、组件级逻辑 | Reviewer 审 + 【审查摘要】| 5-10 行 |
| **P2** | 跨模块、数据流、新增 IPC | Reviewer 审 + 完整报告 | 摘要+关键意见 |
| **P3** | 架构/安全/核心流程 | Reviewer 审 + TPM 深度验证 | 完整介入 |

---

## 四、演化时间线

| 日期 | 版本 | 里程碑 |
|------|------|--------|
| 2026-05-30 | v0.1.0 | 初始发布，8 个模板 |
| 2026-06-06 | v3.2.0 | 大幅扩展至 13 章，wolf-judge 实践案例系统 |
| 2026-06-08 | v3.2.x | 双语支持、CHARTER.md 根迁移、TPM 核心原则重写 |
| 2026-06-09 | v3.3.0-dev | DeepSeek 21 轮深度对话，发现 DECISION 空白 |
| 2026-06-10 | **v3.3.0** | DECISION 文件类型、collaboration-live 自食狗粮实例、信任哲学 |

---

## 五、实战验证

### 5.1 collaboration-live 实例

AgentCharter 团队用 AgentCharter 管理自身。`collaboration-live/` 是开放的实时治理实例：

| 类型 | 数量 | 说明 |
|------|------|------|
| DECISION | 17 | 全部由 `@tpm-pair (Reasonix + Zehee)` 产生 |
| TASK | 27 | TPM 分派 |
| PROACTIVE_REPORT | 4 | 框架进化提案 + 入职报告 |
| REPORT | 14 | 任务执行报告 |

**DECISION 文件质量**：每份包含结对标识、时间、决策、推理链（逐字对话）、替代方案、最终产物表格。

### 5.2 wolf-judge 项目

| 指标 | 数据 |
|------|------|
| 团队规模 | 5 个 Agent |
| 技术栈 | Tauri v2 + Rust + Vue 3 |
| 累计任务 | 120+ |
| 累计审查 | 60+ 份 REVIEW_REPORT |
| 代码规模 | Rust ~15K 行 / Vue ~20K 行 |
| IPC 命令 | 44 个 |
| 协作文档 | 180+ 文件 |

**关键创新**：Jim 一人两角（后端开发 + CodeReviewer）、Designer 阅后即焚模式、跨端改动追加 flash 专项审查、P0-P3 分级审查、Sub-Agent 上下文记忆注入。

---

## 六、外部审计：DeepSeek 21 轮对话

Zehee 与 DeepSeek 进行了一场 21 轮的外部审计对话：

### 6.1 赛道定位

AgentCharter 属于正在形成的 **"文件原生 Agent（File-Native Agent）"** 派系。DeepSeek 定位了 6 个同类项目：ACTA、OpenFused、greatminds、PULSE、AAHP、Agent Business Factory。

**结论**：AgentCharter 在同类中**架构最完整、协议最丰富、审查机制最严密**。

### 6.2 系统性空白：决策过程未被记录

DeepSeek 发现核心缺口：**PROACTIVE_REPORT 只记录决策的产物（"建议 X"），不记录决策的过程（"为什么建议 X"）**。

造成四个子问题：决策上下文不可审计、结对认知劳动重复、经验无法跨团队沉淀、任务因果链断裂。

### 6.3 最小化落地（已被采纳）

不是 DeepSeek 建议的三层体系（PAIR_SESSION + DECISION_DELTA + PROACTIVE_REPORT），而是极简方案：

- ✅ **一种文件类型**：`DECISION_NNN_DATE_AUTHOR.md`
- ✅ **一个目录**：`decisions/`
- ✅ **两条规则**：README.md §6 结对决策记录 + TPM.md §一 原则 #10 战略决策文件化

### 6.4 哲学基石

> "AgentCharter 不仅仅是一个协作框架。它是一种宣言：人类和 AI 可以基于信任和文件，平等地共同创造。"

---

## 七、综合评价

| 维度 | 评分 | 说明 |
|------|------|------|
| **架构简洁性** | ⭐⭐⭐⭐⭐ | 零运行时，纯 Markdown，15 个模板 |
| **并发安全性** | ⭐⭐⭐⭐⭐ | 设计层消除冲突，无需文件锁 |
| **可审计性** | ⭐⭐⭐⭐⭐ | Git + 增量文件链，每个字节可追溯 |
| **人类友好度** | ⭐⭐⭐⭐⭐ | 会编辑文本即可参与，极低门槛 |
| **跨模型兼容性** | ⭐⭐⭐⭐⭐ | 任何能读/写文件的 AI 均可加入 |
| **审查机制** | ⭐⭐⭐⭐⭐ | P0-P3 四级 + 【审查摘要】流转 |
| **生态成熟度** | ⭐⭐⭐☆☆ | 仅 11 天历史，1 个实战案例 |
| **工具链集成** | ⭐⭐☆☆☆ | 无 IDE 插件，无 CLI，纯手动 |
| **规模化能力** | ⭐⭐⭐☆☆ | 理论上可扩展，缺乏大规模验证 |

---

## 八、竞品对比

| 维度 | Manual | AutoGen/CrewAI | MCP | **AgentCharter** |
|------|--------|----------------|-----|-----------------|
| 工作流定义 | 口头临时 | Python 脚本 | 服务器配置 | **ACTIONS.md 表格** |
| 协调成本 | 你的时间 | LLM tokens/轮 | 服务器运行时 | **零 — 文件即路由** |
| 审计线索 | 聊天记录 | 内存，关闭即失 | 无 | **Git 可搜索的文件系统** |
| 跨模型 | 平台锁定 | SDK 锁定 | 协议锁定 | **任何读/写文件的即可** |
| 工作流灵活性 | 无结构 | 受限于框架 API | 无状态 | **编辑表格行即可** |
| Agent 运行位置 | 同平台 | 同进程/网络 | 需在线服务器 | **任何地方，跨机器跨区域** |

---

> **一句话总结**：AgentCharter 不是教 AI 如何协作的**框架**，而是为人类和 AI 共同书写的**协议宪章**。
