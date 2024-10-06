import tkinter as tk
from Header import create_text_frame
from Webcam import WebcamViewer

# Create the main application window
root = tk.Tk()
root.title("Ganjil Genap Application")
root.state('zoomed')
root.configure(bg="#CACFCB")

# Frame 1 (Header)
frame1 = tk.Frame(root, bd=2, padx=10, pady=10, bg="#D8DDD9",
                  highlightbackground="black", highlightcolor="black", highlightthickness=2)
frame1.place(relx=0.0145, rely=0.02, relwidth=0.625)
create_text_frame(frame1)

# Webcam frame
webcam_viewer = WebcamViewer(root, zoom_percent=75, margin=20)
webcam_viewer.start()

# Frame 2 (Spreadsheet)
frame2 = tk.Frame(root, bd=2, padx=10, pady=10, bg="#D8DDD9",
                  highlightbackground="black", highlightcolor="black", highlightthickness=2)
frame2.place(relx=0.65, rely=0.02,
             relheight=0.955, relwidth=0.34,
             anchor='nw')

root.mainloop()
webcam_viewer.release()
