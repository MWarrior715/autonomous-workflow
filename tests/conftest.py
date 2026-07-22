"""Shared pytest fixtures."""

from __future__ import annotations

import pytest

from providers.llm import LLMProvider


@pytest.fixture
def fake_provider():
    """LLM provider that always returns predictable JSON."""

    class FakeProvider(LLMProvider):
        def __init__(self) -> None:
            super().__init__(
                base_url="http://fake",
                api_key="fake",
                model="fake",
                fallback_on_error=False,
            )

        def chat(self, system, user, temperature=0.3, json_mode=True) -> str:
            if "lead qualification analyst" in system.lower():
                return '{"score": 82, "justification": "Buen fit", "risks": ["Presupuesto ajustado"]}'
            return '{"subject": "Propuesta demo", "body": "Estimado demo,\\n\\nEsta es una propuesta.\\n\\nSaludos."}'

    return FakeProvider()


@pytest.fixture
def sample_lead():
    return {
        "name": "Test Lead",
        "company": "Acme Corp",
        "need": "Automatizar reportes",
        "budget": "$5k",
        "timeline": "2 semanas",
        "source": "test",
    }
