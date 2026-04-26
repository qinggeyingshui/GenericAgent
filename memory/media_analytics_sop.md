# media_analytics_sop.md — 自媒体数据分析SOP（R162, 2026-04-20）

工具: tools/media_analytics.py | tools/dashboard_enhanced.py | 基于pandas+matplotlib

## 核心函数

```python
analyze_media_data(file_path, metrics=['views','likes','comments'], date_col='date', output_dir='./analytics_output')
calculate_metrics(df, metrics) → {total, average, max, min}
calculate_growth_rate(df, metric, date_col, period='day') → 增长率%
plot_trend(df, metrics, date_col, output_path, title)
plot_comparison(df, metrics, date_col, output_path, title)
generate_report(df, metrics, date_col, output_path)
```

## 使用示例

```python
from media_analytics import analyze_media_data

# 完整分析流程
result = analyze_media_data(
    'data.csv',
    metrics=['views', 'likes', 'comments'],
    date_col='date',
    output_dir='./output'
)

print(result['report'])  # 报告路径
print(result['trend_chart'])  # 趋势图路径
print(result['comparison_chart'])  # 对比图路径
print(result['metrics'])  # 指标统计
```

## 数据格式

CSV/Excel文件，必须包含：
- date列：日期（YYYY-MM-DD）
- 指标列：views/likes/comments等

示例：
```
date,views,likes,comments
2026-04-14,1000,50,10
2026-04-15,1200,60,12
```

## 输出内容

1. **report.txt**: 文本报告（数据概览+基础指标+增长率）
2. **trend.png**: 趋势折线图
3. **comparison.png**: 对比柱状图

## 指标说明

- **total**: 总计
- **average**: 平均值
- **max**: 最大值
- **min**: 最小值
- **growth_rate**: 增长率（首尾对比）

## 看板增强功能（R198, 2026-04-21）

工具: tools/dashboard_enhanced.py

### 多维度分析

```python
from dashboard_enhanced import DashboardAnalyzer

analyzer = DashboardAnalyzer(data)

# 平台对比
platform_comp = analyzer.platform_comparison(["wechat", "zhihu"], "views")

# 时间趋势
time_trend = analyzer.time_trend_analysis("views", period="day")

# 内容类型分析
content_type = analyzer.content_type_analysis("views")
```

### 趋势预测

```python
from dashboard_enhanced import TrendPredictor, quick_predict

# 预测未来7天
predictions = TrendPredictor.predict_trend([1000, 1200, 1400], periods=7)

# 快速预测
result = quick_predict([1000, 1200, 1400], 7)
# 返回: {"predictions": [...], "trend_score": "strong_growth", "historical_avg": 1200}
```

### 综合看板

```python
from dashboard_enhanced import quick_dashboard

# 一键生成看板
dashboard = quick_dashboard(data, "./dashboard")
# 输出: HTML报告 + 可视化图表 + 分析结果
```

[skill_mapping]
category: data_analysis
skill: social_media
tools: media_analytics.py, dashboard_enhanced.py
[/skill_mapping]

## [record_on_use]
执行完本SOP后，调用以下命令记录使用情况：
```python
import sys
sys.path.append('../memory')
from autonomous_operation_sop.helper import record_skill_usage
record_skill_usage('media_analytics_sop.md')
```
