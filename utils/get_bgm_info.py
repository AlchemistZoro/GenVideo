import json
import os
from pydub import AudioSegment
from pydub.utils import mediainfo
from glob import glob

def analyze_audio(audio_path):
    """分析音频文件，返回采样率、平均分贝和时间长度（毫秒）"""
    audio = AudioSegment.from_file(audio_path)
    duration_ms = len(audio)
    dbfs = audio.dBFS  # 平均分贝
    sampling_rate = mediainfo(audio_path)['sample_rate']
    return sampling_rate, dbfs, duration_ms

# 指定 task 和音频文件夹路径
audio_folder_path = f'/Volumes/PSSD/音乐/白酒加盟BGM/'  # 假设音频文件存储在此文件夹下
bgm_info_path = f'global/bgm_info.json'

# 检索文件夹下的所有 MP3 文件
audio_files = glob(os.path.join(audio_folder_path, '*.mp3'))

# 初始化存储音频信息的列表
bgm_info = []

# 分析每个音频文件
for audio_path in audio_files:
    if os.path.exists(audio_path):
        sampling_rate, dbfs, duration_ms = analyze_audio(audio_path)
        bgm_info.append({
            'file_path': audio_path,
            'sampling_rate': sampling_rate,
            'dbfs': dbfs,
            'duration_ms': duration_ms
        })

# 保存音频信息到 JSON 文件
with open(bgm_info_path, 'w',encoding='utf-8') as file:
    json.dump(bgm_info, file, ensure_ascii=False, indent=4)

print("BGM information has been saved.")
