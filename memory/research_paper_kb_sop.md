# 本地研究论文知识库维护 SOP

## 核心原理
- **持久化存储**：所有抓取的论文附加写入 `./gnn_papers/PAPERS.md`，跨会话保留
- **分层检索**：从 arXiv API 自动抓取 → 本地存储 → 按关键词/年份/作者快速查询
- **智能补充**：由 LLM 逐篇填充论文的深度分析（Problem/Method/Contributions/Threats）
- **零副作用**：仅调用 arXiv 只读 API，写入限定在项目目录

## 物理位置
- 入口脚本：`./local_skills/research_paper_kb_like.py`
- 默认输出文件：`./gnn_papers/PAPERS.md`

## 使用场景

### 场景 1：抓取特定主题的最新论文
**目标**：从 arXiv 导入符合条件的论文列表到本地库

```bash
# 基础用法：搜索 GNN + LLM 相关论文，最多取 5 篇
uv run python local_skills/research_paper_kb_like.py fetch \
  --query 'ti:"graph neural network" AND all:"large language model"' \
  --max_results 5

# 搜索特定年份
uv run python local_skills/research_paper_kb_like.py fetch \
  --query 'submittedDate:[202501010000 TO 202601010000]' \
  --max_results 10
```

**arXiv 查询语法**：
| 语法 | 含义 | 示例 |
|-----|------|------|
| `ti:"关键词"` | 标题精确匹配 | `ti:"graph neural network"` |
| `all:"关键词"` | 全文搜索（标题+摘要+作者） | `all:"attention mechanism"` |
| `AND / OR / NOT` | 逻辑操作 | `ti:"transformer" AND all:"vision"` |
| `au:"作者名"` | 作者搜索 | `au:"LeCun"` |
| `submittedDate:[...]` | 时间范围 | `submittedDate:[202501010000 TO 202601010000]` |

### 场景 2：在已导入的论文库中检索
**目标**：快速找到符合条件的已收录论文

```bash
# 按关键词搜索（标题+摘要，不区分大小写）
uv run python local_skills/research_paper_kb_like.py search --keyword "attention"

# 按精确年份筛选
uv run python local_skills/research_paper_kb_like.py search --year 2025

# 按年份范围
uv run python local_skills/research_paper_kb_like.py search --year_from 2024 --year_to 2026

# 按作者搜索
uv run python local_skills/research_paper_kb_like.py search --author "Zhang"

# 组合查询 + 显示完整摘要
uv run python local_skills/research_paper_kb_like.py search --year_from 2024 --keyword "LLM" --verbose
```

### 场景 3：列出所有论文
**目标**：总览当前知识库规模

```bash
# 仅显示标题+作者
uv run python local_skills/research_paper_kb_like.py list

# 显示完整摘要
uv run python local_skills/research_paper_kb_like.py list --verbose
```

## 输出格式

### PAPERS.md 结构
每篇论文占一个区块，格式如下：

```markdown
---
_Collected at: 2026-03-24 05:43:37 UTC_
_Query: `ti:"graph neural network" AND all:"large language model"`_

## [2026] MASPOB: Bandit-Based Prompt Optimization for Multi-Agent Systems with Graph Neural Networks
- Authors: Alice Zhang, Bob Li, Charlie Wang
- arXiv: http://arxiv.org/abs/2603.02630v1

### Abstract
Large language models (LLMs) combined with graph neural networks (GNNs)...

### Notes (to be filled)
- Problem:
- Method:
- Contributions:
- Threats / Limitations:
```

## 完整工作流

### 第一次设置
1. 从 arXiv 拉取初始论文集：
   ```bash
   uv run python local_skills/research_paper_kb_like.py fetch \
     --query 'cat:cs.LG AND submittedDate:[202501010000 TO 202604160000]' \
     --max_results 20
   ```
2. 检查 `./gnn_papers/PAPERS.md` 是否生成并包含论文

### 迭代过程（每周一次）
1. **定向抓取**：搜索新主题或最新论文
   ```bash
   uv run python local_skills/research_paper_kb_like.py fetch --query '[新主题]' --max_results 5
   ```
2. **检索关键论文**：找到值得深度阅读的文献
   ```bash
   uv run python local_skills/research_paper_kb_like.py search --keyword "[关键词]" --verbose
   ```
3. **补充分析**：LLM 逐篇阅读 PAPERS.md，填充 Notes 区块

### 质量保证
- **防重复**：脚本应自动检查 arXiv ID，避免导入重复论文
- **摘要完整性**：所有论文必须包含完整的 Abstract
- **Notes 填充率**：每月保证 ≥80% 论文完成 Problem/Method/Contributions 字段

