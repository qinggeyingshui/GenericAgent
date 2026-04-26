# R184 - Batch 16 技能拓展规划

## 执行信息
- 时间: 2026-04-21
- 类型: 规划
- 来源: skill_planning_sop.md v2.0

## 数据基础

### Skill Tree 现状
- 总技能数: 54
- 总类别数: 13
- 平均每类别技能数: 4.15
- 最大使用次数: 8 (presentation)

### 高频技能 (>3次)
- presentation: 8次 (document_generation)
- browser_control: 5次 (web_automation)
- paper_acquisition: 4次 (knowledge_management)
- knowledge_search: 4次 (knowledge_management)

### 零使用类别
ai_capability, automation, development, meta_capability, system_control, system_monitoring

### 用户画像
- 长期目标: 自媒体创作大师，靠自媒体获取收益
- 兴趣: 自媒体创作
- 最近任务: R183自媒体内容生产流水线

## 4维度评分

| 任务 | 类型 | B | D | U | I | 综合 |
|------|------|---|---|---|---|------|
| PPT模板市场爬取与管理 | B类 | 0.00 | 18.89 | 8.00 | 4.00 | 6.98 |
| 评论区互动助手 | A类 | 10.00 | 0.00 | 8.00 | 7.00 | 6.80 |
| 知识库多模态检索 | B类 | 0.00 | 12.22 | 7.00 | 8.00 | 6.14 |
| 短视频批量发布工具 | B类 | 0.00 | 7.78 | 10.00 | 5.00 | 5.56 |
| 直播脚本生成与提词器 | A类 | 0.00 | 1.11 | 9.00 | 6.00 | 4.12 |
| 自媒体运营看板Workflow | C类 | 0.00 | 1.11 | 9.00 | 5.00 | 3.92 |

## 去重验证

### 1. PPT模板市场爬取与管理 (document_generation)
- 现有: ppt_template_manager.py (本地模板管理)
- 差异: 新增网络爬取+批量下载功能，现有仅本地管理
- 结论: ✅ 通过

### 2. 评论区互动助手 (community_management)
- 现有: 无此类别
- 差异: 全新领域，自媒体运营核心能力
- 结论: ✅ 通过 (新领域)

### 3. 知识库多模态检索 (knowledge_management)
- 现有: knowledge_search (R173文本TF-IDF检索)
- 差异: 新增图片/表格/公式的OCR+向量化检索
- 结论: ✅ 通过

### 4. 短视频批量发布工具 (web_automation)
- 现有: content_publisher.py (R156微信公众号)
- 差异: 新增抖音/快手/B站短视频平台支持
- 结论: ✅ 通过

### 5. 直播脚本生成与提词器 (content_creation)
- 现有: script_generator.py (R157视频脚本)
- 差异: 直播场景需实时提词+互动话术，与视频脚本不同
- 结论: ✅ 通过

### 6. 自媒体运营看板Workflow (content_creation)
- 现有: media_analytics, trend_tracker, platform_adapter
- 差异: Workflow任务，串联已有工具成端到端流程
- 结论: ✅ 通过 (C类Workflow)

## 最终方案

选择全部6个任务，理由：
1. 全部通过去重验证
2. 符合1个新领域约束 (community_management)
3. 包含1个C类Workflow任务
4. 聚焦用户目标 (自媒体创作)
5. 深化高频技能 (presentation 8次, browser_control 5次)

### 任务分布
- A类 (新SOP): 2个
- B类 (增强): 3个
- C类 (Workflow): 1个
- 新领域: 1个 (community_management)
- 已有领域: 5个

## 产出

已生成 temp/TODO.txt，包含6条任务

## 验收

- [x] 数据准备完整 (skill_tree + USER_PROFILE + 历史任务)
- [x] 4维度评分精确到小数点
- [x] 去重验证章节完整
- [x] 新领域≤1个
- [x] 包含1个C类Workflow
- [x] 文件名为TODO.txt
- [x] 所有任务满足问题映射约束