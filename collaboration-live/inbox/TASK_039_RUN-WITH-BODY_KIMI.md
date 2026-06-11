# TASK_039: 重构工具入口——新增 run_with_body 函数式调用

> **Assignee**: Kimi
> **Priority**: P1
> **Source**: 三方讨论结论——Agent 直接写 markdown 正文比拼 JSON 更自然

---

## 背景

当前工具入口是 `run_create_flow(file_type, agent_name, data: dict)`，Agent 需要：

1. 记住模板有哪些 `{{变量}}`（无参跑一次看字段列表）
2. 把正文内容塞进 JSON（引号转义、换行处理）

这对 LLM 来说体感差。读模板自由写 markdown 然后调函数，比拼 JSON 自然得多。

**新入口：**

```python
from _common import run_with_body

result = run_with_body("REPORT", "KIMI", ref="042", body="""## 完成情况

| 任务 | 状态 | 说明 |
|------|------|------|
| 用户登录 | ✅ | 前后端联调通过 |
""")
```

工具负责：身份校验、NNN 推导、文件名生成、路径路由、引用校验、红线提醒。
Agent 只负责：写正文 markdown。

---

## 改动范围

### 1. `_common.py` — 新增 `run_with_body()`

```python
def run_with_body(file_type: str, agent_name: str, body: str, ref: str = None) -> dict:
    """函数式入口：Agent 只传正文，工具负责校验和路由。

    Args:
        file_type: REPORT / TASK / REVISION / PROACTIVE_REPORT 等
        agent_name: 调用者标识，如 KIMI
        body: markdown 正文内容
        ref: 关联编号（REPORT→TASK_NNN、BLOCKING_REPLY→BLOCKING_NNN）

    Returns:
        同 run_create_flow：{"result":"✅ 文件已创建", "filename":"...", "redlines":"..."}
    """
```

**内部逻辑：**

```
① 组装 data 字典
   - ref → data["ref_nnn"]、data["NNN"]（派生类型用 ref 做编号）
   - author = agent_name
   - DATE = 今天
   - recipient = 从 ACTIONS.md 默认值（REPORT→TPM、NOTICE→ALL）
   - title = 从 body 首行提取
   
② 调用 run_create_flow（走现有校验流程）
   - 身份校验 ✅
   - 引用校验 ✅
   - 文件名生成 ✅
   - 目录路由 ✅
   - 红线提醒 ✅

③ body 覆盖文件内容
   - 不读取模板
   - 不执行 {{}} 替换
   - 由 run_create_flow 在生成文件名和路径后，用 body 替换文件内容
```

**需要调整 `run_create_flow` 内部**：

当 `data["body"]` 存在时，跳过模板读取和 `{{}}` 替换流程，直接以 body 为内容写文件。同时正文空检查也要兼容 body 模式——有 body 就视为正文已填。

### 2. `tpm.py` / `agent.py` — 入口不变

这两个入口转发到 `new-*.py` 脚本，`new-*.py` 内部调 `run_create_flow`。`run_with_body` 是给 Agent 直接调的函数，不需要经过入口。

### 3. 保留现有能力

| 能力 | 保留方式 |
|------|---------|
| JSON 输入 (`run_create_flow`) | 保持不动，向后兼容 |
| 命令行调用 (`new-*.py`) | 保持不动 |
| 大小写不敏感 | 不修改 |
| 正文空检查（body 模式跳过） | body 存在时视为正文已填 |
| 提取 body 标题 | 从 body 首行 `# ` 提取，填入 data["title"] |

---

## 验收标准

- [ ] `run_with_body("REPORT", "KIMI", ref="042", body="## 完成情况...")` → 文件创建成功
- [ ] 生成的文件路径：`outbox/REPORT_042_DATE_KIMI@TPM.md`
- [ ] 生成的文件内容以 body 为准，不含 `{{}}` 残留
- [ ] 文件头部字段（author/date/status/对应）在 body 中自动生成
- [ ] ref 对应的源文件不存在时阻断
- [ ] 无 ref 时（TASK/DECISION）自动编号
- [ ] 不传入 body 时走原有流程不变
- [ ] 传入 body 时正文空检查不阻断
- [ ] 传入 body 时 `{{}}` 替换流程跳过
- [ ] 三份 `scripts/` 同步
- [ ] 提交 REPORT_039_KIMI.md 到 outbox/
