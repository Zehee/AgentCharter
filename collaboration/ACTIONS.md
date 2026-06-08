# 协作链路表

> 此文件由 TPM 维护。其他人只读。

每行定义一条协作通道：谁通过什么方式向谁传递什么。

---

## 字段说明

| 字段 | 含义 | 可选值 |
|------|------|--------|
| **动作** | 做什么 | `分配任务` `提交报告` `审查代码` `审查结论` `阻塞通知` `阻塞回复` `提交主动报告` `质量确认` ... |
| **发起方 → 接收方** | 谁发给谁 | Agent 标识（如 `TPM` `Alice` `Bob`）或 `ALL` |
| **通道** | 用什么传递 | 见下表 |

## 通道类型

| 通道 | 用途 | 方向 |
|------|------|------|
| `inbox/TASK` | 任务分派 | TPM → 执行者 |
| `inbox/TASK_TEST` | 测试分派 | TPM → 测试员 |
| `outbox/REPORT` | 任务完成报告 | 执行者 → TPM |
| `outbox/TEST_REPORT` | 测试完成报告 | 测试员 → TPM |
| `outbox/PROACTIVE_REPORT` | 主动报告（无 TASK） | 任何人 → TPM |
| `outbox/BLOCKING` | 阻塞通知 | 阻塞方 → 被阻塞方 |
| `outbox/BLOCKING_REPLY` | 阻塞解除回复 | 解除方 → 阻塞方 |
| `reviews/REVIEW_REPORT` | 审查结论 | Reviewer → 执行者 |
| `内部通道` | 实时交付（代码 diff / 审查通知） | TPM ↔ Sub-Agent |

## 样例

以下是一个小型团队的工作流配置：

| 动作 | 发起方 → 接收方 | 通道 |
|------|----------------|------|
| 分配任务 | TPM → Alice | inbox/TASK |
| 提交报告 | Alice → TPM | outbox/REPORT |
| 审查代码 | Bob → Alice | REPORT → REVIEW_REPORT |
| 审查结论 | Bob → Alice | reviews/REVIEW_REPORT |
| 质量确认 | Bob → TPM | 内部通道 |
| 阻塞通知 | Alice → Charlie | outbox/BLOCKING |

---

## 协作链路

| 动作 | 发起方 → 接收方 | 通道 |
|------|----------------|------|
| | | |
