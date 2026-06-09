# wolf-judge 实战案例索引

> 5 人团队 · Tauri + Rust + Vue 3 · 120+ 任务闭环
> 本页索引 `examples/` 中的全部协作文件，按类型和生命周期组织。
>
> [English](./README_en.md) · [中文](./README.md)

---

## 一、按文件类型

### 任务分派（inbox/）

| 文件 | 类型 | 说明 | 执行者 |
|------|------|------|--------|
| [TASK_113_AUDIT-LOG-BACKEND.md](./TASK_113_AUDIT-LOG-BACKEND.md) | TASK | 后端审计日志开发 | Peter |

### 执行报告（outbox/）

| 文件 | 类型 | 说明 | 作者 |
|------|------|------|------|
| [REPORT_113_20260604_PETER.md](./REPORT_113_20260604_PETER.md) | REPORT | TASK_113 执行报告 | Peter |
| [PROACTIVE_REPORT_001_20260604_BUDDY.md](./PROACTIVE_REPORT_001_20260604_BUDDY.md) | PROACTIVE_REPORT | 手动测试发现 | Buddy |
| [BLOCKING_043_20260528_FLASH.md](./BLOCKING_043_20260528_FLASH.md) | BLOCKING | 跨模块阻塞通知 | Flash |
| [PATROL_LOG_FLASH_20260610.md](./PATROL_LOG_FLASH_20260610.md) | PATROL_LOG | 外部 Agent 巡检日志 | Flash |

### 审查报告（reviews/）

| 文件 | 类型 | 说明 | 审查者 |
|------|------|------|--------|
| [REVIEW_REPORT_113_20260604_JIM.md](./REVIEW_REPORT_113_20260604_JIM.md) | REVIEW_REPORT | TASK_113 审查结论 | Jim |

### 决策与升级

| 文件 | 类型 | 说明 |
|------|------|------|
| [UPGRADE_REPORT_v3.3.0.md](./UPGRADE_REPORT_v3.3.0.md) | UPGRADE_REPORT | v3.2→v3.3 升级全链路 |

### 项目基础设施

| 文件 | 类型 | 说明 |
|------|------|------|
| [ACTIONS.md](./ACTIONS.md) | 协作链路 | 5 人团队完整链路表 |
| [PROJECT.md](./PROJECT.md) | 项目配置 | 技术栈、成员、规则 |
| [dashboard.md](./dashboard.md) | 进度报告 | 给人类看的进度 |
| [NOTICE_005_REVIEW-FLOW-V3_ALL.md](./NOTICE_005_REVIEW-FLOW-V3_ALL.md) | NOTICE | 审查流程 V3 通知 |

---

## 二、按任务生命周期

```
TASK_113 → REPORT_113 → REVIEW_REPORT_113 → ACCEPTED
     ↑          ↑              ↑
  Peter     Peter+Jim        Jim
```

完整链路见 [wolf-judge README](../README.md) §3.2。

---

## 三、文件命名示范

| 类型 | 实例文件名 | 规范验证 |
|------|-----------|---------|
| TASK | `TASK_113_AUDIT-LOG-BACKEND_PETER.md` | ✅ TASK_NNN_DESC_ASSIGNEE |
| REPORT | `REPORT_113_20260604_PETER.md` | ✅ REPORT_NNN_DATE_AUTHOR |
| REVIEW_REPORT | `REVIEW_REPORT_113_20260604_JIM.md` | ✅ REVIEW_REPORT_NNN_DATE_AUTHOR |
| BLOCKING | `BLOCKING_043_20260528_FLASH.md` | ✅ BLOCKING_NNN_DATE_TARGET |
| PROACTIVE_REPORT | `PROACTIVE_REPORT_001_20260604_BUDDY.md` | ✅ PROACTIVE_REPORT_NNN_DESC_DATE_AUTHOR |
