# 视频剪辑工具包使用文档

## 概述
提供视频剪辑、转码、压缩等核心功能，基于 moviepy 和 ffmpeg-python。

## 依赖
```bash
pip install moviepy ffmpeg-python
```

**注意**: ffmpeg-python 需要系统安装 ffmpeg
- Windows: 下载 ffmpeg.exe 并添加到 PATH
- Linux: `sudo apt install ffmpeg`
- Mac: `brew install ffmpeg`

## video_editor.py - 视频剪辑

### 1. 剪辑视频片段
```python
from tools.video_editor import cut_video

# 剪辑10-30秒片段
result = cut_video(
    input_path="input.mp4",
    output_path="output.mp4",
    start_time=10,
    end_time=30
)
print(result)  # {'success': True, 'output': 'output.mp4', 'duration': 20.0}
```

### 2. 合并多个视频
```python
from tools.video_editor import merge_videos

result = merge_videos(
    input_paths=["video1.mp4", "video2.mp4", "video3.mp4"],
    output_path="merged.mp4"
)
```

### 3. 添加文字
```python
from tools.video_editor import add_text

result = add_text(
    input_path="input.mp4",
    output_path="output.mp4",
    text="会议录像 2026-04-14",
    position=('center', 'bottom'),
    fontsize=50,
    color='white'
)
```

### 4. 添加音频
```python
from tools.video_editor import add_audio

result = add_audio(
    input_path="video.mp4",
    output_path="output.mp4",
    audio_path="bgm.mp3",
    volume=0.5
)
```

### 5. 获取视频信息
```python
from tools.video_editor import get_video_info

info = get_video_info("video.mp4")
print(info)
# {'duration': 120.5, 'fps': 30, 'size': (1920, 1080), 'has_audio': True}
```

## video_converter.py - 视频转码

### 1. 格式转换
```python
from tools.video_converter import convert_format

# MP4 转 AVI
result = convert_format(
    input_path="input.mp4",
    output_path="output.avi"
)

# 支持格式: mp4, avi, mkv, mov, flv, webm 等
```

### 2. 压缩视频
```python
from tools.video_converter import compress_video

result = compress_video(
    input_path="large.mp4",
    output_path="compressed.mp4",
    crf=28,  # 质量参数 18-28
    preset='medium'  # 速度: ultrafast/fast/medium/slow
)
print(f"压缩比: {result['compression_ratio']:.2%}")
```

### 3. 调整分辨率
```python
from tools.video_converter import resize_video

# 缩小到720p
result = resize_video(
    input_path="1080p.mp4",
    output_path="720p.mp4",
    width=1280,
    height=720
)

# 或按比例缩放
result = resize_video(
    input_path="input.mp4",
    output_path="output.mp4",
    scale=0.5  # 缩小一半
)
```

### 4. 提取音频
```python
from tools.video_converter import extract_audio

result = extract_audio(
    input_path="video.mp4",
    output_path="audio.mp3",
    bitrate='192k'
)
```

## 应用场景

### 场景1: 自动剪辑会议录像
```python
from tools.video_editor import cut_video, add_text

# 1. 剪掉开头和结尾
cut_video("meeting.mp4", "temp.mp4", start_time=30, end_time=3600)

# 2. 添加标题
add_text(
    "temp.mp4", "final.mp4",
    text="技术分享会 2026-04-14",
    position=('center', 'top'),
    duration=5
)
```

### 场景2: 批量转换格式
```python
from tools.video_converter import convert_format
from pathlib import Path

for video in Path("./videos").glob("*.avi"):
    output = video.with_suffix(".mp4")
    convert_format(str(video), str(output))
```

### 场景3: 压缩大文件
```python
from tools.video_converter import compress_video

result = compress_video(
    "large_video.mp4",
    "compressed.mp4",
    crf=28,
    preset='fast'
)
print(f"原始: {result['original_size_mb']:.1f}MB")
print(f"压缩后: {result['compressed_size_mb']:.1f}MB")
```

## 性能说明

- **剪辑速度**: 约为视频时长的 0.5-1 倍（取决于编码器）
- **转码速度**: 约为视频时长的 1-2 倍
- **压缩效果**: crf=23 可减小 30-50% 文件大小

## 常见问题

### Q: 提示找不到 ffmpeg
A: 需要系统安装 ffmpeg 并添加到 PATH

### Q: 处理速度慢
A: 使用 preset='ultrafast' 或 preset='fast' 加速

### Q: 添加文字报错
A: moviepy 的 TextClip 需要 ImageMagick，建议使用简单文字

## 限制

- 不支持字幕文件（SRT/ASS），需要额外开发
- 文字样式有限，复杂排版建议用专业工具
- 大文件处理需要足够内存
