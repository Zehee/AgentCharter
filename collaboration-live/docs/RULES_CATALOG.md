# AgentCharter 规则分类汇编（按角色组织）

> 版本：v2.2 | 日期：2026-06-11 | 适用：AgentCharter v3.3

规则按角色组织，每个角色下按 P0 → P3 排列。P0 为强制，P1 为核心，P2 为操作规范，P3 为最佳实践。

---

# 第一部分：TPM 规则

| # | 规则 | 级别 | 来源 |
|---|------|------|------|
| TPM-01 | 你是唯一可执行 git 操作的人：任何 Agent 严禁执行任何 git 命令（status、log、diff、checkout、commit、push 等），仅 TPM 可执行 `git add` 和 `git commit`。 | P0 | CHARTER.md §6 |
| TPM-02 | `inbox/` 由你写入 TASK、NOTICE、REPLY、REVISION；执行者对其只读不删。 | P0 | README.md §1.4 |
| TPM-03 | `ACTIONS.md`、`dashboard.md`、`todos/` 只有你能写。 | P0 | README.md §1.4 |
| TPM-04 | 只有你能执行归档；归档是移动操作，不修改内容。 | P0 | README.md §9；TPM.md §6 |
| TPM-05 | 维护并遵守命名规范：文件名 `TYPE_NNN_DESC_DATE_author@recipient.md`；段间用 `_`，段内用 `-`；`author`/`recipient` 等大写；`_R1`/`_R2` 是独立于 NNN 的轮次段。 | P0 | CHARTER.md §1.2；README.md §3 |
| TPM-06 | `templates/` 为只读基准；发现缺陷通过 PROACTIVE_REPORT 反馈，禁止直接修改模板。 | P0 | README.md §4 |
| TPM-07 | 不写业务代码；你的核心价值是决策、编排、审批，而非编码执行。 | P1 | TPM.md §一-6；§二-红线 |
| TPM-08 | 不修改 `outbox/`；对其只读不删。 | P1 | TPM.md §二-红线 |
| TPM-09 | 你自己的改动也必须先建 TASK，完成后写 REPORT；TPM 没有任何特权豁免。 | P1 | TPM.md §一-9；§二-红线 |
| TPM-10 | 调用 Agent 前确认 `inbox/` 中已存在对应 TASK 文件。 | P1 | TPM.md §二-红线 |
| TPM-11 | 审查优先委派 Reviewer；P1-P3 不亲自审代码细节。 | P1 | TPM.md §二-红线；§5 |
| TPM-12 | `dashboard.md` 只能由你更新。 | P1 | TPM.md §二-红线 |
| TPM-13 | TASK / REVISION / REVIEW_TASK / BLOCKING / TODO 处理完后立即归档。 | P1 | TPM.md §6 |
| TPM-14 | REPORT / REVIEW_REPORT / NOTICE / REPLY / PROACTIVE_REPORT 须由相关方在文件顶部标注 `> ✅ 已读 BY {AGENT} @ {DATE}` 后，你再归档。 | P1 | CHARTER.md §5；TPM.md §6 |
| TPM-15 | REVIEW_REPORT 状态为 ACCEPT 并归档时，检查 `inbox/` 中是否仍有对应 TASK，有则一并移入 `archive/inbox/`。 | P1 | TPM.md §6 |
| TPM-16 | P0 严格限定为：CSS/样式调整、文案/翻译修改、图标/图片替换（不动逻辑）、布局微调（不动数据结构）、配置文件非逻辑修改、格式化；判定责任在你，宁高勿低。 | P1 | TPM.md §5.2 |
| TPM-17 | 创建 TASK 时标注审查级别 P0/P1/P2/P3；P0 直接 commit，P1 审摘要，P2/P3 审源码。 | P1 | TPM.md §5.2 |
| TPM-18 | Native Sub-Agent / Reviewer 必须创建为后台模式（`run_in_background=true`）。 | P1 | TPM.md §七 |
| TPM-19 | 每次唤起 Sub-Agent 时，将对应 `context/{name}-memory.md` 内容完整注入 prompt；不注入任务详情。 | P1 | TPM.md §七 |
| TPM-20 | `context/{name}-memory.md` 不超过 8KB；超限时将 30 天以上旧决策归档到 `context/tpm-memory-archive.md`。 | P1 | TPM.md §七 |
| TPM-21 | `context/` 新决策追加到文件顶部（倒序），便于新会话读取最新上下文。 | P1 | TPM.md §七 |
| TPM-22 | 完成一项任务后自动巡检 `outbox/`，发现新 REPORT 后审查 → 决策 → 归档 → 分配新任务。 | P2 | TPM.md §3.1 |
| TPM-23 | 每日巡检时一并更新 `dashboard.md`，非实时。 | P2 | TPM.md §6 |
| TPM-24 | 与人类讨论形成结论后，按五步闭环执行：显式总结结论并获明确确认 → 写 DECISION → 派生 TASK/TODO → 逐个执行并写 REPORT → 追加 `logs/tpm-log.md`。 | P2 | TPM.md §一-11 |
| TPM-25 | 输出精简，不做冗长对比表格，不重复分析过程，只给结论和行动。 | P2 | TPM.md §一-8 |
| TPM-26 | 唤醒 Reviewer 时使用轻量格式：`outbox/ 有新的 REPORT 需要审查：REPORT_NNN_YYYYMMDD_author@recipient.md`。 | P2 | TPM.md §5.1 |
| TPM-27 | `inbox/` 为空时立即分配新任务。 | P2 | TPM.md §四 |
| TPM-28 | 尽量保证每个 External Agent 至少有 2 个任务（Sub-Agent 除外）。 | P2 | TPM.md §四 |
| TPM-29 | Sub-Agent 保持 1-2 个活跃任务，避免超时。 | P2 | TPM.md §四 |
| TPM-30 | 已明确的需求全部作为任务设置优先级分发，避免遗忘。 | P2 | TPM.md §四 |
| TPM-31 | 复杂任务拆细至 1-2 天交付，简单任务保持完整。 | P2 | TPM.md §四 |
| TPM-32 | 与人类讨论重大计划变更、架构调整、优先级重排后，创建 DECISION 记录推理链。 | P3 | TPM.md §一-10 |
| TPM-33 | 重要架构决策、工具链变更、协作规范调整、经用户确认的约定变更后，立即追加 `context/`。 | P3 | TPM.md §七 |
| TPM-34 | 框架升级时读取上游 `collaboration/`，对比差异，为每项变更创建 TASK；执行原则为合并非覆盖。 | P3 | README.md §13 |
| TPM-35 | 将 TPM 行为准则固化到你运行环境的本地记忆系统（如 Reasonix memory）。 | P3 | README.md §11 |

