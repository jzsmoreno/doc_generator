import os
import requests
import json
from typing import Dict, Any, Optional


class ClaudeClient:
    """Client for interacting with Claude API using environment variables."""

    def __init__(
        self,
        base_url: Optional[str] = None,
        auth_token: Optional[str] = None,
        model: Optional[str] = None,
    ):
        """
        Initialize Claude client with environment variables or explicit parameters.

        Args:
            base_url: Optional base URL override (defaults to ANTHROPIC_BASE_URL env var)
            auth_token: Optional auth token override (defaults to ANTHROPIC_AUTH_TOKEN env var)
            model: Optional model override (defaults to ANTHROPIC_MODEL env var)
        """
        self.base_url = base_url or os.getenv("ANTHROPIC_BASE_URL", "https://api.anthropic.com/v1")
        self.auth_token = (
            auth_token
            or os.getenv("ANTHROPIC_AUTH_TOKEN")
            or os.getenv("ANTHROPIC_API_KEY")
        )
        self.model = model or os.getenv("ANTHROPIC_MODEL", "claude-3-5-sonnet-20240620")

        if not self.auth_token:
            raise ValueError(
                "Anthropic API key is required. Set ANTHROPIC_API_KEY environment variable or use --api-key."
            )

        # Ensure base URL has proper format
        if not self.base_url.endswith("/"):
            self.base_url += "/"

        # Use x-api-key header for official Anthropic API; Bearer for custom proxies
        is_official_api = "api.anthropic.com" in self.base_url
        auth_header = (
            {"x-api-key": self.auth_token}
            if is_official_api
            else {"Authorization": f"Bearer {self.auth_token}"}
        )

        # Create a session for connection pooling
        self.session = requests.Session()
        self.session.headers.update(
            {
                **auth_header,
                "Content-Type": "application/json",
                "anthropic-version": "2023-06-01",
            }
        )

    def _convert_openai_to_claude_format(self, messages: list) -> Dict[str, Any]:
        """
        Convert OpenAI chat format to Claude's message format.

        Claude expects:
        - system prompt as separate parameter
        - user/assistant messages in conversation format
        """
        system_prompt = ""
        claude_messages = []

        for message in messages:
            role = message.get("role", "user")
            content = message.get("content", "")

            if role == "system":
                system_prompt = content
            else:
                claude_messages.append({"role": role, "content": content})

        return {
            "model": self.model,
            "messages": claude_messages,
            "max_tokens": 4096,
            "system": system_prompt if system_prompt else None,
        }

    def _convert_claude_to_openai_format(self, claude_response: Dict[str, Any]) -> Dict[str, Any]:
        """
        Convert Claude response format to OpenAI-compatible format.
        """
        content = claude_response.get("content", [])
        if isinstance(content, list) and len(content) > 0:
            text_content = content[0].get("text", "")
        else:
            text_content = str(content)

        return {"choices": [{"message": {"content": text_content}}]}

    def chat_completions_create(self, model: str, messages: list, **kwargs) -> Any:
        """
        Create a chat completion using Claude API, compatible with OpenAI format.

        Args:
            model: Model name (ignored, uses configured model)
            messages: List of messages in OpenAI format
            **kwargs: Additional parameters (ignored for compatibility)

        Returns:
            Mock response object with OpenAI-compatible structure
        """
        # Convert OpenAI format to Claude format
        claude_payload = self._convert_openai_to_claude_format(messages)

        # Make API request to Claude
        response = self.session.post(f"{self.base_url}messages", json=claude_payload)

        if response.status_code != 200:
            raise Exception(f"Claude API error: {response.status_code} - {response.text}")

        claude_data = response.json()

        # Convert Claude response to OpenAI format
        openai_response = self._convert_claude_to_openai_format(claude_data)

        # Create a mock completion object that mimics OpenAI's structure
        class MockCompletion:
            def __init__(self, response_data):
                self.choices = []

                for choice in response_data.get("choices", []):
                    message_data = choice.get("message", {})
                    message_obj = type(
                        "Message",
                        (),
                        {"content": message_data.get("content", ""), "role": "assistant"},
                    )()

                    choice_obj = type(
                        "Choice", (), {"message": message_obj, "finish_reason": "stop"}
                    )()
                    self.choices.append(choice_obj)

        return MockCompletion(openai_response)

    # Create the nested structure that the existing code expects
    @property
    def chat(self):
        """Return self to support client.chat.completions.create() pattern."""
        return self

    @property
    def completions(self):
        """Return self to support client.chat.completions.create() pattern."""
        return self

    def create(self, model: str, messages: list, **kwargs) -> Any:
        """Alias for chat_completions_create for direct compatibility."""
        return self.chat_completions_create(model, messages, **kwargs)


# Convenience function to create a Claude client from environment variables
def create_claude_client() -> ClaudeClient:
    """
    Create a Claude client using environment variables.

    Returns:
        ClaudeClient instance configured from environment variables
    """
    return ClaudeClient()
