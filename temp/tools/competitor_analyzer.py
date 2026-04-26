#!/usr/bin/env python3
"""
competitor_analyzer.py - 竞品分析与对标工具

功能:
1. 账号对比 - 多账号数据横向对比
2. 内容策略分析 - 发布频率/时间/类型分析
3. 数据可视化 - 生成对比图表和报告

依赖: pandas, matplotlib
"""
import os
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
import random

# ============ 数据模型 ============

@dataclass
class AccountMetrics:
    """账号指标"""
    name: str
    platform: str  # weixin/zhihu/xiaohongshu/douyin
    followers: int
    posts_count: int
    avg_likes: float
    avg_comments: float
    avg_shares: float
    engagement_rate: float  # 互动率
    post_frequency: float   # 每周发文数
    top_categories: List[str]  # 主要内容类型
    
@dataclass
class ContentStrategy:
    """内容策略"""
    account_name: str
    best_post_times: List[str]  # 最佳发布时间
    content_mix: Dict[str, float]  # 内容类型占比
    avg_post_length: int
    hashtag_usage: float  # 话题标签使用率
    image_ratio: float    # 图文比例
    video_ratio: float    # 视频比例

# ============ 核心函数 ============

def create_account(name: str, platform: str, **kwargs) -> AccountMetrics:
    """
    创建账号指标对象
    
    Args:
        name: 账号名称
        platform: 平台(weixin/zhihu/xiaohongshu/douyin)
        **kwargs: 其他指标
    
    Returns:
        AccountMetrics对象
    """
    return AccountMetrics(
        name=name,
        platform=platform,
        followers=kwargs.get('followers', 0),
        posts_count=kwargs.get('posts_count', 0),
        avg_likes=kwargs.get('avg_likes', 0.0),
        avg_comments=kwargs.get('avg_comments', 0.0),
        avg_shares=kwargs.get('avg_shares', 0.0),
        engagement_rate=kwargs.get('engagement_rate', 0.0),
        post_frequency=kwargs.get('post_frequency', 0.0),
        top_categories=kwargs.get('top_categories', [])
    )

def compare_accounts(accounts: List[AccountMetrics]) -> Dict:
    """
    多账号横向对比
    
    Args:
        accounts: 账号列表
    
    Returns:
        对比结果字典
    """
    if not accounts:
        return {"error": "无账号数据"}
    
    result = {
        "account_count": len(accounts),
        "comparison_date": datetime.now().strftime("%Y-%m-%d"),
        "metrics": {},
        "rankings": {},
        "insights": []
    }
    
    # 各指标对比
    metrics_keys = ['followers', 'posts_count', 'avg_likes', 'avg_comments', 
                    'avg_shares', 'engagement_rate', 'post_frequency']
    
    for key in metrics_keys:
        values = [(a.name, getattr(a, key)) for a in accounts]
        values.sort(key=lambda x: -x[1])
        result["metrics"][key] = {name: val for name, val in values}
        result["rankings"][key] = [name for name, _ in values]
    
    # 生成洞察
    top_followers = result["rankings"]["followers"][0]
    top_engagement = result["rankings"]["engagement_rate"][0]
    
    result["insights"].append(f"粉丝量最高: {top_followers}")
    result["insights"].append(f"互动率最高: {top_engagement}")
    
    if top_followers != top_engagement:
        result["insights"].append(f"💡 {top_engagement}虽然粉丝较少但互动率更高，内容质量值得学习")
    
    return result

