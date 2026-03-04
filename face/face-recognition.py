from deepface import DeepFace
import cv2

# Démarrer la capture vidéo
cap = cv2.VideoCapture(0)

while True:
    # Lire une frame de la caméra
    ret, frame = cap.read()
    if not ret:
        break

    # Convertir la frame en RGB (DeepFace utilise RGB)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Détecter les visages avec DeepFace
    try:
        detected_faces = DeepFace.extract_faces(
            img_path=rgb_frame,
            detector_backend='opencv',
            enforce_detection=False
        )

        # Pour chaque visage détecté, dessiner un rectangle vert
        for face_info in detected_faces:
            x, y, w, h = (
                face_info['facial_area']['x'],
                face_info['facial_area']['y'],
                face_info['facial_area']['w'],
                face_info['facial_area']['h']
            )
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    except Exception as e:
        print(f"Erreur: {e}")

    # Afficher la frame
    cv2.imshow('DeepFace - Détection de Visage', frame)

    # Quitter si on appuie sur 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Libérer la caméra et fermer les fenêtres
cap.release()
cv2.destroyAllWindows()