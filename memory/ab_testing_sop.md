# 内容A/B测试 SOP

[skill_mapping]
category: content_creation
skill: ab_testing_sop
tools: ab_testing.py
[/skill_mapping]

> 工具路径: temp/ab_testing.py | 数据目录: temp/ab_test_data/

## 快速开始

```python
import sys; sys.path.append('temp')
from ab_testing import *

# 创建标题测试
test = create_title_test("post_001", ["标题A", "标题B", "标题C"], "weixin")

# 记录效果数据
record_metrics(test["test_id"], 0, {"views": 5000, "likes": 200, "comments": 45, "shares": 30, "ctr": 4.2}, "weixin")

# 分析结果
result = analyze_test(test["test_id"], "weixin")

# 生成报告
report = generate_comparison_report(test["test_id"], "weixin")
```

## 核心函数

| 函数 | 用途 |
|------|------|
| `create_title_test(content_id, variants, platform)` | 创建标题测试 |
| `create_cover_test(content_id, cover_urls, platform)` | 创建封面测试 |
| `create_timing_test(content_id, publish_times, platform)` | 创建发布时间测试 |
| `record_metrics(test_id, variant_index, metrics, platform)` | 记录效果数据 |
| `analyze_test(test_id, platform)` | 分析测试结果 |
| `generate_comparison_report(test_id, platform)` | 生成对比报告 |
| `list_tests(platform, status)` | 列出测试 |

## 效果指标

```json
{
  "views": 5000,      // 浏览量
  "likes": 200,       // 点赞数
  "comments": 45,     // 评论数
  "shares": 30,       // 分享数
  "ctr": 4.2          // 点击率%
}
```

## 综合得分算法

权重: views(0.2) + likes(0.25) + comments(0.25) + shares(0.2) + ctr(0.1)

## 使用流程

1. **创建测试** → 选择测试类型，设置变体
2. **投放内容** → 各变体分别投放
3. **记录数据** → 收集各变体效果指标
4. **分析对比** → 生成报告，确定胜出者
5. **应用结论** → 采用最优方案

## 与其他工具联动

- `fan_analytics.py`: 结合粉丝活跃时段优化发布时间测试
- `content_calendar.py`: 将测试结论应用到排期
- `media_analytics.py`: 获取效果数据用于记录
