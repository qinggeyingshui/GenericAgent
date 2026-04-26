# memory_health_report — 2026-03-25 18:59

## 扫描概况
- 扫描目录: `../memory/`
- 文件总数: 19 个
- 发现问题: 8 条（空文件2+重复key2+零访问4+其他）

## 问题清单

| 类型 | 文件 | 描述 |
|------|------|------|
| `EMPTY` | `autonomous_operation_sop` | 文件大小为0，内容为空 |
| `EMPTY` | `skill_search` | 文件大小为0，内容为空 |
| `DUP_KEY` | `autonomous_operation_sop` | 无扩展名文件与 autonomous_operation_sop.md 同时存在，造成key重复污染 |
| `NO_EXT` | `skill_search` | 无扩展名文件，可能是误创建的空占位符 |
| `ZERO_ACCESS` | `adb_ui.py` | 从未被访问(file_access_stats无记录)，可能是孤立/过时SOP |
| `ZERO_ACCESS` | `ljqCtrl.py` | 从未被访问(file_access_stats无记录)，可能是孤立/过时SOP |
| `ZERO_ACCESS` | `ljqCtrl_sop.md` | 从未被访问(file_access_stats无记录)，可能是孤立/过时SOP |
| `ZERO_ACCESS` | `mem_scanner_sop.md` | 从未被访问(file_access_stats无记录)，可能是孤立/过时SOP |

## 优化建议

1. 删除/合并空文件: autonomous_operation_sop, skill_search (0字节，无内容价值)
2. 统一key命名：删除无扩展名占位符 autonomous_operation_sop, skill_search，仅保留.md版本
3. 评估零访问SOP: adb_ui.py, ljqCtrl.py, ljqCtrl_sop.md, mem_scanner_sop.md 等4个，考虑归档或删除
4. 为零引用SOP添加场景说明，或在insight中补充索引条目
5. 建立定期健康检查机制（每Batch运行一次本脚本）

## 文件清单（含大小）

| 文件名 | 大小 | 状态 |
|--------|------|------|
| `adb_ui.py` | 3512B | ✅ |
| `autonomous_operation_sop` | 0B | ⚠️空 |
| `autonomous_operation_sop.md` | 2178B | ✅ |
| `file_access_stats.json` | 1285B | ⚪ |
| `global_mem.txt` | 2455B | ⚪ |
| `global_mem_insight.txt` | 1767B | ⚪ |
| `ljqCtrl.py` | 6067B | ✅ |
| `ljqCtrl_sop.md` | 2794B | ✅ |
| `mem_scanner.py` | 5069B | ✅ |
| `mem_scanner_sop.md` | 4329B | ✅ |
| `memory_management_sop.md` | 5920B | ✅ |
| `plan_sop.md` | 3091B | ✅ |
| `scheduled_task_sop.md` | 1068B | ✅ |
| `skill_search` | 0B | ⚠️空 |
| `subagent_sop.md` | 4670B | ✅ |
| `task_design_sop.md` | 2560B | ✅ |
| `teaching_kb_sop.md` | 4731B | ✅ |
| `tmwebdriver_sop.md` | 7439B | ✅ |
| `web_setup_sop.md` | 4044B | ✅ |

_由 memory_health_checker.py 生成 | Batch8 TODO#5_
