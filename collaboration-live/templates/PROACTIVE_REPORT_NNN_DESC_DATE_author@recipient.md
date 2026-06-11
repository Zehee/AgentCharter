<!--
  文件类型: 主动报告 (Proactive Report)
  提交者: Reporter (任何角色均可兼任)
  特点: 无对应 TASK，不经过 inbox 任务系统
  处理: TPM 阅后即焚 — 阅读 → 决策 → 批注 → 归档
  命名规范: PROACTIVE_REPORT_NNN_DESC_DATE_AUTHOR.md
    - NNN: 自主顺序编号（与任务编号独立）
    - DESC: 英文简短描述，段内用 `-`
    - DATE: 提交日期 `YYYYMMDD`
    - AUTHOR: 作者标识（大写）
-->

# 🔍 PROACTIVE_REPORT_NNN: {{title}}

> **文件名**: `PROACTIVE_REPORT_NNN_DESC_DATE_author@recipient.md`
> **存放位置**: `outbox/`
> **命名约束**: 段间 `_`，段内 `-`。`NNN`=自主顺序编号，`DESC`=英文简短描述，`DATE`=提交日期 `YYYYMMDD`，`AUTHOR`=作者标识（大写）

**提交人**: {{author}}
**日期**: {{DATE}}
**关联决策**: {{ref_nnn}}

---

## 范围与目标

> 说明本次审计/分析/提案的范围和目标受众。
{{scope_and_goal}}

---

## 分析方法（可选）

> 描述使用的分析方法、参考标准、对比对象等。
{{analysis_method}}

---

## 发现与分析

### {{module_name}} — 评分: {{module_score}}/10

| # | 问题 | 严重级别 | 位置 | 说明 |
|---|------|----------|------|------|
| {{issue_num}} | {{issue_desc}} | {{severity}} | {{location}} | {{details}} |

**改进建议**:
{{improvement_suggestions}}

---

## 优先级改进清单

### 🔴 P0 - 立即修复
{{p0_items}}

### 🟡 P1 - 近期修复
{{p1_items}}

### 💡 P2 - 建议改进
{{p2_items}}

---

## 总结

**整体评分**: {{overall_score}}/10

**优势**:
{{strengths}}

**待改进**:
{{improvements}}

**建议行动**:
{{suggested_actions}}

---

**提交人**: {{author}}
**日期**: {{DATE}}
