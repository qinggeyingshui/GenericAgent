"""
ppt_auto_layout.py — PPT智能排版工具（R145, 2026-04-20）

提供3种自动布局模式：
1. 图文布局：自动调整图片和文字位置
2. 纯文字布局：根据内容长度自动调整字号和行距
3. 图表布局：自动调整图表大小占满空间

依赖: python-pptx
设计规范: 遵循ppt_com_sop五大原则（对齐/留白/配色/字体/图文）
"""

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR


def add_image_text_layout(slide, image_path, title, content, 
                          layout="left_image", margin=0.5):
    """
    图文布局：图片+文字自动排版
    
    Args:
        slide: python-pptx slide对象
        image_path: 图片路径（绝对路径）
        title: 标题文字
        content: 正文内容（支持\n换行）
        layout: "left_image"(左图右文) | "top_image"(上图下文)
        margin: 边距（英寸）
    
    Returns:
        (image_shape, title_shape, content_shape)
    """
    slide_w, slide_h = 10.0, 7.5  # 标准16:9尺寸
    
    if layout == "left_image":
        # 左图右文：图片占40%宽度
        img_w = (slide_w - 3*margin) * 0.4
        img_h = slide_h - 2*margin
        img_l, img_t = margin, margin
        
        text_l = img_l + img_w + margin
        text_w = slide_w - text_l - margin
        title_h = 0.8
        content_h = slide_h - 2*margin - title_h - 0.3
        
        img = slide.shapes.add_picture(image_path, 
                                       Inches(img_l), Inches(img_t),
                                       Inches(img_w), Inches(img_h))
        
        title_box = slide.shapes.add_textbox(
            Inches(text_l), Inches(margin),
            Inches(text_w), Inches(title_h)
        )
        tf = title_box.text_frame
        tf.text = title
        tf.paragraphs[0].font.size = Pt(28)
        tf.paragraphs[0].font.bold = True
        
        content_box = slide.shapes.add_textbox(
            Inches(text_l), Inches(margin + title_h + 0.3),
            Inches(text_w), Inches(content_h)
        )
        tf = content_box.text_frame
        tf.text = content
        tf.word_wrap = True
        # 自动调整字号：根据行数
        lines = content.count('\n') + 1
        if lines <= 5:
            font_size = 22
        elif lines <= 7:
            font_size = 20
        else:
            font_size = 18
        tf.paragraphs[0].font.size = Pt(font_size)
        tf.paragraphs[0].line_spacing = 1.3
        
        return (img, title_box, content_box)
    
    else:  # top_image
        # 上图下文：图片占50%高度
        img_h = (slide_h - 3*margin) * 0.5
        img_w = slide_w - 2*margin
        img_l, img_t = margin, margin
        
        img = slide.shapes.add_picture(image_path,
                                       Inches(img_l), Inches(img_t),
                                       Inches(img_w), Inches(img_h))
        
        text_t = img_t + img_h + margin
        text_h = slide_h - text_t - margin
        title_h = 0.6
        
        title_box = slide.shapes.add_textbox(
            Inches(margin), Inches(text_t),
            Inches(slide_w - 2*margin), Inches(title_h)
        )
        tf = title_box.text_frame
        tf.text = title
        tf.paragraphs[0].font.size = Pt(28)
        tf.paragraphs[0].font.bold = True
        tf.paragraphs[0].alignment = PP_ALIGN.CENTER
        
        content_box = slide.shapes.add_textbox(
            Inches(margin), Inches(text_t + title_h + 0.2),
            Inches(slide_w - 2*margin), Inches(text_h - title_h - 0.2)
        )
        tf = content_box.text_frame
        tf.text = content
        tf.word_wrap = True
        lines = content.count('\n') + 1
        font_size = 20 if lines <= 5 else 18
        tf.paragraphs[0].font.size = Pt(font_size)
        tf.paragraphs[0].line_spacing = 1.3
        
        return (img, title_box, content_box)


