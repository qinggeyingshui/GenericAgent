"""
知识库语义检索模块
使用TF-IDF + 余弦相似度实现语义搜索和相关推荐
"""
import os
import json
from pathlib import Path
from typing import List, Dict, Tuple
import jieba
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class SemanticSearch:
    def __init__(self, kb_root="./teaching_kb"):
        self.kb_root = Path(kb_root)
        self.documents = []  # [{id, path, title, content}]
        self.vectorizer = None
        self.tfidf_matrix = None
        
    def _extract_documents(self):
        """扫描teaching_kb提取所有文档"""
        docs = []
        courses_dir = self.kb_root / "courses"
        if not courses_dir.exists():
            return docs
        
        doc_id = 0
        for course_dir in courses_dir.iterdir():
            if not course_dir.is_dir():
                continue
            lessons_dir = course_dir / "lessons"
            if not lessons_dir.exists():
                continue
            
            for lesson_dir in lessons_dir.iterdir():
                if not lesson_dir.is_dir():
                    continue
                lesson_plan = lesson_dir / "lesson_plan.md"
                if not lesson_plan.exists():
                    continue
                
                # 读取文档
                with open(lesson_plan, "r", encoding="utf-8") as f:
                    content = f.read()
                
                # 提取标题（第一行#标题）
                title = lesson_dir.name
                lines = content.split("\n")
                for line in lines:
                    if line.startswith("#"):
                        title = line.lstrip("#").strip()
                        break
                
                docs.append({
                    "id": doc_id,
                    "path": str(lesson_plan.relative_to(self.kb_root)),
                    "course": course_dir.name,
                    "lesson": lesson_dir.name,
                    "title": title,
                    "content": content
                })
                doc_id += 1
        
        return docs
    
    def _tokenize(self, text):
        """中文分词"""
        return " ".join(jieba.cut(text))
    
    def build_index(self):
        """构建TF-IDF索引"""
        self.documents = self._extract_documents()
        if not self.documents:
            raise ValueError("未找到任何文档")
        
        # 构建语料库（标题+内容）
        corpus = [self._tokenize(doc["title"] + " " + doc["content"]) 
                  for doc in self.documents]
        
        # TF-IDF向量化
        self.vectorizer = TfidfVectorizer(max_features=1000)
        self.tfidf_matrix = self.vectorizer.fit_transform(corpus)
        
        return len(self.documents)
    
    def search(self, query: str, top_k: int = 5) -> List[Dict]:
        """语义搜索"""
        if self.vectorizer is None:
            raise ValueError("索引未构建，请先调用build_index()")
        
        # 查询向量化
        query_vec = self.vectorizer.transform([self._tokenize(query)])
        
        # 计算余弦相似度
        similarities = cosine_similarity(query_vec, self.tfidf_matrix)[0]
        
        # 排序并返回top_k
        top_indices = np.argsort(similarities)[::-1][:top_k]
        
        results = []
        for idx in top_indices:
            if similarities[idx] > 0:  # 过滤相似度为0的结果
                doc = self.documents[idx].copy()
                doc["score"] = float(similarities[idx])
                doc.pop("content")  # 不返回完整内容
                results.append(doc)
        
        return results
    
    def recommend(self, doc_id: int, top_k: int = 5) -> List[Dict]:
        """相关推荐"""
        if self.tfidf_matrix is None:
            raise ValueError("索引未构建，请先调用build_index()")
        
        if doc_id >= len(self.documents):
            raise ValueError(f"文档ID {doc_id} 不存在")
        
        # 计算与目标文档的相似度
        doc_vec = self.tfidf_matrix[doc_id]
        similarities = cosine_similarity(doc_vec, self.tfidf_matrix)[0]
        
        # 排序（排除自身）
        top_indices = np.argsort(similarities)[::-1][1:top_k+1]
        
        results = []
        for idx in top_indices:
            if similarities[idx] > 0:
                doc = self.documents[idx].copy()
                doc["score"] = float(similarities[idx])
                doc.pop("content")
                results.append(doc)
        
        return results
    
    def get_document(self, doc_id: int) -> Dict:
        """获取文档详情"""
        if doc_id >= len(self.documents):
            raise ValueError(f"文档ID {doc_id} 不存在")
        return self.documents[doc_id]

def demo():
    """演示用法"""
    ss = SemanticSearch()
    
    # 构建索引
    doc_count = ss.build_index()
    print(f"已索引 {doc_count} 个文档")
    
    # 搜索示例
    query = "图神经网络"
    results = ss.search(query, top_k=3)
    print(f"\n搜索: {query}")
    for r in results:
        score = r['score']
        course = r['course']
        title = r['title']
        print(f"  [{score:.3f}] {course} - {title}")
    
    # 推荐示例
    if doc_count > 0:
        recs = ss.recommend(0, top_k=3)
        print(f"\n相关推荐 (基于文档0):")
        for r in recs:
            score = r['score']
            course = r['course']
            title = r['title']
            print(f"  [{score:.3f}] {course} - {title}")

if __name__ == "__main__":
    demo()