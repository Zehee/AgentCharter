# AgentCharter

> File-based governance for multi-agent teams.

[English](./README.md) · [中文](./README_CN.md)

基于文件的 AI 多智能体协作框架。通过目录结构、命名规范和协作链路表约束协作行为，不依赖任何平台或协议。

**AgentCharter 不是平等的协作**。它采用**中心化调度模式**——团队有一位最高管理者（TPM），统领全局、指挥调度、分析决策。其他 Agent 各司其职，通过他向 TPM 交付工作。这与 AutoGen/CrewAI 等"Agent 之间平等对话"的范式有根本不同。

> 📖 English version: [README.md](./README.md)

---

## 🚀 快速开始

### 1. 复制协作框架到你的项目

```bash
cp -r collaboration/ /my-project/
```

### 2. 对核心 Agent 说一句话

```
你是 TPM，分析 collaboration 目录并初始化
```

TPM 会分析目录结构、读取文档、理解框架规则，然后：
1. 在 👑 区域签上自己名字
2. 填写 `PROJECT.md`（团队配置、技术栈、构建命令）
3. 填写 `CHARTER.md`（协作宪章——所有规则的摘要）
4. 将 `CHARTER.md` 移至项目根目录

之后你不需要再动任何文件。

### 3. 其他 Agent 如何加入？

对其他 Agent 说：

```
分析 collaboration 目录并按照流程入职
```

Agent 读 `collaboration/README.md` → 👑 区域已有 TPM 名字 → 按 `REGISTER.md` 自助入职。你同样不需要干预。

---

## 🤔 为什么选择 AgentCharter？

AI 多智能体协作目前有三种主流方式。AgentCharter 是第四种。

### 📊 方式对比

| | 人工调度 | 编排框架 | 共享会话 | **AgentCharter** |
|--|---------|---------|---------|-----------------|
| **代表** | 你在 ChatGPT/Claude 里手动指挥 | AutoGen, CrewAI | 同一 IDE 多 Agent 直接对话 | — |
| **工作流定义** | 每次口头描述 | 代码（`RoundRobinGroupChat`） | 无定义，靠自觉 | **文件（ACTIONS.md 表）** |
| **协调开销** | 高（你当路由器） | 低（代码自动路由） | 无 | **零（文件即路由）** |
| **LLM 成本** | 每轮全体消耗 | 每轮全体消耗 | 同上下文，全体消耗 | **无协调调用** |
| **审计追溯** | 聊天记录，难检索 | 内存，丢失即消失 | 同一上下文易混乱 | **文件系统，Git 可查** |
| **跨模型兼容** | 取决于平台 | 绑定 SDK 和模型 | 绑定 IDE 和运行时 | **不绑定任何模型或平台** |
| **人类在场** | 被迫全程参与 | 只设初始参数 | 旁观 | **随时读文件介入** |
| **工作流可定制** | 灵活但非结构化 | 受限于框架 API | 无结构 | **编辑一页表即改整条链路** |
| **Agent 独立性** | 无 | 受 host 进程约束 | 同进程，互相影响 | **完全独立运行** |
| **运行位置** | 同一平台 | 同一进程/网络 | 同一 IDE | **任意环境、任意物理位置、跨区域** |

### 💡 AgentCharter 的核心区别

**1. 文件即路由，不产生协调开销**

其他框架的协调本身消耗 LLM token——决定"下一句话谁来接"就要跑一轮推理。AgentCharter 把这部分交给文件系统：Agent 写文件到目录，下游 Agent 巡检目录发现文件，零 token 完成通信路由。

**2. 协作链路由一张表定义——但你不需要写**

AutoGen 的 `GroupChat`、CrewAI 的 `SequentialProcess` 需要你写 Python 定义流程。AgentCharter 更进一步：你连表都不需要维护。你只需和 TPM 讨论协作流程——"Bob 写代码，Alice 审查，跨端改动时再让 Charlie 审一遍"——TPM 会理解需求，自己去更新 ACTIONS.md：
```
| 审查代码 | Alice → Bob   | REPORT → REVIEW_REPORT |
| 审查代码 | Charlie → Bob | REPORT → REVIEW_REPORT | (跨端改动)
```

