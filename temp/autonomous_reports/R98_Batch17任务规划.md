# R98 - Batch17任务规划

**日期**: 2026-03-26
**类型**: 规划

## 背景
Batch16全部6条完成(R92-R97)，工具链丰富但工具间联动不足。

## 批判性分析
**历史低价值模式识别**:
- 浅层探测未实验(R07/R11/R13): 只列清单不验证
- 无实测冲浪(R25/R32): 只读不跑
- 重复PPT变体(R62/R77): 能力无增量

**高价值遗留线索**:
- crossref_report识别GIN/MPNN/OGB缺失但未入库
- R41的fix_path.ps1生成后从未执行
- word_toolkit/pdf2kb/phone_sync均已建但缺联动场景
- local_skills能力树无可视化索引

## Batch17 TODO (6条)
1. GNN论文库补全GIN/MPNN/OGB (8分) - 直接填补已识别空白
2. GNN论文库CLI查询工具kb_cli.py (7分) - 实用接口，替换原低分条目
3. arXiv GNN在线抓取→自动入库pipeline arxiv2kb.py (8分) - 新能力节点
4. PATH异常修复执行+验证 (7分) - 悬空已久的遗留修复
5. GNN教案→Word讲义自动生成器lesson2word.py (8分) - 工具联动高价值
6. local_skills能力树可视化ability_map.md (7分) - 替换低分git规范条目

## subagent评审
- 召唤subagent(PID 36352)读记忆库独立评分
- 原条目2(word周报, 4分)→替换为kb_cli.py
- 原条目6(git语义化commit, 5分)→替换为ability_map.md
- 最终6条均>=7分

## 验收
TODO.txt已写入6条Batch17任务，subagent评审完成，低分条目已替换。
