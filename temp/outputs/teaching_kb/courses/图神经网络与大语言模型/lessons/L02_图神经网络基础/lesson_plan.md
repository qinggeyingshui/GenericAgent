# 图神经网络与大语言模型 - L02 图神经网络基础 教案

> 参考论文: MASPOB arXiv:2603.02630 (2026); Multi-Scale GNN for Text arXiv:2511.05752 (2025)

## 基本信息
- 课程名称：图神经网络与大语言模型
- 课次编码：L02
- 主题：图神经网络基础（图结构定义、消息传递框架、GCN推导）
- 教学目标：
  - 掌握图的数学定义：邻接矩阵、度矩阵、图拉普拉斯
  - 理解消息传递神经网络（MPNN）统一框架及三步骤
  - 能够推导GCN层间传播公式并理解其谱域含义
  - 理解GCN与GAT、GraphSAGE的差异及适用场景
  - 关联L01：识别MASPOB中GNN模块如何对MAS工作流图编码
- 建议学时：2学时（100分钟）

## 教学内容概述
1. 图的数学基础：节点/边/邻接矩阵/度矩阵/图拉普拉斯
2. 为什么CNN不能直接处理图数据
3. MPNN统一框架：MESSAGE / AGGREGATE / UPDATE
4. GCN：从谱域滤波到层级传播公式推导
5. GCN变体：GAT（注意力）/ GraphSAGE（归纳）/ GIN（表达力）
6. 实践案例：文本图构建与GNN分类（arXiv:2511.05752）
7. GNN作为结构化编码器嵌入LLM管道

## 教学重难点
- 重点：MPNN三步骤统一理解；GCN传播公式推导（谱域→K=1简化）
- 难点：谱域到空域的数学跨越；加自环的必要性；直推式vs归纳式学习

## 教学过程

### 1. 导入与回顾（10分钟）
复习L01：MASPOB的GNN模块 = 建模Agent间依赖，生成拓扑感知prompt表示。
MAS工作流 = 有向图（节点=Agent，边=数据流）。
今天核心问题：GNN内部如何工作？

情境引入（按听众选一）：
- 药物发现：分子=图（原子=节点，化学键=边），预测药效
- 推荐系统：用户-物品交互=二部图，预测评分
- 代码分析：AST/调用图=有向图，预测漏洞

### 2. 图的数学基础（20分钟）

图 G=(V,E,X)：|V|=N节点，|E|=M条边，X∈R^(N×d)节点特征矩阵。

关键矩阵：
- 邻接矩阵 A∈{0,1}^(N×N)：A_ij=1当且仅当(i,j)∈E
- 度矩阵 D：对角阵，D_ii=sum_j A_ij
- 图拉普拉斯 L=D-A；归一化版 L_hat=I-D^(-1/2)AD^(-1/2)

课堂例题（三节点完全图A-B-C两两相连）：
  A=[[0,1,1],[1,0,1],[1,1,0]]，D=diag(2,2,2)，L=[[2,-1,-1],[-1,2,-1],[-1,-1,2]]

为什么CNN不适用图数据：
- 图像：规则网格，邻居数固定=8，平移不变性成立
- 图数据：不规则，邻居数可变，无固定顺序 → CNN不适用
- GNN设计原则：聚合函数必须对节点排列置换不变（permutation invariant）

### 3. MPNN消息传递框架（20分钟）

Gilmer et al.(2017) 将所有GNN统一为三步：

Step 1 — MESSAGE（消息生成）：
  m_ij^(l) = phi^(l)(h_i^(l), h_j^(l), e_ij)
  邻居j向节点i发送消息，由双方表示和边特征决定。

Step 2 — AGGREGATE（消息聚合）：
  M_i^(l) = Aggregate{m_ij^(l) : j∈N(i)}
  置换不变聚合：SUM（GIN）/ MEAN（GCN）/ MAX（GraphSAGE）

Step 3 — UPDATE（节点更新）：
  h_i^(l+1) = psi^(l)(h_i^(l), M_i^(l))
  当前表示 + 聚合消息 → 新节点嵌入。

感受野：l层后感知l-hop邻居。经验上2-4层最优，更深导致过平滑（Oversmoothing）。

### 4. 图卷积网络（GCN）推导（25分钟）

#### 4.1 谱域起点
图傅里叶变换：以图拉普拉斯L的特征向量矩阵U为正交基底。
谱域卷积：x *_G g_theta = U·g_theta(Lambda)·U^T x
问题：U的特征分解复杂度O(N^3)，大图不可行。

#### 4.2 Chebyshev近似（Hammond et al., 2011）
用K阶Chebyshev多项式近似，无需显式求U：
  g_theta(L_hat) ≈ sum_{k=0}^{K} theta_k·T_k(L_tilde)
  L_tilde = 2/lambda_max·L - I（归一化到[-1,1]）
