"""
数据可视化工具包
支持常用图表类型：折线图、柱状图、饼图、散点图
基于 matplotlib，简单易用
"""

import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # 非交互式后端，适合服务器环境
from typing import List, Dict, Optional, Tuple
import os


def line_chart(
    data: Dict[str, List[float]],
    title: str = "Line Chart",
    xlabel: str = "X",
    ylabel: str = "Y",
    output_path: str = "line_chart.png",
    figsize: Tuple[int, int] = (10, 6),
    grid: bool = True
) -> str:
    """
    生成折线图
    
    Args:
        data: 数据字典，格式 {'label1': [y1, y2, ...], 'label2': [...]}
              所有列表长度必须相同
        title: 图表标题
        xlabel: X轴标签
        ylabel: Y轴标签
        output_path: 输出文件路径
        figsize: 图表大小 (宽, 高)
        grid: 是否显示网格
    
    Returns:
        输出文件的绝对路径
    
    Example:
        >>> line_chart(
        ...     {'Sales': [100, 150, 120, 180], 'Target': [120, 120, 120, 120]},
        ...     title="Monthly Sales",
        ...     xlabel="Month",
        ...     ylabel="Amount"
        ... )
    """
    plt.figure(figsize=figsize)
    
    for label, values in data.items():
        plt.plot(values, marker='o', label=label, linewidth=2)
    
    plt.title(title, fontsize=14, fontweight='bold')
    plt.xlabel(xlabel, fontsize=12)
    plt.ylabel(ylabel, fontsize=12)
    plt.legend()
    if grid:
        plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    return os.path.abspath(output_path)


