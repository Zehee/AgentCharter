# DECISION_021: 审查流程重构与目录结构优化

**结对**: @tpm-pair (DSpro + Zehee) / @kimi-pair (Kimi + Zehee)
**时间**: 2026-06-10
**状态**: ✅ 正式 — 经 TPM 审阅确认，待执行

---

## 决策

1. **删除 `reviews/` 目录** — 冗余。审查报告移至 `inbox/`
2. **删除 `archive/reviews/` 目录** — 随 `reviews/` 一并删除
3. **REVIEW_REPORT 模板路径改为 `inbox/`** — reviewer 独占写，作为前置审查输出
4. **REVIEW_TASK 模板保留但标注为"调度审查可选"** — 三种范式共用，不强制
5. **REVISION 保持 TPM 独占** — TPM 深度介入时写的返工任务，与 reviewer 的 REVIEW_REPORT 区分
6. **inbox 写权限精确扩展** — TPM 独占 TASK/NOTICE/REPLY/REVISION/REVIEW_TASK，reviewer 独占 REVIEW_REPORT。coder 不能写任何 inbox 文件
7. **引入三种审查范式** — 以团队结构命名，不暗示优劣：
   - **TPM 直接审查**：1-2 人，无专职 reviewer，TPM 读全部代码
   - **调度审查**：有专职 reviewer，需 TPM 中转（REVIEW_TASK + REVIEW_REPORT）
   - **自循环审查**：信任型团队，reviewer-coder 自循环（推荐）
8. **命名规范保持现状** — 单侧后缀（`_AUTHOR` / `_ASSIGNEE`）在单协作空间内足够。跨空间通信时建议增加接收者标识
9. **collaboration 嵌套预留** — 子协作空间物理嵌套在父协作空间内部，每级部门负责人成为自己部门的 TPM。作为架构能力写入 README，不立即实现
10. **多级汇报线的两种逻辑独立处理** — 
    - 长状态机问题 → 用自循环模式解决（reviewer 直接写 REVISION/REVIEW_REPORT）
    - 管理结构多级问题 → 用 collaboration 嵌套解决（每组一个 TPM）

---

## 推理链

### Round 1: Zehee 发起目录结构优化

- **Zehee**: "我打算对目录结构进行优化，reviews 没有存在的必要。当时的引入是因为项目中有一个 native sub-agent 专门用来 review 代码，需要 tpm 读到任务完成的 report 后，为其创建 review_task，这个 sub-agent 不能直接写 inbox（当时定义 inbox 为 tpm 独占写）所以创建了 reviews 目录让 sub-agent 存放 review_report。后来我发现 report 本身就等于 review_task，所以 review_task 也是多余的，而且以前 tpm 直接 review 代码的时候并不是写 review_report 而是写 REVISION，所以 revision 也是和 review_report 有重叠，这二者我们可以保留一个即可。"

- **Zehee 提议**: 
  - 改进 inbox 的定义：不再是 TPM 独占，而是"执行者领取任务的地方"
  - 任务可以是 task，可以是 review_report
  - 把 report 更名为 task_report
  - 供 TPM 或者 reviewer 触发 review 任务
  - 去掉 reviews 文件夹

### Round 2: Kimi 首轮分析

- **Kimi**: 分析了 `reviews/` 冗余的验证结果（`collaboration/reviews/` 和 `collaboration-live/reviews/` 均为空，只有 `.gitkeep`）
- **Kimi**: 认同 REVISION 和 review_report 重叠，审查应纳入标准任务生命周期
- **Kimi**: 但指出"开放 inbox 给 reviewer"有风险：
  > "多角色同时写 inbox 导致文件命名冲突、任务优先级失控、审计链断裂、协调者模式崩塌。"
- **Kimi 建议**: 维持 inbox TPM 独占，REVIEW 放 `outbox/`，画出 outbox 自循环映射图
- **Kimi**: 提出 REVIEW ≠ PROACTIVE_REPORT（受众不同），REVIEW 是 reviewer 给 coder 的直接反馈

