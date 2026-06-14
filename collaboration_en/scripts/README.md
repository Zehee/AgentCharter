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

body 模式下 Agent 直接写 markdown 正文，脚本自动推断文件名、recipient、DESC 等字段。**JSON 传入方案已废除。**

---

## body 模式 CLI 用法

所有 `new-*.py` 命令均已改为 body 模式：

```
# 从文件读取 body
cat report.md | python new-report.py KIMI --ref 042

# 或显式指定 --body
cat report.md | python new-report.py KIMI --body report.md

# TPM 创建 TASK
cat task.md | python new-task.py TPM

# 创建 DECISION
cat decision.md | python new-decision.py KIMI
```

> ⚠️ **旧式 JSON 参数已废除**：`python new-report.py KIMI '{"ref_nnn":"042"}'` 会返回明确错误提示。

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
python agent.py KIMI new-report     → body 模式用法提示
python agent.py KIMI new-report --ref 042 < report.md → 创建文件
```

## TPM 命令

```
python tpm.py TPM                   → 全览巡检 + @TPM 任务
python tpm.py TPM daily-check       → 全量校验
python tpm.py TPM new-task < task.md → 创建 TASK
python tpm.py TPM new-revision --ref 042 < revision.md → 创建修订
python tpm.py TPM archive           → 链式归档
```

## 红线提醒

每次命令执行完毕，输出末尾自动附带当前项目的红线规则。
