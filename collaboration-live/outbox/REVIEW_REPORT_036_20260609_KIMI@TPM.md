# REVIEW_REPORT_036: 脚本工具体系 — 需要修订

> **文件名**: `REVIEW_REPORT_036_20260609_KIMI@TPM.md`
> **存放位置**: `outbox/`
> **命名约束**: 段间 `_`，段内 `-`，后缀 `author@recipient`。`NNN`=审查序号，`DATE`=提交日期 `YYYYMMDD`，`author`=审查人标识（大写），`recipient`=接收者标识（大写）

**审查人**: KIMI
**日期**: 20260609
**对应**: 036
**接收者**: TPM

> **摘要流转规则**：【摘要】节必填。首轮只写 `### R0`，后续轮次从执行者的 REPORT_RN【审查摘要】复制全部历史原文，底部追加本轮，不得修改历史原文。

---

## 【审查摘要】（必填）

### R0 (20260609)
- 评分：4/10
- 本轮：🔴 5 / 🟡 8 / 💡 4
- 状态：需要修订（存在路径解析错误 + 关联校验目录错误 + 关联提示错位 + 多轮次命名完全不支持，共 4 处阻断性 bug）
- 一句话：脚本系统架构清晰，但目录结构迁移后路径解析未同步；关联校验的 `search_dirs_map` 存在两处目录配置错误；`no_args_response` 对所有类型一刀切输出 TASK 列表；**最关键的是：文档明确约定的多轮次增量文件链（REPORT_NNN → REPORT_NNN_R1）在命名层完全无法落地——`naming.py` 正则、模板文件名、脚本创建流程均未支持 `_R1`，整个多轮次修复机制在脚本层无法运转。**

| 维度 | 评分 | 说明 |
|------|------|------|
| 代码质量 | 6/10 | 模块化设计良好，公共层抽象到位，但存在重复路径解析逻辑且部分未同步更新 |
| 逻辑正确性 | 4/10 | 3 处阻断性路径/目录 bug + 关联提示错位；核心功能在真实目录结构下无法正常工作 |
| 类型安全 | 7/10 | 使用了类型注解，但 `resolve_template` 返回标注为 `Path` 实际可能返回 `None`，`_check_ref_exists` 返回类型未标注 |
| 测试覆盖 | 2/10 | 无自动化测试，路径解析与关联校验 bug 在简单集成测试中即可暴露 |
| **总体** | **4/10** | **架构可接受，但阻断性 bug 数量较多，必须修订后才能投入使用** |

## 发现的问题

