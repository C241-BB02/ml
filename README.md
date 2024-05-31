# Blur or Bokeh - Company Capstone Bangkit
Authored by Arkan Alexei Andrei and Maria Aurellia
## Setup
`pip install -r requirements.txt`

Then run the app using
`python app.py`

Feel free to use the S or L version of the model. Loading the L model might take a while.

## Sample Usage
### Image File
Endpoint: `/predict`

Sample Request

`curl -X POST -F "files=@pictures/normal.jpg" -F "files=@pictures/bokeh.jpg" -F "files=@pictures/blur.png" http://localhost:8080/predict`

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

### Image URL
Endpoint: `/predict-url`

Sample Request
```json
{
    "urls": [
        "https://st5.depositphotos.com/55662820/62581/i/450/depositphotos_625819662-stock-photo-blurred-purpose-urban-traffic-lights.jpg",
        "https://photographylife.com/wp-content/uploads/2009/12/Creamy-Bokeh.jpg",
        "https://sussexbylines.co.uk/wp-content/uploads/2024/03/cat-out-hunting.jpg"
    ]
}
```

Sample Response
```json
[
    {
        "prediction": "Blur",
        "url": "https://st5.depositphotos.com/55662820/62581/i/450/depositphotos_625819662-stock-photo-blurred-purpose-urban-traffic-lights.jpg"
    },
    {
        "prediction": "Bokeh",
        "url": "https://photographylife.com/wp-content/uploads/2009/12/Creamy-Bokeh.jpg"
    },
    {
        "prediction": "Normal",
        "url": "https://sussexbylines.co.uk/wp-content/uploads/2024/03/cat-out-hunting.jpg"
    }
]
```

## Deployment
https://capstone-ml-app-mo5jvyk6cq-as.a.run.app/

## Rebuilding
`docker build -t gcr.io/bangkit-capstone-ml/capstone-ml-app .`

`docker push gcr.io/bangkit-capstone-ml/capstone-ml-app`

`gcloud run deploy capstone-ml-app --image gcr.io/bangkit-capstone-ml/capstone-ml-app --platform managed --region asia-southeast1 --allow-unauthenticated --memory=2Gi --cpu=2`

Note: deploying with 2GiB memory and 2 CPU seems to work well. Didn't work with 1 GiB memory and less.
