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


class PredictionResponse(BaseModel):
    prediction_id: str
    target: str
    result: tuple[TrashType, float]
    probabilities: dict[TrashType, float]
