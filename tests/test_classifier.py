"""Tests for the classifier agent."""

from __future__ import annotations

from agents.classifier import classify, _normalize


def test_classify_with_fake_provider(fake_provider, sample_lead):
    result = classify(sample_lead, fake_provider)
    assert result["score"] == 82
    assert result["justification"] == "Buen fit"
    assert result["risks"] == ["Presupuesto ajustado"]


def test_normalize_rejects_invalid_scores():
    assert _normalize({"score": 200, "justification": "x", "risks": ["r"]})["score"] == 100
    assert _normalize({"score": -10, "justification": "x", "risks": ["r"]})["score"] == 1
    assert _normalize({"score": "abc", "justification": "x", "risks": ["r"]})["score"] == 50
