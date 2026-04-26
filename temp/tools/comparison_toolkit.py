"""
论文对比分析工具
支持从GNN论文库中提取多篇论文进行多维度对比分析
"""
import re
from typing import List, Dict, Optional


def parse_papers(papers_file: str = "../gnn_papers/PAPERS.md") -> List[Dict]:
    """解析论文库文件，返回论文列表"""
    with open(papers_file, "r", encoding="utf-8") as f:
        content = f.read()
    
    papers = []
    blocks = re.split(r"\n---\n", content)
    
    for block in blocks[1:]:  # 跳过文件头
        if not block.strip():
            continue
        
        paper = {}
        lines = block.split("\n")
        current_key = None
        current_value = []
        
        for line in lines:
            # 匹配键值对
            match = re.match(r"^([a-z_]+):\s*(.*)$", line)
            if match:
                # 保存上一个键值
                if current_key:
                    paper[current_key] = "\n".join(current_value).strip()
                
                current_key = match.group(1)
                value = match.group(2).strip()
                # 处理引号
                if value.startswith('"') and value.endswith('"'):
                    value = value[1:-1]
                elif value.startswith(">"):  # 多行值
                    current_value = []
                    continue
                current_value = [value]
            elif current_key and line.strip():
                # 多行值的延续
                current_value.append(line.strip())
        
        # 保存最后一个键值
        if current_key:
            paper[current_key] = "\n".join(current_value).strip()
        
        if paper:
            papers.append(paper)
    
    return papers


def get_paper_by_id(paper_id: str, papers: Optional[List[Dict]] = None) -> Optional[Dict]:
    """根据ID获取论文"""
    if papers is None:
        papers = parse_papers()
    
    for paper in papers:
        if paper.get("id") == paper_id:
            return paper
    return None


def compare_papers(paper_ids: List[str], dimensions: Optional[List[str]] = None) -> str:
    """
    对比多篇论文
    
    Args:
        paper_ids: 论文ID列表
        dimensions: 对比维度列表，默认为常用维度
    
    Returns:
        markdown格式的对比表
    """
    if dimensions is None:
        dimensions = ["title", "year", "venue", "keywords", "summary", "code_url"]
    
    papers = parse_papers()
    selected_papers = [get_paper_by_id(pid, papers) for pid in paper_ids]
    
    # 过滤None
    selected_papers = [p for p in selected_papers if p is not None]
    
    if not selected_papers:
        return "未找到指定论文"
    
    # 生成表格
    table_lines = []
    
    # 表头
    header = "| 维度 | " + " | ".join([p.get("id", "Unknown") for p in selected_papers]) + " |"
    separator = "|------|" + "|".join(["------" for _ in selected_papers]) + "|"
    table_lines.append(header)
    table_lines.append(separator)
    
    # 维度映射（中文显示）
    dim_names = {
        "title": "标题",
        "year": "年份",
        "venue": "发表会议/期刊",
        "keywords": "关键词",
        "summary": "摘要",
        "code_url": "代码链接",
        "arxiv": "arXiv编号",
        "authors": "作者",
        "relevance": "教学相关性",
        "applications": "应用场景"
    }
    
    # 数据行
    for dim in dimensions:
        dim_display = dim_names.get(dim, dim)
        row = f"| **{dim_display}** |"
        
        for paper in selected_papers:
            value = paper.get(dim, "N/A")
            # 处理列表格式的keywords
            if dim == "keywords" and isinstance(value, str) and value.startswith("["):
                value = value.strip("[]").replace('"', "").replace("'", "")
            # 截断过长文本
            if len(value) > 150:
                value = value[:150] + "..."
            # 转义markdown特殊字符
            value = value.replace("|", "\|").replace("\n", " ")
            row += f" {value} |"
        
        table_lines.append(row)
    
    return "\n".join(table_lines)


def list_papers() -> str:
    """列出所有论文的ID和标题"""
    papers = parse_papers()
    lines = ["# 论文库列表\n"]
    for i, paper in enumerate(papers, 1):
        pid = paper.get("id", "Unknown")
        title = paper.get("title", "No title")
        year = paper.get("year", "N/A")
        lines.append(f"{i}. **{pid}** ({year}): {title}")
    return "\n".join(lines)


if __name__ == "__main__":
    # 测试：对比GCN和GAT
    print("=== 测试：对比GCN2017和GAT2018 ===\n")
    result = compare_papers(["GCN2017", "GAT2018"])
    print(result)
    print("\n\n=== 论文库列表 ===\n")
    print(list_papers())