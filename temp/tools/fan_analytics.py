"""
粉丝画像分析工具 - Fan Analytics Toolkit
支持4维度分析：增长曲线/活跃时段/地域分布/兴趣标签
"""
import json
from datetime import datetime, timedelta
from collections import Counter
from pathlib import Path
from typing import Optional
import random

# 数据存储路径
DATA_DIR = Path(__file__).parent / "fan_data"
DATA_DIR.mkdir(exist_ok=True)

def load_fan_data(platform: str = "default") -> dict:
    """加载粉丝数据，无数据时返回空结构"""
    data_file = DATA_DIR / f"{platform}_fans.json"
    if data_file.exists():
        return json.loads(data_file.read_text(encoding='utf-8'))
    return {"followers": [], "daily_stats": [], "platform": platform}

def save_fan_data(data: dict, platform: str = "default"):
    """保存粉丝数据"""
    data_file = DATA_DIR / f"{platform}_fans.json"
    data_file.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')

def import_fans(fans_list: list, platform: str = "default"):
    """
    导入粉丝数据
    fans_list: [{"id": "xxx", "name": "xxx", "region": "北京", "tags": ["科技","数码"], "follow_time": "2026-01-15", "active_hours": [9,12,20]}]
    """
    data = load_fan_data(platform)
    existing_ids = {f["id"] for f in data["followers"]}
    new_count = 0
    for fan in fans_list:
        if fan.get("id") not in existing_ids:
            data["followers"].append(fan)
            new_count += 1
    save_fan_data(data, platform)
    return {"imported": new_count, "total": len(data["followers"])}

def record_daily_stats(count: int, date: str = None, platform: str = "default"):
    """记录每日粉丝数"""
    data = load_fan_data(platform)
    date = date or datetime.now().strftime("%Y-%m-%d")
    # 更新或新增
    for stat in data["daily_stats"]:
        if stat["date"] == date:
            stat["count"] = count
            save_fan_data(data, platform)
            return stat
    new_stat = {"date": date, "count": count}
    data["daily_stats"].append(new_stat)
    data["daily_stats"].sort(key=lambda x: x["date"])
    save_fan_data(data, platform)
    return new_stat

# ========== 4维度分析函数 ==========

def analyze_growth(platform: str = "default", days: int = 30) -> dict:
    """
    维度1: 粉丝增长曲线分析
    返回：日增长数据、增长率、趋势判断
    """
    data = load_fan_data(platform)
    stats = data.get("daily_stats", [])
    if len(stats) < 2:
        return {"error": "数据不足，至少需要2天数据", "data": []}
    
    # 取最近N天
    recent = stats[-days:] if len(stats) >= days else stats
    
    # 计算日增长
    growth_data = []
    for i in range(1, len(recent)):
        prev, curr = recent[i-1], recent[i]
        daily_growth = curr["count"] - prev["count"]
        growth_rate = (daily_growth / prev["count"] * 100) if prev["count"] > 0 else 0
        growth_data.append({
            "date": curr["date"],
            "count": curr["count"],
            "growth": daily_growth,
            "rate": round(growth_rate, 2)
        })
    
    # 趋势判断
    if len(growth_data) >= 7:
        recent_avg = sum(g["growth"] for g in growth_data[-7:]) / 7
        prev_avg = sum(g["growth"] for g in growth_data[-14:-7]) / 7 if len(growth_data) >= 14 else recent_avg
        if recent_avg > prev_avg * 1.2:
            trend = "accelerating"
        elif recent_avg < prev_avg * 0.8:
            trend = "slowing"
        else:
            trend = "stable"
    else:
        trend = "insufficient_data"
    
    total_growth = growth_data[-1]["count"] - recent[0]["count"] if growth_data else 0
    avg_daily = total_growth / len(growth_data) if growth_data else 0
    
    return {
        "period": f"{recent[0]['date']} ~ {recent[-1]['date']}",
        "total_growth": total_growth,
        "avg_daily_growth": round(avg_daily, 1),
        "trend": trend,
        "data": growth_data
    }

def analyze_active_hours(platform: str = "default") -> dict:
    """
    维度2: 粉丝活跃时段分析
    返回：各时段活跃人数、最佳发布时间建议
    """
    data = load_fan_data(platform)
    followers = data.get("followers", [])
    if not followers:
        return {"error": "无粉丝数据", "hours": {}}
    
    # 统计各时段活跃人数
    hour_counts = Counter()
    for fan in followers:
        for hour in fan.get("active_hours", []):
            hour_counts[hour] += 1
    
    # 转换为完整24小时分布
    hours_dist = {h: hour_counts.get(h, 0) for h in range(24)}
    total = sum(hours_dist.values()) or 1
    hours_pct = {h: round(c/total*100, 1) for h, c in hours_dist.items()}
    
    # 找出高峰时段(top 3)
    peak_hours = sorted(hours_dist.items(), key=lambda x: -x[1])[:3]
    
    # 发布建议：高峰前1小时
    best_publish = [(h-1) % 24 for h, _ in peak_hours]
    
    return {
        "total_fans": len(followers),
        "hours_distribution": hours_dist,
        "hours_percentage": hours_pct,
        "peak_hours": [h for h, _ in peak_hours],
        "best_publish_times": best_publish,
        "recommendation": f"建议发布时间: {best_publish[0]}:00, {best_publish[1]}:00, {best_publish[2]}:00"
    }

