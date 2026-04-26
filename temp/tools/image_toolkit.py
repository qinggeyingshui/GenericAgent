#!/usr/bin/env python3
"""
image_toolkit.py - 图像处理工具链
5大核心功能: crop / resize / convert_format / ocr / compress_batch
依赖: Pillow, rapidocr_onnxruntime (pip install rapidocr_onnxruntime)
端到端: image_to_ppt_slide() 图片搜索→裁剪→嵌入PPT
"""
import os, sys
from pathlib import Path
from PIL import Image
from typing import Tuple, List, Optional


# ─── 1. 裁剪 ────────────────────────────────────────────────────────────────
def crop(src: str, box: Tuple[int,int,int,int], dst: str = None) -> str:
    """裁剪图片。box=(left, top, right, bottom)，dst为空则覆盖原文件。
    返回输出路径。
    """
    img = Image.open(src)
    cropped = img.crop(box)
    out = dst or src
    cropped.save(out)
    return out


# ─── 2. 缩放 ────────────────────────────────────────────────────────────────
def resize(src: str, width: int = None, height: int = None,
           dst: str = None, keep_ratio: bool = True) -> str:
    """缩放图片。可只指定width或height，keep_ratio=True自动补全另一边。
    返回输出路径。
    """
    img = Image.open(src)
    w0, h0 = img.size
    if keep_ratio:
        if width and not height:
            height = int(h0 * width / w0)
        elif height and not width:
            width = int(w0 * height / h0)
    width = width or w0
    height = height or h0
    resized = img.resize((width, height), Image.LANCZOS)
    out = dst or src
    resized.save(out)
    return out


# ─── 3. 格式转换 ─────────────────────────────────────────────────────────────
def convert_format(src: str, fmt: str, dst: str = None) -> str:
    """转换图片格式。fmt: PNG/JPEG/WEBP/BMP/GIF等（不区分大小写）。
    JPEG不支持透明通道，自动转RGB。返回输出路径。
    """
    img = Image.open(src)
    fmt = fmt.upper()
    if fmt == "JPG":
        fmt = "JPEG"
    if fmt == "JPEG" and img.mode in ("RGBA", "LA", "P"):
        img = img.convert("RGB")
    if dst is None:
        ext = "jpg" if fmt == "JPEG" else fmt.lower()
        dst = str(Path(src).with_suffix("." + ext))
    img.save(dst, format=fmt)
    return dst


# ─── 4. OCR文字识别 ──────────────────────────────────────────────────────────
_ocr_engine = None

def ocr(src: str, return_detail: bool = False):
    """OCR文字识别（基于RapidOCR，支持中英文）。
    return_detail=False: 返回识别文字字符串
    return_detail=True:  返回列表 [(text, confidence), ...]
    需要: pip install rapidocr_onnxruntime
    """
    global _ocr_engine
    try:
        from rapidocr_onnxruntime import RapidOCR
    except ImportError:
        print("[OCR] 请先安装: pip install rapidocr_onnxruntime")
        return "" if not return_detail else []
    if _ocr_engine is None:
        _ocr_engine = RapidOCR()
    result, _ = _ocr_engine(src)
    if not result:
        return "" if not return_detail else []
    if return_detail:
        return [(item[1], round(float(item[2]), 4)) for item in result]
    return "\n".join(item[1] for item in result)


# ─── 5. 批量压缩 ─────────────────────────────────────────────────────────────
def compress_batch(src_dir: str, dst_dir: str = None, quality: int = 75,
                   max_width: int = 1920,
                   exts: tuple = (".jpg", ".jpeg", ".png", ".webp")) -> dict:
    """批量压缩目录下的图片，统一转JPEG。
    quality: JPEG质量(1-95)，max_width: 超出则等比缩放。
    返回: {"processed": N, "saved_bytes": M, "files": [...]}
    """
    src_path = Path(src_dir)
    dst_path = Path(dst_dir) if dst_dir else src_path / "compressed"
    dst_path.mkdir(parents=True, exist_ok=True)
    results = {"processed": 0, "saved_bytes": 0, "files": []}
    for img_file in src_path.iterdir():
        if img_file.suffix.lower() not in exts:
            continue
        orig_size = img_file.stat().st_size
        img = Image.open(img_file)
        if img.width > max_width:
            new_h = int(img.height * max_width / img.width)
            img = img.resize((max_width, new_h), Image.LANCZOS)
        if img.mode in ("RGBA", "LA", "P"):
            img = img.convert("RGB")
        out_path = dst_path / (img_file.stem + ".jpg")
        img.save(out_path, format="JPEG", quality=quality, optimize=True)
        new_size = out_path.stat().st_size
        saved = orig_size - new_size
        results["processed"] += 1
        results["saved_bytes"] += saved
        results["files"].append({
            "src": str(img_file), "dst": str(out_path),
            "orig_kb": round(orig_size / 1024, 1),
            "new_kb": round(new_size / 1024, 1),
            "saved_kb": round(saved / 1024, 1),
        })
    return results


