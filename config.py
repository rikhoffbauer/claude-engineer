from pathlib import Path
import os
from dotenv import load_dotenv
from typing import Dict, Any

load_dotenv()


class Config:
    # API Keys
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
    OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

    # Model Configuration
    MODEL_PROVIDER = os.getenv("MODEL_PROVIDER", "anthropic")
    SELECTED_MODEL = os.getenv("SELECTED_MODEL", "claude-3-5-sonnet-20241022")

    # OpenRouter Configuration
    OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"

    # Model Settings
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

    # Available Models
    AVAILABLE_MODELS: Dict[str, Dict[str, Any]] = {
        "anthropic": {
            "claude-3-opus-20240229": {"max_tokens": 8000},
            "claude-3-sonnet-20240229": {"max_tokens": 8000},
            "claude-3-haiku-20240229": {"max_tokens": 8000},
            "claude-2.1": {"max_tokens": 8000},
            "claude-instant-1.2": {"max_tokens": 8000},
        },
        "openrouter": {
            "anthropic/claude-3-opus-20240229": {"max_tokens": 8000},
            "anthropic/claude-3-sonnet-20240229": {"max_tokens": 8000},
            "anthropic/claude-3-haiku-20240229": {"max_tokens": 8000},
            "google/gemini-pro": {"max_tokens": 8000},
            "meta-llama/llama-2-70b-chat": {"max_tokens": 4096},
            "mistralai/mistral-7b": {"max_tokens": 4096},
        },
    }
