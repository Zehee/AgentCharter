# REPORT_024: wolf-judge examples 索引页方案

> **提交人**: Kimi
> **日期**: 2026-06-09
> **状态**: REVIEW_PENDING
> **对应**: TASK_024_EXAMPLES-INDEX-PROPOSAL_KIMI

---

## 方案概述

为 `practices/wolf-judge/examples/` 设计索引页，解决"新用户难以导航"的问题。

---

## 一、现有文件盘点

当前 `examples/` 目录共 12 个文件：

| 文件名 | 类型 | 说明 |
|--------|------|------|
| `ACTIONS.md` | 协作链路 | 5 人团队的 ACTIONS.md 实例 |
| `BLOCKING_043_20260528_FLASH.md` | BLOCKING | 跨模块阻塞通知实例 |
| `NOTICE_005_REVIEW-FLOW-V3_ALL.md` | NOTICE | 审查流程升级通知 |
| `PATROL_LOG_FLASH_20260610.md` | 自定义 | 巡检日志（框架外自定义类型）|
| `PROACTIVE_REPORT_001_20260604_BUDDY.md` | PROACTIVE_REPORT | 测试员主动报告 |
| `PROJECT.md` | 项目配置 | wolf-judge 项目配置实例 |
| `REPORT_113_20260604_PETER.md` | REPORT | 后端 Rust 开发报告 |
| `REVIEW_REPORT_113_20260604_JIM.md` | REVIEW_REPORT | 代码审查结论 |
| `TASK_113_AUDIT-LOG-BACKEND.md` | TASK | 后端审计日志开发任务 |
| `UPGRADE_REPORT_v3.3.0.md` | UPGRADE_REPORT | v3.2→v3.3 框架升级报告 |
| `dashboard.md` | 进度报告 | TPM 维护的人类可读进度 |

---

## 二、索引页结构设计

### 方案 A：按文件类型分类（推荐）

```markdown
# wolf-judge 实战案例索引

> 5 人团队 · Tauri + Rust + Vue 3 · 120+ 任务闭环
> 本页索引全部协作文件，按类型和生命周期组织。

---

## 一、按文件类型

### 任务分派（inbox/）
| 文件 | 类型 | 说明 | 执行者 |
|------|------|------|--------|
| TASK_113_AUDIT-LOG-BACKEND.md | TASK | 后端审计日志开发 | Peter |

### 执行报告（outbox/）
| 文件 | 类型 | 说明 | 作者 |
|------|------|------|------|
| REPORT_113_20260604_PETER.md | REPORT | TASK_113 执行报告 | Peter |
| PROACTIVE_REPORT_001_20260604_BUDDY.md | PROACTIVE_REPORT | 手动测试发现 | Buddy |
| BLOCKING_043_20260528_FLASH.md | BLOCKING | 跨模块阻塞通知 | Flash |
| PATROL_LOG_FLASH_20260610.md | PATROL_LOG | 外部 Agent 巡检日志 | Flash |

### 审查报告（reviews/）
| 文件 | 类型 | 说明 | 审查者 |
|------|------|------|--------|
| REVIEW_REPORT_113_20260604_JIM.md | REVIEW_REPORT | TASK_113 审查结论 | Jim |

### 决策与升级
| 文件 | 类型 | 说明 |
|------|------|------|
| UPGRADE_REPORT_v3.3.0.md | UPGRADE_REPORT | v3.2→v3.3 升级全链路 |

### 项目基础设施
| 文件 | 类型 | 说明 |
|------|------|------|
| ACTIONS.md | 协作链路 | 5 人团队完整链路表 |
| PROJECT.md | 项目配置 | 技术栈、成员、规则 |
| dashboard.md | 进度报告 | 给人类看的进度 |
| NOTICE_005_REVIEW-FLOW-V3_ALL.md | NOTICE | 审查流程 V3 通知 |

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
```

### 方案 B：按时间线分类（备选）

按日期排序，适合想了解项目演进过程的读者。但 wolf-judge 案例的价值在于展示"协作类型多样性"，时间线不是核心诉求。

**结论**：采用方案 A（按文件类型分类）。

---

## 三、文件归类方案

### 新增文件

| 文件 | 位置 | 说明 |
|------|------|------|
| `README.md` | `practices/wolf-judge/examples/` | 索引页（本方案）|

### 无需移动现有文件

现有文件全部保留原位置，索引页通过相对路径链接。

---

## 四、CN/EN 双语同步方案

### 现状

- `practices/wolf-judge/README.md` 为中文
- `practices/wolf-judge/README_en.md` 为英文
- `examples/` 仅有中文文件

### 建议

| 方案 | 实施方式 | 优先级 |
|------|---------|--------|
| A. 英文 examples 目录 | 新增 `examples_en/`，翻译关键文件（TASK_113、REPORT_113、REVIEW_REPORT_113） | P2 |
| B. 索引页双语 | 索引页 `README.md` 提供中英文双语内容（类似外层 README） | P1 |

**推荐**：先实施方案 B（索引页本身 bilingual），英文 examples 文件待社区贡献。

原因：
- wolf-judge 的 examples 文件是"证据"而非"规范"，核心价值是展示文件类型多样性
- 索引页 bilingual 足以让英文读者导航
- 具体 example 文件的翻译工作量较大，且翻译后失去"原始文件"的审计价值

---

## 五、验收标准对照

- [x] 索引页的结构设计
- [x] 文件归类方案
- [x] CN/EN 双语同步方案

---

**当前状态**: REVIEW_PENDING — 等待 Zehee / TPM 确认后执行

---

## 📝 TPM 审查结论

**审查人**: Reasonix
**日期**: 2026-06-10
**状态**: ✅ 确认执行

### 决策
- **方案**：方案 A（按文件类型分类）+ 方案 B（索引页自身 bilingual）
- **索引页结构**：同意 Kimi 的设计——12 个文件按类型分组、每行含模板命名规范对照、顶部有定向指引

### 具体指令
1. 写入 `practices/wolf-judge/examples/README.md`（CN 索引页）
2. 同步 `examples_en/README.md`（EN 索引页，保留原始文件名不变）
3. 完成后提交 `outbox/REPORT_024-EXECUTION_KIMI.md`
