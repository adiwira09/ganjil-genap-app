import sqlite3

class Database:
    def __init__(self):
        self.conn = sqlite3.connect('database/database.db')
        self._create_table()

    def _create_table(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS vehicles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                track_id INTEGER,
                vehicle_bbox TEXT,
                vehicle_bbox_score REAL,
                plate_bbox TEXT,
                plate_bbox_score REAL,
                text_plate TEXT,
                text_plate_score REAL,
                date TEXT,
                keterangan TEXT);
            ''')
            
            self.conn.commit()
        except Exception as e:
            print(f"Error creating table: {e}")    

    def write_db(self, track_id, 
                 vehicle_bbox, vehicle_bbox_score, 
                 plate_bbox, plate_bbox_score, 
                 text_plate, text_plate_score, 
                 date, keterangan):
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
            INSERT INTO vehicles (
                track_id, 
                vehicle_bbox, vehicle_bbox_score, 
                plate_bbox, plate_bbox_score, 
                text_plate, text_plate_score, 
                date, keterangan
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
                ''', (track_id, 
                  vehicle_bbox, vehicle_bbox_score, 
                  plate_bbox, plate_bbox_score, 
                  text_plate, text_plate_score, 
                  date, keterangan))
            
            self.conn.commit()
        except Exception as e:
            print(f"Error writing to SQLite: {e}")

    def read_db(self):
        try:
            cursor = self.conn.cursor()

            cursor.execute('''
                SELECT
                    track_id,
                    text_plate,
                    date,
                    keterangan
                FROM 
                    vehicles''')
            rows = cursor.fetchall()
            return rows
        except Exception as e:
            print(f"Error fetching data: {e}")
            return []