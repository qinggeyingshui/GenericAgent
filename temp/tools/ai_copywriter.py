"""
ai_copywriter.py — AI文案生成助手（R161, 2026-04-20）

功能：
1. 支持3种文案类型：标题/正文/摘要
2. 基于模板和规则引擎
3. 支持多种风格：专业/轻松/营销

依赖: 无外部依赖
"""

import random
import re

# 文案模板库
TITLE_TEMPLATES = {
    "professional": [
        "{主题}：{核心观点}",
        "深度解析：{主题}的{数量}个关键点",
        "{主题}完全指南：从入门到精通",
        "如何{动作}：{主题}实战经验分享"
    ],
    "casual": [
        "{主题}？这{数量}个技巧你一定要知道！",
        "太实用了！{主题}的{数量}个小窍门",
        "{主题}原来这么简单！{核心观点}",
        "涨知识了！关于{主题}的{数量}个真相"
    ],
    "marketing": [
        "限时！{主题}{优惠}",
        "{数量}个理由让你选择{主题}",
        "不看后悔！{主题}的{核心观点}",
        "{主题}：{数量}天见效，{优惠}"
    ]
}

SUMMARY_TEMPLATES = {
    "professional": "本文深入探讨了{主题}，分析了{要点1}、{要点2}和{要点3}，为读者提供了系统的理解框架。",
    "casual": "这篇文章讲了{主题}，重点是{要点1}、{要点2}和{要点3}，超级实用！",
    "marketing": "想了解{主题}？本文揭秘{要点1}、{要点2}和{要点3}，助你快速掌握！"
}

CONTENT_TEMPLATES = {
    "professional": """{开头}

## 核心观点

{观点1}

{观点2}

{观点3}

## 总结

{总结}""",
    "casual": """{开头}

💡 {观点1}

💡 {观点2}

💡 {观点3}

{总结}""",
    "marketing": """{开头}

✅ {观点1}

✅ {观点2}

✅ {观点3}

🎁 {总结}"""
}

# 文案规则库
COPYWRITING_RULES = {
    "title": {
        "max_length": 30,
        "keywords_position": "front",  # 关键词位置
        "use_numbers": True,  # 使用数字
        "use_punctuation": ["！", "？", "："]  # 标点符号
    },
    "summary": {
        "max_length": 120,
        "include_keywords": True,
        "structure": "总-分-总"
    },
    "content": {
        "min_length": 300,
        "paragraph_count": 3,
        "use_subheadings": True
    }
}


def generate_title(topic, style="professional", **kwargs):
    """
    生成标题
    
    Args:
        topic: 主题
        style: 风格（professional/casual/marketing）
        **kwargs: 模板变量（核心观点/数量/动作/优惠等）
    
    Returns:
        生成的标题
    """
    if style not in TITLE_TEMPLATES:
        style = "professional"
    
    templates = TITLE_TEMPLATES[style]
    template = random.choice(templates)
    
    # 填充默认值
    params = {"主题": topic, "数量": "3", "核心观点": "实用技巧", "动作": "提升效率", "优惠": "限时优惠"}
    params.update(kwargs)
    
    # 替换模板变量
    title = template
    for key, value in params.items():
        title = title.replace(f"{{{key}}}", str(value))
    
    # 应用规则
    max_len = COPYWRITING_RULES["title"]["max_length"]
    if len(title) > max_len:
        title = title[:max_len-1] + "..."
    
    return title


def generate_summary(topic, style="professional", key_points=None):
    """
    生成摘要
    
    Args:
        topic: 主题
        style: 风格
        key_points: 要点列表
    
    Returns:
        生成的摘要
    """
    if style not in SUMMARY_TEMPLATES:
        style = "professional"
    
    template = SUMMARY_TEMPLATES[style]
    
    # 填充要点
    if not key_points:
        key_points = ["核心方法", "实践技巧", "注意事项"]
    
    params = {
        "主题": topic,
        "要点1": key_points[0] if len(key_points) > 0 else "要点1",
        "要点2": key_points[1] if len(key_points) > 1 else "要点2",
        "要点3": key_points[2] if len(key_points) > 2 else "要点3"
    }
    
    summary = template
    for key, value in params.items():
        summary = summary.replace(f"{{{key}}}", str(value))
    
    # 应用规则
    max_len = COPYWRITING_RULES["summary"]["max_length"]
    if len(summary) > max_len:
        summary = summary[:max_len-1] + "..."
    
    return summary


def generate_content(topic, style="professional", points=None, opening=None, closing=None):
    """
    生成正文
    
    Args:
        topic: 主题
        style: 风格
        points: 观点列表
        opening: 开头
        closing: 结尾
    
    Returns:
        生成的正文
    """
    if style not in CONTENT_TEMPLATES:
        style = "professional"
    
    template = CONTENT_TEMPLATES[style]
    
    # 填充默认值
    if not points:
        points = [
            f"关于{topic}的第一个要点，这是核心内容。",
            f"关于{topic}的第二个要点，这是关键方法。",
            f"关于{topic}的第三个要点，这是实践建议。"
        ]
    
    if not opening:
        opening = f"在当今时代，{topic}变得越来越重要。本文将为你详细介绍相关内容。"
    
    if not closing:
        closing = f"以上就是关于{topic}的全部内容，希望对你有所帮助。"
    
    params = {
        "开头": opening,
        "观点1": points[0] if len(points) > 0 else "观点1",
        "观点2": points[1] if len(points) > 1 else "观点2",
        "观点3": points[2] if len(points) > 2 else "观点3",
        "总结": closing
    }
    
    content = template
    for key, value in params.items():
        content = content.replace(f"{{{key}}}", str(value))
    
    return content


def generate_full_copy(topic, style="professional", **kwargs):
    """
    生成完整文案（标题+摘要+正文）
    
    Args:
        topic: 主题
        style: 风格
        **kwargs: 其他参数
    
    Returns:
        {
            "title": 标题,
            "summary": 摘要,
            "content": 正文
        }
    """
    return {
        "title": generate_title(topic, style, **kwargs),
        "summary": generate_summary(topic, style, kwargs.get("key_points")),
        "content": generate_content(topic, style, kwargs.get("points"), kwargs.get("opening"), kwargs.get("closing"))
    }


# 便捷常量
STYLE_PROFESSIONAL = "professional"
STYLE_CASUAL = "casual"
STYLE_MARKETING = "marketing"