def analyze_content_strategy(account: AccountMetrics, posts_data: List[Dict] = None) -> ContentStrategy:
    """
    分析账号内容策略
    
    Args:
        account: 账号指标
        posts_data: 帖子数据列表(可选)
    
    Returns:
        ContentStrategy对象
    """
    # 如果没有实际数据，生成模拟分析
    if not posts_data:
        # 基于账号特征推断策略
        best_times = ["08:00", "12:00", "20:00"] if account.post_frequency > 3 else ["12:00", "20:00"]
        
        content_mix = {
            "教程干货": 0.4,
            "行业资讯": 0.25,
            "个人观点": 0.2,
            "互动话题": 0.15
        }
        
        return ContentStrategy(
            account_name=account.name,
            best_post_times=best_times,
            content_mix=content_mix,
            avg_post_length=800 if account.platform == "zhihu" else 300,
            hashtag_usage=0.8 if account.platform in ["xiaohongshu", "douyin"] else 0.3,
            image_ratio=0.7,
            video_ratio=0.3 if account.platform == "douyin" else 0.1
        )
    
    # 实际数据分析
    post_hours = []
    content_types = {}
    total_length = 0
    hashtag_count = 0
    image_count = 0
    video_count = 0
    
    for post in posts_data:
        # 发布时间
        if 'publish_time' in post:
            hour = post['publish_time'].split(':')[0] if ':' in str(post['publish_time']) else "12"
            post_hours.append(hour)
        
        # 内容类型
        ctype = post.get('content_type', '其他')
        content_types[ctype] = content_types.get(ctype, 0) + 1
        
        # 长度
        total_length += len(post.get('content', ''))
        
        # 标签
        if post.get('hashtags'):
            hashtag_count += 1
        
        # 媒体类型
        if post.get('has_image'):
            image_count += 1
        if post.get('has_video'):
            video_count += 1
    
    n = len(posts_data) or 1
    
    # 统计最佳发布时间
    from collections import Counter
    hour_counts = Counter(post_hours)
    best_times = [f"{h}:00" for h, _ in hour_counts.most_common(3)]
    
    # 内容类型占比
    total_types = sum(content_types.values()) or 1
    content_mix = {k: v/total_types for k, v in content_types.items()}
    
    return ContentStrategy(
        account_name=account.name,
        best_post_times=best_times or ["12:00"],
        content_mix=content_mix,
        avg_post_length=total_length // n,
        hashtag_usage=hashtag_count / n,
        image_ratio=image_count / n,
        video_ratio=video_count / n
    )