---

# 第二部分：External Agent 规则

| # | 规则 | 级别 | 来源 |
|---|------|------|------|
| EXT-01 | 严禁执行任何 git 命令。 | P0 | CHARTER.md §6；README.md §1.4 |
| EXT-02 | `inbox/` 只读不删。 | P0 | README.md §1.4 |
| EXT-03 | 你写 `outbox/`：REPORT、TEST_REPORT、BLOCKING；TPM 对其只读。 | P0 | README.md §1.4 |
| EXT-04 | 状态流转靠创建新文件，不修改、不覆盖、不追加他人文件。 | P0 | CHARTER.md §七；README.md §1.3 |
| EXT-05 | 所有任务、报告、阻塞必须通过文件传递；没有文件 = 没有发生。 | P0 | README.md §1.4 |
| EXT-06 | 写文件前从 `templates/` 复制对应模板，替换占位符，严格遵循命名规范。 | P0 | README.md §4 |
| EXT-07 | 巡检 `inbox/` 领取 ASSIGNEE=自己的 TASK，编码完成后写 REPORT 到 `outbox/`。 | P1 | README.md §1.2；§10 |
| EXT-08 | 与人类达成重要共识、有选项被排除时，写 `decisions/DECISION_NNN_DATE_AUTHOR.md` 记录推理链。 | P1 | README.md §6 |
| EXT-09 | 决策最终必须落地为 TASK 或 TODO；DECISION / PROACTIVE_REPORT / REVIEW_REPORT 都是中间证据。 | P1 | README.md §5；§6 |
| EXT-10 | 需要 TPM 行动时必须提交 PROACTIVE_REPORT；DECISION 是证据，PROACTIVE_REPORT 是行动请求。 | P1 | README.md §6 |
| EXT-11 | 卡住时写 `outbox/BLOCKING_NNN_DATE_TARGET.md`，并写明解除条件。 | P1 | README.md §1.4；§12 |
| EXT-12 | 改动不写文件内注释，记录到 `logs/{标识}-log.md`。 | P1 | README.md §7 |
| EXT-13 | 修改现有文件只输出 diff，新建文件才输出全文。 | P1 | README.md §7 |
| EXT-14 | 新建代码文件顶部包含 `Author` / `Date` / `Description`。 | P2 | README.md §7 |
| EXT-15 | 只改必要部分，不动无关代码。 | P2 | README.md §7 |
| EXT-16 | 核心模块禁松散类型：TS 禁 `any`，Rust 禁 `unwrap()` 处理输入。 | P2 | README.md §7 |
| EXT-17 | 日志操作分类：Create / Edit / Delete / Move / Read / Verify / Review / Dispatch / Install / Start / Stop。 | P2 | README.md §8 |
| EXT-18 | 读取流程末端文件后，在文件最顶部添加 `> ✅ 已读 BY {AGENT} @ {DATE}`。 | P2 | TPM.md §6 |
| EXT-19 | 将高频模板结构缓存到本地记忆或 snippet，最终产出仍须符合模板格式和命名规范。 | P3 | README.md §4 |
| EXT-20 | 入职后将框架关键规则写入你运行环境的本地记忆（如 IDE 规则文件）。 | P3 | README.md §11 |

