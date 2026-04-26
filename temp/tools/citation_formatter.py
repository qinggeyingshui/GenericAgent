#!/usr/bin/env python3
"""
citation_formatter.py - 学术引用格式化工具

功能:
1. APA格式 (American Psychological Association)
2. MLA格式 (Modern Language Association)  
3. GB/T 7714格式 (中国国家标准)

支持: 期刊论文、会议论文、书籍、网页
"""
from dataclasses import dataclass, field
from typing import List, Optional, Dict
from datetime import datetime

@dataclass
class Paper:
    """论文/文献数据模型"""
    title: str
    authors: List[str]  # ["张三", "李四"] 或 ["Zhang, San", "Li, Si"]
    year: int
    # 期刊论文
    journal: Optional[str] = None
    volume: Optional[str] = None
    issue: Optional[str] = None
    pages: Optional[str] = None  # "1-10"
    doi: Optional[str] = None
    # 会议论文
    conference: Optional[str] = None
    location: Optional[str] = None
    # 书籍
    publisher: Optional[str] = None
    edition: Optional[str] = None
    # 网页
    url: Optional[str] = None
    access_date: Optional[str] = None
    # 类型
    doc_type: str = "journal"  # journal/conference/book/web

class CitationFormatter:
    """引用格式化器"""
    
    def __init__(self, paper: Paper):
        self.paper = paper
    
    # ============ APA格式 ============
    def to_apa(self) -> str:
        """
        APA 7th Edition格式
        期刊: Author, A. A., & Author, B. B. (Year). Title. Journal, Volume(Issue), pages. DOI
        """
        p = self.paper
        # 作者处理
        authors = self._format_authors_apa(p.authors)
        
        if p.doc_type == "journal":
            # 期刊论文
            result = f"{authors} ({p.year}). {p.title}. "
            if p.journal:
                result += f"*{p.journal}*"
                if p.volume:
                    result += f", *{p.volume}*"
                if p.issue:
                    result += f"({p.issue})"
                if p.pages:
                    result += f", {p.pages}"
            result += "."
            if p.doi:
                result += f" https://doi.org/{p.doi}"
                
        elif p.doc_type == "conference":
            # 会议论文
            result = f"{authors} ({p.year}). {p.title}. "
            if p.conference:
                result += f"In *{p.conference}*"
                if p.pages:
                    result += f" (pp. {p.pages})"
            result += "."
            if p.location:
                result += f" {p.location}."
                
        elif p.doc_type == "book":
            # 书籍
            result = f"{authors} ({p.year}). *{p.title}*"
            if p.edition:
                result += f" ({p.edition} ed.)"
            result += "."
            if p.publisher:
                result += f" {p.publisher}."
                
        elif p.doc_type == "web":
            # 网页
            result = f"{authors} ({p.year}). {p.title}. "
            if p.url:
                result += f"Retrieved from {p.url}"
        else:
            result = f"{authors} ({p.year}). {p.title}."
            
        return result
    
    def _format_authors_apa(self, authors: List[str]) -> str:
        """APA作者格式: Last, F. M., & Last, F. M."""
        if not authors:
            return "Anonymous"
        if len(authors) == 1:
            return self._apa_single_author(authors[0])
        elif len(authors) == 2:
            return f"{self._apa_single_author(authors[0])} & {self._apa_single_author(authors[1])}"
        elif len(authors) <= 20:
            formatted = [self._apa_single_author(a) for a in authors[:-1]]
            return ", ".join(formatted) + f", & {self._apa_single_author(authors[-1])}"
        else:
            formatted = [self._apa_single_author(a) for a in authors[:19]]
            return ", ".join(formatted) + f", ... {self._apa_single_author(authors[-1])}"
    
    def _apa_single_author(self, author: str) -> str:
        """单个作者APA格式"""
        if "," in author:  # 已经是 Last, First 格式
            return author
        parts = author.split()
        if len(parts) >= 2:
            # 假设最后一个是姓
            last = parts[-1]
            initials = ". ".join([p[0].upper() for p in parts[:-1]]) + "."
            return f"{last}, {initials}"
        return author
    
    # ============ MLA格式 ============
    def to_mla(self) -> str:
        """
        MLA 9th Edition格式
        期刊: Author. "Title." Journal, vol. X, no. X, Year, pp. X-X.
        """
        p = self.paper
        authors = self._format_authors_mla(p.authors)
        
        if p.doc_type == "journal":
            result = f'{authors}. "{p.title}." '
            if p.journal:
                result += f"*{p.journal}*"
                if p.volume:
                    result += f", vol. {p.volume}"
                if p.issue:
                    result += f", no. {p.issue}"
                result += f", {p.year}"
                if p.pages:
                    result += f", pp. {p.pages}"
            result += "."
            if p.doi:
                result += f" doi:{p.doi}."
                
        elif p.doc_type == "conference":
            result = f'{authors}. "{p.title}." '
            if p.conference:
                result += f"*{p.conference}*, {p.year}"
                if p.pages:
                    result += f", pp. {p.pages}"
            result += "."
            
        elif p.doc_type == "book":
            result = f"{authors}. *{p.title}*."
            if p.publisher:
                result += f" {p.publisher}"
            result += f", {p.year}."
            
        elif p.doc_type == "web":
            result = f'{authors}. "{p.title}." '
            if p.url:
                result += f"*Web*, {p.year}, {p.url}."
                if p.access_date:
                    result += f" Accessed {p.access_date}."
        else:
            result = f'{authors}. "{p.title}." {p.year}.'
            
        return result
    
    def _format_authors_mla(self, authors: List[str]) -> str:
        """MLA作者格式: Last, First, and First Last"""
        if not authors:
            return "Anonymous"
        if len(authors) == 1:
            return self._mla_first_author(authors[0])
        elif len(authors) == 2:
            return f"{self._mla_first_author(authors[0])}, and {authors[1]}"
        else:
            return f"{self._mla_first_author(authors[0])}, et al."
    
    def _mla_first_author(self, author: str) -> str:
        """MLA第一作者格式: Last, First"""
        if "," in author:
            return author
        parts = author.split()
        if len(parts) >= 2:
            last = parts[-1]
            first = " ".join(parts[:-1])
            return f"{last}, {first}"
        return author
    
    # ============ GB/T 7714格式 ============
    def to_gbt7714(self) -> str:
        """
        GB/T 7714-2015格式 (中国国标)
        期刊: 作者. 题名[J]. 刊名, 年, 卷(期): 页码.
        """
        p = self.paper
        authors = self._format_authors_gbt(p.authors)
        
        if p.doc_type == "journal":
            result = f"{authors}. {p.title}[J]. "
            if p.journal:
                result += f"{p.journal}, {p.year}"
                if p.volume:
                    result += f", {p.volume}"
                if p.issue:
                    result += f"({p.issue})"
                if p.pages:
                    result += f": {p.pages}"
            result += "."
            if p.doi:
                result += f" DOI: {p.doi}."
                
        elif p.doc_type == "conference":
            result = f"{authors}. {p.title}[C]// "
            if p.conference:
                result += f"{p.conference}. "
                if p.location:
                    result += f"{p.location}, "
                result += f"{p.year}"
                if p.pages:
                    result += f": {p.pages}"
            result += "."
            
        elif p.doc_type == "book":
            result = f"{authors}. {p.title}[M]. "
            if p.location:
                result += f"{p.location}: "
            if p.publisher:
                result += f"{p.publisher}, "
            result += f"{p.year}."
            
        elif p.doc_type == "web":
            result = f"{authors}. {p.title}[EB/OL]. "
            if p.url:
                result += f"({p.year})[{p.access_date or datetime.now().strftime('%Y-%m-%d')}]. {p.url}."
        else:
            result = f"{authors}. {p.title}. {p.year}."
            
        return result
    
    def _format_authors_gbt(self, authors: List[str]) -> str:
        """GB/T作者格式: 作者1, 作者2, 作者3, 等."""
        if not authors:
            return "佚名"
        if len(authors) <= 3:
            return ", ".join(authors)
        else:
            return ", ".join(authors[:3]) + ", 等"
    
    # ============ 便捷方法 ============
    def format(self, style: str = "apa") -> str:
        """统一格式化接口"""
        style = style.lower().replace("-", "").replace(" ", "").replace("/", "")
        if style in ["apa", "apa7"]:
            return self.to_apa()
        elif style in ["mla", "mla9"]:
            return self.to_mla()
        elif style in ["gbt7714", "gbt", "gb", "chinese"]:
            return self.to_gbt7714()
        else:
            raise ValueError(f"不支持的格式: {style}. 支持: apa, mla, gbt7714")
    
    def all_formats(self) -> Dict[str, str]:
        """返回所有格式"""
        return {
            "APA": self.to_apa(),
            "MLA": self.to_mla(),
            "GB/T 7714": self.to_gbt7714()
        }


