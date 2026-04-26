# local_skills/search_kb_semantic.py
"""
GNN论文知识库语义搜索引擎 - Phase 1 (TF-IDF + Cosine Similarity)

接口:
  search_semantic(query, top_k=5) -> (List[Dict], elapsed_sec)
  build_index(force=False)        -> cache dict
  list_papers()                   -> List[Dict]

Phase 2升级路径: 替换TfidfVectorizer为sentence-transformers
  需要: pip install sentence-transformers torch
"""

import os, sys, re, pickle, time
from typing import List, Dict
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# ─── 路径配置 ────────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# local_skills在temp下，gnn_papers在temp的上级(GenericAgent)下
TEMP_DIR = os.path.dirname(BASE_DIR)
ROOT_DIR = os.path.dirname(TEMP_DIR)
PAPERS_MD = os.path.join(ROOT_DIR, "gnn_papers", "PAPERS.md")
CACHE_FILE = os.path.join(BASE_DIR, "paper_embeddings.pkl")


# ─── PAPERS.md 解析器（适配YAML-like格式）───────────────────────────
def parse_papers_md(path: str = PAPERS_MD) -> List[Dict]:
    """解析YAML-like块格式的PAPERS.md，返回结构化论文列表"""
    if not os.path.exists(path):
        raise FileNotFoundError(f"PAPERS.md not found: {path}")
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    papers = []
    blocks = re.split(r"\n---\n", content)
    for block in blocks:
        block = block.strip()
        if not block or block.startswith("#"):
            continue
        paper = _parse_block(block)
        if paper and paper.get("id") and paper.get("title"):
            if "QUICK_START" in paper.get("id", ""):
                continue
            papers.append(paper)
    return papers


def _parse_block(block: str) -> Dict:
    """解析单个YAML-like块"""
    paper = {}
    lines = block.split("\n")
    i = 0
    while i < len(lines):
        line = lines[i]
        # 多行字段 (summary: >)
        if re.match(r"^(summary|applications|relevance):\s*>\s*$", line):
            key = line.split(":")[0].strip()
            val_lines = []
            i += 1
            while i < len(lines) and (lines[i].startswith("  ") or lines[i].strip() == ""):
                val_lines.append(lines[i].strip())
                i += 1
            paper[key] = " ".join(v for v in val_lines if v)
            continue
        # 单行字段
        m = re.match(r"^(\w+):\s*(.*)", line)
        if m:
            key, val = m.group(1), m.group(2).strip().strip('"')
            if val.startswith("["):
                items = re.findall(r'"([^"]+)"', val)
                paper[key] = items
            else:
                paper[key] = val
        i += 1
    return paper


# ─── 文本特征构建 ────────────────────────────────────────────────────
def _build_doc_text(paper: dict) -> str:
    """将论文各字段拼接为检索文档，重要字段加权重复"""
    parts = []
    title = paper.get("title", "")
    parts.extend([title] * 3)
    kws = paper.get("keywords", [])
    kw_str = " ".join(kws) if isinstance(kws, list) else str(kws)
    parts.extend([kw_str] * 2)
    parts.append(paper.get("summary", ""))
    parts.append(paper.get("relevance", ""))
    parts.append(paper.get("applications", ""))
    parts.append(paper.get("venue", ""))
    parts.append(str(paper.get("year", "")))
    return " ".join(p for p in parts if p)


# ─── 索引构建与缓存 ──────────────────────────────────────────────────
def build_index(force: bool = False) -> dict:
    """构建TF-IDF索引，缓存到pkl文件（自动检测PAPERS.md变更）"""
    if not force and os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "rb") as f:
            cache = pickle.load(f)
        mtime = os.path.getmtime(PAPERS_MD)
        if cache.get("mtime") == mtime:
            return cache

    t0 = time.time()
    papers = parse_papers_md()
    docs = [_build_doc_text(p) for p in papers]

    # 使用char n-gram同时支持中英文（无需jieba）
    # char_wb对中文字符自然分词，对英文也保留词边界
    vectorizer = TfidfVectorizer(
        analyzer="char_wb",
        ngram_range=(2, 4),
        min_df=1,
        max_features=8000,
        sublinear_tf=True
    )
    tfidf_matrix = vectorizer.fit_transform(docs)

    cache = {
        "papers": papers,
        "vectorizer": vectorizer,
        "tfidf_matrix": tfidf_matrix,
        "mtime": os.path.getmtime(PAPERS_MD),
        "build_time": time.time() - t0,
        "engine": "tfidf-phase1"
    }
    with open(CACHE_FILE, "wb") as f:
        pickle.dump(cache, f)
    return cache


# ─── 核心搜索接口 ────────────────────────────────────────────────────
def search_semantic(query: str, top_k: int = 5):
    """
    语义搜索GNN论文知识库

    Args:
        query: 自然语言查询，如"图神经网络时序预测"
        top_k: 返回前K篇论文

    Returns:
        (results: List[Dict], elapsed: float)
        results每项: {id, title, score, year, venue, keywords, relevance, summary_snippet, arxiv}
    """
    t0 = time.time()
    cache = build_index()
    papers = cache["papers"]
    vectorizer = cache["vectorizer"]
    tfidf_matrix = cache["tfidf_matrix"]

    query_vec = vectorizer.transform([query])
    scores = cosine_similarity(query_vec, tfidf_matrix)[0]
    top_indices = np.argsort(scores)[::-1][:top_k]

    results = []
    for idx in top_indices:
        if scores[idx] < 0.001:
            continue
        p = papers[idx]
        summary = p.get("summary", "")
        snippet = (summary[:150] + "...") if len(summary) > 150 else summary
        results.append({
            "id": p.get("id", ""),
            "title": p.get("title", ""),
            "score": round(float(scores[idx]), 4),
            "year": p.get("year", ""),
            "venue": p.get("venue", ""),
            "keywords": p.get("keywords", []),
            "relevance": p.get("relevance", ""),
            "summary_snippet": snippet,
            "arxiv": p.get("arxiv", ""),
        })

    elapsed = time.time() - t0
    return results, elapsed


def list_papers() -> list:
    """列出所有论文 (id, title, year, venue)"""
    papers = parse_papers_md()
    return [
        {"id": p.get("id"), "title": p.get("title"),
         "year": p.get("year"), "venue": p.get("venue")}
        for p in papers
    ]


# ─── CLI ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python search_kb_semantic.py <查询语句> [top_k]")
        print('示例: python search_kb_semantic.py "图神经网络时序预测" 5')
        sys.exit(0)

    query = sys.argv[1]
    top_k = int(sys.argv[2]) if len(sys.argv) > 2 else 5

    print(f"\n搜索: {query}")
    print("-" * 60)
    results, elapsed = search_semantic(query, top_k)

    if not results:
        print("未找到相关论文")
    else:
        for i, r in enumerate(results, 1):
            kws = r["keywords"]
            kw_str = ", ".join(kws[:5]) if isinstance(kws, list) else str(kws)
            print(f"\n#{i} [score={r['score']:.4f}] {r['title']}")
            print(f"   ID: {r['id']} | {r['year']} | {r['venue']}")
            print(f"   关键词: {kw_str}")
            print(f"   摘要: {r['summary_snippet']}")
            if r["relevance"]:
                print(f"   教学: {r['relevance'][:80]}")

    print(f"\n响应时间: {elapsed:.3f}s | 共{len(results)}篇结果")
