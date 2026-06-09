# AgentCharter v3.3.0 框架更新报告

> 来源: wolf-judge 项目（新狼官）TPM DSpro 的执行报告
> 日期: 2026-06-10
> 说明: 这是第一个完成上游 v3.2 → v3.3 升级的外部实例。展示了 TPM 如何独立扫描上游、评估差异、取舍变更、提交报告。

---

## 更新来源

上游 [Zehee/AgentCharter](https://github.com/Zehee/AgentCharter) 于 2026-06-10 发布 v3.3.0。DSpro 评估后采纳了 5 项变更。

## 新增文件（2 个）

**`collaboration/templates/DECISION_NNN_DATE_AUTHOR.md`** — 第 15 个文件模板
- 记录人机结对过程中推演、权衡、达成共识的完整推理链
- 格式：`decisions/DECISION_NNN_DATE_AUTHOR.md`
- 核心字段：`决策（一句话）` / `推理链（对话原始语句）` / `替代方案` / `最终产物（关联 TASK/TODO）`

**`docs/decision-protocol.md`** — 决策记录协议
- 8 章完整规范（动机、格式、触发条件、信息流、关联关系、归档规则、与其他文件类型的关系、设计哲学）
- 三种信息流：TPM 自己执行 / 外部 Agent 汇入 PROACTIVE_REPORT / 仅内部留档

## 修改文件（3 个）

**`collaboration/README.md`**
- 版本号：v3.2 → v3.3
- 文件模板数：14 → 15（新增 DECISION）
- 目录树新增 `decisions/`
- 文件类型速查表新增决策记录行

**`collaboration/ACTIONS.md`**
- 通道类型表新增 `decisions/DECISION` 行

**`CHARTER.md`**
- 速查表新增 "记录决策推理链 → `docs/decision-protocol.md`"

## 未采纳变更（2 项）

| 上游决策 | 否决理由 |
|---------|---------|
| 删除 `scripts/` 目录 | `file-gen.js` 是 External Agent（DSpro）不依赖 Reasonix skill 生成文件的唯一工具 |
| `AGENTS.md` → 改为 `TPM.md` | 项目根 `AGENTS.md` 是我们为 DSpro（外部 CLI 自动加载）设计的特殊场景，上游不支持该模式 |

## 文件变更统计

| 类型 | 数量 | 说明 |
|------|------|------|
| 新增 | 2 | 模板 + 协议文档 |
| 修改 | 3 | README / ACTIONS / CHARTER |
| 删除 | 0 | — |
| 暂缓 | 2 | scripts/ 保留, AGENTS.md 不动 |

## 后续

DECISION 模板和协议文档已就位，但不强制使用。当人机结对产生有多轮推理链的重要决策时，按 `decision-protocol.md` 的规则创建 `decisions/DECISION_NNN`。日常工作中用得上的时候自然会用上。
