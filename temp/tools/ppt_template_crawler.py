"""
PPT模板爬虫工具
从pptsupermarket.com批量下载PPT模板
"""
import os
import json
import time
from urllib.parse import urlparse

class PPTTemplateCrawler:
    def __init__(self, save_dir="./ppt_templates"):
        self.save_dir = save_dir
        self.data_file = os.path.join(save_dir, "templates_data.json")
        os.makedirs(save_dir, exist_ok=True)
        self.templates = []
        
    def save_template_info(self, template_data):
        """保存模板信息到JSON"""
        self.templates.append(template_data)
        with open(self.data_file, "w", encoding="utf-8") as f:
            json.dump({"count": len(self.templates), "templates": self.templates}, f, ensure_ascii=False, indent=2)
        
    def get_download_url(self, detail_url):
        """从详情页URL提取下载链接（需要浏览器JS支持）"""
        # 这个方法需要配合web_execute_js使用
        return None
        
    def categorize_template(self, title, tags=[]):
        """根据标题和标签自动分类"""
        categories = {
            "工作总结": ["总结", "汇报", "述职"],
            "商业计划": ["商业", "计划书", "融资", "创业"],
            "教育培训": ["教学", "说课", "培训", "课件"],
            "答辩演示": ["答辩", "毕业", "论文"],
            "节日庆典": ["节日", "庆典", "活动"],
        }
        
        for category, keywords in categories.items():
            for keyword in keywords:
                if keyword in title or keyword in str(tags):
                    return category
        return "其他"

if __name__ == "__main__":
    crawler = PPTTemplateCrawler()
    print("PPT模板爬虫工具已初始化")