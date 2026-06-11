# TASK_039: 统一工具入口——三态覆盖全功能

> **Assignee**: Kimi
> **Priority**: P1
> **Source**: 三方讨论共识 — Agent 直接写 markdown 正文比拼 JSON 更自然

---

## ⚠️ 开始前必读

**请先 review 本任务的方案设计，确认没有重大遗漏或设计缺陷后再动手执行。**
如果有问题，提交 REPORT_039_REVIEW_KIMI.md 到 outbox/ 说明问题，暂停任务等 TPM 回复。
确认没有问题后，开始编码。

---

## 背景

当前工具有多个入口：`agent.py`、`tpm.py`、`new-*.py`、`daily-check.py`、`archive.py`、`validate-*.py`。
Agent 记不住这么多命令。

方案统一为**一个函数入口**——`charterTool`，三种调用形态覆盖全部场景。

---

## 设计方案

### 函数签名

```python
def charterTool(
    name: str,              # 必填。Agent 标识
    type: str = None,       # 第二参数。文件类型（REPORT/TASK）或命令（archive/validate-all）
    *,                      # 以下为关键字参数
    body: str = None,       # markdown 正文（创建文件时使用）
    ref: str = None,        # 关联编号（REPORT→TASK_NNN，自增类型忽略）
) -> dict:
```

### 三态调用

| 形态 | 调用 | 行为 |
|------|------|------|
| **巡检态** | `charterTool("KIMI")` | 自动检测 TPM/Agent，返回对应 patrol 结果（复用现有 patrol 和 tpm_overview）|
| **命令态** | `charterTool("TPM", "archive")` | TPM 独占。自动归档 inbox/outbox/decisions 中已完成的文件链 |
| | `charterTool("TPM", "validate-all")` | TPM 独占。全量校验（复用现有 daily-check.py 逻辑） |
| **创建态** | `charterTool("KIMI", "REPORT", body="...", ref="042")` | 身份 → 权限 → 引用 → 文件生成 |

### 内部实现框架

```python
def charterTool(name, type=None, *, body=None, ref=None):
    """三种形态：无type→巡检，type为命令→执行，type+body→创建。"""
    if type is None:
        return _patrol(name)                     # 复用现有 patrol 和 tpm_overview
    
    if body is None:
        return _run_command(name, type)           # archive / validate-all
    
    return _create_file(name, type, body, ref)    # 创建文件
```

### 创建态权限规则

| 文件类型 | 谁可创建 | ref |
|---------|---------|-----|
| TASK / TASK_TEST / REVISION / NOTICE / REVIEW_TASK | TPM 独占 | 非自增类型必填；自增类型（TASK/DECISION）填了忽略 |
| REVIEW_REPORT / PROACTIVE_REPORT / BLOCKING | TPM + 外部 Agent | 非自增类型必填；PROACTIVE_REPORT 不自增 |
| REPORT / TEST_REPORT | TPM + 外部 Agent | 必填（对应 TASK 编号）|
| BLOCKING_REPLY | TPM + 外部 Agent（谁阻塞谁回复） | 必填（对应 BLOCKING 编号）|
| DECISION | TPM + 外部 Agent（外部自动补 PROACTIVE_REPORT） | 自增，ref 填了忽略 |
| REPLY | TPM 独占 | 必填（对应 PROACTIVE_REPORT 编号）|

### 模板清理——去掉 {{变量}}，恢复为纯说明文档

body 模式下 Agent 不再通过 `{{变量}}` 填充模板，而是直接写 markdown 正文。
模板不再需要 `{{变量}}` 占位符，恢复为干净易读的指导手册形态。

Kimi 自行判断：
- 哪些 `{{变量}}` 可以去掉、哪些需要保留（例如 JSON 模式仍需字段映射）
- 去掉后模板的指导文字是否足够清晰
- 是否需要补充 `>` 引用行替代原来的 `{{变量}}`