def add_text_layout(slide, title, content, subtitle=None, margin=0.8):
    """
    纯文字布局：标题+正文，自动调整字号和行距
    
    Args:
        slide: python-pptx slide对象
        title: 标题文字
        content: 正文内容（支持\n换行）
        subtitle: 副标题（可选）
        margin: 边距（英寸）
    
    Returns:
        (title_shape, content_shape) 或 (title_shape, subtitle_shape, content_shape)
    """
    slide_w, slide_h = 10.0, 7.5
    
    # 标题区域
    title_h = 1.0
    title_box = slide.shapes.add_textbox(
        Inches(margin), Inches(margin),
        Inches(slide_w - 2*margin), Inches(title_h)
    )
    tf = title_box.text_frame
    tf.text = title
    tf.paragraphs[0].font.size = Pt(32)
    tf.paragraphs[0].font.bold = True
    tf.paragraphs[0].alignment = PP_ALIGN.CENTER
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    
    # 副标题（可选）
    if subtitle:
        subtitle_h = 0.5
        subtitle_box = slide.shapes.add_textbox(
            Inches(margin), Inches(margin + title_h),
            Inches(slide_w - 2*margin), Inches(subtitle_h)
        )
        tf = subtitle_box.text_frame
        tf.text = subtitle
        tf.paragraphs[0].font.size = Pt(20)
        tf.paragraphs[0].alignment = PP_ALIGN.CENTER
        content_t = margin + title_h + subtitle_h + 0.3
    else:
        subtitle_box = None
        content_t = margin + title_h + 0.3
    
    # 正文区域
    content_h = slide_h - content_t - margin
    content_box = slide.shapes.add_textbox(
        Inches(margin), Inches(content_t),
        Inches(slide_w - 2*margin), Inches(content_h)
    )
    tf = content_box.text_frame
    tf.text = content
    tf.word_wrap = True
    
    # 自动调整字号：根据内容长度
    lines = content.count('\n') + 1
    char_count = len(content)
    
    if lines <= 3 and char_count <= 100:
        font_size = 24
        line_spacing = 1.5
    elif lines <= 5 and char_count <= 200:
        font_size = 22
        line_spacing = 1.4
    elif lines <= 7 and char_count <= 300:
        font_size = 20
        line_spacing = 1.3
    else:
        font_size = 18
        line_spacing = 1.2
    
    tf.paragraphs[0].font.size = Pt(font_size)
    tf.paragraphs[0].line_spacing = line_spacing
    
    if subtitle_box:
        return (title_box, subtitle_box, content_box)
    else:
        return (title_box, content_box)


def add_chart_layout(slide, title, chart_data, chart_type="COLUMN", margin=0.6):
    """
    图表布局：标题+图表，自动调整图表大小
    
    Args:
        slide: python-pptx slide对象
        title: 标题文字
        chart_data: 图表数据，格式同ppt_chart_toolkit
                   {"categories": [...], "series": {"名": [值,...]}}
        chart_type: "COLUMN" | "BAR" | "LINE" | "PIE"
        margin: 边距（英寸）
    
    Returns:
        (title_shape, chart_shape)
    
    注意: 需要先导入ppt_chart_toolkit
    """
    import sys
    import os
    sys.path.append(os.path.join(os.path.dirname(__file__)))
    from ppt_chart_toolkit import add_chart
    
    slide_w, slide_h = 10.0, 7.5
    
    # 标题区域
    title_h = 0.8
    title_box = slide.shapes.add_textbox(
        Inches(margin), Inches(margin),
        Inches(slide_w - 2*margin), Inches(title_h)
    )
    tf = title_box.text_frame
    tf.text = title
    tf.paragraphs[0].font.size = Pt(28)
    tf.paragraphs[0].font.bold = True
    tf.paragraphs[0].alignment = PP_ALIGN.CENTER
    
    # 图表区域：占满剩余空间
    chart_t = margin + title_h + 0.3
    chart_h = slide_h - chart_t - margin
    chart_w = slide_w - 2*margin
    
    # add_chart返回Chart对象，需要通过slide.shapes获取最后添加的shape
    chart = add_chart(slide, chart_type, chart_data,
                     l=margin, t=chart_t, w=chart_w, h=chart_h,
                     title=None)  # 标题已在上方
    chart_shape = slide.shapes[-1]  # 最后添加的shape
    
    return (title_box, chart_shape)


