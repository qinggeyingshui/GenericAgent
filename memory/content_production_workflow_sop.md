# 自媒体内容生产流水线 SOP

## 概述
端到端自动化内容生产流程：热点追踪 → 文案生成 → 平台适配 → 发布输出

## 工具依赖
- `temp/tools/trend_tracker.py` - 热点追踪
- `temp/tools/ai_copywriter.py` - AI文案生成
- `temp/tools/platform_adapter.py` - 平台适配

## 完整工作流

### 步骤1: 热点追踪
获取当前热点话题和推荐选题

```python
from tools.trend_tracker import get_trending_topics, recommend_topics

# 获取热点话题
trends = get_trending_topics(platform='weibo', limit=10)
print(f"发现 {len(trends)} 个热点话题")

# 智能推荐选题
recommendations = recommend_topics(
    category='tech',  # 科技/娱乐/财经/生活
    keywords=['AI', '科技'],
    min_heat=1000
)

# 选择话题
selected_topic = recommendations[0]
print(f"选题: {selected_topic['title']}")
print(f"热度: {selected_topic['heat']}")
print(f"理由: {selected_topic['reason']}")
```

### 步骤2: 文案生成
基于选题生成多平台内容

```python
from tools.ai_copywriter import generate_title, generate_content, generate_summary

topic = selected_topic['title']
keywords = selected_topic['keywords']

# 生成标题（3个备选）
titles = generate_title(topic, style='engaging', count=3)
best_title = titles[0]

# 生成正文
content = generate_content(
    topic=topic,
    keywords=keywords,
    length='medium',  # short/medium/long
    tone='professional'  # casual/professional/humorous
)

# 生成摘要
summary = generate_summary(content, max_length=100)

print(f"标题: {best_title}")
print(f"正文: {len(content)} 字")
print(f"摘要: {summary}")
```

### 步骤3: 平台适配
将内容适配到不同平台格式

```python
from tools.platform_adapter import adapt_to_wechat, adapt_to_zhihu, adapt_to_xiaohongshu

# 微信公众号格式
wechat_content = adapt_to_wechat(
    title=best_title,
    content=content,
    summary=summary,
    add_emoji=True,
    add_divider=True
)

# 知乎格式
zhihu_content = adapt_to_zhihu(
    title=best_title,
    content=content,
    add_tags=True,
    tags=keywords
)

# 小红书格式
xiaohongshu_content = adapt_to_xiaohongshu(
    title=best_title,
    content=content,
    add_emoji=True,
    add_hashtags=True
)
```

### 步骤4: 发布输出
保存适配后的内容

```python
import os
from datetime import datetime

# 创建输出目录
output_dir = f"./content_output/{datetime.now().strftime('%Y%m%d_%H%M%S')}"
os.makedirs(output_dir, exist_ok=True)

# 保存各平台内容
platforms = {
    'wechat': wechat_content,
    'zhihu': zhihu_content,
    'xiaohongshu': xiaohongshu_content
}

for platform, content in platforms.items():
    filepath = f"{output_dir}/{platform}.txt"
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"✓ {platform}: {filepath}")

print(f"\n内容已保存到: {output_dir}")
```

## 一键自动化流程

