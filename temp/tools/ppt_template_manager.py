"""
ppt_template_manager.py - PPT模板管理工具
支持保存/加载/应用自定义模板配置
"""
import os
import json

TEMPLATE_DIR = "./ppt_templates"

# 预定义模板
PRESET_TEMPLATES = {
    "business_blue": {
        "name": "商务蓝",
        "colors": {
            "primary": [0, 51, 102],      # 深蓝
            "secondary": [102, 102, 102],  # 灰色
            "accent": [255, 107, 53],      # 橙色
            "bg": [255, 255, 255],         # 白色
            "text": [51, 51, 51]           # 深灰
        },
        "fonts": {
            "title": {"name": "微软雅黑", "size": 32, "bold": True},
            "subtitle": {"name": "微软雅黑", "size": 24, "bold": False},
            "body": {"name": "微软雅黑", "size": 20, "bold": False},
            "note": {"name": "微软雅黑", "size": 14, "bold": False}
        },
        "bg_style": "solid"  # solid or gradient
    },
    
    "tech_gray": {
        "name": "科技灰",
        "colors": {
            "primary": [44, 62, 80],       # 深灰
            "secondary": [52, 152, 219],   # 亮蓝
            "accent": [26, 188, 156],      # 青色
            "bg": [248, 249, 250],         # 浅灰
            "text": [33, 33, 33]           # 深灰
        },
        "fonts": {
            "title": {"name": "微软雅黑", "size": 36, "bold": True},
            "subtitle": {"name": "微软雅黑", "size": 26, "bold": False},
            "body": {"name": "微软雅黑", "size": 22, "bold": False},
            "note": {"name": "微软雅黑", "size": 16, "bold": False}
        },
        "bg_style": "gradient",
        "gradient": {
            "color1": [44, 62, 80],
            "color2": [52, 73, 94],
            "style": 3,
            "variant": 1
        }
    },
    
    "education_orange": {
        "name": "教育橙",
        "colors": {
            "primary": [230, 126, 34],     # 暖橙
            "secondary": [236, 240, 241],  # 米白
            "accent": [52, 73, 94],        # 深灰
            "bg": [255, 255, 255],         # 白色
            "text": [52, 73, 94]           # 深灰
        },
        "fonts": {
            "title": {"name": "微软雅黑", "size": 34, "bold": True},
            "subtitle": {"name": "微软雅黑", "size": 24, "bold": False},
            "body": {"name": "微软雅黑", "size": 20, "bold": False},
            "note": {"name": "微软雅黑", "size": 14, "bold": False}
        },
        "bg_style": "solid"
    }
}

def init_templates():
    """初始化模板目录和预定义模板"""
    os.makedirs(TEMPLATE_DIR, exist_ok=True)
    for key, template in PRESET_TEMPLATES.items():
        path = os.path.join(TEMPLATE_DIR, f"{key}.json")
        if not os.path.exists(path):
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(template, f, ensure_ascii=False, indent=2)
    print(f"[模板管理] 已初始化 {len(PRESET_TEMPLATES)} 个预定义模板")

def save_template(template_config, name):
    """保存模板配置"""
    os.makedirs(TEMPLATE_DIR, exist_ok=True)
    path = os.path.join(TEMPLATE_DIR, f"{name}.json")
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(template_config, f, ensure_ascii=False, indent=2)
    print(f"[模板管理] 已保存模板: {name}")
    return path

def load_template(name):
    """加载模板配置"""
    path = os.path.join(TEMPLATE_DIR, f"{name}.json")
    if not os.path.exists(path):
        raise FileNotFoundError(f"模板不存在: {name}")
    with open(path, 'r', encoding='utf-8') as f:
        template = json.load(f)
    print(f"[模板管理] 已加载模板: {template.get('name', name)}")
    return template

