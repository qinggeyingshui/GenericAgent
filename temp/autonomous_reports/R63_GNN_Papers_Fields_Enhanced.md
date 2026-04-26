# R63 - GNN论文库元数据深化：code_url+applications字段补全
日期: 2026-03-26

## 任务来源
TODO Batch10条目2延伸：gnn_papers/PAPERS.md 5篇论文缺 code_url 和 applications 字段，影响论文库实用价值。

## 执行结果
5篇论文均已通过 file_patch 补入两个新字段：

| id | code_url | applications摘要 |
|----|----------|-----------------|
| MASPOB | arxiv.org/abs/2603.02630 | 多智能体提示优化，图结构提示空间 |
| GraphRAG2024 | github.com/microsoft/graphrag | 企业知识库问答，文献综述自动生成 |
| GraphTransformer2021 | github.com/microsoft/Graphormer | 分子属性预测，蛋白质结构图 |
| LLMonGraph2024 | github.com/CurryTang/Graph-LLM | 文本属性图节点分类，社交网络建模 |
| GNNSurvey2021 | github.com/snap-stanford/ogb | 大规模社交网络，工业推荐系统 |

## 验证
- kb.list_papers(): 5篇全部含 code_url=True, applications=True
- kb.search("GNN"): 返回4条，含code_url字段 ✓
- kb.search("attention"): 0条（search按keywords/title/summary匹配，attention非关键词，属正常）

## 发现
- research_paper_kb_like.py 的 search() 按关键词字段匹配，不做全文搜索
- GAT/注意力机制相关内容可通过补充keywords字段"attention"改善检索

## 建议（供用户审阅）
- 为GNNSurvey2021补充 keywords: ["attention", "GAT"] 提升注意力相关检索覆盖
