import os
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

import cv2
from deepface import DeepFace
import time

CAMERA_INDEX    = 2          
FRAME_SKIP      = 2
SCALE           = 0.5
BACKEND         = "opencv"
NO_FACE_TIMEOUT = 60

def start_face_detection(shutdown_event=None):
    cap = cv2.VideoCapture(CAMERA_INDEX, cv2.CAP_DSHOW)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    frame_count   = 0
    last_faces    = []
    fps           = 0
    prev_time     = time.time()
    no_face_since = None

    print("Press 'q' to leave.")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame_count += 1
        curr_time = time.time()
        fps = 1 / (curr_time - prev_time)
        prev_time = curr_time

        if frame_count % FRAME_SKIP == 0:
            try:
                small = cv2.resize(frame, (0, 0), fx=SCALE, fy=SCALE)
                results = DeepFace.extract_faces(
                    img_path          = small,
                    detector_backend  = BACKEND,
                    enforce_detection = False
                )
                last_faces = []
                for face in results:
                    region = face["facial_area"]
                    x = int(region["x"] / SCALE)
                    y = int(region["y"] / SCALE)
                    w = int(region["w"] / SCALE)
                    h = int(region["h"] / SCALE)
                    conf = face.get("confidence", 0)
                    if conf > 0.5:
                        last_faces.append((x, y, w, h, conf))
            except Exception as e:
                print(f"Error detection: {e}")
                last_faces = []

        # ── Timer no-face ────────────────────────────────────
        if len(last_faces) == 0:
            if no_face_since is None:
                no_face_since = time.time()
            elapsed   = time.time() - no_face_since
            remaining = NO_FACE_TIMEOUT - elapsed
            cv2.putText(frame, f"No face: {remaining:.1f}s", (10, 60),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            if elapsed >= NO_FACE_TIMEOUT:
                print("No face detected, bye!")
                if shutdown_event:
                    shutdown_event.set()
                break
        else:
            no_face_since = None

        
        for (x, y, w, h, conf) in last_faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, f"{conf:.0%}", (x, y - 8),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

        cv2.putText(frame, f"FPS: {fps:.1f}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 200, 255), 2)

    cap.release()

if __name__ == "__main__":
    start_face_detection()