# R60 - L02教案PPT自动生成

**日期**: 2026-03-26
**类型**: 产出
**状态**: 成功

## 任务目标

读取 teaching_kb L02（图神经网络基础）lesson_plan.md，
用 ppt_lab/generate_ppt.py 管道生成配套学术PPT，验收：≥8页。

## 执行结果

- **输出文件**: `ppt_lab/output/L02_GNN基础.pptx`
- **页数**: 12页（超过验收8页要求）
- **文件大小**: 47838B (~47KB)
- **配色方案**: academic_blue

## 幻灯片结构

| 页 | 类型 | 标题 |
|---|------|------|
| 1 | title | 图神经网络基础 |
| 2 | toc | 本讲内容（7个章节） |
| 3 | section | 图的数学基础 |
| 4 | content | 图结构三要素与核心矩阵 |
| 5 | comparison | 为什么CNN不能直接处理图数据？ |
| 6 | section | MPNN消息传递统一框架 |
| 7 | step_cards | MPNN三步骤（MESSAGE/AGGREGATE/UPDATE） |
| 8 | section | GCN推导 |
| 9 | highlight_content | GCN核心传播公式 |
| 10 | comparison | GCN变体速览 |
| 11 | content | GNN与LLM的三种接口范式 |
| 12 | ending | 课堂小结 |

## 技术细节

- 管道：`generate_ppt.py → PPTBuilder(ppt_utils.py) → .pptx`
- ppt_lab路径：`./ppt_lab/`（注意：不在GenericAgent根目录，在temp/下）
- 直接在code_run内构建config dict并调用generate_ppt()，无需中间json文件
- slide类型覆盖：title/toc/section/content/comparison/step_cards/highlight_content/ending

## 关键发现

1. `generate_ppt(config, output_path)` 接口清晰，config为dict直接传入无需写json
2. `step_cards` 的steps格式：`[{"title": "...", "points": [...]}]`
3. `highlight_content` 支持 `highlight_text` + `sub_points` 字段名
4. 生成时出现任何slide错误会自动降级为普通content页，不会中断整体生成

## 验收

- [x] L02_GNN基础.pptx 存在于 ppt_lab/output/
- [x] 页数 12 >= 8
- [x] 覆盖L02教案全部7个章节
- [x] 使用academic_blue学术配色
