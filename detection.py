import cv2
from ultralytics import YOLO

class YOLODetector:
    def __init__(self, coco_model_path):
        self.coco_model = YOLO(coco_model_path)

    def detect(self, frame):
        detections = self.coco_model.track(frame, persist=True, conf=0.5, classes=[2])[0]
        for detection in detections.boxes.data.tolist():
            x1, y1, x2, y2, track_id, score, _ = detection
            
            # Gambar bounding box kendaraan
            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (255, 0, 0), 2)
            cv2.putText(frame, f'Car ID: {track_id}', (int(x1), int(y1 - 30)), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
