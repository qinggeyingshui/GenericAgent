
---
_Collected at: 2026-03-24 05:43:37 UTC_
_Query: `ti:"graph neural network" AND all:"large language model"`_

## [2026] MASPOB: Bandit-Based Prompt Optimization for Multi-Agent Systems with Graph Neural Networks
- Authors: Zhi Hong, Qian Zhang, Jiahang Sun, Zhiwei Shang, Mingze Kong, Xiangyi Wang, Yao Shu, Zhongxiang Dai
- arXiv: http://arxiv.org/abs/2603.02630v1

### Abstract
Large Language Models (LLMs) have achieved great success in many real-world applications, especially the one serving as the cognitive backbone of Multi-Agent Systems (MAS) to orchestrate complex workflows in practice. Since many deployment scenarios preclude MAS workflow modifications and its performance is highly sensitive to the input prompts, prompt optimization emerges as a more natural approach to improve its performance. However, real-world prompt optimization for MAS is impeded by three key challenges: (1) the need of sample efficiency due to prohibitive evaluation costs, (2) topology-induced coupling among prompts, and (3) the combinatorial explosion of the search space. To address these challenges, we introduce MASPOB (Multi-Agent System Prompt Optimization via Bandits), a novel sample-efficient framework based on bandits. By leveraging Upper Confidence Bound (UCB) to quantify uncertainty, the bandit framework balances exploration and exploitation, maximizing gains within a strictly limited budget. To handle topology-induced coupling, MASPOB integrates Graph Neural Networks (GNNs) to capture structural priors, learning topology-aware representations of prompt semantics. Furthermore, it employs coordinate ascent to decompose the optimization into univariate sub-problems, reducing search complexity from exponential to linear. Extensive experiments across diverse benchmarks demonstrate that MASPOB achieves state-of-the-art performance, consistently outperforming existing baselines.

### Notes
- Problem: 多智能体系统中prompt优化面临评估代价高、拓扑耦合、搜索空间指数爆炸三大挑战。
- Method: UCB Bandit框架平衡探索利用；GNN编码MAS有向工作流图，生成拓扑感知prompt语义表示；坐标上升将联合优化分解为线性复杂度子问题。
- Contributions: 首个将GNN结构先验引入MAS prompt优化的框架；搜索复杂度从指数降至线性；在多基准上达到SOTA。
- Threats / Limitations: 依赖固定MAS拓扑（不支持运行时动态图）；UCB假设奖励平稳分布，非平稳场景待验证。

## [2025] Learning Continuous Solvent Effects from Transient Flow Data: A Graph Neural Network Benchmark on Catechol Rearrangement
- Authors: Hongsheng Xing, Qiuxin Si
- arXiv: http://arxiv.org/abs/2512.19530v1

### Abstract
Predicting reaction outcomes across continuous solvent composition ranges remains a critical challenge in organic synthesis and process chemistry. Traditional machine learning approaches often treat solvent identity as a discrete categorical variable, which prevents systematic interpolation and extrapolation across the solvent space. This work introduces the \textbf{Catechol Benchmark}, a high-throughput transient flow chemistry dataset comprising 1,227 experimental yield measurements for the rearrangement of allyl-substituted catechol in 24 pure solvents and their binary mixtures, parameterized by continuous volume fractions ($\% B$). We evaluate various architectures under rigorous leave-one-solvent-out and leave-one-mixture-out protocols to test generalization to unseen chemical environments.   Our results demonstrate that classical tabular methods (e.g., Gradient-Boosted Decision Trees) and large language model embeddings (e.g., Qwen-7B) struggle with quantitative precision, yielding Mean Squared Errors (MSE) of 0.099 and 0.129, respectively. In contrast, we propose a hybrid GNN-based architecture that integrates Graph Attention Networks (GATs) with Differential Reaction Fingerprints (DRFP) and learned mixture-aware solvent encodings. This approach achieves an \textbf{MSE of 0.0039} ($\pm$ 0.0003), representing a 60\% error reduction over competitive baselines and a $>25\times$ improvement over tabular ensembles. Ablation studies confirm that explicit molecular graph message-passing and continuous mixture encoding are essential for robust generalization. The complete dataset, evaluation protocols, and reference implementations are released to facilitate data-efficient reaction prediction and continuous solvent representation learning.

### Notes
- Problem: 有机合成中，溶剂成分连续变化时的反应产率预测困难；传统ML将溶剂视为离散类别，无法内插外推。
- Method: 构建Catechol Benchmark（1227条实验数据，24种纯溶剂及混合物）；设计GAT+差分反应指纹（DRFP）+连续混合溶剂编码的混合GNN架构。
- Contributions: 首个连续溶剂空间基准数据集；MSE 0.0039，比竞争基线降低60%，比表格集成方法提升25倍；消融研究证明图消息传递和连续混合编码均不可缺少。
- Threats / Limitations: 仅验证catechol重排一类反应；真实部署需更多反应类型泛化验证。

## [2025] When Large Language Models Do Not Work: Online Incivility Prediction through Graph Neural Networks
- Authors: Zihan Chen, Lanyu Yu
- arXiv: http://arxiv.org/abs/2512.07684v2

