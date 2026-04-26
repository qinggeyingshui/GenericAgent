"""PPT演讲稿生成与排练助手"""
import time
import re
from typing import List, Dict, Tuple

class SpeechGenerator:
    """演讲稿生成器"""
    def __init__(self):
        self.transitions = ["接下来", "现在", "让我们看看", "另一个重要方面是"]
    
    def extract_content_from_ppt(self, ppt_path: str) -> List[Dict]:
        """从PPT提取内容"""
        import sys
        sys.path.append(".")
        import ppt_com_toolkit as ppt
        
        app = ppt.open_ppt()
        prs = ppt.open_file(app, ppt_path)
        
        slides_content = []
        for i in range(1, prs.Slides.Count + 1):
            slide = prs.Slides(i)
            content = {"slide_num": i, "title": "", "bullets": [], "notes": ""}
            
            for shape in slide.Shapes:
                if shape.HasTextFrame:
                    text = shape.TextFrame.TextRange.Text.strip()
                    if shape.Type == 14:
                        content["title"] = text
                    elif text:
                        content["bullets"].append(text)
            
            if slide.HasNotesPage:
                notes_text = slide.NotesPage.Shapes(2).TextFrame.TextRange.Text
                content["notes"] = notes_text.strip()
            
            slides_content.append(content)
        
        ppt.quit_app(app)
        return slides_content
    
    def generate_speech(self, slides_content: List[Dict]) -> str:
        """生成演讲稿"""
        parts = []
        
        if slides_content:
            title = slides_content[0].get("title", "今天的主题")
            parts.append(f"各位好，今天我要分享的主题是：{title}。")
        
        for idx, slide in enumerate(slides_content):
            if idx > 0:
                trans = self.transitions[idx % len(self.transitions)]
                parts.append(f"\n{trans}：{slide.get('title', '下一部分')}。")
                
                if slide.get("notes"):
                    parts.append(slide["notes"])
                else:
                    for bullet in slide.get("bullets", []):
                        parts.append(f"{bullet}是一个重要方面。")
        
        parts.append("\n以上就是我的分享，感谢大家。")
        return "\n".join(parts)
    
    def optimize_speech(self, speech: str) -> Dict:
        """优化建议"""
        words = len(speech)
        sentences = len(re.findall(r"[。！？]", speech))
        avg_len = words / sentences if sentences > 0 else 0
        
        suggestions = []
        if avg_len > 30:
            suggestions.append("句子偏长，建议拆分")
        if words < 500:
            suggestions.append("内容较少，建议增加细节")
        if words > 3000:
            suggestions.append("内容较多，建议精简")
        
        return {
            "word_count": words,
            "sentence_count": sentences,
            "avg_sentence_length": round(avg_len, 1),
            "estimated_time": f"{words // 150}-{words // 120}分钟",
            "suggestions": suggestions
        }

class RehearsalTimer:
    """排练计时器"""
    def __init__(self, target_minutes: int = 10):
        self.target_time = target_minutes * 60
        self.start_time = None
        self.pause_time = None
        self.paused_duration = 0
    
    def start(self):
        """开始计时"""
        self.start_time = time.time()
        self.pause_time = None
        print(f"计时开始，目标：{self.target_time // 60}分钟")
    
    def pause(self):
        """暂停"""
        if self.start_time and not self.pause_time:
            self.pause_time = time.time()
            print("已暂停")
    
    def resume(self):
        """继续"""
        if self.pause_time:
            self.paused_duration += time.time() - self.pause_time
            self.pause_time = None
            print("继续计时")
    
    def get_elapsed(self) -> Tuple[int, int]:
        """获取已用时间（分钟，秒）"""
        if not self.start_time:
            return (0, 0)
        
        if self.pause_time:
            elapsed = self.pause_time - self.start_time - self.paused_duration
        else:
            elapsed = time.time() - self.start_time - self.paused_duration
        
        minutes = int(elapsed // 60)
        seconds = int(elapsed % 60)
        return (minutes, seconds)
    
    def get_status(self) -> str:
        """获取状态"""
        minutes, seconds = self.get_elapsed()
        elapsed_total = minutes * 60 + seconds
        
        if elapsed_total > self.target_time:
            over = elapsed_total - self.target_time
            return f"已用时：{minutes}分{seconds}秒 [超时{over}秒]"
        else:
            remaining = self.target_time - elapsed_total
            return f"已用时：{minutes}分{seconds}秒 [剩余{remaining}秒]"

class KeyPointHelper:
    """关键点提示"""
    def extract_key_points(self, slides_content: List[Dict]) -> List[Dict]:
        """提取关键点"""
        key_points = []
        
        for slide in slides_content:
            point = {
                "slide_num": slide["slide_num"],
                "title": slide.get("title", ""),
                "key_bullets": slide.get("bullets", [])[:3],
                "notes": slide.get("notes", "")[:100]
            }
            key_points.append(point)
        
        return key_points
    
    def format_prompts(self, key_points: List[Dict]) -> str:
        """格式化提示卡"""
        lines = ["=== 演讲提示卡 ===\n"]
        
        for point in key_points:
            lines.append(f"第{point['slide_num']}页：{point['title']}")
            for bullet in point["key_bullets"]:
                lines.append(f"  • {bullet}")
            if point["notes"]:
                lines.append(f"  备注：{point['notes']}")
            lines.append("")
        
        return "\n".join(lines)
    
    def save_prompts(self, key_points: List[Dict], output_path: str):
        """保存提示卡"""
        content = self.format_prompts(key_points)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(content)
        return output_path

def quick_generate_speech(ppt_path: str, output_path: str = None) -> str:
    """快速生成演讲稿"""
    gen = SpeechGenerator()
    slides = gen.extract_content_from_ppt(ppt_path)
    speech = gen.generate_speech(slides)
    
    if output_path:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(speech)
    
    return speech

def quick_rehearsal(target_minutes: int = 10):
    """快速开始排练"""
    timer = RehearsalTimer(target_minutes)
    timer.start()
    return timer

if __name__ == "__main__":
    print("演讲助手工具")
    print("1. 生成演讲稿: gen = SpeechGenerator()")
    print("2. 排练计时: timer = RehearsalTimer(10)")
    print("3. 关键点提示: helper = KeyPointHelper()")
