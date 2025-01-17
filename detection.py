import cv2
import easyocr
from ultralytics import YOLO

from datetime import date

import util

class YOLODetector:
    def __init__(self, coco_model_path, np_model_path):
        self.coco_model = YOLO(coco_model_path)
        self.np_model = YOLO(np_model_path)
        self.reader = easyocr.Reader(['en'], gpu=False)
        
        self.saved_ids = set()
        self.plate_text_dict = {}
        self.last_track_id = 0

    
    def detect(self, frame, trigger):
        detections = self.coco_model.track(frame, persist=True, conf=0.5, classes=[2])[0]
        for detection in detections.boxes.data.tolist():

            if len(detection) == 7:
                x1, y1, x2, y2, track_id, score, _ = detection
                self.last_track_id = track_id
            else:
                x1, y1, x2, y2, score, _ = detection
                track_id = self.last_track_id + 1

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
                            # _, plate_treshold = cv2.threshold(plate_gray, 64, 255, cv2.THRESH_BINARY_INV)
                            np_text, np_score = util.read_license_plate(reader=self.reader, image=plate_gray)

                            vehicle_bbox = f"{x1},{y1},{x2},{y2}"
                            vehicle_bbox_score = score

                            plate_bbox = f"{plate_x1},{plate_y1},{plate_x2},{plate_y2}"
                            plate_bbox_score = plate_score

                            text_plate = np_text
                            text_plate_score = np_score

                            keterangan = "Keterangan" # Example

                            util.write_csv('result/vehicle_data.csv', int(track_id), 
                                      vehicle_bbox, vehicle_bbox_score, 
                                      plate_bbox, plate_bbox_score,
                                      text_plate, text_plate_score, 
                                      date.today(), keterangan)

                            # cv2.imwrite('result/' + str(track_id) + '_car.jpg', roi)
                            # cv2.imwrite('result/' + str(track_id) + '_plate.jpg', plate)
                            # cv2.imwrite('result/' + str(track_id) + '_plate_gray.jpg', plate_gray)
                            # cv2.imwrite('result/' + str(track_id) + '_plate_threshold.jpg', plate_treshold)
                            
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