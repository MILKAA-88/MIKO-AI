import cv2
import deepface

# Démarrer la capture vidéo
cap = cv2.VideoCapture(0)

while True:
    # Lire une frame de la caméra
    ret, frame = cap.read()
    if not ret:
        break

    # Convertir la frame en RGB (face_recognition utilise RGB)
    rgb_frame = frame[:, :, ::-1]

    # Détecter les visages dans la frame
    face_locations = face_recognition.face_locations(rgb_frame)

    # Pour chaque visage détecté, dessiner un rectangle vert
    for (top, right, bottom, left) in face_locations:
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

    # Afficher la frame
    cv2.imshow('Détection de visage', frame)

    # Quitter si on appuie sur 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Libérer la caméra et fermer les fenêtres
cap.release()
cv2.destroyAllWindows()
