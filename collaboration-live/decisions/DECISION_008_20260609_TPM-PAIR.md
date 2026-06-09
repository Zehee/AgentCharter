# DECISION_008: 外部 Agent 的 DECISION 需要 TPM 行动时必须有 PROACTIVE_REPORT

**结对**: @tpm-pair (Reasonix + Zehee)
**时间**: 2026-06-09 23:58

---

## 决策

外部 Agent 通过人机结对产生的 DECISION 文件，如果需要 TPM 行动，必须汇入 PROACTIVE_REPORT。DECISION 是证据，PROACTIVE_REPORT 是行动请求。TPM 不主动猜测 decisions/ 中哪些文件需要行动。

## 推理链

- **Zehee**: "外部的人机结对有只生产 DECISION 但不汇总主动报告的情况，我们是否允许？"
- **Reasonix**: "需要 TPM 行动就必须有 PROACTIVE_REPORT。不能靠 TPM 自己去猜 decisions/ 里哪个文件在等它处理。"

## 替代方案

1. 允许 DECISION 单独存在，靠 TPM 主动巡检 → 增加 TPM 负担，缺乏明确行动信号，否决

---

## 最终产物

| 类型 | 编号 | 说明 |
|------|------|------|
| — | — | 已在 DECISION_004 和 collaboration/README.md §六中体现 |
