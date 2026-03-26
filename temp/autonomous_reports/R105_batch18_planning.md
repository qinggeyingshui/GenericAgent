# R105 — Batch18 任务规划

**日期**: 2026-03-26
**类型**: 规划
**状态**: 完成

## 背景
Batch17（R98-R104）全部6条TODO已完成。依据SOP，无TODO时执行规划任务生成下一批次。

## Batch17回顾与反思

| 完成项 | 评价 |
|--------|------|
| GNN论文库补全GIN/MPNN/OGB | 补齐缺失，PAPERS.md现16篇 |
| kb_cli.py CLI工具 | 查询便捷，与crossref联动 |
| arxiv2kb.py 抓取pipeline | 支持URL/ID，自动去重 |
| PATH修复 | USER PATH 22→15条，SYSTEM待管理员执行 |
| lesson2word.py 教案→Word | 全流程验证，坑已记录 |
| ability_map.md 能力树 | 75函数5分类，快速查阅 |

**主要缺口**：
1. PPT图表能力仅验证，未封装为可复用函数
2. local_skills只有2个SKILL，无图片搜索能力
3. ppt_com_toolkit缺更多AutoShape类型
4. GNN论文库停留在16篇，2025年新论文未入库

## Batch18规划（TODO.txt已写入）

| # | 方向 | 核心产出 | 验收标准 |
|---|------|---------|---------|
| 1 | PPT图表封装 | add_chart()函数入ppt_com_toolkit | 4种图表类型，test_charts.pptx>30KB |
| 2 | AutoShape扩展 | add_shape()函数，6种类型 | test_shapes.pptx验证通过 |
| 3 | 图片搜索SKILL | local_skills/image_search.py | search()返回本地图片路径 |
| 4 | 教案PPT生成器 | lesson2ppt.py | L01.pptx>=8张，>50KB |
| 5 | 2025新论文入库 | arXiv批量抓取>=5篇 | PAPERS.md>=21篇 |
| 6 | PPT制作SOP深化 | ppt_com_sop.md完整指南 | >100行，含布局/配色/动画 |

## 规划依据
- 用户明确关注PPT/Office能力（条目1/2/4/6优先）
- 价值公式：AI难覆盖的Office自动化实战经验
- 工具联动：图表+图片+论文库→完整教案PPT一键生成
