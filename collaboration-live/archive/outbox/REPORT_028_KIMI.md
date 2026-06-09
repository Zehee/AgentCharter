# REPORT_028: 框架边界标注——注释标记参考模式与规则分层

> **提交人**: Kimi
> **日期**: 2026-06-10
> **状态**: ✅ COMPLETED
> **对应**: TASK_028_ANNOTATE-BOUNDARY_KIMI

---

## 完成情况

| 文件 | 修改 | 说明 |
|------|------|------|
| `collaboration/README.md` §五 | ✅ | P0-P3 前加"参考模式"注释 |
| `collaboration/TPM.md` 初始化前 | ✅ | 加 PART A: 履职初始化（一次性规则）标记 |
| `collaboration/TPM.md` 核心原则前 | ✅ | 加 PART B: 日常履职（持久规则）标记 |
| `collaboration/TPM.md` §五 | ✅ | P0-P3 前加"参考模式"注释 |
| `collaboration_en/README.md` §5 | ✅ | 英文同步 |
| `collaboration_en/TPM.md` | ✅ | 英文同步（PART A/B + 参考模式注释）|

---

## 具体改动

### 1. collaboration/README.md §五

在 `## 五、任务生命周期` 前插入：
```markdown
> 📎 以下为框架提供的参考分级模式，源自 wolf-judge 实战经验。
> 具体级别数量和判定标准由你的项目在 `../CHARTER.md` 中定义。
```

### 2. collaboration/TPM.md PART A

在 `## 初始化` 前插入：
```markdown
## ═══════════════════════════════════════
## PART A: 履职初始化（一次性规则）
## ═══════════════════════════════════════

> TPM 首次履职时阅读，固化到记忆后不再需要重读
```

### 3. collaboration/TPM.md PART B

在 `## 一、核心原则` 前插入：
```markdown
## ═══════════════════════════════════════
## PART B: 日常履职（持久规则）
## ═══════════════════════════════════════

> TPM 日常履职依赖，建议固化到 TPM 记忆系统
```

### 4. collaboration/TPM.md §五

在 `## 五、审查流程` 前插入：
```markdown
> 📎 以下审查分级为参考模式，具体分级标准由项目在 `../CHARTER.md` 中定义。
```

---

## 自检清单

- [x] README.md §五 P0-P3 前有"参考模式"注释
- [x] TPM.md 初始化章节前有 PART A 标记
- [x] TPM.md 核心原则章节前有 PART B 标记
- [x] TPM.md §五 P0-P3 前有"参考模式"注释
- [x] `collaboration_en/` 对应位置已同步
- [x] 不修改文件结构、不修改字段内容、不改动现有规则文本

---

**当前状态**: ✅ COMPLETED — 等待 TPM 归档
