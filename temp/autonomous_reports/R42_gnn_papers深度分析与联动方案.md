# R42 — gnn_papers 目录深度分析与联动方案

**日期**: 2026-03-25
**类型**: 探测+分析
**编号**: R42

## 摘要

完整探测 `./gnn_papers/` 目录结构与内容，评估与 `research_paper_kb` / `teaching_kb` 的联动潜力，设计三层数据流架构。

## 产出

- **分析报告**: `./gnn_papers/gnn_papers_analysis.md`

## 数据盘点

- **论文数量**: 5 篇（GNN+LLM 交叉研究，2025–2026）
- **检索式**: `ti:"graph neural network" AND all:"large language model"`
- **主题**: Prompt优化 / 文本分类 / 内容审核 / 化学反应预测 / 因果医疗
- **Notes 状态**: 全部待填

## 联动评估

| 目标系统 | 可行性 | 优先级 | 方案 |
|---------|--------|--------|------|
| `research_paper_kb_like.py` | 高 | 高 | 批量 add 导入5篇论文 |
| `teaching_kb`（编译原理） | 低 | 低 | 待AI课程模块建立后再联动 |

## 数据流设计

```
[采集层] arXiv → gnn_papers/PAPERS.md
[处理层] 批量导入脚本 → research_paper_kb_like.py
[应用层] search / list / export
```

## 待执行

1. 编写批量导入脚本（TODO#6 gnn_kb联动任务的核心内容）
2. 填写 PAPERS.md 中 5 篇论文的 Notes

## 验收

- 生成 gnn_papers_analysis.md ✔
- 数据盘点完成 ✔
- 联动方案设计完成 ✔