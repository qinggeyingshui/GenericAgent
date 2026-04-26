"""SEO优化与关键词分析工具"""
import re
from collections import Counter
from typing import List, Dict, Tuple

class SEOAnalyzer:
    """SEO分析器"""
    def analyze_keyword_density(self, text: str, top_n: int = 10) -> List[Tuple[str, float]]:
        """分析关键词密度"""
        words = re.findall(r"\b[\w]+\b", text.lower())
        stopwords = {"的", "了", "在", "是", "我", "有", "和", "就", "不", "人", "都", "一", "一个", "上", "也", "很", "到", "说", "要", "去", "你", "会", "着", "没有", "看", "好", "自己", "这"}
        words = [w for w in words if w not in stopwords and len(w) > 1]
        total = len(words)
        if total == 0:
            return []
        counter = Counter(words)
        return [(word, count/total*100) for word, count in counter.most_common(top_n)]
    
    def extract_keywords(self, text: str, min_length: int = 2) -> List[str]:
        """提取关键词"""
        words = re.findall(r"\b[\w]+\b", text)
        return list(set([w for w in words if len(w) >= min_length]))

class TitleOptimizer:
    """标题优化器"""
    def score_title(self, title: str) -> Dict[str, any]:
        """评分标题"""
        score = 100
        issues = []
        suggestions = []
        
        length = len(title)
        if length < 10:
            score -= 20
            issues.append("标题过短")
            suggestions.append("建议标题长度10-60字符")
        elif length > 60:
            score -= 15
            issues.append("标题过长")
            suggestions.append("标题超过60字符可能被截断")
        
        if not any(c in title for c in "？！?!"):
            score -= 5
            suggestions.append("可添加疑问或感叹增加吸引力")
        
        if title.isdigit() or title.isalpha():
            score -= 10
            suggestions.append("建议混合使用数字和文字")
        
        return {"score": max(0, score), "length": length, "issues": issues, "suggestions": suggestions}
    
    def optimize_title(self, title: str, keywords: List[str] = None) -> Dict[str, any]:
        """优化标题"""
        result = self.score_title(title)
        optimized = title
        
        if keywords:
            missing = [k for k in keywords if k.lower() not in title.lower()]
            if missing:
                result["suggestions"].append(f"建议添加关键词: {missing[0]}")
        
        result["original"] = title
        result["optimized"] = optimized
        return result

class DescriptionGenerator:
    """描述生成器"""
    def generate_meta_description(self, content: str, max_length: int = 160, keywords: List[str] = None) -> str:
        """生成meta描述"""
        sentences = re.split(r"[。！？.!?]", content)
        sentences = [s.strip() for s in sentences if len(s.strip()) > 10]
        
        if not sentences:
            return content[:max_length]
        
        description = sentences[0]
        
        if keywords:
            for kw in keywords[:2]:
                if kw.lower() not in description.lower() and len(description) + len(kw) + 1 < max_length:
                    description = f"{kw} - {description}"
        
        if len(description) > max_length:
            description = description[:max_length-3] + "..."
        
        return description
    
    def generate_descriptions(self, content: str, count: int = 3) -> List[str]:
        """生成多个描述变体"""
        base = self.generate_meta_description(content)
        variations = [base]
        
        sentences = re.split(r"[。！？.!?]", content)
        sentences = [s.strip() for s in sentences if len(s.strip()) > 10]
        
        for i in range(1, min(count, len(sentences))):
            variations.append(sentences[i][:160])
        
        return variations[:count]

class KeywordResearch:
    """关键词研究（需要浏览器支持）"""
    def __init__(self):
        self.search_engines = ["google", "bing", "baidu"]
    
    def estimate_competition(self, keyword: str) -> str:
        """估算竞争度（基于关键词长度和常见度）"""
        length = len(keyword)
        if length <= 2:
            return "高"
        elif length <= 4:
            return "中"
        else:
            return "低"
    
    def suggest_related_keywords(self, keyword: str) -> List[str]:
        """建议相关关键词（基于简单规则）"""
        suggestions = [
            f"{keyword}教程",
            f"{keyword}方法",
            f"{keyword}技巧",
            f"如何{keyword}",
            f"{keyword}指南"
        ]
        return suggestions

def quick_seo_analysis(text: str, title: str = None) -> Dict[str, any]:
    """快速SEO分析"""
    analyzer = SEOAnalyzer()
    result = {"keywords": analyzer.analyze_keyword_density(text, 5)}
    
    if title:
        optimizer = TitleOptimizer()
        result["title_score"] = optimizer.score_title(title)
    
    generator = DescriptionGenerator()
    result["meta_description"] = generator.generate_meta_description(text)
    
    return result

if __name__ == "__main__":
    text = "人工智能技术正在改变世界。机器学习和深度学习是人工智能的核心技术。"
    title = "人工智能技术入门"
    result = quick_seo_analysis(text, title)
    print("关键词:", result["keywords"])
    print("标题评分:", result["title_score"]["score"])
    print("描述:", result["meta_description"])