"""
ppt_smartart.py — SmartArt 图形库
使用 python-pptx 形状组合模拟 SmartArt 效果
支持：流程图、列表、循环图、组织结构图、金字塔图
"""

from pptx.util import Inches, Pt
from pptx.enum.shapes import MSO_SHAPE
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN


# ── 流程图 ──────────────────────────────────────────────
def add_process_horizontal(slide, items, left=1.0, top=2.0, width=8.0, height=1.5):
    """
    横向流程图
    items: [{"text": "步骤1", "color": (68,114,196)}, ...]
    返回形状列表
    """
    shapes = []
    n = len(items)
    box_width = (width - 0.3 * (n - 1)) / n  # 减去箭头间距
    box_height = height
    
    for i, item in enumerate(items):
        # 矩形框
        x = left + i * (box_width + 0.3)
        rect = slide.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE,
            Inches(x), Inches(top),
            Inches(box_width), Inches(box_height)
        )
        
        # 填充颜色
        color = item.get("color", (68, 114, 196))
        rect.fill.solid()
        rect.fill.fore_color.rgb = RGBColor(*color)
        
        # 文本
        text_frame = rect.text_frame
        text_frame.text = item["text"]
        text_frame.paragraphs[0].alignment = PP_ALIGN.CENTER
        text_frame.paragraphs[0].font.size = Pt(14)
        text_frame.paragraphs[0].font.color.rgb = RGBColor(255, 255, 255)
        text_frame.vertical_anchor = 1  # 垂直居中
        
        shapes.append(rect)
        
        # 箭头（除最后一个）
        if i < n - 1:
            arrow_x = x + box_width
            arrow = slide.shapes.add_shape(
                MSO_SHAPE.RIGHT_ARROW,
                Inches(arrow_x), Inches(top + box_height / 2 - 0.15),
                Inches(0.3), Inches(0.3)
            )
            arrow.fill.solid()
            arrow.fill.fore_color.rgb = RGBColor(128, 128, 128)
            arrow.line.color.rgb = RGBColor(128, 128, 128)
            shapes.append(arrow)
    
    return shapes


def add_process_vertical(slide, items, left=3.0, top=1.0, width=4.0, height=5.0):
    """
    纵向流程图
    items: [{"text": "步骤1", "color": (68,114,196)}, ...]
    """
    shapes = []
    n = len(items)
    box_height = (height - 0.3 * (n - 1)) / n
    box_width = width
    
    for i, item in enumerate(items):
        y = top + i * (box_height + 0.3)
        rect = slide.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE,
            Inches(left), Inches(y),
            Inches(box_width), Inches(box_height)
        )
        
        color = item.get("color", (68, 114, 196))
        rect.fill.solid()
        rect.fill.fore_color.rgb = RGBColor(*color)
        
        text_frame = rect.text_frame
        text_frame.text = item["text"]
        text_frame.paragraphs[0].alignment = PP_ALIGN.CENTER
        text_frame.paragraphs[0].font.size = Pt(14)
        text_frame.paragraphs[0].font.color.rgb = RGBColor(255, 255, 255)
        text_frame.vertical_anchor = 1
        
        shapes.append(rect)
        
        if i < n - 1:
            arrow_y = y + box_height
            arrow = slide.shapes.add_shape(
                MSO_SHAPE.DOWN_ARROW,
                Inches(left + box_width / 2 - 0.15), Inches(arrow_y),
                Inches(0.3), Inches(0.3)
            )
            arrow.fill.solid()
            arrow.fill.fore_color.rgb = RGBColor(128, 128, 128)
            arrow.line.color.rgb = RGBColor(128, 128, 128)
            shapes.append(arrow)
    
    return shapes


# ── 列表 ──────────────────────────────────────────────
def add_bullet_list(slide, items, left=1.5, top=1.5, width=7.0, height=4.0):
    """
    项目符号列表
    items: ["项目1", "项目2", ...]
    """
    shapes = []
    n = len(items)
    item_height = height / n
    
    for i, text in enumerate(items):
        y = top + i * item_height
        
        # 圆形项目符号
        bullet = slide.shapes.add_shape(
            MSO_SHAPE.OVAL,
            Inches(left), Inches(y + item_height / 2 - 0.1),
            Inches(0.2), Inches(0.2)
        )
        bullet.fill.solid()
        bullet.fill.fore_color.rgb = RGBColor(68, 114, 196)
        bullet.line.fill.background()
        shapes.append(bullet)
        
        # 文本
        textbox = slide.shapes.add_textbox(
            Inches(left + 0.3), Inches(y),
            Inches(width - 0.3), Inches(item_height)
        )
        text_frame = textbox.text_frame
        text_frame.text = text
        text_frame.paragraphs[0].font.size = Pt(16)
        text_frame.vertical_anchor = 1
        shapes.append(textbox)
    
    return shapes