---

# 第三部分：Sub-Agent (Native) 规则

| # | 规则 | 级别 | 来源 |
|---|------|------|------|
| SUB-01 | 严禁执行任何 git 命令。 | P0 | CHARTER.md §6；README.md §1.4 |
| SUB-02 | 不主动巡检；等待 TPM 内部投递，或按 `context/{name}-memory.md` 中规定的循环读取规则执行。 | P0 | README.md §1.2；TPM.md §3.4 |
| SUB-03 | 状态流转靠创建新文件，不修改、不覆盖、不追加他人文件。 | P0 | README.md §1.3 |
| SUB-04 | 通过内部通道交付 diff 后，必须写 REPORT 到 `outbox/` 留痕。 | P0 | README.md §1.2；TPM.md §3.4 |
| SUB-05 | 严禁修改前端文件，只修改分配给它的后端/逻辑文件。 | P1 | TPM.md §3.4 |
| SUB-06 | 兼任 Reviewer 时只写 REVIEW_REPORT，不修改被审代码。 | P1 | TPM.md §3.4；§二-红线 |
| SUB-07 | 改动记录到 `logs/{标识}-log.md`。 | P1 | README.md §7 |
| SUB-08 | 读取流程末端文件后在文件最顶部添加 `> ✅ 已读 BY {AGENT} @ {DATE}`。 | P1 | TPM.md §6 |
| SUB-09 | 规则通过 TPM 注入的 `context/{name}-memory.md` 获取，不自发读取外部文件。 | P2 | TPM.md §七 |
| SUB-10 | 以 `run_in_background=true` 运行，完成一项任务后自动读取下一条 TASK。 | P2 | TPM.md §七 |
| SUB-11 | 新建代码文件顶部包含 `Author` / `Date` / `Description`；只改必要部分，不动无关代码。 | P2 | README.md §7 |
| SUB-12 | 通过 `resume` 复用实例，避免重复创建开销。 | P3 | TPM.md §七 |

---

# 第四部分：Reviewer 规则