### 文档更新

Kimi 自行判断哪些文档需要同步更新（README、TPM.md、review-guide.md、CHANGELOG 等），不逐一指定。

### 现有能力保留

| 能力 | 保留方式 |
|------|---------|
| JSON 输入 (`run_create_flow`) | 保持不动，向后兼容 |
| 命令行调用 (`new-*.py` / `agent.py` / `tpm.py`) | 保持不动，作为 CLI fallback |
| 大小写不敏感 | 不修改 |
| 巡检 patrol | 被 `charterTool(name)` 复用 |
| 归档 archive | 被 `charterTool(name, "archive")` 复用 |
| 全量校验 validate-all | 被 `charterTool(name, "validate-all")` 复用 |
| 红线自动输出 | 所有路径均保持 |

---

## 具体改动

### `_common.py`

新增 `charterTool()` 函数，内部按三态分发到现有逻辑：

```python
def charterTool(name, type=None, *, body=None, ref=None):
    """三种形态覆盖全部场景。"""
    # 形态 1：巡检
    if type is None:
        return _run_patrol(name)
    
    # 形态 2：命令（TPM 独占）
    if body is None:
        return _run_command(name, type)
    
    # 形态 3：创建文件
    return _create_file(name, type, body, ref)
```

各分支的实现：

**`_run_patrol(name)`**：调用 `patrol.patrol()`（外部 Agent）或 `tpm_overview()`（TPM），复用现有逻辑。

**`_run_command(name, command)`**：
- `archive` → 扫描 inbox/outbox/decisions，归档已完成关联链的文件。调用 `is_tpm()` 校验。
- `validate-all` → 调用 `daily-check.py` 或 `validate.validate_all()` 全量扫描。
- 非 TPM 调用 → 返回 `{"error": "命令 TPM 独占"}`

**`_create_file(name, type, body, ref)`**：
- 权限校验：根据文件类型判断调用者是否有权限
- ref 处理：自增类型忽略 ref；非自增类型 ref 必填
- data 组装：`{"author": name, "DATE": today, "title": from body, "ref_nnn": ref, "body": body}`
- 调 `run_create_flow(type, name, data)`，body 存在时跳过模板和 `{{}}` 替换

### `tpm.py` / `agent.py` / `new-*.py`

全部保留不动。它们仍然是有效的 CLI 入口，被 `charterTool` 在内部复用。

---

## 约束条件

- ❌ 不改动已修的 `actions.py`（大小写不敏感、is_tpm）
- ❌ 不改动已修的 `naming.py`（re.IGNORECASE）
- ❌ 不改动已修的 JSON key 统一大写（`data = {k.upper(): v}`）
- ✅ 新增 `charterTool()` 和复用函数
- ✅ `run_create_flow` 可微调（body 模式跳过模板）
- ✅ 三份 `scripts/` 同步

---

## 验收标准

- [ ] `charterTool("KIMI")` → 返回巡检结果（@KIMI 过滤）
- [ ] `charterTool("TPM")` → 返回全览巡检（含总文件数）
- [ ] `charterTool("TPM", "archive")` → 自动归档，非 TPM 调用拒绝
- [ ] `charterTool("TPM", "validate-all")` → 全量校验
- [ ] `charterTool("KIMI", "REPORT", body="## 完成情况", ref="042")` → 创建文件到 outbox/
- [ ] `charterTool("TPM", "TASK", body="## 目标")` → 创建 TASK，NNN 自动编号
- [ ] `charterTool("KIMI", "TASK", body="## 目标")` → 拒绝（TASK TPM 独占）
- [ ] 26 个模板文件（CN+EN）已清除 `{{变量}}`，恢复纯说明文档
- [ ] 已有 `new-*.py` / `agent.py` / `tpm.py` 命令行仍正常工作
- [ ] 三份 `scripts/` 同步
- [ ] 提交 REPORT_039_KIMI.md 到 outbox/
