import aiohttp
import json
from typing import Dict, Any, List, Optional, Union
import logging


class OpenRouterClient:
    def __init__(self, api_key: str, base_url: str = "https://openrouter.ai/api/v1"):
        self.api_key = api_key
        self.base_url = base_url
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/rikhoffbauer/claude-engineer",  # Required by OpenRouter
        }

    async def create_chat_completion(
        self,
        model: str,
        messages: List[Dict[str, Any]],
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None,
        tools: Optional[List[Dict[str, Any]]] = None,
        tool_choice: Optional[Dict[str, str]] = None,
        cache_control: Optional[Dict[str, str]] = None,
    ) -> Dict[str, Any]:
        """
        Create a chat completion using OpenRouter API with optional prompt caching.

        Args:
            model: The model to use for completion
            messages: List of conversation messages
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature
            tools: List of available tools
            tool_choice: Tool choice configuration
            cache_control: Cache control settings for prompt caching
                         Example: {"type": "ephemeral"} or {"type": "persistent", "ttl": 3600}
        """
        payload = {
            "model": model,
            "messages": messages,
        }

        if max_tokens is not None:
            payload["max_tokens"] = max_tokens
        if temperature is not None:
            payload["temperature"] = temperature
        if tools is not None:
            payload["tools"] = tools
        if tool_choice is not None:
            payload["tool_choice"] = tool_choice
        if cache_control is not None:
            payload["cache_control"] = cache_control

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/chat/completions",
                    headers=self.headers,
                    json=payload,
                ) as response:
                    if response.status != 200:
                        error_text = await response.text()
                        raise Exception(f"OpenRouter API error: {error_text}")

                    response_data = await response.json()

                    # Add usage information similar to Anthropic's format
                    if "usage" not in response_data:
                        response_data["usage"] = {
                            "input_tokens": response_data.get("input_tokens", 0),
                            "output_tokens": response_data.get("output_tokens", 0),
                            "cache_creation_input_tokens": response_data.get(
                                "cache_creation_input_tokens", 0
                            ),
                            "cache_read_input_tokens": response_data.get(
                                "cache_read_input_tokens", 0
                            ),
                        }

                    return response_data

        except Exception as e:
            logging.error(f"Error in OpenRouter API call: {str(e)}")
            raise

    async def get_available_models(self) -> List[Dict[str, Any]]:
        """
        Get list of available models from OpenRouter.
        """
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.base_url}/models", headers=self.headers
                ) as response:
                    if response.status != 200:
                        error_text = await response.text()
                        raise Exception(f"OpenRouter API error: {error_text}")

                    return await response.json()
        except Exception as e:
            logging.error(f"Error fetching available models: {str(e)}")
            raise
