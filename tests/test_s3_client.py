"""Tests for S3 client."""

from unittest.mock import MagicMock, patch

import httpx
import pytest

from src.services.s3_client import S3Client


@pytest.fixture
def s3_client() -> S3Client:
    """Fixture for S3Client."""
    return S3Client()


def test_download_scan(s3_client: S3Client) -> None:
    """Test downloading scan as bytes."""
    # Create a proper mock response
    mock_response = MagicMock(spec=httpx.Response)
    mock_response.content = b"image data"
    mock_response.raise_for_status = MagicMock()

    with patch("httpx.get", return_value=mock_response) as mock_get:
        result = s3_client.download_scan("user123/scans/photo456")

        assert result == b"image data"
        # Check that httpx.get was called with correct URL structure
        call_args = mock_get.call_args
        assert call_args is not None
        url = call_args[0][0]
        assert url.endswith("/trashscanner-images/user123/scans/photo456")
        assert call_args[1]["timeout"] == 30.0
        mock_response.raise_for_status.assert_called_once()