**3. 完整的审计线索在 Git 里，不在内存里**

其他框架的通信记录在一次会话结束后消失。AgentCharter 的 inbox/outbox/reviews/logs 全部是文件，人类可以 `git log -- collaboration/archive/` 回溯任意时刻的决策链。

**4. 不绑定模型、平台、IDE**

External Agent 可以在任何支持文件读写的 AI 工具上运行——Claude Code、Cursor、终端 CLI。AgentCharter 只关心文件，不关心你是谁。

**5. Agent 可以运行在任何地方**

External Agent 不需要和 TPM 在同一个 IDE、同一台机器、甚至同一个国家。通信媒介是文件——只要 Agent 能读写文件系统，它在 Windows 上、Mac 上、远程服务器上、不同时区里，都能参与协作。你的前端 Agent 跑在 Cursor 里，后端 Agent 跑在终端 CLI 里，测试 Agent 跑在 CI 机器上——它们通过同一个 `collaboration/` 目录里的文件对话，彼此不知道也不关心对方在哪。

---

### 🆚 和 MCP 的区别是什么？

很多人第一次看到 AgentCharter 的反应："这不就是个文件版的 MCP 吗？"

**相似之处**：两者都是"让 AI 之间能协作"的协议，都追求跨平台、跨模型。AgentCharter 的 registry 概念（REGISTER.md → ACTIONS.md）在形式上接近 MCP 的 server 注册。

**本质区别**：

| | MCP | AgentCharter |
|--|-----|-------------|
| **解决什么问题** | Agent 如何调用**外部工具** | Agent 如何与**其他 Agent** 协作 |
| **通信对象** | Agent ↔ Tool（垂直） | Agent ↔ Agent（水平） |
| **核心概念** | Server 暴露 Tools/Resources/Prompts | TPM 分派 TASK，执行者提交 REPORT |
| **工作流** | 无（每次调用独立） | 完整生命周期（TASK → REPORT → 审查 → 归档） |
| **人工介入** | 不在设计范围内 | 文件通道天然支持人类随时读、随时干预 |
| **传输层** | JSON-RPC over stdio/HTTP | 文件系统（任何能读写文件的传输都行） |
| **运行依赖** | 需要启动 MCP Server 进程并保持连接 | **零运行时，无需任何服务进程** |

**一句话**：MCP 让一个 Agent 学会用锤子和锯子。AgentCharter 让一组 Agent 组成一个施工队——有人画图纸（TPM）、有人砌墙（Sub-Agent）、有人验收（Reviewer），工地上的所有指令和报告都是文件，工头随时能翻看。

---

### 🔧 可扩展性：框架会跟着你的团队长

AgentCharter 的模板和规则不是固化的——它们也是 TPM 维护的文件，存在 `collaboration/` 里。

如果你的协作流程需要**新的节点类型**（比如"安全审计"要在所有 P3 任务后触发）、**新的状态流转**（比如"等待客户确认"→"重新打开"）、**新的文件模板**（比如 `SAFETY_REPORT`），不需要等框架发版。流程是：

```
你 → 对 TPM 说："我们需要一个新的 X，像现有的 Y 那样，但多一个 Z 字段"
  → TPM 读 templates/ 理解模板规范 → 模仿现有模板创建新模板
  → TPM 更新 ACTIONS.md 加上新链路行
  → TPM 更新 TPM.md 加入新规则
  → 新流程从下一个 TASK 开始生效
```

**框架提供了范本和约束范式，TPM 负责按需派生。** 这个仓库里的 14 个模板、12 章规则，本身就是从 wolf-judge 实例的 120+ 个任务中生长出来的——你的项目也会长出属于自己的变体。

---

## 🧠 运行理念：TPM 核心制