### Round 3: DSpro 校正

- **DSpro**: "方向清晰，不做过度分析。"
- **DSpro 认同**: `reviews/` 冗余、REVISION 和 review_report 重叠、审查纳入标准生命周期
- **DSpro 不完全认同 Kimi**: "如果 reviewer 写 REVIEW 到 outbox，TPM 读完后还要再创建 REVISION 到 inbox，那 REVIEW 本质上就是一个 PROACTIVE_REPORT。现有机制已经覆盖了——reviewer 发现问题，写 PROACTIVE_REPORT 到 outbox，TPM 读后创建 TASK/REVISION。不需要新增一个 REVIEW 文件类型。"
- **DSpro 建议路径**:
  ```diff
  - 去掉 reviews/ 目录
  - 去掉 review_task 模板
  + 审查请求走 PROACTIVE_REPORT（已存在，无需新增）
  + REVISION 作为审查返工任务（已存在，无需改动）
  - 不改 outbox 结构
  - 不改 inbox 写权限
  ```
- **DSpro 关于 inbox 权限**:
  > "这不是'对错'问题，而是'框架默认值 vs 实例自定义'的问题。框架的默认值是 TPM 独占 inbox——因为 wolf-judge 的 5 人团队需要协调者。但你的思路（inbox 是'领取任务的地方'，reviewer 也可以写 TASK/REVISION）在小型团队或信任型团队中完全合理。"
  > "改进方向应该是：在 README.md 中标注'inbox 默认 TPM 独占，可根据团队结构调整'，而不是把这条写死。"

- **DSpro 最小步改动范围**:
  | # | 改动 | 文件 |
  |---|------|------|
  | 1 | 删除 `collaboration/reviews/` 目录 | 文件系统 |
  | 2 | 删除 `collaboration/templates/REVIEW_TASK_NNN.md` | 文件系统 |
  | 3 | README.md 去掉所有 `reviews/` 目录引用 | `README.md` + EN |
  | 4 | TPM.md 去掉所有 `reviews/` 引用 | `TPM.md` + EN |
  | 5 | README.md 标注"inbox 默认 TPM 独占，可自定义" | `README.md` |

### Round 4: Zehee 分享三版审查流程迭代

- **Zehee**: "这是我还没有想好的点，我们是否只提供一种最佳实践，还是给用户提供这三种范式..."

- **第一版（TPM 全包）**:
  1. TPM 创建 task → inbox
  2. 执行者完成任务创建 report → outbox
  3. TPM 阅读 report 创建 revision → inbox（loop R1 R2）
  > "tpm 审阅大量代码开销大，但质量有保障"

- **第二版（调度审查）**:
  1. TPM 创建 task → inbox
  2. 执行者完成任务创建 report → outbox
  3. TPM 阅读 report 创建 review_task → inbox
  4. reviewer 读取 review_task 后写 review_report → reviews
  5. TPM 阅读 review_report 写 revision → inbox（loop）
  > "tpm 省去了 review 大量代码的负担，但是多了一层报告文件的读写和 review_task 的创建增加了调度开销，在 review_report 有问题的时候还会额外检查代码"

- **第三版（自循环分级）**:
  1. TPM 创建 task（对任务难度进行分级）→ inbox
  2. 执行者完成任务创建 report → outbox
  3. reviewer 直接读取 report 执行 review 后输出 review_report（附带摘要）→ reviews
  4. 执行者读取 review_report 修复写 report R1（摘要追加流转）→ outbox（loop）
  5. TPM 阅读 accept 状态 review_report（根据任务分级 P0 P1 P2 P3 决定直接 commit / 审阅摘要 / 审阅源码）
  > "TPM 让 reviewer 和 coder 进行自循环碰撞，根据任务分级决定审阅层次，减轻了负担。"

### Round 5: Kimi 重新分析（第三版映射）

