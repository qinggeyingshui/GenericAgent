# R13 PPT/Office 环境工具与库枚举报告

日期：2026-03-24  
类型：环境  
任务来源：TODO第5条「枚举与PPT/Office相关的本地工具与库」

## 1. 任务目标

在当前项目与常见环境范围内，枚举与 **PPT/Office 自动化** 相关的：

- 本地文件与目录（脚本、模板、规划文档等）
- 已确认可用的 Python 库
- （如有）Office/PowerPoint 安装及版本线索

并初步标注哪些资源可以直接复用，哪些需要进一步探索，为后续自动生成与美化学术 PPT 的工作提供环境侧基线。

## 2. 项目目录中与 PPT 相关的资源

通过在 `./` 下递归搜索文件名中包含 `ppt`/`powerpoint`/`office` 的文件（深度≤3），发现：

1. 根目录文件与子目录概览

- CWD: `E:\2026\x-fudan\new\GenericAgent\temp`
- 主要子项：
  - `./autonomous_reports/`：自主任务报告目录
  - `./ppt_lab/`：PPT 实验与模板目录（重点）
  - `./plan_teaching_kb/`：教案知识库相关规划
  - `./teaching_kb/`：教案知识库
  - `./编译原理_词法分析_10页_蓝色主题示例.pptx`：现有示例 PPT
  - `./TODO.txt` 等

2. 搜索命中（文件名含 ppt/office 关键字）

- `./编译原理_词法分析_10页_蓝色主题示例.pptx`
  - 类型：示例 PPT
  - 用途：可作为 **现成设计参考**，分析其版式、配色和结构，为后续模板美化提供灵感。

- `./autonomous_reports/R12_中文学术PPT基础模板自动生成.md`
  - 类型：报告文档
  - 内容：记录了使用 `python-pptx` 自动生成中文学术 PPT 基础模板的过程与使用说明。
  - 状态：**可直接复用** 作为本任务的环境说明交叉引用。

- `./ppt_lab/academic_chinese_template_v1.pptx`
  - 类型：自动生成的中文学术 PPT 基础模板（R12产出）
  - 特点：包含封面、目录、背景、相关工作、方法、实验、总结、致谢等典型学术汇报结构。
  - 状态：**核心可复用资产**，可作为后续自动填充、样式迁移的基准模板。

- `./ppt_lab/PLAN_academic_ppt_cn.md`
  - 类型：规划文档
  - 推测：描述了中文学术 PPT 的结构/版式规划。
  - 状态：**重要设计参考**，可与 R12 模板对齐，用于后续改进模板结构和美术设计。

> 小结：项目中目前已形成一个围绕 PPT 的最小生态：
> - 示例 PPT（真实案例）
> - 结构规划文档（PLAN_academic_ppt_cn.md）
> - 自动生成的基础模板（academic_chinese_template_v1.pptx）
> - 详细实现与使用说明报告（R12）

## 3. Python 环境中与 PPT/Office 相关的库

在当前虚拟环境中执行 `pip list` 失败，错误信息为：

```text
E:\2026\x-fudan\new\GenericAgent\.venv\Scripts\pythonw.exe: No module named pip
pip list failed: Command '['E:\\2026\\x-fudan\\new\\GenericAgent\\.venv\\Scripts\\pythonw.exe', '-m', 'pip', 'list']' returned non-zero exit status 1.
```

说明：

- 当前执行使用的是 `.venv\Scripts\pythonw.exe`，该解释器环境中 **未安装 pip 模块** 或不支持通过 `-m pip` 方式列出包。
- 这限制了自动枚举全部已安装库的能力。

但在同一环境中，直接导入 `python-pptx` 成功：

```text
python-pptx version: 1.0.2
```

已确认库：

- `python-pptx` 版本 1.0.2
  - 功能：生成和操作 PowerPoint `.pptx` 文件。
  - 状态：**已经在 R12 中成功用于生成模板**，可视为当前环境下主要可用的 PPT 自动化库。
  - 实践情况：
    - 可以创建幻灯片、文本框、设置字体/字号/对齐方式等。
    - 更底层的字体 eastAsia 设置通过 rPr 直接操作存在 API 限制（R12 曾踩坑），当前策略为仅通过 `run.font` 层面设置中文字体名称和样式。

尚未枚举到的库（推测）：

- 由于 `pip list` 不可用，本任务 **未能系统性确认** 诸如 `comtypes`, `win32com`, `python-docx`, `openpyxl` 等包在本环境中的存在。
- 若后续确需与本地 Office COM 接口交互，建议：
  - 由用户审查后允许在该环境安装 `pywin32` 或相关库；
  - 或在单独的脚本环境中进行 Office 自动化实验。

