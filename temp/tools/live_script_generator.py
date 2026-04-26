"""
live_script_generator.py - 直播脚本生成与提词器
功能: 生成直播脚本、分段提词、互动话术库
"""
from datetime import datetime

# 互动话术库
INTERACTION_TEMPLATES = {
    "welcome": [
        "欢迎{name}来到直播间！",
        "感谢{name}的关注！",
        "欢迎新朋友{name}！"
    ],
    "thanks": [
        "感谢{name}的{gift}！",
        "谢谢{name}的支持！",
        "感谢{name}送的{gift}，爱你们！"
    ],
    "question": [
        "这个问题很好，让我来解答一下",
        "关于这个问题，我的看法是",
        "很多朋友都在问这个，我详细说说"
    ],
    "guide": [
        "还没关注的朋友点个关注不迷路",
        "喜欢的话给个小心心吧",
        "评论区告诉我你的想法"
    ]
}

def generate_script_outline(topic, duration=30, sections=None):
    """生成脚本大纲"""
    if sections is None:
        sections = ["开场", "主体内容", "互动环节", "结尾"]
    
    time_per_section = duration // len(sections)
    outline = {
        "topic": topic,
        "duration": duration,
        "sections": []
    }
    
    for i, section in enumerate(sections):
        outline["sections"].append({
            "name": section,
            "start_time": i * time_per_section,
            "duration": time_per_section,
            "key_points": []
        })
    
    return outline

def generate_teleprompter(outline, detailed=False):
    """生成提词稿"""
    lines = [
        f"# 直播提词稿 - {outline['topic']}",
        f"总时长: {outline['duration']}分钟",
        ""
    ]
    
    for section in outline["sections"]:
        lines.append(f"## {section['name']} ({section['start_time']}-{section['start_time']+section['duration']}分钟)")
        
        if section["name"] == "开场":
            lines.extend([
                "- 问候观众，自我介绍",
                "- 说明本次直播主题和亮点",
                "- 引导关注点赞"
            ])
        elif section["name"] == "主体内容":
            lines.extend([
                "- 核心知识点1",
                "- 核心知识点2",
                "- 案例分享"
            ])
        elif section["name"] == "互动环节":
            lines.extend([
                "- 回答评论区问题",
                "- 抽奖/福利环节",
                "- 引导互动"
            ])
        elif section["name"] == "结尾":
            lines.extend([
                "- 总结要点",
                "- 预告下次内容",
                "- 感谢观看，引导关注"
            ])
        
        if section.get("key_points"):
            for point in section["key_points"]:
                lines.append(f"- {point}")
        
        lines.append("")
    
    return "\n".join(lines)

def get_interaction_phrase(category, **kwargs):
    """获取互动话术"""
    import random
    if category not in INTERACTION_TEMPLATES:
        return ""
    template = random.choice(INTERACTION_TEMPLATES[category])
    return template.format(**kwargs)

def create_full_script(topic, duration=30, key_points=None):
    """创建完整脚本"""
    outline = generate_script_outline(topic, duration)
    
    if key_points:
        for i, section in enumerate(outline["sections"]):
            if section["name"] == "主体内容" and key_points:
                section["key_points"] = key_points
    
    teleprompter = generate_teleprompter(outline)
    
    return {
        "outline": outline,
        "teleprompter": teleprompter,
        "interaction_lib": INTERACTION_TEMPLATES
    }

def save_script(script, output_path):
    """保存脚本"""
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(script["teleprompter"])
        f.write("\n\n---\n\n")
        f.write("# 互动话术库\n\n")
        for category, phrases in script["interaction_lib"].items():
            f.write(f"## {category}\n")
            for phrase in phrases:
                f.write(f"- {phrase}\n")
            f.write("\n")
    return output_path