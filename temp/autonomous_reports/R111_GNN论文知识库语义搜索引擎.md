# GNN论文知识库语义搜索引擎

**任务类型**: 产出
**执行日期**: 2026-04-09
**对应TODO**: Batch20 Task1 - 语义搜索引擎
**对应缺口**: knowledge_search.语义搜索 [HIGH]

## 产出物

- **文件**: `local_skills/search_kb_semantic.py` (215行)
- **缓存**: `local_skills/paper_embeddings.pkl`

## 实现方案

由于 sentence-transformers/torch 环境缺失，改用 **TF-IDF + char_wb n-gram** 方案：
- `analyzer="char_wb"`, `ngram_range=(2,4)`, `max_features=8000`
- 无需外部模型，纯 sklearn 实现，支持中英文混合查询
- 余弦相似度排序，缓存 pkl 避免重复构建

## 功能接口

```
list_papers()                    # 列出所有论文
search_semantic(query, top_k=5) # 语义搜索，返回(results, time)
build_index(force=False)         # 构建/重建TF-IDF索引
CLI: python search_kb_semantic.py search "GNN知识图谱"
```

## 验证结果

| 查询 | 结果数 | 耗时 | TOP1准确性 |
|------|--------|------|------------|
| GNN knowledge graph reasoning | 3 | 0.018s | ✓ Reasoning on Graphs |
| 大语言模型提示优化 | 3 | 0.017s | ✓ MASPOB |
| 图神经网络时序预测 | 3 | 0.020s | ✓ How Powerful are GNNs |

- 论文数: 18篇
- 索引构建: 0.090s
- 平均搜索: ~0.020s

## 修复的Bug

1. **ROOT_DIR路径错误**: `local_skills/` 在 `temp/` 下，`gnn_papers/` 在 `GenericAgent/` 下，需两级 dirname
2. **分隔符转义**: 文件中 `r"\n---\n"` 实际为 `r"\n---\n"`，需用 `re.split(r"\n---\n", ...)` 匹配
3. **中文搜索**: word analyzer 无法处理中文，改用 char_wb n-gram 解决

## 局限性

- TF-IDF 是词频统计，非真正语义向量，相似度分数较低（0.03-0.43）
- 若后续安装 sentence-transformers，可升级为真正语义搜索
- 当前 18 篇论文，扩充后需 force=True 重建索引

## 记忆更新建议

- global_mem_insight: 新增 `GNN论文语义搜索: local_skills/search_kb_semantic.py(TF-IDF+char_wb,中英文,list/search/build_index)`
