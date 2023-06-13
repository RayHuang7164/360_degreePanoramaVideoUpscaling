import cv2
import numpy as np

def gamma_correction(input_video_path, output_video_path, gamma):
    # 讀取影片
    cap = cv2.VideoCapture(input_video_path)

    # 檢查影片是否成功讀取
    if not cap.isOpened():
        print("無法讀取影片")
        return

    # 影片的寬度和高度
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # 輸出影片的設定
    output = cv2.VideoWriter(output_video_path, 
                             cv2.VideoWriter_fourcc(*'mp4v'), 
                             cap.get(cv2.CAP_PROP_FPS), 
                             (width, height))

    while True:
        # 讀取影格
        ret, frame = cap.read()

        # 影片結束
        if not ret:
            break

        # 將影格轉換為浮點數型態
        frame = frame.astype(float)

        # 正規化像素值到 0-1 範圍
        frame /= 255.0

        # 伽瑪校正
        frame = np.power(frame, gamma)

        # 將像素值重新調整為 0-255 範圍
        frame *= 255.0

        # 四捨五入到整數型態
        frame = np.round(frame)

        # 轉換為 8 位元無符號整數型態
        frame = frame.astype(np.uint8)

        # 寫入輸出影片
        output.write(frame)

        # 顯示處理後的影格
        cv2.imshow('Gamma Corrected Video', frame)

        # 按下 'q' 鍵退出迴圈
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # 釋放資源
    cap.release()
    output.release()
    cv2.destroyAllWindows()

fileName = "HarryPotter"
gamma = 2
gamma_correction(f"D:/Python/研究所/360_degreePanoramaVideoUpscaling/{fileName}.mp4", f"D:/Python/研究所/360_degreePanoramaVideoUpscaling/{fileName}_final_output.mp4", gamma)