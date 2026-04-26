# 粉丝画像分析 SOP

[skill_mapping]
category: data_analysis
skill: fan_analytics_sop
tools: fan_analytics.py
[/skill_mapping]

> 工具路径: temp/fan_analytics.py | 数据目录: temp/fan_data/

## 快速开始

```python
import sys; sys.path.append('temp')
from fan_analytics import *

# 生成演示数据(首次使用)
generate_demo_data("demo", 500)

# 完整4维度分析
report = full_analysis("demo")
```

## 核心函数

| 函数 | 用途 | 返回 |
|------|------|------|
| `import_fans(fans_list, platform)` | 导入粉丝数据 | {imported, total} |
| `record_daily_stats(count, date, platform)` | 记录每日粉丝数 | stat对象 |
| `analyze_growth(platform, days=30)` | 增长曲线分析 | 增长数据+趋势 |
| `analyze_active_hours(platform)` | 活跃时段分析 | 时段分布+发布建议 |
| `analyze_regions(platform)` | 地域分布分析 | 地区占比+集中度 |
| `analyze_interests(platform)` | 兴趣标签分析 | 标签词频+内容建议 |
| `full_analysis(platform)` | 完整4维度报告 | 综合分析结果 |

## 数据格式

### 粉丝数据结构
```json
{
  "id": "fan_001",
  "name": "用户名",
  "region": "北京",
  "tags": ["科技", "数码"],
  "follow_time": "2026-01-15",
  "active_hours": [9, 12, 20]
}
```

### 导入示例
```python
fans = [
    {"id": "u1", "name": "张三", "region": "上海", "tags": ["科技","AI"], "active_hours": [9,20]},
    {"id": "u2", "name": "李四", "region": "北京", "tags": ["职场","效率"], "active_hours": [12,21]}
]
import_fans(fans, "weixin")
```

## 分析维度说明

### 1. 增长曲线 (analyze_growth)
- 输出: 日增长数、增长率、趋势判断(accelerating/stable/slowing)
- 用途: 评估账号健康度，发现增长拐点

### 2. 活跃时段 (analyze_active_hours)
- 输出: 24小时活跃分布、高峰时段、最佳发布时间
- 用途: 优化发布时间，提升内容曝光

### 3. 地域分布 (analyze_regions)
- 输出: 各地区人数占比、集中度(high/medium/low)
- 用途: 指导本地化内容策略

### 4. 兴趣标签 (analyze_interests)
- 输出: 标签词频、Top标签、内容方向建议
- 用途: 指导选题方向，提升内容匹配度

## 多平台支持

```python
# 不同平台独立存储
full_analysis("weixin")
full_analysis("douyin")
full_analysis("xiaohongshu")
```

## 与其他工具联动

- `media_analytics.py`: 内容数据 → 粉丝画像关联分析
- `content_calendar.py`: 根据活跃时段优化排期
- `trend_tracker.py`: 兴趣标签 → 热点匹配
