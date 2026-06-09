# DECISION_012: 所有文档改动必须由 TASK 覆盖——完全可追溯

**结对**: @tpm-pair (Reasonix + Zehee)
**时间**: 2026-06-10

---

## 决策

DECISION_002 确立的"最终产物只有 TASK 和 TODO"是硬约束。这意味着框架核心文件的任何改动——包括 DECISION_011 触发的 README §六 更新——必须先建 TASK，完成后写 REPORT。没有豁免。我今天直接改文件违反了这条规则。从现在开始修正。

## 推理链

- **Zehee**: "我们刚刚的讨论产生的决策还是要落到 DECISION 和 TASK。一个项目中的任何改动都由 TASK 覆盖，做到完全可追溯。你说无需 TASK 是不对的。"
- **Reasonix**: "你说得对。我直接修改了 README 但没建 TASK。这是漏洞——DECISION_002 的硬约束不仅适用于协作团队，也适用于 TPM 自己。现在补。"

## 替代方案

1. 保持原样 → 违反 DECISION_002 和 TPM.md §一 第 9 条原则，否决

---

## 最终产物

| 类型 | 编号 | 说明 |
|------|------|------|
| TASK | 013 | 将 DECISION_011 触发的 README 改动（触发时机 + 决策识别表）补建 TASK 记录 |
| TASK | 014 | 将 DECISION_011 修正（分支 3 硬否定）补建 TASK 记录 |
| TASK | 015 | 将"最终产物只有 TASK/TODO"硬约束嵌入补建 TASK 记录 |
| REPORT | 013-015 | 合并完成报告 |