def analyze_regions(platform: str = "default") -> dict:
    """
    维度3: 粉丝地域分布分析
    返回：各地区人数、占比、地域特征
    """
    data = load_fan_data(platform)
    followers = data.get("followers", [])
    if not followers:
        return {"error": "无粉丝数据", "regions": {}}
    
    # 统计地域
    region_counts = Counter(f.get("region", "未知") for f in followers)
    total = len(followers)
    
    # 排序
    sorted_regions = sorted(region_counts.items(), key=lambda x: -x[1])
    
    regions_data = [
        {"region": r, "count": c, "percentage": round(c/total*100, 1)}
        for r, c in sorted_regions
    ]
    
    # 地域特征判断
    top3_pct = sum(d["percentage"] for d in regions_data[:3])
    if top3_pct > 60:
        concentration = "high"
        tip = "粉丝地域集中，可针对性做本地化内容"
    elif top3_pct > 40:
        concentration = "medium"
        tip = "粉丝地域分布适中，内容可兼顾全国性话题"
    else:
        concentration = "low"
        tip = "粉丝地域分散，建议做全国通用型内容"
    
    return {
        "total_fans": total,
        "regions": regions_data,
        "top_regions": [d["region"] for d in regions_data[:5]],
        "concentration": concentration,
        "recommendation": tip
    }

def analyze_interests(platform: str = "default") -> dict:
    """
    维度4: 粉丝兴趣标签分析
    返回：标签词频、热门标签、内容方向建议
    """
    data = load_fan_data(platform)
    followers = data.get("followers", [])
    if not followers:
        return {"error": "无粉丝数据", "tags": {}}
    
    # 统计标签
    tag_counts = Counter()
    for fan in followers:
        for tag in fan.get("tags", []):
            tag_counts[tag] += 1
    
    total_tags = sum(tag_counts.values()) or 1
    sorted_tags = sorted(tag_counts.items(), key=lambda x: -x[1])
    
    tags_data = [
        {"tag": t, "count": c, "percentage": round(c/total_tags*100, 1)}
        for t, c in sorted_tags
    ]
    
    # 内容方向建议
    top_tags = [d["tag"] for d in tags_data[:5]]
    
    return {
        "total_fans": len(followers),
        "unique_tags": len(tag_counts),
        "tags": tags_data,
        "top_tags": top_tags,
        "recommendation": f"粉丝最关注: {', '.join(top_tags[:3])}，建议围绕这些主题创作"
    }

def full_analysis(platform: str = "default") -> dict:
    """完整4维度分析报告"""
    return {
        "platform": platform,
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "growth": analyze_growth(platform),
        "active_hours": analyze_active_hours(platform),
        "regions": analyze_regions(platform),
        "interests": analyze_interests(platform)
    }

def generate_demo_data(platform: str = "demo", fan_count: int = 500):
    """生成演示数据用于测试"""
    regions = ["北京", "上海", "广州", "深圳", "杭州", "成都", "武汉", "南京", "西安", "重庆"]
    tags_pool = ["科技", "数码", "编程", "AI", "职场", "效率", "读书", "投资", "健身", "美食", "旅行", "摄影"]
    
    fans = []
    base_date = datetime(2026, 1, 1)
    for i in range(fan_count):
        follow_day = random.randint(0, 110)
        fans.append({
            "id": f"fan_{i:05d}",
            "name": f"用户{i}",
            "region": random.choices(regions, weights=[15,12,10,10,8,8,7,7,6,5])[0],
            "tags": random.sample(tags_pool, k=random.randint(2, 5)),
            "follow_time": (base_date + timedelta(days=follow_day)).strftime("%Y-%m-%d"),
            "active_hours": random.sample(range(24), k=random.randint(2, 4))
        })
    
    # 生成每日统计(模拟增长曲线)
    daily_stats = []
    count = 50
    for d in range(120):
        count += random.randint(2, 8)
        daily_stats.append({
            "date": (base_date + timedelta(days=d)).strftime("%Y-%m-%d"),
            "count": count
        })
    
    data = {"followers": fans, "daily_stats": daily_stats, "platform": platform}
    save_fan_data(data, platform)
    return {"fans": fan_count, "days": len(daily_stats)}

if __name__ == "__main__":
    # 生成演示数据并测试
    print("生成演示数据...")
    generate_demo_data("demo", 500)
    
    print("\n=== 完整分析报告 ===")
    report = full_analysis("demo")
    
    print(f"\n【增长分析】")
    g = report["growth"]
    print(f"  周期: {g['period']}")
    print(f"  总增长: {g['total_growth']}, 日均: {g['avg_daily_growth']}")
    print(f"  趋势: {g['trend']}")
    
    print(f"\n【活跃时段】")
    a = report["active_hours"]
    print(f"  高峰时段: {a['peak_hours']}")
    print(f"  {a['recommendation']}")
    
    print(f"\n【地域分布】")
    r = report["regions"]
    print(f"  Top5: {r['top_regions']}")
    print(f"  集中度: {r['concentration']}")
    print(f"  {r['recommendation']}")
    
    print(f"\n【兴趣标签】")
    t = report["interests"]
    print(f"  Top5: {t['top_tags']}")
    print(f"  {t['recommendation']}")
