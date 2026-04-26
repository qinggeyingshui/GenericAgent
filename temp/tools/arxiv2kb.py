#!/usr/bin/env python3
"""
arxiv2kb.py - arXiv论文在线抓取并自动入库GNN论文库
用法:
  python arxiv2kb.py <arxiv_url_or_id> [<arxiv_url_or_id> ...]
  例: python arxiv2kb.py 2402.08678 https://arxiv.org/abs/2412.10234
"""
import sys, os, re, json
import urllib.request
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'local_skills'))
from research_paper_kb_like import add, _parse_papers

def extract_id(raw):
    """从URL或纯ID提取arXiv ID"""
    m = re.search(r'(\d{4}\.\d{4,5})', raw)
    return m.group(1) if m else None

def fetch_meta(arxiv_id):
    """抓取arXiv页面，返回元数据dict"""
    url = f'https://export.arxiv.org/abs/{arxiv_id}'
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=15) as resp:
        html = resp.read().decode('utf-8')

    title_m = re.search(r'<title>(.*?)</title>', html, re.S)
    abstract_m = re.search(
        r'class="abstract mathjax"[^>]*>\s*<span[^>]*>Abstract:</span>(.*?)</blockquote>',
        html, re.S)
    authors_m = re.search(r'class="authors">(.*?)</div>', html, re.S)
    year_m = re.search(r'(20\d{2})', arxiv_id)

    raw_title = title_m.group(1).strip().replace('\n', ' ') if title_m else arxiv_id
    # 去掉 "[2402.08678] " 前缀
    title = re.sub(r'^\[\S+\]\s*', '', raw_title)

    abstract = ''
    if abstract_m:
        abstract = re.sub(r'<[^>]+>', '', abstract_m.group(1)).strip().replace('\n', ' ')

    authors = []
    if authors_m:
        authors = re.findall(r'<a[^>]*>(.*?)</a>', authors_m.group(1))

    year = year_m.group(1) if year_m else '2024'

    return {
        'id': 'arXiv' + arxiv_id.replace('.', ''),
        'title': title,
        'authors': authors,
        'year': year,
        'arxiv': f'arXiv:{arxiv_id}',
        'venue': 'arXiv preprint',
        'keywords': ['GNN', 'graph neural network'],
        'summary': abstract[:300],
        'relevance': f'arXiv:{arxiv_id} 自动入库',
    }

def main():
    if len(sys.argv) < 2:
        print("用法: python arxiv2kb.py <arxiv_id_or_url> ...")
        sys.exit(1)

    existing_ids = {p['id'] for p in _parse_papers()}

    for raw in sys.argv[1:]:
        arxiv_id = extract_id(raw)
        if not arxiv_id:
            print(f"[跳过] 无法解析arXiv ID: {raw}")
            continue

        candidate_id = 'arXiv' + arxiv_id.replace('.', '')
        if candidate_id in existing_ids:
            print(f"[已存在] {arxiv_id} ({candidate_id})，跳过")
            continue

        print(f"[抓取] https://export.arxiv.org/abs/{arxiv_id} ...")
        try:
            meta = fetch_meta(arxiv_id)
            add(meta)
            print(f"  标题: {meta['title'][:60]}")
            print(f"  作者: {meta['authors'][:2]}")
        except Exception as e:
            print(f"[失败] {arxiv_id}: {e}")

if __name__ == "__main__":
    main()
