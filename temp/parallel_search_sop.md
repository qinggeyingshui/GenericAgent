# 并行多引擎搜索 SOP

## 工具位置
`temp/parallel_search.py`

## 核心功能
一次查询并行调用多个搜索引擎，自动聚合去重结果。

## 支持的引擎

### 无需API Key
- **GitHub**: 搜索开源仓库（按stars排序）
- **DuckDuckGo**: 通用网页搜索

### 需要API Key
- **Brave**: 高质量网页搜索（免费tier: 2000次/月）
- **Serper**: Google搜索代理（免费tier: 2500次）

## 使用方法

### 基础用法（无需key）
```python
import sys
sys.path.insert(0, './temp')
from parallel_search import search

# 搜索GitHub仓库
result = search("python async web scraping", engines=["github"], max_results=5)

# 查看聚合结果
for item in result['aggregated']['results']:
    print(f"{item['title']}: {item['url']}")
```

### 多引擎并行
```python
# 同时搜索GitHub和DuckDuckGo
result = search(
    "best python web framework 2026",
    engines=["github", "duckduckgo"],
    max_results=5
)

print(f"总结果: {result['aggregated']['total_results']}条")
print(f"耗时: {result['elapsed_seconds']}秒")
```

### 使用API Key
```python
# 从keychain获取API key
import sys
sys.path.insert(0, '../memory')
from keychain import get_key

brave_key = get_key("BRAVE_SEARCH_API")
serper_key = get_key("SERPER_API_KEY")

result = search(
    "machine learning papers 2026",
    engines=["github", "brave", "serper"],
    max_results=10,
    brave_key=brave_key,
    serper_key=serper_key
)
```

## 结果结构
```python
{
    "query": "搜索关键词",
    "engines": ["github", "duckduckgo"],
    "elapsed_seconds": 2.5,
    "timestamp": "2026-04-16T22:00:00",
    "raw_results": {
        "github": {"success": true, "results": [...]},
        "duckduckgo": {"success": true, "results": [...]}
    },
    "aggregated": {
        "total_results": 10,
        "engines_succeeded": 2,
        "engines_failed": 0,
        "results": [
            {
                "title": "项目名称",
                "url": "https://...",
                "description": "描述",
                "source_engine": "github",
                "stars": 1234  # GitHub特有
            }
        ]
    }
}
```

## 使用场景

### 1. 技术方案调研
```python
# 寻找最佳实践
result = search("python pdf parsing library comparison", engines=["github", "duckduckgo"])
```

### 2. 开源工具查找
```python
# 只搜GitHub，按stars排序
result = search("python web scraping framework", engines=["github"], max_results=10)
```

### 3. 综合信息收集
```python
# 多引擎并行，获取更全面的结果
result = search("GNN graph neural network tutorial", engines=["github", "brave", "serper"])
```

## 最佳实践

1. **引擎选择**
   - 找代码/工具 → 只用 `["github"]`
   - 找教程/文档 → `["duckduckgo"]` 或 `["brave"]`
   - 综合调研 → `["github", "brave", "serper"]`

2. **结果数量**
   - 快速查找: `max_results=3`
   - 深度调研: `max_results=10`

3. **错误处理**
   - 检查 `aggregated.engines_succeeded` 确认成功引擎数
   - 查看 `raw_results[engine].error` 了解失败原因

4. **性能优化**
   - 并行执行，总耗时 ≈ 最慢引擎的耗时
   - 减少 `max_results` 可加快速度

## 注意事项

- ⚠️ GitHub API有rate limit（未认证: 60次/小时，认证: 5000次/小时）
- ⚠️ DuckDuckGo可能不稳定，建议配合其他引擎使用
- ⚠️ Brave/Serper需要API key，从keychain获取
- ⚠️ 网络问题会导致个别引擎失败，但不影响其他引擎

## 集成到工作流

### 复杂任务前调研
```python
# 在执行复杂任务前，先搜索现成方案
task = "实现PDF转Markdown"
result = search(f"python {task} library", engines=["github"], max_results=5)

# 分析top结果
for item in result['aggregated']['results'][:3]:
    print(f"⭐ {item.get('stars', 0)} - {item['title']}")
    print(f"   {item['url']}")
```

### 与research_search_sop配合
1. 先用 `parallel_search` 快速获取候选方案
2. 再按 `research_search_sop` 流程深入对比评估
3. 选定方案后进入详情页核实参数

## 未来扩展

- [ ] 支持图像搜索（Google Images API）
- [ ] 支持视频搜索（YouTube API）
- [ ] 结果智能排序（基于相关性评分）
- [ ] 缓存机制（避免重复查询）
- [ ] 更多引擎（Bing、Yandex等）
