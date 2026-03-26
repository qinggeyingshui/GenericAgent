#!/usr/bin/env python3
"""
pdf_reader.py - PDF解析local_skill
接口: extract(pdf_path), meta(pdf_path), tables(pdf_path), search(pdf_path, keyword)
依赖: pdfplumber (pip install pdfplumber)
输出目录: ./pdf_extracts/<stem>/
"""
import os, sys, json, re, argparse
from pathlib import Path

try:
    import pdfplumber
except ImportError:
    print("ERROR: pdfplumber未安装，请运行: pip install pdfplumber")
    sys.exit(1)

OUTPUT_DIR = Path(__file__).parent / "pdf_extracts"


def _ensure_out(stem):
    d = OUTPUT_DIR / stem
    d.mkdir(parents=True, exist_ok=True)
    return d


def extract(pdf_path, save=True):
    """提取PDF全文文本，返回按页列表"""
    path = Path(pdf_path)
    if not path.exists():
        print(f"ERROR: 文件不存在: {pdf_path}")
        return None
    pages = []
    with pdfplumber.open(path) as pdf:
        for i, page in enumerate(pdf.pages):
            text = page.extract_text() or ""
            pages.append({"page": i+1, "text": text.strip()})
    if save:
        out = _ensure_out(path.stem)
        out_file = out / "text.json"
        with open(out_file, "w", encoding="utf-8") as f:
            json.dump(pages, f, ensure_ascii=False, indent=2)
        print(f"文本已提取: {len(pages)}页 -> {out_file}")
    else:
        print(f"文本提取: {len(pages)}页")
    return pages


def meta(pdf_path):
    """提取PDF元数据（标题/作者/创建时间/页数/版本等）"""
    path = Path(pdf_path)
    if not path.exists():
        print(f"ERROR: 文件不存在: {pdf_path}")
        return None
    with pdfplumber.open(path) as pdf:
        info = {
            "pages": len(pdf.pages),
            "metadata": pdf.metadata or {},
        }
        if pdf.pages:
            p0 = pdf.pages[0]
            info["page_width"] = round(p0.width, 1)
            info["page_height"] = round(p0.height, 1)
    out = _ensure_out(path.stem)
    out_file = out / "meta.json"
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(info, f, ensure_ascii=False, indent=2)
    print(f"元数据: 共{info['pages']}页, 尺寸{info.get('page_width')}x{info.get('page_height')}pt")
    for k, v in info["metadata"].items():
        print(f"  {k}: {v}")
    print(f"  -> 已保存: {out_file}")
    return info


def tables(pdf_path, pages=None):
    """提取PDF中的表格，返回表格列表"""
    path = Path(pdf_path)
    if not path.exists():
        print(f"ERROR: 文件不存在: {pdf_path}")
        return None
    all_tables = []
    with pdfplumber.open(path) as pdf:
        page_list = pdf.pages if pages is None else [pdf.pages[i-1] for i in pages if i <= len(pdf.pages)]
        for page in page_list:
            tbls = page.extract_tables()
            for tbl in tbls:
                all_tables.append({"page": page.page_number, "rows": len(tbl), "cols": len(tbl[0]) if tbl else 0, "data": tbl})
    out = _ensure_out(path.stem)
    out_file = out / "tables.json"
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(all_tables, f, ensure_ascii=False, indent=2)
    print(f"表格提取: 共{len(all_tables)}张表格 -> {out_file}")
    for t in all_tables:
        print(f"  第{t['page']}页: {t['rows']}行x{t['cols']}列")
    return all_tables


def search(pdf_path, keyword, context=80):
    """在PDF全文中搜索关键词，返回命中行及上下文"""
    pages = extract(pdf_path, save=False)
    if pages is None:
        return []
    kw = keyword.lower()
    results = []
    for p in pages:
        text = p["text"]
        idx = 0
        lower_text = text.lower()
        while True:
            pos = lower_text.find(kw, idx)
            if pos == -1:
                break
            start = max(0, pos - context)
            end = min(len(text), pos + len(kw) + context)
            results.append({"page": p["page"], "pos": pos, "snippet": text[start:end].replace("\n", " ")})
            idx = pos + 1
    print(f"搜索 '{keyword}' -> {len(results)} 处命中")
    for r in results[:10]:
        print(f"  第{r['page']}页: ...{r['snippet']}...")
    return results


def main():
    parser = argparse.ArgumentParser(description="PDF解析工具")
    sub = parser.add_subparsers(dest="cmd")

    p_ex = sub.add_parser("extract", help="提取全文文本")
    p_ex.add_argument("pdf", help="PDF文件路径")

    p_meta = sub.add_parser("meta", help="提取元数据")
    p_meta.add_argument("pdf", help="PDF文件路径")

    p_tbl = sub.add_parser("tables", help="提取表格")
    p_tbl.add_argument("pdf", help="PDF文件路径")

    p_srch = sub.add_parser("search", help="搜索关键词")
    p_srch.add_argument("pdf", help="PDF文件路径")
    p_srch.add_argument("keyword", help="搜索关键词")

    args = parser.parse_args()
    if args.cmd == "extract":
        extract(args.pdf)
    elif args.cmd == "meta":
        meta(args.pdf)
    elif args.cmd == "tables":
        tables(args.pdf)
    elif args.cmd == "search":
        search(args.pdf, args.keyword)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
