# gnn_papers 深度分析报告

**生成时间**: 2026-03-25
**来源**: `./gnn_papers/PAPERS.md`

## 一、数据盘点

### 目录结构

```
gnn_papers/
  PAPERS.md  (9858 bytes)
```

### 论文集元信息

- **采集时间**: 2026-03-24 05:43:37 UTC
- **检索式**: `ti:"graph neural network" AND all:"large language model"`
- **论文总数**: 5 篇
- **时间跨度**: 2025–2026
- **Notes 状态**: 全部待填（Problem/Method/Contributions/Threats 均空）

### 论文清单

| # | 年份 | 标题摘要 | arXiv |
|---|------|---------|-------|
| 1 | 2026 | MASPOB: 多智能体系统的 Bandit+GNN Prompt 优化 | 2603.02630 |
| 2 | 2025 | Catechol Benchmark: GNN 预测连续溶剂效应（化学/流动化学） | 2512.19530 |
| 3 | 2025 | GNN 框架检测在线不文明行为（胜过12个LLM） | 2512.07684 |
| 4 | 2025 | GNN+LLM 多尺度特征融合文本分类 | 2511.05752 |
| 5 | 2025 | 因果图神经网络在医疗领域（+ LLM假设生成） | 2511.02531 |

### 主题分布

- **LLM+GNN 协同架构**: #1, #4
- **GNN 替代/优于 LLM**: #3
- **GNN 应用于特定领域**: #2（化学）, #5（医疗）
- **核心技术交叉**: Prompt优化, 文本分类, 在线内容审核, 化学反应预测, 因果推理

---

## 二、与现有系统的联动潜力评估

### 2.1 与 `local_skills/research_paper_kb_like.py` 的联动

**现状**: `research_paper_kb_like.py` 是一个本地论文知识库脚本，已验证可用，当前存有 5 篇论文记录（见 R40）。

**联动方案**:

```
gnn_papers/PAPERS.md
      ↓ 解析
  5篇论文结构化数据（标题/作者/摘要/arXiv链接）
      ↓ 导入
  research_paper_kb_like.py → add 命令
      ↓ 结果
  统一检索入口（search/list/export）
```

**可行性**: 高。PAPERS.md 已有结构化格式，`add` 接口接受标题+摘要+元信息，可直接批量导入。
**价值**: 将 GNN+LLM 领域论文纳入统一知识库，支持后续语义搜索和引用。

### 2.2 与 `teaching_kb`（编译原理课程）的联动

**现状**: teaching_kb 目前只有编译原理课程（L01+L02），不含 GNN/AI 相关课程。

**潜在联动**:
- 若未来扩展 AI/深度学习课程，gnn_papers 可作为课程参考文献库
- 论文 #4（多尺度GNN文本分类）和 #1（MAS Prompt优化）具有较高教学价值
- 短期内无直接联动必要，优先级低

### 2.3 数据流设计

```
[采集层] arXiv API / 手动收集
    → gnn_papers/PAPERS.md（结构化存储）

[处理层] 批量导入脚本（待建）
    → research_paper_kb_like.py add 接口

[应用层]
    ├── search: 语义检索论文
    ├── list: 浏览知识库
    ├── export: 导出引用列表
    └── （未来）teaching_kb 参考文献关联
```

---

## 三、待填工作 & 改进建议

| 优先级 | 工作项 | 说明 |
|--------|--------|------|
| 高 | 填写 PAPERS.md 中 5 篇论文的 Notes | Problem/Method/Contributions/Threats |
| 高 | 编写批量导入脚本将 PAPERS.md 导入 research_paper_kb | 约50行Python |
| 中 | 扩充 gnn_papers 采集，增加更多检索维度 | 如 GNN+RAG, GNN+agent |
| 低 | 与 teaching_kb 建立引用关联 | 待AI课程模块建立后再联动 |

---

## 四、验收结论

- **数据盘点**: 完成（5篇论文、1个PAPERS.md、全部字段已解析）
- **联动潜力评估**: 完成（与research_paper_kb高度可联动，与teaching_kb低优先级）
- **数据流设计**: 完成（三层架构：采集→处理→应用）
- **验收**: 生成gnn_papers_analysis.md ✔