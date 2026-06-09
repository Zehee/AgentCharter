# 巡检日志：NOTICE_003（框架升级通知）

> **角色**: Flash (External Agent，前端开发)
> **日期**: 2026-06-10
> **动作**: 巡检 inbox/，发现 NOTICE_003

---

## 动作记录

打开 `inbox/` 目录，找到 `NOTICE_003_AGENTCHARTER-V3.3-UPDATE_ALL.md`。

## NOTICE_003 摘要

AgentCharter 框架升级到 v3.3.0，主要变化：

| 变更 | 影响 |
|------|------|
| 新增 `DECISION` 文件类型 + `decisions/` 目录 | 记录人机协作中有完整推理链的决策 |
| 新增 `docs/decision-protocol.md` | 8 章规范，DECISION 与 PROACTIVE_REPORT / TASK 的关联 |
| `collaboration/README.md` → v3.3 | 14 → 15 模板 |
| `ACTIONS.md` / `CHARTER.md` | 同步更新 |

## 对我（Flash）的影响

后续如果有"和人类推敲后达成共识"的时刻，需要写 `DECISION` 文件放进 `decisions/`。

没有分配新任务，等待中。

## 已读确认

文件顶部已标注 `✅ 已读 BY FLASH @ 2026-06-10`。
