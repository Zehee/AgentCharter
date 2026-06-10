# TASK_033: collaboration/ 解耦——修正所有外部路径引用

> **Assignee**: TPM (自我分派)
> **Priority**: P1
> **Decision**: DECISION_020_20260610_TPM-PAIR.md

---

## 目标

`collaboration/` 不再侵入项目，CHARTER.md 不再搬家到项目根目录。修正所有指向项目根目录和外部目录的路径引用，改为 `collaboration/` 内部引用或纯文字说明。

---

## 文件与改动

### 1. `collaboration/CHARTER.md` — 2 处

去掉模板中的搬家描述：

**行 3**：
```
> 此文件是模板。由 TPM 在初始化时填写，完成后移至项目根目录（`../CHARTER.md`）。
```
→
```
> 此文件是模板。由 TPM 在初始化时填写，完成后作为项目级压缩规则，与 `README.md` 等框架规则并列。
```

**行 7**：
```
> 此文件由 TPM 在初始化时填写，完成后**移至项目根目录**（`../CHARTER.md`），成为所有 Agent 共享的最高规则。
```
→
```
> 此文件由 TPM 在初始化时填写，完成后成为所有 Agent 共享的最高规则。
```

### 2. `collaboration/PROJECT.md` — 1 处

去掉 practices 路径硬编码：

**行 5**：
```
> 配置示例见 `../practices/` 目录（如果通过 AgentCharter 仓库获取框架）。
```
→
```
> 配置示例可在 AgentCharter 仓库的 `practices/` 目录中查看。
```

### 3. `collaboration/README.md` — 3 处

**行 77（目录树注释）**：
```
│   ├── CHARTER.md               # 协作宪章模板 → TPM 移至项目根目录
```
→
```
│   ├── CHARTER.md               # 协作宪章模板（填好后留在 collaboration/ 中）
```

**行 156（P0-P3 注释）**：
```
> 具体级别数量和判定标准由你的项目在 `../CHARTER.md` 中定义。
```
→
```
> 具体级别数量和判定标准由你的项目在 `CHARTER.md` 中定义。
```

**行 412（已改，确认锁定）**：
`可在 AgentCharter 仓库的 practices/wolf-judge/examples/ 中查看` — 已改为纯文字，确认不再有链接。

### 4. `collaboration/TPM.md` — 3 处

**行 23-25（初始化步骤）**：
删除步骤 5（整行删除）：
```
5. **将 `CHARTER.md` 移至项目根目录**（`../CHARTER.md`）
```
同时调整后续步骤编号（6→5）。

**行 205（审查分级注释）**：
```
> 📎 以下审查分级为参考模式，具体分级标准由项目在 `../CHARTER.md` 中定义。
```
→
```
> 📎 以下审查分级为参考模式，具体分级标准由项目在 `CHARTER.md` 中定义。
```

**行 419（协作框架引用表）**：
```
| 协作宪章（最高规则） | `CHARTER.md`（初始化后移至项目根目录）|
```
→
```
| 协作宪章（最高规则） | `CHARTER.md` |
```

### 5. 外层 `README.md`（GitHub 首页英文版）— 4 处

**行 27**：
```
fills `PROJECT.md` + `CHARTER.md`, and moves the charter to your project root.
```
→
```
fills `PROJECT.md` + `CHARTER.md`. **That's it.**
```

**行 36**：
```
4. **Moves `CHARTER.md` to project root** — now every Agent (including humans) can read the supreme rules
```
→
```
4. **Reads `TPM.md`** — learns its full authority: dispatch tasks, drive reviews, own Git, update dashboard
```
（原第 5 步提前，删除搬家步）

**行 189（结构树）**：
```
│   ├── CHARTER.md               # Charter template → moved to root by TPM
```
→
```
│   ├── CHARTER.md               # Charter template (stays inside collaboration/)
```

**行 213（项目结构图）**：
```
├── CHARTER.md              # ← Global charter (moved by TPM)
```
→
```
（删除这一行，CHARTER.md 在 collaboration/ 内部已列出）
```

### 6. 外层 `README_CN.md`（GitHub 首页中文版）— 4 处

**行 27**：
```
填写 `PROJECT.md` + `CHARTER.md`、把宪章移至项目根目录。
```
→
```
填写 `PROJECT.md` + `CHARTER.md`。
```

**行 36**：
```
4. **把 `CHARTER.md` 移到项目根目录** — 所有 Agent（包括人类）都能读到最高规则
```
→
```
4. **读 `TPM.md`** — 了解完整权限：分派任务、驱动审查、独掌 Git、更新看板
```

**行 189（结构树）**：
```
│   ├── CHARTER.md               # 协作宪章模板 → TPM 移至项目根目录
```
→
```
│   ├── CHARTER.md               # 协作宪章模板（留在 collaboration/ 中）
```

**行 213（项目结构图）**：
```
├── CHARTER.md              # ← 全局宪章（TPM 移出）
```
→
```
（删除这一行，CHARTER.md 在 collaboration/ 内部已列出）
```

### 7. `collaboration_en/` — 同步

同步 `collaboration_en/CHARTER.md`、`collaboration_en/README.md`、`collaboration_en/TPM.md` 对应的 8 处英文改动（逻辑与中文版完全一致，无需逐条列出）。

---

## 约束条件

- ❌ 不修改文件结构
- ❌ 不修改框架规则内容
- ✅ 只修正路径引用和搬家描述

---

## 验收标准

- [ ] CHARTER.md 不再提及"移至项目根目录"
- [ ] TPM.md 初始化步骤不再包含"将 CHARTER.md 移至项目根目录"
- [ ] 所有 `../CHARTER.md` 已改为 `CHARTER.md`
- [ ] PROJECT.md 的 practices 路径改为纯文字
- [ ] 外层 README.md 和 README_CN.md 的 Quick Start、结构树、项目结构图已修正
- [ ] collaboration_en/ 已同步
- [ ] 提交 REPORT_033_KIMI.md 到 outbox/
