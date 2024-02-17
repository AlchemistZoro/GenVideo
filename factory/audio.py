import subprocess
import os
import time
def run_command(command):
    """运行给定的命令，使用subprocess模块"""
    try:
        subprocess.run(command, check=True, shell=True)
    except subprocess.CalledProcessError as e:
        print(f"命令执行出错: {e}")

def calculate_mdbfs(voice_tracks):
    """计算voice_tracks中所有dbfs键的平均值mdbfs"""
    total_dbfs = sum(track['dbfs'] for track in voice_tracks)
    mdbfs = total_dbfs / len(voice_tracks) if voice_tracks else 0
    return mdbfs

def adjust_bgm_volume(bgm_track, mdbfs, adjusted_bgm_path):
    """调整背景音乐的分贝数为mdbfs-5"""
    adjusted_dbfs = mdbfs - 6
    volume_adjustment = adjusted_dbfs - bgm_track['dbfs']  # 计算需要调整的分贝数
    run_command(f"ffmpeg -y -i \"{bgm_track['file_path']}\" -filter:a \"volume={volume_adjustment}dB\" {adjusted_bgm_path}")

def trim_and_delay_audio(input_path, start, end, prev_track_end, track_start, output_path):
    """裁剪音频并在轨道上正确位置添加延迟"""
    duration = (end - start) / 1000  # 转换为秒
    silence_duration = max((track_start - prev_track_end) / 1000, 0)  # 计算需要添加的静音长度，保证非负

    # 生成静音音频
    silence_audio = f"silence_{track_start}.mp3"
    run_command(f"ffmpeg -f lavfi -i anullsrc=r=24000:cl=mono -t {silence_duration} {silence_audio}")

    # 裁剪音频
    trimmed_audio = f"trimmed_{track_start}.mp3"
    run_command(f"ffmpeg -i {input_path} -ss {start / 1000} -t {duration} {trimmed_audio}")

    # 合并静音音频和裁剪后的音频
    run_command(f"ffmpeg -i \"concat:{silence_audio}|{trimmed_audio}\" -acodec copy {output_path}")

    # 清理临时文件
    os.remove(silence_audio)
    os.remove(trimmed_audio)

def merge_audio_tracks(voice_tracks, bgm_track, output_path):
    """合并语音轨道和背景音乐轨道，考虑时间参数"""
    mdbfs = calculate_mdbfs(voice_tracks)
    adjusted_bgm_path = "adjusted_bgm.mp3"
    adjust_bgm_volume(bgm_track, mdbfs, adjusted_bgm_path)
    # time.sleep(10000)
    temp_voice_tracks = []
    prev_track_end = 0

    for track in voice_tracks:
        temp_output_path = f"temp_voice_{track['index']}.mp3"
        trim_and_delay_audio(track['file_path'], track['start'], track['end'], prev_track_end, track['track_start'], temp_output_path)
        temp_voice_tracks.append(temp_output_path)
        prev_track_end = track['track_end']

    # 合并所有处理过的语音轨道
    voice_list_content = "\n".join([f"file '{track}'" for track in temp_voice_tracks])
    voice_list_file = "voice_files.txt"
    with open(voice_list_file, 'w') as f:
        f.write(voice_list_content)

    merged_voice = "merged_voice.mp3"
   
    run_command(f"ffmpeg -y -f concat -safe 0 -i {voice_list_file} -c copy {merged_voice}")

    # 合并语音和背景音乐
    run_command(f"ffmpeg -y -i {merged_voice} -i {adjusted_bgm_path} -filter_complex \"[0:a][1:a]amerge=inputs=2[a]\" -map \"[a]\" -ac 2 {output_path}")

    # 清理临时文件
    for track in temp_voice_tracks:
        os.remove(track)
    os.remove(voice_list_file)
    os.remove(merged_voice)
    
    os.remove(adjusted_bgm_path)
 