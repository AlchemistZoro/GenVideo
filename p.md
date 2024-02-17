# 营销文案生产->GPT4
## 技术
根据商家的信息：
{tech_content}
概括酒月玖品牌的10个技术优点，每个优点概括不要超过16个字。每行一个优点，不要在优点前面添加标题符号。


## 产品
根据商家的信息：
{product_content}
概括酒月玖品牌的30个关于封坛酒的优点，每个优点概括不要超过16个字。每行一个优点，不要在优点前面添加标题符号。

## 加盟
根据商家的信息：
{bussiness_content}
概括酒月玖品牌的30个关于加盟的优点，每个优点概括不要超过16个字，不要主语，用动词开头，语气强烈。每行一个优点，不要在优点前面添加标题符号。

## 钩子
模仿如下的文案，再生产10条营销文案：
酒月玖，白酒加盟新品牌
酒月玖，2024年，绝对值得一试的白酒加盟品牌

## 种草
模仿如下的文案，再生产10条营销文案：
还在等什么，赶快评论区留言咨询吧
对白酒加盟感兴趣的你，快快评论区留言吧
还有什么想了解的，赶紧评论区留言吧

# 脚本生产代码
## gen_textscript.py
写一个python程序通过给定的文案表制作视频文案，
读取config/video_text.xlsx，video_text的表头如下,:
video_type	text
技术	整合酒类全生命周期管理
技术	智能售酒机精确控制出酒量
技术	售酒机二维码个性化生成

到df_video_text
假设要制作x个视频文案，于每个需要制作的视频，结构为【钩子】,【技术/产品/认证/加盟】，【种草】构成
其中技术和认证出现的概率各20%且不会同时出现，产品和加盟是每个视频都会出现的，其中钩子出现一次，种草出现一次，产品的内容出现2-3次，加盟的内容出现2-3次，如下是一个可能的模版：
钩子
产品
产品
产品
技术
加盟
加盟
种草
并且产品的第一句话前需要加封坛酒三个字，加盟的第一句话之前需要加酒月玖三个字
对于文案的每段话，按照标点符号切分成不同的行
对于每个文案，用一个哈希码m进行标注，对于一次运行，产生一个由时间戳定义的任务序列，在./log/产生本次调用的任务序列的文件夹
将做好的x视频文案保存成json文件，文件路径位为./log/text/m.json
将所有文案的哈希码保存成xlsx文件到./log/文件夹下

## gen_audio.py
改写以下代码,row['哈希码']得到json的文件log/{task}/text/{哈希码}.json
读取的内容中，对于每个text，都赋予唯一的标识码t，调用一次 tts_utils.py的amain异步函数
loop = asyncio.get_event_loop_policy().get_event_loop()
    try:
        loop.run_until_complete(amain())
    finally:
        loop.close()
返回的结果保存在log/{task}/voice/{哈希码}/{t}.mp3
同时对于每个text最终返回的内容以：    {
        "index":,
        "text": "酒月玖",
        "video_type": "钩子",做一个保存
        "voice_path":
    },


import pandas as pd

voice_config = [
    {
        'language': "zh",
        'gender' :  "Female",
        'short_name': "zh-CN-XiaoyiNeural"
    },
    {
        'language': "zh",
        'gender' :  "Female",
        'short_name': "zh-CN-XiaoxiaoNeural"
    },
]

task = '20240130181634'
text_df = pd.read_excel('log/{}/hash_codes.xlsx'.format(task))

debug = True
if debug:
    text_df = text_df.head(1)

for index,row in text_df.iterrows():

## gen_script

最终的脚本我希望长这个样子:


# 脚本
## 视频时间/分辨率提取脚本->video_info.py
写一段代码，读取/Users/wzc/Desktop/Utils/GenVideoWine/config/video.xlsx中的所有视频(video_name column)的'/Volumes/PSSD/视频剪辑业务/白酒无声/{video_name}'的视频时间长度（精确到毫秒）和分辨率，将视频的长度和分辨率作为新的键值，将统计的结果保存到/Users/wzc/Desktop/Utils/GenVideoWine/log/20240130181634/video_info.json当中。不要用moviepy这个库用ffmepg

## 音频时间长度/平均分呗->voice_info.py
针对的是一个脚本


