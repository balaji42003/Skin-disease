# Skin Disease Prediction API

A Flask-based API for predicting skin diseases using a trained TensorFlow model.

## Features

- Predict skin diseases from uploaded images
- Support for 8 different skin conditions:
  - Cellulitis
  - Impetigo
  - Athlete's Foot
  - Nail Fungus
  - Ringworm
  - Cutaneous Larva Migrans
  - Chickenpox
  - Shingles

## API Endpoints

- `GET /` - API information and status
- `POST /predict` - Upload an image for prediction
- `GET /status` - API status and supported diseases

## Local Development

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the application:
   ```bash
   python main.py
   ```

## Deployment to Render

This application is ready for deployment to Render with the following files:
- `render.yaml` - Render service configuration
- `Procfile` - Process file for deployment
- `runtime.txt` - Python version specification
- `requirements.txt` - Dependencies

### Steps to Deploy:

1. Push your code to a GitHub repository
2. Connect your GitHub repo to Render
3. Render will automatically detect the configuration and deploy

## Usage

Send a POST request to `/predict` with an image file:

```bash
curl -X POST -F "file=@image.jpg" http://your-render-url.com/predict
```

The API will return a JSON response with the prediction and confidence score.
