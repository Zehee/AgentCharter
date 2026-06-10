# AgentCharter Scripts

**Python 3 可选工具 — 协议层是基石，脚本层是增强。**
没有 Python？目录结构、命名规范、ACTIONS.md 链路表照常运转。
有 Python？`agent.py` 是你的入口。

---

## 快速开始

```bash
python agent.py <你的名字>
# 例如：python agent.py KIMI
```

## 命令

| 命令 | 用途 |
|------|------|
| `agent.py NAME` | 总入口：身份、链路、命令列表、巡检结果 |
| `daily-check.py` | 全量巡检：扫描 inbox/outbox/decisions 全部文件 |
| `new-task.py NAME` | 创建 TASK（自动编号） |
| `new-report.py NAME` | 创建 REPORT |
| `new-revision.py NAME` | 创建 REVISION |
| `new-decision.py NAME` | 创建 DECISION（TPM）/ DECISION+PROACTIVE_REPORT（外部 Agent） |
| `new-review-report.py NAME` | 创建 REVIEW_REPORT |
| `validate-file.py PATH` | 校验单个文件 |
| `validate-all.py` | 校验全部文件 |

## 三态调用

每个 `new-*.py` 命令支持三种模式：

```
# 无参 — 输出模板结构
python new-report.py

# 仅名字 — 输出模板 + 你的待办列表
python new-report.py KIMI

# 名字 + JSON — 校验并创建文件
python new-report.py KIMI '{"TASK_NNN":"042","summary":"登录功能"}'
```

## 红线提醒

每次命令执行完毕，输出末尾自动附带当前项目的红线规则，时刻提醒不可触碰的操作。
