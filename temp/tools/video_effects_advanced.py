"""
video_effects_advanced.py — 视频高级特效工具（R175, 2026-04-20）

提供3类高级特效：
1. 滤镜 - 黑白/复古/锐化/模糊/亮度对比度
2. 特效 - 慢动作/快进/倒放/镜像/裁剪
3. 画中画 - 多视频叠加

依赖: moviepy, numpy, PIL
"""

from moviepy import VideoFileClip, CompositeVideoClip
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter


# ══════════════════════════════════════════════════════
# 滤镜效果
# ══════════════════════════════════════════════════════

def apply_filter(video_path, output_path, filter_type="grayscale", **params):
    """
    应用滤镜效果
    
    Args:
        video_path: 输入视频路径
        output_path: 输出视频路径
        filter_type: 滤镜类型 ("grayscale"|"sepia"|"blur"|"sharpen"|"brightness"|"contrast")
        **params: 滤镜参数
            - blur: radius=5
            - brightness: factor=1.5 (>1变亮, <1变暗)
            - contrast: factor=1.5 (>1增强, <1减弱)
    
    Returns:
        output_path: 输出文件路径
    """
    clip = VideoFileClip(video_path)
    
    if filter_type == "grayscale":
        filtered = _apply_grayscale(clip)
    elif filter_type == "sepia":
        filtered = _apply_sepia(clip)
    elif filter_type == "blur":
        radius = params.get("radius", 5)
        filtered = _apply_blur(clip, radius)
    elif filter_type == "sharpen":
        filtered = _apply_sharpen(clip)
    elif filter_type == "brightness":
        factor = params.get("factor", 1.5)
        filtered = _apply_brightness(clip, factor)
    elif filter_type == "contrast":
        factor = params.get("factor", 1.5)
        filtered = _apply_contrast(clip, factor)
    else:
        raise ValueError(f"不支持的滤镜类型: {filter_type}")
    
    filtered.write_videofile(output_path, codec="libx264", audio_codec="aac", logger=None)
    
    clip.close()
    filtered.close()
    
    return output_path


def _apply_grayscale(clip):
    """黑白滤镜"""
    def grayscale_frame(get_frame, t):
        frame = get_frame(t)
        img = Image.fromarray(frame)
        gray = img.convert('L').convert('RGB')
        return np.array(gray)
    
    return clip.transform(grayscale_frame)


def _apply_sepia(clip):
    """复古棕褐色滤镜"""
    def sepia_frame(frame):
        # 转换为PIL Image
        img = Image.fromarray(frame)
        
        # 应用sepia矩阵
        r, g, b = img.split()
        r_arr = np.array(r)
        g_arr = np.array(g)
        b_arr = np.array(b)
        
        new_r = np.clip(0.393 * r_arr + 0.769 * g_arr + 0.189 * b_arr, 0, 255).astype(np.uint8)
        new_g = np.clip(0.349 * r_arr + 0.686 * g_arr + 0.168 * b_arr, 0, 255).astype(np.uint8)
        new_b = np.clip(0.272 * r_arr + 0.534 * g_arr + 0.131 * b_arr, 0, 255).astype(np.uint8)
        
        result = Image.merge("RGB", (Image.fromarray(new_r), Image.fromarray(new_g), Image.fromarray(new_b)))
        return np.array(result)
    
    return clip.transform(sepia_frame)


def _apply_blur(clip, radius):
    """模糊滤镜"""
    def blur_frame(frame):
        img = Image.fromarray(frame)
        blurred = img.filter(ImageFilter.GaussianBlur(radius))
        return np.array(blurred)
    
    return clip.transform(blur_frame)


def _apply_sharpen(clip):
    """锐化滤镜"""
    def sharpen_frame(frame):
        img = Image.fromarray(frame)
        sharpened = img.filter(ImageFilter.SHARPEN)
        return np.array(sharpened)
    
    return clip.transform(sharpen_frame)


def _apply_brightness(clip, factor):
    """亮度调整"""
    def brightness_frame(frame):
        img = Image.fromarray(frame)
        enhancer = ImageEnhance.Brightness(img)
        enhanced = enhancer.enhance(factor)
        return np.array(enhanced)
    
    return clip.transform(brightness_frame)


def _apply_contrast(clip, factor):
    """对比度调整"""
    def contrast_frame(frame):
        img = Image.fromarray(frame)
        enhancer = ImageEnhance.Contrast(img)
        enhanced = enhancer.enhance(factor)
        return np.array(enhanced)
    
    return clip.transform(contrast_frame)


# ══════════════════════════════════════════════════════
# 特效
# ══════════════════════════════════════════════════════