```python
def auto_produce_content(category='tech', keywords=None, platforms=['wechat', 'zhihu']):
    """
    一键自动化内容生产
    
    Args:
        category: 内容类别
        keywords: 关键词列表
        platforms: 目标平台列表
    
    Returns:
        输出目录路径
    """
    from tools.trend_tracker import recommend_topics
    from tools.ai_copywriter import generate_title, generate_content, generate_summary
    from tools.platform_adapter import adapt_to_wechat, adapt_to_zhihu, adapt_to_xiaohongshu
    import os
    from datetime import datetime
    
    # 1. 热点追踪
    print("📊 追踪热点...")
    topics = recommend_topics(category=category, keywords=keywords, min_heat=500)
    if not topics:
        return "未找到合适话题"
    
    topic = topics[0]
    print(f"✓ 选题: {topic['title']}")
    
    # 2. 文案生成
    print("\n✍️ 生成文案...")
    titles = generate_title(topic['title'], style='engaging', count=3)
    best_title = titles[0]
    
    content = generate_content(
        topic=topic['title'],
        keywords=topic.get('keywords', []),
        length='medium',
        tone='professional'
    )
    
    summary = generate_summary(content, max_length=100)
    print(f"✓ 标题: {best_title}")
    print(f"✓ 正文: {len(content)} 字")
    
    # 3. 平台适配
    print("\n🔄 平台适配...")
    adapted_content = {}
    
    if 'wechat' in platforms:
        adapted_content['wechat'] = adapt_to_wechat(best_title, content, summary)
        print("✓ 微信公众号")
    
    if 'zhihu' in platforms:
        adapted_content['zhihu'] = adapt_to_zhihu(best_title, content, 
                                                    tags=topic.get('keywords', []))
        print("✓ 知乎")
    
    if 'xiaohongshu' in platforms:
        adapted_content['xiaohongshu'] = adapt_to_xiaohongshu(best_title, content)
        print("✓ 小红书")
    
    # 4. 保存输出
    print("\n💾 保存内容...")
    output_dir = f"./content_output/{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    os.makedirs(output_dir, exist_ok=True)
    
    for platform, content_text in adapted_content.items():
        filepath = f"{output_dir}/{platform}.txt"
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content_text)
        print(f"✓ {filepath}")
    
    print(f"\n✅ 完成！内容已保存到: {output_dir}")
    return output_dir

# 使用示例
output = auto_produce_content(
    category='tech',
    keywords=['AI', '人工智能'],
    platforms=['wechat', 'zhihu', 'xiaohongshu']
)
```

## 高级功能

### 批量生产
```python
def batch_produce(topics_list, platforms=['wechat', 'zhihu']):
    """批量生产多个话题的内容"""
    results = []
    for topic in topics_list:
        output = auto_produce_content(
            category=topic['category'],
            keywords=topic['keywords'],
            platforms=platforms
        )
        results.append(output)
    return results
```

### 定时生产
```python
# 结合 scheduled_task_sop.md 实现定时内容生产
# 每天早上9点自动生产内容
```

### 质量检查
```python
def quality_check(content):
    """内容质量检查"""
    checks = {
        'length': len(content) >= 500,  # 最少500字
        'keywords': any(kw in content for kw in ['AI', '科技']),  # 包含关键词
        'readability': True  # 可读性检查（简化）
    }
    return all(checks.values())
```

## 最佳实践

1. **选题策略**
   - 关注热度>1000的话题
   - 结合自身定位选择类别
   - 避免过度追热点

2. **内容质量**
   - 标题吸引但不夸张
   - 正文结构清晰（总-分-总）
   - 适当添加数据和案例

3. **平台差异**
   - 微信：长文深度，专业性强
   - 知乎：逻辑严谨，数据支撑
   - 小红书：轻松活泼，视觉化

4. **发布时机**
   - 微信：早8点、晚8点
   - 知乎：工作日午休、晚上
   - 小红书：晚7-10点

## 注意事项

1. **内容原创性**: AI生成内容需人工审核和修改
2. **平台规则**: 遵守各平台内容规范
3. **版权问题**: 引用数据需注明来源
4. **敏感词过滤**: 发布前检查敏感词

## 相关SOP
- trend_tracking_sop.md - 热点追踪详细说明
- ai_copywriting_sop.md - 文案生成技巧
- platform_adaptation_sop.md - 平台适配规则

[skill_mapping]
category: content_creation
skill: content_production_workflow
tools: trend_tracker.py, ai_copywriter.py, platform_adapter.py
[/skill_mapping]

## [record_on_use]
执行完本SOP后，调用以下命令记录使用情况：
```python
import sys
sys.path.append('../memory')
from autonomous_operation_sop.helper import record_skill_usage
record_skill_usage('content_production_workflow_sop.md')
```