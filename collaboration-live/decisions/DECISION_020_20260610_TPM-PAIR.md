# DECISION_020: collaboration/ 与项目代码完全解耦

**结对**: @tpm-pair (DSpro + Zehee) / @kimi-pair (Kimi + Zehee)
**时间**: 2026-06-10
**状态**: ✅ 正式

---

## 决策

1. **`collaboration/` 不再要求放入项目根目录** — 可以放在任何位置（项目内、NAS、Dropbox、独立服务器），Agent 的工作目录就是 `collaboration/` 所在的位置
2. **CHARTER.md 不再搬家** — 填好后留在 `collaboration/` 内部，不再移至项目根目录。所有 `../CHARTER.md` 引用改为 `CHARTER.md`
3. **不引入配置** — 不新增配置文件、环境变量、搜索顺序。路径是 TPM 在启动 Agent 时传入的上下文信息
4. **移除所有 `../practices/` 硬编码引用** — 改为纯文字说明
5. **保留设计意图引用** — `collaboration/` 内部文件间的相对路径引用保持有效

---

## 推理链

### Round 1: 用户提出"解耦"需求

- **Zehee**: "实际上用户在使用 agentcharter 的时候可以把 collaboration 放在任何地方甚至和项目完全不在一个地方都可以，对不对？"
- **DSpro**: 确认可以，但指出当前存在隐式耦合——路径引用、初始化流程、CHARTER.md 搬家
- **Zehee**: "我们要不要做 collaboration 与项目的解耦"
- **DSpro**: 分析取舍——要改路径引用、初始化流程、模板引用；但这是"做值得但不急着做的事"
- **Zehee**: "我们应该作为特性，尽快的更新掉，这样对用户项目的侵入感会降低很多"

### Round 2: 确认不需要配置

- **DSpro**: "我们需要知道用户的项目在哪里吗？"
- **Zehee**: "不需要"
- **Kimi**: 持续追问配置方案
- **Zehee**: "所以还需要配置吗"
- **DSpro**: 得出结论——不需要配置，路径是 TPM 启动 Agent 时传入的上下文
- **Zehee**: "我们只需要保证我们内部的文件引用是正确的就可以"

### Round 3: 审计内部引用

- **DSpro**: 全面审计 `collaboration/` 内部引用，发现：
  - 16 处 `../CHARTER.md` 引用 — 设计意图（搬家机制）
  - 2 处 `../practices/` 链接 — 不必要的耦合
  - 无 HTTP 外部链接，模板文件干净
- **DSpro**: 发现一处设计矛盾——"位置无关"声明与 `../CHARTER.md` 引用隐含假设冲突

### Round 4: 用户确定方向

- **Zehee**: "我们不再去侵入项目，意味着我们不再要求 charter 放入项目根目录，甚至不再要求放入项目"
- **Zehee**: "外层的 readme 好像有安装完毕你的项目结构是如下"
- **Zehee**: "这段也要改"（指向 After initialization 项目结构图）

### Round 5: 完整改动范围确定

三方确认改动范围涵盖：
- `collaboration/CHARTER.md` — 2 处（去搬家描述）
- `collaboration/PROJECT.md` — 1 处（去 practices 硬编码）
- `collaboration/README.md` — 2 处（目录树注释 + `../CHARTER.md`→`CHARTER.md`）
- `collaboration/TPM.md` — 3 处（删步骤 5 + 2 处 `../CHARTER.md` 修正）
- 外层 `README.md` — 4 处（Quick Start + 结构树 + 项目结构图）
- 外层 `README_CN.md` — 4 处（同上中文）
- `collaboration_en/` — 同步英文版 8 处

---

## 替代方案

1. **不做解耦，维持现状** — CHARTER.md 继续搬家到项目根目录。用户必须将 `collaboration/` 放在项目根目录下。否决
2. **引入配置机制** — 新增 `agentcharter.json` 或环境变量。零配置是框架核心哲学，否决
3. ✅ **只改文字，不改机制** — CHARTER.md 不再搬家，所有引用修正。采纳

---

## 最终产物

| 类型 | 编号 | 说明 |
|------|------|------|
| TASK | 033 | `collaboration/` 解耦——修正所有外部路径引用 |
