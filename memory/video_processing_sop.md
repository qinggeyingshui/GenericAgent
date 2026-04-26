# 视频处理 SOP

## 概述
视频处理工具包，支持视频剪辑、合并、提取帧、添加字幕等功能。

## 依赖
- moviepy (已安装)
- ffmpeg (命令行工具，已安装)
- Pillow (用于帧提取，需要时安装: `pip install pillow`)

## 工具位置
`temp/video_toolkit.py`

## 核心功能

### 1. 视频剪辑
```python
from video_toolkit import clip_video

# 剪辑视频片段（5秒到15秒）
clip_video("input.mp4", "output.mp4", start_time=5, end_time=15)

# 从开头剪辑到10秒
clip_video("input.mp4", "output.mp4", start_time=0, end_time=10)

# 从5秒剪辑到结尾
clip_video("input.mp4", "output.mp4", start_time=5)
```

### 2. 视频合并
```python
from video_toolkit import merge_videos

# 合并多个视频
merge_videos(["video1.mp4", "video2.mp4", "video3.mp4"], "merged.mp4")
```

### 3. 提取视频帧
```python
from video_toolkit import extract_frames

# 每秒提取1帧
frame_count = extract_frames("input.mp4", "./frames", fps=1)
print(f"提取了 {frame_count} 帧")

# 每秒提取2帧
extract_frames("input.mp4", "./frames", fps=2)
```

### 4. 添加字幕
```python
from video_toolkit import add_subtitles

# 添加字幕（时间单位：秒）
subtitles = [
    (0, 3, "第一句字幕"),
    (3, 6, "第二句字幕"),
    (6, 9, "第三句字幕")
]
add_subtitles("input.mp4", "output_with_subs.mp4", subtitles)
```

### 5. 转场特效（R146新增）
```python
from tools.video_effects import add_transition, batch_add_transitions
from tools.video_effects import FADE, SLIDE, ZOOM, ROTATE, WIPE, LEFT, RIGHT, UP, DOWN

# 单个转场：淡入淡出
add_transition("video1.mp4", "video2.mp4", "output.mp4", 
               transition_type=FADE, duration=1.0)

# 滑动转场（从左滑入）
add_transition("video1.mp4", "video2.mp4", "output.mp4",
               transition_type=SLIDE, duration=1.5, direction=LEFT)

# 缩放转场
add_transition("video1.mp4", "video2.mp4", "output.mp4",
               transition_type=ZOOM, duration=1.0)

# 旋转转场
add_transition("video1.mp4", "video2.mp4", "output.mp4",
               transition_type=ROTATE, duration=1.2)

# 擦除转场（从上到下）
add_transition("video1.mp4", "video2.mp4", "output.mp4",
               transition_type=WIPE, duration=1.0, direction=UP)

# 批量添加转场（多个视频）
videos = ["clip1.mp4", "clip2.mp4", "clip3.mp4"]
batch_add_transitions(videos, "final.mp4", transition_type=FADE, duration=1.0)
```

**支持的转场类型**：
- `FADE`: 淡入淡出（透明度渐变）
- `SLIDE`: 滑动（支持LEFT/RIGHT/UP/DOWN四个方向）
- `ZOOM`: 缩放（从小放大）
- `ROTATE`: 旋转（旋转进入）
- `WIPE`: 擦除（支持LEFT/RIGHT/UP/DOWN四个方向）

**参数说明**：
- `duration`: 转场时长（秒），建议0.5-2.0秒
- `direction`: 方向（仅SLIDE和WIPE需要）

## 使用场景

### 场景1: 视频片段提取
用户需要从长视频中提取特定片段。
```python
clip_video("lecture.mp4", "highlight.mp4", start_time=120, end_time=180)
```

### 场景2: 多视频拼接
将多个视频片段合并成一个完整视频。
```python
clips = ["intro.mp4", "main.mp4", "outro.mp4"]
merge_videos(clips, "final.mp4")
```

### 场景3: 视频关键帧提取
从视频中提取关键帧用于分析或缩略图。
```python
extract_frames("video.mp4", "./thumbnails", fps=0.5)  # 每2秒提取1帧
```

### 场景4: 视频字幕添加
为视频添加文字说明或翻译字幕。
```python
subs = [(0, 5, "Welcome"), (5, 10, "Tutorial Start")]
add_subtitles("video.mp4", "video_subtitled.mp4", subs)
```

## 注意事项
1. 视频处理较耗时，大文件需等待
2. 输出格式默认为 H.264 编码的 MP4
3. 字幕功能需要系统安装字体支持
4. 提取帧功能需要 Pillow 库
5. 处理完成后会自动关闭视频对象释放资源

## 错误处理
- 文件不存在：检查输入路径
- 编码错误：确认 ffmpeg 正确安装
- 内存不足：处理大文件时分段处理
- 字幕显示异常：检查字体和文本编码

## 扩展功能（待开发）
- 视频旋转/翻转
- 添加背景音乐
- 视频滤镜效果
- 视频压缩优化
- 批量处理

---

## 6. Video Workflow Orchestration (R170, 2026-04-20)

Tool: tools/video_workflow.py

