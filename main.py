import tkinter as tk

from border import border_frame
from Header import create_text_frame
from Webcam import WebcamViewer

# Create the main application window using tkinter
root = tk.Tk()
root.title("Ganjil Genap Application")
root.state('zoomed')
root.configure(bg="#CACFCB")

# Menggunakan fungsi untuk membuat frame dengan border
frame1 = border_frame(root, relx=0.0145, rely=0.02, relwidth=0.625, relheight=None)
create_text_frame(frame1)

frame2 = border_frame(root, relx=0.65, rely=0.02, relwidth=0.34, relheight=0.955)

# Webcam frame
webcam_viewer = WebcamViewer(root, zoom_percent=75, margin=20)
webcam_viewer.start()

root.mainloop()
webcam_viewer.release()