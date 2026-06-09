# 协作链路表

> 此文件由 TPM 维护。其他人只读。

---

| 动作 | 发起方 → 接收方 | 通道 |
|------|----------------|------|
| 分配任务 | Zehee → Kimi | inbox/TASK |
| 分配任务 | TPM Reasonix → Kimi | inbox/TASK |
| 提交报告 | Kimi → Zehee / Reasonix | outbox/REPORT |
| 审查代码 | Reasonix → Kimi | REPORT → REVIEW_REPORT |
| 提交主动报告 | Kimi → Zehee / Reasonix | outbox/PROACTIVE_REPORT |
| 决策记录 | Kimi → decisions/ | DECISION_NNN_DATE_KIMI-PAIR |
