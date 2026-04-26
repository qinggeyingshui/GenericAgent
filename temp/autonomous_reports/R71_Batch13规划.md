# R71 | Batch13 规划报告

## 背景
- Batch12 全部完成（R65-R70），5条TODO全[x]
- 用户明确指令：空闲时拓展PPT制作能力，包括本地PowerPoint和在线Canva
- improvement_guide.md建议：优先产出类、明确验收标准、低分率目标<20%

## Batch13 规划原则
1. PPT能力扩展为核心主线（响应用户指令）
2. 每条TODO含明确可验证文件产出
3. 兼顾GNN教案知识库完善

## Batch13 TODO 条目（5条）

| # | 类型 | 主题 | 验收 |
|---|------|------|------|
| 1 | 产出 | win32com高级PPT能力（图片/SmartArt模拟/母版） | demo_advanced.pptx>=5页>=100KB |
| 2 | 探测 | Canva Connect API能力评估+接入方案 | canva_api_guide.md含OAuth流程+2个API端点 |
| 3 | 产出 | python-pptx教学模板（4种版式） | template_teaching.pptx含>=4个版式 |
| 4 | 产出 | L02教案topic修复+PPT生成 | L02/slides/下.pptx>=15页 |
| 5 | 产出 | GNN课程L05教案新建 | L05目录含两文件>=2000字 |

## 执行顺序
2→1→3→4→5（先探测Canva，再做本地PPT能力，最后教案）

## 核心发现
1. task_planning.md实际位于./autonomous_reports/（非./autonomous_operation_sop/），SOP路径描述有误
2. Batch12低分率偏高的主要原因已由improvement_guide.md归纳：知识密度不足+纯探测无结论
3. 用户PPT指令优先级高，Batch13以PPT能力扩展占3/5条目

## 记忆更新建议
- ppt_com_sop.md可在Batch13 win32com任务后追加新能力（图片插入/母版操作）
- task_planning.md路径需在autonomous_operation_sop中更正（待用户审批）