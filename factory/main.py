import subprocess
import os
import json
from factory.audio import merge_audio_tracks
from factory.video import merge_video_tracks
from factory.subtitle import add_subtitles_to_video
import shutil  # 导入shutil模块

def run_command(command):
    """运行给定的命令，使用subprocess模块"""
    try:
        subprocess.run(command, check=True, shell=True)
    except subprocess.CalledProcessError as e:
        print(f"命令执行出错: {e}")

def make_one_video(task_hash,text_hash):
    json_file_path = f'log/{task_hash}/script/{text_hash}.json'
    with open(json_file_path, 'r', encoding='utf-8') as file:
        json_data = json.load(file)
    video_dir = f'log/{task_hash}/video/{text_hash}/'
    os.makedirs(video_dir, exist_ok=True)

    merged_audio_path = video_dir+"merged_audio.mp3"
    merge_audio_tracks(json_data["audio_track"]["voice_track"], json_data["audio_track"]["bgm_track"], merged_audio_path)

    merged_video_path = video_dir+"merged_video.mp4"
    merge_video_tracks(json_data["video_track"], merged_video_path)

    video_with_audio_path = video_dir+"video_with_audio.mp4"
    
    command = f"ffmpeg -y -i {merged_video_path} -i {merged_audio_path} -c:v copy -c:a copy -map 0:v:0 -map 1:a:0 {video_with_audio_path}"

    run_command(command)

    final_video_path = video_dir+"final_video.mp4"
    add_subtitles_to_video(video_with_audio_path, json_data["subtitle_track"], final_video_path)
    os.remove(video_with_audio_path)
    os.remove(merged_video_path)
    os.remove(merged_audio_path)

    # 创建video_output目录（如果不存在）
    output_dir = f'log/{task_hash}/video_output/'
    os.makedirs(output_dir, exist_ok=True)

    # 移动最终视频文件到video_output目录，并重命名
    output_video_path = output_dir + f'{text_hash}.mp4'
    shutil.move(final_video_path, output_video_path)

    print("视频制作完成！")

def make_videos(task_code):
    task_dir = f'log/{task_code}/'
    hash_path = task_dir + 'hash_codes.json'
    output_dir = task_dir + 'video_output/'

    # 确保输出目录存在
    os.makedirs(output_dir, exist_ok=True)

    # 读取已经存在的视频文件的哈希列表
    existing_hashes = {filename.split('.')[0] for filename in os.listdir(output_dir) if filename.endswith('.mp4')}

    # 读取需要处理的哈希列表
    with open(hash_path, 'r', encoding='utf-8') as file:
        text_hash_list = json.load(file)

    # 移除已经存在视频文件的哈希
    text_hash_list = [hash_value for hash_value in text_hash_list if hash_value not in existing_hashes]

    # 对剩余的哈希值进行视频生成处理
    for text_hash in text_hash_list:
        make_one_video(task_code, text_hash)

if __name__ == "__main__":
    pass