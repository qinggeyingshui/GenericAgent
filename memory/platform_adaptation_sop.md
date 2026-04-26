# platform_adaptation_sop.md — 多平台内容适配SOP（R160, 2026-04-20）

工具: tools/platform_adapter.py | 基于markdown+PIL

## 核心函数

```python
adapt_content(content, platform, title='', images=None)
batch_adapt(content, platforms, title='', images=None)
resize_image(image_path, max_width, max_height, output_path=None)
```

## 使用示例

### 1. 单平台适配

```python
from tools.platform_adapter import adapt_content, PLATFORM_WECHAT

content = '# 标题\n\n正文内容...'
result = adapt_content(content, PLATFORM_WECHAT, title='文章标题')

print(result['title'])    # 适配后的标题
print(result['content'])  # 适配后的内容
```

### 2. 批量适配多平台

```python
from tools.platform_adapter import batch_adapt, PLATFORM_WECHAT, PLATFORM_ZHIHU, PLATFORM_XIAOHONGSHU

platforms = [PLATFORM_WECHAT, PLATFORM_ZHIHU, PLATFORM_XIAOHONGSHU]
results = batch_adapt(content, platforms, title='文章标题')

for platform, result in results.items():
    print(f'{platform}: {result["title"]}')
```

### 3. 图片适配

```python
from tools.platform_adapter import adapt_content, PLATFORM_WECHAT

images = ['cover.jpg', 'content1.jpg']
result = adapt_content(content, PLATFORM_WECHAT, title='标题', images=images)

# 处理后的图片路径
print(result['images'])  # ['cover_wechat.jpg', 'content1_wechat.jpg']
```

## 平台规则

### 微信公众号
- 标题最大长度：64字符
- 图片最大尺寸：1080×2000
- 输出格式：HTML（带样式）
- 字体大小：16px
- 行间距：1.5em

### 知乎
- 标题最大长度：100字符
- 图片最大尺寸：1200×3000
- 输出格式：Markdown
- 支持LaTeX公式

### 小红书
- 标题最大长度：20字符
- 内容最大长度：1000字符
- 图片最大尺寸：1242×1660
- 推荐比例：3:4
- 建议添加话题标签和emoji

## 注意事项

1. **内容格式**：输入内容建议使用markdown格式，便于跨平台转换
2. **图片处理**：自动调整尺寸，保持原始比例，质量95%
3. **标题长度**：超出平台限制会自动截断
4. **小红书特殊**：内容长度限制严格，建议精简内容或分段发布
5. **微信公众号**：输出HTML格式，可直接复制到编辑器

## 扩展平台

添加新平台规则到`PLATFORM_RULES`字典：

```python
PLATFORM_RULES['new_platform'] = {
    'max_image_width': 1000,
    'max_image_height': 2000,
    'title_max_length': 50,
    # 其他规则...
}
```

并实现对应的`_adapt_new_platform()`函数。

[skill_mapping]
category: content_creation
skill: platform_adaptation
tools: platform_adapter.py
[/skill_mapping]

## [record_on_use]
执行完本SOP后，调用以下命令记录使用情况：
```python
import sys
sys.path.append('../memory')
from autonomous_operation_sop.helper import record_skill_usage
record_skill_usage('platform_adaptation_sop.md')
```
