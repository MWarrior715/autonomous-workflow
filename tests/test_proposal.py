"""Tests for the proposal agent."""

from __future__ import annotations

from agents.proposal import generate_proposal, _normalize


def test_generate_proposal_with_fake_provider(fake_provider, sample_lead):
    qualification = {"score": 82, "justification": "Buen fit", "risks": ["Presupuesto ajustado"]}
    result = generate_proposal(sample_lead, qualification, fake_provider)
    assert result["subject"] == "Propuesta demo"
    assert "Estimado demo" in result["body"]


def test_normalize_defaults():
    result = _normalize({})
    assert result["subject"] == "Propuesta personalizada"
    assert "cliente" in result["body"]
