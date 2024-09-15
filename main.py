import tkinter as tk

from Webcam import Webcam

x_webcam = 100
y_webcam = 180

root = tk.Tk()

canvas = tk.Canvas(root, width=1280, height=720)
canvas.pack()

webcam = Webcam(root, canvas, x=x_webcam, y=y_webcam) # display webcam
root.mainloop()

# x1_excel, y1_excel = 1210, 680
# x2_excel, y2_excel = 900, 50

# canvas.create_rectangle(x1_excel, y1_excel, x2_excel, y2_excel, fill="grey")