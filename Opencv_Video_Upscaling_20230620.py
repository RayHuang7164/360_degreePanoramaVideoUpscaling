import cv2
import moviepy.editor as mp
import numpy as np

# 設置輸入文件和輸出文件路徑
folder_path = "D:/Python/source video/"
filename = "Low"
input_file = folder_path + filename + ".mp4" 
temp_file = folder_path + "temp.mp4"
output_file = folder_path + "output.mp4"
#resized_file = folder_path + "resized.mp4"
final_output_file = folder_path + filename + "_final_output.mp4"

# 定義調整參數
alpha = 1.5  # 亮度調整係數
beta = 20  # 亮度調整偏移量
threshold = 0.5  # 閾值，用於判斷亮度是否過暗或過亮
new_width = 5760 #7680 # 新的寬度
new_height = 2880 #4320  # 新的高度
kernel_size = (5, 5)  # 高斯濾波器的內核大小     

#取得影片
video = cv2.VideoCapture(input_file)

# 檢查視頻是否成功打開
if not video.isOpened():
    print('视频无法打开')
    exit()


#region increase_frame_rate ==提高帧速率==
new_fps = 60  # 设置新的帧速率
video.set(cv2.CAP_PROP_FPS, new_fps)
fps = int(video.get(cv2.CAP_PROP_FPS))  # 更新fps变量

# 獲取視頻的幀率、寬度和高度
width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))

# 創建一個VideoWriter對象，用於保存處理後的視頻
fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # 转换为MP4格式
out = cv2.VideoWriter(output_file, fourcc, new_fps, (new_width, new_height))
#endregion 

# 循環遍歷視頻的每一幀
while video.isOpened():
    ret, frame = video.read()  #frame 是第一個變數

    if ret:
        #放大尺寸
        #resized_frame = cv2.resize(frame, (new_width, new_height), interpolation=cv2.INTER_CUBIC)  
        resized_frame = cv2.resize(frame, (new_width, new_height),interpolation=cv2.INTER_LANCZOS4)
        
        
        #region reduce_noise ==高斯濾波器減少視頻的噪點==
        frame_gamma = cv2.GaussianBlur(resized_frame, kernel_size, 0)
        #endregion 
        
        # #region  ==Gamma Correction==
        # # 將影格轉換為浮點數型態
        # resized_frame = blurred_frame.astype(float)
        # # 正規化像素值到 0-1 範圍 
        # # 每個像素值都會除以 255.0，從而將它們正規化為 0 到 1 之間的小數值。
        # # 這樣做可以將像素值縮放到一個固定的範圍，方便後續的處理和運算
        # resized_frame /= 255.0
        # # 伽瑪校正
        # resized_frame = np.power(resized_frame, 2) #gamma
        # # 將像素值重新調整為 0-255 範圍
        # resized_frame *= 255.0
        # # 四捨五入到整數型態
        # resized_frame = np.round(resized_frame)
        # # 轉換為 8 位元無符號整數型態
        # frame_gamma = resized_frame.astype(np.uint8)
        # #endregion 
        
        
        #region adjust_brightness ==调整影片的亮度==
        # 計算當前幀的像素值分佈情況
        hist = cv2.calcHist([frame_gamma], [0], None, [256], [0, 256])
        hist_norm = hist.ravel() / hist.sum()
        # 計算當前幀的平均像素值和標準差
        mean = cv2.mean(frame_gamma)[0]
        std = cv2.meanStdDev(frame_gamma)[1][0][0]
        # 判斷當前幀的亮度是否過暗或過亮
        if mean / 255 < threshold or mean / 255 + std / 255 < threshold:
        # 進行亮度調整
            frame_adjusted = cv2.convertScaleAbs(frame_gamma, alpha=alpha, beta=beta)
        else:
            frame_adjusted = frame_gamma
        #endregion                  
    else:
        break
    
    # 寫入輸出視頻
    out.write(frame_adjusted)

    # 顯示當前處理進度
    print(f'Processed {video.get(cv2.CAP_PROP_POS_FRAMES)} frames of {total_frames}')

# 清理資源
video.release()
out.release()

#region Description ==加載聲音==
video_with_audio = mp.VideoFileClip(input_file)     # 加載原始視頻文件
#video = cv2.VideoCapture(input_file)                # 取得影片
audio = video_with_audio.audio                      # 讀取原始視頻中的音頻
final_video = mp.VideoFileClip(output_file).set_audio(audio)    # 創建一個新的視頻文件，將處理後的視頻和原始音頻合併
final_video.write_videofile(final_output_file)      # 保存最終的視頻文件
final_video.close()                                 # 關閉最簡單的視頻文件
video_with_audio.close()                            # 清理资源
#endregion   


