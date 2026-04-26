"""
audio_enhance.py - Audio Enhancement with Real pydub Implementation
Features: Noise reduction, Volume normalization, Audio mixing
"""

from pydub import AudioSegment
from pydub.effects import normalize
import os


def reduce_noise(input_file, output_file, low_cutoff=80, high_cutoff=8000):
    """
    Reduce background noise using frequency filters
    
    Args:
        input_file: Input audio file
        output_file: Output audio file
        low_cutoff: High-pass filter cutoff (Hz), removes low frequency noise
        high_cutoff: Low-pass filter cutoff (Hz), removes high frequency noise
    
    Returns:
        Output file path
    """
    audio = AudioSegment.from_file(input_file)
    
    # Apply high-pass filter to remove low frequency noise
    filtered = audio.high_pass_filter(low_cutoff)
    
    # Apply low-pass filter to remove high frequency noise
    filtered = filtered.low_pass_filter(high_cutoff)
    
    # Export
    filtered.export(output_file, format=output_file.split(".")[-1])
    return output_file


def normalize_volume(input_file, output_file, target_dBFS=-20.0):
    """
    Normalize audio volume to target level
    
    Args:
        input_file: Input audio file
        output_file: Output audio file
        target_dBFS: Target volume level (-20 for podcast, -14 for music, -6 for broadcast)
    
    Returns:
        Output file path
    """
    audio = AudioSegment.from_file(input_file)
    
    # Calculate volume adjustment
    change_in_dBFS = target_dBFS - audio.dBFS
    
    # Apply volume adjustment
    normalized = audio.apply_gain(change_in_dBFS)
    
    # Export
    normalized.export(output_file, format=output_file.split(".")[-1])
    return output_file


def mix_audio(voice_file, bgm_file, output_file, voice_volume=0, bgm_volume=-15):
    """
    Mix voice with background music
    
    Args:
        voice_file: Voice audio file
        bgm_file: Background music file
        output_file: Output mixed audio file
        voice_volume: Voice volume adjustment in dB
        bgm_volume: BGM volume adjustment in dB (recommend -10 to -20)
    
    Returns:
        Output file path
    """
    voice = AudioSegment.from_file(voice_file)
    bgm = AudioSegment.from_file(bgm_file)
    
    # Adjust volumes
    voice = voice + voice_volume
    bgm = bgm + bgm_volume
    
    # Loop BGM if shorter than voice
    if len(bgm) < len(voice):
        loops_needed = (len(voice) // len(bgm)) + 1
        bgm = bgm * loops_needed
    
    # Trim BGM to match voice length
    bgm = bgm[:len(voice)]
    
    # Mix by overlaying
    mixed = voice.overlay(bgm)
    
    # Export
    mixed.export(output_file, format=output_file.split(".")[-1])
    return output_file


def enhance_voice(input_file, output_file, target_dBFS=-20.0):
    """
    One-click voice enhancement: noise reduction + volume normalization
    
    Args:
        input_file: Input audio file
        output_file: Output audio file
        target_dBFS: Target volume level
    
    Returns:
        Output file path
    """
    # Step 1: Noise reduction
    temp_file = output_file.replace(".", "_temp.")
    reduce_noise(input_file, temp_file)
    
    # Step 2: Volume normalization
    normalize_volume(temp_file, output_file, target_dBFS)
    
    # Clean up temp file
    if os.path.exists(temp_file):
        os.remove(temp_file)
    
    return output_file


if __name__ == "__main__":
    print("Audio Enhancement Toolkit")
    print("Functions: reduce_noise, normalize_volume, mix_audio, enhance_voice")