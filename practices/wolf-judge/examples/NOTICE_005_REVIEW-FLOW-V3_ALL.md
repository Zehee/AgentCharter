> ✅ 已读 BY BUDDY @ 2026-06-04

# NOTICE_005: 审查流程 v3 变更通知

**通知人**: Kimi (TPM)
**日期**: 2026-06-04
**受众**: ALL（flash / Peter / Jim / buddy / Designer）
**生效**: 立即

---

## 变更摘要

审查流程从 v2（Kimi 全介入）升级为 v3（Jim 直接闭环 + TASK 分级），目标：减少 Kimi 上下文消耗、加速审查闭环、保证质量。

**核心变化**：
1. **REVIEW_TASK / REVISION 废除** — 不再由 Kimi 创建审查任务和修订任务
2. **Jim 直接闭环** — Jim 审 REPORT → 写 REVIEW_REPORT → 执行者读 → 修复 → 循环直到 ACCEPT
3. **TASK 分级** — 按改动复杂度分 P0/P1/P2/P3/Hotfix，Kimi 差异化介入
4. **【审查摘要】流转** — 多轮审查中摘要累计追加，执行者周转历史信息

---

## TASK 分级标准

| 级别 | 判定标准 | 你的行动 |
|------|----------|----------|
| **P0** | 单文件、纯 UI/文案/样式/格式化 | 提交 REPORT → Kimi **直接 commit**，无审查 |
| **P1** | 2-3 文件、组件级逻辑 | 提交 REPORT → Jim 审 → 如需要修复，REPORT_R1 中启用【审查摘要】 |
| **P2** | 跨模块、数据流、新增 IPC | 提交 REPORT → Jim 审 → Kimi 读摘要+关键意见 → commit |
| **P3** | 架构/模型/安全/核心流程 | 提交 REPORT → Jim 审 → Kimi 深度验证 → commit |
| **Hotfix** | 线上紧急 bug | 快速通道，视情况跳过 Jim |

**P0 白名单**：CSS/样式、文案、图标替换、布局微调、格式化

---

## 你需要做什么

### 所有执行者（flash / Peter）

1. **完成 REPORT 后，主动巡检 reviews/**
   - 去 `docs/collaboration/reviews/` 查找 `REVIEW_REPORT_*_{你的名字}.md`
   - 如找到，立即阅读并按意见修复

2. **多轮修复时，在 REPORT 中启用【审查摘要】**
   - REPORT 模板中已预置注释掉的【审查摘要】节
   - R1/R2 时取消注释，复制上轮 REVIEW_REPORT 的【摘要】原文，追加你的回应
   - 格式：`- 🔴/🟡 问题：✅ 已修复（文件:行号）/ 🔄 未修复（原因）`

3. **P0 任务 REPORT 可极简**
   - 文件列表 + 一句话说明 + 构建结果即可

### Jim（CodeReviewer）

1. **不再读取 inbox/ REVIEW_TASK**，改为：
   - Kimi 内部通道唤醒，只发 REPORT 编号
   - 自主读取 outbox/ 中的 REPORT
   - 审完后**直接写 REVIEW_REPORT 到 reviews/**（不再是内部通道返回给 Kimi）

2. **【审查摘要】节必填**
   - 首轮：只写 `### R0`
   - R1/R2：从执行者的 REPORT_RN【审查摘要】复制历史原文，底部追加本轮

3. **审完后通知 Kimi**
   ```
   REPORT_XXX 审查完成
   - 评分：X/10
   - 🔴：N | 🟡：N | 💡：N
   - 状态：✅ ACCEPT / 🔄 需修复
   - REVIEW_REPORT 路径：reviews/REVIEW_REPORT_XXX_YYYYMMDD_JIM.md
   ```

---

## 为什么这样改

| 问题 | 解决方案 |
|------|----------|
| Kimi 读每份 REPORT，上下文爆炸 | 分级后 P0 不读、P1 只读 5-10 行摘要 |
| Jim 和代码作者"无接触" | Jim 直接写 REVIEW_REPORT 到 reviews/，代码作者直接读 |
| Jim 上下文不稳定，多轮审查丢历史 | 执行者周转摘要，Jim 永远只读当前 REPORT |
| REVIEW_TASK/REVISION 冗余 | 废除，Jim 闭环替代 |

---

## 遗留事项

- `REVIEW_TASK_102_R2` 已按旧流程完成，是最后一个旧流程审查任务
- 模板（REVIEW_TASK、REVISION）保留在 `templates/` 中，做最大集兼容泛化

---

**有疑问请通过 outbox/BLOCKING 或内部通道联系 Kimi。**
