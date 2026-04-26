# Data Visualization Toolkit

数据可视化工具包，基于 matplotlib，支持常用图表类型。

## 功能

- **折线图** (line_chart): 趋势分析、多系列对比
- **柱状图** (bar_chart): 类别对比、横向/纵向显示
- **饼图** (pie_chart): 占比分析、突出显示
- **散点图** (scatter_plot): 相关性分析、分布可视化
- **多系列柱状图** (multi_series_bar): 分组对比、年度对比

## 安装依赖

```bash
pip install matplotlib numpy
```

## 快速开始

```python
from data_visualization import line_chart, bar_chart, pie_chart

# 折线图
line_chart(
    {'Sales': [100, 150, 120, 180], 'Target': [120, 120, 120, 120]},
    title="Monthly Sales",
    output_path="sales.png"
)

# 柱状图
bar_chart(
    ['Q1', 'Q2', 'Q3', 'Q4'],
    [250, 300, 280, 350],
    title="Quarterly Revenue",
    output_path="revenue.png"
)

# 饼图
pie_chart(
    ['A', 'B', 'C', 'D'],
    [30, 25, 20, 25],
    title="Market Share",
    output_path="share.png"
)
```

## API 文档

### line_chart()
生成折线图，支持多系列数据。

**参数**:
- `data`: 数据字典，格式 `{'label': [values]}`
- `title`: 图表标题
- `xlabel/ylabel`: 坐标轴标签
- `output_path`: 输出文件路径
- `figsize`: 图表大小 (宽, 高)
- `grid`: 是否显示网格

### bar_chart()
生成柱状图，支持横向/纵向显示。

**参数**:
- `categories`: 类别列表
- `values`: 数值列表
- `horizontal`: 是否横向显示
- `color`: 柱子颜色

### pie_chart()
生成饼图，支持突出显示。

**参数**:
- `labels`: 标签列表
- `sizes`: 数值列表
- `explode`: 突出显示，如 `[0, 0.1, 0, 0]`
- `autopct`: 百分比格式

### scatter_plot()
生成散点图。

**参数**:
- `x/y`: 坐标数据
- `color`: 点的颜色
- `size`: 点的大小
- `alpha`: 透明度 (0-1)

### multi_series_bar()
生成多系列柱状图（分组柱状图）。

**参数**:
- `categories`: 类别列表
- `data`: 数据字典，格式 `{'Series1': [values], 'Series2': [values]}`

## 示例

运行 `python data_visualization.py` 生成 5 个示例图表。

## 特性

- 高分辨率输出 (300 DPI)
- 自动布局优化
- 非交互式后端，适合服务器环境
- 简洁的 API 设计
