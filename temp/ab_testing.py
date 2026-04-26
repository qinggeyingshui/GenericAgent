"""
内容A/B测试框架 - Content A/B Testing Toolkit
支持3类测试：标题/封面/发布时间 + 效果对比报告
"""
import json
from datetime import datetime
from pathlib import Path
from typing import Optional, List
import random
import statistics

# 数据存储
DATA_DIR = Path(__file__).parent / "ab_test_data"
DATA_DIR.mkdir(exist_ok=True)

def _load_tests(platform: str = "default") -> dict:
    """加载测试数据"""
    f = DATA_DIR / f"{platform}_tests.json"
    if f.exists():
        return json.loads(f.read_text(encoding='utf-8'))
    return {"tests": [], "platform": platform}

def _save_tests(data: dict, platform: str = "default"):
    """保存测试数据"""
    f = DATA_DIR / f"{platform}_tests.json"
    f.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')

# ========== 创建测试 ==========

def create_title_test(content_id: str, variants: List[str], platform: str = "default") -> dict:
    """
    创建标题A/B测试
    variants: ["标题A", "标题B", ...]
    """
    data = _load_tests(platform)
    test = {
        "id": f"title_{content_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}",
        "type": "title",
        "content_id": content_id,
        "variants": [{"text": v, "metrics": None} for v in variants],
        "status": "running",
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "winner": None
    }
    data["tests"].append(test)
    _save_tests(data, platform)
    return {"test_id": test["id"], "variants_count": len(variants), "status": "created"}

def create_cover_test(content_id: str, cover_urls: List[str], platform: str = "default") -> dict:
    """
    创建封面A/B测试
    cover_urls: ["url1", "url2", ...]
    """
    data = _load_tests(platform)
    test = {
        "id": f"cover_{content_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}",
        "type": "cover",
        "content_id": content_id,
        "variants": [{"url": u, "metrics": None} for u in cover_urls],
        "status": "running",
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "winner": None
    }
    data["tests"].append(test)
    _save_tests(data, platform)
    return {"test_id": test["id"], "variants_count": len(cover_urls), "status": "created"}

def create_timing_test(content_id: str, publish_times: List[str], platform: str = "default") -> dict:
    """
    创建发布时间A/B测试
    publish_times: ["09:00", "12:00", "20:00"]
    """
    data = _load_tests(platform)
    test = {
        "id": f"timing_{content_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}",
        "type": "timing",
        "content_id": content_id,
        "variants": [{"time": t, "metrics": None} for t in publish_times],
        "status": "running",
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "winner": None
    }
    data["tests"].append(test)
    _save_tests(data, platform)
    return {"test_id": test["id"], "variants_count": len(publish_times), "status": "created"}

# ========== 记录数据 ==========

def record_metrics(test_id: str, variant_index: int, metrics: dict, platform: str = "default") -> dict:
    """
    记录变体的效果数据
    metrics: {"views": 1000, "likes": 50, "comments": 10, "shares": 5, "ctr": 3.5}
    """
    data = _load_tests(platform)
    for test in data["tests"]:
        if test["id"] == test_id:
            if 0 <= variant_index < len(test["variants"]):
                test["variants"][variant_index]["metrics"] = metrics
                _save_tests(data, platform)
                return {"status": "recorded", "test_id": test_id, "variant": variant_index}
            return {"error": f"variant_index {variant_index} 超出范围"}
    return {"error": f"测试 {test_id} 不存在"}

# ========== 分析对比 ==========

def _calc_score(metrics: dict) -> float:
    """计算综合得分（加权）"""
    if not metrics:
        return 0
    weights = {"views": 0.2, "likes": 0.25, "comments": 0.25, "shares": 0.2, "ctr": 0.1}
    score = 0
    for k, w in weights.items():
        val = metrics.get(k, 0)
        score += val * w
    return round(score, 2)

