# Dashboard 项目仪表盘

**最后更新**: 2026-06-04 12:45
**项目**: 新狼官（狼人杀法官助手）
**版本**: v2.0

---

## 📊 项目总览

| 维度 | 状态 | 说明 |
|------|------|------|
| **整体进度** | 🟢 ~96% | M0~M5 核心闭环，第二轮实测 🟡 有条件通过 |
| **构建健康度** | 🟢 健康 | `vue-tsc` ✅ / `cargo check` ✅ / `cargo test` 98 pass ✅ / commit `f1f6bcf` |
| **活跃任务** | 2 | Peter: TASK_118 / buddy: TASK_TEST_108 (维护模式) |
| **待审查** | 0 | — |
| **阻塞** | 0 | 无 BLOCKED |
| **风险** | 🟢 极低 | 核心流程完整跑通，剩余为补充验证 + 小优化 |

---

## 👥 人员状态

| 角色 | 当前工作 | 状态 |
|------|----------|------|
| **Kimi (TPM)** | 审查、任务分派、归档、dashboard 更新 | 🟢 活跃 |
| **flash (前端)** | 待命 | ✅ 待命 |
| **Peter (后端)** | TASK_118 SubPhase Engine 框架 | 🔵 ASSIGNED |
| **buddy (测试)** | TASK_TEST_108 第三轮补充验证 | 🔵 ASSIGNED |
| **Jim (审查)** | 空闲 | ✅ 待命 |
| **用户** | — | ⚪ 观察中 |

---

## 🔔 最近动态

- **6-05 03:30** — flash + 用户提交 game-engine-design.md（SubPhase Engine），Kimi 审阅采纳 → TASK_118 创建，旧 TASK_117 归档
- **6-05 01:50** — PROACTIVE_REPORT_002 采纳：集成测试战略转型，计划文件创建
- **6-04 23:40** — TASK_116 完成：flash 提交 REPORT_116，Kimi 审阅 ACCEPT，commit `3584c87`，已归档
- **6-04 15:15** — TEST_REPORT_108 归档：9 FAIL 根因为 n-modal-mask 遮罩拦截（测试脚本稳定性），PROACTIVE_REPORT_001 采纳 → TASK_116 创建给 flash
- **6-04 12:39** — buddy 提交 TEST_REPORT_107，第二轮回归验证 🟡 有条件通过（10/29 PASS，0 FAIL）
- **6-04 19:20** — TASK_110 状态待确认（Peter 声称已归档但无文件记录）；TASK_113 REVISION_NEEDED；TASK_114 已分派（flash）
- **6-04 12:18** — flash 完成 REVISION_102_R2，Jim 审查 8/10 有条件通过，代码已 commit
- **6-04 11:52** — Peter 完成 TASK_108，Jim 审查 9/10 通过，代码已 commit
- **6-04 11:38** — TASK_107 第二轮实测任务创建
- **6-04 03:23** — 修复 REVIEW_REPORT 命名错误（AUTHOR 应为审查人 JIM）
- **6-04 02:38** — Peter 批量提交 REPORT_093/094/096/100C，后端代码 commit `56cb721`

---

## 活跃任务

| 编号 | 任务 | 执行人 | 状态 | 审查级别 | 优先级 | 说明 |
|------|------|--------|------|----------|--------|------|
| TASK_TEST_108 | M5 第三轮补充验证 | buddy | 🔵 ASSIGNED | — | 🟡 P1 | TEST_REPORT_108 归档：9 FAIL 为 n-modal-mask 遮罩根因（非产品 bug），等待 TASK_116 data-testid 就绪后重新验证 |
| TASK_113 | 操作审计日志 | Peter | ✅ DONE | P2 | 🟢 P2 | Jim R1 9/10 ACCEPT，已 commit `5ab60a5` |
| TASK_116 | data-testid 测试钩子实施 | flash | ✅ DONE | — | 🟢 P1 | ~35 个属性 + Vite 插件生产剥离，commit `3584c87` |
| TASK_114 | 前端审计日志 API 同步 | flash | ✅ DONE | **P0** | 🟢 P2 | Kimi 直接 commit `6ba83bf` |
| TASK_111 | ESLint warnings 清理 | flash | ✅ DONE | **P0** | 🟢 P2 | Kimi 直接 commit `1814fb0`，P0 流程验证通过 |
| TASK_112 | TournamentView 操作列按钮 | flash | ✅ DONE | **P1** | 🟢 P2 | Jim 审查 R2 9/10 ACCEPT，已 commit `84393dc` |

