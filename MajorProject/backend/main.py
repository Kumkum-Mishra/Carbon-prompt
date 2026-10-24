"""GreenPrompt AI backend application entry point."""

import uvicorn

from app import app
from config import HOST, PORT

__all__ = ["app"]

if __name__ == "__main__":
    uvicorn.run("app:app", host=HOST, port=PORT, reload=True)