# ── 便捷函数 ──────────────────────────────────────────────

def new_prs():
    """新建空白演示文稿"""
    return Presentation()


def add_blank_slide(prs):
    """添加空白幻灯片"""
    return prs.slides.add_slide(prs.slide_layouts[6])


def save_prs(prs, path):
    """保存演示文稿"""
    prs.save(path)
    return path


# ── 增强功能 (R174, 2026-04-20) ──────────────────────────

def add_multi_column_layout(slide, title, columns_content, num_columns=2, margin=0.6):
    """
    多列布局：标题+多列文字
    
    Args:
        slide: python-pptx slide对象
        title: 标题文字
        columns_content: 列表，每个元素是一列的文字内容
        num_columns: 列数（2或3）
        margin: 边距（英寸）
    
    Returns:
        (title_shape, [column_shapes])
    """
    slide_w, slide_h = 10.0, 7.5
    
    # 标题区域
    title_h = 0.8
    title_box = slide.shapes.add_textbox(
        Inches(margin), Inches(margin),
        Inches(slide_w - 2*margin), Inches(title_h)
    )
    tf = title_box.text_frame
    tf.text = title
    tf.paragraphs[0].font.size = Pt(28)
    tf.paragraphs[0].font.bold = True
    tf.paragraphs[0].alignment = PP_ALIGN.CENTER
    
    # 计算列宽和间距
    content_t = margin + title_h + 0.3
    content_h = slide_h - content_t - margin
    total_w = slide_w - 2*margin
    gap = 0.3  # 列间距
    col_w = (total_w - gap * (num_columns - 1)) / num_columns
    
    # 创建各列
    column_shapes = []
    for i, content in enumerate(columns_content[:num_columns]):
        col_l = margin + i * (col_w + gap)
        col_box = slide.shapes.add_textbox(
            Inches(col_l), Inches(content_t),
            Inches(col_w), Inches(content_h)
        )
        tf = col_box.text_frame
        tf.text = content
        tf.word_wrap = True
        
        # 自动调整字号
        lines = content.count('\n') + 1
        if lines <= 5:
            font_size = 20
        elif lines <= 8:
            font_size = 18
        else:
            font_size = 16
        
        tf.paragraphs[0].font.size = Pt(font_size)
        tf.paragraphs[0].line_spacing = 1.3
        column_shapes.append(col_box)
    
    return (title_box, column_shapes)


