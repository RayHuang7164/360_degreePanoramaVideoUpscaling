import cv2

fileName = 'Taiwan_720p'

# 加载视频文件 cv2.resize()
video = cv2.VideoCapture(fileName + '.mp4')

# 检查视频是否成功打开
if not video.isOpened():
    print('视频无法打开')
    exit()

# 获取视频的帧率、宽度和高度
fps = int(video.get(cv2.CAP_PROP_FPS))
width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))

# 设置放大比例
scale = 2  # 放大两倍

# 计算放大后的宽度和高度
new_width = int(width * scale)
new_height = int(height * scale)

# 创建一个VideoWriter对象，用于保存放大后的视频
fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # 转换为MP4格式
out = cv2.VideoWriter(fileName + '_output.mp4', fourcc, fps, (new_width, new_height))

# 循环遍历视频的每一帧
while video.isOpened():
    ret, frame = video.read()

    # 如果读取到了视频帧，就将其放大并写入输出视频
    if ret:
        resized_frame = cv2.resize(frame, (new_width, new_height))
        out.write(resized_frame)
    else:
        break

# 清理资源
video.release()
out.release()
#cv2.destroyAllWindows()
