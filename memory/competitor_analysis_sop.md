# 竞品分析SOP (L3)
工具: temp/tools/competitor_analyzer.py

## 快速开始
```python
from competitor_analyzer import *

# 1. 创建账号数据
my_account = create_account("我的账号", "xiaohongshu",
    followers=5000, posts_count=120, avg_likes=150,
    avg_comments=20, avg_shares=10, engagement_rate=0.036,
    post_frequency=3, top_categories=["教程", "测评"])

competitor = create_account("竞品A", "xiaohongshu",
    followers=50000, posts_count=300, avg_likes=800,
    avg_comments=100, avg_shares=50, engagement_rate=0.019,
    post_frequency=7, top_categories=["种草", "日常"])

# 2. 对比分析
accounts = [my_account, competitor]
comparison = compare_accounts(accounts)  # 返回排名和洞察

# 3. 内容策略分析
strategy = analyze_content_strategy(my_account)  # 最佳时间/内容配比

# 4. 生成报告
generate_comparison_report(accounts, "report.md")  # Markdown报告
visualize_comparison(accounts, "chart.png")  # 对比图表

# 5. 数据持久化
save_accounts_data(accounts, "data.json")
accounts = load_accounts_data("data.json")
```

## 核心函数
| 函数 | 用途 | 返回 |
|------|------|------|
| create_account(name, platform, **kwargs) | 创建账号 | AccountMetrics |
| compare_accounts(accounts) | 多账号对比 | Dict(排名+洞察) |
| analyze_content_strategy(account) | 策略分析 | ContentStrategy |
| generate_comparison_report(accounts, path) | 生成报告 | Markdown字符串 |
| visualize_comparison(accounts, path) | 生成图表 | 图片路径 |

## 平台支持
weixin / zhihu / xiaohongshu / douyin

## 指标说明
- engagement_rate: 互动率 = (点赞+评论+分享) / 粉丝数
- post_frequency: 每周发文数

[skill_mapping]
category: data_analysis
skill: competitor_analysis_sop
tools: competitor_analyzer.py
[/skill_mapping]
