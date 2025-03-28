import os
import pickle
import numpy as np
import tensorflow as tf
from flask import Flask, request, jsonify
from tensorflow.keras.preprocessing import image

app = Flask(__name__)

# Load the trained Keras model
MODEL_PATH = r"C:\Users\asoha\Desktop\alzheimer_model.keras"
model = tf.keras.models.load_model(MODEL_PATH)

# Load the label encoder
LABEL_ENCODER_PATH = "label_encoder.pkl"
with open(LABEL_ENCODER_PATH, "rb") as f:
    label_encoder = pickle.load(f)

# Image preprocessing function
def preprocess_image(img_path):
    img = image.load_img(img_path, target_size=(224, 224))  # Resize to model's input size
    img_array = image.img_to_array(img) / 255.0  # Normalize
    img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension
    return img_array

@app.route("/predict", methods=["POST"])
def predict():
    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    file = request.files["image"]
    img_path = "temp.jpg"
    file.save(img_path)

    # Preprocess and predict
    img_array = preprocess_image(img_path)
    prediction = model.predict(img_array)
    predicted_class_index = np.argmax(prediction)
    predicted_label = label_encoder.classes_[predicted_class_index]

    return jsonify({"prediction": predicted_label})

if __name__ == "__main__":
    app.run(debug=True)
