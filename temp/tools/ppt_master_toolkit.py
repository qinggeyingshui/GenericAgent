#!/usr/bin/env python3
"""
ppt_master_toolkit.py - PPT母版与主题深度管理工具

功能:
1. 母版编辑 - 直接操作PPT母版（添加元素、修改背景、设置字体）
2. 主题色提取 - 从现有PPT提取主题色方案
3. 批量应用 - 将母版/主题批量应用到多个PPT

依赖: win32com (pywin32)
"""
import os
import json
from typing import Dict, List, Tuple, Optional
import win32com.client as win32
from win32com.client import constants as c

# ============ 辅助函数 ============

def _ensure_app():
    """获取或创建PowerPoint应用实例"""
    try:
        app = win32.GetActiveObject("PowerPoint.Application")
    except:
        app = win32.Dispatch("PowerPoint.Application")
    app.Visible = True
    return app

def _rgb_to_int(r: int, g: int, b: int) -> int:
    """RGB转win32 color int"""
    return r + (g << 8) + (b << 16)

def _int_to_rgb(color_int: int) -> Tuple[int, int, int]:
    """win32 color int转RGB"""
    r = color_int & 0xFF
    g = (color_int >> 8) & 0xFF
    b = (color_int >> 16) & 0xFF
    return (r, g, b)

# ============ 母版编辑函数 ============

def get_master(prs, index: int = 1):
    """
    获取母版对象
    
    Args:
        prs: Presentation对象
        index: 母版索引（从1开始，默认1）
    
    Returns:
        SlideMaster对象
    """
    # 新建PPT可能没有SlideMasters集合，需先添加幻灯片
    if prs.Slides.Count == 0:
        prs.Slides.Add(1, 12)  # ppLayoutBlank，触发母版创建
    return prs.SlideMaster if index == 1 else prs.Designs(index).SlideMaster

def get_layouts(prs, master_index: int = 1) -> List[Dict]:
    """
    获取母版下所有版式信息
    
    Args:
        prs: Presentation对象
        master_index: 母版索引
    
    Returns:
        版式列表 [{"index": 1, "name": "标题幻灯片"}, ...]
    """
    master = get_master(prs, master_index)
    layouts = []
    for i in range(1, master.CustomLayouts.Count + 1):
        layout = master.CustomLayouts(i)
        layouts.append({
            "index": i,
            "name": layout.Name
        })
    return layouts

def set_master_background(prs, r: int, g: int, b: int, master_index: int = 1):
    """
    设置母版背景色（纯色）
    
    Args:
        prs: Presentation对象
        r, g, b: RGB颜色值
        master_index: 母版索引
    """
    master = get_master(prs, master_index)
    master.Background.Fill.Solid()
    master.Background.Fill.ForeColor.RGB = _rgb_to_int(r, g, b)

def set_master_gradient(prs, r1: int, g1: int, b1: int, 
                        r2: int, g2: int, b2: int,
                        master_index: int = 1):
    """
    设置母版渐变背景
    
    Args:
        prs: Presentation对象
        r1,g1,b1: 起始颜色RGB
        r2,g2,b2: 结束颜色RGB
        master_index: 母版索引
    """
    master = get_master(prs, master_index)
    fill = master.Background.Fill
    fill.TwoColorGradient(1, 1)  # msoGradientHorizontal, variant 1
    fill.GradientStops(1).Color.RGB = _rgb_to_int(r1, g1, b1)
    fill.GradientStops(2).Color.RGB = _rgb_to_int(r2, g2, b2)

def add_master_logo(prs, image_path: str, left: float = 20, top: float = 20,
                    width: float = 80, height: float = -1, master_index: int = 1):
    """
    在母版添加LOGO图片（所有幻灯片自动显示）
    
    Args:
        prs: Presentation对象
        image_path: 图片绝对路径
        left, top: 位置（pt）
        width: 宽度（pt），height=-1时自动按比例
        height: 高度（pt），-1表示自动
        master_index: 母版索引
    
    Returns:
        Shape对象
    """
    master = get_master(prs, master_index)
    if height == -1:
        # 先添加，再调整
        shape = master.Shapes.AddPicture(
            FileName=os.path.abspath(image_path),
            LinkToFile=False,
            SaveWithDocument=True,
            Left=left, Top=top, Width=width, Height=width
        )
        # 保持比例
        shape.LockAspectRatio = True
        shape.Width = width
    else:
        shape = master.Shapes.AddPicture(
            FileName=os.path.abspath(image_path),
            LinkToFile=False,
            SaveWithDocument=True,
            Left=left, Top=top, Width=width, Height=height
        )
    return shape

