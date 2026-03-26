#!/usr/bin/env python3
"""
kb_cli.py - GNN论文库命令行查询工具
用法:
  python kb_cli.py list [--year YEAR] [--keyword KW]
  python kb_cli.py search KEYWORD [--year YEAR]
  python kb_cli.py fetch ARXIV_ID
"""
import sys, os, argparse
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'local_skills'))
from research_paper_kb_like import _parse_papers, fetch as _fetch

def fmt_table(papers):
    """输出Markdown表格"""
    if not papers:
        print("(无结果)")
        return
    print(f"| ID | 标题 | 年份 | 来源 | 会议 |")
    print(f"|---|---|---|---|---|")
    for p in papers:
        tid = p.get("id","?")
        title = p.get("title","")[:50]
        year = p.get("year","")
        arxiv = p.get("arxiv","")
        venue = p.get("venue","")
        print(f"| {tid} | {title} | {year} | {arxiv} | {venue} |")
    print(f"\n共 {len(papers)} 篇")

def cmd_list(args):
    papers = _parse_papers()
    if args.year:
        papers = [p for p in papers if str(p.get("year","")) == str(args.year)]
    if args.keyword:
        kw = args.keyword.lower()
        papers = [p for p in papers if kw in str(p).lower()]
    fmt_table(papers)

def cmd_search(args):
    kw = args.keyword.lower()
    papers = _parse_papers()
    results = [p for p in papers if kw in str(p).lower()]
    if args.year:
        results = [p for p in results if str(p.get("year","")) == str(args.year)]
    fmt_table(results)

def cmd_fetch(args):
    result = _fetch(args.arxiv_id)
    if result:
        print("标题:", result.get("title",""))
        print("摘要:", result.get("abstract","")[:300])

def main():
    parser = argparse.ArgumentParser(description="GNN论文库CLI")
    sub = parser.add_subparsers(dest="cmd")

    p_list = sub.add_parser("list", help="列出论文")
    p_list.add_argument("--year", help="按年份过滤")
    p_list.add_argument("--keyword", help="按关键词过滤")

    p_search = sub.add_parser("search", help="关键词搜索")
    p_search.add_argument("keyword", help="搜索关键词")
    p_search.add_argument("--year", help="按年份过滤")

    p_fetch = sub.add_parser("fetch", help="从arXiv抓取摘要")
    p_fetch.add_argument("arxiv_id", help="arXiv ID, 例如 1810.00826")

    args = parser.parse_args()
    if args.cmd == "list":
        cmd_list(args)
    elif args.cmd == "search":
        cmd_search(args)
    elif args.cmd == "fetch":
        cmd_fetch(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
