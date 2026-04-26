# R78 Batch14 任务规划

**日期**: 2026-03-26
**任务类型**: 规划
**前序**: Batch13(R71-R77)全部完成，PPT能力已覆盖win32com/python-pptx/Canva评估/美化升级

## 现状分析

### 已具备能力
- win32com: 图片/SmartArt模拟/多配色/母版操作 (R73)
- python-pptx: 模板/渐变/卡片/图表/14种页面类型 (R74, R77)
- 教案→PPT管道: lesson2ppt.py批量转换 (R70)
- 课程内容: GNN课程L01-L05完整教案+PPT (R66-R76)
- Canva: API方案已评估，待OAuth credentials (R72)

### 待深化方向
1. **课程扩展**: 编译原理L03+以后的教案尚未建立
2. **PPT动画**: win32com动画效果API未探索
3. **图表增强**: python-pptx Chart类型(折线/饼图/散点)实战
4. **PPT→HTML**: 将PPT内容导出为可发布HTML讲义
5. **全课程批量PPT**: 一键生成GNN+编译原理所有课程PPT

## Batch14 任务列表（5条）

### 执行顺序: 1→2→3→4→5

1. **探测** | 编译原理L03词法分析自动机教案新建 |
   主题：正则表达式→NFA→DFA转换，状态自动机理论；对齐L01/L02结构 |
   验收：L03目录含lesson_plan.md(>=1500字)+materials_index.md

2. **产出** | python-pptx图表页深化 |
   在ppt_utils.py add_chart_slide中实现折线图/饼图/柱状图3种真实数据图表；输出demo_charts.pptx(>=3页) |
   验收：demo_charts.pptx存在且含3种不同图表类型

3. **产出** | win32com PPT动画效果API |
   实现进入/退出/路径3类动画效果，封装add_animation()到ppt_com_toolkit.py；输出demo_animation.pptx |
   验收：demo_animation.pptx存在，ppt_com_toolkit.py含add_animation函数

4. **产出** | 编译原理L03教案→PPT生成 |
   基于新建L03教案跑lesson2ppt.py生成PPT(>=12页) |
   验收：L03/slides/下存在.pptx文件>=12页

5. **探测** | PPT→Markdown讲义导出工具 |
   用python-pptx读取PPT内容，导出结构化Markdown讲义；输出ppt2md.py工具脚本 |
   验收：ppt2md.py存在，能从L05 PPT导出>=10条知识点的md文件

## 价值评估
- 条目1/4: 教案知识库扩充，AI训练数据收益高
- 条目2/3: PPT制作能力纵深，工具性强
- 条目5: PPT→讲义新管道，未来复用价值高

## 记忆更新建议（待用户审查）
- 无需更新L2，当前PPT API记录已充分