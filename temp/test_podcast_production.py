"""
播客制作流程验证脚本
使用前请确保已安装: pip install pydub
"""
import sys
sys.path.append('./tools')
from pydub import AudioSegment
from pydub.generators import Sine
from audio_toolkit import merge_audios
from audio_enhance import enhance_voice, normalize_volume, mix_audio
import os

print("=== 生成测试音频素材 ===")
intro = Sine(440).to_audio_segment(duration=3000).apply_gain(-10)
intro.export("test_intro.mp3", format="mp3")
print("✓ 片头: test_intro.mp3 (3秒)")

content = Sine(523).to_audio_segment(duration=5000).apply_gain(-8)
content.export("test_content.mp3", format="mp3")
print("✓ 正文: test_content.mp3 (5秒)")

outro = Sine(349).to_audio_segment(duration=3000).apply_gain(-10)
outro.export("test_outro.mp3", format="mp3")
print("✓ 片尾: test_outro.mp3 (3秒)")

bgm = Sine(262).to_audio_segment(duration=10000).apply_gain(-15)
bgm.export("test_bgm.mp3", format="mp3")
print("✓ BGM: test_bgm.mp3 (10秒)")

print("\n=== 执行播客制作流程 ===")
normalize_volume("test_intro.mp3", "intro_norm.mp3", -20.0)
enhance_voice("test_content.mp3", "content_enh.mp3", -20.0)
normalize_volume("test_outro.mp3", "outro_norm.mp3", -20.0)
print("✓ 预处理完成")

mix_audio("content_enh.mp3", "test_bgm.mp3", "content_mixed.mp3", 0, -18)
print("✓ 混音完成")

merge_audios(["intro_norm.mp3", "content_mixed.mp3", "outro_norm.mp3"], "final_podcast.mp3")
print("✓ 拼接完成")

final = AudioSegment.from_file("final_podcast.mp3")
print(f"\n✓ 最终播客: final_podcast.mp3 ({len(final)/1000:.1f}秒)")