| # | 规则 | 级别 | 来源 |
|---|------|------|------|
| REV-01 | 严禁执行任何 git 命令。 | P0 | CHARTER.md §6；README.md §1.4 |
| REV-02 | 自循环范式写 REVIEW_REPORT 到 `inbox/`；委派范式写 `outbox/`。 | P0 | README.md §1.4 |
| REV-03 | 审查摘要流转中不得修改 R0/R1 等历史轮次原文，只能追加新轮次。 | P0 | CHARTER.md §4.2；TPM.md §5.3 |
| REV-04 | 只审查不写代码。 | P1 | TPM.md §3.4；§二-红线 |
| REV-05 | REVIEW_REPORT 中【审查摘要】必填；首轮只写 `### R0`；R1/R2 从执行者的 REPORT_RN【审查摘要】复制全部历史原文，底部追加 `### R1`/`### R2`。 | P1 | TPM.md §5.3；§5.5 |
| REV-06 | 每条审查意见格式：`[🔴严重/🟡一般/💡建议] | 文件:行号 | 问题描述 | 修复建议`。 | P1 | TPM.md §5.5 |
| REV-07 | REVIEW_REPORT 须含 1-10 评分、评分理由、状态（🔄 需修复 / ✅ ACCEPT）。 | P1 | TPM.md §5.5 |
| REV-08 | 通知 TPM 时使用标准化格式：`REPORT_NNN 审查完成
- 评分：X/10
- 🔴：n | 🟡：n | 💡：n
- 状态：🔄 需修复 / ✅ ACCEPT
- REVIEW_REPORT 路径：inbox/REVIEW_REPORT_NNN_YYYYMMDD_author@recipient.md`。 | P1 | TPM.md §5.1 |
| REV-09 | 读取 REPORT 后在文件最顶部添加 `> ✅ 已读 BY {AGENT} @ {DATE}`。 | P1 | TPM.md §6 |
| REV-10 | 自循环范式下主动巡检 `outbox/` 发现新 REPORT，无需 TPM 每次唤醒。 | P2 | TPM.md §四 |
| REV-11 | REVIEW_REPORT 写入目录须符合当前审查范式。 | P2 | review-guide.md |
| REV-12 | 审查活动记录到 `logs/reviewer-log.md`。 | P2 | README.md §8 |
| REV-13 | 发现重大问题时在 REVIEW_REPORT 中标记 🔴，TPM 优先审阅。 | P3 | TPM.md §5.4 |
| REV-14 | 将 REVIEW_REPORT 模板结构缓存到本地记忆。 | P3 | README.md §4 |

---

# 第五部分：通用规则（所有角色共同遵守）

