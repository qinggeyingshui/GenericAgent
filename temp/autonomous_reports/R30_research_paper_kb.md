# R30 — research_paper_kb 搜索与筛选功能增强

## 任务来源
TODO#4: 激活 `local_skills/research_paper_kb` 并整合 `PAPERS.md`

## 完成内容

### 1. 新增 PAPERS.md 解析器 (`parse_papers_md`)
- 解析 `./gnn_papers/PAPERS.md` 中的论文条目
- 提取结构化字段：title, year, authors, arxiv_url, abstract, notes
- 基于 `## [YEAR] Title` 格式的正则匹配

### 2. 新增搜索引擎 (`search_papers`)
支持多维度筛选，可组合使用：
- **keyword**: 在标题+摘要中模糊搜索（不区分大小写）
- **year**: 精确年份匹配
- **year_from / year_to**: 年份范围筛选
- **author**: 按作者名搜索（不区分大小写）

### 3. 新增格式化输出 (`format_search_results`)
- 默认模式：显示年份、标题、作者、链接
- `--verbose` 模式：额外显示完整摘要

### 4. CLI 重构为子命令架构
| 子命令 | 功能 | 关键参数 |
|--------|------|----------|
| `fetch` | 从 arXiv 抓取论文 | `--query`, `--max_results` |
| `search` | 搜索已有论文 | `--keyword`, `--year`, `--author`, `--year_from`, `--year_to`, `--verbose` |
| `list` | 列出全部论文 | `--verbose` |

### 5. SKILL.md 文档更新
- 更新 one_line_summary 和 description
- 完整记录三个子命令的参数表和使用示例
- 更新典型用法流程

## 验证结果（6项全通过）
1. ✅ `list` — 列出全部 5 篇论文
2. ✅ `search --keyword "attention"` — 匹配 2 篇
3. ✅ `search --year 2025` — 匹配 4 篇
4. ✅ `search --author "Zhang"` — 匹配 1 篇
5. ✅ `search --year_from 2024 --year_to 2026 --verbose` — 匹配 5 篇（含摘要）
6. ✅ `--help` — 显示子命令帮助

## 修改文件
- `local_skills/research_paper_kb_like.py` — 新增 ~150 行（解析器+搜索+CLI重构）
- `local_skills/research-paper-kb/SKILL.md` — 更新文档