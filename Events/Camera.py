import os
import time

import cv2


class CameraController:
    def __init__(self):
        self.cap = None
        self.recording = False
        self.writer = None

    def open_camera(self):
        """Open the configured camera, returning False when none is available."""
        if self.cap is not None and self.cap.isOpened():
            return True

        self.close_camera()
        try:
            camera_index = int(os.environ.get("CAMERA_INDEX", "0"))
            capture = cv2.VideoCapture(camera_index)
            if not capture.isOpened():
                capture.release()
                return False
            self.cap = capture
            return True
        except (ValueError, cv2.error, OSError):
            self.close_camera()
            return False

    def close_camera(self):
        if self.cap is not None:
            self.cap.release()
            self.cap = None

    def get_frame(self):
        if not self.open_camera():
            return None

        try:
            success, frame = self.cap.read()
            if not success or frame is None:
                self.close_camera()
                return None

            encoded, jpeg = cv2.imencode(".jpg", frame)
            if not encoded:
                return None
            return jpeg.tobytes(), frame
        except cv2.error:
            self.close_camera()
            return None

    @staticmethod
    def _camera_unavailable_frame():
        # Keep the MJPEG endpoint useful without a camera, and avoid returning
        # an HTTP 500 or spinning in a tight loop on hosted servers.
        image = 255 * __import__("numpy").ones((240, 640, 3), dtype="uint8")
        cv2.putText(
            image,
            "Camera unavailable on this server",
            (35, 125),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (30, 30, 180),
            2,
            cv2.LINE_AA,
        )
        encoded, jpeg = cv2.imencode(".jpg", image)
        return jpeg.tobytes() if encoded else b""

    def stream(self):
        unavailable_frame = None
        while True:
            result = self.get_frame()
            if result is None:
                if unavailable_frame is None:
                    unavailable_frame = self._camera_unavailable_frame()
                if unavailable_frame:
                    yield (
                        b"--frame\r\n"
                        b"Content-Type: image/jpeg\r\n\r\n"
                        + unavailable_frame
                        + b"\r\n"
                    )
                time.sleep(1)
                continue

            jpeg, frame = result
            if self.recording and self.writer is not None:
                self.writer.write(frame)

            yield (
                b"--frame\r\n"
                b"Content-Type: image/jpeg\r\n\r\n" + jpeg + b"\r\n"
            )

    def start_recording(self):
        if self.recording or not self.open_camera():
            return None

        width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        if width <= 0 or height <= 0:
            return None

        filename = f"recording_{int(time.time())}.mp4"
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        try:
            writer = cv2.VideoWriter(filename, fourcc, 20.0, (width, height))
            if not writer.isOpened():
                writer.release()
                return None
        except cv2.error:
            return None

        self.writer = writer
        self.recording = True
        return filename

    def stop_recording(self):
        self.recording = False
        if self.writer is not None:
            self.writer.release()
            self.writer = None


camera_controller = CameraController()
