# TASK_028: 框架边界标注——注释标记参考模式与规则分层

> **Assignee**: Kimi
> **Priority**: P1
> **Decision**: DECISION_018_20260610_TPM-PAIR.md
> **Source**: PROACTIVE_REPORT_006 建议 028 + 031（合并打包）

---

## 目标

在 README.md 和 TPM.md 上加注释标记，明确区分"框架铁律"与"参考模式"。不改字段、不改结构、不拆文件。

---

## 文件列表与改动

### 1. `collaboration/README.md` §五（任务生命周期）

在 TASK 分级表格前加注释：

```markdown
> 📎 以下为框架提供的参考分级模式，源自 wolf-judge 实战经验。
> 具体级别数量和判定标准由你的项目在 `../CHARTER.md` 中定义。
```

### 2. `collaboration/TPM.md` — 章节分隔标记

在初始化章节前增加：

```markdown
## ═══════════════════════════════════════
## PART A: 履职初始化（一次性规则）
## ═══════════════════════════════════════
```
> TPM 首次履职时阅读，固化到记忆后不再需要重读

在核心原则章节前增加：

```markdown
## ═══════════════════════════════════════
## PART B: 日常履职（持久规则）
## ═══════════════════════════════════════
```
> TPM 日常履职依赖，建议固化到 TPM 记忆系统

### 3. `collaboration/TPM.md` §五（审查流程）

在 P0-P3 审查分级表前加注释：

```markdown
> 📎 以下审查分级为参考模式，具体分级标准由项目在 `../CHARTER.md` 中定义。
```

### 4. 英文同步

同步更新 `collaboration_en/README.md` 和 `collaboration_en/TPM.md` 的对应位置，翻译应保持语义一致。

---

## 约束条件

- ❌ 不修改文件结构（不拆文件、不建新目录）
- ❌ 不修改字段内容（不改 P0-P3 的定义，只加注释）
- ❌ 不改动现有任何规则文本

---

## 验收标准

- [ ] README.md §五 P0-P3 前有"参考模式"注释
- [ ] TPM.md 初始化章节前有 PART A 标记
- [ ] TPM.md 核心原则章节前有 PART B 标记
- [ ] TPM.md §五 P0-P3 前有"参考模式"注释
- [ ] `collaboration_en/` 对应位置已同步
- [ ] `cargo check` / `vue-tsc --noEmit` 不受影响（非代码改动，确认即可）
- [ ] 提交 REPORT_028_KIMI.md 到 outbox/
