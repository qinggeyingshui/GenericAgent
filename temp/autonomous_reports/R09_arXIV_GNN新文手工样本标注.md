# R09：arXiv GNN 新文手工样本标注（自主任务）

- 任务编号：R09  
- 任务类型：冲浪 / 文献追踪结构验证  
- 起止时间：2026-03-24（单次短任务）  
- 关联 TODO 项：`TODO.txt` 第 5 行  
  - 文本：`[ ] 冲浪 | arXiv GNN 新文手工选取样本并标注`

---

## 1. 任务目标与约束

**目标：**

1. 在 arXiv 上手动挑选少量近期 GNN 相关论文样本（2026 年为主），覆盖不同应用场景。
2. 将这些样本整理为结构化追踪表条目，用于验证本地 GNN 论文追踪表结构在真实数据上的可用性和可维护性。
3. 在不破坏既有脚本和数据格式的前提下，产出一个可迭代扩展的小样本集。

**关键约束：**

- 只能在本地工作目录及子目录下操作：
  - 本任务主要相关路径：
    - `./gnn_paper_tracker_template.md`（字段及表头模板）
    - `./gnn_papers/PAPERS.md`（现有 GNN 论文摘要集合）
    - `./gnn_paper_tracker_2026_samples.md`（本任务新建的追踪表）
    - `./autonomous_reports/`（自主任务报告与历史）
- 不直接修改 `../memory` 下文件（如需修改，必须用 `file_patch` 且遵守 memory SOP，本任务未涉及）。
- 遵守自主任务 SOP：
  - 从 TODO 未完成项中选择任务，本轮选择的是第 5 行 “arXiv GNN 新文手工选取样本并标注”。
  - 完成后必须：
    1. 写本报告；
    2. 在 `./autonomous_reports/history.txt` 顶部追加 R09 记录；
    3. 将 `TODO.txt` 第 5 行标记为已完成 `[x]`。

---

## 2. 实际操作过程

### 2.1 任务选择与环境确认

1. 检查 `TODO.txt`，在第 5 行发现未完成任务：
   - “冲浪 | arXiv GNN 新文手工选取样本并标注”。
2. 查看 `./autonomous_reports/history.txt`，确认上一任务为 R08，当前新任务编号为 R09。
3. 阅读 `./gnn_paper_tracker_template.md`，了解追踪表的字段与 Markdown 表头格式。
4. 阅读 `./gnn_papers/PAPERS.md`，确认现有内容以分节摘要为主，并无统一的表格追踪结构，避免直接将新表混入该文件而破坏已有结构。

### 2.2 arXiv 冲浪与样本抓取

1. 浏览器起始在某 arXiv PDF 页面，尝试直接获取标题/作者等元信息失败（PDF 视图不暴露常规 HTML meta）。
2. 通过 JavaScript 操作，将 PDF URL 转回 `/abs/` 摘要页，确认该论文与 GNN 无关，不纳入样本。
3. 从摘要页跳转到 arXiv 搜索结果页，使用的查询大致为：
   - `query="graph neural network"`，`searchtype=all`，按 `announced_date` 逆序，`size=50`。
4. 在搜索结果页使用 `web_execute_js`，对若干 `<li class="arxiv-result">` 节点执行 DOM 解析，提取字段：
   - `arxivId`
   - `title`（原始文本，含 `arXiv:xxxx [pdf,...]`）
   - `authors`（带有前缀 `Authors:` 和多行换行）
   - `abstract`（完整摘要文本）
   - `submitted`（提交/更新日期描述）
5. 返回结果以 Python 字典字符串形式保存，共抓取到 8 篇 2026 年 3 月附近的 GNN 相关论文。

### 2.3 本地解析与结构化整理

