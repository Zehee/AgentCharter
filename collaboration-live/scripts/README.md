# AgentCharter Scripts

**Python 3 可选工具 — 协议层是基石，脚本层是增强。**
没有 Python？目录结构、命名规范、ACTIONS.md 链路表照常运转。
有 Python？脚本省记忆、防犯错。

---

## 入口

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
python tpm.py TPM archive           → 链式归档（待实现）
```

## 三态调用

每个 `new-*.py` 命令支持三种模式：

```
无参          → 输出模板所有 {{变量}} 字段列表
仅名字        → 输出模板 + 你的待办列表
名字 + JSON   → 自动校验并创建文件
```

> 💡 **不用记模板字段**：无参运行一次，脚本自动输出该文件类型所有需要填写的字段。

## 红线提醒

每次命令执行完毕，输出末尾自动附带当前项目的红线规则。