AgentCharter 的核心是以 **TPM（Task Planning Manager）** 为中心的调度协作模式。

### T-P-M：三个维度，一个大脑

| 维度 | 字母 | 含义 | 具体表现 |
|------|------|------|----------|
| **Task** | T | 任务的创建与编排 | 创建 TASK、分派给合适的 Agent、驱动状态流转（ASSIGNED → REVIEW_PENDING → DONE） |
| **Planning** | P | 任务的规划与约束 | 常驻计划模式，生成任务清单，明确验收标准、代码规范、审查等级（P0-P3） |
| **Manager** | M | 任务的审批与协调 | 垄断审查终审权和 Git 操作，协调 Native Sub-Agent 和 External Agent 按规则推进 |

### 协作拓扑

```
                         ┌────────────────────────────────┐
                         │   TPM (Task Planning Manager)   │
                         │                                │
                         │     Task · Planning · Manager   │
                         │     唯一 Git 权限 · 终审决策    │
                         └───────────┬────────┬───────────┘
                                     │        │
                    文件通道          │        │  内部通道
                    (inbox/outbox)    │        │  (实时 diff / 审查)
                                     │        │
                         ┌───────────┘        └───────────┐
                         ▼                                ▼
              ┌───────────────────┐          ┌───────────────────┐
              │   External Agent  │          │ Sub-Agent (Native) │
              │                   │          │                   │
              │   独立环境运行     │          │   同运行时后台      │
              │   巡检 inbox 领取  │          │   等待 TPM 投递     │
              │   文件通道 REPORT  │          │   内部通道交付 diff  │
              └───────────────────┘          └───────────────────┘
```

**一句话**：TPM 是团队里唯一掌握全局的 Agent——它不写代码，只管"谁做什么、怎么做、做完了没"。所有通信经它调度，所有代码经它审批。

### 工作流不是写死的

AgentCharter **没有硬编码的工作流**。上面的拓扑图只是最简示例——你的团队可以完全不同。

真正定义协作关系的是 `ACTIONS.md`（协作链路表）。它是一张可自由编辑的表：

```
| 动作     | 发起方 → 接收方 | 通道        |
| 分配任务  | TPM → Alice    | inbox/TASK  |
| 审查代码  | Bob → Alice    | REVIEW_REPORT |
| 提交报告  | Alice → TPM    | outbox/REPORT |
| ...      | 任意 → 任意     | 任意通道      |
```

**你可以**：
- 让 Reviewer 直接审查代码作者而不经过 TPM
- 设置跨端改动时的串行审查链（A 审 → B 审 → TPM 决策）
- 为某个 Agent 同时配置"开发者"和"审查者"双重角色
- 让 Agent 之间直接互审，TPM 仅在 ACCEPT 后收到通知

**与固定工作流框架的本质区别**：AutoGen 的 `RoundRobinGroupChat`、CrewAI 的 `SequentialProcess` 需要你在代码中配置流程。AgentCharter 以 ACTIONS.md 文件为契约——改一行表，就改了一条协作通道。团队成员到达后读表即知自己的上下游，无需理解全貌。

---

## 📦 仓库结构

```
AgentCharter/
├── collaboration/                # ← 框架核心（复制到使用者项目根目录）
│   ├── README.md                     # 框架规范（Agent 读，12 章完整规则）
│   ├── CHARTER.md                     # 协作宪章模板（TPM 填写后移至项目根目录）
│   ├── TPM.md                         # TPM 行为准则
│   ├── PROJECT.md                    # 项目配置（填空模板）
│   ├── REGISTER.md                   # 入职登记表
│   ├── ACTIONS.md                    # 协作链路表（空模板，TPM 维护）
│   ├── dashboard.md                  # 项目看板 — TPM 定期汇总给人类看的进度报告
│   ├── templates/                    # 14 个文件模板
│   ├── context/                      # 上下文记忆文件
│   ├── inbox/ outbox/ reviews/ logs/ todos/ archive/
│
├── practices/                    # ← 社区实践案例
│   └── wolf-judge/                   # 5 人团队全栈实践
│
├── CHANGELOG.md
├── LICENSE (MIT)
└── README.md                     # 本文件
```

