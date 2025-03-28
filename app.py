from flask import Flask, request, jsonify
from flask_cors import CORS
import tensorflow as tf
import pickle
import numpy as np
from PIL import Image
import io

app = Flask(__name__)
CORS(app)

# Load Keras model
model = tf.keras.models.load_model(r"C:\Users\asoha\Desktop\alzheimer_model.keras")

# Load Label Encoder (for decoding predictions)
with open(r"C:\Users\asoha\Desktop\label_encoder.pkl", "rb") as f:
    label_encoder = pickle.load(f)

# Image preprocessing function
def preprocess_image(image_bytes):
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")  # Open image
    image = image.resize((224, 224))  # Resize (adjust to match model input size)
    image_array = np.array(image) / 255.0  # Normalize pixel values
    image_array = np.expand_dims(image_array, axis=0)  # Add batch dimension
    return image_array

@app.route("/predict", methods=["POST"])
def predict():
    try:
        if "image" not in request.files:
            return jsonify({"error": "No image uploaded"}), 400

        image = request.files["image"].read()  # Read image file
        processed_image = preprocess_image(image)  # Preprocess image
        prediction = model.predict(processed_image)  # Predict
        predicted_label = np.argmax(prediction, axis=1)  # Get class index
        class_name = label_encoder.inverse_transform(predicted_label)[0]  # Decode label

        return jsonify({"prediction": class_name})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
