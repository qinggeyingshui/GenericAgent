# R106 — ppt_chart_toolkit.py：add_chart()图表封装

**日期**: 2026-03-26
**类型**: 产出
**状态**: 完成

## 任务目标
将 python-pptx 图表能力封装为统一接口 add_chart()，支持 COLUMN/BAR/LINE/PIE 四种类型。

## 产出

| 文件 | 大小 |
|------|------|
| `temp/ppt_chart_toolkit.py` | 2353B, 75行 |
| `temp/ppt_lab/test_charts.pptx` | 56308B (54KB), 4张幻灯片 |

## API 设计

    add_chart(slide, chart_type, data, l, t, w, h, title)
    chart_type: "COLUMN" | "BAR" | "LINE" | "PIE"
    data: {"categories": [...], "series": {"系列名": [值,...]}}
    l, t, w, h: 英寸（左/上/宽/高）

辅助函数：new_prs() / add_blank_slide(prs) / save_prs(prs, path)
常量：CHART_COLUMN / CHART_BAR / CHART_LINE / CHART_PIE

## 验证内容
- 柱状图：5个GNN模型，2个系列对比
- 条形图：4个数据集准确率对比
- 折线图：2017-2023年GNN论文增长趋势
- 饼图：GNN应用方向分布

## 设计决策
- 独立新建 ppt_chart_toolkit.py（不修改 ppt_com_toolkit.py），职责分离
- 使用 python-pptx（非 win32com），避免 AddChart2 需要 visible 窗口的已知坑
- data 格式简洁，支持多系列

## 记忆更新建议
- Insight 更新：PPT制作行增加 ppt_chart_toolkit.py(add_chart/4种类型/python-pptx)
