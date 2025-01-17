import tkinter as tk

from border import border_frame
from Header import create_text_frame
from Webcam import VideoPlayer
from Excel import load_csv_data
from detection import YOLODetector

# Create the main application window using tkinter
root = tk.Tk()
root.title("Ganjil Genap Application")
root.state('zoomed')
root.configure(bg="#CACFCB")

# Menggunakan fungsi untuk membuat frame dengan border
frame1 = border_frame(root, relx=0.0145, rely=0.02, relwidth=0.625, relheight=None)
create_text_frame(frame1)

frame2 = border_frame(root, relx=0.65, rely=0.02, relwidth=0.34, relheight=0.955)
load_csv_data(frame=frame2, file_path="result/vehicle_data.csv")

# untuk video player frame
video_path = 'Notebook/video/traffic.mp4'
yolo_detector = YOLODetector(coco_model_path="Detection/model/yolov8n.pt",
                             np_model_path="Detection/model/license_plate_detector.pt")
video_player = VideoPlayer(root, video_path=video_path, detector=yolo_detector, zoom_percent=75, margin=20)
video_player.start(trigger_line=True, line_start=(0, int(720-200)), line_end=(int(1280), int(720-200)))
# video_player.start(trigger_line=True, line_start=(0, int(1080-100)), line_end=(int(1920), int(1080-100)))

root.mainloop()
video_player.release()