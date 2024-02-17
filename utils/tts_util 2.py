import asyncio
import random
import edge_tts
from edge_tts import VoicesManager
import io
import json
from edge_tts.exceptions import NoAudioReceived
from typing import Optional, Tuple


class EdgeTTSHandler:
    """
    EdgeTTSHandler类用于处理和简化edge_tts的使用。

    用例:
    handler = EdgeTTSHandler(text="你好，世界!")
    handler.save_audio("output.mp3")
    handler.save_audio_with_subtitles("output_with_subs.mp3", "output.vtt")
    """

    def __init__(self, text: str, language: str = "zh", gender: str = "Male", short_name="zh-CN-YunxiNeural"):
        self.text = text
        self.language = language
        self.gender = gender
        self.short_name = short_name
        self.voice = None
        self.communicate = None

    async def _initialize_communicate(self):
        """初始化Communicate对象"""
        if not self.voice:
            self.voice = await self._get_voice(self.gender, self.language, self.short_name)
        self.communicate = edge_tts.Communicate(self.text, self.voice)

    async def _get_voice(self, gender: str, language: str, short_name: str) -> str:
        """根据性别和语言获取语音"""
        voices = await VoicesManager.create()
        voice = voices.find(Gender=gender, Language=language, ShortName=short_name)

        if not voice:
            raise ValueError(f"No voice found for gender '{gender}' and language '{language}'")

        return random.choice(voice)["Name"]

    async def save_in_memory(self) -> Tuple[io.BytesIO, Optional[io.StringIO]]:
        """
        Save the audio and metadata in memory and return them.
        """
        if not self.communicate:
            await self._initialize_communicate()

        written_audio: bool = False
        audio_buffer = io.BytesIO()
        metadata_buffer = io.StringIO()

        async for message in self.communicate.stream():
            if message["type"] == "audio":
                audio_buffer.write(message["data"])
                written_audio = True
            elif message["type"] == "WordBoundary":
                json.dump(message, metadata_buffer)
                metadata_buffer.write("\n")

        if not written_audio:
            raise NoAudioReceived(
                "No audio was received from the service, so the buffer is empty."
            )

        return audio_buffer, metadata_buffer

    async def save_audio(self, output_file: str):
        """
        保存文本为音频文件。

        参数:
        - output_file (str): 输出音频文件的路径。
        """
        if not self.communicate:
            await self._initialize_communicate()
        await self.communicate.save(output_file)

    async def save_audio_with_subtitles(self, output_file: str, webvtt_file: str):
        """
        保存文本为音频文件并生成字幕。

        参数:
        - output_file (str): 输出音频文件的路径。
        - webvtt_file (str): 输出字幕文件的路径。
        """
        if not self.communicate:
            await self._initialize_communicate()
        submaker = edge_tts.SubMaker()
        with open(output_file, "wb") as file:
            async for chunk in self.communicate.stream():
                if chunk["type"] == "audio":
                    file.write(chunk["data"])
                elif chunk["type"] == "WordBoundary":
                    submaker.create_sub((chunk["offset"], chunk["duration"]), chunk["text"])

        with open(webvtt_file, "w", encoding="utf-8") as file:
            file.write(submaker.generate_subs())

async def main_get_voice(language: str = "zh", 
                    gender: str = "Male",
                    short_name = "zh-CN-YunxiNeural",
                    text: str = "hello",
                    save_path: str =  "output.mp3"):
    handler = EdgeTTSHandler(text=text, language=language, gender=gender, short_name=short_name)
    await handler.save_audio(save_path)

async def amain(text, config, voice_path):

    handler = EdgeTTSHandler(text=text, language=config['language'], gender=config['gender'], short_name=config['short_name'])
    await handler.save_audio(voice_path)
    # print(text)
    # await handler.save_audio_with_subtitles("output_with_subs.mp3", "output.vtt")
    # return save_path

if __name__ == "__main__":
    config = {
        'language': "zh",
        'gender': "Female",
        'short_name': "zh-CN-XiaoyiNeural"
    }
    voice_path = '{}.mp3'.format(config['short_name'])
    text = '原神，启动！'
    loop = asyncio.get_event_loop_policy().get_event_loop()
    try:
        loop.run_until_complete(amain(text, config, voice_path))
    finally:
        loop.close()
