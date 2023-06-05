#1.導入必要的庫：導入NumPy、OpenCV和其他需要的庫。
import numpy as np
import cv2


fileName = "VID_20230510_203409_00_005"
video_path = f"D:/Python/{fileName}.mp4"


#2.讀取全景視頻：使用OpenCV庫的cv2.VideoCapture()函數讀取全景視頻。
video = cv2.VideoCapture(video_path)

# 获取视频的帧率、宽度和高度
fps = int(video.get(cv2.CAP_PROP_FPS))
width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))

#3.逐幀處理視頻：使用循環逐幀讀取視頻，並對每一幀進行處理。
while video.isOpened():
    ret, frame = video.read()
    if not ret:
        break
    


#4.圖像增強算法：選擇適當的圖像增強算法對每一幀進行提升。這可以包括超分辨率、去噪、對比度增強等。
#我们选择了邻域直径 d 为 9，颜色空间滤波器的标准差 sigmaColor 和坐标空间滤波器的标准差 sigmaSpace 均为 75。
# 示例：使用OpenCV的双边滤波进行去噪
#denoised_frame = cv2.bilateralFilter(frame, 9, 75, 75)
denoised_frame = video

#5.重建全景圖像：由於全景圖像是環形的，需要將處理後的幀重新映射到全景圖像上。
# 定义映射关系，这里使用一张相同尺寸的全黑图像作为映射关系
map_x = np.zeros(denoised_frame.shape[:2], np.float32)
map_y = np.zeros(denoised_frame.shape[:2], np.float32)

# 遍历每个像素，并进行映射
for i in range(denoised_frame.shape[0]):
    for j in range(denoised_frame.shape[1]):
        # 映射到新的位置
        map_x[i, j] = j
        map_y[i, j] = i

# 示例：使用极坐标映射将帧重建到全景图像
reconstructed_frame = cv2.remap(denoised_frame, map_x, map_y, interpolation=cv2.INTER_LINEAR)

# 创建一个VideoWriter对象，用于保存放大后的视频
fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # 转换为MP4格式
out = cv2.VideoWriter(f"D:/Python/{fileName}_Out.mp4", fourcc, fps, (width*2, height*2))

#6.顯示和保存處理後的視頻：使用OpenCV庫的cv2.imshow()函數在窗口中顯示處理後的視頻幀，並使用cv2.imwrite()函數保存處理後的視頻。
cv2.imshow('Upscaled Video', reconstructed_frame)
out.write(reconstructed_frame)

#7.清理：在程序結束時釋放資源。
video.release()
out.release()
cv2.destroyAllWindows()
