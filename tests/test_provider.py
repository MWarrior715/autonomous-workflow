"""Tests for the LLM provider."""

from __future__ import annotations

import json

from providers.llm import LLMProvider


def test_fallback_json_classifier():
    provider = LLMProvider(fallback_on_error=True)
    fallback = provider._fallback_json("You are a classifier", "score this lead")
    data = json.loads(fallback)
    assert 1 <= data["score"] <= 100
    assert isinstance(data["risks"], list)


def test_extract_json_finds_object():
    provider = LLMProvider(fallback_on_error=True)
    text = 'Here is the result:\n{"score": 90, "justification": "ok", "risks": []}\nThanks!'
    result = provider._extract_json(text)
    assert result["score"] == 90
