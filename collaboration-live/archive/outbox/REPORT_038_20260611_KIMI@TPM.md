# REPORT_038: 支持 @ALL 通配收件人——更新巡检+脚本+校验

> **文件名**: `REPORT_038_20260611_KIMI@TPM.md`
> **存放位置**: `outbox/`
> **命名约束**: 段间 `_`，段内 `-`，后缀 `author@recipient`。`NNN`=任务序号，`DATE`=提交日期 `YYYYMMDD`，`author`=作者标识（大写），`tpm`=接收 TPM 标识（大写）

**提交人**: KIMI
**日期**: 20260611
**轮次**: 
**状态**: REVIEW_PENDING
**对应**: 038
**报告性质**: TASK_COMPLETION

---

## 完成情况

| 任务 | 状态 | 说明 |
|------|------|------|
| patrol.py 扫描 @ALL | ✅ | scan_inbox 同时匹配 TASK(recipient=agent) + NOTICE(@agent 或 @ALL)；scan_review_reports/scan_blockings 正则增加 `\|ALL` |
| no_args_response 区分 | ✅ | 返回 `available_tasks`(TASK only) + `available_notices`(NOTICE)；NOTICE 类型单独展示广播通知 |
| new-notice.py 默认收件人 | ✅ | `_common.run_create_flow` 中 NOTICE 默认 `recipient = "ALL"`，其他保持 `"TPM"` |
| daily-check.py 流向校验 | ✅ | 新增 `_check_notice_sender()`：校验 NOTICE author 必须是 TPM，recipient 为 ALL 或已知 Agent |
| naming.py 正则确认 | ✅ | `[A-Z]+@[A-Z]+` 已自然支持 `TPM@ALL`，无需修改 |
| 英文版同步 | ✅ | collaboration_en/scripts/ 下 patrol.py、_common.py、daily-check.py、validate-all.py、validate-file.py 同步 |
| GBK 编码修复 | ✅ | daily-check.py / validate-all.py / validate-file.py 补加 `sys.stdout.reconfigure(encoding="utf-8")` |

## 改动的文件

| 文件 | 修改内容 |
|------|----------|
| `collaboration/scripts/lib/patrol.py` | scan_inbox 增加 TASK(recipient匹配)+NOTICE(@agent/@ALL)；scan_review_reports/scan_blockings 增加 `@ALL` OR 条件 |
| `collaboration/scripts/_common.py` | `run_create_flow` 中 NOTICE 默认 recipient=ALL；`no_args_response` 区分 tasks/notices，NOTICE 类型展示 available_notices |
| `collaboration/scripts/daily-check.py` | 新增 `_check_notice_sender` 校验；`check_flow` 对 NOTICE 调用该校验；补加 GBK 编码修复 |
| `collaboration/scripts/validate-all.py` | 补加 GBK 编码修复 |
| `collaboration/scripts/validate-file.py` | 补加 GBK 编码修复 |
| `collaboration_en/scripts/*` | 上述全部同步到英文版 |

## 待确认（可选）

- [ ] 是否需要把 `_check_notice_sender` 的校验逻辑也加入 `validate.py` 的 `validate_file` 中，使 validate-all.py 也能捕获 NOTICE 流向错误？（当前仅在 daily-check.py 中实现）

## 补充说明（可选）

**自主识别的遗漏与修复**：

1. **旧格式 TASK 兼容**：原始 `scan_inbox` 正则只匹配 `agent@.*`，无法匹配旧格式 `TASK_038_DESC_KIMI.md`（无 @）以及新格式中 recipient=agent 的 `TASK_038_DESC_TPM@KIMI.md`。已修复为双正则（`task_pattern` + `task_pattern_recipient`），同时兼容 author=agent 和 recipient=agent。

2. **GBK 编码遗漏**：在排查 daily-check.py 输出时发现其 `flow` 字段中文显示为乱码（`��ȷ��...`）。检查发现 `daily-check.py`、`validate-all.py`、`validate-file.py` 三个入口脚本均缺少 `sys.stdout.reconfigure(encoding="utf-8")`，已统一补加。

3. **REPLY 文件名规范问题**：daily-check 扫描中发现 `REPLY_004_20260610_TPM@KIMI-PAIR.md` 被判定为 `UNKNOWN`，因 recipient `KIMI-PAIR` 含连字符，而 `naming.py` 的 `[A-Z]+` 不支持。此问题超出 TASK_038 范围，建议后续在 DECISION 中评估是否放宽 recipient 正则。

---

## 构建结果

| 命令 | 结果 |
|------|------|
| `python lib/patrol.py KIMI` | ✅ inbox 返回 2 条（1 TASK + 1 NOTICE），total_pending=2 |
| `python new-notice.py TPM '{"NNN":"999",...}'` | ✅ 生成 `NOTICE_999_..._TPM@ALL.md`，recipient 默认为 ALL |
| `python daily-check.py inbox/` | ✅ NOTICE(TPM@ALL) 通过，NOTICE(KIMI@ALL) 报 ❌ 发起方错误 |
| `python _common.py (no_args REPORT KIMI)` | ✅ available_tasks 只含 TASK，available_notices 含 NOTICE |

---

**当前状态**: REVIEW_PENDING — 等待 TPM 审查