1. 使用 `code_run` 在本地执行 Python 脚本：
   - 通过 `ast.literal_eval` 将 JS 返回的字符串解析为 Python `dict` 列表。
   - 对 `authors` 字段去掉 `"Authors:\n"` 前缀和多余换行，将其压缩为一行作者名单。
   - 为每篇论文补充字段：
     - `title_clean`：从原始 `title` 中提炼出可读的英文标题。
     - `domain_tags`：粗粒度应用/领域标签。
     - `topic_tags`：更细粒度的技术标签。
     - `summary`：基于摘要写的一句中文摘要说明（简要）。
   - 为所有条目统一设置：
     - `year=2026`，`venue="arXiv"`，`source="arxiv"`；
     - `link="https://arxiv.org/abs/{arxivId}"`；
     - `reading_status="unread"`，`priority=3`；
     - `code_link` 留空，`notes` 留空；
     - `added_at="2026-03-24"`，`last_updated="2026-03-24"`。
2. 在 8 篇候选中，基于“多样应用 + 清晰 GNN 元素”的标准，选取 3 篇作为本次手工样本：

   1. **StreamTGN: Streaming Temporal Graph Neural Network Inference System**  
      - arXiv ID：2603.21090  
      - 类型：系统/工程，专注动态图（Temporal GNN）推理的可扩展性。  
      - 标签：
        - `domain_tags`: `representation; application-systems`
        - `topic_tags`: `temporal-gnn; scalability`
      - 摘要总结：提出 StreamTGN 流式 TGN 推理系统，将推理复杂度从 \(O(|V|)\) 降至 \(O(|A|)\)，显著加速动态图推理。

   2. **Graph Neural Network Surrogates for Knee Joint Contact Mechanics**  
      - arXiv ID：2603.21020  
      - 类型：应用型，生物力学/医疗场景，GNN 作为高成本仿真的代理模型。  
      - 标签：
        - `domain_tags`: `application-biomechanics`
        - `topic_tags`: `surrogate-model; mesh-gnn`
      - 摘要总结：比较拓扑扩散与全局路由等 GNN 变体在膝关节接触力学代理建模中的表现，指出混合模型在高应力区域重建上最优。

   3. **Physics-Informed Graph Neural Jump ODEs for Power Grid Cascading Failures**  
      - arXiv ID：2603.20838  
      - 类型：应用 + 物理约束建模，电力系统级联故障预测。  
      - 标签：
        - `domain_tags`: `application-power-systems; geometric`
        - `topic_tags`: `physics-informed-gnn; neural-ode`
      - 摘要总结：构建物理约束的 Graph Neural Jump ODE，用于电网级级联故障预测，在边/节点失效检测与负荷损失回归上显著优于 GCN 基线。

---

## 3. 追踪表文件设计与填充

### 3.1 与既有结构的兼容性考虑

- `./gnn_paper_tracker_template.md` 提供了标准字段和 Markdown 表格表头（包含示例行）。
- `./gnn_papers/PAPERS.md` 当前采用“按论文分节 + Abstract + Notes 占位”的形式，不是统一的追踪表。
- 为避免：
  - 破坏 `PAPERS.md` 的现有结构；
  - 影响可能依赖其结构的脚本或后续工具，
- 本任务选择**新建独立追踪表文件**：  
  - 路径：`./gnn_paper_tracker_2026_samples.md`  
  - 用途：专门存放 **2026 年 arXiv GNN 论文的手工样本条目**，兼顾实验性和可扩展性。

### 3.2 新建文件内容结构

新文件开头采用简短说明 + 表格，实际内容为：

