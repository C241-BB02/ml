from flask import Flask, request, jsonify
from werkzeug.middleware.profiler import ProfilerMiddleware
import asyncio
from utils import fetch_image
from model import make_prediction, load_model
import aiohttp
from PIL import Image

app = Flask(__name__)
app.wsgi_app = ProfilerMiddleware(app.wsgi_app, restrictions=[0.01])

# Load the model at the start
model = load_model()

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
            predicted_class = make_prediction(img, model)
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
async def predict_url():
    data = request.get_json()
    if 'urls' not in data:
        return jsonify({'error': 'No URLs provided'}), 400

    urls = data['urls']
    if len(urls) == 0:
        return jsonify({'error': 'No URLs provided'}), 400

    predictions_list = []

    async with aiohttp.ClientSession() as session:
        tasks = [fetch_image(session, url) for url in urls]
        images = await asyncio.gather(*tasks, return_exceptions=True)

        for url, img in zip(urls, images):
            if isinstance(img, Exception):
                predictions_list.append({
                    'url': url,
                    'error': str(img)
                })
            else:
                try:
                    predicted_class = make_prediction(img, model)
                    predictions_list.append({
                        'url': url,
                        'prediction': predicted_class
                    })
                except Exception as e:
                    predictions_list.append({
                        'url': url,
                        'error': str(e)
                    })

    return jsonify(predictions_list)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
