from flask import Flask, request, jsonify
import tensorflow as tf
from tensorflow.keras.preprocessing import image
import numpy as np
from PIL import Image
import requests
from io import BytesIO

app = Flask(__name__)

# Load the model at the start
model = tf.keras.models.load_model('models/efficientnet-s.keras')

# Labels
class_labels = ['Blur', 'Bokeh', 'Normal']

def preprocess_image(img, target_size):
    if img.mode != 'RGB':
        img = img.convert('RGB')
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
            predicted_class = class_labels[np.argmax(predictions[0])] # Get the label from max value
            predictions_list.append({
                'filename': file.filename,
                'prediction': predicted_class
            })
        except Exception as e:
            predictions_list.append({
                'filename': file.filename,
                'error': str(e)
            })

    return jsonify(predictions_list)


@app.route('/predict-url', methods=['POST'])
def predict_url():
    data = request.get_json()
    if 'urls' not in data:
        return jsonify({'error': 'No URLs provided'}), 400

    urls = data['urls']
    if len(urls) == 0:
        return jsonify({'error': 'No URLs provided'}), 400

    predictions_list = []

    for url in urls:
        try:
            response = requests.get(url)
            response.raise_for_status()  # Ensure we notice bad responses
            img = Image.open(BytesIO(response.content))
            preprocessed_image = preprocess_image(img, target_size=(260, 260))
            predictions = model.predict(preprocessed_image)
            predicted_class = class_labels[np.argmax(predictions[0])] # Get the label from max value
            predictions_list.append({
                'url': url,
                'prediction': predicted_class
            })
        except requests.exceptions.RequestException as req_err:
            predictions_list.append({
                'url': url,
                'error': f"Request error: {str(req_err)}"
            })
        except Exception as e:
            predictions_list.append({
                'url': url,
                'error': str(e)
            })

    return jsonify(predictions_list)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
