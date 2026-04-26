# subtitle_proofreading_sop.md — 视频字幕智能校对SOP（R163, 2026-04-20）

工具: tools/subtitle_proofreader.py | 基于规则引擎

## 核心函数

```python
proofread_subtitle(file_path, output_path=None)
parse_srt(file_path) → 字幕列表
parse_vtt(file_path) → 字幕列表
check_punctuation(text) → 标点问题列表
check_timeline(subtitles) → 时间轴问题列表
check_text_length(subtitles, max_chars=40) → 长度问题列表
```

## 使用示例

```python
from subtitle_proofreader import proofread_subtitle

# 校对字幕
result = proofread_subtitle('video.srt', 'report.txt')

print(f"总字幕数: {result['total_subtitles']}")
print(f"标点问题: {len(result['issues']['punctuation'])}处")
print(f"时间轴问题: {len(result['issues']['timeline'])}处")
print(f"长度问题: {len(result['issues']['length'])}处")
```

## 支持格式

- **SRT**: SubRip字幕格式
- **VTT**: WebVTT字幕格式

## 检测项目

### 1. 标点符号
- 标点前后多余空格
- 成对标点不匹配（括号/引号等）

### 2. 时间轴
- 开始时间晚于结束时间
- 字幕时间重叠

### 3. 字幕长度
- 单条字幕超过建议字符数（默认40字符）

## 输出报告

生成文本报告，包含：
- 文件信息和总字幕数
- 标点符号问题详情
- 时间轴问题详情
- 字幕长度问题详情

[skill_mapping]
category: media_processing
skill: subtitle
tools: subtitle_proofreader.py
[/skill_mapping]

## [record_on_use]
执行完本SOP后，调用以下命令记录使用情况：
```python
import sys
sys.path.append('../memory')
from autonomous_operation_sop.helper import record_skill_usage
record_skill_usage('subtitle_proofreading_sop.md')
```
