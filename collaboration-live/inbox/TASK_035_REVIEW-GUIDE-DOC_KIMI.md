# TASK_035: 新建审查范式参考文档 review-guide.md

> **Assignee**: Kimi
> **Priority**: P1
> **Decision**: DECISION_022_20260610_TPM-PAIR.md

---

## 目标

在 `collaboration/` 下新建 `review-guide.md`，作为审查范式的独立参考文档。README.md 和 TPM.md 不再展开三种范式细节，只留一句话引用。

---

## 具体改动

### 1. 新建 `collaboration/review-guide.md`

包含以下内容：

**文件头**：
```markdown
# 审查范式参考

> 本文档供 TPM 决策使用。其他角色无需阅读。
> 默认范式：自循环审查。
> 当前项目范式由 TPM 在 `CHARTER.md` 中指定。
```

**快速对比表**：

| 维度 | TPM 直接审查 | 委派审查 | 自循环审查（默认）|
|------|-------------|---------|----------------|
| **适用团队** | 1-2 人，无专职 reviewer | 有专职 reviewer | 信任型团队 |
| **TPM 介入度** | 🔴 高（读全部代码） | 🟡 中（创建 REVIEW_TASK + 读 REVIEW_REPORT + 写 REVISION）| 🟢 低（按 P0-P3 分级抽查）|
| **审查延迟** | 低（直接）| 高（TPM 中转）| 低（reviewer ↔ coder 直接）|
| **文件流向** | REPORT → outbox / REVISION → inbox | REVIEW_TASK → inbox / REVIEW_REPORT → outbox | REVIEW_REPORT → inbox |
| **优势** | 质量最高，无信息损耗 | 分担 TPM 审阅量 | 效率最高，TPM 仅做关键决策 |
| **劣势** | TPM 消耗大，不可规模化 | 调度开销大，reviewer 报告可能需 TPM 复查 | 需要信任文化 |

**范式一：TPM 直接审查**
```
TPM ── TASK ──→ inbox → coder → REPORT → outbox ──→ TPM
  ↑                                                     │
  └────────────── REVISION ←──── inbox ←────────────────┘
```
- 适用场景、文件角色表、优缺点

**范式二：委派审查**
```
TPM ── TASK ─────────→ inbox → coder → REPORT → outbox ──→ TPM
                                    ↑                         │
                                    │                    REVIEW_TASK
                                    │                         ↓
                                    │                    inbox → reviewer
                                    │                         │
                                    └──── REVIEW_REPORT ←─────┘
                                                   │
                                    REVISION ←─────┘ (TPM 介入时)
```
- 适用场景、文件角色表、优缺点

**范式三：自循环审查**
```
                                          自循环
TPM ── TASK(reviewer+级别) ──→ inbox → coder → REPORT → outbox
                               ↑                         │
                               │                    reviewer 读
                               │                         │
                               │                    REVIEW_REPORT
                               │                         │
                               └──── coder → REPORT_R1 ──┘ (loop until ACCEPT)
                                                         │
                                          TPM 按 P0-P3 决定介入深度
```
- 适用场景、文件角色表、优缺点

### 2. 修改 `collaboration/README.md`

在 §五（任务生命周期）审查相关段落，替换为：

```markdown
> 本项目的审查范式由 TPM 在 `CHARTER.md` 中指定。
> 三种范式参考（TPM 直接审查 / 委派审查 / 自循环审查）见 `review-guide.md`。
> 各角色只需按本章文件类型速查中的入口和出口操作。
```

### 3. 修改 `collaboration/TPM.md`

在 §五（审查流程），替换详细的三种范式展开为：

```markdown
> 审查范式选择与完整对比见 `review-guide.md`。以下仅列出当前范式（自循环）下 TPM 的操作要点：
> 1. 创建 TASK 时指定 `reviewer` 和 `级别（P0/P1/P2/P3）`
> 2. 等 reviewer-coder 自循环结束（REVIEW_REPORT 标记 ACCEPT）
> 3. 按分级决定介入深度：P0 直接 commit，P1 审摘要，P2/P3 审源码
```  <!-- 简化为自循环默认操作 -->

### 4. 英文同步

全部同步到 `collaboration_en/`。

---

## 约束条件

- ❌ 不改 README.md 和 TPM.md 的非审查相关章节
- ❌ REVIEW_REPORT、REVIEW_TASK 等模板内容不受影响
- ✅ review-guide.md 是纯说明文档，不影响任何文件类型或权限规则

---

## 验收标准

- [ ] `collaboration/review-guide.md` 已创建，包含快速对比表 + 三种范式详细说明
- [ ] README.md §五 已精简为一句话引用
- [ ] TPM.md §五 已精简为自循环默认操作要点
- [ ] 英文版同步
- [ ] 提交 REPORT_035_KIMI.md 到 outbox/
