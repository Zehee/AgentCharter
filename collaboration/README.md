# AgentCharter

> ⚠️ 这是一个 **Agent 操作手册**，不是项目宪章。项目宪章由 TPM 生成并存放在项目根目录 `/CHARTER.md` 中。本文件定义规则和流程，宪章定义本项目的具体决策。

基于文件的 AI 多智能体协作框架。文件是唯一的通信渠道和审计线索。

> **没有文件 = 没有发生。**

**版本**: v3.2 | **更新**: 2026-06-09

---

## 👑 最高指挥官（TPM）

  - 本项目的 TPM 是 **[如果用户明确告诉你是 TPM 请把这里替换为你的名字]**

> 你是 TPM → 签自己名字 → 读 `TPM.md` 开始工作
> 你不是 TPM → 先读完本文件理解框架 → 然后读 `REGISTER.md` 加入协作

---

## 一、框架规则

### 1.1 通信通道

| 通道 | 谁用 | 方式 | 规则 |
|------|------|------|------|
| **文件通道** | TPM、External Agent | inbox/outbox 读写 | 异步可追溯 |
| **内部通道** | TPM ↔ Sub-Agent (Native) | Host 直连 | 实时交付 diff |

### 1.2 三种角色

| 角色 | 职责 | 通道 |
|------|------|------|
| **TPM** | 分派任务 T、编排计划 P、审批协调 M、Git 唯一权限 | 文件 + 内部 |
| **External Agent** | 巡检 inbox/ 领取任务，编码，提交 REPORT | 文件通道 |
| **Sub-Agent (Native)** | 等待 TPM 内部投递，编码，内部交付 diff + outbox/REPORT 留痕 | 内部 + 文件 |

### 1.3 通信协议

协作流程由 `ACTIONS.md` 定义，非框架硬编码。以下是两种基础文件交换方式：

**任务驱动**：TPM 写 TASK → inbox/ → 执行者领取 → 编码 → 写 REPORT → 审查 → 归档

**主动报告**：任何人写 PROACTIVE_REPORT → TPM 批注决策 → 归档

> **规模说明**：文件系统扫描是常数时间操作。100 个文件还是 1000 个文件，Agent 打开目录的开销几乎相同——瓶颈是 LLM 上下文窗口，不是 I/O。框架的简洁目录结构就是天然的索引。先用起来，规模到了再说。

> **增量文件链**：整个任务的状态流转不是靠修改同一个文件，而是靠一系列增量文件串联起来——`TASK_NNN` → `REPORT_NNN` → `REVIEW_REPORT_NNN` → `REPORT_NNN_R1` → …。每个 Agent 只在自己的命名空间里写入**新文件**，不修改、不覆盖他人的文件。历史是一串不可篡改的增量文件链，天然不可否认。

### 1.4 硬性规则

