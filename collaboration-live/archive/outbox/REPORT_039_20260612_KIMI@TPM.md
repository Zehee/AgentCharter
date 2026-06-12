# REPORT_039: 统一工具入口实现完成

<!-- DESC: UNIFIED-ENTRY-DONE -->

**提交人**: KIMI
**日期**: 20260612
**轮次**:
**状态**: REVIEW_PENDING
**对应**: 039
**报告性质**: 实现报告

---

## 完成情况

| 模块 | 状态 | 说明 |
|------|------|------|
| `charterTool` 统一入口 | ✅ | `_common.py` 新增三态函数，覆盖巡检/命令/创建 |
| body 模式 | ✅ | `run_create_flow` 支持 `BODY` 字段，跳过模板与 `{ { } }` 替换 |
| 模板清理 | ✅ | 14 个模板正文字段占位符已替换为指导性 `>` 文本 |
| 权限校验 | ✅ | TPM 独占类型（TASK/NOTICE 等）对外部 Agent 拒绝 |
| 命令态 | ✅ | `archive` / `validate-all` 仅 TPM 可调用 |
| 复用现有逻辑 | ✅ | `patrol.py` 提取 `tpm_overview`，`tpm.py` 复用；`validate-all` / `archive` 复用底层函数 |
| 文档更新 | ✅ | `README.md`、`scripts/README.md`、`CHANGELOG.md` 已更新 |
| 三份同步 | ✅ | `collaboration/`、`collaboration-live/`、`collaboration_en/` 三份 `scripts/` 与模板已同步 |

## 关键改动

1. **`scripts/lib/patrol.py`**
   - 新增 `tpm_overview(agent_name, available_commands)`，从 `tpm.py` 解耦 TPM 全览巡检逻辑，供 `charterTool` 复用。

2. **`scripts/tpm.py`**
   - `show_overview()` 改为调用 `patrol.tpm_overview()`，CLI 行为保持不变。

3. **`scripts/_common.py`**
   - 新增 `charterTool(name, type=None, *, body=None, ref=None)` 统一入口。
   - 新增 `_run_patrol` / `_run_command` / `_create_file` 三个内部分发函数。
   - 新增 `_extract_title` / `_extract_desc` / `_title_to_desc` / `_infer_recipient` / `_can_create` 等辅助函数。
   - `run_create_flow` 增加 body 模式分支：当 `data` 含 `BODY` 时直接写入正文，不再读取模板。
   - 修复文件名相关字段（author/recipient/date）未写回 `data` 导致 JSON 模式模板替换失败的缺陷。

4. **`scripts/archive.py`**
   - 修复 `archive_chain()` 在主文件移动后仍使用旧路径读取关联文件的 bug。

5. **`templates/`**
   - 所有协作模板中的正文字段 `{{ 变量 }}` 已替换为 `>` 说明文本；仅保留影响文件名生成的头部字段占位符，保证 JSON 模式向后兼容。

6. **文档**
   - `CHANGELOG.md` [Unreleased] 增加 `charterTool` 与模板清理条目。
   - `collaboration/README.md` 与 `collaboration_en/README.md` 快速参考表增加统一入口说明。
   - `collaboration/scripts/README.md` 与 `collaboration_en/scripts/README.md` 重写入口章节，新增 `charterTool` 三态示例。

## 验证结果

- `charterTool("KIMI")`：返回 inbox/outbox 巡检结果 ✅
- `charterTool("TPM")`：返回 TPM 全览与 `@TPM` 任务 ✅
- `charterTool("KIMI", "archive")`：正确拒绝非 TPM 调用 ✅
- `charterTool("TPM", "validate-all")`：返回全量校验摘要 ✅
- `charterTool("KIMI", "REPORT", body=..., ref="039")`：生成 `outbox/REPORT_039_YYYYMMDD_KIMI@TPM.md` ✅
- `charterTool("TPM", "TASK", body=...)`：生成 `inbox/TASK_NNN_DESC_TPM@ASSIGNEE.md` ✅
- `charterTool("TPM", "NOTICE", body=..., ref="004")`：生成 `inbox/NOTICE_004_DESC_TPM@ALL.md` ✅
- `charterTool("KIMI", "TASK", body=...)`：正确拒绝（TASK TPM 独占）✅
- `python scripts/agent.py KIMI` / `python scripts/tpm.py TPM` / `python scripts/new-report.py ...`：原有 CLI 行为不变 ✅
- `python scripts/daily-check.py`：仅历史 `DECISION_*-PAIR.md` 命名错误（超出本任务范围）

## 遗留问题

- `scripts/validate-all.py` 直接调用 `validate.validate_all(str(d))` 会触发 `AttributeError`（期望 `Path`）。本任务通过 `charterTool("TPM", "validate-all")` 内部传 `Path` 避开该问题；修复 `validate-all.py` 建议另建 TASK。
- `decisions/` 中历史 `*-PAIR.md` 文件名因含连字符被判定为 UNKNOWN，与 TASK_039 无关。
