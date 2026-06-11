# AgentCharter 规则分类汇编（按角色组织）

> 版本：v2.5 | 日期：2026-06-11 | 适用：AgentCharter v3.3

规则按角色组织：TPM、External Agent、Sub-Agent、Reviewer、通用、一次性系统规则。每个角色下按 P0 → P3 排列。

- P0：强制。违反即破坏协作基础或权限失控。
- P1：核心。违反会导致协作混乱、追溯困难或质量下降。
- P2：操作规范。违反会降低效率或增加管理成本。
- P3：最佳实践。推荐采纳，非强制。

---

# TPM 规则

## P0 强制

- TPM 是唯一可执行 git 操作的角色；除 TPM 外，任何 Agent 严禁执行任何 git 命令（status、log、diff、checkout、commit、push 等）；TPM 仅可执行 `git add` 和 `git commit`。
- TPM 负责写入 `inbox/`，文件类型包括 TASK、NOTICE、REPLY、REVISION；执行者对 `inbox/` 只读不删。
- TPM 独占写入 `ACTIONS.md`、`dashboard.md`、`todos/`。
- 只有 TPM 可执行归档；归档是移动操作，不修改内容。
- TPM 维护并遵守命名规范：文件名格式为 `TYPE_NNN_DESC_DATE_author@recipient.md`；段间用 `_`，段内用 `-`；`author`/`recipient` 等标识大写；`DATE` 格式为 `YYYYMMDD`；`_R1`/`_R2` 是独立于 NNN 的轮次段。
- `templates/` 为只读基准；发现缺陷时 TPM 通过 PROACTIVE_REPORT 反馈；任何角色禁止直接修改模板。

## P1 核心

- TPM 不写业务代码；核心价值是决策、编排、审批。
- TPM 不修改 `outbox/`，对其只读不删。
- TPM 自身改动须先建 TASK，完成后写 REPORT；TPM 无特权豁免。
- TPM 调用 Agent 前须确认 `inbox/` 已存在对应 TASK 文件。
- TPM 审查 P1-P3 时优先委派 Reviewer，不亲自审代码细节。
- 只有 TPM 可更新 `dashboard.md`。
- TASK / REVISION / REVIEW_TASK / BLOCKING / TODO 处理完成后，TPM 立即归档。
- REPORT / REVIEW_REPORT / NOTICE / REPLY / PROACTIVE_REPORT 须由相关方在文件最顶部标注 `> ✅ 已读 BY {AGENT} @ {DATE}` 后，TPM 再归档。
- REVIEW_REPORT 状态为 ACCEPT 并归档时，TPM 须检查 `inbox/` 中是否仍有对应 TASK；若有，须一并移入 `archive/inbox/`。
- TPM 判定 TASK 审查级别时，P0 严格限定为单文件、无逻辑变更的改动；P0 白名单包括 CSS/样式调整、文案/翻译修改、图标/图片替换（不动逻辑）、布局微调（不动数据结构）、配置文件非逻辑修改、格式化；判定责任在 TPM，宁高勿低。
- TPM 创建 TASK 时须标注审查级别 P0/P1/P2/P3：P0 直接 commit，P1 审摘要，P2 审关键意见与源码，P3 深度验证。
- TPM 创建 Native Sub-Agent / Reviewer 时必须使用后台模式（`run_in_background=true`）。
- TPM 每次唤起 Sub-Agent 时，须将对应 `context/{name}-memory.md` 内容完整注入 prompt，不注入任务详情。
- `context/{name}-memory.md` 大小不超过 8KB；超限时，TPM 须将 30 天以上旧决策归档到 `context/tpm-memory-archive.md`。
- TPM 追加 `context/` 新决策时须放到文件顶部（倒序）。

## P2 操作规范

- TPM 完成一项任务后须巡检 `outbox/`，发现新 REPORT 后执行审查 → 决策 → 归档 → 分配新任务。
- TPM 每日巡检时一并更新 `dashboard.md`，非实时。
- TPM 与人类讨论形成结论后，按五步闭环执行：显式总结结论并获明确确认 → 写 DECISION → 派生 TASK/TODO → 逐个执行并写 REPORT → 追加 `logs/tpm-log.md`。
- TPM 输出须精简：不做冗长对比表格，不重复分析过程，只给结论和行动。
- TPM 唤醒 Reviewer 时使用轻量格式：`outbox/ 有新的 REPORT 需要审查：REPORT_NNN_YYYYMMDD_author@recipient.md`。
- `inbox/` 为空时，TPM 立即分配新任务。
- TPM 尽量保证每个 External Agent 至少有 2 个任务（Sub-Agent 除外）。
- TPM 控制 Sub-Agent 活跃任务在 1-2 个，避免超时。
- TPM 将已明确需求全部作为任务设置优先级分发，避免遗忘。
- TPM 拆分复杂任务至 1-2 天交付，简单任务保持完整。

