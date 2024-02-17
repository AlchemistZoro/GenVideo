import subprocess

number_start = 1
number_end = 17
for i in range(number_start,number_end):
    if i < 10: i_str = '0'+str(i)
    else: i_str = str(i)
    ffmpeg_cmd = f'ffmpeg -i /Users/wzc/Desktop/公司项目数据集/白酒/1.3白酒加盟/C00{str(i_str)}.MOV -vn ../raw_audio/C00{str(i_str)}.mp3'
    subprocess.call(ffmpeg_cmd, shell=True)