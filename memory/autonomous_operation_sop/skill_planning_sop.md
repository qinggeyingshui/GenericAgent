# 技能拓展规划 SOP

> 职责：规划TODO，产出后立即结束。执行和收尾由 autonomous_operation_sop.md 负责。

## 1. 数据准备
```python
import sys; sys.path.append('../memory/autonomous_operation_sop')
from helper import get_skill_stats
stats = get_skill_stats()  # {total, categories, high_usage, all_skills}
```
另必须完整读: ../memory/global_mem.txt(USER_PROFILE) + temp/autonomous_reports/history.txt

## 2. 去重验证（🚫阻断性，必须先做）
**未输出对比表 = 规划无效**

| 候选任务 | 历史相似任务(Rxxx) | 判定 | 差异说明 |
|----------|-------------------|------|----------|
| ... | ... | ❌重复/⚠️扩展/✅新增 | ... |

判定规则：
- ❌重复 → 拒绝
- ⚠️扩展 → 必须B类，领域=被增强SOP所属领域
- ✅新增 → 可A类

## 3. 需求驱动（至少满足一项）
| 条件 | 操作 |
|------|------|
| usage_count > 5 | 优先增强 |
| history中标记失败 | 优先修复 |
| 与用户目标相关 | 提升优先级 |
| 同领域usage≈0 且 last_used>90天 | ❌不新增 |

## 4. 四维度评分
```
S(t) = 0.30*B + 0.20*D + 0.30*U + 0.20*I
```
| 维度 | 公式/标准 |
|------|----------|
| B(广度) | 新领域=10, 已有=10*(1-skill_count/(avg+1)) |
| D(深度) | 10*usage_count/(max_usage+1) |
| U(实用) | 高频刚需9-10, 中频7-8, 低频5-6; 目标相关+2 |
| I(创新) | AI前沿9-10, 新兴7-8, 成熟5-6, 传统3-4 |

⚠️ 必须输出B/D/U/I精确值（2位小数）

## 5. 任务类型
| 类型 | 说明 | 产出 | 约束 |
|------|------|------|------|
| A类（推荐） | 新SOP | xxx_sop.md + xxx.py | 领域命名合理，与skill_tree.json一致 |
| B类（可接受） | 增强现有SOP | 现有SOP新增章节 | 领域=被增强SOP所属领域，禁止自定义 |
| C类（Workflow） | 串联≥2个skill | xxx_workflow_sop.md | 禁止workflow分裂，扩展现有而非创建v2 |
| D类（工具层） | 纯工具 | xxx.py | - |

约束：
- B类 ≤ 3个，新领域 ≤ 1个，覆盖 ≥ 4领域

## 6. 质量检查
| 检查项 | 要求 |
|--------|------|
| 去重验证 | 报告必含对比表 |
| B类领域归属 | = 被增强SOP所属领域 |
| 领域平衡 | ≥4领域，禁低频盲扩(usage=0) |
| 验收可量化 | 具体功能+指标 |
| 数据来源 | 说明从哪来，禁假设存在 |
| 单一问题 | 一个TODO解决一个问题 |

复杂度红线：
- ✅ 成熟API / 稳定开源库(stars>1k) / 本地离线
- ❌ 从头训练 / 复杂OAuth / 付费API无免费额度

## 7. 产出
1. **TODO**：5-7条写入 `temp/TODO.txt`，格式：`[ ] 领域 | 目标 | 产出：xxx_sop.md + xxx.py | 验收`
2. **报告**：写入 `temp/autonomous_reports/Batch_xx_规划.md`，包含数据分析、去重表、评分表

⚠️ 规划阶段不写history.txt，不更新skill_tree，不调用complete_task。

**规划完成后立即结束，禁止执行任何TODO。**
