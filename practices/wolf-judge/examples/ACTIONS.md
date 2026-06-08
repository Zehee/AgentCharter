# 协作链路表

定义协作网络中谁与谁通过什么通道通信。新人入职后由 TPM 从 `REGISTER.md` 移入此表。

---

| 动作 | 发起方 → 接收方 | 通道 |
|------|----------------|------|
| 分配任务 | Kimi → flash | inbox/TASK |
| 分配任务 | Kimi → Peter | 内部通道 + inbox/TASK(记录用) |
| 提交报告 | flash → Kimi | outbox/REPORT |
| 提交报告 | Peter → Kimi | 内部通道（代码diff）+ outbox/REPORT |
| 阻塞通知 | flash → Peter | outbox/BLOCKING |
| 阻塞通知 | Peter → flash | outbox/BLOCKING |
| 主动指派设计任务 | 用户 → Designer | 直接交付（不经过 inbox） |
| 提交主动报告 | Designer → Kimi | outbox/PROACTIVE_REPORT |
| 阻塞通知 | Designer → flash | outbox/BLOCKING |
| 阻塞通知 | flash → Designer | outbox/BLOCKING |
| 阻塞通知 | Designer → Kimi | outbox/BLOCKING（设计基线变更审批） |
| **审查代码** | **Jim → flash** | **REPORT → REVIEW_REPORT（P1/P2/P3，Jim 直接闭环）** |
| **审查代码** | **Jim → Peter** | **REPORT → REVIEW_REPORT（P1/P2/P3，Jim 直接闭环）** |
| **审查结论** | **Jim → flash** | **reviews/REVIEW_REPORT（直接面向代码作者）** |
| **审查结论** | **Jim → Peter** | **reviews/REVIEW_REPORT（直接面向代码作者）** |
| **质量确认** | **Jim → Kimi** | **内部通道 "ACCEPT 通知"（P1/P2/P3）** |
| **唤醒审查** | **Kimi → Jim** | **内部通道轻量通知（只发 REPORT 编号）** |
| **P0 自动通过** | **—** | **Kimi 直接 commit，无 Jim 参与** |
| 分配任务 | Kimi → buddy | inbox/TASK_TEST |
| 提交报告 | buddy → Kimi | outbox/TEST_REPORT |
| 提交主动报告 | buddy → Kimi | outbox/PROACTIVE_REPORT |
| 阻塞通知 | buddy → Kimi | outbox/BLOCKING
