import subprocess

def run_command(command):
    """运行给定的命令，使用subprocess模块"""
    try:
        subprocess.run(command, check=True, shell=True)
    except subprocess.CalledProcessError as e:
        print(f"命令执行出错: {e}")

# def split_text(text, n):
#     """
#     如果字符串长度大于n，将字符串分割为多个长度为n的段，并用换行符连接。
#     :param text: 输入的字符串
#     :param n: 每段字符串的长度
#     :return: 修改后的字符串
#     """
#     # 检查text的长度是否大于n
#     if len(text) > n:
#         # 使用列表推导式将text分割为多个长度为n的段
#         segments = [text[i:i+n] for i in range(0, len(text), n)]
#         # 使用换行符连接各段
#         return '\n'.join(segments)
#     else:
#         # 如果text的长度小于或等于n，直接返回原字符串
#         return text

def split_text(text, n, placeholder=' '):
    """
    如果字符串长度大于n，尽可能均匀地将字符串分割为多行，每行字符数尽可能一致。
    最后一行使用占位符居中。
    :param text: 输入的字符串
    :param n: 指定的最大行字符数
    :param placeholder: 用于填充的占位符，默认为空格
    :return: 修改后的字符串
    """
    text_length = len(text)
    if text_length <= n:
        # 如果文本长度小于等于n，直接居中返回
        padding = (n - text_length) // 2
        return f"{placeholder*padding}{text}{placeholder*padding}"

    # 计算行数
    lines = text_length // n + (1 if text_length % n else 0)
    
    # 计算每行实际的平均字符数
    avg_length_per_line = text_length // lines
    
    # 处理最后一行可能剩余的字符数
    extra_chars = text_length % lines
    
    # 开始分割文本
    segments = []
    start_index = 0
    for i in range(lines):
        end_index = start_index + avg_length_per_line + (1 if i < extra_chars else 0)
        segments.append(text[start_index:end_index])
        start_index = end_index

    # 对最后一行进行居中处理
    last_line = segments[-1]
    padding_length = (n - len(last_line)) // 2
    segments[-1] = f"{placeholder*padding_length}{last_line}{placeholder*padding_length}"

    return '\n'.join(segments)


def add_subtitles_to_video(video_with_audio_path, subtitle_tracks, final_video_path):
    drawtext_commands = []

    for subtitle in subtitle_tracks:
        start_time = subtitle["track_start"] / 1000  # 转换为秒
        end_time = subtitle["track_end"] / 1000

        font_path = subtitle["font_path"]
        font_size = 90  # 字号
        font_color = subtitle["text_color"].replace('#', '0x') + str(hex(int(subtitle["text_alpha"] * 255)))[2:]
        text = subtitle["text"]
        text = split_text(text, 10)
        # 初始化字幕命令
        drawtext_command = f"drawtext=fontfile='{font_path}':text='{text}':fontsize={font_size}:fontcolor={font_color}:x=(w-text_w)/2:y=h-(h*{0.30})-text_h:enable='between(t,{start_time},{end_time})'"

        # 如果设置了背景颜色，则添加背景框
        if subtitle.get("background_color"):
            background_color = subtitle["background_color"].replace('#', '0x') + str(hex(int(subtitle["background_alpha"] * 255)))[2:]
            drawtext_command += f":box=1:boxcolor={background_color}@{subtitle['background_alpha']}:boxborderw=0"

        # 如果设置了边框颜色，则添加边框
        if subtitle.get("border_color"):
            border_color = subtitle["border_color"].replace('#', '0x') + str(hex(int(subtitle["border_alpha"] * 255)))[2:]
            border_width = subtitle["border_width"]*font_size
            drawtext_command += f":bordercolor={border_color}:borderw={border_width}"

        drawtext_commands.append(drawtext_command)
        # print(drawtext_commands)
    # 组合所有字幕命令
    filter_complex_command = ','.join(drawtext_commands)

    # 构建ffmpeg命令
    ffmpeg_command = f"ffmpeg -y -i '{video_with_audio_path}' -vf \"{filter_complex_command}\" -c:a copy '{final_video_path}'"
    # print(ffmpeg_command)
    # 运行ffmpeg命令
    run_command(ffmpeg_command)

# 调用函数示例
# add_subtitles_to_video(video_with_audio_path, json_data["subtitle_track"], final_video_path)


