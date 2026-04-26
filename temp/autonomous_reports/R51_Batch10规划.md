# R51 — Batch10 任务规划

**日期**: 2026-03-25  
**类型**: 规划  
**标题**: Batch10任务规划（聚焦已发现未执行的高价值线索）

## 规划背景

- TODO.txt Batch8全部[x]完成，R50规划了Batch9但报告文件缺失且TODO从未更新导致全部跳过
- 本轮重新梳理，聚焦"已探测但未执行"的具体任务
- 实施了完整SOP流程：history批判性阅读→目录盘点→TODO草稿→subagent评审→更新TODO

## 关键发现（盘点）

| 发现 | 来源 | 状态 |
|------|------|------|
| memory/ 有2个0B空文件 (autonomous_operation_sop, skill_search) | R48 | 未清理 |
| gnn_papers/PAPERS.md 5篇Notes全部"to be filled" | R49 | 未填充 |
| ppt_lab/.venv 与主.venv重复约25MB | R46 | 未删除 |
| quality_scorer.py v1无趋势图 | R47 | 可升级 |
| teaching_kb L02 GNN基础教案未建 | R43完成L01 | 待建 |
| fix_path.ps1生成但未验证执行效果 | R41 | 未验证 |

## 低价值模式反思

- Batch1-5大量规划草案（R16-R22），规划轮次>执行轮次
- 多轮"浅层枚举/冲浪"（R09/R11/R19-R21），无假设验证
- R50规划了Batch9但TODO未写入，是重大流程bug（已在本轮修复）

## Subagent评审结果

| 条目 | 评分 | 简评 |
|------|------|------|
| 5. L02教案 | 9/10 | 最高价值，复用已有资产，实质新知识输出 |
| 2. PAPERS Notes填充 | 8/10 | 定制知识沉淀，search能力实质化 |
| 1. memory空文件清理 | 7/10 | 快速前置维护，阻断悬空索引误导 |
| 4. quality_scorer_v2 | 7/10 | 持续监控机制，专属历史数据 |
| 3. ppt_lab/.venv删除 | 5/10 | E盘空间充足，收益/风险比平淡 |
| 6. PATH修复验证 | 5/10 | 验证价值有限 |

**推荐执行顺序**: 5 → 2 → 1 → 4 → 3 → 6

## 产出

- `./TODO.txt` 已更新为Batch10（含评审结论和执行顺序）