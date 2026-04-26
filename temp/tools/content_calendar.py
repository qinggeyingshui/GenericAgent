#!/usr/bin/env python3
"""
content_calendar.py - 内容日历与排期管理工具

功能:
1. 发布计划管理 - 创建/编辑/删除内容计划
2. 最佳时间分析 - 基于历史数据推荐发布时间
3. 日历视图生成 - 生成可视化日历
4. 提醒功能 - 获取待发布内容提醒
"""
import os
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict, field
from collections import defaultdict

@dataclass
class ContentItem:
    """内容条目"""
    id: str
    title: str
    platform: str  # xiaohongshu/weixin/zhihu/douyin
    content_type: str  # article/video/image/short
    scheduled_time: str  # ISO格式
    status: str = "draft"  # draft/scheduled/published/cancelled
    tags: List[str] = field(default_factory=list)
    notes: str = ""
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())

class ContentCalendar:
    """内容日历管理器"""
    
    def __init__(self, data_file: str = "content_calendar.json"):
        self.data_file = data_file
        self.items: Dict[str, ContentItem] = {}
        self.load()
    
    def load(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.items = {k: ContentItem(**v) for k, v in data.items()}
    
    def save(self):
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump({k: asdict(v) for k, v in self.items.items()}, f, ensure_ascii=False, indent=2)
    
    def add(self, title: str, platform: str, content_type: str, 
            scheduled_time: datetime, tags: List[str] = None, notes: str = "") -> ContentItem:
        """添加内容计划"""
        item_id = f"{platform}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        item = ContentItem(
            id=item_id,
            title=title,
            platform=platform,
            content_type=content_type,
            scheduled_time=scheduled_time.isoformat(),
            status="scheduled",
            tags=tags or [],
            notes=notes
        )
        self.items[item_id] = item
        self.save()
        return item
    
    def update(self, item_id: str, **kwargs) -> Optional[ContentItem]:
        """更新内容计划"""
        if item_id not in self.items:
            return None
        item = self.items[item_id]
        for k, v in kwargs.items():
            if hasattr(item, k):
                if k == 'scheduled_time' and isinstance(v, datetime):
                    v = v.isoformat()
                setattr(item, k, v)
        self.save()
        return item
    
    def delete(self, item_id: str) -> bool:
        """删除内容计划"""
        if item_id in self.items:
            del self.items[item_id]
            self.save()
            return True
        return False
    
    def get_by_date(self, date: datetime) -> List[ContentItem]:
        """获取指定日期的内容"""
        date_str = date.strftime('%Y-%m-%d')
        return [item for item in self.items.values() 
                if item.scheduled_time.startswith(date_str)]
    
    def get_by_range(self, start: datetime, end: datetime) -> List[ContentItem]:
        """获取日期范围内的内容"""
        return [item for item in self.items.values()
                if start.isoformat() <= item.scheduled_time <= end.isoformat()]
    
    def get_reminders(self, hours_ahead: int = 24) -> List[ContentItem]:
        """获取即将发布的内容提醒"""
        now = datetime.now()
        deadline = now + timedelta(hours=hours_ahead)
        return [item for item in self.items.values()
                if item.status == "scheduled" 
                and now.isoformat() <= item.scheduled_time <= deadline.isoformat()]


def analyze_best_times(history_data: List[Dict] = None) -> Dict[str, List[str]]:
    """
    分析最佳发布时间
    
    Args:
        history_data: 历史发布数据 [{"platform": "xx", "time": "HH:MM", "engagement": 100}]
    
    Returns:
        各平台最佳时间 {"xiaohongshu": ["12:00", "20:00"], ...}
    """
    # 默认推荐时间（基于行业经验）
    default_times = {
        "xiaohongshu": ["12:00", "18:00", "21:00"],
        "weixin": ["08:00", "12:00", "20:00"],
        "zhihu": ["10:00", "14:00", "21:00"],
        "douyin": ["12:00", "18:00", "21:00"],
        "bilibili": ["17:00", "20:00", "22:00"]
    }
    
    if not history_data:
        return default_times
    
    # 基于历史数据分析
    platform_times = defaultdict(list)
    for record in history_data:
        platform = record.get("platform", "unknown")
        time = record.get("time", "12:00")
        engagement = record.get("engagement", 0)
        platform_times[platform].append((time, engagement))
    
    result = {}
    for platform, times in platform_times.items():
        # 按互动量排序，取前3
        sorted_times = sorted(times, key=lambda x: x[1], reverse=True)
        result[platform] = [t[0] for t in sorted_times[:3]]
    
    # 补充默认值
    for platform, times in default_times.items():
        if platform not in result:
            result[platform] = times
    
    return result


