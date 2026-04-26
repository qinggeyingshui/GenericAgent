# 图神经网络与大语言模型 - L05 图神经网络前沿 教案

> 参考论文: GraphSAGE arXiv:1706.02216; HAN arXiv:1903.07293; EvolveGCN arXiv:1902.10191; TGN arXiv:2006.10637; HGT arXiv:2003.01332

## 基本信息
- 课程名称：图神经网络与大语言模型
- 课次编码：L05
- 主题：图神经网络前沿（Scalable GNN、异质图、时序GNN、大规模部署）
- 教学目标：
  - 理解大规模图训练的核心挑战（邻域爆炸、内存瓶颈、通信开销）
  - 掌握三类可扩展采样策略：节点采样/子图采样/重要性采样的原理与权衡
  - 理解异质图建模范式：元路径、HAN、HGT模型核心设计
  - 掌握时序GNN两类框架：离散快照TGNN与连续事件TGNN
  - 了解工业级GNN部署策略：在线推理、增量训练、特征缓存
  - 关联L01-L04：在大规模MAS场景中选型合适的前沿GNN变体
- 建议学时：2学时（100分钟）

## 教学内容概述
1. 大规模图的挑战：为什么mini-batch GNN不简单
2. 可扩展GNN：GraphSAGE邻域采样、Cluster-GCN、GraphSAINT
3. 异质图神经网络：元路径定义、HAN注意力、HGT Transformer
4. 时序图神经网络：离散TGNN（EvolveGCN）、连续TGNN（TGAT/TGN）
5. 工业级部署：图采样系统、增量训练、特征服务器
6. 综合案例：大规模学术引用图异质建模与社交网络时序链路预测
7. 与LLM结合的前沿方向：图Tokenization、GraphRAG扩展

## 教学重难点
- 重点：三类采样策略的方差偏差权衡；HGT异质注意力机制；TGN记忆模块
- 难点：连续时间动态图的时间编码原理；工业部署的系统级优化思维

## 教学过程

### 1. 导入与回顾（10分钟）

复习L02-L04核心：L02 MPNN框架（消息传递三步骤）；L03 GNN在知识图谱上的应用；L04 GNN与LLM的联合架构。

今天核心问题：当图有10亿节点、100亿边，或节点和边有多种类型，或图随时间演化时，标准GCN/GAT如何扩展？

动机情境（选一）：
- 微信社交图：10亿用户节点，需要实时推荐，如何训练GNN？
- 学术引用网络：作者/论文/期刊三类节点，如何建模异质关系？
- 金融交易图：每秒数万笔交易，如何捕捉时序异常模式？

### 2. 可扩展GNN：三类采样策略（25分钟）

#### 2.1 邻域爆炸问题

标准GCN需要Full-batch：所有节点同时参与前向传播，内存O(N)，对亿级图不可接受。
K层GNN的感受野爆炸：若平均度数d，K=3层时需聚合d^3个邻居节点，d=10时即1000个节点。
Mini-batch面临挑战：节点的计算依赖其邻居，邻居又依赖其邻居，无法简单切片。

#### 2.2 节点级采样：GraphSAGE（Hamilton et al. 2017）

核心思想：每层随机采样固定数量k个邻居，打破邻域爆炸，将感受野固定为k^L。
传播公式：h_v^l = sigma(W · CONCAT(h_v^(l-1), AGG({h_u^(l-1) : u in sample(N(v), k)})))
聚合函数：均值聚合/最大池化/LSTM聚合（三种，性能递增，计算代价也递增）
优势：归纳式学习，新节点无需重训；内存消耗固定O(batch × k^L)。
代价：引入采样方差，梯度估计噪声较大；k过小时信息损失显著。

#### 2.3 子图级采样：Cluster-GCN（Chiang et al. 2019）

核心思想：用图聚类算法（METIS）将图预划分为C个子图，每批次在子图内做Full-batch GCN。
优势：子图内边保留完整，无邻域截断；矩阵运算密集，GPU利用率高。
代价：跨子图边被完全忽略，可能导致聚类边界处信息传递中断；需预处理聚类（一次性开销）。
改进：随机组合多个小子图为一个batch，增加跨簇边的覆盖率。

#### 2.4 基于重要性采样：GraphSAINT（Zeng et al. 2020）

核心思想：按归一化的节点/边重要性权重采样子图，通过无偏估计器（方差减少技术）修正梯度。
三种采样器：节点采样器、边采样器、随机游走采样器，对应不同图结构特征。
无偏性保证：引入归一化系数消除采样概率的影响，使期望梯度等于Full-batch梯度。
优势：理论保证无偏；实践中方差显著小于GraphSAGE；适用于各类图结构。

