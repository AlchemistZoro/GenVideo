import pandas as pd
import numpy as np
import os
import hashlib
import json
import time
import collections
import re
# 读取Excel文件到df_video_text
df_video_text = pd.read_excel('config/video_text.xlsx')

# 生成哈希码
def generate_hash(text):
    return hashlib.md5(text.encode()).hexdigest()

def generate_video_script(df_video_text):
    script_details = []

    # 定义一个辅助函数来添加文案和类型
    def add_script(text, video_type):
        for line in re.split('，|。|？',text):
            script_details.append({"text": line, "video_type": video_type})

    # 随机选择钩子、种草，并添加到文案详情中
    hook = df_video_text[df_video_text['video_type'] == '钩子'].sample(1).iloc[0]
    add_script(hook['text'], hook['video_type'])



    # 选择产品和加盟，保证第一句话前加上指定内容，并添加到文案详情中
    product_texts = df_video_text[df_video_text['video_type'] == '产品'].sample(np.random.randint(2, 4))
    add_script("封坛酒","产品")
    for p in product_texts.itertuples():
        add_script(p.text, p.video_type)

    franchise_texts = df_video_text[df_video_text['video_type'] == '加盟'].sample(np.random.randint(2, 4))
    add_script("酒月玖","加盟")
    for f in franchise_texts.itertuples():
        add_script(f.text, f.video_type)

    # 20%的概率选择包含“技术”或“认证”，并添加到文案详情中
    tech_or_cert_choice = np.random.choice(['技术', '认证', '无'], p=[0.2, 0.2, 0.6])
    if tech_or_cert_choice != '无':
        tech_or_cert_text = df_video_text[df_video_text['video_type'] == tech_or_cert_choice].sample(1).iloc[0]
        add_script(tech_or_cert_text['text'], tech_or_cert_text['video_type'])

    grass = df_video_text[df_video_text['video_type'] == '种草'].sample(1).iloc[0]
    add_script(grass['text'], grass['video_type'])

    return script_details

def gen_text(task_code,text_number):

    log_dir = f'log/{task_code}'
    os.makedirs(log_dir, exist_ok=True)
    os.makedirs(f'{log_dir}/text', exist_ok=True)  # 确保文案目录存在

    # 生成x个视频文案
    x = text_number
    hash_codes = []
    for i in range(x):
        script_details = generate_video_script(df_video_text)
        script_text = '，'.join([detail['text'] for detail in script_details])  # 将文案列表转换为一个长字符串，以便于哈希
        hash_code = generate_hash(script_text)
        hash_codes.append(hash_code)
        # 保存整个文案为一个JSON文件
        with open(f'{log_dir}/text/{hash_code}.json', 'w', encoding='utf-8') as f:
            json.dump(script_details, f, ensure_ascii=False, indent=4)


    with open(f'{log_dir}/hash_codes.json', 'w') as json_file:
        json.dump(hash_codes, json_file, indent=4)

