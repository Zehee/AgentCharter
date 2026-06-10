# REVISION_NNN: 修复 XXX 发现的问题

> **文件名**: `REVISION_NNN_DATE_author@recipient.md`
> **存放位置**: `inbox/`
> **命名约束**: 段间 `_`，段内 `-`，后缀 `author@recipient`。`NNN`=对应审查序号，`DATE`=创建日期 `YYYYMMDD`，`tpm`=分派 TPM 标识（大写），`assignee`=领取者标识（大写）

**分派人**: {{author}}
**执行人**: {{assignee}}
**日期**: {{DATE}}
**优先级**: {{priority}}
**对应**: {{ref_nnn}}

---

## 目标

一句话说明要修复什么。

## 问题清单

| # | 问题 | 文件/位置 | 修复要求 |
|---|------|----------|---------|
| 1 | 问题描述 | `xxx:行号` | 期望的行为 |
| 2 | 问题描述 | `xxx:行号` | 期望的行为 |

## 验收标准

- [ ] 修复条目 1
- [ ] 修复条目 2
- [ ] `[类型检查命令]` 0 错误
- [ ] 提交 `outbox/REPORT_NNN_R1_DATE_AUTHOR.md`