> **使用者部署**: 只需复制 `collaboration/` 到你的项目根目录。
>
> **`.gitignore` 配置**：忽略运行时通信目录（inbox/、outbox/、logs/、reviews/、context/、todos/），但 **`archive/` 建议纳入 Git**——已完成的 TASK、REPORT、REVIEW_REPORT 是永久审计线索，值得版本留存。框架文件（TPM.md、README.md 等）正常纳入。

---

## 🏗️ 核心概念

### 三种角色

| 角色 | 核心职责 | 通信方式 |
|------|---------|---------|
| **TPM** (Task Planning Manager) | 任务分派、计划编排、架构决策、Git 操作、最终审批 | 文件通道 + 内部通道 |
| **External Agent** | 编码、测试、审查 | 文件通道（inbox/outbox） |
| **Sub-Agent (Native)** | 编码（专注特定技术栈） | 内部通道 + 文件通道 |

### 文件交换协议

框架提供两种文件交换模式，但**实际协作流向由 `ACTIONS.md` 自定义**：

**任务驱动**：TPM 创建 TASK → inbox/ → Agent 领取 → 编码 → REPORT → ACTIONS.md 定义的审查链 → 归档
**主动报告**：任何人提交报告 → TPM 决策 → 归档

### 关键规则

| 规则 | 说明 |
|------|------|
| 双重审查 | 任何代码经另一位 AI 审查后才能合并 |
| Git 隔离 | 只有 TPM 可执行 git 命令 |
| 文件即契约 | 没有文件 = 没有发生 |
| 日志只追加 | 不修改历史 |

---

## 📚 实践案例

框架本身是抽象规则，实践案例展示了在真实项目中的配置方式。

| 实践 | 团队规模 | 技术栈 | 亮点 |
|------|---------|--------|------|
| [wolf-judge](./practices/wolf-judge/README.md) | 5 人 | Tauri + Rust + Vue 3 | P0-P3 分级审查、Sub-Agent 上下文记忆、120+ 任务闭环 |

> 更多实践案例欢迎贡献。详见 `practices/README.md`。

---

## 🤖 在 Agent 端是如何工作的？

Agent 不需要理解这个仓库——它们的入口是项目根目录的 `CHARTER.md`（TPM 初始化后从 `collaboration/` 移出的协作宪章）和 `collaboration/` 目录中的协作规则。

TPM 到达后：读 `collaboration/README.md` → 👑 签自己名 → 填 `CHARTER.md` + `PROJECT.md` → 移动 `CHARTER.md` 到根目录。读 `TPM.md` → 统治全局。

其他 Agent 到达后：读根目录 `CHARTER.md`（全局规则）→ 读 `collaboration/README.md` → 👑 非自己 → 读 `REGISTER.md` → 自助入职。

详见 `collaboration/README.md`（完整的 Agent 端协作规范，12 章）。

---

## 使用者项目结构（初始化后）

```
my-project/
├── CHARTER.md                   # ← 全局协作宪章（TPM 从 collaboration/ 移出）
├── collaboration/               # ← 框架核心
│   ├── README.md                    # Agent 端规范
│   ├── TPM.md                       # TPM 专属行为准则
│   ├── PROJECT.md                   # 项目配置（TPM 已填写）
│   ├── REGISTER.md                  # 入职登记表
│   ├── ACTIONS.md                   # 协作链路表（TPM 已配置）
│   ├── dashboard.md                 # 人类进度看板
│   ├── [运行时目录]                  # inbox/ outbox/ reviews/ logs/ ...
│
├── src/                          # 你的项目源码
└── .gitignore                    # collaboration/ 运行时目录已排除
```

---

## 📋 许可证

MIT License — 详见 `LICENSE`。