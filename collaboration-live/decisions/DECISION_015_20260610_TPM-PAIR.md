# DECISION_015: 澄清 `context/` 目录的职责边界

**结对**: @tpm-pair (Reasonix + Zehee)
**时间**: 2026-06-10

---

## 决策

`context/` 目录在 AgentCharter 中只承担一个职责：为 Native Sub-Agent 准备上下文注入文件，由 TPM 维护。这个目录：

- ✅ Sub-Agent（Native）：TPM 在每次启动/恢复前注入 `context/{name}-memory.md` 的内容
- ❌ TPM 自身：TPM 是独立 Agent，有自己的本地记忆系统（如 Reasonix memory），不使用 `context/`
- ❌ External Agent：同样——各自运行环境有自己的记忆系统，不使用 `context/`

**独立 Agent（TPM 和 External Agent）入职后应立即将框架关键规则固化到自己的运行环境记忆系统中。** 框架不强制采用哪种记忆格式——Reasonix memory、Claude project memory、Cursor rules 都可以——只要 Agent 在新会话中能恢复关键规则即可。

## 推理链

- **Zehee**: "context 下的记忆文件不是给独立 Agents 用的，是给 Native Sub-Agent 在创建时由 TPM 注入的。你有误解，我们要确保项目中不存在这个误解。"
- **Reasonix**: "对。我是 Reasonix，我自己的记忆存在本地的 reasonix memory 目录里。`context/` 是给 Peter 或 Jim 这样的 Sub-Agent 用的。TPM.md §七 中把 `context/tpm-memory.md` 说成是 TPM 的恢复工具——这是错的。"

## 替代方案

1. 保持旧文档不变 → 会产生混淆，TPM 和 External Agent 可能在 `context/` 里面放文件然后意外丢失记忆。否决

---

## 最终产物

| 类型 | 编号 | 说明 |
|------|------|------|
| TASK | 022 | 修正 `collaboration/README.md` 目录树 + 新增 §十一 记忆管理章节 |
| TASK | 023 | 修正 `TPM.md` §七 — 移除错误的"TPM 使用 context/"表述 |
| TASK | 024 | EN 同步全部 |
| TASK | 025 | CHARTER.md CN+EN 目录权限表同步修正 |
