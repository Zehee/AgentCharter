# AgentCharter 规则压缩与分片治理分析

> **Author**: Kimi (External Agent, @kimi-pair)
> **Date**: 2026-06-09
> **Description**: 当规则体系增长时，如何在不牺牲核心哲学的前提下，通过压缩或分片降低上下文压力

---

## 一、为什么要压缩/分片？

### 当前上下文压力的量化

| 文档 | 行数 | 角色 |
|------|------|------|
| `collaboration/README.md` | 404 | 所有 Agent |
| `collaboration/TPM.md` | 430 | 仅 TPM |
| `collaboration/CHARTER.md` | 142 | 所有 Agent（初始化后移至根目录）|
| `collaboration/REGISTER.md` | 112 | 新入职 Agent |
| `collaboration/ACTIONS.md` | 50 | 所有 Agent |
| `collaboration/PROJECT.md` | ~50 | 所有 Agent |
| `context/{name}-memory.md` | ≤150 行（8KB）| Sub-Agent/Reviewer |
| **TPM 总负载** | **~1,138 行** | |
| **External Agent 总负载** | **~708 行** | |
| **Sub-Agent 总负载** | **~708 行 + 150 行 context** | |

**问题**：当项目运行到中后期，ACTIONS.md 增长、CHARTER.md 积累修订记录、dashboard.md 变长，这个负载会持续膨胀。对于本地小模型（7B-13B，8K-32K 上下文）或长项目运行中上下文被压缩后，压力会累积。

---

## 二、路径 A：压缩治理

### 2.1 核心思想

保留一份**极简核心协议**（如 50-80 行），所有 Agent 必须完整加载。详细规则按需读取。

### 2.2 可行的压缩结构

```
collaboration/
├── CORE.md              ← 新增：50 行不可压缩核心
├── README.md            ← 从 404 行压缩到 ~150 行
├── TPM.md               ← 从 430 行压缩到 ~200 行
└── details/             ← 新增：详细规范目录
    ├── lifecycle.md     # 任务生命周期完整版
    ├── review.md        # 审查流程完整版
    ├── archive.md       # 归档规则完整版
    └── subagent.md      # Sub-Agent 管理完整版
```

### 2.3 CORE.md 示例（不可压缩核心）

```markdown
# AgentCharter Core — 不可压缩

> 版本: v3.3 | 读完本文件再读角色专属文件。

## 铁律（违反 = 立即失效）

1. **没有文件 = 没有发生** — 所有任务、报告、决策必须通过文件
2. **Git 禁令** — 只有 TPM 可执行 git 命令，一刀切
3. **只追加，不覆盖** — 状态流转靠创建新文件，不修改他人文件
4. **inbox 仅 TPM 写，outbox 仅执行者写**

## 你是谁？

- TPM → 读 `TPM.md`
- External Agent → 读 `REGISTER.md` → 巡检 inbox/
- Sub-Agent → 等 TPM 内部投递，读 `context/{name}-memory.md`
- Reviewer → 读 `details/review.md`

## 紧急速查

| 操作 | 文件 | 位置 |
|------|------|------|
| 领任务 | inbox/TASK_NNN_*_{YOU}.md | TPM 写入 |
| 交报告 | outbox/REPORT_NNN_DATE_{YOU}.md | 你写入 |
| 被审查 | 等 reviews/REVIEW_REPORT | Reviewer 写入 |
| 决策 | decisions/DECISION_NNN_DATE_{PAIR}.md | 结对写入 |
```

### 2.4 压缩的利弊分析

| 维度 | 效果 | 风险 |
|------|------|------|
| **上下文消耗** | ✅ TPM 从 1,138 行 → ~300 行，External Agent → ~200 行 | — |
| **初始化速度** | ✅ Agent 更快启动工作 | — |
| **规则遗漏** | — | ❌ Agent 可能不读 `details/` 而违反详细规则 |
| **审计完整性** | — | ❌ "我只读了 CORE.md，不知道归档规则"——追溯时责任模糊 |
| **模板一致性** | — | ❌ 压缩后模板引用可能指向不存在的详细章节 |

