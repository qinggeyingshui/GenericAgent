"""
media_analytics.py — 自媒体数据分析工具（R162, 2026-04-20）

功能：
1. 支持阅读量/点赞/评论数据分析
2. 生成趋势图表
3. 生成数据分析报告

依赖: pip install pandas matplotlib
"""

import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import os

# 设置中文字体
plt.rcParams["font.sans-serif"] = ["SimHei", "Microsoft YaHei"]
plt.rcParams["axes.unicode_minus"] = False


def load_data(file_path, date_col="date", metrics=None):
    """
    加载数据
    
    Args:
        file_path: CSV/Excel文件路径
        date_col: 日期列名
        metrics: 指标列名列表，如["views", "likes", "comments"]
    
    Returns:
        DataFrame
    """
    if file_path.endswith(".csv"):
        df = pd.read_csv(file_path)
    else:
        df = pd.read_excel(file_path)
    
    # 转换日期列
    if date_col in df.columns:
        df[date_col] = pd.to_datetime(df[date_col])
        df = df.sort_values(date_col)
    
    return df


def calculate_metrics(df, metrics=None):
    """
    计算基础指标
    
    Args:
        df: 数据框
        metrics: 指标列名列表
    
    Returns:
        {
            "total": {指标: 总计},
            "average": {指标: 平均值},
            "max": {指标: 最大值},
            "min": {指标: 最小值}
        }
    """
    if not metrics:
        metrics = ["views", "likes", "comments"]
    
    result = {
        "total": {},
        "average": {},
        "max": {},
        "min": {}
    }
    
    for metric in metrics:
        if metric in df.columns:
            result["total"][metric] = df[metric].sum()
            result["average"][metric] = df[metric].mean()
            result["max"][metric] = df[metric].max()
            result["min"][metric] = df[metric].min()
    
    return result


def calculate_growth_rate(df, metric, date_col="date", period="day"):
    """
    计算增长率
    
    Args:
        df: 数据框
        metric: 指标名
        date_col: 日期列名
        period: 周期（day/week/month）
    
    Returns:
        增长率（百分比）
    """
    if metric not in df.columns or date_col not in df.columns:
        return 0
    
    df_sorted = df.sort_values(date_col)
    
    if len(df_sorted) < 2:
        return 0
    
    first_value = df_sorted[metric].iloc[0]
    last_value = df_sorted[metric].iloc[-1]
    
    if first_value == 0:
        return 0
    
    growth_rate = ((last_value - first_value) / first_value) * 100
    return round(growth_rate, 2)


def plot_trend(df, metrics, date_col="date", output_path="trend.png", title="数据趋势"):
    """
    绘制趋势图
    
    Args:
        df: 数据框
        metrics: 指标列表
        date_col: 日期列名
        output_path: 输出路径
        title: 图表标题
    
    Returns:
        输出路径
    """
    plt.figure(figsize=(12, 6))
    
    for metric in metrics:
        if metric in df.columns:
            plt.plot(df[date_col], df[metric], marker="o", label=metric)
    
    plt.xlabel("日期")
    plt.ylabel("数值")
    plt.title(title)
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close()
    
    return output_path


def plot_comparison(df, metrics, date_col="date", output_path="comparison.png", title="指标对比"):
    """
    绘制对比柱状图
    
    Args:
        df: 数据框
        metrics: 指标列表
        date_col: 日期列名
        output_path: 输出路径
        title: 图表标题
    
    Returns:
        输出路径
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    
    x = range(len(df))
    width = 0.8 / len(metrics)
    
    for i, metric in enumerate(metrics):
        if metric in df.columns:
            offset = width * i - width * (len(metrics) - 1) / 2
            ax.bar([xi + offset for xi in x], df[metric], width, label=metric)
    
    ax.set_xlabel("日期")
    ax.set_ylabel("数值")
    ax.set_title(title)
    ax.set_xticks(x)
    ax.set_xticklabels(df[date_col].dt.strftime("%Y-%m-%d"), rotation=45)
    ax.legend()
    ax.grid(True, alpha=0.3, axis="y")
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close()
    
    return output_path


def generate_report(df, metrics, date_col="date", output_path="report.txt"):
    """
    生成数据分析报告
    
    Args:
        df: 数据框
        metrics: 指标列表
        date_col: 日期列名
        output_path: 输出路径
    
    Returns:
        输出路径
    """
    report_lines = []
    report_lines.append("# 自媒体数据分析报告\n\n")
    report_lines.append(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
    
    # 数据概览
    report_lines.append("## 数据概览\n\n")
    report_lines.append(f"- 数据条数: {len(df)}\n")
    if date_col in df.columns:
        report_lines.append(f"- 时间范围: {df[date_col].min().strftime('%Y-%m-%d')} 至 {df[date_col].max().strftime('%Y-%m-%d')}\n")
    report_lines.append("\n")
    
    # 基础指标
    report_lines.append("## 基础指标\n\n")
    stats = calculate_metrics(df, metrics)
    
    for metric in metrics:
        if metric in df.columns:
            report_lines.append(f"### {metric}\n\n")
            report_lines.append(f"- 总计: {stats['total'].get(metric, 0):.0f}\n")
            report_lines.append(f"- 平均: {stats['average'].get(metric, 0):.2f}\n")
            report_lines.append(f"- 最大: {stats['max'].get(metric, 0):.0f}\n")
            report_lines.append(f"- 最小: {stats['min'].get(metric, 0):.0f}\n")
            
            # 增长率
            growth = calculate_growth_rate(df, metric, date_col)
            report_lines.append(f"- 增长率: {growth}%\n")
            report_lines.append("\n")
    
    # 写入文件
    with open(output_path, "w", encoding="utf-8") as f:
        f.writelines(report_lines)
    
    return output_path


def analyze_media_data(file_path, metrics=None, date_col="date", output_dir="./analytics_output"):
    """
    完整分析流程
    
    Args:
        file_path: 数据文件路径
        metrics: 指标列表
        date_col: 日期列名
        output_dir: 输出目录
    
    Returns:
        {
            "report": 报告路径,
            "trend_chart": 趋势图路径,
            "comparison_chart": 对比图路径,
            "metrics": 指标统计
        }
    """
    if not metrics:
        metrics = ["views", "likes", "comments"]
    
    # 创建输出目录
    os.makedirs(output_dir, exist_ok=True)
    
    # 加载数据
    df = load_data(file_path, date_col, metrics)
    
    # 计算指标
    stats = calculate_metrics(df, metrics)
    
    # 生成图表
    trend_path = os.path.join(output_dir, "trend.png")
    comparison_path = os.path.join(output_dir, "comparison.png")
    report_path = os.path.join(output_dir, "report.txt")
    
    plot_trend(df, metrics, date_col, trend_path)
    plot_comparison(df, metrics, date_col, comparison_path)
    generate_report(df, metrics, date_col, report_path)
    
    return {
        "report": report_path,
        "trend_chart": trend_path,
        "comparison_chart": comparison_path,
        "metrics": stats
    }