def add_master_text(prs, text: str, left: float, top: float, 
                    width: float, height: float,
                    font_size: int = 12, font_color: Tuple[int,int,int] = (128,128,128),
                    font_name: str = "微软雅黑", master_index: int = 1):
    """
    在母版添加固定文本（如版权信息、页脚）
    
    Args:
        prs: Presentation对象
        text: 文本内容
        left, top, width, height: 位置和尺寸（pt）
        font_size: 字号
        font_color: RGB颜色
        font_name: 字体名
        master_index: 母版索引
    
    Returns:
        Shape对象
    """
    master = get_master(prs, master_index)
    shape = master.Shapes.AddTextbox(1, left, top, width, height)  # 1=msoTextOrientationHorizontal
    tf = shape.TextFrame
    tf.TextRange.Text = text
    tf.TextRange.Font.Size = font_size
    tf.TextRange.Font.Color.RGB = _rgb_to_int(*font_color)
    tf.TextRange.Font.Name = font_name
    return shape

# ============ 主题色提取函数 ============

def extract_theme_colors(prs) -> Dict:
    """
    从PPT提取主题色方案
    
    Args:
        prs: Presentation对象
    
    Returns:
        {
            "background": (r,g,b),
            "text": (r,g,b),
            "accent1": (r,g,b),
            ...
            "accent6": (r,g,b)
        }
    """
    master = get_master(prs, 1)
    scheme = master.Theme.ThemeColorScheme
    
    # 主题色索引映射
    color_map = {
        "background1": 1,   # msoThemeColorBackground1
        "text1": 2,         # msoThemeColorText1
        "background2": 3,   # msoThemeColorBackground2
        "text2": 4,         # msoThemeColorText2
        "accent1": 5,       # msoThemeColorAccent1
        "accent2": 6,
        "accent3": 7,
        "accent4": 8,
        "accent5": 9,
        "accent6": 10,
        "hyperlink": 11,
        "followed_hyperlink": 12
    }
    
    result = {}
    for name, idx in color_map.items():
        try:
            color_int = scheme.Colors(idx).RGB
            result[name] = _int_to_rgb(color_int)
        except:
            result[name] = (0, 0, 0)
    
    return result

def extract_slide_colors(prs, slide_index: int = 1) -> Dict:
    """
    从指定幻灯片提取使用的颜色
    
    Args:
        prs: Presentation对象
        slide_index: 幻灯片索引（从1开始）
    
    Returns:
        {"background": (r,g,b), "shapes": [(r,g,b), ...], "texts": [(r,g,b), ...]}
    """
    slide = prs.Slides(slide_index)
    result = {
        "background": None,
        "shapes": [],
        "texts": []
    }
    
    # 背景色
    try:
        bg_fill = slide.Background.Fill
        if bg_fill.Type == 1:  # msoFillSolid
            result["background"] = _int_to_rgb(bg_fill.ForeColor.RGB)
    except:
        pass
    
    # 形状和文本颜色
    for shape in slide.Shapes:
        try:
            if shape.HasFill:
                fill = shape.Fill
                if fill.Type == 1:  # msoFillSolid
                    color = _int_to_rgb(fill.ForeColor.RGB)
                    if color not in result["shapes"]:
                        result["shapes"].append(color)
        except:
            pass
        
        try:
            if shape.HasTextFrame:
                tf = shape.TextFrame
                if tf.HasText:
                    color = _int_to_rgb(tf.TextRange.Font.Color.RGB)
                    if color not in result["texts"]:
                        result["texts"].append(color)
        except:
            pass
    
    return result

def save_theme_to_json(theme_colors: Dict, output_path: str, 
                       theme_name: str = "extracted_theme"):
    """
    将提取的主题色保存为JSON
    
    Args:
        theme_colors: extract_theme_colors返回的字典
        output_path: 输出JSON路径
        theme_name: 主题名称
    """
    data = {
        "name": theme_name,
        "colors": theme_colors
    }
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    return output_path

# ============ 批量应用函数 ============

def apply_theme_to_master(prs, theme_colors: Dict, master_index: int = 1):
    """
    将主题色应用到母版
    
    Args:
        prs: Presentation对象
        theme_colors: 主题色字典（来自extract_theme_colors或JSON）
        master_index: 母版索引
    """
    master = get_master(prs, master_index)
    scheme = master.Theme.ThemeColorScheme
    
    color_map = {
        "background1": 1, "text1": 2, "background2": 3, "text2": 4,
        "accent1": 5, "accent2": 6, "accent3": 7, "accent4": 8,
        "accent5": 9, "accent6": 10, "hyperlink": 11, "followed_hyperlink": 12
    }
    
    for name, idx in color_map.items():
        if name in theme_colors:
            rgb = theme_colors[name]
            if isinstance(rgb, (list, tuple)) and len(rgb) == 3:
                try:
                    scheme.Colors(idx).RGB = _rgb_to_int(*rgb)
                except:
                    pass