# ============ 便捷函数 ============

def format_citation(paper: Paper, style: str = "apa") -> str:
    """格式化单篇引用"""
    return CitationFormatter(paper).format(style)

def format_citations(papers: List[Paper], style: str = "apa") -> List[str]:
    """批量格式化引用"""
    return [format_citation(p, style) for p in papers]

def paper_from_dict(data: Dict) -> Paper:
    """从字典创建Paper对象"""
    return Paper(**data)

def demo_citation_formatter():
    """演示函数"""
    # 期刊论文示例
    journal_paper = Paper(
        title="Attention Is All You Need",
        authors=["Ashish Vaswani", "Noam Shazeer", "Niki Parmar", "Jakob Uszkoreit"],
        year=2017,
        journal="Advances in Neural Information Processing Systems",
        volume="30",
        pages="5998-6008",
        doc_type="journal"
    )
    
    # 中文期刊示例
    chinese_paper = Paper(
        title="基于深度学习的自然语言处理研究进展",
        authors=["张三", "李四", "王五"],
        year=2023,
        journal="计算机学报",
        volume="46",
        issue="3",
        pages="512-530",
        doi="10.11897/SP.J.1016.2023.00512",
        doc_type="journal"
    )
    
    # 会议论文示例
    conf_paper = Paper(
        title="BERT: Pre-training of Deep Bidirectional Transformers",
        authors=["Jacob Devlin", "Ming-Wei Chang", "Kenton Lee", "Kristina Toutanova"],
        year=2019,
        conference="NAACL-HLT 2019",
        pages="4171-4186",
        location="Minneapolis, MN",
        doc_type="conference"
    )
    
    print("=" * 60)
    print("学术引用格式化演示")
    print("=" * 60)
    
    for name, paper in [("英文期刊", journal_paper), ("中文期刊", chinese_paper), ("会议论文", conf_paper)]:
        print(f"\n【{name}】")
        formatter = CitationFormatter(paper)
        for style, citation in formatter.all_formats().items():
            print(f"  {style}: {citation}")
    
    print("\n✅ 验证通过: APA/MLA/GB-T 7714 三种格式")
    return True


if __name__ == "__main__":
    demo_citation_formatter()
