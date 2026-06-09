# DECISION_003: TPM 和 External Agent 均为默认人机结对

**结对**: @tpm-pair (Reasonix + Zehee)
**时间**: 2026-06-09 22:30

---

## 决策

TPM 和 External Agent 在默认设定下均为"人机结对综合体"——背后可以是一个或多个 Agent 加上一个或多个人类参与者。对话中有共识时产生 DECISION 记录。Sub-Agent (Native) 为纯 AI，不直接与人交互，不产生 DECISION。

## 推理链

- **Zehee**: "一般来说 native sub-agent 应该不是人机结对，这类 agent 无法直接和人类交互。"
- **Reasonix**: "三类区分——TPM 人机结对（有对话入口）、External Agent 人机结对（有对话入口）、Sub-Agent 纯 AI（无对话入口，后台运行）。DECISION 只适用于前两者。"
- **Zehee**: "同意。这个分类应该在 README §1.2 角色定义里说清楚。"

## 替代方案

1. 所有 Agent 默认为纯 AI → 与框架"人类是一等公民"的理念冲突，否决
2. 所有 Agent 默认为人机结对 → Native Sub-Agent 没有对话界面，无法结对，否决

---

## 最终产物

| 类型 | 编号 | 说明 |
|------|------|------|
| TASK | 001 | 更新 README §1.2 三种角色定义，明确谁是人机结对 |
