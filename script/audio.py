import asyncio
import json
import os
import random
from pydub import AudioSegment
from edge_tts import VoicesManager, Communicate
from edge_tts.exceptions import NoAudioReceived

voice_infos = {}  # 全局字典来存储voice_info

class EdgeTTSHandler:
    def __init__(self, text: str, config: dict, hash_code: str, text_index: int, voice_dir: str, task: str, video_type: str):
        self.text = text
        self.config = config
        self.hash_code = hash_code
        self.text_index = text_index
        self.voice_dir = voice_dir
        self.task = task
        self.video_type = video_type
        self.voice_path = f'{voice_dir}/{hash_code}/{text_index}.mp3'
        os.makedirs(os.path.dirname(self.voice_path), exist_ok=True)

    async def _get_voice(self):
        voices = await VoicesManager.create()
        voice = voices.find(Gender=self.config['gender'], Language=self.config['language'], ShortName=self.config['short_name'])
        if not voice:
            raise ValueError(f"No voice found for gender '{self.config['gender']}' and language '{self.config['language']}'")
        return random.choice(voice)["Name"]

    async def save_audio_and_analyze(self):
        voice = await self._get_voice()
        communicate = Communicate(self.text, voice)
        await communicate.save(self.voice_path)
        self.analyze_audio()

    def analyze_audio(self):
        audio = AudioSegment.from_file(self.voice_path)
        voice_info = {
            'index': self.text_index,
            'file_path': self.voice_path,
            'sampling_rate': audio.frame_rate,
            'dbfs': audio.dBFS,
            'duration_ms': len(audio),
            'text': self.text,
            'hash_code': self.hash_code,
            'video_type': self.video_type
        }
        # 将voice_info添加到全局字典中
        if self.hash_code not in voice_infos:
            voice_infos[self.hash_code] = []
        voice_infos[self.hash_code].append(voice_info)

    async def write_voice_info_for_hash_code(self, task):
        voice_info_path = os.path.join('log', task, 'voice_info', f'{self.hash_code}.json')
        os.makedirs(os.path.dirname(voice_info_path), exist_ok=True)
        with open(voice_info_path, 'w', encoding='utf-8') as f:
            json.dump(voice_infos[self.hash_code], f, ensure_ascii=False, indent=4)

async def process_text_voice(text, config, hash_code, text_index, voice_dir, task, video_type):
    handler = EdgeTTSHandler(text, config, hash_code, text_index, voice_dir, task, video_type)
    await handler.save_audio_and_analyze()
    await handler.write_voice_info_for_hash_code(task)  # 在每个文本处理后写入voice_info

async def gen_audio(task, voice_config):
    text_path = os.path.join('log', task, 'text')
    voice_dir = os.path.join('log', task, 'voice')

    for hash_code in os.listdir(text_path):
        if hash_code.endswith('.json') and not os.path.exists(os.path.join(voice_dir, hash_code[:-5])):
            json_file_path = os.path.join(text_path, hash_code)
            with open(json_file_path, 'r', encoding='utf-8') as file:
                texts = json.load(file)

            tasks = []
            config = random.choice(voice_config)
            for text_index, text_info in enumerate(texts):
                tasks.append(process_text_voice(text_info['text'], config, hash_code[:-5], text_index, voice_dir, task, text_info['video_type']))

            await asyncio.gather(*tasks)
        await asyncio.sleep(1)

if __name__ == "__main__":
    task = '20240202003506'
    voice_config = [
        {'language': "zh", 'gender': "Female", 'short_name': "zh-CN-XiaoyiNeural"},
        {'language': "zh", 'gender': "Female", 'short_name': "zh-CN-XiaoxiaoNeural"}
    ]
    asyncio.run(gen_audio(task, voice_config))
