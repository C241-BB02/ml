# Blur or Bokeh - Company Capstone Bangkit
Authored by Arkan Alexei Andrei and Maria Aurellia
## Setup
`pip install -r requirements.txt`

Then run the app using
`python app.py`

Feel free to use the S or L version of the model. Loading the L model might take a while.

## Sample Usage
`curl -X POST -F file=@pictures/normal.jpg  http://localhost:5000/predict`

```json
{
  "Blur": 0.0002159166324418038,
  "Bokeh": 0.04579726234078407,
  "Normal": 0.9539867639541626
}
```
