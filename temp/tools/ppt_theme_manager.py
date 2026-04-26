#!/usr/bin/env python3
"""
ppt_theme_manager.py - PPT主题模板管理工具

功能:
1. 加载主题配置
2. 列出可用主题
3. 获取主题详情
4. 应用主题到PPT配置
"""
import json
import os
from typing import Dict, List, Optional

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
THEMES_FILE = os.path.join(SCRIPT_DIR, "ppt_themes.json")

class ThemeManager:
    def __init__(self):
        self.themes = self._load_themes()
    
    def _load_themes(self) -> Dict:
        """加载主题配置文件"""
        if not os.path.exists(THEMES_FILE):
            raise FileNotFoundError(f"主题配置文件不存在: {THEMES_FILE}")
        
        with open(THEMES_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    
    def list_themes(self) -> List[Dict]:
        """列出所有可用主题"""
        result = []
        for theme_id, theme in self.themes.items():
            result.append({
                "id": theme_id,
                "name": theme["name"],
                "description": theme["description"]
            })
        return result
    
    def get_theme(self, theme_id: str) -> Optional[Dict]:
        """获取指定主题配置"""
        return self.themes.get(theme_id)
    
    def apply_theme(self, config: Dict, theme_id: str = "academic_blue") -> Dict:
        """将主题应用到PPT配置"""
        theme = self.get_theme(theme_id)
        if not theme:
            print(f"警告: 主题 {theme_id} 不存在，使用默认主题")
            theme = self.get_theme("academic_blue")        
        # 应用主题配色和图标
        config["theme"] = theme_id
        config["colors"] = theme["colors"]
        
        # 更新所有幻灯片的图标风格
        for slide in config.get("slides", []):
            if slide.get("type") == "icon_cards":
                # 替换图标为主题图标
                cards = slide.get("cards", [])
                for i, card in enumerate(cards):
                    card["icon"] = theme["icons"][i % len(theme["icons"])]
        
        return config

def main():
    """命令行工具：列出主题"""
    import sys
    
    manager = ThemeManager()
    
    if len(sys.argv) > 1 and sys.argv[1] == "list":
        print("\n可用主题列表:\n")
        for theme in manager.list_themes():
            theme_id = theme["id"]
            theme_name = theme["name"]
            theme_desc = theme["description"]
            print(f"  [{theme_id}] {theme_name}")
            print(f"      {theme_desc}")
    else:
        print("用法: python ppt_theme_manager.py list")

if __name__ == "__main__":
    main()