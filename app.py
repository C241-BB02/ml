from flask import Flask, request, jsonify
import tensorflow as tf
from tensorflow.keras.preprocessing import image
import numpy as np
import os

app = Flask(__name__)

# Load the model at the start
model = tf.keras.models.load_model('models/efficientnet-s.keras')

# Labels
class_labels = ['Blur', 'Bokeh', 'Normal']

def preprocess_image(image_path, target_size):
    img = image.load_img(image_path, target_size=target_size)
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = img_array / 255.0  # Normalize the image
    return img_array

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file provided'}), 400

    # Save the file to a temporary location
    file_path = f'./{file.filename}'
    file.save(file_path)

    # Preprocess the image to match training dimensions
    preprocessed_image = preprocess_image(file_path, target_size=(260, 260))

    # Make prediction
    predictions = model.predict(preprocessed_image)

    # Map predictions to class labels
    class_predictions = {class_labels[i]: float(pred) for i, pred in enumerate(predictions[0])}

    # Delete file
    os.remove(file_path)
    
    return jsonify(class_predictions)

if __name__ == '__main__':
    app.run(debug=True)
