import time
import cv2

class USBCamera:
    def __init__(self, device="/dev/video0", width=1280, height=720):
        self.device = device
        self.width = width
        self.height = height

    def connect(self):
        while True:
            cam = cv2.VideoCapture(self.device)
            cam.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
            cam.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
            if cam.isOpened():
                return cam
            cam.release()
            time.sleep(1)

    def capture_image(self):
        cam = self.connect()
        ret, frame = cam.read()
        cam.release()
        return frame if ret else None

