# TASK_037: 审阅优化工具代码 + 实现多轮次增量文件链

> **Assignee**: Kimi
> **Priority**: P1
> **Decision**: DECISION_024_20260611_TPM-PAIR.md

---

## 目标

基于 REVIEW_REPORT_036 的审查结论，完成两项工作：
1. **审阅优化** — 对已修复的 13 个问题做回归确认，完善代码健壮性
2. **多轮次支持** — 实现 `_R1`、`_R2` 增量文件链的完整支持

---

## 具体改动

### Part A：审阅优化

对 TPM 已修复的 13 个问题做回归确认，检查是否还有其他类似的路径/逻辑隐患：

| 检查项 | 文件 | 说明 |
|--------|------|------|
| `validate-file.py`/`daily-check.py` | `scripts/*.py` | 是否有其他未发现的路径重复 `collaboration/` 前缀 |
| `resolve_template` 返回类型 | `_common.py` | 返回 `Path|None` 但标注 `Path`，修复类型注解 |
| 异常兜底覆盖 | 全部 | 是否有遗漏的子流程未包裹 try/except |
| `_check_ref_exists` 返回类型 | `_common.py` | 标注 `str\|None` |

### Part B：多轮次实现

#### B.1 `lib/naming.py`

**NAME_PATTERNS 正则扩展**（3 类文件加 `(_R\d+)?`）：
```python
"REPORT": r"^REPORT_\d{3}(_R\d+)?_\d{8}_[A-Z]+@[A-Z]+\.md$",
"REVIEW_REPORT": r"^REVIEW_REPORT_\d{3}(_R\d+)?_\d{8}_[A-Z]+@[A-Z]+\.md$",
"REVISION": r"^REVISION_\d{3}[A-Z]?(_R\d+)?_\d{8}_[A-Z]+@[A-Z]+\.md$",
```

**TEMPLATE_BASE_PATTERNS 同步扩展**。

**`generate_filename` 增加 `round` 参数**：
```python
def generate_filename(..., round: Optional[int] = None) -> str:
    round_suffix = f"_R{round}" if round else ""
    # REPORT/REVIEW_REPORT/REVISION 分支插入 round_suffix
    return f"REPORT_{nnn}{round_suffix}_{date}_{author}@{recipient}.md"
```

#### B.2 `_common.py`

**创建前检测同 NNN 已有文件**，自动推断轮次：

```python
def _detect_existing_round(file_type, nnn, target_dir) -> tuple[int, str]:
    """返回 (最大轮次, 提示)。0=无轮次文件。"""
```

在 `run_create_flow` 中：已存在同 NNN 文件 → 自动 `round = max_round + 1` → 生成 `_R1`。不需要用户手动传 round。

**`no_args_response` 增加轮次提示**：

当 Agent 查 `new-report.py KIMI` 时，如果有已存在的 REPORT_042，提示 "已有 REPORT_042，建议创建 R1 或指定 round 参数"。

#### B.3 模板

**不新增 `_R1` 专用模板**。`resolve_template` 做 fallback：
- R1 请求 → 尝试 `REPORT_NNN_R1_DATE_...` 模板
- 不存在 → 回退到 `REPORT_NNN_DATE_...` 基础模板

#### B.4 命名规范文档修正

`docs/` 和注释中 `049C_R1` 作为 NNN 示例是错误的。`_R1` 是独立轮次段。需修正：
- 文档中 `NNN` = 3 位编号示例
- `naming.py` 注释

### Part C：补全 TPM 缺失脚本

补全 REVIEW_REPORT_036 指出的 4 个 TPM 独占脚本：

#### C.1 `new-review-task.py`

- 创建 REVIEW_TASK（委派审查范式用）
- NNN = 关联 TASK 编号，不自增
- 模板已存在：`REVIEW_TASK_NNN_author@recipient.md`
- 走标准 `run_and_exit` 流程
- 入口：`tpm.py` 独占（`agent.py` 不应包含）

#### C.2 `new-notice.py`

- 创建 NOTICE 通知
- 不自增编号，NNN 自定义
- 模板已存在：`NOTICE_NNN_DESC_DATE_author@recipient.md`
- 入口：`tpm.py` 独占

#### C.3 `new-reply.py`

- 创建 REPLY 处理回执
- 不自增编号，NNN = 对应 PROACTIVE_REPORT 编号
- 模板已存在：`REPLY_NNN_DESC_DATE_author@recipient.md`
- 入口：`tpm.py` 独占

#### C.4 `archive.py`

- 链式归档：根据流程链关系归档全套文件
- 核心逻辑：
  1. 输入一个文件（如 TASK_042）
  2. 扫描其关联的 REPORT、REVIEW_REPORT、REVISION 等
  3. 全部 ACTEPT 后 → 全部移入 `archive/` 对应子目录
  4. 同时在文件中追加 `> ✅ 已归档` 标记
- 复杂度最高，建议实现最小可行版本：
  - 单文件归档（`archive.py TASK_042` → 归档 TASK 自身）
  - 链式归档（`archive.py --chain TASK_042` → 归档 TASK + 关联文件）
- 入口：`tpm.py` 独占（需先加入 COMMANDS 列表）

---

## 约束条件

- ❌ 不改动 TASK/DECISION/TODO 的编号和命名（它们没有轮次）
- ✅ 历史文件（archive/）不追溯重命名
- ✅ 不新增模板文件（基础模板回退策略）
- ✅ `archive.py` 最小版——单文件+链式，不涉及 git 操作

---

## 验收标准

### Part A：审阅优化
- [ ] 回归确认 TPM 修复的 13 个问题无遗漏
- [ ] 路径/类型注解/异常覆盖全部扫清

### Part B：多轮次
- [ ] `naming.py` NAME_PATTERNS 支持 `REPORT_NNN_R1_DATE_...` 格式
- [ ] `generate_filename(round=1)` 生成包含 `_R1` 的文件名
- [ ] `run_create_flow` 已存在同 NNN 文件时自动使用下一个轮次
- [ ] `no_args_response` 输出轮次提示
- [ ] `resolve_template` 做 R1 回退
- [ ] 模板增加 `{{round}}` 占位符
- [ ] 命名规范注释已修正（049C_R1 错误示例）

### Part C：TPM 缺失脚本
- [ ] `new-review-task.py` 已创建，使用 REVIEW_TASK 模板
- [ ] `new-notice.py` 已创建，使用 NOTICE 模板
- [ ] `new-reply.py` 已创建，使用 REPLY 模板
- [ ] `archive.py` 已创建（最小版：单文件+链式归档）
- [ ] `tpm.py` COMMANDS 已补全上述 4 个脚本
- [ ] 提交 REPORT_037_KIMI.md 到 outbox/
