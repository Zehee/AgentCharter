# REVIEW_TASK_036: 脚本工具体系深度审查

> **文件名**: `REVIEW_TASK_036_SCRIPTS-DEEP-REVIEW.md`
> **存放位置**: `inbox/`
> **命名约束**: 段间 `_`，段内 `-`。`NNN`=被审查的任务序号

**审查人**: KIMI
**被审查人**: TPM (DSpro)
**优先级**: 🟡 P1
**决策来源**: TASK_036 — 完整脚本工具体系搭建

---

## 审查范围

| 文件 | 路径 | 说明 |
|------|------|------|
| 公共层 | `collaboration/scripts/_common.py` | run_create_flow + run_and_exit + 异常兜底 + 交叉引用校验 + 编号逻辑 |
| 总入口（外部 Agent） | `collaboration/scripts/agent.py` | 命令列表 + 巡检 + 自动 PROACTIVE_REPORT |
| 总入口（TPM） | `collaboration/scripts/tpm.py` | 全览巡检 + 命令列表 |
| lib/actions | `collaboration/scripts/lib/actions.py` | ACTIONS.md 角色/链路/权限解析 |
| lib/naming | `collaboration/scripts/lib/naming.py` | 文件名生成 + 15 种文件类型的命名正则 |
| lib/template | `collaboration/scripts/lib/template.py` | {{变量}} 模板解析器 |
| lib/validate | `collaboration/scripts/lib/validate.py` | 内容字段校验 + 交叉引用 |
| lib/registry | `collaboration/scripts/lib/registry.py` | NNN 序列管理 + 目录映射 |
| lib/patrol | `collaboration/scripts/lib/patrol.py` | inbox/outbox 巡检 |
| lib/redlines | `collaboration/scripts/lib/redlines.py` | 红线规则读取 |
| 倒推式审查 | `collaboration/scripts/new-review-report.py` | 自循环/委派范式自动推导 |
| 其他命令 | `collaboration/scripts/new-*.py` | 所有 new-xxx 命令脚本 |
| 全量巡检 | `collaboration/scripts/daily-check.py` | 命名/流向/内容综合校验 |

---

## 审查重点

### 1. 脚本之间的关联完整性

逐一验证每一对关联关系是否在代码中正确实现：

| 创建脚本 | 依赖 | 是否有交叉引用校验？ | 编号来源是否正确？ |
|---------|------|-------------------|-----------------|
| new-report.py | TASK / REVISION | `_check_ref_exists` | ref_nnn → NNN |
| new-revision.py | REVIEW_REPORT | 同上 | ref_nnn → NNN |
| new-review-report.py | TASK / REPORT | 同上 + 倒推法 | 范式决定 |
| new-review-task.py | TASK | 同上 | ref_nnn → NNN |
| new-blocking-reply.py | BLOCKING | 同上 | ref_nnn → NNN |
| new-decision.py | 无（自增） | 不适用 | AUTO_NNN_TYPES |
| new-task.py | 无（自增） | 不适用 | AUTO_NNN_TYPES（含归档去重） |
| new-proactive-report.py | 无 | 不适用 | 自编号 |
| new-notice.py | 无 | 不适用 | 无编号 |
| new-reply.py | PROACTIVE_REPORT | 应校验？ | 无编号 |

- [x] 审查 `_common._check_ref_exists` 是否覆盖了所有应校验的文件类型
- [x] `REF_MAP` 中是否有遗漏的关联对？
- [x] 每种派生类型的搜索目录是否正确（活跃+归档vs仅活跃）？
- [x] `new-decision.py` 剥离 `is_tpm()` 后，`agent.py` 的自动 PROACTIVE_REPORT 逻辑是否正确？

### 2. 入口分离的正确性

`agent.py` 与 `tpm.py` 的命令划分是否合理：

- [ ] `agent.py` 当前 6 个命令：new-report / new-review-report / new-decision / new-blocking / new-blocking-reply / validate-file。是否越权或缺少？
- [ ] `tpm.py` 的命令列表是否与 `agent.py` 互补且不冲突？
- [ ] 外部 Agent 调 `new-decision` 时 `agent.py` 自动追加 PROACTIVE_REPORT 的实现是否健壮（异常分支、重复追加）？

### 3. 异常处理全面性

- [ ] `_common.py` 的兜底 try/except 是否能捕获所有可能抛出的异常类型？
- [ ] 每个 `new-*.py` 是否统一使用 `run_and_exit`，还是有的走了自定义逻辑？（检查 `new-review-report.py` 和 `new-decision.py`）
- [ ] 当 ACTIONS.md 为空模板时（fresh project），`actions.py` 的行为是否降级正常而非抛异常？
- [ ] 当 `collaboration/archive/` 目录不存在时，`registry.py` 和 `validate.py` 是否正常降级？

### 4. 模板与工具的契合度

- [ ] `template.py` 解析出的字段列表是否覆盖了模板中所有 `{{变量}}`？
- [ ] 模板说明文字（`> 引导行`）是否被误解析为字段？
- [ ] 26 个模板（CN+EN）的 `{{变量}}` 命名是否统一、语义一致？

### 5. 红线的稳定性

- [ ] `CHARTER.md §七` 代码块中的各行格式是否严格一致（`— 内容 ！`）？
- [ ] 当 `CHARTER.md` 用户自行增删红线行时，解析器是否容错？
- [ ] `redlines.py` 在 `CHARTER.md` 不存在或格式异常时的降级行为？

### 6. 安全性

- [ ] `daily-check.py` 的流向校验是否在 ACTIONS.md 不可用时使用硬编码保底规则？
- [ ] 脚本是否在任何路径下都保证输出 JSON 而非裸异常（兜底 catch-all）？
- [ ] `agent.py` 通过 `subprocess` 调用其他脚本，是否存在参数注入风险（`json_data` 传入恶意数据）？

---

## 输出要求

提交 `outbox/REVIEW_REPORT_036_DATE_KIMI@DSpro.md`，包含：

1. **总体评分**（1-10）
2. **按审查重点分类**：每个子项给出 ✅ / ❌ / ⚠️ 结论
3. **发现的问题**：🔴严重 / 🟡一般 / 💡建议，附文件:行号
4. **修复建议**：对 🔴 和 🟡 问题逐条给出具体修复方案
5. **是否建议合并**：通过 / 需修订