```markdown
# GNN 论文追踪表：2026 手工样本

> 本文件由自动代理R09任务创建，用于存放从arXiv手工挑选的2026年GNN论文样本。

| id | title | authors | year | venue | domain_tags | topic_tags | source | link | code_link | reading_status | priority | summary | notes | added_at | last_updated |
|----|-------|---------|------|-------|------------|------------|--------|------|-----------|----------------|----------|---------|-------|----------|-------------|
| 2026-0001 | StreamTGN: Streaming Temporal Graph Neural Network Inference System | Lingling Zhang, Pengpeng Qiao, Zhiwei Zhang, Ye Yuan, Guoren Wang | 2026 | arXiv | representation; application-systems | temporal-gnn; scalability | arxiv | https://arxiv.org/abs/2603.21090 |  | unread | 3 | 提出StreamTGN流式TGN推理系统，将推理复杂度从O(|V|)降至O(|A|)，显著加速动态图推理。 |  | 2026-03-24 | 2026-03-24 |
| 2026-0002 | Graph Neural Network Surrogates for Knee Joint Contact Mechanics | Zhengye Pan, Jianwei Zuo, Jiajia Luo | 2026 | arXiv | application-biomechanics | surrogate-model; mesh-gnn | arxiv | https://arxiv.org/abs/2603.21020 |  | unread | 3 | 系统比较拓扑扩散与全局路由GNN，用于膝关节接触力学代理建模，发现混合模型在高应力区域重建上最优。 |  | 2026-03-24 | 2026-03-24 |
| 2026-0003 | Physics-Informed Graph Neural Jump ODEs for Power Grid Cascading Failures | Birva Sevak, Shrenik Jadhav, Van-Hai Bui | 2026 | arXiv | application-power-systems; geometric | physics-informed-gnn; neural-ode | arxiv | https://arxiv.org/abs/2603.20838 |  | unread | 3 | 提出物理约束的图神经Jump ODE用于电网级级联故障预测，在边/节点失效检测与负荷损失回归上大幅超越GCN基线。 |  | 2026-03-24 | 2026-03-24 |
```

说明：

- 字段顺序与模板保持一致，方便后续自动解析。
- `id` 采用年+递增编号：`2026-0001` 起步，便于未来追加样本。
- `summary` 和标签全部为**轻量级**、可在日后精读时补充详细 notes。

---

## 4. 结构可用性评价与后续建议

### 4.1 初步评价

- **优点：**
  - 结构紧凑：单行即可概览每篇论文的关键信息（题目、作者、领域、主题标签、链接、阅读状态、优先级）。
  - 与模板一致：字段、顺序都对齐 `gnn_paper_tracker_template.md`，便于未来写脚本做筛选/统计。
  - 可扩展：通过 `id` 递增和标签扩展，可以自然追加更多样本或其他年份文件。

- **局限：**
  - `summary` 目前为一句话中文概述，更接近“印象笔记”，不含实验细节或结果数值。
  - `domain_tags` / `topic_tags` 粒度仍较粗，可能不足以支撑复杂查询（如“纯理论 vs 应用”细分、图结构类型等）。
  - 与 `gnn_papers/PAPERS.md` 的摘要式记录尚未打通，存在“表格追踪”与“分节摘要”两种并行体系。

### 4.2 后续建议

1. **按年份分表**：将本文件命名规则固化，如 `gnn_paper_tracker_YYYY_samples.md` 或 `gnn_paper_tracker_YYYY.md`，本次 2026 作为样本年。
2. **标签规范化**：
   - 为 `domain_tags` 和 `topic_tags` 制定一个轻量级枚举或约定列表。
   - 日后可通过简单脚本检查标签拼写和复用情况。
3. **与摘要笔记联动**：
   - 未来可以考虑在 `PAPERS.md` 中，为表格里的 `id` 提供锚点或二级标题，形成“追踪表 -> 详细笔记”的跳转路径。
4. **半自动化抓取**：
   - 当前流程中，JS 抽取 + Python 解析已经证明可行；
   - 后续可以将本轮脚本整理成可重用工具，在用户确认筛选结果后自动写表格，减少手工编辑出错率。

---

## 5. 本轮任务状态与待办

**已完成：**

- 从 arXiv 选取 3 篇 2026 年 GNN 相关论文，覆盖系统、医疗/生物力学、电力系统等不同应用场景。
- 新建 `./gnn_paper_tracker_2026_samples.md` 文件，并写入 3 条结构化追踪表记录。
- 在本报告中记录了：
  - arXiv 冲浪与样本选择过程；
  - 字段设计与文件结构；
  - 对结构可用性的初步评价与改进建议。

**待完成（R09 收尾后续步骤）：**

1. 在 `./autonomous_reports/history.txt` 顶部追加一条 R09 任务记录，格式参考 R08。
2. 将 `TODO.txt` 中第 5 行任务标记为 `[x]`，表示本任务已经完成。
3. 视回合/轮次情况，按需将本轮经验写入长期记忆（结构拆分策略、独立追踪表文件命名等）。