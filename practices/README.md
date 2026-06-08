# 实践案例

> AgentCharter 是一个框架，不是一套死规则。不同团队、不同项目可以演化出不同的协作模式。
> 这些案例展示了如何在实际项目中配置和使用 AgentCharter。

---

## 案例索引

| 实践 | 团队 | 技术栈 | 规模 | 核心特征 |
|------|------|--------|------|----------|
| [wolf-judge](./wolf-judge/README.md) | 5 人 | Tauri + Rust + Vue 3 | 120+ 任务 | P0-P3 分级审查、Sub-Agent 上下文记忆 |

---

## 如何使用

1. 阅读与你项目规模和技术栈相近的案例
2. 关注 `PROJECT.md`（团队配置）和 `ACTIONS.md`（协作关系）
3. 参考其任务分发策略、审查流程、归档规则
4. 根据自己项目的实际情况调整

---

## 贡献实践案例

如果你有成功的 AgentCharter 实践经验，欢迎贡献。提交 PR 时包含：

```
practices/<your-practice-name>/
├── README.md           # 实践概述（必填）
├── CHARTER.md           # 协作宪章（必填）
├── PROJECT.md          # 团队配置（必填）
├── ACTIONS.md          # 协作关系（必填）
└── extra/              # 其他参考材料（可选）
```

> 贡献前请脱敏（去除密钥、内部 URL、敏感信息）。
