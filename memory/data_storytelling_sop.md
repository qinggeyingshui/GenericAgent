# 数据可视化故事化 SOP

## 概述
将数据转化为叙事性图表，通过视觉元素和注释传达数据洞察。

## 工具依赖
- `temp/tools/data_storytelling.py`
- 依赖: matplotlib, numpy

## 四种叙事模式

### 1. 趋势叙事 (Trend Story)
展示数据随时间的变化，突出峰值和低谷。

```python
from tools.data_storytelling import trend_story

data = [120, 135, 128, 145, 160, 155, 170, 165]
labels = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug']

trend_story(
    data=data,
    labels=labels,
    title="Monthly Sales Trend",
    insight="Sales peaked in July with 70% growth from January",
    output="sales_trend.png"
)
```

**适用场景**: 时间序列数据、业绩追踪、趋势分析

### 2. 对比叙事 (Comparison Story)
对比多个类别，突出优胜者。

```python
from tools.data_storytelling import comparison_story

categories = ['Product A', 'Product B', 'Product C', 'Product D']
values = [85, 120, 95, 110]

comparison_story(
    categories=categories,
    values=values,
    title="Product Performance Comparison",
    winner_text="Product B leads with 120 units sold",
    output="product_comparison.png"
)
```

**适用场景**: 产品对比、团队绩效、市场份额

### 3. 分布叙事 (Distribution Story)
展示数据分布特征，标注统计指标。

```python
from tools.data_storytelling import distribution_story
import numpy as np

data = np.random.normal(100, 15, 1000)

distribution_story(
    data=data,
    title="Customer Age Distribution",
    bins=30,
    insight="Most customers are between 85-115 years old",
    output="age_distribution.png"
)
```

**适用场景**: 用户画像、质量控制、风险评估

### 4. 组成叙事 (Composition Story)
展示部分与整体的关系，突出主要组成。

```python
from tools.data_storytelling import composition_story

labels = ['Mobile', 'Desktop', 'Tablet', 'Other']
sizes = [45, 30, 20, 5]

composition_story(
    labels=labels,
    sizes=sizes,
    title="Traffic Source Distribution",
    highlight_idx=0,  # Highlight Mobile
    output="traffic_composition.png"
)
```

**适用场景**: 市场份额、预算分配、流量来源

## 叙事增强技巧

### 1. 标注关键点
- 自动标注最大值/最小值
- 突出异常值或转折点
- 添加箭头和说明文字

### 2. 颜色语义
- 优胜者/主要部分：紫色 (#A23B72)
- 劣势者/次要部分：橙色 (#F18F01)
- 常规数据：蓝色 (#2E86AB)

### 3. 洞察文本框
- 简洁的数据洞察（1-2句话）
- 放置在不遮挡数据的位置
- 使用半透明背景

### 4. 视觉层次
- 标题：16pt 粗体
- 注释：11-12pt
- 坐标轴：12pt
- 使用网格线增强可读性

## 完整示例工作流

```python
import sys
sys.path.append('./tools')
from data_storytelling import *
import numpy as np

# 示例1: 销售趋势
sales_data = [120, 135, 128, 145, 160, 155, 170, 165]
months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug']
trend_story(sales_data, months, "2024 Sales Trend", 
            "Q3 shows strong growth momentum", "sales_trend.png")

# 示例2: 产品对比
products = ['A', 'B', 'C', 'D', 'E']
performance = [85, 120, 95, 110, 78]
comparison_story(products, performance, "Product Performance Q4",
                 "Product B outperforms by 26%", "product_comparison.png")

# 示例3: 用户分布
user_ages = np.random.normal(35, 10, 500)
distribution_story(user_ages, "User Age Distribution",
                   bins=25, insight="Target demographic: 25-45 years",
                   output="user_distribution.png")

# 示例4: 流量来源
sources = ['Organic', 'Paid', 'Social', 'Direct', 'Referral']
traffic = [40, 25, 20, 10, 5]
composition_story(sources, traffic, "Traffic Sources 2024",
                  highlight_idx=0, output="traffic_sources.png")
```

## 最佳实践

1. **选择合适的叙事模式**
   - 时间数据 → 趋势叙事
   - 类别对比 → 对比叙事
   - 连续数据 → 分布叙事
   - 占比数据 → 组成叙事

2. **简化信息**
   - 每张图表传达1个核心洞察
   - 避免过多数据点（<15个类别）
   - 使用清晰的标签

3. **增强可读性**
   - 高分辨率输出（150 DPI）
   - 合适的图表尺寸（10-12英寸宽）
   - 旋转长标签避免重叠

4. **讲好故事**
   - 标题描述"是什么"
   - 注释解释"为什么"
   - 洞察指出"怎么办"

## 扩展功能

可结合其他工具增强叙事：
- Excel数据导入：`excel_toolkit.py`
- PPT自动生成：`ppt_data_viz.py`
- 数据分析：`data_analysis_sop.md`

[skill_mapping]
category: data_analysis
skill: data_storytelling
tools: data_storytelling.py
[/skill_mapping]

## [record_on_use]
执行完本SOP后，调用以下命令记录使用情况：
```python
import sys
sys.path.append('../memory')
from autonomous_operation_sop.helper import record_skill_usage
record_skill_usage('data_storytelling_sop.md')
```