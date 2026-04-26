```markdown
# R08 GNN 论文阅读纪要模板设计

## 1. 背景与目标

- 背景：
  - 已有工具：
    - `gnn_paper_tracker_schema.json`：定义了单篇 GNN 论文的结构化追踪字段（id/title/authors/source/link/...）。
    - `gnn_paper_tracker_template.md`：提供了“多论文追踪表”的 Markdown 表格模板，适合纵览与管理。
  - 缺口：
    - 尚无一份**针对单篇论文精读**的系统化“阅读纪要模板”，用于记录问题、方法、实验细节、优缺点、复现思路等。
- 目标：
  - 设计一份 **Markdown 版单篇 GNN 论文阅读纪要模板**，兼容已有追踪结构，又更关注研究内容与个人思考。
  - 模板应可与追踪表互相链接：追踪表中的 `notes` 字段可指向某次纪要文件。

---

## 2. 设计原则

1. **与 tracker 一致**：头部保留基本元数据字段（id/title/authors/venue/link/status 等），便于互相跳转和自动处理。
2. **突出研究问题与方法**：单独划分“研究问题 / 关键方法 / 数学形式化（若需要）”等模块。
3. **实验与结果细化**：记录数据集、指标、baseline 与 ablation，方便未来对照。
4. **优缺点与个人看法**：包括 strengths / weaknesses / personal takeaways。
5. **复现与工程视角**：专门预留实现笔记和潜在坑位记录。
6. **轻量可裁剪**：各部分可按需要简化；模板以“全量项”为主。

---

## 3. 单篇 GNN 论文阅读纪要模板（建议直接复制使用）

> 建议：以 `notes/gnn/` 或类似目录存放单篇纪要，每篇一个文件，
> 文件名可使用 `id_title_slug.md` 格式，例如：`2026-0001_graph-transformer-xyz.md`。

```markdown
# [id] 标题（可中英并列）

> 关联追踪表记录：`id = ...`  
> 追踪表文件：`gnn_papers/PAPERS.md` 或其他  
> 阅读日期：YYYY-MM-DD  
> 阅读状态：unread / skimmed / deep-read / revisited

---

## 0. 元信息（Meta）

- **Title**：  
- **Authors**：  
- **Year / Venue**：  
- **Source**：arxiv / conference / journal / thesis / other  
- **Domain Tags**：representation / geometric / topological / ...  
- **Topic Tags**：graph-transformer / contrastive-learning / molecular-property / ...  
- **Paper Link**：  
- **Code Link**：  
- **Priority**：1–5  
- **Tracker Entry Link**（可选）：指向追踪表所在行或文件

---

## 1. 研究问题（Problem）

- 这篇论文试图解决的**核心问题**是什么？用自己的话简述：
- 该问题在 GNN 领域/应用中的**重要性**：
  - 为什么值得做？
  - 和已有工作相比，新问题/新设定在哪？

---

## 2. 关键方法（Method）

### 2.1 总体思路（High-level Idea）

- 一句话版本：
- 稍长版本（2–5 句）：
  - 模型/方法的主要组成：
  - 直觉解释：

### 2.2 模型结构或算法细节

> 这一节可以用文字 + 简单图示描述结构，如：
> - 输入图 / 节点 / 边特征
> - 编码方式（消息传递、attention、transformer、position encoding 等）
> - 读出层 / 池化方式
> - 特别的 trick（如 normalization、regularization、pretrain 方式）

- **输入与表示**：
- **图层结构 / 消息传递机制**：
- **读出与预测头**：
- **训练目标 / 损失函数**：
- **关键技巧（Tricks）**：

### 2.3 公式与推导（可选）

> 仅在与数学细节强相关时填写。可用伪公式+文字说明。

- 关键公式/约束：
- 核心推导思路：

---

## 3. 实验设计（Experiments）

### 3.1 数据集与设置

- 使用的数据集：
  - 数据集1：任务/规模/特点
  - 数据集2：...
- 任务类型：node classification / graph classification / link prediction / recommendation / molecular property / ...
- 实验设置：
  - 训练/验证/测试划分：
  - 评估指标（accuracy, F1, ROC-AUC, ...）：
  - 超参数范围（如有）：

### 3.2 对比实验与消融（Baselines & Ablations）

- 对比基线（Baselines）：
  - 列出主要 baseline 模型及其特点：
- 消融实验（Ablation）：
  - 哪些组件/损失/模块做了消融？结论如何？

### 3.3 结果与结论

- 主要结果表格/图表的结论（用文字总结即可）：
  - 在什么场景/数据集上表现最好？
  - 性能提升的幅度与显著性？
- 作者给出的解释是否合理？有无可疑之处？

---

## 4. 优点与不足（Strengths & Weaknesses）

### 4.1 优点（Strengths）

- 方法/设计上的亮点：
- 实验上的优点（如设置全面、对比充分）：
- 对领域可能的长远影响：

### 4.2 不足（Weaknesses / Limitations）

- 方法上的潜在问题或适用性限制：
- 实验上的不足（如数据集/指标单一，缺少 ablation）：
- 论文写作上的模糊点、阅读困难点：

---

## 5. 个人收获与启发（Takeaways & Ideas）

- 我从这篇论文中学到的最重要的 1–3 点：
- 可以迁移到自己工作的思路/模块：
- 新的 research ideas 或后续可以尝试的方向：
  - idea 1：
  - idea 2：

---

## 6. 复现与工程笔记（Implementation Notes）

> 阅读代码或尝试实现时记录。

- 官方代码仓库结构（大致模块划分）：
- 训练/推理流程要点：
- 复现过程中遇到的问题（数据、环境、随机性等）：
- 需要特别注意的参数/实现细节：

---

## 7. 关联与对比（Related Work & Positioning）

- 与哪几篇核心工作最相近？
  - 论文A：主要思想 vs 本文不同点：
  - 论文B：...
- 本文在该系列工作中的位置（例如：更通用、更高效、或专注某一类应用）：

---

## 8. 总结（Overall Verdict）

- 一句话评价：
- 是否值得推荐给他人阅读？（是/否+原因）
- 对自己项目/研究的直接帮助程度（1–5）：
```

---

## 4. 与现有追踪表的衔接建议

1. **从追踪表跳转到纪要**：
   - 在 `gnn_paper_tracker_template.md` 中的 `notes` 字段填入当前纪要文件的相对路径，如：
     - `notes = "详见 notes/gnn/2026-0001_graph-transformer-xyz.md"`
2. **从纪要回指追踪表**：
   - 在纪要顶部“元信息（Meta）”部分加入：
     - `Tracker Entry Link`：可为文件路径+表格行说明，或未来的更结构化链接。
3. **自动化潜力（留作后续任务）**：
   - 可考虑未来编写脚本，根据 `gnn_paper_tracker_schema.json` 生成/校验纪要头部元信息的一致性。

---

## 5. 任务状态

- 本模板已满足 TODO 第4行对“GNN论文阅读纪要模板”的需求：
  - 覆盖问题/方法/实验/优缺点/复现笔记等关键维度；
  - 与现有追踪表（schema + markdown）在元信息层面保持兼容；
  - 适合直接复制到新文件使用。
- 后续收尾步骤（按 autonomous_operation_sop 执行）：
  1. 在 `./autonomous_reports/history.txt` 顶部 prepend 一条 R08 记录；
  2. 在 `./TODO.txt` 中将第4行标记为 `[x]`。
```