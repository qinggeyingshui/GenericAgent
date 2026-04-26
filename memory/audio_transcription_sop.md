# audio_transcription_sop.md — 音频转文字SOP（R200, 2026-04-21）

工具: tools/audio_transcription.py | 基于speech_recognition+pydub

## 核心函数

```python
from audio_transcription import AudioTranscriber, quick_transcribe

# 快速转录
output_path = quick_transcribe("audio.mp3", output_format="txt")

# 完整使用
transcriber = AudioTranscriber(language="zh-CN")
result = transcriber.transcribe("audio.mp3")
# 返回: {"success": True, "text": "...", "language": "zh-CN", "engine": "google"}

# 长音频分段转录
results = transcriber.transcribe_long_audio("long_audio.mp3", chunk_length_ms=30000)
# 返回: [{"index": 0, "start_time": 0, "text": "..."}, ...]

# 导出格式
transcriber.export_txt(result, "output.txt")      # 纯文本
transcriber.export_srt(results, "output.srt")     # 字幕文件
transcriber.export_json(result, "output.json")    # JSON格式
```

## 支持格式

**输入格式**:
- mp3
- wav
- m4a
- flac

**输出格式**:
- TXT: 纯文本
- SRT: 字幕文件（带时间轴）
- JSON: 结构化数据

## 使用场景

### 1. 视频字幕生成
```python
transcriber = AudioTranscriber()
results = transcriber.transcribe_long_audio("video_audio.mp3")
transcriber.export_srt(results, "subtitles.srt")
```

### 2. 音频内容提取
```python
result = transcriber.transcribe("podcast.mp3")
transcriber.export_txt(result, "transcript.txt")
```

### 3. 会议记录
```python
result = transcriber.transcribe("meeting.wav")
transcriber.export_json(result, "meeting_notes.json")
```

## 参数说明

### AudioTranscriber
- `language`: 识别语言（默认"zh-CN"）
  - "zh-CN": 中文
  - "en-US": 英文
  - "ja-JP": 日文

### transcribe
- `audio_path`: 音频文件路径
- `engine`: 识别引擎（默认"google"）
  - "google": Google Speech Recognition（在线，准确率高）
  - "sphinx": CMU Sphinx（离线，准确率较低）

### transcribe_long_audio
- `audio_path`: 音频文件路径
- `chunk_length_ms`: 分段长度（毫秒，默认30000=30秒）

## 返回格式

### 单次转录
```json
{
  "success": true,
  "text": "转录的文本内容",
  "language": "zh-CN",
  "engine": "google"
}
```

### 长音频转录
```json
[
  {
    "index": 0,
    "start_time": 0.0,
    "text": "第一段文本"
  },
  {
    "index": 1,
    "start_time": 30.0,
    "text": "第二段文本"
  }
]
```

## 依赖安装

```bash
pip install SpeechRecognition pydub

# 如需处理mp3等格式，还需安装ffmpeg
# Windows: 下载ffmpeg.exe放到PATH
# macOS: brew install ffmpeg
# Linux: apt-get install ffmpeg
```

## 注意事项

1. **网络依赖**: Google引擎需要网络连接
2. **音频质量**: 清晰的音频可提高准确率
3. **语言设置**: 确保language参数与音频语言匹配
4. **长音频**: 建议使用transcribe_long_audio分段处理
5. **格式转换**: 自动转换为WAV格式，需要pydub和ffmpeg

[skill_mapping]
category: media_processing
skill: speech_recognition
tools: audio_transcription.py
[/skill_mapping]

## [record_on_use]
执行完本SOP后，调用以下命令记录使用情况：
```python
import sys
sys.path.append('../memory')
from autonomous_operation_sop.helper import record_skill_usage
record_skill_usage('audio_transcription_sop.md')
```