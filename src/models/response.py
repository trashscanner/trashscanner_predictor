from enum import Enum

from pydantic import BaseModel


class TrashType(Enum):
    CARDBOARD = 0
    GLASS = 1
    METAL = 2
    PAPER = 3
    PLASTIC = 4
    TRASH = 5
    UNDEFINED = 6


class PredictRequest(BaseModel):
    scan_url: str  # S3 object key (e.g., "user123/scans/photo456")
    prediction_id: str


class PredictionResponse(BaseModel):
    prediction_id: str
    target: str
    result: dict[int, float]  # {TrashType value: probability}
    probabilities: dict[int, float]  # {TrashType value: probability}
