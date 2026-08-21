import cv2
from datetime import datetime


def record_camera():
    camera = cv2.VideoCapture(0)

    if not camera.isOpened():
        print("Error: Could not open camera.")
        return

    frame_width = int(camera.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(camera.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = 20.0

    filename = datetime.now().strftime("stream_recording_%Y%m%d_%H%M%S.mp4")

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    recorder = cv2.VideoWriter(
        filename,
        fourcc,
        fps,
        (frame_width, frame_height)
    )

    print("Camera recording started.")
    print("Press 'q' to stop recording.")

    while True:
        success, frame = camera.read()

        if not success:
            print("Error: Could not read frame.")
            break

        recorder.write(frame)

        cv2.imshow("Camera Stream Recording", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    camera.release()
    recorder.release()
    cv2.destroyAllWindows()

    print(f"Recording saved as: {filename}")

if __name__ == "__main__":
    record_camera()


