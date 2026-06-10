# TASK_034: 审查流程重构——删除 reviews/、整理目录、更新文档

> **Assignee**: Kimi
> **Priority**: P1
> **Decision**: DECISION_021_20260610_TRI-PAIR.md
> **Source**: PROACTIVE_REPORT_007

---

## 目标

根据 DECISION_021 的决策，重构目录结构和审查流程：
1. 删除冗余的 `reviews/` 目录
2. REVIEW_REPORT 模板路径从 `reviews/` 改为 `inbox/`
3. REVIEW_TASK 模板保留（标注"调度审查可选"）
4. README.md / TPM.md 更新审查生命周期，引入三种范式
5. 增加 inbox 写域标注和 collaboration 嵌套说明

---

## 文件与改动

### 1. 物理删除目录（3 个）

```
collaboration/reviews/           → 删除
collaboration/archive/reviews/    → 删除
collaboration-live/reviews/       → 删除
```

### 2. `templates/REVIEW_REPORT_NNN_DATE_AUTHOR.md`

模板中存放位置从 `reviews/` 改为 `inbox/`：

**当前**：
```markdown
> **存放位置**: `reviews/`
```
**改为**：
```markdown
> **存放位置**: `inbox/`
```

### 3. `templates/REVIEW_TASK_NNN.md`

在文件顶部增加可选标注：

**增加**：
```markdown
<!-- 调度审查范式下可选使用。自循环审查范式下不需要此模板。 -->
```

### 4. `collaboration/README.md`（多处）

**4.1 目录树**（约行 75-86）：
- 去掉 `reviews/` 行
- 目录结构说明更新

**4.2 权限表**（约行 94-104）：
- 去掉 `reviews/` 行
- 增加 REVIEW_REPORT 的 inbox 权限行
- 标注 inbox 写域规则

**4.3 文件类型速查**（约行 109-142）：
- 去掉 `reviews/` 相关的 REVIEW_REPORT 条目
- REVIEW_REPORT 从 reviews/ 移至 inbox/ 类别下
- 增加 "inbox 默认 TPM 独占" 说明

**4.4 任务生命周期**（§五）：
- 更新审查流程描述，引入三种范式
- 更新状态机图

**4.5 归档规则**（§九）：
- 去掉 `reviews/` 归档路径

**4.6 新增"协作空间嵌套"一节**：
在快速参考前，加一段架构预留说明，描述 collaboration 嵌套结构

### 5. `collaboration/TPM.md`（多处）

**5.1 PART B 审查流程**（§五）：
- 重写审查流程为三种范式（TPM 直接审查 / 调度审查 / 自循环审查）
- 每种范式说明适用场景和流程

**5.2 归档规则**（§六）：
- 去掉 `reviews/` 归档规则

### 6. `templates/` 验证器

`extras/template-validator/validate.py`：
- 去掉 `reviews/` 相关的目录验证规则

### 7. 英文同步

全部同步到 `collaboration_en/`：
- `collaboration_en/README.md`
- `collaboration_en/TPM.md`
- `collaboration_en/templates/REVIEW_REPORT_NNN_DATE_AUTHOR.md`
- `collaboration_en/templates/REVIEW_TASK_NNN.md`

---

## 约束条件

- ❌ 不改动 TASK、REVISION、NOTICE、REPLY 等非审查相关模板
- ❌ 不改动其他文件类型的路径或权限
- ✅ REVIEW_REPORT 只改存放位置标注，不改模板字段结构
- ✅ 三种范式只做文档描述，不做代码级约束

---

## 验收标准

- [ ] `collaboration/reviews/` 已删除
- [ ] `collaboration/archive/reviews/` 已删除
- [ ] `collaboration-live/reviews/` 已删除
- [ ] REVIEW_REPORT 模板标注存放位置为 `inbox/`
- [ ] REVIEW_TASK 模板标注"调度审查可选"
- [ ] README.md 目录树不再包含 reviews/
- [ ] README.md 权限表更新（inbox 写域标注）
- [ ] README.md 文件类型速查更新
- [ ] README.md 审查生命周期更新为三种范式
- [ ] README.md 增加协作空间嵌套说明
- [ ] TPM.md 审查流程重写为三种范式
- [ ] TPM.md 归档规则去掉 reviews/
- [ ] 英文版同步
- [ ] 验证器更新
- [ ] 提交 REPORT_034_KIMI.md 到 outbox/
