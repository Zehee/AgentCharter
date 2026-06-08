# 变更日志

格式基于 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.0.0/)，
本项目遵循 [语义化版本](https://semver.org/lang/zh-CN/)。

## [Unreleased]

### 新增

- **协作宪章**: `collaboration/CHARTER.md`，TPM 初始化后移至项目根目录作为全局最高规则
- **ACTIONS.md**: 框架内建空模板，含字段说明、通道类型速查、样例
- **GitHub 社区文件**: Issue 模板（bug + feature）、PR 模板、SECURITY.md
- **TPM 核心原则重写**: 8 条新原则——项目合伙人、全生命周期掌控、Agent 管理者、透明汇报、协作工具维护、不写业务代码、Git 独权、输出精简
- **CHARTER.md 移根机制**: TPM 初始化后将 CHARTER.md 移至项目根目录 `../CHARTER.md`，所有 Agent 共享最高规则
- **Sub-Agent 后台内循环**: 原则中明确 Native Sub-Agent 应后台创建 + 内存循环巡检

### 变更

- **AGENTS.md → TPM.md**：防止被 AI 工具自动加载到非 TPM Agent 的 prompt 中
- **阻断声明**: TPM.md 顶部首行 `🛑 你的用户必须已经明确告知"你是 TPM"`
- **初始化独立成章**: 从 §一 移出为独立 `## 初始化` 节（5 步操作）
- **TPM 初始化命令更新**：`你是 TPM，分析 collaboration 目录并初始化`
- **Agent 入职命令更新**：`分析 collaboration 目录并按照流程入职`
- **TPM 权限表化**: §二 改为 T-P-M 三维权限表（18 项 + 6 条红线）
- **外层 README 重写**: 新增运行理念、TPM 核心制、方式对比表（4类9维）、MCP 对比（7维）、可扩展性、零手工入驻、使用者项目结构图
- **collaboration/README.md 精简**: 580 行 → 268 行，去营销语言，面向 Agent
- **删除 scripts/**: Reasonix 专属 file-editor，不应污染通用框架
- **CONTRIBUTING.md 重写**: 更新项目结构速查、Agent 视角原则、占位符规范

### 修复

- TPM.md §3.1 巡检流程图残留"保留一天"（已废除）
- TPM.md §5.5 引用旧章节名 "五、任务与报告" → §五、任务生命周期
- REGISTER.md 过时 REVIEW_TASK 引用 → 改为 REPORT → REVIEW_REPORT 直写模式
- PROJECT.md TPM 角色 "技术产品经理" → "Task Planning Manager"
- TPM.md §十 gitignore 描述从 "collaboration/ 整体忽略" → 分层忽略
- .gitignore 注释残留旧名 AGENTS

## [3.2.0] - 2026-06-06

### 新增

- **实践案例体系**: `practices/` 目录，收录社区实践案例
  - 首个实践：wolf-judge（5 人团队全栈项目，120+ 任务闭环）
  - 实践贡献指南

### 变更

- **collaboration/README.md 大幅扩展**: 106 行 → 430+ 行，4 节 → 13 节
  - 补全通用规则、任务与报告、角色定义、入职流程、最佳实践、适用场景等
- **REGISTER.md 升级**: 3 动作 → 5 动作（新增主动报告、阻塞依赖）
- **5 个模板泛化**: NOTICE/LOG_ENTRY/REPLY/TASK_TEST/TODO 去除实例引用

## [0.1.0] - 2026-05-30

### 初始发布

- 框架规范、8 个文件模板、入职登记、项目配置