### Abstract
Online incivility has emerged as a widespread and persistent problem in digital communities, imposing substantial social and psychological burdens on users. Although many platforms attempt to curb incivility through moderation and automated detection, the performance of existing approaches often remains limited in both accuracy and efficiency. To address this challenge, we propose a Graph Neural Network (GNN) framework for detecting three types of uncivil behavior (i.e., toxicity, aggression, and personal attacks) within the English Wikipedia community. Our model represents each user comment as a node, with textual similarity between comments defining the edges, allowing the network to jointly learn from both linguistic content and relational structures among comments. We also introduce a dynamically adjusted attention mechanism that adaptively balances nodal and topological features during information aggregation. Empirical evaluations demonstrate that our proposed architecture outperforms 12 state-of-the-art Large Language Models (LLMs) across multiple metrics while requiring significantly lower inference cost. These findings highlight the crucial role of structural context in detecting online incivility and address the limitations of text-only LLM paradigms in behavioral prediction. All datasets and comparative outputs will be publicly available in our repository to support further research and reproducibility.

### Notes
- Problem: 在线不文明行为（毒性/攻击/人身攻击）检测中，现有方法准确率和效率均有限；LLM仅依赖文本语义，忽视评论间关系结构。
- Method: 将每条用户评论建模为节点，文本相似度定义边；引入动态调整注意力机制自适应平衡节点特征与拓扑特征的聚合权重。
- Contributions: 提出GNN框架检测维基百科三类不文明行为；在多指标上超越12个SOTA LLM；推理成本显著低于LLM方案；证明结构上下文对行为预测的关键作用。
- Threats / Limitations: 仅在英文维基百科数据集验证；文本相似度构图可能引入噪声边；跨平台迁移效果待验证。

## [2025] Multi-Scale Feature Fusion and Graph Neural Network Integration for Text Classification with Large Language Models
- Authors: Xiangchen Song, Yulin Huang, Jinxu Guo, Yuchen Liu, Yaxuan Luan
- arXiv: http://arxiv.org/abs/2511.05752v1

### Abstract
This study investigates a hybrid method for text classification that integrates deep feature extraction from large language models, multi-scale fusion through feature pyramids, and structured modeling with graph neural networks to enhance performance in complex semantic contexts. First, the large language model captures contextual dependencies and deep semantic representations of the input text, providing a rich feature foundation for subsequent modeling. Then, based on multi-level feature representations, the feature pyramid mechanism effectively integrates semantic features of different scales, balancing global information and local details to construct hierarchical semantic expressions. Furthermore, the fused features are transformed into graph representations, and graph neural networks are employed to capture latent semantic relations and logical dependencies in the text, enabling comprehensive modeling of complex interactions among semantic units. On this basis, the readout and classification modules generate the final category predictions. The proposed method demonstrates significant advantages in robustness alignment experiments, outperforming existing models on ACC, F1-Score, AUC, and Precision, which verifies the effectiveness and stability of the framework. This study not only constructs an integrated framework that balances global and local information as well as semantics and structure, but also provides a new perspective for multi-scale feature fusion and structured semantic modeling in text classification tasks.

### Notes
- Problem: 文本分类中，单一LLM特征难以同时建模全局语义与局部结构；特征尺度单一导致复杂语义语境下性能受限。
- Method: LLM提取深层语境特征→特征金字塔机制融合多尺度语义（全局+局部）→将融合特征转为图表示，GNN捕获语义单元间潜在关系与逻辑依赖→Readout+分类头输出预测。
- Contributions: 提出LLM+特征金字塔+GNN三阶段混合框架；在ACC/F1/AUC/Precision四指标上优于现有模型；鲁棒性对齐实验验证框架稳定性。
- Threats / Limitations: 计算成本较高（三阶段串联）；图构建策略依赖人工设计，泛化性待验证。

## [2025] Causal Graph Neural Networks for Healthcare
- Authors: Munib Mesinovic, Max Buhlan, Tingting Zhu
- arXiv: http://arxiv.org/abs/2511.02531v4

### Abstract
Healthcare artificial intelligence systems routinely fail when deployed across institutions, with documented performance drops and perpetuation of discriminatory patterns embedded in historical data. This brittleness stems, in part, from learning statistical associations rather than causal mechanisms. Causal graph neural networks address this triple crisis of distribution shift, discrimination, and inscrutability by combining graph-based representations of biomedical data with causal inference principles to learn invariant mechanisms rather than spurious correlations. This Review examines methodological foundations spanning structural causal models, disentangled causal representation learning, and techniques for interventional prediction and counterfactual reasoning on graphs. We analyse applications demonstrating clinical value across psychiatric diagnosis through brain network analysis, cancer subtyping via multi-omics causal integration, continuous physiological monitoring with mechanistic interpretation, and drug recommendation correcting prescription bias. These advances establish foundations for patient-specific Causal Digital Twins, enabling in silico clinical experimentation, with integration of large language models for hypothesis generation and causal graph neural networks for mechanistic validation. Substantial barriers remain, including computational requirements precluding real-time deployment, validation challenges demanding multi-modal evidence triangulation beyond cross-validation, and risks of causal-washing where methods employ causal terminology without rigorous evidentiary support. We propose tiered frameworks distinguishing causally-inspired architectures from causally-validated discoveries and identify critical research priorities making causal rather than purely associational claims.

### Notes
- Problem: 医疗AI系统跨机构部署时性能骤降并放大历史数据偏见；根源在于学习统计相关而非因果机制。
- Method: 结合结构因果模型（SCM）、解耦因果表示学习与图上的干预预测/反事实推理，学习跨分布不变机制；综述在精神病诊断、癌症分型、生理监测、药物推荐等场景的因果GNN应用。
- Contributions: 系统综述因果GNN方法论基础与临床应用；提出Patient-Specific因果数字孪生愿景（GNN机制验证+LLM假设生成）；给出区分「因果启发架构」vs「因果验证发现」的分层框架。
- Threats / Limitations: 计算需求高，阻碍实时部署；验证需多模态证据三角，超出交叉验证；存在「因果洗白」风险（术语滥用无严格证据）。

