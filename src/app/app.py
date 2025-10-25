from fastapi import FastAPI, HTTPException, Header
from minio.error import S3Error

from ..services.s3_client import S3Client
from ..services.trash_predictor import TrashPredictor
from ..models.response import PredictionResponse

app = FastAPI(title="Trash Scanner Predictor", description="Backend API for TrashScanner app")

predictor = TrashPredictor()
s3_client = S3Client()


@app.get("/")
async def root() -> dict:
    return {"message": "Welcome to Trash Scanner Predictor API"}


@app.post("/predict", response_model=PredictionResponse, tags=["Prediction"])
async def predict_trash(
    photo_id: str,
    user_id: str = Header(...),
    prediction_id: str = Header(...),
) -> PredictionResponse:
    """Predict trash type from uploaded image key."""
    try:
        # Download file from S3
        image_bytes = s3_client.download_scan(user_id, photo_id)
    except S3Error as e:
        if e.code == "NoSuchKey":
            raise HTTPException(status_code=404, detail="Image not found")
        else:
            raise HTTPException(status_code=500, detail=f"S3 error {e.code}: {e.message}")

    try:
        # Predict
        probabilities = predictor.predict_from_bytes(image_bytes)
        result = max(probabilities, key=lambda k: probabilities[k])
        confidence = probabilities[result]
        return PredictionResponse(
            prediction_id=prediction_id,
            target=photo_id,
            result=(result, confidence),
            probabilities=probabilities,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")
