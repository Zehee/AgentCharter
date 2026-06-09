# DECISION_011: 外部 Agent 的 DECISION 触发时机与信息对齐产物

**结对**: @tpm-pair (Reasonix + Zehee)
**时间**: 2026-06-10

---

## 决策

外部人机结对在人类说"发出去"的瞬间，AI 必须主动判断是否需要先写 DECISION。三种分支明确：

1. **多轮推理 → 先写 DECISION → 再写 PROACTIVE_REPORT**：AI 主动识别推理链，不等人类多此一举
2. **一句话决策 → 只写 PROACTIVE_REPORT**：无推理过程，不产生 DECISION
3. **仅信息对齐 → 可选写 DECISION，不写 PROACTIVE_REPORT**：认知对齐无行动请求，DECISION 作为项目知识资产留存

## 推理链

- **Zehee**: "外部 Agent 在人机结对多轮对话决策后，人类觉得发送主动报告，外部 Agent 能否知道要先写 DECISION？如果只是认知讨论做信息对齐，没有提交主动报告，是否需要记录 DECISION？"
- **Reasonix**: "两个问题。第一个——当前文档只说'汇入 PROACTIVE_REPORT'，没说触发时机。需要在 README §六 把'人类说发出去的瞬间'作为触发点，AI 主动判断。第二个——信息对齐无行动请求时 DECISION 是可选的，留在 decisions/ 里作为知识资产。"

## 替代方案

1. 不管触发时机问题，让人类自己去记 → 人类会忘记，AI 不主动违背"信任"哲学
2. 信息对齐强制要求 DECISION → 太重——对非实质性讨论强制留痕反而降低信噪比

---

## 最终产物

| 类型 | 编号 | 说明 |
|------|------|------|
| — | — | 直接在 `collaboration/README.md` §六 更新，不需要新建 TASK |
