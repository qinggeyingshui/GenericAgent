## R05_GNN论文追踪表结构设计

### 1. 任务与背景

- 任务编号：R05  
- 触发方式：用户离线自主行动，根据 `autonomous_operation_sop` 从现有 TODO 中选择一条执行。  
- 选定 TODO（第 1 行）：  
  > 产出 \| GNN论文跟踪本地数据结构设计 \| 设计一个适合长期维护的GNN论文追踪表结构（markdown/JSON），包含标题、作者、年份、领域标签（表征/几何/拓扑）、来源链接与阅读状态  

目标：在 `cwd=./` 下设计一个适合长期维护的 GNN 论文追踪表结构，给出：
- Markdown 表格模板；
- 一份 JSON schema，便于程序化读写与校验。

该结构将服务后续任务：如 arXiv 冲浪选样标注、自动化抓取站点信息、生成阅读纪要链接等。

---

### 2. 设计产物概览

本轮产出两个核心文件（均在 `./`）：

1. `gnn_paper_tracker_template.md`  
   - 含字段说明 + 可直接复制使用的 Markdown 表格模板；
   - 提供一条示例记录行。

2. `gnn_paper_tracker_schema.json`  
   - 描述单条 GNN 论文追踪记录的数据结构；
   - 采用 JSON Schema draft-07，可用于后续 Python/其它工具进行结构验证。

这两个文件均通过 `code_run` 自动生成，保证格式规范与字段一致。

---

### 3. 字段设计与取舍

综合 TODO 要求和后续任务需求，最终字段集合为：

- `id`：本地唯一标识（如 `2026-0001`），便于引用与排序。
- `title`：论文标题。
- `authors`：
  - Markdown 模板中用字符串字段（约定“姓, 名；姓, 名”分号分隔）；
  - JSON schema 中采用字符串数组 `authors: [ "Zhang, San", "Li, Si" ]`，便于程序处理。
- `year`：
  - 支持整数年份 1900–2100；
  - 或字符串 `"TBD"`，表示暂未确定。
- `venue`：会议/期刊/预印本来源，如 `NeurIPS 2024`、`ICLR 2025`、`arXiv`。
- `domain_tags`：
  - 高层领域标签，至少包括：
    - `representation`（表征 / Graph Foundation Models 等）  
    - `geometric`（几何 GNN，如 SE(3)、Lie 群等）  
    - `topological`（拓扑/同调相关方法）  
  - 支持扩展，如 `application-chem`、`application-recsys`。
  - 在 schema 中为字符串数组。
- `topic_tags`：
  - 细粒度主题标签，如 `graph-transformer`、`contrastive-learning`、`molecular-property`；
  - schema 中为字符串数组。
- `source`：
  - 来源类型枚举：`arxiv` / `conference` / `journal` / `thesis` / `other`；
  - 方便后续按来源过滤与统计。
- `link`：主阅读链接（arXiv/官方 PDF 等 URL）。
- `code_link`：代码仓库地址（如 GitHub），可为空。
- `reading_status`：
  - 状态枚举：
    - `unread`（未读）
    - `skimmed`（粗读/浏览）
    - `deep-read`（精读）
    - `revisited`（复盘/多次阅读）
- `priority`：
  - 整数 1–5，5 为最高阅读优先级。
- `summary`：
  - 1–3 句简要总结，便于快速回忆论文主旨。
- `notes`：
  - 更长笔记，与其他任务（如阅读纪要文件）的联系；
  - 可包含链接或简单 Markdown。
- `added_at`：
  - 加入追踪表日期字符串（YYYY-MM-DD）。
- `last_updated`：
  - 最近一次更新记录的日期字符串。

在 JSON schema 中，设置以下字段为 `required`：
- `id`, `title`, `authors`, `source`, `link`, `reading_status`, `priority`

这样既保证关键元数据完整，又不给备注类字段施加过多约束，便于早期快速录入。

---

### 4. 产出文件细节

#### 4.1 `gnn_paper_tracker_template.md`

主要结构：

1. 标题和用途说明：
   - 用于长期跟踪管理 GNN 论文；
   - 建议按任务/年份分文件使用。

2. 字段约定：
   - 以条目形式详细说明每个字段含义与填写规范；
   - 特别强调 `domain_tags`、`reading_status` 的推荐枚举值。

3. Markdown 表格模板：
   - 表头行与分隔行；
   - 一条完整示例记录，包括：
     - `id = 2026-0001`
     - 示例标题 `Graph Neural Networks for XYZ`
     - 示例作者列表
     - 典型 venue、domain_tags、topic_tags、source 等
   - 用户可复制该表至新文件并按行填充。

#### 4.2 `gnn_paper_tracker_schema.json`

核心要点：

- 使用 draft-07 schema；
- `type: "object"`，字段定义位于 `properties` 下；
- 通过 `oneOf` 对 `year` 支持整数年份或 `"TBD"`；
- 多个字段带有 `description`，便于人读和工具提示；
- `additionalProperties: false` 强制禁止临时字段漂移，防止结构意外膨胀。

---

### 5. 使用建议与后续扩展

**使用建议：**

1. 建议将 `gnn_paper_tracker_template.md` 复制为按主题或时间划分的具体清单：
   - 例如：`gnn_papers_2026_arxiv.md`、`gnn_papers_foundation_models.md`。
2. 后续 “冲浪 | arXiv GNN新文手工选取样本并标注” 任务可以：
   - 在浏览 arXiv 时人工选择若干论文；
   - 按字段规范填入 Markdown 表格；
   - 如有需要，再编写小脚本从 Markdown 转 JSON 并用 schema 校验。
3. “产出 | GNN论文阅读纪要模板” 任务可以与本结构联动：
   - 在 `notes` 或新增字段中记录对应阅读纪要文件路径或 ID。

**后续可改进点（留待未来任务）：**

- 为 `domain_tags` 提供更严格的枚举或受控词表；
- 增加 `task_links` 字段，用于与教案任务、自主任务 R 编号关联；
- 为 GUI 或脚本工具封装简单的录入/筛选界面。

---

### 6. 对记忆与 SOP 的建议（待用户审阅）

如需长期复用，建议在合适时机将以下信息写入记忆或相关 SOP（需用户批准后执行）：

- 在某个研究/教案相关 SOP 中简要记录：  
  “GNN 论文追踪统一使用 `gnn_paper_tracker_template.md` 与 `gnn_paper_tracker_schema.json` 的字段定义”。

---

### 7. 本轮 TODO 与 history 更新说明

- 已完成 TODO：  
  - `[ ] 产出 | GNN论文跟踪本地数据结构设计 | ...`  
  对应产出为上述两个文件。
- 计划 history 记录行（prepend 至 `./autonomous_reports/history.txt` 顶部）：  
  - `R05 | 2026-03-24 | 设计 | GNN论文追踪表结构 | 完成markdown模板与JSON schema用于长期GNN论文管理`

</file_content>
