# TASK_034: 审查流程重构——删除 reviews/、更新文档、迁移命名规范

> **Assignee**: Kimi
> **Priority**: P1
> **Decision**: DECISION_021_20260610_TRI-PAIR.md（含最终校正）
> **Source**: PROACTIVE_REPORT_007

---

## 目标

根据 DECISION_021 的决策（含 Zehee 最终校正），重构目录结构和审查流程：
1. 删除冗余的 `reviews/` 目录
2. REVIEW_REPORT 模板路径改为范式相关（委派→outbox，自循环→inbox）
3. REVIEW_TASK 模板保留（标注"委派审查可选"）
4. README.md / TPM.md 更新审查生命周期，引入三种范式
5. **命名规范统一为双后缀 `_author@assignee.md`** — 全部 15 个模板 + 文档引用

**本轮不做**：collaboration 嵌套说明（已移入 TODO）

---

## 文件与改动

### 1. 物理删除目录（3 个）

```
collaboration/reviews/           → 删除
collaboration/archive/reviews/    → 删除
collaboration-live/reviews/       → 删除
```

### 2. `templates/REVIEW_REPORT_NNN_DATE_AUTHOR.md`

模板中存放位置改为范式相关：

**当前**：
```markdown
> **存放位置**: `reviews/`
```
**改为**：
```markdown
> **存放位置**: 范式相关——委派审查放 `outbox/`（给 TPM），自循环审查放 `inbox/`（给 coder）
```

### 3. `templates/REVIEW_TASK_NNN.md`

在文件顶部增加可选标注：

```markdown
<!-- 委派审查范式下使用。自循环审查范式下不需要此模板。 -->
```

### 4. 命名规范迁移：全部模板改为 `_author@assignee.md`

**当前后缀体系**：
| 当前 | 含义 | 问题 |
|------|------|------|
| `_AUTHOR` | 谁写的 | 不知道给谁 |
| `_ASSIGNEE` | 谁执行的 | 不知道谁发起的 |
| `_TARGET` | 发给谁的通知 | 一致 |
| `_SOURCE` | 从哪来的 TODO | 一致 |

**改为双后缀 `_author@assignee.md`**：

| 模板 | 当前 | 改为 |
|------|------|------|
| TASK | `TASK_NNN_DESC_ASSIGNEE.md` | `TASK_NNN_DESC_tpm@assignee.md` |
| REPORT | `REPORT_NNN_DATE_AUTHOR.md` | `REPORT_NNN_DATE_author@tpm.md` |
| REVISION | `REVISION_NNN_DATE_ASSIGNEE.md` | `REVISION_NNN_DATE_tpm@assignee.md` |
| REVIEW_REPORT | `REVIEW_REPORT_NNN_DATE_AUTHOR.md` | `REVIEW_REPORT_NNN_DATE_author@recipient.md` |
| REVIEW_TASK | `REVIEW_TASK_NNN.md` | `REVIEW_TASK_NNN_tpm@reviewer.md` |
| PROACTIVE_REPORT | `PROACTIVE_REPORT_NNN_DESC_DATE_AUTHOR.md` | `PROACTIVE_REPORT_NNN_DESC_DATE_author@tpm.md` |
| NOTICE | `NOTICE_NNN_DESC_DATE_TARGET.md` | `NOTICE_NNN_DESC_DATE_author@target.md` |
| REPLY | `REPLY_NNN_DESC_DATE_AUTHOR.md` | `REPLY_NNN_DESC_DATE_author@target.md` |
| BLOCKING | `BLOCKING_NNN_DATE_TARGET.md` | `BLOCKING_NNN_DATE_author@target.md` |
| BLOCKING_REPLY | `BLOCKING_REPLY_NNN_DATE_AUTHOR.md` | `BLOCKING_REPLY_NNN_DATE_author@target.md` |
| TODO | `TODO_NNN_DESC_SOURCE.md` | 保持（`_SOURCE` 已双义）|
| DECISION | `DECISION_NNN_DATE_AUTHOR.md` | `DECISION_NNN_DATE_pair@archive.md` |
| TEST_REPORT | `TEST_REPORT_NNN_DATE_AUTHOR.md` | `TEST_REPORT_NNN_DATE_author@tpm.md` |
| TASK_TEST | `TASK_TEST_NNN_DESC_ASSIGNEE.md` | `TASK_TEST_NNN_DESC_tpm@assignee.md` |
| LOG_ENTRY | 不涉及 | 不涉及 |

**约束**：
- 更新文件名规范说明，**模板内容中引用的文件名示例同步更新**
- 历史 archive/ 文件保留原名，不追溯
- collaboration_en/ 同步

### 5. `collaboration/README.md`（多处）

**5.1 目录树**：
- 去掉 `reviews/` 行
- 目录结构说明更新

**5.2 权限表**：
- 去掉 `reviews/` 行
- 增加 inbox 写域精确标注（TPM/reviewer/coder 各能写什么）

**5.3 文件类型速查**：
- REVIEW_REPORT 从 reviews/ 移至 inbox/ 或 outbox/ 类别（范式相关）
- 命名规范更新为双后缀

**5.4 任务生命周期（§五）**：
- 更新审查流程描述，引入三种范式（直接/委派/自循环）
- 每种范式附流程图

**5.5 命名规范（§三）**：
- 从 `_AUTHOR/_ASSIGNEE/_TARGET` 更新为 `_author@assignee` 双后缀
- 说明双后缀的语义："谁写的@给谁的"

**5.6 归档规则（§九）**：
- 去掉 `reviews/` 归档路径

### 6. `collaboration/TPM.md`（多处）

**6.1 审查流程（§五）**：
- 重写为三种范式
- 每种范式说明：适用场景、文件流向、TPM 介入度

**6.2 归档规则（§六）**：
- 去掉 `reviews/` 归档规则

### 7. 验证器更新

`extras/template-validator/validate.py`：
- 去掉 `reviews/` 相关验证规则
- 添加双后缀命名规范的验证

### 8. 英文同步

全部同步到 `collaboration_en/`。

---

## 约束条件

- ✅ 历史 archive 文件保留原名
- ❌ 不改动模板的字段结构（只改文件名和路径标注）
- ❌ 本轮不做 collaboration 嵌套说明（已移入 TODO）

---

## 验收标准

- [ ] `collaboration/reviews/` 已删除
- [ ] `collaboration/archive/reviews/` 已删除
- [ ] `collaboration-live/reviews/` 已删除
- [ ] REVIEW_REPORT 模板标注路径范式相关
- [ ] REVIEW_TASK 模板标注"委派审查可选"
- [ ] 全部 15 个模板文件名规范更新为 `_author@assignee.md`
- [ ] 模板内容中引用的文件名示例同步更新
- [ ] README.md 目录树/权限表/文件类型速查已更新
- [ ] README.md 命名规范章节更新为双后缀
- [ ] README.md 审查生命周期更新为三种范式
- [ ] TPM.md 审查流程重写为三种范式
- [ ] TPM.md 归档规则去掉 reviews/
- [ ] 验证器已更新
- [ ] 英文版同步
- [ ] 提交 REPORT_034_KIMI.md 到 outbox/
