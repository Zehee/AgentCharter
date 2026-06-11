# TEST_REPORT_NNN: {{title}} — {{overall_conclusion}}

> **文件名**: `TEST_REPORT_NNN_DATE_author@recipient.md`
> **存放位置**: `outbox/`
> **命名约束**: 段间 `_`，段内 `-`。`NNN`=对应测试任务序号，`DATE`=提交日期 `YYYYMMDD`，`AUTHOR`=测试员标识（大写）

**测试员**: {{author}}
**日期**: {{DATE}}
**对应**: {{ref_nnn}}
**测试类型**: {{test_type}}
**总体结论**: {{conclusion}}

---

## 环境信息

| 项 | 值 |
|---|---|
| **操作系统** | {{os_value}} |
| **App 版本** | {{app_version_value}} |
| **运行方式** | {{run_mode_value}} |
| **屏幕分辨率** | {{screen_resolution_value}} |
| **浏览器/CDP** | {{browser_cdp_value}} |
| **后端构建** | {{backend_build_value}} |
| **前端构建** | {{frontend_build_value}} |

---

## 验证清单

> 逐项执行测试场景，标记结果。PASS=符合预期，FAIL=不符合，N/A=不适用，BLOCK=被阻塞无法执行。

### {{module_name_1}}

| # | 场景 | 操作步骤 | 预期结果 | 结果 | 备注 |
|---|------|----------|----------|------|------|
| {{test_num_1_1}} | {{scenario_1_1}} | {{steps_1_1}} | {{expected_1_1}} | {{result_1_1}} | {{note_1_1}} |
| {{test_num_1_2}} | {{scenario_1_2}} | {{steps_1_2}} | {{expected_1_2}} | {{result_1_2}} | {{note_1_2}} |

### {{module_name_2}}

| # | 场景 | 操作步骤 | 预期结果 | 结果 | 备注 |
|---|------|----------|----------|------|------|
| {{test_num_2_1}} | {{scenario_2_1}} | {{steps_2_1}} | {{expected_2_1}} | {{result_2_1}} | {{note_2_1}} |

---

## 缺陷清单

> 所有 FAIL/BLOCK 项必须在此详细记录。如未发现缺陷，写「本次测试未发现缺陷」。

### 🔴 {{bug_title_1}}

| 字段 | 内容 |
|------|------|
| **严重级别** | {{severity_1}} |
| **阶段** | {{phase_1}} |
| **复现步骤** | {{repro_steps_1}} |
| **实际现象** | {{actual_behavior_1}} |
| **预期行为** | {{expected_behavior_1}} |
| **截图/录屏** | {{screenshot_1}} |
| **根因分析** | {{root_cause_1}} |
| **修复建议** | {{fix_suggestion_1}} |
| **关联任务** | {{related_task_1}} |

### 🟡 {{bug_title_2}}

{{bug_2_details}}

---

## 已确认功能（通过项汇总）

> 记录本次测试中验证通过的关键功能点，供后续回归测试参考。

| # | 功能点 | 验证方式 | 结果 |
|---|--------|----------|------|
| {{confirmed_num}} | {{feature_point}} | {{verification_method}} | {{result}} |

---

## 已知限制 & 未测项

| # | 限制/未测项 | 原因 | 计划 |
|---|-------------|------|------|
| {{limit_num}} | {{limit_item}} | {{limit_reason}} | {{limit_plan}} |

---

## 测试数据统计

| 维度 | 数值 |
|------|------|
| 总验证项数 | {{total_items}} |
| PASS | {{pass_count}} |
| FAIL | {{fail_count}} |
| BLOCK | {{block_count}} |
| N/A | {{na_count}} |
| 🔴 严重缺陷 | {{critical_count}} |
| 🟡 一般缺陷 | {{major_count}} |
| 💡 建议项 | {{suggestion_count}} |

---

## 结论与建议

**总体结论**: {{final_conclusion}}

**结论理由**:
{{conclusion_reason}}

**下一步行动**:
- [ ] {{next_action_1}}
- [ ] {{next_action_2}}
- [ ] {{next_action_3}}

---

## 附录

### A. 截图目录
```
{{screenshot_dir}}
```

### B. 自动化测试输出（如适用）
```
> （粘贴测试框架的输出摘要，或注明输出文件位置）
{{auto_test_output}}
```

### C. 备注
> （任何不适合放在正文的补充信息）
{{appendix_notes}}
