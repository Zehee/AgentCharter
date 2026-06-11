# TASK_{{NNN}}: {{title}}

> **文件名**: `TASK_{{NNN}}_DESC_author@recipient.md`
> **存放位置**: `inbox/`
> **命名约束**: 段间 `_`，段内 `-`，后缀 `author@recipient`。`NNN`=3位序号，`DESC`=英文简短描述，`author`=分派人标识（大写，通常为 TPM），`assignee`=领取者标识（大写）

**分派人**: {{author}}
**执行人**: {{assignee}}
**优先级**: {{priority}}
**依赖**: {{dependency}}
> 可选：关联的 TASK 编号

**决策来源**: {{decision_source}}
> 可选：DECISION_NNN / PROACTIVE_REPORT_NNN

---

## 目标

> 一句话描述这个任务要完成什么。
{{goal}}

## 当前状态

> 已有的基础是什么，缺什么，为什么需要做这个任务。
{{current_status}}

## 详细需求

> 按功能拆分子模块，说明涉及文件、关键逻辑。
{{requirements}}

## 验收标准

> 验收条目 + [类型检查命令] 0 错误。
{{acceptance_criteria}}

## 参考文件

> 前端/后端源码路径。
{{reference_files}}
