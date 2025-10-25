"""Tests for trash predictor."""

import io
from unittest.mock import patch, MagicMock

from PIL import Image

from src.services.trash_predictor import TrashPredictor
from src.models.response import TrashType


def create_test_image() -> bytes:
    """Create a simple test image in bytes."""
    # Create a 256x256 RGB image
    img = Image.new("RGB", (256, 256), color=(255, 0, 0))  # Red image
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    buf.seek(0)
    return buf.getvalue()


class TestTrashPredictor:
    """Test cases for TrashPredictor."""

    @patch("onnxruntime.InferenceSession")
    def test_init(self, mock_session: MagicMock) -> None:
        """Test initialization of TrashPredictor."""
        predictor = TrashPredictor()
        assert predictor.session == mock_session.return_value
        assert predictor.input_name == mock_session.return_value.get_inputs.return_value[0].name
        assert predictor.output_name == mock_session.return_value.get_outputs.return_value[0].name
        assert predictor.classes == list(TrashType)

    @patch("onnxruntime.InferenceSession")
    def test_preprocess_image(self, mock_session: MagicMock) -> None:
        """Test image preprocessing."""
        predictor = TrashPredictor()
        img = Image.new("RGB", (100, 100), color=(128, 128, 128))
        processed = predictor.preprocess_image(img)
        assert processed.shape == (1, 3, 256, 256)  # Batch, Channels, Height, Width
        assert processed.dtype == "float32"
        assert 0 <= processed.min() <= processed.max() <= 1  # Normalized

    @patch("onnxruntime.InferenceSession")
    def test_predict_from_bytes(self, mock_session: MagicMock) -> None:
        """Test prediction from bytes."""
        # Mock the session run to return dummy probabilities
        mock_session.return_value.run.return_value = [
            [[0.1, 0.2, 0.3, 0.1, 0.1, 0.1, 0.1]]
        ]  # shape (1, 7)
        predictor = TrashPredictor()
        image_bytes = create_test_image()
        result = predictor.predict_from_bytes(image_bytes)
        assert isinstance(result, dict)
        assert len(result) == 7
        assert all(isinstance(k, TrashType) for k in result.keys())
        assert all(isinstance(v, float) for v in result.values())