## P3 最佳实践

- TPM 与人类讨论重大计划变更、架构调整、优先级重排后，创建 DECISION 记录推理链。
- 重要架构决策、工具链变更、协作规范调整、经用户确认的约定变更后，TPM 立即追加 `context/`。
- TPM 框架升级时读取上游 `collaboration/`，对比差异，为每项变更创建 TASK；执行原则为合并非覆盖：新模板复制、新规则段落插入、不覆盖项目实例文件。
- TPM 将行为准则固化到运行环境本地记忆系统（如 Reasonix memory）。

---

# External Agent 规则

## P0 强制

- External Agent 严禁执行任何 git 命令。
- External Agent 对 `inbox/` 只读不删。
- External Agent 写入 `outbox/`，文件类型包括 REPORT、TEST_REPORT、BLOCKING；TPM 对 `outbox/` 只读。
- External Agent 状态流转靠创建新文件，不修改、不覆盖、不追加他人文件。
- External Agent 所有任务、报告、阻塞必须通过文件传递；没有文件 = 没有发生。
- External Agent 写文件前须从 `templates/` 复制模板，替换占位符，严格遵循命名规范。

## P1 核心

- External Agent 巡检 `inbox/` 领取 ASSIGNEE=自己的 TASK，完成后写 REPORT 到 `outbox/`。
- External Agent 与人类达成重要共识、有选项被排除时，写 `decisions/DECISION_NNN_DATE_AUTHOR.md` 记录推理链。
- External Agent 的决策最终须落地为 TASK 或 TODO；DECISION / PROACTIVE_REPORT / REVIEW_REPORT 均为中间证据。
- External Agent 需要 TPM 行动时必须提交 PROACTIVE_REPORT；DECISION 是证据，PROACTIVE_REPORT 是行动请求；有推理链时可先写 DECISION 再写 PROACTIVE_REPORT，无推理过程可直接写 PROACTIVE_REPORT。
- External Agent 卡住时写 `outbox/BLOCKING_NNN_DATE_TARGET.md`，并写明解除条件。
- External Agent 改动不写文件内注释，须记录到 `logs/{标识}-log.md`。
- External Agent 修改现有文件只输出 diff，新建文件输出全文。

## P2 操作规范

- External Agent 新建代码文件顶部包含 `Author` / `Date` / `Description`。
- External Agent 只改必要部分，不动无关代码。
- External Agent 在核心模块中禁用松散类型：TS 禁 `any`，Rust 禁 `unwrap()` 处理输入。
- External Agent 日志操作分类为：Create、Edit、Delete、Move、Read、Verify、Review、Dispatch、Install、Start、Stop。
- External Agent 读取流程末端文件后，须在文件最顶部添加 `> ✅ 已读 BY {AGENT} @ {DATE}`。

## P3 最佳实践

- External Agent 可将高频模板结构缓存到本地记忆或 snippet，最终产出仍须符合模板格式和命名规范。
- External Agent 入职后将框架关键规则写入运行环境记忆（如 IDE 规则文件）。

---

# Sub-Agent (Native) 规则

## P0 强制

- Sub-Agent 严禁执行任何 git 命令。
- Sub-Agent 不主动巡检；等待 TPM 内部投递，或按 `context/{name}-memory.md` 中规定的循环读取规则执行。
- Sub-Agent 状态流转靠创建新文件，不修改、不覆盖、不追加他人文件。
- Sub-Agent 通过内部通道交付 diff 后，必须写 REPORT 到 `outbox/` 留痕。

## P1 核心

- Sub-Agent 严禁修改前端文件，只修改分配给它的后端/逻辑文件。
- Sub-Agent 兼任 Reviewer 时只写 REVIEW_REPORT，不修改被审代码。
- Sub-Agent 改动记录到 `logs/{标识}-log.md`。
- Sub-Agent 读取流程末端文件后，须在文件最顶部添加 `> ✅ 已读 BY {AGENT} @ {DATE}`。

## P2 操作规范

- Sub-Agent 通过 TPM 注入的 `context/{name}-memory.md` 获取规则，不自发读取外部文件。
- Sub-Agent 以 `run_in_background=true` 运行，完成一项任务后自动读取下一条 TASK。
- Sub-Agent 新建代码文件顶部包含 `Author` / `Date` / `Description`；只改必要部分，不动无关代码。

## P3 最佳实践

- Sub-Agent 通过 `resume` 复用实例，避免重复创建开销。

---

# Reviewer 规则

## P0 强制

- Reviewer 严禁执行任何 git 命令。
- Reviewer 自循环范式写 REVIEW_REPORT 到 `inbox/`；委派范式写 `outbox/`。
- Reviewer 在审查摘要流转中不得修改 R0/R1/R2 等历史轮次原文，只能追加新轮次。