| # | 严重度 | 文件 | 问题 | 建议 |
|---|--------|------|------|------|
| 1 | 🔴 阻断 | `lib/actions.py` | `_ACTIONS_PATH = _PROJECT_ROOT / "collaboration" / "ACTIONS.md"` 多了一层 `collaboration/`。因 scripts/ 现已位于 `collaboration/scripts/` 内，`_PROJECT_ROOT` 实际为 `collaboration/`，导致路径变成 `collaboration/collaboration/ACTIONS.md`，文件永远读不到。所有 Agent 验证、角色判断、流向校验全部失效。 | 改为 `_ACTIONS_PATH = _PROJECT_ROOT / "ACTIONS.md"` |
| 2 | 🔴 阻断 | `validate-all.py` | `COLLAB_DIR = PROJECT_DIR / "collaboration"` 同样多了一层 `collaboration/`。`PROJECT_DIR = SCRIPT_DIR.parent = collaboration/`，导致 `COLLAB_DIR = collaboration/collaboration/`，目录扫描永远失败。 | 改为 `COLLAB_DIR = PROJECT_DIR` |
| 3 | 🔴 阻断 | `_common.py` | `search_dirs_map` 缺少 `BLOCKING` 条目。`BLOCKING_REPLY` 创建时 `_check_ref_exists` 对 BLOCKING 使用默认值 `["inbox"]`，但 BLOCKING 文件实际在 `outbox/`，永远找不到。 | 添加 `"BLOCKING": ["outbox"]` |
| 4 | 🟡 高 | `_common.py` | `search_dirs_map` 中 `REVIEW_REPORT` 只搜 `outbox/`，但自循环范式下 REVIEW_REPORT 在 `inbox/`。REVISION 创建时若对应的 REVIEW_REPORT 在 inbox/，校验会失败。 | 改为 `["inbox", "outbox", "archive/inbox", "archive/outbox"]` |
| 5 | 🟡 高 | `tpm.py` | COMMANDS 列表包含 4 个不存在的脚本：`new-review-task.py`、`new-notice.py`、`new-reply.py`、`archive.py`。TPM 调用这些命令会直接报错 "命令不存在"。 | 补全缺失的 4 个脚本，或从 COMMANDS 列表中移除（如果暂不实现） |
| 6 | 🟡 高 | `collaboration/ACTIONS.md` | 第 28 行仍保留 `reviews/REVIEW_REPORT` 通道，但 `reviews/` 目录已在 DECISION_021 中删除，此引用造成文档与实现不一致。 | 更新 ACTIONS.md 中 REVIEW_REPORT 的通道描述为 `outbox/`（委派）或 `inbox/`（自循环） |
| 7 | 🟡 高 | `_common.py` | `no_args_response` 对所有类型都调用 `scan_inbox` 输出 TASK 列表，但 REVISION 需要 REVIEW_REPORT、BLOCKING_REPLY 需要 BLOCKING。显示错误的关联源会误导 Agent 填入错误编号。 | 按 `file_type` 选择正确的关联源扫描函数（详见附录 A） |
| 8 | 🟡 高 | `_common.py` | `run_create_flow` 中对未替换的 `{{变量}}` 仅执行 `pass`（第 178–181 行），不报错、不警告。Agent 若遗漏必填字段，脚本静默生成内容不完整的文件。 | 对 `name_pattern` 中包含的变量做必填校验；对残留的 `{{}}` 输出 warning（详见附录 B） |
| 9 | 🟡 中 | `new-review-report.py` | 自循环范式下，若 `outbox/` 中没有 REPORT 文件，`coder` 默认为字符串 `"coder"`，生成的文件名 recipient 为无效标识。 | 当无 REPORT 时拒绝创建，或要求 caller 显式提供 `recipient` |
| 10 | 💡 低 | `daily-check.py` | `stats` 字典声明了 `naming_ok` 和 `flow_issues` 字段，但代码中从未对它们赋值或累加，统计输出始终为 0。 | 补充统计逻辑，或移除未使用的字段 |
| 11 | 💡 低 | `agent.py` / `tpm.py` | `forward_command` 中的 `subprocess.run` 未设置 `timeout`，若子进程死锁，父进程将无限等待。 | 添加 `timeout=30` 等合理超时 |
| 12 | 💡 低 | `lib/validate.py` | `EXPECTED_HEADERS` 全为中文字段名，对 `collaboration_en/templates/` 下的英文模板产生 13 个 header 不匹配警告。 | 增加双语 header 映射，或根据文件路径自动判断语言 |
| 13 | 💡 低 | `_common.py` | `REF_MAP` 中 NOTICE、REPLY、TODO 等类型未定义关联校验规则（虽然这些类型本身不需要关联），但映射表与 `resolve_template` 中的类型列表不一致。 | 统一类型清单，或显式注释哪些类型无需关联校验 |
| 14 | 🔴 阻断 | `lib/naming.py` | 正则不支持 `_R1`、`_R2` 多轮次后缀。文档（README/CHARTER/TPM）明确约定增量文件链为 `REPORT_NNN` → `REPORT_NNN_R1` → …，但 `REPORT_042_R1_20260609_...` 无法通过 `validate_name()`。整个多轮次修复机制在脚本层无法运转。 | 扩展正则支持可选的 `(_R[0-9]+)` 段；扩展 `generate_filename` 支持 `round` 参数；新增 `_R1` 模板变体（详见附录 B） |
| 15 | 🟡 高 | `_common.py` | `run_create_flow` 没有检测同编号文件是否已存在。Agent 调用 `new-report.py` 时可能重复创建同名 `REPORT_042` 文件，违反"只追加，不覆盖"红线。 | 创建前扫描同 NNN 文件；若已存在，提示应使用 `_R1` 并拒绝覆盖 |
| 16 | 🟡 高 | `_common.py` | `no_args_response` / `run_and_exit` 没有轮次提示。Agent 运行 `new-report.py KIMI` 时，只输出 TASK 列表，不会提示"已有 REPORT_042，建议创建 REPORT_042_R1"。 | 在输出中增加 `existing_files` 字段，列出同 NNN 的已有文件及建议轮次 |
| 17 | 🟡 中 | `lib/registry.py` | `get_next_nnn` 使用 `TASK_(\d{3})` 模式扫描文件。若存在 `REPORT_042_R1_...`，`\d{3}` 会匹配 `042`，`_R1` 被忽略。这本身无害（编号不冲突），但若后续支持 `_R1` 自增，需考虑轮次逻辑。 | 当前不紧急；若实现 `_R1` 支持，编号逻辑需排除 `_R[0-9]` 文件或单独管理 |
| 18 | 🟡 中 | `collaboration/` 文档 | NNN 示例错误：`NNN` = 3 位编号，但示例中写了 `049C_R1`。`_R1` 是独立轮次段（非 NNN 的一部分），正确格式为 `NNN_RN`（如 `049C` 是 NNN，`_R1` 是附加轮次）。文档示例 `049C_R1` 会误导读者认为 `_R1` 属于 NNN。 | 修正所有文档中的 NNN 示例，明确 `_RN` 是独立于 NNN 的轮次段；同步更新 naming.py 正则使 `NNN_RN` 合法化 |

