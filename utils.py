from tensorflow.keras.preprocessing import image
import numpy as np
from PIL import Image
from io import BytesIO
from PIL import Image

def preprocess_image(img, target_size):
    if img.mode != 'RGB':
        img = img.convert('RGB')
    img = img.resize(target_size)
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = img_array / 255.0  # Normalize the image
    return img_array


async def fetch_image(session, url):
    async with session.get(url) as response:
        response.raise_for_status()
        img_data = await response.read()
        return Image.open(BytesIO(img_data))