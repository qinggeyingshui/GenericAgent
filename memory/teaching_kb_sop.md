# teaching_kb_sop（教案知识库与任务协同摘要）

> 本文件记录教案助手知识库 `teaching_kb/` 的核心结构约定，以及与 TODO / 自主任务 / 定时任务 的协同规则。细节结构见 temp 项目内的 R06 报告。

## 1. 教案知识库物理位置与基本结构

- 教案知识库根目录（在当前 temp 项目内）：
  - `./teaching_kb/`
    - `courses/`：按课程组织资源（如 `编译原理/` 等）
      - `课程名/`
        - `syllabus/`：教学大纲
        - `lessons/`：按课次组织教案与素材
          - `LXX_主题/`：课次目录（如 `L02_词法分析/`）
            - `lesson_plan.md`：该课次教案主体（Markdown）
            - `materials_index.md`：该课次素材清单（Markdown）
            - `slides/`：PPT 课件
            - `materials/`：代码、图片、PDF 等补充素材
            - `exercises.md` / `assignment_LXX.md`：练习与作业（可选）
        - `assignments/`：课程级作业与实验（可选）
        - `exam/`：试卷与复习资料（可选）

- 已有示例（用于参考结构）：
  - `teaching_kb/courses/编译原理/lessons/L02_词法分析/`
    - 含 `lesson_plan.md`、`materials_index.md`、`slides/示例PPT`

> 详细设计与示例内容，见：  
> `./autonomous_reports/R06_教案助手知识库结构规划.md`

## 2. TODO 与自主任务协同规则（教案相关）

1. 任何“教案相关”的 TODO 条目，应在描述中**显式包含目标路径或对象**，例如：
   - 具体文件：  
     `teaching_kb/courses/编译原理/lessons/L02_词法分析/lesson_plan.md`
   - 整个课次：  
     `teaching_kb/courses/编译原理/lessons/L03_语法分析/`（新建骨架）

2. 自主任务（依照 `autonomous_operation_sop`）执行教案相关 TODO 时：
   - 只在 `./teaching_kb/` 下新建或更新教案与素材索引等文件；
   - 遵循上述目录与命名规范（课程/课次/资源类型）；
   - 在 `./autonomous_reports/` 下生成对应 RXX 报告，并更新 `./autonomous_reports/history.txt`；
   - 不直接修改 `../memory` 目录。

3. 对教案内容或结构的大改，建议先按 `plan_sop` 在 temp 项目内建立局部 plan（如 `plan_teaching_kb/plan.md`），再执行。

## 3. 定时任务与 teaching_kb 的使用方式

> 定时任务遵循 `scheduled_task_sop`，与自主任务逻辑上独立。

对 `./teaching_kb/`，定时任务的推荐职责是**只读扫描与统计**，不直接修改 autonomous_reports 体系：例如：

- 定期扫描所有课程与课次：
  - 找出缺失 `lesson_plan.md` 或 `materials_index.md` 的课次目录；
  - 汇总“未完成教案列表”或“最近更新的课次列表”。
- 将统计结果输出到定时任务体系指定报告路径（如 `sche_tasks/` 下），**不直接编辑**：
  - `./autonomous_reports/history.txt`
  - 已有的 RXX 报告正文

## 4. 经验要点与避坑

- **路径约定是协同关键**：  
  TODO 必须带上 `teaching_kb/...` 具体路径或至少课次目录名，否则自主任务难以定位准确目标。
- **读写边界**：
  - 教案内容的新增/修改：由自主任务或用户手动完成；
  - teaching_kb 的统计与巡检：交给定时任务，只读。
- **结构扩展**：
  - 新增课程：在 `teaching_kb/courses/` 下创建新目录，内部结构参考 `编译原理` 示例；
  - 新增课次：在对应课程的 `lessons/` 下按 `LXX_主题` 命名创建目录，并至少放置 `lesson_plan.md` 与 `materials_index.md` 骨架。
- **详细规范位置**：  
  如需查阅更详细的章节划分、字段规范示例，优先阅读：  
  `./autonomous_reports/R06_教案助手知识库结构规划.md`（位于 temp/autonomous_reports/ 内）。

## 5. PPT生成管道架构

- 管道流程：`lesson_plan.md` → `lesson2ppt.py`(解析+配置生成) → `ppt_config.json` → `generate_ppt.py`(路由) → `ppt_utils.py`(渲染) → `.pptx`
- 关键文件：
  - `teaching_kb/lesson2ppt.py`：教案解析 + slide配置生成（管道入口）
  - `ppt_lab/generate_ppt.py`：slide类型路由分发
  - `ppt_lab/ppt_utils.py`：各版式渲染实现
- 已支持slide类型：title, toc, section, content, icon_cards, comparison, step_cards, highlight_content, timeline, stats, chart, ending
- 避坑：
  - `step_cards`的steps必须是`[{title, points}]`格式，不能传纯字符串
  - `highlight_content`用`highlight_text`+`sub_points`键，非`content`
  - `stats`的stats必须是`[{icon, value, label}]`格式
  - Windows终端GBK编码不支持emoji，print避免用✅等符号
  - `lesson2ppt.py`解析教学过程子标题必须为`### 数字. 名称`格式（如`### 1. 导入`），否则不被识别为独立slide，页数不足
  - `ppt_lab/`目录可能不存在(R109验证)，此时lesson2ppt.py整条管道不可用；应退回直接用python-pptx写脚本：R(矩形)+T(文本框)+ChartData图表，分段写文件再subprocess执行
