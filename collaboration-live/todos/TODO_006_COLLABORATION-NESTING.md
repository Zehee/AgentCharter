# TODO_006: collaboration 嵌套架构设计

> **排期**: 远期规划，当前不纳入开发
> **来源**: DECISION_021 §9
> **状态**: ⏳ 概念设计

---

## 设计方向（已确认）

- 子协作空间物理嵌套在父协作空间内部（非平级）
- 每级部门负责人成为自己部门的 TPM
- 跨空间通信规则：只读对方 outbox，不写对方 inbox

### 结构示意

```
collaboration/                          ← 父协作空间（总 TPM）
├── inbox/              ← 总 TPM 独占写
├── outbox/             ← 组 TPM 写汇总（给总 TPM 读）
├── CHARTER.md          ← 父级宪章
│
├── collaboration-frontend/             ← 子协作空间（前端 TPM）
│   ├── inbox/          ← 前端 TPM 独占写
│   ├── outbox/         ← 前端 coder 写（给前端 TPM 读）
│   └── CHARTER.md      ← 子级宪章
│
└── collaboration-backend/              ← 子协作空间（后端 TPM）
    ├── inbox/
    ├── outbox/
    └── CHARTER.md
```

## 待细化问题

- [ ] 组 TPM 如何在父空间 outbox 中感知跨组需求？（无通知机制）
- [ ] 子空间 CHARTER.md 与父空间 CHARTER.md 的优先级规则
- [ ] 跨空间命名规范是否需要额外标识
