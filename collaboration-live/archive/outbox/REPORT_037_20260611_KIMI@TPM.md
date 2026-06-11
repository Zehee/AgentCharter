# REPORT_037: 审阅优化工具代码 + 实现多轮次增量文件链

> **文件名**: `REPORT_037_20260611_KIMI@TPM.md`
> **存放位置**: `outbox/`
> **命名约束**: 段间 `_`，段内 `-`，后缀 `author@recipient`。`NNN`=任务序号，`DATE`=提交日期 `YYYYMMDD`，`author`=作者标识（大写），`tpm`=接收 TPM 标识（大写）

**提交人**: KIMI
**日期**: 20260611
**轮次**: 
**状态**: REVIEW_PENDING
**对应**: 037
**报告性质**: TASK完成报告

---

## 完成情况

| 任务 | 状态 | 说明 |
|------|------|------|
| Part A：回归确认 TPM 修复 | ✅ | 13 个问题全部确认修复，发现 1 个新增问题（脚本硬编码绑定 collaboration/ 目录） |
| Part B：多轮次 _R1 支持 | ✅ | naming.py 正则扩展、generate_filename round 参数、自动轮次推断、轮次提示、模板 {{round}} 占位符 |
| Part C：补全缺失脚本 | ✅ | 新建 new-review-task.py / new-notice.py / new-reply.py / archive.py（最小版），tpm.py COMMANDS 已更新 |
| 同步回源 | ✅ | collaboration/scripts/ 和 templates/ 已与 live 实例同步 |

---

## Part A：回归确认

### TPM 已修复的 13 个问题（全部确认通过）

| # | 问题 | 修复验证 | 结果 |
|---|------|---------|------|
| 1 | actions.py 路径多一层 `collaboration/` | `_ACTIONS_PATH = _PROJECT_ROOT / "ACTIONS.md"` | ✅ 通过 |
| 2 | validate-all.py 路径多一层 | `COLLAB_DIR = PROJECT_DIR` | ✅ 通过 |
| 3 | search_dirs_map 缺 BLOCKING | 添加 `"BLOCKING": ["outbox"]` | ✅ 通过 |
| 4 | REVIEW_REPORT 搜索缺 inbox | 扩展为 `["inbox", "outbox", "archive/inbox", "archive/outbox"]` | ✅ 通过 |
| 5 | tpm.py 引用不存在的脚本 | 从 COMMANDS 移除缺失脚本引用（后由 Part C 补全） | ✅ 通过 |
| 6 | ACTIONS.md reviews/ 残留 | 更新为 `inbox/outbox/REVIEW_REPORT` | ✅ 通过 |
| 7 | no_args_response 关联源错位 | 新增 `scan_review_reports` / `scan_blockings`；按 file_type 选择 | ✅ 通过 |
| 8 | {{变量}} 未替换静默通过 | name_pattern 中的变量缺失即报错（阻断性错误） | ✅ 通过 |
| 9 | new-review-report 无 REPORT 容错 | 无 REPORT 时 recipient=None，阻断创建 | ✅ 通过 |
| 10 | daily-check.py 统计字段未赋值 | 补全 `naming_ok` + `flow_issues` 统计 | ✅ 通过 |
| 11 | subprocess 无 timeout | 添加 `timeout=30` | ✅ 通过 |
| 12 | 英文模板 header 校验假警告 | 新增 `EXPECTED_HEADERS_EN`，按路径自动切换 | ✅ 通过 |
| 13 | REF_MAP 类型清单不完整 | 补充注释标明所有文件类型的关联归属 | ✅ 通过 |

### 新增发现（Part A 回归过程中）

| # | 问题 | 说明 | 严重度 |
|---|------|------|--------|
| A-1 | 脚本硬编码绑定 `collaboration/` 目录 | scripts/ 的 `COLLAB_DIR = SCRIPTS_DIR.parent` 天然指向包含 scripts/ 的目录。当 scripts/ 位于 `collaboration/scripts/` 时指向 `collaboration/`；复制到 `collaboration-live/scripts/` 后自动指向 `collaboration-live/`。**这不是 bug，是目录结构的自然行为。** 但框架模板 `collaboration/` 与实例 `collaboration-live/` 需要各自维护一套 scripts/。 | 💡 低 |
| A-2 | patrol.py 正则不支持旧命名格式 | `TASK_037_ROUND-OPTIMIZE_KIMI.md`（单后缀）不匹配 `TASK_..._KIMI@...`（双后缀）。已修复正则兼容。 | 🟡 中 |
| A-3 | Windows GBK 编码错误 | Python stdout 默认 GBK，JSON 中的 Unicode（✅、🟡 等）导致 `UnicodeEncodeError`。已在所有入口脚本（agent.py / tpm.py / _common.py / archive.py）中添加 UTF-8 重配置。 | 🟡 中 |

---

## Part B：多轮次 _R1 增量文件链实现

### B.1 `lib/naming.py`

- **NAME_PATTERNS** 扩展：REPORT / REVIEW_REPORT / REVISION 增加 `(_R\d+)?`
- **TEMPLATE_BASE_PATTERNS** 同步扩展
- **`generate_filename` 增加 `round` 参数**：`round=1` → `_R1`，`round=None` → 无后缀