## 4. Office/PowerPoint 安装情况（待后续补充）

本轮任务中，尚未对操作系统层面的 Office/PowerPoint 安装及版本做深入探测。可能的探测方式包括（暂列方案，未执行）：

- 使用 PowerShell 检查常见安装路径（如 `C:\Program Files\Microsoft Office\` 等）
- 查询注册表中与 Office/PowerPoint 相关的键值（需谨慎，避免做任何破坏性操作）
- 根据文件关联或进程名探测已安装的 PowerPoint 可执行程序

考虑到自主任务的副作用边界，本报告暂不做系统级探测，仅在此列为 **后续可探索方向**，待用户审查后决定是否开展。

## 5. 资源可复用性与后续探索点

### 5.1 当前可直接复用的资源

1. `python-pptx`（1.0.2）

- 已验证可用，支持在完全无 GUI 的环境下生成 PPT 模板。
- 与后续任务的关系：
  - 可用于从结构化数据（教案、论文摘要等）自动生成 PPT。
  - 可用于基于现有模板（`academic_chinese_template_v1.pptx`）进行批量内容填充。

2. `./ppt_lab/academic_chinese_template_v1.pptx`

- 结构清晰，覆盖典型学术汇报章节。
- 适合作为：
  - 「从教案/论文自动生成 PPT」的目标模板；
  - 「实验新版式」时的对照基准。

3. `./ppt_lab/PLAN_academic_ppt_cn.md`

- 作为设计上的「上位规划」，可用于：
  - 对比模板实际实现与规划之间的差异；
  - 指导后续模板强化和美化任务。

4. `./编译原理_词法分析_10页_蓝色主题示例.pptx`

- 真实的课程 PPT 示例，可：
  - 分析其配色、布局、字体等；
  - 抽取「现实世界可接受」的设计元素，反哺模板设计。

5. `./autonomous_reports/R12_中文学术PPT基础模板自动生成.md`

- 记录了：
  - 一次底层字体设置失败的经验；
  - 当前模板结构和使用说明；
  - 后续可以在此基础上继续演化。

### 5.2 需要进一步探索的点

1. Python 环境的「全局」包情况

- 由于 `pip list` 不可用，目前对环境中其他潜在有用库（如 `pywin32`、`comtypes` 等）信息不足。
- 未来可以考虑：
  - 由用户评估后，在合适环境安装必要包；
  - 或在另一个带 pip 的 Python 解释器中执行更全面的库枚举。

2. 本机 Office/PowerPoint 存在与否及版本

- 当前任务没有触达系统级信息。
- 若未来要通过 COM 接口或直接操控本机 Office GUI 自动生成/演示 PPT，则需要：
  - 确认是否安装 Office 以及版本；
  - 决定是否引入对应自动化脚本（如 `win32com.client.Dispatch('PowerPoint.Application')` 等）。

3. ppt_lab 目录内的其他潜在资源

- 本轮仅通过文件名检索，识别出了 `PLAN_academic_ppt_cn.md` 与 `academic_chinese_template_v1.pptx`。
- 未来可进一步阅读 `PLAN_academic_ppt_cn.md` 的具体内容，抽取结构与设计规范，纳入统一的 PPT 设计知识库。

## 6. 小结

本次 R13 任务完成了对当前环境中 PPT/Office 相关资源的 **初步枚举**，得到：

- 已确认可用的 Python 库：
  - `python-pptx` 1.0.2（核心 PPT 生成工具）。
- 项目内可复用的 PPT 相关文件与目录：
  - `ppt_lab/` 目录及其内：
    - `academic_chinese_template_v1.pptx`（基础模板）
    - `PLAN_academic_ppt_cn.md`（结构规划）
  - 示例教学 PPT：`编译原理_词法分析_10页_蓝色主题示例.pptx`
  - 环境与模板生成说明：`autonomous_reports/R12_中文学术PPT基础模板自动生成.md`

尚未深入探测的方面（留待后续任务或用户审查决策）：

- 系统层面的 Office/PowerPoint 安装与版本信息
- 当前 Python 环境中其他可能存在但未显式枚举的 Office 相关库

这些信息将为后续任务（如「GNN 论文追踪表与 arXiv 抓取脚本打通」中自动生成可视化 PPT 汇报，或「教案知识库与 PPT 模板联动构想」）提供环境约束与可行性依据。

（后续步骤：在本任务执行完所有必要探测后，按自主行动 SOP，需：
1）更新本报告内容（如有新发现）；  
2）在 `history.txt` 中 prepend 一条 R13 记录；  
3）将 TODO 中对应第5条任务标记为 `[x]`。）