"""
PPT模板文件管理工具
管理已下载的PPTX文件，支持分类、预览、搜索
"""
import os
import json
import shutil
from pathlib import Path

class PPTFileManager:
    def __init__(self, base_dir="./ppt_templates"):
        self.base_dir = base_dir
        self.files_dir = os.path.join(base_dir, "files")
        self.metadata_file = os.path.join(base_dir, "metadata.json")
        self.categories_dir = os.path.join(base_dir, "categories")
        
        os.makedirs(self.files_dir, exist_ok=True)
        os.makedirs(self.categories_dir, exist_ok=True)
        
        self.metadata = self._load_metadata()
    
    def _load_metadata(self):
        """加载元数据"""
        if os.path.exists(self.metadata_file):
            with open(self.metadata_file, "r", encoding="utf-8") as f:
                return json.load(f)
        return {"templates": {}, "categories": {}}
    
    def _save_metadata(self):
        """保存元数据"""
        with open(self.metadata_file, "w", encoding="utf-8") as f:
            json.dump(self.metadata, f, ensure_ascii=False, indent=2)
    
    def scan_templates(self):
        """扫描并索引所有模板文件"""
        files = [f for f in os.listdir(self.files_dir) if f.endswith(".pptx")]
        
        for filename in files:
            file_path = os.path.join(self.files_dir, filename)
            file_id = filename.replace(".pptx", "")
            
            if file_id not in self.metadata["templates"]:
                size = os.path.getsize(file_path) / (1024 * 1024)
                self.metadata["templates"][file_id] = {
                    "filename": filename,
                    "path": file_path,
                    "size_mb": round(size, 2),
                    "category": "未分类",
                    "tags": [],
                    "description": ""
                }
        
        self._save_metadata()
        return len(files)
    
    def categorize_template(self, file_id, category):
        """为模板分类"""
        if file_id in self.metadata["templates"]:
            self.metadata["templates"][file_id]["category"] = category
            
            if category not in self.metadata["categories"]:
                self.metadata["categories"][category] = []
            
            if file_id not in self.metadata["categories"][category]:
                self.metadata["categories"][category].append(file_id)
            
            self._save_metadata()
            return True
        return False
    
    def add_tags(self, file_id, tags):
        """添加标签"""
        if file_id in self.metadata["templates"]:
            current_tags = self.metadata["templates"][file_id].get("tags", [])
            for tag in tags:
                if tag not in current_tags:
                    current_tags.append(tag)
            self.metadata["templates"][file_id]["tags"] = current_tags
            self._save_metadata()
            return True
        return False
    
    def search_templates(self, keyword=None, category=None, tags=None):
        """搜索模板"""
        results = []
        
        for file_id, info in self.metadata["templates"].items():
            match = True
            
            if category and info.get("category") != category:
                match = False
            
            if tags:
                template_tags = info.get("tags", [])
                if not any(tag in template_tags for tag in tags):
                    match = False
            
            if keyword:
                desc = info.get("description", "")
                tags_str = " ".join(info.get("tags", []))
                searchable = f"{file_id} {desc} {tags_str}"
                if keyword.lower() not in searchable.lower():
                    match = False
            
            if match:
                results.append({**info, "id": file_id})
        
        return results
    
    def get_statistics(self):
        """获取统计信息"""
        total = len(self.metadata["templates"])
        total_size = sum(t.get("size_mb", 0) for t in self.metadata["templates"].values())
        
        categories = {}
        for info in self.metadata["templates"].values():
            cat = info.get("category", "未分类")
            categories[cat] = categories.get(cat, 0) + 1
        
        return {
            "total_templates": total,
            "total_size_mb": round(total_size, 2),
            "categories": categories
        }
    
    def list_by_category(self, category):
        """按分类列出模板"""
        return self.search_templates(category=category)
    
    def export_template(self, file_id, dest_path):
        """导出模板到指定位置"""
        if file_id in self.metadata["templates"]:
            src = self.metadata["templates"][file_id]["path"]
            shutil.copy2(src, dest_path)
            return True
        return False

if __name__ == "__main__":
    manager = PPTFileManager()
    count = manager.scan_templates()
    print(f"已扫描 {count} 个模板")
    
    stats = manager.get_statistics()
    print("\n统计信息:")
    print(f"  总数: {stats['total_templates']}")
    print(f"  总大小: {stats['total_size_mb']} MB")
    print(f"  分类: {stats['categories']}")