# DECISION_014: TPM 工作五步法——从讨论到闭环的标准流程

**结对**: @tpm-pair (Reasonix + Zehee)
**时间**: 2026-06-10

---

## 决策

当 Zehee 和 Reasonix 的讨论形成结论时，按以下五步执行，不可跳过任何一步：

1. **Zehee 最终确认** — Reasonix 总结结论，Zehee 说"可以""同意""好的"等确认词
2. **写 DECISION** — Reasonix 立即将结论写入 `decisions/DECISION_NNN_DATE_TPM-PAIR.md`
3. **写 TASK 或 TODO** — 从 DECISION 的"最终产物"表格派生，放入 `inbox/` 或 `todos/`
4. **执行 TASK** — Reasonix 逐个执行，完成后写 REPORT
5. **写日志** — 追加到 `collaboration-live/logs/tpm-log.md`

## 推理链

- **Zehee**: "我们的讨论如果形成了决策：1、要我最终确认这些结论。2、写 DECISION。3、写 TASK 或 TODO。4、执行。5、写报告和日志。把以上的规则写入记忆，并更新到我们项目合适的地方。"
- **Reasonix**: "这五步应该放进 TPM.md 作为'讨论闭环'原则，确保任何一次我们不漏步。"

## 替代方案

1. 保持现有流程（TASK 执行后再补 DECISION）→ 顺序颠倒，容易漏掉决策文件。否决
2. 五步中省略日志 → 违反"每个字节可追溯"原则。否决

---

## 最终产物

| 类型 | 编号 | 说明 |
|------|------|------|
| TASK | 019 | 在 TPM.md §一 新增第 11 条原则"讨论闭环五步法" |
| TASK | 020 | CN+EN 同步 |
| TASK | 021 | 在 `collaboration-live/logs/` 补建 `tpm-log.md` |