def generate_calendar_view(calendar: ContentCalendar, year: int, month: int) -> str:
    """
    生成月度日历视图（Markdown格式）
    
    Args:
        calendar: ContentCalendar实例
        year: 年份
        month: 月份
    
    Returns:
        Markdown格式的日历
    """
    import calendar as cal
    
    # 获取月份信息
    month_cal = cal.monthcalendar(year, month)
    month_name = cal.month_name[month]
    
    # 获取该月所有内容
    start = datetime(year, month, 1)
    if month == 12:
        end = datetime(year + 1, 1, 1) - timedelta(seconds=1)
    else:
        end = datetime(year, month + 1, 1) - timedelta(seconds=1)
    
    items = calendar.get_by_range(start, end)
    
    # 按日期分组
    items_by_day = defaultdict(list)
    for item in items:
        day = int(item.scheduled_time[8:10])
        items_by_day[day].append(item)
    
    # 生成Markdown
    lines = [
        f"# 📅 {year}年{month}月 内容日历",
        "",
        "| 周一 | 周二 | 周三 | 周四 | 周五 | 周六 | 周日 |",
        "|:----:|:----:|:----:|:----:|:----:|:----:|:----:|"
    ]
    
    platform_emoji = {
        "xiaohongshu": "📕",
        "weixin": "💬",
        "zhihu": "📘",
        "douyin": "🎵",
        "bilibili": "📺"
    }
    
    for week in month_cal:
        row = []
        for day in week:
            if day == 0:
                row.append("")
            else:
                cell = f"**{day}**"
                if day in items_by_day:
                    for item in items_by_day[day][:2]:  # 最多显示2个
                        emoji = platform_emoji.get(item.platform, "📝")
                        cell += f"<br>{emoji}{item.title[:6]}"
                row.append(cell)
        lines.append("| " + " | ".join(row) + " |")
    
    # 添加详细列表
    lines.extend(["", "## 📋 本月内容详情", ""])
    
    status_emoji = {"draft": "📝", "scheduled": "⏰", "published": "✅", "cancelled": "❌"}
    
    for item in sorted(items, key=lambda x: x.scheduled_time):
        emoji = platform_emoji.get(item.platform, "📝")
        status = status_emoji.get(item.status, "📝")
        time_str = item.scheduled_time[5:16].replace("T", " ")
        lines.append(f"- {status} **{time_str}** {emoji} {item.title}")
    
    return "\n".join(lines)


def demo_content_calendar():
    """演示内容日历功能"""
    import os
    
    demo_dir = "./calendar_demo"
    os.makedirs(demo_dir, exist_ok=True)
    
    # 创建日历
    cal = ContentCalendar(f"{demo_dir}/calendar.json")
    
    # 添加示例内容
    now = datetime.now()
    
    cal.add("小红书爆款标题技巧", "xiaohongshu", "article",
            now + timedelta(days=1, hours=12), ["运营", "技巧"])
    cal.add("微信公众号排版指南", "weixin", "article",
            now + timedelta(days=2, hours=20), ["教程"])
    cal.add("知乎高赞回答分析", "zhihu", "article",
            now + timedelta(days=3, hours=14), ["分析"])
    cal.add("抖音短视频脚本", "douyin", "video",
            now + timedelta(days=5, hours=18), ["视频"])
    
    print(f"✓ 已添加 {len(cal.items)} 条内容计划")
    
    # 分析最佳时间
    best_times = analyze_best_times()
    print("\n✓ 最佳发布时间分析:")
    for platform, times in list(best_times.items())[:3]:
        print(f"  {platform}: {', '.join(times)}")
    
    # 生成日历视图
    calendar_md = generate_calendar_view(cal, now.year, now.month)
    output_path = f"{demo_dir}/calendar_{now.year}_{now.month:02d}.md"
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(calendar_md)
    print(f"\n✓ 日历视图已生成: {output_path}")
    
    # 获取提醒
    reminders = cal.get_reminders(hours_ahead=72)
    print(f"\n✓ 72小时内待发布: {len(reminders)} 条")
    
    return output_path


if __name__ == "__main__":
    demo_content_calendar()
