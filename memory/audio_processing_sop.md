# 音频处理 SOP

## 工具
- `temp/tools/audio_toolkit.py`
- 依赖: pydub (pip install pydub)

## 功能清单

### 1. 剪辑音频
```python
from temp.tools.audio_toolkit import clip_audio
clip_audio('input.mp3', 'output.mp3', start_ms=5000, end_ms=15000)
```

### 2. 格式转换
```python
from temp.tools.audio_toolkit import convert_format
convert_format('input.mp3', 'output.wav')  # 支持mp3/wav/ogg/flac
```

### 3. 音量调整
```python
from temp.tools.audio_toolkit import adjust_volume
adjust_volume('input.mp3', 'output.mp3', volume_change_db=5)  # 增加5dB
```

### 4. 合并音频
```python
from temp.tools.audio_toolkit import merge_audios
merge_audios(['part1.mp3', 'part2.mp3'], 'merged.mp3')
```

### 5. 音频增强（R147新增）
```python
from tools.audio_enhance import reduce_noise, mix_audio, normalize_volume, enhance_voice

# 降噪处理（去除背景噪音）
reduce_noise('input.mp3', 'output_clean.mp3', low_cutoff=80, high_cutoff=8000)

# 混音处理（人声+背景音乐）
mix_audio('voice.mp3', 'bgm.mp3', 'mixed.mp3', voice_volume=0, bgm_volume=-10)

# 音量均衡（自动调整到标准响度）
normalize_volume('input.mp3', 'output_normalized.mp3', target_dBFS=-20.0)

# 一键增强（降噪+音量均衡）
enhance_voice('input.mp3', 'output_enhanced.mp3')
```

**功能说明**：
- **降噪**: 使用高通/低通滤波器去除噪音（人声频段80Hz-8000Hz）
- **混音**: 支持音量调整和背景音乐循环播放
- **音量均衡**: 支持多种标准（播客-20dBFS/音乐-14dBFS/广播-6dBFS）
- **一键增强**: 适合快速处理播客、视频配音

**参数说明**：
- `low_cutoff`: 高通滤波器截止频率，去除低频噪音（如空调声）
- `high_cutoff`: 低通滤波器截止频率，去除高频噪音（如电流声）
- `voice_volume`: 人声音量调整(dB)，正值增大，负值减小
- `bgm_volume`: 背景音乐音量调整(dB)，建议-10到-15dB
- `target_dBFS`: 目标响度，-20适合播客，-14适合音乐，-6适合广播

## 应用场景
- 播客/视频配音剪辑
- 音频格式批量转换
- 背景音乐音量调整
- 多段音频拼接

## 注意事项
- 时间单位为毫秒(ms)
- 音量调整单位为分贝(dB)，正值增大，负值减小
- 支持格式: mp3, wav, ogg, flac

---

## 5. Audio Enhancement (R171, 2026-04-20)

Tool: tools/audio_enhance.py

```python
from audio_enhance import reduce_noise, normalize_volume, mix_audio, enhance_audio

# Noise reduction
result = reduce_noise("input.mp3", "output_clean.mp3", noise_reduction_db=15)

# Volume normalization
result = normalize_volume("input.mp3", "output_normalized.mp3", target_db=-20)

# Audio mixing
result = mix_audio(["audio1.mp3", "audio2.mp3"], "mixed.mp3", volumes=[0.8, 0.5])

# Comprehensive enhancement
result = enhance_audio("input.mp3", "enhanced.mp3", reduce_noise=True, normalize=True)
```

Functions:
- reduce_noise(input, output, noise_reduction_db): Reduce background noise
- normalize_volume(input, output, target_db): Normalize volume level
- mix_audio(audio_files, output, volumes): Mix multiple audio files
- enhance_audio(input, output, reduce_noise, normalize): Comprehensive enhancement

Note: Requires pydub and ffmpeg for actual audio processing

[skill_mapping]
category: media_processing
skill: audio_enhance
tools: audio_toolkit.py, audio_enhance.py
[/skill_mapping]

## [record_on_use]
执行完本SOP后，调用以下命令记录使用情况：
```python
import sys
sys.path.append('../memory')
from autonomous_operation_sop.helper import record_skill_usage
record_skill_usage('audio_processing_sop.md')
```
