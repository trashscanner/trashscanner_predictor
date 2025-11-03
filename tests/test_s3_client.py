"""Tests for S3 client."""

from typing import Generator
from unittest.mock import MagicMock, patch

import pytest

from src.services.s3_client import S3Client


@pytest.fixture
def s3_client() -> Generator[S3Client, None, None]:
    """Fixture for S3Client with mocked MinIO."""
    with patch("minio.Minio") as mock_client:
        client = S3Client()
        client.client = mock_client.return_value
        yield client


def test_download_scan(s3_client: S3Client) -> None:
    """Test downloading scan as bytes."""
    mock_response = MagicMock()
    mock_response.read.return_value = b"image data"
    s3_client.client.get_object = MagicMock(  # type: ignore[method-assign]
        return_value=mock_response
    )

    result = s3_client.download_scan("user123/scans/photo456")
    assert result == b"image data"
    s3_client.client.get_object.assert_called_once_with(
        "trashscanner-images", "user123/scans/photo456"
    )
