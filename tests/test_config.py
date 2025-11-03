"""Tests for configuration loading."""

from unittest.mock import patch

from src.config import (
    Settings,
    load_settings,
    ServerConfig,
    LoggingConfig,
    ModelConfig,
    FilestoreConfig,
)


def test_load_settings_from_yaml() -> None:
    """Test loading settings from YAML file."""
    config_path = "config/dev/config.yml"
    with patch("os.getenv", return_value=config_path):
        settings = load_settings()

    # Check values from the actual config file
    assert settings.server.host == "0.0.0.0"
    assert settings.server.port == 8000
    assert settings.auth.token == "secret-token"
    assert settings.logging.level == "info"
    assert settings.logging.file == "logs/app.log"
    assert settings.model.path == "model.onnx"
    assert settings.filestore.endpoint == "127.0.0.1:9000"
    assert settings.filestore.bucket == "trashscanner-images"
    assert settings.filestore.use_ssl is False
    assert settings.image_size == (256, 256)  # Default


def test_load_settings_defaults() -> None:
    """Test loading settings with defaults when file not found."""
    with patch("os.getenv", return_value="nonexistent.yml"):
        settings = load_settings()

    assert settings.server.host == "0.0.0.0"
    assert settings.server.port == 8000
    assert settings.logging.level == "info"
    assert settings.logging.file is None
    assert settings.model.path == "model.onnx"
    assert settings.filestore.endpoint == "localhost:9000"
    assert settings.filestore.bucket == "trashscanner-images"
    assert settings.filestore.use_ssl is False


def test_settings_image_size() -> None:
    """Test image_size property."""
    settings = Settings(
        server=ServerConfig(host="localhost", port=8000),
        logging=LoggingConfig(level="info"),
        model=ModelConfig(path="model.onnx"),
        filestore=FilestoreConfig(
            endpoint="localhost:9000",
            bucket="bucket",
            use_ssl=False,
        ),
    )
    assert settings.image_size == (256, 256)
