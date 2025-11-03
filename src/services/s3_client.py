"""MinIO client for file storage."""

from minio import Minio

from ..config import settings


class S3Client:
    """Client for uploading files to MinIO-compatible storage."""

    def __init__(self) -> None:
        """Initialize MinIO client with settings."""
        self.client = Minio(
            endpoint=settings.filestore.endpoint,
            secure=settings.filestore.use_ssl,
        )
        self.bucket = settings.filestore.bucket

    def download_scan(self, key: str) -> bytes:
        """Download scan file from MinIO and return as bytes."""
        return self.client.get_object(self.bucket, key).read()
