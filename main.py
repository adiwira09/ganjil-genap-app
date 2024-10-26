import tkinter as tk
from tkinter import ttk
import pandas as pd

from border import border_frame
from Header import create_text_frame
from Webcam import WebcamViewer

def load_excel_data(frame, file_path):
    try:
        data = pd.read_excel(file_path)
        tree = ttk.Treeview(frame, columns=list(data.columns), show="headings")

        column_widths = {
            "No": 50,
            "Frame": 80,
            "Text Plate": 200,
            "Keterangan": 150
        }

        for col in data.columns:
            tree.heading(col, text=col)
            tree.column(col, minwidth=50, width=column_widths.get(col, 100), anchor="center")

        for index, row in data.iterrows():
            tree.insert("", "end", values=list(row))

        tree.pack(fill="both", expand=True)

    except Exception as e:
        error_label = tk.Label(frame, text=f"Error loading file: {e}", fg="red")
        error_label.pack()

# Create the main application window using tkinter
root = tk.Tk()
root.title("Ganjil Genap Application")
root.state('zoomed')
root.configure(bg="#CACFCB")

# Menggunakan fungsi untuk membuat frame dengan border
frame1 = border_frame(root, relx=0.0145, rely=0.02, relwidth=0.625, relheight=None)
create_text_frame(frame1)

frame2 = border_frame(root, relx=0.65, rely=0.02, relwidth=0.34, relheight=0.955)
load_excel_data(frame=frame2, file_path="file.xlsx")

# Webcam frame
webcam_viewer = WebcamViewer(root, zoom_percent=75, margin=20)
webcam_viewer.start()

root.mainloop()
webcam_viewer.release()