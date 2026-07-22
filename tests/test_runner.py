"""Tests for the workflow runner."""

from __future__ import annotations

from workflow.runner import run


def test_run_with_default_lead(fake_provider):
    result = run(provider=fake_provider)
    assert result["workflow"] == "Autonomous Workflow Agent"
    assert "lead" in result
    assert "classification" in result
    assert "proposal" in result
    assert result["classification"]["score"] == 82


def test_run_with_custom_lead(fake_provider, sample_lead):
    result = run(lead=sample_lead, provider=fake_provider)
    assert result["lead"]["company"] == "Acme Corp"
    assert result["proposal"]["subject"] == "Propuesta demo"