def list_templates():
    """列出所有可用模板"""
    if not os.path.exists(TEMPLATE_DIR):
        return []
    templates = []
    for fname in os.listdir(TEMPLATE_DIR):
        if fname.endswith('.json'):
            name = fname[:-5]
            try:
                tmpl = load_template(name)
                templates.append({
                    "id": name,
                    "name": tmpl.get("name", name),
                    "path": os.path.join(TEMPLATE_DIR, fname)
                })
            except:
                pass
    return templates

def apply_bg(slide, template, toolkit):
    """应用背景样式"""
    bg_style = template.get("bg_style", "solid")
    colors = template["colors"]
    
    if bg_style == "gradient" and "gradient" in template:
        grad = template["gradient"]
        c1 = grad["color1"]
        c2 = grad["color2"]
        toolkit.set_bg_gradient(slide, c1[0], c1[1], c1[2], 
                               c2[0], c2[1], c2[2],
                               grad.get("style", 3), grad.get("variant", 1))
    else:
        bg = colors["bg"]
        toolkit.set_bg_solid(slide, bg[0], bg[1], bg[2])

def apply_title(slide, template, toolkit, text, pos=None):
    """应用标题样式"""
    fonts = template["fonts"]["title"]
    colors = template["colors"]
    
    if pos is None:
        pos = [2, 2, 20, 3]  # 默认位置
    
    return toolkit.add_text(
        slide, text, pos[0], pos[1], pos[2], pos[3],
        sz=fonts["size"], bold=fonts["bold"],
        color=tuple(colors["primary"]),
        align="center", font=fonts["name"]
    )

def apply_body(slide, template, toolkit, text, pos=None):
    """应用正文样式"""
    fonts = template["fonts"]["body"]
    colors = template["colors"]
    
    if pos is None:
        pos = [2, 6, 20, 10]  # 默认位置
    
    return toolkit.add_text(
        slide, text, pos[0], pos[1], pos[2], pos[3],
        sz=fonts["size"], bold=fonts["bold"],
        color=tuple(colors["text"]),
        align="left", font=fonts["name"]
    )

def create_title_slide(slide, template, toolkit, title, subtitle=""):
    """创建标题页"""
    apply_bg(slide, template, toolkit)
    
    # 主标题
    fonts_title = template["fonts"]["title"]
    colors = template["colors"]
    toolkit.add_text(
        slide, title, 2, 6, 20, 4,
        sz=fonts_title["size"] + 8, bold=True,
        color=tuple(colors["primary"]),
        align="center", font=fonts_title["name"]
    )
    
    # 副标题
    if subtitle:
        fonts_sub = template["fonts"]["subtitle"]
        toolkit.add_text(
            slide, subtitle, 2, 11, 20, 2,
            sz=fonts_sub["size"], bold=False,
            color=tuple(colors["secondary"]),
            align="center", font=fonts_sub["name"]
        )

def create_content_slide(slide, template, toolkit, title, content):
    """创建内容页"""
    apply_bg(slide, template, toolkit)
    apply_title(slide, template, toolkit, title, [2, 1, 20, 2])
    apply_body(slide, template, toolkit, content, [2, 4, 20, 12])

def get_market_manager():
    """获取模板市场管理器"""
    import sys
    import os
    parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if parent_dir not in sys.path:
        sys.path.insert(0, parent_dir)
    from ppt_file_manager import PPTFileManager
    return PPTFileManager()

def search_market_templates(category=None, keyword=None, tags=None):
    """从模板市场搜索模板"""
    manager = get_market_manager()
    return manager.search_templates(category=category, keyword=keyword, tags=tags)

def export_market_template(template_id, output_path):
    """从模板市场导出模板"""
    manager = get_market_manager()
    return manager.export_template(template_id, output_path)

if __name__ == "__main__":
    # 初始化预定义模板
    init_templates()
    
    # 列出所有模板
    print("\n可用模板:")
    for tmpl in list_templates():
        print(f"  - {tmpl['id']}: {tmpl['name']}")