写一段代码，采用pydub库统计log/{task}/text_voice/{text_index}.json 中的的音频文件的音频信息，对于每个音频，统计他的采样率，平均分贝，时间长度（ms），将产生的结果保存到log/{task}/voice_info/{voice_info}.json。如果没有voice_info则创建这个文件夹。如下是{text_index}.json的脚本结构：
[
    {
        "index": 0,
        "text": "酒月玖",
        "video_type": "钩子",
        "voice_path": "log/20240130181634/voice/ca037f36d61b680be1c9acb35258f727/0.mp3"
    },
    {
        "index": 1,
        "text": "白酒加盟新品牌",
        "video_type": "钩子",
        "voice_path": "log/20240130181634/voice/ca037f36d61b680be1c9acb35258f727/1.mp3"
    },


# 视频制作代码

task_hash = '20240131164614'
text_hash = '6c4b65ffc6b258ebbf1d478ce3a97936'
json文件的路径是：/Users/wzc/Desktop/Utils/GenVideoWine/log/task_hash/script/text_hash.json
写一段python代码,给定如下的json文件按照要求制作视频：
1. 用ffmpeg，合并voice_track中的每个音频，其中start,end指的是相对于音频素材本身的时间戳(ms)，track_start,，track_end是相对于音频轨道的时间戳(ms)。
2. 同样合并bgm_track中的每个音频
3. 合并voice_track和bgm_track
4. 用ffmpeg,合并video_track中的每个视频，start,end指的是相对于视频素材本身的时间戳(ms)，track_start,，track_end是相对于视频轨道的时间戳(ms)。
5. 用ffmpeg，合并subtitle_track中的每个字幕文件，字幕放在视频底部20%处且居中的位置，字号15，track_start,，track_end是相对于视频轨道的时间戳(ms)。
6. 产生好的视频保存在log/{task}/video/{text_hash}.mp4
---
参考如下代码的实现方法，修改add_subtitles_to_video函数，没有现成的src文件，  函数调用的方式如下：
    final_video_path = video_dir+"final_video.mp4"
    add_subtitles_to_video(video_with_audio_path, json_data["subtitle_track"], final_video_path)
要求用ffmpeg，合并subtitle_track中的每个字幕文件，字幕放在视频底部20%处且居中的位置，需要实现自适应如果，超过视频尺寸了自动居中换行，字号15，track_start,，track_end是相对于视频轨道的时间戳(ms)。

"subtitle_track":[
        {
            "name":"白字黑边",
            "border_alpha": 1.0,
            "border_color": "#000000",
            "border_width": 1,
            "text_alpha": 1.0,
            "text_color": "#ffffff",
            "font_path":  "/Users/wzc/Desktop/Utils/GenVideoWine/fonts/SystemFont/zh-hans.ttf" ,
            "track_start": 0,
            "track_end": 1488,
            "text": "酒月玖"              
        },
        {
            "name":"黑字白边",
            "border_alpha": 1.0,
            "border_color": "#ffffff",
            "border_width": 1,
            "text_alpha": 1.0,
            "text_color": "#000000",
            "font_path":  "/Users/wzc/Desktop/Utils/GenVideoWine/fonts/SystemFont/zh-hans.ttf" ,
            "track_start": 1488,
            "track_end": 3337,
            "text": "让您事半功倍！"
                                   
        }

def get_ffmpeg_words_command(args,text,start_time,offset):
 
 ffmpeg_words_command = f'drawtext=fontfile={args.font_path}:text={text}:fontsize=({args.fontsize}):fontcolor={args.fontcolor}:x=(main_w/2-text_w/2):y=(main_h/2+text_h/2+{offset}):enable=\'between(t,{start_time},{start_time+3})\':bordercolor={args.bordercolor}:borderw={args.borderw}'
 return ffmpeg_words_command


## 音频自适应分呗
修改以下代码，统计voice_track中所有dbfs键的平均值mdbfs，bgm_track的在合并前需要将分呗数调整为mdbfs-5

# script脚本产生
## voice
补全gen_voice_script函数
1. 按照voice_info_list的index进行排列
2. start=0,end=duration_ms
3. start_track 第一个是0，后面的每个start_track都是上一个的end_track.
4. end_track = start_track + end
5. 需要保留的信息：
                "index": 0,
                "file_path": "log/20240131164614/voice/6c4b65ffc6b258ebbf1d478ce3a97936/0.mp3",
                "dbfs": -20.230462615324146,
                "start":0,
                "end":1488,
                "track_start":0,
                "track_end":1488
6. 以追加的方式存入script_path,格式是:{
    "audio_track" : {
        "voice_track": [
            {
                ...
            },
            {
                ...
            }
        ]
    }
}

## bgm
补全gen_bgm_script

def gen_bgm_script(bgm_info_path,script_path,duration):
    pass


1. 读取bgm_info_path，随机选择一个duration_ms参数大于duraion作为bgm
2. start,track_start = 0,0 end,end_track = duration,duraiton
3. 读取script_path文件,需要把新的内容加到原来的文件中,格式是:{
    "audio_track" : {
        "bgm_track": {
                "file_path": "/Volumes/PSSD/音乐/白酒加盟BGM/Jellyfish.mp3",
                "dbfs": -12.258063112914531,
                "duration_ms": 221379,
                "track_start": 0,
                "track_end": 3337,
                "start":0,
                "end": 3337
        }

    }
}

## subtitle
补全gen_subtitle_script函数
def gen_subtitle_script(script_path,subtitle_info_path):
    pass
1. 读取subtitle_info_path，随机选择一个字幕配置方案
2. 读取script_path文件，"audio_track": {
        "voice_track": [按照voice的index顺序，构造数组，其中subtitle_track的text,track_start,end_track 和 voice一致
3. ,需要把新的内容加到原来的文件中,格式是:
 {"subtitle_track":[
        {
            "name":"白字黑边",
            "background_alpha": 1.0,
            "background_color": "",
            "background_height": 0.14,
            "border_alpha": 1.0,
            "border_color": "#000000",
            "border_width": 10,
            "text_alpha": 1.0,
            "text_color": "#ffffff",
            "font_path":  "/Users/wzc/Desktop/Utils/GenVideoWine/fonts/SystemFont/zh-hans.ttf" ,
            "track_start": 0,
            "track_end": 1488,
            "text": "酒月玖"              
        },{

        }
 }
 这是"audio_track": {
        "voice_track": [
            {
                "index": 0,
                "file_path": "log/20240131164614/voice/6c4b65ffc6b258ebbf1d478ce3a97936/0.mp3",
                "dbfs": -21.949605854899616,
                "start": 0,
                "end": 2040,
                "track_start": 0,
                "track_end": 2040
            },
            {
                "index": 1,
                "file_path": "log/20240131164614/voice/6c4b65ffc6b258ebbf1d478ce3a97936/1.mp3",
                "dbfs": -21.8277081908446,
                "start": 0,
                "end": 2928,
                "track_start": 2040,
                "track_end": 4968
            },

## video
补全gen_subtitle_script函数
def gen_video_script(video_info_path,script_path):
    pass
1. 读取video_info_path，随机选择一个字幕配置方案
2. 读取script_path文件，"audio_track": {
        "voice_track": []
3. 按照index进行划分可以得到按照video_type排列的数组type_list:[
    {video_type:"种草",start_time:,end_time}
]
即在start_time到end_time里都是某个特定的video_type
4. 根据规则匹配对应的视频片段，对于每个type_list,需要满足的条件是只从对应的video_type里挑选视频，从满足条件的video_type并且description不能相同的video_info_path中随机选择长度3-5秒的视频进行填充
video_info_path：
[
    {
        "description": "官方宣传片段",
        "video_path": "/Volumes/PSSD/视频剪辑业务/白酒无声/C0001.MOV",
        "video_type": "钩子",
        "duration_ms": 40040,
        "resolution": "1080x1920"
    },{}]
这是 "audio_track": {
        "voice_track": [
            {
                "index": 0,
                "file_path": "log/20240131164614/voice/10bd237547b9698f7f2d6c1b007a9554/0.mp3",
                "dbfs": -21.949605854899616,
                "start": 0,
                "end": 2040,
                "track_start": 0,
                "track_end": 2040,
                "video_type": "钩子",
                "text": "酒月玖"
            },
            {
                "index": 1,
                "file_path": "log/20240131164614/voice/10bd237547b9698f7f2d6c1b007a9554/1.mp3",
                "dbfs": -22.188419799922055,
                "start": 0,
                "end": 3768,
                "track_start": 2040,
                "track_end": 5808,
                "video_type": "钩子",
                "text": "携手共创白酒加盟新辉煌！"
            },
最后返回的video_track要按照这样的格式，    "video_track":[
        {
            "video_path": "/Volumes/PSSD/视频剪辑业务/白酒无声/C0001.MOV",
            "start":0,
            "end": 1000
        },
        {
            "video_path": "/Volumes/PSSD/视频剪辑业务/白酒无声/C0020.MOV",
            "start":0,
            "end": 1000
        },

二次修改
更改选择视频片段的逻辑，对于type_list的第一个type和最后一个type，只选择一个视频。
对于中间的部分，通过算法匹配使得，每个视频的长度在4-7秒，而不要出现过短的视频片段。
选择好视频之后，start和end进行随机，只需要end-start = 需要的视频长度，并且 start>0,end< duration_ms 即可
出的结果：
1. 对于 type_list 的第一个和最后一个类型，只选择一个视频片段。
2. 对于 type_list 中间的部分，选择一个或多个视频片段，使得每个视频的长度在4到7秒之间。
3. 对于每个选中的视频片段，start 和 end 需要随机确定，满足 end - start 等于所需的视频长度，且 start > 0 且 end < duration_ms。