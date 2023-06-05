import cv2

# 打开全景视频
# 示例用法
fileName = "VID_20230510_203409_00_005"

#video = cv2.VideoCapture(f"C:/Python/Video_Python/{fileName}.mp4")
video = cv2.VideoCapture(f"D:/Python/{fileName}.mp4")

# 获取原始视频的宽度和高度
width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))

# 定义调整后的宽度和高度
new_width = 7680 #12288 
new_height = 4320 #6480 

# 创建输出视频的写入器
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
#output_video = cv2.VideoWriter(f"C:/Python/Video_Python/{fileName}_output_OPENCV.mp4", fourcc, 30.0, (new_width, new_height))
output_video = cv2.VideoWriter(f"D:/Python/{fileName}_output_OPENCV.mp4", fourcc, 30.0, (new_width, new_height))

while True:
    # 读取一帧视频
    ret, frame = video.read()
    if not ret:
        break
    
    # 调整帧的大小
    resized_frame = cv2.resize(frame, (new_width, new_height))
    
    # 写入调整后的帧到输出视频
    output_video.write(resized_frame)
    
    # 显示调整后的帧
    cv2.imshow('Upscaled Frame', resized_frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 释放资源
video.release()
output_video.release()
cv2.destroyAllWindows()
