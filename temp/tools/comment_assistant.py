"""
comment_assistant.py - 评论区互动助手
功能: 评论抓取/情感分析/智能回复/粉丝分层
"""
import json
from datetime import datetime
from collections import defaultdict

# 情感词典
SENTIMENT_WORDS = {
    "positive": ["好", "棒", "赞", "喜欢", "支持", "优秀", "精彩", "厉害", "感谢", "有用"],
    "negative": ["差", "烂", "垃圾", "失望", "不好", "无聊", "浪费", "骗人", "退款"],
}

# 回复模板
REPLY_TEMPLATES = {
    "positive": [
        "感谢支持！会继续努力的💪",
        "谢谢认可！后续会带来更多优质内容",
        "感谢鼓励！你的支持是我最大的动力",
    ],
    "negative": [
        "感谢反馈，我们会改进的🙏",
        "抱歉让您失望了，会认真听取意见",
        "感谢建议，我们会努力做得更好",
    ],
    "neutral": [
        "感谢留言！有问题随时交流",
        "谢谢关注！欢迎多提建议",
        "收到！感谢参与讨论",
    ],
}


def analyze_sentiment(text):
    """情感分析"""
    pos_count = sum(1 for word in SENTIMENT_WORDS["positive"] if word in text)
    neg_count = sum(1 for word in SENTIMENT_WORDS["negative"] if word in text)
    
    if pos_count > neg_count:
        return "positive"
    elif neg_count > pos_count:
        return "negative"
    return "neutral"


def generate_reply(comment_text, sentiment=None):
    """生成智能回复"""
    if sentiment is None:
        sentiment = analyze_sentiment(comment_text)
    
    import random
    return random.choice(REPLY_TEMPLATES[sentiment])


def classify_fan(user_id, comments_data):
    """粉丝分层"""
    user_comments = [c for c in comments_data if c.get("user_id") == user_id]
    comment_count = len(user_comments)
    
    # 计算情感倾向
    sentiments = [analyze_sentiment(c["text"]) for c in user_comments]
    positive_ratio = sentiments.count("positive") / max(len(sentiments), 1)
    
    # 分层逻辑
    if comment_count >= 10 and positive_ratio > 0.7:
        return "核心粉丝"
    elif comment_count >= 5:
        return "活跃粉丝"
    elif comment_count >= 2:
        return "普通粉丝"
    return "新粉丝"


def load_comments(file_path):
    """加载评论数据"""
    with open(file_path, "r", encoding="utf-8") as f:
        if file_path.endswith(".json"):
            return json.load(f)
        else:
            # CSV格式
            import csv
            reader = csv.DictReader(f)
            return list(reader)


def analyze_comments(comments_data):
    """批量分析评论"""
    results = []
    for comment in comments_data:
        sentiment = analyze_sentiment(comment["text"])
        reply = generate_reply(comment["text"], sentiment)
        results.append({
            "user_id": comment.get("user_id", "unknown"),
            "user_name": comment.get("user_name", "匿名"),
            "text": comment["text"],
            "sentiment": sentiment,
            "suggested_reply": reply,
            "timestamp": comment.get("timestamp", datetime.now().isoformat())
        })
    return results


def generate_fan_report(comments_data):
    """生成粉丝分层报告"""
    user_stats = defaultdict(list)
    for comment in comments_data:
        user_id = comment.get("user_id", "unknown")
        user_stats[user_id].append(comment)
    
    report = {}
    for user_id, user_comments in user_stats.items():
        tier = classify_fan(user_id, comments_data)
        user_name = user_comments[0].get("user_name", "匿名")
        report[user_id] = {
            "name": user_name,
            "tier": tier,
            "comment_count": len(user_comments),
            "sentiments": [analyze_sentiment(c["text"]) for c in user_comments]
        }
    return report


def save_analysis(results, output_path):
    """保存分析结果"""
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    return output_path


if __name__ == "__main__":
    print("评论区互动助手")
    print("功能: 情感分析 + 智能回复 + 粉丝分层")