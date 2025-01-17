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
        self.scale_percent = zoom_percent / 100
        self.width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.dim = (int(self.width * self.scale_percent), 
                    int(self.height * self.scale_percent))
        
        self.detector = detector
        self.margin = margin
        self.root = root
        self.label = Label(self.root)

        self.trigger_line = False
        self.line_start = None
        self.line_end = None

    def border_line(self, frame, start_point, end_point, color=(0, 255, 0), thickness=4):
        line_frame = cv2.line(frame, start_point, end_point, color=color, thickness=thickness)
        return line_frame

    def show_frame(self):
        ret, frame = self.cap.read()

        if ret:
            # Proses deteksi pada frame asli (belum di-resize)
            self.detector.detect(frame=frame, trigger=self.line_start[1] if self.trigger_line is True else 0)
            
            # Jika trigger_line aktif, tambahkan garis pada frame sebelum di-resize
            if self.trigger_line and self.line_start and self.line_end:
                frame = self.border_line(frame, self.line_start, self.line_end)
            
            # Resize frame untuk ditampilkan pada tkinter
            resized_frame = cv2.resize(frame, self.dim, interpolation=cv2.INTER_AREA)
            
            # Konversi frame untuk tkinter
            cv2image = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(cv2image)
            imgtk = ImageTk.PhotoImage(image=img)
            
            # Update tampilan label
            self.label.imgtk = imgtk
            self.label.configure(image=imgtk)

        self.label.after(10, self.show_frame)

    def start(self, trigger_line=False, line_start=None, line_end=None):
        self.trigger_line = trigger_line

        if self.trigger_line:
            if line_start is None or line_end is None:
                raise ValueError("line_start dan line_end must be fill.")
            self.line_start = line_start
            self.line_end = line_end

        self.root.update_idletasks()
        self.label.place(x=self.margin, y=self.root.winfo_height() - self.margin, anchor='sw')
        self.show_frame()

    def release(self):
        self.cap.release()