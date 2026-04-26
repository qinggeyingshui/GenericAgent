# 图神经网络与大语言模型 - L03 图注意力网络与Transformer 教案

> 参考论文: GAT (Velickovic et al. 2018, arXiv:1710.10903); Graphormer (Ying et al. 2021, arXiv:2106.05234)
> 前置课次: L01（GNN+LLM联合架构）, L02（GCN推导与MPNN框架）

## 基本信息
- 课程名称：图神经网络与大语言模型
- 课次编码：L03
- 主题：图注意力网络（GAT）与Transformer注意力机制
- 教学目标：
  - 理解Scaled Dot-Product Attention的数学原理
  - 掌握GAT注意力系数计算与多头聚合机制
  - 能够推导Self-Attention公式并与GCN传播公式对比
  - 理解Graphormer如何将Transformer迁移到图结构
  - 关联L02：将GAT定位为MPNN框架中的可学习聚合函数
- 建议学时：2学时（100分钟）

## 教学内容概述
1. 注意力机制动机：为什么需要可学习的聚合权重？
2. Scaled Dot-Product Attention：Q/K/V三矩阵推导
3. Multi-Head Self-Attention：并行多头与输出拼接
4. GAT：基于LeakyReLU的注意力系数eij推导
5. GAT与GCN对比：动态权重 vs 固定归一化权重
6. Graphormer：空间编码/边编码/中心性编码
7. 应用案例：GAT在节点分类(Cora/CiteSeer)的性能对比

## 教学重难点
- 重点：Q/K/V机制；GAT注意力系数softmax归一化
- 难点：多头注意力语义解释；Graphormer如何编码图结构

---

## 教学过程

### 1. 导入与回顾（10分钟）

复习L02：GCN传播公式 H^(l+1) = σ(D̃^(-1/2) Ã D̃^(-1/2) H^(l) W^(l))

核心问题：GCN的聚合权重由图结构（度）固定，无法学习——邻居贡献不应该相同吗？

情境引入：
- 人类阅读时会"注意"关键词，不均等处理每个词
- 推荐系统中，用户历史行为权重不应相同
- 分子图中，不同化学键对药效的贡献差异显著

今日目标：让GNN学会"选择性关注"重要邻居。

---

### 2. 注意力机制基础（20分钟）

#### 2.1 Scaled Dot-Product Attention

给定查询 Q∈R^(n×d_k), 键 K∈R^(m×d_k), 值 V∈R^(m×d_v):

  Attention(Q, K, V) = softmax(QK^T / sqrt(d_k)) · V

- 除以 sqrt(d_k)：防止点积值过大导致softmax梯度消失
- softmax：将相似度归一化为概率分布（注意力权重和为1）

**直觉**：Q问"我需要什么"，K答"我有什么"，点积相似度决定关注程度，V提供实际内容。

#### 2.2 Multi-Head Attention

  MultiHead(Q,K,V) = Concat(head_1, ..., head_h) W^O
  head_i = Attention(Q W_i^Q, K W_i^K, V W_i^V)

- h个头并行，每头关注不同子空间的语义关系（句法/语义/指代等）
- 拼接后线性投影到目标维度

**板书练习**：d_model=512, h=8时，每头d_k=64，总参数量 = 4 × d_model^2 ≈ 1M。

---

### 3. 图注意力网络 GAT（25分钟）

#### 3.1 注意力系数推导

对节点i与邻居j，计算注意力系数：

  e_ij = LeakyReLU( a^T · [W·h_i || W·h_j] )

