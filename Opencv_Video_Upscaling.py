import cv2
import moviepy.editor as mp

# 加载视频文件 cv2.resize()
fileName = "HarryPotter"
#video = cv2.VideoCapture(f"C:/Python/Video_Python/{fileName}.mp4")
video = cv2.VideoCapture(f"D:/Python/研究所/360_degreePanoramaVideoUpscaling/{fileName}.mp4")

# 检查视频是否成功打开
if not video.isOpened():
    print('视频无法打开')
    exit()

# 获取视频的帧率、宽度和高度
fps = int(video.get(cv2.CAP_PROP_FPS))
width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))


# 定義8K影像畫質
new_width = 5760 #7680
new_height = 2880 #4320

# 创建一个VideoWriter对象，用于保存处理后的视频
fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # 转换为MP4格式
out = cv2.VideoWriter(f"D:/Python/研究所/360_degreePanoramaVideoUpscaling/output.mp4", fourcc, fps, (new_width, new_height))


# 设置调整参数
alpha = 1.5  # 亮度调整系数
beta = 20  # 亮度调整偏移量
threshold = 0.5  # 阈值，用于判断亮度是否过暗或过亮

# 循环遍历视频的每一帧
while video.isOpened():
    ret, frame = video.read()

    # 如果读取到了视频帧，就将其放大并写入输出视频
    if ret:
        #雙立方內插法(Bicubic interpolation)放大尺寸
        blurred = cv2.resize(frame, (new_width, new_height), interpolation=cv2.INTER_CUBIC)  
        #resized_frame

        # 使用高斯濾波器減少噪點
        #blurred = cv2.GaussianBlur(resized_frame, (5, 5), 0)
        #out.write(blurred)
     
        # 使用高斯后的图像，计算其目标位置# 进行去除交错
        # resized_frame_1 = cv2.deinterlace(resized_frame, 1)


        # 计算当前帧的像素值分布情况
        hist = cv2.calcHist([blurred], [0], None, [256], [0, 256])
        hist_norm = hist.ravel() / hist.sum()

        # 计算当前帧的平均像素值和标准差
        mean = cv2.mean(blurred)[0]
        std = cv2.meanStdDev(blurred)[1][0][0]

        # 判断当前帧的亮度是否过暗或过亮
        if mean / 255 < threshold or mean / 255 + std / 255 < threshold:
        # 进行亮度调整
            frame_adjusted = cv2.convertScaleAbs(blurred, alpha=alpha, beta=beta)
        else:
            frame_adjusted = blurred
    else:
        break

    # 写入输出视频
    out.write(frame_adjusted)

    # 显示当前处理进度
    print(f'Processed {video.get(cv2.CAP_PROP_POS_FRAMES)} frames of {total_frames}')



# 清理资源
video.release()
out.release()


#===================加載聲音=======================
# 加载原始视频文件
video_with_audio = mp.VideoFileClip(f"D:/Python/研究所/360_degreePanoramaVideoUpscaling/{fileName}.mp4")

video = cv2.VideoCapture(f"D:/Python/研究所/360_degreePanoramaVideoUpscaling/{fileName}.mp4")

# 读取原始视频中的音频
audio = video_with_audio.audio

# 创建一个新的视频文件，将处理后的视频和原始音频合并
final_video = mp.VideoFileClip(f"D:/Python/研究所/360_degreePanoramaVideoUpscaling/output.mp4").set_audio(audio)

# 保存最终的视频文件
final_video.write_videofile(f"D:/Python/研究所/360_degreePanoramaVideoUpscaling/{fileName}_final_output.mp4")

# 清理资源
final_video.close()
video_with_audio.close()



