# BLOCKING REPORT: TASK_043 Scene A Blockers

**Author**: flash
**Date**: 2026-05-28
**Status**: Waiting for backend IPC endpoints

---

## Frontend Completed (awaiting integration)

| Component | Approach | Status |
|------|------|------|
| Naive UI global registration | `app.use(naive)` + `n-config-provider darkTheme` | ✅ Complete |
| SetupView board selection | `n-card` card list + `n-button` confirm | ✅ Complete |
| SetupView seat management | `n-input` nickname edit + `n-modal` dialog | ✅ Complete |
| SeatMap quadrilateral layout | CSS Grid 3-3-3-3 + `n-button`(circle) | ✅ Complete |
| PromptBoard script panel | `n-card` + `n-timeline` + voice.json data source | ✅ Complete |
| `vue-tsc --noEmit` | 0 errors | ✅ Pass |

## Blockers

### Blocker 1: GameView SETUP phase can't integrate identity check

**Cause**: `init_game_with_template` returns a GameState where `players.role` is currently not `null`; the frontend can't simulate the "secrecy" behavior.

**Need confirmation**: Does `init_game_with_template` already set `role` to `null` in its return value?

### Blocker 2: `set_nickname` IPC not ready

**Cause**: In SetupView, clicking a seat → entering nickname → `store.setNickname()` is currently a frontend-local operation. The proper implementation should call backend IPC `set_nickname`, but the command is not yet registered.

**Needed**: 
```rust
#[tauri::command]
pub fn set_nickname(seat: u8, nickname: String, state: State<AppState>) -> Result<(), String>
```

### Blocker 3: `reveal_identity` IPC not ready

**Cause**: The identity check dialog needs to call the backend to get a single player's role info. This is the core of the "secrecy mechanism" — the frontend must not know roles in advance.

**Needed**:
```rust
#[tauri::command]
pub fn reveal_identity(seat: u8, state: State<AppState>) -> Result<RevealedRole, String>
// RevealedRole { role, emoji, faction, ability }
```

---

## Frontend Progress Summary

```
SetupView ── `n-button` select board → `n-input` nickname → `n-modal` dialog
  │
  ├── SeatMap ── CSS Grid 3-3-3-3 quadrilateral, `n-button`(circle) seats
  │
  ├── PromptBoard ── `n-card` + `n-timeline`, voice.json driven
  │     └── Currently supports SETUP + Night scripts; more phases to extend
  │
  └── [Blocked here] ── waiting for set_nickname + reveal_identity + role secrecy policy
        │
        └── GameView SETUP phase integration: identity check dialog + start game
```

**vue-tsc**: ✅ 0 errors  
**vite build**: not verified (to test after backend is ready)