def add_mixed_content_layout(slide, title, content_blocks, margin=0.5):
    """
    图文混排布局：标题+图片和文字混合排列
    
    Args:
        slide: python-pptx slide对象
        title: 标题文字
        content_blocks: 列表，每个元素是字典：
                       {"type": "text", "content": "文字内容"}
                       {"type": "image", "path": "图片路径", "height": 2.0}
        margin: 边距（英寸）
    
    Returns:
        (title_shape, [content_shapes])
    """
    slide_w, slide_h = 10.0, 7.5
    
    # 标题区域
    title_h = 0.7
    title_box = slide.shapes.add_textbox(
        Inches(margin), Inches(margin),
        Inches(slide_w - 2*margin), Inches(title_h)
    )
    tf = title_box.text_frame
    tf.text = title
    tf.paragraphs[0].font.size = Pt(26)
    tf.paragraphs[0].font.bold = True
    
    # 内容区域
    content_t = margin + title_h + 0.2
    content_w = slide_w - 2*margin
    current_y = content_t
    content_shapes = []
    
    for block in content_blocks:
        if current_y >= slide_h - margin:
            break  # 超出页面
        
        if block["type"] == "text":
            # 文字块
            text_h = 1.0  # 预估高度
            text_box = slide.shapes.add_textbox(
                Inches(margin), Inches(current_y),
                Inches(content_w), Inches(text_h)
            )
            tf = text_box.text_frame
            tf.text = block["content"]
            tf.word_wrap = True
            tf.paragraphs[0].font.size = Pt(18)
            tf.paragraphs[0].line_spacing = 1.3
            content_shapes.append(text_box)
            current_y += text_h + 0.2
            
        elif block["type"] == "image":
            # 图片块
            img_h = block.get("height", 2.0)
            img_w = content_w
            img = slide.shapes.add_picture(
                block["path"],
                Inches(margin), Inches(current_y),
                Inches(img_w), Inches(img_h)
            )
            content_shapes.append(img)
            current_y += img_h + 0.2
    
    return (title_box, content_shapes)


def auto_select_layout(slide, content_dict, margin=0.6):
    """
    响应式布局选择：根据内容自动选择最佳布局
    
    Args:
        slide: python-pptx slide对象
        content_dict: 内容字典，包含：
                     {"title": "标题",
                      "text": "文字内容" (可选),
                      "images": ["路径1", "路径2"] (可选),
                      "chart_data": {...} (可选),
                      "columns": ["列1", "列2"] (可选)}
        margin: 边距（英寸）
    
    Returns:
        选择的布局类型和创建的shapes
    """
    title = content_dict.get("title", "")
    text = content_dict.get("text", "")
    images = content_dict.get("images", [])
    chart_data = content_dict.get("chart_data")
    columns = content_dict.get("columns", [])
    
    # 决策逻辑
    if chart_data:
        # 有图表数据 → 图表布局
        return ("chart", add_chart_layout(slide, title, chart_data, margin=margin))
    
    elif columns and len(columns) >= 2:
        # 有多列内容 → 多列布局
        num_cols = min(len(columns), 3)
        return ("multi_column", add_multi_column_layout(slide, title, columns, num_cols, margin))
    
    elif images and text:
        # 有图片和文字 → 图文混排或图文布局
        if len(images) > 1:
            # 多图片 → 混排布局
            blocks = []
            text_parts = text.split('\n\n')  # 按段落分割
            for i, img_path in enumerate(images):
                if i < len(text_parts):
                    blocks.append({"type": "text", "content": text_parts[i]})
                blocks.append({"type": "image", "path": img_path, "height": 1.8})
            return ("mixed", add_mixed_content_layout(slide, title, blocks, margin))
        else:
            # 单图片 → 左图右文布局
            return ("image_text", add_image_text_layout(slide, images[0], title, text, "left_image", margin))
    
    elif images and not text:
        # 只有图片 → 上图下文布局（文字为空）
        return ("image_only", add_image_text_layout(slide, images[0], title, "", "top_image", margin))
    
    else:
        # 只有文字 → 纯文字布局
        return ("text_only", add_text_layout(slide, title, text, margin=margin))


# ========== R204 增强功能 (2026-04-21) ==========

