<!--
  文件类型: 决策记录 (Decision)
  作者: 人机结对 Agent (TPM 或 External Agent 的 AI 部分)
  用途: 记录人机结对讨论中产生的重要决策，保留推理链和审计证据
  创建时机: AI 在对话中识别到人类确认的决策信号时自动提取；或人类主动说"记录这个决策"
  命名规范: DECISION_NNN_DATE_AUTHOR.md
    - NNN: 顺序编号（与任务编号独立）
    - DATE: 决策日期 YYYYMMDD
    - AUTHOR: 结对标识（大写）
-->

# DECISION_NNN: {{title}}

> **文件名**: `DECISION_NNN_DATE_AUTHOR.md`
> **存放位置**: `decisions/`
> **命名约束**: 段间 `_`，段内 `-`。`NNN`=顺序编号，`DATE`=决策日期 `YYYYMMDD`，`AUTHOR`=结对标识（大写）

**结对**: {{pair}}
**时间**: {{DATE}}
**关联主动报告**: {{ref_nnn}}

---

## 决策

> （一句话：决定做什么。）
{{decision}}

## 推理链

> （对话中的原始语句，一字不改。保留人类和 AI 的来回推敲过程。）
{{reasoning_chain}}

## 替代方案

> （考虑过但最终否决的方案，以及否决理由。）
{{alternatives}}

---

## 最终产物（由 TPM 或决策者后续填写）

| 类型 | 编号 | 说明 |
|------|------|------|
| {{artifact_type}} | {{artifact_nnn}} | {{artifact_description}} |
