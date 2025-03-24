from flask import Flask, request, jsonify
from flask_cors import CORS
import cv2
import numpy as np
import face_utils
import base64
import os

app = Flask(__name__)
CORS(app)

#init the db of users if not exist
if not os.path.exists('users.pkl'):
    face_utils.init_db()

#preprocessing each image from the video(image converted to grey, then we perform)
def preprocess_image(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    #clahe performs outline creation, basically like scanning an image to upload as pdf(white and black)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    #applying gray to the clahe
    enhanced = clahe.apply(gray)
    #removing the noise from the img, basically smoothens the image
    denoised = cv2.fastNlMeansDenoising(enhanced, None, 10, 7, 21)
    #then we return the processed image
    return cv2.cvtColor(denoised, cv2.COLOR_GRAY2BGR) 

@app.route('/register', methods=['POST'])
def register():
    try:
        data = request.json
        if not data or 'username' not in data or 'image' not in data:
            return jsonify({'success': False, 'message': 'Invalid request format'}), 400

        username = data['username']
        image_data = data['image']
        
        if not image_data:
            return jsonify({'success': False, 'message': 'Empty image data'}), 400

        # Convert base64 to OpenCV image
        nparr = np.frombuffer(base64.b64decode(image_data), np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if img is None:
            return jsonify({'success': False, 'message': 'Invalid image data'}), 400

        # Preprocess and get encoding
        processed = preprocess_image(img)
        encoding = face_utils.get_face_encoding(processed)
        
        if encoding is None:
            return jsonify({'success': False, 'message': 'No face detected'}), 400

        face_utils.save_user(username, encoding)
        return jsonify({'success': True, 'message': 'Registration successful'})

    except Exception as e:
        print(f"Error in registration: {str(e)}")
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.json
        if not data or 'image' not in data:
            return jsonify({'success': False, 'message': 'Invalid request format'}), 400

        image_data = data['image']
        
        if not image_data:
            return jsonify({'success': False, 'message': 'Empty image data'}), 400

        # Convert base64 to OpenCV image
        nparr = np.frombuffer(base64.b64decode(image_data), np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if img is None:
            return jsonify({'success': False, 'message': 'Invalid image data'}), 400

        # Preprocess and get encoding
        processed = preprocess_image(img)
        encoding = face_utils.get_face_encoding(processed)
        
        if encoding is None:
            return jsonify({'success': False, 'message': 'No face detected'}), 400

        user = face_utils.compare_faces(encoding)
        return jsonify({'success': user is not None, 'user': user})

    except Exception as e:
        print(f"Error in login: {str(e)}")
        return jsonify({'success': False, 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)