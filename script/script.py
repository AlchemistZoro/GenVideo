import json
import pandas as pd
import random
import os
def gen_subtitle_script(script_path, subtitle_info_path):
    # 读取字幕配置方案
    with open(subtitle_info_path, 'r', encoding='utf-8') as file:
        subtitle_info_list = json.load(file)

    # 随机选择一个字幕配置方案
    selected_subtitle_info = random.choice(subtitle_info_list)

    # 读取现有的脚本文件
    with open(script_path, 'r', encoding='utf-8') as file:
        script_data = json.load(file)

    # 获取voice_track信息
    voice_tracks = script_data.get('audio_track', {}).get('voice_track', [])

    # 为每个voice轨道构造相应的subtitle_track
    subtitle_tracks = []
    for voice_track in voice_tracks:
        subtitle_track = selected_subtitle_info.copy()  # 复制选中的字幕配置
        subtitle_track['text'] = voice_track.get('text', '')  # 使用voice轨道的文本作为字幕文本
        subtitle_track['track_start'] = voice_track.get('track_start', 0)
        subtitle_track['track_end'] = voice_track.get('track_end', 0)
        subtitle_tracks.append(subtitle_track)

    # 将构造的subtitle_track数组加入到脚本中
    if 'audio_track' not in script_data:
        script_data['audio_track'] = {}
    script_data['subtitle_track'] = subtitle_tracks

    # 将更新后的数据写回脚本文件
    with open(script_path, 'w', encoding='utf-8') as file:
        json.dump(script_data, file, ensure_ascii=False, indent=4)


def gen_bgm_script(bgm_info_path, script_path, duration):
    # 读取背景音乐信息
    with open(bgm_info_path, 'r', encoding='utf-8') as file:
        bgm_info_list = json.load(file)

    # 筛选出duration_ms大于给定duration的背景音乐
    suitable_bgm = [bgm for bgm in bgm_info_list if bgm['duration_ms'] > duration]

    # 如果没有合适的背景音乐，则不进行任何操作
    if not suitable_bgm:
        print("没有找到合适的背景音乐")
        return

    # 从合适的背景音乐中随机选择一个
    selected_bgm = random.choice(suitable_bgm)

    # 设置bgm的起始和结束参数
    selected_bgm['start'] = 0
    selected_bgm['track_start'] = 0
    selected_bgm['end'] = duration
    selected_bgm['track_end'] = duration

    # 读取原有的脚本文件（如果存在）
    try:
        with open(script_path, 'r', encoding='utf-8') as file:
            script_data = json.load(file)
    except FileNotFoundError:
        script_data = {"audio_track": {}}

    # 将选定的背景音乐信息添加到脚本中
    script_data['audio_track']['bgm_track'] = selected_bgm

    # 将更新后的数据写回脚本文件
    with open(script_path, 'w', encoding='utf-8') as file:
        json.dump(script_data, file, ensure_ascii=False, indent=4)


def gen_voice_script(voice_info_list, script_path):
    # 按照voice_info_list的index进行排序
    sorted_voice_info_list = sorted(voice_info_list, key=lambda x: x['index'])

    # 初始化track_start和track_end
    track_start = 0
    voice_track = []

    # 遍历排序后的voice_info_list，计算每个语音片段的start_track和end_track
    for voice_info in sorted_voice_info_list:
        end_track = track_start + voice_info['duration_ms']  # end_track是当前track_start加上duration
        voice_track.append({
            "index": voice_info['index'],
            "file_path": voice_info['file_path'],
            "dbfs": voice_info['dbfs'],
            "start": 0,  # start始终为0
            "end": voice_info['duration_ms'],  # end使用voice_info中的end值
            "track_start": track_start,
            "track_end": end_track,
            "video_type":voice_info['video_type'],
            "text":voice_info['text']
        })
        track_start = end_track  # 更新下一个语音片段的track_start为当前的end_track

    # 将结果保存到script_path指定的文件中
    script_data = {
        "audio_track": {
            "voice_track": voice_track
        }
    }
    
    # 以追加模式写入文件
    with open(script_path, 'w', encoding='utf-8') as file:
        json.dump(script_data, file, ensure_ascii=False, indent=4)

    # 返回最后一个voice_track的end_track作为duration
    return track_start

