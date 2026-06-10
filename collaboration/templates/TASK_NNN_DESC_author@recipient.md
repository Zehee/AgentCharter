# TASK_NNN: 任务标题

> **文件名**: `TASK_NNN_DESC_author@recipient.md`
> **存放位置**: `inbox/`
> **命名约束**: 段间 `_`，段内 `-`，后缀 `author@recipient`。`NNN`=3位序号，`DESC`=英文简短描述，`author`=分派人标识（大写，通常为 TPM），`assignee`=领取者标识（大写）

**分派人**: [TPM 标识]
**执行人**: [External/Native 标识] / ALL
**优先级**: 🔴 P0 | 🟡 P1 | 🟢 P2
**依赖**: 如 TASK_XXX 已完成（可选）
**决策来源**: DECISION_NNN / PROACTIVE_REPORT_NNN（可选，本任务由哪个决策或主动报告触发）

---

## 目标

一句话描述这个任务要完成什么。

## 当前状态

已有的基础是什么，缺什么，为什么需要做这个任务。

## 详细需求

### 1. 子模块一（按功能拆）

概述 + 涉及文件 + 关键逻辑

### 2. 子模块二

同上

## 验收标准

- [ ] 验收条目 1
- [ ] 验收条目 2
- [ ] `[类型检查命令]` 0 错误
- [ ] 提交 `outbox/REPORT_NNN_YYYYMMDD.md`

## 参考文件

- `[前端源码路径]`
- `[后端源码路径]`
