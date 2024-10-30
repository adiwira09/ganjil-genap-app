import cv2
from PIL import Image, ImageTk

from tkinter import Label

class WebcamViewer:
    def __init__(self, root, zoom_percent=100, margin=50):
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        
        self.zoom_percent = zoom_percent
        self.margin = margin
        self.root = root

        self.label = Label(self.root)

    def show_frame(self):
        ret, frame = self.cap.read()

        if ret:
            scale_percent = self.zoom_percent / 100
            
            width = int(frame.shape[1] * scale_percent)
            height = int(frame.shape[0] * scale_percent)
            dim = (width, height)

            resized_frame = cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)

            cv2image = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(cv2image)
            imgtk = ImageTk.PhotoImage(image=img)

            self.label.imgtk = imgtk
            self.label.configure(image=imgtk)

        self.label.after(10, self.show_frame)

    def start(self):
        self.root.update_idletasks()
        self.label.place(x=self.margin, y=self.root.winfo_height() - self.margin, anchor='sw')
        self.show_frame()

    def release(self):
        self.cap.release()

class VideoPlayer:
    def __init__(self, root, video_path, detector, zoom_percent=100, margin=50):
        self.cap = cv2.VideoCapture(video_path)
        self.detector = detector
        self.zoom_percent = zoom_percent
        self.margin = margin
        self.root = root

        self.label = Label(self.root)

    def show_frame(self):
        ret, frame = self.cap.read()

        if ret:
            scale_percent = self.zoom_percent / 100

            width = int(frame.shape[1] * scale_percent)
            height = int(frame.shape[0] * scale_percent)
            dim = (width, height)

            resized_frame = cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)

            self.detector.detect(resized_frame)

            cv2image = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(cv2image)
            imgtk = ImageTk.PhotoImage(image=img)

            self.label.imgtk = imgtk
            self.label.configure(image=imgtk)
        
        self.label.after(10, self.show_frame)

    def start(self):
        self.root.update_idletasks()
        self.label.place(x=self.margin, y=self.root.winfo_height() - self.margin, anchor='sw')
        self.show_frame()

    def release(self):
        self.cap.release()