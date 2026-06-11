# 协作链路表

> 此文件由 TPM 维护。其他人只读。

每行定义一条协作通道：谁通过什么方式向谁传递什么。

---

## 通道类型

| 通道 | 用途 | 方向 |
|------|------|------|
| `inbox/TASK` | 任务分派 | TPM → 执行者 |
| `inbox/TASK_TEST` | 测试分派 | TPM → 测试员 |
| `inbox/REVISION` | 审查返工 | TPM → 执行者 |
| `inbox/REVIEW_TASK` | 审查委派（委派范式） | TPM → Reviewer |
| `inbox/REVIEW_REPORT` | 审查结论（自循环范式） | Reviewer → 执行者 |
| `inbox/NOTICE` | 系统通知 | TPM → 全员 |
| `outbox/REPORT` | 任务完成报告 | 执行者 → TPM |
| `outbox/REPORT_R1/R2` | 修复报告 | 执行者 → Reviewer |
| `outbox/TEST_REPORT` | 测试完成报告 | 测试员 → TPM |
| `outbox/PROACTIVE_REPORT` | 主动报告（无 TASK） | 任何人 → TPM |
| `outbox/REVIEW_REPORT` | 审查结论（委派范式） | Reviewer → TPM |
| `outbox/BLOCKING` | 阻塞通知 | 任何人 → 被阻塞方 |
| `outbox/BLOCKING_REPLY` | 阻塞解除回复 | 被阻塞方 → 阻塞方 |

> 通道名自带语义。动作列仅为人类阅读辅助，不参与脚本校验。

---

## 协作链路

| 动作 | 发起方 → 接收方 | 通道 |
|------|----------------|------|
| | | |
