"""
platform_adapter.py — 多平台内容适配工具（R160, 2026-04-20）

功能：
1. 支持微信公众号/知乎/小红书格式转换
2. 自动调整图片尺寸和排版
3. 基于markdown解析和平台规则引擎

依赖: pip install markdown pillow
"""

import re
from pathlib import Path
from PIL import Image
import markdown

# 平台规则配置
PLATFORM_RULES = {
    "wechat": {
        "max_image_width": 1080,
        "max_image_height": 2000,
        "title_max_length": 64,
        "summary_max_length": 120,
        "paragraph_spacing": "1.5em",
        "font_size": "16px",
        "support_html": True,
        "emoji_support": True
    },
    "zhihu": {
        "max_image_width": 1200,
        "max_image_height": 3000,
        "title_max_length": 100,
        "paragraph_spacing": "1.2em",
        "support_markdown": True,
        "support_latex": True
    },
    "xiaohongshu": {
        "max_image_width": 1242,
        "max_image_height": 1660,
        "title_max_length": 20,
        "content_max_length": 1000,
        "hashtag_required": True,
        "emoji_recommended": True,
        "image_ratio": "3:4"
    }
}


def resize_image(image_path, max_width, max_height, output_path=None):
    """
    调整图片尺寸
    
    Args:
        image_path: 输入图片路径
        max_width: 最大宽度
        max_height: 最大高度
        output_path: 输出路径（None则覆盖原文件）
    
    Returns:
        输出路径
    """
    img = Image.open(image_path)
    w, h = img.size
    
    # 计算缩放比例
    ratio = min(max_width / w, max_height / h, 1.0)
    
    if ratio < 1.0:
        new_w = int(w * ratio)
        new_h = int(h * ratio)
        img = img.resize((new_w, new_h), Image.Resampling.LANCZOS)
    
    output = output_path or image_path
    img.save(output, quality=95)
    return output


def adapt_content(content, platform, title="", images=None):
    """
    适配内容到指定平台
    
    Args:
        content: 原始内容（markdown格式）
        platform: 目标平台（wechat/zhihu/xiaohongshu）
        title: 标题
        images: 图片路径列表
    
    Returns:
        {
            "title": 适配后的标题,
            "content": 适配后的内容,
            "images": 处理后的图片路径列表,
            "metadata": 平台特定元数据
        }
    """
    if platform not in PLATFORM_RULES:
        raise ValueError(f"不支持的平台: {platform}")
    
    rules = PLATFORM_RULES[platform]
    result = {"metadata": {}}
    
    # 适配标题
    if title:
        max_len = rules.get("title_max_length", 100)
        result["title"] = title[:max_len]
    
    # 适配内容
    adapted_content = content
    
    if platform == "wechat":
        adapted_content = _adapt_wechat(content, rules)
    elif platform == "zhihu":
        adapted_content = _adapt_zhihu(content, rules)
    elif platform == "xiaohongshu":
        adapted_content = _adapt_xiaohongshu(content, rules)
    
    result["content"] = adapted_content
    
    # 处理图片
    if images:
        processed_images = []
        for img_path in images:
            output_path = f"{Path(img_path).stem}_{platform}{Path(img_path).suffix}"
            resized = resize_image(
                img_path,
                rules["max_image_width"],
                rules["max_image_height"],
                output_path
            )
            processed_images.append(resized)
        result["images"] = processed_images
    
    return result


def _adapt_wechat(content, rules):
    """适配微信公众号格式"""
    # 转换为HTML
    html = markdown.markdown(content)
    
    # 添加样式
    styled_html = f'<div style="font-size: {rules["font_size"]}; line-height: {rules["paragraph_spacing"]};">'
    styled_html += html
    styled_html += "</div>"
    
    return styled_html


def _adapt_zhihu(content, rules):
    """适配知乎格式"""
    # 知乎支持markdown，保持原格式
    # 调整段落间距
    adapted = re.sub(r'\n\n+', '\n\n', content)
    return adapted


def _adapt_xiaohongshu(content, rules):
    """适配小红书格式"""
    # 限制长度
    max_len = rules.get("content_max_length", 1000)
    adapted = content[:max_len]
    
    # 添加emoji和话题标签建议
    if rules.get("hashtag_required"):
        adapted += "\n\n💡 建议添加话题标签：#内容创作 #干货分享"
    
    return adapted


def batch_adapt(content, platforms, title="", images=None):
    """
    批量适配到多个平台
    
    Args:
        content: 原始内容
        platforms: 平台列表
        title: 标题
        images: 图片列表
    
    Returns:
        {platform: adapted_result}
    """
    results = {}
    for platform in platforms:
        results[platform] = adapt_content(content, platform, title, images)
    return results


# 便捷常量
PLATFORM_WECHAT = "wechat"
PLATFORM_ZHIHU = "zhihu"
PLATFORM_XIAOHONGSHU = "xiaohongshu"