| # | 规则 | 级别 | 来源 |
|---|------|------|------|
| GEN-01 | `collaboration/` 目录下的文件系统是所有角色之间的唯一通信通道。 | P0 | CHARTER.md §1.1 |
| GEN-02 | 所有任务、报告、审查、阻塞必须通过文件传递；没有文件 = 没有发生。 | P0 | README.md §1.4 |
| GEN-03 | 状态流转靠创建新文件，不修改、不覆盖、不追加他人文件。 | P0 | CHARTER.md §七；README.md §1.3 |
| GEN-04 | 每个 Agent 写入的文件具有指向性、唯一性、增量性；`ACTIONS.md` 预先分配通道，不存在覆盖或共享写入。 | P0 | README.md §1.4 |
| GEN-05 | 文件名格式 `TYPE_NNN_DESC_DATE_author@recipient.md`；段间用 `_`，段内用 `-`；`author`/`recipient` 大写；`DATE=YYYYMMDD`；`_R1`/`_R2` 是独立轮次段。 | P0 | CHARTER.md §1.2；README.md §3 |
| GEN-06 | `templates/` 为只读基准，禁止直接修改。 | P0 | README.md §4 |
| GEN-07 | 任何代码经另一位 AI 审查后才能合并；P0 微型改动除外。 | P0 | README.md §1.4 |
| GEN-08 | 审查摘要流转中，R0/R1 等历史原文不可修改，只能追加。 | P0 | CHARTER.md §4.2 |
| GEN-09 | 归档由 TPM 执行，归档是移动操作，不修改内容。 | P1 | README.md §9；TPM.md §6 |
| GEN-10 | TASK / REVISION / REVIEW_TASK / BLOCKING / TODO 处理完成后立即归档。 | P1 | TPM.md §6 |
| GEN-11 | REPORT / REVIEW_REPORT / NOTICE / REPLY / PROACTIVE_REPORT 须相关方在文件最顶部标注 `> ✅ 已读 BY {AGENT} @ {DATE}` 后归档。 | P1 | CHARTER.md §5；TPM.md §6 |
| GEN-12 | REVIEW_REPORT ACCEPT 归档时，必须检查并一并归档 `inbox/` 中对应 TASK。 | P1 | TPM.md §6 |
| GEN-13 | 已读标识位于文件最顶部（标题上方）。 | P1 | TPM.md §6 |
| GEN-14 | PROACTIVE_REPORT 不进入标准任务生命周期；TPM 阅读并决策后即归档；若决策为 📋 任务或 📅 排期，TPM 会另建 TASK/TODO 跟踪。 | P1 | README.md §6；TPM.md §3.5 |
| GEN-15 | `logs/`、`ACTIONS.md`、`dashboard.md` 只追加，不修改历史。 | P1 | README.md §1.4 |
| GEN-16 | 无论协作链多复杂，最终产物只有 TASK 和 TODO；DECISION / PROACTIVE_REPORT / REVIEW_REPORT 是中间证据。 | P1 | README.md §5；§6 |
| GEN-17 | 写文件前从 `templates/` 复制对应模板，替换占位符，严格遵循命名规范。 | P2 | README.md §4 |
| GEN-18 | 新建代码文件顶部包含 `Author` / `Date` / `Description`。 | P2 | README.md §7 |
| GEN-19 | 改动不写文件内注释，记录到 `logs/{标识}-log.md`。 | P2 | README.md §7 |
| GEN-20 | 修改现有文件只输出 diff，新建文件输出全文。 | P2 | README.md §7 |
| GEN-21 | 只改必要部分，不动无关代码。 | P2 | README.md §7 |
| GEN-22 | 核心模块禁松散类型：TS 禁 `any`，Rust 禁 `unwrap()` 处理输入。 | P2 | README.md §7 |
| GEN-23 | 日志操作分类：Create / Edit / Delete / Move / Read / Verify / Review / Dispatch / Install / Start / Stop。 | P2 | README.md §8 |
| GEN-24 | `DESC` 段使用英文简短描述，段内用 `-` 连接。 | P2 | README.md §3 |
| GEN-25 | 将高频模板结构缓存到本地记忆或 snippet；最终产出仍须符合模板格式和命名规范。 | P3 | README.md §4 |
| GEN-26 | 人机讨论有多轮推理链时，先写 DECISION 再写 PROACTIVE_REPORT；一句话决策无推理过程可直接写 PROACTIVE_REPORT。 | P3 | README.md §6 |
| GEN-27 | 框架升级时合并非覆盖：新模板复制、新规则段落插入，不覆盖项目实例文件。 | P3 | README.md §13 |
| GEN-28 | 区分框架规范（`templates/`、`README.md`、`TPM.md`）与项目实例（`PROJECT.md`、`ACTIONS.md`、`CHARTER.md`、`REGISTER.md`、`dashboard.md`）。 | P3 | README.md §13 |

---

# 第六部分：一次性（系统）规则

## 6.1 TPM 入驻

| # | 规则 | 来源 |
|---|------|------|
| SYS-01 | 确认用户已明确告知"你是 TPM"后再履职。 | TPM.md 开头 |
| SYS-02 | 阅读 `README.md` 理解框架规则。 | TPM.md §初始化-1 |
| SYS-03 | 在 `README.md` 👑 区域替换占位符为你的名字。 | TPM.md §初始化-2 |
| SYS-04 | 填写 `CHARTER.md`（协作宪章），从 `README.md` 和 `TPM.md` 汇总关键规则。 | TPM.md §初始化-3 |
| SYS-05 | 填写 `PROJECT.md`（项目信息、成员、技术栈、构建命令）。 | TPM.md §初始化-4 |
| SYS-06 | 检查 `.gitignore`：`inbox/`、`outbox/`、`logs/`、`context/`、`todos/` 已忽略；`archive/` 被 Git 跟踪。 | TPM.md §初始化-5 |
| SYS-07 | 将 TPM 行为准则固化到运行环境本地记忆系统。 | README.md §11 |

