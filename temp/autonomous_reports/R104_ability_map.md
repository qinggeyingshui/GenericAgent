# R104 — local_skills 能力树可视化

**日期**: 2026-03-26
**类型**: 产出
**状态**: 完成

## 任务目标
扫描 local_skills/ + temp/ 下所有主要 .py 工具文件，提取函数签名+docstring，
生成 ability_map.md 按类别归组，方便快速查阅可用工具。

## 执行过程

1. 用 `ast.parse` 遍历 local_skills/ 和 temp/ 下所有非临时 .py 文件
2. 提取每个函数的名称、参数列表、docstring首行
3. 按5大类别归组写入 ability_map.md

## 产出

| 文件 | 大小 | 行数 | 函数条目 |
|------|------|------|---------|
| `temp/ability_map.md` | 7133B | 164行 | 75条 |

## 覆盖分类

| 类别 | 文件数 | 函数数 |
|------|--------|--------|
| 论文/知识库 | 4 | 15 |
| PPT制作 | 1+pptx | 20+ |
| Word文档 | 2 | 16 |
| 系统/文件 | 3 | 13 |
| 自主任务辅助 | 2 | 8 |
| **合计** | **12** | **75** |

覆盖率：扫描到的所有有docstring函数均已收录，
build_gnn_ppt*.py/gnn_pptx.py等实验脚本因函数名过短无文档未纳入主索引（附注说明）。

## 关键发现

- ppt_com_toolkit.py 是最大工具文件，20+函数，但**缺少图表能力**
  → 本次对话中已用 python-pptx 补充，验证通过（test_chart_pptx.pptx 34572B）
- local_skills/ 目前只有2个SKILL，能力扩展空间大
  → 建议后续增加 image_search.py（图片搜索/下载）
- word_toolkit.py 的 add_bullet_list 在中文Word下有已知BUG，已在ability_map中标注

## 建议记忆更新

- Insight 增加：`能力树索引: temp/ability_map.md(12文件75函数,按论文/PPT/Word/系统/自主分类)`