## P1 核心

- Reviewer 只审查不写代码。
- Reviewer 的 REVIEW_REPORT 中【审查摘要】必填；首轮只写 `### R0`；R1/R2 须从执行者的 REPORT_RN【审查摘要】复制全部历史原文，底部追加 `### R1`/`### R2`。
- Reviewer 每条审查意见格式：`[🔴严重/🟡一般/💡建议] | 文件:行号 | 问题描述 | 修复建议`。
- Reviewer 的 REVIEW_REPORT 须含 1-10 评分、评分理由、状态（🔄 需修复 / ✅ ACCEPT）。
- Reviewer 通知 TPM 时使用标准化格式：`REPORT_NNN 审查完成
- 评分：X/10
- 🔴：n | 🟡：n | 💡：n
- 状态：🔄 需修复 / ✅ ACCEPT
- REVIEW_REPORT 路径：inbox/REVIEW_REPORT_NNN_YYYYMMDD_author@recipient.md`。
- Reviewer 读取 REPORT 后，须在文件最顶部添加 `> ✅ 已读 BY {AGENT} @ {DATE}`。

## P2 操作规范

- Reviewer 自循环范式下主动巡检 `outbox/` 发现新 REPORT，无需 TPM 每次唤醒。
- Reviewer 须按当前审查范式将 REVIEW_REPORT 写入正确目录。
- Reviewer 审查活动记录到 `logs/reviewer-log.md`。

## P3 最佳实践

- Reviewer 发现功能错误、安全漏洞等严重问题时在 REVIEW_REPORT 中标记 🔴，TPM 优先审阅。
- Reviewer 将 REVIEW_REPORT 模板结构缓存到本地记忆。

---

# 通用规则（所有角色共同遵守）

## P0 强制

- `collaboration/` 目录下的文件系统是所有角色之间的唯一通信通道。
- 所有任务、报告、审查、阻塞必须通过文件传递；没有文件 = 没有发生。
- 状态流转靠创建新文件，不修改、不覆盖、不追加他人文件。
- 每个 Agent 写入的文件具有指向性、唯一性、增量性；`ACTIONS.md` 预先分配通道，不存在覆盖或共享写入。
- 文件名须为 `TYPE_NNN_DESC_DATE_author@recipient.md`；段间用 `_`，段内用 `-`；`author`/`recipient` 大写；`DATE=YYYYMMDD`；`_R1`/`_R2` 是独立轮次段。
- `templates/` 为只读基准，任何角色禁止直接修改。
- 任何代码经另一位 AI 审查后才能合并；P0 微型改动除外。
- 审查摘要中 R0/R1/R2 等历史原文不可修改，只能追加。

## P1 核心

- 归档由 TPM 执行；归档是移动操作，不修改内容。
- TASK / REVISION / REVIEW_TASK / BLOCKING / TODO 处理完成后立即归档。
- REPORT / REVIEW_REPORT / NOTICE / REPLY / PROACTIVE_REPORT 须相关方在文件最顶部标注 `> ✅ 已读 BY {AGENT} @ {DATE}` 后归档。
- REVIEW_REPORT ACCEPT 归档时，必须检查并一并归档 `inbox/` 中对应 TASK。
- PROACTIVE_REPORT 不进入标准任务生命周期；TPM 阅读并决策后即归档；若决策为 📋 任务或 📅 排期，TPM 会另建 TASK/TODO 跟踪。
- `logs/`、`ACTIONS.md`、`dashboard.md` 只追加，不修改历史。
- 无论协作链多复杂，最终产物只有 TASK 和 TODO；DECISION / PROACTIVE_REPORT / REVIEW_REPORT 均为中间证据。

## P2 操作规范

- 写文件前从 `templates/` 复制模板，替换占位符，严格遵循命名规范。
- 新建代码文件顶部包含 `Author` / `Date` / `Description`。
- 改动不写文件内注释，须记录到 `logs/{标识}-log.md`。
- 修改现有文件只输出 diff，新建文件输出全文。
- 只改必要部分，不动无关代码。
- 核心模块禁松散类型：TS 禁 `any`，Rust 禁 `unwrap()` 处理输入。
- 日志操作分类为：Create、Edit、Delete、Move、Read、Verify、Review、Dispatch、Install、Start、Stop。
- `DESC` 段使用英文简短描述，段内用 `-` 连接。

## P3 最佳实践

- 可将高频模板结构缓存到本地记忆或 snippet；最终产出仍须符合模板格式和命名规范。
- 人机讨论有多轮推理链时，先写 DECISION 再写 PROACTIVE_REPORT；一句话决策无推理过程可直接写 PROACTIVE_REPORT。
- 框架升级时合并非覆盖：新模板复制、新规则段落插入，不覆盖项目实例文件。
- 区分框架规范（`templates/`、`README.md`、`TPM.md`）与项目实例（`PROJECT.md`、`ACTIONS.md`、`CHARTER.md`、`REGISTER.md`、`dashboard.md`）。