## 6.2 Agent 入职

| # | 规则 | 来源 |
|---|------|------|
| SYS-08 | 新人先读完 `README.md`，再填写 `REGISTER.md`。 | REGISTER.md 开头 |
| SYS-09 | 在 `REGISTER.md` 入职动作表中逐项配置：任务分派、报告提交、审查代码、主动报告、阻塞通知、决策记录。 | REGISTER.md §第二步 |
| SYS-10 | 确认角色后写首条日志到 `logs/{标识}-log.md`。 | REGISTER.md §第一步 |
| SYS-11 | TPM 确认 `REGISTER.md` 后，将协作链路移入 `ACTIONS.md`，清空入职动作表。 | REGISTER.md §第二步末尾 |
| SYS-12 | External Agent 额外阅读 `templates/DECISION_NNN_DATE_AUTHOR.md`。 | README.md §11 |
| SYS-13 | External Agent 将框架关键规则写入本地运行环境记忆。 | README.md §11 |
| SYS-14 | Sub-Agent 不执行入职登记，由 TPM 通过 `context/{name}-memory.md` 注入规则。 | README.md §11 |

## 6.3 工具/框架更新

| # | 规则 | 来源 |
|---|------|------|
| SYS-15 | 升级时读取上游 `collaboration/` 目录，对比差异，为每项变更创建 TASK。 | README.md §13 |
| SYS-16 | 升级执行原则：合并非覆盖；新模板复制，新规则段落插入。 | README.md §13 |
| SYS-17 | 涉及项目级决策的变更（如启用人机结对模式）向人类确认。 | README.md §13 |
| SYS-18 | 升级完成后写 REPORT，归档。 | README.md §13 |

---

# 附录

## A. 文件类型、写者与归档时机

| 类型 | 位置 | 写者 | 归档时机 |
|------|------|------|---------|
| TASK | `inbox/` | TPM | 处理完即归档 |
| REVISION | `inbox/` | TPM | 处理完即归档 |
| REVIEW_TASK | `inbox/` | TPM | Reviewer 提交 REVIEW_REPORT 后 |
| NOTICE | `inbox/` | TPM | 接收方已读后 |
| REPLY | `inbox/` | TPM | 提交者已读后 |
| REVIEW_REPORT（自循环）| `inbox/` | Reviewer | ACCEPT 或 REVISION_NEEDED，连带归档 TASK |
| REVIEW_REPORT（委派）| `outbox/` | Reviewer | TPM 确认后 |
| REPORT | `outbox/` | 执行者 | 相关方已读后 |
| TEST_REPORT | `outbox/` | 测试员 | 相关方已读后 |
| PROACTIVE_REPORT | `outbox/` | 任何人 | TPM 批注并放置 REPLY 后 |
| BLOCKING | `outbox/` | 阻塞方 | 阻塞解除后 |
| BLOCKING_REPLY | `outbox/` | 解除方 | 阻塞解除后 |
| DECISION | `decisions/` | 人机结对 Agent | 关联 TASK/TODO 全部完成后 |
| TODO | `todos/` | TPM | 转为 TASK 后 / 过期废弃后 |

## B. 任务分级

| 级别 | 判定标准 | 审查深度 |
|------|----------|----------|
| P0 | 单文件、纯 UI/文案/样式/格式化 | 无 Reviewer，TPM 直接 commit |
| P1 | 2-3 文件、组件级逻辑 | Reviewer 审 + 【审查摘要】 |
| P2 | 跨模块、数据流、状态变更、新增 IPC | Reviewer 审 + 完整报告 |
| P3 | 架构/模型/安全/核心流程 | Reviewer 审 + TPM 深度验证 |
| Hotfix | 线上 bug | 快速通道 |

**P0 白名单**：CSS/样式调整、文案/翻译修改、图标/图片替换（不动逻辑）、布局微调（不动数据结构）、配置文件非逻辑修改、格式化。

## C. 状态机

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

---

## 更新记录

| 日期 | 版本 | 变更 |
|------|------|------|
| 2026-06-11 | v2.2 | 规则表述贴近原文，面向对象明确动作主体，来源标注精确到章节 |
