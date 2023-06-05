import cv2
from PIL import Image
import numpy as np

def upscale_panorama_video(video_path, scale_factor):
    # 打開影片
    video = cv2.VideoCapture(video_path)

    # 獲取影片帧率和尺寸
    fps = video.get(cv2.CAP_PROP_FPS)
    width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
    total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))

    # 創建新的影片編寫器
    output_path = f"D:/Python/{fileName}_Output.mp4"
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")   #mp4v
    out = cv2.VideoWriter(output_path, fourcc, fps, (width*scale_factor, height*scale_factor))

    while True:
        ret, frame = video.read()
        if not ret:
            break

        # 將影格轉換為PIL圖像
        image = Image.fromarray(frame)

        # 將圖像進行放大
        upscaled_image = image.resize((width*scale_factor, height*scale_factor), Image.LANCZOS)

        # 將圖像轉換回影格
        upscaled_frame = cv2.cvtColor(np.array(upscaled_image), cv2.COLOR_RGB2BGR)

        # 將影格寫入輸出影片
        out.write(upscaled_frame)

        # 显示当前处理进度
        print(f'Processed {video.get(cv2.CAP_PROP_POS_FRAMES)} frames of {total_frames}')

    # 釋放資源
    video.release()
    out.release()



# 示例用法
fileName = "VID_20230510_203409_00_005"
video_path = f"D:/Python/{fileName}.mp4"
scale_factor = 2
upscale_panorama_video(video_path, scale_factor)