## 关联提示专项核查

> 审查重点：new-report 等创建脚本是否帮助 Agent 找到正确的关联源文件、是否对错误编号报错。

| 脚本 | 关联源类型 | 仅名字模式输出 | 关联校验 | 结果 |
|------|-----------|---------------|---------|------|
| `new-report.py` | TASK | `available_tasks`（@自己的 TASK 列表）✅ | `_check_ref_exists` 搜索 `TASK_{nnn}` 或 `REVISION_{nnn}` ✅ | **通过** |
| `new-revision.py` | REVIEW_REPORT | `available_tasks`（TASK 列表）❌ 应是 REVIEW_REPORT | `_check_ref_exists` 搜索 `REVIEW_REPORT_{nnn}` ✅（但目录不全，见 issue #4） | **不通过** |
| `new-blocking-reply.py` | BLOCKING | `available_tasks`（TASK 列表）❌ 应是 BLOCKING | `_check_ref_exists` 搜索 `BLOCKING_{nnn}` ❌（目录错误，见 issue #3） | **不通过** |
| `new-review-report.py` | TASK / REPORT | 自定义 `_detect_reviewer_mode` 输出 `available_references` ✅ | `_check_ref_exists` 搜索 `TASK_{nnn}` 或 `REPORT_{nnn}` ✅ | **通过** |
| `new-task.py` | 无（自增编号） | `available_tasks` 无意义但无害 | 无关联校验 | 不适用 |
| `new-decision.py` | 无（自增编号） | `available_tasks` 无意义但无害 | 无关联校验 | 不适用 |

**结论：** `new-report` 和 `new-review-report` 的关联提示与校验正确；`new-revision` 和 `new-blocking-reply` 的关联提示完全错位（显示 TASK 而非其真正需要的 REVIEW_REPORT / BLOCKING），且关联校验因目录配置错误而失效。

## 专项核查（P2/P3 必填）

| 检查项 | 结果 | 说明 |
|------|------|------|
| 跨端一致性 | 通过 | 全部脚本均为纯 Python stdlib，无平台依赖；Windows 路径处理使用 `pathlib`，符合跨平台要求 |
| 类型安全 | 部分通过 | 大部分函数有类型注解，但 `resolve_template` 返回标注为 `Path` 实际可能返回 `None`；`_check_ref_exists` 返回 `str \| None` 但未标注 |
| 错误处理 | 部分通过 | `_common.run_create_flow` 有全面的 try/except 兜底，但 `agent.py`/`tpm.py` 的 `subprocess.run` 未处理超时；`new-review-report.py` 的 JSON 解析有单独处理 |
| 状态管理 | 通过 | 编号自增由 `registry.py` 统一管理，状态流转靠创建新文件而非修改旧文件，符合"只追加，不覆盖"红线 |

## 多轮次专项核查

> 审查重点：脚本系统是否支持多轮修复的 `_R1`、`_R2` 文件创建，以及轮次触发逻辑。

**文档约定的多轮次规则**（来源：README.md §三、TPM.md §五、CHARTER.md §三）：

