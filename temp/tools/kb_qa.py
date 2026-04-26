"""知识库智能问答与FAQ生成工具"""
import os
import sys
import json
import re
from pathlib import Path
from collections import Counter

# 导入语义搜索
sys.path.append("./teaching_kb")
from semantic_search import SemanticSearch

class KnowledgeBaseQA:
    """知识库问答系统"""
    def __init__(self, kb_path="./teaching_kb"):
        self.kb_path = kb_path
        self.searcher = SemanticSearch(kb_path)
        self.searcher.build_index()
    
    def answer_question(self, question, top_k=3, context_lines=5):
        """回答问题，返回相关内容片段"""
        results = self.searcher.search(question, top_k=top_k)
        answers = []
        for r in results:
            # 读取文件内容
            try:
                with open(r["path"], "r", encoding="utf-8") as f:
                    content = f.read()
                # 提取相关段落
                paragraphs = [p.strip() for p in content.split("\n\n") if p.strip()]
                relevant = [p for p in paragraphs if any(w in p for w in question.split())][:context_lines]
                answers.append({
                    "source": r["title"],
                    "score": r["score"],
                    "content": "\n\n".join(relevant) if relevant else paragraphs[0] if paragraphs else ""
                })
            except Exception as e:
                continue
        return answers
    
    def batch_answer(self, questions):
        """批量回答问题"""
        return {q: self.answer_question(q) for q in questions}

class FAQGenerator:
    """FAQ自动生成器"""
    def __init__(self, kb_path="./teaching_kb"):
        self.kb_path = kb_path
        self.searcher = SemanticSearch(kb_path)
        self.searcher.build_index()
    
    def extract_key_concepts(self, top_n=20):
        """提取关键概念（基于词频）"""
        all_text = []
        for doc in self.searcher.documents:
            all_text.append(doc["content"])
        
        # 简单词频统计（过滤停用词）
        stopwords = {"的", "是", "在", "和", "了", "有", "与", "等", "为", "中", "及"}
        words = []
        for text in all_text:
            words.extend([w for w in text if len(w) > 1 and w not in stopwords])
        
        return [w for w, _ in Counter(words).most_common(top_n)]
    
    def generate_faq(self, concepts=None, questions_per_concept=2):
        """生成FAQ列表"""
        if concepts is None:
            concepts = self.extract_key_concepts(10)
        
        faq = []
        for concept in concepts:
            # 为每个概念生成问题模板
            templates = [
                f"什么是{concept}？",
                f"{concept}有什么作用？",
                f"如何理解{concept}？",
                f"{concept}的应用场景有哪些？"
            ]
            
            for template in templates[:questions_per_concept]:
                # 搜索相关内容作为答案
                results = self.searcher.search(concept, top_k=1)
                if results:
                    try:
                        with open(results[0]["path"], "r", encoding="utf-8") as f:
                            content = f.read()
                        # 提取包含概念的段落
                        paragraphs = [p.strip() for p in content.split("\n\n") if concept in p]
                        answer = paragraphs[0] if paragraphs else content[:200]
                        faq.append({"question": template, "answer": answer, "source": results[0]["title"]})
                    except:
                        continue
        return faq
    
    def save_faq(self, faq, output_path="./faq.md"):
        """保存FAQ到Markdown文件"""
        lines = ["# 常见问题解答 (FAQ)\n"]
        for i, item in enumerate(faq, 1):
            lines.append(f"## {i}. {item['question']}\n")
            lines.append(f"{item['answer']}\n")
            lines.append(f"*来源: {item['source']}*\n")
        
        with open(output_path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
        return output_path

# 便捷函数
def quick_answer(question, kb_path="./teaching_kb"):
    """快速问答"""
    qa = KnowledgeBaseQA(kb_path)
    return qa.answer_question(question)

def quick_faq(output_path="./faq.md", kb_path="./teaching_kb"):
    """快速生成FAQ"""
    gen = FAQGenerator(kb_path)
    faq = gen.generate_faq()
    return gen.save_faq(faq, output_path)

if __name__ == "__main__":
    # 测试问答
    print("=== 测试问答功能 ===")
    qa = KnowledgeBaseQA()
    answers = qa.answer_question("图神经网络")
    for ans in answers:
        print(f"[{ans['score']:.3f}] {ans['source']}")
        print(ans['content'][:100])
    
    # 测试FAQ生成
    print("\n=== 测试FAQ生成 ===")
    gen = FAQGenerator()
    concepts = gen.extract_key_concepts(5)
    print(f"关键概念: {concepts}")
    faq = gen.generate_faq(concepts, questions_per_concept=1)
    print(f"生成FAQ: {len(faq)}条")
    output = gen.save_faq(faq, "./test_faq.md")
    print(f"保存到: {output}")