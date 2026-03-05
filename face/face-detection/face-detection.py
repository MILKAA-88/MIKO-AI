import cv2
from deepface import DeepFace
import time

# ── Configuration ──────────────────────────────────────────
CAMERA_INDEX = 0        # 0 = webcam principale
FRAME_SKIP   = 2        # Analyse 1 frame sur N (plus N est grand = plus de FPS)
SCALE        = 0.5      # Réduit la frame avant analyse (0.5 = moitié de la résolution)
BACKEND      = "opencv" # Le plus rapide : opencv > ssd > mtcnn > retinaface
# ───────────────────────────────────────────────────────────

cap = cv2.VideoCapture(CAMERA_INDEX)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

frame_count = 0
last_faces  = []  # Garde le dernier résultat affiché entre les frames skippées
fps         = 0
prev_time   = time.time()

print("Appuie sur 'q' pour quitter.")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame_count += 1

    # ── Calcul FPS ─────────────────────────────────────────
    curr_time = time.time()
    fps = 1 / (curr_time - prev_time)
    prev_time = curr_time

    # ── Analyse seulement toutes les N frames ──────────────
    if frame_count % FRAME_SKIP == 0:
        try:
            # Réduit la résolution pour accélérer l'analyse
            small = cv2.resize(frame, (0, 0), fx=SCALE, fy=SCALE)

            results = DeepFace.extract_faces(
                img_path       = small,
                detector_backend = BACKEND,
                enforce_detection = False  # Ne plante pas si aucun visage
            )

            last_faces = []
            for face in results:
                region = face["facial_area"]
                # Remet à l'échelle originale
                x = int(region["x"]      / SCALE)
                y = int(region["y"]      / SCALE)
                w = int(region["w"]      / SCALE)
                h = int(region["h"]      / SCALE)
                conf = face.get("confidence", 0)
                last_faces.append((x, y, w, h, conf))

        except Exception as e:
            print(f"Erreur détection : {e}")
            last_faces = []

    # ── Affichage des rectangles ───────────────────────────
    for (x, y, w, h, conf) in last_faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(frame, f"{conf:.0%}", (x, y - 8),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    # ── Affichage FPS ──────────────────────────────────────
    cv2.putText(frame, f"FPS: {fps:.1f}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 200, 255), 2)

    cv2.imshow("MIKO-AI | Detection visage", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()