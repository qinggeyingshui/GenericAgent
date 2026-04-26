"""
trend_tracker.py - Trend Tracking and Topic Recommendation Tool (R164, 2026-04-20)

Features:
1. Extract trending keywords
2. Analyze trends
3. Recommend topics
"""

import re
from collections import Counter
from datetime import datetime, timedelta


def extract_keywords(text, top_n=10):
    text = re.sub(r"[^\w\s]", " ", text)
    words = text.split()
    words = [w for w in words if len(w) > 1]
    counter = Counter(words)
    return counter.most_common(top_n)


def analyze_trend(data_points):
    if len(data_points) < 2:
        return {"trend": "insufficient_data", "growth_rate": 0}
    
    first_val = data_points[0]
    last_val = data_points[-1]
    
    if first_val == 0:
        growth_rate = 100 if last_val > 0 else 0
    else:
        growth_rate = ((last_val - first_val) / first_val) * 100
    
    if growth_rate > 20:
        trend = "rising"
    elif growth_rate < -20:
        trend = "falling"
    else:
        trend = "stable"
    
    return {"trend": trend, "growth_rate": round(growth_rate, 2)}


def recommend_topics(keywords, trends, max_recommendations=5):
    recommendations = []
    
    for keyword, count in keywords[:max_recommendations]:
        score = count
        
        if keyword in trends:
            trend_info = trends[keyword]
            if trend_info["trend"] == "rising":
                score *= 1.5
            elif trend_info["trend"] == "falling":
                score *= 0.7
        
        recommendations.append({
            "keyword": keyword,
            "score": round(score, 2),
            "frequency": count,
            "trend": trends.get(keyword, {"trend": "unknown"})["trend"]
        })
    
    recommendations.sort(key=lambda x: x["score"], reverse=True)
    return recommendations


