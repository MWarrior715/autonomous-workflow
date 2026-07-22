"""OpenAI-compatible LLM provider with deterministic fallback.

This module keeps every LLM dependency in one place.  If the remote motor is not
available, the provider returns a predictable fallback response so the workflow
remains demoable without a running model.
"""

from __future__ import annotations

import json
import logging
from typing import Any

from openai import APIConnectionError, APITimeoutError, OpenAI

from config import settings

logger = logging.getLogger(__name__)


class LLMProvider:
    """Thin wrapper around an OpenAI-compatible chat completion endpoint."""

    def __init__(
        self,
        base_url: str | None = None,
        api_key: str | None = None,
        model: str | None = None,
        fallback_on_error: bool = True,
    ) -> None:
        self.base_url = base_url or settings.OPENAI_BASE_URL
        self.api_key = api_key or settings.OPENAI_API_KEY
        self.model = model or settings.OPENAI_MODEL
        self.fallback_on_error = fallback_on_error
        self._client: OpenAI | None = None

    @property
    def client(self) -> OpenAI:
        if self._client is None:
            self._client = OpenAI(
                base_url=self.base_url,
                api_key=self.api_key,
            )
        return self._client

    def chat(
        self,
        system: str,
        user: str,
        temperature: float = 0.3,
        json_mode: bool = True,
    ) -> str:
        """Send a chat request and return the raw text content.

        Args:
            system: System prompt.
            user: User prompt.
            temperature: Sampling temperature.
            json_mode: When True, the request asks for a JSON object.

        Returns:
            Raw model output, or a deterministic fallback string on failure.
        """
        extra: dict[str, Any] = {}
        if json_mode:
            extra["response_format"] = {"type": "json_object"}

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": user},
                ],
                temperature=temperature,
                **extra,
            )
            content = response.choices[0].message.content or ""
            logger.debug("LLM response received (%d chars)", len(content))
            return content.strip()
        except (APIConnectionError, APITimeoutError) as exc:
            logger.warning("LLM connection failed: %s. Using fallback.", exc)
            if self.fallback_on_error:
                return self._fallback_json(system, user)
            raise
        except Exception as exc:
            logger.warning("LLM request failed: %s. Using fallback.", exc)
            if self.fallback_on_error:
                return self._fallback_json(system, user)
            raise

    @staticmethod
    def _fallback_json(system: str, user: str) -> str:
        """Return a deterministic JSON object when the LLM is unreachable."""
        if "classifier" in system.lower() or "score" in user.lower():
            return json.dumps(
                {
                    "score": 75,
                    "justification": "Lead matches target profile but budget information is incomplete. Fallback score applied because the LLM motor is unavailable.",
                    "risks": ["LLM motor offline - using deterministic fallback", "Budget not confirmed"],
                }
            )
        return json.dumps(
            {
                "subject": "Propuesta personalizada - siguiente paso",
                "body": "Estimado/a cliente,\n\nGracias por compartir los detalles de su proyecto. Hemos evaluado su caso y nos encantaría agendar una llamada de 15 minutos para presentar una propuesta adaptada a sus necesidades.\n\nQuedo atento.\n\nSaludos cordiales,\nEquipo de Operaciones",
            }
        )

    def complete(
        self,
        system: str,
        user: str,
        temperature: float = 0.3,
        json_mode: bool = True,
    ) -> dict[str, Any]:
        """Convenience wrapper that parses the raw response as JSON."""
        raw = self.chat(system, user, temperature, json_mode)
        try:
            return json.loads(raw)
        except json.JSONDecodeError as exc:
            logger.warning("Failed to parse LLM JSON response: %s", exc)
            # Best-effort: try to extract a JSON object from the text.
            return self._extract_json(raw)

    @staticmethod
    def _extract_json(text: str) -> dict[str, Any]:
        start = text.find("{")
        end = text.rfind("}")
        if start != -1 and end != -1 and end > start:
            try:
                return json.loads(text[start : end + 1])
            except json.JSONDecodeError:
                pass
        return {"raw_response": text}


def get_provider() -> LLMProvider:
    """Factory function for the default provider."""
    return LLMProvider()