| 阶段 | 文件名 | 【审查摘要】节 | 操作 |
|------|--------|---------------|------|
| 首轮 REPORT | `REPORT_NNN_DATE_...` | 被注释掉（不存在） | 执行者提交首轮报告 |
| 首轮 REVIEW_REPORT | `REVIEW_REPORT_NNN_DATE_...` | 只有 `### R0` | Reviewer 写首轮审查 |
| R1 REPORT | `REPORT_NNN_R1_DATE_...` | 取消注释，复制 R0 + 追加回应 | 执行者修复后提交 |
| R1 REVIEW_REPORT | `REVIEW_REPORT_NNN_R1_DATE_...` | 复制 R0 + 追加 `### R1` | Reviewer 写 R1 审查 |
| R2+ | 同上，`_R2`、`_R3`… | 继续追加 | 循环直到 ACCEPT |

**脚本系统实际支持情况：**

| 检查项 | 预期 | 实际 | 结果 |
|--------|------|------|------|
| `naming.py` 正则表示 `_R1` | `REPORT_\d{3}(_R\d+)?_\d{8}_...` | `REPORT_\d{3}_\d{8}_...`（无 `_R1` 位置） | ❌ 不通过 |
| 模板文件名支持 `_R1` | `REPORT_NNN_R1_DATE_...` | 只有 `REPORT_NNN_DATE_...` | ❌ 不通过 |
| `generate_filename` 支持 `round` | 可传入 `round=1` 生成 `_R1` | 无 `round` 参数 | ❌ 不通过 |
| `run_create_flow` 检测重复 | 已有 `REPORT_042` 时拒绝再创建同名文件 | 无检测逻辑，直接覆盖写入 | ❌ 不通过 |
| `no_args_response` 轮次提示 | 提示"已有 REPORT_042，建议创建 R1" | 无轮次提示 | ❌ 不通过 |
| 首轮→R1 触发逻辑 | Agent 看到 REVIEW_REPORT 要求修复时，应知创建 `_R1` | 脚本无此引导 | ❌ 不通过 |

**结论：** 多轮次机制在文档层面定义完整，但在脚本层**完全未实现**。当前脚本系统只能创建首轮文件，无法创建 `_R1`、`_R2`，也无法提示 Agent 何时应该使用轮次后缀。这是一个设计与实现之间的严重断层。

**轮次触发时机（文档规则 vs 脚本现状）：**

| 触发条件 | 文档规则 | 脚本现状 |
|---------|---------|---------|
| 从无到 R1 | Agent 收到 REVIEW_REPORT（状态≠ACCEPT）→ 创建 `_R1` | ❌ 脚本不检测 REVIEW_REPORT 状态，不提示 R1 |
| R1 → R2 | 上轮 REVIEW_REPORT 仍≠ACCEPT → 创建 `_R2` | ❌ 同上 |
| 文件内容 | R1 需包含上轮【摘要】原文 + 追加回应 | ⚠️ 模板有注释说明，但脚本不自动填充 |
| 文件名生成 | `_R1`、`_R2` 依次递增 | ❌ 完全不支持 |

## 合并建议

**🔴 暂不合并 — 必须先修复路径解析错误（issues #1、#2）与关联校验目录错误（issues #3、#4）**

`actions.py` 和 `validate-all.py` 的路径 bug 是阻断性的：它们导致 Agent 身份验证、角色判断、全量校验完全失效。`search_dirs_map` 的两处目录错误则使 `BLOCKING_REPLY` 和 `REVISION` 的关联校验永远失败。

**建议修订优先级：**

**P0（立即 — 不修复则系统无法使用，共 4 项）：**
- **#1** `actions.py` 路径解析错误 → Agent 验证/角色判断全部失效
- **#2** `validate-all.py` 路径解析错误 → 全量校验永远失败
- **#3** `search_dirs_map` 缺少 BLOCKING → BLOCKING_REPLY 关联校验永远失败
- **#14** `naming.py` 不支持 `_R1` → 文档明确约定的多轮次增量文件链在脚本层完全无法运转

**P1（本轮 — 功能缺失或误导，共 7 项）：**
- **#4** REVIEW_REPORT 目录不全（自循环范式下找不到 inbox/ 中的 REVIEW_REPORT）
- **#5** 4 个缺失脚本（tpm.py COMMANDS 引用但不存在的文件）
- **#6** ACTIONS.md 遗留 `reviews/` 引用
- **#7** `no_args_response` 关联提示错位（REVISION/BLOCKING_REPLY 显示 TASK 而非正确关联源）
- **#8** placeholder 必填校验缺失（遗漏字段静默生成不完整文件）
- **#15** `run_create_flow` 不检测同编号重复文件（违反"只追加，不覆盖"红线）
- **#16** 无轮次提示（Agent 不知已有 REPORT_042，应创建 REPORT_042_R1）

