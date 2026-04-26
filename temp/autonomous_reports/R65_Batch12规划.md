# R65 - Batch12 任务规划
日期: 2026-03-26

## 质量基线
quality_scorer_v2 (2026-03-26): 47条记录 | 平均5.66分 | 低分18条(38%) | 高分11条(23%)
改进方向：低分率偏高，需提升产出完整性和可验证性

## 现状盘点
### teaching_kb
- GNN课程：L01✓(教案无PPT) | L02✓(教案+PPT) | L03✓(教案无PPT)
- 编译原理：L01✓(教案+PPT) | L02✓(教案+PPT)
- 空缺：GNN L04尚未建立，GNN L01/L03无配套PPT

### ppt_lab/output (9个文件)
L02_GNN基础.pptx(46KB) | GNN_Beautiful_v2.pptx(44KB) | 夏令营×2 | 编译原理×2 | 测试×3

### 论文库
gnn_papers/PAPERS.md: 5篇，均含code_url+applications(R63完成)

## Batch12任务列表
价值公式: AI训练数据无法覆盖 × 对未来协作有持久收益

1. [9分] 产出 | L03教案→PPT自动生成 | 用lesson2ppt.py读L03/lesson_plan.md生成L03_图注意力网络.pptx
   验收：ppt_lab/output/L03_图注意力网络.pptx存在且≥8页

2. [8分] 产出 | GNN课程L04教案新建 | 主题：GNN+LLM联合架构/GraphRAG应用
   对齐L01-L03结构(lesson_plan.md+materials_index.md)，引用PAPERS.md中GraphRAG论文
   验收：teaching_kb/courses/图神经网络与大语言模型/lessons/L04/含两文件字数≥1500

3. [7分] 产出 | L01教案→PPT自动生成 | 用lesson2ppt.py读L01/lesson_plan.md生成L01_GNN与LLM导论.pptx
   验收：ppt_lab/output/L01_GNN与LLM导论.pptx存在且≥8页

4. [7分] 产出 | lesson2ppt批量转换工具改进 | 支持批量输入目录自动扫描lesson_plan.md并生成PPT
   在lesson2ppt.py中加入batch_mode，验收：一条命令生成指定课程全部lesson的PPT

5. [6分] 探测 | 低分报告共性分析 | 读quality_report_v2.html提取低分18条的共性缺陷
   生成改进指南improvement_guide.md，验收：列出≥3条可操作改进建议

## 执行顺序
1→3→2→4→5 (PPT产出优先，工具改进次之，分析收尾)

## 记忆更新建议
L2 USER_PROFILE可补充：teaching_kb GNN课程目标L01-L06，当前完成L01-L03
