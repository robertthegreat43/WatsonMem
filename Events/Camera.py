import cv2

# Safe camera initialization (works locally and on Render)
try:
    camera = cv2.VideoCapture(0)
    if not camera.isOpened():
        camera = None
except:
    camera = None

# These MUST exist so api_views.py can import them
recording = False
writer = None




class CameraController:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.recording = False
        self.writer = None

    def get_frame(self):
        success, frame = self.cap.read()
        if not success:
            return None
        _, jpeg = cv2.imencode('.jpg', frame)
        return jpeg.tobytes(), frame

    def stream(self):
        while True:
            jpeg, frame = self.get_frame()
            if jpeg is None:
                continue

            if self.recording and self.writer:
                self.writer.write(frame)

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + jpeg + b'\r\n')

    def start_recording(self):
        if not self.recording:
            self.recording = True
            filename = f"recording_{int(time.time())}.mp4"
            fourcc = cv2.VideoWriter_fourcc(*"mp4v")
            self.writer = cv2.VideoWriter(filename, fourcc, 20.0, (640, 480))
            return filename
        return None

    def stop_recording(self):
        self.recording = False
        if self.writer:
            self.writer.release()
            self.writer = None
            return None
        return None