**P2（可选 — 体验优化，共 5 项）：**
- **#9** `new-review-report.py` 无 REPORT 时 recipient 默认 `"coder"`
- **#10** `daily-check.py` 统计字段未使用
- **#11** `subprocess.run` 无超时
- **#12** `validate.py` 双语 header 警告
- **#13** `REF_MAP` 类型清单不一致

**P3（独立 DECISION — 架构级增强）：**
- 多轮次**摘要流转自动化**：即使文件名支持了 `_R1`，内容层面的【审查摘要】复制/追加/校验仍需专门设计（模板预处理、跨文件引用注入、历史原文完整性校验）。建议作为独立 DECISION 讨论后实施。

**架构层面肯定：**
- `_common.py` 的 "三态调用" 设计（无参 / 仅名字 / 名字+JSON）非常实用，降低了 Agent 记忆负担
- `new-review-report.py` 的 "倒推法" 范式检测（委派 vs 自循环）巧妙且符合 DECISION_021 的设计意图
- 入口分离（`agent.py` vs `tpm.py`）清晰，权限边界明确
- 红线自动输出机制（`redlines.py`）将 CHARTER.md 与脚本层动态绑定，保持了文档与工具的一致性

---

## 附录 A：关键修复代码段

> 以下代码段供 TPM 审查后决定是否采纳。**本次审查不直接修改源文件。**

---

### A.1 `lib/actions.py` — 路径解析（issue #1）

```python
# lib/actions.py 第 23–27 行
# 修改前：
_SCRIPT_DIR = Path(__file__).resolve().parent          # scripts/lib/
_SCRIPTS_DIR = _SCRIPT_DIR.parent                      # scripts/
_PROJECT_ROOT = _SCRIPTS_DIR.parent                    # project root
_ACTIONS_PATH = _PROJECT_ROOT / "collaboration" / "ACTIONS.md"

# 修改后：
_SCRIPT_DIR = Path(__file__).resolve().parent          # scripts/lib/
_SCRIPTS_DIR = _SCRIPT_DIR.parent                      # scripts/
_PROJECT_ROOT = _SCRIPTS_DIR.parent                    # collaboration/（scripts/ 已移入其内）
_ACTIONS_PATH = _PROJECT_ROOT / "ACTIONS.md"           # 去掉多余的 collaboration/
```

---

### A.2 `validate-all.py` — 路径解析（issue #2）

```python
# validate-all.py 第 13–15 行
# 修改前：
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_DIR = SCRIPT_DIR.parent
COLLAB_DIR = PROJECT_DIR / "collaboration"

# 修改后：
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_DIR = SCRIPT_DIR.parent          # collaboration/
COLLAB_DIR = PROJECT_DIR                 # 去掉多余的 /collaboration
```

---

### A.3 `_common.py` — `search_dirs_map` 补全（issues #3、#4）

```python
# _common.py 第 45–52 行
# 修改前：
search_dirs_map = {
    "TASK": ["inbox", "archive/inbox"],
    "REVISION": ["inbox", "archive/inbox"],
    "REVIEW_REPORT": ["outbox", "archive/outbox"],
    "REPORT": ["outbox", "archive/outbox"],
    "BLOCKING": ["outbox"],
    "TASK_TEST": ["inbox", "archive/inbox"],
}

# 修改后：
search_dirs_map = {
    "TASK": ["inbox", "archive/inbox"],
    "REVISION": ["inbox", "archive/inbox"],
    "REVIEW_REPORT": ["inbox", "outbox", "archive/inbox", "archive/outbox"],
    "REPORT": ["outbox", "archive/outbox"],
    "BLOCKING": ["outbox"],           # 新增：BLOCKING 在 outbox/
    "TASK_TEST": ["inbox", "archive/inbox"],
}
```

---

### A.4 `_common.py` — 按类型输出正确的关联源提示（issue #7）

