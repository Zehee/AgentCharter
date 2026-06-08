# PROJECT: 新狼官

> 本文件由 TPM 维护。记录项目基本信息、团队成员、技术栈和构建命令。
> 通用协作框架见 `README.md`。

---

## 项目信息

- **名称**: 新狼官（狼人杀法官助手）
- **版本**: v2.0
- **技术栈**: 前端 Vue 3 + TypeScript / 后端 Rust + Tauri

## 团队成员

| 角色 | 标识 | 类型 | 说明 |
|------|------|------|------|
| TPM | Kimi | Native Host | 技术产品经理，兼 Native Sub-Agent 宿主 |
| External Agent | flash | External | 前端开发、测试、专项审查 |
| Sub-Agent | Peter | Native | 后端 Rust 开发 |
| Sub-Agent | Jim | Native Sub-Agent (常驻) | 后端 Rust 开发，**兼任 CodeReviewer** |
| External Agent | buddy | External | 测试员，执行手动和端到端测试 |
| External Agent | Designer | External | 前端视觉/交互审查、设计提案，**兼任 Reporter**（主动报告） |

## 构建命令

| 类型 | 命令 |
|------|------|
| 前端类型检查 | `vue-tsc --noEmit` |
| 前端构建 | `vite build` |
| 后端检查 | `cargo check` |
| 后端测试 | `cargo test` |

## 项目特定规则

1. **前后端分工**: 前端 UI/动画，后端 Rust 管状态/逻辑/存储，IPC 为唯一桥梁
2. **TypeScript 严格类型**: 核心模块禁 `any`
3. **后端 IPC 接口**: 44 个 IPC 命令（`docs/tech/ipc-contract.md`）
4. **双重审查**: 任何代码必须经过另一位 AI 审查后才能合并
5. **Native Sub-Agent 通信**: Peter/Jim 可读写全部协作文件（同 External Agent），按 memory 中循环读取规则执行

### 纪律红线

| 规则 | 说明 | 适用范围 |
|------|------|---------|
| **Git 禁令** | 任何 agent 严禁执行任何 git 命令（status、log、diff、checkout、restore、reset、stash 等），一刀切，无白名单 | 所有 agent |
| **前端隔离** | Peter 严禁修改任何前端文件（api/index.ts、views/、components/、stores/ 等） | Peter |
| **越界报告** | 工作目录问题、权限问题立即报告 Kimi，不得自行处理 | Peter、Jim |

### 审查分工

| 产出者 | 代码审查 | 设计审查 | 最终决策 |
|--------|---------|---------|---------|
| Peter | Jim（CodeReviewer） | — | Kimi |
| flash | Jim（CodeReviewer） | Designer | Kimi |
| Designer | — | Kimi | Kimi |

**跨端改动**（IPC/数据结构/共享模型）：Jim 审查 → flash 专项审查 → Kimi 最终决策

---

## 项目实例特有规则

### Dashboard 与归档

| 规则 | 设置 | 说明 |
|------|------|------|
| Dashboard 更新频率 | **每日更新**（非实时） | 在每日巡检时一并更新 |
| 归档保留期限 | 按文件类型区分（见 README.md 3.6 节） | TASK/REVISION 领取后即归档；REPORT/REVIEW_REPORT 保留 1 天；NOTICE 及时归档 |
| 报告格式 | 保持模板详细格式 | 确保可追溯性和用户可读性 |

### 任务分发原则

**核心目标**：不让 agents 空闲，但避免 sub-agent 超时。

| Agent | 策略 | 说明 |
|-------|------|------|
| **Peter**（Native Sub-Agent） | **尽量少** | sub-agent 不稳定，任务过多易超时。保持 1-2 个活跃任务即可 |
| **flash**（External） | **可以多一点** | 稳定，可并行处理多个任务 |
| **Jim**（Native Sub-Agent） | 按需唤醒 | 不通过 inbox 分派，由 Kimi 在代码产出后主动唤醒 |
| **Designer**（External） | **主动指派** | 不同于 flash 的被动领取模式。Kimi 主动指派设计任务，Designer 完成后主动提交报告 |

**分发原则**：
1. **积极分发** — inbox 为空时立即分配新任务
2. **至少 2 条** — 尽量保证每个成员至少有 2 个任务（Peter 除外）
3. **至多不限** — flash 和 Designer 不设上限
4. **确定需求先发** — 已经明确需要执行的需求要全部作为任务设置好优先级分发出去，避免遗忘
5. **任务粒度** — 复杂场景拆细（1-2 天可交付）、简单场景保持完整

## 开发模式

**敏捷渐进式开发（Agile Incremental）**

| 原则 | 说明 |
|------|------|
| 迭代周期 | **无固定 Sprint**，看板驱动，任务完成即交付 |
| 设计基线 | `PRODUCT_DESIGN` / `INTERACTION_SPEC` / `USER_FLOWS` 为基线参考，变更走轻量评审（Kimi 快速批准） |
| 任务粒度 | TPM 按需判断，复杂场景拆细（1-2 天可交付）、简单场景保持完整 |
| 交付节奏 | 持续流动，不批处理审查，完成即审查即合并 |
| 变更控制 | 取消 CHANGE_REQ 重流程，设计/需求变更由 Kimi 评估后直接分派 |