- **Kimi**: 指出第三版在当前框架下的映射——自循环不需要 inbox，只需要 outbox:
  ```
  TPM 分级创建 TASK → inbox
    ↓
  执行者完成 → REPORT → outbox
    ↓
  reviewer 读 REPORT → REVIEW → outbox   ← 改到这里
    ↓
  执行者读 REVIEW → 修复 → REPORT_R1 → outbox
    ↓
  reviewer 读 REPORT_R1 → REVIEW_R1 → outbox
    ↓
  reviewer 标记 ACCEPT → TPM 看到 → 按 P0/P1/P2/P3 决定 commit / 审摘要 / 审源码
  ```
- **Kimi**: 强调 REVIEW ≠ PROACTIVE_REPORT——受众不同：PROACTIVE_REPORT 给 TPM，REVIEW 给 coder + TPM

### Round 6: Zehee 提出 inbox 开放给 reviewer（核心洞察）

- **Zehee**: "现在我之所以会考虑开放 inbox，是因为如果一个自循环是在同一个文件夹完成的（比如 outbox）那么 coder 和 reviewer 任务的进和出就没有分开，如果开放 inbox 给 reviewer，那么对于 coder 任务的进来自 inbox，出 outbox，对于 tpm 和 review 是相反的。"

- **Zehee 的核心诉求**: 目录分离的本质是角色职责的物理隔离——每个角色应该有明确的"进"和"出"目录。

### Round 7: Kimi 分析 inbox 开放可行性

- **Kimi**: 检查 REVISION 模板，发现 REVISION 的存放位置就是 `inbox/`:
  ```markdown
  > **存放位置**: `inbox/`
  > **分派人**: [TPM 标识]
  > **执行人**: [External/Native 标识]
  ```
- **Kimi**: "REVISION 的存放位置就是 inbox/。它**已经是**审查返工任务。"
- **Kimi 画出对称循环图**:
  ```
        TPM / reviewer
    outbox ←────── inbox
   (读 REPORT)    (写 TASK/REVISION)
       ↑              ↓
    coder ──────────────
   (读 inbox)     (写 outbox)
  ```
- **Kimi**: 分析命名冲突问题——`DATE` + `AUTHOR` 的组合保证唯一性，即使 TPM 和 reviewer 同一天针对同一个 REPORT 写 REVISION，文件名也不会冲突。
- **Kimi 建议**: 
  > "支持统一的方向，因为复杂项目确实需要表达通信双方。但不建议现在一次性改所有模板，因为改动面大，且当前简单项目不需要。建议以审查流程重构为契机，为 REVIEW_REPORT 引入双后缀作为试点。"

### Round 8: DSpro 确认精确边界

- **DSpro**: "方向清晰，不做过度分析。我确认几点："
- **DSpro 确认边界**:
  > "**边界非常精确**——不是'放开 inbox'，是'REVISION 的写权限从 TPM 扩展到 reviewer'。"
  - ✅ reviewer 写 `REVISION_NNN_DATE_reviewer.md` → inbox
  - ❌ reviewer 不能写 TASK、NOTICE、REPLY
  - ❌ coder 不能写任何 inbox
  > "框架只有一个目录少了一个角色不对称，结构更干净了。"

- **DSpro 提出两个细节问题**:
  1. "reviewer 如何知道自己该写 REVISION？是 reviewer 主动去读 outbox 的 REPORT，还是 TPM 发 NOTICE 通知？如果是前者，reviewer 需要有一个'巡检 outbox'的行为定义。"
  2. "REVIEW_REPORT 模板还需要保留吗？如果 reviewer 直接写 REVISION 到 inbox，那 REVIEW_REPORT（放 outbox 的版本）就变成了 REVISION 的同体异名——本质上是一样的内容，只是放的位置不同。是否需要把 REVIEW_REPORT 模板和 REVISION 模板合并？"

### Round 9: Zehee 提出保留 REVIEW_REPORT 并开放三种范式

- **Zehee**: "所以这是我还没有想好的点，我们是否只提供一种最佳实践，还是给用户提供这三种范式，并注明适用的场景和缺陷？"