- PPT导出Markdown工具：`teaching_kb/ppt2md.py`
  - 用法：`python ppt2md.py <input.pptx> [output.md|--stdout]`
  - 坑：`prs.slides`不支持切片`[:n]`，必须用`enumerate(prs.slides)`迭代

## 6. 批量导入功能

**工具**：`batch_import_toolkit.py`

**功能**：从文件夹批量导入markdown教案到teaching_kb，自动创建课次目录结构

**用法**：
```bash
# 预览模式（不实际操作）
python batch_import_toolkit.py <源目录> <课程名> --dry-run

# 实际导入
python batch_import_toolkit.py <源目录> <课程名>
```

**支持的文件名格式**：
- `L01_主题.md` / `L01-主题.md`
- `01_主题.md` / `01-主题.md`
- `lesson_01_主题.md` / `lesson_01-主题.md`

**自动操作**：
- 解析文件名提取课次编号和主题
- 创建 `teaching_kb/courses/{课程}/lessons/LXX_{主题}/` 目录
- 复制文件为 `lesson_plan.md`
- 自动生成 `materials_index.md` 骨架
- 跳过已存在的课次（防止覆盖）

**验收**：支持5种命名格式，导入5+个文件，自动创建目录结构

## 6. 语义检索与推荐

**工具**：`teaching_kb/semantic_search.py`

**功能**：
- 基于TF-IDF的语义搜索
- 相关文档推荐
- 支持中文分词（jieba）

**使用示例**：
```python
from teaching_kb.semantic_search import SemanticSearch

ss = SemanticSearch()
ss.build_index()  # 构建索引

# 搜索
results = ss.search("图神经网络", top_k=5)
for r in results:
    print(f"[{r['score']:.3f}] {r['title']}")

# 推荐
recs = ss.recommend(doc_id=0, top_k=5)
```

**验收**：支持语义搜索和相关推荐，检索准确率>80%

## 7. 多模态检索

**工具**：`temp/tools/multimodal_search.py`

**功能**：
- 图片检索（基于文件名/标签）
- 表格检索（CSV/Excel文件）
- 公式检索（LaTeX/Markdown中的数学公式）
- OCR文字提取（预留接口）
- 向量化搜索（预留接口）

**使用示例**：
```python
import sys
sys.path.append('./tools')
import multimodal_search as mms

# 搜索图片
images = mms.search_images('./teaching_kb', keyword='python')

# 搜索表格
tables = mms.search_tables('./teaching_kb', keyword='成绩')

# 搜索公式
formulas = mms.search_formulas('./teaching_kb', keyword='损失函数')

# 多模态综合搜索
results = mms.multimodal_search('./teaching_kb', '数据分析')
print(f"图片: {len(results['images'])}个")
print(f"表格: {len(results['tables'])}个")
print(f"公式: {len(results['formulas'])}个")

# 保存结果
mms.save_search_results(results, './search_results.json')
```

**扩展功能**（需安装额外库）：
```python
# OCR文字提取（需要 pytesseract）
text = mms.extract_text_from_image('./image.png')

# 文本向量化（需要 sentence-transformers）
embedding = mms.vectorize_text('这是一段文本')
```

**验收**：支持图片/表格/公式检索，OCR和向量化接口预留

## 8. 智能问答与FAQ生成

**工具**：`temp/tools/kb_qa.py`

**功能**：
- 基于知识库的智能问答
- 自动生成FAQ文档
- 关键概念提取

**使用示例**：
```python
import sys
sys.path.append('./tools')
import kb_qa

# 智能问答
qa = kb_qa.KnowledgeBaseQA()
answers = qa.answer_question("图神经网络", top_k=3)
for ans in answers:
    print(f"[{ans['score']:.3f}] {ans['source']}")
    print(ans['content'])

# 批量问答
questions = ["什么是GNN？", "如何训练模型？"]
results = qa.batch_answer(questions)

# FAQ生成
gen = kb_qa.FAQGenerator()
concepts = gen.extract_key_concepts(10)  # 提取10个关键概念
faq = gen.generate_faq(concepts, questions_per_concept=2)
gen.save_faq(faq, "./faq.md")

# 快捷函数
answers = kb_qa.quick_answer("编译原理")
faq_path = kb_qa.quick_faq("./teaching_faq.md")
```

**验收**：支持智能问答和FAQ自动生成，基于语义搜索返回相关内容

---
[skill_mapping]
category: knowledge_management
skill: knowledge_organization
tools: teaching_kb/, temp/tools/multimodal_search.py, temp/tools/kb_qa.py
[/skill_mapping]

## [record_on_use]
执行完本SOP后，调用以下命令记录使用情况：
```python
import sys
sys.path.append('../memory')
from autonomous_operation_sop.helper import record_skill_usage
record_skill_usage('teaching_kb_sop.md')
```
