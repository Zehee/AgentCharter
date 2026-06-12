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

# DECISION_{{NNN}}: {{title}}

> **文件名**: `DECISION_{{NNN}}_{{DATE}}_{{author}}.md`
> **存放位置**: `decisions/`
> **命名约束**: 段间 `_`，段内 `-`。`NNN`=顺序编号，`DATE`=决策日期 `YYYYMMDD`，`AUTHOR`=结对标识（大写）

**结对**: {{pair}}
**时间**: {{DATE}}
**关联主动报告**: {{ref_nnn}}

---

## 决策

> 一句话：决定做什么。

## 推理链

> 列出可选方案、排除理由、最终选择的原因。

## 影响范围

> 哪些文件/流程/角色会受到影响。

## 后续行动

> - [ ] 行动 1
> - [ ] 行动 2
