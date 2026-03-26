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