## 常见命令参考表

| 任务 | 命令 |
|-----|------|
| 搜索最新的 GNN 论文 | `fetch --query 'cat:cs.LG AND all:"graph neural network"' --max_results 10` |
| 搜索特定作者的全部论文 | `search --author "Bengio"` |
| 找到 2025 年关于 Transformer 的所有论文 | `search --year 2025 --keyword "transformer" --verbose` |
| 统计当前知识库规模 | `list \| wc -l` |
| 导出某年份的所有论文标题 | `search --year 2026 \| grep "^##"` |

## 故障排查

| 问题 | 排查步骤 |
|-----|---------|
| arXiv API 超时 | 1. 检查网络连通性 2. 减少 `--max_results` 3. 等待 3 秒后重试 |
| 论文重复导入 | 检查脚本是否实现了 arXiv ID 去重逻辑 |
| PAPERS.md 损坏（格式混乱） | 1. 备份当前文件 2. 从 git 恢复最近的好版本 3. 重新导入 |
| 搜索结果为空 | 1. 检查关键词拼写 2. 尝试更宽泛的搜索条件 3. 确认库中确实有数据 |

## R205 多源同步增强 (2026-04-21)

### 新增功能

#### 1. 从BibTeX导入
```python
from local_skills.research_paper_kb_like import import_from_bibtex

result = import_from_bibtex('papers.bib')
print(f"成功: {result['success']}, 失败: {result['failed']}, 重复: {result['duplicates']}")
```

#### 2. 从PDF元数据导入
```python
from local_skills.research_paper_kb_like import import_from_pdf_metadata

result = import_from_pdf_metadata('paper.pdf')
if result['success']:
    print(f"导入成功: {result['paper']['title']}")
```

#### 3. 从Markdown导入
```python
from local_skills.research_paper_kb_like import import_from_markdown

result = import_from_markdown('papers.md')
print(f"成功: {result['success']}, 失败: {result['failed']}, 重复: {result['duplicates']}")
```

#### 4. 多源批量同步
```python
from local_skills.research_paper_kb_like import sync_from_sources

sources = [
    {"type": "bibtex", "path": "papers.bib"},
    {"type": "markdown", "path": "papers.md"},
    {"type": "pdf", "path": "paper.pdf"}
]

result = sync_from_sources(sources)
print(f"同步成功率: {result['success_rate']:.1f}%")
print(f"总计: {result['total']}, 成功: {result['success']}, 失败: {result['failed']}, 重复: {result['duplicates']}")
```

#### 5. 查看同步状态
```python
from local_skills.research_paper_kb_like import get_sync_status

status = get_sync_status()
print(f"总论文数: {status['total_papers']}")
print(f"数据源分布: {status['sources']}")
```

### 自动去重机制
- **ID匹配**: 完全相同的论文ID自动跳过
- **标题匹配**: 标题完全相同视为重复
- **相似度计算**: 使用Jaccard相似度算法

### 支持的数据源
1. **BibTeX** (.bib) - 学术引用标准格式
2. **PDF** (.pdf) - 从文件名提取元数据
3. **Markdown** (.md) - YAML-like格式

---
[skill_mapping]
category: knowledge_management
skill: paper_acquisition
tools: research_paper_kb_like.py
[/skill_mapping]

## [record_on_use]
执行完本SOP后，调用以下命令记录使用情况：
```python
import sys
sys.path.append('../memory')
from autonomous_operation_sop.helper import record_skill_usage
record_skill_usage('research_paper_kb_sop.md')
```

## 引用格式化模块 citation_formatter.py (R212新增)
```python
from citation_formatter import Paper, CitationFormatter, format_citation

# 创建论文对象
paper = Paper(
    title="Attention Is All You Need",
    authors=["Ashish Vaswani", "Noam Shazeer"],
    year=2017,
    journal="NeurIPS",
    volume="30",
    pages="5998-6008",
    doc_type="journal"  # journal/conference/book/web
)

# 格式化输出
formatter = CitationFormatter(paper)
print(formatter.to_apa())      # APA 7th
print(formatter.to_mla())      # MLA 9th
print(formatter.to_gbt7714())  # GB/T 7714-2015

# 便捷函数
citation = format_citation(paper, "gbt7714")
all_formats = formatter.all_formats()  # {"APA":..., "MLA":..., "GB/T 7714":...}
```
支持类型: 期刊[J]/会议[C]/书籍[M]/网页[EB/OL]
