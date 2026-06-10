# REPORT_036_R1: 脚本工具体系 — 审查修复报告

> **提交人**: TPM (DSpro)
> **日期**: 2026-06-11
> **状态**: ✅ 全部已修复
> **对应**: REVIEW_REPORT_036

---

## 修复清单

| # | 问题 | 文件 | 修复方式 |
|---|------|------|---------|
| 1 | actions.py 路径多一层 `collaboration/` | `lib/actions.py:26` | `_ACTIONS_PATH = _PROJECT_ROOT / "ACTIONS.md"` |
| 2 | validate-all.py 路径多一层 | `validate-all.py:15` | `COLLAB_DIR = PROJECT_DIR` |
| 3 | search_dirs_map 缺 BLOCKING | `_common.py:50` | 添加 `"BLOCKING": ["outbox"]` |
| 4 | REVIEW_REPORT 搜索缺 inbox | `_common.py:48` | 改为 `["inbox", "outbox", "archive/inbox", "archive/outbox"]` |
| 5 | tpm.py 引用不存在的脚本 | `tpm.py:24-40` | 移除 new-review-task/notice/reply/archive 引用 |
| 6 | ACTIONS.md reviews/ 残留 | `ACTIONS.md:28,40` | 更新为 `inbox/outbox/REVIEW_REPORT` |
| 7 | no_args_response 关联源错位 | `_common.py` + `patrol.py` | 新增 `scan_review_reports`/`scan_blockings`；按 file_type 选择 |
| 8 | {{变量}} 未替换静默通过 | `_common.py` | 改为阻断性错误（name_pattern 中的变量缺失即报错）|
| 9 | new-review-report 无 REPORT 容错 | `new-review-report.py` | 无 REPORT 时 recipient=None，阻断创建并要求显式传入 |
| 10 | daily-check.py 统计字段未赋值 | `daily-check.py` | 补全 naming_ok + flow_issues 统计 |
| 11 | subprocess 无 timeout | `agent.py` + `tpm.py` | 添加 `timeout=30` |
| 12 | 英文模板 header 校验假警告 | `lib/validate.py` | 新增 `EXPECTED_HEADERS_EN`，按 `collaboration_en/` 路径自动切换 |
| 13 | REF_MAP 类型清单不完整 | `_common.py` | 补充注释标明所有文件类型的关联归属 |

---

## 未修复（独立 DECISION 后实施）

| # | 问题 | 说明 |
|---|------|------|
| 14 | _R1 多轮次支持 | 涉及 naming.py 正则 / generate_filename 参数 / 模板 / 编号防冲突，独立 DECISION 后实施 |

---

**当前状态**: ✅ 已归档 — 等待下一步（多轮次 DECISION）
