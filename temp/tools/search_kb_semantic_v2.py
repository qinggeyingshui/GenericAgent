# local_skills/search_kb_semantic_v2.py
"""
GNN论文知识库语义搜索引擎 - Phase 2 (Sentence-Transformers)

升级内容:
- 使用 sentence-transformers 替代 TF-IDF
- 模型: paraphrase-multilingual-MiniLM-L12-v2 (支持中英文)
- 真正的语义理解，而非词频统计

接口保持兼容:
  search_semantic(query, top_k=5) -> (List[Dict], elapsed_sec)
  build_index(force=False) -> cache_dict
  list_papers() -> List[Dict]
"""

import os
import sys
import time
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# 路径配置
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
KB_PATH = os.path.join(SCRIPT_DIR, "..", "gnn_papers", "PAPERS.md")
CACHE_FILE = os.path.join(SCRIPT_DIR, ".semantic_cache_v2.pkl")
MODEL_NAME = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"

# 全局模型实例（延迟加载）
_model = None

def _get_model():
    """延迟加载模型（首次调用时加载）"""
    global _model
    if _model is None:
        print(f"[INFO] 加载模型: {MODEL_NAME}")
        _model = SentenceTransformer(MODEL_NAME)
        print("[INFO] 模型加载完成")
    return _model

def _parse_papers():
    """解析PAPERS.md，返回论文列表"""
    if not os.path.exists(KB_PATH):
        return []
    
    papers = []
    with open(KB_PATH, "r", encoding="utf-8") as f:
        content = f.read()
    
    # 按## 分割论文条目
    entries = content.split("\n## ")[1:]  # 跳过文件头
    
    for entry in entries:
        lines_in_entry = entry.strip().split("\n")
        if not lines_in_entry:
            continue
        
        title = lines_in_entry[0].strip()
        
        # 提取字段
        authors = ""
        year = ""
        venue = ""
        summary = ""
        
        for line in lines_in_entry[1:]:
            if line.startswith("**作者**:"):
                authors = line.replace("**作者**:", "").strip()
            elif line.startswith("**年份**:"):
                year = line.replace("**年份**:", "").strip()
            elif line.startswith("**会议/期刊**:"):
                venue = line.replace("**会议/期刊**:", "").strip()
            elif line.startswith("**摘要**:"):
                summary = line.replace("**摘要**:", "").strip()
        
        # 构建搜索文本（标题+摘要）
        search_text = f"{title} {summary}"
        
        papers.append({
            "title": title,
            "authors": authors,
            "year": year,
            "venue": venue,
            "summary": summary,
            "search_text": search_text
        })
    
    return papers

def build_index(force=False):
    """
    构建语义索引（向量化所有论文）
    
    Args:
        force: 强制重建索引
    
    Returns:
        cache_dict: {papers, embeddings, model_name, build_time}
    """
    # 检查缓存
    if not force and os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, "rb") as f:
                cache = pickle.load(f)
            print(f"[INFO] 加载缓存: {len(cache['papers'])} 篇论文")
            return cache
        except Exception as e:
            print(f"[WARN] 缓存加载失败: {e}，重建索引")
    
    # 解析论文
    papers = _parse_papers()
    if not papers:
        print("[WARN] 未找到论文数据")
        return {'papers': [], 'embeddings': None, 'model_name': MODEL_NAME, 'build_time': time.time()}
    
    print(f"[INFO] 开始向量化 {len(papers)} 篇论文...")
    
    # 加载模型
    model = _get_model()
    
    # 提取搜索文本
    texts = [p["search_text"] for p in papers]
    
    # 编码为向量
    start_time = time.time()
    embeddings = model.encode(texts, show_progress_bar=True, convert_to_numpy=True)
    elapsed = time.time() - start_time
    
    print(f"[INFO] 向量化完成，耗时 {elapsed:.2f}s")
    print(f"[INFO] 向量维度: {embeddings.shape}")
    
    # 保存缓存
    cache = {
        'papers': papers,
        'embeddings': embeddings,
        'model_name': MODEL_NAME,
        'build_time': time.time()
    }
    
    with open(CACHE_FILE, "wb") as f:
        pickle.dump(cache, f)
    
    print(f"[INFO] 索引已保存: {CACHE_FILE}")
    return cache

