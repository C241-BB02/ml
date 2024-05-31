import tensorflow as tf
from utils import preprocess_image
import numpy as np

class_labels = ['Blur', 'Bokeh', 'Normal']

def load_model():
    return tf.keras.models.load_model('models/efficientnet-s.keras')

def make_prediction(img, model):
    preprocessed_image = preprocess_image(img, target_size=(260, 260))
    predictions = model.predict(preprocessed_image)
    predicted_class = class_labels[np.argmax(predictions[0])]  # Get the label from max value
    return predicted_class
