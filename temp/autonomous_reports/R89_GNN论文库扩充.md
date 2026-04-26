# R89 | GNN论文库扩充

日期: 2026-03-26
类型: 产出
验收: PASS

## 任务目标
用 research_paper_kb_like.py 的 add() 接口向 gnn_papers/PAPERS.md 补充论文，
使总篇数达到 >=10 篇（含摘要）。

## 执行结果
入库前: 5篇 | 入库后: 10篇 | 新增: 5篇

### 新增论文清单

| ID | 标题 | 年份 | 会议 | 课程对应 |
|---|---|---|---|---|
| GCN2017 | Semi-Supervised Classification with Graph Convolutional Networks | 2017 | ICLR 2017 | L02 GNN基础 |
| GAT2018 | Graph Attention Networks | 2018 | ICLR 2018 | L03 图注意力 |
| GraphSAGE2017 | Inductive Representation Learning on Large Graphs | 2017 | NeurIPS 2017 | L02/L05 大规模图 |
| RoG2024 | Reasoning on Graphs: Faithful and Interpretable LLM Reasoning | 2024 | ICLR 2024 | L04 联合应用 |
| GraphGPT2024 | GraphGPT: Graph Instruction Tuning for Large Language Models | 2024 | SIGIR 2024 | L04/L05 前沿 |

## 论文库覆盖分析
- 基础架构: GCN(2017) + GAT(2018) + GraphSAGE(2017) + Graphormer(2021) — 经典模型全覆盖
- GNN+LLM融合: MASPOB / GraphRAG / LLMonGraph / RoG / GraphGPT — 前沿方向5篇
- 综述类: GNNSurvey2021 — 横评背景知识
- 课程映射: L01-L05各课均有>=1篇对应论文

## 技术备注
- fetch()接口能联网抓取arXiv页面，但返回None（只print不return）；摘要改为人工填写
- add()接口正常，必填字段: id/title/year/arxiv
- 建议后续修复fetch()返回值问题（return abstract而非只print）

## 验收
- [x] PAPERS.md论文条目 = 10篇，满足>=10篇要求
- [x] 所有新增论文含摘要(summary字段)
- [x] 覆盖GNN基础+扩展+GNN+LLM前沿多个方向
- [x] 每篇含课程相关性标注
