# 图神经网络与大语言模型 - L04 GNN与LLM联合应用 教案

> 参考论文: MASPOB (Hong et al. 2026, arXiv:2603.02630); LLM on Graphs (Chen et al. 2024); Multi-Scale GNN+LLM for Text Classification (Song et al. 2025, arXiv:2511.05752)
> 前置课次: L01（GNN+LLM联合架构导论）, L02（GCN基础与MPNN）, L03（GAT与Transformer）

## 基本信息

- 课程名称：图神经网络与大语言模型
- 课次编码：L04
- 主题：GNN与LLM联合应用：GraphRAG、提示优化与结构增强文本理解
- 教学目标：
  - 理解GraphRAG（图检索增强生成）的核心思想与架构
  - 掌握GNN在提示优化（MASPOB）中的结构建模作用
  - 能够比较LLM-only方案与GNN+LLM联合方案的性能差异
  - 了解GNN+LLM在文本分类、行为检测、化学预测等领域的典型应用
  - 能够设计一个简单的GNN+LLM联合推理流水线
- 建议学时：2学时（100分钟）

## 教学内容概述

1. GraphRAG核心思想：将知识图谱/文档图结构引入RAG检索流程
2. GNN+LLM联合提示优化：MASPOB框架中UCB+GNN的协同机制
3. 结构增强文本理解：特征金字塔+GNN实现多尺度语义融合
4. 行为预测中的GNN优势：GNN vs 12个SOTA LLM的对比实验分析
5. 联合应用设计模式：串联（LLM特征提取→GNN推理）vs 并联（GNN+LLM双流融合）
6. 实践案例：从教学演示到真实部署的Gap分析

## 教学重难点

- 重点：GraphRAG的图结构检索机制；GNN如何将拓扑信息注入LLM推理
- 难点：串联 vs 并联融合架构的取舍；GNN+LLM联合训练时梯度传播问题

---

## 教学过程

### 1. 导入与回顾（10分钟）

- 复习L03：GAT注意力系数eij的softmax归一化；Graphormer的空间编码
- 提问：LLM在检索增强生成（RAG）中如何使用外部知识？图结构如何改善这一过程？
- 动机：传统RAG基于向量相似度检索，忽略文档/实体间关系；GraphRAG用图结构连接相关知识块

### 2. GraphRAG：图结构增强检索（20分钟）

#### 2.1 传统RAG的局限

- 向量检索：Top-K相似文本块，忽略跨块关系
- 知识碎片化问题：关联实体分散在不同文档，单次检索无法覆盖
- 引入：Microsoft GraphRAG将文档解析为实体-关系图，用图遍历补充检索

#### 2.2 GraphRAG核心流程

- Step1 索引阶段：LLM从文档中提取实体和关系 → 构建知识图谱 KG(V,E)
- Step2 社区检测：对KG运行Leiden算法，聚合相关实体族群
- Step3 查询阶段：用户问题 → 图检索（局部搜索/全局社区摘要）→ LLM生成答案
- 关键优势：多跳推理能力；全局主题摘要能力（传统RAG做不到）

#### 2.3 与GNN的关联

- GraphRAG使用LLM做图构建，用图算法做检索，下一步方向：用GNN替代图算法做端到端可微检索
- 学术前沿：G-Retriever（He et al. 2024）将GNN嵌入RAG管道实现可微图检索

### 3. MASPOB深入：GNN在提示优化中的作用（20分钟）

#### 3.1 问题设定

- MAS工作流：Planner→Researcher→Writer→Reviewer，各Agent有独立Prompt
- 目标：在有限预算内联合优化所有Agent的Prompt
- 挑战：Agent间的依赖关系（Planner的输出是Researcher的输入）使Prompt不可独立优化

#### 3.2 GNN建模MAS拓扑

- 将MAS工作流建模为有向图G(V,E)，节点=Agent，边=数据流依赖
- GNN对节点特征聚合：$h_i^{(l+1)} = \text{AGG}(h_i^{(l)}, \{h_j^{(l)}: j \in \mathcal{N}(i)\})$
- 输出：拓扑感知的Prompt语义表示，用于UCB置信度计算

#### 3.3 性能对比

- 与不含GNN的纯Bandit方法对比：GNN使搜索复杂度从O(K^N)降至O(K*N)
- 在MMLU/HotpotQA/ALFWorld等多基准上达到SOTA

### 4. 结构增强文本理解（15分钟）

#### 4.1 LLM+特征金字塔+GNN三阶段框架（Song et al. 2025）

- Stage1：LLM（如BERT/Llama）提取多层语境特征
- Stage2：特征金字塔（FPN）融合不同层次语义（全局主题+局部实体）
- Stage3：将融合特征转为图表示，GNN捕获语义单元间逻辑依赖关系
- 效果：在ACC/F1/AUC上优于单独使用LLM

#### 4.2 GNN vs LLM：何时GNN更优？

- 不文明行为检测实验（Chen et al. 2025）：GNN在结构丰富任务上超越12个SOTA LLM
- 推理成本：GNN推理成本显著低于大型LLM
- 规律：任务中存在显式关系结构时，GNN优于纯文本LLM

### 5. 联合应用设计模式与讨论（20分钟）

#### 5.1 两种主流融合范式

| 范式 | 描述 | 优点 | 缺点 |
|------|------|------|------|
| 串联(Pipeline) | LLM提取特征 -> GNN推理 | 模块独立，易部署 | 误差传播，不可端到端训练 |
| 并联(Dual-stream) | GNN和LLM并行处理，融合层合并 | 互补互强，联合优化 | 复杂度高，显存占用大 |

#### 5.2 工程取舍原则

- 数据规模小、关系结构显著 -> 优先GNN(成本低)
- 需要语义泛化、多模态 -> 优先LLM
- 二者互补场景 -> 先串联验证价值，再考虑并联端到端

#### 5.3 课堂讨论（10分钟）

- 场景1：学术论文推荐系统（引用图+摘要文本）-> 如何设计GNN+LLM方案？
- 场景2：医疗知识图谱问答 -> GraphRAG vs G-Retriever，哪个更适合？
- 场景3：社交网络谣言检测 -> 仅靠LLM文本判断 vs GNN传播结构，性能差距？

### 6. 总结与作业（15分钟）

#### 6.1 本课核心收获

- GraphRAG = LLM构图 + 图算法检索 + LLM生成（三段式）
- MASPOB = UCB Bandit + GNN拓扑建模 + 坐标上升分解（三层设计）
- GNN优势场景：结构信息显著、关系多跳推理、低推理成本要求
- L01-L04课程主线：GNN基础 -> 注意力机制 -> 与LLM融合 -> 实际应用

#### 6.2 作业

1. 阅读 Microsoft GraphRAG 论文（Edge et al. 2024），总结局部搜索与全局搜索的区别（200字以内）
2. 用PyG(PyTorch Geometric)实现一个2层GCN+BERT的串联文本分类模型（提供代码框架）
3. 思考题：如果MASPOB中的MAS拓扑是动态变化的（Agent数量运行时增减），GNN如何适应？

## 参考资料

- MASPOB: arXiv:2603.02630 (Hong et al. 2026)
- GraphRAG: Edge et al. 2024, "From Local to Global: A Graph RAG Approach to Query-Focused Summarization"
- G-Retriever: He et al. 2024, "G-Retriever: Retrieval-Augmented Generation for Textual Graph Understanding"
- Multi-Scale GNN+LLM: arXiv:2511.05752 (Song et al. 2025)
- Online Incivility GNN: arXiv:2512.07684 (Chen et al. 2025)