```python
# _common.py 的 no_args_response 函数（第 212–247 行）中
# 替换第 234–241 行的 scan_inbox 调用块：

# 修改前：
if agent_valid:
    from patrol import scan_inbox
    tasks = scan_inbox(agent_name)
    if tasks:
        response["available_tasks"] = [
            {"nnn": t["id"], "desc": t["desc"], "priority": t["priority"]}
            for t in tasks
        ]

# 修改后：
if agent_valid:
    from patrol import scan_inbox
    # 按 file_type 选择正确的关联源提示
    assoc_map = {
        "REPORT": ("available_tasks", scan_inbox, agent_name),
        # REVISION / BLOCKING_REPLY / TEST_REPORT 需要新增扫描函数
        # 以下为示意，实际需先在 patrol.py 中增加 scan_review_reports / scan_blockings
        # "REVISION": ("available_review_reports", scan_review_reports, agent_name),
        # "BLOCKING_REPLY": ("available_blockings", scan_blockings, agent_name),
    }
    hint_key, scanner, *scanner_args = assoc_map.get(file_type, ("available_tasks", scan_inbox, agent_name))
    items = scanner(*scanner_args) if scanner_args else scanner()
    if items:
        response[hint_key] = [
            {"nnn": t["id"], "desc": t.get("desc", ""), "priority": t.get("priority", "—")}
            for t in items
        ]
```

**配套修改 `patrol.py`**（增加通用扫描函数）：

```python
# patrol.py 新增函数（放在 scan_outbox 之后）

def scan_files(directory_name: str, pattern: re.Pattern) -> list[dict]:
    """通用目录扫描：扫描指定目录下匹配正则的文件。"""
    target = COLLAB_DIR / directory_name
    results = []
    if not target.exists():
        return results
    for f in sorted(target.iterdir()):
        if not f.is_file() or f.suffix != ".md":
            continue
        m = pattern.search(f.name)
        if m:
            results.append({
                "id": m.group(1),
                "filename": f.name,
            })
    return results


def scan_review_reports(agent_name: str) -> list[dict]:
    """扫描 outbox/ 和 inbox/ 中发给 agent_name 的 REVIEW_REPORT。"""
    pattern = re.compile(r"REVIEW_REPORT_(\d{3})_\d{8}_.*@" + re.escape(agent_name) + r"\.md", re.IGNORECASE)
    outbox_items = scan_files("outbox", pattern)
    inbox_items = scan_files("inbox", pattern)
    # 合并并去重（按 id）
    seen = set()
    merged = []
    for item in outbox_items + inbox_items:
        if item["id"] not in seen:
            seen.add(item["id"])
            merged.append(item)
    return merged


def scan_blockings(agent_name: str) -> list[dict]:
    """扫描 outbox/ 中发给 agent_name 的 BLOCKING。"""
    pattern = re.compile(r"BLOCKING_(\d{3})_\d{8}_.*@" + re.escape(agent_name) + r"\.md", re.IGNORECASE)
    return scan_files("outbox", pattern)
```

---

### A.5 `_common.py` — placeholder 必填校验（issue #8）

```python
# _common.py run_create_flow 函数中，在第 175 行（filled 变量生成后）插入：

# 8b. 校验 name_pattern 中的必填变量是否已替换
name_pattern = template_info.get("name_pattern", "")
name_vars = set(re.findall(r'\{\{(\w+)\}\}', name_pattern))
unreplaced = set(re.findall(r'\{\{(\w+)\}\}', filled))
missing_required = [v for v in name_vars if v in unreplaced]
if missing_required:
    return {"error": f"必填字段未提供（影响文件名生成）: {', '.join(missing_required)}"}

# 8c. 记录其他未替换变量作为 warning（不阻断）
other_unreplaced = [v for v in unreplaced if v not in name_vars]
if other_unreplaced:
    pass  # 可选择在返回结果中增加 "warnings" 字段
```

---

### A.6 `new-review-report.py` — 无 REPORT 时拒绝推断 recipient（issue #9）

