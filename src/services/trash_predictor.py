"""Trash predictor using ONNX model."""

from typing import Dict, Optional

import numpy as np
import onnxruntime as ort  # type: ignore
from PIL import Image

from ..config import settings
from ..models.response import TrashType


class TrashPredictor:
    """Predictor for trash types using ONNX model."""

    def __init__(self, model_path: Optional[str] = None) -> None:
        """Initialize the predictor with the ONNX model."""
        try:
            model_path = model_path or settings.model.path
            self.session = ort.InferenceSession(model_path)
            self.input_name = self.session.get_inputs()[0].name
            self.output_name = self.session.get_outputs()[0].name
            # Assume input shape is (1, 3, H, W), adjust if needed
            self.input_shape = self.session.get_inputs()[0].shape
            self.classes = list(TrashType)
        except Exception as e:
            raise RuntimeError(f"Failed to load ONNX model: {e}")

    def preprocess_image(self, image: Image.Image) -> np.ndarray:
        """Preprocess the image for model input."""
        # Resize to expected size from settings
        image = image.resize(settings.image_size)
        # Convert to RGB if needed
        if image.mode != "RGB":
            image = image.convert("RGB")
        # Convert to numpy array and normalize (0-1)
        img_array = np.array(image).astype(np.float32) / 255.0
        # Transpose to (C, H, W)
        img_array = np.transpose(img_array, (2, 0, 1))
        # Add batch dimension
        img_array = np.expand_dims(img_array, axis=0)
        return img_array

    def predict_from_image(self, image: Image.Image) -> Dict[TrashType, float]:
        """Predict trash type probabilities from PIL Image."""
        input_data = self.preprocess_image(image)
        outputs = self.session.run([self.output_name], {self.input_name: input_data})
        probabilities = outputs[0][
            0
        ]  # Assuming shape (1, num_classes), get the first (and only) batch
        # Model outputs probabilities (sigmoid), no need for softmax
        return {cls: float(prob) for cls, prob in zip(self.classes, probabilities)}

    def predict_from_bytes(self, image_bytes: bytes) -> Dict[TrashType, float]:
        """Predict from image bytes."""
        from io import BytesIO

        image = Image.open(BytesIO(image_bytes))
        return self.predict_from_image(image)
