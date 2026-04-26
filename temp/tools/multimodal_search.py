"""
multimodal_search.py - 知识库多模态检索
功能: 图片/表格/公式检索，支持OCR和向量化
"""
import os
import json
import re
from pathlib import Path

# 支持的图片格式
IMAGE_EXTS = [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg"]

# 支持的表格格式
TABLE_EXTS = [".csv", ".xlsx", ".xls"]


def search_images(kb_dir, keyword=None, tags=None):
    """搜索图片文件"""
    results = []
    
    for root, dirs, files in os.walk(kb_dir):
        for file in files:
            ext = Path(file).suffix.lower()
            if ext in IMAGE_EXTS:
                file_path = os.path.join(root, file)
                
                # 关键词匹配
                if keyword and keyword.lower() not in file.lower():
                    continue
                
                # 标签匹配（从文件名提取）
                if tags:
                    file_tags = extract_tags_from_filename(file)
                    if not any(tag in file_tags for tag in tags):
                        continue
                
                results.append({
                    "path": file_path,
                    "name": file,
                    "type": "image",
                    "ext": ext
                })
    
    return results


def search_tables(kb_dir, keyword=None):
    """搜索表格文件"""
    results = []
    
    for root, dirs, files in os.walk(kb_dir):
        for file in files:
            ext = Path(file).suffix.lower()
            if ext in TABLE_EXTS:
                file_path = os.path.join(root, file)
                
                if keyword and keyword.lower() not in file.lower():
                    continue
                
                results.append({
                    "path": file_path,
                    "name": file,
                    "type": "table",
                    "ext": ext
                })
    
    return results


def search_formulas(kb_dir, keyword=None):
    """搜索公式（LaTeX/Markdown文件中）"""
    results = []
    
    for root, dirs, files in os.walk(kb_dir):
        for file in files:
            if file.endswith((".md", ".tex", ".txt")):
                file_path = os.path.join(root, file)
                
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read()
                    
                    # 提取LaTeX公式
                    formulas = extract_latex_formulas(content)
                    
                    if keyword:
                        formulas = [f for f in formulas if keyword in f]
                    
                    if formulas:
                        results.append({
                            "path": file_path,
                            "name": file,
                            "type": "formula",
                            "formulas": formulas[:5]  # 最多返回5个
                        })
                except:
                    pass
    
    return results


def extract_latex_formulas(text):
    """提取LaTeX公式"""
    # 匹配 $...$ 和 $$...$$ 格式
    patterns = [
        r"\$\$(.+?)\$\$",  # 块级公式
        r"\$(.+?)\$"       # 行内公式
    ]
    
    formulas = []
    for pattern in patterns:
        matches = re.findall(pattern, text, re.DOTALL)
        formulas.extend(matches)
    
    return formulas


def extract_tags_from_filename(filename):
    """从文件名提取标签"""
    # 简单实现：按下划线或连字符分割
    name = Path(filename).stem
    tags = re.split(r"[_\-\s]+", name.lower())
    return tags


def multimodal_search(kb_dir, query, search_types=["image", "table", "formula"]):
    """多模态综合搜索"""
    results = {
        "query": query,
        "images": [],
        "tables": [],
        "formulas": []
    }
    
    if "image" in search_types:
        results["images"] = search_images(kb_dir, keyword=query)
    
    if "table" in search_types:
        results["tables"] = search_tables(kb_dir, keyword=query)
    
    if "formula" in search_types:
        results["formulas"] = search_formulas(kb_dir, keyword=query)
    
    return results


def extract_text_from_image(image_path):
    """OCR文字提取（预留接口）"""
    # 需要 pytesseract 库
    # try:
    #     import pytesseract
    #     from PIL import Image
    #     img = Image.open(image_path)
    #     text = pytesseract.image_to_string(img, lang="chi_sim+eng")
    #     return text
    # except:
    #     return ""
    
    return "[OCR功能需要安装 pytesseract]"


def vectorize_text(text):
    """文本向量化（预留接口）"""
    # 需要 sentence-transformers 库
    # try:
    #     from sentence_transformers import SentenceTransformer
    #     model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")
    #     embedding = model.encode(text)
    #     return embedding.tolist()
    # except:
    #     return []
    
    return "[向量化功能需要安装 sentence-transformers]"


def save_search_results(results, output_path):
    """保存搜索结果"""
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    return output_path


if __name__ == "__main__":
    print("知识库多模态检索")
    print("功能: 图片/表格/公式搜索")