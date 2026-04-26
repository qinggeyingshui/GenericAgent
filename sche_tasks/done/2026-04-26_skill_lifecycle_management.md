# Skill Tree 生命周期检查报告

生成时间: 2026-04-26 16:31
检查范围: 排除meta_capability（核心能力不参与检查）

## 统计摘要

| 指标 | 数值 |
|------|------|
| 检查skill数 | 40 |
| 类别数 | 7 |
| 健康率 | 85.0% |

### 各类别分布
- content_creation: 13个
- media_processing: 7个
- data_analysis: 6个
- document_generation: 5个
- knowledge_management: 4个
- web_automation: 3个
- system_monitoring: 2个

## 删除建议

### 观察中 (15个)

- `knowledge_management/paper_comparison_sop (last: 2026-04-20, tools: 1, funcs: 4)`
- `document_generation/document_conversion_sop (last: 2026-04-20, tools: 1, funcs: 4)`
- `media_processing/image_processing_sop (last: 2026-04-20, tools: 1, funcs: 10)`
- `media_processing/subtitle_proofreading_sop (last: 2026-04-20, tools: 1, funcs: 12)`
- `content_creation/ai_copywriting_sop (last: 2026-04-20, tools: 1, funcs: 4)`
- `content_creation/platform_adaptation_sop (last: 2026-04-20, tools: 1, funcs: 3)`
- `content_creation/community_management_sop (last: 2026-04-20, tools: 2, funcs: 15)`
- `content_creation/live_streaming_sop (last: 2026-04-20, tools: 1, funcs: 5)`
- `content_creation/content_calendar_sop (last: 2026-04-26, tools: 1, funcs: 0)`
- `content_creation/monetization_sop (last: 2026-04-26, tools: 1, funcs: 0)`
- `data_analysis/data_analysis_sop (last: 2026-04-20, tools: 2, funcs: 9)`
- `data_analysis/fan_analytics_sop (last: 2026-04-26, tools: 1, funcs: 0)`
- `web_automation/web_automation_sop (last: 2026-04-20, tools: 2, funcs: 18)`
- `system_monitoring/system_monitoring_sop (last: 2026-04-20, tools: 2, funcs: 18)`
- `system_monitoring/log_analysis_sop (last: 2026-04-20, tools: 1, funcs: 10)`

## 其他问题 (9项)

### 工具文件缺失 (6项)
- `knowledge_management/teaching_kb_sop`: teaching_kb/, temp/tools/kb_qa.py, temp/tools/multimodal_search.py
- `document_generation/ppt_com_sop`: Marp CLI
- `content_creation/content_creation_sop`: script_generator.py
- `content_creation/ab_testing_sop`: ab_testing.py
- `content_creation/monetization_sop`: monetization_toolkit.py
- `web_automation/seo_optimization_sop`: temp/tools/seo_toolkit.py

### 孤儿函数 (3项)
- `knowledge_management/teaching_kb_sop`: 6个
- `content_creation/content_creation_sop`: 5个
- `content_creation/ab_testing_sop`: 12个


---
*本报告由定时任务自动生成，所有清理操作需用户确认后手动执行*
