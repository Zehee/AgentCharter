# DECISION_025: TPM 身份与角色名——链路表、文件名、换人过渡

**结对**: @tpm-pair (DSpro + Zehee) / @kimi-pair (Kimi + Zehee)
**时间**: 2026-06-11
**状态**: ⏳ 待定——已写入 TODO_007，暂不执行

---

## 问题

TPM 在链路表中写 `TPM → KIMI` 还是 `DSpro → KIMI`？文件名后缀用 `@TPM` 还是 `@DSpro`？

当前 `actions.py` 的 `is_tpm`、`validate_agent`、`patrol.py` 的扫描函数均受此影响。

---

## 讨论摘要

### Round 1: TPM 用个人名字调工具时，扫不到 @TPM 文件

- **Zehee**: 如果链路表写的是 `TPM → KIMI`，而不是个人名 `DSpro → KIMI`，DSpro 用 `tpm.py DSpro` 时，巡检扫不到 `@TPM` 文件
- **DSpro**: 提议在 `is_tpm` 中按链路表推断 TPM 身份，在 `patrol.py` 中追加 `@TPM` 别名扫描
- **Zehee**: 不同意——应该从 README 👑 区读 TPM 真名，将 TPM 与真实姓名等价
- **DSpro**: 提出 README 👑 区读真名方案

### Round 2: 用 `@TPM` 而非个人名，换人零过渡

- **Zehee**: 意识到 `@TPM` 不是缺陷而是特性——换人时 `@TPM` 文件天然衔接
- **DSpro**: 进一步推论——链路表和文件名都应该用 `TPM`（角色名），不写真名
- **Zehee**: 但 README 👑 区不写真名是否合理？工具是否需要读 README？

### Round 3: TPM 是一个岗位，不是一个人

- **Zehee**: 颠覆——TPM 应该直接叫自己 `TPM`，不写真名。换人就是岗位交接，不涉及改名
- **DSpro**: 赞同——框架信任 agent 会遵守协议，同样信任 TPM 这个身份。谁坐这个岗位谁叫 TPM
- **Zehee**: 但 agent 会不会困惑？"以前我叫 TPM 现在改名了"
- **DSpro**: 不存在改名场景——是老的不干了新的来干。`TPM` 这个名字留在岗位上不动

### Round 4: 结论待定

- **Zehee**: 需要再想想，这是个复杂问题
- **共识**: 当前暂缓，TPM 在链路表中写真名（方案 B 的暂时妥协），不写 `TPM`
- **Zehee**: 避免通配问题，写入 TODO 待决策

---

## 两种方案的对比

| 维度 | 方案 A：角色名 | 方案 B（当前）：个人名 |
|------|-------------|-------------------|
| 链路表 | `TPM → KIMI` | `DSpro → KIMI` |
| 文件名后缀 | `@TPM` | `@DSpro` |
| `is_tpm` 判断 | 只认字符串 `TPM` | 需推断个人名→角色名 |
| 换人过渡 | ✅ 零成本，新人继承 `TPM` | ❌ 旧文件 @DSpro 无人处理 |
| 认知负担 | ⚠️ TPM=角色名=岗位名 | ✅ 名字就是名字 |
| 与框架哲学 | ✅ "信任，而非控制" | ⚠️ 个人名与角色名耦合 |

---

## 关联文件

| 类型 | 编号 | 说明 |
|------|------|------|
| TODO | 007 | TPM 身份与角色名讨论，待决策 |
| DECISION | 023 | 脚本工具体系（涉及 `is_tpm`、`validate_agent`） |
| ACTIONS.md | — | 协作链路表（TPM 如何出现） |
