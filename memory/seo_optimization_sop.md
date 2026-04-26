# SEO优化与关键词分析 SOP

## 1. 简介

本SOP提供SEO优化和关键词分析的标准流程，帮助提升内容在搜索引擎中的可见度。

**工具位置**: `temp/tools/seo_toolkit.py`

## 2. 核心功能

### 2.1 关键词密度分析
分析文本中关键词出现频率，识别核心主题。

### 2.2 标题优化
评估标题质量，提供优化建议（长度、关键词、吸引力）。

### 2.3 Meta描述生成
自动生成搜索引擎友好的meta描述。

### 2.4 关键词研究
提供相关关键词建议和竞争度估算。

## 3. 使用示例

### 3.1 快速SEO分析
```python
import sys
sys.path.append("./tools")
import seo_toolkit

# 快速分析
text = "你的文章内容..."
title = "你的文章标题"
result = seo_toolkit.quick_seo_analysis(text, title)

print("关键词:", result["keywords"])
print("标题评分:", result["title_score"]["score"])
print("Meta描述:", result["meta_description"])
```

### 3.2 关键词密度分析
```python
analyzer = seo_toolkit.SEOAnalyzer()
keywords = analyzer.analyze_keyword_density(text, top_n=10)
for word, density in keywords:
    print(f"{word}: {density:.2f}%")
```

### 3.3 标题优化
```python
optimizer = seo_toolkit.TitleOptimizer()
score_result = optimizer.score_title("你的标题")
opt_result = optimizer.optimize_title("你的标题", keywords=["关键词1"])
```

### 3.4 Meta描述生成
```python
generator = seo_toolkit.DescriptionGenerator()
description = generator.generate_meta_description(text, max_length=160)
descriptions = generator.generate_descriptions(text, count=3)
```

### 3.5 关键词研究
```python
research = seo_toolkit.KeywordResearch()
competition = research.estimate_competition("人工智能")
related = research.suggest_related_keywords("机器学习")
```

## 4. 最佳实践

### 4.1 标题优化原则
- 长度控制在10-60字符
- 关键词尽量靠前
- 包含数字或疑问增加吸引力
- 避免关键词堆砌

### 4.2 Meta描述要点
- 长度控制在150-160字符
- 包含1-2个核心关键词
- 清晰描述内容价值
- 包含行动号召（CTA）

### 4.3 关键词密度建议
- 主关键词密度: 2-3%
- 相关关键词密度: 1-2%
- 避免过度优化

## 5. 验收标准

- ✓ 关键词密度分析功能正常
- ✓ 标题优化评分准确
- ✓ Meta描述生成符合规范
- ✓ 提供实用的优化建议

---
[skill_mapping]
category: web_automation
skill: seo_optimization
tools: temp/tools/seo_toolkit.py
[/skill_mapping]

## [record_on_use]
执行完本SOP后，调用以下命令记录使用情况：
```python
import sys
sys.path.append("../memory")
from autonomous_operation_sop.helper import record_skill_usage
record_skill_usage("seo_optimization_sop.md")
```