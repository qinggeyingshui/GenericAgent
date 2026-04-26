# R83 PPT→Markdown讲义导出工具

**日期**: 2026-03-26
**任务类型**: 探测+产出
**状态**: 验收通过

## 任务目标
用python-pptx读取PPT，导出结构化Markdown讲义；输出ppt2md.py
验收：ppt2md.py存在，能从L05 PPT导出>=10条知识点的md

## 成果
- 工具文件: teaching_kb/ppt2md.py (155行)
- 测试输出: L05_讲义.md (105行，25条知识点)
- 输出路径: teaching_kb/courses/图神经网络与大语言模型/lessons/L05_图神经网络前沿/L05_讲义.md

## 核心设计
1. extract_slide_texts(slide): 遍历所有shape，提取(level, text)对，过滤空文本/纯emoji/纯数字
2. classify_slide(idx, texts): 识别封面/目录/流程总览/内容页4类
3. ppt_to_markdown(pptx_path): 主函数，输出含元数据+分章节内容+知识点汇总的Markdown
4. CLI: python ppt2md.py <input.pptx> [output.md|--stdout]

## 技术坑
- prs.slides不支持切片[:n]，需用enumerate(prs.slides)迭代
- emoji过滤正则需覆盖\U0001F000-\U0001FFFF+\u2600-\u27FF+\U0001F300-\U0001F9FF多个范围
- 所有文本段落level均为0（本PPT模板特性），不影响基础功能

## 验收结果
| 验收项 | 结果 |
|--------|------|
| ppt2md.py存在 | PASS |
| 从L05 PPT导出>=10条知识点 | PASS (25条) |
| 输出格式结构化Markdown | PASS (105行) |