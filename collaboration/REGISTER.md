# 入职登记表

> 在此之前，请确认你已读完 `README.md` 理解了 AgentCharter 的框架规则。本文件只是入职表单。

新人按下方操作指南完成问答，逐行写入下表。完成后告知 TPM 审查。TPM 确认后移入 `ACTIONS.md`，清空入职动作表。

---

## 入职动作表

| 动作 | 发起方 → 接收方 | 通道 |
|------|----------------|------|
| 分配任务 | | |
| 提交报告 | | |
| 审查代码 | | |
| 主动报告 | | |
| 阻塞通知 | | |
| 决策记录 | | |

---

## 操作指南

### 第一步：声明角色

向开发者确认：

```
我是什么角色？(TPM / External Agent / Sub-Agent (Native) / Reviewer / Reporter)
Reporter 说明: 任何角色均可兼任 Reporter，提交无对应 TASK 的主动报告
```

记录到 `logs/xxx-log.md`。

---

### 第二步：逐项配置动作

打开 `ACTIONS.md`，读取已有成员列表。

逐项提问开发者，每确认一项立即写入上方的入职动作表：

```
动作 1 — 任务分派
  Q: 谁向我分派任务？
  选项: [已有成员列表] 或 [无]
  写入: | 分配任务 | 选择 → 我 | 通道 |
  External → inbox/TASK
  Native   → 内部通道 + inbox/TASK(记录用)
  无       → 跳过

动作 2 — 报告提交
  Q: 我的报告交给谁？
  写入: | 提交报告 | 我 → 选择 | 通道 |
  External → outbox/REPORT
  Native   → 内部通道（代码diff）+ outbox/REPORT

动作 3 — 审查代码
  Q: 我审查谁的代码？（可多选）
  写入: | 审查代码 | 我 → 选择 | REPORT → REVIEW_REPORT |
  Q: 谁审查我的代码？（可多选）
  写入: | 审查代码 | 选择 → 我 | REPORT → REVIEW_REPORT |
  Reviewer 写 REVIEW_REPORT 到 reviews/

动作 4 — 主动报告（Reporter 兼任）
  Q: 我是否需要提交主动报告？（审计、分析、设计提案等无 TASK 的报告）
  是 → 写入: | 提交主动报告 | 我 → TPM | outbox/PROACTIVE_REPORT |
  处理反馈: TPM 处理后在 inbox/ 放置 REPLY 回执

动作 5 — 阻塞依赖
  Q: 我卡住时等谁？
  写入: | 阻塞通知 | 我 → 选择 | outbox/BLOCKING |
  Q: 谁会因为我卡住？
  写入: | 阻塞通知 | 选择 → 我 | outbox/BLOCKING |

动作 6 — 决策记录（人机结对适用，Sub-Agent 跳过）
  Q: 我是否需要记录决策过程？
  如果"是" — 你是人机结对 Agent。当人类与你达成重要共识时，创建 DECISION 文件记录推理链。
  写入: | 决策记录 | 我 → decisions/ | DECISION_NNN_DATE_AUTHOR.md |
  需要 TPM 行动时，将 DECISION 汇入 PROACTIVE_REPORT。
  如果"否" — 跳过（Sub-Agent 不适用）。
```

**写入完成后状态 = 入职中。告知开发者"已填写入职登记，请让 TPM 审查"。TPM 确认后移入 ACTIONS.md，清空入职动作表。**

---

### 第三步：开始工作

```
External Agent:
  → 巡检 inbox/ 找 ASSIGNEE 是自己的 TASK
  → 领取 → 编码 → REPORT 到 outbox/ → 写 logs/
  → 兼任 Reporter 时: 主动报告 → outbox/PROACTIVE_REPORT → 等 inbox/REPLY 回执
  → 人机结对决策时: 写 DECISION → decisions/，需 TPM 行动时汇入 PROACTIVE_REPORT

Sub-Agent (Native):
  → 等 TPM 内部投递 → 编码
  → 写 REPORT 到 outbox/ → 源码直推（内部通道）→ 写 logs/
  → 无 DECISION — 纯 AI，不与人交互

Reviewer:
  → 读 REPORT → 审查 → 写 REVIEW_REPORT 到 reviews/
  → 评分，附文件:行号证据

Reporter（兼任）:
  → 主动报告 → outbox/PROACTIVE_REPORT
  → 关注 inbox/ 中的 REPLY 回执，了解处理结果

阻塞: 查动作表自己的阻塞行 → 写 BLOCKING
被阻塞: 收到后优先处理 → 写 BLOCKING_REPLY
```
