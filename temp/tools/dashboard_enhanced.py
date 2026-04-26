"""自媒体数据分析看板增强"""
import json
from typing import Dict, List, Optional
from datetime import datetime, timedelta

class DashboardAnalyzer:
    """多维度数据分析器"""
    def __init__(self, data: List[Dict]):
        self.data = data
    
    def platform_comparison(self, platforms: List[str], metric: str = "views") -> Dict:
        """平台对比分析"""
        result = {}
        for platform in platforms:
            platform_data = [d for d in self.data if d.get("platform") == platform]
            total = sum(d.get(metric, 0) for d in platform_data)
            avg = total / len(platform_data) if platform_data else 0
            result[platform] = {"total": total, "average": avg, "count": len(platform_data)}
        return result
    
    def time_trend_analysis(self, metric: str = "views", period: str = "day") -> Dict:
        """时间趋势分析"""
        from collections import defaultdict
        trends = defaultdict(int)
        for d in self.data:
            date_str = d.get("date", "")
            if date_str:
                if period == "day":
                    key = date_str
                elif period == "week":
                    dt = datetime.strptime(date_str, "%Y-%m-%d")
                    key = f"{dt.year}-W{dt.isocalendar()[1]}"
                elif period == "month":
                    key = date_str[:7]
                trends[key] += d.get(metric, 0)
        return dict(sorted(trends.items()))
    
    def content_type_analysis(self, metric: str = "views") -> Dict:
        """内容类型分析"""
        from collections import defaultdict
        types = defaultdict(lambda: {"total": 0, "count": 0})
        for d in self.data:
            ctype = d.get("content_type", "unknown")
            types[ctype]["total"] += d.get(metric, 0)
            types[ctype]["count"] += 1
        for t in types:
            types[t]["average"] = types[t]["total"] / types[t]["count"]
        return dict(types)

class AdvancedVisualizer:
    """高级可视化工具"""
    @staticmethod
    def create_heatmap(data: Dict, output_path: str, title: str = "热力图"):
        """创建热力图数据"""
        heatmap_data = {"type": "heatmap", "title": title, "data": data, "output": output_path}
        with open(output_path.replace(".png", ".json"), "w", encoding="utf-8") as f:
            json.dump(heatmap_data, f, ensure_ascii=False, indent=2)
        return output_path
    
    @staticmethod
    def create_pie_chart(data: Dict[str, float], output_path: str, title: str = "饼图"):
        """创建饼图数据"""
        pie_data = {"type": "pie", "title": title, "data": data, "output": output_path}
        with open(output_path.replace(".png", ".json"), "w", encoding="utf-8") as f:
            json.dump(pie_data, f, ensure_ascii=False, indent=2)
        return output_path
    
    @staticmethod
    def create_multi_line(data: Dict[str, List], output_path: str, title: str = "多线图"):
        """创建多线图数据"""
        line_data = {"type": "multi_line", "title": title, "data": data, "output": output_path}
        with open(output_path.replace(".png", ".json"), "w", encoding="utf-8") as f:
            json.dump(line_data, f, ensure_ascii=False, indent=2)
        return output_path

class TrendPredictor:
    """趋势预测器"""
    @staticmethod
    def predict_trend(historical_data: List[float], periods: int = 7) -> List[float]:
        """基于历史数据预测趋势（简单移动平均）"""
        if len(historical_data) < 3:
            return [historical_data[-1]] * periods if historical_data else [0] * periods
        window = min(7, len(historical_data))
        recent_avg = sum(historical_data[-window:]) / window
        growth = (historical_data[-1] - historical_data[0]) / len(historical_data) if len(historical_data) >= 2 else 0
        predictions = [max(0, recent_avg + growth * (i + 1)) for i in range(periods)]
        return predictions
    
    @staticmethod
    def calculate_trend_score(data: List[float]) -> str:
        """计算趋势评分"""
        if len(data) < 2:
            return "insufficient_data"
        growth = (data[-1] - data[0]) / data[0] if data[0] > 0 else 0
        if growth > 0.2: return "strong_growth"
        elif growth > 0.05: return "moderate_growth"
        elif growth > -0.05: return "stable"
        elif growth > -0.2: return "moderate_decline"
        else: return "strong_decline"

class ReportGenerator:
    """报告生成器"""
    @staticmethod
    def generate_html_report(analysis_results: Dict, output_path: str) -> str:
        """生成HTML报告"""
        html_content = """<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>数据分析报告</title>
<style>body{font-family:Arial;margin:20px}h1{color:#333}.section{margin:20px 0;padding:15px;border:1px solid #ddd}</style>
</head><body><h1>自媒体数据分析报告</h1>
<div class="section"><h2>生成时间</h2><p>""" + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + """</p></div>
<div class="section"><h2>分析结果</h2><pre>""" + json.dumps(analysis_results, ensure_ascii=False, indent=2) + """</pre></div>
</body></html>"""
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html_content)
        return output_path
    
    @staticmethod
    def generate_dashboard(data: List[Dict], output_dir: str = "./dashboard") -> Dict:
        """生成综合看板"""
        import os
        os.makedirs(output_dir, exist_ok=True)
        analyzer = DashboardAnalyzer(data)
        visualizer = AdvancedVisualizer()
        results = {
            "platform_comparison": analyzer.platform_comparison(["wechat", "zhihu", "xiaohongshu"]),
            "time_trend": analyzer.time_trend_analysis(),
            "content_type": analyzer.content_type_analysis(),
            "charts": []
        }
        pie_path = os.path.join(output_dir, "content_type_pie.png")
        visualizer.create_pie_chart({k: v["total"] for k, v in results["content_type"].items()}, pie_path, "内容类型分布")
        results["charts"].append(pie_path)
        html_path = os.path.join(output_dir, "dashboard.html")
        ReportGenerator.generate_html_report(results, html_path)
        results["html_report"] = html_path
        return results

def quick_dashboard(data: List[Dict], output_dir: str = "./dashboard") -> Dict:
    """快速生成看板"""
    return ReportGenerator.generate_dashboard(data, output_dir)

def quick_predict(historical_data: List[float], periods: int = 7) -> Dict:
    """快速趋势预测"""
    predictor = TrendPredictor()
    predictions = predictor.predict_trend(historical_data, periods)
    trend_score = predictor.calculate_trend_score(historical_data)
    return {"predictions": predictions, "trend_score": trend_score, "historical_avg": sum(historical_data) / len(historical_data) if historical_data else 0}

if __name__ == "__main__":
    print("数据分析看板增强工具")
    print("1. 多维度分析: DashboardAnalyzer")
    print("2. 高级可视化: AdvancedVisualizer")
    print("3. 趋势预测: TrendPredictor")
    print("4. 报告生成: ReportGenerator")