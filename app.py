from flask import Flask, request, jsonify
import cv2
import numpy as np
from deepface import DeepFace
import mediapipe as mp

app = Flask(__name__)

# Mediapipe Face Mesh setup
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=True, max_num_faces=1, refine_landmarks=True)

# Define emotion-to-product mapping
product_recommendations = {
    'happy': ['Bold Red Lipstick - Maybelline SuperStay Matte Ink', 'Golden Glow Blush - Fenty Beauty'],
    'sad': ['Subtle Nude Lipstick - L\'Oréal Paris', 'Matte Beige Eyeshadow - NYX Professional'],
    'angry': ['Fiery Orange Lipstick - MAC Cosmetics', 'Smoky Black Eyeliner - Urban Decay'],
    'surprise': ['Shimmery Pink Lip Gloss - Glossier', 'Peach Highlighter - Tarte'],
    'neutral': ['Natural Brown Lipstick - Bobbi Brown', 'Soft Pink Blush - Rare Beauty'],
    'fear': ['Deep Purple Lipstick - NARS', 'Violet Eyeshadow - Anastasia Beverly Hills']
}

# Analyze emotion and return recommendations
@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        # Receive the image from the frontend
        image_file = request.files['image']
        image = cv2.imdecode(np.frombuffer(image_file.read(), np.uint8), cv2.IMREAD_COLOR)

        # Analyze emotion
        analysis = DeepFace.analyze(image, actions=['emotion'], enforce_detection=False)
        emotion = analysis[0]['dominant_emotion'] if isinstance(analysis, list) else analysis['dominant_emotion']

        # Get product recommendations
        recommendations = product_recommendations.get(emotion, [])

        return jsonify({
            'emotion': emotion,
            'recommendations': recommendations
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
