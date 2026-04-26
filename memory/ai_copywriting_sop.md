# ai_copywriting_sop.md — AI文案生成SOP（R161, 2026-04-20）

工具: tools/ai_copywriter.py | 基于模板引擎

## 核心函数

```python
generate_title(topic, style='professional', **kwargs)
generate_summary(topic, style='professional', key_points=None)
generate_content(topic, style='professional', points=None, opening=None, closing=None)
generate_full_copy(topic, style='professional', **kwargs)
```

## 使用示例

```python
from ai_copywriter import generate_title, generate_full_copy, STYLE_PROFESSIONAL

# 生成标题
title = generate_title('内容创作', STYLE_PROFESSIONAL, 核心观点='实战方法', 数量='5')

# 生成完整文案
copy = generate_full_copy('内容创作', STYLE_PROFESSIONAL, 
                          key_points=['方法', '技巧', '工具'],
                          points=['观点1', '观点2', '观点3'])
print(copy['title'])
print(copy['summary'])
print(copy['content'])
```

## 风格说明

- **STYLE_PROFESSIONAL**: 专业严谨，适合学术/技术内容
- **STYLE_CASUAL**: 轻松活泼，适合生活/娱乐内容
- **STYLE_MARKETING**: 营销导向，适合推广/销售内容

## 模板变量

### 标题模板
- {主题}: 核心主题
- {核心观点}: 核心观点
- {数量}: 数字（如3个/5个）
- {动作}: 动作词（如提升/优化）
- {优惠}: 优惠信息（营销风格）

### 摘要模板
- {主题}: 核心主题
- {要点1/2/3}: 关键要点

### 正文模板
- {开头}: 开场白
- {观点1/2/3}: 核心观点
- {总结}: 结尾总结

## 文案规则

- 标题：≤30字，关键词前置，使用数字
- 摘要：≤120字，总-分-总结构
- 正文：≥300字，3段结构，使用小标题

[skill_mapping]
category: content_creation
skill: copywriting
tools: ai_copywriter.py
[/skill_mapping]

## [record_on_use]
执行完本SOP后，调用以下命令记录使用情况：
```python
import sys
sys.path.append('../memory')
from autonomous_operation_sop.helper import record_skill_usage
record_skill_usage('ai_copywriting_sop.md')
```