def generate_comparison_report(accounts: List[AccountMetrics], output_path: str = None) -> str:
    """
    生成竞品对比报告(Markdown格式)
    
    Args:
        accounts: 账号列表
        output_path: 输出路径(可选)
    
    Returns:
        报告内容
    """
    comparison = compare_accounts(accounts)
    
    report = f"""# 竞品分析报告

生成时间: {comparison['comparison_date']}
分析账号数: {comparison['account_count']}

## 1. 账号概览

| 账号 | 平台 | 粉丝数 | 发文数 | 互动率 |
|------|------|--------|--------|--------|
"""
    
    for acc in accounts:
        report += f"| {acc.name} | {acc.platform} | {acc.followers:,} | {acc.posts_count} | {acc.engagement_rate:.2%} |\n"
    
    report += "\n## 2. 指标排名\n\n"
    
    metric_names = {
        'followers': '粉丝数',
        'engagement_rate': '互动率',
        'avg_likes': '平均点赞',
        'post_frequency': '发文频率'
    }
    
    for key, name in metric_names.items():
        rankings = comparison['rankings'].get(key, [])
        report += f"**{name}**: {' > '.join(rankings)}\n\n"
    
    report += "## 3. 关键洞察\n\n"
    for insight in comparison['insights']:
        report += f"- {insight}\n"
    
    report += "\n## 4. 内容策略对比\n\n"
    
    for acc in accounts:
        strategy = analyze_content_strategy(acc)
        report += f"### {acc.name}\n"
        report += f"- 最佳发布时间: {', '.join(strategy.best_post_times)}\n"
        report += f"- 内容类型: {', '.join([f'{k}({v:.0%})' for k,v in strategy.content_mix.items()])}\n"
        report += f"- 图文比例: {strategy.image_ratio:.0%} | 视频比例: {strategy.video_ratio:.0%}\n\n"
    
    report += """## 5. 行动建议

1. 学习互动率最高账号的内容风格
2. 参考最佳发布时间调整发文计划
3. 优化内容类型配比，增加高互动类型占比
4. 定期更新竞品数据，持续追踪变化

---
*报告由 competitor_analyzer.py 自动生成*
"""
    
    if output_path:
        os.makedirs(os.path.dirname(output_path) or '.', exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(report)
    
    return report

def visualize_comparison(accounts: List[AccountMetrics], output_path: str = None):
    """
    生成对比可视化图表
    
    Args:
        accounts: 账号列表
        output_path: 图片输出路径
    
    Returns:
        图片路径或None
    """
    try:
        import matplotlib.pyplot as plt
        import matplotlib
        matplotlib.use('Agg')
        plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei']
        plt.rcParams['axes.unicode_minus'] = False
        
        fig, axes = plt.subplots(2, 2, figsize=(12, 10))
        
        names = [a.name for a in accounts]
        
        # 1. 粉丝数对比
        ax1 = axes[0, 0]
        followers = [a.followers for a in accounts]
        ax1.bar(names, followers, color=['#4CAF50', '#2196F3', '#FF9800', '#E91E63'][:len(names)])
        ax1.set_title('粉丝数对比')
        ax1.set_ylabel('粉丝数')
        
        # 2. 互动率对比
        ax2 = axes[0, 1]
        engagement = [a.engagement_rate * 100 for a in accounts]
        ax2.bar(names, engagement, color=['#4CAF50', '#2196F3', '#FF9800', '#E91E63'][:len(names)])
        ax2.set_title('互动率对比 (%)')
        ax2.set_ylabel('互动率')
        
        # 3. 互动指标雷达图(简化为柱状图)
        ax3 = axes[1, 0]
        x = range(len(names))
        width = 0.25
        ax3.bar([i - width for i in x], [a.avg_likes for a in accounts], width, label='点赞')
        ax3.bar(x, [a.avg_comments for a in accounts], width, label='评论')
        ax3.bar([i + width for i in x], [a.avg_shares for a in accounts], width, label='分享')
        ax3.set_xticks(x)
        ax3.set_xticklabels(names)
        ax3.set_title('互动指标对比')
        ax3.legend()
        
        # 4. 发文频率
        ax4 = axes[1, 1]
        frequency = [a.post_frequency for a in accounts]
        ax4.bar(names, frequency, color=['#9C27B0', '#00BCD4', '#FFEB3B', '#795548'][:len(names)])
        ax4.set_title('周发文频率')
        ax4.set_ylabel('篇/周')
        
        plt.tight_layout()
        
        if output_path:
            os.makedirs(os.path.dirname(output_path) or '.', exist_ok=True)
            plt.savefig(output_path, dpi=150, bbox_inches='tight')
            plt.close()
            return output_path
        
        plt.close()
        return None
        
    except ImportError:
        return None

def save_accounts_data(accounts: List[AccountMetrics], filepath: str):
    """保存账号数据到JSON"""
    data = [asdict(a) for a in accounts]
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def load_accounts_data(filepath: str) -> List[AccountMetrics]:
    """从JSON加载账号数据"""
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return [AccountMetrics(**d) for d in data]

# ============ 演示函数 ============

def demo_competitor_analysis(output_dir: str = './competitor_demo'):
    """
    演示竞品分析功能
    """
    os.makedirs(output_dir, exist_ok=True)
    
    # 创建示例账号
    accounts = [
        create_account("我的账号", "xiaohongshu", 
                      followers=5000, posts_count=120, avg_likes=150,
                      avg_comments=20, avg_shares=10, engagement_rate=0.036,
                      post_frequency=3, top_categories=["教程", "测评"]),
        create_account("竞品A", "xiaohongshu",
                      followers=50000, posts_count=300, avg_likes=800,
                      avg_comments=100, avg_shares=50, engagement_rate=0.019,
                      post_frequency=7, top_categories=["种草", "日常"]),
        create_account("竞品B", "xiaohongshu",
                      followers=20000, posts_count=200, avg_likes=600,
                      avg_comments=80, avg_shares=30, engagement_rate=0.036,
                      post_frequency=5, top_categories=["教程", "好物"]),
    ]
    
    # 生成报告
    report_path = os.path.join(output_dir, 'comparison_report.md')
    report = generate_comparison_report(accounts, report_path)
    print(f"报告已生成: {report_path}")
    
    # 生成图表
    chart_path = os.path.join(output_dir, 'comparison_chart.png')
    result = visualize_comparison(accounts, chart_path)
    if result:
        print(f"图表已生成: {chart_path}")
    
    # 保存数据
    data_path = os.path.join(output_dir, 'accounts_data.json')
    save_accounts_data(accounts, data_path)
    print(f"数据已保存: {data_path}")
    
    return report_path

if __name__ == "__main__":
    demo_competitor_analysis()
