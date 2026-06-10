# TASK_036: 搭建快捷脚本体系——scripts/ 公共层 + agent.py 总入口 + 首批命令

> **Assignee**: Kimi
> **Priority**: P1
> **Decision**: DECISION_023_20260610_TPM-PAIR.md

---

## 目标

在项目根目录下新建 `scripts/` 目录，搭建完整的快捷脚本体系。Agent 只需记住 `agent.py NAME` 一个入口。

---

## 目录结构

```
scripts/
├── agent.py             # ★ 总入口
├── daily-check.py       # ★ 全量巡检：扫描 inbox/outbox/decisions 全部文件，检查命名+内容+交叉引用
├── lib/
│   ├── __init__.py
│   ├── template.py      # 解析模板 {{变量名}} → field 列表
│   ├── actions.py       # 读 ACTIONS.md → 角色/链路/权限校验
│   ├── naming.py        # 文件名生成 + 命名正则库（吸收 extras 的命名部分）
│   ├── validate.py      # 文件合规校验：内容头部字段 + 交叉引用（吸收 extras 的内容校验部分）
│   ├── registry.py      # NNN 序列管理
│   ├── patrol.py        # 巡检 inbox/outbox
│   └── redlines.py      # 红线规则读取（每次输出末尾追加）
├── new-task.py          # 创建 TASK（自动编号）
├── new-report.py        # 创建 REPORT
├── new-revision.py      # 创建 REVISION
├── new-decision.py      # 创建 DECISION（TPM）/ DECISION + PROACTIVE_REPORT（外部 Agent）
├── new-review-report.py # 创建 REVIEW_REPORT
├── validate-file.py     # 校验单个文件
├── validate-all.py      # 校验全部文件
└── README.md            # 使用说明
```

---

## 各模块说明

### `agent.py` — 总入口

```
$ python agent.py
→ 返回项目的协作框架信息

$ python agent.py KIMI
→ 返回：
  - role: External Agent
  - links: inbox/outbox 流向
  - available_commands: [new-task, new-report, ...]
  - patrol: inbox 中 KIMI 的未完成任务 + outbox 中待处理项
  - suggested: 下一步操作建议
```

### `lib/actions.py` — 角色与链路

- 读 `collaboration/ACTIONS.md`，解析协作链路表
- 校验 agent 名称是否存在：`get_role("KIMI")` → role / None
- 返回角色允许的写权限列表

### `lib/template.py` — 模板解析

- 读 `collaboration/templates/` 中的 .md 文件
- 正则提取 `{{变量名}}`
- 输出 field 列表（key / label / type / options / default）
- 支持对每字段的提取（类型、可选项等）
- 对模板头部 `> **存放位置**: ` 的提取

### `lib/naming.py` — 文件名生成

- 根据文件类型 + 当前 NNN 序列 + agent 信息 → 生成合规文件名
- 格式：`{TYPE}_{NNN}_{DATE}_{author}@{assignee}.md`
- 下一序号：读 registry 或扫描目录中最大编号+1

### `lib/registry.py` — NNN 序列管理

- 跟踪当前各类文件的最新编号
- 防止并发创建时编号冲突

### `lib/patrol.py` — 巡检

- 扫描 `collaboration/inbox/` 匹配 `TASK_*_{agent}.md` 提取未完成任务
- 扫描 `collaboration/outbox/` 提取当前 agent 相关待处理项

### `lib/validate.py` — 校验

- 文件名格式校验
- 必填字段校验
- 流向校验（与 ACTIONS.md 匹配）
- 关联 TASK 存在性校验

### `lib/redlines.py` — 红线规则

- 读 `collaboration/CHARTER.md`，找到 `## 七、红线` 章节
- 在代码块中定位 `—` 到 `！` 之间的文本，提取为红线内容
- 所有红线内容用 `！` 拼接为一个字符串
- 输出格式：`"redlines": "所有任务、报告、决策必须通过文件传递！任何 Agent 严禁执行 git 命令！只追加不覆盖..."`

### `scripts/daily-check.py` — 全量巡检

- 吸收 `extras/template-validator/validate.py` 的全部功能
- 默认扫描 `inbox/` + `outbox/` + `decisions/` 全部文件
- 三项检查：
  1. **命名校验** — 调用 `lib/naming.py` 的正则库，验证文件名是否合规
  2. **内容校验** — 调用 `lib/validate.py`，检查前 40 行是否包含期望头部字段
  3. **交叉引用** — 验证 TASK↔REPORT 等关联文件是否存在
- 输出格式：`通过: N / 错误: N / 警告: N` + 逐项详情列表
- 调用方式：
  ```
  python daily-check.py                   # 扫描全部
  python daily-check.py inbox/            # 只扫 inbox
  python daily-check.py inbox/ outbox/    # 扫指定目录
  ```

### `new-task.py` — 创建 TASK

- 自动扫描 `inbox/` 中现有 `TASK_*` 文件，取最大 NNN+1（无需用户在 JSON 中传入编号）
- 其余流程同上

### `new-decision.py` — 创建决策与行动请求

- 通过 `lib/actions` 检测调用者角色
- **TPM 角色** → 仅创建 `DECISION` 文件到 `decisions/`
- **非 TPM 角色**（外部 Agent）→ 自动依次创建：
  1. `DECISION` 文件到 `decisions/`（记录推理链）
  2. `PROACTIVE_REPORT` 文件到 `outbox/`（递交 TPM 审批）
- 模板解析、字段校验流程相同，仅输出路径和文件类型不同

---

## 约束条件

- ❌ 不依赖任何三方 Python 库
- ❌ 不改动 `collaboration/` 中的模板和规则文件
- ✅ `README.md` 全英文（社区惯例）

---

## 验收标准

- [ ] `scripts/` 目录结构完整（lib/ + agent.py + 各命令）
- [ ] `agent.py` 无参输出框架信息
- [ ] `agent.py KIMI` 输出角色、链路、命令列表、巡检结果
- [ ] `new-report.py` 无参输出模板 JSON Schema
- [ ] `new-report.py KIMI` 输出 Schema + 可用 TASK 编号
- [ ] `new-report.py KIMI '{"TASK_NNN":"042"}'` 创建文件
- [ ] 无效 agent 名称被拒绝
- [ ] 错误流向被拒绝
- [ ] 提交 REPORT_036_KIMI.md 到 outbox/
