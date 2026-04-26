#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
技能去重验证工具
用于在生成新任务前，强制检查是否与现有技能重复
"""
import json
import sys
from pathlib import Path
from difflib import SequenceMatcher

class DedupChecker:
    def __init__(self, skill_tree_path=None):
        if skill_tree_path is None:
            base = Path(__file__).parent.parent
            skill_tree_path = base / "temp" / "skill_tree" / "skill_tree.json"
        
        with open(skill_tree_path, 'r', encoding='utf-8') as f:
            self.tree = json.load(f)
        
        self.categories = self.tree['skill_categories']
        
    def extract_all_skills(self):
        """提取所有技能的详细信息"""
        all_skills = []
        for cat_name, skills in self.categories.items():
            for skill_name, skill_info in skills.items():
                all_skills.append({
                    'category': cat_name,
                    'skill_name': skill_name,
                    'sop': skill_info.get('sop', ''),
                    'tools': skill_info.get('tools', []),
                    'functions': skill_info.get('functions', []),
                    'usage_count': skill_info.get('usage_count', 0),
                    'last_used': skill_info.get('last_used', '')
                })
        return all_skills
    
    def similarity(self, a, b):
        """计算两个字符串的相似度"""
        return SequenceMatcher(None, a.lower(), b.lower()).ratio()
    
    def search_similar(self, keywords, threshold=0.3):
        """根据关键词搜索相似的技能"""
        all_skills = self.extract_all_skills()
        results = []
        
        for skill in all_skills:
            # 计算与技能名的相似度
            name_sim = max([self.similarity(kw, skill['skill_name']) for kw in keywords])
            
            # 计算与类别名的相似度
            cat_sim = max([self.similarity(kw, skill['category']) for kw in keywords])
            
            # 计算与工具名的相似度
            tool_sim = 0
            if skill['tools']:
                tool_sim = max([
                    max([self.similarity(kw, tool) for kw in keywords])
                    for tool in skill['tools']
                ], default=0)
            
            # 计算与SOP的相似度
            sop_sim = max([self.similarity(kw, skill['sop']) for kw in keywords]) if skill['sop'] else 0
            
            max_sim = max(name_sim, cat_sim, tool_sim, sop_sim)
            
            if max_sim >= threshold:
                results.append({
                    'skill': skill,
                    'similarity': max_sim,
                    'match_type': 'name' if name_sim == max_sim else 
                                 'category' if cat_sim == max_sim else
                                 'tool' if tool_sim == max_sim else 'sop'
                })
        
        # 按相似度排序
        results.sort(key=lambda x: x['similarity'], reverse=True)
        return results
    
    def check_task(self, task_description):
        """检查单个任务是否重复"""
        # 提取关键词（简单分词）
        keywords = [w.strip() for w in task_description.lower().replace('|', ' ').split() if len(w.strip()) > 2]
        
        print(f"\n{'='*80}")
        print(f"检查任务: {task_description}")
        print(f"提取关键词: {keywords}")
        print(f"{'='*80}")
        
        results = self.search_similar(keywords, threshold=0.25)
        
        if not results:
            print("✅ 未发现相似技能，可以添加")
            return True
        
        print(f"\n⚠️  发现 {len(results)} 个相似技能:")
        for i, r in enumerate(results[:10], 1):  # 只显示前10个
            skill = r['skill']
            print(f"\n{i}. [{skill['category']}] {skill['skill_name']}")
            print(f"   相似度: {r['similarity']:.2%} (匹配类型: {r['match_type']})")
            print(f"   SOP: {skill['sop']}")
            print(f"   工具: {', '.join(skill['tools'][:3])}{'...' if len(skill['tools']) > 3 else ''}")
            print(f"   使用次数: {skill['usage_count']} | 最后使用: {skill['last_used']}")
        
        return False
    
    def batch_check(self, tasks):
        """批量检查任务列表"""
        print(f"\n{'#'*80}")
        print(f"开始批量去重验证 - 共 {len(tasks)} 个任务")
        print(f"{'#'*80}")
        
        results = []
        for task in tasks:
            is_unique = self.check_task(task)
            results.append({'task': task, 'is_unique': is_unique})
        
        print(f"\n{'#'*80}")
        print(f"去重验证完成")
        print(f"{'#'*80}")
        print(f"\n总结:")
        unique_count = sum(1 for r in results if r['is_unique'])
        print(f"  - 可添加任务: {unique_count}/{len(tasks)}")
        print(f"  - 疑似重复任务: {len(tasks) - unique_count}/{len(tasks)}")
        
        if unique_count < len(tasks):
            print(f"\n⚠️  建议:")
            for r in results:
                if not r['is_unique']:
                    print(f"  - 重新审视: {r['task']}")
        
        return results

def main():
    """命令行入口"""
    if len(sys.argv) < 2:
        print("用法: python dedup_checker.py <任务描述1> [任务描述2] ...")
        print("示例: python dedup_checker.py 'PPT图表生成' '视频字幕处理'")
        sys.exit(1)
    
    checker = DedupChecker()
    tasks = sys.argv[1:]
    checker.batch_check(tasks)

if __name__ == '__main__':
    main()