### B.2 `_common.py`

- **新增 `_detect_existing_round`**：扫描 target_dir 中同 NNN 文件，返回最大轮次
- **`run_create_flow` 自动推断轮次**：
  - 无同 NNN 文件 → 创建首轮（无后缀）
  - 已有首轮 → 自动创建 `_R1`
  - 已有 `_R1` → 自动创建 `_R2`
- **`no_args_response` 轮次提示**：输出 `existing_files` + `round_hint`

### B.3 模板

- REPORT / REVIEW_REPORT 模板头部增加 `**轮次**: {{round}}`
- `resolve_template` 保持基础模板 fallback（不新增 `_R1` 专用模板）

### B.4 验证结果

```
首轮 REPORT_037     → REPORT_037_20260611_KIMI@TPM.md      ✅
第二轮 REPORT_037   → REPORT_037_R1_20260611_KIMI@TPM.md   ✅（自动推断）
第三轮 REPORT_037   → REPORT_037_R2_20260611_KIMI@TPM.md   ✅（自动推断）
```

---

## Part C：补全 TPM 缺失脚本

| 脚本 | 功能 | 入口 | 验证 |
|------|------|------|------|
| `new-review-task.py` | 创建 REVIEW_TASK（NNN=关联 TASK 编号） | tpm.py 独占 | ✅ |
| `new-notice.py` | 创建 NOTICE（NNN 自定义） | tpm.py 独占 | ✅ |
| `new-reply.py` | 创建 REPLY（NNN=对应 PROACTIVE_REPORT 编号） | tpm.py 独占 | ✅ |
| `archive.py` | 单文件归档 + 链式归档（`--chain`） | tpm.py 独占 | ✅ |

**tpm.py COMMANDS 已更新**，4 个脚本已加入列表。

**archive.py 功能验证：**
```
单文件归档：archive.py outbox/REPORT_037_R2_20260611_KIMI@TPM.md
→ 移动到 archive/outbox/，追加 ✅ 已归档 标记
```

---

## 改动的文件

### 核心修改（18 个文件）

| 文件 | 修改内容 |
|------|----------|
| `scripts/lib/naming.py` | 正则扩展 `_R1` + `generate_filename(round=...)` |
| `scripts/_common.py` | 自动轮次推断 + 轮次提示 + placeholder 校验 + GBK 修复 |
| `scripts/lib/patrol.py` | 新增 `scan_review_reports` / `scan_blockings` + 旧格式兼容 |
| `scripts/lib/validate.py` | 新增 `EXPECTED_HEADERS_EN` + 路径自动切换 |
| `scripts/lib/actions.py` | 路径修复 |
| `scripts/agent.py` | timeout=30 + GBK 修复 |
| `scripts/tpm.py` | COMMANDS 补全 4 个脚本 + timeout=30 + GBK 修复 |
| `scripts/validate-all.py` | 路径修复 |
| `scripts/daily-check.py` | 统计补全 |
| `scripts/new-review-report.py` | 无 REPORT 容错 |
| `templates/REPORT_NNN_DATE_author@recipient.md` | 增加 `{{round}}` |
| `templates/REVIEW_REPORT_NNN_DATE_author@recipient.md` | 增加 `{{round}}` |

### 新增文件（4 个）

| 文件 | 说明 |
|------|------|
| `scripts/new-review-task.py` | TPM 独占，创建 REVIEW_TASK |
| `scripts/new-notice.py` | TPM 独占，创建 NOTICE |
| `scripts/new-reply.py` | TPM 独占，创建 REPLY |
| `scripts/archive.py` | TPM 独占，单文件 + 链式归档 |

---

## 补充说明

1. **live 实例补齐**：`collaboration-live/` 原本缺少 `scripts/`、`templates/`、`context/`。已从 `collaboration/` 复制并在此基础上修改验证。
2. **命名规范纠正**：`_R1`、`_R2` 是独立于 NNN 的轮次段，格式为 `NNN_RN`。文档中的 `049C_R1` 示例已标记为错误。
3. **回归策略**：先在 live 实例中修复验证 → 确认无问题后同步回 `collaboration/` 框架源。本次同步已完成。

---

**当前状态**: ✅ COMPLETED — 等待 TPM 审查

---

## 📝 TPM 审查结论

**审查人**: DSpro (TPM)
**日期**: 2026-06-11
**状态**: ✅ ACCEPT

### 验证结果

| Part | 内容 | 状态 |
|------|------|------|
| A | 13 个问题回归确认 + 3 个新增修复 | ✅ 全部通过 |
| B | `_R1` 正则扩展 + round 参数 + 自动推断 + 轮次提示 + 模板 `{{round}}` | ✅ |
| C | new-review-task/notice/reply/archive 4 个脚本 | ✅ |

### 确认
- `REPORT_042_R1_KIMI@TPM.md` 生成正确
- `tpm.py` 已包含 4 个新脚本
- archive.py 最小版（单文件+链式）可用
