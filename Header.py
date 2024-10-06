import tkinter as tk
from datetime import datetime

BG_COLOR = "#D8DDD9"
TITLE_FONT = ("Arial", 25, "bold")
LABEL_FONT = ("Arial", 20)

def update_time_label(time_label, frame):
    current_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    time_label.config(text=current_time)
    frame.after(1000, update_time_label, time_label, frame)  # Update every second

def create_text_frame(frame):
    # Title Label
    title_label = tk.Label(frame, text="SISTEM GANJIL GENAP", font=TITLE_FONT, bg=BG_COLOR)
    title_label.pack(pady=(10, 20))

    # Camera Info Label
    camera_label = tk.Label(frame, text="Kamera : Kamera 1", font=LABEL_FONT, bg=BG_COLOR)
    camera_label.pack(anchor="w", pady=(0, 15), padx=(30, 0))

    # Create a frame to hold Location and Time labels side by side
    location_time_frame = tk.Frame(frame, bg=BG_COLOR)
    location_time_frame.pack(anchor="w", padx=(30, 0), pady=(0, 15), fill="x")

    # Location Label (Left)
    location_label = tk.Label(location_time_frame, text="Lokasi : Jakarta", font=LABEL_FONT, bg=BG_COLOR)
    location_label.pack(side="left")

    # Time Label (Right)
    time_label = tk.Label(location_time_frame, font=LABEL_FONT, bg=BG_COLOR)
    time_label.pack(side="right", padx=(0, 30))

    # Start updating time
    update_time_label(time_label, frame)