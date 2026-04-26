"""视频剪辑模板库与一键应用"""
import json
import os
from typing import Dict, List, Optional

class VideoTemplateManager:
    """视频模板管理器"""
    def __init__(self, template_dir: str = "./video_templates"):
        self.template_dir = template_dir
        os.makedirs(template_dir, exist_ok=True)
    
    def save_template(self, name: str, template: Dict) -> str:
        """保存模板"""
        path = os.path.join(self.template_dir, f"{name}.json")
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(template, f, indent=2, ensure_ascii=False)
        return path
    
    def load_template(self, name: str) -> Dict:
        """加载模板"""
        path = os.path.join(self.template_dir, f"{name}.json")
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def list_templates(self) -> List[str]:
        """列出所有模板"""
        files = os.listdir(self.template_dir)
        return [f.replace('.json', '') for f in files if f.endswith('.json')]
    
    def delete_template(self, name: str):
        """删除模板"""
        path = os.path.join(self.template_dir, f"{name}.json")
        if os.path.exists(path):
            os.remove(path)

class VideoTemplate:
    """视频模板应用器"""
    
    @staticmethod
    def opening_template(video_path: str, title: str, duration: float = 3.0):
        """开场模板：标题+淡入"""
        from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
        from moviepy.video.fx.all import fadein, fadeout
        
        video = VideoFileClip(video_path)
        txt = TextClip(title, fontsize=70, color='white', font='Arial-Bold')
        txt = txt.set_position('center').set_duration(duration)
        txt = txt.fx(fadein, 0.5).fx(fadeout, 0.5)
        result = CompositeVideoClip([video.subclip(0, duration), txt])
        return result
    
    @staticmethod
    def ending_template(video_path: str, text: str, duration: float = 3.0):
        """片尾模板：感谢文字+淡出"""
        from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
        from moviepy.video.fx.all import fadein, fadeout
        
        video = VideoFileClip(video_path)
        video_duration = video.duration
        txt = TextClip(text, fontsize=50, color='white', font='Arial')
        txt = txt.set_position('center').set_duration(duration)
        txt = txt.fx(fadein, 0.5).fx(fadeout, 0.5)
        end_part = video.subclip(max(0, video_duration - duration), video_duration)
        result = CompositeVideoClip([end_part, txt])
        return result
    
    @staticmethod
    def apply_template(video_path: str, output_path: str, template: Dict):
        """一键应用模板"""
        from moviepy.editor import VideoFileClip, concatenate_videoclips
        
        video = VideoFileClip(video_path)
        clips = []
        
        # 开场
        if template.get('opening'):
            opening = VideoTemplate.opening_template(
                video_path,
                template['opening'].get('title', 'Welcome'),
                template['opening'].get('duration', 3.0)
            )
            clips.append(opening)
        
        # 主体内容
        start = template.get('opening', {}).get('duration', 0)
        end = video.duration - template.get('ending', {}).get('duration', 0)
        if end > start:
            clips.append(video.subclip(start, end))
        
        # 片尾
        if template.get('ending'):
            ending = VideoTemplate.ending_template(
                video_path,
                template['ending'].get('text', 'Thank You'),
                template['ending'].get('duration', 3.0)
            )
            clips.append(ending)
        
        # 合并
        final = concatenate_videoclips(clips)
        final.write_videofile(output_path, codec='libx264', audio_codec='aac')
        
        # 清理
        video.close()
        final.close()
        for clip in clips:
            clip.close()

def create_standard_opening(title: str = "Welcome", duration: float = 3.0) -> Dict:
    """创建标准开场模板"""
    return {
        "type": "opening",
        "title": title,
        "duration": duration,
        "fade_in": 0.5,
        "fade_out": 0.5
    }

def create_standard_ending(text: str = "Thank You", duration: float = 3.0) -> Dict:
    """创建标准片尾模板"""
    return {
        "type": "ending",
        "text": text,
        "duration": duration,
        "fade_in": 0.5,
        "fade_out": 0.5
    }

def quick_apply_template(video_path: str, output_path: str, 
                         opening_title: Optional[str] = None,
                         ending_text: Optional[str] = None):
    """快速应用模板"""
    template = {}
    if opening_title:
        template['opening'] = create_standard_opening(opening_title)
    if ending_text:
        template['ending'] = create_standard_ending(ending_text)
    
    VideoTemplate.apply_template(video_path, output_path, template)

if __name__ == "__main__":
    print("视频模板工具")
    print("1. 模板管理: mgr = VideoTemplateManager()")
    print("2. 应用模板: VideoTemplate.apply_template()")
    print("3. 快速应用: quick_apply_template()")
