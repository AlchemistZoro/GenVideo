import subprocess
import os

def run_command(command):
    """运行给定的命令，使用subprocess模块"""
    try:
        subprocess.run(command, check=True, shell=True)
    except subprocess.CalledProcessError as e:
        print(f"命令执行出错: {e}")

def trim_video_segment(video_path, start, end, trimmed_output_path):
    """剪辑视频片段"""
    start_seconds = start / 1000  # 将毫秒转换为秒
    duration = (end - start) / 1000  # 计算剪辑时长
  
    run_command(f"ffmpeg -y -i {video_path} -ss {start_seconds} -t {duration} {trimmed_output_path}")

def merge_video_tracks(video_tracks, output_path):
    """合并视频轨道"""
    trimmed_videos = []
    for index, track in enumerate(video_tracks):
        trimmed_path = f"temp_trimmed_{index}.mp4"  # 临时文件名
        trim_video_segment(track['video_path'], track['start'], track['end'], trimmed_path)
        trimmed_videos.append(trimmed_path)
    
    # 创建包含所有剪辑视频文件路径的文本文件
    video_files_content = "\n".join([f"file '{video}'" for video in trimmed_videos])
    video_list_file = "video_files.txt"
    with open(video_list_file, 'w') as f:
        f.write(video_files_content)

    # # 错误代码，不重新编码会出现问题
    # run_command(f"ffmpeg -f concat -safe 0 -i {video_list_file} -c copy {output_path}")

    # 使用ffmpeg合并剪辑后的视频
    run_command(f"ffmpeg -y -f concat -safe 0 -i {video_list_file} {output_path}")

    # 清理临时文件
    for video in trimmed_videos:
        os.remove(video)
    os.remove(video_list_file)

