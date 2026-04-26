# local_skills 目录深度探测清单

**日期**: 2026-03-25
**类型**: 探测
**编号**: R40

## 目录结构

```
./local_skills/
├── research_paper_kb_like.py   (13,222 bytes)  ← 主脚本
└── research-paper-kb/
    └── SKILL.md                 (5,169 bytes)   ← 技能描述文档
```

## 脚本详情

### research_paper_kb_like.py

| 字段 | 值 |
|------|-----|
| **key** | `local/research-paper-kb` |
| **状态** | 可用 (实测 returncode=0) |
| **类型** | 论文知识库 (arXiv 拉取 + 本地持久化) |
| **autonomous_safe** | true |
| **依赖** | 标准库（urllib, xml, re, os） + 外网 arXiv API |
| **输出文件** | `./gnn_papers/PAPERS.md` |

#### 子命令接口

| 子命令 | 功能 | 关键参数 |
|--------|------|---------|
| `fetch` | 从 arXiv API 拉取论文追加到 PAPERS.md | `--query`(必填) `--max_results`(默认5) |
| `search` | 在 PAPERS.md 中搜索 | `--keyword` `--year` `--year_from` `--year_to` `--author` `--verbose` |
| `list` | 列出所有已收录论文 | `--verbose` |

#### 实测结果

```
list 命令: 返回 5 篇论文，returncode=0
当前知识库: 5 篇 GNN 相关论文 (2025-2026)
```

#### Notes 格式（已预留但未填）

每篇论文预留 Problem / Method / Contributions / Threats 四个字段，待 LLM 后续填充。

## 能力树评估

| 维度 | 评价 |
|------|------|
| 覆盖度 | 仅 1 个脚本，能力树极为有限 |
| 质量 | 代码质量高，有完整 SKILL.md 文档 |
| 可扩展性 | 设计为 agentskill 风格，易扩展更多技能 |
| 盲区 | 缺少 Web 搜索、图像处理、数据分析等常用技能 |

## 建议

1. `local_skills/` 目前只有 1 个技能，属于**早期占位**状态
2. 可考虑将已有的 `disk_analyzer.py`、`cleanup_executor.py` 等打包为 local_skills
3. GNN 论文知识库已有 5 篇入库，可配合 TODO#5 gnn_papers 联动使用
4. 建议后续 Batch 扩充：代码分析技能、网页摘要技能、PDF 解析技能