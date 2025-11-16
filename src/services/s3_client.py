"""MinIO client for file storage."""

import httpx

from ..config import settings


class S3Client:
    """Client for downloading files from MinIO-compatible storage."""

    def __init__(self) -> None:
        """Initialize client with settings."""
        self.bucket = settings.filestore.bucket
        protocol = "https" if settings.filestore.use_ssl else "http"
        self.base_url = f"{protocol}://{settings.filestore.endpoint}/{self.bucket}"

    def download_scan(self, key: str) -> bytes:
        """Download scan file from MinIO via public URL and return as bytes."""
        url = f"{self.base_url}/{key}"
        response = httpx.get(url, timeout=30.0)
        response.raise_for_status()
        return response.content
