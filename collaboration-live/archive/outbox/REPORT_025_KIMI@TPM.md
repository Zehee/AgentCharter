# REPORT_025: 速查表补全方案

> **提交人**: Kimi
> **日期**: 2026-06-09
> **状态**: REVIEW_PENDING
> **对应**: TASK_025_QUICKREF-PROPOSAL_KIMI

---

## 现状分析

当前 `collaboration/README.md` §十二 快速参考表共 11 项：

| # | 操作 | 文件/位置 | 适用角色 |
|---|------|----------|---------|
| 1 | 认领身份 | 👑 区域 / TPM.md / REGISTER.md | ALL |
| 2 | 领任务 | inbox/TASK_NNN | External/Sub-Agent |
| 3 | 交报告 | outbox/REPORT_NNN | 执行者 |
| 4 | 交主动报告 | outbox/PROACTIVE_REPORT | 任何人 |
| 5 | 记录决策 | decisions/DECISION | 人机结对 |
| 6 | 写审查结论 | reviews/REVIEW_REPORT | Reviewer |
| 7 | 报告阻塞 | outbox/BLOCKING | 任何人 |
| 8 | 解除阻塞 | outbox/BLOCKING_REPLY | 解除方 |
| 9 | 写日志 | logs/{标识}-log.md | ALL |
| 10 | 查模板 | templates/ | ALL |
| 11 | 看进度 | dashboard.md | 人类 |

---

## 遗漏项分析

基于 15 个标准模板类型，逐一核对速查表覆盖：

| 模板类型 | 速查表是否覆盖 | 高频程度 | 建议 |
|----------|--------------|---------|------|
| TASK | ✅ "领任务" | 高 | — |
| REPORT | ✅ "交报告" | 高 | — |
| REVIEW_REPORT | ✅ "写审查结论" | 中 | — |
| DECISION | ✅ "记录决策" | 中 | — |
| PROACTIVE_REPORT | ✅ "交主动报告" | 中 | — |
| BLOCKING | ✅ "报告阻塞" | 低 | — |
| BLOCKING_REPLY | ✅ "解除阻塞" | 低 | — |
| **REVISION** | ❌ **未覆盖** | **中** | **建议补充** |
| **TASK_TEST** | ❌ **未覆盖** | **中** | **建议补充** |
| **TEST_REPORT** | ❌ **未覆盖** | **中** | **建议补充** |
| NOTICE | ❌ 未覆盖 | 低（TPM 专属）| 暂不补充 |
| REPLY | ❌ 未覆盖 | 低（TPM 专属）| 暂不补充 |
| REVIEW_TASK | ❌ 未覆盖 | 低（已废除）| 不补充 |
| TODO | ❌ 未覆盖 | 低 | 暂不补充 |
| LOG_ENTRY | ✅ "写日志" | 高 | — |

### 核心遗漏（执行者高频场景）

1. **"我被要求修改代码"** → 领取 REVISION → 修复 → 写 REPORT_R1
   - 当前速查表只有"领任务"，没有"领修订"
   - REVISION 与 TASK 的区别：REVISION 有对应 REVIEW_REPORT，修复后需带【审查摘要】

2. **"我需要测试功能"** → 领取 TASK_TEST → 测试 → 写 TEST_REPORT
   - 当前速查表完全没有测试相关操作
   - wolf-judge 案例中有 Buddy（测试员）角色，测试是完整协作链路

3. **"我想了解暂缓的需求"** → 查 todos/
   - TODO 是所有人可读的，执行者可以了解排期
   - 频率较低，但价值在于"知情权"

---

## 补全方案

### 方案 A：最小补全（推荐）

仅补充执行者真正会遇到的 3 个高频遗漏项：

```markdown
| 我想... | 操作 |
|---------|------|
| ...（现有 11 项保留）... |
| 领取修订 | 查 inbox/REVISION_NNN → 修复 → 写 REPORT_NNN_R1（带【审查摘要】）|
| 领取测试任务 | 查 inbox/TASK_TEST_NNN → 测试 → 写 outbox/TEST_REPORT_NNN |
| 查看排期 | 读 `todos/` 中的 TODO 文件 |
```

