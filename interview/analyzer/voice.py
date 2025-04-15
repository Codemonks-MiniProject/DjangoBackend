import numpy as np
import librosa
import moviepy.editor as mp
from moviepy.video.io.VideoFileClip import VideoFileClip

from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_audio

def extract_audio(video_path, audio_path):
    ffmpeg_extract_audio(video_path, audio_path)
def analyze_voice_confidence(audio_path):
    try:
        y, sr = librosa.load(audio_path)

        # Volume / energy
        energy = np.mean(librosa.feature.rms(y=y))

        # Pitch estimation
        pitches, magnitudes = librosa.piptrack(y=y, sr=sr)
        pitch_values = pitches[magnitudes > np.median(magnitudes)]
        avg_pitch = np.mean(pitch_values) if len(pitch_values) > 0 else 0

        # Speaking tempo
        tempo, _ = librosa.beat.beat_track(y=y, sr=sr)

        # Normalize and combine scores
        energy_score = min(energy * 1000, 100)
        pitch_score = min(avg_pitch / 5, 100)
        tempo_score = min(tempo, 100)

        final_score = round((energy_score * 0.4 + pitch_score * 0.3 + tempo_score * 0.3), 2)
        return final_score

    except Exception as e:
        print("Voice analysis error:", e)
        return 0