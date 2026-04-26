"""
自主学习引擎
整合: skill_tree + multi_platform_search + 实验验证
流程: 选题 → 搜索 → 学习 → 实验 → 更新
"""

import sys
import json
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent))

from skill_tree_api import SkillTree
from multi_platform_search import MultiPlatformSearch


class LearningEngine:
    """自主学习引擎"""
    
    def __init__(self, tree_path: str = "./skill_tree.json"):
        self.skill_tree = SkillTree(tree_path)
        self.searcher = MultiPlatformSearch()
        self.learning_history = []  # 学习历史
        self.experiments = []  # 实验记录
    
    def select_learning_topic(self, strategy: str = "explore") -> Optional[Dict]:
        """
        选择学习主题（v2.1 - 移除gaps依赖）
        
        Args:
            strategy: 选择策略
                - "explore": 探索新领域（默认，基于动态推荐）
                - "high_priority": 高优先级任务
        
        Returns:
            {"skill": str, "category": str, "priority": float, "suggested_task": str}
        """
        # 使用推荐系统（基于动态等级计算）
        recommendations = self.skill_tree.recommend_tasks(count=5)
        
        if not recommendations:
            return None
        
        # 根据策略选择
        if strategy == "high_priority":
            # 选择score最高的
            top_rec = recommendations[0]
        else:  # explore
            # 选择第一个推荐
            top_rec = recommendations[0]
        
        return {
            "skill": top_rec.get("skill", "unknown"),
            "category": top_rec.get("category", "unknown"),
            "priority": top_rec["score"],
            "strategy": strategy,
            "suggested_task": top_rec.get("suggested_task", "")
        }
    
    def learn(self, topic: Dict, max_resources: int = 3) -> Dict:
        """
        执行学习循环
        
        Args:
            topic: select_learning_topic()返回的主题
            max_resources: 最多获取资源数
        
        Returns:
            学习报告（包含搜索结果和完整内容）
        """
        skill_name = topic["skill"]
        print(f"\n🎯 开始学习: {skill_name}")
        
        # 1. 构建搜索查询
        search_queries = [
            f"{skill_name} 教程",
            f"{skill_name} 实战案例",
            f"{skill_name} 最佳实践"
        ]
        print(f"📚 搜索查询: {search_queries[:2]}")
        
        # 2. 多平台搜索并获取内容
        print(f"🔍 搜索资源...")
        all_resources = []
        
        for query in search_queries[:2]:  # 只用前2个查询
            try:
                # 使用search_and_fetch获取完整内容
                result = self.searcher.search_and_fetch(
                    query=query,
                    platforms=["zhihu", "csdn"],  # 优先知乎和CSDN
                    fetch_top_n=2  # 每个查询获取2个
                )
                all_resources.extend(result["results"])
            except Exception as e:
                print(f"[警告] 查询'{query}'失败: {e}")
        
        # 3. 限制资源数量
        all_resources = all_resources[:max_resources]
        
        # 4. 生成学习报告
        report = {
            "skill": skill_name,
            "category": topic.get("category"),
            "timestamp": datetime.now().isoformat(),
            "search_queries": search_queries[:2],
            "resources": all_resources,
            "resource_count": len(all_resources),
            "status": "resources_fetched",
            "next_steps": [
                "1. 分析resources中的content字段",
                "2. 提取代码示例和关键概念",
                "3. 在temp/experiments/下编写测试代码",
                "4. 验证成功后调用update_skill_tree()"
            ]
        }
        
        self.learning_history.append(report)
        return report
    
    def experiment(self, skill_name: str, code: str, description: str = "") -> Dict:
        """
        记录实验
        
        Args:
            skill_name: 技能名称
            code: 实验代码
            description: 实验描述
        
        Returns:
            实验记录
        """
        experiment = {
            "skill": skill_name,
            "timestamp": datetime.now().isoformat(),
            "description": description,
            "code": code,
            "status": "pending"  # pending/success/failed
        }
        self.experiments.append(experiment)
        return experiment
    
    def update_skill_tree(self, category: str, skill_name: str, 
                          report_id: str = None) -> Dict:
        """
        更新技能树（学习成功后）
        
        Args:
            category: 技能类别
            skill_name: 技能名称
            report_id: 学习报告ID（可选）
        
        Returns:
            更新结果字典
        """
        try:
            # 生成报告ID
            if not report_id:
                report_id = f"learn_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            # 使用skill_tree_api的update_skill_usage方法
            success = self.skill_tree.update_skill_usage(category, skill_name, report_id)
            
            if success:
                print(f"✓ 技能树已更新: {skill_name}")
                print(f"  类别: {category}")
                print(f"  报告ID: {report_id}")
                return {
                    "updated": True,
                    "skill": skill_name,
                    "category": category,
                    "report_id": report_id
                }
            else:
                print(f"✗ 更新失败: 技能不存在")
                return {"updated": False, "error": "skill_not_found"}
            
        except Exception as e:
            print(f"✗ 更新失败: {e}")
            return {"updated": False, "error": str(e)}
    
    def run_learning_cycle(self, strategy: str = "gap_first", 
                           max_iterations: int = 1) -> List[Dict]:
        """
        运行完整学习循环
        
        Args:
            strategy: 学习策略
            max_iterations: 最多学习几个主题
        
        Returns:
            学习报告列表
        """
        reports = []
        
        for i in range(max_iterations):
            separator = "=" * 50
            print(f"\n{separator}")
            print(f"学习循环 {i+1}/{max_iterations}")
            print(separator)
            
            # 1. 选择主题
            topic = self.select_learning_topic(strategy)
            if not topic:
                print("✗ 没有可学习的主题")
                break
            
            # 2. 执行学习
            report = self.learn(topic, max_resources=5)
            reports.append(report)
            
            print(f"\n📊 学习报告:")
            skill = report["skill"]
            query_count = len(report["search_queries"])
            url_count = len(report["urls_to_fetch"])
            print(f"  • 技能: {skill}")
            print(f"  • 搜索查询: {query_count} 个")
            print(f"  • 待访问URL: {url_count} 个")
        
        return reports
    
    def save_learning_report(self, output_path: str = "./learning_report.json"):
        """保存学习历史到文件"""
        report = {
            "timestamp": datetime.now().isoformat(),
            "learning_history": self.learning_history,
            "experiments": self.experiments,
            "summary": {
                "total_topics": len(self.learning_history),
                "total_experiments": len(self.experiments)
            }
        }
        
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        return output_path


if __name__ == "__main__":
    # 使用示例
    engine = LearningEngine()
    
    print("=== 自主学习引擎测试 ===")
    print("\n1. 选择学习主题（优先补缺口）")
    topic = engine.select_learning_topic("gap_first")
    if topic:
        skill_name = topic["skill"]
        category = topic["category"]
        gaps = topic.get("gaps", [])
        print(f"   选中: {skill_name}")
        print(f"   类别: {category}")
        print(f"   缺口: {gaps}")
    
    print("\n2. 运行学习循环")
    reports = engine.run_learning_cycle("gap_first", max_iterations=1)
    
    print("\n3. 保存学习报告")
    report_path = engine.save_learning_report("./learning_report.json")
    print(f"   报告已保存: {report_path}")
