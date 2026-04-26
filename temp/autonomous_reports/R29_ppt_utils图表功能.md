# R29 - PPTBuilder 图表幻灯片功能

## 任务
为 `ppt_lab/ppt_utils.py` 的 `PPTBuilder` 类新增 `add_chart_slide()` 方法，支持柱状图、折线图、饼图等原生图表。

## 实现方案

### 方法签名
```python
add_chart_slide(title, chart_type, categories, series_data,
                chart_title='', value_axis_title='', category_axis_title='')
```

### 支持图表类型
| chart_type | 对应 XL_CHART_TYPE | 说明 |
|---|---|---|
| `'bar'` | BAR_CLUSTERED | 横向柱状图 |
| `'column'` | COLUMN_CLUSTERED | 纵向柱状图 |
| `'line'` | LINE_MARKED | 折线图(带标记) |
| `'pie'` | PIE | 饼图 |

### 数据格式
```python
categories = ["Q1", "Q2", "Q3", "Q4"]
series_data = [
    {"name": "2023年", "values": [120, 150, 180, 200]},
    {"name": "2024年", "values": [140, 170, 210, 250]},
]
```

### 技术要点
- **原生 python-pptx 图表**：使用 `XL_CHART_TYPE` + `CategoryChartData`，无需 matplotlib 依赖
- **配色方案集成**：从 `ColorScheme` 取色，系列颜色自动分配
- **饼图数据标签**：自动添加百分比+类别名标签
- **装饰元素**：复用 `_add_decoration_stripe()` 保持视觉一致性
- **坐标轴**：支持 value_axis_title / category_axis_title，自动设置网格线样式

## 验证结果
- ✅ 生成 `ppt_lab/chart_demo.pptx`（61,165 bytes，6页）
- ✅ 包含：封面 + column图 + line图 + pie图 + bar图 + 结尾页
- ✅ 无运行错误，所有图表类型正常渲染

## 文件变更
- `ppt_lab/ppt_utils.py`：新增 `add_chart_slide()` 方法（约60行），插入于 `save()` 方法之前
- `ppt_lab/chart_demo.pptx`：演示文件（新增）