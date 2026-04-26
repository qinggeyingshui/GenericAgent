# data_analysis_sop.md - Data Analysis SOP (R166, 2026-04-20)

Tool: tools/content_dashboard.py | Data aggregation + Visualization

## Core Functions

```python
aggregate_platform_data(data_sources)  # Multi-platform data aggregation
calculate_trends(historical_data, days=7)  # Trend analysis
generate_dashboard(aggregated_data, trends, output_path)  # Generate dashboard
create_dashboard(data_sources, historical_data, output_path)  # Complete workflow
```

## Usage

```python
from content_dashboard import create_dashboard

data_sources = [
    {"platform": "WeChat", "metrics": {"views": 5000, "followers": 1200, "engagement": 350}},
    {"platform": "Zhihu", "metrics": {"views": 8000, "followers": 2500, "engagement": 600}}
]

historical = [
    {"total_views": 10000, "total_followers": 3000, "total_engagement": 800},
    {"total_views": 16000, "total_followers": 4500, "total_engagement": 1150}
]

result = create_dashboard(data_sources, historical, "dashboard.md")
```

## Features

1. Multi-platform data aggregation (WeChat/Zhihu/Xiaohongshu)
2. Trend analysis (views/followers/engagement growth)
3. Text-based dashboard generation

[skill_mapping]
category: data_analysis
skill: content_dashboard
tools: content_dashboard.py
[/skill_mapping]

## [record_on_use]
执行完本SOP后，调用以下命令记录使用情况：
```python
import sys
sys.path.append('../memory')
from autonomous_operation_sop.helper import record_skill_usage
record_skill_usage('data_analysis_sop.md')
```
