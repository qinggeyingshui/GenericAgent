# GNN + LLM 论文元数据库
# 格式: YAML-like blocks，每篇论文一个条目
# 更新时间: 2026-03-25

---
id: MASPOB
title: "MASPOB: Multi-Agent System for Prompt Optimization Based on GNN"
authors: ["Anonymous et al."]
year: 2026
arxiv: "arXiv:2603.02630"
venue: "arXiv preprint"
keywords: ["GNN", "LLM", "multi-agent", "prompt optimization", "message passing"]
summary: >
  提出基于图神经网络的多智能体提示优化框架。将提示空间建模为图结构，
  利用GNN消息传递机制在多个Agent之间协同优化提示策略，
  在多个基准任务上优于单Agent基线。
relevance: "教学重点：GNN与LLM结合的典型架构，适合L01课程导入案例"
code_url: "https://arxiv.org/abs/2603.02630"
applications: "多智能体协同提示优化，适用于需要多步推理的LLM任务；图结构建模提示空间，提升复杂任务的提示工程效率；可扩展至自动化AI工作流设计场景。"
local_file: ""

---
id: GraphRAG2024
title: "From Local to Global: A Graph RAG Approach to Query-Focused Summarization"
authors: ["Edge, Darren", "Trinh, Ha", "Cheng, Newman"]
year: 2024
arxiv: "arXiv:2404.16130"
venue: "arXiv preprint"
keywords: ["RAG", "knowledge graph", "summarization", "LLM", "community detection"]
summary: >
  Microsoft提出GraphRAG：将文档语料构建为实体关系图，
  通过社区检测（Leiden算法）生成层次化摘要，
  支持全局性查询，显著优于朴素RAG方法。
relevance: "工程重点：知识图谱+LLM的RAG增强，适合L02知识图谱与检索课程"
code_url: "https://github.com/microsoft/graphrag"
applications: "企业知识库全局性问答系统；学术文献综述自动生成；大规模文档语料的结构化摘要与社区分析。"
local_file: ""

---
id: GraphTransformer2021
title: "Do Transformers Really Perform Bad for Graph Representation? (Graphormer)"
authors: ["Ying, Chengxuan", "Cai, Tianle", "Luo, Shengjie", "Zheng, Shuxin"]
year: 2021
arxiv: "arXiv:2106.05234"
venue: "NeurIPS 2021"
keywords: ["Graph Transformer", "GNN", "Graphormer", "molecular property prediction"]
summary: >
  提出Graphormer：将Transformer应用于图结构数据，
  引入空间编码、边编码和中心度编码三类图结构偏置，
  在分子属性预测(OGB-LSC)上取得SOTA，获NeurIPS 2021最佳论文。
relevance: "基础重点：Graph Transformer架构，适合L02模型演进对比教学"
code_url: "https://github.com/microsoft/Graphormer"
applications: "分子属性预测与药物发现；量子化学计算加速；蛋白质结构图的特征表示学习。"
local_file: ""

---
id: LLMonGraph2024
title: "Exploring the Potential of Large Language Models on Graphs"
authors: ["Chen, Zhikai", "Mao, Haitao", "Li, Hang", "Jin, Wei", "Wen, Hongzhi", "Wei, Xiaochi", "Wang, Shuaiqiang", "Yin, Dawei", "Fan, Wenqi", "Liu, Hui", "Tang, Jiliang"]
year: 2024
arxiv: "arXiv:2307.03393"
venue: "ACM SIGKDD Explorations 2024"
keywords: ["LLM", "GNN", "node classification", "text-attributed graph", "survey"]
summary: >
  系统探讨LLM在图任务上的应用潜力。将LLM定位为三种角色：
  增强器(Enhancer)、预测器(Predictor)、对齐器(Aligner)，
  实验表明LLM作为特征增强器时与GNN结合效果最佳。
relevance: "综述重点：LLM+GNN协同范式分类，适合L03前沿方向导读"
code_url: "https://github.com/CurryTang/Graph-LLM"
applications: "文本属性图的节点分类与链接预测；社交网络用户行为建模；电商推荐系统中LLM与图结构的协同增强。"
local_file: ""

---
id: GNNSurvey2021
title: "A Comprehensive Study on Large-Scale Graph Neural Networks"
authors: ["Zhu, Jiong", "Rossi, Ryan A.", "Rao, Anup"]
year: 2021
arxiv: "arXiv:2104.05541"
venue: "KDD 2021"
keywords: ["GNN", "survey", "scalability", "sampling", "GraphSAGE", "GAT", "GCN"]
summary: >
  大规模GNN综述与实证研究。系统评估GraphSAGE、GAT、GCN等主流GNN
  在大规模图上的可扩展性，分析采样策略、聚合方式对性能的影响，
  提供可复现基准测试。
