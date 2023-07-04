import cv2
import numpy as np

def adjust_gamma(image, gamma):
    # 建立Gamma校正的查詢表
    inv_gamma = 1.0 / gamma
    table = np.array([((i / 255.0) ** inv_gamma) * 255 for i in np.arange(0, 256)]).astype(np.uint8)
    
    # 使用查詢表對影像進行Gamma校正
    return cv2.LUT(image, table)


# 設定輸入和輸出檔案路徑
folder_path = "d:/Python/source video/"
filename = "low"

video_path = folder_path + filename + ".mp4"
output_path = folder_path + "output.mp4"
# 讀取影片
cap = cv2.VideoCapture(video_path)

# 建立寫入影片的物件
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = cap.get(cv2.CAP_PROP_FPS)

fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height))

# 調整Gamma值的閾值（可根據需要調整）
gamma_threshold = 100

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # 將影格轉換為灰度圖
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # 計算影格的平均亮度
    mean_brightness = np.mean(gray_frame)

    # 判斷是否需要調整Gamma值
    if mean_brightness < gamma_threshold:
        # 如果亮度過暗，進行Gamma校正
        gamma = 0.5
        adjusted_frame = adjust_gamma(frame, gamma)
    else:
        # 否則保持原始影格
        adjusted_frame = frame

    # 寫入調整後的影格
    out.write(adjusted_frame)

    # 顯示調整前後的影格（可選）
    cv2.imshow('Original', frame)
    cv2.imshow('Adjusted', adjusted_frame)

    # 按下 'q' 鍵結束迴圈
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 釋放物件與關閉視窗
cap.release()
out.release()
cv2.destroyAllWindows()
