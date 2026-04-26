"""音频转文字工具"""
import os
import json
from typing import List, Dict, Optional
from datetime import timedelta

class AudioTranscriber:
    """音频转文字核心类"""
    def __init__(self, language="zh-CN"):
        self.language = language
    
    def transcribe(self, audio_path: str, engine="google") -> Dict:
        """转录音频文件"""
        try:
            import speech_recognition as sr
        except ImportError:
            return {"error": "需要安装speech_recognition: pip install SpeechRecognition"}
        
        if not os.path.exists(audio_path):
            return {"error": f"文件不存在: {audio_path}"}
        
        # 转换音频格式
        wav_path = self._convert_to_wav(audio_path)
        if not wav_path:
            return {"error": "音频格式转换失败"}
        
        recognizer = sr.Recognizer()
        try:
            with sr.AudioFile(wav_path) as source:
                audio = recognizer.record(source)
            
            # 使用指定引擎识别
            if engine == "google":
                text = recognizer.recognize_google(audio, language=self.language)
            else:
                text = recognizer.recognize_sphinx(audio)
            
            return {
                "success": True,
                "text": text,
                "language": self.language,
                "engine": engine
            }
        except Exception as e:
            return {"error": str(e)}
        finally:
            if wav_path != audio_path and os.path.exists(wav_path):
                os.remove(wav_path)
    
    def _convert_to_wav(self, audio_path: str) -> Optional[str]:
        """转换音频为WAV格式"""
        ext = os.path.splitext(audio_path)[1].lower()
        if ext == ".wav":
            return audio_path
        
        try:
            from pydub import AudioSegment
        except ImportError:
            return None
        
        try:
            audio = AudioSegment.from_file(audio_path)
            wav_path = audio_path.rsplit(".", 1)[0] + "_temp.wav"
            audio.export(wav_path, format="wav")
            return wav_path
        except:
            return None
    
    def transcribe_long_audio(self, audio_path: str, chunk_length_ms=30000) -> List[Dict]:
        """转录长音频（分段处理）"""
        try:
            from pydub import AudioSegment
            import speech_recognition as sr
        except ImportError:
            return [{"error": "需要安装依赖"}]
        
        audio = AudioSegment.from_file(audio_path)
        chunks = [audio[i:i+chunk_length_ms] for i in range(0, len(audio), chunk_length_ms)]
        
        results = []
        for idx, chunk in enumerate(chunks):
            chunk_path = f"temp_chunk_{idx}.wav"
            chunk.export(chunk_path, format="wav")
            
            result = self.transcribe(chunk_path)
            if result.get("success"):
                results.append({
                    "index": idx,
                    "start_time": idx * chunk_length_ms / 1000,
                    "text": result["text"]
                })
            
            os.remove(chunk_path)
        
        return results
    
    def export_txt(self, results: List[Dict], output_path: str):
        """导出为TXT格式"""
        with open(output_path, "w", encoding="utf-8") as f:
            if isinstance(results, dict):
                f.write(results.get("text", ""))
            else:
                for r in results:
                    f.write(r.get("text", "") + "\n")
    
    def export_srt(self, results: List[Dict], output_path: str):
        """导出为SRT字幕格式"""
        with open(output_path, "w", encoding="utf-8") as f:
            for idx, r in enumerate(results, 1):
                start = timedelta(seconds=r.get('start_time', 0))
                end = timedelta(seconds=r.get('start_time', 0) + 30)
                f.write(f"{idx}\n")
                f.write(f"{self._format_time(start)} --> {self._format_time(end)}\n")
                text = r.get("text", "")
                f.write(f"{text}\n\n")
    
    def export_json(self, results, output_path: str):
        """导出为JSON格式"""
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
    
    def _format_time(self, td: timedelta) -> str:
        """格式化时间为SRT格式"""
        total_seconds = int(td.total_seconds())
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        milliseconds = td.microseconds // 1000
        return f"{hours:02d}:{minutes:02d}:{seconds:02d},{milliseconds:03d}"

def quick_transcribe(audio_path: str, output_format="txt", output_path=None) -> str:
    """快速转录音频"""
    transcriber = AudioTranscriber()
    result = transcriber.transcribe(audio_path)
    
    if not result.get("success"):
        return result.get("error", "转录失败")
    
    if output_path is None:
        output_path = audio_path.rsplit(".", 1)[0] + f".{output_format}"
    
    if output_format == "txt":
        transcriber.export_txt(result, output_path)
    elif output_format == "json":
        transcriber.export_json(result, output_path)
    
    return output_path

if __name__ == "__main__":
    print("音频转文字工具")
    print("1. AudioTranscriber: 音频转文字核心类")
    print("2. quick_transcribe: 快速转录函数")
    print("支持格式: mp3/wav/m4a/flac")
    print("导出格式: TXT/SRT/JSON")