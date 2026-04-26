# Task4 报告：GNN论文概念知识图谱

## 任务目标
从GNN论文库（17篇）提取关键概念和共现关系，用NetworkX构建知识图谱，pyvis生成可交互HTML，支持年份/领域/关键词过滤。

## 交付成果
- **脚本**：`temp/tools/knowledge_graph.py`（282行）
- **HTML可视化**：`temp/autonomous_reports/gnn_knowledge_graph.html`（56.2KB）
- **CLI用法**：`python knowledge_graph.py [--year 2024] [--venue NeurIPS] [--keyword GNN] [--output path]`

## 验收结果
| 指标 | 要求 | 实际 |
|------|------|------|
| 节点数 | >50 | **86** ✅ |
| 边数 | - | **257** |
| 研究簇数 | ≥3 | **6** ✅ |
| HTML可视化 | 可打开 | **56.2KB** ✅ |

## 图谱结构
- 🔵 **论文节点**（17个）：蓝色，含标题/年份/会议tooltip
- 🟠 **关键词节点**（50个）：橙色，大小按出现频次缩放
- 🟢 **年份节点**（7个）：绿色
- 🟣 **会议节点**（12个）：紫色

## 识别的研究簇（greedy_modularity社区检测）
1. **GNN基础方法簇**（15节点）：核心=GNN, message passing
2. **图分类任务簇**（13节点）：核心=node classification, GCN, GraphSAGE
3. **LLM+图知识簇**（9节点）：核心=LLM, knowledge graph, RoG
4. 簇4（5节点）、簇5（4节点）、簇6（4节点）

## 遇到的问题与解决
1. **f-string嵌套引号**：`c["size"]`在f-string中报SyntaxError → 提取为临时变量
2. **ROOT_DIR路径错误**：tools/下脚本需上移两级才能找到gnn_papers/ → 修复为`dirname(dirname(BASE_DIR))`
3. **连通分量只有2簇**：大部分关键词互相共现在同一连通分量 → 改用`greedy_modularity_communities`，得到6个有意义的簇

## Task1 放弃记录（待审）
- **原因**：sentence-transformers依赖torch（未安装），pip安装超时120s，用户指示放弃
- **建议**：如需语义搜索，可手动安装torch后重启Task1，或考虑用`gensim`的Doc2Vec替代

## 记忆更新建议
- 新增坑：`tools/`子目录下的脚本，ROOT_DIR需要`dirname(dirname(__file__))`才能找到GenericAgent根目录
- 新增能力：NetworkX + pyvis 知识图谱生成（86节点，greedy_modularity社区检测）
