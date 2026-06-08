# TASK_113: Backend Audit Log

**Dispatcher**: Kimi  
**Executor**: Peter  
**Date**: 2026-06-04  
**Priority**: 🟡 P2  
**Level**: P2 (standard review)

---

## Background

The event module `src/backend/src/modules/event/mod.rs` has a placeholder for audit logging. The backend currently lacks audit trail capability for critical operations (phase transitions, votes, role actions, player departures), making post-game review and bug investigation difficult.

## Goal

Implement a backend audit log system that records all critical game-state-changing operations.

## Requirements

### 1. Data Model

New `audit_log` table (SQLite):

```sql
CREATE TABLE audit_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp_ms INTEGER NOT NULL,  -- millisecond timestamp
    round INTEGER NOT NULL,         -- current round
    phase TEXT NOT NULL,            -- current phase
    action_type TEXT NOT NULL,      -- type: NEXT_PHASE, VOTE, NIGHT_ACTION, PLAYER_LEAVE, ROLE_ASSIGN, etc.
    operator TEXT,                  -- operator (judge/system)
    seat_number INTEGER,            -- affected seat (if any)
    details TEXT                    -- JSON details
);
```

### 2. IPC Commands

New `#[tauri::command]`:
- `get_audit_log(round: Option<u8>) -> Vec<AuditLogEntry>` — query audit log by round
- `get_audit_log_summary() -> AuditLogSummary` — get log statistics

Data models must derive `#[derive(Serialize, Deserialize)]`.

### 3. Auto-recording Points

Automatically insert audit log entries at the following points (no frontend call needed):
- `next_phase` — phase transition
- `player_vote` — vote
- `night_action` — night action
- `player_leave` — player departure
- `assign_role` — role assignment
- `kill_player` — player death

### 4. Build Verification

- `cargo check` 0 errors
- `cargo test` 82+ pass (no baseline degradation)
- New unit tests covering audit log write and query

## Acceptance Criteria

- [ ] `audit_log` table migration
- [ ] IPC commands implemented and exported
- [ ] At least 5 auto-recording points wired up
- [ ] ≥3 new unit tests
- [ ] `cargo test` all pass
- [ ] Submit REPORT to `outbox/`

## Constraints

- Seat number: u8, 1-based
- Timestamp: millisecond (`std::time::SystemTime`)
- Must not affect existing FSM logic
- Audit log write failure must not block main flow (silent failure + error log)
