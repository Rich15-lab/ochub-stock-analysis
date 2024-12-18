import cv2
import mediapipe as mp
import numpy as np

# Initialize Mediapipe Face Mesh
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=False, max_num_faces=1, refine_landmarks=True)
mp_drawing = mp.solutions.drawing_utils

# Define function to apply virtual makeup
def apply_makeup(frame, landmarks):
    h, w, _ = frame.shape
    overlay = frame.copy()

    # Use specific indices for lip landmarks
    lip_indices = [
        61, 146, 91, 181, 84, 17, 314, 405, 321, 375, 291, 308, 324, 318,
        402, 317, 14, 87, 178, 88, 95, 185, 40, 39, 37, 0, 267, 269, 270, 409, 291
    ]
    lips = [(int(landmarks.landmark[i].x * w), int(landmarks.landmark[i].y * h)) for i in lip_indices]

    # Draw red lipstick
    if lips:
        points = np.array(lips, np.int32)
        cv2.fillPoly(overlay, [points], (0, 0, 255))  # Red lipstick

    # Blend overlay with the frame
    alpha = 0.5  # Transparency
    frame = cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0)
    return frame

# Initialize webcam
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("Error: Unable to access camera.")
        break

    # Convert frame to RGB for Mediapipe
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = face_mesh.process(rgb_frame)

    if result.multi_face_landmarks:
        for face_landmarks in result.multi_face_landmarks:
            # Draw face landmarks
            mp_drawing.draw_landmarks(frame, face_landmarks, mp_face_mesh.FACEMESH_CONTOURS)

            # Apply virtual makeup
            frame = apply_makeup(frame, face_landmarks)

    # Display the frame
    cv2.imshow("AR Makeup Try-On", frame)

    # Quit with 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