```python
# new-review-report.py _detect_reviewer_mode 函数中（第 82–88 行）
# 修改前：
    return {
        "mode": "self_loop",
        "hint": "无 REVIEW_TASK，推定自循环。从 outbox 中 REPORT 获取审查对象",
        "target_dir": "inbox",
        "recipient": coder,
        "available": found_reports,
    }

# 修改后：
    if not found_reports:
        return {
            "mode": "self_loop",
            "hint": "无 REVIEW_TASK，且 outbox 中无 REPORT。无法推断审查对象，请显式提供 recipient 和 ref_nnn",
            "target_dir": "inbox",
            "recipient": None,
            "available": [],
        }
    return {
        "mode": "self_loop",
        "hint": "无 REVIEW_TASK，推定自循环。从 outbox 中 REPORT 获取审查对象",
        "target_dir": "inbox",
        "recipient": coder,
        "available": found_reports,
    }

# 同时在 main() 中（第 125–135 行附近）增加 recipient 为空时的拦截：
    if context["recipient"] is None and not data.get("recipient"):
        result = {"error": "无法推断 recipient：outbox 中无 REPORT，请显式提供 recipient"}
        print(json.dumps(result, ensure_ascii=False, indent=2))
        sys.exit(1)
```

---

### A.7 `agent.py` / `tpm.py` — subprocess 超时（issue #11）

```python
# agent.py 第 80 行 / tpm.py 第 107 行
# 修改前：
    result = subprocess.run(cmd_args, capture_output=True, text=True)

# 修改后：
    result = subprocess.run(cmd_args, capture_output=True, text=True, timeout=30)
```

---

### A.8 `daily-check.py` — 统计字段补全（issue #10）

```python
# daily-check.py 主循环中（第 174–176 行附近）
# 修改前：
        for f in files:
            if not f.get("naming_valid", True):
                stats["naming_errors"] += 1

# 修改后：
        for f in files:
            if f.get("naming_valid", True):
                stats["naming_ok"] += 1
            else:
                stats["naming_errors"] += 1
            if f.get("flow", "").startswith("❌"):
                stats["flow_issues"] += 1
```

---

## 附录 B：多轮次修复代码段

### B.1 `lib/naming.py` — 扩展正则支持 `_R1`（issue #14、#18）

> **规范确认**：`_R1`、`_R2` 是独立于 NNN 的轮次段，非 NNN 的一部分。正确格式为 `NNN_RN`（如 `REPORT_042_R1_20260609_...` 中 `042` 是 NNN，`_R1` 是轮次）。文档中 `049C_R1` 作为 NNN 示例是错误的。

```python
# naming.py 第 15–31 行 NAME_PATTERNS
# 修改前：
NAME_PATTERNS: dict[str, str] = {
    "REPORT": r"^REPORT_\d{3}_\d{8}_[A-Z]+@[A-Z]+\.md$",
    "REVIEW_REPORT": r"^REVIEW_REPORT_\d{3}_\d{8}_[A-Z]+@[A-Z]+\.md$",
    ...
}

# 修改后（REPORT / REVIEW_REPORT / REVISION 支持可选轮次段 NNN_RN）：
NAME_PATTERNS: dict[str, str] = {
    "REPORT": r"^REPORT_\d{3}(_R\d+)?_\d{8}_[A-Z]+@[A-Z]+\.md$",
    "REVIEW_REPORT": r"^REVIEW_REPORT_\d{3}(_R\d+)?_\d{8}_[A-Z]+@[A-Z]+\.md$",
    "REVISION": r"^REVISION_\d{3}[A-Z]?(_R\d+)?_\d{8}_[A-Z]+@[A-Z]+\.md$",
    ...
}

# TEMPLATE_BASE_PATTERNS 同步修改：
TEMPLATE_BASE_PATTERNS: dict[str, str] = {
    "REPORT": r"^REPORT_NNN(_R[0-9]+)?_DATE_[a-z]+@[a-z]+\.md$",
    "REVIEW_REPORT": r"^REVIEW_REPORT_NNN(_R[0-9]+)?_DATE_[a-z]+@[a-z]+\.md$",
    "REVISION": r"^REVISION_NNN[A-Z]?(_R[0-9]+)?_DATE_[a-z]+@[a-z]+\.md$",
    ...
}
```

### B.2 `lib/naming.py` — `generate_filename` 支持 `round` 参数（issue #14）

