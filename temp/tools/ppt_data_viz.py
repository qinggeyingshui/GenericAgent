"""
ppt_data_viz.py — PPT数据可视化工具（R159, 2026-04-20）

功能：
1. 从Excel/CSV导入数据生成图表
2. 支持数据更新自动刷新图表
3. 集成ppt_chart_toolkit和ppt_auto_layout

依赖: pip install python-pptx pandas openpyxl
"""

import pandas as pd
from pptx import Presentation
from pptx.util import Inches
import sys
import os

# 导入现有工具
sys.path.append(os.path.join(os.path.dirname(__file__)))
from ppt_chart_toolkit import add_chart, new_prs, add_blank_slide, save_prs


def import_data_from_excel(file_path, sheet_name=0, header_row=0):
    """
    从Excel导入数据，返回图表数据格式
    
    Args:
        file_path: Excel文件路径
        sheet_name: 工作表名称或索引（默认0=第一个）
        header_row: 标题行索引（默认0）
    
    Returns:
        {"categories": [...], "series": {"名": [值,...]}}
    
    Excel格式示例：
        | 类别 | 系列1 | 系列2 |
        | Q1   | 100   | 80    |
        | Q2   | 150   | 120   |
    """
    df = pd.read_excel(file_path, sheet_name=sheet_name, header=header_row)
    
    # 第一列作为categories，其余列作为series
    categories = df.iloc[:, 0].astype(str).tolist()
    series = {}
    for col in df.columns[1:]:
        series[str(col)] = df[col].tolist()
    
    return {"categories": categories, "series": series}


def import_data_from_csv(file_path, encoding="utf-8"):
    """
    从CSV导入数据，返回图表数据格式
    
    Args:
        file_path: CSV文件路径
        encoding: 文件编码（默认utf-8，中文可能需要gbk）
    
    Returns:
        {"categories": [...], "series": {"名": [值,...]}}
    """
    df = pd.read_csv(file_path, encoding=encoding)
    
    categories = df.iloc[:, 0].astype(str).tolist()
    series = {}
    for col in df.columns[1:]:
        series[str(col)] = df[col].tolist()
    
    return {"categories": categories, "series": series}


def create_chart_from_file(slide, file_path, chart_type="COLUMN", 
                          l=1.0, t=1.5, w=8.0, h=4.5, title=None,
                          sheet_name=0, encoding="utf-8"):
    """
    从Excel/CSV文件直接创建图表（一步到位）
    
    Args:
        slide: python-pptx slide对象
        file_path: Excel或CSV文件路径
        chart_type: "COLUMN" | "BAR" | "LINE" | "PIE"
        l, t, w, h: 图表位置和大小（英寸）
        title: 图表标题
        sheet_name: Excel工作表（仅Excel有效）
        encoding: CSV编码（仅CSV有效）
    
    Returns:
        Chart对象
    """
    # 根据文件扩展名选择导入方法
    ext = os.path.splitext(file_path)[1].lower()
    
    if ext in [".xlsx", ".xls"]:
        data = import_data_from_excel(file_path, sheet_name=sheet_name)
    elif ext == ".csv":
        data = import_data_from_csv(file_path, encoding=encoding)
    else:
        raise ValueError(f"不支持的文件格式: {ext}，仅支持.xlsx/.xls/.csv")
    
    return add_chart(slide, chart_type, data, l, t, w, h, title)


def update_chart_data(prs, slide_index, chart_index, new_data):
    """
    更新已有图表的数据（实现数据刷新）
    
    Args:
        prs: Presentation对象
        slide_index: 幻灯片索引（从0开始）
        chart_index: 图表在该幻灯片中的索引（从0开始）
        new_data: 新数据，格式同import_data_from_excel返回值
    
    Returns:
        更新后的Chart对象
    
    注意：python-pptx不支持直接修改图表数据，需要删除重建
    """
    from pptx.chart.data import ChartData
    
    slide = prs.slides[slide_index]
    
    # 找到图表shape
    chart_shapes = [s for s in slide.shapes if s.has_chart]
    if chart_index >= len(chart_shapes):
        raise IndexError(f"图表索引{chart_index}超出范围，该幻灯片只有{len(chart_shapes)}个图表")
    
    chart_shape = chart_shapes[chart_index]
    chart = chart_shape.chart
    
    # 保存原图表属性
    chart_type = chart.chart_type
    left, top = chart_shape.left, chart_shape.top
    width, height = chart_shape.width, chart_shape.height
    has_title = chart.has_title
    title_text = chart.chart_title.text_frame.text if has_title else None
    
    # 删除旧图表
    sp = chart_shape.element
    sp.getparent().remove(sp)
    
    # 创建新图表数据
    cd = ChartData()
    cd.categories = new_data["categories"]
    for series_name, values in new_data["series"].items():
        cd.add_series(series_name, values)
    
    # 添加新图表
    new_chart_shape = slide.shapes.add_chart(
        chart_type, left, top, width, height, cd
    )
    new_chart = new_chart_shape.chart
    
    # 恢复标题
    if has_title and title_text:
        new_chart.has_title = True
        new_chart.chart_title.text_frame.text = title_text
    
    return new_chart


def update_chart_from_file(prs, slide_index, chart_index, file_path,
                          sheet_name=0, encoding="utf-8"):
    """
    从文件更新图表数据（便捷函数）
    
    Args:
        prs: Presentation对象
        slide_index: 幻灯片索引
        chart_index: 图表索引
        file_path: Excel或CSV文件路径
        sheet_name: Excel工作表
        encoding: CSV编码
    
    Returns:
        更新后的Chart对象
    """
    ext = os.path.splitext(file_path)[1].lower()
    
    if ext in [".xlsx", ".xls"]:
        new_data = import_data_from_excel(file_path, sheet_name=sheet_name)
    elif ext == ".csv":
        new_data = import_data_from_csv(file_path, encoding=encoding)
    else:
        raise ValueError(f"不支持的文件格式: {ext}")
    
    return update_chart_data(prs, slide_index, chart_index, new_data)


# ── 便捷常量 ──────────────────────────────────────────────
CHART_COLUMN = "COLUMN"
CHART_BAR    = "BAR"
CHART_LINE   = "LINE"
CHART_PIE    = "PIE"