```python
from video_workflow import VideoWorkflow, create_standard_workflow

# Create workflow
wf = VideoWorkflow(output_dir="./output")
wf.clip_step(0, 60)
wf.subtitle_step("subtitles.srt")
wf.transition_step("fade", 1.0)
wf.export_step("mp4", "high")

# Execute
result = wf.execute("input.mp4", "output.mp4")

# Batch processing
results = wf.batch_execute(["video1.mp4", "video2.mp4"])

# Save/load template
wf.save_template("my_workflow")
wf.load_template("my_workflow.json")

# Predefined workflows
standard_wf = create_standard_workflow()
```

Functions:
- clip_step(start, end): Add clip step
- subtitle_step(subtitle_file): Add subtitle step
- transition_step(type, duration): Add transition step
- export_step(format, quality): Add export step
- execute(input_file, output_file): Execute workflow
- batch_execute(input_files): Batch processing
- save_template(name): Save as template
- load_template(file): Load template

---

## 7. 视频剪辑模板库 (R196)

**工具**: `temp/tools/video_templates.py`

### 7.1 核心功能

#### VideoTemplateManager - 模板管理
管理视频剪辑模板，支持保存、加载、列表、删除。

```python
import sys
sys.path.append('./tools')
import video_templates

mgr = video_templates.VideoTemplateManager()
mgr.save_template("my_template", template_dict)
loaded = mgr.load_template("my_template")
templates = mgr.list_templates()
```

#### VideoTemplate - 模板应用
提供预设模板和一键应用功能。

```python
# 开场模板
opening = video_templates.VideoTemplate.opening_template(
    "video.mp4", "欢迎观看", duration=3.0
)

# 片尾模板
ending = video_templates.VideoTemplate.ending_template(
    "video.mp4", "感谢观看", duration=3.0
)

# 一键应用模板
template = {
    "opening": {"title": "我的视频", "duration": 3.0},
    "ending": {"text": "谢谢观看", "duration": 3.0}
}
video_templates.VideoTemplate.apply_template("input.mp4", "output.mp4", template)
```

### 7.2 预设模板

#### 标准开场模板
```python
opening = video_templates.create_standard_opening("标题", 3.0)
```

#### 标准片尾模板
```python
ending = video_templates.create_standard_ending("感谢文字", 3.0)
```

### 7.3 快速使用

```python
# 快速应用开场和片尾
video_templates.quick_apply_template(
    "input.mp4", 
    "output.mp4",
    opening_title="欢迎观看",
    ending_text="感谢观看"
)
```

### 7.4 模板结构

```json
{
  "opening": {
    "type": "opening",
    "title": "标题文字",
    "duration": 3.0,
    "fade_in": 0.5,
    "fade_out": 0.5
  },
  "ending": {
    "type": "ending",
    "text": "结束文字",
    "duration": 3.0,
    "fade_in": 0.5,
    "fade_out": 0.5
  }
}
```

---

## 8. 字幕智能优化 (R202, 2026-04-21)

**工具**: `temp/tools/subtitle_proofreader.py`

### 8.1 增强功能

#### 语言检测
```python
from subtitle_proofreader import detect_language

text = "这是一段中文文本"
lang = detect_language(text)  # 返回: "zh"
```

支持语言: 中文(zh)、英文(en)、日文(ja)

#### AI润色
```python
from subtitle_proofreader import polish_subtitle

# 中文润色
text = polish_subtitle("这是  一段  文本", language="zh")

# 英文润色
text = polish_subtitle("this is a text", language="en")
```

润色功能:
- 移除多余空格
- 规范标点符号
- 首字母大写（英文）

#### 情感标签识别
```python
from subtitle_proofreader import add_emotion_tags

subtitles = [
    {"text": "哈哈太开心了", "start": 0, "end": 2},
    {"text": "这让我很生气", "start": 2, "end": 4}
]

enhanced = add_emotion_tags(subtitles)
# 返回: [{"text": "...", "emotions": ["happy"]}, {"text": "...", "emotions": ["angry"]}]
```

支持情感: happy、sad、angry、surprised、neutral

#### 时间轴优化
```python
from subtitle_proofreader import optimize_timeline

subtitles = [
    {"text": "短字幕", "start": 0, "end": 0.5},  # 太短
    {"text": "长字幕", "start": 1, "end": 10}    # 太长
]

optimized = optimize_timeline(subtitles, min_duration=1.0, max_duration=7.0)
```

#### 一键增强
```python
from subtitle_proofreader import enhance_subtitles

result = enhance_subtitles(
    "input.srt",
    output_path="enhanced.srt",
    enable_polish=True,      # 启用润色
    enable_emotion=True,     # 启用情感标签
    enable_optimize=True     # 启用时间轴优化
)

print(f"语言: {result['language']}")
print(f"总数: {result['total']}")
```

### 8.2 使用场景

**场景1: 字幕质量提升**
```python
# 润色+优化时间轴
enhance_subtitles("raw.srt", "polished.srt", enable_emotion=False)
```

**场景2: 情感分析**
```python
# 添加情感标签用于视频分析
result = enhance_subtitles("video.srt", enable_polish=False, enable_optimize=False)
```

**场景3: 多语言处理**
```python
# 自动检测语言并应用对应规则
enhance_subtitles("multilang.srt", "output.srt")
```

---

[skill_mapping]
category: media_processing
skill: video_workflow
tools: video_toolkit.py, video_templates.py
[/skill_mapping]

## [record_on_use]
执行完本SOP后，调用以下命令记录使用情况：
```python
import sys
sys.path.append('../memory')
from autonomous_operation_sop.helper import record_skill_usage
record_skill_usage('video_processing_sop.md')
```
