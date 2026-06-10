# PROACTIVE_REPORT_007: 审查流程重构与目录结构优化

> **提交人**: @kimi-pair (Kimi + Zehee)
> **日期**: 2026-06-10
> **状态**: 待 TPM 决策
> **关联决策**: DECISION_021_20260610_TRI-PAIR.md

---

## 摘要

基于 DECISION_021 的三方讨论共识（Zehee + DSpro + Kimi），汇总以下讨论点，请 TPM 决策后续处理方式（创建 TASK / 创建 TODO / 暂缓 / 其他）。

---

## 背景

三方系统讨论了 `reviews/` 目录的冗余问题、REVISION 与 review_report 的重叠问题、审查流程的三版迭代优化、inbox 写权限的精确边界、多级汇报线的两种逻辑，以及 collaboration 嵌套架构。详细共识见 `decisions/DECISION_021_20260610_TRI-PAIR.md`。

---

## 讨论点汇总（请 TPM 决策）

### 讨论点 1：`reviews/` 目录删除

- **共识**：`reviews/` 和 `archive/reviews/` 为空目录（仅 `.gitkeep`），审查报告应统一放入 `inbox/`
- **影响文件**：`collaboration/reviews/`、`collaboration-live/reviews/`、`collaboration/archive/reviews/`
- **待决策**：是否删除？是否立即执行？

### 讨论点 2：REVIEW_REPORT 模板路径变更

- **共识**：REVIEW_REPORT 从 `reviews/` 移至 `inbox/`，reviewer 独占写
- **影响文件**：`templates/REVIEW_REPORT_NNN_DATE_AUTHOR.md`
- **待决策**：路径变更 + 模板内容是否需要同步调整？

### 讨论点 3：REVIEW_TASK 模板的去留

- **共识**：REVIEW_TASK 在"调度审查"范式下仍有需要，但在"自循环审查"下不需要
- **影响文件**：`templates/REVIEW_TASK_NNN.md`
- **待决策**：保留并标注"可选"，还是删除？

### 讨论点 4：三种审查范式文档化

- **共识**：框架应提供三种范式，由用户根据团队结构选择：
  - **TPM 直接审查**：1-2 人，无专职 reviewer
  - **调度审查**：有专职 reviewer，需 TPM 中转（REVIEW_TASK + REVIEW_REPORT）
  - **自循环审查**：信任型团队，reviewer-coder 自循环（推荐）
- **影响文件**：`README.md`、`TPM.md`
- **待决策**：三种范式是否全部写入文档？是否标注推荐度？

### 讨论点 5：inbox 写权限精确扩展

- **共识**：不是"放开 inbox"，是"REVIEW_REPORT 的写权限从 TPM 扩展到 reviewer"
- **精确边界**：
  - ✅ reviewer 可写 `REVIEW_REPORT_NNN_DATE_reviewer.md` → `inbox/`
  - ❌ reviewer 不能写 TASK、NOTICE、REPLY、REVISION
  - ❌ coder 不能写任何 inbox 文件
- **影响文件**：`README.md` §并发安全、§文件角色归属
- **待决策**：是否在 README 中标注"默认 TPM 独占，REVIEW_REPORT 可开放给 reviewer"？

### 讨论点 6：REVISION 与 REVIEW_REPORT 的关系

- **共识**：
  - REVIEW_REPORT：reviewer 的前置审查输出（评分、问题列表、摘要流转）
  - REVISION：TPM 深度介入时写的返工任务（问题清单、验收标准）
  - 两者不合并，保留各自模板
- **待决策**：是否确认保留两者？是否需要调整模板内容避免重叠？

### 讨论点 7：命名规范（`_AUTHOR` vs `_ASSIGNEE`）

- **讨论状态**：**未收敛**。三方讨论中两种观点并存：
  - **Kimi 首轮观点**：当前 `_AUTHOR` / `_ASSIGNEE` / `_TARGET` / `_SOURCE` 有内在语义分工（inbox=给谁做，outbox=谁写的），单侧后缀在单空间内足够
  - **Zehee + Kimi 修正观点**：多级汇报线下单侧后缀会丢失"这个 REPORT 是给谁的"信息，需要双后缀
  - **嵌套模型分析**：如果 collaboration 嵌套，双后缀只在跨空间通信时需要，单空间内单侧后缀足够
- **待决策**：维持现状（单侧后缀）/ 全局统一双后缀 / 为特定文件类型引入双后缀 / 其他方案？

### 讨论点 8：collaboration 嵌套预留

- **共识**：子协作空间物理嵌套在父协作空间内部，每级部门负责人成为自己部门的 TPM
- **结构**：
  ```
  collaboration/
  ├── inbox/              ← 总 TPM
  ├── outbox/
  ├── CHARTER.md
  ├── collaboration-frontend/   ← 前端 TPM
  │   ├── inbox/
  │   ├── outbox/
  │   └── CHARTER.md
  └── collaboration-backend/    ← 后端 TPM
      ├── inbox/
      ├── outbox/
      └── CHARTER.md
  ```
- **关键规则**：跨空间通信"只读不写"（读对方 outbox，不写对方 inbox）
- **影响文件**：`README.md`
- **待决策**：是否作为架构能力写入 README？是否立即实现？

---

## 自检清单

- [x] 基于 DECISION_021 的三方共识
- [x] 8 个讨论点均来自实际对话，无遗漏
- [x] 每个讨论点标明"待决策"，不预设立场
- [x] 不越权建议 TASK 或 TODO（由 TPM 决策）

---

**当前状态**: PENDING — 等待 TPM（DSpro）决策每个讨论点的后续处理方式

---

## 📝 TPM 批注意见

**处理人**: DSpro (TPM)
**日期**: 2026-06-10
**状态**: ✅ 全部确认 — 8 个讨论点均在 DECISION_021 中收敛，无未决事项

### 逐项决策

| # | 讨论点 | 决策 | 后续 |
|---|-------|------|------|
| 1 | `reviews/` 目录删除 | ✅ **执行** — 物理删除 | TASK_034 |
| 2 | REVIEW_REPORT 路径改为 `inbox/` | ✅ **执行** — reviewer 独占写 | TASK_034 |
| 3 | REVIEW_TASK 模板去留 | ✅ **保留** — 标注"调度审查可选" | TASK_034 |
| 4 | 三种审查范式文档化 | ✅ **执行** — 以团队结构命名，标注推荐度 | TASK_034 |
| 5 | inbox 写权限扩展 | ✅ **精确扩展** — reviewer 可写 REVIEW_REPORT，不能写 TASK/NOTICE/REPLY/REVISION | TASK_034 |
| 6 | REVISION vs REVIEW_REPORT | ✅ **保留两者** — REVIEW_REPORT 是前置审查输出，REVISION 是 TPM 深度介入的返工任务 | TASK_034 |
| 7 | 命名规范 | ✅ **维持现状** — 单侧后缀在单协作空间内足够。暂缓双后缀 | 等嵌套实际需求 |
| 8 | collaboration 嵌套预留 | ✅ **写入 README** — 作为架构能力说明，不立即实现 | TASK_034 |

### 执行计划

合 1 个 TASK（TASK_034）：物理删除 reviews/ + 模板路径改 inbox/ + README/TPM.md 更新三种范式

### 关联 DECISION

- DECISION_021_20260610_TRI-PAIR.md 已正式化
