# 贡献指南

感谢你对 AgentCharter 的兴趣！

## 项目结构速查

```
collaboration/          # 框架核心 — Agent 端规范和模板
├── README.md           # Agent 协作规范（12 章）
├── CHARTER.md          # 协作宪章模板（TPM 初始化后移至项目根目录）
├── TPM.md              # TPM 行为准则
├── PROJECT.md          # 项目配置模板
├── REGISTER.md         # 入职登记表
├── ACTIONS.md          # 协作链路表模板
├── templates/          # 14 个文件模板
├── context/            # Sub-Agent 上下文记忆
├── inbox/ outbox/ reviews/ logs/ todos/ archive/

practices/              # 社区实践案例
├── wolf-judge/         # 5 人团队全栈实践
```

## 如何贡献

### 报告问题

- 用 GitHub Issue 描述问题
- Bug 类：说明哪个文件、哪条规则有问题、预期行为
- 框架规则改进：说明理由和影响范围

### 提交改进

1. Fork 本仓库
2. 创建特性分支：`git checkout -b feature/xxx`
3. 提交改动：`git commit -m '描述'`
4. 推送：`git push origin feature/xxx`
5. 创建 Pull Request

### 框架文件修改原则

AgentCharter 的核心是规则的一致性和简洁性：

- **最小改动**：只改必要的部分，不动无关内容
- **Agent 视角**：`collaboration/` 下的文件面向 AI Agent，避免人类营销语言
- **通用性**：不引入特定技术栈或 Agent 平台的假设
- **占位符**：使用 `[占位符]` 而非具体名称（如 `[你的技术栈]`）
- **模板基准**：`templates/` 是只读基准，修改会导致所有下游实例的文件格式断裂

### 实践案例贡献

提交 `practices/<name>/` 目录，包含 README.md（参照 wolf-judge 格式）。重点写角色设置、协作关系、个性化规则。

## 讨论

需要社区共识的改动（如新增文件类型、调整角色定义），建议先开 Issue 讨论。
