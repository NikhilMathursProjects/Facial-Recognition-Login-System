import face_recognition
import cv2
import pickle
import os
import numpy as np

def init_db():
    with open('users.pkl', 'wb') as f:
        pickle.dump({}, f)

def load_db():
    with open('users.pkl', 'rb') as f:
        return pickle.load(f)

def save_user(username, encoding):
    db = load_db()
    db[username] = encoding
    with open('users.pkl', 'wb') as f:
        pickle.dump(db, f)

def base64_to_image(base64_str):
    encoded_data = base64_str.split(',')[1]
    nparr = np.frombuffer(base64.b64decode(encoded_data), np.uint8)
    return cv2.imdecode(nparr, cv2.IMREAD_COLOR)

def get_face_encoding(image):
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    rgb = cv2.resize(rgb, (0,0), fx=1.5, fy=1.5)  # Upscale for better detection
    
    faces = face_recognition.face_locations(rgb, model='hog')
    if len(faces) == 0:
        return None
        
    return face_recognition.face_encodings(rgb, faces)[0]

def compare_faces(unknown_enc, tolerance=0.5):
    db = load_db()
    for name, known_enc in db.items():
        if face_recognition.compare_faces([known_enc], unknown_enc, tolerance)[0]:
            return name
    return None