# 高质量技术方案搜索 SOP

## 核心原则
- **官方+主流** → 直接用（省时间）
- **有争议/多选项** → 对比3个（保质量）
- **实现细节** → GitHub找现成代码复用

## 搜索流程

### 1. 问题定义（30秒）
明确三要素：
- **任务目标**：我要做什么
- **输入输出**：数据格式/接口规范
- **约束条件**：性能要求/兼容性/依赖限制

### 2. 快速判断（1分钟）
- Google搜索：`best way to [task] [language]`
- 观察前3条结果：
  - 如果都指向同一方案 → **跳到步骤4**（官方主流）
  - 如果有分歧/多个选项 → **进入步骤3**（需要对比）

### 3. 方案对比（5分钟）

#### 渠道选择矩阵
| 问题类型 | 优先渠道 | 次选渠道 | 避开 |
|---------|---------|---------|------|
| 技术选型/库对比 | GitHub (awesome列表/Trending) + 官方文档 | Stack Overflow 高赞 | 个人博客 |
| API用法/代码示例 | 官方文档 > Stack Overflow | GitHub Issues | 过时教程 |
| 最佳实践/架构 | 知乎/Medium 深度文章 + GitHub 优秀项目 | 技术社区 | 营销软文 |
| 快速上手/教程 | 官方 Quick Start + Bilibili | 实战项目 | 纯视频无文档 |
| 故障排查 | Google 精确搜索 + GitHub Issues | Stack Overflow | 未验证答案 |

#### 对比维度（4个关键指标）
1. **维护状态**：最近commit < 6个月，issue响应速度
2. **社区规模**：star数/fork数/contributor数/下载量
3. **上手难度**：README质量/示例完整度/文档覆盖率
4. **适配度**：是否满足约束条件（Python版本/依赖冲突/License）

#### 并行搜索技巧
- 同时开3个tab，分别搜不同关键词组合
- 设置时间盒：每个渠道最多5分钟
- 快速筛选：
  - GitHub: 看star + 最近更新 + issue关闭率
  - 文章: 看日期 + 作者背景 + 评论质量
  - 视频: 看时长（>30分钟跳过）+ 弹幕密度

### 4. GitHub验证（3分钟）
找到目标repo后：
1. **README检查**：Quick Start能否直接跑
2. **示例查找**：`examples/` 或 `demos/` 目录有无类似场景
3. **代码复用**：
   - 复制关键代码片段
   - 标注来源：`# From: github.com/user/repo/path/to/file.py`
   - 记录版本：`# Version: v1.2.3 (2026-04-13)`
4. **依赖检查**：`requirements.txt` 或 `package.json` 是否有冲突

### 5. 开始实现
- 先跑通最小示例（MVP）
- 验证核心功能
- 再扩展到完整需求

## 语言特定渠道

### Python
- 包对比：PyPI stats + GitHub stars
- 文档：官方 ReadTheDocs
- 社区：Python官方论坛 / r/Python

### JavaScript/Node.js
- 包对比：npm trends + bundlephobia (包体积)
- 文档：MDN > 官方文档
- 社区：Dev.to / r/javascript

### 其他语言
- Go: awesome-go + pkg.go.dev
- Rust: crates.io + lib.rs
- Java: Maven Central + Baeldung

## 失败降级策略

### 找不到现成方案时
1. 拆解问题：能否分解成多个子问题
2. 降低要求：是否可以接受部分功能
3. 自己实现：评估开发成本 vs 搜索成本

### 方案冲突时
1. 看时间线：新方案是否解决了旧方案的痛点
2. 看场景：不同方案可能适用不同场景
3. 看趋势：社区正在迁移到哪个方案

## 知识沉淀机制

### 即时记录
- 好方案 → 记录到 `temp/verified_solutions.md`
- 踩坑 → 记录到 `../memory/self_improvement.md`

### 定期归档
- 每周整理 → 更新到对应领域的knowledge base
- 通用模式 → 提炼成新的SOP

### 技能树更新
- 使用新工具 → `skill_tree_api.record_usage()`
- 发现缺口 → `skill_tree_api.add_gap()`
- 补齐能力 → `skill_tree_api.fill_gap()`

## 实战案例

### 案例1：PDF转Markdown
```
1. 问题：PDF文件 → Markdown文本，保留表格结构
2. 快速判断：Google "python pdf to markdown"
   → 发现主流方案：pdfplumber, PyPDF2, pdfminer.six
3. 方案对比：
   - pdfplumber: 12.8k stars, 2周前更新, 表格支持好
   - PyPDF2: 7.9k stars, 1月前更新, 纯文本提取
   - pdfminer.six: 5.6k stars, 3月前更新, 底层解析
   → 选择 pdfplumber（表格需求+维护活跃）
4. GitHub验证：
   - examples/tables.py 有表格提取示例
   - 复制代码并标注来源
5. 实现：成功提取表格并转换为Markdown
```

### 案例2：视频字幕生成
```
1. 问题：视频文件 → SRT字幕，支持中文
2. 快速判断：Google "python video subtitle generation"
   → 有分歧：Whisper (OpenAI), vosk, DeepSpeech
3. 方案对比：
   - Whisper: 官方推荐, 精度高, 但需GPU
   - vosk: 轻量级, 离线, 中文支持一般
   - DeepSpeech: Mozilla停止维护
   → 选择 Whisper（精度优先）
4. GitHub验证：
   - openai/whisper README有完整示例
   - 检查依赖：需要 ffmpeg
5. 实现：先测试CPU模式，确认可行后再优化
```

## 注意事项
- ⚠️ 技术选型时，同一功能有多个可选库且不确定最优时，**必须先搜索**，禁止凭印象选库
- ⚠️ 禁信搜索摘要，数值/API参数必进详情页核实
- ⚠️ 复制代码必须标注来源和版本，便于后续追溯
- ⚠️ 新库装到 `.venv` 前先检查依赖冲突

---
[skill_mapping]
category: web_automation
skill: web_scraping
tools: parallel_search.py
[/skill_mapping]

## [record_on_use]
执行完本SOP后，调用以下命令记录使用情况：
```python
import sys
sys.path.append('../memory')
from autonomous_operation_sop.helper import record_skill_usage
record_skill_usage('research_search_sop.md')
```