relevance: "综述基础：GNN主流模型横评，适合L01/L02背景知识铺垫"
code_url: "https://github.com/snap-stanford/ogb"
applications: "大规模社交网络社区检测与影响力传播分析；工业推荐系统中亿级节点图的实时推理；生物信息学蛋白质互作网络分析。"
local_file: ""
---
id: "GCN2017"
arxiv: "arXiv:1609.02907"
title: "Semi-Supervised Classification with Graph Convolutional Networks"
year: "2017"
venue: "ICLR 2017"
keywords: ["GCN", "graph convolutional network", "semi-supervised", "node classification", "spectral graph theory"]
summary: "We present a scalable approach for semi-supervised learning on graph-structured data based on an efficient variant of convolutional neural networks operating directly on graphs. The model scales linearly in the number of graph edges and learns hidden layer representations that encode both local graph structure and features of nodes. Evaluated on citation networks (Cora, Citeseer, Pubmed) and a knowledge graph dataset, outperforming related methods by a significant margin."
relevance: "基础必读：GCN原论文，图卷积网络开山之作，适合L02图神经网络基础课程核心内容"

---
id: "GAT2018"
arxiv: "arXiv:1710.10903"
title: "Graph Attention Networks"
year: "2018"
venue: "ICLR 2018"
keywords: ["GAT", "graph attention", "attention mechanism", "node classification", "GNN"]
summary: "We present graph attention networks (GATs), novel neural network architectures that operate on graph-structured data, leveraging masked self-attentional layers to address the shortcomings of prior graph convolution methods. By stacking layers in which nodes are able to attend over their neighborhoods features, the model implicitly assigns different importances to different nodes without requiring costly matrix operations or prior knowledge of the graph structure."
relevance: "核心架构：图注意力网络GAT原论文，适合L03图注意力网络与Transformer课程，与Transformer注意力机制对比教学"

---
id: "GraphSAGE2017"
arxiv: "arXiv:1706.02216"
title: "Inductive Representation Learning on Large Graphs"
year: "2017"
venue: "NeurIPS 2017"
keywords: ["GraphSAGE", "inductive learning", "neighbor sampling", "scalable GNN", "graph representation"]
summary: "We present GraphSAGE, a general inductive framework that leverages node feature information to efficiently generate node embeddings for previously unseen data. Instead of training individual embeddings for each node, we learn a function that generates embeddings by sampling and aggregating features from a node local neighborhood. Demonstrated on three inductive node classification benchmarks with significant improvements over transductive baselines."
relevance: "扩展性重点：GraphSAGE归纳式学习，解决大规模图和新节点问题，适合L02/L05大规模图处理教学"

---
id: "RoG2024"
arxiv: "arXiv:2310.01061"
title: "Reasoning on Graphs: Faithful and Interpretable Large Language Model Reasoning"
year: "2024"
venue: "ICLR 2024"
keywords: ["LLM", "knowledge graph", "reasoning", "GNN", "interpretable", "RoG", "faithful"]
summary: "Large language models (LLMs) have demonstrated impressive reasoning abilities but lack up-to-date knowledge and experience hallucinations. We propose Reasoning on Graphs (RoG) that synergizes LLMs with knowledge graphs (KGs) to enable faithful and interpretable reasoning. RoG generates relation paths grounded by KGs as faithful plans, then retrieves valid reasoning paths to conduct faithful reasoning. Evaluated on multi-hop reasoning datasets with state-of-the-art performance."
relevance: "前沿应用：LLM+知识图谱联合推理RoG框架，适合L04 GNN与LLM联合应用课程，展示可解释推理"

---
id: "GraphGPT2024"
arxiv: "arXiv:2310.13023"
title: "GraphGPT: Graph Instruction Tuning for Large Language Models"
year: "2024"
venue: "SIGIR 2024"
keywords: ["GraphGPT", "instruction tuning", "LLM", "GNN", "graph understanding", "graph token"]
summary: "Graph Neural Networks (GNNs) have evolved to understand graph structures through recursive exchanges and aggregations among nodes. We propose GraphGPT that aligns GNNs with a large language model to enable graph instruction tuning. A graph encoder converts structural graph signals into tokens that LLMs can process, enabling zero-shot and few-shot generalization to unseen graphs. Outperforms existing GNN models on various graph learning tasks."
relevance: "前沿架构：Graph token + LLM指令微调，适合L04/L05前沿系统课程，展示GNN与LLM的深度融合"

---
id: "QUICK_START"
title: "🚀 从零开始： 分钟跑起来"
year: "2024"
arxiv: "QUICK_START"
venue: "unknown"
summary: "(auto-imported test)"
keywords: []
relevance: "auto-imported"
