#!/usr/bin/env python3
"""
research_paper_kb_like.py — GNN+LLM论文知识库
接口: fetch(arxiv_id), add(meta_dict), list(), search(keyword)
数据源: ../gnn_papers/PAPERS.md (YAML-like格式)
"""
import os, re, sys, json
from pathlib import Path

PAPERS_MD = Path(__file__).parent.parent / 'gnn_papers' / 'PAPERS.md'

def _parse_papers():
    """解析PAPERS.md，返回论文列表"""
    if not PAPERS_MD.exists():
        return []
    text = PAPERS_MD.read_text(encoding='utf-8')
    blocks = re.split(r'\n---\n', text)
    papers = []
    for block in blocks:
        block = block.strip()
        if not block or block.startswith('#'):
            continue
        paper = {}
        for line in block.splitlines():
            line = line.strip()
            m = re.match(r'^(\w+):\s*(.+)$', line)
            if m:
                key, val = m.group(1), m.group(2).strip('"')
                if val.startswith('['):
                    try:
                        val = json.loads(val.replace("'", '"'))
                    except:
                        pass
                paper[key] = val
            elif line.startswith('>') and paper:
                # 多行summary
                last_key = 'summary'
                paper[last_key] = paper.get(last_key, '') + line.lstrip('> ') + ' '
        if 'id' in paper:
            papers.append(paper)
    return papers

def list_papers():
    """列出所有论文"""
    papers = _parse_papers()
    print(f"共 {len(papers)} 篇论文:\n")
    for p in papers:
        print(f"[{p.get('id','?')}] {p.get('title','')}")
        print(f"  年份: {p.get('year','')} | 来源: {p.get('arxiv','')} | 会议: {p.get('venue','')}")
        kw = p.get('keywords', [])
        if isinstance(kw, list):
            print(f"  关键词: {', '.join(kw[:5])}")
        print(f"  相关性: {p.get('relevance','')}")
        print()
    return papers

def search(keyword):
    """按关键词搜索论文（标题/摘要/关键词）"""
    papers = _parse_papers()
    kw = keyword.lower()
    results = []
    for p in papers:
        text = ' '.join([
            str(p.get('title','')),
            str(p.get('summary','')),
            str(p.get('keywords','')),
            str(p.get('relevance',''))
        ]).lower()
        if kw in text:
            results.append(p)
    print(f"搜索 '{keyword}' → {len(results)} 条结果:")
    for p in results:
        print(f"  [{p.get('id')}] {p.get('title','')[:60]}")
    return results

def add(meta_dict):
    """追加一篇论文到PAPERS.md"""
    required = ['id', 'title', 'year', 'arxiv']
    for k in required:
        if k not in meta_dict:
            raise ValueError(f"缺少必填字段: {k}")
    block = "\n---\n"
    for k, v in meta_dict.items():
        if isinstance(v, list):
            block += f'{k}: {json.dumps(v, ensure_ascii=False)}\n'
        else:
            block += f'{k}: "{v}"\n'
    with open(PAPERS_MD, 'a', encoding='utf-8') as f:
        f.write(block)
    print(f"已添加论文: [{meta_dict['id']}] {meta_dict['title']}")

def fetch(arxiv_id):
    """从arXiv获取论文摘要（需联网）"""
    try:
        import urllib.request
        url = f"https://export.arxiv.org/abs/{arxiv_id}"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as resp:
            html = resp.read().decode('utf-8')
        title_m = re.search(r'<title>(.*?)</title>', html, re.S)
        abstract_m = re.search(r'class="abstract mathjax"[^>]*>(.*?)</blockquote>', html, re.S)
        title = title_m.group(1).strip().replace('\n',' ') if title_m else ''
        abstract = re.sub(r'<[^>]+>', '', abstract_m.group(1)).strip() if abstract_m else ''
        print(f"标题: {title}")
        print(f"摘要: {abstract[:200]}...")
        return {'title': title, 'abstract': abstract}
    except Exception as e:
        print(f"fetch失败: {e}")
        return None

if __name__ == '__main__':
    if len(sys.argv) < 2:
        list_papers()
    elif sys.argv[1] == 'search' and len(sys.argv) > 2:
        search(sys.argv[2])
    elif sys.argv[1] == 'fetch' and len(sys.argv) > 2:
        fetch(sys.argv[2])
    else:
        list_papers()

# ========== R205 多源同步增强 (2026-04-21) ==========

import hashlib
from datetime import datetime

