"""Configuration for the Autonomous Workflow Agent.

Values are loaded from environment variables (or a `.env` file) and exposed as
plain Python attributes so the rest of the codebase does not need to know about
pydantic/dotenv internals.
"""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

# Load `.env` if it exists next to this file.
load_dotenv(Path(__file__).with_name(".env"))


class Config:
    """Runtime configuration."""

    # Motor de IA Local/Cloud (API OpenAI-compatible)
    OPENAI_BASE_URL: str = os.getenv("OPENAI_BASE_URL", "http://localhost:11434/v1")
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "not-needed-for-local")
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "default-model")

    # Workflow defaults
    APP_NAME: str = "Autonomous Workflow Agent"
    APP_VERSION: str = "0.1.0"


settings = Config()
