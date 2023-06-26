import cv2
import moviepy.editor as mp
import numpy as np
from pydub import AudioSegment

# 設置輸入文件和輸出文件路徑
folder_path = "D:/Python/source video/"
filename = "Low"
input_file = folder_path + filename + ".mp4" 
output_file = folder_path + "output.mp4"
final_output_file = folder_path + filename + "_final_output.mp4"

# 定義調整參數
alpha = 1.5  # 亮度調整係數
beta = 20  # 亮度調整偏移量
threshold = 0.5  # 閾值，用於判斷亮度是否過暗或過亮
new_width = 5760
new_height = 2880
kernel_size = (5, 5)  # 高斯濾波器的內核大小

# 加載視頻
video = cv2.VideoCapture(input_file)

# 檢查視頻是否成功打開
if not video.isOpened():
    print('無法打開視頻')
    exit()

# 獲取視頻的帧速率
sourse_fps = int(video.get(cv2.CAP_PROP_FPS))

 # 提高帧速率
if (sourse_fps > 120):
    new_fps = 120  # 设置新的帧速率
    video.set(cv2.CAP_PROP_FPS, new_fps)
    fps = int(video.get(cv2.CAP_PROP_FPS))
else:
    fps = sourse_fps


# 獲取視頻的寬度和高度
width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))

# 創建一個VideoWriter對象，用於保存處理後的視頻
fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # 轉換為MP4格式
out = cv2.VideoWriter(output_file, fourcc, new_fps, (new_width, new_height))

# 循環遍歷視頻的每一幀
while video.isOpened():
    ret, frame = video.read()

    if ret:
        # 影像縮放
        resized_frame = cv2.resize(frame, (new_width, new_height), interpolation=cv2.INTER_LANCZOS4)

        # 減少噪點
        blurred_frame = cv2.GaussianBlur(resized_frame, kernel_size, 0)

        # 亮度調整
        frame_normalized = blurred_frame.astype(float) / 255.0
        frame_gamma = np.power(frame_normalized, 2) * 255.0
        frame_gamma = np.round(frame_gamma).astype(np.uint8)

        # 判斷亮度並進行調整
        mean = cv2.mean(frame_gamma)[0] / 255
        std = cv2.meanStdDev(frame_gamma)[1][0][0] / 255
        if mean < threshold or mean + std < threshold:
            adjusted_frame = cv2.convertScaleAbs(frame_gamma, alpha=alpha, beta=beta)
        else:
            adjusted_frame = frame_gamma

        # 寫入輸出視頻
        out.write(adjusted_frame)

        # 顯示處理進度
        print(f'Processed {video.get(cv2.CAP_PROP_POS_FRAMES)} frames of {total_frames}')
    else:
        break

# 釋放資源
video.release()
out.release()

# 加載音頻
video_with_audio = mp.VideoFileClip(input_file)
audio = video_with_audio.audio
audio_segment = AudioSegment.from_file(audio.fps, audio.nchannels, audio.sample_width, audio.raw_data, audio.frame_rate)
audio_segment = audio_segment.set_frame_rate(44100)
modified_audio = mp.AudioFileClip(audio_segment)

# 合併處理後的視頻和音頻
final_video = mp.VideoFileClip(output_file).set_audio(modified_audio)
final_video.write_videofile(final_output_file)
final_video.close()
video_with_audio.close()
