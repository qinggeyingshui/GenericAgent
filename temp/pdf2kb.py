#!/usr/bin/env python3
"""
pdf2kb.py — PDF→GNN论文库自动入库pipeline
用法:
  python pdf2kb.py <pdf_path>          # 单文件入库
  python pdf2kb.py <dir/>              # 批量处理目录下所有PDF
  python pdf2kb.py <pdf_path> --dry    # 仅预览不写入
依赖: pdfplumber, local_skills/pdf_reader.py + research_paper_kb_like.py
"""
import os, sys, re, json, argparse
from pathlib import Path

AGENT_ROOT = Path(__file__).parent.parent
LOCAL_SKILLS = AGENT_ROOT / "local_skills"
sys.path.insert(0, str(LOCAL_SKILLS))

from pdf_reader import extract, meta
from research_paper_kb_like import add, search, _parse_papers


def _existing_ids():
    """已入库的论文ID集合，防重复"""
    return {p["id"] for p in _parse_papers()}


def _extract_title_from_text(pages):
    """从PDF首页文本启发式提取标题（取第一非空行）"""
    if not pages:
        return "Unknown Title"
    first = pages[0].get("text", "")
    for line in first.splitlines():
        line = line.strip()
        if len(line) > 10 and not line.startswith("http"):
            return line[:120]
    return "Unknown Title"


def _extract_year_from_text(pages):
    """从PDF前3页文本启发式提取年份（取最早的4位年份数字）"""
    text = " ".join(p.get("text", "") for p in pages[:3])
    years = re.findall(r"\b(20[0-2][0-9])\b", text)
    if years:
        return min(years)
    return "2024"


def _extract_abstract(pages, max_chars=400):
    """提取Abstract段落"""
    text = " ".join(p.get("text", "") for p in pages[:3])
    m = re.search(r"Abstract[.:\s]+(.{50,}?)(?:\n\n|Introduction|1\s+Intro)", text, re.DOTALL | re.IGNORECASE)
    if m:
        ab = m.group(1).replace("\n", " ").strip()
        return ab[:max_chars]
    return ""


def process_pdf(pdf_path, dry_run=False):
    """处理单个PDF，提取元数据并入库"""
    path = Path(pdf_path)
    if not path.exists():
        print(f"[SKIP] 文件不存在: {pdf_path}")
        return None

    stem = path.stem
    print(f"\n处理: {path.name}")

    # 检查是否已入库（按文件名stem判断ID）
    existing = _existing_ids()
    paper_id = re.sub(r"[^a-zA-Z0-9_-]", "_", stem)[:30]
    if paper_id in existing:
        print(f"  [已存在] ID={paper_id}，跳过")
        return None

    # 提取文本
    pages = extract(pdf_path, save=False)
    if not pages:
        print(f"  [ERROR] 文本提取失败")
        return None

    # 构建元数据
    title = _extract_title_from_text(pages)
    year  = _extract_year_from_text(pages)
    abstract = _extract_abstract(pages)

    meta_dict = {
        "id":      paper_id,
        "title":   title,
        "year":    year,
        "arxiv":   stem,
        "venue":   "unknown",
        "summary": abstract or "(无摘要)",
        "keywords": [],
        "relevance": "auto-imported",
    }

    print(f"  ID:    {meta_dict['id']}")
    print(f"  Title: {meta_dict['title'][:80]}")
    print(f"  Year:  {meta_dict['year']}")
    print(f"  Abstr: {meta_dict['summary'][:60]}...")

    if dry_run:
        print("  [DRY-RUN] 不写入")
        return meta_dict

    add(meta_dict)
    return meta_dict


def process_dir(dir_path, dry_run=False):
    """批量处理目录下所有PDF"""
    d = Path(dir_path)
    pdfs = list(d.glob("*.pdf"))
    print(f"发现 {len(pdfs)} 个PDF文件")
    results = []
    for p in pdfs:
        r = process_pdf(str(p), dry_run=dry_run)
        if r:
            results.append(r)
    print(f"\n入库完成: {len(results)}/{len(pdfs)} 个")
    return results


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="PDF→GNN论文库自动入库")
    parser.add_argument("path", help="PDF文件或目录路径")
    parser.add_argument("--dry", action="store_true", help="仅预览不写入")
    args = parser.parse_args()

    p = Path(args.path)
    if p.is_dir():
        process_dir(args.path, dry_run=args.dry)
    else:
        process_pdf(args.path, dry_run=args.dry)
