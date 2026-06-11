# TASK_029: CHARTER.md 模板定位注释

> **Assignee**: Kimi
> **Priority**: P2
> **Decision**: DECISION_018_20260610_TPM-PAIR.md
> **Source**: PROACTIVE_REPORT_006 建议 029

---

## 目标

在 `collaboration/CHARTER.md` 模板顶部添加注释，明确其"个性层"定位——框架只提供模板，填写后是项目实例。

---

## 具体改动

### `collaboration/CHARTER.md`

在文件顶部（`# AgentCharter — 项目宪章` 标题下方）增加注释段落：

```markdown
> 此文件是模板。由 TPM 在初始化时填写，完成后移至项目根目录（`../CHARTER.md`）。
> 填写后的 CHARTER.md 成为项目级压缩规则，与框架通用规则（`collaboration/README.md`）并列，不由框架统一治理。
> 你的项目可以调整、简化或扩展本模板中的任何内容。
```

---

## 约束条件

- ❌ 不修改模板中的任何字段结构
- ❌ 不修改现有字段的默认值
- ✅ 只在顶部加注释段落

---

## 验收标准

- [ ] CHARTER.md 顶部有定位注释
- [ ] 注释明确标注 CHARTER.md 是"模板/个性层"
- [ ] 现有字段和结构未受任何影响
- [ ] 提交 REPORT_029_KIMI.md 到 outbox/
