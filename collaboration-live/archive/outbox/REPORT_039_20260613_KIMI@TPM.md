# REPORT_039: 统一工具入口实现完成

<!-- DESC: UNIFIED-ENTRY-DONE -->

**提交人**: KIMI
**日期**: 20260613
**轮次**:
**状态**: REVIEW_PENDING
**对应**: 039
**报告性质**: 实现报告

---

## 完成情况

| 模块 | 状态 | 说明 |
|------|------|------|
| `charterTool` 统一入口 | ✅ | `_common.py` 新增三态函数，覆盖巡检/命令/创建 |
| body 模式 | ✅ | `run_create_flow` 仅支持 `BODY` 字段，直接写入 markdown |
| JSON 废除 | ✅ | `run_and_exit` / `agent.py` / `tpm.py` 收到 JSON 时返回明确错误提示 |
| CLI body 支持 | ✅ | 全部 `new-*.py` 改为从 stdin 或 `--body` 读取 body |
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
   - `run_create_flow` 彻底移除 JSON/模板填充路径，仅支持 body 模式；无 body 时返回明确错误提示。
   - `run_and_exit` 收到 JSON 数据时返回"JSON 传入方案已废除"错误。
   - 新增 `run_body_and_exit(file_type, agent_name, ref, body_file)` 供 `new-*.py` 使用。
   - `no_args_response` 改为返回 body 模式用法与模板示例，不再返回字段列表。

4. **`scripts/new-*.py`**
   - 全部改为 body 模式 CLI：`new-*.py NAME < body.md` 或 `new-*.py NAME --body body.md` 或 `new-*.py NAME --ref NNN --body body.md`。
   - `new-decision.py` 保留外部 Agent 创建 DECISION 后自动追加 PROACTIVE_REPORT 的逻辑。

5. **`scripts/agent.py` / `scripts/tpm.py`**
   - 命令转发改为支持额外参数列表；检测到旧式 JSON 参数时返回废除提示。

6. **`scripts/archive.py`**
   - 修复 `archive_chain()` 在主文件移动后仍使用旧路径读取关联文件的 bug。

7. **`templates/`**
   - 所有协作模板中的正文字段 `{ { 变量 } }` 已替换为 `>` 说明文本；仅保留影响文件名生成的头部字段占位符。

8. **文档**
   - `CHANGELOG.md` [Unreleased] 增加 `charterTool`、body 模式、JSON 废除条目。
   - `collaboration/README.md` 与 `collaboration_en/README.md` 快速参考表增加统一入口说明。
   - `collaboration/scripts/README.md` 与 `collaboration_en/scripts/README.md` 重写入口章节，新增 `charterTool` 三态示例与 body 模式 CLI 用法。

## 验证结果

- `charterTool("KIMI")`：返回 inbox/outbox 巡检结果 ✅
- `charterTool("TPM")`：返回 TPM 全览与 `@TPM` 任务 ✅
- `charterTool("KIMI", "archive")`：正确拒绝（命令态 TPM 独占）✅
- `charterTool("TPM", "validate-all")`：返回全量校验摘要 ✅
- `charterTool("KIMI", "REPORT", body=..., ref="039")`：生成正确文件名 ✅
- `python scripts/new-report.py KIMI --ref 039 --body body.md`：body 模式 CLI 工作 ✅
- `cat body.md | python scripts/new-report.py KIMI --ref 039`：stdin 模式工作 ✅
- `python scripts/new-report.py KIMI '{"ref_nnn":"039","title":"测试"}'`：返回 JSON 已废除提示 ✅
- `python scripts/agent.py KIMI new-report '{"ref_nnn":"039","title":"测试"}'`：返回 JSON 已废除提示 ✅
- `python scripts/agent.py KIMI` / `python scripts/tpm.py TPM`：原有巡检 CLI 不变 ✅
- `python scripts/daily-check.py`：仅历史 `DECISION_*-PAIR.md` 命名错误（超出本任务范围）

## 遗留问题

- `scripts/validate-all.py` 直接调用 `validate.validate_all(str(d))` 会触发 `AttributeError`（期望 `Path`）。本任务通过 `charterTool("TPM", "validate-all")` 内部传 `Path` 避开该问题；修复 `validate-all.py` 建议另建 TASK。
- `decisions/` 中历史 `*-PAIR.md` 文件名因含连字符被判定为 UNKNOWN，与 TASK_039 无关。
