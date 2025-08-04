from flask import Flask, request, jsonify
from flask_cors import CORS
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array
from PIL import Image
import numpy as np
import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'


app = Flask(__name__)
CORS(app)  # Enable CORS for React Native frontend
model = load_model("skin_disease_model.h5")


#Defining the classes

class_names  =["Cellulitis", "Impetigo", "Athelete-Foot", "Nail-Fungus", "Ringworm","Cutaneous-larva-migrans","Chickenpox", "Shingles"]


#Preparing the image before feeding it to the model
def preprocess_image(img, target_size):
    img = img.resize(target_size)
    img_array = img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = img_array / 255.0
    return img_array


#Defining the routes
@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "service": "Skin Disease Prediction API",
        "status": "Active",
        "message": "API is running - use /predict endpoint for predictions",
        "endpoints": {
            "/predict": "POST - Image prediction",
            "/status": "GET - API status"
        }
    })

@app.route("/predict", methods=["POST"])
def predict():
    try:
        if 'file' not in request.files:
            return jsonify({
                "success": False,
                "error": "No file uploaded",
                "message": "Please upload an image file"
            }), 400

        file = request.files['file']
        
        if file.filename == '':
            return jsonify({
                "success": False,
                "error": "No file selected",
                "message": "Please select an image file"
            }), 400

        if file:
            # Process the image
            image = Image.open(file.stream)
            processed_image = preprocess_image(image, target_size=(150,150))
            prediction = model.predict(processed_image)
            predicted_class = class_names[np.argmax(prediction)]
            confidence = float(np.max(prediction))

            return jsonify({
                "success": True,
                "prediction": predicted_class,
                "confidence": confidence,
                "confidence_percentage": f"{confidence:.2%}",
                "all_predictions": {
                    class_names[i]: float(prediction[0][i]) 
                    for i in range(len(class_names))
                },
                "message": f"Detected: {predicted_class} with {confidence:.2%} confidence"
            })

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e),
            "message": "An error occurred while processing the image"
        }), 500

@app.route("/status", methods=["GET"])
def status():
    return jsonify({
        "service": "Skin Disease Prediction API",
        "status": "Active",
        "supported_diseases": class_names,
        "endpoints": {
            "/": "GET - API info",
            "/predict": "POST - Image prediction for mobile apps",
            "/status": "GET - API status"
        },
        "usage": {
            "method": "POST",
            "endpoint": "/predict",
            "content_type": "multipart/form-data",
            "field_name": "file",
            "supported_formats": ["jpg", "jpeg", "png"]
        }
    })
    

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5002))
    app.run(debug=False, host='0.0.0.0', port=port)