### 2.5 框架的已有压缩尝试

AgentCharter **已经在做压缩**：

- `README.md` §十二"快速参考"就是一个压缩表（"我想… → 操作"）
- `TPM.md` §九"快捷命令"（`-work` / `-check` / `-sub` / `-upgrade`）是命令式压缩
- `collaboration/README.md` §4.2 明确建议："将高频模板结构缓存到 prompt 记忆/snippet/skill"

**但这些压缩是"建议性"的，不是"强制性分层的"**。Agent 仍然被期望读完完整文档。

---

## 三、路径 B：分片治理

### 3.1 核心思想

**不是所有人都需要知道所有事**。按角色、按场景、按会话阶段分片加载。

### 3.2 方案 B1：角色分片（横向切分）

```
collaboration/
├── README.md              # 通用框架（150 行）— 所有人必读
├── TPM/
│   ├── CORE.md            # TPM 核心（100 行）
│   ├── DISPATCH.md        # 任务分发细则
│   ├── REVIEW.md          # 审查 orchestration
│   ├── ARCHIVE.md         # 归档规则
│   └── SUBAGENT.md        # Sub-Agent 管理
├── AGENT/
│   ├── REGISTER.md        # 入职指南（压缩版）
│   ├── WORKFLOW.md        # 任务生命周期
│   └── REPORTING.md       # 报告规范
└── SHARED/
    ├── CHARTER.md
    ├── ACTIONS.md
    ├── PROJECT.md
    └── templates/
```

**效果**：
- TPM 加载：~150 + ~400 = 550 行（比当前 1,138 少一半）
- External Agent 加载：~150 + ~200 = 350 行
- Sub-Agent 加载：~150 + ~150 = 300 行

**风险**：
- ❌ TPM 做决策时需要引用 `AGENT/WORKFLOW.md` 中的规则，可能没读过
- ❌ 跨角色协作时认知基线不一致

### 3.3 方案 B2：阶段分片（纵向切分）

按 Agent 的生命周期阶段加载：

```
collaboration/
├── onboarding/
│   ├── WELCOME.md         # 50 行：你是谁，该读什么
│   ├── QUICKSTART.md      # 100 行：第一步做什么
│   └── ROLE_{X}.md        # 角色确认 + 专属规则入口
├── running/
│   ├── TASK_GUIDE.md      # 领取→编码→报告
│   ├── REVIEW_GUIDE.md    # 审查流程
│   ├── BLOCKING_GUIDE.md  # 阻塞处理
│   └── DECISION_GUIDE.md  # 决策记录
├── admin/
│   ├── TPM_GUIDE.md       # TPM 完整手册
│   ├── UPGRADE_GUIDE.md   # 框架升级
│   └── AUDIT_GUIDE.md     # 归档与审计
└── reference/
    ├── TEMPLATES_INDEX.md # 15 个模板速查
    ├── NAMING.md          # 命名规范
    └── GLOSSARY.md        # 术语表
```

**加载策略**：
- **入职阶段**：`onboarding/WELCOME.md` + `onboarding/QUICKSTART.md` + `onboarding/ROLE_{X}.md`
- **运行阶段**：按需加载 `running/*`（第一次遇到审查时读 `REVIEW_GUIDE.md`）
- **管理阶段**：仅 TPM 读 `admin/*`

**效果**：
- 入职时只加载 ~150 行
- 运行时按需加载，单次不超过 100 行
- 上下文压力分散到整个生命周期

**风险**：
- ❌ **Agent 可能不知道某个阶段存在**（"原来还有 DECISION_GUIDE？我没读过"）
- ❌ 阶段边界模糊（入职时是否需要了解审查流程？）
- ❌ 文件碎片化增加 I/O 开销

### 3.4 方案 B3：能力分片（功能切分）

按"能力模块"分片，类似技能系统：

```
collaboration/
├── core/
│   └── PROTOCOL.md        # 100 行核心协议
├── skills/
│   ├── task-management/   # 任务管理技能包
│   ├── code-review/       # 代码审查技能包
│   ├── decision-recording/# 决策记录技能包
│   ├── blocking/          # 阻塞处理技能包
│   └── proactive-report/  # 主动报告技能包
└── roles/
    ├── TPM.md
    ├── EXTERNAL.md
    └── SUBAGENT.md
```

