# Blur or Bokeh - Company Capstone Bangkit
Authored by Arkan Alexei Andrei and Maria Aurellia
## Setup
`pip install -r requirements.txt`

Then run the app using
`python app.py`

Feel free to use the S or L version of the model. Loading the L model might take a while.

## Sample Usage
`curl -X POST -F "files=@pictures/normal.jpg" -F "files=@pictures/bokeh.jpg" -F "files=@pictures/blur.png" http://localhost:8080/predict`

If you are using Python, use the `requests` library like so
```python
import requests

url = 'http://localhost:8080/predict'

files = {
    'files': [
        ('files', open('/path/to/image1.jpg', 'rb')),
        ('files', open('/path/to/image2.jpg', 'rb'))
    ]
}

response = requests.post(url, files=files)
print(response.json())
```

Sample Response
```json
[
  {
    "filename": "normal.jpg",
    "prediction": "Normal"
  },
  {
    "filename": "bokeh.jpg",
    "prediction": "Bokeh"
  },
  {
    "filename": "blur.png",
    "prediction": "Blur"
  }
]
```
