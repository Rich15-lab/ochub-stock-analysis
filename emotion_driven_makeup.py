import cv2
import mediapipe as mp
import numpy as np
from deepface import DeepFace
from tkinter import Tk, Label, Button
from PIL import Image, ImageTk
import os

# Product recommendations with links
product_recommendations = {
    'happy': ['Bold Red Lipstick - Maybelline SuperStay Matte Ink', 'Golden Glow Blush - Fenty Beauty'],
    'sad': ['Subtle Nude Lipstick - L’Oréal Paris', 'Matte Beige Eyeshadow - NYX Professional'],
    'angry': ['Fiery Orange Lipstick - MAC Cosmetics', 'Smoky Black Eyeliner - Urban Decay'],
    'surprise': ['Shimmery Pink Lip Gloss - Glossier', 'Peach Highlighter - Tarte'],
    'neutral': ['Natural Brown Lipstick - Bobbi Brown', 'Soft Pink Blush - Rare Beauty'],
    'fear': ['Deep Purple Lipstick - NARS', 'Violet Eyeshadow - Anastasia Beverly Hills']
}

# Initialize Mediapipe Face Mesh
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=False, max_num_faces=1, refine_landmarks=True)

# Function to apply makeup
def apply_makeup(frame, landmarks, emotion):
    h, w, _ = frame.shape
    overlay = frame.copy()

    # Define lip landmarks
    lip_indices = [61, 146, 91, 181, 84, 17, 314, 405, 321, 375, 291, 308, 324, 318]
    lips = [(int(landmarks.landmark[i].x * w), int(landmarks.landmark[i].y * h)) for i in lip_indices]

    # Apply lipstick (based on emotion)
    if lips:
        points = np.array(lips, np.int32)
        color = (255, 0, 0) if emotion == 'happy' else (128, 0, 128)  # Example for happy and sad
        cv2.fillPoly(overlay, [points], color)

    # Blend overlay with frame
    alpha = 0.5
    frame = cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0)
    return frame

# Function to save snapshots
def take_snapshot(frame):
    if not os.path.exists("snapshots"):
        os.makedirs("snapshots")
    filename = f"snapshots/snapshot_{len(os.listdir('snapshots')) + 1}.png"
    cv2.imwrite(filename, frame)
    print(f"Snapshot saved as {filename}")

# Initialize the GUI
def start_app():
    root = Tk()
    root.title("Emotion-Driven Makeup App")

    # Video Label
    video_label = Label(root)
    video_label.pack()

    # Emotion Label
    emotion_label = Label(root, text="Emotion: Detecting...", font=("Helvetica", 16))
    emotion_label.pack()

    # Recommendation Label
    recommendation_label = Label(root, text="Recommended Products:", font=("Helvetica", 14))
    recommendation_label.pack()

    # Snapshot Button
    snapshot_button = Button(root, text="Take Snapshot", font=("Helvetica", 14), command=lambda: take_snapshot(current_frame))
    snapshot_button.pack()

    # Start webcam
    cap = cv2.VideoCapture(0)

    def update_frame():
        global current_frame
        ret, frame = cap.read()
        if not ret:
            return

        # Detect emotion
        try:
            analysis = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)
            emotion = analysis[0]['dominant_emotion'] if isinstance(analysis, list) else analysis['dominant_emotion']
            emotion_label.config(text=f"Emotion: {emotion}")

            # Get recommendations
            recommendations = product_recommendations.get(emotion, [])
            recommendation_label.config(text=f"Recommended Products: {', '.join(recommendations)}")

            # Process face landmarks
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = face_mesh.process(rgb_frame)

            if results.multi_face_landmarks:
                for landmarks in results.multi_face_landmarks:
                    frame = apply_makeup(frame, landmarks, emotion)

            # Convert frame for Tkinter
            img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            imgtk = ImageTk.PhotoImage(image=img)
            video_label.imgtk = imgtk
            video_label.configure(image=imgtk)

            # Save current frame for snapshot
            current_frame = frame.copy()

        except Exception as e:
            emotion_label.config(text=f"Error: {str(e)}")

        # Schedule next frame update
        video_label.after(10, update_frame)

    update_frame()
    root.mainloop()
    cap.release()
    cv2.destroyAllWindows()

# Start the application
start_app()