---

## 本周期完成

| 编号 | 任务 | 执行人 | 评分 | 轮次 | 状态 |
|------|------|--------|------|------|------|
| REVISION_102_R2 | 投票拖动修复（第二轮） | flash | 8/10 | R2 | ✅ ACCEPT | mouseup document 级别监听 + 选择器修正 + 死代码清理 |
| TASK_108 | 后端优化清理 | Peter | 9/10 | R0 | ✅ ACCEPT | death_log 清理 / seat 校验 / 弃票信息 / 测试重命名 |
| TEST_REPORT_107 | M5 第二轮回归验证 | buddy | — | — | 🟡 有条件通过 | 10/29 PASS，0 FAIL，核心流程完整跑通 |
| REVISION_101/104/105 | 前端 UX 和交互修复 | flash | — | — | ✅ ACCEPT | Jim 批量审查：3 份通过，代码已 commit `eec1546` |
| REPORT_101_104_105_112_R2 | Jim 审查批量修复 | flash | 9/10 | R2 | ✅ ACCEPT | 13 项修复全部验证通过，已 commit `84393dc` |
| TASK_113 | 后端操作审计日志 | Peter | 9/10 | R1 | ✅ ACCEPT | audit_log 表 + IPC + 9 记录点，commit `5ab60a5` |
| TASK_114 | 前端审计日志 API 同步 | flash | — | — | ✅ DONE | P0 直接 commit `6ba83bf` |

---

## 已知问题

| 问题 | 优先级 | 状态 |
|------|--------|------|
| 女巫同晚互锁 | 🔴 P0 | ✅ REVISION_095/096 已完成 |
| 角色不持久 + 药水跨局残留 | 🔴 P0 | ✅ REVISION_098 已修复 |
| Night 回退报错 | 🔴 P0 | ✅ REVISION_100C 已修复 |
| 轮次历史 loading 卡死 | 🔴 P0 | ✅ REVISION_098/100 已修复 |
| Setup 角色过滤/冲突提示 | 🟡 P1 | ✅ REVISION_104 已修复 |
| Nomination 上警/离场按钮 | 🟡 P1 | ✅ REVISION_105 已修复 |
| PhaseTimeline 按钮文案 | 🟢 P2 | ✅ TASK_109 已完成 |
| CDP 自动化偶发崩溃 | 🟡 P1 | TASK_110 状态待确认（Peter 声称已归档但无文件记录）|
| TournamentView 操作列无功能按钮 | 🟡 P2 | 可迭代，非阻塞 |

## ✅ 已决策

| 事项 | 决策 | 影响 |
|------|------|------|
| Dawn 阶段回退 | **永远支持回退**（选项B） | REVISION_100 Bug-3 改为取消所有阶段回退限制 |
| 回退动作记录 | **必须记录**，供馆主统计 | 新增 TASK_103：回退日志表 + IPC |
| TEST_REPORT_107 结论 | **🟡 有条件通过** | 16 项 PENDING 拆分为 TASK_TEST_108，Bug-1/2 拆分为 TASK_109/110 |
| buddy 入职 | **✅ 接受** | 注册为 External Agent（测试员），协作关系已写入 ACTIONS.md |

---

## 里程碑

| 里程碑 | 状态 | 完成度 |
|--------|------|--------|
| M0 技术骨架 | ✅ | 100% |
| M1 开局与夜间 | ✅ | 100% |
| M2 白天流程 | ✅ | 100% |
| M3 完整闭环 | ✅ | 95% |
| M4 异常路径 | ✅ | 100% |
| M5 MVP发布 | 🟡 | 90% |

> **历史归档**: 已完成任务详见 `archive/inbox/` 与 `archive/outbox/`
