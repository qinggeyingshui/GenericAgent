# 论文对比分析 SOP

## 功能概述
提供GNN论文库的多维度对比分析能力，支持2篇或多篇论文的并排对比，生成结构化markdown对比表。

## 工具文件
- **comparison_toolkit.py**: 论文对比分析工具（位于 temp/）
- **依赖**: GNN论文库 `../gnn_papers/PAPERS.md`

## 核心功能

### 1. 解析论文库
```python
from comparison_toolkit import parse_papers

papers = parse_papers()  # 返回所有论文的字典列表
```

### 2. 列出所有论文
```python
from comparison_toolkit import list_papers

print(list_papers())  # 显示所有论文ID、年份和标题
```

### 3. 对比论文（核心功能）
```python
from comparison_toolkit import compare_papers

# 对比2篇论文（默认维度）
result = compare_papers(["GCN2017", "GAT2018"])
print(result)

# 对比3篇论文（自定义维度）
result = compare_papers(
    ["GCN2017", "GAT2018", "GraphSAGE2017"],
    dimensions=["title", "year", "venue", "summary", "applications"]
)
print(result)
```

### 4. 获取单篇论文
```python
from comparison_toolkit import get_paper_by_id

paper = get_paper_by_id("GCN2017")
print(paper["title"])
```

## 对比维度

支持的对比维度（可自由组合）：
- `title`: 标题
- `year`: 年份
- `venue`: 发表会议/期刊
- `keywords`: 关键词
- `summary`: 摘要
- `code_url`: 代码链接
- `arxiv`: arXiv编号
- `authors`: 作者
- `relevance`: 教学相关性
- `applications`: 应用场景

默认维度：`["title", "year", "venue", "keywords", "summary", "code_url"]`

## 使用场景

### 场景1: 对比经典GNN模型
```python
# 对比GCN、GAT、GraphSAGE三大经典模型
result = compare_papers(
    ["GCN2017", "GAT2018", "GraphSAGE2017"],
    dimensions=["title", "year", "venue", "keywords", "summary"]
)
```

### 场景2: 对比LLM+GNN融合方法
```python
# 对比GraphRAG和LLMonGraph
result = compare_papers(
    ["GraphRAG2024", "LLMonGraph2024"],
    dimensions=["title", "summary", "applications", "code_url"]
)
```

### 场景3: 生成教学对比材料
```python
# 对比Transformer在图上的应用
result = compare_papers(
    ["GraphTransformer2021", "GAT2018"],
    dimensions=["title", "year", "summary", "relevance"]
)

# 保存到文件
with open("./comparison_result.md", "w", encoding="utf-8") as f:
    f.write("# 论文对比分析\n\n")
    f.write(result)
```

## 与现有系统集成

### 与 research_paper_kb_like.py 配合
```python
import sys
sys.path.append("../local_skills")
from research_paper_kb_like import list_papers as kb_list
from comparison_toolkit import compare_papers

# 1. 从知识库获取论文列表
papers_info = kb_list()

# 2. 提取论文ID进行对比
paper_ids = ["GCN2017", "GAT2018"]  # 根据需求选择
comparison = compare_papers(paper_ids)
print(comparison)
```

## 输出格式

生成的对比表为标准markdown表格格式：

```markdown
| 维度 | GCN2017 | GAT2018 |
|------|---------|---------|
| **标题** | Semi-Supervised Classification... | Graph Attention Networks |
| **年份** | 2017 | 2018 |
| **发表会议/期刊** | ICLR 2017 | ICLR 2018 |
...
```

## 注意事项

1. **论文ID必须准确**：使用 `list_papers()` 查看可用的论文ID
2. **维度名称区分大小写**：使用小写字段名（如 `title` 而非 `Title`）
3. **长文本自动截断**：摘要等长文本超过150字符会自动截断
4. **特殊字符转义**：表格中的 `|` 字符会自动转义为 `\|`

## 扩展开发

### 添加新的对比维度
在 `compare_papers()` 函数的 `dim_names` 字典中添加新维度映射：
```python
dim_names = {
    "title": "标题",
    "your_new_field": "新字段中文名",  # 添加这里
    ...
}
```

### 自定义输出格式
修改 `compare_papers()` 函数的表格生成逻辑，支持HTML、CSV等格式。

## 验收测试

```python
# 测试1: 对比2篇论文
result = compare_papers(["GCN2017", "GAT2018"])
assert "GCN2017" in result
assert "GAT2018" in result
assert "标题" in result

# 测试2: 对比3篇论文
result = compare_papers(["GCN2017", "GAT2018", "GraphSAGE2017"])
assert result.count("|") > 20  # 表格应有多行

# 测试3: 自定义维度
result = compare_papers(["GCN2017", "GAT2018"], dimensions=["title", "year"])
assert "年份" in result
assert "2017" in result

print("✓ 所有测试通过")
```

---
[skill_mapping]
category: knowledge_management
skill: paper_comparison
tools: comparison_toolkit.py
[/skill_mapping]

## [record_on_use]
执行完本SOP后，调用以下命令记录使用情况：
```python
import sys
sys.path.append('../memory')
from autonomous_operation_sop.helper import record_skill_usage
record_skill_usage('paper_comparison_sop.md')
```
