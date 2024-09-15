import cv2
from PIL import Image, ImageTk

class Webcam:
    def __init__(self, root, canvas, x, y):
        self.root = root
        self.canvas = canvas
        self.x, self.y = x, y
        self.vid = cv2.VideoCapture(0) # capture video dari webcam
        self.update() # start video streaming

    def update(self):
        ret, frame = self.vid.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) # convert dari BGR to RGB
            img = Image.fromarray(frame)
            imgtk = ImageTk.PhotoImage(image=img)
            self.canvas.create_image(self.x, self.y, anchor='nw', image=imgtk)
            self.canvas.imgtk = imgtk
        self.root.after(20, self.update)
    
    def __del__(self):
        self.vid.release()