def search_semantic(query, top_k=5):
    """
    语义搜索
    
    Args:
        query: 查询语句
        top_k: 返回前k个结果
    
    Returns:
        (results, elapsed_sec)
        results: List[Dict] 包含title, authors, year, venue, summary, score
    """
    start_time = time.time()
    
    # 加载索引
    cache = build_index()
    papers = cache['papers']
    embeddings = cache['embeddings']
    
    if not papers or embeddings is None:
        return [], 0.0
    
    # 加载模型
    model = _get_model()
    
    # 编码查询
    query_embedding = model.encode([query], convert_to_numpy=True)
    
    # 计算余弦相似度
    similarities = cosine_similarity(query_embedding, embeddings)[0]
    
    # 排序并取top_k
    top_indices = np.argsort(similarities)[::-1][:top_k]
    
    # 构建结果
    results = []
    for idx in top_indices:
        paper = papers[idx].copy()
        paper['score'] = float(similarities[idx])
        del paper['search_text']  # 移除内部字段
        results.append(paper)
    
    elapsed = time.time() - start_time
    return results, elapsed

def list_papers():
    """列出所有论文"""
    cache = build_index()
    papers = cache['papers']
    return [{k: v for k, v in p.items() if k != 'search_text'} for p in papers]

def recommend_papers(paper_title, top_k=5):
    """
    基于论文标题推荐相关论文
    
    Args:
        paper_title: 目标论文标题（支持部分匹配）
        top_k: 返回前k个相关论文
    
    Returns:
        (results, elapsed_sec)
        results: List[Dict] 包含title, authors, year, venue, summary, score
    """
    start_time = time.time()
    
    # 加载索引
    cache = build_index()
    papers = cache['papers']
    embeddings = cache['embeddings']
    
    if not papers or embeddings is None:
        return [], 0.0
    
    # 查找目标论文
    target_idx = None
    paper_title_lower = paper_title.lower()
    
    for idx, paper in enumerate(papers):
        if paper_title_lower in paper['title'].lower():
            target_idx = idx
            break
    
    if target_idx is None:
        print(f"[WARN] 未找到论文: {paper_title}")
        return [], time.time() - start_time
    
    # 获取目标论文向量
    target_embedding = embeddings[target_idx:target_idx+1]
    
    # 计算与所有论文的相似度
    similarities = cosine_similarity(target_embedding, embeddings)[0]
    
    # 排序（排除自己）
    indices_scores = [(i, similarities[i]) for i in range(len(papers)) if i != target_idx]
    indices_scores.sort(key=lambda x: x[1], reverse=True)
    
    # 取top_k
    top_indices = [i for i, _ in indices_scores[:top_k]]
    
    # 构建结果
    results = []
    for idx in top_indices:
        paper = papers[idx].copy()
        paper['score'] = float(similarities[idx])
        del paper['search_text']
        results.append(paper)
    
    elapsed = time.time() - start_time
    return results, elapsed

# ─── CLI ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法:")
        print("  搜索: python search_kb_semantic_v2.py search <查询语句> [top_k]")
        print("  推荐: python search_kb_semantic_v2.py recommend <论文标题> [top_k]")
        print('示例:')
        print('  python search_kb_semantic_v2.py search "图神经网络时序预测" 5')
        print('  python search_kb_semantic_v2.py recommend "GraphSAGE" 3')
        sys.exit(0)
    
    command = sys.argv[1]
    
    if command == "search":
        if len(sys.argv) < 3:
            print("错误: 缺少查询语句")
            sys.exit(1)
        
        query = sys.argv[2]
        top_k = int(sys.argv[3]) if len(sys.argv) > 3 else 5
        
        print(f"\n查询: {query}")
        print(f"Top-{top_k} 结果:\n")
        
        results, elapsed = search_semantic(query, top_k)
        
        for i, paper in enumerate(results, 1):
            print(f"{i}. [{paper['score']:.4f}] {paper['title']}")
            print(f"   {paper['authors']} ({paper['year']}) - {paper['venue']}")
            print(f"   {paper['summary'][:100]}...\n")
        
        print(f"搜索耗时: {elapsed:.3f}s")
    
    elif command == "recommend":
        if len(sys.argv) < 3:
            print("错误: 缺少论文标题")
            sys.exit(1)
        
        paper_title = sys.argv[2]
        top_k = int(sys.argv[3]) if len(sys.argv) > 3 else 5
        
        print(f"\n基于论文: {paper_title}")
        print(f"推荐 Top-{top_k} 相关论文:\n")
        
        results, elapsed = recommend_papers(paper_title, top_k)
        
        if not results:
            print("未找到相关论文")
        else:
            for i, paper in enumerate(results, 1):
                print(f"{i}. [{paper['score']:.4f}] {paper['title']}")
                print(f"   {paper['authors']} ({paper['year']}) - {paper['venue']}")
                print(f"   {paper['summary'][:100]}...\n")
        
        print(f"推荐耗时: {elapsed:.3f}s")
    
    else:
        print(f"错误: 未知命令 '{command}'")
        print("支持的命令: search, recommend")
        sys.exit(1)
