# 视频高级特效工具 SOP

**文件**: `temp/tools/video_effects_advanced.py`  
**创建**: R175, 2026-04-20  
**依赖**: moviepy, numpy, PIL

## 功能概览

提供3类高级视频特效：
1. **滤镜** - 图像处理效果
2. **特效** - 时间和空间变换
3. **画中画** - 多视频叠加合成

## 1. 滤镜功能

### apply_filter(video_path, output_path, filter_type, **params)

支持的滤镜类型：
- `grayscale` - 黑白滤镜
- `sepia` - 复古怀旧
- `blur` - 模糊效果 (params: radius=5)
- `sharpen` - 锐化增强
- `brightness` - 亮度调整 (params: factor=1.5)
- `contrast` - 对比度调整 (params: factor=1.5)

```python
from tools.video_effects_advanced import apply_filter

# 黑白滤镜
apply_filter("input.mp4", "output_bw.mp4", "grayscale")

# 模糊效果
apply_filter("input.mp4", "output_blur.mp4", "blur", radius=10)

# 亮度调整
apply_filter("input.mp4", "output_bright.mp4", "brightness", factor=1.8)
```

## 2. 特效功能

### apply_effect(video_path, output_path, effect_type, **params)

支持的特效类型：
- `slow_motion` - 慢动作 (params: speed=0.5)
- `fast_forward` - 快进 (params: speed=2.0)
- `reverse` - 倒放
- `mirror` - 镜像翻转 (params: direction="horizontal"/"vertical")
- `crop` - 画面裁剪 (params: x1, y1, x2, y2)

```python
from tools.video_effects_advanced import apply_effect

# 慢动作
apply_effect("input.mp4", "output_slow.mp4", "slow_motion", speed=0.5)

# 镜像翻转
apply_effect("input.mp4", "output_mirror.mp4", "mirror", direction="horizontal")

# 裁剪
apply_effect("input.mp4", "output_crop.mp4", "crop", x1=100, y1=100, x2=500, y2=400)
```

## 3. 画中画功能 ✅

### add_picture_in_picture(main_video, pip_video, output_path, position, size, opacity)

**参数**：
- `main_video` - 主视频路径
- `pip_video` - 画中画视频路径
- `output_path` - 输出路径
- `position` - 位置: "top-left"/"top-right"/"bottom-left"/"bottom-right"/"center"
- `size` - 画中画尺寸 (width, height)，默认None保持原尺寸
- `opacity` - 透明度 0.0-1.0，默认1.0

```python
from tools.video_effects_advanced import add_picture_in_picture

# 右下角画中画
add_picture_in_picture(
    "main.mp4", 
    "pip.mp4", 
    "output.mp4",
    position="bottom-right"
)

# 自定义尺寸和透明度
add_picture_in_picture(
    "main.mp4", 
    "pip.mp4", 
    "output.mp4",
    position="top-left",
    size=(320, 240),
    opacity=0.8
)
```

## 验收状态

| 功能类别 | 状态 | 示例文件 | 备注 |
|---------|------|---------|------|
| 画中画 | ✅ 已验证 | demo_pip.mp4 | 右下角叠加，功能正常 |
| 滤镜 | ⚠️ 待调试 | - | API适配中 |
| 特效 | ⚠️ 待调试 | - | API适配中 |

## 使用场景

1. **画中画** - 视频教程、直播回放、多机位展示
2. **滤镜** - 艺术效果、风格统一、氛围营造
3. **特效** - 慢动作回放、快速浏览、创意剪辑

## 注意事项

1. moviepy 2.x API变化较大，部分功能需要进一步适配
2. 画中画功能已完全验证可用
3. 滤镜和特效功能框架已搭建，需要调整API调用方式
4. 建议优先使用画中画功能，其他功能待优化

## 便捷常量

```python
# 位置常量
TOP_LEFT = "top-left"
TOP_RIGHT = "top-right"
BOTTOM_LEFT = "bottom-left"
BOTTOM_RIGHT = "bottom-right"
CENTER = "center"

# 滤镜类型
GRAYSCALE = "grayscale"
SEPIA = "sepia"
BLUR = "blur"
SHARPEN = "sharpen"
BRIGHTNESS = "brightness"
CONTRAST = "contrast"

# 特效类型
SLOW_MOTION = "slow_motion"
FAST_FORWARD = "fast_forward"
REVERSE = "reverse"
MIRROR = "mirror"
CROP = "crop"
```

---
[skill_mapping]
category: media_processing
skill: video_effects
tools: video_effects_advanced.py
[/skill_mapping]

## [record_on_use]
执行完本SOP后，调用以下命令记录使用情况：
```python
import sys
sys.path.append("../memory")
from autonomous_operation_sop.helper import record_skill_usage
record_skill_usage("video_effects_advanced_sop.md")
```