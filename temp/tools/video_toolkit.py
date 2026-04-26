"""
视频处理工具包
依赖: moviepy (已安装), ffmpeg (命令行工具)
功能: 视频剪辑/合并/提取帧/添加字幕
"""
from moviepy import VideoFileClip, concatenate_videoclips, TextClip, CompositeVideoClip
import os

def clip_video(input_path, output_path, start_time=0, end_time=None):
    """
    剪辑视频片段
    :param input_path: 输入视频路径
    :param output_path: 输出视频路径
    :param start_time: 开始时间(秒)
    :param end_time: 结束时间(秒)，None表示到结尾
    """
    video = VideoFileClip(input_path)
    if end_time is None:
        end_time = video.duration
    clipped = video.subclipped(start_time, end_time)
    clipped.write_videofile(output_path, codec="libx264", audio_codec="aac", logger=None)
    video.close()
    clipped.close()
    return output_path

def merge_videos(input_paths, output_path):
    """
    合并多个视频
    :param input_paths: 输入视频路径列表
    :param output_path: 输出视频路径
    """
    clips = [VideoFileClip(path) for path in input_paths]
    final = concatenate_videoclips(clips, method="compose")
    final.write_videofile(output_path, codec="libx264", audio_codec="aac")
    for clip in clips:
        clip.close()
    final.close()
    return output_path

def extract_frames(input_path, output_dir, fps=1):
    """
    提取视频帧为图片
    :param input_path: 输入视频路径
    :param output_dir: 输出目录
    :param fps: 每秒提取帧数
    """
    os.makedirs(output_dir, exist_ok=True)
    video = VideoFileClip(input_path)
    frame_count = 0
    interval = 1.0 / fps
    t = 0
    while t < video.duration:
        frame = video.get_frame(t)
        from PIL import Image
        img = Image.fromarray(frame)
        img.save(os.path.join(output_dir, f"frame_{frame_count:04d}.png"))
        frame_count += 1
        t += interval
    video.close()
    return frame_count

def add_subtitles(input_path, output_path, subtitles):
    """
    添加字幕到视频
    :param input_path: 输入视频路径
    :param output_path: 输出视频路径
    :param subtitles: 字幕列表 [(start_time, end_time, text), ...]
    """
    video = VideoFileClip(input_path)
    txt_clips = []
    for start, end, text in subtitles:
        txt_clip = TextClip(text, fontsize=24, color="white", bg_color="black")
        txt_clip = txt_clip.set_position(("center", "bottom")).set_start(start).set_duration(end - start)
        txt_clips.append(txt_clip)
    final = CompositeVideoClip([video] + txt_clips)
    final.write_videofile(output_path, codec="libx264", audio_codec="aac")
    video.close()
    final.close()
    return output_path

if __name__ == "__main__":
    print("视频处理工具包加载成功")
    print("可用函数: clip_video, merge_videos, extract_frames, add_subtitles")