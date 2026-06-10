# 审查范式参考

> 本文档供 TPM 决策使用。其他角色无需阅读。
> 默认范式：自循环审查。
> 当前项目范式由 TPM 在 `CHARTER.md` 中指定。

---

## 快速对比

| 维度 | TPM 直接审查 | 委派审查 | 自循环审查（默认）|
|------|-------------|---------|----------------|
| **适用团队** | 1-2 人，无专职 reviewer | 有专职 reviewer | 信任型团队 |
| **TPM 介入度** | 🔴 高（读全部代码） | 🟡 中（创建 REVIEW_TASK + 读 REVIEW_REPORT + 写 REVISION）| 🟢 低（按 P0-P3 分级抽查）|
| **审查延迟** | 低（直接）| 高（TPM 中转）| 低（reviewer ↔ coder 直接）|
| **文件流向** | REPORT → outbox / REVISION → inbox | REVIEW_TASK → inbox / REVIEW_REPORT → outbox | REVIEW_REPORT → inbox |
| **优势** | 质量最高，无信息损耗 | 分担 TPM 审阅量 | 效率最高，TPM 仅做关键决策 |
| **劣势** | TPM 消耗大，不可规模化 | 调度开销大，reviewer 报告可能需 TPM 复查 | 需要信任文化 |

---

## 范式一：TPM 直接审查

```
TPM ── TASK ──→ inbox → coder → REPORT → outbox ──→ TPM
  ↑                                                     │
  └────────────── REVISION ←──── inbox ←────────────────┘
```

**适用场景**
- 团队只有 1-2 人，没有专职 reviewer
- 代码量小，TPM 可以直接审完
- 对质量要求极高，不允许信息传递损耗

**文件角色**

| 文件 | 位置 | 写者 | 读者 |
|------|------|------|------|
| TASK | inbox/ | TPM | coder |
| REPORT | outbox/ | coder | TPM |
| REVISION | inbox/ | TPM | coder |

**流程**
1. TPM 创建 TASK → inbox/
2. coder 领取 → 编码 → 写 REPORT → outbox/
3. TPM 直接审 REPORT
4. 发现问题 → 写 REVISION → inbox/
5. coder 修复 → 写 REPORT_R1 → outbox/
6. 循环直到 TPM ACCEPT → commit → 归档

---

## 范式二：委派审查

```
TPM ── TASK ─────────→ inbox → coder → REPORT → outbox ──→ TPM
                                    ↑                         │
                                    │                    REVIEW_TASK
                                    │                         ↓
                                    │                    inbox → reviewer
                                    │                         │
                                    └──── REVIEW_REPORT ←─────┘
                                               │
                                    REVISION ←─┘ (TPM 介入时)
```

**适用场景**
- 有专职 reviewer，但 reviewer 需要 TPM 显式委派
- TPM 希望控制审查节奏和范围
- reviewer 不熟悉项目，需要 TPM 指定审查重点

**文件角色**

| 文件 | 位置 | 写者 | 读者 |
|------|------|------|------|
| TASK | inbox/ | TPM | coder |
| REPORT | outbox/ | coder | TPM + reviewer |
| REVIEW_TASK | inbox/ | TPM | reviewer |
| REVIEW_REPORT | outbox/ | reviewer | TPM |
| REVISION | inbox/ | TPM | coder |

**流程**
1. TPM 创建 TASK → inbox/
2. coder 领取 → 编码 → 写 REPORT → outbox/
3. TPM 读 REPORT → 创建 REVIEW_TASK → inbox/
4. reviewer 领取 REVIEW_TASK → 读 REPORT → 写 REVIEW_REPORT → outbox/
5. TPM 读 REVIEW_REPORT
6. 需要修复 → TPM 写 REVISION → inbox/
7. coder 修复 → 写 REPORT_R1 → outbox/
8. 循环直到 TPM ACCEPT → commit → 归档

---

## 范式三：自循环审查（默认）

```
                                          自循环
TPM ── TASK(reviewer+级别) ──→ inbox → coder → REPORT → outbox
                               ↑                         │
                               │                    reviewer 读
                               │                         │
                               │                    REVIEW_REPORT
                               │                         │
                               └──── coder → REPORT_R1 ──┘ (loop until ACCEPT)
                                                         │
                                          TPM 按 P0-P3 决定介入深度
```

**适用场景**
- 信任型团队，reviewer 和 coder 可以自组织
- TPM 需要减负，只做关键决策
- 项目规模大，TPM 无法审完所有代码

**文件角色**

| 文件 | 位置 | 写者 | 读者 |
|------|------|------|------|
| TASK | inbox/ | TPM | coder + reviewer |
| REPORT | outbox/ | coder | reviewer |
| REVIEW_REPORT | inbox/ | reviewer | coder + TPM |

**流程**
1. TPM 创建 TASK（含 reviewer 和 P0-P3 级别）→ inbox/
2. coder 领取 → 编码 → 写 REPORT → outbox/
3. reviewer 主动巡检 outbox/ → 读 REPORT → 写 REVIEW_REPORT → inbox/
4. coder 读 REVIEW_REPORT → 修复 → 写 REPORT_R1 → outbox/
5. reviewer 读 REPORT_R1 → 写 REVIEW_REPORT_R1 → inbox/
6. 循环直到 reviewer 在 REVIEW_REPORT 中写 "✅ ACCEPT"
7. TPM 按 P0-P3 分级决定介入深度：
   - P0：直接 commit
   - P1：审摘要
   - P2/P3：审源码
8. TPM 决策 → commit → 归档

**关键规则**
- reviewer 和 coder 的自循环**不经过 TPM 中转**
- TPM 只在循环结束时按分级介入
- 如果 reviewer 发现重大问题，可以在 REVIEW_REPORT 中标记 🔴，TPM 优先审阅