---

# 一次性（系统）规则

## TPM 入驻

- TPM 须确认用户已明确告知"你是 TPM"后再履职。
- TPM 须阅读 `README.md` 理解框架规则。
- TPM 须在 `README.md` 👑 区域替换占位符为 TPM 名字。
- TPM 须填写 `CHARTER.md`（协作宪章），从 `README.md` 和 `TPM.md` 汇总关键规则。
- TPM 须填写 `PROJECT.md`（项目信息、成员、技术栈、构建命令）。
- TPM 须检查 `.gitignore`：`inbox/`、`outbox/`、`logs/`、`context/`、`todos/` 已忽略；`archive/` 被 Git 跟踪。
- TPM 须将行为准则固化到运行环境本地记忆系统。

## Agent 入职

- 新人须先读完 `README.md`，再填写 `REGISTER.md`。
- 新人须在 `REGISTER.md` 入职动作表中逐项配置：任务分派、报告提交、审查代码、主动报告、阻塞通知、决策记录。
- 新人确认角色后须写首条日志到 `logs/{标识}-log.md`。
- TPM 确认 `REGISTER.md` 后，须将协作链路移入 `ACTIONS.md`，清空入职动作表。
- External Agent 须额外阅读 `templates/DECISION_NNN_DATE_AUTHOR.md`。
- External Agent 须将框架关键规则写入本地运行环境记忆。
- Sub-Agent 不执行入职登记，由 TPM 通过 `context/{name}-memory.md` 注入规则。

## 工具/框架更新

- TPM 升级时须读取上游 `collaboration/` 目录，对比差异，为每项变更创建 TASK。
- TPM 升级执行原则为合并非覆盖：新模板复制、新规则段落插入，不覆盖项目实例文件。
- TPM 对涉及项目级决策的变更（如启用人机结对模式）须向人类确认。
- TPM 升级完成后须写 REPORT，归档。

---

# 附录

## A. 文件类型、写者与归档时机

- TASK：位于 `inbox/`，由 TPM 写入，处理完即归档。
- REVISION：位于 `inbox/`，由 TPM 写入，处理完即归档。
- REVIEW_TASK：位于 `inbox/`，由 TPM 写入，Reviewer 提交 REVIEW_REPORT 后归档。
- NOTICE：位于 `inbox/`，由 TPM 写入，接收方已读后归档。
- REPLY：位于 `inbox/`，由 TPM 写入，提交者已读后归档。
- REVIEW_REPORT（自循环）：位于 `inbox/`，由 Reviewer 写入，ACCEPT 或 REVISION_NEEDED 后归档，并连带归档对应 TASK。
- REVIEW_REPORT（委派）：位于 `outbox/`，由 Reviewer 写入，TPM 确认后归档。
- REPORT：位于 `outbox/`，由执行者写入，相关方已读后归档。
- TEST_REPORT：位于 `outbox/`，由测试员写入，相关方已读后归档。
- PROACTIVE_REPORT：位于 `outbox/`，由任何人写入，TPM 批注并放置 REPLY 后归档。
- BLOCKING：位于 `outbox/`，由阻塞方写入，阻塞解除后归档。
- BLOCKING_REPLY：位于 `outbox/`，由解除方写入，阻塞解除后归档。
- DECISION：位于 `decisions/`，由人机结对 Agent 写入，关联 TASK/TODO 全部完成后归档。
- TODO：位于 `todos/`，由 TPM 写入，转为 TASK 后或过期废弃后归档。

## B. 任务分级

- P0 微型：单文件、纯 UI/文案/样式/格式化；无 Reviewer，TPM 直接 commit。
- P1 标准：2-3 文件、组件级逻辑；Reviewer 审 + 【审查摘要】。
- P2 复杂：跨模块、数据流、状态变更、新增 IPC；Reviewer 审 + 完整报告。
- P3 关键：架构/模型/安全/核心流程；Reviewer 审 + TPM 深度验证。
- Hotfix：线上 bug；快速通道。

## C. 状态机

- 🔵 ASSIGNED：已分派，等待领取。
- 🟡 IN_PROGRESS：执行中。
- 🟠 REVIEW_PENDING：已提交，等待审查。
- ✅ ACCEPTED：审查通过。
- 🔴 REVISION_NEEDED：需修改。
- 🟢 DONE：已合并/关闭。
- ⚪ CANCELLED：已取消。
- 🔴 BLOCKED：被阻塞。
- ✅ RESOLVED：已解除。

---

## 更新记录

- 2026-06-11 v2.5：合并过于原子的枚举项，保持每条规则围绕单一约束或动作；保留对象名开头、无表格、无来源。