def import_from_bibtex(bibtex_file):
    """从BibTeX文件导入论文
    
    Args:
        bibtex_file: BibTeX文件路径
    
    Returns:
        dict: {"success": int, "failed": int, "duplicates": int}
    """
    if not os.path.exists(bibtex_file):
        return {"success": 0, "failed": 1, "duplicates": 0, "error": "File not found"}
    
    with open(bibtex_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 简单解析BibTeX
    entries = re.findall(r'@\w+\{([^,]+),\s*(.+?)\}', content, re.DOTALL)
    
    success, failed, duplicates = 0, 0, 0
    for entry_id, fields in entries:
        try:
            paper = {"id": entry_id.strip()}
            for line in fields.split('\n'):
                m = re.match(r'\s*(\w+)\s*=\s*\{(.+?)\}', line)
                if m:
                    key, val = m.group(1).lower(), m.group(2).strip()
                    if key == 'title':
                        paper['title'] = val
                    elif key == 'author':
                        paper['authors'] = val
                    elif key == 'year':
                        paper['year'] = val
            
            if _is_duplicate(paper):
                duplicates += 1
            else:
                add_paper(paper)
                success += 1
        except:
            failed += 1
    
    return {"success": success, "failed": failed, "duplicates": duplicates}

def import_from_pdf_metadata(pdf_file):
    """从PDF元数据导入论文
    
    Args:
        pdf_file: PDF文件路径
    
    Returns:
        dict: {"success": bool, "paper": dict or None}
    """
    if not os.path.exists(pdf_file):
        return {"success": False, "error": "File not found"}
    
    # 简化版：从文件名提取信息
    filename = os.path.basename(pdf_file)
    paper_id = filename.replace('.pdf', '').replace(' ', '_')
    
    paper = {
        "id": paper_id,
        "title": filename.replace('.pdf', '').replace('_', ' '),
        "source": "pdf",
        "file": pdf_file
    }
    
    if _is_duplicate(paper):
        return {"success": False, "duplicate": True}
    
    add_paper(paper)
    return {"success": True, "paper": paper}

def import_from_markdown(md_file):
    """从Markdown文件导入论文
    
    Args:
        md_file: Markdown文件路径
    
    Returns:
        dict: {"success": int, "failed": int, "duplicates": int}
    """
    if not os.path.exists(md_file):
        return {"success": 0, "failed": 1, "duplicates": 0, "error": "File not found"}
    
    with open(md_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 解析Markdown格式（类似PAPERS.md）
    blocks = re.split(r'\n---\n', content)
    
    success, failed, duplicates = 0, 0, 0
    for block in blocks:
        block = block.strip()
        if not block or block.startswith('#'):
            continue
        
        paper = {}
        for line in block.splitlines():
            m = re.match(r'^(\w+):\s*(.+)$', line)
            if m:
                paper[m.group(1)] = m.group(2).strip('"')
        
        if 'id' in paper:
            if _is_duplicate(paper):
                duplicates += 1
            else:
                try:
                    add_paper(paper)
                    success += 1
                except:
                    failed += 1
    
    return {"success": success, "failed": failed, "duplicates": duplicates}

def _is_duplicate(paper):
    """检查论文是否重复
    
    Args:
        paper: 论文字典
    
    Returns:
        bool: True表示重复
    """
    existing = _parse_papers()
    
    # 方法1: ID完全匹配
    if any(p.get('id') == paper.get('id') for p in existing):
        return True
    
    # 方法2: 标题相似度（简化版：完全匹配）
    paper_title = paper.get('title', '').lower().strip()
    if paper_title:
        for p in existing:
            if p.get('title', '').lower().strip() == paper_title:
                return True
    
    return False

def calc_similarity(text1, text2):
    """计算文本相似度（简化版）
    
    Args:
        text1, text2: 待比较文本
    
    Returns:
        float: 相似度 0-1
    """
    if not text1 or not text2:
        return 0.0
    
    text1 = text1.lower().strip()
    text2 = text2.lower().strip()
    
    if text1 == text2:
        return 1.0
    
    # 简单的Jaccard相似度
    words1 = set(text1.split())
    words2 = set(text2.split())
    
    intersection = len(words1 & words2)
    union = len(words1 | words2)
    
    return intersection / union if union > 0 else 0.0

def sync_from_sources(sources):
    """从多个数据源同步
    
    Args:
        sources: [{"type": "bibtex|pdf|markdown", "path": str}, ...]
    
    Returns:
        dict: 同步统计
    """
    total_success = 0
    total_failed = 0
    total_duplicates = 0
    results = []
    
    for source in sources:
        source_type = source.get('type')
        path = source.get('path')
        
        if source_type == 'bibtex':
            result = import_from_bibtex(path)
        elif source_type == 'pdf':
            result = import_from_pdf_metadata(path)
            if result.get('success'):
                result = {"success": 1, "failed": 0, "duplicates": 0}
            elif result.get('duplicate'):
                result = {"success": 0, "failed": 0, "duplicates": 1}
            else:
                result = {"success": 0, "failed": 1, "duplicates": 0}
        elif source_type == 'markdown':
            result = import_from_markdown(path)
        else:
            result = {"success": 0, "failed": 1, "duplicates": 0, "error": "Unknown type"}
        
        total_success += result.get('success', 0)
        total_failed += result.get('failed', 0)
        total_duplicates += result.get('duplicates', 0)
        results.append({"source": path, "result": result})
    
    total = total_success + total_failed + total_duplicates
    success_rate = (total_success / total * 100) if total > 0 else 0
    
    return {
        "total": total,
        "success": total_success,
        "failed": total_failed,
        "duplicates": total_duplicates,
        "success_rate": success_rate,
        "details": results
    }

def get_sync_status():
    """获取同步状态
    
    Returns:
        dict: 状态信息
    """
    papers = _parse_papers()
    
    sources = {}
    for p in papers:
        src = p.get('source', 'unknown')
        sources[src] = sources.get(src, 0) + 1
    
    return {
        "total_papers": len(papers),
        "sources": sources,
        "last_sync": datetime.now().isoformat()
    }
