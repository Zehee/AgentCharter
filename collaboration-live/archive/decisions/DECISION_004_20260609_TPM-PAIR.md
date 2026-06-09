# DECISION_004: 外部 Agent 的决策必须通过 PROACTIVE_REPORT 请求 TPM 行动

**结对**: @tpm-pair (Reasonix + Zehee)
**时间**: 2026-06-09 22:45

---

## 决策

外部 Agent 通过人机结对产生的 DECISION 文件，如果需要 TPM 行动，必须汇入 PROACTIVE_REPORT。DECISION 是证据（可选），PROACTIVE_REPORT 是行动请求（必须）。TPM 不主动猜测 decisions/ 中哪些文件需要行动。

## 推理链

- **Zehee**: "外部的人机结对有只生产 decision 但不汇总主动报告的情况，我们是否允许？"
- **Reasonix**: "不允许。需要 TPM 行动就必须有 PROACTIVE_REPORT。DECISION 是证据，PROACTIVE_REPORT 是行动请求。"
- **Zehee**: "有时候一句话就能决策——'写成主动报告，结束'——不需要 DECISION。"
- **Reasonix**: "正确。没有推理过程就不需要 DECISION。它是可选的质量增强，不是强制环节。"

## 替代方案

1. TPM 主动巡检 decisions/ 并自行判断 → 增加 TPM 负担，且缺乏明确的行动信号，否决

---

## 最终产物

| 类型 | 编号 | 说明 |
|------|------|------|
| TASK | 003 | 在 README §六旁边加"结对决策记录"说明 |
| TASK | 005 | 同步 EN 版 |
