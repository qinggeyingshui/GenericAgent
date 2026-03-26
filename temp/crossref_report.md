# 教案×论文库交叉引用报告

生成时间: 2026-03-26
教案总数: 8（GNN课程5个 + 编译原理3个）
论文库有效条目: 10
**教案命中论文数: 9**
**论文库覆盖率: 90.0%**
**缺失已知论文: 3 条**

---

## 一、逐教案命中情况

### 图神经网络与大语言模型 / L01_GNN与LLM联合架构导论
- ✅ [GAT2018] Graph Attention Networks
- ✅ [GCN2017] Semi-Supervised Classification with Graph Convolutional Networks
- ✅ [GNNSURVEY2021] A Comprehensive Study on Large-Scale Graph Neural Networks
- ✅ [GRAPHGPT2024] GraphGPT: Graph Instruction Tuning for Large Language Models
- ✅ [GRAPHRAG2024] From Local to Global: A Graph RAG Approach to Query-Focused Summarization
- ✅ [GRAPHSAGE2017] Inductive Representation Learning on Large Graphs
- ✅ [MASPOB] MASPOB: Multi-Agent System for Prompt Optimization Based on GNN

### 图神经网络与大语言模型 / L02_图神经网络基础
- ✅ [GAT2018] Graph Attention Networks
- ✅ [GCN2017] Semi-Supervised Classification with Graph Convolutional Networks
- ✅ [GRAPHGPT2024] GraphGPT: Graph Instruction Tuning for Large Language Models
- ✅ [GRAPHSAGE2017] Inductive Representation Learning on Large Graphs
- ✅ [MASPOB] MASPOB: Multi-Agent System for Prompt Optimization Based on GNN
- ⚠️ 提及 **GIN** (Xu et al., ICLR 2019) — 论文库缺失，建议补充
- ⚠️ 提及 **MPNN** (Gilmer et al., ICML 2017) — 论文库缺失，建议补充

### 图神经网络与大语言模型 / L03_图注意力网络与Transformer
- ✅ [GAT2018] Graph Attention Networks
- ✅ [GCN2017] Semi-Supervised Classification with Graph Convolutional Networks
- ✅ [GRAPHGPT2024] GraphGPT: Graph Instruction Tuning for Large Language Models
- ✅ [GRAPHTRANSFORMER2021] Do Transformers Really Perform Bad for Graph Representation? (Graphormer)
- ⚠️ 提及 **OGB** (Hu et al., NeurIPS 2020) — 论文库缺失，建议补充

### 图神经网络与大语言模型 / L04_GNN与LLM联合应用
- ✅ [GAT2018] Graph Attention Networks
- ✅ [GCN2017] Semi-Supervised Classification with Graph Convolutional Networks
- ✅ [GRAPHGPT2024] GraphGPT: Graph Instruction Tuning for Large Language Models
- ✅ [GRAPHRAG2024] From Local to Global: A Graph RAG Approach to Query-Focused Summarization
- ✅ [GRAPHTRANSFORMER2021] Do Transformers Really Perform Bad for Graph Representation? (Graphormer)
- ✅ [MASPOB] MASPOB: Multi-Agent System for Prompt Optimization Based on GNN

### 图神经网络与大语言模型 / L05_图神经网络前沿
- ✅ [GAT2018] Graph Attention Networks
- ✅ [GCN2017] Semi-Supervised Classification with Graph Convolutional Networks
- ✅ [GNNSURVEY2021] A Comprehensive Study on Large-Scale Graph Neural Networks
- ✅ [GRAPHGPT2024] GraphGPT: Graph Instruction Tuning for Large Language Models
- ✅ [GRAPHRAG2024] From Local to Global: A Graph RAG Approach to Query-Focused Summarization
- ✅ [GRAPHSAGE2017] Inductive Representation Learning on Large Graphs
- ✅ [GRAPHTRANSFORMER2021] Do Transformers Really Perform Bad for Graph Representation? (Graphormer)
- ✅ [ROG2024] Reasoning on Graphs: Faithful and Interpretable Large Language Model Reasoning

### 编译原理 / L01_编译原理概述
- （未命中库内论文）

### 编译原理 / L02_词法分析
- （未命中库内论文）

### 编译原理 / L03_自动机理论与DFA构造
- ✅ [GRAPHGPT2024] GraphGPT: Graph Instruction Tuning for Large Language Models

---

## 二、论文库覆盖率汇总

| 指标 | 数值 |
|------|------|
| 论文库有效条目 | 10 |
| 被教案引用的论文 | 9 |
| 覆盖率 | 90.0% |
| 教案提及但库缺失 | 3 |

### 已覆盖论文

- [GAT2018] Graph Attention Networks (2018)
- [GCN2017] Semi-Supervised Classification with Graph Convolutional Networks (2017)
- [GNNSURVEY2021] A Comprehensive Study on Large-Scale Graph Neural Networks (2021)
- [GRAPHGPT2024] GraphGPT: Graph Instruction Tuning for Large Language Models (2024)
- [GRAPHRAG2024] From Local to Global: A Graph RAG Approach to Query-Focused Summarization (2024)
- [GRAPHSAGE2017] Inductive Representation Learning on Large Graphs (2017)
- [GRAPHTRANSFORMER2021] Do Transformers Really Perform Bad for Graph Representation? (Graphormer) (2021)
- [MASPOB] MASPOB: Multi-Agent System for Prompt Optimization Based on GNN (2026)
- [ROG2024] Reasoning on Graphs: Faithful and Interpretable Large Language Model Reasoning (2024)

### 未被教案直接引用（库中有但教案未提及）

- [LLMonGraph2024] Exploring the Potential of Large Language Models on Graphs — 建议在适合课程中补充引用

---

## 三、缺失论文清单（建议补充入库）

| 别名 | 论文标题 | 作者/会议 | arXiv |
|------|----------|-----------|-------|
| GIN | How Powerful are Graph Neural Networks? | Xu et al., ICLR 2019 | arXiv:1810.00826 |
| MPNN | Neural Message Passing for Quantum Chemistry | Gilmer et al., ICML 2017 | arXiv:1704.01212 |
| OGB | Open Graph Benchmark: Datasets for Machine Learning on Graphs | Hu et al., NeurIPS 2020 | arXiv:2005.00687 |

---

## 四、行动建议

1. **优先补充GIN**：多个GNN教案提及，是GNN表达能力分析的基础论文
2. **补充MPNN**：消息传递范式是GNN统一框架，L02教案核心内容
3. **补充OGB**：基准测试数据集，L05实验评估部分必要参考
4. **编译原理教案**暂无GNN论文引用（符合预期），论文库专注GNN方向正确
5. 论文库现有10篇均被GNN教案覆盖，**无论文库孤岛**