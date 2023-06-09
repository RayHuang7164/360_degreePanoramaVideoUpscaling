import cv2
import moviepy.editor as mp
import numpy as np
from pydub import AudioSegment

# 設定輸入和輸出檔案路徑
folder_path = "c:/Python/source video/"
filename = "Low"
input_file = folder_path + filename + ".mp4"
output_file = folder_path + "output.mp4"
final_output_file = folder_path + filename + "_final_output.mp4"

# 定義調整參數
gamma = 0.5  # Gamma 調整參數

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

print(f'原始帧数: {total_frames}')
print(f'原始寬度: {width}')
print(f'原始高度: {height}')

# 創建一個 VideoWriter 對象，用於保存提升帧后的影片
fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # 轉換為 MP4 格式
out = cv2.VideoWriter(output_file, fourcc, fps, (width, height))

# 循環遍歷影片的每一帧
while video.isOpened():
    ret, frame = video.read()

    if ret:
        # Gamma 調整
        gamma_frame = np.power(frame / 255.0, gamma)
        adjusted_frame = np.round(gamma_frame * 255.0).astype(np.uint8)

        # 寫入調整帧後的影片
        out.write(adjusted_frame)

        # 顯示處理進度
        frame_count = int(video.get(cv2.CAP_PROP_POS_FRAMES))
        print(f'已處理 {frame_count} 帧 / 總帧数 {total_frames}')

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