# ─── 端到端：图片搜索 → 裁剪 → 嵌入PPT ─────────────────────────────────────
def image_to_ppt_slide(keyword: str, ppt_path: str, slide_idx: int = 0,
                       width_px: int = 800, crop_box: Tuple = None) -> str:
    """端到端流程：搜索关键词图片 → (可选裁剪) → 嵌入PPT指定幻灯片。
    返回下载的图片路径。
    """
    root = Path(__file__).parent
    sys.path.insert(0, str(root / "local_skills"))
    from image_search import search
    paths = search(keyword, w=width_px, h=int(width_px * 0.6), count=1)
    if not paths:
        raise FileNotFoundError(f"未找到关键词 {keyword!r} 的图片")
    img_path = paths[0]
    if crop_box:
        cropped_path = str(Path(img_path).with_stem(Path(img_path).stem + "_cropped"))
        img_path = crop(img_path, crop_box, dst=cropped_path)
    sys.path.insert(0, str(root))
    from ppt_com_toolkit import add_image_to_slide
    add_image_to_slide(ppt_path, slide_idx, img_path)
    return img_path


# ─── CLI ─────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import argparse, json
    parser = argparse.ArgumentParser(description="图像处理工具链 image_toolkit.py")
    sub = parser.add_subparsers(dest="cmd")

    p = sub.add_parser("crop");  p.add_argument("src")
    p.add_argument("box", help="left,top,right,bottom"); p.add_argument("--dst")

    p = sub.add_parser("resize"); p.add_argument("src")
    p.add_argument("--width", type=int); p.add_argument("--height", type=int)
    p.add_argument("--dst")

    p = sub.add_parser("convert"); p.add_argument("src")
    p.add_argument("fmt"); p.add_argument("--dst")

    p = sub.add_parser("ocr"); p.add_argument("src")
    p.add_argument("--detail", action="store_true")

    p = sub.add_parser("compress"); p.add_argument("src_dir")
    p.add_argument("--dst_dir"); p.add_argument("--quality", type=int, default=75)
    p.add_argument("--max_width", type=int, default=1920)

    args = parser.parse_args()
    if args.cmd == "crop":
        box = tuple(int(x) for x in args.box.split(","))
        print(crop(args.src, box, args.dst))
    elif args.cmd == "resize":
        print(resize(args.src, args.width, args.height, args.dst))
    elif args.cmd == "convert":
        print(convert_format(args.src, args.fmt, args.dst))
    elif args.cmd == "ocr":
        print(ocr(args.src, return_detail=args.detail))
    elif args.cmd == "compress":
        r = compress_batch(args.src_dir, args.dst_dir, args.quality, args.max_width)
        print(json.dumps(r, ensure_ascii=False, indent=2))
    else:
        parser.print_help()

# ============ R213新增: 封面/缩略图/水印 ============

