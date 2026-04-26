"""
ppt_chart_styles.py — 图表样式模板库
提供10+种预设图表样式，包含配色方案、字体、边框等
依赖: python-pptx
"""

from pptx.util import Pt
from pptx.enum.chart import XL_LEGEND_POSITION
from pptx.dml.color import RGBColor

# ── 配色方案 ──────────────────────────────────────────────
COLOR_SCHEMES = {
    "business": [  # 商务蓝
        RGBColor(68, 114, 196),   # 主蓝
        RGBColor(237, 125, 49),   # 橙
        RGBColor(165, 165, 165),  # 灰
        RGBColor(255, 192, 0),    # 黄
        RGBColor(91, 155, 213),   # 浅蓝
    ],
    "vibrant": [  # 活力彩
        RGBColor(255, 87, 87),    # 红
        RGBColor(255, 195, 0),    # 金
        RGBColor(0, 184, 148),    # 青
        RGBColor(108, 92, 231),   # 紫
        RGBColor(255, 159, 64),   # 橙
    ],
    "nature": [  # 自然绿
        RGBColor(112, 173, 71),   # 绿
        RGBColor(158, 188, 66),   # 黄绿
        RGBColor(84, 130, 53),    # 深绿
        RGBColor(192, 215, 140),  # 浅绿
        RGBColor(146, 208, 80),   # 亮绿
    ],
    "elegant": [  # 优雅紫
        RGBColor(112, 48, 160),   # 紫
        RGBColor(192, 0, 0),      # 酒红
        RGBColor(146, 208, 80),   # 绿
        RGBColor(255, 192, 0),    # 金
        RGBColor(0, 176, 240),    # 蓝
    ],
    "warm": [  # 暖色调
        RGBColor(255, 127, 80),   # 珊瑚
        RGBColor(255, 215, 0),    # 金
        RGBColor(255, 160, 122),  # 浅珊瑚
        RGBColor(255, 99, 71),    # 番茄
        RGBColor(255, 228, 181),  # 杏
    ],
    "cool": [  # 冷色调
        RGBColor(70, 130, 180),   # 钢蓝
        RGBColor(100, 149, 237),  # 矢车菊蓝
        RGBColor(135, 206, 250),  # 天蓝
        RGBColor(176, 224, 230),  # 粉蓝
        RGBColor(95, 158, 160),   # 军蓝
    ],
    "monochrome": [  # 单色灰
        RGBColor(64, 64, 64),     # 深灰
        RGBColor(128, 128, 128),  # 中灰
        RGBColor(192, 192, 192),  # 浅灰
        RGBColor(224, 224, 224),  # 极浅灰
        RGBColor(96, 96, 96),     # 灰
    ],
}


# ── 样式模板 ──────────────────────────────────────────────
CHART_STYLES = {
    "default": {
        "color_scheme": "business",
        "font_size": 12,
        "legend_position": XL_LEGEND_POSITION.BOTTOM,
        "has_legend": True,
        "data_labels": False,
    },
    "minimal": {
        "color_scheme": "monochrome",
        "font_size": 10,
        "legend_position": XL_LEGEND_POSITION.RIGHT,
        "has_legend": True,
        "data_labels": False,
    },
    "colorful": {
        "color_scheme": "vibrant",
        "font_size": 14,
        "legend_position": XL_LEGEND_POSITION.BOTTOM,
        "has_legend": True,
        "data_labels": True,
    },
    "professional": {
        "color_scheme": "business",
        "font_size": 11,
        "legend_position": XL_LEGEND_POSITION.RIGHT,
        "has_legend": True,
        "data_labels": False,
    },
    "presentation": {
        "color_scheme": "elegant",
        "font_size": 16,
        "legend_position": XL_LEGEND_POSITION.BOTTOM,
        "has_legend": True,
        "data_labels": True,
    },
    "report": {
        "color_scheme": "cool",
        "font_size": 10,
        "legend_position": XL_LEGEND_POSITION.RIGHT,
        "has_legend": True,
        "data_labels": False,
    },
    "dashboard": {
        "color_scheme": "nature",
        "font_size": 12,
        "legend_position": XL_LEGEND_POSITION.BOTTOM,
        "has_legend": False,
        "data_labels": True,
    },
    "infographic": {
        "color_scheme": "warm",
        "font_size": 14,
        "legend_position": XL_LEGEND_POSITION.BOTTOM,
        "has_legend": True,
        "data_labels": True,
    },
}


def apply_style(chart, style_name="default"):
    """
    应用预设样式到图表对象
    chart: python-pptx Chart 对象
    style_name: 样式名称，见 CHART_STYLES
    """
    if style_name not in CHART_STYLES:
        style_name = "default"
    
    style = CHART_STYLES[style_name]
    colors = COLOR_SCHEMES[style["color_scheme"]]
    
    # 应用配色
    for i, series in enumerate(chart.series):
        color = colors[i % len(colors)]
        series.format.fill.solid()
        series.format.fill.fore_color.rgb = color
    
    # 图例
    chart.has_legend = style["has_legend"]
    if chart.has_legend:
        chart.legend.position = style["legend_position"]
        chart.legend.font.size = Pt(style["font_size"] - 2)
    
    # 数据标签
    if style["data_labels"]:
        for series in chart.series:
            series.has_data_labels = True
            series.data_labels.font.size = Pt(style["font_size"] - 2)
    
    # 字体大小
    if chart.has_title:
        chart.chart_title.text_frame.paragraphs[0].font.size = Pt(style["font_size"] + 4)
    
    return chart


def list_styles():
    """列出所有可用样式"""
    return list(CHART_STYLES.keys())


def get_style_info(style_name):
    """获取样式详细信息"""
    if style_name not in CHART_STYLES:
        return None
    return CHART_STYLES[style_name]