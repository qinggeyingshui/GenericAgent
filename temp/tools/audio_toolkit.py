"""音频处理工具包 - 基于pydub"""
from pydub import AudioSegment
import os

def clip_audio(input_path, output_path, start_ms=0, end_ms=None):
    """剪辑音频片段 (毫秒)"""
    audio = AudioSegment.from_file(input_path)
    clipped = audio[start_ms:end_ms]
    clipped.export(output_path, format=output_path.split(".")[-1])
    return output_path

def convert_format(input_path, output_path):
    """格式转换 (自动识别扩展名)"""
    audio = AudioSegment.from_file(input_path)
    audio.export(output_path, format=output_path.split(".")[-1])
    return output_path

def adjust_volume(input_path, output_path, db_change):
    """调整音量 (db_change: +增大 -减小)"""
    audio = AudioSegment.from_file(input_path)
    adjusted = audio + db_change
    adjusted.export(output_path, format=output_path.split(".")[-1])
    return output_path

def merge_audios(input_paths, output_path):
    """合并多个音频"""
    combined = AudioSegment.empty()
    for path in input_paths:
        combined += AudioSegment.from_file(path)
    combined.export(output_path, format=output_path.split(".")[-1])
    return output_path

if __name__ == "__main__":
    print("音频处理工具已加载")
    print("函数: clip_audio, convert_format, adjust_volume, merge_audios")