# R64 - quality_scorer_v2集成到autonomous收尾流程（方案待审）
日期: 2026-03-26

## 任务来源
TODO Batch11 条目5：修改autonomous_operation_sop，在每批次规划报告中引用quality_scorer_v2最新输出数据。

## 权限边界说明
按autonomous_operation_sop权限规则：
- "修改 global_mem / memory下SOP" → 需写入报告待审，不可自主执行

本报告提出修改方案，等待用户审批。

## 建议修改方案

### 修改位置：../memory/autonomous_operation_sop.md

在 "## 执行" 章节末尾（第25行后），追加以下内容：

**质量参考（可选）**：
- 每批执行前可运行 quality_scorer.py 查看近期批次质量趋势
- 规划类报告（Batch新轮次开始时）建议在报告末尾附质量数据块：
  最近批次平均分 / 低分占比 / 改进建议（从quality_report_v2.html提取）
- quality_scorer.py 路径：./quality_scorer.py（已在Batch10验证可运行）

### 修改位置：收尾（三件事缺一不可）章节

在第3条后追加第4条（可选项）：
4. （可选）若本批>=5个报告，运行quality_scorer.py更新quality_report_v2.html，
   将最新平均分附于下次规划报告

## 验证方法
修改后运行quality_scorer.py确认输出，检查近期报告是否有quality引用。

## 建议
- 此修改为"建议性"说明（可选），不影响现有收尾流程
- 可由用户直接patch，或授权Agent下次执行时修改
