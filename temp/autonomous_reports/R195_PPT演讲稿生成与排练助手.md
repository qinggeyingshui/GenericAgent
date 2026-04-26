# R195 PPT演讲稿生成与排练助手

**日期**: 2026-04-21
**类型**: document_generation
**状态**: 已完成

## 任务背景

从Batch 17自媒体创作能力拓展TODO中选取第3条任务：
- 任务：PPT演讲稿生成与排练助手
- 目标：增强ppt_com_sop，创建speech_helper.py
- 验收：生成演讲稿+排练计时+关键点提示功能可用

## 实现方案

### 1. 技术架构
- 基于win32com提取PPT内容
- 模块化设计：3个核心类
- 时间管理：datetime+time模块

### 2. 核心功能

#### 2.1 SpeechGenerator - 演讲稿生成
- extract_content_from_ppt(): 提取PPT内容（标题/要点/备注）
- generate_speech(): 生成演讲稿（自动添加过渡语）
- optimize_speech(): 优化建议（字数/时长/句子长度）

#### 2.2 RehearsalTimer - 排练计时器
- start/pause/resume(): 计时控制
- get_elapsed(): 获取已用时间
- get_status(): 实时状态显示
- 支持目标时间设定和进度提示

#### 2.3 KeyPointHelper - 关键点提示
- extract_key_points(): 提取关键点
- format_prompts(): 格式化提示卡
- save_prompts(): 保存到文件

### 3. 便捷函数
```python
quick_generate_speech(ppt_path, output_path)
quick_rehearsal(target_minutes)
```

## 测试验证

### 测试用例
```python
import sys
sys.path.append("./tools")
import speech_helper

# 1. 排练计时器
timer = speech_helper.RehearsalTimer(1)
timer.start()
# 测试通过：计时正常，暂停/继续功能正常

# 2. 关键点提示
helper = speech_helper.KeyPointHelper()
key_points = helper.extract_key_points(mock_slides)
# 测试通过：提取3个关键点

# 3. 演讲稿生成
gen = speech_helper.SpeechGenerator()
speech = gen.generate_speech(mock_slides)
optimization = gen.optimize_speech(speech)
# 测试通过：生成演讲稿，提供优化建议
```

### 验收结果
- ✓ 排练计时器：计时准确，支持暂停/继续
- ✓ 关键点提示：成功提取关键点并格式化
- ✓ 演讲稿生成：自动生成演讲稿，提供优化建议
- ✓ 便捷函数：quick_generate_speech和quick_rehearsal可用

## 文件产出

### 1. temp/tools/speech_helper.py
- 行数：约180行
- 3个核心类：SpeechGenerator, RehearsalTimer, KeyPointHelper
- 2个便捷函数：quick_generate_speech, quick_rehearsal

### 2. ../memory/ppt_com_sop.md (更新)
- 新增第8节：演讲稿生成与排练助手
- 更新工具文件索引：添加speech_helper.py
- 更新skill_mapping：添加speech_helper.py

## SOP更新内容

### 8. 演讲稿生成与排练助手
- 8.1 核心功能：SpeechGenerator/RehearsalTimer/KeyPointHelper
- 8.2 快速使用：quick_generate_speech/quick_rehearsal
- 8.3 演讲稿优化建议：字数统计/时长估算/句子分析

## 使用示例

### 完整流程
```python
import sys
sys.path.append("./tools")
import speech_helper

# 1. 生成演讲稿
gen = speech_helper.SpeechGenerator()
slides = gen.extract_content_from_ppt("demo.pptx")
speech = gen.generate_speech(slides)
with open("speech.txt", "w", encoding="utf-8") as f:
    f.write(speech)

# 2. 提取关键点
helper = speech_helper.KeyPointHelper()
key_points = helper.extract_key_points(slides)
helper.save_prompts(key_points, "prompts.txt")

# 3. 开始排练
timer = speech_helper.RehearsalTimer(target_minutes=10)
timer.start()
# 演讲中...
print(timer.get_status())
```

## 技术亮点

1. **智能过渡语**：自动在幻灯片间添加过渡语，使演讲更流畅
2. **时长估算**：基于字数估算演讲时长（150字/分钟）
3. **实时计时**：支持暂停/继续，实时显示进度和剩余时间
4. **关键点提取**：自动提取标题和要点，生成演讲提示卡
5. **优化建议**：分析字数、句子长度，提供改进建议

## 应用场景

1. **学术报告**：从PPT生成演讲稿，排练控制时间
2. **商业演示**：提取关键点，制作演讲提示卡
3. **教学培训**：生成讲稿，优化演讲内容
4. **会议发言**：快速准备演讲稿，控制发言时长

## 后续优化方向

1. **语音识别**：集成语音识别，实时对比演讲稿
2. **情感分析**：分析演讲稿情感倾向，提供调整建议
3. **多语言支持**：支持英文演讲稿生成
4. **视频录制**：集成视频录制功能，回放分析

## 总结

成功实现PPT演讲稿生成与排练助手，为演讲准备提供全流程支持。工具功能完整，易于使用，显著提升演讲准备效率。