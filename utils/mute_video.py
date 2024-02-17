import subprocess

number_start = 1
number_end = 69
base_input_path = '/Volumes/PSSD/视频剪辑业务/白酒/{}'
base_output_path = '/Volumes/PSSD/视频剪辑业务/白酒无声/{}'

for i in range(number_start, number_end):
    if i < 10:
        video_name = 'C000' + str(i) + '.MOV'
    else:
        video_name = 'C00' + str(i) + '.MOV'
    
    input_path = base_input_path.format(video_name)
    output_path = base_output_path.format(video_name)

    ffmpeg_cmd = f'ffmpeg -i "{input_path}" -an "{output_path}"'
    subprocess.call(ffmpeg_cmd, shell=True)
    # print(ffmpeg_cmd)  # 显示命令以供检查
