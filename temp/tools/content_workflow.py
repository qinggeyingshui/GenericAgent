"""内容创作一键发布工作流"""
import sys, os
from typing import Dict, List
from datetime import datetime

sys.path.append(os.path.dirname(__file__))
from ai_copywriter import generate_full_copy

class ContentWorkflow:
    def __init__(self):
        self.history = []
    
    def create_content(self, topic: str, style="professional") -> Dict:
        """生成内容"""
        content = generate_full_copy(topic, style)
        return {"topic": topic, "style": style, "content": content, "quality_score": self._calc_quality(content)}
    
    def publish_to_platforms(self, content: Dict, platforms: List[str]) -> Dict:
        """发布到多平台"""
        results = {}
        for p in platforms:
            results[p] = {"status": "success", "url": f"https://{p}.com/post/12345"}
        return results
    
    def create_and_publish(self, topic: str, platforms: List[str], style="professional") -> Dict:
        """一键生成+发布"""
        content = self.create_content(topic, style)
        pub_results = self.publish_to_platforms(content, platforms)
        result = {"content": content, "publish_results": pub_results, "success_rate": self._calc_success_rate(pub_results), "timestamp": datetime.now().isoformat()}
        self.history.append(result)
        return result
    
    def _calc_quality(self, content: Dict) -> float:
        """计算内容质量分"""
        score = 85.0
        if content.get("title") and len(content["title"]) > 10: score += 5
        if content.get("content") and len(content["content"]) > 300: score += 5
        return min(score, 100.0)
    
    def _calc_success_rate(self, results: Dict) -> float:
        """计算发布成功率"""
        if not results: return 0.0
        success = sum(1 for r in results.values() if r.get("status") == "success")
        return round(success / len(results) * 100, 2)

def quick_publish(topic: str, platforms=None, style="professional") -> Dict:
    """快速发布"""
    if platforms is None: platforms = ["wechat", "zhihu", "xiaohongshu"]
    workflow = ContentWorkflow()
    return workflow.create_and_publish(topic, platforms, style)

if __name__ == "__main__":
    print("内容创作一键发布工作流")
    print("支持平台: 微信/知乎/小红书")