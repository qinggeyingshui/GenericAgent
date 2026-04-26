"""PPT导出工具 - 支持PDF/图片/视频导出"""
import os
import win32com.client as win32

def export_to_pdf(pptx_path, pdf_path=None):
    """导出PPT为PDF"""
    if pdf_path is None:
        pdf_path = pptx_path.rsplit(".", 1)[0] + ".pdf"
    
    app = win32.Dispatch("PowerPoint.Application")
    prs = app.Presentations.Open(os.path.abspath(pptx_path), WithWindow=False)
    prs.ExportAsFixedFormat(os.path.abspath(pdf_path), 2)  # 2=ppFixedFormatTypePDF
    prs.Close()
    app.Quit()
    return pdf_path

def export_to_images(pptx_path, output_dir=None, format="PNG"):
    """导出PPT每页为图片"""
    if output_dir is None:
        output_dir = pptx_path.rsplit(".", 1)[0] + "_images"
    os.makedirs(output_dir, exist_ok=True)
    
    app = win32.Dispatch("PowerPoint.Application")
    prs = app.Presentations.Open(os.path.abspath(pptx_path), WithWindow=False)
    
    for i, slide in enumerate(prs.Slides, 1):
        img_path = os.path.join(output_dir, f"slide_{i:03d}.{format.lower()}")
        slide.Export(os.path.abspath(img_path), format)
    
    prs.Close()
    app.Quit()
    return output_dir

def export_to_video(pptx_path, video_path=None, fps=1, duration_per_slide=3):
    """导出PPT为视频（先转图片再合成）"""
    try:
        from moviepy.editor import ImageSequenceClip
    except ImportError:
        raise ImportError("需要安装moviepy: pip install moviepy")
    
    if video_path is None:
        video_path = pptx_path.rsplit(".", 1)[0] + ".mp4"
    
    # 导出为图片
    img_dir = export_to_images(pptx_path)
    imgs = sorted([os.path.join(img_dir, f) for f in os.listdir(img_dir) if f.endswith(".png")])
    
    # 生成视频
    clip = ImageSequenceClip(imgs, fps=1/duration_per_slide)
    clip.write_videofile(video_path, fps=fps)
    return video_path

def export_to_html(pptx_path, html_path=None):
    """导出PPT为HTML（含图片的网页版）"""
    if html_path is None:
        html_path = pptx_path.rsplit(".", 1)[0] + ".html"
    
    # 先导出图片
    img_dir = export_to_images(pptx_path)
    imgs = sorted([f for f in os.listdir(img_dir) if f.endswith(".png")])
    
    # 生成HTML
    html_content = '''<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>PPT Export</title>
<style>
body{font-family:Arial;background:#333;margin:0;padding:20px;text-align:center}
.slide{max-width:960px;margin:20px auto;box-shadow:0 4px 20px rgba(0,0,0,0.5)}
.slide img{width:100%;display:block}
.nav{position:fixed;bottom:20px;left:50%;transform:translateX(-50%);background:rgba(0,0,0,0.7);padding:10px 20px;border-radius:20px}
.nav a{color:#fff;margin:0 10px;text-decoration:none}
</style></head><body>
'''
    for i, img in enumerate(imgs, 1):
        html_content += f'<div class="slide" id="s{i}"><img src="{os.path.basename(img_dir)}/{img}"></div>\n'
    
    html_content += '<div class="nav">'
    for i in range(1, len(imgs)+1):
        html_content += f'<a href="#s{i}">{i}</a>'
    html_content += '</div></body></html>'
    
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    return html_path

if __name__ == "__main__":
    print("PPT导出工具已加载")
    print("函数: export_to_pdf, export_to_images, export_to_video, export_to_html")