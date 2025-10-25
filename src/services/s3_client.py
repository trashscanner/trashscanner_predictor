"""MinIO client for file storage."""

from minio import Minio

from ..config import settings


class S3Client:
    """Client for uploading files to MinIO-compatible storage."""

    def __init__(self) -> None:
        """Initialize MinIO client with settings."""
        self.client = Minio(
            endpoint=settings.filestore.endpoint,
            access_key=settings.filestore.access_key,
            secret_key=settings.filestore.secret_key,
            secure=settings.filestore.use_ssl,
        )
        self.bucket = settings.filestore.bucket

    def download_scan(self, user_id: str, photo_id: str) -> bytes:
        """Download scan file from MinIO and return as bytes."""
        key = f"{user_id}/scans/{photo_id}"
        response = self.client.get_object(self.bucket, key)
        return response.read()

    def get_file_url(self, key: str) -> str:
        """Generate presigned URL for the file."""
        return self.client.presigned_get_object(self.bucket, key)