def analyze_test(test_id: str, platform: str = "default") -> dict:
    """
    分析单个测试结果
    返回：各变体对比、胜出者、提升幅度
    """
    data = _load_tests(platform)
    for test in data["tests"]:
        if test["id"] == test_id:
            variants = test["variants"]
            
            # 检查数据完整性
            has_data = [v["metrics"] is not None for v in variants]
            if not all(has_data):
                return {"error": "部分变体缺少数据", "missing": [i for i, h in enumerate(has_data) if not h]}
            
            # 计算得分
            scores = []
            for i, v in enumerate(variants):
                score = _calc_score(v["metrics"])
                scores.append({
                    "variant": i,
                    "label": v.get("text") or v.get("url") or v.get("time"),
                    "score": score,
                    "metrics": v["metrics"]
                })
            
            # 排序找胜出者
            scores.sort(key=lambda x: -x["score"])
            winner = scores[0]
            runner_up = scores[1] if len(scores) > 1 else None
            
            # 计算提升幅度
            improvement = 0
            if runner_up and runner_up["score"] > 0:
                improvement = round((winner["score"] - runner_up["score"]) / runner_up["score"] * 100, 1)
            
            # 更新测试状态
            test["status"] = "completed"
            test["winner"] = winner["variant"]
            _save_tests(data, platform)
            
            return {
                "test_id": test_id,
                "type": test["type"],
                "status": "completed",
                "rankings": scores,
                "winner": winner,
                "improvement": f"+{improvement}%" if improvement > 0 else f"{improvement}%",
                "recommendation": f"建议采用变体{winner['variant']}: {winner['label']}"
            }
    return {"error": f"测试 {test_id} 不存在"}

def generate_comparison_report(test_id: str, platform: str = "default") -> str:
    """生成效果对比报告（Markdown格式）"""
    result = analyze_test(test_id, platform)
    if "error" in result:
        return f"# 错误\n{result['error']}"
    
    report = f"""# A/B测试报告: {result['test_id']}

## 测试类型
{'标题测试' if result['type']=='title' else '封面测试' if result['type']=='cover' else '发布时间测试'}

## 效果排名

| 排名 | 变体 | 综合得分 | 浏览 | 点赞 | 评论 | 分享 | CTR |
|------|------|----------|------|------|------|------|-----|
"""
    for i, r in enumerate(result["rankings"]):
        m = r["metrics"]
        report += f"| {i+1} | {r['label'][:20]} | {r['score']} | {m.get('views',0)} | {m.get('likes',0)} | {m.get('comments',0)} | {m.get('shares',0)} | {m.get('ctr',0)}% |\n"
    
    w = result["winner"]
    report += f"""
## 结论

**胜出变体**: {w['label']}

**提升幅度**: {result['improvement']}

**建议**: {result['recommendation']}
"""
    return report

def list_tests(platform: str = "default", status: str = None) -> list:
    """列出所有测试"""
    data = _load_tests(platform)
    tests = data.get("tests", [])
    if status:
        tests = [t for t in tests if t["status"] == status]
    return [{"id": t["id"], "type": t["type"], "status": t["status"], "created": t["created_at"]} for t in tests]

def get_test(test_id: str, platform: str = "default") -> dict:
    """获取测试详情"""
    data = _load_tests(platform)
    for t in data["tests"]:
        if t["id"] == test_id:
            return t
    return {"error": "测试不存在"}

# ========== 演示 ==========

def run_demo():
    """运行演示"""
    platform = "demo"
    
    # 1. 创建标题测试
    print("=== 创建标题A/B测试 ===")
    t1 = create_title_test("post_001", [
        "10个提升效率的神器，第5个太绝了！",
        "效率工具推荐：这10款软件让你事半功倍",
        "程序员必备：10款效率神器深度评测"
    ], platform)
    print(f"测试创建: {t1}")
    
    # 2. 模拟记录数据
    print("\n=== 记录效果数据 ===")
    record_metrics(t1["test_id"], 0, {"views": 5000, "likes": 200, "comments": 45, "shares": 30, "ctr": 4.2}, platform)
    record_metrics(t1["test_id"], 1, {"views": 3500, "likes": 150, "comments": 35, "shares": 20, "ctr": 3.1}, platform)
    record_metrics(t1["test_id"], 2, {"views": 4200, "likes": 280, "comments": 60, "shares": 45, "ctr": 5.0}, platform)
    print("数据已记录")
    
    # 3. 分析结果
    print("\n=== 分析结果 ===")
    result = analyze_test(t1["test_id"], platform)
    print(f"胜出: 变体{result['winner']['variant']} - {result['winner']['label'][:30]}")
    print(f"提升: {result['improvement']}")
    
    # 4. 生成报告
    print("\n=== 对比报告 ===")
    report = generate_comparison_report(t1["test_id"], platform)
    print(report)

if __name__ == "__main__":
    run_demo()