def apply_effect(video_path, output_path, effect_type="slow_motion", **params):
    """
    应用特效
    
    Args:
        video_path: 输入视频路径
        output_path: 输出视频路径
        effect_type: 特效类型 ("slow_motion"|"fast_forward"|"reverse"|"mirror"|"crop")
        **params: 特效参数
            - slow_motion: speed=0.5 (0.5倍速)
            - fast_forward: speed=2.0 (2倍速)
            - mirror: direction="horizontal"|"vertical"
            - crop: x1, y1, x2, y2 (裁剪区域)
    
    Returns:
        output_path: 输出文件路径
    """
    clip = VideoFileClip(video_path)
    
    if effect_type == "slow_motion":
        speed = params.get("speed", 0.5)
        result = clip.multiply_speed(speed)
    elif effect_type == "fast_forward":
        speed = params.get("speed", 2.0)
        result = clip.multiply_speed(speed)
    elif effect_type == "reverse":
        result = clip.with_effects([lambda c: c.with_fps(c.fps).reversed()])
    elif effect_type == "mirror":
        direction = params.get("direction", "horizontal")
        result = _apply_mirror(clip, direction)
    elif effect_type == "crop":
        x1 = params.get("x1", 0)
        y1 = params.get("y1", 0)
        x2 = params.get("x2", clip.w)
        y2 = params.get("y2", clip.h)
        result = clip.cropped(x1=x1, y1=y1, x2=x2, y2=y2)
    else:
        raise ValueError(f"不支持的特效类型: {effect_type}")
    
    result.write_videofile(output_path, codec="libx264", audio_codec="aac", logger=None)
    
    clip.close()
    result.close()
    
    return output_path


def _apply_mirror(clip, direction):
    """镜像翻转"""
    if direction == "horizontal":
        return clip.with_effects([("mirror_x",)])
    else:  # vertical
        return clip.with_effects([("mirror_y",)])


# ══════════════════════════════════════════════════════
# 画中画
# ══════════════════════════════════════════════════════

def add_picture_in_picture(main_video_path, pip_video_path, output_path, 
                          position="bottom-right", size_ratio=0.25, opacity=1.0, margin=20):
    """
    添加画中画效果
    
    Args:
        main_video_path: 主视频路径
        pip_video_path: 画中画视频路径
        output_path: 输出视频路径
        position: 位置 ("top-left"|"top-right"|"bottom-left"|"bottom-right"|"center")
        size_ratio: 画中画大小比例（相对于主视频宽度）
        opacity: 透明度 (0.0-1.0)
        margin: 边距（像素）
    
    Returns:
        output_path: 输出文件路径
    """
    main_clip = VideoFileClip(main_video_path)
    pip_clip = VideoFileClip(pip_video_path)
    
    # 调整画中画大小
    pip_width = int(main_clip.w * size_ratio)
    pip_clip_resized = pip_clip.resized(width=pip_width)
    
    # 设置透明度
    if opacity < 1.0:
        pip_clip_resized = pip_clip_resized.with_opacity(opacity)
    
    # 计算位置
    if position == "top-left":
        pos = (margin, margin)
    elif position == "top-right":
        pos = (main_clip.w - pip_clip_resized.w - margin, margin)
    elif position == "bottom-left":
        pos = (margin, main_clip.h - pip_clip_resized.h - margin)
    elif position == "bottom-right":
        pos = (main_clip.w - pip_clip_resized.w - margin, main_clip.h - pip_clip_resized.h - margin)
    else:  # center
        pos = ((main_clip.w - pip_clip_resized.w) // 2, (main_clip.h - pip_clip_resized.h) // 2)
    
    # 设置画中画位置和时长
    pip_clip_resized = pip_clip_resized.with_position(pos).with_duration(main_clip.duration)
    
    # 合成
    result = CompositeVideoClip([main_clip, pip_clip_resized])
    result.write_videofile(output_path, codec="libx264", audio_codec="aac", logger=None)
    
    main_clip.close()
    pip_clip.close()
    result.close()
    
    return output_path


# 便捷常量
GRAYSCALE = "grayscale"
SEPIA = "sepia"
BLUR = "blur"
SHARPEN = "sharpen"
BRIGHTNESS = "brightness"
CONTRAST = "contrast"

SLOW_MOTION = "slow_motion"
FAST_FORWARD = "fast_forward"
REVERSE = "reverse"
MIRROR = "mirror"
CROP = "crop"

TOP_LEFT = "top-left"
TOP_RIGHT = "top-right"
BOTTOM_LEFT = "bottom-left"
BOTTOM_RIGHT = "bottom-right"
CENTER = "center"