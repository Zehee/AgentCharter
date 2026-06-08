# AgentCharter

> 🗂️ File-based governance for multi-agent teams.
> 👉 试一下：对你的 Agent 说 *"评价这个仓库 — https://github.com/Zehee/AgentCharter"*

[English](./README.md) · [中文](./README_CN.md)

基于文件的 AI 多智能体协作框架。Agent 之间通过共享目录通信——不依赖 SDK、不需要服务、不绑定平台。**把 `collaboration/` 放进项目，告诉你的核心 Agent 它是 TPM，结束。**

---

## 🚀 快速开始

### 1. 复制

```bash
cp -r collaboration/ /my-project/
```

### 2. 告诉你的核心 Agent

> 把这句话直接发给你的 AI——在任何你平时跟它对话的地方（IDE 对话框、终端、网页）。就这么简单。

```
你是 TPM，阅读 collaboration 目录并开始工作
```

TPM 读取框架、在 👑 区签上自己的名字、填写 `PROJECT.md` + `CHARTER.md`、把宪章移至项目根目录。**这就完了。**

<details>
<summary>👇 说这句话后到底发生了什么？</summary>

Agent 读取 `collaboration/` 后发现：
1. **👑 签自己名字** — 把 `README.md` 中的占位符替换为自己的名字
2. **填写 `PROJECT.md`** — 向你询问项目名称、技术栈、构建命令、团队成员
3. **填写 `CHARTER.md`** — 从 `README.md` 和 `TPM.md` 汇总关键规则形成协作宪章
4. **把 `CHARTER.md` 移到项目根目录** — 所有 Agent（包括人类）都能读到最高规则
5. **读 `TPM.md`** — 了解完整权限：分派任务、驱动审查、独掌 Git、更新看板

从此以后，没有任何 Agent 会不经 `TASK` 文件就去改 `src/`。除了 TPM，没有人执行 `git`。一切都在 `inbox/` → `outbox/` → `reviews/` → `archive/` 里流转。

</details>

### 3. 引入更多 Agent

> 同样 — 把这句话发给每个新 Agent：

```
阅读 collaboration 目录并加入协作
```

它们读 👑 区、看到不是自己的名字、按 `REGISTER.md` 自助入职。你不再需要碰任何文件。

---

## 🧠 怎么工作的

AgentCharter 围绕一个中心角色构建——**TPM (Task Planning Manager)**。TPM 不写代码。它计划、分派、审查、汇报。

### 三种角色，一个大脑

| 角色 | 性质 | 职责 |
|------|--------|----------------|
| 👑 **TPM** | 项目的管理者 Agent | 拆工作为 TASK 文件、分派、驱动审查、独揽 Git、更新人类看板 |
| 📁 **External Agent** | 运行在任何地方、任何工具 | 巡检 `inbox/` 找自己的 TASK、编码、提交 REPORT 文件 |
| 🔗 **Sub-Agent (Native)** | 后台常驻、同运行时 | 等待 TPM 投递、直接交付代码 diff、写 REPORT 留痕 |

### T-P-M：TPM 具体做什么

| | T · Task | P · Planning | M · Manager |
|--|----------|-------------|------------|
| **创建** | 在 inbox/ 写 TASK | 带验收标准的任务清单 | 协作链路表 (ACTIONS.md) |
| **驱动** | 状态流转 (ASSIGNED → REVIEW_PENDING → DONE) | 代码规范、审查等级 (P0–P3) | 审查闭环、终审、Git commit |
| **维护** | 巡检 outbox/ 发现新 REPORT | 人类看板、Sub-Agent 上下文记忆 | 归档、Agent 入职、框架扩展 |

```
                         ┌────────────────────────────────┐
                         │   TPM (Task Planning Manager)   │
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
              │   独立环境运行     │          │   后台常驻          │
              │   巡检 inbox 领取  │          │   等待 TPM 投递     │
              │   文件通道 REPORT  │          │   内部通道交付 diff  │
              └───────────────────┘          └───────────────────┘
```

### 工作流是表，不是代码

协作链路全在一张表——`ACTIONS.md`。加一行，加一条通道：

| 动作     | 发起方 → 接收方 | 通道           |
|----------|----------------|----------------|
| 分配任务  | TPM → Alice    | inbox/TASK     |
| 审查代码  | Bob → Alice    | REVIEW_REPORT  |
| 提交报告  | Alice → TPM    | outbox/REPORT  |

改一行，改一条协作链路。Agent 读表就知道上下游。不需要 Python 脚本，不需要框架 API。

---

## 📊 与其他方案对比

