# R103 - GNN教案→Word讲义自动生成器 lesson2word.py

**日期**: 2026-03-26
**任务**: TODO条目5 - GNN教案→Word讲义自动生成器

## 执行结果

**验收通过**: lesson2word.py 存在，L01_GNN导论_讲义.docx 生成成功(14889 bytes)。

## 产出文件

- `temp/lesson2word.py` — 教案→Word讲义转换工具
- `teaching_kb/courses/图神经网络与大语言模型/lessons/L01_GNN与LLM联合架构导论/L01_GNN导论_讲义.docx` — 验证输出讲义

## 关键实现

### 功能
- 读取 L01 lesson_plan.md，将教案结构转换为格式化Word讲义
- 支持：封面、教学目标、重难点、教学过程（5节）、论文引用表格、作业、参考资料
- 命令行调用：`python lesson2word.py [md路径] [输出路径]`，无参数默认生成L01

### 核心坑点（已解决）
- **中文Word List Bullet样式名问题**：`doc.Styles("List Bullet")` 在中文版Word中报错「集合所要求的成员不存在」
- **解决方案**：改用 `add_bullets()` 函数，直接操作 Paragraphs.Add() + LeftIndent + "·  " 前缀，完全绕过样式名

### word_toolkit.py 兼容性
- `add_bullet_list()` 在中文Word环境下不可用（样式名硬编码为英文）
- 建议后续更新 word_toolkit.py 的 add_bullet_list，改用 ListNum 或直接段落格式

## 记忆更新建议
- ppt_com_sop.md 或 word相关SOP中补充：中文Word环境下 "List Bullet" 样式不存在，用段落+前缀替代