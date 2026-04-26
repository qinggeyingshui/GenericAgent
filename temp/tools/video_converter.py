"""
视频转码工具包
提供视频格式转换、压缩、分辨率调整等功能
依赖: ffmpeg-python (需要系统安装ffmpeg)
"""
import ffmpeg
from pathlib import Path
import os


def convert_format(input_path, output_path, video_codec='libx264', audio_codec='aac'):
    """
    转换视频格式
    
    Args:
        input_path: 输入视频路径
        output_path: 输出视频路径
        video_codec: 视频编码器 (libx264, libx265, vp9等)
        audio_codec: 音频编码器 (aac, mp3, opus等)
    
    Returns:
        dict: {'success': bool, 'output': str, 'error': str}
    """
    try:
        stream = ffmpeg.input(input_path)
        stream = ffmpeg.output(stream, output_path, vcodec=video_codec, acodec=audio_codec)
        ffmpeg.run(stream, overwrite_output=True, capture_stdout=True, capture_stderr=True)
        
        return {'success': True, 'output': output_path}
    except ffmpeg.Error as e:
        return {'success': False, 'error': e.stderr.decode() if e.stderr else str(e)}
    except Exception as e:
        return {'success': False, 'error': str(e)}


def compress_video(input_path, output_path, crf=23, preset='medium'):
    """
    压缩视频
    
    Args:
        input_path: 输入视频路径
        output_path: 输出视频路径
        crf: 质量参数 (0-51, 越小质量越高, 推荐18-28)
        preset: 压缩速度 (ultrafast, fast, medium, slow, veryslow)
    
    Returns:
        dict: {'success': bool, 'output': str, 'compression_ratio': float}
    """
    try:
        # 获取原始大小
        original_size = os.path.getsize(input_path)
        
        stream = ffmpeg.input(input_path)
        stream = ffmpeg.output(stream, output_path, 
                              vcodec='libx264', crf=crf, preset=preset,
                              acodec='aac')
        ffmpeg.run(stream, overwrite_output=True, capture_stdout=True, capture_stderr=True)
        
        # 计算压缩比
        compressed_size = os.path.getsize(output_path)
        ratio = compressed_size / original_size
        
        return {
            'success': True,
            'output': output_path,
            'compression_ratio': ratio,
            'original_size_mb': original_size / (1024*1024),
            'compressed_size_mb': compressed_size / (1024*1024)
        }
    except ffmpeg.Error as e:
        return {'success': False, 'error': e.stderr.decode() if e.stderr else str(e)}
    except Exception as e:
        return {'success': False, 'error': str(e)}


def resize_video(input_path, output_path, width=None, height=None, scale=None):
    """
    调整视频分辨率
    
    Args:
        input_path: 输入视频路径
        output_path: 输出视频路径
        width: 目标宽度
        height: 目标高度
        scale: 缩放比例 (如0.5表示缩小一半)
    
    Returns:
        dict: {'success': bool, 'output': str}
    """
    try:
        stream = ffmpeg.input(input_path)
        
        if scale:
            # 按比例缩放
            stream = ffmpeg.filter(stream, 'scale', f'iw*{scale}', f'ih*{scale}')
        elif width and height:
            # 指定宽高
            stream = ffmpeg.filter(stream, 'scale', width, height)
        elif width:
            # 只指定宽度，高度自动
            stream = ffmpeg.filter(stream, 'scale', width, -1)
        elif height:
            # 只指定高度，宽度自动
            stream = ffmpeg.filter(stream, 'scale', -1, height)
        else:
            return {'success': False, 'error': '必须指定width/height/scale之一'}
        
        stream = ffmpeg.output(stream, output_path, vcodec='libx264', acodec='aac')
        ffmpeg.run(stream, overwrite_output=True, capture_stdout=True, capture_stderr=True)
        
        return {'success': True, 'output': output_path}
    except ffmpeg.Error as e:
        return {'success': False, 'error': e.stderr.decode() if e.stderr else str(e)}
    except Exception as e:
        return {'success': False, 'error': str(e)}


def extract_audio(input_path, output_path, audio_codec='mp3', bitrate='192k'):
    """
    提取视频中的音频
    
    Args:
        input_path: 输入视频路径
        output_path: 输出音频路径
        audio_codec: 音频格式 (mp3, aac, wav等)
        bitrate: 比特率
    
    Returns:
        dict: {'success': bool, 'output': str}
    """
    try:
        stream = ffmpeg.input(input_path)
        stream = ffmpeg.output(stream, output_path, acodec=audio_codec, audio_bitrate=bitrate)
        ffmpeg.run(stream, overwrite_output=True, capture_stdout=True, capture_stderr=True)
        
        return {'success': True, 'output': output_path}
    except ffmpeg.Error as e:
        return {'success': False, 'error': e.stderr.decode() if e.stderr else str(e)}
    except Exception as e:
        return {'success': False, 'error': str(e)}


def get_video_info(input_path):
    """
    获取视频详细信息
    
    Args:
        input_path: 视频路径
    
    Returns:
        dict: 视频信息
    """
    try:
        probe = ffmpeg.probe(input_path)
        
        video_stream = next((s for s in probe['streams'] if s['codec_type'] == 'video'), None)
        audio_stream = next((s for s in probe['streams'] if s['codec_type'] == 'audio'), None)
        
        info = {
            'format': probe['format']['format_name'],
            'duration': float(probe['format']['duration']),
            'size_mb': int(probe['format']['size']) / (1024*1024),
            'bitrate': int(probe['format']['bit_rate']) / 1000  # kbps
        }
        
        if video_stream:
            info['video'] = {
                'codec': video_stream['codec_name'],
                'width': video_stream['width'],
                'height': video_stream['height'],
                'fps': eval(video_stream.get('r_frame_rate', '0/1'))
            }
        
        if audio_stream:
            info['audio'] = {
                'codec': audio_stream['codec_name'],
                'sample_rate': audio_stream.get('sample_rate'),
                'channels': audio_stream.get('channels')
            }
        
        return {'success': True, 'info': info}
    except Exception as e:
        return {'success': False, 'error': str(e)}


if __name__ == '__main__':
    # 测试代码
    print("视频转码工具包")
    print("支持的功能:")
    print("  - convert_format: 格式转换")
    print("  - compress_video: 视频压缩")
    print("  - resize_video: 分辨率调整")
    print("  - extract_audio: 提取音频")
    print("  - get_video_info: 获取视频信息")
