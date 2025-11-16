from fastapi import FastAPI, HTTPException, Header, Depends
import httpx

from ..services.s3_client import S3Client
from ..services.trash_predictor import TrashPredictor
from ..models.response import PredictionResponse, PredictRequest
from ..config import settings

app = FastAPI(title="Trash Scanner Predictor", description="Backend API for TrashScanner app")


async def verify_token(token: str = Header(..., alias="token")) -> str:
    """Verify authentication token in request headers."""
    if token != settings.auth.token:
        raise HTTPException(status_code=403, detail="Invalid authentication token")
    return token


predictor = TrashPredictor()
s3_client = S3Client()


@app.get("/")
async def root() -> dict:
    return {"message": "Welcome to Trash Scanner Predictor API"}


@app.post("/predict", response_model=PredictionResponse, tags=["Prediction"])
async def predict_trash(
    body: PredictRequest,
    _: str = Depends(verify_token),
) -> PredictionResponse:
    """Predict trash type from S3 object key."""
    try:
        # Download image from S3
        image_bytes = s3_client.download_scan(body.scan_url)
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            raise HTTPException(status_code=404, detail="Image not found")
        else:
            raise HTTPException(
                status_code=500,
                detail=(
                    f"Failed to download image: "
                    f"{e.response.status_code} {e.response.reason_phrase}"
                ),
            )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to download image: {str(e)}")

    try:
        probabilities = predictor.predict_from_bytes(image_bytes)
        result = max(probabilities, key=lambda k: probabilities[k])
        confidence = probabilities[result]
        return PredictionResponse(
            prediction_id=body.prediction_id,
            target=body.scan_url,
            result={result.value: confidence},
            probabilities={k.value: v for k, v in probabilities.items()},
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")