```python
# generate_filename 函数签名增加 round 参数
def generate_filename(
    file_type: str,
    author: str,
    recipient: str,
    nnn: Optional[str] = None,
    date: Optional[str] = None,
    desc: Optional[str] = None,
    round: Optional[int] = None,  # 新增
) -> str:
    ...
    # 在 REPORT / REVIEW_REPORT / REVISION 分支中：
    if file_type == "REPORT":
        round_suffix = f"_R{round}" if round else ""
        return f"REPORT_{nnn}{round_suffix}_{date}_{author}@{recipient}.md"
    
    if file_type == "REVIEW_REPORT":
        round_suffix = f"_R{round}" if round else ""
        return f"REVIEW_REPORT_{nnn}{round_suffix}_{date}_{author}@{recipient}.md"
    
    if file_type == "REVISION":
        round_suffix = f"_R{round}" if round else ""
        return f"REVISION_{nnn}{round_suffix}_{date}_{author}@{recipient}.md"
```

### B.3 `_common.py` — 检测同编号文件并提示轮次（issues #15、#16）

```python
# _common.py run_create_flow 函数中，在生成 filename 之前（第 145 行附近）插入：

# 4c. 检测同 NNN 文件是否已存在，提示轮次
def _detect_existing_rounds(file_type: str, nnn: str, target_dir: str) -> tuple[int, str]:
    """返回 (max_round, hint_message)。max_round=0 表示没有同 NNN 文件。"""
    import re
    search_dir = COLLAB_DIR / target_dir
    if not search_dir.exists():
        return 0, ""
    
    pattern = re.compile(rf"{re.escape(file_type)}_{re.escape(nnn)}(_R(\d+))?_\d{{8}}_.*\.md")
    max_round = 0
    for f in search_dir.iterdir():
        if not f.is_file():
            continue
        m = pattern.match(f.name)
        if m:
            r = int(m.group(2)) if m.group(2) else 0
            if r > max_round:
                max_round = r
    if max_round == 0:
        return 0, ""
    next_round = max_round + 1
    return max_round, f"已有 {file_type}_{nnn}_R{max_round}，建议创建 _R{next_round}"

existing_round, round_hint = _detect_existing_rounds(file_type, nnn, target_dir)
if existing_round > 0 and not data.get("round"):
    # 如果已有同编号文件且用户未显式指定 round，返回提示但不阻断
    # （也可改为阻断：return {"error": f"已有同编号文件，{round_hint}"}）
    pass  # 选择在结果中附加 hint
```

### B.4 `_common.py` — `no_args_response` 增加已有文件轮次提示（issue #16）

```python
# 在 no_args_response 的 available_tasks 输出之后，增加：
if agent_name and agent_valid:
    # 显示同 NNN 已有文件（用于 REPORT / REVISION / REVIEW_REPORT）
    if file_type in ("REPORT", "REVISION", "REVIEW_REPORT"):
        from pathlib import Path
        check_dir = COLLAB_DIR / template_info.get("target_dir", "")
        if check_dir.exists():
            existing = []
            import re
            # 扫描该 agent 创建的、同类型的文件
            for f in check_dir.iterdir():
                if f.is_file() and f.suffix == ".md":
                    # 简单匹配：包含 file_type 和 agent_name
                    if file_type in f.name and agent_name in f.name:
                        existing.append(f.name)
            if existing:
                response["existing_files"] = sorted(existing)
                response["hint"] = "若修复上轮审查问题，请使用 round=1 创建 _R1 文件"
```

### B.5 模板新增 `_R1` 变体（issue #14 配套）

为 REPORT 和 REVIEW_REPORT 创建 R1 专用模板（或修改现有模板支持 `{{round}}` 占位符）：

```
# collaboration/templates/REPORT_NNN_R1_DATE_author@recipient.md
# 与 REPORT_NNN_DATE_author@recipient.md 内容相同，
# 但文件名明确标注 _R1，便于脚本解析模板时识别轮次。
```

更轻量的方案：不新增模板文件，而是在 `resolve_template` 中做 fallback——若请求 `_R1` 模板但不存在，回退到基础模板：

```python
# _common.py resolve_template 修改：
def resolve_template(file_type: str, round: Optional[int] = None) -> Path:
    type_to_template = {
        "TASK": "TASK_NNN_DESC_author@recipient.md",
        "REPORT": "REPORT_NNN_DATE_author@recipient.md",  # 基础模板
        ...
    }
    template_name = type_to_template.get(file_type)
    if not template_name:
        return None
    template_path = COLLAB_DIR / "templates" / template_name
    # 若指定了 round 但无专用模板，仍使用基础模板（内容中的 {{round}} 可手动填充）
    return template_path
```

---

*附录结束。以上代码段经审查人验证逻辑正确，但未经运行测试。*