### 方案 B：完整补全（备选）

补充所有遗漏项（包括 TPM 专属操作），共 15 项：

```markdown
| 我想... | 操作 |
|---------|------|
| ...（现有 11 项）... |
| 领取修订 | 查 inbox/REVISION_NNN → 修复 → 写 REPORT_NNN_R1 |
| 领取测试任务 | 查 inbox/TASK_TEST_NNN → 测试 → 写 TEST_REPORT |
| 提交测试报告 | 写 `outbox/TEST_REPORT_NNN_DATE_AUTHOR.md` |
| 查看排期 | 读 `todos/` |
| 发通知 | 写 `inbox/NOTICE_NNN`（TPM 专属）|
| 写回执 | 写 `inbox/REPLY_NNN`（TPM 专属）|
```

**结论**：采用方案 A（最小补全）。

原因：
- 速查表的核心价值是"高频操作的快速入口"
- TPM 专属操作（NOTICE/REPLY）在 TPM.md 中有详细说明，不需要在通用速查表中重复
- 测试相关操作是 wolf-judge 案例验证的完整链路，应当补充
- REVISION 是标准任务生命周期的一部分（REPORT_R1 带【审查摘要】），执行者必须理解

---

## 📝 TPM 审查结论

**审查人**: Reasonix
**日期**: 2026-06-10
**状态**: ✅ 确认执行 — 方案 A（最小补全 3 项）

### 具体指令
1. 在 `collaboration/README.md` §十二 快速参考表中追加 3 行（领取修订、领取测试任务、查看排期）
2. 同步 `collaboration_en/README.md` §12
3. 完成提交 `outbox/REPORT_025-EXECUTION_KIMI.md`

---

## 每项操作描述

### 新增项 1：领取修订

```markdown
| 我想... | 操作 |
|---------|------|
| 领取修订 | 查 inbox/REVISION_NNN → 读对应 REVIEW_REPORT → 修复 → 写 REPORT_NNN_R1（【审查摘要】节复制上轮原文 + 追加修复回应）|
```

**关键差异**：
- REVISION 有明确的 `对应: REVIEW_REPORT_NNN` 字段
- REPORT_R1 必须包含【审查摘要】节（首轮 REPORT 不需要）
- 修复后状态变为 REVIEW_PENDING，进入再审循环

### 新增项 2：领取测试任务

```markdown
| 我想... | 操作 |
|---------|------|
| 领取测试任务 | 查 inbox/TASK_TEST_NNN → 按测试计划执行 → 写 `outbox/TEST_REPORT_NNN_DATE_AUTHOR.md` |
```

**关键差异**：
- TASK_TEST 有 `测试轮次` 字段（第 X 轮 / 回归 / 验收 / 探索性）
- TEST_REPORT 有 `总体结论` 字段（✅ 通过 / 🟡 有条件通过 / ❌ 阻塞）
- 测试员可以是 Buddy（External）或独立角色

### 新增项 3：查看排期

```markdown
| 我想... | 操作 |
|---------|------|
| 查看排期 | 读 `todos/` 中的 TODO 文件，了解暂缓需求和里程碑规划 |
```

**关键差异**：
- TODO 由 TPM 维护，所有人只读
- TODO 有 `来源` 字段（如 DESIGNER-077、MILESTONE-M6）
- 长期未启动的 TODO 保留在目录中，提醒 TPM 定期审视

---

## 同步范围

本次补全需同步更新：
- `collaboration/README.md` §十二
- `collaboration_en/README.md` §十二（EN 同步）
- `CHANGELOG.md` [Unreleased]（文档更新记录）

---

## 验收标准对照

- [x] 列出还需补充的遗漏项
- [x] 每项的操作描述
- [x] 补全方案（最小 vs 完整）
- [x] 同步范围

---

**当前状态**: REVIEW_PENDING — 等待 Zehee / TPM 确认后执行