def create_cover(
    background: str,
    title: str,
    output_path: str,
    subtitle: str = "",
    size: tuple = (1280, 720),
    title_color: tuple = (255, 255, 255),
    bg_color: tuple = (30, 60, 114),
    font_size: int = 72,
    subtitle_size: int = 36
) -> str:
    """
    生成封面图片（用于视频/文章封面）
    
    Args:
        background: 背景图片路径，若为空则使用纯色背景
        title: 主标题
        output_path: 输出路径
        subtitle: 副标题
        size: 输出尺寸 (宽, 高)
        title_color: 标题颜色RGB
        bg_color: 背景色RGB（无背景图时使用）
        font_size: 标题字号
        subtitle_size: 副标题字号
    
    Returns:
        输出文件路径
    """
    from PIL import Image, ImageDraw, ImageFont
    import os
    
    # 创建或加载背景
    if background and os.path.exists(background):
        img = Image.open(background).convert('RGBA')
        img = img.resize(size, Image.Resampling.LANCZOS)
        # 添加半透明遮罩增强文字可读性
        overlay = Image.new('RGBA', size, (0, 0, 0, 100))
        img = Image.alpha_composite(img, overlay)
    else:
        # 渐变背景
        img = Image.new('RGB', size, bg_color)
    
    draw = ImageDraw.Draw(img)
    
    # 尝试加载字体
    try:
        title_font = ImageFont.truetype("msyh.ttc", font_size)
        sub_font = ImageFont.truetype("msyh.ttc", subtitle_size)
    except:
        title_font = ImageFont.load_default()
        sub_font = ImageFont.load_default()
    
    # 绘制标题（居中）
    bbox = draw.textbbox((0, 0), title, font=title_font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    tx = (size[0] - tw) // 2
    ty = (size[1] - th) // 2 - 30
    draw.text((tx, ty), title, fill=title_color, font=title_font)
    
    # 绘制副标题
    if subtitle:
        bbox = draw.textbbox((0, 0), subtitle, font=sub_font)
        sw = bbox[2] - bbox[0]
        sx = (size[0] - sw) // 2
        sy = ty + th + 20
        draw.text((sx, sy), subtitle, fill=(*title_color[:3], 200), font=sub_font)
    
    # 保存
    if img.mode == 'RGBA':
        img = img.convert('RGB')
    img.save(output_path, quality=95)
    return output_path


def create_thumbnail(
    image_path: str,
    output_path: str,
    size: tuple = (320, 180),
    maintain_aspect: bool = True
) -> str:
    """
    生成缩略图
    
    Args:
        image_path: 原图路径
        output_path: 输出路径
        size: 缩略图尺寸
        maintain_aspect: 是否保持宽高比
    
    Returns:
        输出文件路径
    """
    from PIL import Image
    
    img = Image.open(image_path)
    
    if maintain_aspect:
        img.thumbnail(size, Image.Resampling.LANCZOS)
    else:
        img = img.resize(size, Image.Resampling.LANCZOS)
    
    img.save(output_path, quality=85)
    return output_path


def add_watermark(
    image_path: str,
    output_path: str,
    watermark_text: str = None,
    watermark_image: str = None,
    position: str = "bottom_right",
    opacity: int = 128,
    font_size: int = 24,
    color: tuple = (255, 255, 255)
) -> str:
    """
    添加水印（文字或图片）
    
    Args:
        image_path: 原图路径
        output_path: 输出路径
        watermark_text: 文字水印内容
        watermark_image: 图片水印路径
        position: 位置 (top_left/top_right/bottom_left/bottom_right/center)
        opacity: 透明度 (0-255)
        font_size: 文字水印字号
        color: 文字颜色RGB
    
    Returns:
        输出文件路径
    """
    from PIL import Image, ImageDraw, ImageFont
    
    img = Image.open(image_path).convert('RGBA')
    
    if watermark_image:
        # 图片水印
        wm = Image.open(watermark_image).convert('RGBA')
        # 调整透明度
        wm_data = wm.getdata()
        new_data = [(r, g, b, min(a, opacity)) for r, g, b, a in wm_data]
        wm.putdata(new_data)
    elif watermark_text:
        # 文字水印
        try:
            font = ImageFont.truetype("msyh.ttc", font_size)
        except:
            font = ImageFont.load_default()
        
        # 创建文字水印图层
        bbox = ImageDraw.Draw(img).textbbox((0, 0), watermark_text, font=font)
        wm_size = (bbox[2] - bbox[0] + 20, bbox[3] - bbox[1] + 10)
        wm = Image.new('RGBA', wm_size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(wm)
        draw.text((10, 5), watermark_text, fill=(*color, opacity), font=font)
    else:
        raise ValueError("需要提供watermark_text或watermark_image")
    
    # 计算位置
    positions = {
        "top_left": (10, 10),
        "top_right": (img.width - wm.width - 10, 10),
        "bottom_left": (10, img.height - wm.height - 10),
        "bottom_right": (img.width - wm.width - 10, img.height - wm.height - 10),
        "center": ((img.width - wm.width) // 2, (img.height - wm.height) // 2)
    }
    pos = positions.get(position, positions["bottom_right"])
    
    # 合成
    img.paste(wm, pos, wm)
    
    # 保存
    if output_path.lower().endswith('.jpg') or output_path.lower().endswith('.jpeg'):
        img = img.convert('RGB')
    img.save(output_path, quality=95)
    return output_path


def demo_image_toolkit():
    """演示新增的3个函数"""
    import os
    
    demo_dir = './image_demo'
    os.makedirs(demo_dir, exist_ok=True)
    
    # 1. 封面生成
    cover_path = create_cover(
        background="",
        title="自媒体运营指南",
        subtitle="从0到1打造个人品牌",
        output_path=f"{demo_dir}/cover.jpg"
    )
    print(f"✓ 封面生成: {cover_path}")
    
    # 2. 缩略图
    thumb_path = create_thumbnail(
        cover_path,
        f"{demo_dir}/thumbnail.jpg",
        size=(320, 180)
    )
    print(f"✓ 缩略图: {thumb_path}")
    
    # 3. 水印
    wm_path = add_watermark(
        cover_path,
        f"{demo_dir}/watermarked.jpg",
        watermark_text="@我的账号",
        position="bottom_right",
        opacity=180
    )
    print(f"✓ 水印添加: {wm_path}")
    
    return True
