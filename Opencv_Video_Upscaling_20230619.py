import cv2
import moviepy.editor as mp


# 設置輸入文件和輸出文件路徑
folder_path = "C:/Python/source video/"
filename = "low"
input_file = folder_path + filename + ".mp4" 
temp_file = folder_path + "temp.mp4"
output_file = folder_path + "output.mp4"
resized_file = folder_path + "resized.mp4"
final_output_file = folder_path + filename + "_final_output.mp4"

# 定義調整參數
alpha = 1.5  # 亮度調整係數
beta = 20  # 亮度調整偏移量
threshold = 0.5  # 閾值，用於判斷亮度是否過暗或過亮
new_width = 5760 #7680 # 新的寬度
new_height = 2880 #4320  # 新的高度
kernel_size = (5, 5)  # 高斯濾波器的內核大小     

#取得影片
video1 = cv2.VideoCapture(input_file)

# 檢查視頻是否成功打開
if not video1.isOpened():
    print('视频无法打开')
    exit()

# 獲取視頻的幀率、寬度和高度
fps1 = int(video1.get(cv2.CAP_PROP_FPS))
width1 = int(video1.get(cv2.CAP_PROP_FRAME_WIDTH))
height1 = int(video1.get(cv2.CAP_PROP_FRAME_HEIGHT))
total_frames1 = int(video1.get(cv2.CAP_PROP_FRAME_COUNT))

#region Description ==提高幀率又不改變影片撥放==
newfps = cv2.VideoWriter(temp_file, cv2.VideoWriter_fourcc(*'mp4v'), 120, (width1, height1)) #提高幀率120fps
while True:
    ret, frame = video1.read()

    if not ret:
        break
    # 將每個幀重複 n 次，以增加幀數
    n = int(round(120 / fps1))
    for _ in range(n):
        newfps.write(frame) 
     
#endregion 

#取得影片
video = cv2.VideoCapture(temp_file)

# 獲取視頻的幀率、寬度和高度
fps = int(video.get(cv2.CAP_PROP_FPS))
width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))

# 創建一個VideoWriter對象，用於保存處理後的視頻
fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # 转换为MP4格式
out = cv2.VideoWriter(output_file, fourcc, fps, (new_width, new_height))

# 循環遍歷視頻的每一幀
while video.isOpened():
    ret, frame = video.read()  #frame 是第一個變數

    if ret:
        #放大尺寸
        blurred = cv2.resize(frame, (new_width, new_height), interpolation=cv2.INTER_CUBIC)  
        #resized_frame = cv2.resize(frame, (new_width, new_height),interpolation=cv2.INTER_LANCZOS4)
        
        #region Description ==调整影片的亮度==
        # 計算當前幀的像素值分佈情況
        hist = cv2.calcHist([blurred], [0], None, [256], [0, 256])
        hist_norm = hist.ravel() / hist.sum()

        # 計算當前幀的平均像素值和標準差
        mean = cv2.mean(blurred)[0]
        std = cv2.meanStdDev(blurred)[1][0][0]

        # 判斷當前幀的亮度是否過暗或過亮
        if mean / 255 < threshold or mean / 255 + std / 255 < threshold:
        # 進行亮度調整
            frame_adjusted = cv2.convertScaleAbs(blurred, alpha=alpha, beta=beta)
        else:
            frame_adjusted = blurred
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
# 加載原始視頻文件
video_with_audio = mp.VideoFileClip(input_file)
#取得影片
video = cv2.VideoCapture(input_file)
# 讀取原始視頻中的音頻
audio = video_with_audio.audio
# 創建一個新的視頻文件，將處理後的視頻和原始音頻合併
final_video = mp.VideoFileClip(output_file).set_audio(audio)
# 保存最終的視頻文件
final_video.write_videofile(final_output_file)
# 清理资源

final_video.close()
video_with_audio.close()
#endregion   


