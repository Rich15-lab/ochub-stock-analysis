from deepface import DeepFace
import cv2

# Define emotion-to-makeup mapping
makeup_styles = {
    'happy': 'Bright and radiant look with highlighter',
    'sad': 'Soft, neutral tones with minimal contour',
    'angry': 'Smoky eyes and bold eyeliner',
    'surprise': 'Shimmery eyeshadow with a subtle glow',
    'neutral': 'Natural tones with light coverage',
    'fear': 'Cool tones with defined contour'
}

# Function to get makeup style based on emotion
def get_makeup_style(emotion):
    return makeup_styles.get(emotion, 'Natural look')  # Default to "Natural look" if emotion not in dictionary

# Initialize webcam
cap = cv2.VideoCapture(0)

# Check if the camera is opened successfully
if not cap.isOpened():
    print("Error: Could not access the camera. Ensure it is connected and authorized.")
    exit()

# User preference
custom_makeup_style = None

while True:
    ret, frame = cap.read()

    if not ret:
        print("Error: Failed to read frame from camera.")
        break

    try:
        # Analyze emotions
        analysis = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)
        if isinstance(analysis, list):  # Handle list output if DeepFace returns multiple results
            analysis = analysis[0]

        dominant_emotion = analysis.get('dominant_emotion', 'neutral')  # Default to 'neutral' if key missing

        # Use custom makeup style if set, otherwise use the detected style
        makeup_style = custom_makeup_style if custom_makeup_style else get_makeup_style(dominant_emotion)
        print(f"Emotion: {dominant_emotion} -> Makeup Style: {makeup_style}")

        # Display emotion and makeup style on video feed
        cv2.putText(frame, f'Emotion: {dominant_emotion}', (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
        cv2.putText(frame, f'Makeup: {makeup_style}', (30, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)

        # Add instructions to the feed
        cv2.putText(frame, "Press 1: Bright look", (30, 150), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (200, 200, 200), 2, cv2.LINE_AA)
        cv2.putText(frame, "Press 2: Neutral look", (30, 180), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (200, 200, 200), 2, cv2.LINE_AA)
        cv2.putText(frame, "Press 3: Smoky look", (30, 210), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (200, 200, 200), 2, cv2.LINE_AA)
        cv2.putText(frame, "Press 4: Shimmery look", (30, 240), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (200, 200, 200), 2, cv2.LINE_AA)
        cv2.putText(frame, "Press 0: Reset", (30, 270), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (200, 200, 200), 2, cv2.LINE_AA)
        cv2.putText(frame, "Press Q: Quit", (30, 300), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (200, 200, 200), 2, cv2.LINE_AA)
    except Exception as e:
        print(f"Error in emotion analysis: {e}")

    # Display the video feed
    cv2.imshow('Emotion Detection with Makeup Suggestions', frame)

    # Handle user input for custom makeup style
    key = cv2.waitKey(1) & 0xFF
    if key == ord('1'):
        custom_makeup_style = 'Bright and radiant look with highlighter'
        print("Custom Makeup: Bright and radiant look with highlighter")
    elif key == ord('2'):
        custom_makeup_style = 'Soft, neutral tones with minimal contour'
        print("Custom Makeup: Soft, neutral tones with minimal contour")
    elif key == ord('3'):
        custom_makeup_style = 'Smoky eyes and bold eyeliner'
        print("Custom Makeup: Smoky eyes and bold eyeliner")
    elif key == ord('4'):
        custom_makeup_style = 'Shimmery eyeshadow with a subtle glow'
        print("Custom Makeup: Shimmery eyeshadow with a subtle glow")
    elif key == ord('0'):
        custom_makeup_style = None
        print("Custom Makeup: Reset to emotion-based recommendations")
    elif key == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
