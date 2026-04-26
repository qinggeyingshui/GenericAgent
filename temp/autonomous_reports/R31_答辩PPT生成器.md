# R31 — 答辩PPT一键生成器 (defense_ppt_builder.py)

## 任务来源
TODO#5：封装 defense_ppt_builder.py，输入 {姓名/学校/研究方向/成果} 即可一键生成 ≥15 页答辩 PPT。

## 产出物
- `ppt_lab/defense_ppt_builder.py` — 16860 字节，含完整生成逻辑 + 内置 Demo 数据 + CLI 入口

## 设计要点

### 数据模型 (PROFILE_TEMPLATE)
| 分类 | 字段 | 说明 |
|------|------|------|
| 基本信息 | name/university/major/gpa/rank | 封面+简介页 |
| 学术能力 | english/skills/core_courses | icon_cards 页 |
| 科研经历 | research_projects[] | 每段独立 content 页 |
| 实验数据 | experiment_chart | 可选 bar chart 页 |
| 竞赛荣誉 | awards/honors/timeline | timeline + comparison 页 |
| 未来规划 | future_plans/why_this_school | content + icon_cards 页 |

### 生成页面结构（Demo 数据 → 16 页）
1. 封面 (title_slide)
2. 目录 (toc_slide, 4 章节)
3. 章节一分隔页
4. 个人信息 icon_cards（6 卡片）
5. 学业数据 stats（4 指标）
6. 章节二分隔页
7. 科研项目一 content（5 要点 + 高亮）
8. 科研项目二 content
9. 实验结果 chart（bar 对比图）
10. 章节三分隔页
11. 成长历程 timeline（6 节点）
12. 竞赛 vs 实践 comparison
13. 章节四分隔页
14. 研究计划 content（6 要点 + 首尾高亮）
15. 选择贵校 icon_cards（4 卡片）
16. 致谢 ending

### CLI 用法
```bash
python defense_ppt_builder.py                        # 内置Demo
python defense_ppt_builder.py -o out.pptx             # 指定输出
python defense_ppt_builder.py -s morandi_warm          # 切换配色
python defense_ppt_builder.py -p my_profile.json       # 自定义数据
```

### API 用法
```python
from defense_ppt_builder import build_defense_ppt
build_defense_ppt(profile_dict, "output.pptx")
```

## 验收结果
- ✅ 模拟数据生成 16 页 / 61450 字节
- ✅ 页数 ≥ 15 达标
- ✅ 覆盖全部 8 种页面类型（title/toc/section/content/icon_cards/stats/timeline/comparison/chart/ending）
- ✅ 支持 CLI + API 双入口
- ✅ 动态章节：字段缺失时自动跳过对应页面