def batch_apply_master(source_ppt: str, target_ppts: List[str], 
                       output_dir: str = None) -> List[str]:
    """
    将源PPT的母版批量应用到多个目标PPT
    
    Args:
        source_ppt: 源PPT路径（提供母版）
        target_ppts: 目标PPT路径列表
        output_dir: 输出目录（None则覆盖原文件）
    
    Returns:
        处理后的文件路径列表
    """
    app = _ensure_app()
    
    # 打开源PPT提取主题
    src_prs = app.Presentations.Open(os.path.abspath(source_ppt))
    theme_colors = extract_theme_colors(src_prs)
    src_prs.Close()
    
    results = []
    for target in target_ppts:
        try:
            prs = app.Presentations.Open(os.path.abspath(target))
            apply_theme_to_master(prs, theme_colors)
            
            if output_dir:
                os.makedirs(output_dir, exist_ok=True)
                out_path = os.path.join(output_dir, os.path.basename(target))
            else:
                out_path = target
            
            prs.SaveAs(os.path.abspath(out_path))
            prs.Close()
            results.append(out_path)
        except Exception as e:
            print(f"处理失败 {target}: {e}")
    
    return results

def copy_master_elements(source_ppt: str, target_ppt: str, 
                         elements: List[str] = ["logo", "footer"]):
    """
    从源PPT复制母版元素到目标PPT
    
    Args:
        source_ppt: 源PPT路径
        target_ppt: 目标PPT路径
        elements: 要复制的元素类型 ["logo", "footer", "background"]
    
    Note:
        由于win32com限制，此函数主要复制背景和主题色
        LOGO等图片元素需要手动指定路径重新添加
    """
    app = _ensure_app()
    
    src_prs = app.Presentations.Open(os.path.abspath(source_ppt))
    tgt_prs = app.Presentations.Open(os.path.abspath(target_ppt))
    
    src_master = get_master(src_prs, 1)
    tgt_master = get_master(tgt_prs, 1)
    
    if "background" in elements:
        # 复制背景
        try:
            src_fill = src_master.Background.Fill
            tgt_fill = tgt_master.Background.Fill
            if src_fill.Type == 1:  # Solid
                tgt_fill.Solid()
                tgt_fill.ForeColor.RGB = src_fill.ForeColor.RGB
        except:
            pass
    
    if "theme" in elements or "logo" in elements or "footer" in elements:
        # 复制主题色
        theme_colors = extract_theme_colors(src_prs)
        apply_theme_to_master(tgt_prs, theme_colors)
    
    tgt_prs.Save()
    src_prs.Close()
    tgt_prs.Close()

# ============ 演示函数 ============

def demo_master_toolkit(output_path: str = "./demo_master.pptx"):
    """
    演示母版工具功能
    
    Args:
        output_path: 输出PPT路径
    
    Returns:
        输出文件路径
    """
    app = _ensure_app()
    prs = app.Presentations.Add()
    
    # 1. 设置母版背景
    set_master_background(prs, 240, 248, 255)  # AliceBlue
    
    # 2. 添加页脚文本
    add_master_text(prs, "© 2026 Demo Presentation", 
                    left=50, top=510, width=300, height=30,
                    font_size=10, font_color=(128, 128, 128))
    
    # 3. 提取主题色
    theme = extract_theme_colors(prs)
    print("提取的主题色:")
    for k, v in list(theme.items())[:6]:
        print(f"  {k}: RGB{v}")
    
    # 4. 添加测试幻灯片
    slide = prs.Slides.Add(1, 12)  # ppLayoutBlank
    slide.Shapes.AddTextbox(1, 100, 200, 500, 100).TextFrame.TextRange.Text = "母版工具演示"
    
    # 5. 获取版式信息
    layouts = get_layouts(prs)
    print(f"\n母版版式数量: {len(layouts)}")
    
    # 保存
    abs_path = os.path.abspath(output_path)
    prs.SaveAs(abs_path)
    prs.Close()
    
    print(f"\n演示PPT已保存: {abs_path}")
    return abs_path


if __name__ == "__main__":
    demo_master_toolkit()
