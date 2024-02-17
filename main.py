

from script.text import gen_text
from script.audio import gen_audio
from script.script import gen_script
from factory.main import make_videos
import time
import asyncio


def main(text_number):
    # 创建任务序列和日志目录
    # task_code = time.strftime("%Y%m%d%H%M%S")
    task_code = '20240202142532'
    # gen_text(task_code,text_number)
    voice_config = [
        {'language': "zh", 'gender': "Female", 'short_name': "zh-CN-XiaoyiNeural"},
        {'language': "zh", 'gender': "Female", 'short_name': "zh-CN-XiaoxiaoNeural"}
    ]
    # asyncio.run(gen_audio(task_code, voice_config))

    gen_script(task_code)

    # time.sleep(20)

    make_videos(task_code)


if __name__ == "__main__":
    
    text_number = 100
    main(text_number)