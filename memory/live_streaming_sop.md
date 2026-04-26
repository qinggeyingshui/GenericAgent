# 直播脚本生成与提词 SOP

## 功能
生成直播脚本、分段提词、互动话术库

## 工具
- `temp/tools/live_script_generator.py`

## 使用流程

### 1. 生成脚本大纲
```python
import sys
sys.path.append('./tools')
import live_script_generator as lsg

outline = lsg.generate_script_outline(
    topic='Python自动化技巧',
    duration=30,  # 分钟
    sections=['开场', '主体内容', '互动环节', '结尾']
)
```

### 2. 生成提词稿
```python
teleprompter = lsg.generate_teleprompter(outline)
print(teleprompter)
```

### 3. 使用互动话术
```python
# 欢迎话术
welcome = lsg.get_interaction_phrase('welcome', name='观众名')

# 感谢话术
thanks = lsg.get_interaction_phrase('thanks', name='观众名', gift='礼物名')

# 提问回应
question = lsg.get_interaction_phrase('question')

# 引导话术
guide = lsg.get_interaction_phrase('guide')
```

### 4. 创建完整脚本
```python
script = lsg.create_full_script(
    topic='直播主题',
    duration=30,
    key_points=['要点1', '要点2', '要点3']
)

# 保存脚本
lsg.save_script(script, './my_script.txt')
```

## 脚本结构

### 标准分段
1. **开场** (0-7分钟)
   - 问候观众，自我介绍
   - 说明直播主题和亮点
   - 引导关注点赞

2. **主体内容** (7-14分钟)
   - 核心知识点讲解
   - 案例分享
   - 实操演示

3. **互动环节** (14-21分钟)
   - 回答评论区问题
   - 抽奖/福利环节
   - 引导互动

4. **结尾** (21-28分钟)
   - 总结要点
   - 预告下次内容
   - 感谢观看，引导关注

## 互动话术库

### 欢迎类
- 欢迎{name}来到直播间！
- 感谢{name}的关注！
- 欢迎新朋友{name}！

### 感谢类
- 感谢{name}的{gift}！
- 谢谢{name}的支持！
- 感谢{name}送的{gift}，爱你们！

### 提问回应
- 这个问题很好，让我来解答一下
- 关于这个问题，我的看法是
- 很多朋友都在问这个，我详细说说

### 引导类
- 还没关注的朋友点个关注不迷路
- 喜欢的话给个小心心吧
- 评论区告诉我你的想法

## 最佳实践

1. **时间控制**: 每段预留缓冲时间，避免超时
2. **互动频率**: 每5-10分钟互动一次
3. **话术变化**: 使用随机话术避免重复
4. **关键点**: 主体内容提前准备详细要点

## 示例

完整示例见 `temp/test_scripts/demo_script.txt`

---

[skill_mapping]
category: content_creation
tools: temp/tools/live_script_generator.py
[/skill_mapping]