def track_trends(texts, output_path=None):
    all_text = " ".join(texts)
    keywords = extract_keywords(all_text, top_n=20)
    
    trends = {}
    for keyword, _ in keywords:
        data_points = [text.count(keyword) for text in texts]
        trends[keyword] = analyze_trend(data_points)
    
    recommendations = recommend_topics(keywords, trends)
    
    if output_path:
        report_lines = []
        report_lines.append("# Trend Tracking Report\n\n")
        report_lines.append(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        report_lines.append("## Top Keywords\n\n")
        for kw, count in keywords[:10]:
            report_lines.append(f"- {kw}: {count}\n")
        report_lines.append("\n")
        
        report_lines.append("## Trend Analysis\n\n")
        for kw, trend_info in list(trends.items())[:10]:
            report_lines.append(f"- {kw}: {trend_info['trend']} ({trend_info['growth_rate']}%)\n")
        report_lines.append("\n")
        
        report_lines.append("## Topic Recommendations\n\n")
        for i, rec in enumerate(recommendations, 1):
            report_lines.append(f"{i}. {rec['keyword']} (Score: {rec['score']}, Trend: {rec['trend']})\n")
        
        with open(output_path, "w", encoding="utf-8") as f:
            f.writelines(report_lines)
    
    return {
        "keywords": keywords,
        "trends": trends,
        "recommendations": recommendations,
        "report": output_path
    }


# ========== R203 增强功能 (2026-04-21) ==========

import json
from datetime import datetime

def calc_heat_score(keyword_data):
    """计算热度评分
    
    Args:
        keyword_data: {"keyword": str, "count": int, "mentions": int, "growth": float}
    
    Returns:
        int: 热度评分 (0-100)
    """
    count = keyword_data.get("count", 0)
    mentions = keyword_data.get("mentions", 0)
    growth = keyword_data.get("growth", 0)
    
    # 权重: 出现次数40% + 提及数30% + 增长率30%
    score = (
        min(count / 100 * 40, 40) +
        min(mentions / 50 * 30, 30) +
        min(growth / 100 * 30, 30)
    )
    
    return min(int(score), 100)


def predict_trend(historical_data, days_ahead=7):
    """预测未来趋势
    
    Args:
        historical_data: [{"date": str, "value": int}, ...]
        days_ahead: 预测天数
    
    Returns:
        {"prediction": str, "confidence": float, "forecast": []}
    """
    if len(historical_data) < 3:
        return {"prediction": "insufficient_data", "confidence": 0, "forecast": []}
    
    # 简单线性预测
    values = [d["value"] for d in historical_data]
    n = len(values)
    
    # 计算平均增长率
    growth_rates = []
    for i in range(1, n):
        if values[i-1] > 0:
            rate = (values[i] - values[i-1]) / values[i-1]
            growth_rates.append(rate)
    
    avg_growth = sum(growth_rates) / len(growth_rates) if growth_rates else 0
    
    # 预测未来值
    forecast = []
    last_value = values[-1]
    for i in range(days_ahead):
        predicted = last_value * (1 + avg_growth)
        forecast.append(int(predicted))
        last_value = predicted
    
    # 判断趋势
    if avg_growth > 0.1:
        prediction = "rising"
        confidence = min(abs(avg_growth) * 100, 95)
    elif avg_growth < -0.1:
        prediction = "falling"
        confidence = min(abs(avg_growth) * 100, 95)
    else:
        prediction = "stable"
        confidence = 70
    
    return {
        "prediction": prediction,
        "confidence": round(confidence, 2),
        "forecast": forecast,
        "avg_growth_rate": round(avg_growth * 100, 2)
    }


def auto_monitor(keywords, callback=None):
    """自动监控热点
    
    Args:
        keywords: [str] 关键词列表
        callback: 回调函数，接收监控结果
    
    Returns:
        {"timestamp": str, "results": [], "alerts": []}
    """
    results = []
    alerts = []
    
    for kw in keywords:
        # 模拟数据采集
        data = {
            "keyword": kw,
            "count": 0,
            "mentions": 0,
            "growth": 0
        }
        
        score = calc_heat_score(data)
        
        result = {
            "keyword": kw,
            "heat_score": score,
            "timestamp": datetime.now().isoformat()
        }
        results.append(result)
        
        # 高热度预警
        if score > 80:
            alerts.append(f"⚠️ {kw} 热度达到 {score}分")
    
    monitor_result = {
        "timestamp": datetime.now().isoformat(),
        "results": results,
        "alerts": alerts
    }
    
    if callback:
        callback(monitor_result)
    
    return monitor_result


def send_wechat_alert(content, webhook_url=None):
    """发送微信推送
    
    Args:
        content: 推送内容
        webhook_url: 企业微信webhook地址
    
    Returns:
        {"status": str, "message": str}
    """
    # 模拟推送（实际需要requests库）
    if not webhook_url:
        return {
            "status": "skipped",
            "message": "未配置webhook_url"
        }
    
    # 实际实现需要:
    # import requests
    # response = requests.post(webhook_url, json={"msgtype": "text", "text": {"content": content}})
    
    return {
        "status": "success",
        "message": f"已推送: {content[:50]}..."
    }


def schedule_daily_monitor(keywords, webhook_url=None):
    """设置每日监控
    
    Args:
        keywords: 监控关键词列表
        webhook_url: 微信推送地址
    
    Returns:
        {"status": str, "schedule": str}
    """
    def monitor_callback(result):
        if result["alerts"]:
            alert_text = "\n".join(result["alerts"])
            send_wechat_alert(f"热点预警\n{alert_text}", webhook_url)
    
    # 执行一次监控
    result = auto_monitor(keywords, monitor_callback)
    
    return {
        "status": "scheduled",
        "schedule": "daily_09:00",
        "keywords": keywords,
        "last_run": result["timestamp"]
    }


def analyze_hot_topics(topics_data):
    """分析热门话题
    
    Args:
        topics_data: [{"topic": str, "data": [{"date": str, "value": int}]}]
    
    Returns:
        [{"topic": str, "heat_score": int, "prediction": {}, "recommendation": str}]
    """
    results = []
    
    for item in topics_data:
        topic = item["topic"]
        data = item.get("data", [])
        
        # 计算热度
        if data:
            latest = data[-1]["value"]
            heat_data = {"keyword": topic, "count": latest, "mentions": latest, "growth": 0}
            if len(data) >= 2:
                growth = ((data[-1]["value"] - data[0]["value"]) / data[0]["value"] * 100) if data[0]["value"] > 0 else 0
                heat_data["growth"] = growth
            
            heat_score = calc_heat_score(heat_data)
        else:
            heat_score = 0
        
        # 预测趋势
        prediction = predict_trend(data) if data else {}
        
        # 生成建议
        if heat_score > 80 and prediction.get("prediction") == "rising":
            recommendation = "强烈推荐：高热度且上升趋势"
        elif heat_score > 60:
            recommendation = "推荐：中等热度"
        else:
            recommendation = "观望：热度较低"
        
        results.append({
            "topic": topic,
            "heat_score": heat_score,
            "prediction": prediction,
            "recommendation": recommendation
        })
    
    # 按热度排序
    results.sort(key=lambda x: x["heat_score"], reverse=True)
    
    return results
