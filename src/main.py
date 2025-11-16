"""Main module for trash scanner predictor."""

import logging

import uvicorn

from .app.app import app
from .config import settings

logger = logging.getLogger(__name__)


def main() -> None:
    try:
        uvicorn.run(
            app,
            host=settings.server.host,
            port=settings.server.port,
            log_level=settings.logging.level.lower(),
        )
    except Exception as e:
        logger.error(f"Error starting server: {e}", exc_info=True)
        raise


if __name__ == "__main__":
    main()
