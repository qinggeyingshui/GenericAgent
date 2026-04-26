"""
media_dashboard_workflow.py - 自媒体运营看板Workflow
串联 media_analytics + trend_tracker + platform_adapter
生成运营日报/周报，包含数据可视化
"""
import os
import sys
from datetime import datetime
sys.path.append("./tools")

import media_analytics as ma
import trend_tracker as tt
import platform_adapter as pa


def generate_daily_report(data_file, content_texts, output_dir="./reports"):
    """生成运营日报"""
    os.makedirs(output_dir, exist_ok=True)
    date_str = datetime.now().strftime("%Y%m%d")
    
    # 1. 数据分析
    df = ma.load_data(data_file)
    metrics = ma.calculate_metrics(df)
    
    # 2. 趋势分析
    trends = tt.track_trends(content_texts, None)
    
    # 3. 生成报告
    report_path = os.path.join(output_dir, f"daily_report_{date_str}.txt")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(f"# 运营日报 {date_str}\n\n")
        f.write("## 数据概览\n")
        for key, vals in metrics.items():
            f.write(f"### {key}\n")
            for metric, val in vals.items():
                f.write(f"- {metric}: {val:.2f}\n")
        f.write("\n## 趋势分析\n")
        f.write(f"热点关键词: {trends}\n")
    
    return report_path


def generate_weekly_report(data_file, content_texts, output_dir="./reports"):
    """生成运营周报（含可视化）"""
    os.makedirs(output_dir, exist_ok=True)
    date_str = datetime.now().strftime("%Y%m%d")
    
    # 1. 完整数据分析（含图表）
    chart_dir = os.path.join(output_dir, "charts")
    os.makedirs(chart_dir, exist_ok=True)
    
    df = ma.load_data(data_file)
    metrics = ma.calculate_metrics(df)
    
    # 生成趋势图
    trend_chart = os.path.join(chart_dir, f"trend_{date_str}.png")
    ma.plot_trend(df, ["views", "likes"], "date", trend_chart, "数据趋势")
    
    # 2. 趋势和选题推荐
    trends = tt.track_trends(content_texts, None)
    
    # 3. 生成周报
    report_path = os.path.join(output_dir, f"weekly_report_{date_str}.txt")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(f"# 运营周报 {date_str}\n\n")
        f.write("## 数据概览\n")
        for key, vals in metrics.items():
            f.write(f"### {key}\n")
            for metric, val in vals.items():
                f.write(f"- {metric}: {val:.2f}\n")
        f.write("\n## 可视化图表\n")
        f.write(f"- 趋势图: {trend_chart}\n")
        f.write("\n## 趋势分析\n")
        f.write(f"热点关键词: {trends}\n")
    
    return report_path


def create_dashboard(data_file, content_texts, platforms=None, output_dir="./dashboard"):
    """创建完整运营看板"""
    os.makedirs(output_dir, exist_ok=True)
    
    # 1. 生成周报
    report = generate_weekly_report(data_file, content_texts, output_dir)
    
    # 2. 平台适配（如果提供了平台列表）
    if platforms:
        content = "\n".join(content_texts[:3]) if content_texts else ""
        adapted = pa.batch_adapt(content, platforms, "运营周报", [])
        
        adapt_path = os.path.join(output_dir, "platform_adapted.txt")
        with open(adapt_path, "w", encoding="utf-8") as f:
            for platform, text in adapted.items():
                f.write(f"## {platform}\n{text}\n\n")
    
    return output_dir


if __name__ == "__main__":
    print("自媒体运营看板Workflow")
    print("功能: 串联数据分析+趋势追踪+平台适配")