# 播客制作流程 SOP

## 概述
整合音频剪辑、降噪、混音、拼接功能，实现完整播客制作流程。

## 工具依赖
- `temp/tools/audio_toolkit.py` - 基础音频操作
- `temp/tools/audio_enhance.py` - 音频增强
- 依赖: pydub, ffmpeg

## 完整流程

### 1. 准备素材
```python
# 素材清单
intro_file = "intro.mp3"      # 片头音乐
content_file = "content.mp3"  # 正文录音
outro_file = "outro.mp3"      # 片尾音乐
bgm_file = "bgm.mp3"          # 背景音乐（可选）
```

### 2. 音频预处理
```python
from tools.audio_enhance import enhance_voice, normalize_volume

# 正文降噪+音量均衡
enhanced_content = enhance_voice(content_file, "content_enhanced.mp3", target_dBFS=-20.0)

# 片头片尾音量统一
normalize_volume(intro_file, "intro_normalized.mp3", target_dBFS=-20.0)
normalize_volume(outro_file, "outro_normalized.mp3", target_dBFS=-20.0)
```

### 3. 混音（可选）
```python
from tools.audio_enhance import mix_audio

# 正文添加背景音乐
mixed_content = mix_audio(
    "content_enhanced.mp3",
    bgm_file,
    "content_mixed.mp3",
    voice_volume=0,      # 人声保持原音量
    bgm_volume=-18       # 背景音乐降低18dB
)
```

### 4. 拼接成品
```python
from tools.audio_toolkit import merge_audios

# 拼接：片头 + 正文 + 片尾
final_podcast = merge_audios(
    ["intro_normalized.mp3", "content_mixed.mp3", "outro_normalized.mp3"],
    "final_podcast.mp3"
)
```

## 一键制作函数

```python
def produce_podcast(intro, content, outro, bgm=None, output="podcast.mp3"):
    """
    一键制作播客
    
    Args:
        intro: 片头音频文件
        content: 正文音频文件
        outro: 片尾音频文件
        bgm: 背景音乐文件（可选）
        output: 输出文件名
    
    Returns:
        最终播客文件路径
    """
    import sys
    sys.path.append('./tools')
    from audio_toolkit import merge_audios
    from audio_enhance import enhance_voice, normalize_volume, mix_audio
    import os
    
    temp_files = []
    
    # Step 1: 预处理
    intro_norm = "temp_intro.mp3"
    content_enh = "temp_content.mp3"
    outro_norm = "temp_outro.mp3"
    
    normalize_volume(intro, intro_norm, -20.0)
    enhance_voice(content, content_enh, -20.0)
    normalize_volume(outro, outro_norm, -20.0)
    
    temp_files.extend([intro_norm, content_enh, outro_norm])
    
    # Step 2: 混音（如果有BGM）
    if bgm:
        content_mixed = "temp_mixed.mp3"
        mix_audio(content_enh, bgm, content_mixed, voice_volume=0, bgm_volume=-18)
        temp_files.append(content_mixed)
        content_final = content_mixed
    else:
        content_final = content_enh
    
    # Step 3: 拼接
    merge_audios([intro_norm, content_final, outro_norm], output)
    
    # Step 4: 清理临时文件
    for f in temp_files:
        if os.path.exists(f):
            os.remove(f)
    
    return output
```

## 使用示例

### 基础播客（无BGM）
```python
produce_podcast(
    intro="intro.mp3",
    content="recording.mp3",
    outro="outro.mp3",
    output="my_podcast.mp3"
)
```

### 完整播客（含BGM）
```python
produce_podcast(
    intro="intro.mp3",
    content="recording.mp3",
    outro="outro.mp3",
    bgm="background_music.mp3",
    output="my_podcast_with_bgm.mp3"
)
```

## 参数调优

### 音量建议
- 播客标准: -20 dBFS
- 音乐标准: -14 dBFS
- 广播标准: -6 dBFS

### BGM音量
- 纯音乐段: -10 dB
- 人声段背景: -15 到 -20 dB

### 降噪参数
- 人声频段: 80Hz - 8000Hz
- 音乐频段: 20Hz - 20000Hz

## 注意事项
1. 所有素材建议使用相同采样率（44.1kHz或48kHz）
2. 片头片尾建议控制在5-10秒
3. BGM选择无版权音乐
4. 导出前试听检查音量平衡

[skill_mapping]
category: media_processing
skill: podcast_production
tools: audio_toolkit.py, audio_enhance.py
[/skill_mapping]

## [record_on_use]
执行完本SOP后，调用以下命令记录使用情况：
```python
import sys
sys.path.append('../memory')
from autonomous_operation_sop.helper import record_skill_usage
record_skill_usage('podcast_production_sop.md')
```