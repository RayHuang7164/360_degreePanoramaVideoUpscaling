import cv2
from PIL import Image
import numpy as np
import subprocess

def upscale_panorama_video(video_path, scale_factor):
    # 打開視訊
    video = cv2.VideoCapture(video_path)

    # 獲取視訊帧率和尺寸
    fps = video.get(cv2.CAP_PROP_FPS)
    width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
 
    # 計算放大後的影片尺寸
    new_width = 7680 #12288
    new_height = 4320 #6480 

    # 使用 FFmpeg 放大影片
    output_path = {fileName} + "_FFOutput.mp4"
    #ffmpeg_command = f'ffmpeg -i "{video_path}" -vf "scale={new_width}:{new_height}" -c:v libx264 -crf 23 -c:a aac -b:a 128k "{output_path}"'
    # ffmpeg -i VID_20230510_203409_00_005.mp4 -vf "scale=7680:4320" -c:v libx265 -crf 18 -preset slow output_8K_panorama_video.mp4
    ffmpeg_command = f'ffmpeg -i "{video_path} + .mp4" -vf "scale={new_width}:{new_height}" -c:v libx265 -crf 18 -preset slow "{output_path}"'
    subprocess.call(ffmpeg_command, shell=True)

   
    # 釋放資源
    video.release()


# 示例用法 C:/Python/Video_Python/
fileName = "VID_20230510_203409_00_005"
video_path = f"D:/Python/{fileName}"
scale_factor = 2
upscale_panorama_video(video_path, scale_factor)