- **Zehee 提出保留策略**:
  > "如果保持最大兼容，那我们还是可以去掉 reviews 目录但保留 review_task 模板，允许 reviewer 写 review_report（这个模板内容比 revision 要丰富的多）到 inbox（限定类型），coder 可以根据 review_report 来修复代码。"
  > "我们可以推定，如果引入了三方 reviewer 那么他将是 tpm 的前置审查者，为了减轻 tpm 工作量的，如果 TPM 需要介入，也应该是在 review_report 基础上插入审核写 revision（该类型 TPM 专属），如果不需要介入，则 coder 和 reviewer 自循环。"

- **DSpro 回应**:
  > "这个思路很成熟。核心是两个决策点："

  **决策一：三种范式都文档化**
  > "框架提供三种范式，但明确标注推荐度和适用场景。这不是推卸设计责任——框架的核心哲学就是'信任用户能做出适合自己的选择'。"

  | 范式 | 适用场景 | TPM 介入度 | 推荐度 |
  |------|---------|-----------|--------|
  | **TPM 直接审查** | 1-2 人，无专职 reviewer | 🔴 高（读全部代码） | 默认 |
  | **调度审查** | 有专职 reviewer，需 TPM 中转 | 🟡 中（创建 REVIEW_TASK） | 按需 |
  | **自循环审查** | 信任型团队，reviewer-coder 自闭环 | 🟢 低（按分级抽查） | 推荐 |

  **决策二：文件夹结构和文件类型**
  > "目录结构支持最大兼容，三种范式共用同一个目录树，区别在于谁写什么文件："

  ```
  inbox/  ← 执行者读
  ├── TASK_NNN            → TPM 独占
  ├── NOTICE_NNN          → TPM 独占
  ├── REPLY_NNN           → TPM 独占
  ├── REVISION_NNN        → TPM 独占（TPM 深度介入时写）
  ├── REVIEW_REPORT_NNN   → Reviewer 独占（前置审查输出）
  ├── REVIEW_TASK_NNN     → TPM 独占（可选，调度审查时需要）

  outbox/  ← TPM + reviewer 读
  ├── REPORT_NNN          → 执行者写

  reviews/ → ❌ 删除
  ```

### Round 10: Kimi 汇总改动范围

- **Kimi**: 汇总了最终改动范围：
  | # | 改动 | 说明 |
  |---|------|------|
  | 1 | 删除 `reviews/` 目录 | 物理删除 |
  | 2 | 删除 `archive/reviews/` 目录 | 随 reviews/ 一并删除 |
  | 3 | REVIEW_REPORT 模板路径改为 `inbox/` | 路径更新 |
  | 4 | REVIEW_TASK 模板保留（标注"调度审查可选"） | 不改内容 |
  | 5 | README/TPM.md 更新审查生命周期 | 引入自循环范式 |
  | 6 | README 增加"协作空间嵌套"说明 | 预留多级管理能力 |
  | 7 | **命名规范不改** | 单侧后缀在单空间内足够 |

- **Kimi 提出细节问题**: reviewer 触发机制（三种范式下不同）和 `archive/reviews/` 实际存在需要处理。

### Round 11: Zehee 提出命名规范统一问题

- **Zehee**: "我们的模板命名目前最后的结尾有的是 author 有的是 assignee，我们要不要统一为 _author_assignee?"

### Round 12: Kimi 首轮分析命名规范

- **Kimi**: 列出 15 个模板的当前后缀，分析内在语义：
  - `_ASSIGNEE`：inbox 文件，"这是给谁做的"
  - `_AUTHOR`：outbox 文件，"这是谁写的"
  - `_TARGET`：通知类，"这是发给谁的"
  - `_SOURCE`：TODO，"这是从哪来的"
- **Kimi**: 认为当前命名有内在逻辑，不是缺陷：
  > "语义清晰：_ASSIGNEE vs _AUTHOR 的区分本身就是'文件角色归属'的一部分，inbox 用 ASSIGNEE、outbox 用 AUTHOR，规则一致。"
