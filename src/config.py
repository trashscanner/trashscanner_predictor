"""Configuration settings for the application."""

import os
from pathlib import Path
from typing import Optional

import yaml
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class ServerConfig(BaseModel):
    host: str = "0.0.0.0"
    port: int = 8000


class AuthConfig(BaseModel):
    token: str = "secret-token"


class LoggingConfig(BaseModel):
    level: str = "info"
    file: Optional[str] = None


class ModelConfig(BaseModel):
    path: str = "model.onnx"


class FilestoreConfig(BaseModel):
    endpoint: str = "localhost:9000"
    bucket: str = "trashscanner-images"
    use_ssl: bool = False


class Settings(BaseSettings):
    """Application settings."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
    )

    config_path: str = "config/dev/config.yml"

    server: ServerConfig = ServerConfig()
    auth: AuthConfig = AuthConfig()
    logging: LoggingConfig = LoggingConfig()
    model: ModelConfig = ModelConfig()
    filestore: FilestoreConfig = FilestoreConfig()

    @property
    def image_size(self) -> tuple[int, int]:
        # Assuming fixed for now, can add to YAML if needed
        return (256, 256)


def load_settings() -> Settings:
    """Load settings from YAML config file, with env overrides."""
    config_path = os.getenv("CONFIG_PATH", "config/dev/config.yml")

    # Load from YAML
    if Path(config_path).exists():
        with open(config_path, "r", encoding="utf-8") as f:
            config_data = yaml.safe_load(f) or {}
    else:
        config_data = {}

    # Override with environment variables
    # Format: SERVER__HOST, AUTH__TOKEN, FILESTORE__ENDPOINT, etc.
    env_overrides: dict[str, dict[str, str | int | bool]] = {}

    # Server overrides
    server_host = os.getenv("SERVER__HOST")
    if server_host:
        env_overrides.setdefault("server", {})["host"] = server_host
    server_port = os.getenv("SERVER__PORT")
    if server_port:
        env_overrides.setdefault("server", {})["port"] = int(server_port)

    # Auth overrides
    auth_token = os.getenv("AUTH__TOKEN")
    if auth_token:
        env_overrides.setdefault("auth", {})["token"] = auth_token

    # Logging overrides
    logging_level = os.getenv("LOGGING__LEVEL")
    if logging_level:
        env_overrides.setdefault("logging", {})["level"] = logging_level
    logging_file = os.getenv("LOGGING__FILE")
    if logging_file:
        env_overrides.setdefault("logging", {})["file"] = logging_file

    # Model overrides
    model_path = os.getenv("MODEL__PATH")
    if model_path:
        env_overrides.setdefault("model", {})["path"] = model_path

    # Filestore overrides
    filestore_endpoint = os.getenv("FILESTORE__ENDPOINT")
    if filestore_endpoint:
        env_overrides.setdefault(
            "filestore", {}
        )["endpoint"] = filestore_endpoint
    filestore_bucket = os.getenv("FILESTORE__BUCKET")
    if filestore_bucket:
        env_overrides.setdefault("filestore", {})["bucket"] = filestore_bucket
    filestore_use_ssl = os.getenv("FILESTORE__USE_SSL")
    if filestore_use_ssl:
        env_overrides.setdefault("filestore", {})["use_ssl"] = (
            filestore_use_ssl.lower() in ("true", "1", "yes")
        )

    # Merge: YAML config + env overrides
    for section, values in env_overrides.items():
        if section in config_data:
            config_data[section].update(values)
        else:
            config_data[section] = values

    settings = Settings(**config_data)
    return settings


settings = load_settings()