def gen_video_script(video_info_path, script_path):
    # 读取视频信息
    with open(video_info_path, 'r', encoding='utf-8') as file:
        video_info_list = json.load(file)

    # 按视频类型分类视频信息
    video_info_by_type = {}
    for video_info in video_info_list:
        video_type = video_info['video_type']
        if video_type not in video_info_by_type:
            video_info_by_type[video_type] = []
        video_info_by_type[video_type].append(video_info)

    # 读取脚本信息，获取voice_track
    with open(script_path, 'r', encoding='utf-8') as file:
        script_data = json.load(file)
    voice_tracks = script_data.get('audio_track', {}).get('voice_track', [])

    # 构造type_list
    type_list = []
    for voice_track in sorted(voice_tracks, key=lambda x: x['index']):
        if not type_list or type_list[-1]['video_type'] != voice_track['video_type']:
            # 如果type_list为空或者当前voice_track的video_type与type_list最后一项的video_type不同
            # 则添加新的条目到type_list
            type_list.append({
                "video_type": voice_track['video_type'],
                "start_time": voice_track['track_start'],
                "end_time": voice_track['track_end']
            })
        else:
            # 如果当前voice_track的video_type与type_list最后一项的video_type相同
            # 则更新type_list最后一项的end_time
            type_list[-1]['end_time'] = max(type_list[-1]['end_time'], voice_track['track_end'])
    
    
    video_tracks = []

    for index, type_item in enumerate(type_list):
        used_descriptions = set()  # 用于记录已使用的视频描述以避免重复
        time_needed = type_item['end_time'] - type_item['start_time']

        # 对于中间部分，确保每个视频的长度在4到7秒之间
        if index != 0 and index != len(type_list) - 1:
            current_time = 0
            while current_time < time_needed:
                possible_videos = [video for video in video_info_by_type.get(type_item['video_type'], [])
                                if video['description'] not in used_descriptions and video['duration_ms'] >= 4000]

                if not possible_videos:
                    break  # 如果没有符合条件的视频，跳出循环

                selected_video = random.choice(possible_videos)
                # 确保视频时长选择范围有效
                max_possible_duration = min(7000, selected_video['duration_ms'], time_needed - current_time)
                if max_possible_duration < 4000:  # 如果最大可能时长小于4秒，调整选择范围
                    video_duration = max_possible_duration
                else:
                    video_duration = random.randint(4000, max_possible_duration)

                video_start = random.randint(0, selected_video['duration_ms'] - video_duration)
                video_tracks.append({
                "video_path": selected_video['video_path'],
                "video_type": selected_video['video_type'],
                "duration_ms": selected_video['duration_ms'],
                "resolution": selected_video['resolution'],
                "start": video_start,
                "end": video_start + video_duration,
                "description":selected_video['description']
                })

                used_descriptions.add(selected_video['description'])
                current_time += video_duration


        else:
            current_time = 0

            while current_time < time_needed:
                possible_videos = [video for video in video_info_by_type.get(type_item['video_type'], [])
                                if video['description'] not in used_descriptions and video['duration_ms'] > 7000]

                if not possible_videos:
                    break  # 如果没有符合条件的视频，跳出循环

                selected_video = random.choice(possible_videos)
                video_duration = time_needed
                video_start = random.randint(0, selected_video['duration_ms'] - video_duration)

                video_tracks.append({
                "video_path": selected_video['video_path'],
                "video_type": selected_video['video_type'],
                "duration_ms": selected_video['duration_ms'],
                "resolution": selected_video['resolution'],
                "start": video_start,
                "end": video_start + video_duration,
                "description":selected_video['description']
                })

                used_descriptions.add(selected_video['description'])
                current_time += video_duration

    # 将选择的视频信息加入到脚本中
    if 'video_track' not in script_data:
        script_data['video_track'] = []
    script_data['video_track'].extend(video_tracks)

    # 将更新后的数据写回脚本文件
    with open(script_path, 'w', encoding='utf-8') as file:
        json.dump(script_data, file, ensure_ascii=False, indent=4)
   

def gen_script(task_code):
    task_dir = f'log/{task_code}/'
    hash_path = task_dir+'hash_codes.json'
    bgm_info_path = 'global/bgm_info.json'
    video_info_path = 'global/video_info.json'
    subtitle_info_path = 'global/subtitle_info.json'
    voice_info_dir = task_dir+'voice_info/'
    script_dir = task_dir+'script/'

    os.makedirs(script_dir,exist_ok=True)

    with open(hash_path, 'r', encoding='utf-8') as file:
        text_hash_list = json.load(file)

    for text_hash in text_hash_list:
        voice_info_path = voice_info_dir + text_hash + '.json'
        with open(voice_info_path, 'r', encoding='utf-8') as file:
            voice_info_list = json.load(file)
        script_path = script_dir + text_hash + '.json'

        duration = gen_voice_script(voice_info_list,script_path)
        
        gen_bgm_script(bgm_info_path,script_path,duration)
        
        gen_subtitle_script(script_path,subtitle_info_path)
        
        gen_video_script(video_info_path,script_path)

        


  

