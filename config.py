from pathlib import Path
import os
from dotenv import load_dotenv
from typing import Dict, Any

load_dotenv()


class OpenRouterConfig:
    BASE_URL = "https://openrouter.ai/api/v1"
    API_KEY = os.getenv("OPENROUTER_API_KEY")

    # Available models mapping
    AVAILABLE_MODELS = {
        "claude-3-opus": "anthropic/claude-3-opus-20240229",
        "claude-3-sonnet": "anthropic/claude-3-sonnet-20240229",
        "gpt-4": "openai/gpt-4-turbo-preview",
        "mistral": "mistralai/mistral-7b-instruct",
        # Add more models as needed
    }


class Config:
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
    MODEL_PROVIDER = os.getenv("MODEL_PROVIDER", "anthropic")
    SELECTED_MODEL = os.getenv("SELECTED_MODEL", "claude-3-sonnet-20240229")

    # OpenRouter configuration
    OPENROUTER = OpenRouterConfig()

    # Model configuration
    MODEL = (
        OPENROUTER.AVAILABLE_MODELS.get(SELECTED_MODEL, SELECTED_MODEL)
        if MODEL_PROVIDER == "openrouter"
        else SELECTED_MODEL
    )
    MAX_TOKENS = 8000
    MAX_CONVERSATION_TOKENS = 200000  # Maximum tokens per conversation

    # Paths
    BASE_DIR = Path(__file__).parent
    TOOLS_DIR = BASE_DIR / "tools"
    PROMPTS_DIR = BASE_DIR / "prompts"

    # Assistant Configuration
    ENABLE_THINKING = True
    SHOW_TOOL_USAGE = True
    DEFAULT_TEMPERATURE = 0.7
