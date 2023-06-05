import cv2

# 加载视频文件
video = cv2.VideoCapture('20230502_000403.mp4')

# 检查视频是否成功打开
if not video.isOpened():
    print('视频无法打开')
    exit()

# 获取视频的宽度和高度
width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))

# 创建一个VideoWriter对象，用于保存处理后的视频
out = cv2.VideoWriter('output.mp4', cv2.VideoWriter_fourcc(*'mp4v'), 25, (width, height))

# 循环遍历视频的每一帧
while video.isOpened():
    ret, frame = video.read()

    # 如果读取到了视频帧，就进行处理
    if ret:
        # 在此处添加你的图像处理代码
        # 例如，将图像转换为灰度图像
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # 将处理后的帧写入输出视频
        out.write(gray_frame)

        # 显示处理后的帧（可选）
        cv2.imshow('frame', gray_frame)
        
        # 按下q键退出
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

# 清理资源
video.release()
out.release()
cv2.destroyAllWindows()
