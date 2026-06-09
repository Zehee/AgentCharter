# TASK_001: 更新 README §1.2 角色定义——明确人机结对类型

> **文件名**: `TASK_001_ROLE-PAIR-CLARITY_TPM.md`
> **存放位置**: `inbox/`
> **命名约束**: 段间 `_`，段内 `-`。`NNN`=3位序号，`DESC`=英文简短描述，`ASSIGNEE`=领取者标识（大写）

**分派人**: TPM
**执行人**: TPM
**优先级**: 🟡 P1
**决策来源**: DECISION_003 / DECISION_001

---

## 目标

在 `collaboration/README.md` §1.2 和 `collaboration_en/README.md` §1.2，将三种角色的定义改为明确标注谁是人机结对、谁不是。

当前表述是"External Agent 可以是人也可以是 AI"，改为"TPM 和 External Agent 默认为人机结对综合体——背后可以是人类+AI 任意组合。Sub-Agent (Native) 为纯 AI，无对话入口。"

## 当前状态

三种角色定义在 collaboration/README.md L30-35 和 collaboration_en/README.md L30-35。Current text treats "pair" as optional.

## 详细需求

### 1. CN README §1.2

修改 `External Agent` 行和 `Sub-Agent (Native)` 行，新增注释说明人机结对适用性。

### 2. EN README §1.2

同步修改。

## 验收标准

- [ ] CN 版本明确标注 TPM 和 External Agent 为人机结对
- [ ] CN 版本明确标注 Sub-Agent 为纯 AI
- [ ] EN 版本同步
- [ ] 提交 `outbox/REPORT_001_YYYYMMDD_TPM.md`
