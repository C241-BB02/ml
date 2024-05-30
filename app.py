from flask import Flask, request, jsonify
import tensorflow as tf
from tensorflow.keras.preprocessing import image
import numpy as np
from PIL import Image

app = Flask(__name__)

# Load the model at the start
model = tf.keras.models.load_model('models/efficientnet-s.keras')

# Labels
class_labels = ['Blur', 'Bokeh', 'Normal']

def preprocess_image(img, target_size):
    img = img.resize(target_size)
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = img_array / 255.0  # Normalize the image
    return img_array

@app.route('/predict', methods=['POST'])
def predict():
    # Handle no files
    if 'files' not in request.files:
        return jsonify({'error': 'No files provided'}), 400

    files = request.files.getlist('files')
    if len(files) == 0:
        return jsonify({'error': 'No files provided'}), 400

    predictions_list = []

    # Handle each file's prediction
    for file in files:
        try:
            img = Image.open(file)
            preprocessed_image = preprocess_image(img, target_size=(260, 260))
            predictions = model.predict(preprocessed_image)
            class_predictions = {class_labels[i]: float(pred) for i, pred in enumerate(predictions[0])}
            predictions_list.append({
                'filename': file.filename,
                'predictions': class_predictions
            })
        except Exception as e:
            predictions_list.append({
                'filename': file.filename,
                'error': str(e)
            })

    return jsonify(predictions_list)

if __name__ == '__main__':
    app.run(debug=True)
