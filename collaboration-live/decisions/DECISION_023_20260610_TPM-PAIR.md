# DECISION_023: 快捷工具脚本体系

**结对**: @tpm-pair (DSpro + Zehee)
**时间**: 2026-06-10
**状态**: ✅ 正式

---

## 决策

1. **语言选型：Python 标准库** — 零三方依赖，健壮性好于 bash，与已有 `extras/` 一致
2. **脚本架构：分层设计** — `scripts/lib/` 公共层 + 按功能拆分的独立命令
3. **模板感知** — 统一占位符为 `{{变量名}}`，脚本自动解析模板结构，不硬编码字段映射
4. **链路感知** — 脚本读取 `ACTIONS.md`，自动校验文件流向，拒绝错误路由
5. **可组合** — 每个脚本可独立运行，也可作为模块被其他脚本调用
6. **总入口 `agent.py`** — Agent 只需记住这一个脚本。无参输出角色、链路、可用命令、巡检结果
7. **调用协议** — `agent.py NAME` 三态返回值：
   - 无参：输出 JSON Schema（查看模板）
   - `NAME` 仅名字：输出角色信息 + 可用命令列表 + inbox/outbox 巡检结果
   - `NAME '{"key":"val"}'` 名字 + JSON：执行创建文件
8. **Agent 名称为必传校验参数** — 从 `ACTIONS.md` 实时读取，不在脚本中硬编码。无效名称直接拒绝
9. **上下文感知** — `new-report.py NAME` 仅传名字时，自动扫描 inbox 列出该 Agent 的未完成任务编号作为可选值
10. **`new-task.py` 自动编号** — 扫描现有 `inbox/TASK_*` 文件，自动生成下一个 NNN，不要求用户在 JSON 中传入
11. **`new-decision.py` 角色分流** — TPM 调用时创建 `DECISION` 文件；非 TPM 调用时自动创建 `PROACTIVE_REPORT`（遵循"只有 TPM 人机结对可写 DECISION"的规则）
12. **已有 `extras/` 保持不动** — `scripts/` 是新入口
11. **`scripts/` 与 `collaboration/` 并列** — 放项目根目录，不属于 `collaboration/` 框架核心

---

## 推理链

**Zehee**: 提出在现有工具基础上增加便捷工具。脚本不依赖三方库，减少 Agent token 开销、减负规则层、减少犯错机会、增加合规校验。

**DSpro**: 补充脚本粒度建议——每脚本只做一件事，自解释命名；占位符统一为 `{{变量名}}`；脚本读取 ACTIONS.md 做路由感知。

**Zehee**: 进一步提出脚本应有解析器——无参空跑时自动解析模板占位符，输出 JSON。脚本应能互相关联调用。

**DSpro**: 建议用 Python 标准库替代纯 bash，因为需要解析 Markdown 表、校验规则、模块间调用。

**Zehee**: "那我们就用 Python，做都做了，就干脆做的强壮一点。"

**DSpro**: 进一步细化架构——总入口 `agent.py`、Agent 名字从 ACTIONS.md 获取、无参返回 JSON Schema、上下文感知扫描 inbox 任务编号。

**Zehee**: "这样再也不用担心他们忘东西了，因为只需要记住这个脚本入口，这个东西时时提醒他们。"

### Round 2: 最终校正

- **Zehee**: "decision 创建如果 agent 不是 tpm 会关联创建主动报告"
  - 结论：`new-decision.py` 检测调用者角色——TPM 创建 `DECISION`，非 TPM 自动转为 `PROACTIVE_REPORT`，遵循"只有 TPM 人机结对可写 DECISION"的框架规则

- **Zehee**: "task 创建应该检测编号自动生成"
  - 结论：`new-task.py` 扫描 `inbox/` 中现有 `TASK_*` 文件，自动取最大 NNN+1，不要求用户在 JSON 中传入编号

---

## 架构

```
scripts/
├── agent.py             # ★ 总入口。Agent 只需记住这一个脚本
├── lib/
│   ├── __init__.py
│   ├── template.py      # 解析模板 {{变量名}} → field 列表
│   ├── actions.py       # 读 ACTIONS.md → 角色/链路/权限校验
│   ├── naming.py        # 文件名生成（NNN 自增 + _author@assignee）
│   ├── validate.py      # 文件合规校验
│   ├── registry.py      # 当前 NNN 序列管理（防冲突）
│   └── patrol.py        # 巡检 inbox/outbox → 未完成任务列表
├── new-task.py          # 创建 TASK
├── new-report.py        # 创建 REPORT
├── new-revision.py      # 创建 REVISION
├── new-decision.py      # 创建 DECISION
├── new-review-report.py # 创建 REVIEW_REPORT
├── validate-file.py     # 校验单个文件
├── validate-all.py      # 校验全部文件
└── README.md            # 使用说明
```

**Agent 工作流程**（所有 Agent 共用）：

```
# 第 1 步：启动时跑一次总入口
$ python agent.py KIMI
→ 返回：你的角色、协作链路、可用命令、当前任务列表

# 第 2 步：选一个命令执行
$ python new-report.py KIMI
→ 返回：无参 → 模板解析结果 + 你的未完成任务编号

$ python new-report.py KIMI '{"TASK_NNN":"042","summary":"登录功能"}'
→ 返回：✅ 文件已创建 + 路径 + 自检结果
```

**无参调用流程**：
```
agent.py → 输出角色/链路/可用命令
new-report.py KIMI → 解析模板 → 扫描 inbox 列未完成任务 → 输出 JSON Schema
```

**有参调用流程**：
```
new-report.py KIMI '{"TASK_NNN":"042","AUTHOR":"KIMI","summary":"登录功能"}'
  → lib/actions.py 读 ACTIONS.md，校验 KIMI 身份 ✅
  → lib/template.py 解析模板
  → lib/actions.py 校验流向：REPORT → KIMI@TPM ✅
  → lib/naming.py 生成文件名 REPORT_042_20260610_KIMI@TPM.md
  → lib/validate.py 校验：必填字段 ✅ / 命名 ✅ / TASK 042 存在 ✅
  → 写入 outbox/REPORT_042_20260610_KIMI@TPM.md
  → 输出确认信息
```

---

## 替代方案

1. **纯 bash 脚本** → 解析 Markdown 表吃力，跨平台兼容差，模块化困难。否决
2. **单一大 CLI** → 维护成本高，学习曲线陡。否决
3. ✅ **每个脚本独立 + lib/ 公共层** → 每个脚本聚焦一件事，lib/ 保证一致性。采纳

---

## 最终产物

| 类型 | 编号 | 说明 |
|------|------|------|
| TASK | 036 | 搭建 scripts/lib/ 公共层 + 首批命令 |
