"""Main module for trash scanner predictor."""

import uvicorn

from .app.app import app
from .config import settings


def main() -> None:
    try:
        uvicorn.run(app, host=settings.server.host, port=settings.server.port)
    except Exception as e:
        print(f"Error starting server: {e}")
        raise


if __name__ == "__main__":
    main()