复杂度降至O(K·|E|)，具备K跳局部性。

#### 4.3 GCN最终公式（Kipf & Welling, 2017）
取K=1，令lambda_max≈2，合并参数，对A_tilde=A+I做对称归一化：

  H^(l+1) = sigma( D_tilde^(-1/2) · A_tilde · D_tilde^(-1/2) · H^(l) · W^(l) )

符号说明：
| 符号 | 含义 | 作用 |
|------|------|------|
| A_tilde = A+I | 加自环邻接矩阵 | 保留自身信息 |
| D_tilde | A_tilde对应度矩阵 | 归一化基准 |
| D_tilde^(-1/2)·A_tilde·D_tilde^(-1/2) | 对称归一化 | 防大度节点主导 |
| W^(l) | 可学习权重矩阵 | 特征空间变换 |
| sigma | 非线性激活（ReLU）| 增加表达力 |

直觉：每节点新表示 = (自身+邻居特征的归一化均值) × 权重矩阵 + 激活。

#### 4.4 关联MASPOB
- GNN编码层 = GCN变体
- Agent i的表示 = 自身prompt语义嵌入 + 下游依赖Agent信息聚合
- 拓扑感知表示 → Bandit打分时自动感知全局依赖结构

### 5. GCN变体速览（15分钟）

| 模型 | 聚合函数 | 关键创新 | 局限性 |
|------|----------|----------|--------|
| GCN | 对称归一化均值 | 谱域简化，高效 | 直推式，新节点无法推断 |
| GAT | 注意力加权alpha_ij | 自适应邻居权重 | 计算开销稍高 |
| GraphSAGE | 采样+MEAN/LSTM/MAX | 归纳式，支持新节点 | 采样引入随机性 |
| GIN | 求和（epsilon可学习）| 表达力=WL图同构测试上界 | 图级需Readout |

论文关联：arXiv:2511.05752使用特征金字塔融合LLM特征后转化为图，
再用GNN捕获语义关系——GCN/GAT在NLP文本分类中的典型应用。

### 6. GNN在LLM中的接口设计（10分钟）

三种嵌入方式：
1. 前置编码器：GNN先处理图结构→节点嵌入作为LLM输入token
2. 并行融合：GNN和LLM分别处理→跨模态对齐层融合（arXiv:2511.05752方案）
3. 后置精炼：LLM生成初始表示→GNN利用图结构精炼（MASPOB方案）

### 7. 课堂小结与预告（10分钟）

核心结论：
- 图=(V,E,X)，三矩阵：邻接/度/拉普拉斯
- MPNN统一框架：MESSAGE → AGGREGATE → UPDATE
- GCN=谱域K=1简化+对称归一化+自环
- 变体：GAT（注意力）/ GraphSAGE（归纳）/ GIN（表达力上界）

预告L03：图注意力网络（GAT）详解+动态图上的时序GNN

---

## 板书设计

    图结构基础                    MPNN统一框架
    G=(V,E,X)                    Step1: m_ij=phi(h_i,h_j,e_ij)
    A: 邻接矩阵（0/1）            Step2: M_i=Aggregate{m_ij}
    D: 度矩阵（对角）              Step3: h_i'=psi(h_i,M_i)
    L=D-A: 拉普拉斯

    GCN传播公式（Kipf & Welling 2017）：
    H^(l+1) = sigma(D_tilde^(-1/2)·A_tilde·D_tilde^(-1/2)·H^(l)·W^(l))
                    ↑ 对称归一化        ↑ A+I（自环）            ↑ 可学习权重

## 参考资料

1. Kipf & Welling (2017). Semi-Supervised Classification with GCN. ICLR. arXiv:1609.02907
2. Gilmer et al. (2017). Neural Message Passing for Quantum Chemistry. ICML.
3. Velickovic et al. (2018). Graph Attention Networks. ICLR. arXiv:1710.10903
4. Hamilton et al. (2017). Inductive Representation Learning on Large Graphs. NeurIPS.
5. Xu et al. (2019). How Powerful are Graph Neural Networks? ICLR. arXiv:1810.00826
6. 本课程PAPERS.md: MASPOB(arXiv:2603.02630), Multi-Scale GNN(arXiv:2511.05752)

## 课后作业

1. 理论：推导完全图时GCN传播公式的退化形式？加自环前后区别？
2. 实现：用PyTorch Geometric实现2层GCN，在Cora数据集完成节点分类，报告测试准确率。
3. 思考：MASPOB将MAS工作流建模为有向图，方向性如何影响GCN聚合？
   （提示：有向图邻接矩阵不对称，对称归一化公式需如何修改？）
