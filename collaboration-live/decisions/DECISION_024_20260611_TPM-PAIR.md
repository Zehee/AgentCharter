# DECISION_024: 多轮次增量文件链支持（_R1、_R2）

**结对**: @tpm-pair (DSpro + Zehee) / @kimi-pair (Kimi + Zehee)
**时间**: 2026-06-11
**状态**: ✅ 正式

---

## 决策

1. **`_R1`、`_R2` 是独立轮次段，非 NNN 的一部分** — 正确格式 `REPORT_042_R1_DATE_...`，`042` 是 NNN，`_R1` 是轮次
2. **受影响文件类型**：REPORT、REVIEW_REPORT、REVISION（有自循环修复场景）— TASK/DECISION 等无需轮次
3. **naming.py 正则扩展** — 三类文件的正则加 `(_R\d+)?` 可选段
4. **`generate_filename` 增加 `round` 参数** — 传 `round=1` 生成 `_R1`
5. **`_common.py` 创建前检测同 NNN 文件** — 已存在时按已有最大轮次+1自动设置 `round`，或提示用户
6. **不新增 `_R1` 专用模板** — `resolve_template` 回退到基础模板（内容相同）
7. **模板中 `{{round}}` 占位符** — 基础模板增加 `{{round}}` 变量，首轮为空，R1+为 `_R1`

---

## 推理链

基于 Kimi's REVIEW_REPORT_036 的附录 B（多轮次专项核查），三方确认：
- 文档层面多轮次规则已完善（README.md §三、TPM.md §五、CHARTER.md §三）
- 脚本层完全未实现（naming.py 正则、generate_filename 参数、创建前检测、轮次提示）
- 改动涉及命名/模板/脚本三层，独立实施