# ── 循环图 ──────────────────────────────────────────────
def add_cycle(slide, items, center_x=5.0, center_y=3.75, radius=2.0):
    """
    循环图
    items: [{"text": "阶段1", "color": (68,114,196)}, ...]
    """
    import math
    shapes = []
    n = len(items)
    angle_step = 2 * math.pi / n
    box_size = 1.2
    
    for i, item in enumerate(items):
        angle = i * angle_step - math.pi / 2  # 从顶部开始
        x = center_x + radius * math.cos(angle) - box_size / 2
        y = center_y + radius * math.sin(angle) - box_size / 2
        
        # 圆角矩形
        rect = slide.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE,
            Inches(x), Inches(y),
            Inches(box_size), Inches(box_size)
        )
        
        color = item.get("color", (68, 114, 196))
        rect.fill.solid()
        rect.fill.fore_color.rgb = RGBColor(*color)
        
        text_frame = rect.text_frame
        text_frame.text = item["text"]
        text_frame.paragraphs[0].alignment = PP_ALIGN.CENTER
        text_frame.paragraphs[0].font.size = Pt(12)
        text_frame.paragraphs[0].font.color.rgb = RGBColor(255, 255, 255)
        text_frame.vertical_anchor = 1
        text_frame.word_wrap = True
        
        shapes.append(rect)
    
    # 中心圆形箭头提示
    center_circle = slide.shapes.add_shape(
        MSO_SHAPE.OVAL,
        Inches(center_x - 0.3), Inches(center_y - 0.3),
        Inches(0.6), Inches(0.6)
    )
    center_circle.fill.solid()
    center_circle.fill.fore_color.rgb = RGBColor(200, 200, 200)
    center_circle.line.color.rgb = RGBColor(128, 128, 128)
    shapes.append(center_circle)
    
    return shapes


# ── 组织结构图 ──────────────────────────────────────────────
def add_org_chart(slide, root, left=1.0, top=1.0, width=8.0, level_height=1.5):
    """
    组织结构图
    root: {"text": "CEO", "children": [{"text": "CTO", "children": [...]}, ...]}
    """
    shapes = []
    
    def count_leaves(node):
        if "children" not in node or not node["children"]:
            return 1
        return sum(count_leaves(child) for child in node["children"])
    
    def draw_node(node, x, y, node_width, level):
        # 绘制节点
        rect = slide.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE,
            Inches(x), Inches(y),
            Inches(node_width), Inches(1.0)
        )
        
        color = node.get("color", (68, 114, 196))
        rect.fill.solid()
        rect.fill.fore_color.rgb = RGBColor(*color)
        
        text_frame = rect.text_frame
        text_frame.text = node["text"]
        text_frame.paragraphs[0].alignment = PP_ALIGN.CENTER
        text_frame.paragraphs[0].font.size = Pt(12)
        text_frame.paragraphs[0].font.color.rgb = RGBColor(255, 255, 255)
        text_frame.vertical_anchor = 1
        
        shapes.append(rect)
        
        # 递归绘制子节点
        if "children" in node and node["children"]:
            children = node["children"]
            total_leaves = sum(count_leaves(child) for child in children)
            child_x = x
            
            for child in children:
                child_leaves = count_leaves(child)
                child_width = (width * child_leaves / total_leaves) * 0.8
                child_x_center = child_x + (width * child_leaves / total_leaves) / 2 - child_width / 2
                
                # 连接线
                line = slide.shapes.add_connector(
                    1,  # msoConnectorStraight
                    Inches(x + node_width / 2), Inches(y + 1.0),
                    Inches(child_x_center + child_width / 2), Inches(y + level_height)
                )
                line.line.color.rgb = RGBColor(128, 128, 128)
                shapes.append(line)
                
                draw_node(child, child_x_center, y + level_height, child_width, level + 1)
                child_x += width * child_leaves / total_leaves
    
    # 计算根节点宽度
    root_width = min(2.5, width * 0.3)
    root_x = left + width / 2 - root_width / 2
    draw_node(root, root_x, top, root_width, 0)
    
    return shapes


# ── 金字塔图 ──────────────────────────────────────────────
def add_pyramid(slide, items, left=2.0, top=1.0, width=6.0, height=5.0):
    """
    金字塔图
    items: [{"text": "顶层", "color": (68,114,196)}, ...] 从上到下
    """
    shapes = []
    n = len(items)
    layer_height = height / n
    
    for i, item in enumerate(items):
        # 计算梯形宽度（从上到下递增）
        top_width = width * (i + 1) / n
        bottom_width = width * (i + 2) / n if i < n - 1 else width
        
        y = top + i * layer_height
        x_top = left + (width - top_width) / 2
        x_bottom = left + (width - bottom_width) / 2
        
        # 使用梯形形状
        trapezoid = slide.shapes.add_shape(
            MSO_SHAPE.TRAPEZOID,
            Inches(x_bottom), Inches(y),
            Inches(bottom_width), Inches(layer_height)
        )
        
        color = item.get("color", (68, 114, 196))
        trapezoid.fill.solid()
        trapezoid.fill.fore_color.rgb = RGBColor(*color)
        trapezoid.line.color.rgb = RGBColor(255, 255, 255)
        trapezoid.line.width = Pt(2)
        
        text_frame = trapezoid.text_frame
        text_frame.text = item["text"]
        text_frame.paragraphs[0].alignment = PP_ALIGN.CENTER
        text_frame.paragraphs[0].font.size = Pt(14)
        text_frame.paragraphs[0].font.color.rgb = RGBColor(255, 255, 255)
        text_frame.vertical_anchor = 1
        
        shapes.append(trapezoid)
    
    return shapes