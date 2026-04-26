"""
示例2: 批量转换视频格式
功能: 将目录下所有AVI转为MP4
"""
import sys
sys.path.insert(0, '..')
from tools.video_converter import convert_format
from pathlib import Path


def batch_convert(input_dir, output_dir, from_ext='.avi', to_ext='.mp4'):
    """批量转换格式"""
    input_path = Path(input_dir)
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    # 查找所有视频
    videos = list(input_path.glob(f'*{from_ext}'))
    print(f"找到 {len(videos)} 个{from_ext}文件\n")
    
    success_count = 0
    for i, video in enumerate(videos, 1):
        output_file = output_path / video.with_suffix(to_ext).name
        
        print(f"[{i}/{len(videos)}] 转换: {video.name}")
        result = convert_format(str(video), str(output_file))
        
        if result['success']:
            print(f"  ✓ 完成: {output_file.name}\n")
            success_count += 1
        else:
            print(f"  ✗ 失败: {result['error']}\n")
    
    print(f"\n转换完成: {success_count}/{len(videos)}")


if __name__ == '__main__':
    # 使用示例
    batch_convert(
        input_dir="./videos_avi",
        output_dir="./videos_mp4",
        from_ext='.avi',
        to_ext='.mp4'
    )
