import os
import csv
import tempfile
import shutil

def write_csv(file_path, track_id, vehicle_bbox, vehicle_bbox_score, plate_bbox, plate_bbox_score, text_plate, text_plate_score, date, keterangan):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, newline='')
    try:
        header = [
            'Track ID',
            'Vehicle BBOX', 'Vehicle BBOX Score',
            'Plate BBOX', 'plate_bbox_score',
            'Text Plate', 'text_plate_score',
            'Date', 'Keterangan']
        
        new_row = [track_id, 
                   vehicle_bbox, vehicle_bbox_score, 
                   plate_bbox, plate_bbox_score, 
                   text_plate, text_plate_score, 
                   date, keterangan]
        
        csv_writer = csv.writer(temp_file)
        csv_writer.writerow(header)
        csv_writer.writerow(new_row)

        # If original file exists, append existing data (excluding header)
        if os.path.exists(file_path):
            with open(file_path, 'r', newline='') as original_file:
                csv_reader = csv.reader(original_file)
                next(csv_reader)  # Skip header
                for row in csv_reader:
                    csv_writer.writerow(row)

        temp_file.close()
        shutil.move(temp_file.name, file_path) # Replace original file with temporary file

    except Exception as e:
        print(f"Error writing to CSV: {e}")
        if os.path.exists(temp_file.name):
            os.unlink(temp_file.name)

def read_license_plate(reader, image):
    detections = reader.readtext(image)
    for detection in detections:
        bbox, text, score = detection
        text = text.upper().replace(' ', '')
        return text, score
    return None, None        