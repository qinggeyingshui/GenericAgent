# R109 教案PPT生成器 — L01_GNN导论.pptx

## 任务
TODO4: lesson2ppt.py生成L01_GNN导论.pptx >= 8张, > 50KB

## 结果
- 文件: teaching_kb/courses/图神经网络与大语言模型/lessons/L01_GNN与LLM联合架构导论/slides/L01_GNN导论.pptx
- 幻灯片: 10张
- 文件大小: 55.2 KB (56481 bytes) OK
- git commit: 576db01

## 幻灯片内容
S1 封面 | S2 教学目标 | S3 课程大纲 | S4 GNN基础回顾
S5 LLM在MAS中的角色 | S6 MASPOB框架 | S7 实验结果(含柱状图+折线图)
S8 架构展望 | S9 课堂练习与总结 | S10 结语

## 技术方案
- lesson2ppt.py依赖ppt_lab(不存在)无法用
- 直接python-pptx: R(矩形)+T(文本框)+ChartData(图表)
- 脚本超长截断问题: 分段写gen_l01.py(Part1+Part2)再执行
- 关键坑: code_run回复正文代码块>~300行会被系统截断，必须用分段写文件+执行

## 完成时间
2026-03-26 23:09