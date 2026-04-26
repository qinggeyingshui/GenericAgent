"""
subtitle_proofreader.py - Video Subtitle Proofreading Tool (R163, 2026-04-20)

Features:
1. Support SRT/VTT format
2. Detect punctuation/timeline/length issues
3. Generate proofreading report
"""

import re
from datetime import datetime

PUNCTUATION_RULES = {
    "no_space_before": [",", ".", "!", "?", ";", ":"],
    "paired": {"(": ")", "[": "]", "{": "}", "<": ">"}
}


def parse_srt(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    subtitles = []
    blocks = content.strip().split("\n\n")
    
    for block in blocks:
        lines = block.strip().split("\n")
        if len(lines) < 3:
            continue
        
        try:
            index = int(lines[0])
            time_line = lines[1]
            text = "\n".join(lines[2:])
            
            time_match = re.match(r"(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})", time_line)
            if time_match:
                subtitles.append({
                    "index": index,
                    "start": time_match.group(1),
                    "end": time_match.group(2),
                    "text": text
                })
        except:
            continue
    
    return subtitles


def parse_vtt(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    content = re.sub(r"^WEBVTT.*?\n\n", "", content, flags=re.DOTALL)
    subtitles = []
    blocks = content.strip().split("\n\n")
    index = 1
    
    for block in blocks:
        lines = block.strip().split("\n")
        if len(lines) < 2:
            continue
        
        time_line = lines[0]
        text = "\n".join(lines[1:])
        time_match = re.match(r"(\d{2}:\d{2}:\d{2}\.\d{3}) --> (\d{2}:\d{2}:\d{2}\.\d{3})", time_line)
        
        if time_match:
            subtitles.append({
                "index": index,
                "start": time_match.group(1),
                "end": time_match.group(2),
                "text": text
            })
            index += 1
    
    return subtitles


def check_punctuation(text):
    issues = []
    
    for punct in PUNCTUATION_RULES["no_space_before"]:
        if f" {punct}" in text:
            issues.append(f"Punctuation space before: {punct}")
    
    for open_p, close_p in PUNCTUATION_RULES["paired"].items():
        if text.count(open_p) != text.count(close_p):
            issues.append(f"Paired punctuation mismatch: {open_p}{close_p}")
    
    return issues


def check_timeline(subtitles):
    issues = []
    
    for i in range(len(subtitles)):
        sub = subtitles[i]
        start = sub["start"].replace(",", ".")
        end = sub["end"].replace(",", ".")
        
        if start >= end:
            issues.append({
                "index": sub["index"],
                "type": "Timeline error",
                "detail": f"Start >= End: {start} >= {end}"
            })
        
        if i < len(subtitles) - 1:
            next_sub = subtitles[i + 1]
            next_start = next_sub["start"].replace(",", ".")
            if end > next_start:
                issues.append({
                    "index": sub["index"],
                    "type": "Timeline overlap",
                    "detail": f"Overlap with subtitle {next_sub['index']}"
                })
    
    return issues


def check_text_length(subtitles, max_chars=40):
    issues = []
    
    for sub in subtitles:
        text_len = len(sub["text"].replace("\n", ""))
        if text_len > max_chars:
            issues.append({
                "index": sub["index"],
                "type": "Text too long",
                "detail": f"Length {text_len} > {max_chars}"
            })
    
    return issues


def proofread_subtitle(file_path, output_path=None):
    if file_path.endswith(".srt"):
        subtitles = parse_srt(file_path)
    elif file_path.endswith(".vtt"):
        subtitles = parse_vtt(file_path)
    else:
        raise ValueError("Unsupported format, only .srt and .vtt")
    
    punctuation_issues = []
    for sub in subtitles:
        issues = check_punctuation(sub["text"])
        if issues:
            punctuation_issues.append({"index": sub["index"], "issues": issues})
    
    timeline_issues = check_timeline(subtitles)
    length_issues = check_text_length(subtitles)
    
    if not output_path:
        output_path = file_path.rsplit(".", 1)[0] + "_proofread.txt"
    
    report_lines = []
    report_lines.append("# Subtitle Proofreading Report\n\n")
    report_lines.append(f"File: {file_path}\n")
    report_lines.append(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
    report_lines.append(f"Total subtitles: {len(subtitles)}\n\n")
    
    report_lines.append(f"## Punctuation Issues ({len(punctuation_issues)})\n\n")
    if punctuation_issues:
        for item in punctuation_issues:
            issues_str = ", ".join(item['issues'])
            issues_str = ", ".join(item['issues'])
            issues_str = ", ".join(item['issues'])
            issues_str = ", ".join(item['issues'])
            issues_str = ", ".join(item['issues'])
            report_lines.append(f"- #{item['index']}: {issues_str}\n")
    else:
        report_lines.append("No issues\n")
    report_lines.append("\n")
    
    report_lines.append(f"## Timeline Issues ({len(timeline_issues)})\n\n")
    if timeline_issues:
        for item in timeline_issues:
            report_lines.append(f"- #{item['index']}: {item['type']} - {item['detail']}\n")
    else:
        report_lines.append("No issues\n")
    report_lines.append("\n")
    
    report_lines.append(f"## Length Issues ({len(length_issues)})\n\n")
    if length_issues:
        for item in length_issues:
            report_lines.append(f"- #{item['index']}: {item['detail']}\n")
    else:
        report_lines.append("No issues\n")
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.writelines(report_lines)
    
    return {
        "total_subtitles": len(subtitles),
        "issues": {
            "punctuation": punctuation_issues,
            "timeline": timeline_issues,
            "length": length_issues
        },
        "report": output_path
    }


# ========== R202 增强功能 (2026-04-21) ==========

EMOTION_KEYWORDS = {
    "happy": ["哈哈", "开心", "高兴", "快乐", "笑", "happy", "joy", "laugh"],
    "sad": ["难过", "伤心", "哭", "悲伤", "sad", "cry", "tears"],
    "angry": ["生气", "愤怒", "气", "angry", "mad", "furious"],
    "surprised": ["惊讶", "吃惊", "哇", "surprised", "wow", "amazing"]
}

LANGUAGE_PATTERNS = {
    "zh": r'[\u4e00-\u9fff]',
    "en": r'[a-zA-Z]',
    "ja": r'[\u3040-\u309f\u30a0-\u30ff]'
}

def detect_language(text):
    """检测文本语言"""
    scores = {}
    for lang, pattern in LANGUAGE_PATTERNS.items():
        matches = len(re.findall(pattern, text))
        scores[lang] = matches
    return max(scores, key=scores.get) if max(scores.values()) > 0 else "unknown"

def add_emotion_tags(subtitles):
    """添加情感标签"""
    for sub in subtitles:
        text = sub.get("text", "").lower()
        emotions = []
        for emotion, keywords in EMOTION_KEYWORDS.items():
            if any(kw in text for kw in keywords):
                emotions.append(emotion)
        sub["emotions"] = emotions if emotions else ["neutral"]
    return subtitles

def polish_subtitle(text, language="zh"):
    """AI润色字幕文本"""
    text = text.strip()
    if language == "zh":
        text = re.sub(r'\s+', '', text)  # 移除多余空格
        text = re.sub(r'([，。！？])([^，。！？])', r'\1 \2', text)  # 标点后加空格
    elif language == "en":
        text = re.sub(r'\s+', ' ', text)  # 规范化空格
        text = text.capitalize()  # 首字母大写
    return text

def optimize_timeline(subtitles, min_duration=1.0, max_duration=7.0):
    """优化时间轴"""
    optimized = []
    for sub in subtitles:
        duration = sub["end"] - sub["start"]
        if duration < min_duration:
            sub["end"] = sub["start"] + min_duration
        elif duration > max_duration:
            sub["end"] = sub["start"] + max_duration
        optimized.append(sub)
    return optimized

def enhance_subtitles(file_path, output_path=None, enable_polish=True, enable_emotion=True, enable_optimize=True):
    """增强字幕（润色+情感+优化）"""
    if file_path.endswith('.srt'):
        subtitles = parse_srt(file_path)
    else:
        subtitles = parse_vtt(file_path)
    
    # 检测语言
    all_text = " ".join([s.get("text", "") for s in subtitles])
    language = detect_language(all_text)
    
    # 润色
    if enable_polish:
        for sub in subtitles:
            sub["text"] = polish_subtitle(sub["text"], language)
    
    # 情感标签
    if enable_emotion:
        subtitles = add_emotion_tags(subtitles)
    
    # 时间轴优化
    if enable_optimize:
        subtitles = optimize_timeline(subtitles)
    
    # 保存
    if output_path:
        with open(output_path, 'w', encoding='utf-8') as f:
            for i, sub in enumerate(subtitles, 1):
                f.write(f"{i}\n")
                f.write(f"{format_time(sub['start'])} --> {format_time(sub['end'])}\n")
                f.write(f"{sub['text']}\n\n")
    
    return {
        "language": language,
        "total": len(subtitles),
        "enhanced": True,
        "output": output_path
    }

def format_time(seconds):
    """格式化时间"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds % 1) * 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"
