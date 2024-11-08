import cv2
import easyocr
from ultralytics import YOLO

class YOLODetector:
    def __init__(self, coco_model_path, np_model_path):
        self.coco_model = YOLO(coco_model_path)
        self.np_model = YOLO(np_model_path)
        self.reader = easyocr.Reader(['en'], gpu=False)
        
        self.saved_ids = set()
        self.plate_text_dict = {}

    def read_license_plate(self, reader, image):
        detections = reader.readtext(image)
        for detection in detections:
            bbox, text, score = detection
            text = text.upper().replace(' ', '')
            return text, score
        return None, None

    def detect(self, frame, trigger):
        detections = self.coco_model.track(frame, persist=True, conf=0.5, classes=[2])[0]
        for detection in detections.boxes.data.tolist():
            x1, y1, x2, y2, track_id, score, _ = detection

            if y2 > trigger:
                vehicle_bounding_boxes = []
                vehicle_bounding_boxes.append([x1, y1, x2, y2, track_id, score])

                # Ambil gambar kendaraan
                for x1, y1, x2, y2, track_id, score in vehicle_bounding_boxes:
                    roi = frame[int(y1):int(y2), int(x1):int(x2)]

                    # Deteksi plat
                    license_plates = self.np_model(roi)[0] # Detektor plat dari roi (image kendaraan)

                    for license_plate in license_plates.boxes.data.tolist():
                        plate_x1, plate_y1, plate_x2, plate_y2, plate_score, _ = license_plate
                        
                        if track_id not in self.saved_ids: # not to save the same image
                            plate = roi[int(plate_y1):int(plate_y2), int(plate_x1):int(plate_x2)]
                            plate_gray = cv2.cvtColor(plate, cv2.COLOR_BGR2GRAY)
                            np_text, np_score = self.read_license_plate(reader=self.reader, image=plate_gray)

                            text_plate = np_text
                            
                            self.saved_ids.add(track_id)
                            self.plate_text_dict[track_id] = text_plate

                # Gambar bounding box kendaraan
                cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (255, 0, 0), 2)
                cv2.putText(frame, f'Car ID: {track_id}', (int(x1), int(y1 - 30)), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
                
                if track_id in self.plate_text_dict: # ambil text_plate dari dictionary plate_text_dict
                    cv2.putText(frame, f'Text Plate: {self.plate_text_dict[track_id]}', (int(x1), int(y1 - 10)),  
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
                else: # jika text_plate belum ada di dictionary, gunakan nilai terbaru
                    cv2.putText(frame, 'Text Plate: Not Detected', (int(x1), int(y1 - 10)),  
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)