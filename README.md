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

## Deployment
https://capstone-ml-app-mo5jvyk6cq-as.a.run.app/

Try with your pictures using the same cURL command as mentioned in Sample Usage

`curl -X POST -F "files=@pictures/normal.jpg" -F "files=@pictures/bokeh.jpg" -ttps://capstone-ml-app-mo5jvyk6cq-as.a.run.app/predict`

## Rebuilding
`docker build -t gcr.io/bangkit-capstone-ml/capstone-ml-app .`

`docker push gcr.io/bangkit-capstone-ml/capstone-ml-app`

`gcloud run deploy capstone-ml-app --image gcr.io/bangkit-capstone-ml/capstone-ml-app --platform managed --region asia-southeast1 --allow-unauthenticated --memory=2Gi --cpu=2`

Note: deploying with 2GiB memory and 2 CPU seems to work well. Didn't work with 1 GiB memory and less.
