# AgentCharter Scripts

**Python 3 可选工具 — 协议层是基石，脚本层是增强。**
没有 Python？目录结构、命名规范、ACTIONS.md 链路表照常运转。
有 Python？脚本省记忆、防犯错。

---

## 统一入口 `charterTool`（推荐）

`scripts/_common.py` 提供统一函数入口，三态覆盖全部场景：

```python
from _common import charterTool

# 形态 1 — 巡检
charterTool("KIMI")                 # 外部 Agent 巡检
charterTool("TPM")                  # TPM 全览巡检

# 形态 2 — 命令（TPM 独占）
charterTool("TPM", "archive")       # 自动归档已完成文件链
charterTool("TPM", "validate-all")  # 全量校验

# 形态 3 — 创建文件
charterTool("KIMI", "REPORT", body="# REPORT_042: ...", ref="042")
charterTool("TPM", "TASK", body="# TASK_043: ...")
```

body 模式下 Agent 直接写 markdown 正文，脚本自动推断文件名、recipient、DESC 等字段，不再依赖 `{{变量}}` 填充。原有 CLI 入口（`agent.py` / `tpm.py` / `new-*.py`）继续可用。

---

## 传统 CLI 入口

| 身份 | 入口 | 命令 |
|------|------|------|
| **外部 Agent** | `python agent.py <名字>` | new-report / new-review-report / new-decision / new-blocking / new-blocking-reply / validate-file |
| **TPM** | `python tpm.py TPM` | 全部命令 + 全览巡检 + 归档 |

> 外部 Agent 调 `new-decision` 时自动追加 PROACTIVE_REPORT 递交 TPM。

## 外部 Agent 命令

```
python agent.py KIMI               → 身份 + 巡检（只扫 @KIMI）
python agent.py KIMI new-report     → 模板 Schema + 可选编号
python agent.py KIMI new-report '{"ref_nnn":"042"}' → 创建文件
```

## TPM 命令

```
python tpm.py TPM                   → 全览巡检 + @TPM 任务
python tpm.py TPM daily-check       → 全量校验
python tpm.py TPM new-task '{"assignee":"KIMI","goal":"..."}' → 创建 TASK
python tpm.py TPM new-revision '{"assignee":"KIMI","ref_nnn":"042"}' → 创建修订
python tpm.py TPM archive           → 链式归档
```

## 三态调用

每个 `new-*.py` 命令支持三种模式：

```
无参          → 输出模板所有 {{变量}} 字段列表
仅名字        → 输出模板 + 你的待办列表
名字 + JSON   → 自动校验并创建文件
```

> 💡 **不用记模板字段**：无参运行一次，脚本自动输出该文件类型需要填写的字段。body 模式下直接写 markdown 正文即可。

## 红线提醒

每次命令执行完毕，输出末尾自动附带当前项目的红线规则。
