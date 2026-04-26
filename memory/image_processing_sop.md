# 图片处理SOP (L3)
工具: temp/tools/image_toolkit.py (Pillow)

## 基础功能
```python
from image_toolkit import crop, resize, convert_format, compress_batch
crop(img, x, y, w, h, out)      # 裁剪
resize(img, w, h, out)          # 缩放
convert_format(img, "png", out) # 格式转换
compress_batch(dir, quality=80) # 批量压缩
```

## R213新增: 封面/缩略图/水印
```python
from image_toolkit import create_cover, create_thumbnail, add_watermark

# 封面生成 (视频/文章封面)
create_cover(
    background="bg.jpg",  # 可选，空则纯色
    title="主标题",
    subtitle="副标题",
    output_path="cover.jpg",
    size=(1280, 720),
    bg_color=(30, 60, 114)
)

# 缩略图
create_thumbnail("img.jpg", "thumb.jpg", size=(320, 180))

# 水印 (文字或图片)
add_watermark("img.jpg", "out.jpg", watermark_text="@账号", position="bottom_right", opacity=180)
add_watermark("img.jpg", "out.jpg", watermark_image="logo.png", position="bottom_right")
```
position: top_left/top_right/bottom_left/bottom_right/center

[skill_mapping]
category: media_processing
skill: image_processing_sop
tools: image_toolkit.py
[/skill_mapping]