def bar_chart(
    categories: List[str],
    values: List[float],
    title: str = "Bar Chart",
    xlabel: str = "Category",
    ylabel: str = "Value",
    output_path: str = "bar_chart.png",
    figsize: Tuple[int, int] = (10, 6),
    color: str = 'steelblue',
    horizontal: bool = False
) -> str:
    """
    生成柱状图
    
    Args:
        categories: 类别列表
        values: 数值列表
        title: 图表标题
        xlabel: X轴标签
        ylabel: Y轴标签
        output_path: 输出文件路径
        figsize: 图表大小
        color: 柱子颜色
        horizontal: 是否横向显示
    
    Returns:
        输出文件的绝对路径
    """
    plt.figure(figsize=figsize)
    
    if horizontal:
        plt.barh(categories, values, color=color)
        plt.xlabel(ylabel, fontsize=12)
        plt.ylabel(xlabel, fontsize=12)
    else:
        plt.bar(categories, values, color=color)
        plt.xlabel(xlabel, fontsize=12)
        plt.ylabel(ylabel, fontsize=12)
        plt.xticks(rotation=45, ha='right')
    
    plt.title(title, fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    return os.path.abspath(output_path)


def pie_chart(
    labels: List[str],
    sizes: List[float],
    title: str = "Pie Chart",
    output_path: str = "pie_chart.png",
    figsize: Tuple[int, int] = (8, 8),
    explode: Optional[List[float]] = None,
    autopct: str = '%1.1f%%',
    colors: Optional[List[str]] = None
) -> str:
    """
    生成饼图
    
    Args:
        labels: 标签列表
        sizes: 数值列表
        title: 图表标题
        output_path: 输出文件路径
        figsize: 图表大小
        explode: 突出显示某些扇区，如 [0, 0.1, 0, 0]
        autopct: 百分比格式
        colors: 自定义颜色列表
    
    Returns:
        输出文件的绝对路径
    """
    plt.figure(figsize=figsize)
    
    plt.pie(sizes, labels=labels, autopct=autopct, startangle=90,
            explode=explode, colors=colors, shadow=True)
    plt.title(title, fontsize=14, fontweight='bold')
    plt.axis('equal')
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    return os.path.abspath(output_path)


def scatter_plot(
    x: List[float],
    y: List[float],
    title: str = "Scatter Plot",
    xlabel: str = "X",
    ylabel: str = "Y",
    output_path: str = "scatter_plot.png",
    figsize: Tuple[int, int] = (10, 6),
    color: str = 'steelblue',
    size: int = 50,
    alpha: float = 0.6,
    grid: bool = True
) -> str:
    """
    生成散点图
    
    Args:
        x: X轴数据
        y: Y轴数据
        title: 图表标题
        xlabel: X轴标签
        ylabel: Y轴标签
        output_path: 输出文件路径
        figsize: 图表大小
        color: 点的颜色
        size: 点的大小
        alpha: 透明度 (0-1)
        grid: 是否显示网格
    
    Returns:
        输出文件的绝对路径
    """
    plt.figure(figsize=figsize)
    
    plt.scatter(x, y, c=color, s=size, alpha=alpha, edgecolors='black', linewidth=0.5)
    plt.title(title, fontsize=14, fontweight='bold')
    plt.xlabel(xlabel, fontsize=12)
    plt.ylabel(ylabel, fontsize=12)
    
    if grid:
        plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    return os.path.abspath(output_path)


def multi_series_bar(
    categories: List[str],
    data: Dict[str, List[float]],
    title: str = "Multi-Series Bar Chart",
    xlabel: str = "Category",
    ylabel: str = "Value",
    output_path: str = "multi_bar_chart.png",
    figsize: Tuple[int, int] = (12, 6)
) -> str:
    """
    生成多系列柱状图（分组柱状图）
    
    Args:
        categories: 类别列表
        data: 数据字典，格式 {'Series1': [v1, v2, ...], 'Series2': [...]}
        title: 图表标题
        xlabel: X轴标签
        ylabel: Y轴标签
        output_path: 输出文件路径
        figsize: 图表大小
    
    Returns:
        输出文件的绝对路径
    """
    import numpy as np
    
    plt.figure(figsize=figsize)
    
    x = np.arange(len(categories))
    width = 0.8 / len(data)  # 柱子宽度
    
    for i, (label, values) in enumerate(data.items()):
        offset = width * i - (width * len(data) / 2 - width / 2)
        plt.bar(x + offset, values, width, label=label)
    
    plt.xlabel(xlabel, fontsize=12)
    plt.ylabel(ylabel, fontsize=12)
    plt.title(title, fontsize=14, fontweight='bold')
    plt.xticks(x, categories, rotation=45, ha='right')
    plt.legend()
    plt.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    return os.path.abspath(output_path)


if __name__ == "__main__":
    # 示例：生成测试图表
    print("Generating example charts...")
    
    # 1. 折线图
    line_chart(
        {'Sales': [100, 150, 120, 180, 200], 'Target': [120, 120, 120, 120, 120]},
        title="Monthly Sales vs Target",
        xlabel="Month",
        ylabel="Amount ($)",
        output_path="example_line.png"
    )
    print("[OK] Line chart: example_line.png")
    
    # 2. 柱状图
    bar_chart(
        ['Q1', 'Q2', 'Q3', 'Q4'],
        [250, 300, 280, 350],
        title="Quarterly Revenue",
        xlabel="Quarter",
        ylabel="Revenue ($K)",
        output_path="example_bar.png"
    )
    print("[OK] Bar chart: example_bar.png")
    
    # 3. 饼图
    pie_chart(
        ['Product A', 'Product B', 'Product C', 'Product D'],
        [30, 25, 20, 25],
        title="Market Share",
        output_path="example_pie.png"
    )
    print("[OK] Pie chart: example_pie.png")
    
    # 4. 散点图
    import random
    x_data = [random.uniform(0, 100) for _ in range(50)]
    y_data = [x * 2 + random.uniform(-20, 20) for x in x_data]
    scatter_plot(
        x_data, y_data,
        title="Correlation Analysis",
        xlabel="Variable X",
        ylabel="Variable Y",
        output_path="example_scatter.png"
    )
    print("[OK] Scatter plot: example_scatter.png")
    
    # 5. 多系列柱状图
    multi_series_bar(
        ['Jan', 'Feb', 'Mar', 'Apr'],
        {'2023': [100, 120, 110, 130], '2024': [120, 140, 130, 150]},
        title="Year-over-Year Comparison",
        output_path="example_multi_bar.png"
    )
    print("[OK] Multi-series bar chart: example_multi_bar.png")
    
    print("\nAll example charts generated successfully!")
