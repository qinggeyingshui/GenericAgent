# 内容创作 SOP

## 工具概述
自媒体脚本生成器，支持快速生成视频脚本。

## 核心工具
- `script_generator.py` - 脚本生成器

## 使用方法

### 1. 基础用法
```python
from script_generator import create_script_generator, ScriptStyle

generator = create_script_generator()

# 生成知识科普风格脚本
script = generator.generate(
    topic="人工智能",
    style=ScriptStyle.KNOWLEDGE,
    key_points=["AI定义", "应用场景", "未来趋势"]
)

print(script["full_script"])
```

### 2. 三种风格

#### 知识科普 (KNOWLEDGE)
- 适用场景：教育、科普、技术分享
- 特点：严谨、专业、结构清晰
- 开头：引入主题，激发兴趣
- 正文：分点阐述，逻辑递进
- 结尾：总结要点，引导互动

#### 娱乐搞笑 (ENTERTAINMENT)
- 适用场景：轻松娱乐、搞笑吐槽
- 特点：轻松、幽默、接地气
- 开头：活泼开场，拉近距离
- 正文：笑点密集，节奏紧凑
- 结尾：互动引导，增加粘性

#### 情感故事 (EMOTION)
- 适用场景：情感共鸣、人生感悟
- 特点：温暖、真诚、有代入感
- 开头：引发思考，营造氛围
- 正文：故事叙述，情感递进
- 结尾：升华主题，引发共鸣

### 3. 生成多风格对比
```python
# 一次生成所有风格，方便选择
all_scripts = generator.generate_multi_style(
    topic="时间管理",
    key_points=["制定计划", "优先级排序", "避免拖延"]
)

for style, script in all_scripts.items():
    print(f"\n=== {style} ===\n{script['opening']}")
```

### 4. 脚本结构
生成的脚本包含：
- `opening`: 开头部分
- `body`: 正文部分
- `closing`: 结尾部分
- `full_script`: 完整脚本

## 最佳实践

1. **明确主题**：主题要具体，避免过于宽泛
2. **准备要点**：提前整理3-5个关键要点
3. **选对风格**：根据目标受众选择合适风格
4. **二次加工**：生成后根据实际需求调整细节
5. **测试效果**：可生成多风格对比，选择最佳方案

## 扩展建议

- 可添加更多风格模板（如新闻播报、访谈对话等）
- 可集成AI大模型进行内容扩写
- 可结合素材库自动匹配配图配乐

## 注意事项

- 生成的脚本为模板化内容，需要人工润色
- 关键要点需要自行准备，工具不提供内容创作
- 不同平台受众偏好不同，需针对性调整

[skill_mapping]
category: content_creation
skill: content_creation_sop
functions: ScriptGenerator.generate, ScriptGenerator.generate_multi_style, create_script_generator
tools: script_generator.py
[/skill_mapping]

## [record_on_use]
执行完本SOP后，调用以下命令记录使用情况：
```python
import sys
sys.path.append('../memory')
from autonomous_operation_sop.helper import record_skill_usage
record_skill_usage('content_creation_sop.md')
```
