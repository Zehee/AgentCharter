# DECISION_006: 版本号发布策略

**结对**: @tpm-pair (Reasonix + Zehee)
**时间**: 2026-06-09 23:50

---

## 决策

- `collaboration/README.md` 中的主版本号（v3.2）作为 Agent 运行时可见的版本标识
- `CHANGELOG.md` 中的完整版本历史，发布时打 `git tag v3.2.1`
- README 不写版本号
- 本次发布标记为 `v3.2.1`

## 推理链

- **Zehee**: "版本号怎么维护？"
- **Reasonix**: "三个地方：collaboration/README.md（Agent 看到）、CHANGELOG.md（人看到）、Git tag（机器看到）。README 不放版本号。"

## 替代方案

1. 所有地方写版本号 → 更新太分散，否决
2. 只在 Git tag 写 → Agent 无法自检版本，否决

---

## 最终产物

| 类型 | 编号 | 说明 |
|------|------|------|
| Git tag | v3.2.1 | 发布标记 |