其中：
- W ∈ R^(d'×d)：共享线性变换，将节点特征投影到新空间
- a ∈ R^(2d')：可学习注意力向量（参数量极小）
- ||：向量拼接（concatenation）
- LeakyReLU：负值区域斜率0.2，防止死神经元

归一化（softmax over 邻域 N_i，含自环）：

  α_ij = exp(e_ij) / Σ_{k∈N_i∪{i}} exp(e_ik)

节点特征更新：

  h_i' = σ( Σ_{j∈N_i∪{i}} α_ij · W · h_j )

关键性质：
- α_ij 是节点对(i,j)特征的函数，随输入动态变化
- 无需事先知道全图结构（归纳学习友好）

#### 3.2 多头GAT

中间层（拼接）：

  h_i' = Concat_{k=1}^{K} σ( Σ_{j∈N_i} α_ij^k · W^k · h_j )

输出层（平均，防止维度爆炸）：

  h_i' = σ( (1/K) · Σ_{k=1}^{K} Σ_{j∈N_i} α_ij^k · W^k · h_j )

#### 3.3 GAT vs GCN 对比表

| 维度 | GCN | GAT |
|------|-----|-----|
| 聚合权重 | 固定（度归一化） | 可学习（注意力） |
| 归纳能力 | 弱（依赖全图结构） | 强（节点特征驱动） |
| 计算复杂度 | O(|E|·d·d') | O(N·d'^2 + |E|·d') |
| 适用场景 | 同质图，度分布均匀 | 异质特征，边重要性差异大 |
| 可解释性 | 低 | 高（α_ij可视化） |

**与L02联系**：GAT = MPNN框架中 MESSAGE 步骤用注意力加权，AGGREGATE 步骤用softmax归一化求和。

---

### 4. Graphormer：图上的Transformer（20分钟）

#### 4.1 核心问题

标准Transformer处理序列（全连接注意力）；图有结构约束。
问题：如何在保留Transformer表达能力的同时，编码图的拓扑信息？

#### 4.2 三种结构编码

**中心性编码**：节点度（入度/出度）反映重要性：
  h_i^(0) = x_i + z^-(deg^-(i)) + z^+(deg^+(i))
z^-, z^+ 是可学习的度嵌入向量。

**空间编码**：最短路径距离 SPD(i,j) 作为注意力偏置：
  A_ij = (Q_i · K_j^T) / sqrt(d) + b_{SPD(i,j)}
b 为可学习标量偏置，不可达节点 SPD=-1（特殊标记）。

**边特征编码**：最短路径上边特征加权平均加入注意力分数：
  c_ij = (1/N) * sum_n( x_{e_n}^T * w_n )

#### 4.3 性能表现

- OGB-LSC（分子属性预测）：Graphormer获2021年KDD Cup冠军
- 证明：图结构信息可通过空间/位置编码完全注入Transformer

---

### 5. 应用案例与实验（15分钟）

#### 5.1 节点分类基准

Cora（2708节点，5429边，7类，1433维词袋特征）：

| 模型 | 准确率 |
|------|--------|
| GCN（Kipf 2017） | 81.5% |
| GAT（8头） | 83.0% ± 0.7% |

CiteSeer（3327节点，4732边，6类）：GCN 70.3% vs GAT 72.5% ± 0.7%

#### 5.2 PyG实现骨架（GATConv）

    from torch_geometric.nn import GATConv
    conv1 = GATConv(in_ch, hid_ch, heads=8, dropout=0.6)
    conv2 = GATConv(hid_ch*8, out_ch, heads=1, concat=False, dropout=0.6)
    # forward: dropout -> elu(conv1) -> dropout -> conv2

引导提问：为什么conv2用concat=False？dropout加在注意力权重上的作用？

---

### 6. 总结与展望（10分钟）

本节核心：注意力 = 可学习的动态聚合权重

| 模型 | 注意力类型 | 输入 |
|------|-----------|------|
| GCN | 无（结构固定） | 图结构 |
| GAT | 节点特征驱动 | 节点特征对 |
| Transformer | 全局序列注意力 | 全序列Q/K/V |
| Graphormer | 图结构增强注意力 | 图+节点+边特征 |

下节预告：L04将探讨GNN与大语言模型的深度融合——图结构遇到预训练语言模型。

---

## 作业与思考题

1. **推导**：证明当 α_ij = 1/|N_i| 时，GAT退化为GCN（忽略自环差异）。
2. **实现**：用纯PyTorch实现单头GAT注意力系数计算（不依赖PyG）。
3. **思考**：Graphormer的空间编码能否处理有向图？需要什么修改？
4. **扩展**：阅读GAT原文（arXiv:1710.10903），找出本教案简化的技术细节。

## 板书/PPT结构建议

- Slide 1: 标题 + L02回顾（GCN公式一行）
- Slide 2: 动机——固定权重的局限性（图示）
- Slide 3-4: Self-Attention推导（Q/K/V矩阵图示）
- Slide 5-6: GAT注意力系数推导（公式逐步展开）
- Slide 7: GAT vs GCN 对比表
- Slide 8-9: Graphormer三种编码（图示）
- Slide 10: 实验结果 + PyG代码骨架
- Slide 11: 总结表 + 作业