def add_timeline_layout(slide, title, timeline_items, margin=0.5):
    """时间线布局（新增布局模式4）
    
    Args:
        slide: slide对象
        title: 标题
        timeline_items: [{"time": str, "event": str}, ...]
        margin: 边距
    
    Returns:
        list of shapes
    """
    slide_w, slide_h = 10.0, 7.5
    
    # 标题
    title_box = slide.shapes.add_textbox(
        Inches(margin), Inches(margin),
        Inches(slide_w - 2*margin), Inches(0.8)
    )
    title_frame = title_box.text_frame
    title_frame.text = title
    title_p = title_frame.paragraphs[0]
    title_p.font.size = Pt(32)
    title_p.font.bold = True
    title_p.alignment = PP_ALIGN.CENTER
    
    # 时间线
    start_y = margin + 1.2
    item_h = (slide_h - start_y - margin) / len(timeline_items)
    shapes = [title_box]
    
    for i, item in enumerate(timeline_items):
        y = start_y + i * item_h
        
        # 时间点
        time_box = slide.shapes.add_textbox(
            Inches(margin), Inches(y),
            Inches(2.0), Inches(item_h * 0.8)
        )
        time_frame = time_box.text_frame
        time_frame.text = item["time"]
        time_frame.paragraphs[0].font.size = Pt(18)
        time_frame.paragraphs[0].font.bold = True
        
        # 事件
        event_box = slide.shapes.add_textbox(
            Inches(margin + 2.5), Inches(y),
            Inches(slide_w - margin - 3.0), Inches(item_h * 0.8)
        )
        event_frame = event_box.text_frame
        event_frame.text = item["event"]
        event_frame.paragraphs[0].font.size = Pt(16)
        
        shapes.extend([time_box, event_box])
    
    return shapes


def add_comparison_layout(slide, title, left_content, right_content, margin=0.5):
    """对比布局（新增布局模式5）
    
    Args:
        slide: slide对象
        title: 标题
        left_content: {"title": str, "points": [str]}
        right_content: {"title": str, "points": [str]}
        margin: 边距
    
    Returns:
        list of shapes
    """
    slide_w, slide_h = 10.0, 7.5
    
    # 标题
    title_box = slide.shapes.add_textbox(
        Inches(margin), Inches(margin),
        Inches(slide_w - 2*margin), Inches(0.8)
    )
    title_frame = title_box.text_frame
    title_frame.text = title
    title_p = title_frame.paragraphs[0]
    title_p.font.size = Pt(32)
    title_p.font.bold = True
    title_p.alignment = PP_ALIGN.CENTER
    
    # 左右两栏
    col_w = (slide_w - 3*margin) / 2
    start_y = margin + 1.2
    content_h = slide_h - start_y - margin
    
    shapes = [title_box]
    
    for i, content in enumerate([left_content, right_content]):
        x = margin if i == 0 else margin + col_w + margin
        
        # 子标题
        subtitle_box = slide.shapes.add_textbox(
            Inches(x), Inches(start_y),
            Inches(col_w), Inches(0.6)
        )
        subtitle_frame = subtitle_box.text_frame
        subtitle_frame.text = content["title"]
        subtitle_frame.paragraphs[0].font.size = Pt(24)
        subtitle_frame.paragraphs[0].font.bold = True
        subtitle_frame.paragraphs[0].alignment = PP_ALIGN.CENTER
        
        # 要点列表
        points_box = slide.shapes.add_textbox(
            Inches(x), Inches(start_y + 0.8),
            Inches(col_w), Inches(content_h - 0.8)
        )
        points_frame = points_box.text_frame
        points_frame.word_wrap = True
        
        for point in content["points"]:
            p = points_frame.add_paragraph()
            p.text = f"• {point}"
            p.font.size = Pt(16)
            p.space_before = Pt(6)
        
        shapes.extend([subtitle_box, points_box])
    
    return shapes


def detect_content_type(content):
    """检测内容类型
    
    Args:
        content: {"title": str, "text": str, "images": [], "data": {}}
    
    Returns:
        str: timeline/comparison/chart/image_text/text_only
    """
    text = content.get("text", "")
    images = content.get("images", [])
    data = content.get("data", {})
    
    # 时间线检测
    if any(keyword in text for keyword in ["时间线", "历程", "发展", "timeline"]):
        return "timeline"
    
    # 对比检测
    if any(keyword in text for keyword in ["对比", "比较", "vs", "VS", "versus"]):
        return "comparison"
    
    # 图表检测
    if data or any(keyword in text for keyword in ["数据", "图表", "统计", "chart"]):
        return "chart"
    
    # 图文检测
    if images and text:
        return "image_text"
    
    # 纯文字
    return "text_only"