Agent 按需"加载技能包"。框架当前已经推荐 Agent 将模板缓存到自身记忆系统——这本质上就是**技能分片**的雏形。

---

## 四、核心矛盾：完整性与简洁性的张力

### 4.1 AgentCharter 的"不可压缩部分"

以下规则如果被压缩或分片，**框架会失效**：

| 规则 | 为什么不可压缩 | 如果分片的后果 |
|------|--------------|--------------|
| **"没有文件 = 没有发生"** | 框架存在的根基 | Agent 跳过文件直接操作 |
| **Git 禁令** | 安全底线 | Agent 执行 git push 破坏仓库 |
| **inbox/outbox 写域隔离** | 并发安全核心 | 覆盖冲突、状态混乱 |
| **增量文件链** | 审计追溯基础 | 历史被篡改、责任不清 |
| **命名规范** | 文件唯一性保证 | 文件名冲突、无法检索 |

### 4.2 可压缩/分片的部分

| 规则 | 压缩方式 | 风险等级 |
|------|---------|---------|
| 任务生命周期详细说明 | 速查表 + 链接到完整版 | 🟡 低 — Agent 可边做边学 |
| 归档规则的例外条款 | 保留通用规则，例外放入 `details/` | 🟡 低 — TPM 读详细版 |
| Sub-Agent 上下文记忆维护 | 保留核心原则，详细操作放入子文档 | 🟢 极低 — 仅 TPM 关注 |
| 审查摘要流转机制 | 首次遇到时学习 | 🟡 低 — 有模板指导 |
| 框架升级流程（§十三）| 放入 `details/upgrade.md` | 🟢 极低 — 非常用功能 |
| 人机结对决策感知指南（§六）| 保留触发原则，详细示例分片 | 🟡 低 — 示例可补充 |

---

## 五、混合方案推荐：分层核心 + 按需引用

基于框架现状，最务实的演进路径是**"分层核心"**——不极端压缩，也不完全扁平：

### 5.1 三层架构

```
┌─────────────────────────────────────────┐
│  Layer 1: 绝对核心（50-80 行）           │
│  所有 Agent 必须完整加载，不可跳过        │
│  — 铁律、角色入口、紧急速查              │
├─────────────────────────────────────────┤
│  Layer 2: 角色核心（100-150 行）         │
│  按角色加载，TPM/External/Sub 各不同     │
│  — 日常操作规范、权限边界                │
├─────────────────────────────────────────┤
│  Layer 3: 详细参考（按需加载）           │
│  遇到具体场景时打开                      │
│  — 审查流程细则、归档例外、升级指南      │
└─────────────────────────────────────────┘
```

### 5.2 具体实施（以 `collaboration/README.md` 重构为例）

```markdown
# AgentCharter v3.4 — 分层协议

> **必读顺序**：Layer 1 → Layer 2（你的角色）→ Layer 3（遇到时）

---

## Layer 1: 绝对核心（不可跳过）

### 铁律
1. 没有文件 = 没有发生
2. Git 禁令 — 只有 TPM 可 git commit
3. 只追加，不覆盖
4. inbox 仅 TPM 写，outbox 仅执行者写

### 你是谁？
| 角色 | 下一步 |
|------|--------|
| TPM | 读 Layer 2-TPM，签 👑 |
| External Agent | 读 Layer 2-Agent，填 REGISTER |
| Sub-Agent | 等 TPM 投递，读 context/memory |

### 紧急速查（7 件事）
| 我想... | 文件 | 位置 |
|---------|------|------|
| 领任务 | TASK_NNN_*_{YOU} | inbox/ |
| 交报告 | REPORT_NNN_DATE_{YOU} | outbox/ |
| ... | ... | ... |

---

## Layer 2: 角色核心

[根据角色展开，当前 README.md 的 §1-§5 放这里]

---

## Layer 3: 详细参考

- [审查流程完整版](./details/review.md) — 第一次审查时阅读
- [归档规则完整版](./details/archive.md) — TPM 归档时参考
- [框架升级指南](./details/upgrade.md) — 升级时阅读
- [决策记录范例](./details/decision-examples.md) — 写 DECISION 时参考
```

