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

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

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
    if Path(config_path).exists():
        with open(config_path, "r", encoding="utf-8") as f:
            config_data = yaml.safe_load(f)
    else:
        config_data = {}

    # Override with env variables
    settings = Settings(**config_data)
    return settings


settings = load_settings()
