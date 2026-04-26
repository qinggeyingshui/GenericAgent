# 内容日历SOP (L3)
工具: temp/tools/content_calendar.py

## 快速开始
```python
from content_calendar import ContentCalendar, analyze_best_times, generate_calendar_view
from datetime import datetime, timedelta

# 创建日历
cal = ContentCalendar("my_calendar.json")

# 添加内容计划
cal.add("标题", "xiaohongshu", "article", datetime.now() + timedelta(days=1), tags=["运营"])

# 更新/删除
cal.update(item_id, status="published")
cal.delete(item_id)

# 查询
items = cal.get_by_date(datetime.now())  # 按日期
items = cal.get_by_range(start, end)     # 按范围
reminders = cal.get_reminders(hours_ahead=24)  # 提醒
```

## 最佳时间分析
```python
best_times = analyze_best_times()  # 返回各平台推荐时间
# {"xiaohongshu": ["12:00","18:00","21:00"], "weixin": ["08:00","12:00","20:00"], ...}
```

## 日历视图
```python
md = generate_calendar_view(cal, 2026, 4)  # 生成Markdown月历
```

平台: xiaohongshu/weixin/zhihu/douyin/bilibili
状态: draft/scheduled/published/cancelled

[skill_mapping]
category: content_creation
skill: content_calendar_sop
tools: content_calendar.py
[/skill_mapping]