- **Kimi 建议**: 保持现状，不统一。

### Round 13: Zehee 指出多级汇报线问题

- **Zehee**: "因为如果我们的工具适用于复杂项目的时候汇报线就不再扁平，当前很多默认是给 tpm 的，但是如果出现多级汇报线就可能出问题。"

- **Zehee 的前瞻性洞察**: 当前 `_AUTHOR` vs `_ASSIGNEE` 的区分基于"所有人 ↔ TPM"的星型结构。如果项目变大出现多级汇报线（初级 coder → 组长 → TPM），单侧后缀无法表达"这个 REPORT 是给谁看的"。

### Round 14: Kimi 重新评估命名规范

- **Kimi**: 承认之前分析过于局限：
  > "当前命名隐含了'星型扁平汇报'假设... 当前所有模板的流向假设：inbox 文件默认从 TPM 发出，outbox 文件默认给 TPM。"
- **Kimi 分析多级汇报场景**:
  | 场景 | 当前文件名 | 问题 |
  |------|-----------|------|
  | 初级 coder → 组长 → TPM | `REPORT_042_20260610_JUNIOR.md` | 这是给组长的还是给 TPM 的？ |
  | reviewer → coder（自循环） | `REVIEW_REPORT_042_20260610_DSpro.md` | 给 Kimi 还是给 TPM？ |

- **Kimi 支持统一为双后缀**: 
  > "支持统一的方向，因为复杂项目确实需要表达通信双方。"
- **Kimi 给出改动代价评估**: 15 个模板 × 2 语言 × README/TPM.md 多处引用，archive 历史文件不追溯。总代价中等。

### Round 15: Zehee 区分两种多级汇报逻辑（架构级洞察）

- **Zehee**: "其实这里面多级汇报线隐含了两种逻辑："

  **第一种：扁平管理 + 长状态机**
  > "管理结构扁平但是状态机流程长，具体的例子就是 reviewer 需要 tpm 介入的情景。"

  **第二种：多级管理**
  > "管理结构多级的情况，这种情况我考虑到的方案是允许 collaboration 嵌套并重命名（例如改为自己部门名字）这样每级部门负责人成为自己部门的 tpm。"

- **Zehee 的解决方案对应**:
  - 长状态机 → 自循环模式（reviewer 直接写 REVISION/REVIEW_REPORT）
  - 多级管理 → collaboration 嵌套（每组一个 TPM）

### Round 16: Kimi 分析两种逻辑

- **Kimi**: 分析两种逻辑独立且互补：
  > "两种路径不冲突，可以同时存在。一个复杂项目可以同时使用两种机制：前端组内部用自循环审查，跨组协作通过嵌套协作空间通信。"

- **Kimi 画出嵌套结构**（初始版本为平级，后被纠正）:
  ```
  项目根目录
  ├── collaboration/          ← 总协作空间
  ├── collaboration-frontend/ ← 前端组
  └── collaboration-backend/  ← 后端组
  ```

- **Kimi 分析嵌套模型下命名规范问题被重新定位**:
  > "在嵌套模型下，单侧后缀在单空间内仍然足够。双后缀不是全局必需品，而是'跨协作空间通信'的扩展能力。"

- **Kimi 建议**: 现在不需要改全局命名，但为跨空间通信预留双后缀能力。

### Round 17: Zehee 纠正嵌套结构

- **Zehee**: "如果嵌套的话，子 collaboration 应该在上层 collaboration 的内部。"

### Round 18: Kimi 确认嵌套结构

- **Kimi**: 画出正确的嵌套结构：
  ```
  collaboration/                          ← 父协作空间（总 TPM）
  ├── inbox/              ← 总 TPM 独占写
  ├── outbox/             ← 组 TPM 写汇总（给总 TPM 读）
  ├── CHARTER.md          ← 父级宪章
  │
  ├── collaboration-frontend/             ← 子协作空间（前端 TPM）
  │   ├── inbox/          ← 前端 TPM 独占写
  │   ├── outbox/         ← 前端 coder 写（给前端 TPM 读）
  │   └── CHARTER.md      ← 子级宪章
  │
  └── collaboration-backend/
      ├── inbox/          ← 后端 TPM 独占写
      ├── outbox/
      └── CHARTER.md      ← 子级宪章
  ```

