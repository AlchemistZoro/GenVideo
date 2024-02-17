import pandas as pd
import subprocess
import json
import os

# 读取 Excel 文件
excel_path = '/Users/wzc/Desktop/Utils/GenVideoWine/config/video.xlsx'
videos_df = pd.read_excel(excel_path)

# 初始化存储结果的字典
videos_info = []

# 循环处理每个视频
for index,row in videos_df.iterrows():
    video_name = row['video_name']
    video_path = f'/Volumes/PSSD/视频剪辑业务/白酒无声/{video_name}.MOV'

    # 检查文件是否存在
    if os.path.exists(video_path):
        try:
            # 使用 ffmpeg 获取视频信息
            cmd = f"ffprobe -v error -select_streams v:0 -show_entries stream=width,height,duration -of default=noprint_wrappers=1:nokey=1 {video_path}"
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
            output, _ = process.communicate()
            width, height, duration = output.decode().strip().split('\n')

            # 将视频信息保存到字典中
            videos_info.append({
                'description':row['description'],
                'video_path':video_path,
                'video_type':row['video_type'],
                'description':row['description'],
                'duration_ms': round(float(duration) * 1000),  # 转换为毫秒
                'resolution': f"{width}x{height}"
            })
        except Exception as e:
            print(f"Error processing {video_name}: {e}")
    else:
        print(f"Video file not found: {video_path}")

# 将结果保存到 JSON 文件
output_path = 'global/video_info.json'

# 保存音频信息到 JSON 文件，确保中文路径可读
with open(output_path, 'w', encoding='utf-8') as file:
    json.dump(videos_info, file, ensure_ascii=False, indent=4)

print("Video information has been saved.")
