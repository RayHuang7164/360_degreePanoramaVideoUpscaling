import cv2
import moviepy.editor as mp
import numpy as np
from pydub import AudioSegment

# 设置输入文件和输出文件路径
folder_path = "D:/Python/source video/"
filename = "Low"
input_file = folder_path + filename + ".mp4"
output_file = folder_path + "output.mp4"
final_output_file = folder_path + filename + "_final_output.mp4"

# 定义调整参数
alpha = 1.5  # 亮度调整系数
beta = 20  # 亮度调整偏移量
threshold = 0.5  # 阈值，用于判断亮度是否过暗或过亮
new_width = 5760
new_height = 2880
frame_increase = 1  # 帧数提高倍数

# 加载视频
video = cv2.VideoCapture(input_file)

# 检查视频是否成功打开
if not video.isOpened():
    print('无法打开视频')
    exit()

# 获取视频的宽度和高度
width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = int(video.get(cv2.CAP_PROP_FPS))
total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))

# 计算新的目标帧数和帧间隔
new_total_frames = total_frames * frame_increase
frame_interval = int(round(total_frames / new_total_frames))

print(f'原始帧数: {total_frames}')
print(f'原始宽度: {width}')
print(f'原始高度: {height}')
print(f'目标帧数: {new_total_frames}')
print(f'帧间隔: {frame_interval}')

# 创建一个VideoWriter对象，用于保存提升帧后的视频
fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # 转换为MP4格式
out = cv2.VideoWriter(output_file, fourcc, fps, (new_width, new_height))

# 循环遍历视频的每一帧
frame_count = 0
while video.isOpened():
    ret, frame = video.read()

    if ret:
        # 图像缩放
        resized_frame = cv2.resize(frame, (new_width, new_height), interpolation=cv2.INTER_LANCZOS4)

        # 减少噪点
        blurred_frame = cv2.GaussianBlur(resized_frame, (5, 5), 0)

        # 亮度调整
        frame_normalized = blurred_frame.astype(float) / 255.0
        frame_gamma = np.power(frame_normalized, 2) * 255.0
        frame_gamma = np.round(frame_gamma).astype(np.uint8)

        # 判断亮度并进行调整
        mean = cv2.mean(frame_gamma)[0] / 255
        std = cv2.meanStdDev(frame_gamma)[1][0][0] / 255
        if mean < threshold or mean + std < threshold:
            adjusted_frame = cv2.convertScaleAbs(frame_gamma, alpha=alpha, beta=beta)
        else:
            adjusted_frame = frame_gamma

        # 写入提升帧后的视频
        for _ in range(frame_increase):
            out.write(adjusted_frame)

        # 显示处理进度
        print(f'Processed {frame_count + 1} frames of {new_total_frames}')
        frame_count += 1

        # 跳过帧间隔
        video.set(cv2.CAP_PROP_POS_FRAMES, frame_count * frame_interval)
    else:
        break

# 释放资源
video.release()
out.release()

# 加载音频
video_with_audio = mp.VideoFileClip(input_file)
audio = video_with_audio.audio
audio_segment = audio.to_soundarray(fps=44100)
modified_audio = AudioSegment(audio_segment.tobytes(), frame_rate=44100, channels=audio_segment.shape[1])

# 合并提升帧后的视频和音频
final_video = mp.VideoFileClip(output_file).set_audio(modified_audio)
final_video.write_videofile(final_output_file, fps=fps)
final_video.close()
video_with_audio.close()
