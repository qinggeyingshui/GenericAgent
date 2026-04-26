"""
content_dashboard.py - Content Creation Dashboard Tool (R166, 2026-04-20)

Features:
1. Multi-platform data aggregation
2. Visualization dashboard (views/followers/engagement)
3. Trend analysis
"""

import json
from datetime import datetime, timedelta
import os


def aggregate_platform_data(data_sources):
    """
    Aggregate data from multiple platforms
    
    Args:
        data_sources: List of data source dicts with platform/metrics
    
    Returns:
        Aggregated data dict
    """
    aggregated = {
        "total_views": 0,
        "total_followers": 0,
        "total_engagement": 0,
        "platforms": {},
        "timestamp": datetime.now().isoformat()
    }
    
    for source in data_sources:
        platform = source.get("platform", "unknown")
        metrics = source.get("metrics", {})
        
        aggregated["total_views"] += metrics.get("views", 0)
        aggregated["total_followers"] += metrics.get("followers", 0)
        aggregated["total_engagement"] += metrics.get("engagement", 0)
        
        aggregated["platforms"][platform] = metrics
    
    return aggregated


def calculate_trends(historical_data, days=7):
    """
    Calculate trends from historical data
    
    Args:
        historical_data: List of historical data points
        days: Number of days to analyze
    
    Returns:
        Trend analysis dict
    """
    if len(historical_data) < 2:
        return {"trend": "insufficient_data"}
    
    recent = historical_data[-days:] if len(historical_data) >= days else historical_data
    
    views_trend = []
    followers_trend = []
    engagement_trend = []
    
    for data in recent:
        views_trend.append(data.get("total_views", 0))
        followers_trend.append(data.get("total_followers", 0))
        engagement_trend.append(data.get("total_engagement", 0))
    
    def calc_growth(values):
        if len(values) < 2 or values[0] == 0:
            return 0
        return ((values[-1] - values[0]) / values[0]) * 100
    
    return {
        "views_growth": round(calc_growth(views_trend), 2),
        "followers_growth": round(calc_growth(followers_trend), 2),
        "engagement_growth": round(calc_growth(engagement_trend), 2),
        "period_days": len(recent)
    }


def generate_dashboard(aggregated_data, trends, output_path):
    """
    Generate text-based dashboard report
    
    Args:
        aggregated_data: Aggregated metrics
        trends: Trend analysis
        output_path: Output file path
    
    Returns:
        Dashboard file path
    """
    lines = [
        "# Content Creation Dashboard\n\n",
        f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n",
        "## Overall Metrics\n\n",
        f"- Total Views: {aggregated_data['total_views']:,}\n",
        f"- Total Followers: {aggregated_data['total_followers']:,}\n",
        f"- Total Engagement: {aggregated_data['total_engagement']:,}\n\n",
        "## Platform Breakdown\n\n"
    ]
    
    for platform, metrics in aggregated_data.get("platforms", {}).items():
        lines.append(f"### {platform}\n\n")
        lines.append(f"- Views: {metrics.get('views', 0):,}\n")
        lines.append(f"- Followers: {metrics.get('followers', 0):,}\n")
        lines.append(f"- Engagement: {metrics.get('engagement', 0):,}\n\n")
    
    if trends.get("trend") != "insufficient_data":
        lines.append("## Trends\n\n")
        lines.append(f"Period: {trends['period_days']} days\n\n")
        lines.append(f"- Views Growth: {trends['views_growth']}%\n")
        lines.append(f"- Followers Growth: {trends['followers_growth']}%\n")
        lines.append(f"- Engagement Growth: {trends['engagement_growth']}%\n")
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.writelines(lines)
    
    return output_path


def create_dashboard(data_sources, historical_data=None, output_path="dashboard.md"):
    """
    Create complete dashboard
    
    Args:
        data_sources: List of platform data sources
        historical_data: Optional historical data for trends
        output_path: Output file path
    
    Returns:
        Result dict with dashboard path and metrics
    """
    aggregated = aggregate_platform_data(data_sources)
    
    trends = {}
    if historical_data:
        trends = calculate_trends(historical_data)
    else:
        trends = {"trend": "insufficient_data"}
    
    dashboard_path = generate_dashboard(aggregated, trends, output_path)
    
    return {
        "dashboard": dashboard_path,
        "metrics": aggregated,
        "trends": trends
    }


if __name__ == "__main__":
    # Test
    test_data = [
        {
            "platform": "WeChat",
            "metrics": {"views": 5000, "followers": 1200, "engagement": 350}
        },
        {
            "platform": "Zhihu",
            "metrics": {"views": 8000, "followers": 2500, "engagement": 600}
        },
        {
            "platform": "Xiaohongshu",
            "metrics": {"views": 3000, "followers": 800, "engagement": 200}
        }
    ]
    
    historical = [
        {"total_views": 10000, "total_followers": 3000, "total_engagement": 800},
        {"total_views": 12000, "total_followers": 3500, "total_engagement": 900},
        {"total_views": 16000, "total_followers": 4500, "total_engagement": 1150}
    ]
    
    result = create_dashboard(test_data, historical, "./test_dashboard.md")
    print(f"Dashboard: {result['dashboard']}")
    print(f"Total Views: {result['metrics']['total_views']:,}")
    print(f"Views Growth: {result['trends']['views_growth']}%")