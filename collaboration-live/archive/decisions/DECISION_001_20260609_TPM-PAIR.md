# DECISION_001: DECISION 文件为第 15 种标准模板

**结对**: @tpm-pair (Reasonix + Zehee)
**时间**: 2026-06-09 22:00
**关联主动报告**: PROACTIVE_REPORT_001_20260609_DECISION-PROTOCOL.md

---

## 决策

新增 `DECISION_NNN_DATE_AUTHOR.md` 为 AgentCharter 的第 15 种标准文件类型。人机结对 Agent（TPM 或 External Agent）在对话中产生决策时，AI 提取推理链并写入 decisions/ 目录。

## 推理链

- **Zehee**: "结对的决策信息不仅仅是 log，还要更明确他们的地位。"
- **Reasonix**: "对。DECISION 文件是证据，PROACTIVE_REPORT 是行动请求。不能让 TPM 猜测 decisions/ 里的文件是否需要行动。"
- **Zehee**: "TPM 和外部 Agent 的人机结对决策是同一种物质，区别只在汇报关系。"
- **Reasonix**: "同意。一种文件类型就够了——`DECISION_NNN_DATE_AUTHOR.md`，不分 strategic vs tactical。"

## 替代方案

1. PAIR_SESSION + DECISION_DELTA + PROACTIVE_REPORT 三层体系 → 太复杂，违反应极简哲学，否决
2. STRATEGIC_DELTA vs TACTICAL_DECISION 分层 → 伪分层，TPM 和 External Agent 本质都是人机结对，否决

---

## 最终产物

| 类型 | 编号 | 说明 |
|------|------|------|
| TASK | 001-006 | 批量升级项目文档，补全 DECISION 相关规范 |
| TODO | 001-002 | PAIR_SESSION 和社区实践试点 |