### 5.3 TPM.md 的对应重构

```
TPM.md
├── Layer 1: TPM 绝对核心（50 行）
│   └── 你是谁、8 条铁律、快捷命令
├── Layer 2: TPM 日常操作（150 行）
│   └── 巡检流程、任务分发、审查 orchestration
└── Layer 3: TPM 高级参考（按需）
    ├── details/tpm-archive.md      # 归档规则
    ├── details/tpm-subagent.md     # Sub-Agent 管理
    └── details/tpm-upgrade.md      # 框架升级
```

---

## 六、对框架哲学的冲击评估

### 6.1 信任哲学是否兼容分片？

AgentCharter 的核心信念是**"Agent 会读并遵守协议"**。

分片治理对这个信念的影响：

| 影响 | 评估 |
|------|------|
| **Agent 选择不读 Layer 3** | 框架设计允许 — Layer 1+2 足够日常操作，Layer 3 是"增强" |
| **Agent 不知道 Layer 3 存在** | 风险可控 — Layer 1 的"紧急速查"链接到 Layer 3 |
| **分片导致规则矛盾** | 风险高 — 必须保证 Layer 1 是"唯一真相源"，Layer 3 是对 Layer 1 的展开 |

**结论**：分片与信任哲学**兼容**，但需要严格的分层契约——Layer 1 不可违反，Layer 2 角色专属，Layer 3 补充说明。

### 6.2 "没有文件 = 没有发生"是否会被削弱？

如果 Agent 的操作依据是"我读过的 Layer 2"，但审计时发现它没读 Layer 3 而违反了详细规则，责任归属会变模糊。

**缓解方案**：
- Layer 1 明确声明："本文件是协议的不可压缩核心。你执行的操作默认已理解全部层级的规则。"
- Layer 3 的文档顶部标注："本文件是 Layer 1 中 `[具体规则]` 的详细展开，不改变其含义。"
- 引入 `ACKNOWLEDGMENT.md`：Agent 入职时声明"我已阅读 Layer 1 和 Layer 2-{角色}，理解 Layer 3 按需补充"

但这增加了仪式感，与框架的极简精神有张力。

---

## 七、终极判断

| 方案 | 推荐度 | 理由 |
|------|--------|------|
| **维持现状（完全扁平）** | ⭐⭐⭐ | 当前 1,138 行对现代 LLM 仍可承受，但长期不可持续 |
| **极端压缩（只留 50 行）** | ⭐⭐ | 风险过高，规则遗漏会导致框架失效 |
| **角色分片（B1）** | ⭐⭐⭐⭐ | 最平衡，TPM/External/Sub 各取所需 |
| **阶段分片（B2）** | ⭐⭐⭐ | 理想但复杂，阶段边界难以划定 |
| **能力分片（B3）** | ⭐⭐⭐⭐ | 与框架现有"模板缓存"建议一致，最自然 |
| **⭐ 分层核心 + 按需引用（推荐）** | ⭐⭐⭐⭐⭐ | 保留不可压缩核心，允许按需深入，最务实 |

**分层核心方案的关键成功因素**：
1. **Layer 1 必须是真的不可压缩**——不能为了简洁牺牲安全
2. **层级间引用必须显式**——"本规则是 Layer 1 §X 的展开"
3. **Agent 记忆缓存策略不变**——"高频规则缓存到本地记忆"仍然有效
4. **版本号统一到 Layer 1**——Agent 看到 `v3.4` 就知道协议已分层

如果 AgentCharter 走向 v3.4，分层治理几乎必然发生——不是因为现在有问题，而是因为**它要为规模化做准备**。wolf-judge 的 120+ 任务已经让 ACTIONS.md 和 archive/ 开始膨胀。如果不提前分层，下一个 500+ 任务的项目会让 TPM 的上下文不堪重负。
