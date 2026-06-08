# TASK_113: 后端操作审计日志

**分派人**: Kimi  
**执行人**: Peter  
**日期**: 2026-06-04  
**优先级**: 🟡 P2  
**级别**: P2（标准审查）

---

## 背景

赛事版模块 `src/backend/src/modules/event/mod.rs` 预留了操作审计日志功能。当前后端缺乏对关键操作（阶段推进、投票、角色行动、玩家离场等）的审计追踪能力，不利于复盘和 Bug 排查。

## 目标

实现后端操作审计日志系统，记录所有影响游戏状态的关键操作。

## 需求

### 1. 数据模型

新增 `audit_log` 表（SQLite）：

```sql
CREATE TABLE audit_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp_ms INTEGER NOT NULL,  -- 毫秒级时间戳
    round INTEGER NOT NULL,         -- 当前轮次
    phase TEXT NOT NULL,            -- 当前阶段
    action_type TEXT NOT NULL,      -- 操作类型：NEXT_PHASE, VOTE, NIGHT_ACTION, PLAYER_LEAVE, ROLE_ASSIGN 等
    operator TEXT,                  -- 操作人（法官/系统）
    seat_number INTEGER,            -- 涉及座位号（如有）
    details TEXT                    -- JSON 详情
);
```

### 2. IPC 命令

新增 `#[tauri::command]`：
- `get_audit_log(round: Option<u8>) -> Vec<AuditLogEntry>` — 按轮次查询审计日志
- `get_audit_log_summary() -> AuditLogSummary` — 获取日志统计

数据模型必须 `#[derive(Serialize, Deserialize)]`。

### 3. 自动记录点

在以下位置自动插入审计日志（无需前端调用）：
- `next_phase` — 阶段推进
- `player_vote` — 投票
- `night_action` — 夜间行动
- `player_leave` — 玩家离场
- `assign_role` — 角色分配
- `kill_player` — 玩家死亡

### 4. 构建验证

- `cargo check` 0 errors
- `cargo test` 82+ pass（不降低现有测试基线）
- 新增单元测试覆盖审计日志的写入和查询

## 验收标准

- [ ] `audit_log` 表创建迁移
- [ ] IPC 命令实现并导出
- [ ] 至少 5 个自动记录点接入
- [ ] 新增单元测试 ≥ 3 个
- [ ] `cargo test` 全部通过
- [ ] 写 REPORT 到 `outbox/`

## 约束

- 座位号：u8，1-based
- 时间戳：毫秒级（`std::time::SystemTime`）
- 不影响现有 FSM 逻辑
- 审计日志写入失败不能阻塞主流程（静默失败 + error log）
