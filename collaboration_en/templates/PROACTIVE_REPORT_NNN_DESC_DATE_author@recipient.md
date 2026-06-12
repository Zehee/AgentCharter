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

# 🔍 PROACTIVE_REPORT_{{NNN}}: {{title}}

> **文件名**: `PROACTIVE_REPORT_{{NNN}}_DESC_{{DATE}}_{{author}}@{{recipient}}.md`
> **存放位置**: `outbox/`
> **命名约束**: 段间 `_`，段内 `-`。`NNN`=自主顺序编号，`DESC`=英文简短描述，`DATE`=提交日期 `YYYYMMDD`，`AUTHOR`=作者标识（大写）

**提交人**: {{author}}
**日期**: {{DATE}}
**关联决策**: {{ref_nnn}}

---

## 范围与目标

> 说明本次审计/分析/提案的范围和目标受众。

## 发现

> 列出观察到的问题、机会或风险。

## 建议

> 给出可执行的选项和推荐方案。

## 需要的决策

> 明确需要 TPM 做出的决策。
