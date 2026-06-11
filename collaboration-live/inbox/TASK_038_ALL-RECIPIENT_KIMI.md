# TASK_038: 支持 @ALL 通配收件人——更新巡检+脚本+校验

> **Assignee**: Kimi
> **Priority**: P1
> **Source**: TPM 讨论—NOTICE 可发送给 @ALL，Agent 巡检需同时检测 @自己 和 @ALL

---

## 背景

TPM 发送 NOTICE 时收件人为 `ALL`，文件名格式为 `NOTICE_NNN_DESC_DATE_TPM@ALL.md`。
外部 Agent 的巡检和工具需要能识别 `@ALL` 的文件——"发给全体的通知就是发给我的"。

---

## 改动范围

### 1. `lib/patrol.py` — 扫描函数增加 @ALL 匹配

**`scan_inbox(agent_name)`**：
- 当前：只匹配 `TASK_*_agent@*.md`
- 改为：同时匹配 `TASK_*_*@ALL.md` 和 `NOTICE_*_*_TPM@ALL.md`

**`scan_files_by_type` / `scan_review_reports` / `scan_blockings`**：
- 当前：只按 `@agent_name` 过滤
- 改为：同时匹配 `@agent_name` 和 `@ALL`

**修改原则**：在所有 `re.compile(...)` 的 `@agent_name` 匹配后加一个 `|@ALL` 的 OR 条件，或在新循环中补充扫描 `@ALL` 文件。

### 2. 各 `new-*.py` 的 no_args_response

当前 `_common.py` 的 `no_args_response` 输出 `available_tasks` 时只返回 `@agent_name` 的任务。
改为：返回 `@agent_name` + `@ALL` 的合并列表（去重，按 NNN 升序）。

### 3. `lib/naming.py` — 文件名规范

确认当前正则是否支持 `TPM@ALL` 作为 recipient。
```
NOTICE_NNN_DESC_DATE_author@recipient.md
→ NOTICE_001_SYS-UPDATE_20260611_TPM@ALL.md
```
如果正则不支持 `ALL`（大写字母），需在 NAME_PATTERNS 和 TEMPLATE_BASE_PATTERNS 中补充。

### 4. `lib/validate.py` — 流向校验

`daily-check.py` 和 `validate-all.py` 中，NOTICE 流向校验应确认：
- 发起方是 TPM
- 接收方可以是具体 Agent 或 ALL

### 5. `new-notice.py` — 确认默认 recipient

当前 `new-notice.py` 的 `_common.run_and_exit` 中 `recipient` 默认值为 `"TPM"`。
NOTICE 应默认 `recipient = "ALL"`（TPM 创建通知时通常是全员）。

---

## 约束条件

- ✅ 只 `NOTICE` 允许 `@ALL`。TASK/REPORT/REVISION/REVIEW_REPORT 等不应出现 `@ALL`
- ✅ `new-notice.py` 默认 recipient = ALL，其他脚本默认 recipient = TPM
- ❌ 不改动 DECISION/TODO 的命名规范

---

## 验收标准

- [ ] `patrol.scan_inbox("KIMI")` 返回同时包含 `TASK_042_KIMI@TPM.md` 和 `NOTICE_001_TPM@ALL.md`
- [ ] `no_args_response` 输出包含 `@ALL` 的任务
- [ ] `naming.py` 正则支持 `TPM@ALL.md`
- [ ] `new-notice.py` 默认 recipient = `ALL`
- [ ] 英文版同步
- [ ] 提交 REPORT_038_KIMI.md 到 outbox/
