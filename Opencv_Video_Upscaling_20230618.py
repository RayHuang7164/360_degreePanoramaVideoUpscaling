import cv2
import moviepy.editor as mp
#将视频文件调整为指定的宽度和高度。
def resize_video(input_file, output_file, new_width, new_height):
    video = cv2.VideoCapture(input_file)

    if not video.isOpened():
        print('视频无法打开')
        exit()

    fps = int(video.get(cv2.CAP_PROP_FPS))
    width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))

    total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))

    out = cv2.VideoWriter(output_file, cv2.VideoWriter_fourcc(*'mp4v'), fps, (new_width, new_height))

    frame_count = 0  # 初始化帧计数器

    while frame_count < total_frames:  # 使用帧计数器作为循环终止条件
        ret, frame = video.read()

        if ret:
            #resized_frame = cv2.resize(frame, (new_width, new_height),interpolation=cv2.INTER_CUBIC)
            resized_frame = cv2.resize(frame, (new_width, new_height),interpolation=cv2.INTER_LANCZOS4)
            out.write(resized_frame)
            
            frame_count += 1  # 每处理完一帧，帧计数器递增
        else:
            break

    video.release()
    out.release()

#调整视频的亮度。
def adjust_brightness(input_file, output_file, alpha, beta, threshold):
    video = cv2.VideoCapture(input_file)

    if not video.isOpened():
        print('视频无法打开')
        exit()

    fps = int(video.get(cv2.CAP_PROP_FPS))
    width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))

    total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))

    out = cv2.VideoWriter(output_file, cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))

    frame_count = 0  # 初始化帧计数器
    # 循环遍历视频的每一帧
    while frame_count < total_frames:  # 使用帧计数器作为循环终止条件
        ret, frame = video.read()

        # 计算当前帧的像素值分布情况
        hist = cv2.calcHist([frame], [0], None, [256], [0, 256])
        hist_norm = hist.ravel() / hist.sum()

        # 计算当前帧的平均像素值和标准差
        mean = cv2.mean(frame)[0]
        std = cv2.meanStdDev(frame)[1][0][0]

        if ret:
             # 判断当前帧的亮度是否过暗或过亮
            if mean / 255 < threshold or mean / 255 + std / 255 < threshold:
            # 进行亮度调整
                frame_adjusted = cv2.convertScaleAbs(frame, alpha=alpha, beta=beta)
            else:
                frame_adjusted = frame
            out.write(frame_adjusted)
            
            frame_count += 1  # 每处理完一帧，帧计数器递增
        else:
            break

    video.release()
    out.release()

#使用高斯滤波器减少视频的噪点。
def reduce_noise(input_file, output_file, kernel_size):
    video = cv2.VideoCapture(input_file)

    if not video.isOpened():
        print('视频无法打开')
        exit()

    fps = int(video.get(cv2.CAP_PROP_FPS))
    width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))

    total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))

    out = cv2.VideoWriter(output_file, cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))

    frame_count = 0  # 初始化帧计数器

    while frame_count < total_frames:  # 使用帧计数器作为循环终止条件
        ret, frame = video.read()

        if ret:
            blurred_frame = cv2.GaussianBlur(frame, kernel_size, 0)
            out.write(blurred_frame) 
            frame_count += 1  # 每处理完一帧，帧计数器递增

        else:
            break

    video.release()
    out.release()

#提高幀率又不改變影片撥放
def increase_frame_rate(input_file, output_file, target_fps):
    video = cv2.VideoCapture(input_file)

    if not video.isOpened():
        print('無法打開影片檔案')
        exit()

    original_fps = video.get(cv2.CAP_PROP_FPS)
    frame_count = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    original_width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    original_height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))

    output_width = original_width
    output_height = original_height
    output_fps = target_fps

    out = cv2.VideoWriter(output_file, cv2.VideoWriter_fourcc(*'mp4v'), output_fps, (output_width, output_height))

    while video.isOpened():
        ret, frame = video.read()

        if ret:
            # 將每個幀重複 n 次，以增加幀數
            n = int(round(output_fps / original_fps)) 
            for _ in range(n):
                out.write(frame)       
        else:    
            break  
    video.release()
    out.release()

#将处理后的视频与原始音频合并，并保存最终的视频文件。
def process_video_with_audio(input_file, output_file, final_output_file):
   # 加載原始影片檔案
    video_with_audio = mp.VideoFileClip(input_file)
    # 讀取原始影片中的音訊
    audio = video_with_audio.audio

    # 讀取處理後的影片
    #processed_video = mp.VideoFileClip(output_file)
    # 確保截取的原始影片和處理後的影片的持續時間相同
    #subclip = video_with_audio.subclip(0, processed_video.duration)
    #final_video = processed_video.set_audio(audio).set_duration(subclip.duration)
    
    # 根據處理後的影片的長度截取原始影片的部分範圍
    #subclip = video_with_audio.subclip(0, processed_video.duration)
    # 將處理後的影片與截取的原始影片進行合併
    #final_video = processed_video.set_audio(audio)

    # 读取原始视频中的音频
    audio = video_with_audio.audio

    # 创建一个新的视频文件，将处理后的视频和原始音频合并
    final_video = mp.VideoFileClip(output_file).set_audio(audio)

    # 保存最終的影片檔案
    #final_video.write_videofile(final_output_file, audio_codec='aac')
    final_video.write_videofile(final_output_file)

    # 釋放資源
    final_video.close()
    #processed_video.close()
    #subclip.close()
    video_with_audio.close()
    #video_with_audio = mp.VideoFileClip(input_file, audio=True, video=True, method='ffmpeg')



def main():
    # 设置输入文件和输出文件路径
    folder_path = "C:/Python/source video/"
    filename = "low"
    input_file = folder_path + filename + ".mp4" 
    temp_file = folder_path + "temp.mp4"
    output_file = folder_path + "output.mp4"
    resized_file = folder_path + "resized.mp4"
    final_output_file = folder_path + filename + "_final_output.mp4"

    # 定义调整参数
    alpha = 1.5  # 亮度调整系数cd
    beta = 20  # 亮度调整偏移量
    threshold = 0.5  # 阈值，用于判断亮度是否过暗或过亮
    new_width = 5760 #7680 # 新的宽度
    new_height = 2880 #4320  # 新的高度
    kernel_size = (5, 5)  # 高斯滤波器的内核大小

  
    print("提高幀率又不改變影片撥放速度") 
    increase_frame_rate(input_file, temp_file, 120) # 目標幀率

    #print("放大视频")
    #resize_video(input_file, resized_file, new_width, new_height)
    #resize_video(output_file, resized_file, new_width, new_height)
    
    #print("调整亮度") 
    #adjust_brightness(temp_file, output_file, alpha, beta, threshold)
    

    # print("减少噪点")
    # reduce_noise(resized_file, output_file, kernel_size)
    
    print("合并视频和音频")  
    process_video_with_audio(input_file, temp_file, final_output_file)




if __name__ == '__main__':
    main()
