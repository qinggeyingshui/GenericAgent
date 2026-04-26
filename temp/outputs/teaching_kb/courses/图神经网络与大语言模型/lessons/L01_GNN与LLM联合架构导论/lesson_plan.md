# 图神经网络与大语言模型 - L01 GNN与LLM联合架构导论 教案

> **来源论文**: MASPOB: Bandit-Based Prompt Optimization for Multi-Agent Systems with Graph Neural Networks
> **arXiv**: http://arxiv.org/abs/2603.02630v1
> **作者**: Zhi Hong, Qian Zhang et al. (2026)

## 基本信息

- 课程名称：图神经网络与大语言模型
- 课次编码：L01
- 主题：GNN与LLM联合架构导论
- 教学目标：
  - 理解图神经网络（GNN）的基本概念与信息传播机制
  - 了解大语言模型（LLM）在多智能体系统（MAS）中的角色
  - 掌握GNN与LLM结合的核心动机：结构化关系建模 + 语言理解能力
  - 能够描述基于Bandit的Prompt优化框架（MASPOB）的工作流程
- 建议学时：2 学时

## 教学内容概述

- 图神经网络回顾：节点/边/图结构，消息传递机制
- 大语言模型在多智能体系统中的部署模式
- Prompt优化的必要性：MAS工作流不可改、性能对prompt高度敏感
- MASPOB框架：Bandit算法 + GNN依赖建模 + 无标注黑盒优化
- GNN+LLM联合架构的应用前景

## 教学重难点

- 重点：GNN消息传递机制 vs LLM上下文理解机制的互补性
- 难点：Bandit优化在无标注场景下的探索-利用权衡；GNN如何建模Agent间依赖关系

## 教学过程

### 1. 导入（10分钟）

- 提问：如果有一个由多个LLM组成的AI团队（多智能体），如何在不修改代码的情况下提升其性能？
- 展示：一个MAS工作流示意图（Planner → Researcher → Writer → Reviewer）
- 引入：Prompt是唯一可调旋钮，但Agent间存在依赖——GNN能建模这种依赖

### 2. 背景知识（20分钟）

#### 2.1 图神经网络基础

- 图的定义：节点（Agents/概念）、边（依赖/关系）、属性
- 消息传递：$h_v^{(l+1)} = \text{UPDATE}(h_v^{(l)}, \text{AGG}(\{h_u^{(l)} : u \in \mathcal{N}(v)\}))$
- 典型架构：GCN / GAT / GraphSAGE 一句话对比

#### 2.2 LLM作为MAS认知核心

- LLM的能力边界：推理、规划、生成
- MAS中的角色分工：每个Agent = LLM + System Prompt + 工具集
- 关键瓶颈：工作流固定，Prompt是唯一优化变量

### 3. 论文精读：MASPOB框架（30分钟）

#### 3.1 问题定义

- 输入：MAS工作流图 G = (V, E)，每个节点 v 有当前 prompt p_v
- 目标：最大化整体系统输出质量 f(p_1,...,p_n)
- 挑战：
  1. 样本效率：标注数据稀缺
  2. 黑盒优化：无梯度信息
  3. Agent间依赖：改一个prompt影响下游所有Agent

#### 3.2 MASPOB解法

- **GNN模块**：对MAS工作流图进行编码，捕获Agent间依赖，生成每个节点的上下文向量
- **Bandit模块**：将Prompt优化建模为多臂赌博机问题，用UCB/Thompson Sampling平衡探索-利用
- **优化循环**：GNN预测 → Bandit选择候选prompt → 评估 → 更新

#### 3.3 实验亮点

- 在多个MAS基准任务上优于基线（固定prompt / 随机搜索 / 贪心优化）
- 样本效率是关键优势：相同评估次数下，MASPOB效果更好

### 4. 讨论与延伸（20分钟）

- GNN+LLM联合架构的三种范式：
  1. GNN辅助LLM（结构化检索增强）
  2. LLM辅助GNN（自然语言特征生成）
  3. 双向协同（MASPOB类）
- 思考题：如果MAS工作流是动态变化的（边会增删），如何修改MASPOB？

### 5. 课堂小结（10分钟）

- GNN建模关系 + LLM处理语言 → 互补优势
- MASPOB = 依赖感知 + 样本高效 + 黑盒友好的Prompt优化框架
- 预告：下节课探讨GNN用于文本分类（论文#4：多尺度特征融合）

## 板书设计

```
MAS工作流图
  Planner ──→ Researcher ──→ Writer
                              ↓
                           Reviewer
         GNN编码依赖关系
         Bandit优化Prompt
```

## 参考资料

1. MASPOB论文: arXiv:2603.02630 (2026)
2. GNN综述: Scarselli et al., "The Graph Neural Network Model" (2009)
3. Prompt优化综述: Zhou et al., "Large Language Models Are Human-Level Prompt Engineers" (2022)

## 作业布置

1. 阅读 MASPOB 摘要（见 gnn_papers/PAPERS.md），用自己的话描述其核心创新点（200字以内）
2. 思考题：在编译原理课程中，编译器各阶段（词法→语法→语义）是否也构成一个有向图？如果用GNN建模，节点和边各代表什么？
3. 扩展（选做）：检索arXiv上1篇"GNN+RAG"论文，简述其思路