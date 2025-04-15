import cv2
import os
from deepface import DeepFace

def analyze_facial_emotions(video_path):
    cap = cv2.VideoCapture(video_path)
    frame_rate = int(cap.get(cv2.CAP_PROP_FPS))
    frame_count = 0
    emotion_scores = []

    print("Analyzing video...")

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        if frame_count % (frame_rate * 2) == 0:  # analyze every 2 seconds
            try:
                result = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)
                dominant_emotion = result[0]['dominant_emotion']
                emotion_scores.append(dominant_emotion)
            except Exception as e:
                print("Error analyzing frame:", e)

        frame_count += 1

    cap.release()

    # Confidence boosting emotions
    confidence_emotions = ['happy', 'neutral', 'surprise']

    if not emotion_scores:
        return 0

    # Calculate confidence score
    score = 0
    for emo in emotion_scores:
        if emo in confidence_emotions:
            score += 1

    confidence_score = round((score / len(emotion_scores)) * 100, 2)
    return confidence_score