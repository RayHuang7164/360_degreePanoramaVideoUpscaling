import cv2
import moviepy.editor as mp
import numpy as np

# 設定輸入和輸出檔案路徑
folder_path = "c:/Python/source video/"
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
frame_increase = 2  # 帧数提高倍数

# 載入影片
video = cv2.VideoCapture(input_file)

# 檢查影片是否成功打開
if not video.isOpened():
    print('無法打開影片')
    exit()

# 獲取影片的寬度、高度和幀率
width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = int(video.get(cv2.CAP_PROP_FPS))
total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))

# 計算新的目標帧数和帧間隔
new_total_frames = total_frames * frame_increase
frame_interval = int(round(1 / frame_increase))

print(f'原始帧数: {total_frames}')
print(f'原始寬度: {width}')
print(f'原始高度: {height}')
print(f'目標帧数: {new_total_frames}')
print(f'帧間隔: {frame_interval}')

# 創建一個 VideoWriter 對象，用於保存提升帧后的影片
fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # 轉換為 MP4 格式
out = cv2.VideoWriter(output_file, fourcc, fps, (new_width, new_height))

# 循環遍歷影片的每一帧
frame_count = 0
frame_multiplier = 0
while True:
    ret, frame = video.read()

    if ret:
        # 圖像縮放
        resized_frame = cv2.resize(frame, (new_width, new_height), interpolation=cv2.INTER_LANCZOS4)

        # 減少噪點
        blurred_frame = cv2.GaussianBlur(resized_frame, (5, 5), 0)

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

        # 寫入提升帧后的影片
        out.write(adjusted_frame)

        # 顯示處理進度
        print(f'已處理 {frame_count + 1} 帧 / 總帧数 {new_total_frames}')
        frame_count += 1

        # 檢查是否已處理完畢所有原始帧
        if frame_multiplier == frame_increase - 1:
            frame_multiplier = 0
            frame_count += frame_interval
        else:
            frame_multiplier += 1
    else:
        break

# 釋放資源
video.release()
out.release()

# 加載聲音
video_with_audio = mp.VideoFileClip(input_file)

# 读取原始视频中的音频
audio = video_with_audio.audio

# 创建一个新的视频文件，将处理后的视频和原始音频合并
final_video = mp.VideoFileClip(output_file).set_audio(audio)

# 保存最终的视频文件
final_video.write_videofile(final_output_file, codec='libx264')

# 清理资源
final_video.close()
video_with_audio.close()