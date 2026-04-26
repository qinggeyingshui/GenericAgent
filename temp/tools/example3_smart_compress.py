"""
示例3: 智能压缩视频
功能: 根据文件大小自动选择压缩参数
"""
import sys
sys.path.insert(0, '..')
from tools.video_converter import compress_video, get_video_info
import os


def smart_compress(input_path, output_path, target_size_mb=None):
    """智能压缩视频"""
    # 获取原始信息
    original_size = os.path.getsize(input_path) / (1024 * 1024)
    info = get_video_info(input_path)
    
    print(f"原始文件: {input_path}")
    print(f"  大小: {original_size:.1f}MB")
    print(f"  分辨率: {info['width']}x{info['height']}")
    print(f"  时长: {info['duration']:.1f}秒\n")
    
    # 根据大小选择压缩参数
    if original_size < 50:
        print("文件较小，使用轻度压缩")
        crf, preset = 23, 'medium'
    elif original_size < 200:
        print("文件中等，使用标准压缩")
        crf, preset = 26, 'medium'
    else:
        print("文件较大，使用高度压缩")
        crf, preset = 28, 'fast'
    
    # 执行压缩
    print(f"\n压缩参数: crf={crf}, preset={preset}")
    result = compress_video(
        input_path,
        output_path,
        crf=crf,
        preset=preset
    )
    
    if result['success']:
        print(f"\n✓ 压缩完成!")
        print(f"  原始: {result['original_size_mb']:.1f}MB")
        print(f"  压缩后: {result['compressed_size_mb']:.1f}MB")
        print(f"  压缩比: {result['compression_ratio']:.1%}")
        print(f"  节省: {result['original_size_mb'] - result['compressed_size_mb']:.1f}MB")
    else:
        print(f"\n✗ 压缩失败: {result['error']}")


if __name__ == '__main__':
    # 使用示例
    smart_compress(
        input_path="large_video.mp4",
        output_path="compressed.mp4"
    )
