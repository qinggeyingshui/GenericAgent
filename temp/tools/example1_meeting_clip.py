"""
示例1: 自动剪辑会议录像
功能: 剪掉开头结尾 + 添加标题
"""
import sys
sys.path.insert(0, '..')
from tools.video_editor import cut_video, add_text


def process_meeting_video(input_path, output_path, title, skip_start=30, skip_end=10):
    """处理会议录像"""
    print(f"处理会议录像: {input_path}")
    
    # 1. 获取视频信息
    from tools.video_editor import get_video_info
    info = get_video_info(input_path)
    duration = info['duration']
    print(f"原始时长: {duration:.1f}秒")
    
    # 2. 剪掉开头和结尾
    temp_path = "temp_cut.mp4"
    print(f"\n剪辑: 跳过前{skip_start}秒和后{skip_end}秒...")
    result = cut_video(
        input_path,
        temp_path,
        start_time=skip_start,
        end_time=duration - skip_end
    )
    
    if not result['success']:
        print(f"剪辑失败: {result['error']}")
        return
    
    print(f"✓ 剪辑完成，时长: {result['duration']:.1f}秒")
    
    # 3. 添加标题（显示5秒）
    print(f"\n添加标题: {title}")
    result = add_text(
        temp_path,
        output_path,
        text=title,
        position=('center', 'top'),
        fontsize=60,
        color='white',
        duration=5
    )
    
    if result['success']:
        print(f"✓ 处理完成: {output_path}")
        # 删除临时文件
        import os
        os.remove(temp_path)
    else:
        print(f"添加标题失败: {result['error']}")


if __name__ == '__main__':
    # 使用示例
    process_meeting_video(
        input_path="meeting_raw.mp4",
        output_path="meeting_final.mp4",
        title="技术分享会 2026-04-14",
        skip_start=30,
        skip_end=10
    )
