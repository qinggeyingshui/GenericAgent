# 自媒体运营看板 Workflow SOP

## 功能
串联 media_analytics + trend_tracker + platform_adapter，生成运营日报/周报/看板

## 工具
- `temp/tools/media_dashboard_workflow.py`

## 使用流程

### 1. 生成日报
```python
import sys
sys.path.append('./tools')
import media_dashboard_workflow as mdw

mdw.generate_daily_report(
    data_file='data.csv',
    content_texts=['文本1', '文本2'],
    output_dir='./reports'
)
```

### 2. 生成周报
```python
mdw.generate_weekly_report(
    data_file='data.csv',
    content_texts=['文本1', '文本2'],
    output_dir='./reports'
)
```

### 3. 创建完整看板
```python
mdw.create_dashboard(
    data_file='data.csv',
    content_texts=['文本1', '文本2'],
    platforms=['wechat', 'zhihu'],
    output_dir='./dashboard'
)
```

## 数据格式
CSV/Excel文件需包含列: date, views, likes, comments, shares

## 输出
- 日报/周报文本文件
- 趋势图表 (PNG)
- 平台适配内容

[skill_mapping]
category: data_analysis
skill: media_dashboard
tools: media_dashboard_workflow.py
[/skill_mapping]