| 规则 | 内容 |
|------|------|
| **文件即契约** | 所有任务、报告、审查、阻塞必须通过文件传递 |
| **并发安全** | 每个 Agent 写入的文件是**指向性、唯一性、增量性的**——`ACTIONS.md` 预先分配通道，inbox/ 仅 TPM 写入，outbox/ 每个 Agent 有独立命名空间。每次写入是一个新文件（TASK_NNN、REPORT_NNN_DATE_AUTHOR 等），不存在覆盖、追加或共享写入。文件冲突在设计层已被消除 |
| **Git 权限隔离** | 只有 TPM 可执行任何 git 命令。其他 Agent 严禁。一刀切，无白名单 |
| **双重审查** | 任何代码经另一位 AI 审查后才能合并 |
| **日志只追加** | logs/、ACTIONS.md、dashboard.md 只追加，不修改历史 |
| **inbox 写域** | TPM 写，执行者只读不删 |
| **outbox 写域** | 执行者写，TPM 只读不删不修改 |
| **logs/** | 每人独占一份 `{标识}-log.md`，他人只读 |
| **ACTIONS.md / dashboard.md / todos/** | 只有 TPM 能写 |
| **阻塞** | 写 `BLOCKING` 到对方读目录；解除写 `BLOCKING_REPLY` |

---

## 二、目录与权限

```
collaboration/
├── README.md              本文件
├── CHARTER.md             协作宪章模板（TPM 填写后移至项目根目录）
├── TPM.md                  TPM 行为准则
├── PROJECT.md             项目配置（技术栈、成员、规则）
├── REGISTER.md            入职登记表
├── ACTIONS.md             协作链路表（空模板，TPM 维护）
├── dashboard.md           TPM 维护，给人类看的进度报告；人类发现错误可以在这里写指令，TPM 巡检时读取
├── context/               Sub-Agent 上下文记忆（TPM 维护）
├── inbox/                 TASK / REVISION / NOTICE / REPLY
├── outbox/                REPORT / PROACTIVE_REPORT / BLOCKING
├── reviews/               REVIEW_REPORT（Reviewer 写，所有人读）
├── logs/                  每人独占一份操作日志
├── todos/                 TODO 排期事项（TPM 维护）
├── templates/             14 个文件模板（只读基准）
└── archive/               已完成归档（inbox / outbox / reviews / events）
```

| 路径 | 谁写 | 谁读 |
|------|------|------|
| `inbox/` | TPM | 执行者只读 |
| `outbox/` | 执行者 | TPM 只读 |
| `reviews/` | Reviewer + TPM | 所有人 |
| `logs/` | 每人独占 | 他人只读 |
| `ACTIONS.md` | TPM | 所有人 |
| `dashboard.md` | TPM | 人类 |
| `todos/` | TPM | 所有人 |
| `context/` | TPM | Sub-Agent |

> `inbox/ outbox/ logs/ reviews/ context/ todos/` 加入 .gitignore。`archive/` 纳入 Git 作为永久审计线索。

---

## 三、命名规范

- **段间 `_`**，**段内 `-`**
- `NNN` = 3 位编号（001、042、049C_R1）
- `DESC` = 英文简短描述，段内用 `-`
- `ASSIGNEE` / `AUTHOR` / `TARGET` = 标识一律**大写**
- `DATE` = `YYYYMMDD`

```
TASK_053_HUNTER-SHOOT-BACKEND_PETER.md
REPORT_053_20260530_PETER.md
REVISION_049C_20260530_FLASH.md
```

---

## 四、文件类型速查

| 文件类型 | 模板 | 位置 | 谁写 |
|----------|------|------|------|
| 任务 | `TASK_NNN_DESC_ASSIGNEE.md` | inbox/ | TPM |
| 测试任务 | `TASK_TEST_NNN_DESC_ASSIGNEE.md` | inbox/ | TPM |
| 修订任务 | `REVISION_NNN_DATE_ASSIGNEE.md` | inbox/ | TPM |
| 通知 | `NOTICE_NNN_DESC_DATE_TARGET.md` | inbox/ | TPM |
| 回执 | `REPLY_NNN_DESC_DATE_AUTHOR.md` | inbox/ | TPM |
| 任务报告 | `REPORT_NNN_DATE_AUTHOR.md` | outbox/ | 执行者 |
| 测试报告 | `TEST_REPORT_NNN_DATE_AUTHOR.md` | outbox/ | 测试员 |
| 主动报告 | `PROACTIVE_REPORT_NNN_DESC_DATE_AUTHOR.md` | outbox/ | 任何人 |
| 审查报告 | `REVIEW_REPORT_NNN_DATE_AUTHOR.md` | reviews/ | Reviewer |
| 阻塞通知 | `BLOCKING_NNN_DATE_TARGET.md` | outbox/ | 阻塞方 |
| 阻塞回复 | `BLOCKING_REPLY_NNN_DATE_AUTHOR.md` | outbox/ | 解除方 |
| 待办 | `TODO_NNN_DESC_SOURCE.md` | todos/ | TPM |
| 日志 | `{标识}-log.md` | logs/ | 每人 |

### 写文件规则

> 团队通常从 3-4 个模板开始（TASK、REPORT、REVIEW_REPORT），随需求增长逐步引入。14 个模板是框架提供的最大集合，不是必用清单。

1. 从 `templates/` 复制对应模板到目标位置，替换占位符
2. 严格遵循模板顶部的命名规范
3. 不修改 `templates/` 本身——发现缺陷通过主动报告反馈给 TPM
4. **节省上下文**：模板是固定格式，每次写文件都重读一遍浪费上下文。建议所有 Agent 利用自己平台的快捷能力——无论是 prompt 记忆、snippet、rule、skill 还是其他机制——将高频模板的结构缓存起来，需要时直接按格式生成文件，不必每次打开 `templates/` 逐字读取。无论用哪种快捷方式，最终产出的文件必须符合模板格式和命名规范。本条为效率建议，非强制。

---

## 五、任务生命周期

```
TPM 写 TASK → inbox/
  → 执行者领取 → 编码 → 写 REPORT → outbox/
  → 审查 → 写 REVIEW_REPORT → reviews/
  → ACCEPTED → 归档
  → 需修订 → 写 REPORT_R1 → 再审 → 循环直到 ACCEPTED
```

| 状态 | 含义 |
|------|------|
| 🔵 ASSIGNED | 已分派，等待领取 |
| 🟡 IN_PROGRESS | 执行中 |
| 🟠 REVIEW_PENDING | 已提交，等待审查 |
| ✅ ACCEPTED | 审查通过 |
| 🔴 REVISION_NEEDED | 需修改 |
| 🟢 DONE | 已合并/关闭 |
| ⚪ CANCELLED | 已取消 |
| 🔴 BLOCKED | 被阻塞 |
| ✅ RESOLVED | 已解除 |

> 审查流程的可选分级（P0-P3）见 `TPM.md`。实际审查链由 `ACTIONS.md` 定义。
> **TPM 不豁免**：TPM 自己的改动也必须先建 TASK，完成后写 REPORT，与其他 Agent 同等追溯。

---

## 六、主动报告（阅后即焚）

无对应 TASK 的报告。任何人可提交 `PROACTIVE_REPORT` 到 outbox/。

```
提交 → TPM 阅读 → 决策 → 报告末尾批注 → 写 REPLY 回执 → 归档
```

**为什么叫"阅后即焚"**：主动报告不进入标准任务生命周期。TPM 阅读并决策后，报告即归档。如果决策是 📋 任务或 📅 排期，TPM 会创建对应的 TASK 或 TODO 另行跟踪。

| TPM 决策 | 含义 |
|----------|------|
| ✅ 采纳 | 直接接受 |
| ❌ 忽略 | 不采纳 |
| 📋 任务 | 已创建 TASK/REVISION |
| 📅 排期 | 创建 TODO |
| ✓ 已处理 | 已实现/修复 |

---

### `todos/` 目录

排期事项的暂存区。当 TPM 决定某个需求**暂不执行、后续安排**时，创建 `TODO_NNN_DESC_SOURCE.md` 放此处。

**来源**：主动报告中 📅 排期的建议、里程碑规划中暂缓的需求、用户提出的低优先级想法。

**生命周期**：TODO 被排入计划 → TPM 转为 TASK 放入 inbox/ → 原 TODO 归档。过期或决定废弃的 TODO 直接归档。长期未启动的 TODO 保留在 todos/，提醒 TPM 定期审视。

---

## 七、代码规范

| 规则 | 说明 |
|------|------|
| 新建文件署名头 | 顶部 3 行：`Author` / `Date` / `Description` |
| 修改记录写日志 | 不写文件内注释，改动记 `logs/{标识}-log.md` |
| 修改展示 diff | 改现有文件只给 diff，新建才给全文 |
| 严格类型 | 核心模块禁松散类型（TS 禁 `any`、Rust 禁 `unwrap()` 处理输入） |
| 最小改动 | 只改必要部分，不动无关代码 |

---

## 八、日志规范

每人独占 `logs/{标识}-log.md`，按日期分段。操作分类：`Create` / `Edit` / `Delete` / `Move` / `Read` / `Verify` / `Review` / `Dispatch` / `Install` / `Start` / `Stop`

```markdown
## YYYY-MM-DD

| 时间 | 操作 | 对象 | 说明 |
|------|------|------|------|
| 22:00 | Create | `src/xxx.vue` | 新建 X 组件 |
```

---

## 九、归档规则

只有 TPM 执行归档。归档是移动操作，不修改内容。

| 文件类型 | 归档时机 |
|----------|----------|
| TASK / REVISION | 处理完即归档 |
| NOTICE / REPLY | 接收方读取后归档 |
| BLOCKING / BLOCKING_REPLY | 阻塞解除后归档 |
| REPORT | TPM 读取并决策后归档 |
| REVIEW_REPORT | ACCEPT 或 REVISION_NEEDED 结论后归档 |
| PROACTIVE_REPORT | TPM 批注并放置 REPLY 后归档 |
| TODO | 转为 TASK 后归档 / 过期废弃后归档 |

**目标路径**：`archive/inbox/` / `archive/outbox/` / `archive/reviews/` / `archive/events/`

---

## 十、角色定义

### TPM

**职责**：创建与分派 TASK、编排计划、终审、Git 操作、维护 ACTIONS.md / dashboard.md / todos/、归档、为 Sub-Agent 注入上下文

**红线**：任务先行、不修改 outbox/、审查委派 Reviewer、不写业务代码

> **单点不是你选的**：最小的团队就是 1 个 TPM。如果你的 TPM 崩溃或产生幻觉，`ACTIONS.md` 可以增加一个备用 TPM 行——审查和 Git 权限可以多人持有。框架不强制只有一个人有钥匙。

### External Agent

**入职后**：巡检 inbox/ 找 ASSIGNEE=自己的 TASK → 领取 → 编码 → REPORT → outbox/

**规则**：严禁 git 命令。阻塞写 BLOCKING。

### Sub-Agent (Native)

**入职后**：等 TPM 内部投递 → 编码 → 内部通道交付 diff → REPORT 到 outbox/ 留痕 → 完成后去 inbox/ 读下一条 ASSIGNEE=自己的 TASK

**规则**：可读写全部协作文件但无法主动巡检。严禁 git 命令。严禁跨职责修改文件。上下文由 `context/{name}-memory.md` 提供。

---

## 十一、入职流程

1. 确认角色（TPM / External / Sub-Agent / Reviewer），写首条日志
2. 按 `REGISTER.md` 回答问题，填入入职动作表
3. TPM 确认后移入 `ACTIONS.md`，入职完成

**Reporter 不是独立角色**，任何角色均可兼任。提交 `PROACTIVE_REPORT` 时即为 Reporter。

---

## 十二、快速参考

| 我想... | 操作 |
|---------|------|
| 认领身份 | 读 👑 区域 → 你是 TPM：签名字 → 读 `TPM.md` / 你不是 TPM → 读 `REGISTER.md` |
| 领任务 | 查 `ACTIONS.md` 自己的分派行 → 巡检 inbox/ 或等内部投递 |
| 交报告 | 写 `outbox/REPORT_NNN_DATE_AUTHOR.md` |
| 交主动报告 | 写 `outbox/PROACTIVE_REPORT_NNN_DESC_DATE_AUTHOR.md` |
| 写审查结论 | 写 `reviews/REVIEW_REPORT_NNN_DATE_AUTHOR.md`，附文件:行号 + 严重度 |
| 报告阻塞 | 写 `outbox/BLOCKING_NNN_DATE_TARGET.md`（写明解除条件） |
| 解除阻塞 | 写 `outbox/BLOCKING_REPLY_NNN_DATE_AUTHOR.md` |
| 写日志 | 追加到 `logs/{标识}-log.md` |
| 查模板 | 读 `templates/` 对应文件 |
| 看进度（人类） | 读 `dashboard.md` |