- **Kimi 分析关键推论**:
  > "在这种嵌套结构下，'inbox TPM 独占'仍然成立，而且更自然。"
  > "组 TPM 的双重身份：在父空间中，组 TPM 是执行者（读父空间 outbox）；在子空间中，组 TPM 是协调者（写子空间 inbox）。"

- **Kimi 分析跨空间通信规则**:
  > "跨空间通信通过'读对方的 outbox'完成，绝不写对方的 inbox。"
  ```
  总 TPM 写跨组需求 → collaboration/outbox/
      ↓
  前端组 TPM 巡检父空间 outbox/ → 读取涉及前端的任务
      ↓
  前端组 TPM 拆解 → 写 TASK → collaboration-frontend/inbox/
      ↓
  前端 coder 领取执行
  ```

- **Kimi 最终结论**: 
  > "命名规范现在确实不需要改。单侧后缀在单空间内完全足够，跨空间通信时目录位置已经表达了层级关系。"

---

## 替代方案

1. **维持现状** — `reviews/` 保留，REVIEW_TASK 和 REVISION 并行。否决：reviews/ 为空，流程冗余
2. **完全放开 inbox** — 任何角色均可写 inbox。否决：破坏协调者模式，任务冲突不可控
3. **新增 `review-inbox/` 目录** — 给 reviewer 单独的任务池。否决：增加目录复杂度，与简化目标矛盾
4. ✅ **精确扩展 REVISION 写权限 + 保留 REVIEW_REPORT** — reviewer 可写 REVIEW_REPORT 到 inbox，TPM 仍独占 TASK/NOTICE/REPLY/REVISION。采纳

---

## 最终产物

| 类型 | 编号 | 说明 |
|------|------|------|
| TASK | 033 | `collaboration/` 解耦 + 审查流程重构 |

### TASK_033 具体改动清单

| # | 改动 | 文件 |
|---|------|------|
| 1 | 删除 `reviews/` 目录 | `collaboration/reviews/` + `collaboration-live/reviews/` |
| 2 | 删除 `archive/reviews/` 目录 | `collaboration/archive/reviews/` |
| 3 | REVIEW_REPORT 模板存放位置改为 `inbox/` | `templates/REVIEW_REPORT_NNN_DATE_AUTHOR.md` |
| 4 | REVIEW_TASK 模板保留，标注"调度审查可选" | `templates/REVIEW_TASK_NNN.md` |
| 5 | README.md 更新目录树（去掉 reviews/） | `README.md` + EN |
| 6 | README.md 更新权限表 | `README.md` + EN |
| 7 | README.md 更新文件生命周期（去掉 reviews/ 归档路径） | `README.md` + EN |
| 8 | TPM.md 更新审查流程（三种范式 + 自循环） | `TPM.md` + EN |
| 9 | TPM.md 更新归档规则 | `TPM.md` + EN |
| 10 | README.md 增加 inbox 写域标注（默认 TPM 独占，REVIEW_REPORT 可开放给 reviewer） | `README.md` + EN |
| 11 | README.md 增加"协作空间可嵌套"架构预留说明 | `README.md` + EN |
| 12 | 验证器更新（去掉 reviews/ 相关规则） | `extras/template-validator/validate.py` |

---

## 关联文件

- **DECISION_018**: 框架规则边界标记与治理分层（铁律/格式契约/字段建议/示例模式/实例自定义）
- **DECISION_019**: 规则编号与分类体系（草案，待审阅）
- **DECISION_020**: `collaboration/` 与项目代码完全解耦（解耦为前提，嵌套为扩展）
- **TODO_003/004**: 暂缓任务
