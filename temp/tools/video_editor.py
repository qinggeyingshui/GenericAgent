"""
视频剪辑工具包
提供视频剪辑、合并、添加文字/音频等核心功能
依赖: moviepy
"""
from moviepy.editor import VideoFileClip, concatenate_videoclips, TextClip, CompositeVideoClip, AudioFileClip
from pathlib import Path
import os


def cut_video(input_path, output_path, start_time=0, end_time=None):
    """
    剪辑视频片段
    
    Args:
        input_path: 输入视频路径
        output_path: 输出视频路径
        start_time: 开始时间(秒)
        end_time: 结束时间(秒)，None表示到结尾
    
    Returns:
        dict: {'success': bool, 'output': str, 'duration': float}
    """
    try:
        video = VideoFileClip(input_path)
        
        # 剪辑
        if end_time is None:
            end_time = video.duration
        
        clipped = video.subclip(start_time, end_time)
        
        # 输出
        clipped.write_videofile(output_path, codec='libx264', audio_codec='aac')
        
        duration = clipped.duration
        
        # 清理
        clipped.close()
        video.close()
        
        return {
            'success': True,
            'output': output_path,
            'duration': duration
        }
    except Exception as e:
        return {'success': False, 'error': str(e)}


def merge_videos(input_paths, output_path, method='compose'):
    """
    合并多个视频
    
    Args:
        input_paths: 输入视频路径列表
        output_path: 输出视频路径
        method: 合并方式 ('compose'顺序拼接 或 'stack'并排)
    
    Returns:
        dict: {'success': bool, 'output': str, 'duration': float}
    """
    try:
        clips = [VideoFileClip(p) for p in input_paths]
        
        if method == 'compose':
            # 顺序拼接
            final = concatenate_videoclips(clips)
        else:
            return {'success': False, 'error': '暂不支持stack模式'}
        
        final.write_videofile(output_path, codec='libx264', audio_codec='aac')
        
        duration = final.duration
        
        # 清理
        final.close()
        for clip in clips:
            clip.close()
        
        return {
            'success': True,
            'output': output_path,
            'duration': duration
        }
    except Exception as e:
        return {'success': False, 'error': str(e)}


def add_text(input_path, output_path, text, position=('center', 'bottom'),
             fontsize=50, color='white', duration=None, start_time=0):
    """
    添加文字到视频
    
    Args:
        input_path: 输入视频路径
        output_path: 输出视频路径
        text: 文字内容
        position: 位置 ('center', 'top') 或 (x, y)
        fontsize: 字体大小
        color: 颜色
        duration: 文字显示时长(秒)，None表示全程
        start_time: 文字开始时间(秒)
    
    Returns:
        dict: {'success': bool, 'output': str}
    """
    try:
        video = VideoFileClip(input_path)
        
        # 创建文字
        txt_clip = TextClip(text, fontsize=fontsize, color=color)
        
        # 设置时长
        if duration is None:
            duration = video.duration - start_time
        
        txt_clip = txt_clip.set_duration(duration).set_start(start_time)
        
        # 设置位置
        txt_clip = txt_clip.set_position(position)
        
        # 合成
        final = CompositeVideoClip([video, txt_clip])
        
        final.write_videofile(output_path, codec='libx264', audio_codec='aac')
        
        # 清理
        final.close()
        txt_clip.close()
        video.close()
        
        return {'success': True, 'output': output_path}
    except Exception as e:
        return {'success': False, 'error': str(e)}


def add_audio(input_path, output_path, audio_path, start_time=0, volume=1.0):
    """
    添加音频到视频
    
    Args:
        input_path: 输入视频路径
        output_path: 输出视频路径
        audio_path: 音频文件路径
        start_time: 音频开始时间(秒)
        volume: 音量(0.0-1.0)
    
    Returns:
        dict: {'success': bool, 'output': str}
    """
    try:
        video = VideoFileClip(input_path)
        audio = AudioFileClip(audio_path)
        
        # 调整音量
        audio = audio.volumex(volume)
        
        # 设置开始时间
        audio = audio.set_start(start_time)
        
        # 合成音频
        final = video.set_audio(audio)
        
        final.write_videofile(output_path, codec='libx264', audio_codec='aac')
        
        # 清理
        final.close()
        audio.close()
        video.close()
        
        return {'success': True, 'output': output_path}
    except Exception as e:
        return {'success': False, 'error': str(e)}


def get_video_info(input_path):
    """
    获取视频信息
    
    Args:
        input_path: 视频路径
    
    Returns:
        dict: {'duration': float, 'fps': float, 'size': tuple, 'has_audio': bool}
    """
    try:
        video = VideoFileClip(input_path)
        
        info = {
            'duration': video.duration,
            'fps': video.fps,
            'size': video.size,
            'has_audio': video.audio is not None
        }
        
        video.close()
        
        return info
    except Exception as e:
        return {'error': str(e)}


if __name__ == '__main__':
    # 测试代码
    print("视频剪辑工具包")
    print("功能: cut_video, merge_videos, add_text, add_audio, get_video_info")
