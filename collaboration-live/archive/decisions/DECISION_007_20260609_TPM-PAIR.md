# DECISION_007: "深度分析并评价"——AI 不偷懒的提示词

**结对**: @tpm-pair (Reasonix + Zehee)
**时间**: 2026-06-09 23:55

---

## 决策

将 README 顶部的一键复制提示从 `Evaluate this repo` 改为 `深度分析并评价这个仓库`（CN）和 `Do a deep analysis and review of this repo`（EN）。"深度分析"四个字明确告诉 AI 要深入读，不是扫一眼目录就走。

## 推理链

- **Zehee**: "很多 AI 读 Evaluate 这个 repo 会偷懒，只扫一眼目录就下结论。"
- **Reasonix**: "同意。'深度分析并评价'是一个明确信号——需要深入读、给出判断。"
- **Zehee**: "英文版也要同步。"
- **Reasonix**: "`Do a deep analysis and review of this repo`。"

## 替代方案

1. 不写提示词，靠 README 内容本身 → AI 跳过的概率太高，否决
2. 写更长的提示词 → 增加认知负担，与"一句话就能用"的 Quick Start 矛盾，否决

---

## 最终产物

| 类型 | 编号 | 说明 |
|------|------|------|
| — | — | 已在 COMMIT cc7a3f9 和 41af6da 中完成 |
