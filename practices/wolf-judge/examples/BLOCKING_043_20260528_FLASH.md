# BLOCKING REPORT: TASK_043 场景 A 阻塞项

**提交人**: deepseek-v4-flash
**日期**: 2026-05-28
**状态**: 等待后端 IPC 接口

---

## 前端已完成（等待联调）

| 组件 | 方案 | 状态 |
|------|------|------|
| Naive UI 全局注册 | `app.use(naive)` + `n-config-provider darkTheme` | ✅ 完成 |
| SetupView 版型选择 | `n-card` 卡片列表 + `n-button` 确认 | ✅ 完成 |
| SetupView 座位管理 | `n-input` 昵称编辑 + `n-modal` 弹窗 | ✅ 完成 |
| SeatMap 四边形布局 | CSS Grid 3-3-3-3 + `n-button`(circle) | ✅ 完成 |
| PromptBoard 话术板 | `n-card` + `n-timeline` + voice.json 数据源 | ✅ 完成 |
| `vue-tsc --noEmit` | 0 错误 | ✅ 通过 |

## 阻塞项

### 阻塞 1: GameView SETUP 阶段无法集成验牌

**原因**: `init_game_with_template` 返回的 GameState 中 `players.role` 目前不是 `null`，前端无法模拟"保密"行为。

**需要你确认**: `init_game_with_template` 的返回值是否已将 `role` 字段设为 `null`？

### 阻塞 2: `set_nickname` IPC 未就绪

**原因**: SetupView 中点击座位 → 输入昵称 → `store.setNickname()` 目前是前端本地操作。正式方案应调用后端 IPC `set_nickname`，但命令尚未注册。

**需要**: 
```rust
#[tauri::command]
pub fn set_nickname(seat: u8, nickname: String, state: State<AppState>) -> Result<(), String>
```

### 阻塞 3: `reveal_identity` IPC 未就绪

**原因**: 验牌弹窗需要调用后端获取单个玩家的角色信息。这是"保密机制"的核心——前端不能提前知道角色。

**需要**:
```rust
#[tauri::command]
pub fn reveal_identity(seat: u8, state: State<AppState>) -> Result<RevealedRole, String>
// RevealedRole { role, emoji, faction, ability }
```

---

## 前端已完成的部分

```
SetupView ── `n-button`选择版型 → `n-input`昵称 → `n-modal`弹窗
  │
  ├── SeatMap ── CSS Grid 3-3-3-3 四边形，`n-button`(circle) 座位
  │
  ├── PromptBoard ── `n-card` + `n-timeline`，voice.json 驱动
  │     └── 当前支持 SETUP + Night 话术，后续场景扩展
  │
  └── [停在这里] ── 等 set_nickname + reveal_identity + role 保密策略
        │
        └── GameView SETUP 阶段集成验牌弹窗 + 开始游戏
```

**vue-tsc**: ✅ 0 错误  
**vite build**: 未验证（待后端就绪后一起测）