def calc_beauty_score(slide):
    """计算排版美观度评分
    
    Args:
        slide: slide对象
    
    Returns:
        int: 美观度评分 (0-100)
    """
    score = 100
    shapes = slide.shapes
    
    if len(shapes) == 0:
        return 0
    
    # 1. 对齐检查 (30分)
    left_positions = []
    top_positions = []
    for shape in shapes:
        if hasattr(shape, 'left'):
            left_positions.append(shape.left)
        if hasattr(shape, 'top'):
            top_positions.append(shape.top)
    
    # 检查是否有对齐
    if len(set(left_positions)) > len(shapes) * 0.8:
        score -= 15  # 左对齐不足
    if len(set(top_positions)) > len(shapes) * 0.8:
        score -= 15  # 顶对齐不足
    
    # 2. 留白检查 (30分)
    slide_w = 9144000  # EMU单位
    slide_h = 6858000
    
    total_area = 0
    for shape in shapes:
        if hasattr(shape, 'width') and hasattr(shape, 'height'):
            total_area += shape.width * shape.height
    
    coverage = total_area / (slide_w * slide_h)
    if coverage > 0.8:
        score -= 20  # 过于拥挤
    elif coverage < 0.3:
        score -= 10  # 过于空旷
    
    # 3. 字体大小检查 (20分)
    font_sizes = []
    for shape in shapes:
        if hasattr(shape, 'text_frame'):
            for paragraph in shape.text_frame.paragraphs:
                if paragraph.font.size:
                    font_sizes.append(paragraph.font.size)
    
    if font_sizes:
        min_size = min(font_sizes)
        max_size = max(font_sizes)
        if min_size < 140000:  # 小于14pt
            score -= 10
        if max_size - min_size > 500000:  # 字号差异过大
            score -= 10
    
    # 4. 元素数量检查 (20分)
    if len(shapes) > 15:
        score -= 15  # 元素过多
    elif len(shapes) < 2:
        score -= 5  # 元素过少
    
    return max(0, min(100, score))


def smart_layout(slide, content, auto_detect=True):
    """智能布局（整合所有布局模式）
    
    Args:
        slide: slide对象
        content: {
            "title": str,
            "text": str,
            "images": [],
            "data": {},
            "timeline": [],
            "comparison": {}
        }
        auto_detect: 是否自动检测内容类型
    
    Returns:
        {"layout_type": str, "shapes": [], "beauty_score": int}
    """
    if auto_detect:
        content_type = detect_content_type(content)
    else:
        content_type = content.get("type", "text_only")
    
    title = content.get("title", "")
    margin = 0.5
    
    # 根据类型选择布局
    if content_type == "timeline" and content.get("timeline"):
        shapes = add_timeline_layout(slide, title, content["timeline"], margin)
    elif content_type == "comparison" and content.get("comparison"):
        left = content["comparison"].get("left", {"title": "A", "points": []})
        right = content["comparison"].get("right", {"title": "B", "points": []})
        shapes = add_comparison_layout(slide, title, left, right, margin)
    elif content_type == "chart" and content.get("data"):
        from ppt_chart_toolkit import add_chart
        shapes = [add_chart(slide, content["data"], title=title)]
    elif content_type == "image_text" and content.get("images"):
        shapes = list(add_image_text_layout(
            slide, content["images"][0], title, 
            content.get("text", ""), "left_image", margin
        ))
    else:
        shapes = list(add_text_layout(slide, title, content.get("text", ""), margin))
    
    # 计算美观度
    beauty_score = calc_beauty_score(slide)
    
    return {
        "layout_type": content_type,
        "shapes": shapes,
        "beauty_score": beauty_score
    }