| | 人工调度 | AutoGen / CrewAI | MCP | **AgentCharter** |
|--|-----------------|-------------------|-----|-----------------|
| **解决的什么** | 你手动指挥 | Agent 之间自动对话 | Agent↔工具（垂直） | Agent↔Agent（水平） |
| **工作流定义** | 口头描述 | Python 代码 | 服务端配置 | **ACTIONS.md 文件表** |
| **协调开销** | 你的时间 | 每轮消耗 LLM token | 服务进程 | **零 — 文件即路由** |
| **审计追溯** | 聊天记录 | 内存，会话结束消失 | 无 | **文件系统，Git 可查** |
| **跨模型** | 绑定平台 | 绑定 SDK | 绑定协议 | **任何能读写文件的工具** |
| **工作流灵活度** | 灵活但非结构化 | 受框架 API 限制 | 无（无状态） | **改一行表** |
| **Agent 运行位置** | 同一平台 | 同一进程/网络 | 需要活服务 | **任意位置 — 跨机器、跨区域** |

**一句话**：MCP 教 Agent 用工具。AgentCharter 组施工队——画图（TPM）、砌墙（Sub-Agent）、验收（Reviewer）——每一条指令都是文件，工头随时能翻。

### 🔧 框架跟着你的团队成长

需要新节点？新状态？新模板？告诉 TPM。它读 `templates/`、模仿范本、更新 `ACTIONS.md`，下一个 TASK 就按新流程走。不用等框架发版。这 14 个模板和 12 章规则，本身就是 120+ 个真实任务中长出来的——你的也会。

---

## 📚 实践案例

看真实项目怎么跑：

| 案例 | 团队 | 技术栈 | 亮点 |
|------|------|-------|------------|
| [wolf-judge](./practices/wolf-judge/README.md) | 5 人 | Tauri + Rust + Vue 3 | P0–P3 分级审查、Sub-Agent 记忆注入、120+ 任务闭环 — [查看真实文件](./practices/wolf-judge/examples/) |

---

## 📦 文件层级（从高到低）

```
/CHARTER.md              ← 项目级宪章 — TPM 根据模板生成，移至项目根，所有 Agent 的最高规则
/collaboration/
  ├── README.md          ← Agent 操作手册 — 只定义规则和流程，不落地具体决策
  ├── TPM.md             ← TPM 行为准则
  ├── PROJECT.md         ← 项目配置
  ├── REGISTER.md        ← Agent 入职登记
  ├── ACTIONS.md         ← 协作链路表
  └── inbox/ outbox/ reviews/ logs/ ...  ← 运行时通信空间
```

> **关键区分**：`collaboration/README.md` 定义"如何协作"的规则；`/CHARTER.md` 定义"我们这个项目的具体选择"。

## 📦 仓库结构

```
AgentCharter/
├── collaboration/           # 框架核心（中文）— 复制到你的项目根目录
│   ├── README.md                # Agent 端规范（12 章）
│   ├── CHARTER.md               # 协作宪章模板 → TPM 移至项目根目录
│   ├── TPM.md                    # TPM 行为准则
│   ├── PROJECT.md               # 项目配置（填空）
│   ├── REGISTER.md              # Agent 入职登记
│   ├── ACTIONS.md               # 协作链路表（空模板）
│   ├── dashboard.md             # 给人类看的进度报告
│   ├── templates/               # 14 个文件模板
│   └── inbox/ outbox/ reviews/ logs/ todos/ archive/
│
├── collaboration_en/        # 同上，英文版
├── practices/               # 社区实践案例
│   └── wolf-judge/              # 5 人团队全栈实践
│
├── .github/                 # Issue & PR 模板
├── CHANGELOG.md
└── LICENSE (MIT)
```

> **部署**：复制 `collaboration/`（中文）或 `collaboration_en/`（英文）到你的项目根目录。
>
> **`.gitignore`**：忽略 `inbox/ outbox/ logs/ reviews/ context/ todos/`——这些是运行时状态，纳入版本控制反而有害（`git checkout` 会回滚正在执行的任务分派和审查进度）。**但 `archive/` 留在 Git 里**——已完成的 TASK、REPORT、REVIEW_REPORT 是永久审计线索。框架文件正常纳入版本控制。
>
> **初始化后**，你的项目长这样：
> ```
> my-project/
> ├── CHARTER.md              # ← 全局宪章（TPM 移出）
> ├── collaboration/          # ← 框架（Agent 工作区）
> ├── src/                    # ← 你的代码
> └── .gitignore
> ```

---

## 📋 许可证

MIT — 详见 [LICENSE](./LICENSE)。