三类方法对比：
- GraphSAGE：节点邻居粒度，有偏，适用于归纳学习和新节点实时推断
- Cluster-GCN：子图粒度，跨簇有偏，适用于同质密集图的高效训练
- GraphSAINT：加权子图粒度，无偏，适用于高精度需求的通用场景

### 3. 异质图神经网络（20分钟）

#### 3.1 异质图定义
异质图 G=(V,E,tau,phi)：|A|+|R|>2。学术图：A={作者,论文,期刊}，R={写作,发表于,引用}。

#### 3.2 元路径
元路径：节点类型序列定义的复合语义关系。APA（合著），APVPA（同期刊作者）。
将异质图按元路径投影为多个同质子图，各自跑GNN后融合。局限：需人工设计。

#### 3.3 HAN：异质图注意力网络
两层注意力：节点级（同元路径邻居加权）+ 语义级（不同元路径重要性softmax加权）。
缺陷：依赖人工元路径；跨类型特征空间投影损失信息。

#### 3.4 HGT：异质图Transformer
为每种(源类型,边类型,目标类型)三元组学习独立Q/K/V矩阵。
Att(s→t) = softmax(K_phi(s)·Q_phi(t)^T / sqrt(d)) · mu[tau(s),phi,tau(t)]
优势：无需手工元路径，端到端学习异质关系，支持任意类型节点特征维度。

### 4. 时序图神经网络（20分钟）

#### 4.1 两类动态图范式
离散时间动态图（DTDG）：快照序列G_1,...,G_T，间隔固定。适用：金融季报图、学术年度引用图。
连续时间动态图（CTDG）：事件流{(u,v,t,e)}，时间戳连续。适用：社交互动、电商购买、金融转账。

#### 4.2 EvolveGCN（离散TGNN）
RNN演化GCN权重矩阵：W^(t) = GRU(W^(t-1), H^(t-1))，H^(t) = GCN(A^(t), X^(t); W^(t))。
适用：图结构变化是主信号的场景。局限：细粒度时序信息丢失。

#### 4.3 TGN（连续TGNN）
四模块：记忆模块（每节点状态向量s_v） / 消息函数 / 记忆更新GRU / 时间感知图注意力嵌入。
时间编码：phi(dt) = [cos(w1*dt), sin(w1*dt), ..., cos(wd*dt), sin(wd*dt)]，可学习频率w。
是连续时序GNN的标准基线，链路预测和节点分类均达SOTA。

### 5. 工业级部署（10分钟）

三大挑战：大规模图存储（百亿边分布式）/ 在线推理延迟（<10ms K跳采样）/ 增量训练。
应对策略：特征缓存（预计算高频节点嵌入）/ 计算图压缩预取 / 异步分布式训练。

### 6. 综合案例与练习（10分钟）

案例A：OAG学术图（2亿节点、16亿边）——论文领域分类与合著预测。
讨论：为什么选HGT而非标准GCN？为什么用GraphSAINT而非Full-batch？

案例B：微博转发时序分析——预测1小时内病毒式扩散。
方法：TGN + 时间感知注意力，记忆模块压缩用户历史行为。

### 7. 与LLM结合的前沿方向（5分钟）

图Tokenization：将图结构序列化为Token序列输入LLM（Graph-Llama/GraphGPT）。
GraphRAG扩展：知识图谱+GNN多跳推理路径增强LLM结构化推理。
MAS前沿（关联L01）：时序MAS图（Agent动态加入/离开）/ 异质MAS图（不同角色异质关系）。

## 课后作业

1. （理论）对比GraphSAGE与GraphSAINT在方差控制上的本质差异，各举一个最适用场景。
2. （设计）给定一个电影知识图谱（节点：电影/演员/导演/类型；边：出演/执导/属于），
   设计元路径列表，并说明HAN和HGT在此场景上的优劣。
3. （实现）用PyG的TemporalData和TGNMemory，在JODIE数据集上复现TGN链路预测基线。
4. （思考）在MASPOB框架中，如果Agent节点会动态加入和退出，应选DTDG还是CTDG方案？理由？

## 参考资料

- Hamilton et al. (2017). Inductive Representation Learning on Large Graphs. NeurIPS.
- Chiang et al. (2019). Cluster-GCN: An Efficient Algorithm for Training Deep and Large GCNs. KDD.
- Zeng et al. (2020). GraphSAINT: Graph Sampling Based Inductive Learning Method. ICLR.
- Wang et al. (2019). Heterogeneous Graph Attention Network. WWW.
- Hu et al. (2020). Heterogeneous Graph Transformer. WWW.
- Pareja et al. (2020). EvolveGCN: Evolving Graph Convolutional Networks. AAAI.
- Rossi et al. (2020). Temporal Graph Networks for Deep Learning on Dynamic Graphs. arXiv:2006.10637.
- He et al. (2024). A Survey on Graph Neural Networks for Large-Scale Graphs. arXiv:2312.09147.
