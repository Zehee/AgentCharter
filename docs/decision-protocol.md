# 决策记录协议 v1.0

> 可选规范。基于文件的人机结对决策记录机制，与 AgentCharter v3.2 框架核心兼容。

---

## 一、动机

AgentCharter 的 `PROACTIVE_REPORT` 是一个从结对流向 TPM 的单向交接——它记录了决策的**产物**（"建议 X"），但不记录决策的**过程**（"为什么建议 X"）。

结对内部人机通过对话推敲、权衡、达成共识的推理链条，在 `PROACTIVE_REPORT` 归档后全部丢失。这与人机结对作为"一等公民"的设计定位形成矛盾。

`DECISION` 文件类型填补了这个空缺。

---

## 二、DECISION 文件格式

**文件名**: `DECISION_NNN_DATE_AUTHOR.md`
- `NNN`: 顺序编号（与 TASK 编号独立）
- `DATE`: 决策日期 `YYYYMMDD`
- `AUTHOR`: 结对标识（大写），如 `BACKEND-PAIR`、`TPM-PAIR`

**存放位置**: `decisions/`

### 模板结构

```markdown
# DECISION_NNN: 决策标题

**结对**: [结对标识]
**时间**: YYYY-MM-DD HH:MM
**关联主动报告**: PROACTIVE_REPORT_NNN（可选）

## 决策
（一句话：决定做什么。）

## 推理链
（对话中的原始语句，一字不改。）

- **[人类]**: "原始语句…"
- **[AI]**: "原始语句…"

## 替代方案
1. 方案 A → 否决理由
2. 方案 B → 否决理由

## 最终产物
| 类型 | 编号 | 说明 |
|------|------|------|
| TASK / TODO | NNN | 从本决策创建的任务或排期事项 |
```

---

## 三、触发条件

DECISION 文件在两种情况下被创建：

### 3.1 多轮推理（产生 DECISION）

人类与 AI 在对话中反复推敲，有明显的推理链。AI 在人类确认后提取 DECISION 文件。

**示例信号**：人类说"好的，就这样""同意，按这个方案""记一下我们的决定"。

### 3.2 一句话决策（不产生 DECISION）

决策没有多轮推理过程。直接写 PROACTIVE_REPORT。

**示例场景**：人类说"这 Notice 写得很好，写成主动报告，结束。"

---

## 四、信息流

### 4.1 TPM 的 DECISION

```
人机讨论 → AI 提取 DECISION → TPM 自己执行 → TASK / TODO
```

TPM 自己做的决策直接转化为行动，不需要 PROACTIVE_REPORT 中转。

### 4.2 外部 Agent 的 DECISION

```
人机讨论 → AI 提取 DECISION → 汇入 PROACTIVE_REPORT → TPM 批注 → TASK / TODO
```

需要 TPM 行动就必须有 PROACTIVE_REPORT。DECISION 是证据，PROACTIVE_REPORT 是行动请求。

### 4.3 仅内部有效的 DECISION

```
人机讨论 → AI 提取 DECISION → 归档即可
```

不需要 TPM 行动，仅在结对内部留档。

---

## 五、关联关系

DECISION 与 AgentCharter 其他文件类型的关联：

| 文件类型 | 引用字段 | 方向 |
|---------|---------|------|
| DECISION | `关联主动报告` | DECISION → PROACTIVE_REPORT |
| DECISION | `最终产物` | DECISION → TASK / TODO |
| TASK | `决策来源` | TASK ← DECISION / PROACTIVE_REPORT |
| PROACTIVE_REPORT | `关联决策` | PROACTIVE_REPORT ← DECISION |
| TODO | `来源类型: 决策` | TODO ← DECISION |

---

## 六、归档规则

DECISION 自身不单独归档。当 `最终产物` 字段列出的所有 TASK 和 TODO 完成后，DECISION 移入 `archive/decisions/`。

Proactive Report 在 TPM 批注后按"阅后即焚"规则归档（可早于 DECISION 归档），但其引用的 DECISION 不受影响。

---

## 七、与其他文件类型的关系

### 与 PROACTIVE_REPORT 的关系

| 场景 | 产生 DECISION | 产生 PROACTIVE_REPORT |
|------|-------------|---------------------|
| 一句话决策，需要 TPM 行动 | ❌ | ✅ |
| 多轮推理，需要 TPM 行动 | ✅ → 汇入 | ✅（关联一组 DECISION） |
| 多轮推理，仅内部留档 | ✅ | ❌ |
| 没有决策，例行工作 | ❌ | ❌ |

### 与 TASK 的关系

DECISION 的 `最终产物` 表格记录从本决策创建的所有 TASK。TASK 的 `决策来源` 字段反向引用。形成可追溯的双向链路。

---

## 八、设计哲学

- **DECISION 是只读证据**：一旦写入，不可篡改。TPM 加工时读取它，但不修改它。
- **DECISION 不取代任何现有文件类型**：它是增量，不是替代。PROACTIVE_REPORT 继续承载交接职责。
- **DECISION 可选**：没有推理过程的简单决策不需要 DECISION。框架最小值是 15 个模板；实际使用时从 TASK、REPORT、REVIEW_REPORT、DECISION 开始。
- **人机结对 = 同一套协议**：TPM 和 External Agent 使用完全相同的 DECISION 格式。区别只在信息流（自己执行 vs 需要 TPM 行动）。
